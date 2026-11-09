#!/usr/bin/env python3
"""A06_02_02 freeze-split common-stability audit."""

from __future__ import annotations

import argparse
import bisect
import csv
import datetime as dt
import glob
import hashlib
import json
import math
import os
import random
import socket
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import numpy as np
import torch
import torch.distributed as dist
import torch.nn.functional as F

RESEARCH_ROOT = Path("/data/250010109/Research_System")
MOE_ROOT = Path("/data/250010109/MoE_Router")
if str(MOE_ROOT) not in sys.path:
    sys.path.insert(0, str(MOE_ROOT))

from src.model.qwen3_moe.myqwen import MyQwen3ForCausalLM
from src.model.qwen3_moe.qwen3config import Qwen3Config


def now_slug() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str), encoding="utf-8")


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                fields.append(key)
                seen.add(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class PackedBinDataset:
    def __init__(self, root: Path, input_length: int = 256, span_length: int = 257):
        self.root = root
        self.input_length = input_length
        self.span_length = span_length
        self.dtype = np.uint32
        self.files = [Path(p) for p in sorted(glob.glob(str(root / "**/*.bin"), recursive=True))]
        if not self.files:
            raise FileNotFoundError(f"No .bin files under {root}")
        self.starts: list[int] = []
        self.offsets: list[tuple[int, int, Path]] = []
        total = 0
        for path in self.files:
            n = path.stat().st_size // np.dtype(self.dtype).itemsize
            if n <= 0:
                continue
            self.starts.append(total)
            self.offsets.append((total, total + n, path))
            total += n
        self.total_tokens = total
        self._mmap_cache: dict[Path, np.memmap] = {}

    def __len__(self) -> int:
        return max(0, self.total_tokens // self.span_length)

    def manifest_row(self, sample_index: int, split: str) -> dict[str, Any]:
        global_offset = sample_index * self.span_length
        file_idx = bisect.bisect_right(self.starts, global_offset) - 1
        start, _, path = self.offsets[file_idx]
        return {
            "dataset": "DCLM-bin",
            "split": split,
            "shard_path": str(path),
            "loader_sample_index": sample_index,
            "global_token_offset": global_offset,
            "start_token_offset": global_offset - start,
            "span_length": self.span_length,
            "input_token_start_delta": 0,
            "input_token_count": self.input_length,
            "target_token_start_delta": 1,
            "target_token_count": self.input_length,
            "sample_stride": self.span_length,
        }

    def _mmap(self, path: Path) -> np.memmap:
        mm = self._mmap_cache.get(path)
        if mm is None:
            mm = np.memmap(path, dtype=self.dtype, mode="r")
            self._mmap_cache[path] = mm
        return mm

    def get(self, sample_index: int) -> tuple[torch.Tensor, torch.Tensor]:
        start_global = sample_index * self.span_length
        remaining = self.span_length
        current = start_global
        parts = []
        while remaining > 0:
            file_idx = bisect.bisect_right(self.starts, current) - 1
            file_start, file_end, path = self.offsets[file_idx]
            local_start = current - file_start
            read_len = min(remaining, file_end - current)
            arr = self._mmap(path)[local_start : local_start + read_len].astype(np.int64)
            parts.append(torch.from_numpy(arr))
            remaining -= read_len
            current += read_len
        span = torch.cat(parts, dim=0).long()
        return span[: self.input_length], span[1 : self.input_length + 1]

    def batch(self, indices: list[int], device: torch.device) -> tuple[torch.Tensor, torch.Tensor]:
        xs, ys = [], []
        for idx in indices:
            x, y = self.get(idx)
            xs.append(x)
            ys.append(y)
        return torch.stack(xs).to(device), torch.stack(ys).to(device)


def setup_dist() -> tuple[int, int, int]:
    if "RANK" in os.environ and "WORLD_SIZE" in os.environ:
        # Replay work is seed-parallel and can leave one 4-GPU rank idle while
        # the other ranks stream all cross-checkpoint pairs. Keep the process
        # group timeout above the replay tail latency so completed results are
        # not marked failed by an idle-rank barrier timeout.
        dist.init_process_group(backend="nccl", timeout=dt.timedelta(minutes=60))
        rank = dist.get_rank()
        world = dist.get_world_size()
        local_rank = int(os.environ.get("LOCAL_RANK", rank))
        torch.cuda.set_device(local_rank)
        return rank, world, local_rank
    return 0, 1, 0


def barrier() -> None:
    if dist.is_available() and dist.is_initialized():
        dist.barrier()


def make_config(num_experts: int, args: argparse.Namespace) -> Qwen3Config:
    cfg = Qwen3Config(
        vocab_size=args.vocab_size,
        hidden_size=args.hidden_size,
        intermediate_size=args.hidden_size * 4,
        num_hidden_layers=args.num_layers,
        num_attention_heads=args.num_heads,
        num_key_value_heads=args.num_key_value_heads,
        head_dim=args.hidden_size // args.num_heads,
        max_position_embeddings=4096,
        attention_dropout=0.0,
        torch_dtype="float32",
        use_cache=False,
        tie_word_embeddings=True,
        moe_type="moe",
        num_experts=num_experts,
        num_experts_per_tok=1,
        norm_topk_prob=False,
        use_shared_expert=False,
        moe_intermediate_size=args.expert_hidden_dim,
        gating_reference="hidden_states",
        router_center_input=False,
        router_aux_gate=False,
        router_acp_transform=False,
        router_type="linear",
        lambda_lb=0.0,
        initializer_range=args.initializer_range,
    )
    cfg.pad_token_id = 0
    cfg.bos_token_id = 151643
    cfg.eos_token_id = 151645
    cfg.rope_scaling = {"rope_type": "linear", "factor": 1.0}
    return cfg


def make_model(num_experts: int, seed: int, args: argparse.Namespace, device: torch.device) -> MyQwen3ForCausalLM:
    torch.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)
    model = MyQwen3ForCausalLM(make_config(num_experts, args))
    model.to(device)
    model.train()
    return model


def iter_gate_modules(model: MyQwen3ForCausalLM):
    for layer_idx, layer in enumerate(model.model.layers):
        mlp = getattr(layer, "mlp", None)
        gate = getattr(mlp, "gate", None)
        if gate is not None:
            yield layer_idx, mlp, gate


class GateCapture:
    def __init__(self, model: MyQwen3ForCausalLM):
        self.records: dict[int, tuple[torch.Tensor, torch.Tensor]] = {}
        self.handles = []
        for layer_idx, _, gate in iter_gate_modules(model):
            self.handles.append(gate.register_forward_hook(self._hook(layer_idx)))

    def _hook(self, layer_idx: int):
        def hook(_module, inputs, output):
            self.records[layer_idx] = (inputs[0].detach(), output.detach())
        return hook

    def clear(self) -> None:
        self.records.clear()

    def close(self) -> None:
        for handle in self.handles:
            handle.remove()


def top_margin(x: torch.Tensor) -> torch.Tensor:
    vals = torch.topk(x, k=2, dim=-1).values
    return vals[..., 0] - vals[..., 1]


def load_metrics(routes: torch.Tensor, num_experts: int) -> dict[str, float]:
    counts = torch.bincount(routes.reshape(-1), minlength=num_experts).float()
    total = counts.sum().clamp_min(1.0)
    p = counts / total
    entropy = -(p[p > 0] * torch.log(p[p > 0])).sum() / math.log(num_experts)
    sorted_counts = torch.sort(counts).values
    n = float(num_experts)
    gini = (2 * torch.arange(1, num_experts + 1, device=counts.device).float() - n - 1)
    gini = (gini * sorted_counts).sum() / (n * sorted_counts.sum().clamp_min(1.0))
    return {
        "max_load": float(p.max().item()),
        "routing_entropy": float(entropy.item()),
        "active_experts": int((counts > 0).sum().item()),
        "active_experts_ratio": float((counts > 0).float().mean().item()),
        "gini_load": float(gini.item()),
    }


def audit_model(
    model: MyQwen3ForCausalLM,
    dataset: PackedBinDataset,
    sample_indices: list[int],
    args: argparse.Namespace,
    device: torch.device,
    model_seed: int,
    num_experts: int,
    step: int,
    collect_sample: bool = True,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[int, torch.Tensor]]:
    model.eval()
    cap = GateCapture(model)
    layers = [idx for idx, _, _ in iter_gate_modules(model)]
    if getattr(args, "audit_layers", None):
        keep_layers = set(args.audit_layers)
        layers = [idx for idx in layers if idx in keep_layers]
    sums = {l: torch.zeros(args.hidden_size, device=device) for l in layers}
    bucket_sums = {(l, b): torch.zeros(args.hidden_size, device=device) for l in layers for b in range(4)}
    counts = {l: 0 for l in layers}
    bucket_counts = {(l, b): 0 for l in layers for b in range(4)}
    sampled: dict[int, list[torch.Tensor]] = {l: [] for l in layers}
    sampled_count = {l: 0 for l in layers}
    max_sample = args.max_analyzed_tokens_per_layer

    with torch.no_grad():
        for start in range(0, len(sample_indices), args.audit_batch_size):
            batch_idx = sample_indices[start : start + args.audit_batch_size]
            x, _ = dataset.batch(batch_idx, device)
            bsz, seq_len = x.shape
            cap.clear()
            _ = model.model(input_ids=x, use_cache=False)
            pos = torch.arange(seq_len, device=device).repeat(bsz)
            for layer_idx, (h, _logits) in cap.records.items():
                if layer_idx not in sums:
                    continue
                hf = h.float()
                sums[layer_idx] += hf.sum(dim=0)
                counts[layer_idx] += hf.shape[0]
                if collect_sample and sampled_count[layer_idx] < max_sample:
                    take = min(max_sample - sampled_count[layer_idx], hf.shape[0])
                    sampled[layer_idx].append(hf[:take].cpu())
                    sampled_count[layer_idx] += take
                for bucket in range(4):
                    mask = (pos >= bucket * 64) & (pos < (bucket + 1) * 64)
                    if mask.any():
                        bucket_sums[(layer_idx, bucket)] += hf[mask].sum(dim=0)
                        bucket_counts[(layer_idx, bucket)] += int(mask.sum().item())

    c = {l: sums[l] / max(counts[l], 1) for l in layers}
    c_bucket = {
        (l, b): bucket_sums[(l, b)] / max(bucket_counts[(l, b)], 1)
        for l in layers
        for b in range(4)
    }
    sampled_h = {l: torch.cat(sampled[l], dim=0) if sampled[l] else torch.empty(0, args.hidden_size) for l in layers}

    route_rows: list[dict[str, Any]] = []
    bucket_rows: list[dict[str, Any]] = []
    acc = {
        l: {
            "residual_margin_sum": 0.0,
            "n": 0,
            "agree": 0,
            "raw_routes": [],
            "centered_routes": [],
            "max_recon_error": 0.0,
        }
        for l in layers
    }
    bacc = {
        (l, b): {"n": 0, "agree": 0, "raw_routes": [], "centered_routes": [], "residual_margin_sum": 0.0}
        for l in layers
        for b in range(4)
    }
    with torch.no_grad():
        for start in range(0, len(sample_indices), args.audit_batch_size):
            batch_idx = sample_indices[start : start + args.audit_batch_size]
            x, _ = dataset.batch(batch_idx, device)
            bsz, seq_len = x.shape
            cap.clear()
            _ = model.model(input_ids=x, use_cache=False)
            pos = torch.arange(seq_len, device=device).repeat(bsz)
            for layer_idx, mlp, gate in iter_gate_modules(model):
                if layer_idx not in c:
                    continue
                h, logits = cap.records[layer_idx]
                hf = h.float()
                w = gate.weight.detach().float()
                recon = hf @ w.t()
                err = (recon - logits.float()).abs().max().item()
                acc[layer_idx]["max_recon_error"] = max(acc[layer_idx]["max_recon_error"], err)
                raw_routes = torch.argmax(recon, dim=-1)
                centered_logits = (hf - c[layer_idx].view(1, -1)) @ w.t()
                centered_routes = torch.argmax(centered_logits, dim=-1)
                residual_margin = top_margin(centered_logits)
                common_logits = w @ c[layer_idx]
                common_winner = int(torch.argmax(common_logits).item())
                acc[layer_idx]["residual_margin_sum"] += float(residual_margin.sum().item())
                acc[layer_idx]["n"] += hf.shape[0]
                acc[layer_idx]["agree"] += int((raw_routes == common_winner).sum().item())
                acc[layer_idx]["raw_routes"].append(raw_routes.cpu())
                acc[layer_idx]["centered_routes"].append(centered_routes.cpu())
                for bucket in range(4):
                    mask = (pos >= bucket * 64) & (pos < (bucket + 1) * 64)
                    if mask.any():
                        hb = hf[mask]
                        cb = c_bucket[(layer_idx, bucket)]
                        logits_b = hb @ w.t()
                        centered_b = (hb - cb.view(1, -1)) @ w.t()
                        common_b = w @ cb
                        winner_b = int(torch.argmax(common_b).item())
                        bacc[(layer_idx, bucket)]["n"] += hb.shape[0]
                        bacc[(layer_idx, bucket)]["agree"] += int((torch.argmax(logits_b, dim=-1) == winner_b).sum().item())
                        bacc[(layer_idx, bucket)]["residual_margin_sum"] += float(top_margin(centered_b).sum().item())
                        bacc[(layer_idx, bucket)]["raw_routes"].append(torch.argmax(logits_b, dim=-1).cpu())
                        bacc[(layer_idx, bucket)]["centered_routes"].append(torch.argmax(centered_b, dim=-1).cpu())
    cap.close()

    for layer_idx, _, gate in iter_gate_modules(model):
        if layer_idx not in c:
            continue
        w = gate.weight.detach().float()
        common_logits = w @ c[layer_idx]
        common_margin = float(top_margin(common_logits.view(1, -1)).item())
        raw_routes = torch.cat(acc[layer_idx]["raw_routes"])
        centered_routes = torch.cat(acc[layer_idx]["centered_routes"])
        raw_m = load_metrics(raw_routes, num_experts)
        centered_m = load_metrics(centered_routes, num_experts)
        residual_margin = acc[layer_idx]["residual_margin_sum"] / max(acc[layer_idx]["n"], 1)
        row = {
            "model_seed": model_seed,
            "num_experts": num_experts,
            "step": step,
            "layer": layer_idx,
            "token_count": acc[layer_idx]["n"],
            "common_margin": common_margin,
            "residual_margin": residual_margin,
            "dominance_ratio": common_margin / max(residual_margin, 1e-8),
            "common_winner_agreement": acc[layer_idx]["agree"] / max(acc[layer_idx]["n"], 1),
            "gate_weight_std": float(w.std().item()),
            "gate_reconstruction_max_error": acc[layer_idx]["max_recon_error"],
        }
        row.update({f"raw_{k}": v for k, v in raw_m.items()})
        row.update({f"centered_{k}": v for k, v in centered_m.items()})
        row["delta_max_load"] = row["raw_max_load"] - row["centered_max_load"]
        row["delta_active_experts"] = row["centered_active_experts"] - row["raw_active_experts"]
        route_rows.append(row)
        for bucket in range(4):
            raw_b = torch.cat(bacc[(layer_idx, bucket)]["raw_routes"])
            centered_b = torch.cat(bacc[(layer_idx, bucket)]["centered_routes"])
            cb = c_bucket[(layer_idx, bucket)]
            common_b = w @ cb
            cm_b = float(top_margin(common_b.view(1, -1)).item())
            rm_b = bacc[(layer_idx, bucket)]["residual_margin_sum"] / max(bacc[(layer_idx, bucket)]["n"], 1)
            brow = {
                "model_seed": model_seed,
                "num_experts": num_experts,
                "step": step,
                "layer": layer_idx,
                "bucket": bucket,
                "position_start": bucket * 64,
                "position_end": (bucket + 1) * 64 - 1,
                "token_count": bacc[(layer_idx, bucket)]["n"],
                "common_margin": cm_b,
                "residual_margin": rm_b,
                "dominance_ratio": cm_b / max(rm_b, 1e-8),
                "common_winner_agreement": bacc[(layer_idx, bucket)]["agree"] / max(bacc[(layer_idx, bucket)]["n"], 1),
            }
            brow.update({f"raw_{k}": v for k, v in load_metrics(raw_b, num_experts).items()})
            brow.update({f"centered_{k}": v for k, v in load_metrics(centered_b, num_experts).items()})
            bucket_rows.append(brow)
    model.train()
    return route_rows, bucket_rows, sampled_h


def virtual_scaling_rows(
    sampled_h: dict[int, torch.Tensor],
    phase1_rows: list[dict[str, Any]],
    args: argparse.Namespace,
    model_seed: int,
    device: torch.device,
) -> list[dict[str, Any]]:
    by_layer = {int(r["layer"]): r for r in phase1_rows if int(r["model_seed"]) == model_seed and int(r["step"]) == 0}
    out: list[dict[str, Any]] = []
    for layer, h_cpu in sampled_h.items():
        if h_cpu.numel() == 0:
            continue
        h = h_cpu.to(device=device, dtype=torch.float32)
        c = h.mean(dim=0, keepdim=True)
        centered = h - c
        d = h.shape[1]
        scales = {"protocol": 1.0 / math.sqrt(d)}
        if layer in by_layer:
            scales["matched_real_gate"] = float(by_layer[layer]["gate_weight_std"])
        for scale_name, scale in scales.items():
            for e in args.virtual_expert_counts:
                for vseed in range(args.virtual_router_seeds):
                    gen = torch.Generator(device=device).manual_seed(10_000_000 + model_seed * 100_000 + layer * 1000 + e * 67 + vseed)
                    w = torch.randn(e, d, generator=gen, device=device) * scale
                    common_logits = (w @ c.squeeze(0))
                    common_margin = float(top_margin(common_logits.view(1, -1)).item())
                    raw_routes_all = []
                    centered_routes_all = []
                    residual_sum = 0.0
                    agree = 0
                    n = 0
                    winner = int(torch.argmax(common_logits).item())
                    for start in range(0, h.shape[0], args.virtual_chunk_tokens):
                        hb = h[start : start + args.virtual_chunk_tokens]
                        cb = centered[start : start + args.virtual_chunk_tokens]
                        logits = hb @ w.t()
                        clogits = cb @ w.t()
                        raw_routes = torch.argmax(logits, dim=-1)
                        centered_routes = torch.argmax(clogits, dim=-1)
                        raw_routes_all.append(raw_routes)
                        centered_routes_all.append(centered_routes)
                        residual_sum += float(top_margin(clogits).sum().item())
                        agree += int((raw_routes == winner).sum().item())
                        n += hb.shape[0]
                    raw = torch.cat(raw_routes_all)
                    cent = torch.cat(centered_routes_all)
                    row = {
                        "model_seed": model_seed,
                        "layer": layer,
                        "E_virtual": e,
                        "virtual_router_seed": vseed,
                        "scale_name": scale_name,
                        "weight_std": scale,
                        "sampled_tokens": n,
                        "common_margin": common_margin,
                        "residual_margin": residual_sum / max(n, 1),
                        "dominance_ratio": common_margin / max(residual_sum / max(n, 1), 1e-8),
                        "common_winner_agreement": agree / max(n, 1),
                    }
                    row.update({f"raw_{k}": v for k, v in load_metrics(raw, e).items()})
                    row.update({f"centered_{k}": v for k, v in load_metrics(cent, e).items()})
                    out.append(row)
        del h
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    return out


def counts_to_metrics(counts: torch.Tensor) -> dict[str, float]:
    counts = counts.float()
    total = counts.sum().clamp_min(1.0)
    p = counts / total
    n_experts = counts.numel()
    entropy = -(p[p > 0] * torch.log(p[p > 0])).sum() / math.log(max(n_experts, 2))
    sorted_counts = torch.sort(counts).values
    n = float(n_experts)
    gini_weights = 2 * torch.arange(1, n_experts + 1, device=counts.device).float() - n - 1
    gini = (gini_weights * sorted_counts).sum() / (n * sorted_counts.sum().clamp_min(1.0))
    return {
        "max_load": float(p.max().item()),
        "routing_entropy": float(entropy.item()),
        "effective_experts": float(torch.exp(-(p[p > 0] * torch.log(p[p > 0])).sum()).item()),
        "active_experts": int((counts > 0).sum().item()),
        "active_experts_ratio": float((counts > 0).float().mean().item()),
        "gini_load": float(gini.item()),
    }


def selected_layers(model: MyQwen3ForCausalLM, args: argparse.Namespace) -> list[int]:
    available = [idx for idx, _, _ in iter_gate_modules(model)]
    if args.audit_layers:
        keep = set(args.audit_layers)
        return [idx for idx in available if idx in keep]
    return available


def gate_weight_snapshot(model: MyQwen3ForCausalLM, args: argparse.Namespace) -> dict[int, torch.Tensor]:
    layers = set(selected_layers(model, args))
    out = {}
    for layer_idx, _, gate in iter_gate_modules(model):
        if layer_idx in layers:
            out[layer_idx] = gate.weight.detach().cpu().float().clone()
    return out


def grad_group_norm(model: MyQwen3ForCausalLM) -> dict[str, float]:
    router_sq = 0.0
    expert_sq = 0.0
    other_sq = 0.0
    for name, p in model.named_parameters():
        if p.grad is None:
            continue
        val = float(p.grad.detach().float().pow(2).sum().item())
        if ".mlp.gate." in name:
            router_sq += val
        elif ".mlp.experts." in name or ".mlp.shared_expert." in name:
            expert_sq += val
        else:
            other_sq += val
    return {
        "router_grad_norm": math.sqrt(router_sq),
        "expert_grad_norm": math.sqrt(expert_sq),
        "other_grad_norm": math.sqrt(other_sq),
    }


def _freeze_module(module: torch.nn.Module, prefix: str, info: dict[str, Any]) -> None:
    for p in module.parameters():
        p.requires_grad_(False)
    info["frozen_prefixes"].append(prefix)


def apply_variant_freeze(model: MyQwen3ForCausalLM, variant: str, args: argparse.Namespace) -> dict[str, Any]:
    for p in model.parameters():
        p.requires_grad_(True)
    info: dict[str, Any] = {"variant": variant, "frozen_prefixes": [], "trainable_prefixes": []}
    if variant == "normal":
        return info
    if variant in {"freeze_gate", "freeze_gate_all"}:
        for layer_idx, _, gate in iter_gate_modules(model):
            for p in gate.parameters():
                p.requires_grad_(False)
        info["frozen_prefixes"].append("all MoE gate weights fixed at initialization W0")
        return info
    if variant in {"freeze_experts", "freeze_experts_all"}:
        for _layer_idx, mlp, _gate in iter_gate_modules(model):
            for name, p in mlp.named_parameters():
                if not name.startswith("gate."):
                    p.requires_grad_(False)
        info["frozen_prefixes"].append("all expert MLP parameters; use_shared_expert=false")
        info["trainable_prefixes"].append("all MoE gate weights")
        return info
    if variant == "freeze_gate_and_experts":
        for _layer_idx, mlp, _gate in iter_gate_modules(model):
            for p in mlp.parameters():
                p.requires_grad_(False)
        info["frozen_prefixes"].append("all MoE gate weights and all expert MLP parameters; use_shared_expert=false")
        info["trainable_prefixes"].append("attention, layernorms, embeddings, final norm, lm_head")
        return info
    if variant == "freeze_last_layer_hidden_producer":
        final_layer_idx = args.num_layers - 1
        _freeze_module(model.model.embed_tokens, "model.model.embed_tokens", info)
        for layer_idx, layer in enumerate(model.model.layers):
            if layer_idx < final_layer_idx:
                _freeze_module(layer, f"model.model.layers.{layer_idx}", info)
            elif layer_idx == final_layer_idx:
                for module_name in ["input_layernorm", "self_attn", "post_attention_layernorm"]:
                    _freeze_module(getattr(layer, module_name), f"model.model.layers.{layer_idx}.{module_name}", info)
                info["trainable_prefixes"].append(f"model.model.layers.{layer_idx}.mlp")
        info["trainable_prefixes"].extend(["model.model.norm", "lm_head"])
        return info
    if variant in {"freeze_prefix_before_layer3", "freeze_prefix_before_layer4", "freeze_prefix_before_layer5"}:
        target_layer = int(variant.rsplit("layer", 1)[1])
        _freeze_module(model.model.embed_tokens, "model.model.embed_tokens", info)
        for layer_idx, layer in enumerate(model.model.layers):
            if layer_idx < target_layer:
                _freeze_module(layer, f"model.model.layers.{layer_idx}", info)
            elif layer_idx == target_layer and target_layer == args.num_layers - 1:
                # This condition intentionally matches the previous
                # final-layer-hidden-producer freeze: every module that can
                # alter the final layer's gate input is fixed, while the final
                # MoE gate/expert path remains trainable.
                for module_name in ["input_layernorm", "self_attn", "post_attention_layernorm"]:
                    _freeze_module(getattr(layer, module_name), f"model.model.layers.{layer_idx}.{module_name}", info)
        info["trainable_prefixes"].append(f"model.model.layers.{target_layer} and later, except frozen pre-gate path above")
        info["target_layer"] = target_layer
        return info
    raise ValueError(f"Unknown variant: {variant}")


def save_checkpoint(
    model: MyQwen3ForCausalLM,
    ckpt_dir: Path,
    variant: str,
    seed: int,
    step: int,
    args: argparse.Namespace,
) -> tuple[Path, Path]:
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    model_path = ckpt_dir / f"{variant}_seed{seed}_step{step}.pt"
    gate_path = ckpt_dir / f"{variant}_seed{seed}_step{step}_gates.pt"
    torch.save({"model_state_dict": model.state_dict(), "variant": variant, "seed": seed, "step": step}, model_path)
    torch.save(gate_weight_snapshot(model, args), gate_path)
    return model_path, gate_path


def train_variant(
    variant: str,
    seed: int,
    dataset: PackedBinDataset,
    audit_indices: list[int],
    train_indices: list[int],
    args: argparse.Namespace,
    device: torch.device,
    run_dir: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    model = make_model(args.num_experts, seed, args, device)
    freeze_info = apply_variant_freeze(model, variant, args)
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=args.learning_rate, weight_decay=0.0)
    rows: list[dict[str, Any]] = []
    grad_rows: list[dict[str, Any]] = []
    ckpt_rows: list[dict[str, Any]] = []
    last_loss = None
    ckpts = set(args.checkpoints)
    train_ptr = 0
    if variant != "normal":
        write_json(run_dir / f"config/freeze_{variant}_seed{seed}.json", freeze_info)
    for step in range(0, args.max_train_steps + 1):
        if step in ckpts:
            r, _, _ = audit_model(
                model,
                dataset,
                audit_indices[: args.trajectory_audit_num_sequences],
                args,
                device,
                seed,
                args.num_experts,
                step,
                collect_sample=False,
            )
            model_path, gate_path = save_checkpoint(model, run_dir / "checkpoints", variant, seed, step, args)
            for row in r:
                row["variant"] = variant
                row["lm_loss"] = last_loss
                rows.append(row)
            ckpt_rows.append(
                {
                    "variant": variant,
                    "model_seed": seed,
                    "step": step,
                    "model_checkpoint": str(model_path.relative_to(run_dir)),
                    "gate_checkpoint": str(gate_path.relative_to(run_dir)),
                    "lm_loss": last_loss,
                }
            )
        if step == args.max_train_steps:
            break
        model.train()
        if train_ptr + args.train_batch_size > len(train_indices):
            rng = random.Random(seed + step)
            rng.shuffle(train_indices)
            train_ptr = 0
        batch_idx = train_indices[train_ptr : train_ptr + args.train_batch_size]
        train_ptr += args.train_batch_size
        x, y = dataset.batch(batch_idx, device)
        opt.zero_grad(set_to_none=True)
        out = model(input_ids=x, use_cache=False)
        loss = F.cross_entropy(out.logits.reshape(-1, out.logits.shape[-1]), y.reshape(-1))
        loss.backward()
        norms = grad_group_norm(model)
        if step + 1 in ckpts or step < args.gradient_log_first_steps:
            grad_rows.append({"variant": variant, "model_seed": seed, "after_backward_step": step, **norms})
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        last_loss = float(loss.detach().item())
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return rows, grad_rows, ckpt_rows


def compute_c_for_checkpoint(
    model: MyQwen3ForCausalLM,
    dataset: PackedBinDataset,
    audit_indices: list[int],
    args: argparse.Namespace,
    device: torch.device,
) -> tuple[dict[int, torch.Tensor], dict[int, int]]:
    model.eval()
    cap = GateCapture(model)
    layers = selected_layers(model, args)
    sums = {l: torch.zeros(args.hidden_size, device=device) for l in layers}
    counts = {l: 0 for l in layers}
    with torch.no_grad():
        for start in range(0, len(audit_indices), args.audit_batch_size):
            batch_idx = audit_indices[start : start + args.audit_batch_size]
            x, _ = dataset.batch(batch_idx, device)
            cap.clear()
            _ = model.model(input_ids=x, use_cache=False)
            for layer_idx, (h, _logits) in cap.records.items():
                if layer_idx not in sums:
                    continue
                hf = h.detach().float()
                sums[layer_idx] += hf.sum(dim=0)
                counts[layer_idx] += hf.shape[0]
    cap.close()
    return {l: sums[l] / max(counts[l], 1) for l in layers}, counts


def replay_metrics_for_seed(
    variant: str,
    seed: int,
    dataset: PackedBinDataset,
    audit_indices: list[int],
    args: argparse.Namespace,
    device: torch.device,
    run_dir: Path,
) -> list[dict[str, Any]]:
    ckpt_dir = run_dir / "checkpoints"
    model = make_model(args.num_experts, seed, args, device)
    gate_by_step: dict[int, dict[int, torch.Tensor]] = {}
    for step in args.checkpoints:
        gate_path = ckpt_dir / f"{variant}_seed{seed}_step{step}_gates.pt"
        gate_by_step[step] = torch.load(gate_path, map_location="cpu")
    rows: list[dict[str, Any]] = []
    for b_step in args.checkpoints:
        model_path = ckpt_dir / f"{variant}_seed{seed}_step{b_step}.pt"
        state = torch.load(model_path, map_location=device)
        model.load_state_dict(state["model_state_dict"])
        model.eval()
        c_by_layer, n_by_layer = compute_c_for_checkpoint(model, dataset, audit_indices, args, device)
        cap = GateCapture(model)
        acc: dict[tuple[int, int], dict[str, Any]] = {}
        for a_step in args.checkpoints:
            for layer in c_by_layer:
                acc[(a_step, layer)] = {
                    "raw_counts": torch.zeros(args.num_experts),
                    "centered_counts": torch.zeros(args.num_experts),
                    "residual_margin_sum": 0.0,
                    "n": 0,
                    "agree": 0,
                    "max_recon_error": 0.0,
                }
        with torch.no_grad():
            for start in range(0, len(audit_indices), args.audit_batch_size):
                batch_idx = audit_indices[start : start + args.audit_batch_size]
                x, _ = dataset.batch(batch_idx, device)
                cap.clear()
                _ = model.model(input_ids=x, use_cache=False)
                for layer_idx, (h, logged_logits) in cap.records.items():
                    if layer_idx not in c_by_layer:
                        continue
                    hf = h.detach().float()
                    cb = c_by_layer[layer_idx].view(1, -1)
                    centered = hf - cb
                    for a_step, gate_layers in gate_by_step.items():
                        w = gate_layers[layer_idx].to(device=device, dtype=torch.float32)
                        logits = hf @ w.t()
                        centered_logits = centered @ w.t()
                        raw_routes = torch.argmax(logits, dim=-1)
                        centered_routes = torch.argmax(centered_logits, dim=-1)
                        common_logits = w @ c_by_layer[layer_idx]
                        common_winner = int(torch.argmax(common_logits).item())
                        key = (a_step, layer_idx)
                        acc[key]["raw_counts"] += torch.bincount(raw_routes.cpu(), minlength=args.num_experts).float()
                        acc[key]["centered_counts"] += torch.bincount(centered_routes.cpu(), minlength=args.num_experts).float()
                        acc[key]["residual_margin_sum"] += float(top_margin(centered_logits).sum().item())
                        acc[key]["n"] += hf.shape[0]
                        acc[key]["agree"] += int((raw_routes == common_winner).sum().item())
                        if a_step == b_step:
                            err = (logits - logged_logits.float()).abs().max().item()
                            acc[key]["max_recon_error"] = max(acc[key]["max_recon_error"], err)
        cap.close()
        for a_step in args.checkpoints:
            for layer_idx, c in c_by_layer.items():
                w = gate_by_step[a_step][layer_idx].to(device=device, dtype=torch.float32)
                common_logits = w @ c
                common_margin = float(top_margin(common_logits.view(1, -1)).item())
                key = (a_step, layer_idx)
                n = max(acc[key]["n"], 1)
                residual_margin = acc[key]["residual_margin_sum"] / n
                raw_m = counts_to_metrics(acc[key]["raw_counts"])
                centered_m = counts_to_metrics(acc[key]["centered_counts"])
                row = {
                    "variant": variant,
                    "model_seed": seed,
                    "replay_a_step": a_step,
                    "replay_b_step": b_step,
                    "layer": layer_idx,
                    "token_count": n,
                    "hidden_checkpoint_token_count": n_by_layer[layer_idx],
                    "common_margin": common_margin,
                    "residual_margin": residual_margin,
                    "dominance_ratio": common_margin / max(residual_margin, 1e-8),
                    "log_dominance_ratio": math.log(common_margin + 1e-8) - math.log(residual_margin + 1e-8),
                    "common_winner_agreement": acc[key]["agree"] / n,
                    "gate_reconstruction_max_error": acc[key]["max_recon_error"] if a_step == b_step else None,
                }
                row.update({f"raw_{k}": v for k, v in raw_m.items()})
                row.update({f"centered_{k}": v for k, v in centered_m.items()})
                row["delta_max_load"] = row["raw_max_load"] - row["centered_max_load"]
                rows.append(row)
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    del model
    return rows


def replay_fraction_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key = {
        (
            str(r["variant"]),
            int(r["model_seed"]),
            int(r["layer"]),
            int(r["replay_a_step"]),
            int(r["replay_b_step"]),
        ): r
        for r in rows
    }
    out = []
    for variant in sorted({str(r["variant"]) for r in rows}):
        for seed in sorted({int(r["model_seed"]) for r in rows if str(r["variant"]) == variant}):
            for layer in sorted({int(r["layer"]) for r in rows if str(r["variant"]) == variant and int(r["model_seed"]) == seed}):
                needed = [(0, 0), (10, 10), (10, 0), (0, 10)]
                if any((variant, seed, layer, a, b) not in by_key for a, b in needed):
                    continue
                m00 = float(by_key[(variant, seed, layer, 0, 0)]["common_margin"])
                m1010 = float(by_key[(variant, seed, layer, 10, 10)]["common_margin"])
                m100 = float(by_key[(variant, seed, layer, 10, 0)]["common_margin"])
                m010 = float(by_key[(variant, seed, layer, 0, 10)]["common_margin"])
                actual = m1010 - m00
                gate = m100 - m00
                hidden = m010 - m00
                interaction = actual - gate - hidden
                denom = actual if abs(actual) > 1e-8 else float("nan")
                out.append(
                    {
                        "variant": variant,
                        "model_seed": seed,
                        "layer": layer,
                        "common_margin_00": m00,
                        "common_margin_1010": m1010,
                        "A_actual": actual,
                        "A_gate": gate,
                        "A_hidden": hidden,
                        "A_interaction": interaction,
                        "F_gate": gate / denom if denom == denom else None,
                        "F_hidden": hidden / denom if denom == denom else None,
                        "F_interaction": interaction / denom if denom == denom else None,
                    }
                )
    return out


def make_figures(run_dir: Path) -> None:
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
    except Exception:
        return
    fig_dir = run_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    traj_path = run_dir / "results/trajectory_metrics.csv"
    if traj_path.exists() and traj_path.stat().st_size > 0:
        df = pd.read_csv(traj_path)
        for variant in df["variant"].unique():
            sub = df[df["variant"] == variant].groupby("step")[["common_margin", "raw_max_load", "centered_max_load"]].mean().reset_index()
            plt.figure(figsize=(7, 4))
            plt.plot(sub["step"], sub["common_margin"], marker="o", label="common_margin")
            plt.legend()
            plt.tight_layout()
            plt.savefig(fig_dir / f"trajectory_common_margin_{variant}.png", dpi=160)
            plt.close()
            plt.figure(figsize=(7, 4))
            plt.plot(sub["step"], sub["raw_max_load"], marker="o", label="raw")
            plt.plot(sub["step"], sub["centered_max_load"], marker="o", label="centered")
            plt.legend()
            plt.tight_layout()
            plt.savefig(fig_dir / f"trajectory_max_load_{variant}.png", dpi=160)
            plt.close()
    replay_path = run_dir / "results/replay_metrics.csv"
    if replay_path.exists() and replay_path.stat().st_size > 0:
        df = pd.read_csv(replay_path)
        for variant in df["variant"].unique():
            vdf = df[df["variant"] == variant]
            for metric in ["common_margin", "raw_max_load"]:
                pivot = vdf.groupby(["replay_b_step", "replay_a_step"])[metric].mean().reset_index()
                mat = pivot.pivot(index="replay_b_step", columns="replay_a_step", values=metric).sort_index().sort_index(axis=1)
                plt.figure(figsize=(7, 5))
                plt.imshow(mat.values, aspect="auto", origin="lower")
                plt.xticks(range(len(mat.columns)), mat.columns, rotation=45)
                plt.yticks(range(len(mat.index)), mat.index)
                plt.xlabel("gate checkpoint a")
                plt.ylabel("hidden checkpoint b")
                plt.colorbar(label=metric)
                plt.tight_layout()
                plt.savefig(fig_dir / f"replay_heatmap_{metric}_{variant}.png", dpi=160)
                plt.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-name", default=f"freeze_split_common_stability_{now_slug()}")
    parser.add_argument("--output-dir", type=Path, default=RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_01_E03_freeze_split_common_stability")
    parser.add_argument("--data-path", type=Path, default=Path("/data/share/109_cache_dir/hf_data/dclm_bin"))
    parser.add_argument("--hidden-size", type=int, default=512)
    parser.add_argument("--num-layers", type=int, default=6)
    parser.add_argument("--num-heads", type=int, default=8)
    parser.add_argument("--num-key-value-heads", type=int, default=4)
    parser.add_argument("--expert-hidden-dim", type=int, default=2048)
    parser.add_argument("--num-experts", type=int, default=8)
    parser.add_argument("--vocab-size", type=int, default=151936)
    parser.add_argument("--initializer-range", type=float, default=0.02)
    parser.add_argument("--audit-num-sequences", type=int, default=8192)
    parser.add_argument("--trajectory-audit-num-sequences", type=int, default=8192)
    parser.add_argument("--train-num-sequences", type=int, default=32768)
    parser.add_argument("--audit-batch-size", type=int, default=8)
    parser.add_argument("--train-batch-size", type=int, default=2)
    parser.add_argument("--max-analyzed-tokens-per-layer", type=int, default=1024)
    parser.add_argument("--model-seeds", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument(
        "--variants",
        nargs="+",
        default=[
            "normal",
            "freeze_gate_all",
            "freeze_experts_all",
            "freeze_gate_and_experts",
            "freeze_prefix_before_layer3",
            "freeze_prefix_before_layer4",
            "freeze_prefix_before_layer5",
        ],
    )
    parser.add_argument("--audit-layers", type=int, nargs="*", default=None)
    parser.add_argument("--max-train-steps", type=int, default=300)
    parser.add_argument("--checkpoints", type=int, nargs="+", default=[0, 1, 2, 3, 5, 10, 20, 50, 100, 200, 300])
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--gradient-log-first-steps", type=int, default=5)
    args = parser.parse_args()

    rank, world, local_rank = setup_dist()
    device = torch.device(f"cuda:{local_rank}" if torch.cuda.is_available() else "cpu")
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

    run_dir = args.output_dir / "runs/freeze_split_common_stability" / args.run_name
    partial_dir = run_dir / "partials"
    for d in ["config", "logs", "results", "figures", "notes", "partials", "checkpoints"]:
        (run_dir / d).mkdir(parents=True, exist_ok=True)

    if rank == 0:
        write_json(run_dir / "config/run_config.json", vars(args))
        write_json(
            run_dir / "config/source_manifest.json",
            {
                "timestamp": dt.datetime.now().isoformat(),
                "machine": socket.gethostname(),
                "moe_root": str(MOE_ROOT),
                "runner": str(Path(__file__).resolve()),
                "runner_sha256": sha256_file(Path(__file__).resolve()),
                "model_files": {
                    "myqwen.py": sha256_file(MOE_ROOT / "src/model/qwen3_moe/myqwen.py"),
                    "qwen3config.py": sha256_file(MOE_ROOT / "src/model/qwen3_moe/qwen3config.py"),
                    "train_qwen3_moe.py": sha256_file(MOE_ROOT / "train_qwen3_moe.py"),
                },
                "data_path": str(args.data_path),
            },
        )
    barrier()

    dataset = PackedBinDataset(args.data_path)
    audit_indices = list(range(args.audit_num_sequences))
    train_indices_base = list(range(args.audit_num_sequences, args.audit_num_sequences + args.train_num_sequences))
    if rank == 0:
        append_jsonl(run_dir / "config/audit_manifest_preview.jsonl", [dataset.manifest_row(i, "audit") for i in audit_indices[:64]])
        append_jsonl(run_dir / "config/train_manifest_preview.jsonl", [dataset.manifest_row(i, "train") for i in train_indices_base[:64]])
    barrier()

    tasks = [(variant, seed) for variant in args.variants for seed in args.model_seeds]
    for task_idx, (variant, seed) in enumerate(tasks):
        if task_idx % world != rank:
            continue
        print(f"[rank{rank}] train start variant={variant} seed={seed}", flush=True)
        train_indices = train_indices_base[:]
        random.Random(seed + 17).shuffle(train_indices)
        traj, grads, ckpts = train_variant(variant, seed, dataset, audit_indices, train_indices, args, device, run_dir)
        append_jsonl(partial_dir / f"trajectory_rank{rank}.jsonl", traj)
        append_jsonl(partial_dir / f"gradients_rank{rank}.jsonl", grads)
        append_jsonl(partial_dir / f"checkpoints_rank{rank}.jsonl", ckpts)
        print(f"[rank{rank}] train done variant={variant} seed={seed} trajectory_rows={len(traj)}", flush=True)
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    barrier()

    replay_tasks = [(variant, seed) for variant in args.variants for seed in args.model_seeds]
    for task_idx, (variant, seed) in enumerate(replay_tasks):
        if task_idx % world != rank:
            continue
        print(f"[rank{rank}] replay start variant={variant} seed={seed}", flush=True)
        rows = replay_metrics_for_seed(variant, seed, dataset, audit_indices, args, device, run_dir)
        append_jsonl(partial_dir / f"replay_rank{rank}.jsonl", rows)
        print(f"[rank{rank}] replay done variant={variant} seed={seed} rows={len(rows)}", flush=True)
    barrier()

    if rank == 0:
        traj = []
        grads = []
        ckpts = []
        replay = []
        for p in sorted(partial_dir.glob("phase1_rank*.jsonl")):
            pass
        for p in sorted(partial_dir.glob("trajectory_rank*.jsonl")):
            traj.extend(read_jsonl(p))
        for p in sorted(partial_dir.glob("gradients_rank*.jsonl")):
            grads.extend(read_jsonl(p))
        for p in sorted(partial_dir.glob("checkpoints_rank*.jsonl")):
            ckpts.extend(read_jsonl(p))
        for p in sorted(partial_dir.glob("replay_rank*.jsonl")):
            replay.extend(read_jsonl(p))
        fractions = replay_fraction_summary(replay)
        write_csv(run_dir / "results/trajectory_metrics.csv", traj)
        write_csv(run_dir / "results/gradient_metrics.csv", grads)
        write_csv(run_dir / "results/checkpoint_manifest.csv", ckpts)
        write_csv(run_dir / "results/replay_metrics.csv", replay)
        write_csv(run_dir / "results/replay_fraction_summary.csv", fractions)
        write_json(
            run_dir / "run_summary.json",
            {
                "run_name": args.run_name,
                "trajectory_rows": len(traj),
                "gradient_rows": len(grads),
                "checkpoint_rows": len(ckpts),
                "replay_rows": len(replay),
                "fraction_rows": len(fractions),
                "completed_at": dt.datetime.now().isoformat(),
            },
        )
        make_figures(run_dir)
    barrier()
    if dist.is_available() and dist.is_initialized():
        dist.destroy_process_group()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

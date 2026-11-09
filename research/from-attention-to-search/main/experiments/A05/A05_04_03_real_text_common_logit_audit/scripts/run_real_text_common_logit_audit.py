#!/usr/bin/env python3
"""DCLM real-text random-init MoE common-logit audit."""

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
        dist.init_process_group(backend="nccl")
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


def train_task(
    num_experts: int,
    seed: int,
    dataset: PackedBinDataset,
    audit_indices: list[int],
    train_indices: list[int],
    args: argparse.Namespace,
    device: torch.device,
) -> list[dict[str, Any]]:
    model = make_model(num_experts, seed, args, device)
    opt = torch.optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=0.0)
    rows: list[dict[str, Any]] = []
    last_loss = None
    ckpts = set(args.checkpoints)
    train_ptr = 0
    for step in range(0, args.max_train_steps + 1):
        if step in ckpts:
            r, _, _ = audit_model(
                model,
                dataset,
                audit_indices[: args.trajectory_audit_num_sequences],
                args,
                device,
                seed,
                num_experts,
                step,
                collect_sample=False,
            )
            for row in r:
                row["lm_loss"] = last_loss
                rows.append(row)
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
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        last_loss = float(loss.detach().item())
    return rows


def summarize_virtual(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for r in rows:
        key = (r["scale_name"], r["E_virtual"], r["model_seed"], r["layer"])
        groups.setdefault(key, []).append(r)
    out = []
    fields = ["common_margin", "residual_margin", "dominance_ratio", "raw_active_experts_ratio", "centered_active_experts_ratio", "raw_max_load", "centered_max_load"]
    for key, vals in groups.items():
        scale_name, e, model_seed, layer = key
        row = {"scale_name": scale_name, "E_virtual": e, "model_seed": model_seed, "layer": layer, "n": len(vals)}
        for f in fields:
            arr = [float(v[f]) for v in vals]
            row[f"{f}_mean"] = float(np.mean(arr))
            row[f"{f}_std"] = float(np.std(arr))
        out.append(row)
    return out


def make_figures(run_dir: Path) -> None:
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
    except Exception:
        return
    fig_dir = run_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    p1 = run_dir / "results/phase1_step0_metrics.csv"
    if p1.exists() and p1.stat().st_size > 0:
        df = pd.read_csv(p1)
        plt.figure(figsize=(8, 4))
        df.groupby("layer")[["common_margin", "residual_margin"]].mean().plot(kind="bar", ax=plt.gca())
        plt.tight_layout()
        plt.savefig(fig_dir / "phase1_common_vs_residual_margin.png", dpi=160)
        plt.close()
        plt.figure(figsize=(8, 4))
        df.groupby("layer")[["raw_max_load", "centered_max_load"]].mean().plot(kind="bar", ax=plt.gca())
        plt.tight_layout()
        plt.savefig(fig_dir / "phase1_raw_vs_centered_load.png", dpi=160)
        plt.close()
    p2 = run_dir / "results/phase2_virtual_scaling_summary.csv"
    if p2.exists() and p2.stat().st_size > 0:
        df = pd.read_csv(p2)
        for scale in df["scale_name"].unique():
            sub = df[df["scale_name"] == scale].groupby("E_virtual").mean(numeric_only=True).reset_index()
            plt.figure(figsize=(7, 4))
            plt.plot(sub["E_virtual"], sub["common_margin_mean"], marker="o")
            plt.xscale("log", base=2)
            plt.tight_layout()
            plt.savefig(fig_dir / f"phase2_E_vs_common_margin_{scale}.png", dpi=160)
            plt.close()
            plt.figure(figsize=(7, 4))
            plt.plot(sub["E_virtual"], sub["raw_active_experts_ratio_mean"], marker="o", label="raw")
            plt.plot(sub["E_virtual"], sub["centered_active_experts_ratio_mean"], marker="o", label="centered")
            plt.xscale("log", base=2)
            plt.legend()
            plt.tight_layout()
            plt.savefig(fig_dir / f"phase2_E_vs_active_experts_ratio_{scale}.png", dpi=160)
            plt.close()
    for name, xcol, ycols, out in [
        ("phase3_trajectory_metrics.csv", "step", ["raw_max_load", "centered_max_load"], "phase3_max_load_over_steps.png"),
        ("phase4_actual_E_sweep_metrics.csv", "num_experts", ["raw_active_experts_ratio", "centered_active_experts_ratio"], "phase4_E_train_vs_active_experts_ratio.png"),
    ]:
        p = run_dir / "results" / name
        if p.exists() and p.stat().st_size > 0:
            df = pd.read_csv(p)
            sub = df.groupby(xcol)[ycols].mean().reset_index()
            plt.figure(figsize=(7, 4))
            for y in ycols:
                plt.plot(sub[xcol], sub[y], marker="o", label=y)
            plt.legend()
            plt.tight_layout()
            plt.savefig(fig_dir / out, dpi=160)
            plt.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-stage", choices=["smoke", "full"], default="smoke")
    parser.add_argument("--run-name", default=f"real_text_common_logit_audit_v5_{now_slug()}")
    parser.add_argument("--output-dir", type=Path, default=RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A05/A05_04_03_real_text_common_logit_audit")
    parser.add_argument("--data-path", type=Path, default=Path("/data/share/109_cache_dir/hf_data/dclm_bin"))
    parser.add_argument("--hidden-size", type=int, default=512)
    parser.add_argument("--num-layers", type=int, default=6)
    parser.add_argument("--num-heads", type=int, default=8)
    parser.add_argument("--num-key-value-heads", type=int, default=4)
    parser.add_argument("--expert-hidden-dim", type=int, default=2048)
    parser.add_argument("--vocab-size", type=int, default=151936)
    parser.add_argument("--initializer-range", type=float, default=0.02)
    parser.add_argument("--audit-num-sequences", type=int, default=8192)
    parser.add_argument("--trajectory-audit-num-sequences", type=int, default=8192)
    parser.add_argument("--train-num-sequences", type=int, default=32768)
    parser.add_argument("--audit-batch-size", type=int, default=8)
    parser.add_argument("--train-batch-size", type=int, default=2)
    parser.add_argument("--max-analyzed-tokens-per-layer", type=int, default=262144)
    parser.add_argument("--virtual-router-seeds", type=int, default=64)
    parser.add_argument("--virtual-expert-counts", type=int, nargs="+", default=[4, 8, 16, 32, 64, 128, 256, 512, 1024])
    parser.add_argument("--virtual-chunk-tokens", type=int, default=8192)
    parser.add_argument("--model-seeds", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument("--actual-e-values", type=int, nargs="+", default=[4, 8, 16, 32])
    parser.add_argument("--max-train-steps", type=int, default=300)
    parser.add_argument("--checkpoints", type=int, nargs="+", default=[0, 1, 10, 50, 100, 300])
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    args = parser.parse_args()

    rank, world, local_rank = setup_dist()
    device = torch.device(f"cuda:{local_rank}" if torch.cuda.is_available() else "cpu")
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

    if args.run_stage == "smoke":
        args.audit_num_sequences = min(args.audit_num_sequences, 16)
        args.trajectory_audit_num_sequences = min(args.trajectory_audit_num_sequences, 16)
        args.train_num_sequences = min(args.train_num_sequences, 64)
        args.max_analyzed_tokens_per_layer = min(args.max_analyzed_tokens_per_layer, 1024)
        args.virtual_router_seeds = min(args.virtual_router_seeds, 2)
        args.virtual_expert_counts = [4, 8]
        args.model_seeds = [0]
        args.actual_e_values = [4]
        args.max_train_steps = 2
        args.checkpoints = [0, 1, 2]
        args.audit_batch_size = min(args.audit_batch_size, 2)
        args.train_batch_size = 1

    run_dir = args.output_dir / "runs/real_text_common_logit_audit_v5" / args.run_name
    partial_dir = run_dir / "partials"
    for d in ["config", "logs", "results", "figures", "notes", "partials"]:
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

    phase1_all: list[dict[str, Any]] = []
    tasks = list(enumerate(args.model_seeds))
    for task_idx, seed in tasks:
        if task_idx % world != rank:
            continue
        print(f"[rank{rank}] phase1/2 start seed={seed}", flush=True)
        model = make_model(8, seed, args, device)
        p1, buckets, sampled = audit_model(model, dataset, audit_indices, args, device, seed, 8, 0, collect_sample=True)
        append_jsonl(partial_dir / f"phase1_rank{rank}.jsonl", p1)
        append_jsonl(partial_dir / f"phase1_buckets_rank{rank}.jsonl", buckets)
        print(f"[rank{rank}] phase2 start seed={seed}", flush=True)
        p2 = virtual_scaling_rows(sampled, p1, args, seed, device)
        append_jsonl(partial_dir / f"phase2_rank{rank}.jsonl", p2)
        print(f"[rank{rank}] phase1/2 done seed={seed} phase2_rows={len(p2)}", flush=True)
        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    barrier()

    train_tasks = []
    for e in args.actual_e_values:
        for seed in args.model_seeds:
            train_tasks.append((e, seed))
    for task_idx, (e, seed) in enumerate(train_tasks):
        if task_idx % world != rank:
            continue
        print(f"[rank{rank}] train start E={e} seed={seed}", flush=True)
        train_indices = train_indices_base[:]
        random.Random(seed + e * 1000).shuffle(train_indices)
        rows = train_task(e, seed, dataset, audit_indices, train_indices, args, device)
        append_jsonl(partial_dir / f"trajectory_rank{rank}.jsonl", rows)
        print(f"[rank{rank}] train done E={e} seed={seed} rows={len(rows)}", flush=True)
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    barrier()

    if rank == 0:
        phase1 = []
        buckets = []
        phase2 = []
        traj = []
        for p in sorted(partial_dir.glob("phase1_rank*.jsonl")):
            phase1.extend(read_jsonl(p))
        for p in sorted(partial_dir.glob("phase1_buckets_rank*.jsonl")):
            buckets.extend(read_jsonl(p))
        for p in sorted(partial_dir.glob("phase2_rank*.jsonl")):
            phase2.extend(read_jsonl(p))
        for p in sorted(partial_dir.glob("trajectory_rank*.jsonl")):
            traj.extend(read_jsonl(p))
        phase3 = [r for r in traj if int(r["num_experts"]) == 8]
        phase4 = traj
        write_csv(run_dir / "results/phase1_step0_metrics.csv", phase1)
        write_csv(run_dir / "results/phase1_position_bucket_metrics.csv", buckets)
        write_csv(run_dir / "results/phase1_layer_summary.csv", phase1)
        write_csv(run_dir / "results/phase2_virtual_scaling_metrics.csv", phase2)
        write_csv(run_dir / "results/phase2_virtual_scaling_summary.csv", summarize_virtual(phase2))
        write_csv(run_dir / "results/phase3_trajectory_metrics.csv", phase3)
        write_csv(run_dir / "results/phase4_actual_E_sweep_metrics.csv", phase4)
        write_json(
            run_dir / "run_summary.json",
            {
                "run_name": args.run_name,
                "run_stage": args.run_stage,
                "phase1_rows": len(phase1),
                "phase2_rows": len(phase2),
                "phase3_rows": len(phase3),
                "phase4_rows": len(phase4),
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

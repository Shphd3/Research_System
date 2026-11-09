#!/usr/bin/env python3
"""A06_10: real-DCLM label-free proxy feature audit."""

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


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    seen = set()
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
            "input_token_count": self.input_length,
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


def make_config(args: argparse.Namespace) -> Qwen3Config:
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
        num_experts=args.num_experts,
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


def make_model(seed: int, args: argparse.Namespace, device: torch.device) -> MyQwen3ForCausalLM:
    torch.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)
    model = MyQwen3ForCausalLM(make_config(args))
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


def selected_layers(model: MyQwen3ForCausalLM, args: argparse.Namespace) -> list[int]:
    available = [idx for idx, _, _ in iter_gate_modules(model)]
    if args.audit_layers:
        keep = set(args.audit_layers)
        return [idx for idx in available if idx in keep]
    return available


def train_to_step(
    model: MyQwen3ForCausalLM,
    dataset: PackedBinDataset,
    train_indices: list[int],
    step: int,
    args: argparse.Namespace,
    device: torch.device,
) -> float | None:
    if step <= 0:
        return None
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=args.learning_rate, weight_decay=0.0)
    last_loss = None
    ptr = 0
    for train_step in range(step):
        if ptr + args.train_batch_size > len(train_indices):
            random.Random(args.shuffle_seed + train_step).shuffle(train_indices)
            ptr = 0
        batch_idx = train_indices[ptr : ptr + args.train_batch_size]
        ptr += args.train_batch_size
        x, y = dataset.batch(batch_idx, device)
        opt.zero_grad(set_to_none=True)
        out = model(input_ids=x, use_cache=False)
        loss = F.cross_entropy(out.logits.reshape(-1, out.logits.shape[-1]), y.reshape(-1))
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        last_loss = float(loss.detach().item())
    return last_loss


def collect_layer_samples(
    model: MyQwen3ForCausalLM,
    dataset: PackedBinDataset,
    sample_indices: list[int],
    split_name: str,
    args: argparse.Namespace,
    device: torch.device,
) -> tuple[dict[int, dict[str, np.ndarray]], list[dict[str, Any]]]:
    model.eval()
    cap = GateCapture(model)
    layers = selected_layers(model, args)
    per_layer = {
        layer: {"h": [], "token_id": [], "position": [], "sample_index": []}
        for layer in layers
    }
    collected = {layer: 0 for layer in layers}
    audit_rows: list[dict[str, Any]] = []
    with torch.no_grad():
        for start in range(0, len(sample_indices), args.audit_batch_size):
            if all(collected[layer] >= args.tokens_per_split_per_layer for layer in layers):
                break
            batch_idx = sample_indices[start : start + args.audit_batch_size]
            x, _ = dataset.batch(batch_idx, device)
            bsz, seq_len = x.shape
            token_flat = x.reshape(-1).detach().cpu().numpy().astype(np.int64)
            pos_flat = np.tile(np.arange(seq_len, dtype=np.int64), bsz)
            sample_flat = np.repeat(np.array(batch_idx, dtype=np.int64), seq_len)
            cap.clear()
            _ = model.model(input_ids=x, use_cache=False)
            for layer_idx, (h, _logits) in cap.records.items():
                if layer_idx not in per_layer:
                    continue
                remain = args.tokens_per_split_per_layer - collected[layer_idx]
                if remain <= 0:
                    continue
                hf = h.detach().float().cpu().numpy()
                if hf.ndim == 3:
                    hf = hf.reshape(-1, hf.shape[-1])
                take = min(remain, hf.shape[0])
                per_layer[layer_idx]["h"].append(hf[:take])
                per_layer[layer_idx]["token_id"].append(token_flat[:take])
                per_layer[layer_idx]["position"].append(pos_flat[:take])
                per_layer[layer_idx]["sample_index"].append(sample_flat[:take])
                collected[layer_idx] += take
    cap.close()
    out: dict[int, dict[str, np.ndarray]] = {}
    for layer in layers:
        if collected[layer] == 0:
            continue
        out[layer] = {
            key: np.concatenate(vals, axis=0)
            for key, vals in per_layer[layer].items()
            if vals
        }
        audit_rows.append(
            {
                "split": split_name,
                "layer": layer,
                "tokens_collected": int(out[layer]["h"].shape[0]),
                "hidden_dim": int(out[layer]["h"].shape[1]),
                "finite": bool(np.isfinite(out[layer]["h"]).all()),
                "unique_token_ids": int(np.unique(out[layer]["token_id"]).size),
                "unique_positions": int(np.unique(out[layer]["position"]).size),
            }
        )
    model.train()
    return out, audit_rows


def preprocess_fit(x: np.ndarray, condition: str) -> dict[str, np.ndarray | str]:
    mean = x.mean(axis=0, keepdims=True)
    std = x.std(axis=0, keepdims=True) + 1e-6
    return {"condition": condition, "mean": mean.astype(np.float32), "std": std.astype(np.float32)}


def preprocess_apply(x: np.ndarray, state: dict[str, np.ndarray | str]) -> np.ndarray:
    condition = str(state["condition"])
    mean = state["mean"]
    std = state["std"]
    if condition == "raw":
        z = x.astype(np.float32)
    elif condition in {"residual", "spherical_residual"}:
        z = x.astype(np.float32) - mean
    elif condition == "whitened_residual":
        z = (x.astype(np.float32) - mean) / std
    else:
        raise ValueError(f"Unknown condition: {condition}")
    if condition == "spherical_residual":
        norm = np.linalg.norm(z, axis=1, keepdims=True) + 1e-8
        z = z / norm
    return z.astype(np.float32)


def fit_kmeans(x: np.ndarray, k: int, seed: int):
    from sklearn.cluster import MiniBatchKMeans

    km = MiniBatchKMeans(
        n_clusters=k,
        random_state=seed,
        n_init=10,
        batch_size=min(4096, max(256, x.shape[0])),
        max_iter=200,
        reassignment_ratio=0.01,
    )
    km.fit(x)
    return km.cluster_centers_.astype(np.float32), km.labels_.astype(np.int64)


def assign_centers(x: np.ndarray, centers: np.ndarray) -> np.ndarray:
    x2 = np.sum(x * x, axis=1, keepdims=True)
    c2 = np.sum(centers * centers, axis=1, keepdims=True).T
    dist = x2 + c2 - 2.0 * x @ centers.T
    return np.argmin(dist, axis=1).astype(np.int64)


def match_centers(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, float]:
    an = a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-8)
    bn = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-8)
    sim = an @ bn.T
    try:
        from scipy.optimize import linear_sum_assignment

        row, col = linear_sum_assignment(-sim)
        mapping = np.zeros(a.shape[0], dtype=np.int64)
        mapping[col] = row
        return mapping, float(sim[row, col].mean())
    except Exception:
        mapping = np.zeros(a.shape[0], dtype=np.int64)
        used = set()
        vals = []
        for bi in range(b.shape[0]):
            order = np.argsort(-sim[:, bi])
            for ai in order:
                if int(ai) not in used:
                    mapping[bi] = int(ai)
                    used.add(int(ai))
                    vals.append(float(sim[int(ai), bi]))
                    break
        return mapping, float(np.mean(vals)) if vals else float("nan")


def remap(labels: np.ndarray, mapping: np.ndarray) -> np.ndarray:
    out = labels.copy()
    for old, new in enumerate(mapping):
        out[labels == old] = int(new)
    return out


def nmi(a: np.ndarray, b: np.ndarray) -> float:
    from sklearn.metrics import normalized_mutual_info_score

    return float(normalized_mutual_info_score(a, b))


def adjusted_rand(a: np.ndarray, b: np.ndarray) -> float:
    from sklearn.metrics import adjusted_rand_score

    return float(adjusted_rand_score(a, b))


def entropy_load(labels: np.ndarray, k: int) -> dict[str, float]:
    counts = np.bincount(labels, minlength=k).astype(np.float64)
    p = counts / max(counts.sum(), 1.0)
    active = int((counts > 0).sum())
    ent = -float(np.sum(p[p > 0] * np.log(p[p > 0]))) / math.log(max(k, 2))
    return {
        "active_clusters": active,
        "active_cluster_ratio": active / float(k),
        "max_cluster_load": float(p.max()) if p.size else 0.0,
        "cluster_entropy": ent,
        "min_cluster_count": int(counts.min()) if counts.size else 0,
    }


def frequency_bins(token_ids: np.ndarray, num_bins: int) -> np.ndarray:
    values, counts = np.unique(token_ids, return_counts=True)
    freq = dict(zip(values.tolist(), counts.tolist()))
    tok_counts = np.array([freq[int(t)] for t in token_ids], dtype=np.float64)
    qs = np.quantile(tok_counts, np.linspace(0, 1, num_bins + 1))
    bins = np.digitize(tok_counts, qs[1:-1], right=True)
    return bins.astype(np.int64)


def top_frequency_mask(token_ids: np.ndarray, pct: float) -> np.ndarray:
    values, counts = np.unique(token_ids, return_counts=True)
    top_n = max(1, int(math.ceil(values.size * pct)))
    top_tokens = set(values[np.argsort(-counts)[:top_n]].tolist())
    return np.array([int(t) not in top_tokens for t in token_ids], dtype=bool)


def compare_condition(
    seed: int,
    step: int,
    layer: int,
    condition: str,
    split_a: dict[str, np.ndarray],
    split_b: dict[str, np.ndarray],
    split_eval: dict[str, np.ndarray],
    args: argparse.Namespace,
) -> tuple[dict[str, Any], dict[str, Any]]:
    state_a = preprocess_fit(split_a["h"], condition)
    state_b = preprocess_fit(split_b["h"], condition)
    za = preprocess_apply(split_a["h"], state_a)
    zb = preprocess_apply(split_b["h"], state_b)
    ze_a = preprocess_apply(split_eval["h"], state_a)
    ze_b = preprocess_apply(split_eval["h"], state_b)
    centers_a, labels_a = fit_kmeans(za, args.num_clusters, seed + step * 101 + layer * 1009)
    centers_b, labels_b = fit_kmeans(zb, args.num_clusters, seed + step * 101 + layer * 1009 + 17)
    eval_a = assign_centers(ze_a, centers_a)
    eval_b_raw = assign_centers(ze_b, centers_b)
    mapping_b_to_a, center_cos = match_centers(centers_a, centers_b)
    eval_b = remap(eval_b_raw, mapping_b_to_a)
    agree = float(np.mean(eval_a == eval_b))
    eval_nmi = nmi(eval_a, eval_b)
    eval_ari = adjusted_rand(eval_a, eval_b)
    rand = np.random.default_rng(seed + step + layer + len(condition)).integers(
        0, args.num_clusters, size=eval_a.shape[0], dtype=np.int64
    )
    freq = frequency_bins(split_eval["token_id"], args.frequency_bins)
    pos_bucket = (split_eval["position"] // args.position_bucket_size).astype(np.int64)
    top1_mask = top_frequency_mask(split_eval["token_id"], 0.01)
    top5_mask = top_frequency_mask(split_eval["token_id"], 0.05)
    row = {
        "model_seed": seed,
        "checkpoint_step": step,
        "layer": layer,
        "condition": condition,
        "eval_tokens": int(eval_a.shape[0]),
        "center_match_cosine": center_cos,
        "eval_assignment_agreement": agree,
        "eval_assignment_nmi": eval_nmi,
        "eval_assignment_ari": eval_ari,
        "random_assignment_nmi": nmi(eval_a, rand),
        "token_id_nmi": nmi(eval_a, split_eval["token_id"]),
        "frequency_bin_nmi": nmi(eval_a, freq),
        "position_bucket_nmi": nmi(eval_a, pos_bucket),
        "top1_removed_eval_nmi": nmi(eval_a[top1_mask], eval_b[top1_mask]) if top1_mask.any() else None,
        "top5_removed_eval_nmi": nmi(eval_a[top5_mask], eval_b[top5_mask]) if top5_mask.any() else None,
        "top1_kept_fraction": float(top1_mask.mean()),
        "top5_kept_fraction": float(top5_mask.mean()),
    }
    row.update({f"calib_a_{k}": v for k, v in entropy_load(labels_a, args.num_clusters).items()})
    row.update({f"calib_b_{k}": v for k, v in entropy_load(labels_b, args.num_clusters).items()})
    row.update({f"eval_a_{k}": v for k, v in entropy_load(eval_a, args.num_clusters).items()})
    examples = {
        "model_seed": seed,
        "checkpoint_step": step,
        "layer": layer,
        "condition": condition,
        "cluster_examples": [],
    }
    for cluster in range(args.num_clusters):
        idx = np.where(eval_a == cluster)[0][: args.examples_per_cluster]
        examples["cluster_examples"].append(
            {
                "cluster": cluster,
                "token_ids": [int(x) for x in split_eval["token_id"][idx].tolist()],
                "positions": [int(x) for x in split_eval["position"][idx].tolist()],
                "sample_indices": [int(x) for x in split_eval["sample_index"][idx].tolist()],
            }
        )
    return row, examples


def run_task(
    seed: int,
    step: int,
    dataset: PackedBinDataset,
    args: argparse.Namespace,
    device: torch.device,
    run_dir: Path,
    rank: int,
) -> None:
    model = make_model(seed, args, device)
    rng = random.Random(seed + 123)
    train_indices = list(range(args.train_start, args.train_start + args.train_num_sequences))
    rng.shuffle(train_indices)
    last_loss = train_to_step(model, dataset, train_indices, step, args, device)
    offsets = {
        "calib_a": args.audit_start,
        "calib_b": args.audit_start + args.seqs_per_split,
        "eval": args.audit_start + 2 * args.seqs_per_split,
    }
    split_data: dict[str, dict[int, dict[str, np.ndarray]]] = {}
    hidden_rows: list[dict[str, Any]] = []
    for split_name, start in offsets.items():
        idx = list(range(start, start + args.seqs_per_split))
        data, rows = collect_layer_samples(model, dataset, idx, split_name, args, device)
        split_data[split_name] = data
        for row in rows:
            row.update({"model_seed": seed, "checkpoint_step": step})
        hidden_rows.extend(rows)
    summary_rows: list[dict[str, Any]] = []
    example_rows: list[dict[str, Any]] = []
    layers = sorted(set(split_data["calib_a"]) & set(split_data["calib_b"]) & set(split_data["eval"]))
    for layer in layers:
        for condition in args.conditions:
            row, examples = compare_condition(
                seed,
                step,
                layer,
                condition,
                split_data["calib_a"][layer],
                split_data["calib_b"][layer],
                split_data["eval"][layer],
                args,
            )
            row["last_train_loss"] = last_loss
            summary_rows.append(row)
            example_rows.append(examples)
    append_jsonl(run_dir / "partials" / f"hidden_audit_rank{rank}.jsonl", hidden_rows)
    append_jsonl(run_dir / "partials" / f"proxy_summary_rank{rank}.jsonl", summary_rows)
    append_jsonl(run_dir / "partials" / f"cluster_examples_rank{rank}.jsonl", example_rows)
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def make_figures(run_dir: Path) -> None:
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
    except Exception:
        return
    path = run_dir / "results/proxy_cluster_summary.csv"
    if not path.exists() or path.stat().st_size == 0:
        return
    df = pd.read_csv(path)
    fig_dir = run_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    for metric, name in [
        ("eval_assignment_nmi", "proxy_stability_by_condition.png"),
        ("frequency_bin_nmi", "nuisance_frequency_nmi_by_condition.png"),
        ("position_bucket_nmi", "nuisance_position_nmi_by_condition.png"),
    ]:
        sub = df.groupby("condition")[metric].agg(["mean", "std"]).reset_index()
        plt.figure(figsize=(8, 4))
        plt.bar(sub["condition"], sub["mean"], yerr=sub["std"].fillna(0.0), capsize=3)
        plt.xticks(rotation=25, ha="right")
        plt.ylabel(metric)
        plt.tight_layout()
        plt.savefig(fig_dir / name, dpi=160)
        plt.close()


def aggregate(run_dir: Path) -> None:
    hidden, summary, examples = [], [], []
    for path in sorted((run_dir / "partials").glob("hidden_audit_rank*.jsonl")):
        hidden.extend(read_jsonl(path))
    for path in sorted((run_dir / "partials").glob("proxy_summary_rank*.jsonl")):
        summary.extend(read_jsonl(path))
    for path in sorted((run_dir / "partials").glob("cluster_examples_rank*.jsonl")):
        examples.extend(read_jsonl(path))
    write_csv(run_dir / "results/hidden_audit.csv", hidden)
    write_csv(run_dir / "results/proxy_cluster_summary.csv", summary)
    write_json(run_dir / "results/cluster_examples.json", examples)
    make_figures(run_dir)
    if summary:
        residual = [r for r in summary if r["condition"] == "residual"]
        best = sorted(summary, key=lambda r: float(r["eval_assignment_nmi"]), reverse=True)[:10]
        write_json(
            run_dir / "run_summary.json",
            {
                "run_name": run_dir.name,
                "completed_at": dt.datetime.now().isoformat(),
                "summary_rows": len(summary),
                "hidden_rows": len(hidden),
                "residual_mean_eval_assignment_nmi": float(np.mean([r["eval_assignment_nmi"] for r in residual])) if residual else None,
                "residual_mean_frequency_bin_nmi": float(np.mean([r["frequency_bin_nmi"] for r in residual])) if residual else None,
                "residual_mean_position_bucket_nmi": float(np.mean([r["position_bucket_nmi"] for r in residual])) if residual else None,
                "top_rows_by_eval_assignment_nmi": best,
            },
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-name", default=f"a06_10_real_dclm_proxy_{now_slug()}")
    parser.add_argument("--output-dir", type=Path, default=RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_04_E01_real_proxy_operationalization")
    parser.add_argument("--data-path", type=Path, default=Path("/data/share/109_cache_dir/hf_data/dclm_bin"))
    parser.add_argument("--hidden-size", type=int, default=512)
    parser.add_argument("--num-layers", type=int, default=6)
    parser.add_argument("--num-heads", type=int, default=8)
    parser.add_argument("--num-key-value-heads", type=int, default=4)
    parser.add_argument("--expert-hidden-dim", type=int, default=2048)
    parser.add_argument("--num-experts", type=int, default=8)
    parser.add_argument("--num-clusters", type=int, default=8)
    parser.add_argument("--vocab-size", type=int, default=151936)
    parser.add_argument("--initializer-range", type=float, default=0.02)
    parser.add_argument("--audit-start", type=int, default=0)
    parser.add_argument("--seqs-per-split", type=int, default=2048)
    parser.add_argument("--train-start", type=int, default=8192)
    parser.add_argument("--train-num-sequences", type=int, default=32768)
    parser.add_argument("--audit-batch-size", type=int, default=8)
    parser.add_argument("--train-batch-size", type=int, default=2)
    parser.add_argument("--tokens-per-split-per-layer", type=int, default=65536)
    parser.add_argument("--model-seeds", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument("--checkpoints", type=int, nargs="+", default=[0, 10])
    parser.add_argument("--audit-layers", type=int, nargs="*", default=[0, 3, 4, 5])
    parser.add_argument("--conditions", nargs="+", default=["raw", "residual", "spherical_residual", "whitened_residual"])
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--frequency-bins", type=int, default=8)
    parser.add_argument("--position-bucket-size", type=int, default=32)
    parser.add_argument("--examples-per-cluster", type=int, default=12)
    parser.add_argument("--shuffle-seed", type=int, default=7001)
    args = parser.parse_args()

    rank, world, local_rank = setup_dist()
    device = torch.device(f"cuda:{local_rank}" if torch.cuda.is_available() else "cpu")
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

    run_dir = args.output_dir / "runs/real_dclm_proxy_feature_operationalization" / args.run_name
    for sub in ["config", "logs", "results", "figures", "partials", "notes"]:
        (run_dir / sub).mkdir(parents=True, exist_ok=True)
    if rank == 0:
        write_json(run_dir / "config/run_config.json", vars(args))
        write_json(
            run_dir / "config/source_manifest.json",
            {
                "timestamp": dt.datetime.now().isoformat(),
                "machine": socket.gethostname(),
                "runner": str(Path(__file__).resolve()),
                "runner_sha256": sha256_file(Path(__file__).resolve()),
                "moe_root": str(MOE_ROOT),
                "model_files": {
                    "myqwen.py": sha256_file(MOE_ROOT / "src/model/qwen3_moe/myqwen.py"),
                    "qwen3config.py": sha256_file(MOE_ROOT / "src/model/qwen3_moe/qwen3config.py"),
                },
                "data_path": str(args.data_path),
            },
        )
    barrier()

    dataset = PackedBinDataset(args.data_path)
    if rank == 0:
        preview = []
        for split, start in [("calib_a", args.audit_start), ("calib_b", args.audit_start + args.seqs_per_split), ("eval", args.audit_start + 2 * args.seqs_per_split)]:
            preview.extend(dataset.manifest_row(i, split) for i in range(start, min(start + 16, start + args.seqs_per_split)))
        append_jsonl(run_dir / "config/data_manifest_preview.jsonl", preview)
    barrier()

    tasks = [(seed, step) for seed in args.model_seeds for step in args.checkpoints]
    for task_idx, (seed, step) in enumerate(tasks):
        if task_idx % world != rank:
            continue
        print(f"[rank{rank}] start seed={seed} step={step}", flush=True)
        run_task(seed, step, dataset, args, device, run_dir, rank)
        print(f"[rank{rank}] done seed={seed} step={step}", flush=True)
    barrier()
    if rank == 0:
        aggregate(run_dir)
    barrier()
    if dist.is_available() and dist.is_initialized():
        dist.destroy_process_group()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

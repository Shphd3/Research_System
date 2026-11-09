#!/usr/bin/env python3
"""A06_12: train after real-DCLM proxy-center router initialization."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import os
import random
import socket
import sys
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.distributed as dist
import torch.nn.functional as F

RESEARCH_ROOT = Path("/data/250010109/Research_System")
A06_10_SCRIPT_DIR = RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_04_E01_real_proxy_operationalization/scripts"
if str(A06_10_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(A06_10_SCRIPT_DIR))

import run_real_dclm_proxy_feature_operationalization as a10


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


def top_margin_np(scores: np.ndarray) -> np.ndarray:
    part = np.partition(scores, kth=-2, axis=1)
    return part[:, -1] - part[:, -2]


def normalize_rows(w: np.ndarray, scale: float) -> np.ndarray:
    return (w / (np.linalg.norm(w, axis=1, keepdims=True) + 1e-8) * scale).astype(np.float32)


def collect_hidden_logits(
    model: a10.MyQwen3ForCausalLM,
    dataset: a10.PackedBinDataset,
    sample_indices: list[int],
    args: argparse.Namespace,
    device: torch.device,
) -> dict[int, dict[str, np.ndarray]]:
    model.eval()
    cap = a10.GateCapture(model)
    layers = a10.selected_layers(model, args)
    per_layer = {layer: {"h": [], "logits": [], "token_id": [], "position": []} for layer in layers}
    collected = {layer: 0 for layer in layers}
    with torch.no_grad():
        for start in range(0, len(sample_indices), args.audit_batch_size):
            if all(collected[layer] >= args.tokens_per_eval_per_layer for layer in layers):
                break
            batch_idx = sample_indices[start : start + args.audit_batch_size]
            x, _ = dataset.batch(batch_idx, device)
            bsz, seq_len = x.shape
            token_flat = x.reshape(-1).detach().cpu().numpy().astype(np.int64)
            pos_flat = np.tile(np.arange(seq_len, dtype=np.int64), bsz)
            cap.clear()
            _ = model.model(input_ids=x, use_cache=False)
            for layer_idx, (h, logits) in cap.records.items():
                if layer_idx not in per_layer:
                    continue
                remain = args.tokens_per_eval_per_layer - collected[layer_idx]
                if remain <= 0:
                    continue
                hf = h.detach().float().cpu().numpy()
                lf = logits.detach().float().cpu().numpy()
                if hf.ndim == 3:
                    hf = hf.reshape(-1, hf.shape[-1])
                if lf.ndim == 3:
                    lf = lf.reshape(-1, lf.shape[-1])
                take = min(remain, hf.shape[0])
                per_layer[layer_idx]["h"].append(hf[:take])
                per_layer[layer_idx]["logits"].append(lf[:take])
                per_layer[layer_idx]["token_id"].append(token_flat[:take])
                per_layer[layer_idx]["position"].append(pos_flat[:take])
                collected[layer_idx] += take
    cap.close()
    out: dict[int, dict[str, np.ndarray]] = {}
    for layer in layers:
        if collected[layer] == 0:
            continue
        out[layer] = {key: np.concatenate(vals, axis=0) for key, vals in per_layer[layer].items() if vals}
    model.train()
    return out


def fit_step0_proxies(
    model: a10.MyQwen3ForCausalLM,
    dataset: a10.PackedBinDataset,
    calib_indices: list[int],
    eval_indices: list[int],
    args: argparse.Namespace,
    device: torch.device,
) -> tuple[dict[int, dict[str, Any]], dict[int, np.ndarray]]:
    calib, _ = a10.collect_layer_samples(model, dataset, calib_indices, "calib_a", args, device)
    eval_data = collect_hidden_logits(model, dataset, eval_indices, args, device)
    proxies: dict[int, dict[str, Any]] = {}
    eval_labels: dict[int, np.ndarray] = {}
    for layer in sorted(set(calib) & set(eval_data)):
        raw_state = a10.preprocess_fit(calib[layer]["h"], "raw")
        raw_zc = a10.preprocess_apply(calib[layer]["h"], raw_state)
        raw_ze = a10.preprocess_apply(eval_data[layer]["h"], raw_state)
        raw_centers, _ = a10.fit_kmeans(raw_zc, args.num_clusters, args.proxy_seed + layer * 1009)
        residual_state = a10.preprocess_fit(calib[layer]["h"], "residual")
        residual_zc = a10.preprocess_apply(calib[layer]["h"], residual_state)
        residual_centers, _ = a10.fit_kmeans(residual_zc, args.num_clusters, args.proxy_seed + layer * 1009 + 17)
        eval_labels[layer] = a10.assign_centers(raw_ze, raw_centers)
        proxies[layer] = {
            "raw_centers": raw_centers,
            "residual_centers": residual_centers,
            "raw_state": raw_state,
            "residual_state": residual_state,
        }
    return proxies, eval_labels


def apply_router_init(model: a10.MyQwen3ForCausalLM, proxies: dict[int, dict[str, Any]], variant: str, seed: int, args: argparse.Namespace) -> None:
    for layer_idx, _mlp, gate in a10.iter_gate_modules(model):
        if layer_idx not in proxies:
            continue
        original = gate.weight.detach().float().cpu().numpy()
        scale = float(np.linalg.norm(original, axis=1).mean())
        if variant == "random":
            continue
        if variant == "equal_norm_random":
            rng = np.random.default_rng(seed * 100003 + layer_idx)
            rows = normalize_rows(rng.standard_normal(original.shape).astype(np.float32), scale)
        elif variant == "raw_center":
            rows = normalize_rows(proxies[layer_idx]["raw_centers"], scale)
        elif variant == "residual_center":
            rows = normalize_rows(proxies[layer_idx]["residual_centers"], scale)
        else:
            raise ValueError(f"Unknown init variant: {variant}")
        with torch.no_grad():
            gate.weight.copy_(torch.from_numpy(rows).to(device=gate.weight.device, dtype=gate.weight.dtype))


def load_metrics(labels: np.ndarray, k: int) -> dict[str, Any]:
    return a10.entropy_load(labels.astype(np.int64), k)


def audit_checkpoint(
    model: a10.MyQwen3ForCausalLM,
    dataset: a10.PackedBinDataset,
    eval_indices: list[int],
    fixed_labels: dict[int, np.ndarray],
    variant: str,
    seed: int,
    step: int,
    last_loss: float | None,
    args: argparse.Namespace,
    device: torch.device,
) -> list[dict[str, Any]]:
    data = collect_hidden_logits(model, dataset, eval_indices, args, device)
    rows = []
    for layer, d in data.items():
        if layer not in fixed_labels:
            continue
        labels = fixed_labels[layer][: d["logits"].shape[0]]
        routes = np.argmax(d["logits"], axis=1).astype(np.int64)
        mean = d["h"].mean(axis=0, keepdims=True).astype(np.float32)
        gate_w = None
        for lidx, _mlp, gate in a10.iter_gate_modules(model):
            if lidx == layer:
                gate_w = gate.weight.detach().float().cpu().numpy()
                break
        assert gate_w is not None
        common_logits = mean.reshape(-1) @ gate_w.T
        margins = top_margin_np(d["logits"])
        freq = a10.frequency_bins(d["token_id"], args.frequency_bins)
        pos_bucket = (d["position"] // args.position_bucket_size).astype(np.int64)
        row = {
            "variant": variant,
            "model_seed": seed,
            "step": step,
            "layer": layer,
            "lm_loss": last_loss,
            "eval_tokens": int(routes.shape[0]),
            "proxy_route_nmi": a10.nmi(labels, routes),
            "proxy_route_ari": a10.adjusted_rand(labels, routes),
            "proxy_route_agreement": float(np.mean(labels == routes)),
            "route_frequency_bin_nmi": a10.nmi(routes, freq),
            "route_position_bucket_nmi": a10.nmi(routes, pos_bucket),
            "route_token_id_nmi": a10.nmi(routes, d["token_id"]),
            "common_margin": float(top_margin_np(common_logits.reshape(1, -1)).mean()),
            "route_margin_mean": float(margins.mean()),
            "route_margin_p05": float(np.quantile(margins, 0.05)),
            "gate_row_norm_mean": float(np.linalg.norm(gate_w, axis=1).mean()),
            "gate_row_norm_std": float(np.linalg.norm(gate_w, axis=1).std()),
        }
        row.update({f"route_{k}": v for k, v in load_metrics(routes, args.num_clusters).items()})
        rows.append(row)
    return rows


def train_variant(
    variant: str,
    seed: int,
    dataset: a10.PackedBinDataset,
    args: argparse.Namespace,
    device: torch.device,
) -> list[dict[str, Any]]:
    model = a10.make_model(seed, args, device)
    calib_indices = list(range(args.audit_start, args.audit_start + args.seqs_per_split))
    eval_indices = list(range(args.audit_start + 2 * args.seqs_per_split, args.audit_start + 3 * args.seqs_per_split))
    proxies, fixed_labels = fit_step0_proxies(model, dataset, calib_indices, eval_indices, args, device)
    apply_router_init(model, proxies, variant, seed, args)
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=args.learning_rate, weight_decay=0.0)
    train_indices = list(range(args.train_start, args.train_start + args.train_num_sequences))
    random.Random(seed + 17).shuffle(train_indices)
    train_ptr = 0
    last_loss = None
    rows: list[dict[str, Any]] = []
    checkpoints = set(args.checkpoints)
    for step in range(0, args.max_train_steps + 1):
        if step in checkpoints:
            rows.extend(audit_checkpoint(model, dataset, eval_indices, fixed_labels, variant, seed, step, last_loss, args, device))
        if step == args.max_train_steps:
            break
        if train_ptr + args.train_batch_size > len(train_indices):
            random.Random(seed + step).shuffle(train_indices)
            train_ptr = 0
        batch_idx = train_indices[train_ptr : train_ptr + args.train_batch_size]
        train_ptr += args.train_batch_size
        x, y = dataset.batch(batch_idx, device)
        model.train()
        opt.zero_grad(set_to_none=True)
        out = model(input_ids=x, use_cache=False)
        loss = F.cross_entropy(out.logits.reshape(-1, out.logits.shape[-1]), y.reshape(-1))
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        last_loss = float(loss.detach().item())
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return rows


def make_figures(run_dir: Path) -> None:
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
    except Exception:
        return
    path = run_dir / "results/training_preservation_summary.csv"
    if not path.exists() or path.stat().st_size == 0:
        return
    df = pd.read_csv(path)
    fig_dir = run_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    for metric in ["proxy_route_nmi", "route_max_cluster_load", "common_margin", "lm_loss"]:
        sub = df.groupby(["variant", "step"])[metric].mean().reset_index()
        plt.figure(figsize=(8, 4))
        for variant, vv in sub.groupby("variant"):
            plt.plot(vv["step"], vv[metric], marker="o", label=variant)
        plt.xlabel("step")
        plt.ylabel(metric)
        plt.legend()
        plt.tight_layout()
        plt.savefig(fig_dir / f"trajectory_{metric}.png", dpi=160)
        plt.close()


def aggregate(run_dir: Path) -> None:
    rows = []
    for path in sorted((run_dir / "partials").glob("trajectory_rank*.jsonl")):
        rows.extend(read_jsonl(path))
    write_csv(run_dir / "results/training_preservation_summary.csv", rows)
    make_figures(run_dir)
    if rows:
        import pandas as pd

        df = pd.DataFrame(rows)
        main = df.groupby(["variant", "step"])["proxy_route_nmi"].mean().reset_index().to_dict("records")
        write_json(
            run_dir / "run_summary.json",
            {
                "run_name": run_dir.name,
                "completed_at": dt.datetime.now().isoformat(),
                "rows": len(rows),
                "mean_proxy_route_nmi_by_variant_step": main,
            },
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-name", default=f"a06_12_proxy_init_training_{now_slug()}")
    parser.add_argument("--output-dir", type=Path, default=RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_04_E03_real_proxy_training_overwrite")
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
    parser.add_argument("--tokens-per-eval-per-layer", type=int, default=65536)
    parser.add_argument("--model-seeds", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument("--variants", nargs="+", default=["random", "equal_norm_random", "raw_center", "residual_center"])
    parser.add_argument("--audit-layers", type=int, nargs="*", default=[3, 4, 5])
    parser.add_argument("--max-train-steps", type=int, default=50)
    parser.add_argument("--checkpoints", type=int, nargs="+", default=[0, 1, 2, 3, 5, 10, 20, 50])
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--frequency-bins", type=int, default=8)
    parser.add_argument("--position-bucket-size", type=int, default=32)
    parser.add_argument("--proxy-seed", type=int, default=9101)
    args = parser.parse_args()

    rank, world, local_rank = setup_dist()
    device = torch.device(f"cuda:{local_rank}" if torch.cuda.is_available() else "cpu")
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    run_dir = args.output_dir / "runs/real_dclm_proxy_init_training_preservation" / args.run_name
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
                "a06_10_runner_sha256": sha256_file(A06_10_SCRIPT_DIR / "run_real_dclm_proxy_feature_operationalization.py"),
                "moe_root": str(a10.MOE_ROOT),
                "data_path": str(args.data_path),
            },
        )
    barrier()
    dataset = a10.PackedBinDataset(args.data_path)
    tasks = [(variant, seed) for variant in args.variants for seed in args.model_seeds]
    for task_idx, (variant, seed) in enumerate(tasks):
        if task_idx % world != rank:
            continue
        print(f"[rank{rank}] start variant={variant} seed={seed}", flush=True)
        rows = train_variant(variant, seed, dataset, args, device)
        append_jsonl(run_dir / "partials" / f"trajectory_rank{rank}.jsonl", rows)
        print(f"[rank{rank}] done variant={variant} seed={seed} rows={len(rows)}", flush=True)
    barrier()
    if rank == 0:
        aggregate(run_dir)
    barrier()
    if dist.is_available() and dist.is_initialized():
        dist.destroy_process_group()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""A06_11: convert real-DCLM proxy centers into linear router rows."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import os
import socket
import sys
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.distributed as dist

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


def normalize_rows(w: np.ndarray, scale: float = 1.0) -> np.ndarray:
    return (w / (np.linalg.norm(w, axis=1, keepdims=True) + 1e-8) * scale).astype(np.float32)


def make_rows(
    condition: str,
    centers: np.ndarray,
    state: dict[str, np.ndarray | str],
    hidden_dim: int,
    seed: int,
    layer: int,
    step: int,
) -> np.ndarray:
    if condition == "random_gaussian":
        rng = np.random.default_rng(seed * 100003 + step * 1009 + layer)
        return (rng.standard_normal((centers.shape[0], hidden_dim)).astype(np.float32) / math.sqrt(hidden_dim)).astype(np.float32)
    if condition == "random_equal_norm":
        rng = np.random.default_rng(seed * 100003 + step * 1009 + layer + 17)
        return normalize_rows(rng.standard_normal((centers.shape[0], hidden_dim)).astype(np.float32))
    if condition == "raw_center_equal_norm":
        return normalize_rows(centers)
    if condition == "residual_center_equal_norm":
        return normalize_rows(centers)
    if condition == "whitened_center_equal_norm":
        std = state["std"]
        return normalize_rows(centers / std.reshape(1, -1))
    raise ValueError(f"Unknown router condition: {condition}")


def route_metrics(
    proxy_labels: np.ndarray,
    routes: np.ndarray,
    scores: np.ndarray,
    token_id: np.ndarray,
    position: np.ndarray,
    args: argparse.Namespace,
) -> dict[str, Any]:
    freq = a10.frequency_bins(token_id, args.frequency_bins)
    pos_bucket = (position // args.position_bucket_size).astype(np.int64)
    out = {
        "proxy_route_nmi": a10.nmi(proxy_labels, routes),
        "proxy_route_ari": a10.adjusted_rand(proxy_labels, routes),
        "proxy_route_agreement": float(np.mean(proxy_labels == routes)),
        "route_frequency_bin_nmi": a10.nmi(routes, freq),
        "route_position_bucket_nmi": a10.nmi(routes, pos_bucket),
        "route_token_id_nmi": a10.nmi(routes, token_id),
        "route_margin_mean": float(top_margin_np(scores).mean()),
        "route_margin_p05": float(np.quantile(top_margin_np(scores), 0.05)),
    }
    out.update({f"route_{k}": v for k, v in a10.entropy_load(routes, args.num_clusters).items()})
    return out


def evaluate_layer(
    seed: int,
    step: int,
    layer: int,
    calib: dict[str, np.ndarray],
    eval_data: dict[str, np.ndarray],
    args: argparse.Namespace,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    residual_state = a10.preprocess_fit(calib["h"], "residual")
    zc_res = a10.preprocess_apply(calib["h"], residual_state)
    ze_res = a10.preprocess_apply(eval_data["h"], residual_state)
    residual_centers, _ = a10.fit_kmeans(zc_res, args.num_clusters, seed + step * 101 + layer * 1009)
    residual_proxy = a10.assign_centers(ze_res, residual_centers)
    proxy_sources = {
        "raw": "raw_center_equal_norm",
        "residual": "residual_center_equal_norm",
        "whitened_residual": "whitened_center_equal_norm",
    }
    for proxy_condition, router_condition in proxy_sources.items():
        state = a10.preprocess_fit(calib["h"], proxy_condition)
        zc = a10.preprocess_apply(calib["h"], state)
        ze = a10.preprocess_apply(eval_data["h"], state)
        centers, _ = a10.fit_kmeans(zc, args.num_clusters, seed + step * 101 + layer * 1009 + len(proxy_condition))
        proxy_labels = a10.assign_centers(ze, centers)
        w = make_rows(router_condition, centers, state, eval_data["h"].shape[1], seed, layer, step)
        mean = state["mean"].astype(np.float32)
        raw_scores = eval_data["h"].astype(np.float32) @ w.T
        centered_scores = (eval_data["h"].astype(np.float32) - mean) @ w.T
        raw_routes = np.argmax(raw_scores, axis=1).astype(np.int64)
        centered_routes = np.argmax(centered_scores, axis=1).astype(np.int64)
        common_logits = (mean.reshape(-1) @ w.T).reshape(1, -1)
        for route_space, routes, scores in [("raw_input", raw_routes, raw_scores), ("centered_input", centered_routes, centered_scores)]:
            row = {
                "model_seed": seed,
                "source_checkpoint_step": step,
                "layer": layer,
                "proxy_condition": proxy_condition,
                "router_condition": router_condition,
                "route_space": route_space,
                "eval_tokens": int(routes.shape[0]),
                "row_norm_mean": float(np.linalg.norm(w, axis=1).mean()),
                "row_norm_std": float(np.linalg.norm(w, axis=1).std()),
                "common_margin": float(top_margin_np(common_logits).mean()),
            }
            row.update(route_metrics(proxy_labels, routes, scores, eval_data["token_id"], eval_data["position"], args))
            rows.append(row)
    for router_condition in ["random_gaussian", "random_equal_norm"]:
        w = make_rows(router_condition, residual_centers, residual_state, eval_data["h"].shape[1], seed, layer, step)
        mean = residual_state["mean"].astype(np.float32)
        raw_scores = eval_data["h"].astype(np.float32) @ w.T
        centered_scores = (eval_data["h"].astype(np.float32) - mean) @ w.T
        raw_routes = np.argmax(raw_scores, axis=1).astype(np.int64)
        centered_routes = np.argmax(centered_scores, axis=1).astype(np.int64)
        common_logits = (mean.reshape(-1) @ w.T).reshape(1, -1)
        for route_space, routes, scores in [("raw_input", raw_routes, raw_scores), ("centered_input", centered_routes, centered_scores)]:
            row = {
                "model_seed": seed,
                "source_checkpoint_step": step,
                "layer": layer,
                "proxy_condition": "residual",
                "router_condition": router_condition,
                "route_space": route_space,
                "eval_tokens": int(routes.shape[0]),
                "row_norm_mean": float(np.linalg.norm(w, axis=1).mean()),
                "row_norm_std": float(np.linalg.norm(w, axis=1).std()),
                "common_margin": float(top_margin_np(common_logits).mean()),
            }
            row.update(route_metrics(residual_proxy, routes, scores, eval_data["token_id"], eval_data["position"], args))
            rows.append(row)
    rng = np.random.default_rng(seed * 99991 + step * 701 + layer)
    shuffled_proxy = residual_proxy.copy()
    rng.shuffle(shuffled_proxy)
    w = normalize_rows(residual_centers)
    raw_scores = eval_data["h"].astype(np.float32) @ w.T
    routes = np.argmax(raw_scores, axis=1).astype(np.int64)
    row = {
        "model_seed": seed,
        "source_checkpoint_step": step,
        "layer": layer,
        "proxy_condition": "residual_shuffled",
        "router_condition": "label_shuffled_guard",
        "route_space": "raw_input",
        "eval_tokens": int(routes.shape[0]),
        "row_norm_mean": float(np.linalg.norm(w, axis=1).mean()),
        "row_norm_std": float(np.linalg.norm(w, axis=1).std()),
        "common_margin": float(top_margin_np((residual_state["mean"].reshape(-1) @ w.T).reshape(1, -1)).mean()),
    }
    row.update(route_metrics(shuffled_proxy, routes, raw_scores, eval_data["token_id"], eval_data["position"], args))
    rows.append(row)
    return rows


def run_task(seed: int, step: int, dataset: a10.PackedBinDataset, args: argparse.Namespace, device: torch.device, run_dir: Path, rank: int) -> None:
    model = a10.make_model(seed, args, device)
    train_indices = list(range(args.train_start, args.train_start + args.train_num_sequences))
    a10.random.Random(seed + 123).shuffle(train_indices)
    last_loss = a10.train_to_step(model, dataset, train_indices, step, args, device)
    split_indices = {
        "calib_a": list(range(args.audit_start, args.audit_start + args.seqs_per_split)),
        "eval": list(range(args.audit_start + 2 * args.seqs_per_split, args.audit_start + 3 * args.seqs_per_split)),
    }
    split_data: dict[str, dict[int, dict[str, np.ndarray]]] = {}
    hidden_rows: list[dict[str, Any]] = []
    for split_name, indices in split_indices.items():
        data, rows = a10.collect_layer_samples(model, dataset, indices, split_name, args, device)
        split_data[split_name] = data
        for row in rows:
            row.update({"model_seed": seed, "source_checkpoint_step": step})
        hidden_rows.extend(rows)
    all_rows: list[dict[str, Any]] = []
    for layer in sorted(set(split_data["calib_a"]) & set(split_data["eval"])):
        rows = evaluate_layer(seed, step, layer, split_data["calib_a"][layer], split_data["eval"][layer], args)
        for row in rows:
            row["last_train_loss"] = last_loss
        all_rows.extend(rows)
    append_jsonl(run_dir / "partials" / f"hidden_audit_rank{rank}.jsonl", hidden_rows)
    append_jsonl(run_dir / "partials" / f"router_summary_rank{rank}.jsonl", all_rows)
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def make_figures(run_dir: Path) -> None:
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
    except Exception:
        return
    path = run_dir / "results/router_initialization_summary.csv"
    if not path.exists() or path.stat().st_size == 0:
        return
    df = pd.read_csv(path)
    fig_dir = run_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    sub = df.groupby(["source_checkpoint_step", "router_condition", "route_space"])["proxy_route_nmi"].mean().reset_index()
    for step in sorted(sub["source_checkpoint_step"].unique()):
        ss = sub[sub["source_checkpoint_step"] == step]
        labels = ss["router_condition"] + "/" + ss["route_space"]
        plt.figure(figsize=(10, 4))
        plt.bar(labels, ss["proxy_route_nmi"])
        plt.xticks(rotation=35, ha="right")
        plt.ylabel("proxy_route_nmi")
        plt.title(f"source step {step}")
        plt.tight_layout()
        plt.savefig(fig_dir / f"proxy_route_nmi_source_step_{int(step)}.png", dpi=160)
        plt.close()


def aggregate(run_dir: Path) -> None:
    hidden, rows = [], []
    for path in sorted((run_dir / "partials").glob("hidden_audit_rank*.jsonl")):
        hidden.extend(read_jsonl(path))
    for path in sorted((run_dir / "partials").glob("router_summary_rank*.jsonl")):
        rows.extend(read_jsonl(path))
    write_csv(run_dir / "results/hidden_audit.csv", hidden)
    write_csv(run_dir / "results/router_initialization_summary.csv", rows)
    make_figures(run_dir)
    if rows:
        main = [
            r
            for r in rows
            if r["router_condition"] == "residual_center_equal_norm" and r["route_space"] == "raw_input"
        ]
        centered = [
            r
            for r in rows
            if r["router_condition"] == "residual_center_equal_norm" and r["route_space"] == "centered_input"
        ]
        write_json(
            run_dir / "run_summary.json",
            {
                "run_name": run_dir.name,
                "completed_at": dt.datetime.now().isoformat(),
                "summary_rows": len(rows),
                "hidden_rows": len(hidden),
                "main_raw_residual_mean_proxy_route_nmi": float(np.mean([r["proxy_route_nmi"] for r in main])) if main else None,
                "diagnostic_centered_residual_mean_proxy_route_nmi": float(np.mean([r["proxy_route_nmi"] for r in centered])) if centered else None,
                "top_rows_by_proxy_route_nmi": sorted(rows, key=lambda r: float(r["proxy_route_nmi"]), reverse=True)[:20],
            },
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-name", default=f"a06_11_proxy_center_router_{now_slug()}")
    parser.add_argument("--output-dir", type=Path, default=RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_04_E02_real_proxy_router_initialization")
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
    parser.add_argument("--source-checkpoints", type=int, nargs="+", default=[0, 10])
    parser.add_argument("--audit-layers", type=int, nargs="*", default=[0, 3, 4, 5])
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--frequency-bins", type=int, default=8)
    parser.add_argument("--position-bucket-size", type=int, default=32)
    parser.add_argument("--shuffle-seed", type=int, default=7001)
    args = parser.parse_args()

    rank, world, local_rank = setup_dist()
    device = torch.device(f"cuda:{local_rank}" if torch.cuda.is_available() else "cpu")
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    run_dir = args.output_dir / "runs/real_dclm_proxy_center_router_initialization" / args.run_name
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
                "a06_10_runner": str(A06_10_SCRIPT_DIR / "run_real_dclm_proxy_feature_operationalization.py"),
                "a06_10_runner_sha256": sha256_file(A06_10_SCRIPT_DIR / "run_real_dclm_proxy_feature_operationalization.py"),
                "moe_root": str(a10.MOE_ROOT),
                "data_path": str(args.data_path),
            },
        )
    barrier()
    dataset = a10.PackedBinDataset(args.data_path)
    tasks = [(seed, step) for seed in args.model_seeds for step in args.source_checkpoints]
    for task_idx, (seed, step) in enumerate(tasks):
        if task_idx % world != rank:
            continue
        print(f"[rank{rank}] start seed={seed} source_step={step}", flush=True)
        run_task(seed, step, dataset, args, device, run_dir, rank)
        print(f"[rank{rank}] done seed={seed} source_step={step}", flush=True)
    barrier()
    if rank == 0:
        aggregate(run_dir)
    barrier()
    if dist.is_available() and dist.is_initialized():
        dist.destroy_process_group()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

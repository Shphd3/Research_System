#!/usr/bin/env python3
"""Real-DCLM gate-logit feedback bridge for A01_04."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import random
import socket
import sys
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn.functional as F

RESEARCH_ROOT = Path("/data/250010109/Research_System")
A06_12_SCRIPT_DIR = RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_04_E03_real_proxy_training_overwrite/scripts"
if str(A06_12_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(A06_12_SCRIPT_DIR))

import run_real_dclm_proxy_init_training_preservation as a12

a10 = a12.a10


def now_slug() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str), encoding="utf-8")


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


def top_eigvecs_sym(matrix: np.ndarray, k: int) -> np.ndarray:
    sym = 0.5 * (matrix + matrix.T)
    vals, vecs = np.linalg.eigh(sym)
    order = np.argsort(vals)[::-1]
    return vecs[:, order[:k]]


def projector(u: np.ndarray) -> np.ndarray:
    return u @ u.T


def random_basis(seed: int, d: int, k: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    q, _ = np.linalg.qr(rng.normal(size=(d, k)))
    return q[:, :k]


def route_metrics(logits: np.ndarray, labels: np.ndarray, num_clusters: int) -> dict[str, Any]:
    routes = np.argmax(logits, axis=1).astype(np.int64)
    out = {
        "proxy_route_nmi": a10.nmi(labels, routes),
        "proxy_route_ari": a10.adjusted_rand(labels, routes),
        "proxy_route_agreement": float(np.mean(labels == routes)),
    }
    out.update({f"route_{k}": v for k, v in a12.load_metrics(routes, num_clusters).items()})
    return out


def save_logit_artifact(
    artifact_dir: Path,
    seed: int,
    step: int,
    layer: int,
    logits: np.ndarray,
    labels: np.ndarray,
    token_id: np.ndarray,
    position: np.ndarray,
) -> Path:
    path = artifact_dir / f"seed_{seed}" / f"step_{step:05d}" / f"layer_{layer}_gate_logits.npz"
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        path,
        logits=logits.astype(np.float32),
        proxy_labels=labels.astype(np.int64),
        token_id=token_id.astype(np.int64),
        position=position.astype(np.int64),
    )
    return path


def replay_bridge_rows(
    by_layer_step: dict[int, dict[int, dict[str, np.ndarray]]],
    seed: int,
    args: argparse.Namespace,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for layer, by_step in sorted(by_layer_step.items()):
        if 0 not in by_step:
            continue
        z0 = by_step[0]["logits"]
        labels = by_step[0]["labels"]
        step0_metrics = route_metrics(z0, labels, args.num_clusters)
        for step in args.replay_steps:
            if step == 0 or step not in by_step:
                continue
            zt = by_step[step]["logits"]
            dz = zt - z0
            rank = min(args.feedback_rank, dz.shape[1])
            fb_basis = top_eigvecs_sym((dz.T @ dz) / dz.shape[0], rank)
            p_fb = projector(fb_basis)
            rand = random_basis(seed=300_000 + seed * 1009 + layer * 37 + step, d=dz.shape[1], k=rank)
            p_random = projector(rand)

            states = {
                "full": zt,
                "feedback_only": z0 + dz @ p_fb,
                "residual_only": z0 + dz - dz @ p_fb,
                "random_feedback_only": z0 + dz @ p_random,
                "random_residual_only": z0 + dz - dz @ p_random,
            }
            metrics = {name: route_metrics(logits, labels, args.num_clusters) for name, logits in states.items()}
            nmi0 = float(step0_metrics["proxy_route_nmi"])
            nmi_full = float(metrics["full"]["proxy_route_nmi"])
            nmi_fb = float(metrics["feedback_only"]["proxy_route_nmi"])
            nmi_res = float(metrics["residual_only"]["proxy_route_nmi"])
            nmi_rand_fb = float(metrics["random_feedback_only"]["proxy_route_nmi"])
            nmi_rand_res = float(metrics["random_residual_only"]["proxy_route_nmi"])
            full_drop = nmi0 - nmi_full
            denom_valid = full_drop >= args.min_full_drop
            denom = full_drop if denom_valid else 1.0
            row: dict[str, Any] = {
                "seed": seed,
                "layer": layer,
                "step": step,
                "step0_proxy_nmi": nmi0,
                "full_proxy_nmi": nmi_full,
                "feedback_only_proxy_nmi": nmi_fb,
                "residual_only_proxy_nmi": nmi_res,
                "random_feedback_only_proxy_nmi": nmi_rand_fb,
                "random_residual_only_proxy_nmi": nmi_rand_res,
                "full_nmi_drop": full_drop,
                "denominator_valid": bool(denom_valid),
                "proxy_nmi_drop_explained_by_feedback_logit_common": (nmi0 - nmi_fb) / denom,
                "feedback_logit_removal_rescue_fraction": (nmi_res - nmi_full) / denom,
                "random_drop_explained": (nmi0 - nmi_rand_fb) / denom,
                "random_removal_rescue_fraction": (nmi_rand_res - nmi_full) / denom,
                "feedback_rank": rank,
            }
            for name, mm in {"step0": step0_metrics, **metrics}.items():
                for key in ["route_max_cluster_load", "route_active_clusters", "route_cluster_entropy"]:
                    row[f"{name}_{key}"] = mm.get(key)
            rows.append(row)
    return rows


def train_seed(seed: int, dataset: Any, run_dir: Path, args: argparse.Namespace, device: torch.device) -> list[dict[str, Any]]:
    model = a10.make_model(seed, args, device)
    calib_indices = list(range(args.audit_start, args.audit_start + args.seqs_per_split))
    eval_indices = list(range(args.audit_start + 2 * args.seqs_per_split, args.audit_start + 3 * args.seqs_per_split))
    proxies, fixed_labels = a12.fit_step0_proxies(model, dataset, calib_indices, eval_indices, args, device)
    a12.apply_router_init(model, proxies, "raw_center", seed, args)

    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=args.learning_rate, weight_decay=0.0)
    train_indices = list(range(args.train_start, args.train_start + args.train_num_sequences))
    random.Random(seed + 17).shuffle(train_indices)
    train_ptr = 0

    by_layer_step: dict[int, dict[int, dict[str, np.ndarray]]] = {}
    artifact_rows: list[dict[str, Any]] = []
    checkpoint_set = set(args.checkpoints)

    for step in range(0, args.max_train_steps + 1):
        if step in checkpoint_set:
            data = a12.collect_hidden_logits(model, dataset, eval_indices, args, device)
            for layer, d in data.items():
                labels = fixed_labels[layer][: d["logits"].shape[0]]
                artifact_path = save_logit_artifact(
                    run_dir / "artifacts/gate_logits",
                    seed=seed,
                    step=step,
                    layer=layer,
                    logits=d["logits"],
                    labels=labels,
                    token_id=d["token_id"],
                    position=d["position"],
                )
                by_layer_step.setdefault(layer, {})[step] = {
                    "logits": d["logits"].astype(np.float32),
                    "labels": labels.astype(np.int64),
                }
                artifact_rows.append(
                    {
                        "seed": seed,
                        "step": step,
                        "layer": layer,
                        "tokens": int(d["logits"].shape[0]),
                        "artifact": str(artifact_path.relative_to(run_dir)),
                    }
                )
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

    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    bridge_rows = replay_bridge_rows(by_layer_step, seed=seed, args=args)
    for row in bridge_rows:
        row["variant"] = "raw_center"
    write_csv(run_dir / "artifacts" / f"seed_{seed}_artifact_index.csv", artifact_rows)
    return bridge_rows


def aggregate(rows: list[dict[str, Any]], run_dir: Path, args: argparse.Namespace) -> dict[str, Any]:
    valid = [row for row in rows if bool(row["denominator_valid"])]
    if valid:
        explain = np.array([float(row["proxy_nmi_drop_explained_by_feedback_logit_common"]) for row in valid])
        rescue = np.array([float(row["feedback_logit_removal_rescue_fraction"]) for row in valid])
        random_explain = np.array([float(row["random_drop_explained"]) for row in valid])
        random_rescue = np.array([float(row["random_removal_rescue_fraction"]) for row in valid])
    else:
        explain = rescue = random_explain = random_rescue = np.array([])

    summary_rows = []
    for step in args.replay_steps:
        if step == 0:
            continue
        step_rows = [row for row in rows if int(row["step"]) == step]
        valid_rows = [row for row in step_rows if bool(row["denominator_valid"])]
        out: dict[str, Any] = {"step": step, "cells": len(step_rows), "denominator_valid_cells": len(valid_rows)}
        for metric in [
            "step0_proxy_nmi",
            "full_proxy_nmi",
            "feedback_only_proxy_nmi",
            "residual_only_proxy_nmi",
            "full_nmi_drop",
            "proxy_nmi_drop_explained_by_feedback_logit_common",
            "feedback_logit_removal_rescue_fraction",
            "random_drop_explained",
            "random_removal_rescue_fraction",
        ]:
            vals = np.array([float(row[metric]) for row in valid_rows])
            out[f"{metric}_mean"] = float(vals.mean()) if vals.size else float("nan")
            out[f"{metric}_std"] = float(vals.std(ddof=1)) if vals.size > 1 else 0.0
        summary_rows.append(out)
    write_csv(run_dir / "tables/real_feedback_logit_bridge_by_step.csv", summary_rows)

    meta = {
        "primary_metric": "proxy_nmi_drop_explained_by_feedback_logit_common",
        "total_cells": len(rows),
        "denominator_valid_cells": len(valid),
        "mean_explain_valid": float(explain.mean()) if explain.size else float("nan"),
        "mean_rescue_valid": float(rescue.mean()) if rescue.size else float("nan"),
        "mean_random_explain_valid": float(random_explain.mean()) if random_explain.size else float("nan"),
        "mean_random_rescue_valid": float(random_rescue.mean()) if random_rescue.size else float("nan"),
        "pass_rule": "at least 3 denominator-valid cells; mean explain>=0.5; mean rescue>=0.5; both beat random controls by >=0.2",
        "pass": bool(
            len(valid) >= 3
            and explain.size
            and explain.mean() >= 0.5
            and rescue.mean() >= 0.5
            and explain.mean() >= random_explain.mean() + 0.2
            and rescue.mean() >= random_rescue.mean() + 0.2
        ),
    }
    write_json(run_dir / "tables/real_feedback_logit_bridge_summary.json", meta)
    make_figures(rows, run_dir)
    return meta


def make_figures(rows: list[dict[str, Any]], run_dir: Path) -> None:
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
    except Exception:
        return
    if not rows:
        return
    fig_dir = run_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    valid = df[df["denominator_valid"] == True].copy()
    if valid.empty:
        return

    metric_cols = [
        "step0_proxy_nmi",
        "full_proxy_nmi",
        "feedback_only_proxy_nmi",
        "residual_only_proxy_nmi",
    ]
    plot_df = valid.melt(id_vars=["step"], value_vars=metric_cols, var_name="condition", value_name="proxy_nmi")
    sub = plot_df.groupby(["step", "condition"])["proxy_nmi"].mean().reset_index()
    plt.figure(figsize=(8, 4.5))
    for cond, cc in sub.groupby("condition"):
        plt.plot(cc["step"], cc["proxy_nmi"], marker="o", label=cond)
    plt.xlabel("step")
    plt.ylabel("proxy-route NMI")
    plt.title("Real-DCLM logit bridge NMI by replay condition")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(fig_dir / "real_feedback_logit_bridge_nmi_by_step.png", dpi=170)
    plt.close()

    frac_cols = [
        "proxy_nmi_drop_explained_by_feedback_logit_common",
        "feedback_logit_removal_rescue_fraction",
        "random_drop_explained",
    ]
    frac_df = valid.melt(id_vars=["step"], value_vars=frac_cols, var_name="metric", value_name="fraction")
    sub = frac_df.groupby(["step", "metric"])["fraction"].mean().reset_index()
    plt.figure(figsize=(8, 4.5))
    for metric, mm in sub.groupby("metric"):
        plt.plot(mm["step"], mm["fraction"], marker="o", label=metric)
    plt.axhline(0.5, color="black", linestyle="--", linewidth=0.8)
    plt.xlabel("step")
    plt.ylabel("fraction of full NMI drop")
    plt.title("Real-DCLM logit bridge explanation/rescue")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(fig_dir / "real_feedback_logit_bridge_explain_rescue.png", dpi=170)
    plt.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-name", default=f"a01_04_real_dclm_feedback_logit_bridge_{now_slug()}")
    parser.add_argument("--output-dir", type=Path, default=RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run")
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
    parser.add_argument("--audit-layers", type=int, nargs="*", default=[3, 4, 5])
    parser.add_argument("--max-train-steps", type=int, default=10)
    parser.add_argument("--checkpoints", type=int, nargs="+", default=[0, 5, 10])
    parser.add_argument("--replay-steps", type=int, nargs="+", default=[5, 10])
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--frequency-bins", type=int, default=8)
    parser.add_argument("--position-bucket-size", type=int, default=32)
    parser.add_argument("--proxy-seed", type=int, default=9101)
    parser.add_argument("--feedback-rank", type=int, default=1)
    parser.add_argument("--min-full-drop", type=float, default=0.05)
    args = parser.parse_args()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

    run_dir = args.output_dir / "runs" / args.run_name
    for sub in ["config", "tables", "figures", "artifacts", "logs"]:
        (run_dir / sub).mkdir(parents=True, exist_ok=True)
    write_json(run_dir / "config/run_config.json", vars(args))
    write_json(
        run_dir / "config/source_manifest.json",
        {
            "timestamp": dt.datetime.now().isoformat(),
            "machine": socket.gethostname(),
            "runner": str(Path(__file__).resolve()),
            "runner_sha256": sha256_file(Path(__file__).resolve()),
            "a06_12_runner": str((A06_12_SCRIPT_DIR / "run_real_dclm_proxy_init_training_preservation.py").resolve()),
            "a06_12_runner_sha256": sha256_file(A06_12_SCRIPT_DIR / "run_real_dclm_proxy_init_training_preservation.py"),
            "moe_root": str(a10.MOE_ROOT),
            "data_path": str(args.data_path),
            "device": str(device),
        },
    )

    dataset = a10.PackedBinDataset(args.data_path)
    all_rows: list[dict[str, Any]] = []
    for seed in args.model_seeds:
        print(f"[run] seed={seed}", flush=True)
        all_rows.extend(train_seed(seed, dataset, run_dir, args, device))
    write_csv(run_dir / "tables/real_feedback_logit_bridge_scores.csv", all_rows)
    meta = aggregate(all_rows, run_dir, args)
    print(json.dumps({"run_dir": str(run_dir), **meta}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

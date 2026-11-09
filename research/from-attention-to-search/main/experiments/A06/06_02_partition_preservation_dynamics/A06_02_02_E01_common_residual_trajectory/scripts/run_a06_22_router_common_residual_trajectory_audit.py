#!/usr/bin/env python3
"""A06_22: common/residual router-gap trajectory audit for real-DCLM proxy init."""

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

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

RESEARCH_ROOT = Path("/data/250010109/Research_System")
A06_10_SCRIPT_DIR = RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_04_E01_real_proxy_operationalization/scripts"
A06_12_SCRIPT_DIR = RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_04_E03_real_proxy_training_overwrite/scripts"
for path in [A06_10_SCRIPT_DIR, A06_12_SCRIPT_DIR]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import run_real_dclm_proxy_feature_operationalization as a10
import run_real_dclm_proxy_init_training_preservation as a12


def now_slug() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str), encoding="utf-8")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
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


def finite_float(x: float | np.floating[Any]) -> float:
    y = float(x)
    if math.isfinite(y):
        return y
    return float("nan")


def quantile_or_nan(values: np.ndarray, q: float) -> float:
    values = values[np.isfinite(values)]
    if values.size == 0:
        return float("nan")
    return finite_float(np.quantile(values, q))


def mean_or_nan(values: np.ndarray) -> float:
    values = values[np.isfinite(values)]
    if values.size == 0:
        return float("nan")
    return finite_float(values.mean())


def median_or_nan(values: np.ndarray) -> float:
    values = values[np.isfinite(values)]
    if values.size == 0:
        return float("nan")
    return finite_float(np.median(values))


def orthonormal_rows_from_basis(rows: np.ndarray, rank: int) -> np.ndarray:
    x = np.asarray(rows, dtype=np.float64)
    if x.ndim == 1:
        x = x.reshape(1, -1)
    finite = np.isfinite(x).all(axis=1)
    x = x[finite]
    norms = np.linalg.norm(x, axis=1)
    x = x[norms > 1e-10]
    if x.size == 0:
        return np.zeros((0, rows.shape[-1]), dtype=np.float32)
    try:
        _, _s, vt = np.linalg.svd(x, full_matrices=False)
        keep = min(rank, vt.shape[0])
        return vt[:keep].astype(np.float32)
    except np.linalg.LinAlgError:
        q, _r = np.linalg.qr(x.T)
        keep = min(rank, q.shape[1])
        return q[:, :keep].T.astype(np.float32)


def top_hidden_pc_basis(h: np.ndarray, rank: int) -> np.ndarray:
    x = h.astype(np.float64, copy=False)
    if x.shape[0] < 2:
        return np.zeros((0, x.shape[1]), dtype=np.float32)
    x = x - x.mean(axis=0, keepdims=True)
    cov = (x.T @ x) / max(x.shape[0] - 1, 1)
    try:
        vals, vecs = np.linalg.eigh(cov)
        order = np.argsort(vals)[::-1]
        keep = min(rank, vecs.shape[1])
        return vecs[:, order[:keep]].T.astype(np.float32)
    except np.linalg.LinAlgError:
        return orthonormal_rows_from_basis(x[: min(x.shape[0], 4096)], rank)


def project_vec(basis: np.ndarray, x: np.ndarray) -> np.ndarray:
    if basis.size == 0:
        return np.zeros_like(x)
    return (basis.T @ (basis @ x)).astype(np.float32)


def feature_centers(h: np.ndarray, labels: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    dim = h.shape[1]
    centers = np.zeros((k, dim), dtype=np.float32)
    counts = np.zeros(k, dtype=np.int64)
    for f in range(k):
        mask = labels == f
        counts[f] = int(mask.sum())
        if counts[f] > 0:
            centers[f] = h[mask].mean(axis=0).astype(np.float32)
        else:
            centers[f] = np.nan
    return centers, counts


def majority_route_by_feature(labels: np.ndarray, routes: np.ndarray, k: int, num_experts: int) -> np.ndarray:
    matched = np.full(k, -1, dtype=np.int64)
    for f in range(k):
        mask = labels == f
        if not np.any(mask):
            continue
        counts = np.bincount(routes[mask], minlength=num_experts)
        matched[f] = int(np.argmax(counts))
    return matched


def matched_preserve(labels: np.ndarray, routes: np.ndarray, matched: np.ndarray) -> tuple[float, float]:
    vals = []
    for f, expert in enumerate(matched.tolist()):
        if expert < 0:
            continue
        mask = labels == f
        if np.any(mask):
            vals.append(float(np.mean(routes[mask] == expert)))
    if not vals:
        return float("nan"), float("nan")
    arr = np.array(vals, dtype=np.float64)
    return finite_float(arr.mean()), finite_float(arr.min())


def collect_gate_rows(model: a10.MyQwen3ForCausalLM, layers: list[int]) -> dict[int, np.ndarray]:
    rows: dict[int, np.ndarray] = {}
    keep = set(layers)
    for layer_idx, _mlp, gate in a10.iter_gate_modules(model):
        if layer_idx in keep:
            rows[layer_idx] = gate.weight.detach().float().cpu().numpy().astype(np.float32)
    return rows


def checkpoint_state(
    model: a10.MyQwen3ForCausalLM,
    dataset: a10.PackedBinDataset,
    eval_indices: list[int],
    fixed_labels: dict[int, np.ndarray],
    args: argparse.Namespace,
    device: torch.device,
) -> dict[int, dict[str, np.ndarray]]:
    data = a12.collect_hidden_logits(model, dataset, eval_indices, args, device)
    gate_rows = collect_gate_rows(model, list(data.keys()))
    out: dict[int, dict[str, np.ndarray]] = {}
    for layer, d in data.items():
        n = int(d["logits"].shape[0])
        labels = fixed_labels[layer][:n].astype(np.int64)
        routes = np.argmax(d["logits"], axis=1).astype(np.int64)
        out[layer] = {
            "h": d["h"].astype(np.float32),
            "logits": d["logits"].astype(np.float32),
            "token_id": d["token_id"].astype(np.int64),
            "position": d["position"].astype(np.int64),
            "labels": labels,
            "routes": routes,
            "gate_w": gate_rows[layer],
        }
    return out


def make_projectors(h0: np.ndarray, gate_w0: np.ndarray, args: argparse.Namespace) -> dict[str, np.ndarray]:
    mean = h0.mean(axis=0).astype(np.float32)
    mean_norm = np.linalg.norm(mean)
    if mean_norm > 1e-10:
        mean_basis = (mean / mean_norm).reshape(1, -1).astype(np.float32)
    else:
        mean_basis = np.zeros((0, h0.shape[1]), dtype=np.float32)
    router_rows = gate_w0 - gate_w0.mean(axis=0, keepdims=True)
    return {
        "mean_common": mean_basis,
        "top_hidden_pc": top_hidden_pc_basis(h0, args.common_rank),
        "router_row_subspace": orthonormal_rows_from_basis(router_rows, args.common_rank),
    }


def analyze_layer_checkpoint(
    variant: str,
    seed: int,
    step: int,
    layer: int,
    last_loss: float | None,
    state: dict[str, np.ndarray],
    base: dict[str, Any],
    args: argparse.Namespace,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    h = state["h"]
    labels = state["labels"]
    routes = state["routes"]
    gate_w = state["gate_w"]
    mu_t, counts_t = feature_centers(h, labels, args.num_clusters)
    mu0 = base["mu0"]
    gate_w0 = base["gate_w0"]
    matched = base["matched"]
    projectors: dict[str, np.ndarray] = base["projectors"]
    proxy_nmi = a10.nmi(labels, routes)
    proxy_ari = a10.adjusted_rand(labels, routes)
    preserve_mean, preserve_min = matched_preserve(labels, routes, matched)
    load = a10.entropy_load(routes, args.num_experts)
    inventory_row = {
        "variant": variant,
        "model_seed": seed,
        "step": step,
        "layer": layer,
        "eval_tokens": int(routes.shape[0]),
        "finite_hidden": bool(np.isfinite(h).all()),
        "finite_gate_rows": bool(np.isfinite(gate_w).all()),
        "unique_proxy_labels": int(np.unique(labels).size),
        "unique_routes": int(np.unique(routes).size),
        "lm_loss": last_loss,
        "proxy_route_nmi": proxy_nmi,
    }
    pair_rows: list[dict[str, Any]] = []
    trajectory_rows: list[dict[str, Any]] = []
    for projector_name, basis in projectors.items():
        ratios = []
        update_common_abs = []
        update_residual_abs = []
        gamma_total = []
        gamma_common = []
        gamma_residual = []
        residual_share = []
        sign_flips = []
        identity_errors = []
        gamma0_values = []
        residual_margin0_values = []
        for f in range(args.num_clusters):
            a = int(matched[f])
            if a < 0 or counts_t[f] <= 0 or not np.isfinite(mu0[f]).all() or not np.isfinite(mu_t[f]).all():
                continue
            for e in range(args.num_experts):
                if e == a:
                    continue
                u0 = gate_w0[a] - gate_w0[e]
                ut = gate_w[a] - gate_w[e]
                du = ut - u0
                pc_mu0 = project_vec(basis, mu0[f])
                res_mu0 = mu0[f] - pc_mu0
                pc_mut = project_vec(basis, mu_t[f])
                res_mut = mu_t[f] - pc_mut
                gamma0 = float(u0 @ mu0[f])
                g_t = float(ut @ mu_t[f])
                g_c = float(ut @ pc_mut)
                g_r = float(ut @ res_mut)
                upd_c = float(du @ pc_mu0)
                upd_r = float(du @ res_mu0)
                router_update = float(du @ mu0[f])
                feature_drift = float(u0 @ (mu_t[f] - mu0[f]))
                interaction = float(du @ (mu_t[f] - mu0[f]))
                reconstructed = gamma0 + router_update + feature_drift + interaction
                identity_error = float(g_t - reconstructed)
                ratio = abs(upd_c) / (abs(upd_r) + args.epsilon)
                res_share = abs(g_r) / (abs(g_c) + abs(g_r) + args.epsilon)
                sign_flip = int(g_t <= 0.0)
                pair_rows.append(
                    {
                        "variant": variant,
                        "model_seed": seed,
                        "step": step,
                        "layer": layer,
                        "projector": projector_name,
                        "projector_rank": int(basis.shape[0]),
                        "feature": f,
                        "matched_expert": a,
                        "competitor_expert": e,
                        "feature_count": int(counts_t[f]),
                        "gamma0_total": finite_float(gamma0),
                        "gamma_t_total": finite_float(g_t),
                        "gamma_common": finite_float(g_c),
                        "gamma_residual": finite_float(g_r),
                        "router_update_common": finite_float(upd_c),
                        "router_update_residual": finite_float(upd_r),
                        "router_update_total": finite_float(router_update),
                        "feature_center_drift": finite_float(feature_drift),
                        "interaction_drift": finite_float(interaction),
                        "lambda_pair": finite_float(ratio),
                        "residual_margin_share": finite_float(res_share),
                        "sign_flip": sign_flip,
                        "identity_error": finite_float(identity_error),
                    }
                )
                ratios.append(ratio)
                update_common_abs.append(abs(upd_c))
                update_residual_abs.append(abs(upd_r))
                gamma_total.append(g_t)
                gamma_common.append(g_c)
                gamma_residual.append(g_r)
                residual_share.append(res_share)
                sign_flips.append(float(sign_flip))
                identity_errors.append(abs(identity_error))
                gamma0_values.append(gamma0)
                residual_margin0_values.append(float(u0 @ res_mu0))
        ratios_a = np.array(ratios, dtype=np.float64)
        common_a = np.array(update_common_abs, dtype=np.float64)
        residual_a = np.array(update_residual_abs, dtype=np.float64)
        gamma_a = np.array(gamma_total, dtype=np.float64)
        gamma_c_a = np.array(gamma_common, dtype=np.float64)
        gamma_r_a = np.array(gamma_residual, dtype=np.float64)
        residual_share_a = np.array(residual_share, dtype=np.float64)
        sign_a = np.array(sign_flips, dtype=np.float64)
        err_a = np.array(identity_errors, dtype=np.float64)
        gamma0_a = np.array(gamma0_values, dtype=np.float64)
        residual0_a = np.array(residual_margin0_values, dtype=np.float64)
        row = {
            "variant": variant,
            "model_seed": seed,
            "step": step,
            "layer": layer,
            "projector": projector_name,
            "projector_rank": int(basis.shape[0]),
            "lm_loss": last_loss,
            "eval_tokens": int(routes.shape[0]),
            "proxy_route_nmi": proxy_nmi,
            "proxy_route_ari": proxy_ari,
            "matched_preserve_frac_mean": preserve_mean,
            "matched_preserve_frac_min": preserve_min,
            "route_active_experts": load["active_clusters"],
            "route_active_expert_ratio": load["active_cluster_ratio"],
            "route_max_load": load["max_cluster_load"],
            "route_entropy": load["cluster_entropy"],
            "lambda_upd_median": median_or_nan(ratios_a),
            "lambda_upd_p25": quantile_or_nan(ratios_a, 0.25),
            "lambda_upd_p75": quantile_or_nan(ratios_a, 0.75),
            "update_common_abs_mean": mean_or_nan(common_a),
            "update_residual_abs_mean": mean_or_nan(residual_a),
            "update_common_minus_residual_abs_mean": mean_or_nan(common_a - residual_a),
            "gamma0_total_min": quantile_or_nan(gamma0_a, 0.0),
            "gamma0_residual_min": quantile_or_nan(residual0_a, 0.0),
            "gamma_t_total_min": quantile_or_nan(gamma_a, 0.0),
            "gamma_t_total_median": median_or_nan(gamma_a),
            "gamma_common_abs_mean": mean_or_nan(np.abs(gamma_c_a)),
            "gamma_residual_abs_mean": mean_or_nan(np.abs(gamma_r_a)),
            "residual_margin_share_median": median_or_nan(residual_share_a),
            "sign_flip_rate": mean_or_nan(sign_a),
            "identity_error_max_abs": quantile_or_nan(err_a, 1.0),
            "pair_count": int(ratios_a.size),
        }
        trajectory_rows.append(row)
    return pair_rows, trajectory_rows, [inventory_row]


def train_variant(
    variant: str,
    seed: int,
    dataset: a10.PackedBinDataset,
    args: argparse.Namespace,
    device: torch.device,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    model = a10.make_model(seed, args, device)
    calib_indices = list(range(args.audit_start, args.audit_start + args.seqs_per_split))
    eval_indices = list(range(args.audit_start + 2 * args.seqs_per_split, args.audit_start + 3 * args.seqs_per_split))
    proxies, fixed_labels = a12.fit_step0_proxies(model, dataset, calib_indices, eval_indices, args, device)
    a12.apply_router_init(model, proxies, variant, seed, args)
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=args.learning_rate, weight_decay=0.0)
    train_indices = list(range(args.train_start, args.train_start + args.train_num_sequences))
    random.Random(seed + 17).shuffle(train_indices)
    train_ptr = 0
    last_loss = None
    checkpoints = set(args.checkpoints)
    bases: dict[int, dict[str, Any]] = {}
    pair_rows: list[dict[str, Any]] = []
    trajectory_rows: list[dict[str, Any]] = []
    inventory_rows: list[dict[str, Any]] = []
    for step in range(0, args.max_train_steps + 1):
        if step in checkpoints:
            states = checkpoint_state(model, dataset, eval_indices, fixed_labels, args, device)
            for layer, state in states.items():
                if step == 0:
                    labels = state["labels"]
                    routes = state["routes"]
                    mu0, counts0 = feature_centers(state["h"], labels, args.num_clusters)
                    matched = majority_route_by_feature(labels, routes, args.num_clusters, args.num_experts)
                    bases[layer] = {
                        "mu0": mu0,
                        "counts0": counts0,
                        "matched": matched,
                        "gate_w0": state["gate_w"].copy(),
                        "projectors": make_projectors(state["h"], state["gate_w"], args),
                    }
                if layer not in bases:
                    continue
                p_rows, t_rows, i_rows = analyze_layer_checkpoint(
                    variant=variant,
                    seed=seed,
                    step=step,
                    layer=layer,
                    last_loss=last_loss,
                    state=state,
                    base=bases[layer],
                    args=args,
                )
                pair_rows.extend(p_rows)
                trajectory_rows.extend(t_rows)
                inventory_rows.extend(i_rows)
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
    return pair_rows, trajectory_rows, inventory_rows


def make_figures(run_dir: Path) -> None:
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
    except Exception:
        return
    traj_path = run_dir / "results/router_update_trajectory.csv"
    if not traj_path.exists() or traj_path.stat().st_size == 0:
        return
    df = pd.read_csv(traj_path)
    fig_dir = run_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    nmi = df[df["projector"] == "mean_common"].groupby(["variant", "step"])["proxy_route_nmi"].mean().reset_index()
    plt.figure(figsize=(8, 4))
    for variant, vv in nmi.groupby("variant"):
        plt.plot(vv["step"], vv["proxy_route_nmi"], marker="o", label=variant)
    plt.xlabel("step")
    plt.ylabel("proxy_route_nmi")
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_dir / "proxy_route_nmi_reproduction.png", dpi=160)
    plt.close()

    raw = df[df["variant"] == "raw_center"].copy()
    if not raw.empty:
        lam = raw.groupby(["projector", "step"])["lambda_upd_median"].median().reset_index()
        plt.figure(figsize=(8, 4))
        for projector, vv in lam.groupby("projector"):
            plt.plot(vv["step"], vv["lambda_upd_median"], marker="o", label=projector)
        plt.axhline(1.0, linestyle="--", color="black", linewidth=1)
        plt.xlabel("step")
        plt.ylabel("median Lambda_upd")
        plt.legend()
        plt.tight_layout()
        plt.savefig(fig_dir / "raw_center_lambda_trajectory.png", dpi=160)
        plt.close()

        sub = raw[raw["step"].isin([5, 10])]
        plt.figure(figsize=(8, 4))
        labels = []
        values = []
        for _, row in sub.groupby(["projector", "step"])["lambda_upd_median"].median().reset_index().iterrows():
            labels.append(f"{row['projector']}@{int(row['step'])}")
            values.append(float(row["lambda_upd_median"]))
        if values:
            plt.bar(range(len(values)), values)
            plt.axhline(1.0, linestyle="--", color="black", linewidth=1)
            plt.xticks(range(len(values)), labels, rotation=35, ha="right")
            plt.ylabel("median Lambda_upd")
            plt.tight_layout()
            plt.savefig(fig_dir / "projector_lambda_step5_step10.png", dpi=160)
        plt.close()

        terms = raw.groupby(["projector", "step"])[["update_common_abs_mean", "update_residual_abs_mean"]].mean().reset_index()
        for projector, vv in terms.groupby("projector"):
            plt.figure(figsize=(8, 4))
            plt.plot(vv["step"], vv["update_common_abs_mean"], marker="o", label="common update abs mean")
            plt.plot(vv["step"], vv["update_residual_abs_mean"], marker="o", label="residual update abs mean")
            plt.xlabel("step")
            plt.ylabel("absolute update term")
            plt.title(projector)
            plt.legend()
            plt.tight_layout()
            plt.savefig(fig_dir / f"raw_center_common_residual_update_terms_{projector}.png", dpi=160)
            plt.close()

        scatter = raw[raw["step"].isin([1, 2, 3, 5, 10, 20, 50])]
        plt.figure(figsize=(6, 4))
        for projector, vv in scatter.groupby("projector"):
            plt.scatter(vv["proxy_route_nmi"], vv["lambda_upd_median"], label=projector, alpha=0.7)
        plt.axhline(1.0, linestyle="--", color="black", linewidth=1)
        plt.xlabel("proxy_route_nmi")
        plt.ylabel("median Lambda_upd")
        plt.legend()
        plt.tight_layout()
        plt.savefig(fig_dir / "raw_center_lambda_vs_nmi.png", dpi=160)
        plt.close()


def aggregate(run_dir: Path) -> None:
    pair_rows: list[dict[str, Any]] = []
    trajectory_rows: list[dict[str, Any]] = []
    inventory_rows: list[dict[str, Any]] = []
    for path in sorted((run_dir / "partials").glob("pairs_rank*.jsonl")):
        pair_rows.extend(read_jsonl(path))
    for path in sorted((run_dir / "partials").glob("trajectory_rank*.jsonl")):
        trajectory_rows.extend(read_jsonl(path))
    for path in sorted((run_dir / "partials").glob("inventory_rank*.jsonl")):
        inventory_rows.extend(read_jsonl(path))
    write_csv(run_dir / "results/common_residual_margin_by_pair.csv", pair_rows)
    write_csv(run_dir / "results/router_update_trajectory.csv", trajectory_rows)
    write_csv(run_dir / "results/snapshot_inventory.csv", inventory_rows)
    make_figures(run_dir)
    try:
        import pandas as pd
    except Exception:
        write_json(run_dir / "run_summary.json", {"rows": len(trajectory_rows), "pair_rows": len(pair_rows)})
        return
    if not trajectory_rows:
        write_json(run_dir / "run_summary.json", {"rows": 0, "pair_rows": len(pair_rows)})
        return
    df = pd.DataFrame(trajectory_rows)
    robustness = (
        df[df["step"].isin([5, 10])]
        .groupby(["variant", "projector", "step"])
        .agg(
            lambda_upd_median=("lambda_upd_median", "median"),
            proxy_route_nmi=("proxy_route_nmi", "mean"),
            sign_flip_rate=("sign_flip_rate", "mean"),
            gamma0_residual_min=("gamma0_residual_min", "mean"),
            gamma_t_total_min=("gamma_t_total_min", "mean"),
            identity_error_max_abs=("identity_error_max_abs", "max"),
        )
        .reset_index()
    )
    robustness["lambda_gt_1"] = robustness["lambda_upd_median"] > 1.0
    robustness.to_csv(run_dir / "results/common_projector_robustness.csv", index=False)

    raw_mean = df[(df["variant"] == "raw_center") & (df["projector"] == "mean_common")]
    raw_steps = {}
    for step in [0, 5, 10, 50]:
        sub = raw_mean[raw_mean["step"] == step]
        if not sub.empty:
            raw_steps[str(step)] = {
                "proxy_route_nmi_mean": float(sub["proxy_route_nmi"].mean()),
                "route_max_load_mean": float(sub["route_max_load"].mean()),
                "matched_preserve_frac_min_mean": float(sub["matched_preserve_frac_min"].mean()),
            }
    raw_lambdas = {}
    raw = df[df["variant"] == "raw_center"]
    for projector in sorted(raw["projector"].unique().tolist()):
        raw_lambdas[projector] = {}
        for step in [5, 10]:
            sub = raw[(raw["projector"] == projector) & (raw["step"] == step)]
            if not sub.empty:
                raw_lambdas[projector][str(step)] = {
                    "lambda_upd_median": float(sub["lambda_upd_median"].median()),
                    "update_common_abs_mean": float(sub["update_common_abs_mean"].mean()),
                    "update_residual_abs_mean": float(sub["update_residual_abs_mean"].mean()),
                    "gamma0_residual_min_mean": float(sub["gamma0_residual_min"].mean()),
                    "sign_flip_rate_mean": float(sub["sign_flip_rate"].mean()),
                }
    random_mean = df[(df["variant"] == "random") & (df["projector"] == "mean_common")]
    loss_guard = {}
    for step in [5, 10]:
        raw_sub = raw_mean[raw_mean["step"] == step]
        random_sub = random_mean[random_mean["step"] == step]
        if not raw_sub.empty and not random_sub.empty:
            loss_guard[str(step)] = float(raw_sub["lm_loss"].mean() - random_sub["lm_loss"].mean())
    collapse_reproduced = False
    if "0" in raw_steps and "10" in raw_steps:
        collapse_reproduced = (
            raw_steps["0"]["proxy_route_nmi_mean"] > 0.5
            and raw_steps["10"]["proxy_route_nmi_mean"] < 0.1
        )
    robust_projectors = ["mean_common", "top_hidden_pc", "router_row_subspace"]
    h1_projector_pass = {}
    for projector in robust_projectors:
        vals = []
        for step in ["5", "10"]:
            if projector in raw_lambdas and step in raw_lambdas[projector]:
                vals.append(raw_lambdas[projector][step]["lambda_upd_median"] > 1.0)
        h1_projector_pass[projector] = bool(vals and any(vals))
    h1_supported = bool(collapse_reproduced and all(h1_projector_pass.values()))
    summary = {
        "run_name": run_dir.name,
        "completed_at": dt.datetime.now().isoformat(),
        "trajectory_rows": len(trajectory_rows),
        "pair_rows": len(pair_rows),
        "inventory_rows": len(inventory_rows),
        "collapse_reproduced": collapse_reproduced,
        "h1_common_trajectory_supported": h1_supported,
        "h1_projector_pass": h1_projector_pass,
        "raw_center_steps": raw_steps,
        "raw_center_lambdas": raw_lambdas,
        "loss_delta_raw_minus_random": loss_guard,
        "max_identity_error_abs": float(df["identity_error_max_abs"].max()),
        "primary_decision_rule": "support H1 only if raw_center collapse is reproduced and all robust projectors have Lambda_upd > 1 at step 5 or 10",
    }
    write_json(run_dir / "run_summary.json", summary)


def apply_smoke_overrides(args: argparse.Namespace) -> None:
    if args.run_stage != "smoke":
        return
    args.model_seeds = [args.model_seeds[0]]
    args.variants = [v for v in args.variants if v in {"raw_center", "random"}]
    args.audit_layers = [args.audit_layers[-1] if args.audit_layers else 5]
    args.max_train_steps = min(args.max_train_steps, 5)
    args.checkpoints = [0, 1, 5]
    args.seqs_per_split = min(args.seqs_per_split, 256)
    args.train_num_sequences = min(args.train_num_sequences, 1024)
    args.tokens_per_split_per_layer = min(args.tokens_per_split_per_layer, 4096)
    args.tokens_per_eval_per_layer = min(args.tokens_per_eval_per_layer, 4096)
    args.audit_batch_size = min(args.audit_batch_size, 4)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-name", default=f"a06_22_router_common_residual_trajectory_{now_slug()}")
    parser.add_argument("--run-stage", choices=["smoke", "full"], default="full")
    parser.add_argument("--output-dir", type=Path, default=RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_02_E01_common_residual_trajectory")
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
    parser.add_argument("--common-rank", type=int, default=4)
    parser.add_argument("--epsilon", type=float, default=1e-8)
    parser.add_argument("--aggregate-only", action="store_true")
    args = parser.parse_args()
    apply_smoke_overrides(args)
    return args


def main() -> int:
    args = parse_args()
    run_dir = args.output_dir / "runs/router_common_residual_trajectory" / args.run_name
    if args.aggregate_only:
        aggregate(run_dir)
        return 0
    rank, world, local_rank = setup_dist()
    device = torch.device(f"cuda:{local_rank}" if torch.cuda.is_available() else "cpu")
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
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
                "a06_12_runner_sha256": sha256_file(A06_12_SCRIPT_DIR / "run_real_dclm_proxy_init_training_preservation.py"),
                "moe_root": str(a10.MOE_ROOT),
                "data_path": str(args.data_path),
                "run_stage": args.run_stage,
            },
        )
    barrier()
    dataset = a10.PackedBinDataset(args.data_path)
    tasks = [(variant, seed) for variant in args.variants for seed in args.model_seeds]
    for task_idx, (variant, seed) in enumerate(tasks):
        if task_idx % world != rank:
            continue
        print(f"[rank{rank}] start variant={variant} seed={seed}", flush=True)
        pair_rows, trajectory_rows, inventory_rows = train_variant(variant, seed, dataset, args, device)
        append_jsonl(run_dir / "partials" / f"pairs_rank{rank}.jsonl", pair_rows)
        append_jsonl(run_dir / "partials" / f"trajectory_rank{rank}.jsonl", trajectory_rows)
        append_jsonl(run_dir / "partials" / f"inventory_rank{rank}.jsonl", inventory_rows)
        print(
            f"[rank{rank}] done variant={variant} seed={seed} pairs={len(pair_rows)} trajectory={len(trajectory_rows)}",
            flush=True,
        )
    barrier()
    if rank == 0:
        aggregate(run_dir)
    barrier()
    if dist.is_available() and dist.is_initialized():
        dist.destroy_process_group()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

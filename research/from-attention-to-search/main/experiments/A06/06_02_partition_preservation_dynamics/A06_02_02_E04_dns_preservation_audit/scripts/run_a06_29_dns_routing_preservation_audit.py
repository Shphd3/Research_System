#!/usr/bin/env python3
"""Run A06_29 DNS routing preservation audit."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import os
import time
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.nn import functional as F


EXPERIMENT_ID = "A06_02_02_E04_dns_preservation_audit"
REPO_ROOT = Path(__file__).resolve().parents[7]
A06_28_RUNNER = (
    REPO_ROOT
    / "Projects"
    / "from-attention-to-search"
    / "main"
    / "experiments"
    / "A06"
    / "A06_01_05_E04_full_lm_gradient_guard"
    / "scripts"
    / "run_a06_28_full_sequence_lm_gradient_selector_guard.py"
)


def load_a06_28():
    spec = importlib.util.spec_from_file_location("a06_28", A06_28_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import A06_28 runner at {A06_28_RUNNER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


a28 = load_a06_28()
base = a28.base


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys = sorted({k for row in rows for k in row.keys()})
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_int_list(text: str) -> list[int]:
    return base.parse_int_list(text)


def clone_state(model) -> dict[str, torch.Tensor]:
    return {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}


def load_state(model, state: dict[str, torch.Tensor], device: torch.device) -> None:
    model.load_state_dict({k: v.to(device) for k, v in state.items()})


def generate_batch(args: argparse.Namespace, n: int, slot_len: int, seed: int):
    return base.generate_batch(args, n, slot_len, seed, balanced=True)


def make_model(args: argparse.Namespace, seed: int, device: torch.device):
    return base.make_model(args, seed, device)


def route_slice(x: torch.Tensor, route_pos: torch.Tensor) -> torch.Tensor:
    return base.route_slice(x, route_pos)


def compute_full_lm_loss(logits: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
    pred = logits[:, :-1, :].reshape(-1, logits.shape[-1])
    labels = x[:, 1:].reshape(-1)
    return F.cross_entropy(pred, labels)


def normalize_rows(rows: torch.Tensor, scale: float) -> torch.Tensor:
    return rows.float() / rows.float().norm(dim=1, keepdim=True).clamp_min(1e-8) * float(scale)


def set_router_rows(model, rows: torch.Tensor, scale: float) -> None:
    with torch.no_grad():
        model.moe.router.weight.copy_(normalize_rows(rows, scale).to(model.moe.router.weight.device))


def project_router_rows(model, common_vec: torch.Tensor | None) -> None:
    if common_vec is None:
        return
    c = common_vec.to(model.moe.router.weight.device).float()
    c = c / c.norm().clamp_min(1e-8)
    with torch.no_grad():
        w = model.moe.router.weight.data.float()
        model.moe.router.weight.data = w - (w @ c).unsqueeze(1) * c.unsqueeze(0)


def train_warmup(args: argparse.Namespace, seed: int, slot_len: int, device: torch.device) -> dict[str, torch.Tensor]:
    model = make_model(args, seed + 25000, device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(args.lr), weight_decay=float(args.weight_decay))
    for step in range(1, int(args.warmup_steps) + 1):
        model.train()
        batch = generate_batch(args, int(args.train_batch_size), slot_len, seed + 500000 + step)
        x = batch.x.to(device)
        logits, _info = model(x, common_vec=None)
        loss = compute_full_lm_loss(logits, x)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(args.grad_clip))
        optimizer.step()
    return clone_state(model)


def margin_from_mapping(scores: torch.Tensor, feature: torch.Tensor, mapping: dict[int, int]) -> torch.Tensor:
    target = torch.tensor([mapping[int(f)] for f in feature.detach().cpu().tolist()], dtype=torch.long)
    scores_cpu = scores.detach().cpu().float()
    target_scores = scores_cpu[torch.arange(scores_cpu.shape[0]), target]
    masked = scores_cpu.clone()
    masked[torch.arange(scores_cpu.shape[0]), target] = -1e9
    return target_scores - masked.max(dim=1).values


def p05(values: torch.Tensor) -> float:
    if int(values.numel()) == 0:
        return float("nan")
    vals = torch.sort(values.detach().cpu().float()).values
    idx = max(0, min(int(vals.numel()) - 1, int(math.floor(0.05 * max(0, int(vals.numel()) - 1)))))
    return float(vals[idx].item())


@torch.no_grad()
def collect_eval(model, batch, args, device: torch.device, common_vec: torch.Tensor | None):
    model.eval()
    score_parts = []
    route_parts = []
    proj_parts = []
    loss_sum = 0.0
    correct = 0
    count = 0
    c_hat = None
    if common_vec is not None:
        c_hat = common_vec.detach().cpu().float()
        c_hat = c_hat / c_hat.norm().clamp_min(1e-8)
    for start in range(0, batch.x.shape[0], int(args.eval_batch_size)):
        x = batch.x[start : start + int(args.eval_batch_size)].to(device)
        rp = batch.route_pos[start : start + x.shape[0]].to(device)
        target = batch.target[start : start + x.shape[0]].to(device)
        cv = common_vec.to(device) if common_vec is not None else None
        logits, info = model(x, common_vec=cv)
        route_logits = route_slice(logits, rp)
        scores = route_slice(info["route_scores"], rp)
        assign = scores.argmax(dim=-1)
        loss_sum += float(F.cross_entropy(route_logits, target, reduction="sum").detach().cpu().item())
        correct += int((route_logits.argmax(dim=-1) == target).sum().detach().cpu().item())
        count += int(x.shape[0])
        score_parts.append(scores.detach().cpu())
        route_parts.append(assign.detach().cpu())
        if c_hat is not None:
            route_h = route_slice(info["hidden"], rp).detach().cpu().float()
            proj_parts.append(route_h @ c_hat)
    scores_all = torch.cat(score_parts, dim=0)
    assign_all = torch.cat(route_parts, dim=0)
    if proj_parts:
        proj = torch.cat(proj_parts, dim=0)
    else:
        proj = torch.tensor([], dtype=torch.float)
    return scores_all, assign_all, loss_sum / max(1, count), correct / max(1, count), proj


def router_common_metrics(model, common_vec: torch.Tensor | None) -> dict[str, float]:
    if common_vec is None:
        return {
            "router_common_abs_cos_mean": float("nan"),
            "router_common_abs_cos_max": float("nan"),
        }
    rows = model.moe.router.weight.detach().cpu().float()
    rows = rows / rows.norm(dim=1, keepdim=True).clamp_min(1e-8)
    c = common_vec.detach().cpu().float()
    c = c / c.norm().clamp_min(1e-8)
    vals = (rows @ c).abs()
    return {
        "router_common_abs_cos_mean": float(vals.mean().item()),
        "router_common_abs_cos_max": float(vals.max().item()),
    }


def evaluate_model(
    model,
    batch,
    args: argparse.Namespace,
    device: torch.device,
    condition: str,
    seed: int,
    slot_len: int,
    checkpoint: int,
    common_vec: torch.Tensor | None,
    mapping: dict[int, int] | None,
    step0_margin: torch.Tensor | None,
) -> tuple[dict, dict[int, int], torch.Tensor]:
    scores, assign, loss, acc, proj = collect_eval(model, batch, args, device, common_vec)
    feature = batch.feature.detach().cpu()
    slot_start = batch.slot_start.detach().cpu()
    if mapping is None:
        mapping = base.best_feature_mapping(feature, assign, int(args.num_features), int(args.num_experts))
    matched = torch.tensor([mapping[int(f)] for f in feature.tolist()], dtype=torch.long)
    margin = margin_from_mapping(scores, feature, mapping)
    if step0_margin is not None:
        eligible = step0_margin.detach().cpu() > 0
        sign_flip = float((margin[eligible] <= 0).float().mean().item()) if bool(eligible.any()) else float("nan")
    else:
        sign_flip = 0.0
    row = {
        "experiment_id": EXPERIMENT_ID,
        "condition": condition,
        "seed": seed,
        "slot_len": slot_len,
        "checkpoint": checkpoint,
        "eval_count": int(feature.numel()),
        "loss": loss,
        "target_accuracy": acc,
        "feature_NMI": base.nmi(feature, assign),
        "matched_preserve_fraction": float((assign == matched).float().mean().item()),
        "margin_mean": float(margin.mean().item()),
        "margin_p05": p05(margin),
        "positive_margin_frac": float((margin > 0).float().mean().item()),
        "sign_flip_rate": sign_flip,
        "slot_start_NMI": base.nmi(slot_start, assign),
        "route_common_projection_mean": float(proj.mean().item()) if int(proj.numel()) else float("nan"),
        "route_common_projection_abs_mean": float(proj.abs().mean().item()) if int(proj.numel()) else float("nan"),
        **base.load_metrics(assign, int(args.num_experts)),
        **router_common_metrics(model, common_vec),
    }
    for f, e in mapping.items():
        row[f"map_feature_{f}_expert"] = e
    return row, mapping, margin


def position_zscore_score(score: torch.Tensor, n: int, seq_len: int) -> torch.Tensor:
    s = score.view(n, seq_len).float()
    mu = s.mean(dim=0, keepdim=True)
    std = s.std(dim=0, keepdim=True, unbiased=False).clamp_min(1e-8)
    return ((s - mu) / std).reshape(-1)


def kmeans_rows(x: torch.Tensor, args: argparse.Namespace, seed: int, device: torch.device) -> torch.Tensor:
    return base.kmeans(
        x.float(),
        int(args.num_experts),
        seed,
        int(args.kmeans_n_init),
        int(args.kmeans_max_iter),
        device,
    )


def build_conditions(args, warm_model, calib, seed: int, slot_len: int, device: torch.device) -> tuple[dict[str, dict], dict]:
    states = base.collect_states(warm_model, calib, device, int(args.eval_batch_size))
    all_h = states["all"]
    route_h = states["route"]
    common_all = all_h.mean(dim=0)
    common_route = route_h.mean(dim=0)
    oracle = a28.oracle_centers(route_h, calib.feature, int(args.num_features))
    grad = a28.collect_gradient_signals(warm_model, calib, args, device, "full_lm")
    emb_score = grad["emb_grad_score"]
    n = int(calib.x.shape[0])
    seq_len = int(calib.x.shape[1])
    raw_top1 = a28.topk_indices_per_sample(emb_score, n, seq_len, 1)
    z_top1 = a28.topk_indices_per_sample(position_zscore_score(emb_score, n, seq_len), n, seq_len, 1)
    raw_grad_rows_raw = kmeans_rows(all_h[raw_top1] - all_h[raw_top1].mean(dim=0), args, seed + 1001, device)
    raw_grad_rows_dns = kmeans_rows(all_h[raw_top1] - common_all, args, seed + 1002, device)
    den_grad_rows_dns = kmeans_rows(all_h[z_top1] - common_all, args, seed + 1003, device)
    route_raw = kmeans_rows(route_h - common_route, args, seed + 1101, device)
    route_dns = kmeans_rows(route_h - common_all, args, seed + 1102, device)
    oracle_raw = oracle - common_route
    oracle_dns = oracle - common_all
    conditions = {
        "raw_oracle": {"rows": oracle_raw, "common_vec": None, "router_lr_scale": 1.0, "freeze_steps": 0, "row_project": False},
        "dns_oracle": {"rows": oracle_dns, "common_vec": common_all, "router_lr_scale": 1.0, "freeze_steps": 0, "row_project": False},
        "raw_route_center": {"rows": route_raw, "common_vec": None, "router_lr_scale": 1.0, "freeze_steps": 0, "row_project": False},
        "dns_route_center": {"rows": route_dns, "common_vec": common_all, "router_lr_scale": 1.0, "freeze_steps": 0, "row_project": False},
        "raw_grad_top1": {"rows": raw_grad_rows_raw, "common_vec": None, "router_lr_scale": 1.0, "freeze_steps": 0, "row_project": False},
        "dns_grad_top1": {"rows": raw_grad_rows_dns, "common_vec": common_all, "router_lr_scale": 1.0, "freeze_steps": 0, "row_project": False},
        "dns_denoised_grad_top1": {"rows": den_grad_rows_dns, "common_vec": common_all, "router_lr_scale": 1.0, "freeze_steps": 0, "row_project": False},
        "dns_denoised_grad_top1_rowproj": {"rows": den_grad_rows_dns, "common_vec": common_all, "router_lr_scale": 1.0, "freeze_steps": 0, "row_project": True},
        "dns_denoised_grad_top1_lr01": {"rows": den_grad_rows_dns, "common_vec": common_all, "router_lr_scale": 0.1, "freeze_steps": 0, "row_project": False},
        "dns_denoised_grad_top1_freeze160": {"rows": den_grad_rows_dns, "common_vec": common_all, "router_lr_scale": 1.0, "freeze_steps": 160, "row_project": False},
    }
    meta = a28.flatten_position_meta(calib, args)
    diag = []
    for name, idx in [("raw_grad_top1", raw_top1), ("dns_denoised_grad_top1", z_top1)]:
        row = a28.selector_diag(args, name, emb_score, idx, meta)
        row["condition"] = name
        row["seed"] = seed
        row["slot_len"] = slot_len
        diag.append(row)
    reference = {"common_all": common_all, "common_route": common_route, "selector_diag": diag}
    return conditions, reference


def init_model(args, base_state: dict[str, torch.Tensor], spec: dict, seed: int, device: torch.device):
    model = make_model(args, seed, device)
    load_state(model, base_state, device)
    set_router_rows(model, spec["rows"], float(args.router_init_scale))
    if bool(spec.get("row_project", False)):
        project_router_rows(model, spec.get("common_vec"))
    return model


def make_optimizer(model, args, router_lr_scale: float):
    router_ids = {id(p) for p in model.moe.router.parameters()}
    router_params = [p for p in model.parameters() if id(p) in router_ids]
    other_params = [p for p in model.parameters() if id(p) not in router_ids]
    return torch.optim.AdamW(
        [
            {"params": other_params, "lr": float(args.lr)},
            {"params": router_params, "lr": float(args.lr) * float(router_lr_scale)},
        ],
        weight_decay=float(args.weight_decay),
    )


def train_condition(args, condition: str, spec: dict, base_state: dict[str, torch.Tensor], eval_batch, seed: int, slot_len: int, device: torch.device) -> list[dict]:
    model = init_model(args, base_state, spec, seed + 61000, device)
    optimizer = make_optimizer(model, args, float(spec.get("router_lr_scale", 1.0)))
    checkpoints = sorted(set([0] + parse_int_list(args.checkpoints)))
    checkpoint_set = set(checkpoints)
    common_vec = spec.get("common_vec")
    rows = []
    mapping = None
    step0_margin = None
    row, mapping, step0_margin = evaluate_model(model, eval_batch, args, device, condition, seed, slot_len, 0, common_vec, None, None)
    rows.append(row)
    freeze_steps = int(spec.get("freeze_steps", 0))
    row_project = bool(spec.get("row_project", False))
    router_params = list(model.moe.router.parameters())
    for step in range(1, int(args.train_steps) + 1):
        model.train()
        batch = generate_batch(args, int(args.train_batch_size), slot_len, seed + 800000 + step)
        x = batch.x.to(device)
        cv = common_vec.to(device) if common_vec is not None else None
        logits, _info = model(x, common_vec=cv)
        loss = compute_full_lm_loss(logits, x)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        if step <= freeze_steps:
            for p in router_params:
                p.grad = None
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(args.grad_clip))
        optimizer.step()
        if row_project:
            project_router_rows(model, common_vec)
        if step in checkpoint_set:
            row, _mapping, _margin = evaluate_model(
                model,
                eval_batch,
                args,
                device,
                condition,
                seed,
                slot_len,
                step,
                common_vec,
                mapping,
                step0_margin,
            )
            rows.append(row)
    return rows


def run_cell(args, seed: int, slot_len: int, device: torch.device) -> tuple[list[dict], list[dict], list[dict]]:
    calib = generate_batch(args, int(args.calib_samples), slot_len, seed + 101)
    eval_batch = generate_batch(args, int(args.eval_samples), slot_len, seed + 202)
    data_rows = []
    for split, batch in [("calib", calib), ("eval", eval_batch)]:
        data_rows.append(
            {
                "experiment_id": EXPERIMENT_ID,
                "split": split,
                "seed": seed,
                "slot_len": slot_len,
                "sample_count": int(batch.feature.numel()),
                "feature0_fraction": float((batch.feature == 0).float().mean().item()),
                "feature1_fraction": float((batch.feature == 1).float().mean().item()),
                "feature2_fraction": float((batch.feature == 2).float().mean().item()),
                "feature3_fraction": float((batch.feature == 3).float().mean().item()),
                "slot_start_unique": int(torch.unique(batch.slot_start).numel()),
            }
        )
    warm_state = train_warmup(args, seed, slot_len, device)
    warm_model = make_model(args, seed + 25000, device)
    load_state(warm_model, warm_state, device)
    conditions, reference = build_conditions(args, warm_model, calib, seed + 9700, slot_len, device)
    selected = [m for m in str(args.conditions).replace(",", " ").split() if m.strip()]
    train_rows = []
    diag_rows = []
    for row in reference["selector_diag"]:
        row["experiment_id"] = EXPERIMENT_ID
        diag_rows.append(row)
    for condition in selected:
        if condition not in conditions:
            raise ValueError(f"unknown condition {condition}; available={sorted(conditions)}")
        train_rows.extend(train_condition(args, condition, conditions[condition], warm_state, eval_batch, seed, slot_len, device))
    return data_rows, diag_rows, train_rows


def aggregate_rows(rows: list[dict], keys: list[str], metrics: list[str]) -> list[dict]:
    groups: dict[tuple, list[dict]] = {}
    for row in rows:
        group_key = tuple(row.get(k, "") for k in keys)
        groups.setdefault(group_key, []).append(row)
    out = []
    for group_key, group_rows in sorted(groups.items()):
        base_row = {k: group_key[i] for i, k in enumerate(keys)}
        base_row["n"] = len(group_rows)
        for metric in metrics:
            vals = []
            for row in group_rows:
                try:
                    val = float(row.get(metric, "nan"))
                except (TypeError, ValueError):
                    val = float("nan")
                if not math.isnan(val):
                    vals.append(val)
            base_row[f"{metric}_mean"] = float(np.mean(vals)) if vals else float("nan")
            base_row[f"{metric}_std"] = float(np.std(vals)) if vals else float("nan")
            base_row[f"{metric}_min"] = float(np.min(vals)) if vals else float("nan")
            base_row[f"{metric}_max"] = float(np.max(vals)) if vals else float("nan")
        out.append(base_row)
    return out


def plot_results(traj: list[dict], fig_dir: Path) -> None:
    if not traj:
        return
    labels = {
        "raw_oracle": "raw oracle",
        "dns_oracle": "DNS oracle",
        "raw_route_center": "raw route",
        "dns_route_center": "DNS route",
        "raw_grad_top1": "raw grad top1",
        "dns_grad_top1": "grad top1 + DNS",
        "dns_denoised_grad_top1": "denoised grad + DNS",
        "dns_denoised_grad_top1_rowproj": "denoised + DNS + row proj",
        "dns_denoised_grad_top1_lr01": "denoised + DNS + LR0.1",
        "dns_denoised_grad_top1_freeze160": "denoised + DNS + freeze160",
    }
    order = [c for c in labels if any(str(r["condition"]) == c for r in traj)]
    colors = plt.cm.tab10(np.linspace(0, 1, max(10, len(order))))
    fig_dir.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    for idx, cond in enumerate(order):
        rows = sorted([r for r in traj if str(r["condition"]) == cond], key=lambda r: int(r["checkpoint"]))
        xs = [int(r["checkpoint"]) for r in rows]
        axes[0].plot(xs, [float(r["feature_NMI_mean"]) for r in rows], marker="o", linewidth=1.8, label=labels[cond], color=colors[idx])
        axes[1].plot(xs, [float(r["margin_p05_mean"]) for r in rows], marker="o", linewidth=1.8, label=labels[cond], color=colors[idx])
    axes[0].set_title("Feature NMI trajectory")
    axes[0].set_ylabel("Feature NMI")
    axes[0].set_ylim(0, 1.05)
    axes[1].set_title("Margin p05 trajectory")
    axes[1].set_ylabel("Margin p05")
    axes[1].axhline(0, color="black", linewidth=1)
    for ax in axes:
        ax.set_xlabel("post-reinit step")
        ax.grid(axis="y", alpha=0.25)
    axes[1].legend(fontsize=7, loc="lower left")
    fig.suptitle("A06_29 DNS routing preservation audit", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(fig_dir / "a06_29_dns_margin_trajectory.png", dpi=220)
    plt.close(fig)
    final_step = max(int(r["checkpoint"]) for r in traj)
    final = [r for r in traj if int(r["checkpoint"]) == final_step]
    final_by = {str(r["condition"]): r for r in final}
    xs = np.arange(len(order))
    fig2, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    nmi = [float(final_by[c]["feature_NMI_mean"]) for c in order]
    margin = [float(final_by[c]["margin_p05_mean"]) for c in order]
    axes[0].bar(xs, nmi, color=colors[: len(order)])
    axes[0].set_title(f"Feature NMI at step {final_step}")
    axes[0].set_ylim(0, 1.05)
    axes[1].bar(xs, margin, color=colors[: len(order)])
    axes[1].set_title(f"Margin p05 at step {final_step}")
    axes[1].axhline(0, color="black", linewidth=1)
    for ax in axes:
        ax.set_xticks(xs)
        ax.set_xticklabels([labels[c] for c in order], rotation=35, ha="right")
        ax.grid(axis="y", alpha=0.2)
    fig2.suptitle("A06_29 final state", fontsize=14)
    fig2.tight_layout(rect=[0, 0, 1, 0.93])
    fig2.savefig(fig_dir / "a06_29_dns_final_step2000.png", dpi=220)
    plt.close(fig2)


def summarize(output_dir: Path, args: argparse.Namespace, run_name: str) -> dict:
    partial_dir = output_dir / "partials" / run_name
    data_rows = []
    diag_rows = []
    train_rows = []
    for path in sorted(partial_dir.glob("data_rank*.csv")):
        data_rows.extend(read_csv(path))
    for path in sorted(partial_dir.glob("diag_rank*.csv")):
        diag_rows.extend(read_csv(path))
    for path in sorted(partial_dir.glob("train_rank*.csv")):
        train_rows.extend(read_csv(path))
    table_dir = output_dir / "tables"
    fig_dir = output_dir / "figures"
    write_csv(table_dir / "data_audit.csv", data_rows)
    write_csv(table_dir / "selector_diagnostics.csv", diag_rows)
    write_csv(table_dir / "training_trajectory.csv", train_rows)
    metrics = [
        "feature_NMI",
        "matched_preserve_fraction",
        "margin_mean",
        "margin_p05",
        "positive_margin_frac",
        "sign_flip_rate",
        "slot_start_NMI",
        "max_load",
        "effective_experts",
        "target_accuracy",
        "loss",
        "router_common_abs_cos_mean",
        "router_common_abs_cos_max",
        "route_common_projection_mean",
        "route_common_projection_abs_mean",
    ]
    diag_metrics = [
        "selection_count",
        "selection_route_frac",
        "selection_slot_frac",
        "selection_target_frac",
        "top1_route_frac",
        "top1_slot_frac",
        "top1_target_frac",
        "score_route_share",
        "score_slot_share",
        "score_target_share",
    ]
    traj = aggregate_rows(train_rows, ["condition", "checkpoint"], metrics)
    reinit = aggregate_rows([r for r in train_rows if int(r["checkpoint"]) == 0], ["condition"], metrics)
    final_step = max([int(r["checkpoint"]) for r in train_rows] or [0])
    final = aggregate_rows([r for r in train_rows if int(r["checkpoint"]) == final_step], ["condition"], metrics)
    by_slot_final = aggregate_rows([r for r in train_rows if int(r["checkpoint"]) == final_step], ["condition", "slot_len"], metrics)
    diag = aggregate_rows(diag_rows, ["condition"], diag_metrics)
    write_csv(table_dir / "condition_trajectory_aggregate.csv", traj)
    write_csv(table_dir / "condition_aggregate_reinit.csv", reinit)
    write_csv(table_dir / "condition_aggregate_final.csv", final)
    write_csv(table_dir / "condition_final_by_slot.csv", by_slot_final)
    write_csv(table_dir / "selector_diagnostics_aggregate.csv", diag)
    plot_results(traj, fig_dir)

    def find(rows: list[dict], condition: str, metric: str) -> float:
        for row in rows:
            if str(row.get("condition")) == condition:
                return float(row.get(f"{metric}_mean", "nan"))
        return float("nan")

    key = {
        "completed_cells": len({(r["seed"], r["slot_len"]) for r in train_rows}),
        "completed_training_rows": len(train_rows),
        "final_step": final_step,
        "raw_grad_top1_final_nmi": find(final, "raw_grad_top1", "feature_NMI"),
        "raw_grad_top1_final_margin": find(final, "raw_grad_top1", "margin_p05"),
        "dns_grad_top1_final_nmi": find(final, "dns_grad_top1", "feature_NMI"),
        "dns_grad_top1_final_margin": find(final, "dns_grad_top1", "margin_p05"),
        "dns_denoised_final_nmi": find(final, "dns_denoised_grad_top1", "feature_NMI"),
        "dns_denoised_final_margin": find(final, "dns_denoised_grad_top1", "margin_p05"),
        "dns_denoised_rowproj_final_margin": find(final, "dns_denoised_grad_top1_rowproj", "margin_p05"),
        "dns_denoised_lr01_final_margin": find(final, "dns_denoised_grad_top1_lr01", "margin_p05"),
        "dns_denoised_freeze160_final_margin": find(final, "dns_denoised_grad_top1_freeze160", "margin_p05"),
        "dns_oracle_final_margin": find(final, "dns_oracle", "margin_p05"),
        "raw_oracle_final_margin": find(final, "raw_oracle", "margin_p05"),
    }
    best_margin = max(
        key["dns_grad_top1_final_margin"],
        key["dns_denoised_final_margin"],
        key["dns_denoised_rowproj_final_margin"],
        key["dns_denoised_lr01_final_margin"],
        key["dns_denoised_freeze160_final_margin"],
    )
    if best_margin > key["raw_grad_top1_final_margin"] + 1.0:
        verdict = "dns_or_preservation_improves_margin"
    else:
        verdict = "dns_or_preservation_not_supported"
    summary = {
        "experiment_id": EXPERIMENT_ID,
        "run_name": run_name,
        "run_stage": args.run_stage,
        "verdict": verdict,
        "key_metrics": key,
        "config": vars(args),
        "generated_at_unix": time.time(),
        "tables": {
            "training_trajectory": str(table_dir / "training_trajectory.csv"),
            "condition_trajectory_aggregate": str(table_dir / "condition_trajectory_aggregate.csv"),
            "condition_aggregate_final": str(table_dir / "condition_aggregate_final.csv"),
            "condition_final_by_slot": str(table_dir / "condition_final_by_slot.csv"),
            "selector_diagnostics_aggregate": str(table_dir / "selector_diagnostics_aggregate.csv"),
        },
        "figures": {
            "margin_trajectory": str(fig_dir / "a06_29_dns_margin_trajectory.png"),
            "final_step": str(fig_dir / "a06_29_dns_final_step2000.png"),
        },
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-stage", choices=["smoke", "full"], default="full")
    parser.add_argument("--run-name", default=f"{EXPERIMENT_ID}_{int(time.time())}")
    parser.add_argument("--output-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--seeds", default="0 1 2 3 4 5 6 7")
    parser.add_argument("--slot-lengths", default="1 2 4 8")
    parser.add_argument("--warmup-steps", type=int, default=40)
    parser.add_argument("--conditions", default=(
        "raw_oracle dns_oracle raw_route_center dns_route_center "
        "raw_grad_top1 dns_grad_top1 dns_denoised_grad_top1 "
        "dns_denoised_grad_top1_rowproj dns_denoised_grad_top1_lr01 dns_denoised_grad_top1_freeze160"
    ))
    parser.add_argument("--seq-len", type=int, default=32)
    parser.add_argument("--slot-starts", default="2 10 18")
    parser.add_argument("--num-features", type=int, default=4)
    parser.add_argument("--num-experts", type=int, default=4)
    parser.add_argument("--num-neutral-tokens", type=int, default=32)
    parser.add_argument("--common-prob", type=float, default=0.25)
    parser.add_argument("--d-model", type=int, default=64)
    parser.add_argument("--num-heads", type=int, default=4)
    parser.add_argument("--d-ff", type=int, default=128)
    parser.add_argument("--calib-samples", type=int, default=2048)
    parser.add_argument("--eval-samples", type=int, default=2048)
    parser.add_argument("--train-batch-size", type=int, default=256)
    parser.add_argument("--eval-batch-size", type=int, default=512)
    parser.add_argument("--train-steps", type=int, default=2000)
    parser.add_argument("--checkpoints", default="0 160 500 1000 2000")
    parser.add_argument("--lr", type=float, default=2e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--grad-clip", type=float, default=1.0)
    parser.add_argument("--router-init-scale", type=float, default=1.5)
    parser.add_argument("--kmeans-n-init", type=int, default=4)
    parser.add_argument("--kmeans-max-iter", type=int, default=40)
    parser.add_argument("--grad-batch-size", type=int, default=256)
    parser.add_argument("--selector-topks", default="1")
    args = parser.parse_args()
    if args.run_stage == "smoke":
        args.seeds = "0"
        args.slot_lengths = "1"
        args.train_steps = 5
        args.checkpoints = "0 2 5"
        args.warmup_steps = 2
        args.calib_samples = 256
        args.eval_samples = 256
        args.train_batch_size = 64
        args.eval_batch_size = 128
        args.grad_batch_size = 64
        args.kmeans_n_init = 2
        args.kmeans_max_iter = 8
        args.conditions = "raw_grad_top1 dns_grad_top1 dns_denoised_grad_top1 dns_denoised_grad_top1_rowproj"
    output_dir = Path(args.output_dir)
    rank, local_rank, world_size = base.local_rank_world()
    dist_enabled = base.init_dist_if_needed(world_size)
    if torch.cuda.is_available():
        device = torch.device(f"cuda:{local_rank % torch.cuda.device_count()}")
        torch.cuda.set_device(device)
    else:
        device = torch.device("cpu")
    seeds = parse_int_list(args.seeds)
    slot_lengths = parse_int_list(args.slot_lengths)
    tasks = [(seed, slot_len) for seed in seeds for slot_len in slot_lengths]
    my_tasks = [task for i, task in enumerate(tasks) if i % world_size == rank]
    partial_dir = output_dir / "partials" / args.run_name
    partial_dir.mkdir(parents=True, exist_ok=True)
    print(json.dumps({"event": "start", "rank": rank, "world_size": world_size, "device": str(device), "tasks": my_tasks}), flush=True)
    data_rows: list[dict] = []
    diag_rows: list[dict] = []
    train_rows: list[dict] = []
    for seed, slot_len in my_tasks:
        cell_data, cell_diag, cell_train = run_cell(args, seed, slot_len, device)
        data_rows.extend(cell_data)
        diag_rows.extend(cell_diag)
        train_rows.extend(cell_train)
        print(json.dumps({"event": "cell_done", "rank": rank, "seed": seed, "slot_len": slot_len}), flush=True)
    write_csv(partial_dir / f"data_rank{rank}.csv", data_rows)
    write_csv(partial_dir / f"diag_rank{rank}.csv", diag_rows)
    write_csv(partial_dir / f"train_rank{rank}.csv", train_rows)
    base.dist_barrier(dist_enabled)
    if rank == 0:
        summary = summarize(output_dir, args, args.run_name)
        print(json.dumps({"event": "summary", "summary": summary}, indent=2), flush=True)
    base.dist_barrier(dist_enabled)


if __name__ == "__main__":
    main()

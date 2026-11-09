#!/usr/bin/env python3
"""Run A06_25 warmup and expert-spectral router reinitialization audit."""

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


EXPERIMENT_ID = "A06_01_05_E01_warmup_spectral_reinit"
BASE_RUNNER = (
    Path(__file__).resolve().parents[2]
    / "A06_02_02_E03_transformer_common_rare"
    / "scripts"
    / "run_a06_24_synthetic_common_rare_transformer_moe.py"
)


def load_base_module():
    spec = importlib.util.spec_from_file_location("a06_24_base", BASE_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import base runner at {BASE_RUNNER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_base_module()


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


def normalize_rows(rows: torch.Tensor, scale: float) -> torch.Tensor:
    return rows / rows.norm(dim=1, keepdim=True).clamp_min(1e-8) * float(scale)


def project_out(rows: torch.Tensor, direction: torch.Tensor) -> torch.Tensor:
    c = direction.float()
    c = c / c.norm().clamp_min(1e-8)
    return rows.float() - (rows.float() @ c).unsqueeze(1) * c.unsqueeze(0)


def orthogonalize_rows(rows: torch.Tensor) -> torch.Tensor:
    q, _r = torch.linalg.qr(rows.float().T, mode="reduced")
    return q.T.contiguous()


def set_router_rows(model, rows: torch.Tensor, scale: float) -> None:
    with torch.no_grad():
        model.moe.router.weight.copy_(normalize_rows(rows, scale).to(model.moe.router.weight.device))


def route_slice(x: torch.Tensor, route_pos: torch.Tensor) -> torch.Tensor:
    return base.route_slice(x, route_pos)


def generate_uniform_batch(args: argparse.Namespace, n: int, slot_len: int, seed: int):
    batch = base.generate_batch(args, n, slot_len, seed, balanced=True)
    return batch


def clone_state(model) -> dict[str, torch.Tensor]:
    return {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}


def load_state(model, state: dict[str, torch.Tensor], device: torch.device) -> None:
    model.load_state_dict({k: v.to(device) for k, v in state.items()})


def make_model(args: argparse.Namespace, seed: int, device: torch.device):
    return base.make_model(args, seed, device)


def train_warmup_states(
    args: argparse.Namespace,
    seed: int,
    slot_len: int,
    device: torch.device,
) -> dict[int, dict[str, torch.Tensor]]:
    warm_steps = sorted(set(parse_int_list(args.warmup_steps)))
    max_warm = max(warm_steps)
    model = make_model(args, seed + 25000, device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(args.lr), weight_decay=float(args.weight_decay))
    states: dict[int, dict[str, torch.Tensor]] = {}
    if 0 in warm_steps:
        states[0] = clone_state(model)
    for step in range(1, max_warm + 1):
        model.train()
        batch = generate_uniform_batch(args, int(args.train_batch_size), slot_len, seed + 500000 + step)
        x = batch.x.to(device)
        rp = batch.route_pos.to(device)
        target = batch.target.to(device)
        logits, _info = model(x, common_vec=None)
        route_logits = route_slice(logits, rp)
        loss = F.cross_entropy(route_logits, target)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(args.grad_clip))
        optimizer.step()
        if step in warm_steps:
            states[step] = clone_state(model)
    return states


@torch.no_grad()
def collect_route_scores(model, batch, args, device: torch.device):
    model.eval()
    score_parts = []
    route_parts = []
    loss_sum = 0.0
    correct = 0
    count = 0
    for start in range(0, batch.x.shape[0], int(args.eval_batch_size)):
        x = batch.x[start : start + int(args.eval_batch_size)].to(device)
        rp = batch.route_pos[start : start + x.shape[0]].to(device)
        target = batch.target[start : start + x.shape[0]].to(device)
        logits, info = model(x, common_vec=None)
        route_logits = route_slice(logits, rp)
        scores = route_slice(info["route_scores"], rp)
        assign = scores.argmax(dim=-1)
        loss_sum += float(F.cross_entropy(route_logits, target, reduction="sum").detach().cpu().item())
        correct += int((route_logits.argmax(dim=-1) == target).sum().detach().cpu().item())
        count += int(x.shape[0])
        score_parts.append(scores.detach().cpu())
        route_parts.append(assign.detach().cpu())
    return torch.cat(score_parts, dim=0), torch.cat(route_parts, dim=0), loss_sum / max(1, count), correct / max(1, count)


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
    sorted_values = torch.sort(values.detach().cpu().float()).values
    idx = max(0, min(int(sorted_values.numel()) - 1, int(math.floor(0.05 * max(0, int(sorted_values.numel()) - 1)))))
    return float(sorted_values[idx].item())


def evaluate_model(
    model,
    batch,
    args: argparse.Namespace,
    device: torch.device,
    condition: str,
    seed: int,
    slot_len: int,
    warmup_step: int,
    method: str,
    checkpoint: int,
    mapping: dict[int, int] | None,
    step0_margin: torch.Tensor | None,
) -> tuple[dict, dict[int, int], torch.Tensor]:
    scores, assign, loss, acc = collect_route_scores(model, batch, args, device)
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
        "method": method,
        "warmup_step": warmup_step,
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
        **base.load_metrics(assign, int(args.num_experts)),
    }
    for f, e in mapping.items():
        row[f"map_feature_{f}_expert"] = e
    return row, mapping, margin


def expert_svd_rows(model, align_to_router: bool = True) -> torch.Tensor:
    rows = []
    router_rows = model.moe.router.weight.detach().cpu().float()
    for e, expert in enumerate(model.moe.experts):
        first = expert[0].weight.detach().cpu().float()
        _u, _s, vh = torch.linalg.svd(first, full_matrices=False)
        v = vh[0].clone()
        if align_to_router and float(torch.dot(v, router_rows[e])) < 0:
            v = -v
        rows.append(v)
    return torch.stack(rows, dim=0)


def oracle_centers(route_states: torch.Tensor, feature: torch.Tensor, num_features: int) -> torch.Tensor:
    return base.oracle_centers(route_states, feature, num_features)


def build_rows_for_warmup(
    args: argparse.Namespace,
    warm_model,
    calib,
    seed: int,
    device: torch.device,
) -> tuple[dict[str, torch.Tensor | None], dict[str, dict]]:
    states = base.collect_states(warm_model, calib, device, int(args.eval_batch_size))
    all_h = states["all"]
    route_h = states["route"]
    common_all = all_h.mean(dim=0)
    common_route = route_h.mean(dim=0)
    all_rows = base.kmeans(
        all_h - common_all,
        int(args.num_experts),
        seed + 7001,
        int(args.kmeans_n_init),
        int(args.kmeans_max_iter),
        device,
    )
    route_rows = base.kmeans(
        route_h - common_route,
        int(args.num_experts),
        seed + 7101,
        int(args.kmeans_n_init),
        int(args.kmeans_max_iter),
        device,
    )
    oracle_rows = oracle_centers(route_h, calib.feature, int(args.num_features)) - common_route
    svd = expert_svd_rows(warm_model)
    svd_decommon = project_out(svd, common_route)
    svd_orth = orthogonalize_rows(svd)
    rows: dict[str, torch.Tensor | None] = {
        "no_reinit": None,
        "allpos_centered": all_rows,
        "route_centered": route_rows,
        "oracle_centered": oracle_rows,
        "expert_svd": svd,
        "expert_svd_decommon": svd_decommon,
        "expert_svd_orth": svd_orth,
    }
    reference = {
        "common_all": common_all,
        "common_route": common_route,
        "route_feature_centers": oracle_centers(route_h, calib.feature, int(args.num_features)),
        "current_router_rows": warm_model.moe.router.weight.detach().cpu().float(),
    }
    return rows, reference


def cosine_matrix(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    aa = a.float() / a.float().norm(dim=1, keepdim=True).clamp_min(1e-8)
    bb = b.float() / b.float().norm(dim=1, keepdim=True).clamp_min(1e-8)
    return aa @ bb.T


def diagnostics_for_rows(
    args: argparse.Namespace,
    rows: torch.Tensor,
    reference: dict,
    condition: str,
    method: str,
    warmup_step: int,
    seed: int,
    slot_len: int,
) -> dict:
    rows = normalize_rows(rows.detach().cpu().float(), 1.0)
    n = rows.shape[0]
    pair = cosine_matrix(rows, rows).abs()
    off = pair[~torch.eye(n, dtype=torch.bool)]
    common = reference["common_route"].float().view(1, -1)
    common_cos = cosine_matrix(rows, common).abs().view(-1)
    feature_centers = reference["route_feature_centers"].float()
    feat_cos = cosine_matrix(rows, feature_centers).abs()
    current_cos = cosine_matrix(rows, reference["current_router_rows"].float()).abs()
    center_scores = feature_centers @ rows.T
    center_assign = center_scores.argmax(dim=1)
    center_feature = torch.arange(int(args.num_features), dtype=torch.long)
    center_mapping = base.best_feature_mapping(center_feature, center_assign, int(args.num_features), int(args.num_experts))
    center_margin = margin_from_mapping(center_scores, center_feature, center_mapping)
    return {
        "experiment_id": EXPERIMENT_ID,
        "condition": condition,
        "method": method,
        "warmup_step": warmup_step,
        "seed": seed,
        "slot_len": slot_len,
        "row_pair_abs_cos_mean": float(off.mean().item()) if int(off.numel()) else float("nan"),
        "row_pair_abs_cos_max": float(off.max().item()) if int(off.numel()) else float("nan"),
        "common_abs_cos_mean": float(common_cos.mean().item()),
        "common_abs_cos_max": float(common_cos.max().item()),
        "feature_center_abs_cos_best_mean": float(feat_cos.max(dim=0).values.mean().item()),
        "feature_center_abs_cos_best_min": float(feat_cos.max(dim=0).values.min().item()),
        "current_router_abs_cos_diag_mean": float(torch.diag(current_cos).mean().item()),
        "center_margin_mean": float(center_margin.mean().item()),
        "center_margin_p05": p05(center_margin),
    }


def init_condition_model(
    args: argparse.Namespace,
    base_state: dict[str, torch.Tensor],
    rows: torch.Tensor | None,
    seed: int,
    device: torch.device,
):
    model = make_model(args, seed, device)
    load_state(model, base_state, device)
    if rows is not None:
        set_router_rows(model, rows, float(args.router_init_scale))
    return model


def train_after_reinit(
    args: argparse.Namespace,
    condition: str,
    method: str,
    warmup_step: int,
    model,
    eval_batch,
    seed: int,
    slot_len: int,
    device: torch.device,
) -> list[dict]:
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(args.lr), weight_decay=float(args.weight_decay))
    checkpoints = sorted(set([0] + parse_int_list(args.checkpoints)))
    checkpoint_set = set(checkpoints)
    rows = []
    mapping = None
    step0_margin = None
    row, mapping, step0_margin = evaluate_model(
        model, eval_batch, args, device, condition, seed, slot_len, warmup_step, method, 0, None, None
    )
    rows.append(row)
    for step in range(1, int(args.train_steps) + 1):
        model.train()
        batch = generate_uniform_batch(args, int(args.train_batch_size), slot_len, seed + 800000 + warmup_step * 1000 + step)
        x = batch.x.to(device)
        rp = batch.route_pos.to(device)
        target = batch.target.to(device)
        logits, _info = model(x, common_vec=None)
        route_logits = route_slice(logits, rp)
        loss = F.cross_entropy(route_logits, target)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(args.grad_clip))
        optimizer.step()
        if step in checkpoint_set:
            row, _mapping, _margin = evaluate_model(
                model,
                eval_batch,
                args,
                device,
                condition,
                seed,
                slot_len,
                warmup_step,
                method,
                step,
                mapping,
                step0_margin,
            )
            rows.append(row)
    return rows


def run_cell(args: argparse.Namespace, seed: int, slot_len: int, device: torch.device) -> tuple[list[dict], list[dict], list[dict]]:
    calib = generate_uniform_batch(args, int(args.calib_samples), slot_len, seed + 101)
    eval_batch = generate_uniform_batch(args, int(args.eval_samples), slot_len, seed + 202)
    data_rows = [
        {
            "experiment_id": EXPERIMENT_ID,
            "split": "calib",
            "seed": seed,
            "slot_len": slot_len,
            "sample_count": int(calib.feature.numel()),
            "feature0_fraction": float((calib.feature == 0).float().mean().item()),
            "feature1_fraction": float((calib.feature == 1).float().mean().item()),
            "feature2_fraction": float((calib.feature == 2).float().mean().item()),
            "feature3_fraction": float((calib.feature == 3).float().mean().item()),
            "slot_start_unique": int(torch.unique(calib.slot_start).numel()),
        },
        {
            "experiment_id": EXPERIMENT_ID,
            "split": "eval",
            "seed": seed,
            "slot_len": slot_len,
            "sample_count": int(eval_batch.feature.numel()),
            "feature0_fraction": float((eval_batch.feature == 0).float().mean().item()),
            "feature1_fraction": float((eval_batch.feature == 1).float().mean().item()),
            "feature2_fraction": float((eval_batch.feature == 2).float().mean().item()),
            "feature3_fraction": float((eval_batch.feature == 3).float().mean().item()),
            "slot_start_unique": int(torch.unique(eval_batch.slot_start).numel()),
        },
    ]
    warm_states = train_warmup_states(args, seed, slot_len, device)
    train_rows: list[dict] = []
    diag_rows: list[dict] = []
    methods = [m for m in str(args.methods).replace(",", " ").split() if m.strip()]
    for warmup_step in sorted(warm_states):
        warm_model = make_model(args, seed + 25000, device)
        load_state(warm_model, warm_states[warmup_step], device)
        row_map, reference = build_rows_for_warmup(args, warm_model, calib, seed + warmup_step * 97, device)
        for method in methods:
            if method not in row_map:
                raise ValueError(f"unknown method {method}")
            rows = row_map[method]
            condition = f"w{warmup_step}_{method}"
            if rows is not None:
                diag_rows.append(diagnostics_for_rows(args, rows, reference, condition, method, warmup_step, seed, slot_len))
            else:
                diag_rows.append(
                    diagnostics_for_rows(
                        args,
                        reference["current_router_rows"],
                        reference,
                        condition,
                        method,
                        warmup_step,
                        seed,
                        slot_len,
                    )
                )
            model = init_condition_model(args, warm_states[warmup_step], rows, seed + 61000 + warmup_step, device)
            train_rows.extend(train_after_reinit(args, condition, method, warmup_step, model, eval_batch, seed, slot_len, device))
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


def plot_metric_by_method_warm(rows: list[dict], metric: str, title: str, path: Path) -> None:
    methods = sorted({str(r["method"]) for r in rows})
    warmups = sorted({int(r["warmup_step"]) for r in rows})
    width = 0.8 / max(1, len(methods))
    xs = np.arange(len(warmups))
    plt.figure(figsize=(10.5, 5.2))
    for idx, method in enumerate(methods):
        vals = []
        for warm in warmups:
            found = [
                float(r[f"{metric}_mean"])
                for r in rows
                if str(r["method"]) == method and int(r["warmup_step"]) == warm and f"{metric}_mean" in r
            ]
            vals.append(float(np.mean(found)) if found else float("nan"))
        plt.bar(xs + (idx - (len(methods) - 1) / 2) * width, vals, width=width, label=method)
    plt.xticks(xs, [str(w) for w in warmups])
    plt.xlabel("warmup steps")
    plt.ylabel(metric)
    plt.title(title)
    plt.legend(fontsize=7, ncol=2)
    plt.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=180)
    plt.close()


def plot_trajectory(rows: list[dict], metric: str, title: str, path: Path, keep_methods: set[str]) -> None:
    conds = sorted({str(r["condition"]) for r in rows if str(r.get("method")) in keep_methods})
    plt.figure(figsize=(10.5, 5.4))
    for cond in conds:
        cond_rows = sorted([r for r in rows if str(r["condition"]) == cond], key=lambda r: int(r["checkpoint"]))
        xs = [int(r["checkpoint"]) for r in cond_rows]
        ys = [float(r[f"{metric}_mean"]) for r in cond_rows]
        plt.plot(xs, ys, marker="o", linewidth=1.4, label=cond)
    plt.xlabel("post-reinit checkpoint")
    plt.ylabel(metric)
    plt.title(title)
    plt.legend(fontsize=7, ncol=2)
    plt.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=180)
    plt.close()


def summarize_and_plot(output_dir: Path, args: argparse.Namespace, run_name: str) -> dict:
    partial_dir = output_dir / "partials" / run_name
    data_rows: list[dict] = []
    diag_rows: list[dict] = []
    train_rows: list[dict] = []
    for path in sorted(partial_dir.glob("data_audit_rank*.csv")):
        data_rows.extend(read_csv(path))
    for path in sorted(partial_dir.glob("spectral_diagnostics_rank*.csv")):
        diag_rows.extend(read_csv(path))
    for path in sorted(partial_dir.glob("training_trajectory_rank*.csv")):
        train_rows.extend(read_csv(path))
    table_dir = output_dir / "tables"
    fig_dir = output_dir / "figures"
    write_csv(table_dir / "data_audit.csv", data_rows)
    write_csv(table_dir / "spectral_diagnostics.csv", diag_rows)
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
    ]
    diag_metrics = [
        "row_pair_abs_cos_mean",
        "row_pair_abs_cos_max",
        "common_abs_cos_mean",
        "common_abs_cos_max",
        "feature_center_abs_cos_best_mean",
        "feature_center_abs_cos_best_min",
        "current_router_abs_cos_diag_mean",
        "center_margin_mean",
        "center_margin_p05",
    ]
    condition_trajectory = aggregate_rows(train_rows, ["condition", "method", "warmup_step", "checkpoint"], metrics)
    final_step = max(int(r["checkpoint"]) for r in train_rows) if train_rows else 0
    reinit_rows = [r for r in train_rows if int(r["checkpoint"]) == 0]
    final_rows = [r for r in train_rows if int(r["checkpoint"]) == final_step]
    condition_reinit = aggregate_rows(reinit_rows, ["condition", "method", "warmup_step"], metrics)
    condition_final = aggregate_rows(final_rows, ["condition", "method", "warmup_step"], metrics)
    diag_agg = aggregate_rows(diag_rows, ["condition", "method", "warmup_step"], diag_metrics)
    write_csv(table_dir / "condition_trajectory_aggregate.csv", condition_trajectory)
    write_csv(table_dir / "condition_aggregate_reinit.csv", condition_reinit)
    write_csv(table_dir / "condition_aggregate_final.csv", condition_final)
    write_csv(table_dir / "spectral_diagnostics_aggregate.csv", diag_agg)
    if condition_reinit:
        plot_metric_by_method_warm(condition_reinit, "feature_NMI", "Immediate feature NMI after router reinit", fig_dir / "reinit_feature_nmi_by_method_warmup.png")
        plot_metric_by_method_warm(condition_reinit, "margin_p05", "Immediate margin p05 after router reinit", fig_dir / "reinit_margin_p05_by_method_warmup.png")
    if condition_final:
        plot_metric_by_method_warm(condition_final, "feature_NMI", "Final feature NMI after post-reinit training", fig_dir / "final_feature_nmi_by_method_warmup.png")
        plot_metric_by_method_warm(condition_final, "margin_p05", "Final margin p05 after post-reinit training", fig_dir / "final_margin_p05_by_method_warmup.png")
    if condition_trajectory:
        keep = {"allpos_centered", "route_centered", "expert_svd", "expert_svd_decommon", "expert_svd_orth"}
        plot_trajectory(condition_trajectory, "feature_NMI", "Feature NMI trajectory for central methods", fig_dir / "feature_nmi_trajectory_central_methods.png", keep)
    if diag_agg:
        plot_metric_by_method_warm(diag_agg, "common_abs_cos_mean", "Expert/source row common alignment", fig_dir / "diagnostic_common_alignment_by_method_warmup.png")
        plot_metric_by_method_warm(diag_agg, "row_pair_abs_cos_mean", "Source row pairwise cosine", fig_dir / "diagnostic_row_similarity_by_method_warmup.png")
        plot_metric_by_method_warm(diag_agg, "feature_center_abs_cos_best_mean", "Source row best feature-center cosine", fig_dir / "diagnostic_feature_center_alignment_by_method_warmup.png")

    def find(rows: list[dict], method: str, warmup_step: int, metric: str) -> float:
        for row in rows:
            if str(row.get("method")) == method and int(row.get("warmup_step", -1)) == warmup_step:
                return float(row.get(f"{metric}_mean", "nan"))
        return float("nan")

    key = {
        "completed_cells": len({(r["seed"], r["slot_len"]) for r in train_rows}),
        "completed_training_rows": len(train_rows),
        "final_step": final_step,
        "w0_allpos_reinit_feature_nmi": find(condition_reinit, "allpos_centered", 0, "feature_NMI"),
        "w10_allpos_reinit_feature_nmi": find(condition_reinit, "allpos_centered", 10, "feature_NMI"),
        "w40_allpos_reinit_feature_nmi": find(condition_reinit, "allpos_centered", 40, "feature_NMI"),
        "w10_route_reinit_feature_nmi": find(condition_reinit, "route_centered", 10, "feature_NMI"),
        "w40_route_reinit_feature_nmi": find(condition_reinit, "route_centered", 40, "feature_NMI"),
        "w10_expert_svd_reinit_feature_nmi": find(condition_reinit, "expert_svd", 10, "feature_NMI"),
        "w40_expert_svd_reinit_feature_nmi": find(condition_reinit, "expert_svd", 40, "feature_NMI"),
        "w10_expert_svd_decommon_reinit_feature_nmi": find(condition_reinit, "expert_svd_decommon", 10, "feature_NMI"),
        "w10_expert_svd_orth_reinit_feature_nmi": find(condition_reinit, "expert_svd_orth", 10, "feature_NMI"),
        "w10_allpos_final_feature_nmi": find(condition_final, "allpos_centered", 10, "feature_NMI"),
        "w10_route_final_feature_nmi": find(condition_final, "route_centered", 10, "feature_NMI"),
        "w10_expert_svd_final_feature_nmi": find(condition_final, "expert_svd", 10, "feature_NMI"),
        "max_slot_start_nmi_reinit": max([float(r.get("slot_start_NMI_mean", "nan")) for r in condition_reinit] or [float("nan")]),
    }
    route_ref = max(key["w10_route_reinit_feature_nmi"], key["w40_route_reinit_feature_nmi"])
    allpos_best = max(key["w10_allpos_reinit_feature_nmi"], key["w40_allpos_reinit_feature_nmi"])
    svd_best = max(
        key["w10_expert_svd_reinit_feature_nmi"],
        key["w40_expert_svd_reinit_feature_nmi"],
        key["w10_expert_svd_decommon_reinit_feature_nmi"],
        key["w10_expert_svd_orth_reinit_feature_nmi"],
    )
    if not math.isnan(route_ref) and (allpos_best + 0.10 < route_ref) and (svd_best + 0.10 < route_ref):
        verdict = "supported_negative_boundary"
    elif not math.isnan(route_ref) and (allpos_best >= route_ref - 0.10 or svd_best >= route_ref - 0.10):
        verdict = "warmup_source_candidate_found"
    else:
        verdict = "insufficient"
    summary = {
        "experiment_id": EXPERIMENT_ID,
        "run_name": run_name,
        "run_stage": args.run_stage,
        "verdict": verdict,
        "key_metrics": key,
        "config": vars(args),
        "generated_at_unix": time.time(),
        "tables": {
            "data_audit": str(table_dir / "data_audit.csv"),
            "training_trajectory": str(table_dir / "training_trajectory.csv"),
            "spectral_diagnostics": str(table_dir / "spectral_diagnostics.csv"),
            "condition_aggregate_reinit": str(table_dir / "condition_aggregate_reinit.csv"),
            "condition_aggregate_final": str(table_dir / "condition_aggregate_final.csv"),
            "spectral_diagnostics_aggregate": str(table_dir / "spectral_diagnostics_aggregate.csv"),
        },
        "figures": {
            "reinit_feature_nmi": str(fig_dir / "reinit_feature_nmi_by_method_warmup.png"),
            "reinit_margin_p05": str(fig_dir / "reinit_margin_p05_by_method_warmup.png"),
            "final_feature_nmi": str(fig_dir / "final_feature_nmi_by_method_warmup.png"),
            "final_margin_p05": str(fig_dir / "final_margin_p05_by_method_warmup.png"),
            "feature_nmi_trajectory": str(fig_dir / "feature_nmi_trajectory_central_methods.png"),
            "diagnostic_common_alignment": str(fig_dir / "diagnostic_common_alignment_by_method_warmup.png"),
            "diagnostic_row_similarity": str(fig_dir / "diagnostic_row_similarity_by_method_warmup.png"),
            "diagnostic_feature_alignment": str(fig_dir / "diagnostic_feature_center_alignment_by_method_warmup.png"),
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
    parser.add_argument("--warmup-steps", default="0 10 40")
    parser.add_argument(
        "--methods",
        default="no_reinit allpos_centered route_centered oracle_centered expert_svd expert_svd_decommon expert_svd_orth",
    )
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
    parser.add_argument("--train-steps", type=int, default=160)
    parser.add_argument("--checkpoints", default="0 10 40 80 160")
    parser.add_argument("--lr", type=float, default=2e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--grad-clip", type=float, default=1.0)
    parser.add_argument("--router-init-scale", type=float, default=1.5)
    parser.add_argument("--kmeans-n-init", type=int, default=4)
    parser.add_argument("--kmeans-max-iter", type=int, default=40)
    args = parser.parse_args()

    if args.run_stage == "smoke":
        args.seeds = "0"
        args.slot_lengths = "1"
        args.warmup_steps = "0 10"
        args.train_steps = 20
        args.checkpoints = "0 5 20"
        args.calib_samples = 512
        args.eval_samples = 512
        args.methods = "no_reinit allpos_centered route_centered oracle_centered expert_svd expert_svd_decommon expert_svd_orth"

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
    print(
        json.dumps(
            {
                "event": "start",
                "rank": rank,
                "world_size": world_size,
                "device": str(device),
                "run_stage": args.run_stage,
                "run_name": args.run_name,
                "tasks": my_tasks,
            }
        ),
        flush=True,
    )
    all_data: list[dict] = []
    all_diag: list[dict] = []
    all_train: list[dict] = []
    for seed, slot_len in my_tasks:
        data_rows, diag_rows, train_rows = run_cell(args, seed, slot_len, device)
        all_data.extend(data_rows)
        all_diag.extend(diag_rows)
        all_train.extend(train_rows)
        print(json.dumps({"event": "cell_done", "rank": rank, "seed": seed, "slot_len": slot_len}), flush=True)
    write_csv(partial_dir / f"data_audit_rank{rank}.csv", all_data)
    write_csv(partial_dir / f"spectral_diagnostics_rank{rank}.csv", all_diag)
    write_csv(partial_dir / f"training_trajectory_rank{rank}.csv", all_train)
    base.dist_barrier(dist_enabled)
    if rank == 0:
        summary = summarize_and_plot(output_dir, args, args.run_name)
        print(json.dumps({"event": "summary", "summary": summary}, indent=2), flush=True)
    base.dist_barrier(dist_enabled)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Run A06_26 MPI router audit on the uniform no-position slot bridge."""

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
from torch import nn
from torch.nn import functional as F


EXPERIMENT_ID = "A06_01_05_E02_manifold_power_iteration"
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


def parse_int_list(text: str) -> list[int]:
    return base.parse_int_list(text)


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


def generate_uniform_batch(args: argparse.Namespace, n: int, slot_len: int, seed: int):
    return base.generate_batch(args, n, slot_len, seed, balanced=True)


def route_slice(x: torch.Tensor, route_pos: torch.Tensor) -> torch.Tensor:
    return base.route_slice(x, route_pos)


def normalize_rows(rows: torch.Tensor, scale: float = 1.0) -> torch.Tensor:
    return rows / rows.norm(dim=1, keepdim=True).clamp_min(1e-8) * float(scale)


def p05(values: torch.Tensor) -> float:
    if int(values.numel()) == 0:
        return float("nan")
    sorted_values = torch.sort(values.detach().cpu().float()).values
    idx = int(math.floor(0.05 * max(0, int(sorted_values.numel()) - 1)))
    return float(sorted_values[max(0, min(idx, int(sorted_values.numel()) - 1))].item())


def margin_from_mapping(scores: torch.Tensor, feature: torch.Tensor, mapping: dict[int, int]) -> torch.Tensor:
    feature_cpu = feature.detach().cpu()
    scores_cpu = scores.detach().cpu().float()
    target = torch.tensor([mapping[int(f)] for f in feature_cpu.tolist()], dtype=torch.long)
    target_scores = scores_cpu[torch.arange(scores_cpu.shape[0]), target]
    masked = scores_cpu.clone()
    masked[torch.arange(scores_cpu.shape[0]), target] = -1e9
    return target_scores - masked.max(dim=1).values


def cosine_matrix(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    aa = a.float() / a.float().norm(dim=1, keepdim=True).clamp_min(1e-8)
    bb = b.float() / b.float().norm(dim=1, keepdim=True).clamp_min(1e-8)
    return aa @ bb.T


class MPITop1MoE(nn.Module):
    def __init__(self, d_model: int, d_ff: int, num_experts: int, router_mode: str, c_prime: float):
        super().__init__()
        self.router_mode = router_mode
        self.c_prime = float(c_prime)
        self.router = nn.Linear(d_model, num_experts, bias=False)
        self.experts = nn.ModuleList(
            [
                nn.Sequential(
                    nn.Linear(d_model, d_ff),
                    nn.GELU(),
                    nn.Linear(d_ff, d_model),
                )
                for _ in range(num_experts)
            ]
        )

    def expert_input_mats(self) -> torch.Tensor:
        mats = []
        for expert in self.experts:
            # Paper pseudo-code uses wg as [N, D, d]. For this GLU-free bridge,
            # the first expert projection is the input-side expert matrix.
            mats.append(expert[0].weight.T)
        return torch.stack(mats, dim=0)

    def mpi_power_rows(self) -> torch.Tensor:
        rows = self.router.weight
        wg = self.expert_input_mats()
        return (rows.unsqueeze(1) @ wg @ wg.transpose(1, 2)).squeeze(1)

    def effective_router_rows(self) -> torch.Tensor:
        n = self.router.weight.shape[0]
        if self.router_mode == "vanilla":
            return self.router.weight
        scale = self.c_prime * (float(n) ** -0.5)
        if self.router_mode == "retract":
            return normalize_rows(self.router.weight, scale)
        if self.router_mode == "mpi":
            return normalize_rows(self.mpi_power_rows(), scale)
        if self.router_mode == "mpi_no_retract":
            return self.mpi_power_rows()
        raise ValueError(f"unknown router_mode={self.router_mode}")

    def forward(self, h: torch.Tensor, router_input: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        rows = self.effective_router_rows()
        scores = router_input @ rows.T
        probs = F.softmax(scores, dim=-1)
        top = probs.argmax(dim=-1)
        expert_outs = torch.stack([expert(h) for expert in self.experts], dim=2)
        gather_idx = top.unsqueeze(-1).unsqueeze(-1).expand(-1, -1, 1, h.shape[-1])
        selected = expert_outs.gather(2, gather_idx).squeeze(2)
        selected_prob = probs.gather(-1, top.unsqueeze(-1)).squeeze(-1).unsqueeze(-1)
        return selected * selected_prob, scores, top


class TinyTransformerMPI(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        d_model: int,
        num_heads: int,
        d_ff: int,
        num_experts: int,
        router_mode: str,
        c_prime: float,
    ):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)
        self.attn = nn.MultiheadAttention(d_model, num_heads, batch_first=True)
        self.ln1 = nn.LayerNorm(d_model)
        self.moe = MPITop1MoE(d_model, d_ff, num_experts, router_mode, c_prime)
        self.ln2 = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)

    def router_states(self, x: torch.Tensor) -> torch.Tensor:
        emb = self.embed(x)
        t = x.shape[1]
        mask = torch.triu(torch.ones(t, t, dtype=torch.bool, device=x.device), diagonal=1)
        attn_out, _ = self.attn(emb, emb, emb, attn_mask=mask, need_weights=False)
        return self.ln1(emb + attn_out)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        h = self.router_states(x)
        moe_out, scores, route = self.moe(h, h)
        y = self.ln2(h + moe_out)
        logits = self.lm_head(y)
        return logits, {"route_scores": scores, "route": route, "hidden": h, "router_input": h}


def make_model(args: argparse.Namespace, seed: int, device: torch.device, router_mode: str, c_prime: float):
    base.set_seed(seed)
    vocab_size = int(args.num_neutral_tokens) + 2 * int(args.num_features)
    model = TinyTransformerMPI(
        vocab_size=vocab_size,
        d_model=int(args.d_model),
        num_heads=int(args.num_heads),
        d_ff=int(args.d_ff),
        num_experts=int(args.num_experts),
        router_mode=router_mode,
        c_prime=c_prime,
    ).to(device)
    return model


@torch.no_grad()
def collect_route_states(model, batch, args: argparse.Namespace, device: torch.device) -> torch.Tensor:
    model.eval()
    parts = []
    for start in range(0, batch.x.shape[0], int(args.eval_batch_size)):
        x = batch.x[start : start + int(args.eval_batch_size)].to(device)
        rp = batch.route_pos[start : start + x.shape[0]].to(device)
        h = model.router_states(x)
        parts.append(route_slice(h, rp).detach().cpu())
    return torch.cat(parts, dim=0)


def set_router_from_rows(model, rows: torch.Tensor, scale: float) -> None:
    with torch.no_grad():
        model.moe.router.weight.copy_(normalize_rows(rows.float(), scale).to(model.moe.router.weight.device))


def oracle_centers(route_states: torch.Tensor, feature: torch.Tensor, num_features: int) -> torch.Tensor:
    return base.oracle_centers(route_states, feature, num_features)


def init_special_router(args: argparse.Namespace, model, method: str, calib, seed: int, device: torch.device) -> None:
    allpos_methods = {"allpos_centered_init"} | {f"allpos_centered_mpi_c{c}" for c in (1, 2, 4, 8)}
    if method not in {"route_centered_init", "oracle_centered_init", "static_svd_init"} | allpos_methods:
        return
    if method == "static_svd_init":
        rows = expert_svd_rows(model)
        set_router_from_rows(model, rows, float(args.router_init_scale))
        return
    if method in allpos_methods:
        states = base.collect_states(model, calib, device, int(args.eval_batch_size))
        all_h = states["all"]
        common_all = all_h.mean(dim=0)
        rows = base.kmeans(
            all_h - common_all,
            int(args.num_experts),
            seed + 8101,
            int(args.kmeans_n_init),
            int(args.kmeans_max_iter),
            device,
        )
        set_router_from_rows(model, rows, float(args.router_init_scale))
        return
    route_h = collect_route_states(model, calib, args, device)
    common_route = route_h.mean(dim=0)
    if method == "route_centered_init":
        rows = base.kmeans(
            route_h - common_route,
            int(args.num_experts),
            seed + 9101,
            int(args.kmeans_n_init),
            int(args.kmeans_max_iter),
            device,
        )
    else:
        rows = oracle_centers(route_h, calib.feature, int(args.num_features)) - common_route
    set_router_from_rows(model, rows, float(args.router_init_scale))


def expert_svd_rows(model) -> torch.Tensor:
    rows = []
    router_rows = model.moe.router.weight.detach().cpu().float()
    for e, expert in enumerate(model.moe.experts):
        first = expert[0].weight.detach().cpu().float()
        _u, _s, vh = torch.linalg.svd(first, full_matrices=False)
        v = vh[0].clone()
        if float(torch.dot(v, router_rows[e])) < 0:
            v = -v
        rows.append(v)
    return torch.stack(rows, dim=0)


@torch.no_grad()
def collect_route_scores(model, batch, args: argparse.Namespace, device: torch.device):
    model.eval()
    score_parts = []
    assign_parts = []
    loss_sum = 0.0
    correct = 0
    count = 0
    for start in range(0, batch.x.shape[0], int(args.eval_batch_size)):
        x = batch.x[start : start + int(args.eval_batch_size)].to(device)
        rp = batch.route_pos[start : start + x.shape[0]].to(device)
        target = batch.target[start : start + x.shape[0]].to(device)
        logits, info = model(x)
        route_logits = route_slice(logits, rp)
        scores = route_slice(info["route_scores"], rp)
        assign = scores.argmax(dim=-1)
        loss_sum += float(F.cross_entropy(route_logits, target, reduction="sum").detach().cpu().item())
        correct += int((route_logits.argmax(dim=-1) == target).sum().detach().cpu().item())
        count += int(x.shape[0])
        score_parts.append(scores.detach().cpu())
        assign_parts.append(assign.detach().cpu())
    return torch.cat(score_parts, dim=0), torch.cat(assign_parts, dim=0), loss_sum / max(1, count), correct / max(1, count)


@torch.no_grad()
def diagnostics(
    model,
    calib,
    args: argparse.Namespace,
    condition: str,
    method: str,
    seed: int,
    slot_len: int,
    c_prime: float,
    checkpoint: int,
    device,
):
    route_h = collect_route_states(model, calib, args, device)
    feature_centers = oracle_centers(route_h, calib.feature, int(args.num_features))
    rows_eff = model.moe.effective_router_rows().detach().cpu().float()
    rows_unit = normalize_rows(rows_eff, 1.0)
    svd_rows = normalize_rows(expert_svd_rows(model), 1.0)
    pair = cosine_matrix(rows_unit, rows_unit).abs()
    off = pair[~torch.eye(pair.shape[0], dtype=torch.bool)]
    align = torch.diag(cosine_matrix(rows_unit, svd_rows).abs())
    feat_cos = cosine_matrix(rows_unit, feature_centers).abs()
    center_scores = feature_centers @ rows_eff.T
    center_assign = center_scores.argmax(dim=1)
    center_feature = torch.arange(int(args.num_features), dtype=torch.long)
    mapping = base.best_feature_mapping(center_feature, center_assign, int(args.num_features), int(args.num_experts))
    center_margin = margin_from_mapping(center_scores, center_feature, mapping)
    return {
        "experiment_id": EXPERIMENT_ID,
        "condition": condition,
        "method": method,
        "seed": seed,
        "slot_len": slot_len,
        "c_prime": c_prime,
        "checkpoint": checkpoint,
        "router_svd_diag_abs_cos_mean": float(align.mean().item()),
        "router_svd_diag_abs_cos_min": float(align.min().item()),
        "row_pair_abs_cos_mean": float(off.mean().item()) if int(off.numel()) else float("nan"),
        "row_pair_abs_cos_max": float(off.max().item()) if int(off.numel()) else float("nan"),
        "feature_center_abs_cos_best_mean": float(feat_cos.max(dim=0).values.mean().item()),
        "feature_center_abs_cos_best_min": float(feat_cos.max(dim=0).values.min().item()),
        "center_margin_mean": float(center_margin.mean().item()),
        "center_margin_p05": p05(center_margin),
    }


def evaluate_model(
    model,
    eval_batch,
    args: argparse.Namespace,
    device: torch.device,
    condition: str,
    method: str,
    seed: int,
    slot_len: int,
    c_prime: float,
    checkpoint: int,
) -> dict:
    scores, assign, loss, acc = collect_route_scores(model, eval_batch, args, device)
    feature = eval_batch.feature.detach().cpu()
    slot_start = eval_batch.slot_start.detach().cpu()
    mapping = base.best_feature_mapping(feature, assign, int(args.num_features), int(args.num_experts))
    margin = margin_from_mapping(scores, feature, mapping)
    row = {
        "experiment_id": EXPERIMENT_ID,
        "condition": condition,
        "method": method,
        "seed": seed,
        "slot_len": slot_len,
        "c_prime": c_prime,
        "checkpoint": checkpoint,
        "eval_count": int(feature.numel()),
        "loss": loss,
        "target_accuracy": acc,
        "feature_NMI": base.nmi(feature, assign),
        "margin_mean": float(margin.mean().item()),
        "margin_p05": p05(margin),
        "positive_margin_frac": float((margin > 0).float().mean().item()),
        "slot_start_NMI": base.nmi(slot_start, assign),
        **base.load_metrics(assign, int(args.num_experts)),
    }
    matched = torch.tensor([mapping[int(f)] for f in feature.tolist()], dtype=torch.long)
    row["matched_fraction_current_mapping"] = float((assign == matched).float().mean().item())
    for f, e in mapping.items():
        row[f"map_feature_{f}_expert"] = e
    return row


def train_condition(
    args: argparse.Namespace,
    method: str,
    seed: int,
    slot_len: int,
    device: torch.device,
) -> tuple[list[dict], list[dict], list[dict]]:
    if method.startswith("allpos_centered_mpi_c"):
        router_mode = "mpi"
        c_prime = float(method.removeprefix("allpos_centered_mpi_c"))
    elif method.startswith("mpi_c"):
        router_mode = "mpi"
        c_prime = float(method.removeprefix("mpi_c"))
    elif method.startswith("retract_c"):
        router_mode = "retract"
        c_prime = float(method.removeprefix("retract_c"))
    elif method == "mpi_no_retract":
        router_mode = "mpi_no_retract"
        c_prime = 1.0
    else:
        router_mode = "vanilla"
        c_prime = 1.0
    condition = method
    model = make_model(args, seed + 33000, device, router_mode, c_prime)
    calib = generate_uniform_batch(args, int(args.calib_samples), slot_len, seed + 101)
    eval_batch = generate_uniform_batch(args, int(args.eval_samples), slot_len, seed + 202)
    init_special_router(args, model, method, calib, seed, device)
    data_rows = [
        {
            "experiment_id": EXPERIMENT_ID,
            "split": "calib",
            "condition": condition,
            "method": method,
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
            "condition": condition,
            "method": method,
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
    rows: list[dict] = []
    diag_rows: list[dict] = []
    checkpoints = sorted(set([0] + parse_int_list(args.checkpoints)))
    checkpoint_set = set(checkpoints)
    rows.append(evaluate_model(model, eval_batch, args, device, condition, method, seed, slot_len, c_prime, 0))
    diag_rows.append(diagnostics(model, calib, args, condition, method, seed, slot_len, c_prime, 0, device))
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(args.lr), weight_decay=float(args.weight_decay))
    for step in range(1, int(args.train_steps) + 1):
        model.train()
        batch = generate_uniform_batch(args, int(args.train_batch_size), slot_len, seed + 900000 + step)
        x = batch.x.to(device)
        rp = batch.route_pos.to(device)
        target = batch.target.to(device)
        logits, _info = model(x)
        route_logits = route_slice(logits, rp)
        loss = F.cross_entropy(route_logits, target)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(args.grad_clip))
        optimizer.step()
        if step in checkpoint_set:
            rows.append(evaluate_model(model, eval_batch, args, device, condition, method, seed, slot_len, c_prime, step))
            diag_rows.append(diagnostics(model, calib, args, condition, method, seed, slot_len, c_prime, step, device))
    return data_rows, diag_rows, rows


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


def plot_metric_by_method(rows: list[dict], metric: str, title: str, path: Path) -> None:
    methods = [str(r["method"]) for r in rows]
    vals = [float(r[f"{metric}_mean"]) for r in rows]
    plt.figure(figsize=(10.5, 5.2))
    plt.bar(np.arange(len(methods)), vals)
    plt.xticks(np.arange(len(methods)), methods, rotation=35, ha="right")
    plt.ylabel(metric)
    plt.title(title)
    plt.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=180)
    plt.close()


def plot_trajectory(rows: list[dict], metric: str, title: str, path: Path) -> None:
    methods = sorted({str(r["method"]) for r in rows})
    plt.figure(figsize=(10.5, 5.4))
    for method in methods:
        mr = sorted([r for r in rows if str(r["method"]) == method], key=lambda r: int(r["checkpoint"]))
        plt.plot([int(r["checkpoint"]) for r in mr], [float(r[f"{metric}_mean"]) for r in mr], marker="o", label=method)
    plt.xlabel("checkpoint")
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
    for path in sorted(partial_dir.glob("diagnostics_rank*.csv")):
        diag_rows.extend(read_csv(path))
    for path in sorted(partial_dir.glob("training_trajectory_rank*.csv")):
        train_rows.extend(read_csv(path))
    table_dir = output_dir / "tables"
    fig_dir = output_dir / "figures"
    write_csv(table_dir / "data_audit.csv", data_rows)
    write_csv(table_dir / "diagnostics.csv", diag_rows)
    write_csv(table_dir / "training_trajectory.csv", train_rows)
    metrics = [
        "feature_NMI",
        "margin_mean",
        "margin_p05",
        "positive_margin_frac",
        "slot_start_NMI",
        "max_load",
        "effective_experts",
        "target_accuracy",
        "loss",
        "matched_fraction_current_mapping",
    ]
    diag_metrics = [
        "router_svd_diag_abs_cos_mean",
        "router_svd_diag_abs_cos_min",
        "row_pair_abs_cos_mean",
        "row_pair_abs_cos_max",
        "feature_center_abs_cos_best_mean",
        "feature_center_abs_cos_best_min",
        "center_margin_mean",
        "center_margin_p05",
    ]
    trajectory = aggregate_rows(train_rows, ["condition", "method", "checkpoint"], metrics)
    final_step = max(int(r["checkpoint"]) for r in train_rows) if train_rows else 0
    final_rows = [r for r in train_rows if int(r["checkpoint"]) == final_step]
    init_rows = [r for r in train_rows if int(r["checkpoint"]) == 0]
    condition_final = aggregate_rows(final_rows, ["condition", "method"], metrics)
    condition_init = aggregate_rows(init_rows, ["condition", "method"], metrics)
    diag_final_rows = [r for r in diag_rows if int(r.get("checkpoint", 0)) == final_step]
    diag_final = aggregate_rows(diag_final_rows, ["condition", "method"], diag_metrics)
    diag_trajectory = aggregate_rows(diag_rows, ["condition", "method", "checkpoint"], diag_metrics)
    write_csv(table_dir / "condition_trajectory_aggregate.csv", trajectory)
    write_csv(table_dir / "condition_aggregate_init.csv", condition_init)
    write_csv(table_dir / "condition_aggregate_final.csv", condition_final)
    write_csv(table_dir / "diagnostics_aggregate.csv", diag_final)
    write_csv(table_dir / "diagnostics_trajectory_aggregate.csv", diag_trajectory)
    if condition_final:
        plot_metric_by_method(condition_final, "feature_NMI", "Final feature NMI by router method", fig_dir / "final_feature_nmi_by_method.png")
        plot_metric_by_method(condition_final, "margin_p05", "Final margin p05 by router method", fig_dir / "final_margin_p05_by_method.png")
        plot_metric_by_method(condition_final, "max_load", "Final max load by router method", fig_dir / "final_max_load_by_method.png")
    if trajectory:
        plot_trajectory(trajectory, "feature_NMI", "Feature NMI trajectory by router method", fig_dir / "feature_nmi_trajectory_by_method.png")
        plot_trajectory(trajectory, "margin_p05", "Margin p05 trajectory by router method", fig_dir / "margin_p05_trajectory_by_method.png")
    if diag_final:
        plot_metric_by_method(diag_final, "router_svd_diag_abs_cos_mean", "Router-SVD alignment by method", fig_dir / "router_svd_alignment_by_method.png")

    def find(rows: list[dict], method: str, metric: str) -> float:
        for row in rows:
            if str(row.get("method")) == method:
                return float(row.get(f"{metric}_mean", "nan"))
        return float("nan")

    def finite_max(values: list[float]) -> float:
        finite = [v for v in values if not math.isnan(v)]
        return max(finite) if finite else float("nan")

    key = {
        "completed_cells": len({(r["seed"], r["slot_len"], r["method"]) for r in train_rows}),
        "completed_training_rows": len(train_rows),
        "final_step": final_step,
        "vanilla_final_feature_nmi": find(condition_final, "vanilla", "feature_NMI"),
        "retract_c1_final_feature_nmi": find(condition_final, "retract_c1", "feature_NMI"),
        "mpi_c1_final_feature_nmi": find(condition_final, "mpi_c1", "feature_NMI"),
        "mpi_c2_final_feature_nmi": find(condition_final, "mpi_c2", "feature_NMI"),
        "mpi_c4_final_feature_nmi": find(condition_final, "mpi_c4", "feature_NMI"),
        "mpi_c8_final_feature_nmi": find(condition_final, "mpi_c8", "feature_NMI"),
        "allpos_centered_init_final_feature_nmi": find(condition_final, "allpos_centered_init", "feature_NMI"),
        "allpos_centered_mpi_c8_final_feature_nmi": find(condition_final, "allpos_centered_mpi_c8", "feature_NMI"),
        "route_centered_init_final_feature_nmi": find(condition_final, "route_centered_init", "feature_NMI"),
        "oracle_centered_init_final_feature_nmi": find(condition_final, "oracle_centered_init", "feature_NMI"),
        "max_slot_start_nmi_final": max([float(r.get("slot_start_NMI_mean", "nan")) for r in condition_final] or [float("nan")]),
    }
    mpi_best = finite_max(
        [
            key["mpi_c1_final_feature_nmi"],
            key["mpi_c2_final_feature_nmi"],
            key["mpi_c4_final_feature_nmi"],
            key["mpi_c8_final_feature_nmi"],
            key["allpos_centered_mpi_c8_final_feature_nmi"],
        ]
    )
    route_ref = key["route_centered_init_final_feature_nmi"]
    if not math.isnan(route_ref) and mpi_best >= route_ref - 0.05:
        verdict = "mpi_matches_route_control"
    elif mpi_best >= finite_max([key["vanilla_final_feature_nmi"], key["retract_c1_final_feature_nmi"]]) + 0.05:
        verdict = "mpi_improves_but_not_route_control"
    else:
        verdict = "mpi_not_feature_specialization_solution"
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
            "diagnostics": str(table_dir / "diagnostics.csv"),
            "condition_aggregate_init": str(table_dir / "condition_aggregate_init.csv"),
            "condition_aggregate_final": str(table_dir / "condition_aggregate_final.csv"),
            "diagnostics_aggregate": str(table_dir / "diagnostics_aggregate.csv"),
            "diagnostics_trajectory_aggregate": str(table_dir / "diagnostics_trajectory_aggregate.csv"),
        },
        "figures": {
            "final_feature_nmi": str(fig_dir / "final_feature_nmi_by_method.png"),
            "final_margin_p05": str(fig_dir / "final_margin_p05_by_method.png"),
            "final_max_load": str(fig_dir / "final_max_load_by_method.png"),
            "feature_nmi_trajectory": str(fig_dir / "feature_nmi_trajectory_by_method.png"),
            "margin_p05_trajectory": str(fig_dir / "margin_p05_trajectory_by_method.png"),
            "router_svd_alignment": str(fig_dir / "router_svd_alignment_by_method.png"),
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
    parser.add_argument(
        "--methods",
        default="vanilla retract_c1 mpi_c1 mpi_c2 mpi_c4 mpi_c8 static_svd_init route_centered_init oracle_centered_init",
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
        args.methods = "vanilla retract_c1 mpi_c1 mpi_c4 route_centered_init oracle_centered_init"
        args.train_steps = 20
        args.checkpoints = "0 5 20"
        args.calib_samples = 512
        args.eval_samples = 512
        args.kmeans_n_init = 2
        args.kmeans_max_iter = 20

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
    methods = [m for m in str(args.methods).replace(",", " ").split() if m.strip()]
    tasks = [(seed, slot_len, method) for seed in seeds for slot_len in slot_lengths for method in methods]
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
    for seed, slot_len, method in my_tasks:
        data_rows, diag_rows, train_rows = train_condition(args, method, seed, slot_len, device)
        all_data.extend(data_rows)
        all_diag.extend(diag_rows)
        all_train.extend(train_rows)
        print(json.dumps({"event": "cell_done", "rank": rank, "seed": seed, "slot_len": slot_len, "method": method}), flush=True)
    write_csv(partial_dir / f"data_audit_rank{rank}.csv", all_data)
    write_csv(partial_dir / f"diagnostics_rank{rank}.csv", all_diag)
    write_csv(partial_dir / f"training_trajectory_rank{rank}.csv", all_train)
    base.dist_barrier(dist_enabled)
    if rank == 0:
        summary = summarize_and_plot(output_dir, args, args.run_name)
        print(json.dumps({"event": "summary", "summary": summary}, indent=2), flush=True)
    base.dist_barrier(dist_enabled)


if __name__ == "__main__":
    main()

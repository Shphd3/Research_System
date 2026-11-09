#!/usr/bin/env python3
"""Checkpoint-level collapse mechanism audit for the original uniform feature setting."""

from __future__ import annotations

import argparse
import csv
import json
import math
import multiprocessing as mp
import random
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import torch
from torch.nn import functional as F


RESEARCH_ROOT = Path(__file__).resolve().parents[6]
WORKSPACE = (
    RESEARCH_ROOT
    / "Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding"
)
RAW_RESULT_DIR = (
    WORKSPACE
    / "results/h0605a_true_token_conditioned_inhibition_replay/h0605a_true_token_conditioned_inhibition_replay_4gpu_20260604"
)
sys.path.insert(0, str(WORKSPACE / "scripts"))
sys.path.insert(0, str(WORKSPACE / "src"))

import run_h0605a_true_token_conditioned_inhibition_replay as runner  # noqa: E402


CONDITIONS = ["R0-dot", "R1-dot", "S0-dot", "S1-dot", "R0-cos", "R1-cos", "S0-cos", "S1-cos"]
SEEDS = [20260521, 20260522, 20260523]
AUDIT_STEPS = [0, 10, 20, 50, 100, 200, 800, 1600]
TRAJECTORY_AVAILABLE_STEPS = [0] + list(range(100, 1700, 100))
FEATURE_AVAILABLE_STEPS = [0, 800, 1600]
COLLAPSE_THRESHOLD = 0.95


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    fieldnames = list(rows[0].keys())
    seen = set(fieldnames)
    for row in rows[1:]:
        for key in row.keys():
            if key not in seen:
                fieldnames.append(key)
                seen.add(key)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def load_cfg() -> dict:
    return json.loads((WORKSPACE / "configs/h0605a_true_token_conditioned_inhibition_replay.json").read_text())


def feature_eval_batch(cfg: dict, condition: str, seed: int):
    return runner.generate_feature_variant_data(cfg, condition, "multi_b_primary", seed)


def route_entropy(counts: torch.Tensor) -> tuple[float, float]:
    counts = counts.float()
    total = float(counts.sum().item())
    if total <= 0:
        return math.nan, math.nan
    p = counts / total
    mask = p > 0
    ent = float(-(p[mask] * p[mask].log()).sum().item())
    return ent, ent / math.log(max(2, counts.numel()))


def evaluate_checkpoint(
    model: torch.nn.Module,
    cfg: dict,
    condition: str,
    seed: int,
    step: int,
    initial_router_weight: torch.Tensor,
    device: torch.device,
) -> dict[str, list[dict]]:
    data = feature_eval_batch(cfg, condition, seed)
    batch_size = int(cfg["evaluation"]["batch_size"])
    b_pos = int(cfg["data"]["b_position"])
    num_slots = int(cfg["data"]["num_slots"])
    b_count = int(cfg["data"]["b_token_count_multi"])
    num_features = num_slots * b_count
    num_experts = int(cfg["model"]["num_experts"])
    d_model = int(cfg["model"]["d_model"])

    counts = torch.zeros(num_features, num_experts, dtype=torch.long)
    slot_counts = torch.zeros(num_slots, num_experts, dtype=torch.long)
    h_sum = torch.zeros(num_features, d_model)
    h_count = torch.zeros(num_features, dtype=torch.long)
    correct = 0
    total = 0
    model.eval()
    with torch.no_grad():
        for start in range(0, data.x.shape[0], batch_size):
            x = data.x[start : start + batch_size].to(device)
            logits, info = model(x, return_acts=True)
            experts = info["expert_idx"][:, b_pos].detach().cpu()
            h = info["ffn_input"][:, b_pos, :].detach().cpu().float()
            target = data.target[start : start + batch_size]
            pred = logits[:, b_pos, :].argmax(dim=-1).detach().cpu()
            correct += int((pred == target).sum().item())
            total += int(x.shape[0])
            slots = data.slot[start : start + batch_size]
            b_idxs = data.b_idx[start : start + batch_size]
            for i, (slot, b_idx, expert) in enumerate(zip(slots.tolist(), b_idxs.tolist(), experts.tolist())):
                feature = int(slot) * b_count + int(b_idx)
                counts[feature, int(expert)] += 1
                slot_counts[int(slot), int(expert)] += 1
                h_sum[feature] += h[i]
                h_count[feature] += 1
    model.train()

    feature_centroids = h_sum / h_count.clamp_min(1).unsqueeze(1)
    slot_centroids = torch.stack(
        [feature_centroids[s * b_count : (s + 1) * b_count].mean(dim=0) for s in range(num_slots)]
    )
    router_w = model.moe.router.weight.detach().cpu().float()
    router_w_norm = F.normalize(router_w, p=2, dim=1, eps=1e-8)
    feature_norm = F.normalize(feature_centroids, p=2, dim=1, eps=1e-8)
    slot_norm = F.normalize(slot_centroids, p=2, dim=1, eps=1e-8)
    feature_cos = feature_norm @ router_w_norm.T
    slot_cos = slot_norm @ router_w_norm.T
    top2_vals, top2_idx = feature_cos.topk(2, dim=1)
    top1_expert = top2_idx[:, 0]
    top1_margin = top2_vals[:, 0] - top2_vals[:, 1]
    load_counts = counts.sum(dim=0)
    load_total = int(load_counts.sum().item())
    max_fraction = float(load_counts.max().item() / load_total) if load_total else math.nan
    dominant = int(load_counts.argmax().item()) if load_total else -1
    active = int((load_counts > 0).sum().item())
    entropy, entropy_norm = route_entropy(load_counts)

    common = F.normalize(feature_centroids.mean(dim=0), p=2, dim=0, eps=1e-8)
    common_cos = router_w_norm @ common
    proj = (feature_centroids @ common).unsqueeze(1) * common.unsqueeze(0)
    residual = feature_centroids - proj
    residual_norm = F.normalize(residual, p=2, dim=1, eps=1e-8)
    residual_cos = residual_norm @ router_w_norm.T
    slot_residual_rows = []
    for slot in range(num_slots):
        block = residual[slot * b_count : (slot + 1) * b_count].mean(dim=0)
        block = F.normalize(block, p=2, dim=0, eps=1e-8)
        vals = router_w_norm @ block
        for expert in range(num_experts):
            slot_residual_rows.append(
                {
                    "condition": condition,
                    "seed": seed,
                    "step": step,
                    "slot": slot,
                    "expert": expert,
                    "slot_residual_cosine": float(vals[expert].item()),
                }
            )

    load_rows = []
    for expert in range(num_experts):
        count = int(load_counts[expert].item())
        load_rows.append(
            {
                "condition": condition,
                "seed": seed,
                "step": step,
                "expert": expert,
                "count": count,
                "fraction": count / load_total if load_total else math.nan,
                "max_load_fraction": max_fraction,
                "load_entropy": entropy,
                "load_entropy_norm": entropy_norm,
                "active_experts": active,
                "dominant_expert": dominant,
                "collapsed": int(max_fraction >= COLLAPSE_THRESHOLD or active <= 1),
                "target_accuracy": correct / total if total else math.nan,
            }
        )

    slot_assignment_rows = []
    for slot in range(num_slots):
        denom = float(slot_counts[slot].sum().item())
        for expert in range(num_experts):
            slot_assignment_rows.append(
                {
                    "condition": condition,
                    "seed": seed,
                    "step": step,
                    "slot": slot,
                    "expert": expert,
                    "count": int(slot_counts[slot, expert].item()),
                    "fraction": float(slot_counts[slot, expert].item() / denom) if denom else math.nan,
                }
            )

    slot_cos_rows = []
    for slot in range(num_slots):
        for expert in range(num_experts):
            slot_cos_rows.append(
                {
                    "condition": condition,
                    "seed": seed,
                    "step": step,
                    "slot": slot,
                    "expert": expert,
                    "cosine": float(slot_cos[slot, expert].item()),
                }
            )

    common_rows = []
    for expert in range(num_experts):
        vals = residual_cos[:, expert]
        common_rows.append(
            {
                "condition": condition,
                "seed": seed,
                "step": step,
                "expert": expert,
                "common_direction_cosine": float(common_cos[expert].item()),
                "feature_residual_abs_cosine_mean": float(vals.abs().mean().item()),
                "feature_residual_cosine_mean": float(vals.mean().item()),
            }
        )

    router_rows = []
    router_delta = (router_w - initial_router_weight.cpu().float()).norm(dim=1)
    router_norms = router_w.norm(dim=1)
    pair = router_w_norm @ router_w_norm.T
    for expert in range(num_experts):
        router_rows.append(
            {
                "condition": condition,
                "seed": seed,
                "step": step,
                "expert": expert,
                "router_norm": float(router_norms[expert].item()),
                "delta_from_init": float(router_delta[expert].item()),
            }
        )
    pair_rows = []
    for i in range(num_experts):
        for j in range(num_experts):
            pair_rows.append(
                {
                    "condition": condition,
                    "seed": seed,
                    "step": step,
                    "expert_i": i,
                    "expert_j": j,
                    "cosine": float(pair[i, j].item()),
                }
            )

    margin_rows = []
    # Store compact per-run summaries rather than all 1024 feature margins.
    margin_rows.append(
        {
            "condition": condition,
            "seed": seed,
            "step": step,
            "top1_margin_mean": float(top1_margin.mean().item()),
            "top1_margin_median": float(top1_margin.median().item()),
            "top1_margin_p10": float(torch.quantile(top1_margin, 0.10).item()),
            "top1_margin_p90": float(torch.quantile(top1_margin, 0.90).item()),
            "top1_expert_0_fraction": float((top1_expert == 0).float().mean().item()),
            "top1_expert_1_fraction": float((top1_expert == 1).float().mean().item()),
            "top1_expert_2_fraction": float((top1_expert == 2).float().mean().item()),
            "top1_expert_3_fraction": float((top1_expert == 3).float().mean().item()),
            "top1_equals_dominant_fraction": float((top1_expert == dominant).float().mean().item()),
        }
    )

    feature_summary_rows = []
    feature_main = counts.argmax(dim=1)
    for slot in range(num_slots):
        block = feature_main[slot * b_count : (slot + 1) * b_count]
        for expert in range(num_experts):
            feature_summary_rows.append(
                {
                    "condition": condition,
                    "seed": seed,
                    "step": step,
                    "slot": slot,
                    "expert": expert,
                    "main_expert_feature_fraction": float((block == expert).float().mean().item()),
                }
            )

    return {
        "load_rows": load_rows,
        "slot_assignment_rows": slot_assignment_rows,
        "slot_cos_rows": slot_cos_rows,
        "common_rows": common_rows,
        "slot_residual_rows": slot_residual_rows,
        "router_rows": router_rows,
        "pair_rows": pair_rows,
        "margin_rows": margin_rows,
        "feature_summary_rows": feature_summary_rows,
    }


def audit_one(args_tuple: tuple[str, int, str, int]) -> dict[str, list[dict]]:
    condition, seed, device_prefix, device_id = args_tuple
    cfg = load_cfg()
    device = torch.device(f"{device_prefix}:{device_id}" if device_prefix == "cuda" and torch.cuda.is_available() else "cpu")
    cond = runner.parse_true_token_condition(condition)
    random.seed(seed)
    torch.manual_seed(seed + 1009)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed + 1009)
    # Match the original run's RNG consumption before the actual model.
    audit_model = runner.make_condition_model(condition, cfg, device)
    del audit_model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    model = runner.make_condition_model(condition, cfg, device)
    if cond.router_init:
        runner.init_router_from_slot_centroids(model, cfg, condition, "multi_b_primary", seed, device)
    initial_router_weight = model.moe.router.weight.detach().cpu().clone()
    train_data = runner.generate_slot_data(
        cfg, condition, "multi_b_primary", "train", int(cfg["data"]["train_samples_per_slot"]), seed
    )
    batch_size = int(cfg["training"]["batch_size"])
    opt = torch.optim.AdamW(model.parameters(), lr=float(cfg["training"]["lr"]), weight_decay=float(cfg["training"]["weight_decay"]))
    rng = random.Random(seed + 17)
    indices = list(range(train_data.x.shape[0]))
    b_pos = int(cfg["data"]["b_position"])
    steps = int(cfg["training"]["steps"])

    out: dict[str, list[dict]] = {
        "load_rows": [],
        "slot_assignment_rows": [],
        "slot_cos_rows": [],
        "common_rows": [],
        "slot_residual_rows": [],
        "router_rows": [],
        "pair_rows": [],
        "margin_rows": [],
        "feature_summary_rows": [],
    }

    def collect(step: int) -> None:
        result = evaluate_checkpoint(model, cfg, condition, seed, step, initial_router_weight, device)
        for key, rows in result.items():
            out[key].extend(rows)

    print(f"audit {condition} seed={seed} step=0 device={device}", flush=True)
    collect(0)
    model.train()
    for step in range(1, steps + 1):
        batch_idx = [indices[rng.randrange(len(indices))] for _ in range(batch_size)]
        x = train_data.x[batch_idx].to(device)
        logits, info = model(x, return_acts=True)
        loss = runner.full_ntp_loss(logits, x)
        if cond.token_inhibition:
            inh, _ = runner.true_token_conditioned_inhibition_loss(
                model,
                info["ffn_input"][:, b_pos, :],
                info["expert_idx"][:, b_pos],
                info["router_logits"][:, b_pos, :],
                cfg,
            )
            loss = loss + float(cfg["true_token_inhibition"]["loss_weight"]) * inh
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(cfg["training"]["grad_clip"]))
        opt.step()
        if step in AUDIT_STEPS:
            print(f"audit {condition} seed={seed} step={step} device={device}", flush=True)
            collect(step)
            model.train()
    return out


def merge_results(results: list[dict[str, list[dict]]]) -> dict[str, list[dict]]:
    merged: dict[str, list[dict]] = {}
    for result in results:
        for key, rows in result.items():
            merged.setdefault(key, []).extend(rows)
    return merged


def copy_existing_log_tables(out_dir: Path) -> None:
    """Copy compact existing trajectory tables to document missing checkpoint coverage."""
    rows = []
    for condition in CONDITIONS:
        for seed in SEEDS:
            base = RAW_RESULT_DIR / "multi_b_primary" / condition / f"seed_{seed}"
            if not base.exists():
                continue
            for fname in ["trajectory_route_metrics_by_step.csv", "feature_key_consistency_by_step.csv"]:
                path = base / fname
                if path.exists():
                    for row in read_csv(path):
                        row = dict(row)
                        row["source_file"] = fname
                        rows.append(row)
    write_csv(out_dir / "tables/existing_checkpoint_coverage.csv", rows)


def plot_outputs(out_dir: Path) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    fig_dir = out_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    load_rows = read_csv(out_dir / "tables/audit_load_by_checkpoint.csv")
    slot_rows = read_csv(out_dir / "tables/audit_slot_assignment_by_checkpoint.csv")
    cos_rows = read_csv(out_dir / "tables/audit_slot_router_cosine_by_checkpoint.csv")
    margin_rows = read_csv(out_dir / "tables/audit_top1_margin_by_checkpoint.csv")
    common_rows = read_csv(out_dir / "tables/audit_common_direction_alignment.csv")
    router_rows = read_csv(out_dir / "tables/audit_router_vector_geometry.csv")
    pair_rows = read_csv(out_dir / "tables/audit_router_pairwise_cosine.csv")

    # 1. Collapse load timeline by seed/condition.
    colors = ["#386cb0", "#fdb462", "#1b9e77", "#756bb1"]
    fig, axes = plt.subplots(len(CONDITIONS), len(SEEDS), figsize=(14, 22), sharex=True, sharey=True)
    for r, condition in enumerate(CONDITIONS):
        for c, seed in enumerate(SEEDS):
            ax = axes[r, c]
            rows = [x for x in load_rows if x["condition"] == condition and int(x["seed"]) == seed]
            for expert in range(4):
                xs = [int(x["step"]) for x in rows if int(x["expert"]) == expert]
                ys = [float(x["fraction"]) for x in rows if int(x["expert"]) == expert]
                ax.plot(xs, ys, marker="o", markersize=2.8, linewidth=1.4, color=colors[expert], label=f"E{expert}")
            ax.axhline(COLLAPSE_THRESHOLD, linestyle="--", linewidth=0.9, color="#444444", alpha=0.55)
            ax.set_title(f"{condition} seed {seed}", fontsize=8)
            ax.grid(alpha=0.2)
            ax.set_ylim(-0.03, 1.03)
    for ax in axes[-1, :]:
        ax.set_xlabel("checkpoint")
    for ax in axes[:, 0]:
        ax.set_ylabel("load fraction")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=4, loc="lower center", frameon=False)
    fig.suptitle("Collapse load timeline by seed and condition", fontsize=14, y=0.995)
    fig.tight_layout(rect=(0, 0.025, 1, 0.985))
    fig.savefig(fig_dir / "collapse_load_timeline_by_seed_condition.png", dpi=180)
    plt.close(fig)

    def contact_heatmap(rows: list[dict], value_key: str, filename: str, title: str, vmin=None, vmax=None, cmap="viridis"):
        steps = [0, 10, 20, 50, 100, 200, 800, 1600]
        # Slot-aggregated contact sheet. Exact feature heatmaps are too large to read in one figure.
        fig, axes = plt.subplots(len(CONDITIONS) * len(SEEDS), len(steps), figsize=(18, 34))
        row_idx = 0
        for condition in CONDITIONS:
            for seed in SEEDS:
                for col, step in enumerate(steps):
                    ax = axes[row_idx, col]
                    sub = [x for x in rows if x["condition"] == condition and int(x["seed"]) == seed and int(x["step"]) == step]
                    mat = np.full((4, 4), np.nan)
                    for x in sub:
                        slot = int(x["slot"])
                        expert = int(x["expert"])
                        mat[slot, expert] = float(x[value_key])
                    im = ax.imshow(mat, aspect="auto", vmin=vmin, vmax=vmax, cmap=cmap)
                    if row_idx == 0:
                        ax.set_title(f"step {step}", fontsize=8)
                    if col == 0:
                        ax.set_ylabel(f"{condition}\n{seed}", fontsize=7)
                    ax.set_xticks([])
                    ax.set_yticks([])
                row_idx += 1
        fig.suptitle(title, fontsize=13, y=0.995)
        fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.5)
        fig.savefig(fig_dir / filename, dpi=170, bbox_inches="tight")
        plt.close(fig)

    contact_heatmap(
        slot_rows,
        "fraction",
        "feature_expert_assignment_timeline.png",
        "Slot-aggregated feature-to-expert assignment timeline",
        vmin=0,
        vmax=1,
        cmap="magma",
    )
    contact_heatmap(
        cos_rows,
        "cosine",
        "feature_router_cosine_timeline.png",
        "Slot centroid x router-vector cosine timeline",
        vmin=-1,
        vmax=1,
        cmap="coolwarm",
    )

    # 4. Top-1 margin dynamics.
    fig, axes = plt.subplots(4, 2, figsize=(13, 12), sharex=True)
    for ax, condition in zip(axes.flat, CONDITIONS):
        for seed in SEEDS:
            rows = [x for x in margin_rows if x["condition"] == condition and int(x["seed"]) == seed]
            xs = [int(x["step"]) for x in rows]
            ys = [float(x["top1_margin_mean"]) for x in rows]
            agree = [float(x["top1_equals_final_dominant_fraction"]) for x in rows]
            ax.plot(xs, ys, marker="o", linewidth=1.5, label=f"{seed} margin")
            ax.plot(xs, agree, marker="x", linewidth=1.0, linestyle="--", alpha=0.75, label=f"{seed} top1=final")
        ax.set_title(condition)
        ax.grid(alpha=0.2)
    for ax in axes[-1, :]:
        ax.set_xlabel("checkpoint")
    for ax in axes[:, 0]:
        ax.set_ylabel("value")
    fig.suptitle("Top-1 margin and early agreement with final dominant expert", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(fig_dir / "top1_margin_dynamics.png", dpi=180)
    plt.close(fig)

    # 5. Common direction alignment.
    final_dom = final_dominants(load_rows)
    fig, axes = plt.subplots(len(CONDITIONS), len(SEEDS), figsize=(14, 22), sharex=True, sharey=True)
    for r, condition in enumerate(CONDITIONS):
        for c, seed in enumerate(SEEDS):
            ax = axes[r, c]
            rows = [x for x in common_rows if x["condition"] == condition and int(x["seed"]) == seed]
            dom = final_dom[(condition, seed)]
            for expert in range(4):
                xs = [int(x["step"]) for x in rows if int(x["expert"]) == expert]
                ys = [float(x["common_direction_cosine"]) for x in rows if int(x["expert"]) == expert]
                lw = 2.4 if expert == dom else 1.1
                ax.plot(xs, ys, marker="o", markersize=2.5, linewidth=lw, color=colors[expert], label=f"E{expert}")
            ax.axhline(0, color="#444444", linewidth=0.6)
            ax.set_title(f"{condition} seed {seed}; final E{dom}", fontsize=8)
            ax.grid(alpha=0.2)
            ax.set_ylim(-1.03, 1.03)
    for ax in axes[-1, :]:
        ax.set_xlabel("checkpoint")
    for ax in axes[:, 0]:
        ax.set_ylabel("cos(w_e, common)")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=4, loc="lower center", frameon=False)
    fig.suptitle("Common-direction alignment; final dominant expert highlighted", fontsize=14, y=0.995)
    fig.tight_layout(rect=(0, 0.025, 1, 0.985))
    fig.savefig(fig_dir / "common_direction_alignment.png", dpi=180)
    plt.close(fig)

    # 6. Router geometry.
    fig, axes = plt.subplots(4, 2, figsize=(13, 12), sharex=True)
    for ax, condition in zip(axes.flat, CONDITIONS):
        for seed in SEEDS:
            rows = [x for x in router_rows if x["condition"] == condition and int(x["seed"]) == seed]
            by_step = {}
            for x in rows:
                by_step.setdefault(int(x["step"]), []).append(float(x["delta_from_init"]))
            xs = sorted(by_step)
            ys = [sum(by_step[s]) / len(by_step[s]) for s in xs]
            ax.plot(xs, ys, marker="o", linewidth=1.4, label=str(seed))
        ax.set_title(condition)
        ax.grid(alpha=0.2)
    for ax in axes[-1, :]:
        ax.set_xlabel("checkpoint")
    for ax in axes[:, 0]:
        ax.set_ylabel("mean ||w_e(t)-w_e(0)||")
    fig.suptitle("Router vector movement from initialization", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(fig_dir / "router_geometry_timeline.png", dpi=180)
    plt.close(fig)

    # Additional pairwise cosine table visualization for the most collapse-relevant S0/S1-cos pair.
    fig, axes = plt.subplots(6, 4, figsize=(11, 15))
    idx = 0
    for condition in ["S0-cos", "S1-cos"]:
        for seed in SEEDS:
            for step in [0, 100, 1600]:
                ax = axes.flat[idx]
                mat = np.full((4, 4), np.nan)
                for x in pair_rows:
                    if x["condition"] == condition and int(x["seed"]) == seed and int(x["step"]) == step:
                        mat[int(x["expert_i"]), int(x["expert_j"])] = float(x["cosine"])
                ax.imshow(mat, vmin=-1, vmax=1, cmap="coolwarm")
                ax.set_title(f"{condition} {seed} step {step}", fontsize=8)
                ax.set_xticks([])
                ax.set_yticks([])
                idx += 1
    fig.suptitle("Router expert-expert cosine matrices: key cosine conditions", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(fig_dir / "router_pairwise_cosine_key_conditions.png", dpi=180)
    plt.close(fig)


def final_dominants(load_rows: list[dict]) -> dict[tuple[str, int], int]:
    out = {}
    for condition in CONDITIONS:
        for seed in SEEDS:
            rows = [x for x in load_rows if x["condition"] == condition and int(x["seed"]) == seed]
            max_step = max(int(x["step"]) for x in rows)
            final = [x for x in rows if int(x["step"]) == max_step]
            dom = max(final, key=lambda x: float(x["fraction"]))
            out[(condition, seed)] = int(dom["expert"])
    return out


def add_final_dominant_agreement(out_dir: Path) -> None:
    load_rows = read_csv(out_dir / "tables/audit_load_by_checkpoint.csv")
    margin_rows = read_csv(out_dir / "tables/audit_top1_margin_by_checkpoint.csv")
    dom = final_dominants(load_rows)
    new_rows = []
    for row in margin_rows:
        condition = row["condition"]
        seed = int(row["seed"])
        final_e = dom[(condition, seed)]
        row = dict(row)
        row["final_dominant_expert"] = final_e
        row["top1_equals_final_dominant_fraction"] = row[f"top1_expert_{final_e}_fraction"]
        new_rows.append(row)
    write_csv(out_dir / "tables/audit_top1_margin_by_checkpoint.csv", new_rows)


def write_timing_table(out_dir: Path) -> None:
    load_rows = read_csv(out_dir / "tables/audit_load_by_checkpoint.csv")
    by_run = {}
    for row in load_rows:
        key = (row["condition"], int(row["seed"]))
        by_run.setdefault(key, []).append(row)
    timing = []
    for (condition, seed), rows in sorted(by_run.items()):
        by_step = {}
        for row in rows:
            if int(row["expert"]) == int(row["dominant_expert"]):
                by_step[int(row["step"])] = row
        final_step = max(by_step)
        final = by_step[final_step]
        first = None
        for step in sorted(by_step):
            row = by_step[step]
            if int(row["collapsed"]) == 1:
                first = step
                break
        if first is None:
            label = "not_collapsed"
        elif first == 0:
            label = "step0"
        elif first <= 100:
            label = "early"
        else:
            label = "late"
        final_dom = int(final["dominant_expert"])
        timing.append(
            {
                "condition": condition,
                "seed": seed,
                "final_collapsed": int(final["collapsed"]),
                "collapse_first_step": "" if first is None else first,
                "collapse_timing": label,
                "final_dominant_expert": final_dom,
                "step0_dominant_expert": int(by_step[0]["dominant_expert"]),
                "step10_dominant_expert": int(by_step[10]["dominant_expert"]),
                "step20_dominant_expert": int(by_step[20]["dominant_expert"]),
                "step50_dominant_expert": int(by_step[50]["dominant_expert"]),
                "step100_dominant_expert": int(by_step[100]["dominant_expert"]),
                "same_dominant_step0_final": int(int(by_step[0]["dominant_expert"]) == final_dom),
                "same_dominant_step10_final": int(int(by_step[10]["dominant_expert"]) == final_dom),
                "same_dominant_step20_final": int(int(by_step[20]["dominant_expert"]) == final_dom),
                "same_dominant_step50_final": int(int(by_step[50]["dominant_expert"]) == final_dom),
                "same_dominant_step100_final": int(int(by_step[100]["dominant_expert"]) == final_dom),
                "step0_max_fraction": by_step[0]["max_load_fraction"],
                "step10_max_fraction": by_step[10]["max_load_fraction"],
                "step20_max_fraction": by_step[20]["max_load_fraction"],
                "step50_max_fraction": by_step[50]["max_load_fraction"],
                "step100_max_fraction": by_step[100]["max_load_fraction"],
                "final_max_fraction": final["max_load_fraction"],
                "step0_entropy_norm": by_step[0]["load_entropy_norm"],
                "step100_entropy_norm": by_step[100]["load_entropy_norm"],
                "final_entropy_norm": final["load_entropy_norm"],
            }
        )
    write_csv(out_dir / "tables/audit_collapse_timing_by_seed.csv", timing)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--device-prefix", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--plot-only", action="store_true")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    (out_dir / "tables").mkdir(parents=True, exist_ok=True)
    (out_dir / "figures").mkdir(parents=True, exist_ok=True)

    if not args.plot_only:
        tasks = []
        device_count = torch.cuda.device_count() if torch.cuda.is_available() and args.device_prefix == "cuda" else 1
        for i, condition in enumerate(CONDITIONS):
            for j, seed in enumerate(SEEDS):
                tasks.append((condition, seed, args.device_prefix, (i * len(SEEDS) + j) % max(1, device_count)))
        results = []
        with ProcessPoolExecutor(max_workers=args.workers, mp_context=mp.get_context("spawn")) as ex:
            futs = [ex.submit(audit_one, task) for task in tasks]
            for fut in as_completed(futs):
                results.append(fut.result())
        merged = merge_results(results)
        write_csv(out_dir / "tables/audit_load_by_checkpoint.csv", merged["load_rows"])
        write_csv(out_dir / "tables/audit_slot_assignment_by_checkpoint.csv", merged["slot_assignment_rows"])
        write_csv(out_dir / "tables/audit_slot_router_cosine_by_checkpoint.csv", merged["slot_cos_rows"])
        write_csv(out_dir / "tables/audit_common_direction_alignment.csv", merged["common_rows"])
        write_csv(out_dir / "tables/audit_slot_residual_alignment.csv", merged["slot_residual_rows"])
        write_csv(out_dir / "tables/audit_router_vector_geometry.csv", merged["router_rows"])
        write_csv(out_dir / "tables/audit_router_pairwise_cosine.csv", merged["pair_rows"])
        write_csv(out_dir / "tables/audit_top1_margin_by_checkpoint.csv", merged["margin_rows"])
        write_csv(out_dir / "tables/audit_slot_main_expert_feature_fraction.csv", merged["feature_summary_rows"])
        add_final_dominant_agreement(out_dir)
        write_timing_table(out_dir)
        copy_existing_log_tables(out_dir)
    plot_outputs(out_dir)


if __name__ == "__main__":
    main()

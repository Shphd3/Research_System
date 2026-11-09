#!/usr/bin/env python3
"""Run A05_03 support/later protocols P4-P7.

This script deliberately writes separate remaining_* artifacts so that the
already-audited P0-P3 tables are not overwritten.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

import torch
from torch.nn import functional as F


EXP_DIR = Path(__file__).resolve().parents[1]
RESEARCH_ROOT = EXP_DIR.parents[4]
WORKSPACE = (
    RESEARCH_ROOT
    / "Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding"
)

sys.path.insert(0, str(EXP_DIR / "scripts"))
sys.path.insert(0, str(WORKSPACE / "scripts"))
sys.path.insert(0, str(WORKSPACE / "src"))

import run_a05_03_common_offset_experiments as base  # noqa: E402
import run_h0605a_true_token_conditioned_inhibition_replay as runner  # noqa: E402


PATTERNS = base.PATTERNS
SEEDS = base.SEEDS
METRIC = "dot_product"
P4_VARIANTS = [
    "I0_default",
    "I1_reduced_scale_0p25",
    "I2_common_orthogonal_rescale",
    "I3_common_score_matched",
    "I4_residual_subspace_orthogonal",
]
P4_TRAIN_VARIANTS = P4_VARIANTS
P5_VARIANTS = [
    "P5A_frozen_projection_residual",
    "P5B_logit_common_offset_cancel",
    "P5C_row_common_orthogonalize",
    "P5D_ema_mean_residual",
    "P5E_lowrank1_residual",
]
P6_VARIANTS = [
    "P6A_aux_load_balance_warmup",
    "P6B_dynamic_bias_warmup",
]
P7_VARIANTS = [
    "baseline_full_hidden",
    "logit_common_offset_cancel",
]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    fields = list(rows[0].keys())
    seen = set(fields)
    for row in rows[1:]:
        for key in row:
            if key not in seen:
                fields.append(key)
                seen.add(key)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True))


def parse_csv_ints(value: str, default: list[int]) -> list[int]:
    if not value:
        return default
    return [int(v.strip()) for v in value.split(",") if v.strip()]


def row_geometry(model, c: torch.Tensor) -> dict:
    w = model.moe.router.weight.detach().cpu().float()
    c = c.detach().cpu().float()
    c_unit = F.normalize(c.view(1, -1), p=2, dim=1).view(-1)
    scores = w @ c
    scores_unit = w @ c_unit
    norms = w.norm(dim=1)
    cos = F.normalize(w, p=2, dim=1) @ F.normalize(w, p=2, dim=1).T
    off_diag = cos[~torch.eye(cos.shape[0], dtype=torch.bool)]
    return {
        "common_scores": " ".join(f"{float(v):.6f}" for v in scores),
        "common_score_std": float(scores.std(unbiased=False).item()),
        "common_score_range": float((scores.max() - scores.min()).item()),
        "unit_common_scores": " ".join(f"{float(v):.6f}" for v in scores_unit),
        "router_row_norms": " ".join(f"{float(v):.6f}" for v in norms),
        "router_row_norm_mean": float(norms.mean().item()),
        "router_pairwise_cosine_mean": float(off_diag.mean().item()),
        "router_pairwise_cosine_abs_mean": float(off_diag.abs().mean().item()),
    }


def common_direction_for_model(cfg: dict, model, pattern: str, seed: int, variants: int, device: torch.device, batch_size: int) -> torch.Tensor:
    _, c0 = base.step0_diagnostic(cfg, model, pattern, METRIC, seed, variants, device, batch_size)
    return c0


def apply_p4_init(model, variant: str, c: torch.Tensor) -> None:
    if variant == "I0_default":
        return
    with torch.no_grad():
        w = model.moe.router.weight
        c_dev = c.to(w.device).float()
        c_unit = F.normalize(c_dev.view(1, -1), p=2, dim=1).view(-1)
        old_norm = w.norm(dim=1, keepdim=True).clamp_min(1e-12)
        if variant == "I1_reduced_scale_0p25":
            w.mul_(0.25)
            return
        if variant == "I2_common_orthogonal_rescale":
            proj = (w @ c_unit).unsqueeze(1) * c_unit.view(1, -1)
            w.sub_(proj)
            w.mul_(old_norm / w.norm(dim=1, keepdim=True).clamp_min(1e-12))
            return
        if variant == "I3_common_score_matched":
            scores = w @ c_dev
            target = scores.mean()
            adjust = ((target - scores) / c_dev.dot(c_dev).clamp_min(1e-12)).unsqueeze(1) * c_dev.view(1, -1)
            w.add_(adjust)
            return
        if variant == "I4_residual_subspace_orthogonal":
            proj = (w @ c_unit).unsqueeze(1) * c_unit.view(1, -1)
            residual = w - proj
            q, _ = torch.linalg.qr(residual.T, mode="reduced")
            new_w = q.T[: w.shape[0]]
            new_w.mul_(old_norm)
            w.copy_(new_w)
            return
    raise ValueError(f"unknown P4 init variant {variant}")


def install_projection_residual_router(model, c: torch.Tensor, beta: float = 1.0):
    original_router_logits = model.moe.router_logits
    c_dev_cache = c.detach().float()

    def projected_router_logits(x: torch.Tensor) -> torch.Tensor:
        c_dev = c_dev_cache.to(x.device)
        c_unit = F.normalize(c_dev.view(1, -1), p=2, dim=1).view(-1)
        proj = (x.float() @ c_unit).unsqueeze(-1) * c_unit.view(*([1] * (x.ndim - 1)), -1)
        return original_router_logits(x - beta * proj.to(x.dtype))

    model.moe.router_logits = projected_router_logits  # type: ignore[method-assign]


def install_lowrank_router(model, u: torch.Tensor, beta: float = 1.0):
    original_router_logits = model.moe.router_logits
    u_cache = u.detach().float()

    def lowrank_router_logits(x: torch.Tensor) -> torch.Tensor:
        u_dev = u_cache.to(x.device)
        coeff = x.float() @ u_dev
        proj = coeff.unsqueeze(-1) * u_dev.view(*([1] * (x.ndim - 1)), -1)
        return original_router_logits(x - beta * proj.to(x.dtype))

    model.moe.router_logits = lowrank_router_logits  # type: ignore[method-assign]


def install_ema_router(model, c0: torch.Tensor, momentum: float = 0.99, beta: float = 1.0) -> dict:
    original_router_logits = model.moe.router_logits
    state = {"mu": c0.detach().cpu().float(), "momentum": momentum, "beta": beta}

    def ema_router_logits(x: torch.Tensor) -> torch.Tensor:
        mu = state["mu"].to(x.device)
        return original_router_logits(x - state["beta"] * mu.view(*([1] * (x.ndim - 1)), -1).to(x.dtype))

    model.moe.router_logits = ema_router_logits  # type: ignore[method-assign]
    return state


def update_ema_state(state: dict | None, h_batch: torch.Tensor) -> None:
    if state is None:
        return
    with torch.no_grad():
        mu = state["mu"]
        batch_mu = h_batch.detach().cpu().float().mean(dim=0)
        state["mu"] = state["momentum"] * mu + (1.0 - state["momentum"]) * batch_mu


def orthogonalize_rows_to_c(model, c: torch.Tensor) -> None:
    with torch.no_grad():
        w = model.moe.router.weight
        c_unit = F.normalize(c.to(w.device).float().view(1, -1), p=2, dim=1).view(-1)
        old_norm = w.norm(dim=1, keepdim=True).clamp_min(1e-12)
        w.sub_((w @ c_unit).unsqueeze(1) * c_unit.view(1, -1))
        w.mul_(old_norm / w.norm(dim=1, keepdim=True).clamp_min(1e-12))


def estimate_lowrank_u(cfg: dict, model, pattern: str, seed: int, variants: int, device: torch.device, batch_size: int) -> torch.Tensor:
    grid = base.generate_feature_grid(cfg, pattern, seed, variants)
    data = base.feature_hidden(model, cfg, grid, device, batch_size)
    h_feat, _ = base.feature_centroids(data, cfg)
    centered = h_feat - h_feat.mean(dim=0, keepdim=True)
    _, _, vh = torch.linalg.svd(centered, full_matrices=False)
    return vh[0].detach().cpu().float()


def eval_state(
    cfg: dict,
    model,
    pattern: str,
    seed: int,
    protocol: str,
    variant: str,
    step: int,
    variants_per_key: int,
    device: torch.device,
    batch_size: int,
    c0: torch.Tensor,
) -> tuple[dict, list[dict]]:
    row, heat = base.eval_training_state(
        cfg,
        model,
        pattern,
        METRIC,
        seed,
        variant,
        step,
        variants_per_key,
        device,
        batch_size,
        c0,
    )
    row["protocol"] = protocol
    row["variant"] = variant
    row.update(row_geometry(model, c0))
    for h in heat:
        h["protocol"] = protocol
        h["variant"] = variant
    return row, heat


def train_variant(
    cfg: dict,
    pattern: str,
    seed: int,
    protocol: str,
    variant: str,
    args,
    device: torch.device,
    return_model: bool = False,
):
    model = base.actual_model(cfg, METRIC, seed, device)
    c0 = common_direction_for_model(cfg, model, pattern, seed, args.variants_per_key, device, args.eval_batch_size)
    ema_state = None
    dynamic_bias_state = None

    if protocol == "P4":
        apply_p4_init(model, variant, c0)
    elif protocol == "P5":
        if variant == "P5A_frozen_projection_residual":
            install_projection_residual_router(model, c0, beta=1.0)
        elif variant == "P5B_logit_common_offset_cancel":
            base.install_logit_correction(model, METRIC, c0)
        elif variant == "P5C_row_common_orthogonalize":
            orthogonalize_rows_to_c(model, c0)
        elif variant == "P5D_ema_mean_residual":
            ema_state = install_ema_router(model, c0, momentum=args.ema_momentum, beta=1.0)
        elif variant == "P5E_lowrank1_residual":
            u = estimate_lowrank_u(cfg, model, pattern, seed, args.variants_per_key, device, args.eval_batch_size)
            install_lowrank_router(model, u, beta=1.0)
        else:
            raise ValueError(f"unknown P5 variant {variant}")
    elif protocol == "P6":
        if variant == "P6B_dynamic_bias_warmup":
            original_router_logits = model.moe.router_logits
            num_experts = int(cfg["model"]["num_experts"])
            dynamic_bias_state = {
                "bias": torch.zeros(num_experts),
                "ema": torch.full((num_experts,), 1.0 / num_experts),
            }

            def biased_router_logits(x: torch.Tensor) -> torch.Tensor:
                return original_router_logits(x) + dynamic_bias_state["bias"].to(x.device).view(
                    *([1] * (x.ndim - 1)), -1
                )

            model.moe.router_logits = biased_router_logits  # type: ignore[method-assign]
        elif variant != "P6A_aux_load_balance_warmup":
            raise ValueError(f"unknown P6 variant {variant}")
    elif protocol == "P7":
        if variant == "logit_common_offset_cancel":
            base.install_logit_correction(model, METRIC, c0)
        elif variant != "baseline_full_hidden":
            raise ValueError(f"unknown P7 variant {variant}")
    else:
        raise ValueError(f"unknown protocol {protocol}")

    train_data = base.generate_train_data(cfg, pattern, args.train_samples_per_slot, seed)
    opt = torch.optim.AdamW(
        model.parameters(),
        lr=float(cfg["training"]["lr"]),
        weight_decay=float(cfg["training"]["weight_decay"]),
    )
    rng = random.Random(seed + hash((protocol, variant)) % 100000)
    indices = list(range(train_data.x.shape[0]))
    eval_steps = sorted({0, 10, 20, 50, 100, 200, args.train_steps})
    eval_steps = [s for s in eval_steps if s <= args.train_steps]
    metric_rows, heat_rows = [], []
    b_pos = int(cfg["data"]["b_position"])
    num_experts = int(cfg["model"]["num_experts"])
    uniform = torch.full((num_experts,), 1.0 / num_experts, device=device)

    for step in range(args.train_steps + 1):
        if step in eval_steps:
            row, heat = eval_state(
                cfg,
                model,
                pattern,
                seed,
                protocol,
                variant,
                step,
                args.variants_per_key,
                device,
                args.eval_batch_size,
                c0,
            )
            metric_rows.append(row)
            heat_rows.extend(heat)
        if step == args.train_steps:
            break

        model.train()
        batch_idx = [indices[rng.randrange(len(indices))] for _ in range(args.batch_size)]
        x = train_data.x[batch_idx].to(device)
        logits, info = model(x, return_acts=True)
        loss = runner.full_ntp_loss(logits, x)

        if protocol == "P6" and variant == "P6A_aux_load_balance_warmup" and step < args.warmup_steps:
            probs = info["router_probs"][:, b_pos, :]
            loss = loss + args.load_balance_weight * ((probs.mean(dim=0) - uniform) ** 2).sum()

        update_ema_state(ema_state, info["ffn_input"][:, b_pos, :])
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(cfg["training"]["grad_clip"]))
        opt.step()

        if protocol == "P5" and variant == "P5C_row_common_orthogonalize":
            orthogonalize_rows_to_c(model, c0)

        if dynamic_bias_state is not None:
            with torch.no_grad():
                load = torch.bincount(info["expert_idx"][:, b_pos].detach().cpu(), minlength=num_experts).float()
                load = load / load.sum().clamp_min(1.0)
                dynamic_bias_state["ema"] = (
                    args.load_ema_momentum * dynamic_bias_state["ema"]
                    + (1.0 - args.load_ema_momentum) * load
                )
                if step < args.warmup_steps:
                    dynamic_bias_state["bias"] = -args.dynamic_bias_strength * (
                        dynamic_bias_state["ema"] - 1.0 / num_experts
                    )
                else:
                    dynamic_bias_state["bias"].zero_()

    if return_model:
        return metric_rows, heat_rows, model, c0
    return metric_rows, heat_rows


def collapse_rate(items: list[dict]) -> float:
    if not items:
        return math.nan
    return sum(1 for r in items if float(r["max_load"]) >= 0.95 or int(r["active_experts"]) <= 1) / len(items)


def summarize_training(rows: list[dict], train_steps: int) -> list[dict]:
    final_rows = [r for r in rows if int(r["step"]) == train_steps]
    grouped = defaultdict(list)
    for row in final_rows:
        grouped[(row["protocol"], row["pattern"], row["variant"])].append(row)
    out = []
    for key, items in grouped.items():
        n = len(items)
        out.append(
            {
                "protocol": key[0],
                "pattern": key[1],
                "variant": key[2],
                "n": n,
                "final_collapse_rate": collapse_rate(items),
                "final_max_load_mean": sum(float(r["max_load"]) for r in items) / n if n else math.nan,
                "final_load_entropy_mean": sum(float(r["load_entropy_norm"]) for r in items) / n if n else math.nan,
                "target_accuracy_mean": sum(float(r["target_accuracy"]) for r in items) / n if n else math.nan,
                "feature_key_consistency_mean": sum(float(r["feature_key_consistency"]) for r in items) / n if n else math.nan,
                "common_score_std_mean": sum(float(r["common_score_std"]) for r in items) / n if n else math.nan,
                "common_score_range_mean": sum(float(r["common_score_range"]) for r in items) / n if n else math.nan,
            }
        )
    return out


def p4_step0_rows(cfg: dict, args, device: torch.device) -> list[dict]:
    rows = []
    for pattern in PATTERNS:
        for seed in args.seeds:
            base_model = base.actual_model(cfg, METRIC, seed, device)
            c0 = common_direction_for_model(cfg, base_model, pattern, seed, args.variants_per_key, device, args.eval_batch_size)
            for variant in P4_VARIANTS:
                model = base.actual_model(cfg, METRIC, seed, device)
                apply_p4_init(model, variant, c0)
                grid = base.generate_feature_grid(cfg, pattern, seed, args.variants_per_key)
                data = base.feature_hidden(model, cfg, grid, device, args.eval_batch_size)
                h_feat, _ = base.feature_centroids(data, cfg)
                scores = base.router_scores(model, h_feat, METRIC)
                top = scores.argmax(dim=1)
                load = base.load_from_top(top, int(cfg["model"]["num_experts"]))
                top2 = torch.topk(scores, 2, dim=1).values
                row = {
                    "protocol": "P4",
                    "pattern": pattern,
                    "seed": seed,
                    "variant": variant,
                    "step0_loads": " ".join(f"{v:.6f}" for v in load),
                    "step0_max_load": max(load),
                    "step0_load_entropy_norm": base.entropy_norm(load),
                    "step0_mean_top1_margin": float((top2[:, 0] - top2[:, 1]).mean().item()),
                    "step0_dominant_expert": int(max(range(len(load)), key=lambda i: load[i])),
                }
                row.update(row_geometry(model, c0))
                rows.append(row)
    return rows


def force_utility_matrix(
    cfg: dict,
    model,
    pattern: str,
    seed: int,
    protocol_variant: str,
    variants_per_key: int,
    device: torch.device,
    batch_size: int,
) -> tuple[list[dict], list[dict]]:
    grid = base.generate_feature_grid(cfg, pattern, seed, variants_per_key)
    b_pos = int(cfg["data"]["b_position"])
    num_experts = int(cfg["model"]["num_experts"])
    rows = []
    sample_rows = []
    model.eval()
    with torch.no_grad():
        for start in range(0, grid.x.shape[0], batch_size):
            x = grid.x[start : start + batch_size].to(device)
            logits, info = model(x, return_acts=True)
            default_route = info["expert_idx"].detach()
            router_chosen = default_route[:, b_pos].detach().cpu()
            losses = []
            probs = []
            for expert in range(num_experts):
                force = default_route.clone()
                force[:, b_pos] = expert
                flogits, _ = model(x, return_acts=True, force_expert_idx=force)
                token_logits = flogits[:, b_pos, :]
                target = grid.target[start : start + batch_size].to(device)
                losses.append(F.cross_entropy(token_logits, target, reduction="none").detach().cpu())
                probs.append(F.softmax(token_logits, dim=-1).gather(1, target.view(-1, 1)).view(-1).detach().cpu())
            loss_mat = torch.stack(losses, dim=1)
            prob_mat = torch.stack(probs, dim=1)
            best_loss_expert = loss_mat.argmin(dim=1)
            best_prob_expert = prob_mat.argmax(dim=1)
            for i in range(x.shape[0]):
                sample_rows.append(
                    {
                        "pattern": pattern,
                        "seed": seed,
                        "variant": protocol_variant,
                        "slot": int(grid.slot[start + i].item()),
                        "b_idx": int(grid.b_idx[start + i].item()),
                        "router_chosen_expert": int(router_chosen[i].item()),
                        "best_loss_expert": int(best_loss_expert[i].item()),
                        "best_prob_expert": int(best_prob_expert[i].item()),
                        "loss_by_expert": " ".join(f"{float(v):.6f}" for v in loss_mat[i]),
                        "prob_by_expert": " ".join(f"{float(v):.6f}" for v in prob_mat[i]),
                    }
                )

    grouped = defaultdict(list)
    for row in sample_rows:
        grouped[(row["slot"], row["b_idx"])].append(row)
    feature_best_counts = Counter()
    feature_router_counts = Counter()
    utility_match = []
    utility_gap = []
    for (slot, b_idx), items in grouped.items():
        router_mode = Counter(int(r["router_chosen_expert"]) for r in items).most_common(1)[0][0]
        best_mode = Counter(int(r["best_loss_expert"]) for r in items).most_common(1)[0][0]
        losses_by_expert = [[] for _ in range(num_experts)]
        for r in items:
            vals = [float(v) for v in r["loss_by_expert"].split()]
            for expert, val in enumerate(vals):
                losses_by_expert[expert].append(val)
        mean_losses = [sum(vs) / len(vs) for vs in losses_by_expert]
        sorted_losses = sorted(mean_losses)
        feature_best_counts[best_mode] += 1
        feature_router_counts[router_mode] += 1
        utility_match.append(int(router_mode == best_mode))
        utility_gap.append(sorted_losses[1] - sorted_losses[0])
        rows.append(
            {
                "pattern": pattern,
                "seed": seed,
                "variant": protocol_variant,
                "slot": slot,
                "b_idx": b_idx,
                "router_mode_expert": router_mode,
                "best_loss_expert": best_mode,
                "router_matches_best": int(router_mode == best_mode),
                "utility_gap_loss": sorted_losses[1] - sorted_losses[0],
                "mean_loss_by_expert": " ".join(f"{v:.6f}" for v in mean_losses),
            }
        )
    summary = {
        "protocol": "P7",
        "pattern": pattern,
        "seed": seed,
        "variant": protocol_variant,
        "num_features": len(grouped),
        "route_utility_match_rate": sum(utility_match) / len(utility_match) if utility_match else math.nan,
        "mean_utility_gap_loss": sum(utility_gap) / len(utility_gap) if utility_gap else math.nan,
        "best_expert_load_distribution": " ".join(
            f"{feature_best_counts[e] / max(1, len(grouped)):.6f}" for e in range(num_experts)
        ),
        "router_expert_load_distribution": " ".join(
            f"{feature_router_counts[e] / max(1, len(grouped)):.6f}" for e in range(num_experts)
        ),
        "best_expert_max_fraction": max(feature_best_counts.values()) / max(1, len(grouped)) if feature_best_counts else math.nan,
        "router_expert_max_fraction": max(feature_router_counts.values()) / max(1, len(grouped)) if feature_router_counts else math.nan,
    }
    return [summary], rows


def make_remaining_figures(fig_dir: Path, p4_step0: list[dict], training_rows: list[dict], p7_summary: list[dict], train_steps: int) -> None:
    import matplotlib.pyplot as plt

    fig_dir.mkdir(parents=True, exist_ok=True)

    if p4_step0:
        labels, vals, stds = [], [], []
        grouped = defaultdict(list)
        for row in p4_step0:
            grouped[(row["pattern"], row["variant"])].append(row)
        for key, items in grouped.items():
            labels.append(f"{key[0]}\n{key[1]}")
            vals.append(sum(float(r["step0_max_load"]) for r in items) / len(items))
            stds.append(sum(float(r["common_score_std"]) for r in items) / len(items))
        fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        axes[0].bar(range(len(labels)), vals, color="tab:blue")
        axes[0].axhline(0.25, color="tab:red", linestyle=":", linewidth=1)
        axes[0].set_ylabel("mean step0 max load")
        axes[0].set_title("P4 initialization: step-0 routing load")
        axes[0].grid(axis="y", alpha=0.25)
        axes[1].bar(range(len(labels)), stds, color="tab:orange")
        axes[1].set_ylabel("mean common-score std")
        axes[1].set_title("P4 initialization: common-score variance")
        axes[1].set_xticks(range(len(labels)))
        axes[1].set_xticklabels(labels, rotation=75, ha="right", fontsize=7)
        axes[1].grid(axis="y", alpha=0.25)
        fig.tight_layout()
        fig.savefig(fig_dir / "remaining_p4_init_step0.png", dpi=180)
        plt.close(fig)

    if training_rows:
        final_rows = [r for r in training_rows if int(r["step"]) == train_steps]
        labels = [f"{r['protocol']}\n{r['pattern']}\n{r['variant']}\n{r['seed']}" for r in final_rows]
        max_load = [float(r["max_load"]) for r in final_rows]
        acc = [float(r["target_accuracy"]) for r in final_rows]
        fig, axes = plt.subplots(2, 1, figsize=(max(12, len(labels) * 0.35), 7), sharex=True)
        axes[0].bar(range(len(labels)), max_load)
        axes[0].axhline(0.95, color="tab:red", linestyle=":", linewidth=1)
        axes[0].set_ylabel("final max load")
        axes[0].set_title("P4/P5/P6 final routing load by seed")
        axes[0].grid(axis="y", alpha=0.25)
        axes[1].bar(range(len(labels)), acc)
        axes[1].set_ylabel("final target accuracy")
        axes[1].set_ylim(0.85, 1.01)
        axes[1].set_title("P4/P5/P6 final target accuracy by seed")
        axes[1].set_xticks(range(len(labels)))
        axes[1].set_xticklabels(labels, rotation=80, ha="right", fontsize=6)
        axes[1].grid(axis="y", alpha=0.25)
        fig.tight_layout()
        fig.savefig(fig_dir / "remaining_p4_p5_p6_final_by_seed.png", dpi=180)
        plt.close(fig)

        summary = summarize_training(training_rows, train_steps)
        labels = [f"{r['protocol']}\n{r['pattern']}\n{r['variant']}" for r in summary]
        vals = [float(r["final_max_load_mean"]) for r in summary]
        accs = [float(r["target_accuracy_mean"]) for r in summary]
        fig, axes = plt.subplots(2, 1, figsize=(max(12, len(labels) * 0.45), 7), sharex=True)
        axes[0].bar(range(len(labels)), vals)
        axes[0].axhline(0.95, color="tab:red", linestyle=":", linewidth=1)
        axes[0].set_ylabel("mean final max load")
        axes[0].set_title("P4/P5/P6 mean final load")
        axes[0].grid(axis="y", alpha=0.25)
        axes[1].bar(range(len(labels)), accs)
        axes[1].set_ylabel("mean target accuracy")
        axes[1].set_ylim(0.85, 1.01)
        axes[1].set_title("P4/P5/P6 mean target accuracy")
        axes[1].set_xticks(range(len(labels)))
        axes[1].set_xticklabels(labels, rotation=80, ha="right", fontsize=6)
        axes[1].grid(axis="y", alpha=0.25)
        fig.tight_layout()
        fig.savefig(fig_dir / "remaining_p4_p5_p6_summary.png", dpi=180)
        plt.close(fig)

    if p7_summary:
        labels = [f"{r['pattern']}\n{r['variant']}\n{r['seed']}" for r in p7_summary]
        match = [float(r["route_utility_match_rate"]) for r in p7_summary]
        bestmax = [float(r["best_expert_max_fraction"]) for r in p7_summary]
        routermax = [float(r["router_expert_max_fraction"]) for r in p7_summary]
        fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
        axes[0].bar(range(len(labels)), match, color="tab:green")
        axes[0].set_ylabel("match rate")
        axes[0].set_title("P7 router-chosen expert vs forced-routing best expert")
        axes[0].grid(axis="y", alpha=0.25)
        axes[1].bar(range(len(labels)), bestmax, color="tab:purple")
        axes[1].set_ylabel("best expert max frac")
        axes[1].set_title("P7 utility-best expert concentration")
        axes[1].grid(axis="y", alpha=0.25)
        axes[2].bar(range(len(labels)), routermax, color="tab:blue")
        axes[2].set_ylabel("router max frac")
        axes[2].set_title("P7 router expert concentration")
        axes[2].set_xticks(range(len(labels)))
        axes[2].set_xticklabels(labels, rotation=75, ha="right", fontsize=7)
        axes[2].grid(axis="y", alpha=0.25)
        fig.tight_layout()
        fig.savefig(fig_dir / "remaining_p7_forced_utility.png", dpi=180)
        plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(base.WORKSPACE / "configs/h0605a_true_token_conditioned_inhibition_replay.json"))
    parser.add_argument("--output-dir", default=str(EXP_DIR))
    parser.add_argument("--seeds", default="20260521,20260522,20260523")
    parser.add_argument("--train-steps", type=int, default=400)
    parser.add_argument("--train-samples-per-slot", type=int, default=2000)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--eval-batch-size", type=int, default=512)
    parser.add_argument("--variants-per-key", type=int, default=4)
    parser.add_argument("--protocols", default="P4,P5,P6,P7")
    parser.add_argument("--warmup-steps", type=int, default=100)
    parser.add_argument("--load-balance-weight", type=float, default=2.0)
    parser.add_argument("--dynamic-bias-strength", type=float, default=4.0)
    parser.add_argument("--load-ema-momentum", type=float, default=0.9)
    parser.add_argument("--ema-momentum", type=float, default=0.99)
    args = parser.parse_args()
    args.seeds = parse_csv_ints(args.seeds, SEEDS)
    protocols = {p.strip() for p in args.protocols.split(",") if p.strip()}

    out_dir = Path(args.output_dir)
    table_dir = out_dir / "tables"
    fig_dir = out_dir / "figures"
    table_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    cfg = base.load_cfg(args.config)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    p4_step0 = []
    training_rows = []
    heat_rows = []
    p7_summary = []
    p7_feature_rows = []

    if "P4" in protocols:
        p4_step0 = p4_step0_rows(cfg, args, device)
        write_csv(table_dir / "remaining_p4_init_step0.csv", p4_step0)
        for pattern in PATTERNS:
            for variant in P4_TRAIN_VARIANTS:
                for seed in args.seeds:
                    rows, hrows = train_variant(cfg, pattern, seed, "P4", variant, args, device)
                    training_rows.extend(rows)
                    heat_rows.extend(hrows)
                    final = rows[-1]
                    print(
                        f"P4 pattern={pattern} variant={variant} seed={seed} "
                        f"final_max={float(final['max_load']):.3f} acc={float(final['target_accuracy']):.3f}",
                        flush=True,
                    )

    if "P5" in protocols:
        for pattern in PATTERNS:
            for variant in P5_VARIANTS:
                for seed in args.seeds:
                    rows, hrows = train_variant(cfg, pattern, seed, "P5", variant, args, device)
                    training_rows.extend(rows)
                    heat_rows.extend(hrows)
                    final = rows[-1]
                    print(
                        f"P5 pattern={pattern} variant={variant} seed={seed} "
                        f"final_max={float(final['max_load']):.3f} acc={float(final['target_accuracy']):.3f}",
                        flush=True,
                    )

    if "P6" in protocols:
        for pattern in PATTERNS:
            for variant in P6_VARIANTS:
                for seed in args.seeds:
                    rows, hrows = train_variant(cfg, pattern, seed, "P6", variant, args, device)
                    training_rows.extend(rows)
                    heat_rows.extend(hrows)
                    final = rows[-1]
                    print(
                        f"P6 pattern={pattern} variant={variant} seed={seed} "
                        f"final_max={float(final['max_load']):.3f} acc={float(final['target_accuracy']):.3f}",
                        flush=True,
                    )

    if "P7" in protocols:
        for pattern in PATTERNS:
            for variant in P7_VARIANTS:
                for seed in args.seeds:
                    rows, hrows, model, _ = train_variant(
                        cfg,
                        pattern,
                        seed,
                        "P7",
                        variant,
                        args,
                        device,
                        return_model=True,
                    )
                    training_rows.extend(rows)
                    heat_rows.extend(hrows)
                    srows, frows = force_utility_matrix(
                        cfg,
                        model,
                        pattern,
                        seed,
                        variant,
                        args.variants_per_key,
                        device,
                        args.eval_batch_size,
                    )
                    p7_summary.extend(srows)
                    p7_feature_rows.extend(frows)
                    print(
                        f"P7 pattern={pattern} variant={variant} seed={seed} "
                        f"match={float(srows[0]['route_utility_match_rate']):.3f} "
                        f"best_max={float(srows[0]['best_expert_max_fraction']):.3f}",
                        flush=True,
                    )

    write_csv(table_dir / "remaining_training_metrics_by_step.csv", training_rows)
    write_csv(table_dir / "remaining_training_summary_by_condition.csv", summarize_training(training_rows, args.train_steps))
    write_csv(table_dir / "remaining_slot_route_heatmap.csv", heat_rows)
    write_csv(table_dir / "remaining_p7_forced_utility_summary.csv", p7_summary)
    write_csv(table_dir / "remaining_p7_forced_utility_by_feature.csv", p7_feature_rows)
    make_remaining_figures(fig_dir, p4_step0, training_rows, p7_summary, args.train_steps)
    write_json(
        table_dir / "remaining_run_manifest.json",
        {
            "anchor": str(EXP_DIR.parent.parent / "problem_anchors/05_failure_mechanism/05_03_uniform_collapse_common_offset_anchor.md"),
            "protocol": str(EXP_DIR / "protocol_for_approval.md"),
            "runner": str(Path(__file__).resolve()),
            "config": str(args.config),
            "workspace": str(WORKSPACE),
            "device": str(device),
            "torch_cuda_available": torch.cuda.is_available(),
            "torch_cuda_device_count": torch.cuda.device_count(),
            "seeds": args.seeds,
            "patterns": PATTERNS,
            "metric": METRIC,
            "protocols": sorted(protocols),
            "p4_variants": P4_VARIANTS,
            "p5_variants": P5_VARIANTS,
            "p6_variants": P6_VARIANTS,
            "p7_variants": P7_VARIANTS,
            "train_steps": args.train_steps,
            "train_samples_per_slot": args.train_samples_per_slot,
            "batch_size": args.batch_size,
            "eval_batch_size": args.eval_batch_size,
            "variants_per_key": args.variants_per_key,
            "can_answer": {
                "P4": "yes for whether common-aware initialization reduces early and final load in the tested shortened run",
                "P5": "yes for comparing stable common-subtraction estimators in the tested shortened run",
                "P6": "yes for whether early anti-lockin pressure prevents amplification in the tested shortened run",
                "P7": "yes as a forced-routing utility diagnostic on the trained models; not a full utility theorem",
            },
        },
    )


if __name__ == "__main__":
    main()

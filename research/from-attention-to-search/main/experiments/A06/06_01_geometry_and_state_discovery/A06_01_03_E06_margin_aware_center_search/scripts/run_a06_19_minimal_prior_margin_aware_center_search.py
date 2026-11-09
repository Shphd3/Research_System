#!/usr/bin/env python3
"""Run A06_19 M1/M2 minimal-prior center-search sanity check."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from pathlib import Path

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

WORKSPACE = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(WORKSPACE / "src"))
sys.path.insert(0, str(SCRIPT_DIR))

import torch
from torch.nn import functional as F

from synthetic_data_understanding.io_utils import load_json, resolve_output, workspace_root, write_csv, write_json

from run_a06_04_real_hidden_state_gate_geometry_decomposition import (
    load_imbalance,
    parse_list,
    set_seed,
)
from run_a06_06_feature_level_initialization_positive_control import (
    feature_centroids,
    margin_stats,
    normalized_mutual_info,
    purity_from_heatmap,
)
from run_a06_16_synthetic_to_realistic_proxy_bridge import (
    ALL_POSITION_CELL,
    BridgeBatch,
    BridgeMoELM,
    aggregate_mean_std,
    collect_hidden,
    feature_expert_heatmap_rows,
    fit_bridge_kmeans,
    generate_bridge_batch,
    router_scores,
)
from run_a06_18_label_free_route_relevant_state_selector import (
    PositionTable,
    collect_position_table,
    composition_rows,
    merge_rows,
    pool_indices,
    role_summary,
)


TABLE_NAMES = [
    "state_manifest",
    "leakage_checklist",
    "gradient_profile",
    "center_profile",
    "score_profile",
    "method_candidates",
    "sanity_methods",
    "positive_controls",
    "shortcut_audit",
    "feature_heatmap",
    "feature_mapping",
    "method_aggregate",
]


def read_csv_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def nmi_t(labels: torch.Tensor, preds: torch.Tensor) -> float:
    return normalized_mutual_info([int(v) for v in labels.tolist()], [int(v) for v in preds.tolist()])


def sample_indices(idx: torch.Tensor, cap: int, seed: int) -> torch.Tensor:
    idx = idx.detach().cpu().long()
    if int(idx.numel()) <= int(cap):
        return idx
    gen = torch.Generator().manual_seed(int(seed))
    perm = torch.randperm(int(idx.numel()), generator=gen)[: int(cap)]
    return idx[perm]


def split_indices(n: int, seed: int) -> tuple[torch.Tensor, torch.Tensor]:
    gen = torch.Generator().manual_seed(int(seed))
    perm = torch.randperm(int(n), generator=gen)
    half = int(n) // 2
    return perm[:half], perm[half:]


def collect_functional_signal(
    model: BridgeMoELM,
    batch: BridgeBatch,
    cfg: dict,
    device: torch.device,
) -> dict[str, torch.Tensor]:
    data = cfg["data"]
    batch_size = int(data.get("functional_batch_size", data.get("batch_size", 128)))
    seq_len = int(data["seq_len"])
    loss_parts: list[torch.Tensor] = []
    grad_norm_parts: list[torch.Tensor] = []
    valid_parts: list[torch.Tensor] = []
    model.eval()
    lm_w = model.lm_head.weight.detach()
    with torch.no_grad():
        for start in range(0, int(batch.x.shape[0]), batch_size):
            x = batch.x[start : start + batch_size].to(device)
            logits, _info = model(x)
            pred_logits = logits[:, :-1, :]
            target = x[:, 1:]
            flat_logits = pred_logits.reshape(-1, pred_logits.shape[-1])
            flat_target = target.reshape(-1)
            flat_loss = F.cross_entropy(flat_logits, flat_target, reduction="none")
            probs = F.softmax(flat_logits, dim=-1)
            grad = probs @ lm_w - lm_w[flat_target]
            grad_norm = grad.norm(dim=1)
            bsz = int(x.shape[0])
            full_loss = torch.full((bsz, seq_len), math.nan, device=device)
            full_grad_norm = torch.zeros((bsz, seq_len), device=device)
            full_valid = torch.zeros((bsz, seq_len), dtype=torch.bool, device=device)
            full_loss[:, :-1] = flat_loss.view(bsz, seq_len - 1)
            full_grad_norm[:, :-1] = grad_norm.view(bsz, seq_len - 1)
            full_valid[:, :-1] = True
            loss_parts.append(full_loss.detach().cpu().reshape(-1))
            grad_norm_parts.append(full_grad_norm.detach().cpu().reshape(-1))
            valid_parts.append(full_valid.detach().cpu().reshape(-1))
    return {
        "loss": torch.cat(loss_parts, dim=0),
        "grad_norm": torch.cat(grad_norm_parts, dim=0),
        "valid": torch.cat(valid_parts, dim=0),
    }


def normalized_gap(scores: torch.Tensor) -> torch.Tensor:
    top2 = torch.topk(scores.float(), k=2, dim=1).values
    denom = scores.float().std(dim=1, unbiased=False).clamp_min(1e-8)
    return (top2[:, 0] - top2[:, 1]) / denom


def score_assignments(scores: torch.Tensor, cfg: dict) -> tuple[dict, torch.Tensor]:
    assign = scores.argmax(dim=1).detach().cpu()
    gap = normalized_gap(scores).detach().cpu()
    sorted_gap = torch.sort(gap).values
    p05_idx = max(0, min(int(sorted_gap.numel()) - 1, int(math.floor(0.05 * (int(sorted_gap.numel()) - 1)))))
    row = {
        "score_gap_mean": float(gap.mean().item()),
        "score_gap_p05": float(sorted_gap[p05_idx].item()),
        "score_gap_median": float(sorted_gap[int(sorted_gap.numel()) // 2].item()),
        **{f"score_{k}": v for k, v in load_imbalance(assign, int(cfg["data"]["num_experts"])).items()},
    }
    return row, assign


def assignment_metrics(
    scores: torch.Tensor,
    feature: torch.Tensor,
    nuisance: torch.Tensor,
    slot_start: torch.Tensor,
    cfg: dict,
) -> tuple[dict, torch.Tensor]:
    assign = scores.argmax(dim=1).detach().cpu()
    feature = feature.detach().cpu()
    nuisance = nuisance.detach().cpu()
    slot_start = slot_start.detach().cpu()
    purity, dominant = purity_from_heatmap(feature, assign, int(cfg["data"]["num_features"]))
    return (
        {
            "feature_NMI": nmi_t(feature, assign),
            "nuisance_NMI": nmi_t(nuisance, assign),
            "slot_start_NMI": nmi_t(slot_start, assign),
            "feature_purity": purity,
            "dominant_expert_count": dominant,
            **load_imbalance(assign, int(cfg["data"]["num_experts"])),
            **margin_stats(scores.detach().cpu()),
        },
        assign,
    )


def center_profile(seed: int, method: str, centers: torch.Tensor, cluster_assign: torch.Tensor, k: int) -> list[dict]:
    rows = []
    counts = torch.bincount(cluster_assign.detach().cpu(), minlength=k)
    norms = centers.detach().cpu().float().norm(dim=1)
    for cluster in range(k):
        rows.append(
            {
                "seed": seed,
                "method": method,
                "cluster": cluster,
                "cluster_count": int(counts[cluster].item()),
                "center_norm": float(norms[cluster].item()),
                "empty_cluster": int(counts[cluster].item()) == 0,
            }
        )
    return rows


def centers_from_assignments(h_pool: torch.Tensor, assign: torch.Tensor, fallback_centers: torch.Tensor, k: int) -> torch.Tensor:
    centers = []
    for cluster in range(k):
        mask = assign.detach().cpu() == cluster
        if bool(mask.any()):
            centers.append(h_pool[mask].float().mean(dim=0))
        else:
            centers.append(fallback_centers[cluster].float())
    return torch.stack(centers, dim=0)


def fit_unweighted_centers(
    table: PositionTable,
    idx: torch.Tensor,
    method: str,
    seed: int,
    cfg: dict,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor, list[dict]]:
    k = int(cfg["data"]["num_experts"])
    h_pool = table.hidden[idx].float()
    common = h_pool.mean(dim=0, keepdim=True)
    residual = h_pool - common
    centers_res, assign, _rows = fit_bridge_kmeans(residual, k, seed, cfg, device)
    fallback = centers_res.float() + common.squeeze(0)
    centers = centers_from_assignments(h_pool, assign, fallback, k)
    return centers, assign, center_profile(seed, method, centers, assign, k)


def fit_weighted_kmeans(
    x: torch.Tensor,
    weights: torch.Tensor,
    k: int,
    seed: int,
    cfg: dict,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor]:
    method = cfg["method"]
    n_init = int(method.get("weighted_kmeans_n_init", 3))
    max_iter = int(method.get("weighted_kmeans_max_iter", 50))
    tol = float(method.get("kmeans_tol", 1e-5))
    x_dev = x.float().to(device)
    w_dev = weights.float().to(device).clamp_min(1e-8)
    n, d = x_dev.shape
    if n < k:
        raise ValueError(f"weighted k-means needs n >= k, got n={n}, k={k}")
    generator = torch.Generator(device=device).manual_seed(int(seed) % (2**32 - 1))
    init_idx = torch.randint(0, n, (max(1, n_init), k), generator=generator, device=device)
    centers = x_dev[init_idx].contiguous()
    best_loss = torch.tensor(float("inf"), device=device)
    best_assign = torch.zeros(n, dtype=torch.long, device=device)
    best_centers = centers[0].clone()
    prev_loss = torch.full((max(1, n_init),), float("inf"), device=device)
    x_norm = (x_dev * x_dev).sum(dim=1, keepdim=True)
    for _ in range(max(1, max_iter)):
        flat = centers.reshape(max(1, n_init) * k, d)
        c_norm = (flat * flat).sum(dim=1).view(1, max(1, n_init), k)
        dist = x_norm.view(n, 1, 1) + c_norm - 2.0 * (x_dev @ flat.T).view(n, max(1, n_init), k)
        min_dist, assign = dist.min(dim=2)
        losses = (min_dist * w_dev.view(n, 1)).sum(dim=0) / w_dev.sum().clamp_min(1e-8)
        winner = int(torch.argmin(losses).item())
        if float(losses[winner].item()) < float(best_loss.item()):
            best_loss = losses[winner].detach().clone()
            best_assign = assign[:, winner].detach().clone()
            best_centers = centers[winner].detach().clone()
        new_centers = torch.empty_like(centers)
        for init in range(max(1, n_init)):
            labels = assign[:, init]
            weighted = x_dev * w_dev.view(n, 1)
            sums = torch.zeros(k, d, dtype=x_dev.dtype, device=device)
            sums.index_add_(0, labels, weighted)
            counts = torch.zeros(k, dtype=x_dev.dtype, device=device)
            counts.index_add_(0, labels, w_dev)
            nonempty = counts > 1e-8
            updated = centers[init].clone()
            updated[nonempty] = sums[nonempty] / counts[nonempty].unsqueeze(1)
            if bool((~nonempty).any()):
                empty_ids = torch.nonzero(~nonempty, as_tuple=False).flatten()
                repl = torch.randint(0, n, (int(empty_ids.numel()),), generator=generator, device=device)
                updated[empty_ids] = x_dev[repl]
            new_centers[init] = updated
        max_delta = torch.max(torch.abs(prev_loss - losses))
        centers = new_centers
        if float(max_delta.item()) < tol:
            break
        prev_loss = losses
    return best_centers.detach().cpu(), best_assign.detach().cpu()


def m1_static_bootstrap(
    table: PositionTable,
    fit_idx: torch.Tensor,
    score_idx: torch.Tensor,
    alpha: float,
    seed: int,
    cfg: dict,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor, list[dict], list[dict], list[dict]]:
    method = cfg["method"]
    k = int(cfg["data"]["num_experts"])
    banks = int(method.get("bootstrap_banks", 16))
    cap = int(method.get("bootstrap_sample_cap", 12000))
    candidate_seed_base = seed + int(method.get("candidate_seed_offset", 350003))
    score_h = table.hidden[score_idx].float()
    candidate_centers: list[torch.Tensor] = []
    candidate_assigns: list[torch.Tensor] = []
    candidate_rows: list[dict] = []
    candidate_profiles: list[dict] = []
    for bank in range(banks):
        boot_seed = candidate_seed_base + bank * 997
        sampled = sample_indices(fit_idx, cap, boot_seed)
        centers, assign, profiles = fit_unweighted_centers(table, sampled, f"m1_bank_{bank}", boot_seed, cfg, device)
        scores = router_scores(score_h, centers, alpha)
        score_row, score_assign = score_assignments(scores, cfg)
        candidate_centers.append(centers)
        candidate_assigns.append(score_assign)
        candidate_profiles.extend({**p, "candidate_bank": bank} for p in profiles)
        candidate_rows.append(
            {
                "seed": seed,
                "method": "m1_static_bootstrap_margin",
                "candidate_bank": bank,
                "fit_pool_size": int(sampled.numel()),
                **score_row,
            }
        )
    for i, row in enumerate(candidate_rows):
        nmis = []
        for j, other in enumerate(candidate_assigns):
            if i == j:
                continue
            nmis.append(nmi_t(candidate_assigns[i], other))
        stability = sum(nmis) / max(1, len(nmis))
        row["candidate_consensus_nmi"] = stability
        row["selection_score"] = (
            float(method.get("score_stability_weight", 1.0)) * stability
            + float(method.get("score_gap_p05_weight", 0.05)) * float(row["score_gap_p05"])
            - float(method.get("score_load_penalty", 1.0)) * float(row["score_load_imbalance_L"])
        )
    best_idx = max(range(len(candidate_rows)), key=lambda i: float(candidate_rows[i]["selection_score"]))
    selected_centers = candidate_centers[best_idx]
    selected_assign = candidate_assigns[best_idx]
    selected_rows = [{**r, "selected": int(i == best_idx)} for i, r in enumerate(candidate_rows)]
    selected_profile = [
        {**p, "seed": seed, "method": "m1_static_bootstrap_margin", "selected": int(int(p["candidate_bank"]) == best_idx)}
        for p in candidate_profiles
        if int(p["candidate_bank"]) == best_idx
    ]
    return selected_centers, selected_assign, selected_rows, selected_profile, selected_rows


def gradient_weights(signal: dict[str, torch.Tensor], idx: torch.Tensor, mode: str, cfg: dict) -> torch.Tensor:
    vals = signal["grad_norm"][idx].float()
    valid = signal["valid"][idx]
    vals = vals[valid]
    if int(vals.numel()) == 0:
        return vals
    q = float(cfg["method"].get("gradient_clip_quantile", 0.95))
    clip = torch.quantile(vals, q)
    clipped = vals.clamp_max(float(clip.item())).clamp_min(1e-8)
    if mode == "continuous":
        return clipped / clipped.mean().clamp_min(1e-8)
    if mode == "top20":
        frac = float(cfg["method"].get("gradient_top_fraction", 0.20))
        threshold = torch.quantile(clipped, max(0.0, min(1.0, 1.0 - frac)))
        return torch.where(clipped >= threshold, torch.ones_like(clipped), torch.full_like(clipped, 1e-3))
    raise ValueError(f"unknown M2 weight mode: {mode}")


def m2_gradient_weighted(
    table: PositionTable,
    signal: dict[str, torch.Tensor],
    fit_idx: torch.Tensor,
    score_idx: torch.Tensor,
    alpha: float,
    seed: int,
    mode: str,
    cfg: dict,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor, list[dict], list[dict]]:
    k = int(cfg["data"]["num_experts"])
    valid_fit = fit_idx[signal["valid"][fit_idx]]
    cap = int(cfg["method"].get("fit_sample_cap", 20000))
    sampled = sample_indices(valid_fit, cap, seed + 830003 + len(mode))
    weights = gradient_weights(signal, sampled, mode, cfg)
    h_pool = table.hidden[sampled].float()
    common = h_pool.mean(dim=0, keepdim=True)
    residual = h_pool - common
    centers_res, assign = fit_weighted_kmeans(residual, weights, k, seed + 910009 + len(mode), cfg, device)
    fallback = centers_res.float() + common.squeeze(0)
    centers = centers_from_assignments(h_pool, assign, fallback, k)
    scores = router_scores(table.hidden[score_idx].float(), centers, alpha)
    score_row, score_assign = score_assignments(scores, cfg)
    valid_score = score_idx[signal["valid"][score_idx]]
    if int(valid_score.numel()) > 0:
        score_cluster = score_assign[signal["valid"][score_idx]]
        grad_vals = signal["grad_norm"][valid_score].float()
        overall = float(grad_vals.mean().item())
        enrichments = []
        for cluster in range(k):
            mask = score_cluster == cluster
            if bool(mask.any()):
                enrichments.append(float(grad_vals[mask].mean().item()) / max(overall, 1e-8))
        functional_coherence = max(enrichments) if enrichments else math.nan
    else:
        functional_coherence = math.nan
    row = {
        "seed": seed,
        "method": f"m2_gradient_weighted_{mode}",
        "candidate_bank": 0,
        "fit_pool_size": int(sampled.numel()),
        "candidate_consensus_nmi": math.nan,
        "functional_coherence": functional_coherence,
        **score_row,
    }
    row["selection_score"] = (
        float(cfg["method"].get("score_gap_p05_weight", 0.05)) * float(row["score_gap_p05"])
        - float(cfg["method"].get("score_load_penalty", 1.0)) * float(row["score_load_imbalance_L"])
        + float(cfg["method"].get("score_functional_weight", 0.10)) * float(functional_coherence if not math.isnan(functional_coherence) else 0.0)
    )
    return centers, score_assign, [row], center_profile(seed, f"m2_gradient_weighted_{mode}", centers, assign, k)


def evaluate_centers(
    seed: int,
    method: str,
    centers: torch.Tensor,
    alpha: float,
    eval_route_hidden: torch.Tensor,
    eval_b: BridgeBatch,
    cfg: dict,
) -> tuple[dict, torch.Tensor]:
    scores = router_scores(eval_route_hidden, centers, alpha)
    metrics, assign = assignment_metrics(scores, eval_b.feature_id, eval_b.nuisance_id, eval_b.slot_start, cfg)
    return {"seed": seed, "method": method, **metrics}, assign


def shortcut_rows(seed: int, method: str, score_assign: torch.Tensor, score_idx: torch.Tensor, table: PositionTable, signal: dict[str, torch.Tensor]) -> list[dict]:
    score_assign = score_assign.detach().cpu()
    idx = score_idx.detach().cpu()
    rows = []
    for name, values in [
        ("position", table.position[idx]),
        ("role_id", table.role_id[idx]),
        ("slot_start", table.slot_start[idx]),
    ]:
        rows.append(
            {
                "seed": seed,
                "method": method,
                "guard": name,
                "guard_NMI": nmi_t(values.detach().cpu(), score_assign),
            }
        )
    valid = signal["valid"][idx]
    if bool(valid.any()):
        loss = signal["loss"][idx][valid].float()
        grad = signal["grad_norm"][idx][valid].float()
        assign_valid = score_assign[valid]
        for name, vals in [("loss_bin", loss), ("grad_norm_bin", grad)]:
            quantiles = torch.quantile(vals, torch.tensor([0.25, 0.5, 0.75]))
            bins = torch.bucketize(vals, quantiles)
            rows.append({"seed": seed, "method": method, "guard": name, "guard_NMI": nmi_t(bins, assign_valid)})
    return rows


def run_one(seed: int, cfg: dict, args: argparse.Namespace) -> dict[str, list[dict]]:
    set_seed(seed)
    device = torch.device(args.device)
    data = cfg["data"]
    calib_n = int(data["calibration_samples_per_combo"])
    eval_n = int(data["eval_samples_per_combo"])
    batch_size = int(data["batch_size"])
    k = int(data["num_experts"])
    methods = parse_list(args.methods, ["raw_all_token", "route_only_control", "m1_static_bootstrap_margin", "m2_gradient_weighted_continuous", "m2_gradient_weighted_top20"])

    model = BridgeMoELM(cfg).to(device)
    alpha = float(model.backbone.blocks[-1].moe.router.weight.detach().norm(dim=1).mean().item())
    calib = generate_bridge_batch(cfg, ALL_POSITION_CELL, calib_n, seed + 101)
    eval_b = generate_bridge_batch(cfg, ALL_POSITION_CELL, eval_n, seed + 202)
    table = collect_position_table(model, calib, cfg, device, batch_size)
    signal = collect_functional_signal(model, calib, cfg, device)
    eval_route_hidden = collect_hidden(model, eval_b, device, batch_size, "route")
    fit_idx, score_idx = split_indices(int(table.hidden.shape[0]), seed + int(cfg["method"].get("split_seed_offset", 240001)))
    fit_idx = sample_indices(fit_idx, int(cfg["method"].get("fit_sample_cap", 20000)), seed + 17)
    score_idx = sample_indices(score_idx, int(cfg["method"].get("fit_sample_cap", 20000)), seed + 19)

    rows: dict[str, list[dict]] = defaultdict(list)
    rows["state_manifest"].append(
        {
            "seed": seed,
            "calibration_sequences": int(calib.x.shape[0]),
            "eval_sequences": int(eval_b.x.shape[0]),
            "all_token_states": int(table.hidden.shape[0]),
            "fit_states": int(fit_idx.numel()),
            "score_states": int(score_idx.numel()),
            "route_eval_states": int(eval_route_hidden.shape[0]),
            "d_model": int(table.hidden.shape[1]),
        }
    )
    valid_grad = signal["grad_norm"][signal["valid"]].float()
    rows["gradient_profile"].append(
        {
            "seed": seed,
            "valid_functional_tokens": int(signal["valid"].sum().item()),
            "invalid_functional_tokens": int((~signal["valid"]).sum().item()),
            "loss_mean": float(torch.nanmean(signal["loss"]).item()),
            "grad_norm_mean": float(valid_grad.mean().item()),
            "grad_norm_std": float(valid_grad.std(unbiased=False).item()),
            "grad_norm_p95": float(torch.quantile(valid_grad, 0.95).item()),
            "nonfinite_grad_norm_count": int((~torch.isfinite(valid_grad)).sum().item()),
        }
    )
    rows["leakage_checklist"].extend(
        [
            {"seed": seed, "stage": "method_input", "field": "hidden_state", "allowed": 1, "used": 1},
            {"seed": seed, "stage": "method_input", "field": "loss_or_gradient_norm", "allowed": 1, "used": int(any(m.startswith("m2_") for m in methods))},
            {"seed": seed, "stage": "method_input", "field": "feature_label", "allowed": 0, "used": 0},
            {"seed": seed, "stage": "method_input", "field": "position_label", "allowed": 0, "used": 0},
            {"seed": seed, "stage": "method_input", "field": "route_position_membership", "allowed": 0, "used": 0},
            {"seed": seed, "stage": "final_audit", "field": "feature_label_position_route_metadata", "allowed": 1, "used": 1},
        ]
    )

    for method in methods:
        print(f"[A06_19] seed={seed} method={method} start", flush=True)
        if method == "raw_all_token":
            centers, cluster_assign, profiles = fit_unweighted_centers(table, fit_idx, method, seed + 1009, cfg, device)
            profiles = [{**p, "seed": seed} for p in profiles]
            score_assign = router_scores(table.hidden[score_idx].float(), centers, alpha).argmax(dim=1).detach().cpu()
            rows["center_profile"].extend(profiles)
            candidate_rows = [{"seed": seed, "method": method, "candidate_bank": 0, "fit_pool_size": int(fit_idx.numel()), "selection_score": math.nan}]
        elif method == "route_only_control":
            route_idx = pool_indices(table, "route_only", seed, cfg)
            centers, cluster_assign, profiles = fit_unweighted_centers(table, route_idx, method, seed + 2003, cfg, device)
            profiles = [{**p, "seed": seed} for p in profiles]
            score_assign = router_scores(table.hidden[score_idx].float(), centers, alpha).argmax(dim=1).detach().cpu()
            rows["center_profile"].extend(profiles)
            candidate_rows = [{"seed": seed, "method": method, "candidate_bank": 0, "fit_pool_size": int(route_idx.numel()), "selection_score": math.nan}]
        elif method == "m1_static_bootstrap_margin":
            centers, score_assign, candidate_rows, profiles, _score_rows = m1_static_bootstrap(table, fit_idx, score_idx, alpha, seed, cfg, device)
            rows["center_profile"].extend(profiles)
        elif method.startswith("m2_gradient_weighted_"):
            mode = method.replace("m2_gradient_weighted_", "")
            centers, score_assign, candidate_rows, profiles = m2_gradient_weighted(table, signal, fit_idx, score_idx, alpha, seed, mode, cfg, device)
            rows["center_profile"].extend(profiles)
        else:
            raise ValueError(f"unknown method: {method}")

        rows["method_candidates"].extend(candidate_rows)
        rows["score_profile"].extend(candidate_rows)
        audit_row, eval_assign = evaluate_centers(seed, method, centers, alpha, eval_route_hidden, eval_b, cfg)
        if method == "route_only_control":
            rows["positive_controls"].append(audit_row)
        rows["sanity_methods"].append(
            {
                **audit_row,
                "fit_pool_size": candidate_rows[0].get("fit_pool_size", math.nan),
                "selection_score": candidate_rows[0].get("selection_score", math.nan),
                "uses_feature_labels_for_fit": 0,
                "uses_position_for_fit": 0,
                "uses_route_prior_for_fit": int(method == "route_only_control"),
                **role_summary(table, route_idx if method == "route_only_control" else fit_idx),
            }
        )
        heatmap, mapping = feature_expert_heatmap_rows(seed, ALL_POSITION_CELL, method, eval_b.feature_id, eval_assign, cfg)
        rows["feature_heatmap"].extend([{**r, "method": method} for r in heatmap])
        rows["feature_mapping"].extend([{**r, "method": method} for r in mapping])
        rows["shortcut_audit"].extend(shortcut_rows(seed, method, score_assign, score_idx, table, signal))
        rows["shortcut_audit"].extend(composition_rows(seed, method, score_assign, table.role_id[score_idx], "role"))
        rows["shortcut_audit"].extend(merge_rows(seed, method, mapping, eval_route_hidden, eval_b.feature_id, cfg))
        print(f"[A06_19] seed={seed} method={method} done", flush=True)
    return rows


def write_tables(out_dir: Path, rows: dict[str, list[dict]], suffix: str = "") -> None:
    table_dir = out_dir / "tables"
    for name in TABLE_NAMES:
        if name == "method_aggregate":
            continue
        write_csv(table_dir / f"{name}{suffix}.csv", rows.get(name, []))


def combine_shards(out_dir: Path) -> dict[str, list[dict]]:
    table_dir = out_dir / "tables"
    combined: dict[str, list[dict]] = {}
    for name in TABLE_NAMES:
        if name == "method_aggregate":
            continue
        rows: list[dict] = []
        shard_paths = sorted(table_dir.glob(f"{name}_shard*.csv"))
        if shard_paths:
            for path in shard_paths:
                rows.extend(read_csv_rows(path))
        else:
            rows.extend(read_csv_rows(table_dir / f"{name}.csv"))
        combined[name] = rows
        write_csv(table_dir / f"{name}.csv", rows)
    return combined


def aggregate_outputs(out_dir: Path, fig_dir: Path) -> None:
    rows = combine_shards(out_dir)
    comparison = rows.get("sanity_methods", [])
    agg = aggregate_mean_std(
        comparison,
        ["method"],
        [
            "feature_NMI",
            "nuisance_NMI",
            "slot_start_NMI",
            "feature_purity",
            "dominant_expert_count",
            "load_imbalance_L",
            "max_load",
            "active_experts",
            "margin_mean",
            "margin_p05",
            "fit_pool_role_entropy",
            "fit_pool_route_fraction",
            "fit_pool_slot_nonroute_fraction",
            "fit_pool_target_fraction",
            "fit_pool_neutral_fraction",
        ],
    )
    write_csv(out_dir / "tables" / "method_aggregate.csv", agg)
    write_json(
        out_dir / "run_summary.json",
        {
            "method_count": len({r["method"] for r in comparison}),
            "row_count": len(comparison),
            "aggregate_path": str(out_dir / "tables" / "method_aggregate.csv"),
            "figure_dir": str(fig_dir),
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--seeds", default=None)
    parser.add_argument("--methods", default=None)
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--num-shards", type=int, default=1)
    parser.add_argument("--aggregate-only", action="store_true")
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()

    cfg = load_json(Path(args.config))
    root = workspace_root()
    out_dir = resolve_output(root, cfg["output"]["result_dir"], args.run_name)
    fig_dir = resolve_output(root, cfg["output"]["figure_dir"], args.run_name)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "tables").mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    if not args.aggregate_only:
        write_json(out_dir / "run_config.json", cfg)
    if args.aggregate_only:
        aggregate_outputs(out_dir, fig_dir)
        return

    all_seeds = [int(v) for v in parse_list(args.seeds, [str(v) for v in cfg["seeds"]])]
    seeds = [s for i, s in enumerate(all_seeds) if i % max(1, args.num_shards) == args.shard_index]
    rows: dict[str, list[dict]] = defaultdict(list)
    for seed in seeds:
        seed_rows = run_one(seed, cfg, args)
        for key, vals in seed_rows.items():
            rows[key].extend(vals)
    suffix = f"_shard{args.shard_index}" if args.num_shards > 1 else ""
    write_tables(out_dir, rows, suffix=suffix)
    if args.num_shards == 1:
        aggregate_outputs(out_dir, fig_dir)


if __name__ == "__main__":
    main()

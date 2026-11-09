#!/usr/bin/env python3
"""Run A06_18 label-free route-relevant state selector audit."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

WORKSPACE = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(WORKSPACE / "src"))
sys.path.insert(0, str(SCRIPT_DIR))

import torch
from torch import nn
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
    feature_geometry_rows,
    feature_pca_rows,
    fit_bridge_kmeans,
    generate_bridge_batch,
    router_scores,
)


ROLE_NAMES = {
    0: "route_slot_offset_3",
    1: "slot_offset_0",
    2: "slot_offset_1",
    3: "slot_offset_2",
    4: "nuisance",
    5: "neutral",
    6: "target",
    7: "other",
}

POOL_ORDER = [
    "all_position",
    "route_only",
    "slot_offset_3",
    "selector_stability_top1_position",
    "selector_stability_top3_positions",
    "selector_stability_threshold_positions",
    "pca_q4",
    "pca_q8",
    "pca_q16",
    "pca_q32",
    "bottleneck_ae_q4",
    "bottleneck_ae_q8",
    "bottleneck_ae_q16",
    "bottleneck_ae_q32",
    "sae_l1_4x",
    "sae_topk_4x",
    "sae_l1_8x",
    "sae_topk_8x",
]

POOL_SEED_OFFSETS = {pool: 1009 * (idx + 1) for idx, pool in enumerate(POOL_ORDER)}

TABLE_NAMES = [
    "pool_comparison",
    "selector_search",
    "pool_heatmap",
    "pool_mapping_audit",
    "cluster_role_composition",
    "cluster_position_composition",
    "representation_audit",
    "merge_audit",
    "route_feature_distance",
    "route_feature_pca",
]


@dataclass
class PositionTable:
    hidden: torch.Tensor
    feature_id: torch.Tensor
    nuisance_id: torch.Tensor
    slot_start: torch.Tensor
    position: torch.Tensor
    role_id: torch.Tensor


class BottleneckAE(nn.Module):
    def __init__(self, d_model: int, latent_dim: int):
        super().__init__()
        self.encoder = nn.Linear(d_model, latent_dim)
        self.decoder = nn.Linear(latent_dim, d_model)

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        return self.encoder(x)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        z = self.encode(x)
        return self.decoder(z), z


class SparseAutoencoder(nn.Module):
    def __init__(self, d_model: int, d_sae: int, sparsity: str, top_k: int):
        super().__init__()
        self.encoder = nn.Linear(d_model, d_sae)
        self.decoder = nn.Linear(d_sae, d_model)
        self.sparsity = sparsity
        self.top_k = top_k

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        z = F.relu(self.encoder(x))
        if self.sparsity == "topk":
            k = min(int(self.top_k), z.shape[1])
            vals, idx = torch.topk(z, k, dim=1)
            sparse = torch.zeros_like(z)
            sparse.scatter_(1, idx, vals)
            return sparse
        return z

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        z = self.encode(x)
        return self.decoder(z), z


def read_csv_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def nmi_t(labels: torch.Tensor, preds: torch.Tensor) -> float:
    return normalized_mutual_info([int(v) for v in labels.tolist()], [int(v) for v in preds.tolist()])


def pool_seed_offset(pool: str) -> int:
    if pool in POOL_SEED_OFFSETS:
        return POOL_SEED_OFFSETS[pool]
    return 1000003 + sum((i + 1) * ord(ch) for i, ch in enumerate(pool))


def configured_pool_order(cfg: dict, pools: list[str]) -> list[str]:
    known = [p for p in POOL_ORDER if p in pools]
    extras = [p for p in pools if p not in known]
    return known + extras


def representation_specs(cfg: dict) -> dict[str, dict]:
    return {str(spec["name"]): dict(spec) for spec in cfg.get("representation_pools", [])}


def role_summary(table: PositionTable, idx: torch.Tensor) -> dict:
    if int(idx.numel()) == 0:
        return {
            "fit_pool_role_entropy": math.nan,
            "fit_pool_route_fraction": math.nan,
            "fit_pool_slot_nonroute_fraction": math.nan,
            "fit_pool_target_fraction": math.nan,
            "fit_pool_neutral_fraction": math.nan,
        }
    role_counts = torch.bincount(table.role_id[idx], minlength=len(ROLE_NAMES)).float()
    role_prob = role_counts / role_counts.sum().clamp_min(1)
    entropy = float((-(role_prob[role_prob > 0] * torch.log2(role_prob[role_prob > 0]))).sum().item())
    total = max(1.0, float(role_counts.sum().item()))
    return {
        "fit_pool_role_entropy": entropy,
        "fit_pool_route_fraction": float(role_counts[0].item() / total),
        "fit_pool_slot_nonroute_fraction": float(role_counts[1:4].sum().item() / total),
        "fit_pool_target_fraction": float(role_counts[6].item() / total),
        "fit_pool_neutral_fraction": float(role_counts[5].item() / total),
    }


def position_roles(x: torch.Tensor, batch: BridgeBatch, cfg: dict, local_start: int) -> tuple[torch.Tensor, torch.Tensor]:
    data = cfg["data"]
    bsz, seq_len = x.shape
    pos = torch.arange(seq_len, dtype=torch.long).view(1, seq_len).expand(bsz, seq_len)
    slot_start = batch.slot_start[local_start : local_start + bsz].view(-1, 1)
    route_pos = batch.route_pos[local_start : local_start + bsz].view(-1, 1)
    target_pos = route_pos + 1
    offset = pos - slot_start
    role = torch.full((bsz, seq_len), 7, dtype=torch.long)

    nuisance_start = int(data["nuisance_token_start"])
    nuisance_end = nuisance_start + int(data["num_nuisance"])
    neutral_start = int(data["neutral_token_start"])
    neutral_end = neutral_start + int(data["neutral_token_count"])
    x_cpu = x.detach().cpu()

    role[(x_cpu >= neutral_start) & (x_cpu < neutral_end)] = 5
    role[(x_cpu >= nuisance_start) & (x_cpu < nuisance_end)] = 4
    role[pos == target_pos] = 6
    role[(offset == 0)] = 1
    role[(offset == 1)] = 2
    role[(offset == 2)] = 3
    role[pos == route_pos] = 0
    return pos, role


def collect_position_table(model: BridgeMoELM, batch: BridgeBatch, cfg: dict, device: torch.device, batch_size: int) -> PositionTable:
    hidden_parts: list[torch.Tensor] = []
    feature_parts: list[torch.Tensor] = []
    nuisance_parts: list[torch.Tensor] = []
    slot_parts: list[torch.Tensor] = []
    pos_parts: list[torch.Tensor] = []
    role_parts: list[torch.Tensor] = []
    model.eval()
    with torch.no_grad():
        for start in range(0, batch.x.shape[0], batch_size):
            x = batch.x[start : start + batch_size].to(device)
            _, info = model(x)
            h = info["post_ln"].detach().cpu()
            bsz, seq_len, dim = h.shape
            pos, role = position_roles(batch.x[start : start + bsz], batch, cfg, start)
            hidden_parts.append(h.reshape(bsz * seq_len, dim))
            feature_parts.append(batch.feature_id[start : start + bsz].repeat_interleave(seq_len))
            nuisance_parts.append(batch.nuisance_id[start : start + bsz].repeat_interleave(seq_len))
            slot_parts.append(batch.slot_start[start : start + bsz].repeat_interleave(seq_len))
            pos_parts.append(pos.reshape(-1))
            role_parts.append(role.reshape(-1))
    return PositionTable(
        hidden=torch.cat(hidden_parts, dim=0),
        feature_id=torch.cat(feature_parts, dim=0),
        nuisance_id=torch.cat(nuisance_parts, dim=0),
        slot_start=torch.cat(slot_parts, dim=0),
        position=torch.cat(pos_parts, dim=0),
        role_id=torch.cat(role_parts, dim=0),
    )


def balanced_role_indices(table: PositionTable, seed: int, cfg: dict) -> torch.Tensor:
    groups = {
        "route": torch.nonzero(table.role_id == 0, as_tuple=False).flatten(),
        "slot_nonroute": torch.nonzero((table.role_id == 1) | (table.role_id == 2) | (table.role_id == 3), as_tuple=False).flatten(),
        "nuisance": torch.nonzero(table.role_id == 4, as_tuple=False).flatten(),
        "neutral": torch.nonzero(table.role_id == 5, as_tuple=False).flatten(),
    }
    take = min(int(v.numel()) for v in groups.values())
    gen = torch.Generator().manual_seed(seed + int(cfg["method"].get("role_balance_seed_offset", 73001)))
    picked = []
    for idx in groups.values():
        perm = torch.randperm(int(idx.numel()), generator=gen)[:take]
        picked.append(idx[perm])
    return torch.cat(picked, dim=0)


def pool_indices(table: PositionTable, pool: str, seed: int, cfg: dict) -> torch.Tensor:
    if pool == "all_position":
        return torch.arange(table.hidden.shape[0])
    if pool == "route_only" or pool == "slot_offset_3":
        return torch.nonzero(table.role_id == 0, as_tuple=False).flatten()
    if pool == "slot_mixed":
        return torch.nonzero((table.role_id >= 0) & (table.role_id <= 3), as_tuple=False).flatten()
    if pool == "slot_offset_0":
        return torch.nonzero(table.role_id == 1, as_tuple=False).flatten()
    if pool == "slot_offset_1":
        return torch.nonzero(table.role_id == 2, as_tuple=False).flatten()
    if pool == "slot_offset_2":
        return torch.nonzero(table.role_id == 3, as_tuple=False).flatten()
    if pool == "role_balanced_all":
        return balanced_role_indices(table, seed, cfg)
    if pool == "non_slot_no_target":
        return torch.nonzero((table.role_id == 4) | (table.role_id == 5) | (table.role_id == 7), as_tuple=False).flatten()
    raise ValueError(f"unknown pool: {pool}")


def assign_by_euclidean(states: torch.Tensor, centers: torch.Tensor) -> torch.Tensor:
    x = states.float()
    c = centers.float()
    dist = (x * x).sum(dim=1, keepdim=True) + (c * c).sum(dim=1).view(1, -1) - 2.0 * (x @ c.T)
    return dist.argmin(dim=1).detach().cpu()


def selector_kmeans(
    residual: torch.Tensor,
    seed: int,
    cfg: dict,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor, list[dict]]:
    selector_cfg = dict(cfg)
    selector_cfg["method"] = dict(cfg["method"])
    selector_cfg["method"]["kmeans_n_init"] = int(cfg["method"].get("selector_kmeans_n_init", 5))
    selector_cfg["method"]["kmeans_max_iter"] = int(cfg["method"].get("selector_kmeans_max_iter", 50))
    return fit_bridge_kmeans(
        residual,
        int(cfg["data"]["num_experts"]),
        seed,
        selector_cfg,
        device,
    )


def representation_kmeans_cfg(cfg: dict) -> dict:
    rep_cfg = dict(cfg)
    rep_cfg["method"] = dict(cfg["method"])
    rep_cfg["method"]["kmeans_n_init"] = int(cfg["method"].get("representation_kmeans_n_init", cfg["method"]["kmeans_n_init"]))
    rep_cfg["method"]["kmeans_max_iter"] = int(cfg["method"].get("representation_kmeans_max_iter", cfg["method"].get("kmeans_max_iter", 80)))
    return rep_cfg


def selector_position_scores(table: PositionTable, seed: int, cfg: dict, device: torch.device) -> list[dict]:
    selector = cfg.get("selector", {})
    min_count = int(selector.get("min_position_count", int(cfg["data"]["num_experts"]) * 8))
    rows: list[dict] = []
    for pos in sorted({int(v) for v in table.position.tolist()}):
        idx = torch.nonzero(table.position == pos, as_tuple=False).flatten()
        if int(idx.numel()) < min_count:
            continue
        h = table.hidden[idx].float()
        gen = torch.Generator().manual_seed(seed + int(selector.get("split_seed_offset", 91031)) + pos)
        perm = torch.randperm(int(h.shape[0]), generator=gen)
        half = int(h.shape[0]) // 2
        idx_a = perm[:half]
        idx_b = perm[half:]
        if int(idx_a.numel()) < int(cfg["data"]["num_experts"]) or int(idx_b.numel()) < int(cfg["data"]["num_experts"]):
            continue
        common_a = h[idx_a].mean(dim=0, keepdim=True)
        common_b = h[idx_b].mean(dim=0, keepdim=True)
        centers_a, _assign_a, _rows_a = selector_kmeans(h[idx_a] - common_a, seed + 17 * pos + 1, cfg, device)
        centers_b, _assign_b, _rows_b = selector_kmeans(h[idx_b] - common_b, seed + 17 * pos + 2, cfg, device)
        assign_a = assign_by_euclidean(h - common_a, centers_a)
        assign_b = assign_by_euclidean(h - common_b, centers_b)
        stability = nmi_t(assign_a, assign_b)
        role_counts = torch.bincount(table.role_id[idx], minlength=len(ROLE_NAMES)).float()
        role_total = float(role_counts.sum().item())
        rows.append(
            {
                "seed": seed,
                "selector_family": "position_split_stability",
                "candidate_position": pos,
                "split_assignment_nmi": stability,
                "candidate_count": int(idx.numel()),
                "route_role_fraction": float(role_counts[0].item() / max(1.0, role_total)),
                "slot_nonroute_fraction": float(role_counts[1:4].sum().item() / max(1.0, role_total)),
                "target_fraction": float(role_counts[6].item() / max(1.0, role_total)),
                "neutral_fraction": float(role_counts[5].item() / max(1.0, role_total)),
            }
        )
    rows.sort(key=lambda r: (-float(r["split_assignment_nmi"]), int(r["candidate_position"])))
    for rank, row in enumerate(rows, start=1):
        row["selector_rank"] = rank
    return rows


def selector_positions(pool: str, search_rows: list[dict], cfg: dict) -> list[int]:
    if not search_rows:
        return []
    if pool == "selector_stability_top1_position":
        return [int(search_rows[0]["candidate_position"])]
    if pool == "selector_stability_top3_positions":
        return [int(r["candidate_position"]) for r in search_rows[:3]]
    if pool == "selector_stability_threshold_positions":
        selector = cfg.get("selector", {})
        threshold = float(selector.get("stability_delta_from_best", 0.05))
        max_positions = int(selector.get("max_threshold_positions", 6))
        best = float(search_rows[0]["split_assignment_nmi"])
        chosen = [int(r["candidate_position"]) for r in search_rows if float(r["split_assignment_nmi"]) >= best - threshold]
        return chosen[:max_positions]
    raise ValueError(f"not a selector pool: {pool}")


def selector_pool_indices(
    table: PositionTable,
    pool: str,
    seed: int,
    cfg: dict,
    device: torch.device,
) -> tuple[torch.Tensor, list[dict], list[int]]:
    search_rows = selector_position_scores(table, seed, cfg, device)
    positions = selector_positions(pool, search_rows, cfg)
    if positions:
        mask = torch.zeros_like(table.position, dtype=torch.bool)
        for pos in positions:
            mask |= table.position == pos
        idx = torch.nonzero(mask, as_tuple=False).flatten()
    else:
        idx = torch.empty(0, dtype=torch.long)
    annotated_rows = []
    selected_set = set(positions)
    for row in search_rows:
        annotated_rows.append(
            {
                **row,
                "pool": pool,
                "selected_by_pool": int(int(row["candidate_position"]) in selected_set),
                "selected_positions": " ".join(str(v) for v in positions),
            }
        )
    return idx, annotated_rows, positions


def train_sample(x: torch.Tensor, seed: int, cfg: dict, args: argparse.Namespace) -> torch.Tensor:
    rep_cfg = cfg.get("representation", {})
    cap_key = "smoke_train_sample_cap" if args.run_stage == "smoke" else "train_sample_cap"
    cap = int(rep_cfg.get(cap_key, x.shape[0]))
    n = min(int(x.shape[0]), cap)
    gen = torch.Generator().manual_seed(seed + int(rep_cfg.get("train_sample_seed_offset", 130211)))
    idx = torch.randperm(int(x.shape[0]), generator=gen)[:n]
    return x[idx].float()


def fit_pca_latent(x: torch.Tensor, spec: dict, cfg: dict, device: torch.device) -> tuple[torch.Tensor, dict]:
    q = int(spec["latent_dim"])
    x_dev = x.float().to(device)
    mean = x_dev.mean(dim=0, keepdim=True)
    centered = x_dev - mean
    cov = centered.T @ centered / max(1, int(centered.shape[0]) - 1)
    eigvals, eigvecs = torch.linalg.eigh(cov)
    order = torch.argsort(eigvals, descending=True)
    comps = eigvecs[:, order[:q]]
    latent = centered @ comps
    recon = latent @ comps.T
    reconstruction_mse = float(F.mse_loss(recon, centered).detach().cpu().item())
    retained_variance = float(eigvals[order[:q]].sum().detach().cpu().item())
    total_variance = float(eigvals.clamp_min(0).sum().detach().cpu().item())
    audit = {
        "representation_type": "pca",
        "latent_dim": q,
        "d_sae": math.nan,
        "sae_expansion": math.nan,
        "sparsity": "",
        "top_k": math.nan,
        "l1_lambda": math.nan,
        "train_sample_count": int(x.shape[0]),
        "train_epochs": 0,
        "train_reconstruction_mse": reconstruction_mse,
        "reconstruction_mse": reconstruction_mse,
        "retained_variance_fraction": retained_variance / max(total_variance, 1e-12),
        "latent_l0_mean": float(q),
        "latent_active_fraction": 1.0,
    }
    return latent.detach().cpu().float(), audit


def fit_autoencoder_model(
    model: nn.Module,
    x: torch.Tensor,
    mean: torch.Tensor,
    seed: int,
    spec: dict,
    cfg: dict,
    args: argparse.Namespace,
    device: torch.device,
) -> tuple[nn.Module, float, int]:
    rep_cfg = cfg.get("representation", {})
    stage_prefix = "smoke_" if args.run_stage == "smoke" else ""
    if isinstance(model, SparseAutoencoder):
        epochs = int(rep_cfg.get(f"{stage_prefix}sae_epochs", rep_cfg.get("sae_epochs", 8)))
        lr = float(rep_cfg.get("sae_lr", 1e-3))
        weight_decay = float(rep_cfg.get("sae_weight_decay", 0.0))
    else:
        epochs = int(rep_cfg.get(f"{stage_prefix}ae_epochs", rep_cfg.get("ae_epochs", 8)))
        lr = float(rep_cfg.get("ae_lr", 1e-3))
        weight_decay = float(rep_cfg.get("ae_weight_decay", 1e-5))
    batch_size = int(rep_cfg.get("train_batch_size", 4096))
    train_x = train_sample(x, seed, cfg, args)
    train_x = train_x - mean.cpu()
    model = model.to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    l1_lambda = float(spec.get("l1_lambda", 0.0))
    last_mse = math.nan
    for epoch in range(epochs):
        gen = torch.Generator().manual_seed(seed + 170003 + epoch)
        perm = torch.randperm(int(train_x.shape[0]), generator=gen)
        epoch_sse = 0.0
        epoch_count = 0
        for start in range(0, int(train_x.shape[0]), batch_size):
            idx = perm[start : start + batch_size]
            xb = train_x[idx].to(device)
            recon, z = model(xb)
            mse = F.mse_loss(recon, xb)
            loss = mse
            if isinstance(model, SparseAutoencoder) and model.sparsity == "l1":
                loss = loss + l1_lambda * z.abs().mean()
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
            epoch_sse += float(F.mse_loss(recon.detach(), xb, reduction="sum").cpu().item())
            epoch_count += int(xb.numel())
        last_mse = epoch_sse / max(1, epoch_count)
    return model.eval(), last_mse, int(train_x.shape[0])


def encode_autoencoder(
    model: nn.Module,
    x: torch.Tensor,
    mean: torch.Tensor,
    cfg: dict,
    device: torch.device,
) -> tuple[torch.Tensor, dict]:
    rep_cfg = cfg.get("representation", {})
    batch_size = int(rep_cfg.get("encode_batch_size", rep_cfg.get("train_batch_size", 4096)))
    latents = []
    total_sse = 0.0
    total_count = 0
    active_total = 0.0
    code_total = 0.0
    model.eval()
    with torch.no_grad():
        for start in range(0, int(x.shape[0]), batch_size):
            xb_raw = x[start : start + batch_size].float()
            xb = (xb_raw - mean.cpu()).to(device)
            recon, z = model(xb)
            total_sse += float(F.mse_loss(recon, xb, reduction="sum").cpu().item())
            total_count += int(xb.numel())
            active_total += float((z.detach() > 1e-8).sum(dim=1).float().sum().cpu().item())
            code_total += float(z.shape[0] * z.shape[1])
            latents.append(z.detach().cpu().float())
    n = max(1, int(x.shape[0]))
    return torch.cat(latents, dim=0), {
        "reconstruction_mse": total_sse / max(1, total_count),
        "latent_l0_mean": active_total / n,
        "latent_active_fraction": active_total / max(1.0, code_total),
    }


def fit_ae_latent(
    x: torch.Tensor,
    spec: dict,
    seed: int,
    cfg: dict,
    args: argparse.Namespace,
    device: torch.device,
) -> tuple[torch.Tensor, dict]:
    d_model = int(x.shape[1])
    latent_dim = int(spec["latent_dim"])
    mean = x.float().mean(dim=0, keepdim=True)
    model = BottleneckAE(d_model, latent_dim)
    model, train_mse, train_count = fit_autoencoder_model(model, x, mean, seed, spec, cfg, args, device)
    latent, eval_audit = encode_autoencoder(model, x, mean, cfg, device)
    audit = {
        "representation_type": "bottleneck_ae",
        "latent_dim": latent_dim,
        "d_sae": math.nan,
        "sae_expansion": math.nan,
        "sparsity": "",
        "top_k": math.nan,
        "l1_lambda": math.nan,
        "train_sample_count": train_count,
        "train_epochs": int(cfg.get("representation", {}).get("smoke_ae_epochs" if args.run_stage == "smoke" else "ae_epochs", 8)),
        "train_reconstruction_mse": train_mse,
        "retained_variance_fraction": math.nan,
        **eval_audit,
    }
    return latent, audit


def fit_sae_latent(
    x: torch.Tensor,
    spec: dict,
    seed: int,
    cfg: dict,
    args: argparse.Namespace,
    device: torch.device,
) -> tuple[torch.Tensor, dict]:
    d_model = int(x.shape[1])
    expansion = int(spec["expansion"])
    d_sae = expansion * d_model
    sparsity = str(spec["sparsity"])
    top_k = int(spec.get("top_k", cfg.get("representation", {}).get("sae_top_k", 8)))
    mean = x.float().mean(dim=0, keepdim=True)
    model = SparseAutoencoder(d_model, d_sae, sparsity, top_k)
    model, train_mse, train_count = fit_autoencoder_model(model, x, mean, seed, spec, cfg, args, device)
    latent, eval_audit = encode_autoencoder(model, x, mean, cfg, device)
    audit = {
        "representation_type": "sae",
        "latent_dim": d_sae,
        "d_sae": d_sae,
        "sae_expansion": expansion,
        "sparsity": sparsity,
        "top_k": top_k if sparsity == "topk" else math.nan,
        "l1_lambda": float(spec.get("l1_lambda", 0.0)) if sparsity == "l1" else math.nan,
        "train_sample_count": train_count,
        "train_epochs": int(cfg.get("representation", {}).get("smoke_sae_epochs" if args.run_stage == "smoke" else "sae_epochs", 8)),
        "train_reconstruction_mse": train_mse,
        "retained_variance_fraction": math.nan,
        **eval_audit,
    }
    return latent, audit


def fit_representation_latent(
    x: torch.Tensor,
    pool: str,
    spec: dict,
    seed: int,
    cfg: dict,
    args: argparse.Namespace,
    device: torch.device,
) -> tuple[torch.Tensor, dict]:
    kind = str(spec["type"])
    if kind == "pca":
        return fit_pca_latent(x, spec, cfg, device)
    if kind == "bottleneck_ae":
        return fit_ae_latent(x, spec, seed + pool_seed_offset(pool), cfg, args, device)
    if kind == "sae":
        return fit_sae_latent(x, spec, seed + pool_seed_offset(pool), cfg, args, device)
    raise ValueError(f"unknown representation type for {pool}: {kind}")


def assignment_metrics(scores: torch.Tensor, feature: torch.Tensor, nuisance: torch.Tensor, slot_start: torch.Tensor, cfg: dict) -> tuple[dict, torch.Tensor]:
    assign = scores.argmax(dim=1).detach().cpu()
    feature = feature.detach().cpu()
    nuisance = nuisance.detach().cpu()
    slot_start = slot_start.detach().cpu()
    purity, dominant = purity_from_heatmap(feature, assign, int(cfg["data"]["num_features"]))
    row = {
        "feature_NMI": nmi_t(feature, assign),
        "nuisance_NMI": nmi_t(nuisance, assign),
        "slot_start_NMI": nmi_t(slot_start, assign),
        "feature_purity": purity,
        "dominant_expert_count": dominant,
        **load_imbalance(assign, int(cfg["data"]["num_experts"])),
        **margin_stats(scores.detach().cpu()),
    }
    return row, assign


def composition_rows(seed: int, pool: str, assignments: torch.Tensor, values: torch.Tensor, value_name: str) -> list[dict]:
    rows = []
    assignments = assignments.detach().cpu()
    values = values.detach().cpu()
    for cluster in sorted({int(v) for v in assignments.tolist()}):
        mask = assignments == cluster
        total = int(mask.sum().item())
        for value in sorted({int(v) for v in values[mask].tolist()}):
            count = int(((values == value) & mask).sum().item())
            label = ROLE_NAMES.get(value, str(value)) if value_name == "role" else value
            rows.append(
                {
                    "seed": seed,
                    "pool": pool,
                    "cluster": cluster,
                    value_name: label,
                    "count": count,
                    "fraction": count / max(1, total),
                    "cluster_total": total,
                }
            )
    return rows


def dominant_mapping(mapping_rows: list[dict]) -> dict[int, int]:
    return {int(row["feature_id"]): int(row["dominant_expert"]) for row in mapping_rows}


def merge_rows(seed: int, pool: str, mapping_rows: list[dict], route_states: torch.Tensor, feature: torch.Tensor, cfg: dict) -> list[dict]:
    mapping = dominant_mapping(mapping_rows)
    num_features = int(cfg["data"]["num_features"])
    states = route_states.detach().cpu().float()
    feature = feature.detach().cpu()
    centered = states - states.mean(dim=0, keepdim=True)
    centroids = []
    for f in range(num_features):
        centroids.append(centered[feature == f].mean(dim=0))
    centroids_t = torch.stack(centroids, dim=0)
    cos = F.normalize(centroids_t, p=2, dim=1) @ F.normalize(centroids_t, p=2, dim=1).T
    pair_vals = []
    for i in range(num_features):
        for j in range(i + 1, num_features):
            pair_vals.append((i, j, float((centroids_t[i] - centroids_t[j]).norm().item()), float(cos[i, j].item())))
    euclid_rank = {(i, j): rank + 1 for rank, (i, j, _d, _c) in enumerate(sorted(pair_vals, key=lambda x: x[2]))}
    cosine_rank = {(i, j): rank + 1 for rank, (i, j, _d, _c) in enumerate(sorted(pair_vals, key=lambda x: -x[3]))}
    out = []
    for i, j, dist, cosine in pair_vals:
        out.append(
            {
                "seed": seed,
                "pool": pool,
                "feature_i": i,
                "feature_j": j,
                "expert_i": mapping.get(i, -1),
                "expert_j": mapping.get(j, -1),
                "merged_same_expert": mapping.get(i, -2) == mapping.get(j, -3),
                "route_centroid_euclidean": dist,
                "route_centroid_cosine": cosine,
                "euclidean_closeness_rank": euclid_rank[(i, j)],
                "cosine_closeness_rank": cosine_rank[(i, j)],
            }
        )
    return out


def fit_eval_representation_pool(
    model: BridgeMoELM,
    cfg: dict,
    args: argparse.Namespace,
    seed: int,
    pool: str,
    spec: dict,
    table: PositionTable,
    eval_route_hidden: torch.Tensor,
    eval_b: BridgeBatch,
    device: torch.device,
) -> dict[str, list[dict]]:
    rows: dict[str, list[dict]] = defaultdict(list)
    alpha = float(model.backbone.blocks[-1].moe.router.weight.detach().norm(dim=1).mean().item())
    idx = pool_indices(table, str(spec.get("fit_pool", "all_position")), seed, cfg)
    h_pool = table.hidden[idx].float()
    latent, audit = fit_representation_latent(h_pool, pool, spec, seed, cfg, args, device)
    latent_common = latent.mean(dim=0, keepdim=True)
    latent_res = latent - latent_common
    centers_latent, cluster_assign, _cluster_rows = fit_bridge_kmeans(
        latent_res,
        int(cfg["data"]["num_experts"]),
        seed + pool_seed_offset(pool),
        representation_kmeans_cfg(cfg),
        device,
    )
    raw_centers = []
    for cluster in range(int(cfg["data"]["num_experts"])):
        mask = cluster_assign == cluster
        if bool(mask.any()):
            raw_centers.append(h_pool[mask].mean(dim=0))
        else:
            raw_centers.append(h_pool.mean(dim=0))
    centers = torch.stack(raw_centers, dim=0)
    scores = router_scores(eval_route_hidden, centers, alpha)
    metrics, assign = assignment_metrics(scores, eval_b.feature_id, eval_b.nuisance_id, eval_b.slot_start, cfg)
    comparison = {
        "seed": seed,
        "pool": pool,
        "fit_pool_size": int(idx.numel()),
        "uses_feature_labels_for_fit": False,
        "selected_positions": "",
        **role_summary(table, idx),
        **audit,
        **metrics,
    }
    rows["pool_comparison"].append(comparison)
    rows["representation_audit"].append({**comparison, "feature_NMI": metrics["feature_NMI"]})
    rows["cluster_role_composition"].extend(composition_rows(seed, pool, cluster_assign, table.role_id[idx], "role"))
    rows["cluster_position_composition"].extend(composition_rows(seed, pool, cluster_assign, table.position[idx], "position"))
    heatmap, mapping = feature_expert_heatmap_rows(seed, ALL_POSITION_CELL, pool, eval_b.feature_id, assign, cfg)
    rows["pool_heatmap"].extend([{**r, "pool": pool} for r in heatmap])
    rows["pool_mapping_audit"].extend([{**r, "pool": pool} for r in mapping])
    rows["merge_audit"].extend(merge_rows(seed, pool, mapping, eval_route_hidden, eval_b.feature_id, cfg))
    return rows


def fit_eval_pool(
    model: BridgeMoELM,
    cfg: dict,
    args: argparse.Namespace,
    seed: int,
    pool: str,
    table: PositionTable,
    eval_route_hidden: torch.Tensor,
    eval_b: BridgeBatch,
    device: torch.device,
) -> dict[str, list[dict]]:
    rows: dict[str, list[dict]] = defaultdict(list)
    alpha = float(model.backbone.blocks[-1].moe.router.weight.detach().norm(dim=1).mean().item())
    rep_spec = representation_specs(cfg).get(pool)
    if rep_spec is not None:
        return fit_eval_representation_pool(model, cfg, args, seed, pool, rep_spec, table, eval_route_hidden, eval_b, device)
    if pool == "oracle_route_upper_bound":
        route_idx = pool_indices(table, "route_only", seed, cfg)
        centers = feature_centroids(table.hidden[route_idx].float(), table.feature_id[route_idx], int(cfg["data"]["num_features"]))
        scores = router_scores(eval_route_hidden, centers, alpha)
        metrics, assign = assignment_metrics(scores, eval_b.feature_id, eval_b.nuisance_id, eval_b.slot_start, cfg)
        comparison = {
            "seed": seed,
            "pool": pool,
            "fit_pool_size": int(route_idx.numel()),
            "uses_feature_labels_for_fit": True,
            **role_summary(table, route_idx),
            **metrics,
        }
        rows["pool_comparison"].append(comparison)
        heatmap, mapping = feature_expert_heatmap_rows(seed, ALL_POSITION_CELL, pool, eval_b.feature_id, assign, cfg)
        rows["pool_heatmap"].extend([{**r, "pool": pool} for r in heatmap])
        rows["pool_mapping_audit"].extend([{**r, "pool": pool} for r in mapping])
        rows["merge_audit"].extend(merge_rows(seed, pool, mapping, eval_route_hidden, eval_b.feature_id, cfg))
        return rows

    selected_positions = ""
    if pool.startswith("selector_stability_"):
        idx, search_rows, positions = selector_pool_indices(table, pool, seed, cfg, device)
        rows["selector_search"].extend(search_rows)
        selected_positions = " ".join(str(v) for v in positions)
    else:
        idx = pool_indices(table, pool, seed, cfg)
    if int(idx.numel()) == 0:
        rows["pool_comparison"].append(
            {
                "seed": seed,
                "pool": pool,
                "fit_pool_size": 0,
                "uses_feature_labels_for_fit": False,
                "selected_positions": selected_positions,
                **role_summary(table, idx),
                "feature_NMI": math.nan,
                "nuisance_NMI": math.nan,
                "slot_start_NMI": math.nan,
                "feature_purity": math.nan,
                "dominant_expert_count": 0,
                **load_imbalance(torch.empty(0, dtype=torch.long), int(cfg["data"]["num_experts"])),
                **margin_stats(torch.empty(0, 2)),
            }
        )
        return rows
    h_pool = table.hidden[idx].float()
    common = h_pool.mean(dim=0, keepdim=True)
    residual = h_pool - common
    centers_res, cluster_assign, _cluster_rows = fit_bridge_kmeans(
        residual,
        int(cfg["data"]["num_experts"]),
        seed + POOL_SEED_OFFSETS.get(pool, 99991),
        cfg,
        device,
    )
    raw_centers = []
    for cluster in range(int(cfg["data"]["num_experts"])):
        mask = cluster_assign == cluster
        if bool(mask.any()):
            raw_centers.append(h_pool[mask].mean(dim=0))
        else:
            raw_centers.append(centers_res[cluster].float() + common.squeeze(0))
    centers = torch.stack(raw_centers, dim=0)
    scores = router_scores(eval_route_hidden, centers, alpha)
    metrics, assign = assignment_metrics(scores, eval_b.feature_id, eval_b.nuisance_id, eval_b.slot_start, cfg)
    rows["pool_comparison"].append(
        {
            "seed": seed,
            "pool": pool,
            "fit_pool_size": int(idx.numel()),
            "uses_feature_labels_for_fit": False,
            "selected_positions": selected_positions,
            **role_summary(table, idx),
            **metrics,
        }
    )
    rows["cluster_role_composition"].extend(composition_rows(seed, pool, cluster_assign, table.role_id[idx], "role"))
    rows["cluster_position_composition"].extend(composition_rows(seed, pool, cluster_assign, table.position[idx], "position"))
    heatmap, mapping = feature_expert_heatmap_rows(seed, ALL_POSITION_CELL, pool, eval_b.feature_id, assign, cfg)
    rows["pool_heatmap"].extend([{**r, "pool": pool} for r in heatmap])
    rows["pool_mapping_audit"].extend([{**r, "pool": pool} for r in mapping])
    rows["merge_audit"].extend(merge_rows(seed, pool, mapping, eval_route_hidden, eval_b.feature_id, cfg))
    return rows


def run_one(seed: int, cfg: dict, args: argparse.Namespace) -> dict[str, list[dict]]:
    set_seed(seed)
    device = torch.device(args.device)
    data = cfg["data"]
    calib_n = int(data["smoke_calibration_samples_per_combo"] if args.run_stage == "smoke" else data["calibration_samples_per_combo"])
    eval_n = int(data["smoke_eval_samples_per_combo"] if args.run_stage == "smoke" else data["eval_samples_per_combo"])
    batch_size = int(data["batch_size"])
    pools = parse_list(args.pools, [str(v) for v in cfg["pools"]])

    model = BridgeMoELM(cfg).to(device)
    calib = generate_bridge_batch(cfg, ALL_POSITION_CELL, calib_n, seed + 101)
    eval_b = generate_bridge_batch(cfg, ALL_POSITION_CELL, eval_n, seed + 202)
    table = collect_position_table(model, calib, cfg, device, batch_size)
    eval_route_hidden = collect_hidden(model, eval_b, device, batch_size, "route")
    rows: dict[str, list[dict]] = defaultdict(list)
    centered_eval = eval_route_hidden.float() - eval_route_hidden.float().mean(dim=0, keepdim=True)
    rows["route_feature_distance"].extend(
        feature_geometry_rows(seed, ALL_POSITION_CELL, "route_eval", "route_hidden_centered", centered_eval, eval_b.feature_id, cfg)
    )
    rows["route_feature_pca"].extend(
        feature_pca_rows(seed, ALL_POSITION_CELL, "route_eval", "route_hidden_centered", centered_eval, eval_b.feature_id, cfg)
    )
    for pool in configured_pool_order(cfg, pools):
        print(f"[A06_18] seed={seed} pool={pool} fit_eval_start", flush=True)
        pool_rows = fit_eval_pool(model, cfg, args, seed, pool, table, eval_route_hidden, eval_b, device)
        for key, vals in pool_rows.items():
            rows[key].extend(vals)
        print(f"[A06_18] seed={seed} pool={pool} fit_eval_done", flush=True)
    return rows


def write_tables(out_dir: Path, rows: dict[str, list[dict]], suffix: str = "") -> None:
    table_dir = out_dir / "tables"
    for name in TABLE_NAMES:
        write_csv(table_dir / f"{name}{suffix}.csv", rows.get(name, []))


def combine_shards(out_dir: Path) -> dict[str, list[dict]]:
    table_dir = out_dir / "tables"
    combined: dict[str, list[dict]] = {}
    for name in TABLE_NAMES:
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


def plot_results(fig_dir: Path, rows: list[dict]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig_dir.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    seen = [str(r["pool"]) for r in rows]
    pools = [p for p in POOL_ORDER if p in seen] + [p for p in seen if p not in POOL_ORDER]
    pools = list(dict.fromkeys(pools))
    means, mins, maxs = [], [], []
    for pool in pools:
        vals = [float(r["feature_NMI"]) for r in rows if r["pool"] == pool]
        means.append(sum(vals) / len(vals))
        mins.append(min(vals))
        maxs.append(max(vals))
    fig, ax = plt.subplots(figsize=(max(10, 0.55 * len(pools)), 4.8))
    xs = list(range(len(pools)))
    ax.bar(xs, means, color="#4c78a8")
    ax.errorbar(xs, means, yerr=[[m - lo for m, lo in zip(means, mins)], [hi - m for m, hi in zip(means, maxs)]], fmt="none", ecolor="#222222", capsize=3)
    for x, pool in zip(xs, pools):
        vals = [float(r["feature_NMI"]) for r in rows if r["pool"] == pool]
        ax.scatter([x] * len(vals), vals, color="#f58518", s=16, zorder=3)
    ax.set_xticks(xs, pools, rotation=30, ha="right")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("held-out route feature NMI")
    ax.set_title("A06_18 label-free pool selection for route-relevant feature discovery")
    fig.tight_layout()
    fig.savefig(fig_dir / "pool_feature_nmi.png", dpi=200)
    plt.close(fig)

    seeds = sorted({int(r["seed"]) for r in rows})
    mat = []
    for seed in seeds:
        mat.append([next((float(r["feature_NMI"]) for r in rows if int(r["seed"]) == seed and r["pool"] == pool), math.nan) for pool in pools])
    fig, ax = plt.subplots(figsize=(10, 3.8))
    im = ax.imshow(mat, vmin=0.0, vmax=1.0, cmap="viridis", aspect="auto")
    ax.set_yticks(range(len(seeds)), [str(s) for s in seeds])
    ax.set_xticks(range(len(pools)), pools, rotation=35, ha="right")
    ax.set_title("A06_18 feature NMI by seed and pool")
    fig.colorbar(im, ax=ax, label="feature NMI")
    fig.tight_layout()
    fig.savefig(fig_dir / "pool_feature_nmi_heatmap.png", dpi=200)
    plt.close(fig)


def aggregate_outputs(out_dir: Path, fig_dir: Path) -> None:
    rows = combine_shards(out_dir)
    comparison = rows.get("pool_comparison", [])
    agg = aggregate_mean_std(
        comparison,
        ["pool"],
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
            "fit_pool_role_entropy",
            "fit_pool_route_fraction",
            "fit_pool_slot_nonroute_fraction",
            "fit_pool_target_fraction",
            "fit_pool_neutral_fraction",
            "reconstruction_mse",
            "train_reconstruction_mse",
            "retained_variance_fraction",
            "latent_l0_mean",
            "latent_active_fraction",
        ],
    )
    order_index = {p: i for i, p in enumerate(POOL_ORDER)}
    agg = sorted(agg, key=lambda r: order_index.get(str(r["pool"]), 999))
    write_csv(out_dir / "tables" / "pool_comparison_aggregate.csv", agg)
    plot_results(fig_dir, comparison)
    write_json(
        out_dir / "run_summary.json",
        {
            "pool_count": len({r["pool"] for r in comparison}),
            "row_count": len(comparison),
            "aggregate_path": str(out_dir / "tables" / "pool_comparison_aggregate.csv"),
            "figure_dir": str(fig_dir),
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--run-stage", default="smoke", choices=["smoke", "full"])
    parser.add_argument("--seeds", default=None)
    parser.add_argument("--pools", default=None)
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

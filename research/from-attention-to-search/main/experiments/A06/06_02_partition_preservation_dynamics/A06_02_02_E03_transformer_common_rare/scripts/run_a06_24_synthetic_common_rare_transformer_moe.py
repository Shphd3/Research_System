#!/usr/bin/env python3
"""Run A06_24 synthetic common/rare Transformer-MoE routing audit."""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import os
import time
from dataclasses import dataclass
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


EXPERIMENT_ID = "A06_02_02_E03_transformer_common_rare"
FEATURE_NAMES = ["common_f0", "rare_f1", "rare_f2", "rare_f3"]
STEP0_CONDITIONS = [
    "random_raw",
    "random_common_subtract",
    "allpos_kmeans_raw",
    "allpos_kmeans_common_subtract",
    "route_kmeans_raw",
    "route_kmeans_residual_input",
    "oracle_raw",
    "oracle_residual_input",
]
TRAIN_CONDITIONS = [
    "random_raw",
    "random_common_subtract",
    "allpos_kmeans_common_subtract",
    "route_kmeans_raw",
    "route_kmeans_residual_input",
    "oracle_raw",
    "oracle_residual_input",
    "oracle_row_projected",
]


@dataclass
class Batch:
    x: torch.Tensor
    feature: torch.Tensor
    slot_start: torch.Tensor
    route_pos: torch.Tensor
    target: torch.Tensor


def parse_int_list(text: str) -> list[int]:
    return [int(part) for part in str(text).replace(",", " ").split() if part.strip()]


def set_seed(seed: int) -> None:
    torch.manual_seed(seed)
    np.random.seed(seed % (2**32 - 1))


def local_rank_world() -> tuple[int, int, int]:
    rank = int(os.environ.get("RANK", "0"))
    local_rank = int(os.environ.get("LOCAL_RANK", "0"))
    world_size = int(os.environ.get("WORLD_SIZE", "1"))
    return rank, local_rank, world_size


def init_dist_if_needed(world_size: int) -> bool:
    if world_size <= 1:
        return False
    import torch.distributed as dist

    if not dist.is_initialized():
        dist.init_process_group(backend="gloo")
    return True


def dist_barrier(enabled: bool) -> None:
    if not enabled:
        return
    import torch.distributed as dist

    dist.barrier()


def nmi(labels: torch.Tensor, preds: torch.Tensor) -> float:
    labels_np = labels.detach().cpu().numpy().astype(np.int64)
    preds_np = preds.detach().cpu().numpy().astype(np.int64)
    if labels_np.size == 0:
        return float("nan")
    label_vals = np.unique(labels_np)
    pred_vals = np.unique(preds_np)
    n = float(labels_np.size)
    mi = 0.0
    h_l = 0.0
    h_p = 0.0
    for lv in label_vals:
        p_l = float(np.sum(labels_np == lv)) / n
        h_l -= p_l * math.log(p_l + 1e-12)
    for pv in pred_vals:
        p_p = float(np.sum(preds_np == pv)) / n
        h_p -= p_p * math.log(p_p + 1e-12)
    for lv in label_vals:
        mask_l = labels_np == lv
        p_l = float(mask_l.sum()) / n
        for pv in pred_vals:
            mask_p = preds_np == pv
            p_lp = float(np.logical_and(mask_l, mask_p).sum()) / n
            if p_lp > 0:
                p_p = float(mask_p.sum()) / n
                mi += p_lp * math.log((p_lp + 1e-12) / (p_l * p_p + 1e-12))
    denom = math.sqrt(max(h_l, 0.0) * max(h_p, 0.0))
    if denom <= 1e-12:
        return 0.0
    return float(mi / denom)


def load_metrics(assign: torch.Tensor, num_experts: int) -> dict[str, float]:
    counts = torch.bincount(assign.detach().cpu(), minlength=num_experts).float()
    probs = counts / counts.sum().clamp_min(1.0)
    entropy = -(probs[probs > 0] * torch.log(probs[probs > 0])).sum()
    return {
        "max_load": float(probs.max().item()),
        "min_load": float(probs.min().item()),
        "load_imbalance": float(num_experts * torch.max(torch.abs(probs - 1.0 / num_experts)).item()),
        "effective_experts": float(torch.exp(entropy).item()),
        "active_experts": int((counts > 0).sum().item()),
    }


def best_feature_mapping(feature: torch.Tensor, assign: torch.Tensor, num_features: int, num_experts: int) -> dict[int, int]:
    feature = feature.detach().cpu()
    assign = assign.detach().cpu()
    counts = torch.zeros(num_features, num_experts, dtype=torch.long)
    for f in range(num_features):
        mask = feature == f
        if bool(mask.any()):
            counts[f] = torch.bincount(assign[mask], minlength=num_experts)
    best_perm = None
    best_score = -1
    for perm in itertools.permutations(range(num_experts), num_features):
        score = sum(int(counts[f, perm[f]].item()) for f in range(num_features))
        if score > best_score:
            best_score = score
            best_perm = perm
    return {f: int(best_perm[f]) for f in range(num_features)}


def margin_metrics(
    scores: torch.Tensor,
    feature: torch.Tensor,
    mapping: dict[int, int],
    rare_ids: list[int],
    step0_margin: torch.Tensor | None = None,
) -> tuple[dict[str, float], torch.Tensor]:
    scores_cpu = scores.detach().cpu().float()
    feature_cpu = feature.detach().cpu()
    target = torch.tensor([mapping[int(f)] for f in feature_cpu.tolist()], dtype=torch.long)
    target_scores = scores_cpu[torch.arange(scores_cpu.shape[0]), target]
    masked = scores_cpu.clone()
    masked[torch.arange(scores_cpu.shape[0]), target] = -1e9
    margin = target_scores - masked.max(dim=1).values
    rare_mask = torch.zeros_like(feature_cpu, dtype=torch.bool)
    for rid in rare_ids:
        rare_mask |= feature_cpu == int(rid)
    rare_margin = margin[rare_mask]
    sorted_rare = torch.sort(rare_margin).values if int(rare_margin.numel()) > 0 else torch.tensor([float("nan")])
    p05_idx = max(0, min(int(sorted_rare.numel()) - 1, int(math.floor(0.05 * max(0, int(sorted_rare.numel()) - 1)))))
    metrics = {
        "margin_mean": float(margin.mean().item()),
        "margin_p05": float(torch.sort(margin).values[max(0, min(int(margin.numel()) - 1, int(math.floor(0.05 * max(0, int(margin.numel()) - 1)))))].item()),
        "rare_margin_mean": float(rare_margin.mean().item()),
        "rare_margin_p05": float(sorted_rare[p05_idx].item()),
        "rare_positive_margin_frac": float((rare_margin > 0).float().mean().item()),
    }
    if step0_margin is not None:
        step0 = step0_margin.detach().cpu()
        rare_step0 = step0[rare_mask]
        eligible = rare_step0 > 0
        if bool(eligible.any()):
            metrics["rare_sign_flip_rate"] = float((rare_margin[eligible] <= 0).float().mean().item())
        else:
            metrics["rare_sign_flip_rate"] = float("nan")
    else:
        metrics["rare_sign_flip_rate"] = 0.0
    return metrics, margin


def rare_collision(feature: torch.Tensor, assign: torch.Tensor, rare_ids: list[int], num_experts: int) -> dict[str, float]:
    dominant = []
    purities = []
    for rid in rare_ids:
        mask = feature.detach().cpu() == int(rid)
        if not bool(mask.any()):
            continue
        counts = torch.bincount(assign.detach().cpu()[mask], minlength=num_experts).float()
        dominant.append(int(torch.argmax(counts).item()))
        purities.append(float((counts.max() / counts.sum().clamp_min(1.0)).item()))
    collision = 1.0 - (len(set(dominant)) / max(1, len(dominant)))
    return {
        "rare_dominant_experts": len(set(dominant)),
        "rare_collision_rate": float(collision),
        "rare_feature_purity_mean": float(np.mean(purities)) if purities else float("nan"),
    }


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


def generate_batch(args: argparse.Namespace, n: int, slot_len: int, seed: int, balanced: bool) -> Batch:
    gen = torch.Generator().manual_seed(int(seed))
    num_features = int(args.num_features)
    rare_prob = (1.0 - float(args.common_prob)) / (num_features - 1)
    probs = torch.tensor([float(args.common_prob)] + [rare_prob] * (num_features - 1), dtype=torch.float)
    if balanced:
        feature = torch.arange(n, dtype=torch.long) % num_features
        feature = feature[torch.randperm(n, generator=gen)]
    else:
        feature = torch.multinomial(probs, n, replacement=True, generator=gen)
    slot_choices = torch.tensor([v for v in parse_int_list(args.slot_starts) if v + slot_len < int(args.seq_len)], dtype=torch.long)
    if int(slot_choices.numel()) == 0:
        raise ValueError(f"no valid slot start for slot_len={slot_len}, seq_len={args.seq_len}")
    if balanced:
        slot_start = slot_choices[torch.arange(n) % int(slot_choices.numel())]
        slot_start = slot_start[torch.randperm(n, generator=gen)]
    else:
        slot_start = slot_choices[torch.randint(0, int(slot_choices.numel()), (n,), generator=gen)]
    x = torch.randint(0, int(args.num_neutral_tokens), (n, int(args.seq_len)), generator=gen)
    feature_base = int(args.num_neutral_tokens)
    target_base = feature_base + num_features
    for i in range(n):
        f = int(feature[i].item())
        start = int(slot_start[i].item())
        x[i, start : start + slot_len] = feature_base + f
        x[i, start + slot_len] = target_base + f
    route_pos = slot_start + slot_len - 1
    target = target_base + feature
    return Batch(x=x, feature=feature, slot_start=slot_start, route_pos=route_pos, target=target)


class WeightedTop1MoE(nn.Module):
    def __init__(self, d_model: int, d_ff: int, num_experts: int):
        super().__init__()
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

    def forward(self, h: torch.Tensor, router_input: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        scores = self.router(router_input)
        probs = F.softmax(scores, dim=-1)
        top = probs.argmax(dim=-1)
        expert_outs = torch.stack([expert(h) for expert in self.experts], dim=2)
        gather_idx = top.unsqueeze(-1).unsqueeze(-1).expand(-1, -1, 1, h.shape[-1])
        selected = expert_outs.gather(2, gather_idx).squeeze(2)
        selected_prob = probs.gather(-1, top.unsqueeze(-1)).squeeze(-1).unsqueeze(-1)
        return selected * selected_prob, scores, top


class TinyTransformerMoE(nn.Module):
    def __init__(self, vocab_size: int, d_model: int, num_heads: int, d_ff: int, num_experts: int):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)
        self.attn = nn.MultiheadAttention(d_model, num_heads, batch_first=True)
        self.ln1 = nn.LayerNorm(d_model)
        self.moe = WeightedTop1MoE(d_model, d_ff, num_experts)
        self.ln2 = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)

    def router_states(self, x: torch.Tensor) -> torch.Tensor:
        emb = self.embed(x)
        t = x.shape[1]
        mask = torch.triu(torch.ones(t, t, dtype=torch.bool, device=x.device), diagonal=1)
        attn_out, _ = self.attn(emb, emb, emb, attn_mask=mask, need_weights=False)
        h = self.ln1(emb + attn_out)
        return h

    def forward(self, x: torch.Tensor, common_vec: torch.Tensor | None = None) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        h = self.router_states(x)
        if common_vec is None:
            router_input = h
        else:
            router_input = h - common_vec.view(1, 1, -1).to(h.device)
        moe_out, scores, route = self.moe(h, router_input)
        y = self.ln2(h + moe_out)
        logits = self.lm_head(y)
        return logits, {"router_input": router_input, "route_scores": scores, "route": route, "hidden": h}


def route_slice(x: torch.Tensor, route_pos: torch.Tensor) -> torch.Tensor:
    return x[torch.arange(x.shape[0], device=x.device), route_pos.to(x.device)]


@torch.no_grad()
def collect_states(model: TinyTransformerMoE, batch: Batch, device: torch.device, batch_size: int) -> dict[str, torch.Tensor]:
    model.eval()
    route_states = []
    all_states = []
    all_feature = []
    all_slot_start = []
    for start in range(0, batch.x.shape[0], batch_size):
        x = batch.x[start : start + batch_size].to(device)
        rp = batch.route_pos[start : start + batch_size].to(device)
        h = model.router_states(x).detach().cpu()
        route_states.append(route_slice(h, rp.cpu()))
        all_states.append(h.reshape(-1, h.shape[-1]))
        all_feature.append(batch.feature[start : start + x.shape[0]].repeat_interleave(x.shape[1]))
        all_slot_start.append(batch.slot_start[start : start + x.shape[0]].repeat_interleave(x.shape[1]))
    return {
        "route": torch.cat(route_states, dim=0),
        "all": torch.cat(all_states, dim=0),
        "all_feature": torch.cat(all_feature, dim=0),
        "all_slot_start": torch.cat(all_slot_start, dim=0),
    }


def kmeans(x: torch.Tensor, k: int, seed: int, n_init: int, max_iter: int, device: torch.device) -> torch.Tensor:
    x_dev = x.float().to(device)
    best_centers = None
    best_obj = float("inf")
    n = x_dev.shape[0]
    for init in range(n_init):
        gen = torch.Generator(device="cpu").manual_seed(seed + 1009 * init)
        idx = torch.randperm(n, generator=gen)[:k].to(device)
        centers = x_dev[idx].clone()
        prev_assign = None
        for _ in range(max_iter):
            dist = torch.cdist(x_dev, centers)
            assign = dist.argmin(dim=1)
            if prev_assign is not None and torch.equal(assign, prev_assign):
                break
            prev_assign = assign
            new_centers = []
            for j in range(k):
                mask = assign == j
                if bool(mask.any()):
                    new_centers.append(x_dev[mask].mean(dim=0))
                else:
                    new_centers.append(x_dev[torch.randint(0, n, (1,), device=device)].squeeze(0))
            centers = torch.stack(new_centers, dim=0)
        obj = float(torch.cdist(x_dev, centers).min(dim=1).values.mean().detach().cpu().item())
        if obj < best_obj:
            best_obj = obj
            best_centers = centers.detach().cpu()
    return best_centers.float()


def equal_norm(centers: torch.Tensor, scale: float) -> torch.Tensor:
    centered = centers.float()
    centered = centered - centered.mean(dim=0, keepdim=True)
    return scale * centered / centered.norm(dim=1, keepdim=True).clamp_min(1e-8)


def set_router_from_centers(model: TinyTransformerMoE, centers: torch.Tensor, scale: float) -> None:
    rows = equal_norm(centers, scale)
    with torch.no_grad():
        model.moe.router.weight.copy_(rows.to(model.moe.router.weight.device))


def project_router_rows(model: TinyTransformerMoE, common_vec: torch.Tensor) -> None:
    c = common_vec.to(model.moe.router.weight.device).float()
    c = c / c.norm().clamp_min(1e-8)
    with torch.no_grad():
        w = model.moe.router.weight.data
        model.moe.router.weight.data = w - (w @ c).unsqueeze(1) * c.unsqueeze(0)


def oracle_centers(route_states: torch.Tensor, feature: torch.Tensor, num_features: int) -> torch.Tensor:
    centers = []
    for f in range(num_features):
        mask = feature == f
        if bool(mask.any()):
            centers.append(route_states[mask].mean(dim=0))
        else:
            centers.append(route_states.mean(dim=0))
    return torch.stack(centers, dim=0)


def make_model(args: argparse.Namespace, seed: int, device: torch.device) -> TinyTransformerMoE:
    set_seed(seed)
    vocab_size = int(args.num_neutral_tokens) + int(args.num_features) * 2
    model = TinyTransformerMoE(
        vocab_size=vocab_size,
        d_model=int(args.d_model),
        num_heads=int(args.num_heads),
        d_ff=int(args.d_ff),
        num_experts=int(args.num_experts),
    )
    return model.to(device)


def evaluate(
    model: TinyTransformerMoE,
    batch: Batch,
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
    model.eval()
    scores_parts = []
    route_parts = []
    loss_sum = 0.0
    correct = 0
    count = 0
    with torch.no_grad():
        for start in range(0, batch.x.shape[0], int(args.eval_batch_size)):
            x = batch.x[start : start + int(args.eval_batch_size)].to(device)
            rp = batch.route_pos[start : start + x.shape[0]].to(device)
            target = batch.target[start : start + x.shape[0]].to(device)
            logits, info = model(x, common_vec=common_vec)
            route_logits = route_slice(logits, rp)
            scores = route_slice(info["route_scores"], rp)
            routes = scores.argmax(dim=-1)
            loss = F.cross_entropy(route_logits, target, reduction="sum")
            loss_sum += float(loss.detach().cpu().item())
            correct += int((route_logits.argmax(dim=-1) == target).sum().detach().cpu().item())
            count += int(x.shape[0])
            scores_parts.append(scores.detach().cpu())
            route_parts.append(routes.detach().cpu())
    scores_all = torch.cat(scores_parts, dim=0)
    assign = torch.cat(route_parts, dim=0)
    feature = batch.feature.detach().cpu()
    slot_start = batch.slot_start.detach().cpu()
    rare_mask = feature > 0
    binary = (feature > 0).long()
    if mapping is None:
        mapping = best_feature_mapping(feature, assign, int(args.num_features), int(args.num_experts))
    margin_row, margins = margin_metrics(scores_all, feature, mapping, rare_ids=list(range(1, int(args.num_features))), step0_margin=step0_margin)
    rare_feature_nmi = nmi(feature[rare_mask], assign[rare_mask]) if bool(rare_mask.any()) else float("nan")
    common_rare_nmi = nmi(binary, assign)
    row = {
        "experiment_id": EXPERIMENT_ID,
        "condition": condition,
        "seed": seed,
        "slot_len": slot_len,
        "checkpoint": checkpoint,
        "eval_count": int(feature.numel()),
        "rare_eval_count": int(rare_mask.sum().item()),
        "loss": loss_sum / max(1, count),
        "target_accuracy": correct / max(1, count),
        "feature_NMI": nmi(feature, assign),
        "rare_feature_NMI": rare_feature_nmi,
        "common_rare_NMI": common_rare_nmi,
        "joint_feature_score": rare_feature_nmi * common_rare_nmi,
        "slot_start_NMI": nmi(slot_start, assign),
        **load_metrics(assign, int(args.num_experts)),
        **rare_collision(feature, assign, list(range(1, int(args.num_features))), int(args.num_experts)),
        **margin_row,
    }
    for f, e in mapping.items():
        row[f"map_feature_{f}_expert"] = e
    return row, mapping, margins


def build_initializers(
    args: argparse.Namespace,
    base_model: TinyTransformerMoE,
    calib: Batch,
    eval_batch: Batch,
    seed: int,
    slot_len: int,
    device: torch.device,
) -> dict[str, dict]:
    states = collect_states(base_model, calib, device, int(args.eval_batch_size))
    route_h = states["route"]
    all_h = states["all"]
    common_all = all_h.mean(dim=0)
    common_route = route_h.mean(dim=0)
    route_centers = kmeans(route_h, int(args.num_experts), seed + 1101, int(args.kmeans_n_init), int(args.kmeans_max_iter), device)
    route_res_centers = kmeans(route_h - common_route, int(args.num_experts), seed + 1201, int(args.kmeans_n_init), int(args.kmeans_max_iter), device)
    all_centers = kmeans(all_h, int(args.num_experts), seed + 1301, int(args.kmeans_n_init), int(args.kmeans_max_iter), device)
    all_res_centers = kmeans(all_h - common_all, int(args.num_experts), seed + 1401, int(args.kmeans_n_init), int(args.kmeans_max_iter), device)
    oracle_raw = oracle_centers(route_h, calib.feature, int(args.num_features))
    oracle_res = oracle_raw - common_route
    return {
        "random_raw": {"centers": None, "input_common": None, "project_common": None, "row_project": False},
        "random_common_subtract": {"centers": None, "input_common": common_all, "project_common": None, "row_project": False},
        "allpos_kmeans_raw": {"centers": all_centers, "input_common": None, "project_common": None, "row_project": False},
        "allpos_kmeans_common_subtract": {"centers": all_res_centers, "input_common": common_all, "project_common": None, "row_project": False},
        "route_kmeans_raw": {"centers": route_centers, "input_common": None, "project_common": None, "row_project": False},
        "route_kmeans_residual_input": {"centers": route_res_centers, "input_common": common_route, "project_common": None, "row_project": False},
        "oracle_raw": {"centers": oracle_raw, "input_common": None, "project_common": None, "row_project": False},
        "oracle_residual_input": {"centers": oracle_res, "input_common": common_route, "project_common": None, "row_project": False},
        "oracle_row_projected": {"centers": oracle_raw, "input_common": None, "project_common": common_all, "row_project": True},
    }


def init_condition_model(
    args: argparse.Namespace,
    condition: str,
    initializer: dict,
    seed: int,
    device: torch.device,
    base_state: dict[str, torch.Tensor],
) -> TinyTransformerMoE:
    model = make_model(args, seed, device)
    model.load_state_dict({k: v.to(device) for k, v in base_state.items()})
    centers = initializer.get("centers")
    if centers is not None:
        set_router_from_centers(model, centers, float(args.router_init_scale))
    if initializer.get("row_project", False):
        project_router_rows(model, initializer["project_common"])
    return model


def train_condition(
    args: argparse.Namespace,
    condition: str,
    initializer: dict,
    eval_batch: Batch,
    seed: int,
    slot_len: int,
    device: torch.device,
    base_state: dict[str, torch.Tensor],
) -> list[dict]:
    model = init_condition_model(args, condition, initializer, seed + 70001, device, base_state)
    common_vec = initializer.get("input_common")
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(args.lr), weight_decay=float(args.weight_decay))
    checkpoints = sorted(set([0] + parse_int_list(args.checkpoints)))
    checkpoint_set = set(checkpoints)
    rows = []
    mapping = None
    step0_margin = None
    row, mapping, step0_margin = evaluate(model, eval_batch, args, device, condition, seed, slot_len, 0, common_vec, None, None)
    rows.append(row)
    for step in range(1, int(args.train_steps) + 1):
        model.train()
        train_batch = generate_batch(args, int(args.train_batch_size), slot_len, seed + 900000 + step, balanced=False)
        x = train_batch.x.to(device)
        rp = train_batch.route_pos.to(device)
        target = train_batch.target.to(device)
        logits, _info = model(x, common_vec=common_vec)
        route_logits = route_slice(logits, rp)
        loss = F.cross_entropy(route_logits, target)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(args.grad_clip))
        optimizer.step()
        if initializer.get("row_project", False):
            project_router_rows(model, initializer["project_common"])
        if step in checkpoint_set:
            row, _mapping, _margins = evaluate(
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


def run_cell(args: argparse.Namespace, seed: int, slot_len: int, device: torch.device) -> tuple[list[dict], list[dict], list[dict]]:
    calib = generate_batch(args, int(args.calib_samples), slot_len, seed + 101, balanced=False)
    eval_batch = generate_batch(args, int(args.eval_samples), slot_len, seed + 202, balanced=True)
    base_model = make_model(args, seed + 3001, device)
    base_state = {k: v.detach().cpu().clone() for k, v in base_model.state_dict().items()}
    initializers = build_initializers(args, base_model, calib, eval_batch, seed, slot_len, device)
    data_rows = [
        {
            "seed": seed,
            "slot_len": slot_len,
            "split": "calib",
            "sample_count": int(calib.feature.numel()),
            "common_fraction": float((calib.feature == 0).float().mean().item()),
            "rare_fraction": float((calib.feature > 0).float().mean().item()),
            "slot_start_unique": int(torch.unique(calib.slot_start).numel()),
        },
        {
            "seed": seed,
            "slot_len": slot_len,
            "split": "eval",
            "sample_count": int(eval_batch.feature.numel()),
            "common_fraction": float((eval_batch.feature == 0).float().mean().item()),
            "rare_fraction": float((eval_batch.feature > 0).float().mean().item()),
            "slot_start_unique": int(torch.unique(eval_batch.slot_start).numel()),
        },
    ]
    step0_rows = []
    for condition in STEP0_CONDITIONS:
        model = init_condition_model(args, condition, initializers[condition], seed + 70001, device, base_state)
        common_vec = initializers[condition].get("input_common")
        row, _mapping, _margins = evaluate(model, eval_batch, args, device, condition, seed, slot_len, 0, common_vec, None, None)
        step0_rows.append(row)
    train_rows = []
    for condition in TRAIN_CONDITIONS:
        train_rows.extend(train_condition(args, condition, initializers[condition], eval_batch, seed, slot_len, device, base_state))
    return data_rows, step0_rows, train_rows


def aggregate_rows(rows: list[dict], keys: list[str], metrics: list[str]) -> list[dict]:
    groups: dict[tuple, list[dict]] = {}
    for row in rows:
        group_key = tuple(row[k] for k in keys)
        groups.setdefault(group_key, []).append(row)
    out = []
    for group_key, group_rows in sorted(groups.items()):
        base = {k: group_key[i] for i, k in enumerate(keys)}
        base["n"] = len(group_rows)
        for metric in metrics:
            vals = []
            for row in group_rows:
                try:
                    val = float(row.get(metric, "nan"))
                except (TypeError, ValueError):
                    val = float("nan")
                if not math.isnan(val):
                    vals.append(val)
            base[f"{metric}_mean"] = float(np.mean(vals)) if vals else float("nan")
            base[f"{metric}_std"] = float(np.std(vals)) if vals else float("nan")
            base[f"{metric}_min"] = float(np.min(vals)) if vals else float("nan")
            base[f"{metric}_max"] = float(np.max(vals)) if vals else float("nan")
        out.append(base)
    return out


def plot_bar(rows: list[dict], metric: str, title: str, path: Path, final_only: bool = False) -> None:
    if final_only:
        rows = [r for r in rows if str(r.get("checkpoint")) == str(max(int(x.get("checkpoint", 0)) for x in rows))]
    conds = []
    vals = []
    for row in rows:
        cond = str(row["condition"])
        if cond not in conds:
            conds.append(cond)
    for cond in conds:
        cond_vals = [float(r[f"{metric}_mean"]) for r in rows if str(r["condition"]) == cond and not math.isnan(float(r[f"{metric}_mean"]))]
        vals.append(float(np.mean(cond_vals)) if cond_vals else float("nan"))
    plt.figure(figsize=(max(8, 0.65 * len(conds)), 4.8))
    plt.bar(range(len(conds)), vals, color="#4C78A8")
    plt.xticks(range(len(conds)), conds, rotation=35, ha="right", fontsize=8)
    plt.ylabel(metric)
    plt.title(title)
    plt.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=180)
    plt.close()


def plot_trajectory(rows: list[dict], metric: str, title: str, path: Path) -> None:
    conds = sorted({str(r["condition"]) for r in rows})
    plt.figure(figsize=(8.5, 5.0))
    for cond in conds:
        cond_rows = sorted([r for r in rows if str(r["condition"]) == cond], key=lambda r: int(r["checkpoint"]))
        xs = [int(r["checkpoint"]) for r in cond_rows]
        ys = [float(r[f"{metric}_mean"]) for r in cond_rows]
        plt.plot(xs, ys, marker="o", linewidth=1.6, label=cond)
    plt.xlabel("checkpoint")
    plt.ylabel(metric)
    plt.title(title)
    plt.legend(fontsize=7, ncol=2)
    plt.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=180)
    plt.close()


def summarize_and_plot(output_dir: Path, args: argparse.Namespace, run_name: str, job_id: str | None = None) -> dict:
    partial_dir = output_dir / "partials" / run_name
    data_rows: list[dict] = []
    step0_rows: list[dict] = []
    train_rows: list[dict] = []
    for path in sorted(partial_dir.glob("data_audit_rank*.csv")):
        data_rows.extend(read_csv(path))
    for path in sorted(partial_dir.glob("step0_discovery_rank*.csv")):
        step0_rows.extend(read_csv(path))
    for path in sorted(partial_dir.glob("training_trajectory_rank*.csv")):
        train_rows.extend(read_csv(path))
    table_dir = output_dir / "tables"
    fig_dir = output_dir / "figures"
    write_csv(table_dir / "data_audit.csv", data_rows)
    write_csv(table_dir / "step0_discovery.csv", step0_rows)
    write_csv(table_dir / "training_trajectory.csv", train_rows)
    metrics = [
        "rare_feature_NMI",
        "feature_NMI",
        "common_rare_NMI",
        "joint_feature_score",
        "slot_start_NMI",
        "max_load",
        "effective_experts",
        "rare_margin_mean",
        "rare_margin_p05",
        "rare_sign_flip_rate",
        "target_accuracy",
        "loss",
        "rare_collision_rate",
    ]
    step0_agg = aggregate_rows(step0_rows, ["condition", "slot_len"], metrics)
    train_agg = aggregate_rows(train_rows, ["condition", "checkpoint", "slot_len"], metrics)
    final_step = max(int(r["checkpoint"]) for r in train_rows) if train_rows else 0
    final_rows = [r for r in train_rows if int(r["checkpoint"]) == final_step]
    final_agg = aggregate_rows(final_rows, ["condition", "slot_len"], metrics)
    write_csv(table_dir / "step0_discovery_aggregate.csv", step0_agg)
    write_csv(table_dir / "training_trajectory_aggregate.csv", train_agg)
    write_csv(table_dir / "final_aggregate.csv", final_agg)
    condition_agg_step0 = aggregate_rows(step0_rows, ["condition"], metrics)
    condition_agg_final = aggregate_rows(final_rows, ["condition"], metrics)
    trajectory_condition = aggregate_rows(train_rows, ["condition", "checkpoint"], metrics)
    write_csv(table_dir / "condition_aggregate_step0.csv", condition_agg_step0)
    write_csv(table_dir / "condition_aggregate_final.csv", condition_agg_final)
    write_csv(table_dir / "condition_trajectory_aggregate.csv", trajectory_condition)
    if condition_agg_step0:
        plot_bar(condition_agg_step0, "rare_feature_NMI", "Step-0 rare-feature NMI by condition", fig_dir / "step0_rare_feature_nmi_by_condition.png")
        plot_bar(condition_agg_step0, "joint_feature_score", "Step-0 joint common/rare and rare-feature separation", fig_dir / "step0_joint_feature_score_by_condition.png")
        plot_bar(condition_agg_step0, "max_load", "Step-0 max load by condition", fig_dir / "step0_max_load_by_condition.png")
        plot_bar(condition_agg_step0, "slot_start_NMI", "Step-0 slot-start NMI guard", fig_dir / "step0_slot_start_nmi_guard.png")
    if trajectory_condition:
        plot_trajectory(trajectory_condition, "rare_feature_NMI", "Rare-feature NMI trajectory", fig_dir / "rare_feature_nmi_trajectory.png")
        plot_trajectory(trajectory_condition, "rare_margin_p05", "Rare margin p05 trajectory", fig_dir / "rare_margin_p05_trajectory.png")
    if condition_agg_final:
        plot_bar(condition_agg_final, "rare_feature_NMI", "Final rare-feature NMI by condition", fig_dir / "final_rare_feature_nmi_by_condition.png")
        plot_bar(condition_agg_final, "joint_feature_score", "Final joint common/rare and rare-feature separation", fig_dir / "final_joint_feature_score_by_condition.png")
        plot_bar(condition_agg_final, "rare_margin_p05", "Final rare margin p05 by condition", fig_dir / "final_rare_margin_p05_by_condition.png")
    def find_metric(rows: list[dict], condition: str, metric: str) -> float:
        for row in rows:
            if str(row.get("condition")) == condition:
                return float(row.get(f"{metric}_mean", "nan"))
        return float("nan")
    key = {
        "step0_allpos_common_rare_nmi": find_metric(condition_agg_step0, "allpos_kmeans_common_subtract", "rare_feature_NMI"),
        "step0_allpos_common_joint": find_metric(condition_agg_step0, "allpos_kmeans_common_subtract", "joint_feature_score"),
        "step0_route_residual_rare_nmi": find_metric(condition_agg_step0, "route_kmeans_residual_input", "rare_feature_NMI"),
        "step0_route_residual_joint": find_metric(condition_agg_step0, "route_kmeans_residual_input", "joint_feature_score"),
        "step0_oracle_rare_nmi": find_metric(condition_agg_step0, "oracle_residual_input", "rare_feature_NMI"),
        "step0_oracle_joint": find_metric(condition_agg_step0, "oracle_residual_input", "joint_feature_score"),
        "step0_common_subtract_max_load": find_metric(condition_agg_step0, "random_common_subtract", "max_load"),
        "step0_random_max_load": find_metric(condition_agg_step0, "random_raw", "max_load"),
        "final_allpos_common_rare_nmi": find_metric(condition_agg_final, "allpos_kmeans_common_subtract", "rare_feature_NMI"),
        "final_allpos_common_joint": find_metric(condition_agg_final, "allpos_kmeans_common_subtract", "joint_feature_score"),
        "final_route_residual_rare_nmi": find_metric(condition_agg_final, "route_kmeans_residual_input", "rare_feature_NMI"),
        "final_route_residual_joint": find_metric(condition_agg_final, "route_kmeans_residual_input", "joint_feature_score"),
        "final_oracle_residual_rare_nmi": find_metric(condition_agg_final, "oracle_residual_input", "rare_feature_NMI"),
        "final_oracle_residual_joint": find_metric(condition_agg_final, "oracle_residual_input", "joint_feature_score"),
        "final_oracle_raw_rare_margin_p05": find_metric(condition_agg_final, "oracle_raw", "rare_margin_p05"),
        "final_oracle_residual_rare_margin_p05": find_metric(condition_agg_final, "oracle_residual_input", "rare_margin_p05"),
        "final_oracle_row_projected_rare_margin_p05": find_metric(condition_agg_final, "oracle_row_projected", "rare_margin_p05"),
        "max_slot_start_nmi_step0": max([float(r.get("slot_start_NMI_mean", "nan")) for r in condition_agg_step0] or [float("nan")]),
        "completed_cells": len({(r["seed"], r["slot_len"]) for r in step0_rows}),
        "completed_training_rows": len(train_rows),
        "final_step": final_step,
    }
    allpos = key["step0_allpos_common_joint"]
    route = key["step0_route_residual_joint"]
    oracle = key["step0_oracle_joint"]
    if not math.isnan(allpos) and not math.isnan(route) and not math.isnan(oracle):
        verdict = "supported" if allpos + 0.10 < min(route, oracle) else "weakened_or_insufficient"
    else:
        verdict = "insufficient"
    summary = {
        "experiment_id": EXPERIMENT_ID,
        "run_name": run_name,
        "run_stage": args.run_stage,
        "job_id": job_id or "",
        "verdict": verdict,
        "key_metrics": key,
        "config": vars(args),
        "generated_at_unix": time.time(),
        "tables": {
            "data_audit": str(table_dir / "data_audit.csv"),
            "step0_discovery": str(table_dir / "step0_discovery.csv"),
            "training_trajectory": str(table_dir / "training_trajectory.csv"),
            "condition_aggregate_step0": str(table_dir / "condition_aggregate_step0.csv"),
            "condition_aggregate_final": str(table_dir / "condition_aggregate_final.csv"),
        },
        "figures": {
            "step0_rare_feature_nmi": str(fig_dir / "step0_rare_feature_nmi_by_condition.png"),
            "step0_joint_feature_score": str(fig_dir / "step0_joint_feature_score_by_condition.png"),
            "step0_max_load": str(fig_dir / "step0_max_load_by_condition.png"),
            "slot_start_guard": str(fig_dir / "step0_slot_start_nmi_guard.png"),
            "rare_nmi_trajectory": str(fig_dir / "rare_feature_nmi_trajectory.png"),
            "rare_margin_trajectory": str(fig_dir / "rare_margin_p05_trajectory.png"),
            "final_rare_feature_nmi": str(fig_dir / "final_rare_feature_nmi_by_condition.png"),
            "final_joint_feature_score": str(fig_dir / "final_joint_feature_score_by_condition.png"),
            "final_rare_margin": str(fig_dir / "final_rare_margin_p05_by_condition.png"),
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
    parser.add_argument("--seq-len", type=int, default=32)
    parser.add_argument("--slot-starts", default="2 10 18")
    parser.add_argument("--num-features", type=int, default=4)
    parser.add_argument("--num-experts", type=int, default=4)
    parser.add_argument("--num-neutral-tokens", type=int, default=32)
    parser.add_argument("--common-prob", type=float, default=0.70)
    parser.add_argument("--d-model", type=int, default=64)
    parser.add_argument("--num-heads", type=int, default=4)
    parser.add_argument("--d-ff", type=int, default=128)
    parser.add_argument("--calib-samples", type=int, default=2048)
    parser.add_argument("--eval-samples", type=int, default=2048)
    parser.add_argument("--train-batch-size", type=int, default=256)
    parser.add_argument("--eval-batch-size", type=int, default=512)
    parser.add_argument("--train-steps", type=int, default=160)
    parser.add_argument("--checkpoints", default="10 40 80 160")
    parser.add_argument("--lr", type=float, default=2e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--grad-clip", type=float, default=1.0)
    parser.add_argument("--router-init-scale", type=float, default=1.5)
    parser.add_argument("--kmeans-n-init", type=int, default=4)
    parser.add_argument("--kmeans-max-iter", type=int, default=40)
    parser.add_argument("--job-id", default="")
    args = parser.parse_args()

    if args.run_stage == "smoke":
        args.seeds = "0"
        args.slot_lengths = "1 4"
        args.calib_samples = min(args.calib_samples, 512)
        args.eval_samples = min(args.eval_samples, 512)
        args.train_steps = min(args.train_steps, 20)
        args.checkpoints = "5 20"
        args.kmeans_n_init = min(args.kmeans_n_init, 2)
        args.kmeans_max_iter = min(args.kmeans_max_iter, 20)

    rank, local_rank, world_size = local_rank_world()
    dist_enabled = init_dist_if_needed(world_size)
    if torch.cuda.is_available():
        device = torch.device(f"cuda:{local_rank % torch.cuda.device_count()}")
        torch.cuda.set_device(device)
    else:
        device = torch.device("cpu")

    output_dir = Path(args.output_dir).resolve()
    partial_dir = output_dir / "partials" / args.run_name
    partial_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "logs").mkdir(parents=True, exist_ok=True)
    if rank == 0:
        (output_dir / "tables").mkdir(parents=True, exist_ok=True)
        (output_dir / "figures").mkdir(parents=True, exist_ok=True)
        (output_dir / "run_config.json").write_text(json.dumps(vars(args), indent=2), encoding="utf-8")

    seeds = parse_int_list(args.seeds)
    slot_lengths = parse_int_list(args.slot_lengths)
    tasks = [(seed, slot_len) for seed in seeds for slot_len in slot_lengths]
    my_tasks = tasks[rank::world_size]
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
    data_rows: list[dict] = []
    step0_rows: list[dict] = []
    train_rows: list[dict] = []
    for seed, slot_len in my_tasks:
        cell_data, cell_step0, cell_train = run_cell(args, seed, slot_len, device)
        data_rows.extend(cell_data)
        step0_rows.extend(cell_step0)
        train_rows.extend(cell_train)
        print(json.dumps({"event": "cell_done", "rank": rank, "seed": seed, "slot_len": slot_len}), flush=True)
    write_csv(partial_dir / f"data_audit_rank{rank}.csv", data_rows)
    write_csv(partial_dir / f"step0_discovery_rank{rank}.csv", step0_rows)
    write_csv(partial_dir / f"training_trajectory_rank{rank}.csv", train_rows)
    dist_barrier(dist_enabled)
    if rank == 0:
        summary = summarize_and_plot(output_dir, args, args.run_name, args.job_id)
        print(json.dumps({"event": "summary", "summary": summary}, indent=2), flush=True)
    dist_barrier(dist_enabled)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Run position/template source ablations for A05_03 common-offset collapse.

This runner writes a separate result directory and does not overwrite A05_03
common-offset raw outputs.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from multiprocessing import get_context
from pathlib import Path
from typing import Any

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import torch
from torch.nn import functional as F


EXP_DIR = Path(__file__).resolve().parents[1]
RESEARCH_ROOT = EXP_DIR.parents[4]
COMMON_EXP = RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A05/A05_03_uniform_collapse_common_offset"
WORKSPACE = (
    RESEARCH_ROOT
    / "Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding"
)

sys.path.insert(0, str(COMMON_EXP / "scripts"))
sys.path.insert(0, str(WORKSPACE / "scripts"))
sys.path.insert(0, str(WORKSPACE / "src"))

import run_a05_03_common_offset_experiments as base  # noqa: E402
import run_h0605a_true_token_conditioned_inhibition_replay as runner  # noqa: E402


METRIC = "dot_product"
PATTERNS = base.PATTERNS
SEEDS = base.SEEDS
STEP0_VARIANTS = [
    "baseline_pos",
    "zero_all_pos_step0",
    "zero_routed_pos_step0",
    "shuffle_pos_vectors_step0",
    "random_feature_position_eval_only",
]
TRAIN_VARIANTS = [
    "fixed_position_baseline",
    "no_pos_frozen_train",
    "random_feature_position_train_eval",
]


@dataclass
class PositionBatch:
    x: torch.Tensor
    slot: torch.Tensor
    b_idx: torch.Tensor
    target: torch.Tensor
    route_pos: torch.Tensor
    target_pos: torch.Tensor
    variant: torch.Tensor | None = None


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                fields.append(key)
                seen.add(key)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True))


def parse_csv_ints(value: str, default: list[int]) -> list[int]:
    if not value:
        return default
    return [int(v.strip()) for v in value.split(",") if v.strip()]


def stable_offset(*parts: object) -> int:
    text = "::".join(str(p) for p in parts)
    return sum((i + 1) * ord(ch) for i, ch in enumerate(text)) % 1_000_003


def target_token(slot: int, b_idx: int, cfg: dict) -> int:
    data = cfg["data"]
    return int(data["target_token_start"]) + slot * int(data["b_token_count_multi"]) + b_idx


def fixed_positions(cfg: dict) -> tuple[int, int]:
    data = cfg["data"]
    return int(data["b_position"]), int(data["target_position"])


def random_block_starts(cfg: dict) -> list[int]:
    data = cfg["data"]
    seq_len = int(data["seq_len"])
    block_len = int(data["prefix_len"]) + 2
    return list(range(0, seq_len - block_len + 1))


def generate_position_batch(
    cfg: dict,
    pattern: str,
    seed: int,
    samples_per_slot: int | None,
    variants_per_key: int,
    random_feature_position: bool,
    split: str,
) -> PositionBatch:
    data = cfg["data"]
    rng = random.Random(seed + (0 if split == "train" else 10000) + (911 if random_feature_position else 0))
    seq_len = int(data["seq_len"])
    prefix_start = int(data["prefix_start"])
    prefix_len = int(data["prefix_len"])
    b_pos, target_pos = fixed_positions(cfg)
    bg = int(data["background_token"])
    b_count = int(data["b_token_count_multi"])
    b_start = int(data["b_token_start"])
    starts = random_block_starts(cfg)

    rows: list[list[int]] = []
    slots: list[int] = []
    b_indices: list[int] = []
    targets: list[int] = []
    route_positions: list[int] = []
    target_positions: list[int] = []
    variants: list[int] = []

    if samples_per_slot is not None:
        for slot in range(int(data["num_slots"])):
            code = base.slot_code(pattern, slot, cfg)
            for n in range(samples_per_slot):
                b_idx = (n + rng.randrange(b_count)) % b_count
                if random_feature_position:
                    block_start = starts[(n + rng.randrange(len(starts))) % len(starts)]
                    local_prefix_start = block_start
                    local_b_pos = block_start + prefix_len
                    local_target_pos = local_b_pos + 1
                else:
                    local_prefix_start = prefix_start
                    local_b_pos = b_pos
                    local_target_pos = target_pos
                x = [bg] * seq_len
                for offset, tok in enumerate(code):
                    x[local_prefix_start + offset] = tok
                x[local_b_pos] = b_start + b_idx
                y = target_token(slot, b_idx, cfg)
                x[local_target_pos] = y
                rows.append(x)
                slots.append(slot)
                b_indices.append(b_idx)
                targets.append(y)
                route_positions.append(local_b_pos)
                target_positions.append(local_target_pos)
                variants.append(-1)
    else:
        feature_cfg = cfg.get("feature_key_eval", {})
        nuisance_tokens = [int(v) for v in feature_cfg.get("nuisance_tokens", [bg])]
        protected = set(range(prefix_start, prefix_start + prefix_len))
        protected.add(b_pos)
        protected.add(target_pos)
        variant_positions = [int(p) for p in feature_cfg.get("variant_positions", []) if int(p) not in protected]
        if not variant_positions:
            variant_positions = [p for p in range(seq_len) if p not in protected][:4]
        for slot in range(int(data["num_slots"])):
            code = base.slot_code(pattern, slot, cfg)
            for b_idx in range(b_count):
                for variant in range(variants_per_key):
                    if random_feature_position:
                        block_start = starts[(variant + slot * b_count + b_idx) % len(starts)]
                        local_prefix_start = block_start
                        local_b_pos = block_start + prefix_len
                        local_target_pos = local_b_pos + 1
                    else:
                        local_prefix_start = prefix_start
                        local_b_pos = b_pos
                        local_target_pos = target_pos
                    x = [bg] * seq_len
                    for offset, tok in enumerate(code):
                        x[local_prefix_start + offset] = tok
                    x[local_b_pos] = b_start + b_idx
                    y = target_token(slot, b_idx, cfg)
                    x[local_target_pos] = y
                    if not random_feature_position:
                        for pos_j, pos in enumerate(variant_positions):
                            x[pos] = nuisance_tokens[(variant + pos_j + rng.randrange(len(nuisance_tokens))) % len(nuisance_tokens)]
                    rows.append(x)
                    slots.append(slot)
                    b_indices.append(b_idx)
                    targets.append(y)
                    route_positions.append(local_b_pos)
                    target_positions.append(local_target_pos)
                    variants.append(variant)

    order = list(range(len(rows)))
    rng.shuffle(order)
    return PositionBatch(
        x=torch.tensor([rows[i] for i in order], dtype=torch.long),
        slot=torch.tensor([slots[i] for i in order], dtype=torch.long),
        b_idx=torch.tensor([b_indices[i] for i in order], dtype=torch.long),
        target=torch.tensor([targets[i] for i in order], dtype=torch.long),
        route_pos=torch.tensor([route_positions[i] for i in order], dtype=torch.long),
        target_pos=torch.tensor([target_positions[i] for i in order], dtype=torch.long),
        variant=torch.tensor([variants[i] for i in order], dtype=torch.long),
    )


def make_model(cfg: dict, seed: int, device: torch.device):
    return base.actual_model(cfg, METRIC, seed, device)


def apply_position_variant(model, cfg: dict, variant: str, seed: int, freeze_zero: bool = False) -> None:
    with torch.no_grad():
        if variant in {"zero_all_pos_step0", "no_pos_frozen_train"}:
            model.pos_emb.weight.zero_()
        elif variant == "zero_routed_pos_step0":
            b_pos, _ = fixed_positions(cfg)
            model.pos_emb.weight[b_pos].zero_()
        elif variant == "shuffle_pos_vectors_step0":
            g = torch.Generator(device=model.pos_emb.weight.device)
            g.manual_seed(seed + 424242)
            perm = torch.randperm(model.pos_emb.weight.shape[0], generator=g, device=model.pos_emb.weight.device)
            model.pos_emb.weight.copy_(model.pos_emb.weight[perm])
    if freeze_zero or variant == "no_pos_frozen_train":
        model.pos_emb.weight.requires_grad_(False)


def gather_route_tensor(tensor: torch.Tensor, route_pos: torch.Tensor) -> torch.Tensor:
    batch = torch.arange(tensor.shape[0], device=tensor.device)
    return tensor[batch, route_pos.to(tensor.device)]


def feature_hidden(
    model,
    batch: PositionBatch,
    device: torch.device,
    batch_size: int,
) -> dict[str, torch.Tensor]:
    hs, routes, logits, slots, b_indices, targets, route_pos, target_pos = [], [], [], [], [], [], [], []
    model.eval()
    with torch.no_grad():
        for start in range(0, batch.x.shape[0], batch_size):
            x = batch.x[start : start + batch_size].to(device)
            rp = batch.route_pos[start : start + batch_size].to(device)
            out_logits, info = model(x, return_acts=True)
            hs.append(gather_route_tensor(info["ffn_input"], rp).detach().cpu().float())
            routes.append(gather_route_tensor(info["expert_idx"], rp).detach().cpu())
            logits.append(gather_route_tensor(out_logits, rp).detach().cpu().float())
            slots.append(batch.slot[start : start + batch_size].detach().cpu())
            b_indices.append(batch.b_idx[start : start + batch_size].detach().cpu())
            targets.append(batch.target[start : start + batch_size].detach().cpu())
            route_pos.append(batch.route_pos[start : start + batch_size].detach().cpu())
            target_pos.append(batch.target_pos[start : start + batch_size].detach().cpu())
    return {
        "h": torch.cat(hs),
        "route": torch.cat(routes),
        "lm_logits": torch.cat(logits),
        "slot": torch.cat(slots),
        "b_idx": torch.cat(b_indices),
        "target": torch.cat(targets),
        "route_pos": torch.cat(route_pos),
        "target_pos": torch.cat(target_pos),
    }


def feature_centroids(data: dict[str, torch.Tensor], cfg: dict) -> tuple[torch.Tensor, list[tuple[int, int]]]:
    num_slots = int(cfg["data"]["num_slots"])
    b_count = int(cfg["data"]["b_token_count_multi"])
    centroids, keys = [], []
    for slot in range(num_slots):
        for b_idx in range(b_count):
            mask = (data["slot"] == slot) & (data["b_idx"] == b_idx)
            centroids.append(data["h"][mask].mean(dim=0))
            keys.append((slot, b_idx))
    return torch.stack(centroids), keys


def common_ratio(h_feat: torch.Tensor) -> float:
    c = h_feat.mean(dim=0)
    denom = (h_feat.norm(dim=1) ** 2).mean().item()
    return float(c.norm().item() ** 2 / denom) if denom > 0 else math.nan


def entropy_norm(load: list[float]) -> float:
    return base.entropy_norm(load)


def router_scores(model, h: torch.Tensor, correction_c: torch.Tensor | None = None) -> torch.Tensor:
    return base.router_scores(model, h, METRIC, correction_c=correction_c)


def load_from_scores(scores: torch.Tensor, num_experts: int) -> tuple[list[float], torch.Tensor]:
    top = scores.argmax(dim=1)
    return base.load_from_top(top, num_experts), top


def target_accuracy(data: dict[str, torch.Tensor]) -> float:
    pred = data["lm_logits"].argmax(dim=1)
    return float((pred == data["target"]).float().mean().item())


def feature_position_uniformity(batch: PositionBatch) -> dict[str, Any]:
    grouped = defaultdict(Counter)
    for slot, b_idx, pos in zip(batch.slot.tolist(), batch.b_idx.tolist(), batch.route_pos.tolist()):
        grouped[(int(slot), int(b_idx))][int(pos)] += 1
    counts = [count for counter in grouped.values() for count in counter.values()]
    positions = sorted({int(p) for p in batch.route_pos.tolist()})
    return {
        "num_route_positions": len(positions),
        "route_positions": " ".join(str(p) for p in positions),
        "position_count_min": min(counts) if counts else 0,
        "position_count_max": max(counts) if counts else 0,
    }


def eval_model_state(
    cfg: dict,
    model,
    pattern: str,
    seed: int,
    variant: str,
    step: int,
    random_feature_position: bool,
    variants_per_key: int,
    device: torch.device,
    eval_batch_size: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    grid = generate_position_batch(
        cfg,
        pattern,
        seed,
        samples_per_slot=None,
        variants_per_key=variants_per_key,
        random_feature_position=random_feature_position,
        split="eval",
    )
    data = feature_hidden(model, grid, device, eval_batch_size)
    h_feat, keys = feature_centroids(data, cfg)
    c = h_feat.mean(dim=0)
    scores = router_scores(model, h_feat)
    load, top = load_from_scores(scores, int(cfg["model"]["num_experts"]))
    cancel_scores = router_scores(model, h_feat, correction_c=c)
    cancel_load, cancel_top = load_from_scores(cancel_scores, int(cfg["model"]["num_experts"]))
    common_scores = router_scores(model, c.view(1, -1)).view(-1)
    common_rank = torch.argsort(common_scores, descending=True)
    dominant = int(max(range(len(load)), key=lambda i: load[i]))
    rank_of_dom = int((common_rank == dominant).nonzero(as_tuple=False)[0].item() + 1)
    b_pos, _ = fixed_positions(cfg)
    pos_vec = model.pos_emb.weight.detach().cpu().float()[b_pos]
    cos_c_pos = (
        float(F.cosine_similarity(c.detach().cpu().view(1, -1), pos_vec.view(1, -1)).item())
        if c.norm().item() > 0 and pos_vec.norm().item() > 0
        else math.nan
    )
    pos_info = feature_position_uniformity(grid)
    row = {
        "pattern": pattern,
        "seed": seed,
        "variant": variant,
        "step": step,
        "random_feature_position": int(random_feature_position),
        "common_ratio": common_ratio(h_feat),
        "cos_c_pos_embedding_at_routed_position": cos_c_pos,
        "common_score_rank_of_dominant_expert": rank_of_dom,
        "common_score_agrees_dominant": int(rank_of_dom == 1),
        "common_score_margin": float((torch.topk(common_scores, 2).values[0] - torch.topk(common_scores, 2).values[1]).item()),
        "step0_or_current_max_load_full_hidden": max(load),
        "step0_or_current_max_load_after_logit_cancel": max(cancel_load),
        "load_entropy_norm": entropy_norm(load),
        "active_experts": sum(1 for v in load if v > 0),
        "dominant_expert": dominant,
        "target_accuracy": target_accuracy(data),
        "loads": " ".join(f"{v:.6f}" for v in load),
        "cancel_loads": " ".join(f"{v:.6f}" for v in cancel_load),
        **pos_info,
    }
    heat_rows = []
    route_counts = defaultdict(Counter)
    cancel_counts = defaultdict(Counter)
    for (slot, b_idx), expert, cancel_expert in zip(keys, top.tolist(), cancel_top.tolist()):
        route_counts[(slot, b_idx)][int(expert)] += 1
        cancel_counts[(slot, b_idx)][int(cancel_expert)] += 1
    for slot, b_idx in keys:
        for expert in range(int(cfg["model"]["num_experts"])):
            heat_rows.append(
                {
                    "pattern": pattern,
                    "seed": seed,
                    "variant": variant,
                    "step": step,
                    "slot": slot,
                    "b_idx": b_idx,
                    "expert": expert,
                    "route_fraction": 1.0 if top[keys.index((slot, b_idx))].item() == expert else 0.0,
                    "cancel_route_fraction": 1.0 if cancel_top[keys.index((slot, b_idx))].item() == expert else 0.0,
                }
            )
    return row, heat_rows


def step0_position_ablation_task(task: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    cfg = base.load_cfg(task["config"])
    device = torch.device(task["device"])
    rows: list[dict[str, Any]] = []
    heat_rows: list[dict[str, Any]] = []
    for variant in STEP0_VARIANTS:
        model = make_model(cfg, int(task["seed"]), device)
        random_pos = variant == "random_feature_position_eval_only"
        if variant in {"zero_all_pos_step0", "zero_routed_pos_step0", "shuffle_pos_vectors_step0"}:
            apply_position_variant(model, cfg, variant, int(task["seed"]))
        row, heat = eval_model_state(
            cfg,
            model,
            str(task["pattern"]),
            int(task["seed"]),
            variant,
            0,
            random_pos,
            int(task["variants_per_key"]),
            device,
            int(task["eval_batch_size"]),
        )
        rows.append(row)
        heat_rows.extend(heat)
    return rows, heat_rows


def train_variant_task(task: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    cfg = base.load_cfg(task["config"])
    device = torch.device(task["device"])
    seed = int(task["seed"])
    pattern = str(task["pattern"])
    variant = str(task["variant"])
    random_pos = variant == "random_feature_position_train_eval"
    model = make_model(cfg, seed, device)
    if variant == "no_pos_frozen_train":
        apply_position_variant(model, cfg, variant, seed, freeze_zero=True)
    train_data = generate_position_batch(
        cfg,
        pattern,
        seed + stable_offset(variant),
        samples_per_slot=int(task["train_samples_per_slot"]),
        variants_per_key=int(task["variants_per_key"]),
        random_feature_position=random_pos,
        split="train",
    )
    opt = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad],
        lr=float(cfg["training"]["lr"]),
        weight_decay=float(cfg["training"]["weight_decay"]),
    )
    rng = random.Random(seed + stable_offset("train", variant, pattern))
    indices = list(range(train_data.x.shape[0]))
    eval_steps = sorted({0, 10, 20, 50, 100, 200, 400, 800, int(task["train_steps"])})
    eval_steps = [s for s in eval_steps if s <= int(task["train_steps"])]
    rows: list[dict[str, Any]] = []
    heat_rows: list[dict[str, Any]] = []
    for step in range(int(task["train_steps"]) + 1):
        if step in eval_steps:
            row, heat = eval_model_state(
                cfg,
                model,
                pattern,
                seed,
                variant,
                step,
                random_pos,
                int(task["variants_per_key"]),
                device,
                int(task["eval_batch_size"]),
            )
            row["variant"] = variant
            row["seed"] = seed
            rows.append(row)
            heat_rows.extend(heat)
        if step == int(task["train_steps"]):
            break
        model.train()
        batch_idx = [indices[rng.randrange(len(indices))] for _ in range(int(task["batch_size"]))]
        x = train_data.x[batch_idx].to(device)
        logits, _ = model(x, return_acts=True)
        loss = runner.full_ntp_loss(logits, x)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(cfg["training"]["grad_clip"]))
        opt.step()
        if variant == "no_pos_frozen_train":
            with torch.no_grad():
                model.pos_emb.weight.zero_()
    return rows, heat_rows


def worker(task: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if task["kind"] == "step0":
        return step0_position_ablation_task(task)
    return train_variant_task(task)


def summarize(rows: list[dict[str, Any]], train_steps: int) -> list[dict[str, Any]]:
    grouped = defaultdict(list)
    for row in rows:
        if int(row["step"]) == train_steps or str(row["variant"]) in STEP0_VARIANTS:
            grouped[(row["pattern"], row["variant"])].append(row)
    out = []
    for (pattern, variant), items in sorted(grouped.items()):
        final_items = [r for r in items if int(r["step"]) == train_steps]
        use_items = final_items if final_items else [r for r in items if int(r["step"]) == 0]
        n = len(use_items)
        out.append(
            {
                "pattern": pattern,
                "variant": variant,
                "n": n,
                "common_ratio_mean": sum(float(r["common_ratio"]) for r in use_items) / n if n else math.nan,
                "common_ratio_std": std([float(r["common_ratio"]) for r in use_items]),
                "step0_max_load_mean": mean_step(rows, pattern, variant, 0, "step0_or_current_max_load_full_hidden"),
                "step0_logit_cancel_max_load_mean": mean_step(rows, pattern, variant, 0, "step0_or_current_max_load_after_logit_cancel"),
                "common_score_agreement_mean": sum(float(r["common_score_agrees_dominant"]) for r in use_items) / n if n else math.nan,
                "final_max_load_mean": sum(float(r["step0_or_current_max_load_full_hidden"]) for r in final_items) / len(final_items) if final_items else math.nan,
                "final_collapse_rate": collapse_rate(final_items) if final_items else math.nan,
                "accuracy_mean": sum(float(r["target_accuracy"]) for r in final_items) / len(final_items) if final_items else math.nan,
                "interpretation": interpretation_for_variant(variant),
            }
        )
    return out


def std(vals: list[float]) -> float:
    vals = [v for v in vals if not math.isnan(v)]
    if len(vals) <= 1:
        return 0.0
    mu = sum(vals) / len(vals)
    return math.sqrt(sum((v - mu) ** 2 for v in vals) / (len(vals) - 1))


def mean_step(rows: list[dict[str, Any]], pattern: str, variant: str, step: int, key: str) -> float:
    vals = [float(r[key]) for r in rows if r["pattern"] == pattern and r["variant"] == variant and int(r["step"]) == step]
    return sum(vals) / len(vals) if vals else math.nan


def collapse_rate(items: list[dict[str, Any]]) -> float:
    if not items:
        return math.nan
    return sum(
        1
        for r in items
        if float(r["step0_or_current_max_load_full_hidden"]) >= 0.95 or int(r["active_experts"]) <= 1
    ) / len(items)


def interpretation_for_variant(variant: str) -> str:
    return {
        "baseline_pos": "original fixed-position step-0 geometry",
        "zero_all_pos_step0": "step-0 forward diagnostic with all position embeddings zeroed",
        "zero_routed_pos_step0": "step-0 forward diagnostic with only routed position embedding zeroed",
        "shuffle_pos_vectors_step0": "step-0 diagnostic testing whether absolute position vector identity matters",
        "random_feature_position_eval_only": "step-0 diagnostic with logical feature routed at variable positions",
        "fixed_position_baseline": "full-training baseline with original template",
        "no_pos_frozen_train": "full training with positional embeddings zeroed and frozen",
        "random_feature_position_train_eval": "full training/eval with feature block at variable positions and route at logical B token",
    }.get(variant, "")


def make_figures(fig_dir: Path, rows: list[dict[str, Any]], heat_rows: list[dict[str, Any]], train_steps: int) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    fig_dir.mkdir(parents=True, exist_ok=True)

    # Required route heatmaps: step0 baseline, step0 position ablation, final baseline, final position ablation.
    required = {
        "step0_baseline": ("baseline_pos", 0),
        "step0_position_ablation": ("zero_routed_pos_step0", 0),
        "final_baseline": ("fixed_position_baseline", train_steps),
        "final_position_ablation": ("no_pos_frozen_train", train_steps),
        "final_random_feature_position": ("random_feature_position_train_eval", train_steps),
    }
    num_experts = 4
    for label, (variant, step) in required.items():
        for pattern in PATTERNS:
            seeds = sorted({int(r["seed"]) for r in heat_rows if r["pattern"] == pattern and r["variant"] == variant and int(r["step"]) == step})
            for seed in seeds:
                items = [
                    r
                    for r in heat_rows
                    if r["pattern"] == pattern and r["variant"] == variant and int(r["step"]) == step and int(r["seed"]) == seed
                ]
                if not items:
                    continue
                max_b = max(int(r["b_idx"]) for r in items) + 1
                mat = np.zeros((max_b * 4, num_experts), dtype=float)
                for r in items:
                    row_idx = int(r["slot"]) * max_b + int(r["b_idx"])
                    mat[row_idx, int(r["expert"])] = float(r["route_fraction"])
                fig, ax = plt.subplots(figsize=(6, 10))
                im = ax.imshow(mat, aspect="auto", interpolation="nearest", vmin=0, vmax=1, cmap="viridis")
                ax.set_title(f"{label}: {pattern} seed={seed}")
                ax.set_xlabel("expert")
                ax.set_ylabel("feature = slot x B_i")
                ax.set_xticks(range(num_experts))
                fig.colorbar(im, ax=ax, fraction=0.045, pad=0.02)
                fig.tight_layout()
                fig.savefig(fig_dir / f"route_heatmap_{label}_{pattern}_seed{seed}.png", dpi=160)
                plt.close(fig)

    final_rows = [r for r in rows if int(r["step"]) in {0, train_steps}]
    labels = [f"{r['pattern']}\n{r['variant']}\nseed={r['seed']}\nstep={r['step']}" for r in final_rows]
    vals = [float(r["step0_or_current_max_load_full_hidden"]) for r in final_rows]
    cr = [float(r["common_ratio"]) for r in final_rows]
    if labels:
        fig, axes = plt.subplots(2, 1, figsize=(max(12, len(labels) * 0.35), 8), sharex=True)
        axes[0].bar(range(len(labels)), vals)
        axes[0].axhline(0.25, linestyle=":", color="tab:red", linewidth=1)
        axes[0].axhline(0.95, linestyle=":", color="tab:orange", linewidth=1)
        axes[0].set_ylabel("max load")
        axes[0].set_title("Position/source variants: step0 and final max-load")
        axes[0].grid(axis="y", alpha=0.25)
        axes[1].bar(range(len(labels)), cr, color="tab:green")
        axes[1].set_ylabel("common ratio")
        axes[1].set_xticks(range(len(labels)))
        axes[1].set_xticklabels(labels, rotation=80, ha="right", fontsize=6)
        axes[1].grid(axis="y", alpha=0.25)
        fig.tight_layout()
        fig.savefig(fig_dir / "position_source_max_load_and_common_ratio.png", dpi=180)
        plt.close(fig)


def run_tasks(tasks: list[dict[str, Any]], parallel: bool, max_parallel: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    heat_rows: list[dict[str, Any]] = []
    if parallel and max_parallel > 1:
        ctx = get_context("spawn")
        with ctx.Pool(processes=max_parallel) as pool:
            for rws, hws in pool.imap_unordered(worker, tasks):
                rows.extend(rws)
                heat_rows.extend(hws)
                print(f"completed task rows={len(rws)} heat={len(hws)}", flush=True)
    else:
        for task in tasks:
            rws, hws = worker(task)
            rows.extend(rws)
            heat_rows.extend(hws)
            print(f"completed {task['kind']} pattern={task['pattern']} seed={task['seed']} variant={task.get('variant','step0')}", flush=True)
    return rows, heat_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(WORKSPACE / "configs/h0605a_true_token_conditioned_inhibition_replay.json"))
    parser.add_argument("--output-dir", default=str(EXP_DIR))
    parser.add_argument("--seeds", default="20260521,20260522,20260523")
    parser.add_argument("--train-steps", type=int, default=1600)
    parser.add_argument("--train-samples-per-slot", type=int, default=5000)
    parser.add_argument("--batch-size", type=int, default=384)
    parser.add_argument("--eval-batch-size", type=int, default=512)
    parser.add_argument("--variants-per-key", type=int, default=16)
    parser.add_argument("--run-step0", action="store_true")
    parser.add_argument("--run-training", action="store_true")
    parser.add_argument("--parallel", action="store_true")
    parser.add_argument("--max-parallel", type=int, default=4)
    args = parser.parse_args()
    args.seeds = parse_csv_ints(args.seeds, SEEDS)
    if not args.run_step0 and not args.run_training:
        args.run_step0 = True
        args.run_training = True

    out_dir = Path(args.output_dir)
    table_dir = out_dir / "tables"
    fig_dir = out_dir / "figures"
    table_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    cfg = base.load_cfg(args.config)
    cuda_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
    tasks: list[dict[str, Any]] = []
    task_index = 0
    for pattern in PATTERNS:
        for seed in args.seeds:
            device = f"cuda:{task_index % cuda_count}" if cuda_count else "cpu"
            if args.run_step0:
                tasks.append(
                    {
                        "kind": "step0",
                        "config": args.config,
                        "pattern": pattern,
                        "seed": seed,
                        "variants_per_key": args.variants_per_key,
                        "eval_batch_size": args.eval_batch_size,
                        "device": device,
                    }
                )
                task_index += 1
            if args.run_training:
                for variant in TRAIN_VARIANTS:
                    device = f"cuda:{task_index % cuda_count}" if cuda_count else "cpu"
                    tasks.append(
                        {
                            "kind": "train",
                            "config": args.config,
                            "pattern": pattern,
                            "seed": seed,
                            "variant": variant,
                            "train_steps": args.train_steps,
                            "train_samples_per_slot": args.train_samples_per_slot,
                            "batch_size": args.batch_size,
                            "eval_batch_size": args.eval_batch_size,
                            "variants_per_key": args.variants_per_key,
                            "device": device,
                        }
                    )
                    task_index += 1

    rows, heat_rows = run_tasks(tasks, args.parallel, args.max_parallel)
    rows = sorted(rows, key=lambda r: (str(r["pattern"]), str(r["variant"]), int(r["seed"]), int(r["step"])))
    heat_rows = sorted(
        heat_rows,
        key=lambda r: (str(r["pattern"]), str(r["variant"]), int(r["seed"]), int(r["step"]), int(r["slot"]), int(r["b_idx"]), int(r["expert"])),
    )
    write_csv(table_dir / "p7_position_source_metrics_by_seed.csv", rows)
    write_csv(table_dir / "p7_position_source_summary.csv", summarize(rows, args.train_steps))
    write_csv(table_dir / "p7_position_source_route_heatmap.csv", heat_rows)
    make_figures(fig_dir, rows, heat_rows, args.train_steps)
    write_json(
        table_dir / "p7_position_source_run_manifest.json",
        {
            "runner": str(Path(__file__).resolve()),
            "config": str(args.config),
            "workspace": str(WORKSPACE),
            "common_experiment": str(COMMON_EXP),
            "device_count": cuda_count,
            "seeds": args.seeds,
            "patterns": PATTERNS,
            "step0_variants": STEP0_VARIANTS,
            "train_variants": TRAIN_VARIANTS,
            "train_steps": args.train_steps,
            "train_samples_per_slot": args.train_samples_per_slot,
            "batch_size": args.batch_size,
            "eval_batch_size": args.eval_batch_size,
            "variants_per_key": args.variants_per_key,
            "notes": {
                "random_feature_position": "moves the contiguous slot-code, B-token, target-token block; target token identity rule stays unchanged; route is measured at the logical B-token position",
                "no_pos_frozen_train": "zeros all positional embeddings before training and freezes the position embedding table",
            },
        },
    )


if __name__ == "__main__":
    main()

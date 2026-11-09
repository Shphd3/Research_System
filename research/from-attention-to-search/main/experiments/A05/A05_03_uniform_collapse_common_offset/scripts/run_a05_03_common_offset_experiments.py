#!/usr/bin/env python3
"""A05_03 common-offset diagnostics and intervention runs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable

import torch
from torch.nn import functional as F


RESEARCH_ROOT = Path(__file__).resolve().parents[6]
PROJECT_EXP_DIR = RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A05/A05_03_uniform_collapse_common_offset"
WORKSPACE = (
    RESEARCH_ROOT
    / "Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding"
)

sys.path.insert(0, str(WORKSPACE / "scripts"))
sys.path.insert(0, str(WORKSPACE / "src"))

import run_h0605a_true_token_conditioned_inhibition_replay as runner  # noqa: E402


PATTERNS = ["repeated", "distributed_complex"]
METRICS = ["dot_product", "cosine"]
SEEDS = [20260521, 20260522, 20260523]
MODE = "multi_b_primary"


class PatternBatch:
    def __init__(self, x: torch.Tensor, slot: torch.Tensor, b_idx: torch.Tensor, target: torch.Tensor, variant: torch.Tensor | None = None):
        self.x = x
        self.slot = slot
        self.b_idx = b_idx
        self.target = target
        self.variant = variant


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


def sha_tensor(t: torch.Tensor) -> str:
    return hashlib.sha256(t.detach().cpu().contiguous().numpy().tobytes()).hexdigest()[:16]


def parse_csv_ints(value: str, default: list[int]) -> list[int]:
    if not value:
        return default
    return [int(v.strip()) for v in value.split(",") if v.strip()]


def load_cfg(config: str) -> dict:
    path = Path(config)
    if not path.is_absolute():
        path = WORKSPACE / config
    return json.loads(path.read_text())


def slot_code(pattern: str, slot: int, cfg: dict) -> list[int]:
    data = cfg["data"]
    if pattern == "repeated":
        return [int(data["repeated_cue_tokens"][slot])] * int(data["prefix_len"])
    if pattern == "distributed_complex":
        codes = [
            ["p0", "q0", "r0", "t0", "u0"],
            ["p0", "q1", "r1", "t1", "u1"],
            ["p1", "q0", "r1", "t0", "u1"],
            ["p1", "q1", "r0", "t1", "u0"],
        ]
        token_map = data["distributed_code_tokens"]
        return [int(token_map[name]) for name in codes[slot]]
    raise ValueError(f"unknown slot pattern {pattern}")


def target_token(slot: int, b_idx: int, cfg: dict) -> int:
    return runner.target_token(slot, b_idx, cfg)


def make_condition(metric: str) -> str:
    if metric == "dot_product":
        return "R0-dot"
    if metric == "cosine":
        return "R0-cos"
    raise ValueError(f"unknown metric {metric}")


def actual_model(cfg: dict, metric: str, seed: int, device: torch.device):
    condition = make_condition(metric)
    random.seed(seed)
    torch.manual_seed(seed + 1009)
    audit_model = runner.make_condition_model(condition, cfg, device)
    del audit_model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    model = runner.make_condition_model(condition, cfg, device)
    model.eval()
    return model


def generate_train_data(cfg: dict, pattern: str, samples_per_slot: int, seed: int) -> PatternBatch:
    data = cfg["data"]
    rng = random.Random(seed)
    seq_len = int(data["seq_len"])
    prefix_start = int(data["prefix_start"])
    b_pos = int(data["b_position"])
    target_pos = int(data["target_position"])
    bg = int(data["background_token"])
    b_count = int(data["b_token_count_multi"])
    rows, slots, b_indices, targets = [], [], [], []
    for slot in range(int(data["num_slots"])):
        code = slot_code(pattern, slot, cfg)
        for n in range(samples_per_slot):
            b_idx = (n + rng.randrange(b_count)) % b_count
            x = [bg] * seq_len
            for offset, tok in enumerate(code):
                x[prefix_start + offset] = tok
            x[b_pos] = int(data["b_token_start"]) + b_idx
            y = target_token(slot, b_idx, cfg)
            x[target_pos] = y
            rows.append(x)
            slots.append(slot)
            b_indices.append(b_idx)
            targets.append(y)
    order = list(range(len(rows)))
    rng.shuffle(order)
    return PatternBatch(
        x=torch.tensor([rows[i] for i in order], dtype=torch.long),
        slot=torch.tensor([slots[i] for i in order], dtype=torch.long),
        b_idx=torch.tensor([b_indices[i] for i in order], dtype=torch.long),
        target=torch.tensor([targets[i] for i in order], dtype=torch.long),
    )


def generate_feature_grid(cfg: dict, pattern: str, seed: int, variants_per_key: int) -> PatternBatch:
    data = cfg["data"]
    feature_cfg = cfg["feature_key_eval"]
    rng = random.Random(seed + int(feature_cfg.get("seed_offset", 70001)))
    seq_len = int(data["seq_len"])
    prefix_start = int(data["prefix_start"])
    b_pos = int(data["b_position"])
    target_pos = int(data["target_position"])
    bg = int(data["background_token"])
    b_count = int(data["b_token_count_multi"])
    nuisance = [int(v) for v in feature_cfg.get("nuisance_tokens", [bg])]
    protected = set(range(prefix_start, prefix_start + int(data["prefix_len"])))
    protected.add(b_pos)
    protected.add(target_pos)
    variant_positions = [int(p) for p in feature_cfg.get("variant_positions", []) if int(p) not in protected]
    if not variant_positions:
        variant_positions = [p for p in range(seq_len) if p not in protected][:4]
    rows, slots, b_indices, variants, targets = [], [], [], [], []
    for slot in range(int(data["num_slots"])):
        code = slot_code(pattern, slot, cfg)
        for b_idx in range(b_count):
            for variant in range(variants_per_key):
                x = [bg] * seq_len
                for offset, tok in enumerate(code):
                    x[prefix_start + offset] = tok
                x[b_pos] = int(data["b_token_start"]) + b_idx
                y = target_token(slot, b_idx, cfg)
                x[target_pos] = y
                for pos_j, pos in enumerate(variant_positions):
                    x[pos] = nuisance[(variant + pos_j + rng.randrange(len(nuisance))) % len(nuisance)]
                rows.append(x)
                slots.append(slot)
                b_indices.append(b_idx)
                variants.append(variant)
                targets.append(y)
    order = list(range(len(rows)))
    rng.shuffle(order)
    return PatternBatch(
        x=torch.tensor([rows[i] for i in order], dtype=torch.long),
        slot=torch.tensor([slots[i] for i in order], dtype=torch.long),
        b_idx=torch.tensor([b_indices[i] for i in order], dtype=torch.long),
        target=torch.tensor([targets[i] for i in order], dtype=torch.long),
        variant=torch.tensor([variants[i] for i in order], dtype=torch.long),
    )


def router_scores(model, h: torch.Tensor, metric: str, correction_c: torch.Tensor | None = None) -> torch.Tensor:
    w = model.moe.router.weight.detach().to(h.device).float()
    if metric == "dot_product":
        scores = F.linear(h, w)
        if correction_c is not None:
            offset = F.linear(correction_c.to(h.device).float().view(1, -1), w).view(-1)
            scores = scores - offset
        return scores
    h_norm = F.normalize(h, p=2, dim=-1, eps=float(model.moe.router_eps))
    w_norm = F.normalize(w, p=2, dim=-1, eps=float(model.moe.router_eps))
    scores = float(model.moe.router_temperature) * (h_norm @ w_norm.T)
    if correction_c is not None:
        c_norm = F.normalize(correction_c.to(h.device).float().view(1, -1), p=2, dim=-1, eps=float(model.moe.router_eps))
        offset = float(model.moe.router_temperature) * (c_norm @ w_norm.T).view(-1)
        scores = scores - offset
    return scores


def feature_hidden(model, cfg: dict, grid: PatternBatch, device: torch.device, batch_size: int):
    b_pos = int(cfg["data"]["b_position"])
    hs, routes, logits, slots, b_indices, targets = [], [], [], [], [], []
    model.eval()
    with torch.no_grad():
        for start in range(0, grid.x.shape[0], batch_size):
            x = grid.x[start : start + batch_size].to(device)
            out_logits, info = model(x, return_acts=True)
            hs.append(info["ffn_input"][:, b_pos, :].detach().cpu().float())
            routes.append(info["expert_idx"][:, b_pos].detach().cpu())
            logits.append(out_logits[:, b_pos, :].detach().cpu().float())
            slots.append(grid.slot[start : start + batch_size].detach().cpu())
            b_indices.append(grid.b_idx[start : start + batch_size].detach().cpu())
            targets.append(grid.target[start : start + batch_size].detach().cpu())
    return {
        "h": torch.cat(hs),
        "route": torch.cat(routes),
        "lm_logits": torch.cat(logits),
        "slot": torch.cat(slots),
        "b_idx": torch.cat(b_indices),
        "target": torch.cat(targets),
    }


def feature_centroids(data: dict, cfg: dict):
    num_slots = int(cfg["data"]["num_slots"])
    b_count = int(cfg["data"]["b_token_count_multi"])
    centroids, keys = [], []
    for slot in range(num_slots):
        for b_idx in range(b_count):
            mask = (data["slot"] == slot) & (data["b_idx"] == b_idx)
            centroids.append(data["h"][mask].mean(dim=0))
            keys.append((slot, b_idx))
    return torch.stack(centroids), keys


def load_from_top(top: torch.Tensor, num_experts: int) -> list[float]:
    counts = torch.bincount(top.cpu(), minlength=num_experts).float()
    load = counts / counts.sum().clamp_min(1)
    return [float(v.item()) for v in load]


def entropy_norm(load: list[float]) -> float:
    vals = [v for v in load if v > 0]
    if not vals:
        return math.nan
    ent = -sum(v * math.log(v) for v in vals)
    return ent / math.log(len(load)) if len(load) > 1 else 1.0


def source_alignment(model, cfg: dict, pattern: str, c: torch.Tensor) -> dict:
    data = cfg["data"]
    b_pos = int(data["b_position"])
    b_count = int(data["b_token_count_multi"])
    b_start = int(data["b_token_start"])
    token_emb = model.token_emb.weight.detach().cpu().float()
    pos_emb = model.pos_emb.weight.detach().cpu().float()
    c_unit = F.normalize(c.view(1, -1), p=2, dim=1).view(-1)
    slot_tokens = []
    for slot in range(int(data["num_slots"])):
        slot_tokens.extend(slot_code(pattern, slot, cfg))
    raw_b = torch.stack([token_emb[b_start + b] + pos_emb[b_pos] for b in range(b_count)])
    sources = {
        "cos_pos_emb": pos_emb[b_pos],
        "cos_raw_b_position": raw_b.mean(dim=0),
        "cos_mean_b_emb": token_emb[torch.arange(b_start, b_start + b_count)].mean(dim=0),
        "cos_mean_slot_emb": token_emb[torch.tensor(slot_tokens)].mean(dim=0),
        "cos_background_emb": token_emb[int(data["background_token"])],
    }
    out = {}
    for name, vec in sources.items():
        out[name] = float((F.normalize(vec.view(1, -1), p=2, dim=1).view(-1) * c_unit).sum().item())
    return out


def step0_diagnostic(cfg: dict, model, pattern: str, metric: str, seed: int, variants: int, device: torch.device, batch_size: int) -> tuple[dict, torch.Tensor]:
    grid = generate_feature_grid(cfg, pattern, seed, variants)
    data = feature_hidden(model, cfg, grid, device, batch_size)
    h_feat, _ = feature_centroids(data, cfg)
    c = h_feat.mean(dim=0)
    residual = h_feat - c
    pos_sub = h_feat - model.pos_emb.weight.detach().cpu().float()[int(cfg["data"]["b_position"])]
    common_ratio = float(c.norm().item() / h_feat.norm(dim=1).mean().item())
    full_scores = router_scores(model, h_feat, metric)
    residual_scores = router_scores(model, residual, metric)
    pos_sub_scores = router_scores(model, pos_sub, metric)
    cancel_scores = router_scores(model, h_feat, metric, correction_c=c)
    full_top = full_scores.argmax(dim=1)
    residual_top = residual_scores.argmax(dim=1)
    pos_sub_top = pos_sub_scores.argmax(dim=1)
    cancel_top = cancel_scores.argmax(dim=1)
    full_load = load_from_top(full_top, int(cfg["model"]["num_experts"]))
    residual_load = load_from_top(residual_top, int(cfg["model"]["num_experts"]))
    pos_sub_load = load_from_top(pos_sub_top, int(cfg["model"]["num_experts"]))
    cancel_load = load_from_top(cancel_top, int(cfg["model"]["num_experts"]))
    common_scores = router_scores(model, c.view(1, -1), metric).view(-1)
    top2 = torch.topk(common_scores, 2).values
    full_top2 = torch.topk(full_scores, 2, dim=1).values
    row = {
        "protocol": "P1_P2",
        "pattern": pattern,
        "metric": metric,
        "seed": seed,
        "num_features": h_feat.shape[0],
        "variants_per_feature": variants,
        "common_norm": float(c.norm().item()),
        "feature_norm_mean": float(h_feat.norm(dim=1).mean().item()),
        "common_ratio": common_ratio,
        "full_loads": " ".join(f"{v:.6f}" for v in full_load),
        "full_max_load": max(full_load),
        "full_entropy_norm": entropy_norm(full_load),
        "residual_loads": " ".join(f"{v:.6f}" for v in residual_load),
        "residual_max_load": max(residual_load),
        "position_subtracted_loads": " ".join(f"{v:.6f}" for v in pos_sub_load),
        "position_subtracted_max_load": max(pos_sub_load),
        "logit_cancel_step0_loads": " ".join(f"{v:.6f}" for v in cancel_load),
        "logit_cancel_step0_max_load": max(cancel_load),
        "common_scores": " ".join(f"{float(v.item()):.6f}" for v in common_scores),
        "common_score_argmax": int(common_scores.argmax().item()),
        "full_dominant_expert": int(full_top.bincount(minlength=int(cfg["model"]["num_experts"])).argmax().item()),
        "common_score_margin": float((top2[0] - top2[1]).item()),
        "mean_top1_margin": float((full_top2[:, 0] - full_top2[:, 1]).mean().item()),
        "common_argmax_matches_full_dominant": int(common_scores.argmax().item() == full_top.bincount(minlength=int(cfg["model"]["num_experts"])).argmax().item()),
    }
    row.update(source_alignment(model, cfg, pattern, c))
    return row, c.detach().cpu()


def install_logit_correction(model, metric: str, c: torch.Tensor) -> None:
    original_router_logits = model.moe.router_logits
    c_cpu = c.detach().cpu().float()

    def corrected_router_logits(x: torch.Tensor) -> torch.Tensor:
        logits = original_router_logits(x)
        w = model.moe.router.weight
        if metric == "dot_product":
            offset = F.linear(c_cpu.to(x.device).view(1, -1), w).view(-1)
        else:
            c_norm = F.normalize(c_cpu.to(x.device).view(1, -1), p=2, dim=-1, eps=float(model.moe.router_eps))
            w_norm = F.normalize(w, p=2, dim=-1, eps=float(model.moe.router_eps))
            offset = float(model.moe.router_temperature) * (c_norm @ w_norm.T).view(-1)
        return logits - offset.view(*([1] * (logits.ndim - 1)), -1)

    model.moe.router_logits = corrected_router_logits  # type: ignore[method-assign]


def eval_training_state(cfg: dict, model, pattern: str, metric: str, seed: int, intervention: str, step: int, variants: int, device: torch.device, batch_size: int, c0: torch.Tensor) -> tuple[dict, list[dict]]:
    grid = generate_feature_grid(cfg, pattern, seed, variants)
    data = feature_hidden(model, cfg, grid, device, batch_size)
    num_experts = int(cfg["model"]["num_experts"])
    load = load_from_top(data["route"], num_experts)
    pred = data["lm_logits"].argmax(dim=1)
    acc = float((pred == data["target"]).float().mean().item())
    loss = float(F.cross_entropy(data["lm_logits"], data["target"]).item())
    route_counts = defaultdict(Counter)
    for slot, b_idx, expert in zip(data["slot"].tolist(), data["b_idx"].tolist(), data["route"].tolist()):
        route_counts[(slot, b_idx)][expert] += 1
    consistency = []
    for counts in route_counts.values():
        total = sum(counts.values())
        consistency.append(max(counts.values()) / total)
    h_feat, _ = feature_centroids(data, cfg)
    c_now = h_feat.mean(dim=0)
    common_scores_raw = router_scores(model, c_now.view(1, -1), metric).view(-1)
    common_scores_c0 = router_scores(model, c0.view(1, -1), metric).view(-1)
    row = {
        "protocol": "P3",
        "pattern": pattern,
        "metric": metric,
        "seed": seed,
        "intervention": intervention,
        "step": step,
        "load_by_expert": " ".join(f"{v:.6f}" for v in load),
        "max_load": max(load),
        "load_entropy_norm": entropy_norm(load),
        "active_experts": sum(1 for v in load if v > 0),
        "dominant_expert": int(max(range(len(load)), key=lambda i: load[i])),
        "target_accuracy": acc,
        "target_loss": loss,
        "feature_key_consistency": sum(consistency) / len(consistency),
        "common_score_raw": " ".join(f"{float(v.item()):.6f}" for v in common_scores_raw),
        "common_score_on_c0": " ".join(f"{float(v.item()):.6f}" for v in common_scores_c0),
        "c_norm": float(c_now.norm().item()),
    }
    heat_rows = []
    for slot in range(int(cfg["data"]["num_slots"])):
        mask = data["slot"] == slot
        counts = torch.bincount(data["route"][mask], minlength=num_experts).float()
        fractions = counts / counts.sum().clamp_min(1)
        for expert in range(num_experts):
            heat_rows.append(
                {
                    "pattern": pattern,
                    "metric": metric,
                    "seed": seed,
                    "intervention": intervention,
                    "step": step,
                    "slot": slot,
                    "expert": expert,
                    "fraction": float(fractions[expert].item()),
                }
            )
    return row, heat_rows


def train_one(cfg: dict, pattern: str, metric: str, seed: int, intervention: str, args, device: torch.device) -> tuple[list[dict], list[dict]]:
    model = actual_model(cfg, metric, seed, device)
    _, c0 = step0_diagnostic(cfg, model, pattern, metric, seed, args.variants_per_key, device, args.eval_batch_size)
    if intervention == "logit_common_offset_cancel":
        install_logit_correction(model, metric, c0)
    train_data = generate_train_data(cfg, pattern, args.train_samples_per_slot, seed)
    opt = torch.optim.AdamW(
        model.parameters(),
        lr=float(cfg["training"]["lr"]),
        weight_decay=float(cfg["training"]["weight_decay"]),
    )
    rng = random.Random(seed + 17)
    indices = list(range(train_data.x.shape[0]))
    eval_steps = sorted({0, 10, 20, 50, 100, 200, args.train_steps})
    eval_steps = [s for s in eval_steps if s <= args.train_steps]
    metric_rows, heat_rows = [], []
    for step in range(0, args.train_steps + 1):
        if step in eval_steps:
            row, rows = eval_training_state(cfg, model, pattern, metric, seed, intervention, step, args.variants_per_key, device, args.eval_batch_size, c0)
            metric_rows.append(row)
            heat_rows.extend(rows)
        if step == args.train_steps:
            break
        model.train()
        batch_idx = [indices[rng.randrange(len(indices))] for _ in range(args.batch_size)]
        x = train_data.x[batch_idx].to(device)
        logits, _ = model(x, return_acts=True)
        loss = runner.full_ntp_loss(logits, x)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(cfg["training"]["grad_clip"]))
        opt.step()
    return metric_rows, heat_rows


def data_count_rows(cfg: dict, args) -> list[dict]:
    rows = []
    for pattern in PATTERNS:
        for seed in args.seeds:
            grid = generate_feature_grid(cfg, pattern, seed, args.variants_per_key)
            counts = Counter(zip(grid.slot.tolist(), grid.b_idx.tolist()))
            vals = list(counts.values())
            rows.append(
                {
                    "pattern": pattern,
                    "seed": seed,
                    "num_rows": int(grid.x.shape[0]),
                    "x_hash": sha_tensor(grid.x[: min(4096, grid.x.shape[0])]),
                    "num_keys": len(counts),
                    "min_count": min(vals),
                    "max_count": max(vals),
                    "expected_count": args.variants_per_key,
                    "balanced_exact": int(min(vals) == max(vals) == args.variants_per_key),
                }
            )
    return rows


def p0_rows(base_dir: Path) -> list[dict]:
    source_dir = RESEARCH_ROOT / "daily_research_reports/0607/uniform_collapse_audit/tables"
    required = [
        "data_uniformity_counts.csv",
        "batch_order_entropy.csv",
        "initialization_parameter_stats.csv",
        "step0_hidden_common_geometry.csv",
        "common_direction_source_alignment.csv",
        "router_score_decomposition.csv",
        "random_geometry_baseline.csv",
        "early_gradient_self_reinforcement.csv",
    ]
    rows = []
    for name in required:
        path = source_dir / name
        rows.append({"artifact": name, "exists": int(path.exists()), "source": str(path)})
    rows.append({"artifact": "p0_pass", "exists": int(all((source_dir / name).exists() for name in required)), "source": str(source_dir)})
    return rows


def summarize_p2(rows: list[dict]) -> list[dict]:
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["pattern"], row["metric"])].append(row)
    out = []
    for (pattern, metric), items in grouped.items():
        n = len(items)
        matches = sum(int(r["common_argmax_matches_full_dominant"]) for r in items)
        out.append(
            {
                "pattern": pattern,
                "metric": metric,
                "n": n,
                "common_argmax_step0_agreement": matches / n if n else math.nan,
                "random_baseline": 0.25,
                "mean_full_max_load": sum(float(r["full_max_load"]) for r in items) / n if n else math.nan,
                "mean_residual_max_load": sum(float(r["residual_max_load"]) for r in items) / n if n else math.nan,
                "mean_logit_cancel_step0_max_load": sum(float(r["logit_cancel_step0_max_load"]) for r in items) / n if n else math.nan,
            }
        )
    return out


def summarize_p3(rows: list[dict], train_steps: int) -> list[dict]:
    final_rows = [r for r in rows if int(r["step"]) == train_steps]
    grouped = defaultdict(list)
    for row in final_rows:
        grouped[(row["pattern"], row["metric"], row["intervention"])].append(row)
    out = []
    for key, items in grouped.items():
        n = len(items)
        collapse = sum(1 for r in items if float(r["max_load"]) >= 0.95 or int(r["active_experts"]) <= 1)
        out.append(
            {
                "pattern": key[0],
                "metric": key[1],
                "intervention": key[2],
                "n": n,
                "final_collapse_rate": collapse / n if n else math.nan,
                "final_max_load_mean": sum(float(r["max_load"]) for r in items) / n if n else math.nan,
                "final_load_entropy_mean": sum(float(r["load_entropy_norm"]) for r in items) / n if n else math.nan,
                "target_accuracy_mean": sum(float(r["target_accuracy"]) for r in items) / n if n else math.nan,
                "feature_key_consistency_mean": sum(float(r["feature_key_consistency"]) for r in items) / n if n else math.nan,
            }
        )
    return out


def make_figures(fig_dir: Path, p1_rows: list[dict], p3_rows: list[dict], heat_rows: list[dict], train_steps: int) -> None:
    import matplotlib.pyplot as plt

    fig_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    labels = []
    full, resid, cancel = [], [], []
    for row in p1_rows:
        if row["metric"] != "dot_product":
            continue
        labels.append(f"{row['pattern']}\n{row['seed']}")
        full.append(float(row["full_max_load"]))
        resid.append(float(row["residual_max_load"]))
        cancel.append(float(row["logit_cancel_step0_max_load"]))
    x = torch.arange(len(labels)).float()
    axes[0].bar((x - 0.25).tolist(), full, width=0.25, label="full")
    axes[0].bar(x.tolist(), resid, width=0.25, label="residual")
    axes[0].bar((x + 0.25).tolist(), cancel, width=0.25, label="logit cancel")
    axes[0].axhline(0.25, color="#555555", linestyle="--", linewidth=0.8)
    axes[0].set_xticks(x.tolist(), labels, rotation=45, ha="right", fontsize=7)
    axes[0].set_ylabel("max load")
    axes[0].set_title("P1: step-0 load by slot pattern")
    axes[0].legend(frameon=False)

    margins = [float(r["common_score_margin"]) for r in p1_rows if r["metric"] == "dot_product"]
    loads = [float(r["full_max_load"]) for r in p1_rows if r["metric"] == "dot_product"]
    colors = ["#386cb0" if r["pattern"] == "repeated" else "#fdb462" for r in p1_rows if r["metric"] == "dot_product"]
    axes[1].scatter(margins, loads, c=colors)
    axes[1].set_xlabel("common-score margin")
    axes[1].set_ylabel("full max load")
    axes[1].set_title("P2: common-score margin vs step-0 load")
    axes[1].grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(fig_dir / "p1_p2_common_source_prediction.png", dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharex=True)
    for pattern in PATTERNS:
        for intervention, linestyle in [("baseline_full_hidden", "-"), ("logit_common_offset_cancel", "--")]:
            rows = [r for r in p3_rows if r["pattern"] == pattern and r["intervention"] == intervention]
            by_step = defaultdict(list)
            for r in rows:
                by_step[int(r["step"])].append(r)
            steps = sorted(by_step)
            if not steps:
                continue
            max_load = [sum(float(r["max_load"]) for r in by_step[s]) / len(by_step[s]) for s in steps]
            acc = [sum(float(r["target_accuracy"]) for r in by_step[s]) / len(by_step[s]) for s in steps]
            label = f"{pattern} {intervention}"
            axes[0].plot(steps, max_load, linestyle=linestyle, marker="o", label=label)
            axes[1].plot(steps, acc, linestyle=linestyle, marker="o", label=label)
    axes[0].set_title("P3: max load")
    axes[0].set_ylabel("max load")
    axes[0].axhline(0.95, color="#aa3333", linestyle=":", linewidth=0.8)
    axes[1].set_title("P3: target accuracy")
    axes[1].set_ylabel("accuracy")
    for ax in axes:
        ax.set_xlabel("step")
        ax.grid(alpha=0.25)
    axes[0].legend(frameon=False, fontsize=7)
    fig.tight_layout()
    fig.savefig(fig_dir / "p3_training_load_accuracy.png", dpi=180)
    plt.close(fig)

    final_heat = [r for r in heat_rows if int(r["step"]) == train_steps and r["metric"] == "dot_product"]
    if final_heat:
        panels = []
        for pattern in PATTERNS:
            for intervention in ["baseline_full_hidden", "logit_common_offset_cancel"]:
                subset = [r for r in final_heat if r["pattern"] == pattern and r["intervention"] == intervention]
                if subset:
                    panels.append((pattern, intervention, subset))
        fig, axes = plt.subplots(len(panels), 1, figsize=(6, max(3, 2.2 * len(panels))))
        if len(panels) == 1:
            axes = [axes]
        for ax, (pattern, intervention, subset) in zip(axes, panels):
            mat = torch.zeros(4, 4)
            counts = torch.zeros(4, 4)
            for r in subset:
                slot = int(r["slot"])
                expert = int(r["expert"])
                mat[slot, expert] += float(r["fraction"])
                counts[slot, expert] += 1
            mat = mat / counts.clamp_min(1)
            im = ax.imshow(mat.numpy(), vmin=0, vmax=1, cmap="viridis", aspect="auto")
            ax.set_title(f"{pattern} / {intervention} final slot-route")
            ax.set_xlabel("expert")
            ax.set_ylabel("slot")
            fig.colorbar(im, ax=ax, fraction=0.03)
        fig.tight_layout()
        fig.savefig(fig_dir / "p3_route_heatmap_by_condition.png", dpi=180)
        plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(WORKSPACE / "configs/h0605a_true_token_conditioned_inhibition_replay.json"))
    parser.add_argument("--output-dir", default=str(PROJECT_EXP_DIR))
    parser.add_argument("--seeds", default="20260521,20260522,20260523")
    parser.add_argument("--train-steps", type=int, default=400)
    parser.add_argument("--train-samples-per-slot", type=int, default=2000)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--eval-batch-size", type=int, default=512)
    parser.add_argument("--variants-per-key", type=int, default=8)
    parser.add_argument("--skip-training", action="store_true")
    args = parser.parse_args()
    args.seeds = parse_csv_ints(args.seeds, SEEDS)

    out_dir = Path(args.output_dir)
    table_dir = out_dir / "tables"
    fig_dir = out_dir / "figures"
    table_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    cfg = load_cfg(args.config)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    p0 = p0_rows(out_dir)
    write_csv(table_dir / "p0_audit_closure.csv", p0)
    write_csv(table_dir / "data_pattern_counts.csv", data_count_rows(cfg, args))

    p1_rows = []
    c_cache = {}
    for pattern in PATTERNS:
        for metric in METRICS:
            for seed in args.seeds:
                model = actual_model(cfg, metric, seed, device)
                row, c = step0_diagnostic(cfg, model, pattern, metric, seed, args.variants_per_key, device, args.eval_batch_size)
                p1_rows.append(row)
                c_cache[(pattern, metric, seed)] = c
                print(
                    f"P1/P2 pattern={pattern} metric={metric} seed={seed} "
                    f"full_max={row['full_max_load']:.3f} cancel0={row['logit_cancel_step0_max_load']:.3f} "
                    f"match={row['common_argmax_matches_full_dominant']}",
                    flush=True,
                )
    write_csv(table_dir / "p1_step0_common_source.csv", p1_rows)
    write_csv(table_dir / "p2_common_score_prediction.csv", summarize_p2(p1_rows))

    p3_rows: list[dict] = []
    heat_rows: list[dict] = []
    if not args.skip_training:
        for pattern in PATTERNS:
            for intervention in ["baseline_full_hidden", "logit_common_offset_cancel"]:
                for seed in args.seeds:
                    rows, hrows = train_one(cfg, pattern, "dot_product", seed, intervention, args, device)
                    p3_rows.extend(rows)
                    heat_rows.extend(hrows)
                    final = rows[-1]
                    print(
                        f"P3 pattern={pattern} intervention={intervention} seed={seed} "
                        f"final_max={final['max_load']:.3f} acc={final['target_accuracy']:.3f}",
                        flush=True,
                    )
    write_csv(table_dir / "p3_training_metrics_by_step.csv", p3_rows)
    write_csv(table_dir / "p3_slot_route_heatmap.csv", heat_rows)
    write_csv(table_dir / "p3_summary_by_condition.csv", summarize_p3(p3_rows, args.train_steps))

    make_figures(fig_dir, p1_rows, p3_rows, heat_rows, args.train_steps)
    write_json(
        table_dir / "run_manifest.json",
        {
            "anchor": str(PROJECT_EXP_DIR.parent.parent / "problem_anchors/05_failure_mechanism/05_03_uniform_collapse_common_offset_anchor.md"),
            "protocol": str(PROJECT_EXP_DIR / "protocol_for_approval.md"),
            "config": str(args.config),
            "workspace": str(WORKSPACE),
            "device": str(device),
            "seeds": args.seeds,
            "patterns": PATTERNS,
            "metrics": METRICS,
            "train_steps": args.train_steps,
            "train_samples_per_slot": args.train_samples_per_slot,
            "batch_size": args.batch_size,
            "eval_batch_size": args.eval_batch_size,
            "variants_per_key": args.variants_per_key,
            "skip_training": args.skip_training,
            "can_answer": {
                "P0": "yes, if required audit artifacts exist",
                "P1": "yes for step-0 common-source diagnosis",
                "P2": "yes for step-0 common-score prediction; final prediction depends on P3 training coverage",
                "P3": "yes for causal intervention if training completes; CPU-shortened runs are mechanism evidence, not full 4-card evidence",
            },
        },
    )


if __name__ == "__main__":
    main()

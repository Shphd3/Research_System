#!/usr/bin/env python3
"""Forced feature-to-expert trajectory audit for A05_04."""

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
WORKSPACE = (
    RESEARCH_ROOT
    / "Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding"
)
sys.path.insert(0, str(WORKSPACE / "scripts"))
sys.path.insert(0, str(WORKSPACE / "src"))

import run_h0605a_true_token_conditioned_inhibition_replay as h0605a  # noqa: E402
from synthetic_data_understanding.tiny_moe import make_sparse_model  # noqa: E402


MODEL_NAME = "top1_selected_gate"
VARIANTS = [
    "V0_vanilla_random",
    "V1_random_balanced_init",
    "V2_feature_init_trainable",
    "V3_oracle_frozen",
    "V4_feature_init_inhibition",
]


@dataclass
class VarPosBatch:
    x: torch.Tensor
    slot: torch.Tensor
    target: torch.Tensor
    route_pos: torch.Tensor
    target_pos: torch.Tensor


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                fields.append(key)
                seen.add(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_list(raw: str | None, default: list[str]) -> list[str]:
    if not raw:
        return default
    return [part.strip() for part in raw.replace(" ", ",").split(",") if part.strip()]


def target_token(slot: int, cfg: dict) -> int:
    data = cfg["data"]
    return int(data["target_token_start"]) + slot * int(data["b_token_count_multi"])


def slot_code(slot: int, cfg: dict) -> list[int]:
    return [int(cfg["data"]["repeated_cue_tokens"][slot])] * int(cfg["data"]["prefix_len"])


def valid_block_starts(cfg: dict) -> list[int]:
    data = cfg["data"]
    seq_len = int(data["seq_len"])
    width = int(data["prefix_len"]) + 2
    return list(range(0, seq_len - width + 1))


def generate_varpos_batch(cfg: dict, samples_per_slot: int, seed: int, split: str) -> VarPosBatch:
    data = cfg["data"]
    rng = random.Random(seed + {"train": 0, "eval": 10000, "probe": 20000, "cal": 30000}.get(split, 40000))
    seq_len = int(data["seq_len"])
    prefix_len = int(data["prefix_len"])
    bg = int(data["background_token"])
    b_tok = int(data["b_token_start"])
    starts = valid_block_starts(cfg)
    rows: list[list[int]] = []
    slots: list[int] = []
    targets: list[int] = []
    route_positions: list[int] = []
    target_positions: list[int] = []
    for slot in range(int(data["num_slots"])):
        code = slot_code(slot, cfg)
        for n in range(samples_per_slot):
            start = starts[(n + rng.randrange(len(starts))) % len(starts)]
            route_pos = start + prefix_len
            target_pos = route_pos + 1
            x = [bg] * seq_len
            for offset, tok in enumerate(code):
                x[start + offset] = tok
            y = target_token(slot, cfg)
            x[route_pos] = b_tok
            x[target_pos] = y
            rows.append(x)
            slots.append(slot)
            targets.append(y)
            route_positions.append(route_pos)
            target_positions.append(target_pos)
    order = list(range(len(rows)))
    rng.shuffle(order)
    return VarPosBatch(
        x=torch.tensor([rows[i] for i in order], dtype=torch.long),
        slot=torch.tensor([slots[i] for i in order], dtype=torch.long),
        target=torch.tensor([targets[i] for i in order], dtype=torch.long),
        route_pos=torch.tensor([route_positions[i] for i in order], dtype=torch.long),
        target_pos=torch.tensor([target_positions[i] for i in order], dtype=torch.long),
    )


def model_cfg(cfg: dict, router_metric: str) -> dict:
    local = json.loads(json.dumps(cfg))
    local["model"]["router_metric"] = router_metric
    local["model"]["router_temperature"] = float(cfg["router_init"].get("cosine_temperature", 8.0)) if router_metric == "cosine" else 1.0
    local["model"]["router_eps"] = float(cfg["router_init"].get("router_eps", 1e-6))
    return local


def make_model(cfg: dict, router_metric: str, device: torch.device) -> torch.nn.Module:
    model = make_sparse_model(MODEL_NAME, model_cfg(cfg, router_metric), device)
    with torch.no_grad():
        model.pos_emb.weight.zero_()
    model.pos_emb.weight.requires_grad_(False)
    return model


def gather_positions(tensor: torch.Tensor, pos: torch.Tensor) -> torch.Tensor:
    idx = pos.to(tensor.device)
    return tensor[torch.arange(tensor.shape[0], device=tensor.device), idx]


def full_ntp_loss(logits: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
    return F.cross_entropy(logits[:, :-1, :].reshape(-1, logits.shape[-1]), x[:, 1:].reshape(-1))


def target_loss(logits: torch.Tensor, batch: VarPosBatch, reduction: str = "mean") -> torch.Tensor:
    route_pos = batch.route_pos.to(logits.device)
    target = batch.target.to(logits.device)
    pred_logits = logits[torch.arange(logits.shape[0], device=logits.device), route_pos]
    return F.cross_entropy(pred_logits, target, reduction=reduction)


def nmi(labels_a: list[int], labels_b: list[int]) -> float:
    if not labels_a or len(labels_a) != len(labels_b):
        return math.nan
    n = len(labels_a)
    ca = Counter(labels_a)
    cb = Counter(labels_b)
    cab = Counter(zip(labels_a, labels_b))
    mi = 0.0
    for (a, b), c in cab.items():
        mi += (c / n) * math.log((c * n) / (ca[a] * cb[b] + 1e-12) + 1e-12)
    ha = -sum((c / n) * math.log(c / n) for c in ca.values())
    hb = -sum((c / n) * math.log(c / n) for c in cb.values())
    return float(mi / math.sqrt(max(ha * hb, 1e-12)))


def load_entropy(counts: torch.Tensor) -> tuple[float, float]:
    counts = counts.float().cpu()
    total = float(counts.sum().item())
    if total <= 0:
        return math.nan, math.nan
    p = counts / total
    mask = p > 0
    entropy = float(-(p[mask] * p[mask].log()).sum().item())
    return entropy, entropy / math.log(max(2, counts.numel()))


def router_similarity(model: torch.nn.Module, h: torch.Tensor) -> torch.Tensor:
    return h0605a.router_similarity(model, h)


def feature_init_router(model: torch.nn.Module, cfg: dict, seed: int, device: torch.device) -> dict[str, float]:
    cal = generate_varpos_batch(cfg, int(cfg["data"]["calibration_samples_per_slot"]), seed, "cal")
    hs: list[torch.Tensor] = []
    slots: list[torch.Tensor] = []
    batch_size = int(cfg["evaluation"]["batch_size"])
    model.eval()
    with torch.no_grad():
        for start in range(0, cal.x.shape[0], batch_size):
            sub = VarPosBatch(cal.x[start:start + batch_size], cal.slot[start:start + batch_size], cal.target[start:start + batch_size], cal.route_pos[start:start + batch_size], cal.target_pos[start:start + batch_size])
            _, info = model(sub.x.to(device), return_acts=True)
            hs.append(gather_positions(info["ffn_input"], sub.route_pos).detach().cpu())
            slots.append(sub.slot)
    h = torch.cat(hs).float()
    slot = torch.cat(slots)
    num_slots = int(cfg["data"]["num_slots"])
    means = torch.stack([h[slot == s].mean(dim=0) for s in range(num_slots)])
    center = means.mean(dim=0, keepdim=True)
    dirs = means - center
    if bool(cfg["router_init"].get("use_whitening", True)):
        centered = h - h.mean(dim=0, keepdim=True)
        cov = centered.T @ centered / max(1, centered.shape[0] - 1)
        eye = torch.eye(cov.shape[0])
        dirs = torch.linalg.solve(cov + float(cfg["router_init"]["ridge"]) * eye, dirs.T).T
    dirs = dirs / dirs.norm(dim=1, keepdim=True).clamp_min(1e-8)
    alpha = float(cfg["router_init"]["alpha"])
    with torch.no_grad():
        model.moe.router.weight.copy_(alpha * dirs.to(device))
    return {"feature_init_centroid_norm": float((means - center).norm(dim=1).mean().item()), "feature_init_alpha": alpha}


def route_metrics_for_weights(model: torch.nn.Module, cfg: dict, seed: int, device: torch.device) -> tuple[float, float]:
    data = generate_varpos_batch(cfg, 128, seed, "cal")
    counts = torch.zeros(int(cfg["data"]["num_slots"]), int(cfg["model"]["num_experts"]))
    slot_labels: list[int] = []
    expert_labels: list[int] = []
    model.eval()
    with torch.no_grad():
        for start in range(0, data.x.shape[0], int(cfg["evaluation"]["batch_size"])):
            sub = VarPosBatch(data.x[start:start + int(cfg["evaluation"]["batch_size"])], data.slot[start:start + int(cfg["evaluation"]["batch_size"])], data.target[start:start + int(cfg["evaluation"]["batch_size"])], data.route_pos[start:start + int(cfg["evaluation"]["batch_size"])], data.target_pos[start:start + int(cfg["evaluation"]["batch_size"])])
            _, info = model(sub.x.to(device), return_acts=True)
            expert = gather_positions(info["expert_idx"], sub.route_pos).detach().cpu()
            for s, e in zip(sub.slot.tolist(), expert.tolist()):
                counts[int(s), int(e)] += 1
                slot_labels.append(int(s))
                expert_labels.append(int(e))
    load = counts.sum(dim=0)
    return float((load / load.sum().clamp_min(1)).max().item()), nmi(slot_labels, expert_labels)


def random_balanced_init(model: torch.nn.Module, cfg: dict, seed: int, device: torch.device, candidates: int = 128) -> dict[str, float]:
    gen = torch.Generator(device=device)
    gen.manual_seed(seed + 991)
    original = model.moe.router.weight.detach().clone()
    best_score = float("inf")
    best_weight = original.clone()
    best = {"balanced_init_max_load": math.nan, "balanced_init_slot_nmi": math.nan}
    bound = 1.0 / math.sqrt(model.moe.router.weight.shape[1])
    with torch.no_grad():
        for _ in range(candidates):
            cand = torch.empty_like(model.moe.router.weight).uniform_(-bound, bound, generator=gen)
            model.moe.router.weight.copy_(cand)
            max_load, slot_nmi = route_metrics_for_weights(model, cfg, seed, device)
            score = abs(max_load - 0.25) + 0.5 * slot_nmi
            if score < best_score:
                best_score = score
                best_weight = cand.clone()
                best = {"balanced_init_max_load": max_load, "balanced_init_slot_nmi": slot_nmi}
        model.moe.router.weight.copy_(best_weight)
    return best


def forced_matrix_from_natural(model: torch.nn.Module, x: torch.Tensor, route_pos: torch.Tensor, forced_route_expert: torch.Tensor | int | None) -> torch.Tensor | None:
    if forced_route_expert is None:
        return None
    with torch.no_grad():
        _, info = model(x, return_acts=True)
        force = info["expert_idx"].detach().clone()
        idx = torch.arange(x.shape[0], device=x.device)
        if isinstance(forced_route_expert, int):
            force[idx, route_pos.to(x.device)] = int(forced_route_expert)
        else:
            force[idx, route_pos.to(x.device)] = forced_route_expert.to(x.device, dtype=torch.long)
    return force


def forward_variant(model: torch.nn.Module, batch: VarPosBatch, variant: str, device: torch.device, return_acts: bool = True):
    x = batch.x.to(device)
    if variant == "V3_oracle_frozen":
        force = forced_matrix_from_natural(model, x, batch.route_pos, batch.slot)
        return model(x, return_acts=return_acts, force_expert_idx=force)
    return model(x, return_acts=return_acts)


def linear_probe_accuracy(h: torch.Tensor, y: torch.Tensor, num_classes: int, steps: int = 80) -> float:
    if h.shape[0] < num_classes * 4:
        return math.nan
    device = h.device
    gen = torch.Generator(device=device)
    gen.manual_seed(123)
    perm = torch.randperm(h.shape[0], generator=gen, device=device)
    split = max(num_classes, int(0.7 * h.shape[0]))
    train_idx = perm[:split]
    test_idx = perm[split:]
    if test_idx.numel() == 0:
        return math.nan
    probe = torch.nn.Linear(h.shape[1], num_classes).to(device)
    opt = torch.optim.AdamW(probe.parameters(), lr=0.05)
    for _ in range(steps):
        logits = probe(h[train_idx])
        loss = F.cross_entropy(logits, y[train_idx])
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    with torch.no_grad():
        return float((probe(h[test_idx]).argmax(dim=-1) == y[test_idx]).float().mean().item())


def evaluate(model: torch.nn.Module, cfg: dict, variant: str, metric: str, seed: int, step: int, device: torch.device, samples_per_slot: int) -> dict[str, list[dict[str, Any]] | dict[str, Any]]:
    data = generate_varpos_batch(cfg, samples_per_slot, seed + step * 17, "eval")
    batch_size = int(cfg["evaluation"]["batch_size"])
    num_slots = int(cfg["data"]["num_slots"])
    num_experts = int(cfg["model"]["num_experts"])
    route_counts = torch.zeros(num_slots, num_experts)
    slot_labels: list[int] = []
    expert_labels: list[int] = []
    target_correct = 0
    total = 0
    target_losses: list[float] = []
    hs: list[torch.Tensor] = []
    slots_h: list[torch.Tensor] = []
    margins: list[float] = []
    utility_loss_sum = torch.zeros(num_slots, num_experts)
    utility_loss_count = torch.zeros(num_slots, num_experts)
    model.eval()
    with torch.no_grad():
        for start in range(0, data.x.shape[0], batch_size):
            sub = VarPosBatch(data.x[start:start + batch_size], data.slot[start:start + batch_size], data.target[start:start + batch_size], data.route_pos[start:start + batch_size], data.target_pos[start:start + batch_size])
            logits, info = forward_variant(model, sub, variant, device, return_acts=True)
            route_pos = sub.route_pos.to(device)
            expert = gather_positions(info["expert_idx"], sub.route_pos).detach().cpu()
            pred = logits[torch.arange(logits.shape[0], device=device), route_pos].argmax(dim=-1).detach().cpu()
            loss_vec = target_loss(logits, sub, reduction="none").detach().cpu()
            target_losses.extend([float(v) for v in loss_vec])
            target_correct += int((pred == sub.target).sum().item())
            total += int(sub.x.shape[0])
            h_route = gather_positions(info["ffn_input"], sub.route_pos).detach()
            hs.append(h_route)
            slots_h.append(sub.slot.to(device))
            rlog = gather_positions(info["router_logits"], sub.route_pos).detach().cpu()
            top2 = torch.topk(rlog, k=2, dim=-1).values
            margins.extend([float(v) for v in (top2[:, 0] - top2[:, 1]).tolist()])
            for s, e in zip(sub.slot.tolist(), expert.tolist()):
                route_counts[int(s), int(e)] += 1
                slot_labels.append(int(s))
                expert_labels.append(int(e))
            x = sub.x.to(device)
            _, natural_info = model(x, return_acts=True)
            natural_force = natural_info["expert_idx"].detach().clone()
            for forced_e in range(num_experts):
                force = natural_force.clone()
                force[torch.arange(x.shape[0], device=device), route_pos] = forced_e
                flogits, _ = model(x, return_acts=True, force_expert_idx=force)
                fl = target_loss(flogits, sub, reduction="none").detach().cpu()
                for slot, val in zip(sub.slot.tolist(), fl.tolist()):
                    utility_loss_sum[int(slot), forced_e] += float(val)
                    utility_loss_count[int(slot), forced_e] += 1
    load = route_counts.sum(dim=0)
    entropy, entropy_norm = load_entropy(load)
    route_rows = []
    for slot in range(num_slots):
        denom = float(route_counts[slot].sum().item())
        for expert in range(num_experts):
            route_rows.append({"variant": variant, "router_metric": metric, "seed": seed, "step": step, "slot": slot, "expert": expert, "count": int(route_counts[slot, expert].item()), "fraction": float(route_counts[slot, expert].item() / denom) if denom else 0.0})
    util_rows = []
    utility_best: dict[int, int] = {}
    for slot in range(num_slots):
        vals = []
        for expert in range(num_experts):
            mean_ce = float(utility_loss_sum[slot, expert].item() / max(1.0, utility_loss_count[slot, expert].item()))
            vals.append(mean_ce)
            util_rows.append({"variant": variant, "router_metric": metric, "seed": seed, "step": step, "slot": slot, "expert": expert, "forced_mean_ce": mean_ce})
        utility_best[slot] = int(min(range(num_experts), key=lambda e: vals[e]))
    route_utility_match = sum(1 for s, e in zip(slot_labels, expert_labels) if utility_best[int(s)] == int(e)) / max(1, len(slot_labels))
    h_all = torch.cat(hs).float()
    slot_all = torch.cat(slots_h).long()
    probe_acc = linear_probe_accuracy(h_all, slot_all, num_slots)
    means = torch.stack([h_all[slot_all == s].mean(dim=0) for s in range(num_slots)])
    c = means.mean(dim=0)
    residuals = means - c.unsqueeze(0)
    common_ratio = float(c.pow(2).sum().item() / means.pow(2).sum(dim=1).mean().clamp_min(1e-12).item())
    with torch.no_grad():
        w = model.moe.router.weight.detach().float()
        c_dir = c / c.norm().clamp_min(1e-8)
        r_dirs = residuals / residuals.norm(dim=1, keepdim=True).clamp_min(1e-8)
        grad_norm = math.nan
        grad_common_abs_mean = math.nan
        grad_feature_abs_mean = math.nan
        logits_cent = router_similarity(model, means.to(device)).detach().cpu()
        common_logits = (w.cpu() @ c_dir.cpu()).float()
        feature_logits = (r_dirs.cpu() @ w.cpu().T).float()
        logit_rows = [{
            "variant": variant,
            "router_metric": metric,
            "seed": seed,
            "step": step,
            "common_ratio": common_ratio,
            "common_logit_range": float((common_logits.max() - common_logits.min()).item()),
            "feature_logit_range": float((feature_logits.max() - feature_logits.min()).item()),
            "centroid_logit_range": float((logits_cent.max() - logits_cent.min()).item()),
            "top1_margin_mean": sum(margins) / len(margins) if margins else math.nan,
        }]
    metrics = {
        "variant": variant,
        "router_metric": metric,
        "seed": seed,
        "step": step,
        "route_slot_nmi": nmi(slot_labels, expert_labels),
        "max_load": float((load / load.sum().clamp_min(1)).max().item()),
        "load_entropy": entropy,
        "load_entropy_norm": entropy_norm,
        "active_experts": int((load > 0).sum().item()),
        "target_accuracy": target_correct / total if total else math.nan,
        "target_ce": sum(target_losses) / len(target_losses) if target_losses else math.nan,
        "probe_slot_from_h": probe_acc,
        "route_utility_match": route_utility_match,
        "common_ratio": common_ratio,
        "top1_margin_mean": sum(margins) / len(margins) if margins else math.nan,
        "utility_best_by_slot": json.dumps(utility_best, sort_keys=True),
    }
    return {"metrics": metrics, "route_rows": route_rows, "utility_rows": util_rows, "logit_rows": logit_rows}


def gradient_diagnostic(model: torch.nn.Module, cfg: dict, variant: str, metric: str, seed: int, step: int, device: torch.device) -> dict[str, Any]:
    data = generate_varpos_batch(cfg, min(128, int(cfg["data"]["train_samples_per_slot"])), seed + step * 19, "probe")
    sub = VarPosBatch(data.x, data.slot, data.target, data.route_pos, data.target_pos)
    model.zero_grad(set_to_none=True)
    logits, info = forward_variant(model, sub, variant, device, return_acts=True)
    loss = target_loss(logits, sub)
    if variant == "V4_feature_init_inhibition":
        h_route = gather_positions(info["ffn_input"], sub.route_pos)
        exp_route = gather_positions(info["expert_idx"], sub.route_pos)
        log_route = gather_positions(info["router_logits"], sub.route_pos)
        inh, _ = h0605a.true_token_conditioned_inhibition_loss(model, h_route, exp_route, log_route, cfg)
        loss = loss + float(cfg["true_token_inhibition"]["loss_weight"]) * inh
    loss.backward()
    grad = model.moe.router.weight.grad
    if grad is None:
        return {"variant": variant, "router_metric": metric, "seed": seed, "step": step, "router_grad_norm": 0.0, "grad_common_abs_mean": 0.0, "grad_feature_abs_mean": 0.0}
    h_route = gather_positions(info["ffn_input"], sub.route_pos).detach().float()
    slots = sub.slot.to(device)
    means = torch.stack([h_route[slots == s].mean(dim=0) for s in range(int(cfg["data"]["num_slots"]))])
    c = means.mean(dim=0)
    residuals = means - c.unsqueeze(0)
    c_dir = c / c.norm().clamp_min(1e-8)
    r_dirs = residuals / residuals.norm(dim=1, keepdim=True).clamp_min(1e-8)
    common_proj = torch.abs(grad.detach().float() @ c_dir)
    feature_proj = torch.abs(grad.detach().float() @ r_dirs.T)
    return {
        "variant": variant,
        "router_metric": metric,
        "seed": seed,
        "step": step,
        "router_grad_norm": float(grad.detach().float().norm().item()),
        "grad_common_abs_mean": float(common_proj.mean().item()),
        "grad_feature_abs_mean": float(feature_proj.mean().item()),
        "target_loss_for_grad": float(loss.detach().cpu().item()),
    }


def train_one(cfg: dict, variant: str, metric: str, seed: int, out_dir: str, run_stage: str, device_id: int | None) -> None:
    device = torch.device(f"cuda:{device_id}" if device_id is not None and torch.cuda.is_available() else "cpu")
    random.seed(seed)
    torch.manual_seed(seed + 1009)
    root = Path(out_dir)
    run_dir = root / metric / variant / f"seed_{seed}"
    run_dir.mkdir(parents=True, exist_ok=True)
    model = make_model(cfg, metric, device)
    init_meta: dict[str, Any] = {}
    if variant in {"V2_feature_init_trainable", "V4_feature_init_inhibition"}:
        init_meta.update(feature_init_router(model, cfg, seed, device))
    if variant == "V1_random_balanced_init":
        init_meta.update(random_balanced_init(model, cfg, seed, device, int(cfg.get("balanced_init_candidates", 128))))
    if variant == "V3_oracle_frozen":
        for p in model.moe.router.parameters():
            p.requires_grad_(False)
        init_meta["oracle_router"] = "logical route token forced to slot expert; router frozen"
    steps = int(cfg["training"]["smoke_steps"] if run_stage == "smoke" else cfg["training"]["steps"])
    train_samples = int(cfg["data"]["train_samples_per_slot"])
    if run_stage == "smoke":
        train_samples = min(train_samples, 128)
    train_data = generate_varpos_batch(cfg, train_samples, seed, "train")
    batch_size = int(cfg["training"]["batch_size"])
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=float(cfg["training"]["lr"]), weight_decay=float(cfg["training"]["weight_decay"]))
    rng = random.Random(seed + 17)
    indices = list(range(train_data.x.shape[0]))
    eval_steps = sorted({0, 10, 20, 50, 100, 200, 400, 800, steps} if run_stage != "smoke" else {0, max(1, steps // 2), steps})
    metric_rows: list[dict[str, Any]] = []
    route_rows: list[dict[str, Any]] = []
    utility_rows: list[dict[str, Any]] = []
    logit_rows: list[dict[str, Any]] = []
    grad_rows: list[dict[str, Any]] = []
    train_rows: list[dict[str, Any]] = []

    def collect(step: int) -> None:
        out = evaluate(model, cfg, variant, metric, seed, step, device, int(cfg["evaluation"].get("eval_samples_per_slot", 256)))
        metric_rows.append(out["metrics"])
        route_rows.extend(out["route_rows"])
        utility_rows.extend(out["utility_rows"])
        logit_rows.extend(out["logit_rows"])
        grad_rows.append(gradient_diagnostic(model, cfg, variant, metric, seed, step, device))
        print(f"EVAL {metric} {variant} seed={seed} step={step} nmi={out['metrics']['route_slot_nmi']:.3f} max={out['metrics']['max_load']:.3f} acc={out['metrics']['target_accuracy']:.3f}", flush=True)

    collect(0)
    for step in range(1, steps + 1):
        batch_idx = [indices[rng.randrange(len(indices))] for _ in range(batch_size)]
        sub = VarPosBatch(train_data.x[batch_idx], train_data.slot[batch_idx], train_data.target[batch_idx], train_data.route_pos[batch_idx], train_data.target_pos[batch_idx])
        logits, info = forward_variant(model, sub, variant, device, return_acts=True)
        loss = full_ntp_loss(logits, sub.x.to(device))
        tgt = target_loss(logits, sub)
        if variant == "V4_feature_init_inhibition":
            h_route = gather_positions(info["ffn_input"], sub.route_pos)
            exp_route = gather_positions(info["expert_idx"], sub.route_pos)
            log_route = gather_positions(info["router_logits"], sub.route_pos)
            inh, _ = h0605a.true_token_conditioned_inhibition_loss(model, h_route, exp_route, log_route, cfg)
            loss = loss + float(cfg["true_token_inhibition"]["loss_weight"]) * inh
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(cfg["training"]["grad_clip"]))
        opt.step()
        if step == 1 or step % int(cfg["training"]["log_every"]) == 0 or step == steps:
            train_rows.append({"variant": variant, "router_metric": metric, "seed": seed, "step": step, "full_ntp_ce": float(loss.detach().cpu().item()), "target_ce": float(tgt.detach().cpu().item())})
            print(f"TRAIN {metric} {variant} seed={seed} step={step} loss={float(loss.detach().cpu().item()):.4f} target={float(tgt.detach().cpu().item()):.4f}", flush=True)
        if step in eval_steps:
            collect(step)
            model.train()
    write_json(run_dir / "init_meta.json", init_meta)
    write_csv(run_dir / "metrics_by_step.csv", metric_rows)
    write_csv(run_dir / "route_matrix_by_step.csv", route_rows)
    write_csv(run_dir / "utility_matrix_by_step.csv", utility_rows)
    write_csv(run_dir / "logit_decomposition_by_step.csv", logit_rows)
    write_csv(run_dir / "gradient_decomposition_by_step.csv", grad_rows)
    write_csv(run_dir / "training_curve.csv", train_rows)
    torch.save({"model": MODEL_NAME, "variant": variant, "router_metric": metric, "seed": seed, "config": cfg, "model_state": model.state_dict()}, run_dir / "model.pt")


def aggregate_and_plot(out_dir: Path, fig_dir: Path, metrics: list[str], variants: list[str], seeds: list[int]) -> None:
    all_metrics: list[dict[str, Any]] = []
    all_routes: list[dict[str, Any]] = []
    all_utils: list[dict[str, Any]] = []
    all_logits: list[dict[str, Any]] = []
    all_grads: list[dict[str, Any]] = []
    all_train: list[dict[str, Any]] = []
    for metric in metrics:
        for variant in variants:
            for seed in seeds:
                run_dir = out_dir / metric / variant / f"seed_{seed}"
                for name, target in [
                    ("metrics_by_step.csv", all_metrics),
                    ("route_matrix_by_step.csv", all_routes),
                    ("utility_matrix_by_step.csv", all_utils),
                    ("logit_decomposition_by_step.csv", all_logits),
                    ("gradient_decomposition_by_step.csv", all_grads),
                    ("training_curve.csv", all_train),
                ]:
                    for row in read_csv(run_dir / name):
                        target.append(row)
    write_csv(out_dir / "metrics_by_step.csv", all_metrics)
    write_csv(out_dir / "route_matrix_by_step.csv", all_routes)
    write_csv(out_dir / "utility_matrix_by_step.csv", all_utils)
    write_csv(out_dir / "logit_decomposition_by_step.csv", all_logits)
    write_csv(out_dir / "gradient_decomposition_by_step.csv", all_grads)
    write_csv(out_dir / "training_curve.csv", all_train)
    final_rows = []
    max_step: dict[tuple[str, str, str], int] = {}
    for row in all_metrics:
        key = (row["router_metric"], row["variant"], row["seed"])
        max_step[key] = max(max_step.get(key, -1), int(row["step"]))
    for row in all_metrics:
        key = (row["router_metric"], row["variant"], row["seed"])
        if int(row["step"]) == max_step[key]:
            final_rows.append(row)
    write_csv(out_dir / "final_metrics_by_seed.csv", final_rows)
    summary = []
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in final_rows:
        grouped[(row["router_metric"], row["variant"])].append(row)
    for (metric, variant), rows in sorted(grouped.items()):
        out: dict[str, Any] = {"router_metric": metric, "variant": variant, "num_seeds": len(rows)}
        for field in ["route_slot_nmi", "max_load", "load_entropy_norm", "target_accuracy", "target_ce", "probe_slot_from_h", "route_utility_match", "common_ratio"]:
            vals = [float(r[field]) for r in rows]
            out[f"{field}_mean"] = sum(vals) / len(vals) if vals else math.nan
            out[f"{field}_min"] = min(vals) if vals else math.nan
            out[f"{field}_max"] = max(vals) if vals else math.nan
            if len(vals) > 1:
                mean = out[f"{field}_mean"]
                out[f"{field}_std"] = math.sqrt(sum((v - mean) ** 2 for v in vals) / len(vals))
            else:
                out[f"{field}_std"] = 0.0 if vals else math.nan
        summary.append(out)
    write_csv(out_dir / "summary_by_variant.csv", summary)
    plot_outputs(out_dir, fig_dir, metrics, variants, seeds)


def plot_outputs(out_dir: Path, fig_dir: Path, metrics: list[str], variants: list[str], seeds: list[int]) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:
        print(f"plot skipped: {exc}", flush=True)
        return
    fig_dir.mkdir(parents=True, exist_ok=True)
    route_rows = read_csv(out_dir / "route_matrix_by_step.csv")
    metric_rows = read_csv(out_dir / "metrics_by_step.csv")
    utility_rows = read_csv(out_dir / "utility_matrix_by_step.csv")
    metric_by_key = {(r["router_metric"], r["variant"], int(r["seed"]), int(r["step"])): r for r in metric_rows}
    max_step = {}
    for r in metric_rows:
        key = (r["router_metric"], r["variant"], int(r["seed"]))
        max_step[key] = max(max_step.get(key, -1), int(r["step"]))
    by_route: dict[tuple[str, str, int, int], list[dict[str, str]]] = defaultdict(list)
    for r in route_rows:
        by_route[(r["router_metric"], r["variant"], int(r["seed"]), int(r["step"]))].append(r)

    heat_dir = fig_dir / "route_heatmaps"
    heat_dir.mkdir(parents=True, exist_ok=True)
    for metric in metrics:
        for step_name in ["step0", "final"]:
            n_rows = len(variants)
            n_cols = len(seeds)
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(3.2 * n_cols, 2.65 * n_rows), squeeze=False)
            for i, variant in enumerate(variants):
                for j, seed in enumerate(seeds):
                    step = 0 if step_name == "step0" else max_step.get((metric, variant, seed), -1)
                    ax = axes[i][j]
                    rows = by_route.get((metric, variant, seed, step), [])
                    if not rows:
                        ax.axis("off")
                        ax.set_title(f"{variant} s{seed}\\nmissing", fontsize=7)
                        continue
                    mat = torch.zeros(4, 4)
                    for r in rows:
                        mat[int(r["slot"]), int(r["expert"])] = float(r["fraction"])
                    im = ax.imshow(mat.numpy(), cmap="viridis", vmin=0, vmax=1, aspect="auto")
                    mr = metric_by_key[(metric, variant, seed, step)]
                    ax.set_title(f"{variant} s{seed}\\nNMI={float(mr['route_slot_nmi']):.2f} max={float(mr['max_load']):.2f} acc={float(mr['target_accuracy']):.2f}", fontsize=6)
                    ax.set_xticks(range(4))
                    ax.set_yticks(range(4))
                    ax.tick_params(labelsize=6)
                    for a in range(4):
                        for b in range(4):
                            val = float(mat[a, b])
                            ax.text(b, a, f"{val:.2f}", ha="center", va="center", fontsize=5, color="white" if val > 0.45 else "black")
            fig.suptitle(f"{metric} route heatmaps {step_name}", fontsize=12)
            fig.tight_layout(rect=[0, 0, 1, 0.98])
            fig.savefig(heat_dir / f"{metric}_route_heatmaps_{step_name}.png", dpi=180)
            plt.close(fig)

    for metric in metrics:
        rows = [r for r in metric_rows if r["router_metric"] == metric]
        fig, axes = plt.subplots(2, 2, figsize=(11, 7))
        fields = [("max_load", "Max load"), ("route_slot_nmi", "Route-slot NMI"), ("target_accuracy", "Target accuracy"), ("route_utility_match", "Route-utility match")]
        for ax, (field, title) in zip(axes.ravel(), fields):
            for variant in variants:
                vals_by_step: dict[int, list[float]] = defaultdict(list)
                for r in rows:
                    if r["variant"] == variant:
                        vals_by_step[int(r["step"])].append(float(r[field]))
                xs = sorted(vals_by_step)
                ys = [sum(vals_by_step[x]) / len(vals_by_step[x]) for x in xs]
                ax.plot(xs, ys, marker="o", label=variant)
            ax.set_title(title)
            ax.set_xlabel("step")
            ax.grid(alpha=0.25)
        axes[0][0].legend(fontsize=7)
        fig.tight_layout()
        fig.savefig(fig_dir / f"{metric}_trajectory_summary.png", dpi=180)
        plt.close(fig)

    util_dir = fig_dir / "utility_heatmaps"
    util_dir.mkdir(parents=True, exist_ok=True)
    by_util: dict[tuple[str, str, int, int], list[dict[str, str]]] = defaultdict(list)
    for r in utility_rows:
        by_util[(r["router_metric"], r["variant"], int(r["seed"]), int(r["step"]))].append(r)
    for metric in metrics:
        n_rows = len(variants)
        n_cols = len(seeds)
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(3.2 * n_cols, 2.65 * n_rows), squeeze=False)
        for i, variant in enumerate(variants):
            for j, seed in enumerate(seeds):
                step = max_step.get((metric, variant, seed), -1)
                rows = by_util.get((metric, variant, seed, step), [])
                ax = axes[i][j]
                if not rows:
                    ax.axis("off")
                    continue
                mat = torch.zeros(4, 4)
                for r in rows:
                    mat[int(r["slot"]), int(r["expert"])] = float(r["forced_mean_ce"])
                im = ax.imshow(mat.numpy(), cmap="magma", aspect="auto")
                ax.set_title(f"{variant} s{seed}", fontsize=7)
                ax.set_xticks(range(4))
                ax.set_yticks(range(4))
                ax.tick_params(labelsize=6)
            fig.colorbar(im, ax=axes[i].tolist(), fraction=0.015, pad=0.01)
        fig.suptitle(f"{metric} final utility CE heatmaps lower is better", fontsize=12)
        fig.tight_layout(rect=[0, 0, 1, 0.98])
        fig.savefig(util_dir / f"{metric}_utility_heatmaps_final.png", dpi=180)
        plt.close(fig)


def run_task(args: argparse.Namespace) -> None:
    cfg = h0605a.load_json(args.config)
    cfg = json.loads(json.dumps(cfg))
    if args.train_steps:
        cfg["training"]["steps"] = int(args.train_steps)
    if args.smoke_steps:
        cfg["training"]["smoke_steps"] = int(args.smoke_steps)
    if args.train_samples_per_slot:
        cfg["data"]["train_samples_per_slot"] = int(args.train_samples_per_slot)
    if args.eval_samples_per_slot:
        cfg["evaluation"]["eval_samples_per_slot"] = int(args.eval_samples_per_slot)
    else:
        cfg["evaluation"]["eval_samples_per_slot"] = 256
    if args.batch_size:
        cfg["training"]["batch_size"] = int(args.batch_size)
    if args.eval_batch_size:
        cfg["evaluation"]["batch_size"] = int(args.eval_batch_size)
    cfg["balanced_init_candidates"] = int(args.balanced_init_candidates)

    variants = parse_list(args.variants, VARIANTS)
    metrics = parse_list(args.router_metrics, ["cosine"])
    seeds = [int(v) for v in parse_list(args.seeds, [str(v) for v in cfg["seeds"]])]
    if args.run_stage == "smoke":
        seeds = seeds[:1]
    out_dir = Path(args.output_dir).resolve() / "results" / args.run_name
    fig_dir = Path(args.output_dir).resolve() / "figures" / args.run_name
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "resolved_config.json", cfg)
    write_json(out_dir / "run_manifest.json", {
        "experiment": "A05_04_01_no_position_forced_feature_init_trajectory",
        "run_name": args.run_name,
        "position_intervention": "pos_emb.weight zeroed and frozen; logical feature block randomly positioned",
        "variants": variants,
        "router_metrics": metrics,
        "seeds": seeds,
        "run_stage": args.run_stage,
        "result_dir": str(out_dir),
        "figure_dir": str(fig_dir),
    })
    audit_rows = []
    starts = valid_block_starts(cfg)
    for slot in range(int(cfg["data"]["num_slots"])):
        audit_rows.append({"slot": slot, "valid_position_count": len(starts), "positions": ",".join(str(s + int(cfg["data"]["prefix_len"])) for s in starts)})
    write_csv(out_dir / "position_support_audit.csv", audit_rows)
    device_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
    max_parallel = int(args.max_parallel or max(1, device_count))
    jobs = [(metric, variant, seed) for metric in metrics for variant in variants for seed in seeds]
    print(f"RUN_NAME={args.run_name} jobs={len(jobs)} cuda_devices={device_count} max_parallel={max_parallel}", flush=True)
    if args.parallel and len(jobs) > 1 and max_parallel > 1:
        ctx = get_context("spawn")
        active = []
        for idx, (metric, variant, seed) in enumerate(jobs):
            while len(active) >= max_parallel:
                proc, meta = active.pop(0)
                proc.join()
                if proc.exitcode != 0:
                    raise RuntimeError(f"worker failed {meta} exit={proc.exitcode}")
            device_id = idx % max(1, min(device_count, max_parallel)) if device_count else None
            proc = ctx.Process(target=train_one, args=(cfg, variant, metric, seed, str(out_dir), args.run_stage, device_id))
            proc.start()
            active.append((proc, (metric, variant, seed)))
        for proc, meta in active:
            proc.join()
            if proc.exitcode != 0:
                raise RuntimeError(f"worker failed {meta} exit={proc.exitcode}")
    else:
        for idx, (metric, variant, seed) in enumerate(jobs):
            device_id = idx % device_count if device_count else None
            train_one(cfg, variant, metric, seed, str(out_dir), args.run_stage, device_id)
    aggregate_and_plot(out_dir, fig_dir, metrics, variants, seeds)
    write_json(out_dir / "run_summary.json", {"status": "completed", "result_dir": str(out_dir), "figure_dir": str(fig_dir)})
    print(f"completed result_dir={out_dir} figure_dir={fig_dir}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=EXP_DIR)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--run-stage", choices=["smoke", "full"], default="full")
    parser.add_argument("--variants", default="")
    parser.add_argument("--router-metrics", default="cosine")
    parser.add_argument("--seeds", default="")
    parser.add_argument("--parallel", action="store_true")
    parser.add_argument("--max-parallel", type=int, default=0)
    parser.add_argument("--train-steps", type=int, default=0)
    parser.add_argument("--smoke-steps", type=int, default=0)
    parser.add_argument("--train-samples-per-slot", type=int, default=0)
    parser.add_argument("--eval-samples-per-slot", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=0)
    parser.add_argument("--eval-batch-size", type=int, default=0)
    parser.add_argument("--balanced-init-candidates", type=int, default=128)
    args = parser.parse_args()
    run_task(args)


if __name__ == "__main__":
    main()


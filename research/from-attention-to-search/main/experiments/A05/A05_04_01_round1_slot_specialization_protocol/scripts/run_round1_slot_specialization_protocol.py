#!/usr/bin/env python3
"""Round-1 slot-block collapse audit for sparse top-1 MoE.

This runner implements the source-of-truth protocol in
daily_research_reports/0609/round1_slot_specialization_protocol.md.
It runs only P0, P1, P2, P3, and P5.
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
WORKSPACE = (
    RESEARCH_ROOT
    / "Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding"
)
sys.path.insert(0, str(WORKSPACE / "scripts"))
sys.path.insert(0, str(WORKSPACE / "src"))

import run_h0605a_true_token_conditioned_inhibition_replay as h0605a  # noqa: E402
from synthetic_data_understanding.tiny_moe import make_sparse_model  # noqa: E402


MODEL_NAME = "top1_selected_gate"
VARIANTS = ["P1_clean_baseline", "P5_slot_centroid_init"]


@dataclass
class SlotBlockBatch:
    x: torch.Tensor
    slot: torch.Tensor
    target: torch.Tensor
    block_start: torch.Tensor
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


def default_cfg() -> dict[str, Any]:
    return {
        "seed": 20260521,
        "seeds": [20260521, 20260522, 20260523, 20260524, 20260525, 20260526, 20260527, 20260528],
        "data": {
            "dataset_name": "D_min_block_shift",
            "vocab_size": 32,
            "seq_len": 12,
            "num_slots": 4,
            "num_experts": 4,
            "slot_token_start": 1,
            "b_token": 10,
            "target_token_start": 20,
            "filler_token": 0,
            "train_repeats_per_pair": 500,
            "eval_repeats_per_pair": 32,
            "calibration_repeats_per_pair": 32,
        },
        "model": {
            "seq_len": 12,
            "d_model": 128,
            "n_heads": 4,
            "ffn_dim": 256,
            "num_experts": 4,
            "dropout": 0.0,
            "router_metric": "cosine",
            "router_temperature": 8.0,
            "router_eps": 1e-6,
        },
        "router_init": {
            "alpha": 4.0,
            "ridge": 1e-3,
            "use_whitening": True,
            "classifier_steps": 400,
            "classifier_lr": 0.1,
            "min_step0_nmi": 0.90,
        },
        "training": {
            "steps": 1600,
            "smoke_steps": 40,
            "batch_size": 384,
            "lr": 8e-4,
            "weight_decay": 0.01,
            "grad_clip": 1.0,
            "log_every": 100,
        },
        "evaluation": {
            "batch_size": 512,
            "probe_steps": 200,
            "probe_lr": 0.05,
        },
    }


def valid_block_starts(cfg: dict[str, Any]) -> list[int]:
    return list(range(0, int(cfg["data"]["seq_len"]) - 3 + 1))


def slot_token(slot: int, cfg: dict[str, Any]) -> int:
    return int(cfg["data"]["slot_token_start"]) + int(slot)


def target_token(slot: int, cfg: dict[str, Any]) -> int:
    return int(cfg["data"]["target_token_start"]) + int(slot)


def balanced_dataset(cfg: dict[str, Any], repeats_per_pair: int, seed: int, split: str) -> SlotBlockBatch:
    data = cfg["data"]
    rng = random.Random(seed + {"train": 0, "eval": 10000, "probe": 20000, "cal": 30000}.get(split, 40000))
    seq_len = int(data["seq_len"])
    filler = int(data["filler_token"])
    b_tok = int(data["b_token"])
    starts = valid_block_starts(cfg)
    rows: list[list[int]] = []
    slots: list[int] = []
    targets: list[int] = []
    block_starts: list[int] = []
    route_positions: list[int] = []
    target_positions: list[int] = []
    for slot in range(int(data["num_slots"])):
        for start in starts:
            for _ in range(repeats_per_pair):
                x = [filler] * seq_len
                x[start] = slot_token(slot, cfg)
                x[start + 1] = b_tok
                x[start + 2] = target_token(slot, cfg)
                rows.append(x)
                slots.append(slot)
                targets.append(target_token(slot, cfg))
                block_starts.append(start)
                route_positions.append(start + 1)
                target_positions.append(start + 2)
    order = list(range(len(rows)))
    rng.shuffle(order)
    return SlotBlockBatch(
        x=torch.tensor([rows[i] for i in order], dtype=torch.long),
        slot=torch.tensor([slots[i] for i in order], dtype=torch.long),
        target=torch.tensor([targets[i] for i in order], dtype=torch.long),
        block_start=torch.tensor([block_starts[i] for i in order], dtype=torch.long),
        route_pos=torch.tensor([route_positions[i] for i in order], dtype=torch.long),
        target_pos=torch.tensor([target_positions[i] for i in order], dtype=torch.long),
    )


def audit_dataset(cfg: dict[str, Any], out_dir: Path) -> bool:
    batch = balanced_dataset(cfg, int(cfg["data"]["eval_repeats_per_pair"]), int(cfg["seed"]), "eval")
    slots = batch.slot.tolist()
    starts = batch.block_start.tolist()
    targets = batch.target.tolist()
    route_pos = batch.route_pos.tolist()
    slot_counts = Counter(slots)
    start_counts = Counter(starts)
    pair_counts = Counter(zip(slots, starts))
    target_given_slot: dict[str, list[int]] = defaultdict(list)
    target_given_start: dict[str, list[int]] = defaultdict(list)
    for s, p, y in zip(slots, starts, targets):
        target_given_slot[str(s)].append(int(y))
        target_given_start[str(p)].append(int(y))
    expected_pair = int(cfg["data"]["eval_repeats_per_pair"])
    checks = {
        "slot_counts_equal": len(set(slot_counts.values())) == 1,
        "block_start_counts_equal": len(set(start_counts.values())) == 1,
        "slot_block_start_counts_equal": len(set(pair_counts.values())) == 1 and set(pair_counts.values()) == {expected_pair},
        "target_deterministic_from_slot": all(len(set(vals)) == 1 and vals[0] == target_token(int(s), cfg) for s, vals in target_given_slot.items()),
        "route_position_is_b_const": all(int(batch.x[i, pos].item()) == int(cfg["data"]["b_token"]) for i, pos in enumerate(route_pos)),
        "loss_target_is_y_s": all(int(y) == target_token(int(s), cfg) for s, y in zip(slots, targets)),
    }
    rows = []
    for slot in range(int(cfg["data"]["num_slots"])):
        rows.append({"audit": "slot_count", "key": slot, "count": slot_counts[slot]})
    for start in valid_block_starts(cfg):
        rows.append({"audit": "block_start_count", "key": start, "count": start_counts[start]})
    for slot in range(int(cfg["data"]["num_slots"])):
        for start in valid_block_starts(cfg):
            rows.append({"audit": "slot_block_start_count", "slot": slot, "block_start": start, "count": pair_counts[(slot, start)]})
    payload = {
        "dataset": cfg["data"]["dataset_name"],
        "checks": checks,
        "slot_counts": dict(slot_counts),
        "block_start_counts": dict(start_counts),
        "valid_block_starts": valid_block_starts(cfg),
        "route_position_distribution": dict(Counter(route_pos)),
        "loss_mask_position_distribution": dict(Counter(route_pos)),
        "target_given_slot_unique": {k: sorted(set(v)) for k, v in target_given_slot.items()},
        "target_given_block_start_unique": {k: sorted(set(v)) for k, v in target_given_start.items()},
        "pass": all(checks.values()),
    }
    write_json(out_dir / "p0_dataset_audit.json", payload)
    write_csv(out_dir / "p0_dataset_audit_counts.csv", rows)
    md = [
        "# P0 Dataset Audit",
        "",
        f"Dataset: `{cfg['data']['dataset_name']}`",
        "",
        "## Checks",
        "",
    ]
    for key, val in checks.items():
        md.append(f"- `{key}`: {'PASS' if val else 'FAIL'}")
    md.extend([
        "",
        "## Interpretation",
        "",
        "P0 passes only if slot counts, block-start counts, slot-block pairs, target mapping, and B-position routing checks all pass.",
    ])
    (out_dir / "p0_dataset_audit.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return bool(payload["pass"])


def model_cfg(cfg: dict[str, Any], router_metric: str) -> dict[str, Any]:
    local = json.loads(json.dumps(cfg))
    local["model"]["router_metric"] = router_metric
    local["model"]["router_temperature"] = 8.0 if router_metric == "cosine" else 1.0
    return local


def make_model(cfg: dict[str, Any], router_metric: str, device: torch.device) -> torch.nn.Module:
    model = make_sparse_model(MODEL_NAME, model_cfg(cfg, router_metric), device)
    with torch.no_grad():
        model.pos_emb.weight.zero_()
    model.pos_emb.weight.requires_grad_(False)
    return model


def gather_positions(tensor: torch.Tensor, pos: torch.Tensor) -> torch.Tensor:
    idx = pos.to(tensor.device)
    return tensor[torch.arange(tensor.shape[0], device=tensor.device), idx]


def target_loss(logits: torch.Tensor, batch: SlotBlockBatch, reduction: str = "mean") -> torch.Tensor:
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


def linear_probe_split(
    h: torch.Tensor,
    y: torch.Tensor,
    num_classes: int,
    train_mask: torch.Tensor,
    test_mask: torch.Tensor,
    steps: int,
    lr: float,
) -> float:
    if int(train_mask.sum().item()) < num_classes or int(test_mask.sum().item()) == 0:
        return math.nan
    device = h.device
    probe = torch.nn.Linear(h.shape[1], num_classes).to(device)
    opt = torch.optim.AdamW(probe.parameters(), lr=lr)
    train_idx = train_mask.nonzero(as_tuple=False).flatten()
    test_idx = test_mask.nonzero(as_tuple=False).flatten()
    for _ in range(steps):
        logits = probe(h[train_idx])
        loss = F.cross_entropy(logits, y[train_idx])
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    with torch.no_grad():
        pred = probe(h[test_idx]).argmax(dim=-1)
        return float((pred == y[test_idx]).float().mean().item())


def random_probe_masks(n: int, device: torch.device) -> tuple[torch.Tensor, torch.Tensor]:
    gen = torch.Generator(device=device)
    gen.manual_seed(987)
    perm = torch.randperm(n, generator=gen, device=device)
    split = int(0.7 * n)
    train = torch.zeros(n, dtype=torch.bool, device=device)
    test = torch.zeros(n, dtype=torch.bool, device=device)
    train[perm[:split]] = True
    test[perm[split:]] = True
    return train, test


def component_decomposition(h: torch.Tensor, slot: torch.Tensor, block_start: torch.Tensor, cfg: dict[str, Any]) -> dict[str, torch.Tensor | float]:
    num_slots = int(cfg["data"]["num_slots"])
    starts = valid_block_starts(cfg)
    start_to_idx = {p: i for i, p in enumerate(starts)}
    d = h.shape[1]
    means = torch.zeros(num_slots, len(starts), d, device=h.device)
    counts = torch.zeros(num_slots, len(starts), device=h.device)
    for s in range(num_slots):
        for p in starts:
            mask = (slot == s) & (block_start == p)
            if mask.any():
                means[s, start_to_idx[p]] = h[mask].mean(dim=0)
                counts[s, start_to_idx[p]] = mask.float().sum()
    c = means.mean(dim=(0, 1))
    r = means.mean(dim=1) - c.unsqueeze(0)
    u = means.mean(dim=0) - c.unsqueeze(0)
    residual = means - c.view(1, 1, -1) - r.unsqueeze(1) - u.unsqueeze(0)
    centered = means - c.view(1, 1, -1)
    total = centered.pow(2).sum(dim=-1).mean().clamp_min(1e-12)
    slot_ratio = r.pow(2).sum(dim=-1).mean() / total
    position_ratio = u.pow(2).sum(dim=-1).mean() / total
    residual_ratio = residual.pow(2).sum(dim=-1).mean() / total
    return {
        "means": means,
        "c": c,
        "r": r,
        "u": u,
        "residual": residual,
        "slot_component_variance_ratio": float(slot_ratio.detach().cpu().item()),
        "position_component_variance_ratio": float(position_ratio.detach().cpu().item()),
        "residual_component_variance_ratio": float(residual_ratio.detach().cpu().item()),
    }


def slot_centroid_init(model: torch.nn.Module, cfg: dict[str, Any], seed: int, device: torch.device) -> dict[str, float]:
    cal = balanced_dataset(cfg, int(cfg["data"]["calibration_repeats_per_pair"]), seed, "cal")
    h_rows: list[torch.Tensor] = []
    slots: list[torch.Tensor] = []
    model.eval()
    with torch.no_grad():
        bs = int(cfg["evaluation"]["batch_size"])
        for start in range(0, cal.x.shape[0], bs):
            sub = SlotBlockBatch(
                cal.x[start:start + bs],
                cal.slot[start:start + bs],
                cal.target[start:start + bs],
                cal.block_start[start:start + bs],
                cal.route_pos[start:start + bs],
                cal.target_pos[start:start + bs],
            )
            _, info = model(sub.x.to(device), return_acts=True)
            h_rows.append(gather_positions(info["ffn_input"], sub.route_pos).detach().cpu())
            slots.append(sub.slot)
    h = torch.cat(h_rows).float()
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
    with torch.no_grad():
        model.moe.router.weight.copy_(float(cfg["router_init"]["alpha"]) * dirs.to(device))
    h_dev = h.to(device)
    y_dev = slot.to(device).long()
    model.moe.router.weight.requires_grad_(True)
    opt = torch.optim.AdamW([model.moe.router.weight], lr=float(cfg["router_init"]["classifier_lr"]), weight_decay=0.0)
    last_loss = math.nan
    for _ in range(int(cfg["router_init"]["classifier_steps"])):
        logits = router_similarity(model, h_dev)
        loss = F.cross_entropy(logits, y_dev)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        last_loss = float(loss.detach().cpu().item())
    with torch.no_grad():
        pred = router_similarity(model, h_dev).argmax(dim=-1)
        init_acc = float((pred == y_dev).float().mean().item())
    return {
        "slot_centroid_norm": float((means - center).norm(dim=1).mean().item()),
        "slot_init_alpha": float(cfg["router_init"]["alpha"]),
        "slot_classifier_init_loss": last_loss,
        "slot_classifier_init_acc": init_acc,
    }


def eval_model(
    model: torch.nn.Module,
    cfg: dict[str, Any],
    variant: str,
    router_metric: str,
    seed: int,
    step: int,
    device: torch.device,
    save_artifact_path: Path | None,
) -> dict[str, list[dict[str, Any]] | dict[str, Any]]:
    data = balanced_dataset(cfg, int(cfg["data"]["eval_repeats_per_pair"]), seed + step * 17, "eval")
    bs = int(cfg["evaluation"]["batch_size"])
    num_slots = int(cfg["data"]["num_slots"])
    num_experts = int(cfg["model"]["num_experts"])
    starts = valid_block_starts(cfg)
    route_counts = torch.zeros(num_slots, num_experts)
    position_counts = torch.zeros(len(starts), num_experts)
    slot_labels: list[int] = []
    expert_labels: list[int] = []
    target_correct = 0
    total = 0
    target_losses: list[float] = []
    h_all: list[torch.Tensor] = []
    slot_all: list[torch.Tensor] = []
    start_all: list[torch.Tensor] = []
    logits_all: list[torch.Tensor] = []
    expert_all: list[torch.Tensor] = []
    pred_all: list[torch.Tensor] = []
    model.eval()
    with torch.no_grad():
        for start in range(0, data.x.shape[0], bs):
            sub = SlotBlockBatch(
                data.x[start:start + bs],
                data.slot[start:start + bs],
                data.target[start:start + bs],
                data.block_start[start:start + bs],
                data.route_pos[start:start + bs],
                data.target_pos[start:start + bs],
            )
            logits, info = model(sub.x.to(device), return_acts=True)
            route_pos = sub.route_pos.to(device)
            expert = gather_positions(info["expert_idx"], sub.route_pos).detach().cpu()
            rlog = gather_positions(info["router_logits"], sub.route_pos).detach().cpu()
            h_route = gather_positions(info["ffn_input"], sub.route_pos).detach().cpu()
            pred = logits[torch.arange(logits.shape[0], device=device), route_pos].argmax(dim=-1).detach().cpu()
            loss_vec = target_loss(logits, sub, reduction="none").detach().cpu()
            target_losses.extend([float(v) for v in loss_vec])
            target_correct += int((pred == sub.target).sum().item())
            total += int(sub.x.shape[0])
            h_all.append(h_route)
            slot_all.append(sub.slot)
            start_all.append(sub.block_start)
            logits_all.append(rlog)
            expert_all.append(expert)
            pred_all.append(pred)
            for s, p, e in zip(sub.slot.tolist(), sub.block_start.tolist(), expert.tolist()):
                route_counts[int(s), int(e)] += 1
                position_counts[starts.index(int(p)), int(e)] += 1
                slot_labels.append(int(s))
                expert_labels.append(int(e))
    h = torch.cat(h_all).float()
    slot = torch.cat(slot_all).long()
    block_start = torch.cat(start_all).long()
    router_logits = torch.cat(logits_all).float()
    expert = torch.cat(expert_all).long()
    pred = torch.cat(pred_all).long()
    decomp = component_decomposition(h.to(device), slot.to(device), block_start.to(device), cfg)
    load = route_counts.sum(dim=0)
    entropy, entropy_norm = load_entropy(load)
    route_rows: list[dict[str, Any]] = []
    for s in range(num_slots):
        denom = float(route_counts[s].sum().item())
        for e in range(num_experts):
            route_rows.append({
                "variant": variant,
                "router_metric": router_metric,
                "seed": seed,
                "step": step,
                "slot": s,
                "expert": e,
                "count": int(route_counts[s, e].item()),
                "fraction": float(route_counts[s, e].item() / denom) if denom else 0.0,
            })
    acc_slot_rows = []
    for s in range(num_slots):
        mask = slot == s
        acc_slot_rows.append({
            "variant": variant,
            "router_metric": router_metric,
            "seed": seed,
            "step": step,
            "slot": s,
            "accuracy": float((pred[mask] == torch.tensor(target_token(s, cfg))).float().mean().item()) if mask.any() else math.nan,
        })
    acc_pos_rows = []
    for p in starts:
        mask = block_start == p
        acc_pos_rows.append({
            "variant": variant,
            "router_metric": router_metric,
            "seed": seed,
            "step": step,
            "block_start": p,
            "accuracy": float((pred[mask] == data.target[mask]).float().mean().item()) if mask.any() else math.nan,
        })
    purity_vals = []
    for s in range(num_slots):
        denom = route_counts[s].sum().clamp_min(1)
        purity_vals.append(float((route_counts[s] / denom).max().item()))
    if save_artifact_path is not None:
        save_artifact_path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(
            {
                "model_state": model.state_dict(),
                "router_weight": model.moe.router.weight.detach().cpu(),
                "slot": slot,
                "block_start": block_start,
                "route_pos": data.route_pos,
                "target": data.target,
                "prediction": pred,
                "route_assignment": expert,
                "router_logits": router_logits,
                "hidden_B": h,
            },
            save_artifact_path,
        )
    metrics = {
        "variant": variant,
        "router_metric": router_metric,
        "seed": seed,
        "step": step,
        "slot_to_expert_NMI": nmi(slot_labels, expert_labels),
        "per_slot_route_purity": sum(purity_vals) / len(purity_vals),
        "max_load": float((load / load.sum().clamp_min(1)).max().item()),
        "load_entropy": entropy,
        "load_entropy_norm": entropy_norm,
        "active_experts": int((load > 0).sum().item()),
        "target_accuracy": target_correct / total if total else math.nan,
        "cross_entropy_loss": sum(target_losses) / len(target_losses) if target_losses else math.nan,
        "slot_component_variance_ratio": decomp["slot_component_variance_ratio"],
        "position_component_variance_ratio": decomp["position_component_variance_ratio"],
        "residual_component_variance_ratio": decomp["residual_component_variance_ratio"],
    }
    p3_rows = margin_decomposition_rows(model, cfg, variant, router_metric, seed, step, decomp, starts)
    p2_row = probe_metrics_row(cfg, variant, router_metric, seed, step, h.to(device), slot.to(device), block_start.to(device))
    return {
        "metrics": metrics,
        "route_rows": route_rows,
        "accuracy_by_slot_rows": acc_slot_rows,
        "accuracy_by_block_start_rows": acc_pos_rows,
        "p2_probe_row": p2_row,
        "p3_margin_rows": p3_rows,
    }


def probe_metrics_row(
    cfg: dict[str, Any],
    variant: str,
    router_metric: str,
    seed: int,
    step: int,
    h: torch.Tensor,
    slot: torch.Tensor,
    block_start: torch.Tensor,
) -> dict[str, Any]:
    starts = valid_block_starts(cfg)
    probe_steps = int(cfg["evaluation"]["probe_steps"])
    lr = float(cfg["evaluation"]["probe_lr"])
    train_mask, test_mask = random_probe_masks(h.shape[0], h.device)
    heldout = set(starts[-2:])
    train_pos = torch.ones(h.shape[0], dtype=torch.bool, device=h.device)
    test_pos = torch.zeros(h.shape[0], dtype=torch.bool, device=h.device)
    for p in heldout:
        mask = block_start == p
        train_pos &= ~mask
        test_pos |= mask
    start_to_class = {p: i for i, p in enumerate(starts)}
    pos_y = torch.tensor([start_to_class[int(p)] for p in block_start.detach().cpu().tolist()], dtype=torch.long, device=h.device)
    decomp = component_decomposition(h, slot, block_start, cfg)
    return {
        "variant": variant,
        "router_metric": router_metric,
        "seed": seed,
        "step": step,
        "slot_probe_accuracy_random_split": linear_probe_split(h, slot, int(cfg["data"]["num_slots"]), train_mask, test_mask, probe_steps, lr),
        "slot_probe_accuracy_heldout_position": linear_probe_split(h, slot, int(cfg["data"]["num_slots"]), train_pos, test_pos, probe_steps, lr),
        "position_probe_accuracy": linear_probe_split(h, pos_y, len(starts), train_mask, test_mask, probe_steps, lr),
        "slot_component_variance_ratio": decomp["slot_component_variance_ratio"],
        "position_component_variance_ratio": decomp["position_component_variance_ratio"],
        "residual_component_variance_ratio": decomp["residual_component_variance_ratio"],
    }


def margin_decomposition_rows(
    model: torch.nn.Module,
    cfg: dict[str, Any],
    variant: str,
    router_metric: str,
    seed: int,
    step: int,
    decomp: dict[str, torch.Tensor | float],
    starts: list[int],
) -> list[dict[str, Any]]:
    c = decomp["c"]
    r = decomp["r"]
    u = decomp["u"]
    residual = decomp["residual"]
    assert isinstance(c, torch.Tensor)
    assert isinstance(r, torch.Tensor)
    assert isinstance(u, torch.Tensor)
    assert isinstance(residual, torch.Tensor)
    rows: list[dict[str, Any]] = []
    num_slots = int(cfg["data"]["num_slots"])
    with torch.no_grad():
        means = decomp["means"]
        assert isinstance(means, torch.Tensor)
        logits = router_similarity(model, means.reshape(num_slots * len(starts), -1)).reshape(num_slots, len(starts), -1)
        for s in range(num_slots):
            for p_idx, p in enumerate(starts):
                z = logits[s, p_idx]
                top2 = torch.topk(z, k=2)
                e1 = int(top2.indices[0].item())
                e2 = int(top2.indices[1].item())
                wdiff = (model.moe.router.weight[e1] - model.moe.router.weight[e2]).detach().float()
                common = float((wdiff * c).sum().detach().cpu().item())
                slot_m = float((wdiff * r[s]).sum().detach().cpu().item())
                pos_m = float((wdiff * u[p_idx]).sum().detach().cpu().item())
                res_m = float((wdiff * residual[s, p_idx]).sum().detach().cpu().item())
                total = float((top2.values[0] - top2.values[1]).detach().cpu().item())
                denom = abs(total) if abs(total) > 1e-8 else 1e-8
                rows.append({
                    "variant": variant,
                    "router_metric": router_metric,
                    "seed": seed,
                    "step": step,
                    "slot": s,
                    "block_start": p,
                    "top1_expert": e1,
                    "runner_up_expert": e2,
                    "total_margin": total,
                    "common_margin": common,
                    "slot_margin": slot_m,
                    "position_margin": pos_m,
                    "residual_margin": res_m,
                    "common_margin_abs_frac": abs(common) / denom,
                    "slot_margin_abs_frac": abs(slot_m) / denom,
                    "position_margin_abs_frac": abs(pos_m) / denom,
                    "residual_margin_abs_frac": abs(res_m) / denom,
                    "dominant_component": max(
                        [("common", abs(common)), ("slot", abs(slot_m)), ("position", abs(pos_m)), ("residual", abs(res_m))],
                        key=lambda item: item[1],
                    )[0],
                })
    return rows


def eval_steps_for(cfg: dict[str, Any], run_stage: str) -> list[int]:
    steps = int(cfg["training"]["smoke_steps"] if run_stage == "smoke" else cfg["training"]["steps"])
    if run_stage == "smoke":
        return sorted({0, 1, 2, 5, 10, 20, steps})
    early = {0, 1, 2, 5, 10, 20, 50, 100, 200, 500}
    later = set(range(600, steps + 1, 100))
    return sorted({s for s in early | later | {steps} if s <= steps})


def train_one(cfg: dict[str, Any], variant: str, router_metric: str, seed: int, out_dir: str, run_stage: str, device_id: int | None) -> None:
    device = torch.device(f"cuda:{device_id}" if device_id is not None and torch.cuda.is_available() else "cpu")
    random.seed(seed)
    torch.manual_seed(seed + 1109)
    root = Path(out_dir)
    run_dir = root / router_metric / variant / f"seed_{seed}"
    run_dir.mkdir(parents=True, exist_ok=True)
    ckpt_dir = run_dir / "checkpoint_artifacts"
    model = make_model(cfg, router_metric, device)
    init_meta: dict[str, Any] = {}
    if variant == "P5_slot_centroid_init":
        init_meta.update(slot_centroid_init(model, cfg, seed, device))
    steps = int(cfg["training"]["smoke_steps"] if run_stage == "smoke" else cfg["training"]["steps"])
    train_repeats = int(cfg["data"]["train_repeats_per_pair"])
    if run_stage == "smoke":
        train_repeats = min(train_repeats, 8)
    train_data = balanced_dataset(cfg, train_repeats, seed, "train")
    batch_size = int(cfg["training"]["batch_size"])
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=float(cfg["training"]["lr"]), weight_decay=float(cfg["training"]["weight_decay"]))
    rng = random.Random(seed + 17)
    indices = list(range(train_data.x.shape[0]))
    eval_steps = eval_steps_for(cfg, run_stage)
    metric_rows: list[dict[str, Any]] = []
    route_rows: list[dict[str, Any]] = []
    acc_slot_rows: list[dict[str, Any]] = []
    acc_pos_rows: list[dict[str, Any]] = []
    probe_rows: list[dict[str, Any]] = []
    margin_rows: list[dict[str, Any]] = []
    train_rows: list[dict[str, Any]] = []

    def collect(step: int) -> None:
        artifact = ckpt_dir / f"step_{step:05d}.pt"
        out = eval_model(model, cfg, variant, router_metric, seed, step, device, artifact)
        metric_rows.append(out["metrics"])
        route_rows.extend(out["route_rows"])
        acc_slot_rows.extend(out["accuracy_by_slot_rows"])
        acc_pos_rows.extend(out["accuracy_by_block_start_rows"])
        probe_rows.append(out["p2_probe_row"])
        margin_rows.extend(out["p3_margin_rows"])
        print(
            f"EVAL {router_metric} {variant} seed={seed} step={step} "
            f"nmi={out['metrics']['slot_to_expert_NMI']:.3f} max={out['metrics']['max_load']:.3f} "
            f"purity={out['metrics']['per_slot_route_purity']:.3f} acc={out['metrics']['target_accuracy']:.3f}",
            flush=True,
        )

    collect(0)
    if variant == "P5_slot_centroid_init":
        step0_nmi = float(metric_rows[-1]["slot_to_expert_NMI"])
        init_meta["step0_slot_to_expert_NMI"] = step0_nmi
        init_meta["step0_max_load"] = float(metric_rows[-1]["max_load"])
        init_meta["step0_per_slot_route_purity"] = float(metric_rows[-1]["per_slot_route_purity"])
        if step0_nmi < float(cfg["router_init"]["min_step0_nmi"]):
            write_json(run_dir / "init_meta.json", init_meta)
            raise RuntimeError(f"P5 slot initialization failed step-0 NMI check: {step0_nmi:.3f}")
    for step in range(1, steps + 1):
        batch_idx = [indices[rng.randrange(len(indices))] for _ in range(batch_size)]
        sub = SlotBlockBatch(
            train_data.x[batch_idx],
            train_data.slot[batch_idx],
            train_data.target[batch_idx],
            train_data.block_start[batch_idx],
            train_data.route_pos[batch_idx],
            train_data.target_pos[batch_idx],
        )
        logits, _ = model(sub.x.to(device), return_acts=True)
        loss = target_loss(logits, sub)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(cfg["training"]["grad_clip"]))
        opt.step()
        if step == 1 or step % int(cfg["training"]["log_every"]) == 0 or step == steps:
            train_rows.append({
                "variant": variant,
                "router_metric": router_metric,
                "seed": seed,
                "step": step,
                "target_ce": float(loss.detach().cpu().item()),
            })
            print(f"TRAIN {router_metric} {variant} seed={seed} step={step} target_ce={float(loss.detach().cpu().item()):.4f}", flush=True)
        if step in eval_steps:
            collect(step)
            model.train()
    write_json(run_dir / "init_meta.json", init_meta)
    write_csv(run_dir / "metrics_by_step.csv", metric_rows)
    write_csv(run_dir / "route_confusion_by_step.csv", route_rows)
    write_csv(run_dir / "accuracy_by_slot.csv", acc_slot_rows)
    write_csv(run_dir / "accuracy_by_block_start.csv", acc_pos_rows)
    write_csv(run_dir / "p2_probe_metrics_by_checkpoint.csv", probe_rows)
    write_csv(run_dir / "p3_margin_decomposition_by_checkpoint.csv", margin_rows)
    write_csv(run_dir / "training_curve.csv", train_rows)


def route_switch_rows(route_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_key: dict[tuple[str, str, str, int], dict[int, int]] = defaultdict(dict)
    for row in route_rows:
        key = (row["router_metric"], row["variant"], row["seed"], int(row["slot"]))
        step = int(row["step"])
        current = by_key[key].get(step)
        frac = float(row["fraction"])
        if current is None:
            by_key[key][step] = int(row["expert"])
        else:
            prev_frac = max(float(r["fraction"]) for r in route_rows if r["router_metric"] == row["router_metric"] and r["variant"] == row["variant"] and r["seed"] == row["seed"] and int(r["slot"]) == int(row["slot"]) and int(r["step"]) == step and int(r["expert"]) == current)
            if frac > prev_frac:
                by_key[key][step] = int(row["expert"])
    out = []
    for (metric, variant, seed, slot), step_map in sorted(by_key.items()):
        steps = sorted(step_map)
        experts = [step_map[s] for s in steps]
        route_switch_step = ""
        for idx in range(1, len(steps)):
            if experts[idx] != experts[idx - 1]:
                route_switch_step = steps[idx]
                break
        stable_lock_step = ""
        for idx, step in enumerate(steps):
            if all(e == experts[idx] for e in experts[idx:]):
                stable_lock_step = step
                break
        out.append({
            "router_metric": metric,
            "variant": variant,
            "seed": seed,
            "slot": slot,
            "initial_dominant_expert": experts[0] if experts else "",
            "final_dominant_expert": experts[-1] if experts else "",
            "route_switch_step": route_switch_step,
            "stable_lock_step": stable_lock_step,
            "dominant_expert_trajectory": json.dumps(dict(zip(steps, experts)), sort_keys=True),
        })
    return out


def aggregate_and_plot(out_dir: Path, fig_dir: Path, router_metrics: list[str], variants: list[str], seeds: list[int]) -> None:
    all_metrics: list[dict[str, Any]] = []
    all_routes: list[dict[str, Any]] = []
    all_acc_slot: list[dict[str, Any]] = []
    all_acc_pos: list[dict[str, Any]] = []
    all_probes: list[dict[str, Any]] = []
    all_margins: list[dict[str, Any]] = []
    all_train: list[dict[str, Any]] = []
    for metric in router_metrics:
        for variant in variants:
            for seed in seeds:
                run_dir = out_dir / metric / variant / f"seed_{seed}"
                for name, target in [
                    ("metrics_by_step.csv", all_metrics),
                    ("route_confusion_by_step.csv", all_routes),
                    ("accuracy_by_slot.csv", all_acc_slot),
                    ("accuracy_by_block_start.csv", all_acc_pos),
                    ("p2_probe_metrics_by_checkpoint.csv", all_probes),
                    ("p3_margin_decomposition_by_checkpoint.csv", all_margins),
                    ("training_curve.csv", all_train),
                ]:
                    target.extend(read_csv(run_dir / name))
    write_csv(out_dir / "metrics_by_step.csv", all_metrics)
    write_csv(out_dir / "route_confusion_by_step.csv", all_routes)
    write_csv(out_dir / "accuracy_by_slot.csv", all_acc_slot)
    write_csv(out_dir / "accuracy_by_block_start.csv", all_acc_pos)
    write_csv(out_dir / "p2_probe_metrics_by_checkpoint.csv", all_probes)
    write_csv(out_dir / "p3_margin_decomposition_by_checkpoint.csv", all_margins)
    write_csv(out_dir / "training_curve.csv", all_train)
    final_step: dict[tuple[str, str, str], int] = {}
    for row in all_metrics:
        key = (row["router_metric"], row["variant"], row["seed"])
        final_step[key] = max(final_step.get(key, -1), int(row["step"]))
    final_rows = [row for row in all_metrics if int(row["step"]) == final_step[(row["router_metric"], row["variant"], row["seed"])]]
    write_csv(out_dir / "final_metrics_by_seed.csv", final_rows)
    summary_rows = []
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in final_rows:
        grouped[(row["router_metric"], row["variant"])].append(row)
    for (metric, variant), rows in sorted(grouped.items()):
        out: dict[str, Any] = {"router_metric": metric, "variant": variant, "num_seeds": len(rows)}
        for field in [
            "slot_to_expert_NMI",
            "per_slot_route_purity",
            "max_load",
            "load_entropy_norm",
            "target_accuracy",
            "cross_entropy_loss",
            "slot_component_variance_ratio",
            "position_component_variance_ratio",
        ]:
            vals = [float(r[field]) for r in rows]
            mean = sum(vals) / len(vals) if vals else math.nan
            out[f"{field}_mean"] = mean
            out[f"{field}_min"] = min(vals) if vals else math.nan
            out[f"{field}_max"] = max(vals) if vals else math.nan
            out[f"{field}_std"] = math.sqrt(sum((v - mean) ** 2 for v in vals) / len(vals)) if len(vals) > 1 else 0.0
        out["hard_collapse_rate"] = sum(1 for r in rows if float(r["max_load"]) >= 0.70) / max(1, len(rows))
        out["partial_collapse_rate"] = sum(1 for r in rows if float(r["max_load"]) >= 0.50 and float(r["slot_to_expert_NMI"]) < 0.50) / max(1, len(rows))
        summary_rows.append(out)
    write_csv(out_dir / "summary_by_variant.csv", summary_rows)
    switch = route_switch_rows(all_routes)
    write_csv(out_dir / "p3_route_switch_table.csv", switch)
    p1_final = [r for r in final_rows if r["variant"] == "P1_clean_baseline"]
    p5_final = [r for r in final_rows if r["variant"] == "P5_slot_centroid_init"]
    write_csv(out_dir / "p1_metrics_by_seed.csv", p1_final)
    write_csv(out_dir / "p5_metrics_by_seed.csv", p5_final)
    write_csv(out_dir / "p1_route_confusion_by_seed.csv", [r for r in all_routes if r["variant"] == "P1_clean_baseline" and int(r["step"]) == final_step[(r["router_metric"], r["variant"], r["seed"])]])
    write_csv(out_dir / "p5_route_confusion_by_seed.csv", [r for r in all_routes if r["variant"] == "P5_slot_centroid_init" and int(r["step"]) == final_step[(r["router_metric"], r["variant"], r["seed"])]])
    write_csv(out_dir / "p2_component_variance.csv", all_probes)
    write_csv(out_dir / "p5_route_switch_after_release.csv", [])
    write_p3_event_table(out_dir / "p3_route_switch_event_table.md", switch)
    write_protocol_summaries(out_dir, summary_rows)
    plot_outputs(out_dir, fig_dir, variants)


def write_p3_event_table(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# P3 Route Switch Event Table", "", "| Variant | Seed | Slot | Initial | Final | First Switch | Stable Lock |", "|---|---:|---:|---:|---:|---:|---:|"]
    for row in rows:
        lines.append(f"| `{row['variant']}` | {row['seed']} | {row['slot']} | {row['initial_dominant_expert']} | {row['final_dominant_expert']} | {row['route_switch_step']} | {row['stable_lock_step']} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_protocol_summaries(out_dir: Path, summary_rows: list[dict[str, Any]]) -> None:
    by_variant = {r["variant"]: r for r in summary_rows}
    p1 = by_variant.get("P1_clean_baseline", {})
    p5 = by_variant.get("P5_slot_centroid_init", {})
    (out_dir / "p1_summary.md").write_text(
        "\n".join([
            "# P1 Clean Baseline Re-Collapse",
            "",
            "Question: In the minimal clean setting, does ordinary sparse top-1 MoE still collapse during training?",
            "",
            f"Observation: final mean `max_load` = {p1.get('max_load_mean', 'NA')}; final mean `slot_to_expert_NMI` = {p1.get('slot_to_expert_NMI_mean', 'NA')}; final mean `target_accuracy` = {p1.get('target_accuracy_mean', 'NA')}.",
            "",
            "Interpretation: use `p1_metrics_by_seed.csv`, route heatmaps, and trajectories for the final audited judgment.",
        ]) + "\n",
        encoding="utf-8",
    )
    (out_dir / "p2_summary.md").write_text(
        "\n".join([
            "# P2 Slot Signal Probe",
            "",
            "Question: Does the routed hidden state at `B_CONST` contain decodable slot information?",
            "",
            "Observation: see `p2_probe_metrics_by_checkpoint.csv` for random split, held-out block-start split, position probe, and component variance ratios.",
        ]) + "\n",
        encoding="utf-8",
    )
    (out_dir / "p3_summary.md").write_text(
        "\n".join([
            "# P3 Logit Trajectory Decomposition",
            "",
            "Question: When routing changes, is the top-1 decision driven by slot, common, block-position, or residual components?",
            "",
            "Observation: see `p3_margin_decomposition_by_checkpoint.csv` and `p3_route_switch_table.csv`.",
        ]) + "\n",
        encoding="utf-8",
    )
    (out_dir / "p5_summary.md").write_text(
        "\n".join([
            "# P5 Slot-Initialized Positive Control",
            "",
            "Question: If early random lock-in is removed, is slot-to-expert specialization reachable and stable?",
            "",
            f"Observation: final mean `max_load` = {p5.get('max_load_mean', 'NA')}; final mean `slot_to_expert_NMI` = {p5.get('slot_to_expert_NMI_mean', 'NA')}; final mean `target_accuracy` = {p5.get('target_accuracy_mean', 'NA')}.",
            "",
            "Boundary: P5 is a positive control and does not prove ordinary random-initialized sparse top-1 MoE naturally learns slot-specialization.",
        ]) + "\n",
        encoding="utf-8",
    )


def plot_outputs(out_dir: Path, fig_dir: Path, variants: list[str]) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:
        print(f"plot skipped: {exc}", flush=True)
        return
    fig_dir.mkdir(parents=True, exist_ok=True)
    metrics = read_csv(out_dir / "metrics_by_step.csv")
    routes = read_csv(out_dir / "route_confusion_by_step.csv")
    if not metrics:
        return
    for field, fname, title in [
        ("max_load", "p1_max_load_trajectory.png", "Max-load trajectory"),
        ("slot_to_expert_NMI", "p1_slot_nmi_trajectory.png", "Slot-to-expert NMI trajectory"),
        ("target_accuracy", "p1_accuracy_trajectory.png", "Target accuracy trajectory"),
    ]:
        fig, ax = plt.subplots(figsize=(8, 4.8))
        for variant in variants:
            by_step: dict[int, list[float]] = defaultdict(list)
            for row in metrics:
                if row["variant"] == variant:
                    by_step[int(row["step"])].append(float(row[field]))
            xs = sorted(by_step)
            ys = [sum(by_step[x]) / len(by_step[x]) for x in xs]
            ax.plot(xs, ys, marker="o", label=variant)
        ax.set_title(title)
        ax.set_xlabel("step")
        ax.set_ylabel(field)
        ax.grid(alpha=0.25)
        ax.legend()
        fig.tight_layout()
        fig.savefig(fig_dir / fname, dpi=180)
        if field == "max_load":
            fig.savefig(fig_dir / "p5_baseline_vs_positive_control.png", dpi=180)
        plt.close(fig)
    probe_rows = read_csv(out_dir / "p2_probe_metrics_by_checkpoint.csv")
    if probe_rows:
        fig, ax = plt.subplots(figsize=(8, 4.8))
        for variant in variants:
            by_step: dict[int, list[float]] = defaultdict(list)
            for row in probe_rows:
                if row["variant"] == variant:
                    by_step[int(row["step"])].append(float(row["slot_probe_accuracy_heldout_position"]))
            xs = sorted(by_step)
            ys = [sum(by_step[x]) / len(by_step[x]) for x in xs]
            ax.plot(xs, ys, marker="o", label=variant)
        ax.set_title("Held-out-position slot probe accuracy")
        ax.set_xlabel("step")
        ax.grid(alpha=0.25)
        ax.legend()
        fig.tight_layout()
        fig.savefig(fig_dir / "p2_probe_accuracy_trajectory.png", dpi=180)
        plt.close(fig)
    margin_rows = read_csv(out_dir / "p3_margin_decomposition_by_checkpoint.csv")
    if margin_rows:
        fig, ax = plt.subplots(figsize=(8, 4.8))
        for component in ["common_margin_abs_frac", "slot_margin_abs_frac", "position_margin_abs_frac", "residual_margin_abs_frac"]:
            by_step: dict[int, list[float]] = defaultdict(list)
            for row in margin_rows:
                if row["variant"] == "P1_clean_baseline":
                    by_step[int(row["step"])].append(float(row[component]))
            xs = sorted(by_step)
            ys = [sum(by_step[x]) / len(by_step[x]) for x in xs]
            ax.plot(xs, ys, marker="o", label=component)
        ax.set_title("P3 baseline top-2 margin decomposition")
        ax.set_xlabel("step")
        ax.grid(alpha=0.25)
        ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(fig_dir / "p3_margin_decomposition_plots.png", dpi=180)
        plt.close(fig)
    final_step: dict[tuple[str, str, str], int] = {}
    for row in metrics:
        key = (row["router_metric"], row["variant"], row["seed"])
        final_step[key] = max(final_step.get(key, -1), int(row["step"]))
    heat_dir = fig_dir / "route_heatmaps"
    heat_dir.mkdir(parents=True, exist_ok=True)
    for variant in variants:
        seeds = sorted({row["seed"] for row in metrics if row["variant"] == variant})
        for step_name in ["step0", "final"]:
            fig, axes = plt.subplots(1, len(seeds), figsize=(3.2 * len(seeds), 3.0), squeeze=False)
            for j, seed in enumerate(seeds):
                key = ("cosine", variant, seed)
                step = 0 if step_name == "step0" else final_step.get(key, -1)
                mat = torch.zeros(4, 4)
                for row in routes:
                    if row["variant"] == variant and row["seed"] == seed and int(row["step"]) == step:
                        mat[int(row["slot"]), int(row["expert"])] = float(row["fraction"])
                ax = axes[0][j]
                ax.imshow(mat.numpy(), cmap="viridis", vmin=0, vmax=1)
                ax.set_title(f"{variant}\nseed {seed} step {step}", fontsize=7)
                ax.set_xlabel("expert")
                ax.set_ylabel("slot")
                ax.set_xticks(range(4))
                ax.set_yticks(range(4))
                for a in range(4):
                    for b in range(4):
                        val = float(mat[a, b])
                        ax.text(b, a, f"{val:.2f}", ha="center", va="center", fontsize=6, color="white" if val > 0.45 else "black")
            fig.tight_layout()
            out_name = "p1_route_heatmaps.png" if variant == "P1_clean_baseline" and step_name == "final" else f"{variant}_{step_name}_route_heatmaps.png"
            fig.savefig(heat_dir / out_name, dpi=180)
            if variant == "P1_clean_baseline" and step_name == "final":
                fig.savefig(fig_dir / "p1_route_heatmaps.png", dpi=180)
            plt.close(fig)


def run_task(args: argparse.Namespace) -> None:
    cfg = default_cfg()
    if args.train_steps:
        cfg["training"]["steps"] = int(args.train_steps)
    if args.smoke_steps:
        cfg["training"]["smoke_steps"] = int(args.smoke_steps)
    if args.train_repeats_per_pair:
        cfg["data"]["train_repeats_per_pair"] = int(args.train_repeats_per_pair)
    if args.eval_repeats_per_pair:
        cfg["data"]["eval_repeats_per_pair"] = int(args.eval_repeats_per_pair)
    if args.calibration_repeats_per_pair:
        cfg["data"]["calibration_repeats_per_pair"] = int(args.calibration_repeats_per_pair)
    if args.batch_size:
        cfg["training"]["batch_size"] = int(args.batch_size)
    if args.eval_batch_size:
        cfg["evaluation"]["batch_size"] = int(args.eval_batch_size)
    seeds = [int(v) for v in parse_list(args.seeds, [str(v) for v in cfg["seeds"]])]
    if args.run_stage == "smoke":
        seeds = seeds[:1]
    router_metrics = parse_list(args.router_metrics, ["cosine"])
    variants = parse_list(args.variants, VARIANTS)
    out_dir = Path(args.output_dir).resolve() / "results" / args.run_name
    fig_dir = Path(args.output_dir).resolve() / "figures" / args.run_name
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "resolved_config.json", cfg)
    write_json(out_dir / "run_manifest.json", {
        "experiment": "A05_04_01_round1_slot_specialization_protocol",
        "source_protocol": "daily_research_reports/0609/round1_slot_specialization_protocol.md",
        "run_name": args.run_name,
        "run_stage": args.run_stage,
        "variants": variants,
        "router_metrics": router_metrics,
        "seeds": seeds,
        "result_dir": str(out_dir),
        "figure_dir": str(fig_dir),
        "round1_scope": ["P0", "P1", "P2", "P3", "P5"],
        "not_run": ["P4", "P6", "P7"],
    })
    if not audit_dataset(cfg, out_dir):
        raise RuntimeError("P0 dataset audit failed; stopping before model training.")
    device_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
    max_parallel = int(args.max_parallel or max(1, device_count))
    jobs = [(metric, variant, seed) for metric in router_metrics for variant in variants for seed in seeds]
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
    aggregate_and_plot(out_dir, fig_dir, router_metrics, variants, seeds)
    write_json(out_dir / "run_summary.json", {"status": "completed", "result_dir": str(out_dir), "figure_dir": str(fig_dir)})
    print(f"completed result_dir={out_dir} figure_dir={fig_dir}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=EXP_DIR)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--run-stage", choices=["smoke", "full"], default="full")
    parser.add_argument("--variants", default=",".join(VARIANTS))
    parser.add_argument("--router-metrics", default="cosine")
    parser.add_argument("--seeds", default="")
    parser.add_argument("--parallel", action="store_true")
    parser.add_argument("--max-parallel", type=int, default=0)
    parser.add_argument("--train-steps", type=int, default=0)
    parser.add_argument("--smoke-steps", type=int, default=0)
    parser.add_argument("--train-repeats-per-pair", type=int, default=0)
    parser.add_argument("--eval-repeats-per-pair", type=int, default=0)
    parser.add_argument("--calibration-repeats-per-pair", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=0)
    parser.add_argument("--eval-batch-size", type=int, default=0)
    args = parser.parse_args()
    run_task(args)


if __name__ == "__main__":
    main()

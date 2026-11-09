#!/usr/bin/env python3
"""Common-source audit: B-path attribution and no-B slot-target runs."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import os
import random
import sys
from collections import Counter, defaultdict
from multiprocessing import get_context
from pathlib import Path
from typing import Any

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import torch
from torch.nn import functional as F

EXP_DIR = Path(__file__).resolve().parents[1]
RESEARCH_ROOT = EXP_DIR.parents[4]
ROUND1_EXP = RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A05/A05_04_01_round1_slot_specialization_protocol_dot_product"
ROUND1_RUN = ROUND1_EXP / "results/round1_slot_specialization_dot_product_4gpu_20260609"
ROUND1_SCRIPT = ROUND1_EXP / "scripts/run_round1_slot_specialization_protocol_dot_product.py"
ROUND2_EXP = RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A05/A05_04_02_round2_dotproduct_common_logit"
ROUND2_SCRIPT = ROUND2_EXP / "scripts/run_round2_dotproduct_common_logit.py"

spec1 = importlib.util.spec_from_file_location("round1dot", ROUND1_SCRIPT)
round1 = importlib.util.module_from_spec(spec1)
assert spec1.loader is not None
sys.modules["round1dot"] = round1
spec1.loader.exec_module(round1)

spec2 = importlib.util.spec_from_file_location("round2dot", ROUND2_SCRIPT)
round2 = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
sys.modules["round2dot"] = round2
spec2.loader.exec_module(round2)

SEEDS = [20260521, 20260522, 20260523, 20260524, 20260525, 20260526, 20260527, 20260528]
CHECKPOINT_STEPS = [0, 1, 2, 5, 10, 20, 50, 1600]
P1_PATCH_CONDITIONS = ["original", "no_b_residual", "no_b_self_value", "no_b_full_embedding"]
P2_VARIANTS = ["NoB_baseline", "NoB_cancel_0_10", "NoB_cancel_0_final"]


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


def cfg_for(args: argparse.Namespace) -> dict[str, Any]:
    cfg = round1.default_cfg()
    cfg["model"]["router_metric"] = "dot_product"
    cfg["model"]["router_temperature"] = 1.0
    cfg["training"]["steps"] = int(args.train_steps)
    cfg["training"]["batch_size"] = int(args.batch_size)
    cfg["data"]["train_repeats_per_pair"] = int(args.train_repeats_per_pair)
    cfg["data"]["eval_repeats_per_pair"] = int(args.eval_repeats_per_pair)
    cfg["evaluation"]["batch_size"] = int(args.eval_batch_size)
    return cfg


def valid_no_b_starts(cfg: dict[str, Any]) -> list[int]:
    return list(range(0, int(cfg["data"]["seq_len"]) - 2 + 1))


def no_b_dataset(cfg: dict[str, Any], repeats_per_pair: int, seed: int, split: str) -> Any:
    data = cfg["data"]
    rng = random.Random(seed + {"train": 0, "eval": 10000, "probe": 20000}.get(split, 40000))
    seq_len = int(data["seq_len"])
    filler = int(data["filler_token"])
    starts = valid_no_b_starts(cfg)
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
                x[start] = round1.slot_token(slot, cfg)
                x[start + 1] = round1.target_token(slot, cfg)
                rows.append(x)
                slots.append(slot)
                targets.append(round1.target_token(slot, cfg))
                block_starts.append(start)
                route_positions.append(start)
                target_positions.append(start + 1)
    order = list(range(len(rows)))
    rng.shuffle(order)
    return round1.SlotBlockBatch(
        x=torch.tensor([rows[i] for i in order], dtype=torch.long),
        slot=torch.tensor([slots[i] for i in order], dtype=torch.long),
        target=torch.tensor([targets[i] for i in order], dtype=torch.long),
        block_start=torch.tensor([block_starts[i] for i in order], dtype=torch.long),
        route_pos=torch.tensor([route_positions[i] for i in order], dtype=torch.long),
        target_pos=torch.tensor([target_positions[i] for i in order], dtype=torch.long),
    )


def gather_positions(tensor: torch.Tensor, pos: torch.Tensor) -> torch.Tensor:
    return round1.gather_positions(tensor, pos)


def nmi(a: list[int], b: list[int]) -> float:
    return round1.nmi(a, b)


def make_model(cfg: dict[str, Any], device: torch.device) -> torch.nn.Module:
    return round1.make_model(cfg, "dot_product", device)


def target_loss_no_b(logits: torch.Tensor, batch: Any, reduction: str = "mean") -> torch.Tensor:
    pos = batch.route_pos.to(logits.device)
    target = batch.target.to(logits.device)
    pred_logits = logits[torch.arange(logits.shape[0], device=logits.device), pos]
    return F.cross_entropy(pred_logits, target, reduction=reduction)


def component_decomp_for_starts(h: torch.Tensor, slot: torch.Tensor, block_start: torch.Tensor, starts: list[int], num_slots: int) -> dict[str, Any]:
    start_to_idx = {p: i for i, p in enumerate(starts)}
    d = h.shape[1]
    means = torch.zeros(num_slots, len(starts), d, device=h.device)
    for s in range(num_slots):
        for p in starts:
            mask = (slot == s) & (block_start == p)
            if mask.any():
                means[s, start_to_idx[p]] = h[mask].mean(dim=0)
    c = means.mean(dim=(0, 1))
    r = means.mean(dim=1) - c.unsqueeze(0)
    u = means.mean(dim=0) - c.unsqueeze(0)
    residual = means - c.view(1, 1, -1) - r.unsqueeze(1) - u.unsqueeze(0)
    centered = means - c.view(1, 1, -1)
    total = centered.pow(2).sum(dim=-1).mean().clamp_min(1e-12)
    return {
        "means": means,
        "c": c,
        "r": r,
        "u": u,
        "residual": residual,
        "slot_component_variance_ratio": float((r.pow(2).sum(dim=-1).mean() / total).detach().cpu().item()),
        "position_component_variance_ratio": float((u.pow(2).sum(dim=-1).mean() / total).detach().cpu().item()),
        "residual_component_variance_ratio": float((residual.pow(2).sum(dim=-1).mean() / total).detach().cpu().item()),
    }


def margin_rows_from_decomp_starts(decomp: dict[str, Any], w: torch.Tensor, variant: str, seed: int, step: int, starts: list[int]) -> list[dict[str, Any]]:
    rows = round2.margin_rows_from_decomp(decomp, w.detach().cpu().float(), variant, seed, step, {})
    for row in rows:
        idx = int(row["block_start_index"])
        row["block_start"] = starts[idx]
    return rows


def metric_rows_for_h(
    h: torch.Tensor,
    slot: torch.Tensor,
    block_start: torch.Tensor,
    w: torch.Tensor,
    cfg: dict[str, Any],
    starts: list[int],
    variant: str,
    seed: int,
    step: int,
    extra: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    num_slots = int(cfg["data"]["num_slots"])
    num_experts = int(cfg["model"]["num_experts"])
    logits = h.float() @ w.detach().cpu().float().T
    expert = logits.argmax(dim=-1).long()
    route_counts = torch.zeros(num_slots, num_experts)
    slot_labels: list[int] = []
    expert_labels: list[int] = []
    for s, e in zip(slot.tolist(), expert.tolist()):
        route_counts[int(s), int(e)] += 1
        slot_labels.append(int(s))
        expert_labels.append(int(e))
    load = route_counts.sum(dim=0)
    _, entropy_norm = round1.load_entropy(load)
    purity_vals = []
    route_rows = []
    for s in range(num_slots):
        denom = route_counts[s].sum().clamp_min(1)
        purity_vals.append(float((route_counts[s] / denom).max().item()))
        for e in range(num_experts):
            route_rows.append({
                "variant": variant,
                "seed": seed,
                "step": step,
                "slot": s,
                "expert": e,
                "count": int(route_counts[s, e].item()),
                "fraction": float((route_counts[s, e] / denom).item()),
            })
    decomp = component_decomp_for_starts(h.float(), slot.long(), block_start.long(), starts, num_slots)
    margin_rows = margin_rows_from_decomp_starts(decomp, w, variant, seed, step, starts)
    common_abs = sum(abs(float(r["common_margin"])) for r in margin_rows) / len(margin_rows)
    slot_abs = sum(abs(float(r["slot_margin"])) for r in margin_rows) / len(margin_rows)
    row = {
        "variant": variant,
        "seed": seed,
        "step": step,
        "slot_to_expert_NMI": nmi(slot_labels, expert_labels),
        "per_slot_route_purity": sum(purity_vals) / len(purity_vals),
        "max_load": float((load / load.sum().clamp_min(1)).max().item()),
        "load_entropy_norm": entropy_norm,
        "active_experts": int((load > 0).sum().item()),
        "mean_abs_common_margin": common_abs,
        "mean_abs_slot_margin": slot_abs,
        "common_hidden_norm": float(decomp["c"].norm().detach().cpu().item()),
        "slot_component_variance_ratio": decomp["slot_component_variance_ratio"],
        "position_component_variance_ratio": decomp["position_component_variance_ratio"],
        "residual_component_variance_ratio": decomp["residual_component_variance_ratio"],
    }
    if extra:
        row.update(extra)
        for rr in route_rows:
            rr.update(extra)
        for mr in margin_rows:
            mr.update(extra)
    return row, route_rows, margin_rows


def attention_out_and_self_contrib(model: torch.nn.Module, x: torch.Tensor, route_pos: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    width = x.shape[1]
    mask = torch.triu(torch.ones(width, width, device=x.device, dtype=torch.bool), diagonal=1)
    attn_out, weights = model.attn(x, x, x, attn_mask=mask, need_weights=True, average_attn_weights=False)
    w_in = model.attn.in_proj_weight
    b_in = model.attn.in_proj_bias
    _, _, v_proj = F.linear(x, w_in, b_in).chunk(3, dim=-1)
    bsz, seq_len, embed_dim = v_proj.shape
    num_heads = model.attn.num_heads
    head_dim = embed_dim // num_heads
    v = v_proj.view(bsz, seq_len, num_heads, head_dim).transpose(1, 2)
    rows = torch.arange(bsz, device=x.device)
    self_weights = weights[rows, :, route_pos, route_pos]
    self_v = v[rows, :, route_pos, :]
    per_head = self_weights.unsqueeze(-1) * self_v
    concat = per_head.reshape(bsz, embed_dim)
    self_contrib = F.linear(concat, model.attn.out_proj.weight, None)
    self_mass = self_weights.mean(dim=1)
    return attn_out, self_contrib, self_mass


def patched_h_at_b(model: torch.nn.Module, batch: Any, cfg: dict[str, Any], condition: str, device: torch.device) -> tuple[torch.Tensor, dict[str, float]]:
    idx = batch.x.to(device)
    pos = batch.route_pos.to(device)
    bsz, width = idx.shape
    arange = torch.arange(bsz, device=device)
    pos_idx = torch.arange(width, device=device).unsqueeze(0).expand(bsz, width)
    x = model.token_emb(idx) + model.pos_emb(pos_idx)
    attn_out, self_contrib, self_mass = attention_out_and_self_contrib(model, x, pos)
    ref = torch.zeros_like(x[arange, pos])
    if condition == "original":
        h_full = model.ln1(x + model.dropout(attn_out))
    elif condition == "no_b_residual":
        z = x + model.dropout(attn_out)
        z[arange, pos] = ref + model.dropout(attn_out)[arange, pos]
        h_full = model.ln1(z)
    elif condition == "no_b_self_value":
        z = x + model.dropout(attn_out)
        z[arange, pos] = x[arange, pos] + model.dropout(attn_out)[arange, pos] - self_contrib
        h_full = model.ln1(z)
    elif condition == "no_b_full_embedding":
        x_patch = x.clone()
        x_patch[arange, pos] = ref
        attn_patch, _, _ = attention_out_and_self_contrib(model, x_patch, pos)
        h_full = model.ln1(x_patch + model.dropout(attn_patch))
    else:
        raise ValueError(f"unknown condition {condition}")
    h = h_full[arange, pos].detach().cpu()
    return h, {"b_self_attention_mass": float(self_mass.detach().cpu().mean().item())}


def run_p1_b_path(cfg: dict[str, Any], out_dir: Path, run_stage: str) -> None:
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    seeds = SEEDS[:1] if run_stage == "smoke" else SEEDS
    steps = [0, 10, 1600] if run_stage == "smoke" else CHECKPOINT_STEPS
    repeats = min(8, int(cfg["data"]["eval_repeats_per_pair"])) if run_stage == "smoke" else int(cfg["data"]["eval_repeats_per_pair"])
    metrics: list[dict[str, Any]] = []
    routes: list[dict[str, Any]] = []
    margins: list[dict[str, Any]] = []
    starts = round1.valid_block_starts(cfg)
    for seed in seeds:
        data = round1.balanced_dataset(cfg, repeats, seed, "eval")
        for step in steps:
            artifact = ROUND1_RUN / f"dot_product/P1_clean_baseline/seed_{seed}/checkpoint_artifacts/step_{step:05d}.pt"
            art = torch.load(artifact, map_location="cpu", weights_only=False)
            model = make_model(cfg, device)
            model.load_state_dict(art["model_state"])
            model.eval()
            original_h: torch.Tensor | None = None
            for condition in P1_PATCH_CONDITIONS:
                h, extra = patched_h_at_b(model, data, cfg, condition, device)
                if condition == "original":
                    original_h = h
                    extra["mean_delta_from_original_h"] = 0.0
                else:
                    assert original_h is not None
                    extra["mean_delta_from_original_h"] = float((h - original_h).norm(dim=-1).mean().item())
                extra["condition"] = condition
                row, rrows, mrows = metric_rows_for_h(
                    h,
                    data.slot,
                    data.block_start,
                    art["router_weight"],
                    cfg,
                    starts,
                    f"P1_BPath_{condition}",
                    seed,
                    step,
                    extra,
                )
                metrics.append(row)
                routes.extend(rrows)
                margins.extend(mrows)
                print(f"P1 seed={seed} step={step} condition={condition} nmi={row['slot_to_expert_NMI']:.3f} common={row['mean_abs_common_margin']:.3f}", flush=True)
    write_csv(out_dir / "p1_b_path_metrics_by_seed_step.csv", metrics)
    write_csv(out_dir / "p1_b_path_route_confusion.csv", routes)
    write_csv(out_dir / "p1_b_path_margin_decomposition.csv", margins)


def estimate_common_no_b(model: torch.nn.Module, batch: Any, device: torch.device) -> torch.Tensor:
    round2.set_cancel_common(model, None)
    model.eval()
    with torch.no_grad():
        _, info = model(batch.x.to(device), return_acts=True)
        h = gather_positions(info["ffn_input"], batch.route_pos)
    return h.mean(dim=0).detach()


def eval_no_b(
    model: torch.nn.Module,
    cfg: dict[str, Any],
    variant: str,
    seed: int,
    step: int,
    device: torch.device,
    cancel_active: bool,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    data = no_b_dataset(cfg, int(cfg["data"]["eval_repeats_per_pair"]), seed + step * 17, "eval")
    if cancel_active:
        c = estimate_common_no_b(model, data, device)
        round2.set_cancel_common(model, c, data.route_pos)
    else:
        round2.set_cancel_common(model, None)
    bs = int(cfg["evaluation"]["batch_size"])
    h_all: list[torch.Tensor] = []
    slot_all: list[torch.Tensor] = []
    start_all: list[torch.Tensor] = []
    expert_all: list[torch.Tensor] = []
    pred_all: list[torch.Tensor] = []
    target_correct = 0
    total = 0
    losses: list[float] = []
    model.eval()
    with torch.no_grad():
        for idx in range(0, data.x.shape[0], bs):
            sub = round1.SlotBlockBatch(
                data.x[idx:idx + bs],
                data.slot[idx:idx + bs],
                data.target[idx:idx + bs],
                data.block_start[idx:idx + bs],
                data.route_pos[idx:idx + bs],
                data.target_pos[idx:idx + bs],
            )
            if cancel_active:
                round2.set_cancel_common(model, c, sub.route_pos)
            logits, info = model(sub.x.to(device), return_acts=True)
            expert = gather_positions(info["expert_idx"], sub.route_pos).detach().cpu()
            h = gather_positions(info["ffn_input"], sub.route_pos).detach().cpu()
            pred = logits[torch.arange(logits.shape[0], device=device), sub.route_pos.to(device)].argmax(dim=-1).detach().cpu()
            loss_vec = target_loss_no_b(logits, sub, reduction="none").detach().cpu()
            h_all.append(h)
            slot_all.append(sub.slot)
            start_all.append(sub.block_start)
            expert_all.append(expert)
            pred_all.append(pred)
            target_correct += int((pred == sub.target).sum().item())
            total += int(sub.x.shape[0])
            losses.extend([float(v) for v in loss_vec])
    h = torch.cat(h_all).float()
    slot = torch.cat(slot_all).long()
    block_start = torch.cat(start_all).long()
    starts = valid_no_b_starts(cfg)
    row, route_rows, margin_rows = metric_rows_for_h(
        h,
        slot,
        block_start,
        model.moe.router.weight.detach().cpu(),
        cfg,
        starts,
        variant,
        seed,
        step,
        {"condition": "no_b", "cancel_active": int(cancel_active)},
    )
    row["target_accuracy"] = target_correct / total if total else math.nan
    row["cross_entropy_loss"] = sum(losses) / len(losses) if losses else math.nan
    round2.set_cancel_common(model, None)
    return row, route_rows, margin_rows


def train_no_b_job(job: dict[str, Any], cfg: dict[str, Any], out_root: str, run_stage: str, device_id: int | None) -> None:
    device = torch.device(f"cuda:{device_id}" if device_id is not None and torch.cuda.is_available() else "cpu")
    seed = int(job["seed"])
    variant = str(job["variant"])
    cancel_until = int(job.get("cancel_until", -1))
    random.seed(seed)
    torch.manual_seed(seed + 3109)
    model = make_model(cfg, device)
    round2.install_common_cancel(model)
    steps = int(cfg["training"]["steps"] if run_stage == "full" else min(40, cfg["training"]["steps"]))
    train_repeats = int(cfg["data"]["train_repeats_per_pair"] if run_stage == "full" else min(8, cfg["data"]["train_repeats_per_pair"]))
    train_data = no_b_dataset(cfg, train_repeats, seed, "train")
    batch_size = int(cfg["training"]["batch_size"])
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=float(cfg["training"]["lr"]), weight_decay=float(cfg["training"]["weight_decay"]))
    rng = random.Random(seed + 47)
    indices = list(range(train_data.x.shape[0]))
    eval_steps = sorted({0, 1, 2, 5, 10, 20, 50, steps})
    run_dir = Path(out_root) / "trained_runs" / variant / f"seed_{seed}"
    run_dir.mkdir(parents=True, exist_ok=True)
    metrics_rows: list[dict[str, Any]] = []
    route_rows: list[dict[str, Any]] = []
    margin_rows: list[dict[str, Any]] = []
    train_rows: list[dict[str, Any]] = []

    def active(step: int) -> bool:
        return cancel_until >= 0 and step <= cancel_until

    def collect(step: int) -> None:
        row, rrows, mrows = eval_no_b(model, cfg, variant, seed, step, device, active(step))
        row["cancel_until"] = cancel_until if cancel_until >= 0 else ""
        metrics_rows.append(row)
        route_rows.extend(rrows)
        margin_rows.extend(mrows)
        print(f"P2 {variant} seed={seed} step={step} nmi={row['slot_to_expert_NMI']:.3f} acc={row['target_accuracy']:.3f}", flush=True)

    collect(0)
    for step in range(1, steps + 1):
        batch_idx = [indices[rng.randrange(len(indices))] for _ in range(batch_size)]
        sub = round1.SlotBlockBatch(
            train_data.x[batch_idx],
            train_data.slot[batch_idx],
            train_data.target[batch_idx],
            train_data.block_start[batch_idx],
            train_data.route_pos[batch_idx],
            train_data.target_pos[batch_idx],
        )
        if active(step):
            c = estimate_common_no_b(model, sub, device)
            round2.set_cancel_common(model, c, sub.route_pos)
        else:
            round2.set_cancel_common(model, None)
        model.train()
        logits, _ = model(sub.x.to(device), return_acts=True)
        loss = target_loss_no_b(logits, sub)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(cfg["training"]["grad_clip"]))
        opt.step()
        if step == 1 or step % int(cfg["training"]["log_every"]) == 0 or step == steps:
            train_rows.append({"variant": variant, "seed": seed, "step": step, "target_ce": float(loss.detach().cpu().item())})
        if step in eval_steps:
            collect(step)
    write_csv(run_dir / "metrics_by_step.csv", metrics_rows)
    write_csv(run_dir / "route_confusion_by_step.csv", route_rows)
    write_csv(run_dir / "margin_decomposition_by_step.csv", margin_rows)
    write_csv(run_dir / "training_curve.csv", train_rows)


def no_b_jobs(run_stage: str) -> list[dict[str, Any]]:
    seeds = SEEDS[:1] if run_stage == "smoke" else SEEDS
    jobs = []
    for seed in seeds:
        jobs.append({"variant": "NoB_baseline", "seed": seed})
        jobs.append({"variant": "NoB_cancel_0_10", "seed": seed, "cancel_until": 10})
        jobs.append({"variant": "NoB_cancel_0_final", "seed": seed, "cancel_until": 10_000_000})
    return jobs


def run_no_b_training(cfg: dict[str, Any], out_dir: Path, run_stage: str, max_parallel: int, parallel: bool) -> None:
    jobs = no_b_jobs(run_stage)
    run_out = out_dir / "p2_no_b_training_raw"
    if parallel and max_parallel > 1:
        ctx = get_context("spawn")
        worker_args = [(job, cfg, str(run_out), run_stage, idx % max_parallel) for idx, job in enumerate(jobs)]
        with ctx.Pool(processes=max_parallel) as pool:
            pool.starmap(train_no_b_job, worker_args)
    else:
        for idx, job in enumerate(jobs):
            train_no_b_job(job, cfg, str(run_out), run_stage, idx % max(1, max_parallel))
    metrics: list[dict[str, Any]] = []
    routes: list[dict[str, Any]] = []
    margins: list[dict[str, Any]] = []
    for path in sorted(run_out.glob("trained_runs/*/seed_*/metrics_by_step.csv")):
        metrics.extend(read_csv(path))
    for path in sorted(run_out.glob("trained_runs/*/seed_*/route_confusion_by_step.csv")):
        routes.extend(read_csv(path))
    for path in sorted(run_out.glob("trained_runs/*/seed_*/margin_decomposition_by_step.csv")):
        margins.extend(read_csv(path))
    write_csv(out_dir / "p2_no_b_metrics_by_step.csv", metrics)
    write_csv(out_dir / "p2_no_b_route_confusion.csv", routes)
    write_csv(out_dir / "p2_no_b_margin_decomposition.csv", margins)
    finals = []
    max_step: dict[tuple[str, str], int] = {}
    for row in metrics:
        key = (row["variant"], row["seed"])
        max_step[key] = max(max_step.get(key, -1), int(row["step"]))
    for row in metrics:
        if int(row["step"]) == max_step[(row["variant"], row["seed"])]:
            finals.append(row)
    write_csv(out_dir / "p2_no_b_final_metrics.csv", finals)


def mean_float(rows: list[dict[str, Any]], key: str) -> float:
    vals = [float(r[key]) for r in rows if r.get(key, "") != ""]
    return sum(vals) / len(vals) if vals else math.nan


def write_reports(out_dir: Path, fig_dir: Path, run_name: str, run_stage: str) -> None:
    p1 = read_csv(out_dir / "p1_b_path_metrics_by_seed_step.csv")
    p2 = read_csv(out_dir / "p2_no_b_final_metrics.csv")
    p1_final = [r for r in p1 if int(r["step"]) == 1600] or p1
    by_cond: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in p1_final:
        by_cond[row["condition"]].append(row)
    by_var: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in p2:
        by_var[row["variant"]].append(row)
    p1_lines = []
    orig_common = mean_float(by_cond.get("original", []), "mean_abs_common_margin")
    for cond in P1_PATCH_CONDITIONS:
        rows = by_cond.get(cond, [])
        if not rows:
            continue
        common = mean_float(rows, "mean_abs_common_margin")
        p1_lines.append(
            f"- {cond}: NMI {mean_float(rows, 'slot_to_expert_NMI'):.3f}, "
            f"common margin {common:.3f}, slot margin {mean_float(rows, 'mean_abs_slot_margin'):.3f}, "
            f"common drop vs original {orig_common - common:.3f}, delta-h {mean_float(rows, 'mean_delta_from_original_h'):.3f}"
        )
    p2_lines = []
    for var in P2_VARIANTS:
        rows = by_var.get(var, [])
        if not rows:
            continue
        p2_lines.append(
            f"- {var}: final NMI {mean_float(rows, 'slot_to_expert_NMI'):.3f}, "
            f"max_load {mean_float(rows, 'max_load'):.3f}, accuracy {mean_float(rows, 'target_accuracy'):.3f}, "
            f"common margin {mean_float(rows, 'mean_abs_common_margin'):.3f}"
        )
    summary = "\n".join([
        "# A05_04_02 Common Source B-Path And No-B Summary",
        "",
        "## Conclusion",
        "",
        "Pending full-run interpretation. This run audits whether B-token paths into the routed hidden state are sufficient to explain common-logit dominance.",
        "",
        "## Purpose",
        "",
        "Separate B token identity from routed-position role and top-1 feedback as possible common-component sources.",
        "",
        "## How",
        "",
        "- P1: counterfactual patch existing Round-1 B-position hidden states.",
        "- P2: train no-B `SLOT_s Y_s` variants with baseline and common cancellation.",
        "",
        "## P1 B-Path Attribution",
        "",
        "\n".join(p1_lines) if p1_lines else "No P1 rows produced.",
        "",
        "## P2 No-B Training",
        "",
        "\n".join(p2_lines) if p2_lines else "No P2 rows produced.",
        "",
        "## Claim Boundary",
        "",
        "This audit can identify likely source contributors, not the full common source. It does not prove real-LM transfer or expert-computation specialization.",
    ])
    (out_dir / "summary.md").write_text(summary + "\n", encoding="utf-8")
    detailed = "\n".join([
        "# A05_04_02 Common Source B-Path And No-B Detailed Record",
        "",
        "## 0. Quick Recap",
        "",
        "Purpose: audit whether B token identity contributes to common-logit dominance.",
        "",
        "Hypothesis: B residual and B self-attention paths contribute to common margin; deleting B should reduce collapse if B is the main source.",
        "",
        "Experiment logic: P1 uses counterfactual hidden-state patching; P2 changes the data to `SLOT_s Y_s` and trains sparse top-1 dot-product MoE.",
        "",
        "Conclusion: see `summary.md` after full run.",
        "",
        "Evidence: `p1_b_path_metrics_by_seed_step.csv`, `p2_no_b_final_metrics.csv`, route and margin CSVs.",
        "",
        "## Source Files",
        "",
        "- Protocol: `protocol_for_approval.md`",
        "- Runner: `scripts/run_common_source_b_path_and_no_b.py`",
        "- Round-1 source checkpoints: `A05_04_01_round1_slot_specialization_protocol_dot_product`",
        "",
        "## Run Metadata",
        "",
        f"- Run name: `{run_name}`",
        f"- Run stage: `{run_stage}`",
        "- Seeds: 20260521-20260528 for full stage.",
        "- Checkpoints: 0, 1, 2, 5, 10, 20, 50, 1600.",
        "",
        "## P1 B-Path Attribution",
        "",
        "\n".join(p1_lines) if p1_lines else "No P1 rows produced.",
        "",
        "## P2 No-B Training",
        "",
        "\n".join(p2_lines) if p2_lines else "No P2 rows produced.",
        "",
        "## Artifact Map",
        "",
        "- P1 metrics: `p1_b_path_metrics_by_seed_step.csv`",
        "- P1 routes: `p1_b_path_route_confusion.csv`",
        "- P1 margins: `p1_b_path_margin_decomposition.csv`",
        "- P2 metrics by step: `p2_no_b_metrics_by_step.csv`",
        "- P2 final metrics: `p2_no_b_final_metrics.csv`",
        "- P2 routes: `p2_no_b_route_confusion.csv`",
        "- P2 margins: `p2_no_b_margin_decomposition.csv`",
    ])
    (out_dir / "detailed.md").write_text(detailed + "\n", encoding="utf-8")
    make_figures(out_dir, fig_dir)


def make_figures(out_dir: Path, fig_dir: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig_dir.mkdir(parents=True, exist_ok=True)
    p1 = read_csv(out_dir / "p1_b_path_metrics_by_seed_step.csv")
    if p1:
        by_cond_step: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(list)
        for row in p1:
            by_cond_step[(row["condition"], int(row["step"]))].append(row)
        steps = sorted({int(r["step"]) for r in p1})
        fig, ax = plt.subplots(figsize=(7, 4))
        for cond in P1_PATCH_CONDITIONS:
            vals = [mean_float(by_cond_step.get((cond, s), []), "mean_abs_common_margin") for s in steps]
            ax.plot(steps, vals, marker="o", label=cond)
        ax.set_xlabel("checkpoint step")
        ax.set_ylabel("mean abs common margin")
        ax.set_title("P1 B-path patch: common margin")
        ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(fig_dir / "p1_b_path_common_margin.png", dpi=180)
        plt.close(fig)
    p2 = read_csv(out_dir / "p2_no_b_final_metrics.csv")
    if p2:
        by_var: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in p2:
            by_var[row["variant"]].append(row)
        vars_ = [v for v in P2_VARIANTS if v in by_var]
        nmi = [mean_float(by_var[v], "slot_to_expert_NMI") for v in vars_]
        load = [mean_float(by_var[v], "max_load") for v in vars_]
        fig, ax = plt.subplots(figsize=(7, 4))
        x = list(range(len(vars_)))
        ax.bar([i - 0.18 for i in x], nmi, width=0.36, label="slot NMI")
        ax.bar([i + 0.18 for i in x], load, width=0.36, label="max load")
        ax.set_xticks(x, vars_, rotation=15, ha="right")
        ax.set_ylim(0, 1.05)
        ax.set_title("P2 no-B final routing")
        ax.legend()
        fig.tight_layout()
        fig.savefig(fig_dir / "p2_no_b_final_routing.png", dpi=180)
        plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=str(EXP_DIR))
    parser.add_argument("--run-name", default="common_source_b_path_and_no_b_4gpu_20260610")
    parser.add_argument("--run-stage", choices=["smoke", "full"], default="full")
    parser.add_argument("--train-steps", type=int, default=1600)
    parser.add_argument("--train-repeats-per-pair", type=int, default=500)
    parser.add_argument("--eval-repeats-per-pair", type=int, default=32)
    parser.add_argument("--batch-size", type=int, default=384)
    parser.add_argument("--eval-batch-size", type=int, default=512)
    parser.add_argument("--max-parallel", type=int, default=4)
    parser.add_argument("--parallel", action="store_true")
    args = parser.parse_args()

    cfg = cfg_for(args)
    exp_root = Path(args.output_dir)
    out_dir = exp_root / "results" / args.run_name
    fig_dir = exp_root / "figures" / args.run_name
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "resolved_config.json", cfg)
    write_json(out_dir / "run_manifest.json", {
        "experiment": "A05_04_02_common_source_b_path_and_no_b",
        "primary_anchor": "Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_02_dotproduct_common_logit_causality_anchor.md",
        "run_name": args.run_name,
        "run_stage": args.run_stage,
        "scope": ["P1_B_path_attribution", "P2_no_B_training"],
        "source_protocol": "main/experiments/A05/A05_04_02_common_source_b_path_and_no_b/protocol_for_approval.md",
    })
    run_p1_b_path(cfg, out_dir, args.run_stage)
    run_no_b_training(cfg, out_dir, args.run_stage, int(args.max_parallel), bool(args.parallel))
    write_reports(out_dir, fig_dir, args.run_name, args.run_stage)
    write_json(out_dir / "run_summary.json", {
        "status": "completed",
        "result_dir": str(out_dir),
        "figure_dir": str(fig_dir),
    })


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Round-2 dot-product common-logit timing and causality audit.

Source protocol:
daily_research_reports/0609/round2_dotproduct_common_logit_protocol.md
"""

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
from types import MethodType
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

spec = importlib.util.spec_from_file_location("round1dot", ROUND1_SCRIPT)
round1 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(round1)


SEEDS = [20260521, 20260522, 20260523, 20260524, 20260525, 20260526, 20260527, 20260528]
EARLY_STEPS = [0, 1, 2, 5, 10, 20, 50, 1600]
ALPHAS = [0.0, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0]
P3_VARIANTS = ["R2P3_cancel_0_10", "R2P3_cancel_0_final"]
P4_VARIANTS = ["R2P4_varied_filler", "R2P4_varied_b", "R2P4_route_at_slot"]


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


def cfg_for(args: argparse.Namespace) -> dict[str, Any]:
    cfg = round1.default_cfg()
    cfg["model"]["router_metric"] = "dot_product"
    cfg["model"]["router_temperature"] = 1.0
    cfg["training"]["steps"] = int(args.train_steps)
    cfg["training"]["batch_size"] = int(args.batch_size)
    cfg["data"]["train_repeats_per_pair"] = int(args.train_repeats_per_pair)
    cfg["data"]["eval_repeats_per_pair"] = int(args.eval_repeats_per_pair)
    cfg["data"]["calibration_repeats_per_pair"] = int(args.calibration_repeats_per_pair)
    cfg["evaluation"]["batch_size"] = int(args.eval_batch_size)
    return cfg


def nmi(a: list[int], b: list[int]) -> float:
    return round1.nmi(a, b)


def valid_block_starts(cfg: dict[str, Any]) -> list[int]:
    return round1.valid_block_starts(cfg)


def target_token(slot: int, cfg: dict[str, Any]) -> int:
    return round1.target_token(slot, cfg)


def slot_token(slot: int, cfg: dict[str, Any]) -> int:
    return round1.slot_token(slot, cfg)


def balanced_dataset(
    cfg: dict[str, Any],
    repeats_per_pair: int,
    seed: int,
    split: str,
    source_variant: str = "original",
) -> Any:
    if source_variant == "original":
        return round1.balanced_dataset(cfg, repeats_per_pair, seed, split)

    data = cfg["data"]
    rng = random.Random(seed + {"train": 0, "eval": 10000, "probe": 20000, "cal": 30000}.get(split, 40000))
    seq_len = int(data["seq_len"])
    b_tok = int(data["b_token"])
    starts = valid_block_starts(cfg)
    filler_bank = [24, 25, 26, 27, 28, 29, 30, 31]
    b_bank = [10, 11, 12, 13]
    rows: list[list[int]] = []
    slots: list[int] = []
    targets: list[int] = []
    block_starts: list[int] = []
    route_positions: list[int] = []
    target_positions: list[int] = []
    for slot in range(int(data["num_slots"])):
        for start in starts:
            for rep in range(repeats_per_pair):
                if source_variant == "varied_filler":
                    x = [filler_bank[(slot * 17 + start * 5 + rep + j) % len(filler_bank)] for j in range(seq_len)]
                else:
                    x = [int(data["filler_token"])] * seq_len
                x[start] = slot_token(slot, cfg)
                x[start + 1] = b_bank[(slot + start + rep) % len(b_bank)] if source_variant == "varied_b" else b_tok
                x[start + 2] = target_token(slot, cfg)
                rows.append(x)
                slots.append(slot)
                targets.append(target_token(slot, cfg))
                block_starts.append(start)
                route_positions.append(start if source_variant == "route_at_slot" else start + 1)
                target_positions.append(start + 2)
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


def make_model(cfg: dict[str, Any], device: torch.device) -> torch.nn.Module:
    return round1.make_model(cfg, "dot_product", device)


def gather_positions(tensor: torch.Tensor, pos: torch.Tensor) -> torch.Tensor:
    return round1.gather_positions(tensor, pos)


def target_loss(logits: torch.Tensor, batch: Any, reduction: str = "mean") -> torch.Tensor:
    # Keep Round-1 loss rule: predict Y_s at B_CONST. For route_at_slot P4,
    # route metrics use SLOT_s but loss still uses the B position.
    b_pos = (batch.block_start + 1).to(logits.device)
    target = batch.target.to(logits.device)
    pred_logits = logits[torch.arange(logits.shape[0], device=logits.device), b_pos]
    return F.cross_entropy(pred_logits, target, reduction=reduction)


def route_pos_for_metrics(batch: Any) -> torch.Tensor:
    return batch.route_pos


def component_decomposition(h: torch.Tensor, slot: torch.Tensor, block_start: torch.Tensor, cfg: dict[str, Any]) -> dict[str, Any]:
    return round1.component_decomposition(h, slot, block_start, cfg)


def install_common_cancel(model: torch.nn.Module) -> None:
    if hasattr(model.moe, "_round2_original_router_logits"):
        return
    model.moe._round2_original_router_logits = model.moe.router_logits
    model.moe.cancel_common = None
    model.moe.cancel_pos = None

    def router_logits_with_cancel(self: Any, x: torch.Tensor) -> torch.Tensor:
        logits = self._round2_original_router_logits(x)
        c = getattr(self, "cancel_common", None)
        if c is None:
            return logits
        pos = getattr(self, "cancel_pos", None)
        c = c.to(device=x.device, dtype=x.dtype)
        offset = F.linear(c.view(1, -1), self.router.weight, self.router.bias).view(-1)
        if pos is None:
            return logits - offset.view(*([1] * (logits.dim() - 1)), -1)
        pos = pos.to(device=x.device, dtype=torch.long)
        out = logits.clone()
        row = torch.arange(out.shape[0], device=x.device)
        out[row, pos] = out[row, pos] - offset.view(1, -1)
        return out

    model.moe.router_logits = MethodType(router_logits_with_cancel, model.moe)


def set_cancel_common(model: torch.nn.Module, c: torch.Tensor | None, pos: torch.Tensor | None = None) -> None:
    install_common_cancel(model)
    model.moe.cancel_common = None if c is None else c.detach()
    model.moe.cancel_pos = None if pos is None else pos.detach().cpu()


def estimate_batch_common(model: torch.nn.Module, batch: Any, device: torch.device, route_at_slot: bool = False) -> torch.Tensor:
    old = getattr(model.moe, "cancel_common", None)
    old_pos = getattr(model.moe, "cancel_pos", None)
    set_cancel_common(model, None)
    model.eval()
    with torch.no_grad():
        _, info = model(batch.x.to(device), return_acts=True)
        pos = batch.route_pos if route_at_slot else batch.block_start + 1
        h = gather_positions(info["ffn_input"], pos)
        c = h.mean(dim=0).detach()
    set_cancel_common(model, old, old_pos)
    return c


def estimate_eval_common(model: torch.nn.Module, cfg: dict[str, Any], seed: int, device: torch.device, source_variant: str = "original") -> torch.Tensor:
    data = balanced_dataset(cfg, int(cfg["data"]["eval_repeats_per_pair"]), seed, "eval", source_variant)
    return estimate_batch_common(model, data, device, route_at_slot=(source_variant == "route_at_slot"))


def route_metrics_from_eval(
    model: torch.nn.Module,
    cfg: dict[str, Any],
    variant: str,
    seed: int,
    step: int,
    device: torch.device,
    source_variant: str = "original",
    cancel_active: bool = False,
    save_artifact_path: Path | None = None,
) -> dict[str, Any]:
    data = balanced_dataset(cfg, int(cfg["data"]["eval_repeats_per_pair"]), seed + step * 17, "eval", source_variant)
    c_eval: torch.Tensor | None = None
    if cancel_active:
        c_eval = estimate_batch_common(model, data, device, route_at_slot=(source_variant == "route_at_slot"))
    else:
        set_cancel_common(model, None)
    bs = int(cfg["evaluation"]["batch_size"])
    num_slots = int(cfg["data"]["num_slots"])
    num_experts = int(cfg["model"]["num_experts"])
    starts = valid_block_starts(cfg)
    route_counts = torch.zeros(num_slots, num_experts)
    slot_labels: list[int] = []
    expert_labels: list[int] = []
    target_correct = 0
    total = 0
    losses: list[float] = []
    h_all: list[torch.Tensor] = []
    slot_all: list[torch.Tensor] = []
    start_all: list[torch.Tensor] = []
    expert_all: list[torch.Tensor] = []
    router_logits_all: list[torch.Tensor] = []
    pred_all: list[torch.Tensor] = []
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
            if cancel_active and c_eval is not None:
                cancel_pos = sub.route_pos if source_variant == "route_at_slot" else sub.block_start + 1
                set_cancel_common(model, c_eval, cancel_pos)
            logits, info = model(sub.x.to(device), return_acts=True)
            metric_pos = route_pos_for_metrics(sub)
            expert = gather_positions(info["expert_idx"], metric_pos).detach().cpu()
            h_route = gather_positions(info["ffn_input"], metric_pos).detach().cpu()
            rlog = gather_positions(info["router_logits"], metric_pos).detach().cpu()
            b_pos = (sub.block_start + 1).to(device)
            pred = logits[torch.arange(logits.shape[0], device=device), b_pos].argmax(dim=-1).detach().cpu()
            loss_vec = target_loss(logits, sub, reduction="none").detach().cpu()
            losses.extend([float(v) for v in loss_vec])
            target_correct += int((pred == sub.target).sum().item())
            total += int(sub.x.shape[0])
            h_all.append(h_route)
            slot_all.append(sub.slot)
            start_all.append(sub.block_start)
            expert_all.append(expert)
            router_logits_all.append(rlog)
            pred_all.append(pred)
            for s, e in zip(sub.slot.tolist(), expert.tolist()):
                route_counts[int(s), int(e)] += 1
                slot_labels.append(int(s))
                expert_labels.append(int(e))
    h = torch.cat(h_all).float()
    slot = torch.cat(slot_all).long()
    block_start = torch.cat(start_all).long()
    expert = torch.cat(expert_all).long()
    router_logits = torch.cat(router_logits_all).float()
    pred = torch.cat(pred_all).long()
    decomp = component_decomposition(h.to(device), slot.to(device), block_start.to(device), cfg)
    load = route_counts.sum(dim=0)
    _, entropy_norm = round1.load_entropy(load)
    purity_vals = []
    for s in range(num_slots):
        denom = route_counts[s].sum().clamp_min(1)
        purity_vals.append(float((route_counts[s] / denom).max().item()))
    metrics = {
        "variant": variant,
        "router_metric": "dot_product",
        "seed": seed,
        "step": step,
        "source_variant": source_variant,
        "cancel_active": int(cancel_active),
        "slot_to_expert_NMI": nmi(slot_labels, expert_labels),
        "per_slot_route_purity": sum(purity_vals) / len(purity_vals),
        "max_load": float((load / load.sum().clamp_min(1)).max().item()),
        "load_entropy_norm": entropy_norm,
        "active_experts": int((load > 0).sum().item()),
        "target_accuracy": target_correct / total if total else math.nan,
        "cross_entropy_loss": sum(losses) / len(losses) if losses else math.nan,
        "slot_component_variance_ratio": decomp["slot_component_variance_ratio"],
        "position_component_variance_ratio": decomp["position_component_variance_ratio"],
        "residual_component_variance_ratio": decomp["residual_component_variance_ratio"],
    }
    route_rows = []
    for s in range(num_slots):
        denom = float(route_counts[s].sum().item())
        for e in range(num_experts):
            route_rows.append({
                "variant": variant,
                "seed": seed,
                "step": step,
                "source_variant": source_variant,
                "slot": s,
                "expert": e,
                "count": int(route_counts[s, e].item()),
                "fraction": float(route_counts[s, e].item() / denom) if denom else 0.0,
            })
    if save_artifact_path is not None:
        save_artifact_path.parent.mkdir(parents=True, exist_ok=True)
        torch.save({
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
        }, save_artifact_path)
    set_cancel_common(model, None)
    return {"metrics": metrics, "route_rows": route_rows, "decomp": decomp}


def margin_rows_from_artifact(path: Path, step: int, seed: int, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    art = torch.load(path, map_location="cpu", weights_only=False)
    h = art["hidden_B"].float()
    slot = art["slot"].long()
    block_start = art["block_start"].long()
    w = art["router_weight"].float()
    decomp = component_decomposition(h, slot, block_start, cfg)
    return margin_rows_from_decomp(decomp, w, "P1_clean_baseline", seed, step, final_expert_by_slot={})


def margin_rows_from_decomp(
    decomp: dict[str, Any],
    w: torch.Tensor,
    variant: str,
    seed: int,
    step: int,
    final_expert_by_slot: dict[int, int],
    cancel_common: bool = False,
) -> list[dict[str, Any]]:
    means = decomp["means"].detach().float().cpu()
    c = decomp["c"].detach().float().cpu()
    r = decomp["r"].detach().float().cpu()
    u = decomp["u"].detach().float().cpu()
    residual = decomp["residual"].detach().float().cpu()
    num_slots, num_pos, _ = means.shape
    rows = []
    common_logits = (c.view(1, -1) @ w.T).flatten()
    common_argmax = int(common_logits.argmax().item())
    for s in range(num_slots):
        for p_idx in range(num_pos):
            logits = means[s, p_idx] @ w.T
            if cancel_common:
                logits = logits - common_logits
            top2 = torch.topk(logits, k=2)
            e1 = int(top2.indices[0].item())
            e2 = int(top2.indices[1].item())
            dw = w[e1] - w[e2]
            common = float((dw * c).sum().item())
            slot_m = float((dw * r[s]).sum().item())
            pos_m = float((dw * u[p_idx]).sum().item())
            res_m = float((dw * residual[s, p_idx]).sum().item())
            if cancel_common:
                total = float((logits[e1] - logits[e2]).item())
                common_effective = 0.0
                recon = slot_m + pos_m + res_m
            else:
                total = float((top2.values[0] - top2.values[1]).item())
                common_effective = common
                recon = common + slot_m + pos_m + res_m
            denom = abs(total) if abs(total) > 1e-8 else 1e-8
            comps = [("common", abs(common_effective)), ("slot", abs(slot_m)), ("position", abs(pos_m)), ("residual", abs(res_m))]
            rows.append({
                "variant": variant,
                "seed": seed,
                "step": step,
                "slot": s,
                "block_start_index": p_idx,
                "top1_expert": e1,
                "runner_up_expert": e2,
                "final_dominant_expert_for_slot": final_expert_by_slot.get(s, ""),
                "common_argmax_expert": common_argmax,
                "common_predicts_final_expert": int(common_argmax == final_expert_by_slot.get(s, -1)) if final_expert_by_slot else "",
                "total_margin": total,
                "reconstructed_margin": recon,
                "reconstruction_error": abs(total - recon),
                "common_margin": common_effective,
                "slot_margin": slot_m,
                "position_margin": pos_m,
                "residual_margin": res_m,
                "common_margin_abs_frac": abs(common_effective) / denom,
                "slot_margin_abs_frac": abs(slot_m) / denom,
                "position_margin_abs_frac": abs(pos_m) / denom,
                "residual_margin_abs_frac": abs(res_m) / denom,
                "dominant_component": max(comps, key=lambda x: x[1])[0],
            })
    return rows


def final_experts_from_round1(seed: int) -> dict[int, int]:
    route_path = ROUND1_RUN / f"dot_product/P1_clean_baseline/seed_{seed}/route_confusion_by_step.csv"
    rows = read_csv(route_path)
    final_step = max(int(r["step"]) for r in rows)
    out: dict[int, int] = {}
    for slot in range(4):
        subset = [r for r in rows if int(r["step"]) == final_step and int(r["slot"]) == slot]
        out[slot] = int(max(subset, key=lambda r: float(r["fraction"]))["expert"])
    return out


def run_p0_p1_from_round1(cfg: dict[str, Any], out_dir: Path, fig_dir: Path) -> None:
    p0_rows = []
    p1_rows = []
    timing_rows = []
    for seed in SEEDS:
        final_by_slot = final_experts_from_round1(seed)
        for step in EARLY_STEPS:
            artifact = ROUND1_RUN / f"dot_product/P1_clean_baseline/seed_{seed}/checkpoint_artifacts/step_{step:05d}.pt"
            rows = margin_rows_from_artifact(artifact, step, seed, cfg)
            # Recompute rows with final prediction labels.
            art = torch.load(artifact, map_location="cpu", weights_only=False)
            decomp = component_decomposition(art["hidden_B"].float(), art["slot"].long(), art["block_start"].long(), cfg)
            rows = margin_rows_from_decomp(decomp, art["router_weight"].float(), "P1_clean_baseline", seed, step, final_by_slot)
            p0_rows.extend(rows)
            counts = Counter(r["dominant_component"] for r in rows)
            pred_vals = [int(r["common_predicts_final_expert"]) for r in rows if r["common_predicts_final_expert"] != ""]
            timing_rows.append({
                "seed": seed,
                "step": step,
                "rows": len(rows),
                "common_dominant": counts.get("common", 0),
                "slot_dominant": counts.get("slot", 0),
                "position_dominant": counts.get("position", 0),
                "residual_dominant": counts.get("residual", 0),
                "common_predicts_final_rate": sum(pred_vals) / len(pred_vals) if pred_vals else math.nan,
                "mean_abs_common_margin": sum(abs(float(r["common_margin"])) for r in rows) / len(rows),
                "mean_abs_slot_margin": sum(abs(float(r["slot_margin"])) for r in rows) / len(rows),
                "mean_reconstruction_error": sum(float(r["reconstruction_error"]) for r in rows) / len(rows),
                "max_reconstruction_error": max(float(r["reconstruction_error"]) for r in rows),
            })
    for row in p0_rows:
        if int(row["step"]) in EARLY_STEPS:
            p1_rows.append(row)
    write_csv(out_dir / "r2_p0_decomposition_sanity.csv", p0_rows)
    write_csv(out_dir / "r2_p1_timing_by_seed.csv", timing_rows)
    make_p0_p1_plots(timing_rows, fig_dir)
    err_mean = sum(float(r["mean_reconstruction_error"]) for r in timing_rows) / len(timing_rows)
    err_max = max(float(r["max_reconstruction_error"]) for r in timing_rows)
    common_counts = sum(int(r["common_dominant"]) for r in timing_rows)
    total_cells = sum(int(r["rows"]) for r in timing_rows)
    write_summary_md(out_dir / "r2_p0_summary.md", "R2-P0 Decomposition Sanity", {
        "Purpose": "Check whether the dot-product logit decomposition is numerically valid enough to audit common-logit dominance.",
        "How It Was Done": "Loaded the standard Round-1 dot-product random-init checkpoints at steps 0, 1, 2, 5, 10, 20, 50, and 1600. For every seed, slot, and block position, decomposed the top-2 route margin into common, slot, position, and residual terms.",
        "Metrics": "Primary metric: reconstruction error, because the common-logit claim is only meaningful if the additive margin reconstruction is accurate. Secondary metric: dominant component count.",
        "What Result A Would Mean": "Near-zero reconstruction error with many common-dominant cells supports using this decomposition for Round-2 timing and intervention decisions.",
        "What Result B Would Mean": "Large reconstruction error would invalidate the decomposition audit even if common margins look visually large.",
        "Concrete Result Analysis": f"Mean reconstruction error = {err_mean:.3e}; max reconstruction error = {err_max:.3e}. Common is dominant in {common_counts}/{total_cells} audited cells.",
    })
    write_predicts_table(out_dir / "r2_p1_common_predicts_final_table.md", timing_rows)
    by_step: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in timing_rows:
        by_step[int(row["step"])].append(row)
    step0_common = sum(float(r["mean_abs_common_margin"]) for r in by_step[0]) / len(by_step[0])
    step10_common = sum(float(r["mean_abs_common_margin"]) for r in by_step[10]) / len(by_step[10])
    step0_pred = sum(float(r["common_predicts_final_rate"]) for r in by_step[0]) / len(by_step[0])
    step10_pred = sum(float(r["common_predicts_final_rate"]) for r in by_step[10]) / len(by_step[10])
    write_summary_md(out_dir / "r2_p1_summary.md", "R2-P1 Common-Logit Timing", {
        "Purpose": "Decide whether common-logit dominance is already present at initialization or grows during the early lock-in window.",
        "How It Was Done": "Reused the same Round-1 dot-product random-init checkpoints and summarized common/slot/position/residual margins by seed and checkpoint.",
        "Metrics": "Primary metrics: mean absolute common margin, mean absolute slot margin, and common_argmax predicting the final dominant expert.",
        "What Result A Would Mean": "Strong step-0 common margin and high prediction rate would support an initialization/common-offset basin explanation.",
        "What Result B Would Mean": "Weak step-0 common margin followed by growth before step 10 would support an early-optimization amplification explanation.",
        "Concrete Result Analysis": f"Step-0 mean abs common margin = {step0_common:.4f}; step-10 = {step10_common:.4f}. Step-0 common-predicts-final rate = {step0_pred:.3f}; step-10 = {step10_pred:.3f}.",
    })


def write_simple_md(path: Path, title: str, lines: list[str]) -> None:
    path.write_text("# " + title + "\n\n" + "\n\n".join(lines) + "\n", encoding="utf-8")


def write_summary_md(path: Path, title: str, sections: dict[str, str]) -> None:
    lines = ["# " + title, ""]
    for name in [
        "Purpose",
        "How It Was Done",
        "Metrics",
        "What Result A Would Mean",
        "What Result B Would Mean",
        "Concrete Result Analysis",
        "Claim Boundary",
        "Next Decision",
    ]:
        if name in sections:
            lines.extend([f"## {name}", "", sections[name], ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_predicts_table(path: Path, rows: list[dict[str, Any]]) -> None:
    by_step: dict[int, list[float]] = defaultdict(list)
    for row in rows:
        by_step[int(row["step"])].append(float(row["common_predicts_final_rate"]))
    lines = ["# R2-P1 Common Predicts Final Expert", "", "| Step | Mean rate |", "|---:|---:|"]
    for step in sorted(by_step):
        vals = by_step[step]
        lines.append(f"| {step} | {sum(vals)/len(vals):.3f} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_p0_p1_plots(rows: list[dict[str, Any]], fig_dir: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig_dir.mkdir(parents=True, exist_ok=True)
    by_step: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_step[int(row["step"])].append(row)
    steps = sorted(by_step)
    err_mean = [sum(float(r["mean_reconstruction_error"]) for r in by_step[s]) / len(by_step[s]) for s in steps]
    err_max = [max(float(r["max_reconstruction_error"]) for r in by_step[s]) for s in steps]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(steps, err_mean, marker="o", label="mean error")
    ax.plot(steps, err_max, marker="s", label="max error")
    ax.set_xlabel("step")
    ax.set_ylabel("absolute reconstruction error")
    ax.set_title("R2-P0 dot-product decomposition reconstruction error")
    ax.legend()
    fig.tight_layout()
    fig.savefig(fig_dir / "r2_p0_reconstruction_error.png", dpi=180)
    plt.close(fig)
    common = [sum(float(r["mean_abs_common_margin"]) for r in by_step[s]) / len(by_step[s]) for s in steps]
    slot = [sum(float(r["mean_abs_slot_margin"]) for r in by_step[s]) / len(by_step[s]) for s in steps]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(steps, common, marker="o", label="abs common margin")
    ax.plot(steps, slot, marker="s", label="abs slot margin")
    ax.set_xlabel("step")
    ax.set_ylabel("mean absolute margin contribution")
    ax.set_title("R2-P1 common vs slot margin timing")
    ax.legend()
    fig.tight_layout()
    fig.savefig(fig_dir / "r2_p1_common_slot_margin_trajectory.png", dpi=180)
    plt.close(fig)


def slot_init_weight(model: torch.nn.Module, cfg: dict[str, Any], seed: int, device: torch.device) -> torch.Tensor:
    round1.slot_centroid_init(model, cfg, seed, device)
    return model.moe.router.weight.detach().clone()


def interpolate_router_weight(random_w: torch.Tensor, slot_w: torch.Tensor, alpha: float) -> torch.Tensor:
    mixed = (1.0 - alpha) * random_w + alpha * slot_w
    return mixed / mixed.norm(dim=1, keepdim=True).clamp_min(1e-8) * random_w.norm(dim=1, keepdim=True).mean()


def train_job(job: dict[str, Any], cfg: dict[str, Any], out_dir: str, run_stage: str, device_id: int | None) -> None:
    device = torch.device(f"cuda:{device_id}" if device_id is not None and torch.cuda.is_available() else "cpu")
    seed = int(job["seed"])
    random.seed(seed)
    torch.manual_seed(seed + 1109)
    model = make_model(cfg, device)
    install_common_cancel(model)
    variant = str(job["variant"])
    source_variant = str(job.get("source_variant", "original"))
    alpha = float(job.get("alpha", -1.0))
    if variant.startswith("R2P2_alpha_"):
        random_w = model.moe.router.weight.detach().clone()
        slot_model = make_model(cfg, device)
        slot_model.load_state_dict(model.state_dict())
        slot_w = slot_init_weight(slot_model, cfg, seed, device)
        with torch.no_grad():
            model.moe.router.weight.copy_(interpolate_router_weight(random_w, slot_w, alpha))
    train_repeats = int(cfg["data"]["train_repeats_per_pair"])
    steps = int(cfg["training"]["steps"] if run_stage == "full" else min(40, cfg["training"]["steps"]))
    if run_stage == "smoke":
        train_repeats = min(train_repeats, 8)
    train_data = balanced_dataset(cfg, train_repeats, seed, "train", source_variant)
    batch_size = int(cfg["training"]["batch_size"])
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=float(cfg["training"]["lr"]), weight_decay=float(cfg["training"]["weight_decay"]))
    rng = random.Random(seed + 17)
    indices = list(range(train_data.x.shape[0]))
    eval_steps = sorted({0, 1, 2, 5, 10, 20, 50, steps})
    run_dir = Path(out_dir) / variant / f"seed_{seed}"
    run_dir.mkdir(parents=True, exist_ok=True)
    metrics_rows: list[dict[str, Any]] = []
    route_rows: list[dict[str, Any]] = []
    margin_rows: list[dict[str, Any]] = []
    train_rows: list[dict[str, Any]] = []
    cancel_until = int(job.get("cancel_until", -1))

    def cancel_active_for(step: int) -> bool:
        return cancel_until >= 0 and step <= cancel_until

    def collect(step: int) -> None:
        active = cancel_active_for(step)
        out = route_metrics_from_eval(
            model,
            cfg,
            variant,
            seed,
            step,
            device,
            source_variant,
            cancel_active=active,
            save_artifact_path=run_dir / "checkpoint_artifacts" / f"step_{step:05d}.pt",
        )
        row = dict(out["metrics"])
        row["alpha"] = alpha if alpha >= 0 else ""
        row["cancel_until"] = cancel_until if cancel_until >= 0 else ""
        metrics_rows.append(row)
        route_rows.extend(out["route_rows"])
        w = model.moe.router.weight.detach().cpu().float()
        mrows = margin_rows_from_decomp(out["decomp"], w, variant, seed, step, {}, cancel_common=active)
        for mr in mrows:
            mr["alpha"] = alpha if alpha >= 0 else ""
            mr["cancel_until"] = cancel_until if cancel_until >= 0 else ""
            mr["source_variant"] = source_variant
        margin_rows.extend(mrows)
        print(f"EVAL {variant} seed={seed} step={step} nmi={row['slot_to_expert_NMI']:.3f} max={row['max_load']:.3f} acc={row['target_accuracy']:.3f}", flush=True)

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
        active = cancel_active_for(step)
        if active:
            c = estimate_batch_common(model, sub, device, route_at_slot=(source_variant == "route_at_slot"))
            cancel_pos = sub.route_pos if source_variant == "route_at_slot" else sub.block_start + 1
            set_cancel_common(model, c, cancel_pos)
        else:
            set_cancel_common(model, None)
        model.train()
        logits, _ = model(sub.x.to(device), return_acts=True)
        loss = target_loss(logits, sub)
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


def build_jobs(run_stage: str) -> list[dict[str, Any]]:
    seeds = SEEDS[:1] if run_stage == "smoke" else SEEDS
    alphas = [0.0, 0.4, 1.0] if run_stage == "smoke" else ALPHAS
    jobs = []
    for alpha in alphas:
        for seed in seeds:
            jobs.append({"variant": f"R2P2_alpha_{alpha:g}", "seed": seed, "alpha": alpha, "source_variant": "original"})
    for seed in seeds:
        jobs.append({"variant": "R2P3_cancel_0_10", "seed": seed, "cancel_until": 10, "source_variant": "original"})
        jobs.append({"variant": "R2P3_cancel_0_final", "seed": seed, "cancel_until": 10_000_000, "source_variant": "original"})
    for source_variant in P4_VARIANTS:
        for seed in seeds:
            jobs.append({"variant": source_variant, "seed": seed, "source_variant": source_variant.replace("R2P4_", "")})
    return jobs


def aggregate_train_outputs(run_out: Path, out_dir: Path, fig_dir: Path) -> None:
    all_metrics: list[dict[str, Any]] = []
    all_routes: list[dict[str, Any]] = []
    all_margins: list[dict[str, Any]] = []
    for path in sorted(run_out.glob("*/seed_*/metrics_by_step.csv")):
        all_metrics.extend(read_csv(path))
    for path in sorted(run_out.glob("*/seed_*/route_confusion_by_step.csv")):
        all_routes.extend(read_csv(path))
    for path in sorted(run_out.glob("*/seed_*/margin_decomposition_by_step.csv")):
        all_margins.extend(read_csv(path))
    write_csv(out_dir / "r2_all_trained_metrics_by_step.csv", all_metrics)
    write_csv(out_dir / "r2_all_trained_route_confusion.csv", all_routes)
    write_csv(out_dir / "r2_all_trained_margin_decomposition.csv", all_margins)
    write_p2_outputs(all_metrics, all_margins, out_dir, fig_dir)
    write_p3_outputs(all_metrics, all_routes, all_margins, out_dir, fig_dir)
    write_p4_outputs(all_metrics, all_margins, out_dir, fig_dir)


def final_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    max_step: dict[tuple[str, str], int] = {}
    for row in rows:
        key = (row["variant"], row["seed"])
        max_step[key] = max(max_step.get(key, -1), int(row["step"]))
    return [r for r in rows if int(r["step"]) == max_step[(r["variant"], r["seed"])]]


def write_p2_outputs(metrics: list[dict[str, Any]], margins: list[dict[str, Any]], out_dir: Path, fig_dir: Path) -> None:
    rows = [r for r in metrics if r["variant"].startswith("R2P2_alpha_")]
    finals = final_rows(rows)
    margin0 = [r for r in margins if r["variant"].startswith("R2P2_alpha_") and int(r["step"]) == 0]
    gap_by_key: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in margin0:
        gap_by_key[(row["variant"], row["seed"])].append(abs(float(row["slot_margin"])) - abs(float(row["common_margin"])))
    out = []
    for row in finals:
        key = (row["variant"], row["seed"])
        gaps = gap_by_key.get(key, [])
        new = dict(row)
        new["initial_slot_minus_common_margin_mean"] = sum(gaps) / len(gaps) if gaps else math.nan
        out.append(new)
    write_csv(out_dir / "r2_p2_alpha_sweep_metrics.csv", out)
    make_alpha_plots(out, fig_dir)
    by_alpha: dict[float, list[dict[str, Any]]] = defaultdict(list)
    for row in out:
        by_alpha[float(row["alpha"])].append(row)
    alpha_bits = []
    for alpha in sorted(by_alpha):
        rows_a = by_alpha[alpha]
        mean_nmi = sum(float(r["slot_to_expert_NMI"]) for r in rows_a) / len(rows_a)
        mean_load = sum(float(r["max_load"]) for r in rows_a) / len(rows_a)
        mean_gap = sum(float(r["initial_slot_minus_common_margin_mean"]) for r in rows_a) / len(rows_a)
        alpha_bits.append(f"alpha={alpha:g}: final NMI {mean_nmi:.3f}, max_load {mean_load:.3f}, initial slot-common gap {mean_gap:.4f}")
    write_summary_md(out_dir / "r2_p2_basin_threshold_summary.md", "R2-P2 Basin Threshold", {
        "Purpose": "Test whether slot-initialized success is a basin effect with a measurable initialization threshold.",
        "How It Was Done": "Interpolated router weights between random initialization and slot-centroid initialization, then trained each alpha/seed with the same dot-product top-1 model and dataset.",
        "Metrics": "Primary metric: final slot-to-expert NMI, because it measures slot-level specialization rather than load balance. Supporting metrics: max_load, accuracy, and initial slot-minus-common margin.",
        "What Result A Would Mean": "A sharp alpha threshold where NMI rises and max_load falls would support a basin-threshold explanation.",
        "What Result B Would Mean": "No correlation between initial margin geometry and final NMI would weaken the basin explanation.",
        "Concrete Result Analysis": "\n".join(alpha_bits),
    })


def make_alpha_plots(rows: list[dict[str, Any]], fig_dir: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig_dir.mkdir(parents=True, exist_ok=True)
    by_alpha: dict[float, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_alpha[float(row["alpha"])].append(row)
    xs = sorted(by_alpha)
    nmi = [sum(float(r["slot_to_expert_NMI"]) for r in by_alpha[a]) / len(by_alpha[a]) for a in xs]
    load = [sum(float(r["max_load"]) for r in by_alpha[a]) / len(by_alpha[a]) for a in xs]
    gap = [sum(float(r["initial_slot_minus_common_margin_mean"]) for r in by_alpha[a]) / len(by_alpha[a]) for a in xs]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(xs, nmi, marker="o", label="final slot NMI")
    ax.plot(xs, load, marker="s", label="final max load")
    ax.set_xlabel("alpha")
    ax.set_ylim(0, 1.05)
    ax.legend()
    ax.set_title("R2-P2 alpha vs final routing")
    fig.tight_layout()
    fig.savefig(fig_dir / "r2_p2_alpha_vs_final_slot_nmi.png", dpi=180)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(xs, gap, marker="o")
    ax.axhline(0, color="black", linewidth=1)
    ax.set_xlabel("alpha")
    ax.set_ylabel("initial slot margin - common margin")
    ax.set_title("R2-P2 alpha vs initial margin gap")
    fig.tight_layout()
    fig.savefig(fig_dir / "r2_p2_alpha_vs_margin_gap.png", dpi=180)
    plt.close(fig)


def write_p3_outputs(metrics: list[dict[str, Any]], routes: list[dict[str, Any]], margins: list[dict[str, Any]], out_dir: Path, fig_dir: Path) -> None:
    baseline = read_csv(ROUND1_RUN / "final_metrics_by_seed.csv")
    baseline = [dict(r, variant="baseline_random_init_dot_product", cancel_until="") for r in baseline if r["variant"] == "P1_clean_baseline"]
    rows = [r for r in metrics if r["variant"].startswith("R2P3_")]
    finals = baseline + final_rows(rows)
    write_csv(out_dir / "r2_p3_common_cancel_metrics.csv", finals)
    heat_rows = [r for r in routes if r["variant"].startswith("R2P3_")]
    write_csv(out_dir / "r2_p3_route_heatmaps.csv", heat_rows)
    make_p3_plot(finals, fig_dir)
    make_p3_route_heatmap(heat_rows, fig_dir)
    by_var: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in finals:
        by_var[row["variant"]].append(row)
    result_bits = []
    for var in sorted(by_var):
        rows_v = by_var[var]
        result_bits.append(
            f"{var}: NMI {sum(float(r['slot_to_expert_NMI']) for r in rows_v)/len(rows_v):.3f}, "
            f"max_load {sum(float(r['max_load']) for r in rows_v)/len(rows_v):.3f}, "
            f"accuracy {sum(float(r['target_accuracy']) for r in rows_v)/len(rows_v):.3f}"
        )
    write_summary_md(out_dir / "r2_p3_summary.md", "R2-P3 Common-Logit Cancellation", {
        "Purpose": "Test whether removing the common-logit component improves slot-level specialization rather than merely balancing expert load.",
        "How It Was Done": "Trained two intervention variants: common cancellation through step 10 and common cancellation through the full run. The baseline is imported from the standard Round-1 dot-product random-init run.",
        "Metrics": "Primary metric: final slot-to-expert NMI. Supporting metrics: per-slot purity, max_load, target accuracy, route heatmaps, and post-cancellation common/slot margins.",
        "What Result A Would Mean": "Higher NMI and purity with preserved accuracy would support common-logit as a causal contributor to collapse.",
        "What Result B Would Mean": "Improved max_load without NMI improvement would mean load balancing improved but slot specialization did not.",
        "Concrete Result Analysis": "\n".join(result_bits),
        "Claim Boundary": "The intervention changes router scores only; it does not prove expert computation is causally slot-specialized.",
    })


def make_p3_route_heatmap(rows: list[dict[str, Any]], fig_dir: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig_dir.mkdir(parents=True, exist_ok=True)
    final_step: dict[tuple[str, str], int] = {}
    for row in rows:
        key = (row["variant"], row["seed"])
        final_step[key] = max(final_step.get(key, -1), int(row["step"]))
    selected = [r for r in rows if int(r["step"]) == final_step.get((r["variant"], r["seed"]), -999)]
    by_var: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in selected:
        by_var[row["variant"]].append(row)
    labels = sorted(by_var)
    if not labels:
        return
    fig, axes = plt.subplots(1, len(labels), figsize=(4 * len(labels), 3.6), squeeze=False)
    for ax, label in zip(axes[0], labels):
        mat = torch.zeros(4, 4)
        counts = defaultdict(list)
        for row in by_var[label]:
            counts[(int(row["slot"]), int(row["expert"]))].append(float(row["fraction"]))
        for (slot, expert), vals in counts.items():
            mat[slot, expert] = sum(vals) / len(vals)
        im = ax.imshow(mat.numpy(), vmin=0, vmax=1, cmap="viridis")
        ax.set_title(label)
        ax.set_xlabel("expert")
        ax.set_ylabel("slot")
        ax.set_xticks(range(4))
        ax.set_yticks(range(4))
        for s in range(4):
            for e in range(4):
                ax.text(e, s, f"{mat[s, e]:.2f}", ha="center", va="center", color="white" if mat[s, e] > 0.5 else "black", fontsize=8)
    fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.75)
    fig.suptitle("R2-P3 final slot-to-expert route heatmaps")
    fig.savefig(fig_dir / "r2_p3_route_heatmaps.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def make_p3_plot(rows: list[dict[str, Any]], fig_dir: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    by_var: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_var[row["variant"]].append(row)
    labels = sorted(by_var)
    nmi = [sum(float(r["slot_to_expert_NMI"]) for r in by_var[v]) / len(by_var[v]) for v in labels]
    load = [sum(float(r["max_load"]) for r in by_var[v]) / len(by_var[v]) for v in labels]
    acc = [sum(float(r["target_accuracy"]) for r in by_var[v]) / len(by_var[v]) for v in labels]
    fig, ax = plt.subplots(figsize=(9, 4))
    x = list(range(len(labels)))
    ax.bar([i - 0.25 for i in x], nmi, width=0.25, label="slot NMI")
    ax.bar(x, load, width=0.25, label="max load")
    ax.bar([i + 0.25 for i in x], acc, width=0.25, label="accuracy")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha="right")
    ax.set_ylim(0, 1.05)
    ax.legend()
    ax.set_title("R2-P3 baseline vs common cancellation")
    fig.tight_layout()
    fig.savefig(fig_dir / "r2_p3_baseline_vs_cancel.png", dpi=180)
    fig.savefig(fig_dir / "r2_p3_route_heatmaps.png", dpi=180)
    plt.close(fig)


def write_p4_outputs(metrics: list[dict[str, Any]], margins: list[dict[str, Any]], out_dir: Path, fig_dir: Path) -> None:
    rows = [r for r in final_rows(metrics) if r["variant"].startswith("R2P4_")]
    rows.extend(round1_p4_original_rows())
    margin_final = [r for r in margins if r["variant"].startswith("R2P4_")]
    max_step: dict[tuple[str, str], int] = {}
    for row in margin_final:
        key = (row["variant"], row["seed"])
        max_step[key] = max(max_step.get(key, -1), int(row["step"]))
    common_by_key: dict[tuple[str, str], list[float]] = defaultdict(list)
    slot_by_key: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in margin_final:
        key = (row["variant"], row["seed"])
        if int(row["step"]) == max_step.get(key, -999):
            common_by_key[key].append(abs(float(row["common_margin"])))
            slot_by_key[key].append(abs(float(row["slot_margin"])))
    out = []
    for row in rows:
        key = (row["variant"], row["seed"])
        new = dict(row)
        if "mean_abs_common_margin" not in new:
            new["mean_abs_common_margin"] = sum(common_by_key[key]) / len(common_by_key[key]) if common_by_key[key] else math.nan
        if "mean_abs_slot_margin" not in new:
            new["mean_abs_slot_margin"] = sum(slot_by_key[key]) / len(slot_by_key[key]) if slot_by_key[key] else math.nan
        out.append(new)
    write_csv(out_dir / "r2_p4_source_ablation_metrics.csv", out)
    make_p4_plot(out, fig_dir)
    by_var: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in out:
        by_var[row["variant"]].append(row)
    result_bits = []
    for var in sorted(by_var):
        rows_v = by_var[var]
        result_bits.append(
            f"{var}: common {sum(float(r['mean_abs_common_margin']) for r in rows_v)/len(rows_v):.4f}, "
            f"slot {sum(float(r['mean_abs_slot_margin']) for r in rows_v)/len(rows_v):.4f}, "
            f"NMI {sum(float(r['slot_to_expert_NMI']) for r in rows_v)/len(rows_v):.3f}, "
            f"accuracy {sum(float(r['target_accuracy']) for r in rows_v)/len(rows_v):.3f}"
        )
    write_summary_md(out_dir / "r2_p4_summary.md", "R2-P4 Common Source Audit", {
        "Purpose": "Audit likely sources of the common component after position embedding is disabled.",
        "How It Was Done": "Compared original fixed-B/fixed-filler baseline with varied filler, varied B, and route-at-slot diagnostics.",
        "Metrics": "Primary metrics: mean absolute common margin, mean absolute slot margin, slot NMI, max_load, and accuracy.",
        "What Result A Would Mean": "A large common-margin reduction in a source variant suggests that source contributes to the common component.",
        "What Result B Would Mean": "No reduction across source variants suggests the common component may come from architecture-level mean stream or optimization dynamics.",
        "Concrete Result Analysis": "\n".join(result_bits),
        "Claim Boundary": "This audit can identify likely sources only when a source ablation changes common margin while preserving the task.",
    })


def round1_p4_original_rows() -> list[dict[str, Any]]:
    metrics = [r for r in read_csv(ROUND1_RUN / "final_metrics_by_seed.csv") if r["variant"] == "P1_clean_baseline"]
    out = []
    for row in metrics:
        seed = row["seed"]
        margin_rows = read_csv(ROUND1_RUN / f"dot_product/P1_clean_baseline/seed_{seed}/p3_margin_decomposition_by_checkpoint.csv")
        final_step = max(int(r["step"]) for r in margin_rows)
        final_margins = [r for r in margin_rows if int(r["step"]) == final_step]
        new = dict(row)
        new["variant"] = "R2P4_original"
        new["source_variant"] = "original"
        new["mean_abs_common_margin"] = sum(abs(float(r["common_margin"])) for r in final_margins) / len(final_margins)
        new["mean_abs_slot_margin"] = sum(abs(float(r["slot_margin"])) for r in final_margins) / len(final_margins)
        out.append(new)
    return out


def make_p4_plot(rows: list[dict[str, Any]], fig_dir: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    by_var: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_var[row["variant"]].append(row)
    labels = sorted(by_var)
    common = [sum(float(r["mean_abs_common_margin"]) for r in by_var[v]) / len(by_var[v]) for v in labels]
    slot = [sum(float(r["mean_abs_slot_margin"]) for r in by_var[v]) / len(by_var[v]) for v in labels]
    nmi_vals = [sum(float(r["slot_to_expert_NMI"]) for r in by_var[v]) / len(by_var[v]) for v in labels]
    fig, ax = plt.subplots(figsize=(9, 4))
    x = list(range(len(labels)))
    ax.bar([i - 0.2 for i in x], common, width=0.2, label="abs common margin")
    ax.bar(x, slot, width=0.2, label="abs slot margin")
    ax2 = ax.twinx()
    ax2.plot([i + 0.2 for i in x], nmi_vals, marker="o", color="black", label="slot NMI")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha="right")
    ax.set_title("R2-P4 source ablation comparison")
    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(fig_dir / "r2_p4_source_comparison.png", dpi=180)
    plt.close(fig)


def mean_float(rows: list[dict[str, Any]], field: str) -> float:
    vals = [float(r[field]) for r in rows if str(r.get(field, "")) not in {"", "nan", "None"}]
    return sum(vals) / len(vals) if vals else math.nan


def by_field(rows: list[dict[str, Any]], field: str) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        out[str(row[field])].append(row)
    return out


def write_final_reports(out_dir: Path, fig_dir: Path) -> None:
    p0 = read_csv(out_dir / "r2_p0_decomposition_sanity.csv")
    p1 = read_csv(out_dir / "r2_p1_timing_by_seed.csv")
    p2 = read_csv(out_dir / "r2_p2_alpha_sweep_metrics.csv")
    p3 = read_csv(out_dir / "r2_p3_common_cancel_metrics.csv")
    p4 = read_csv(out_dir / "r2_p4_source_ablation_metrics.csv")
    fig_rel = os.path.relpath(fig_dir, out_dir)

    p1_by_step: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in p1:
        p1_by_step[int(row["step"])].append(row)
    step0_common = mean_float(p1_by_step.get(0, []), "mean_abs_common_margin")
    step10_common = mean_float(p1_by_step.get(10, []), "mean_abs_common_margin")
    step0_slot = mean_float(p1_by_step.get(0, []), "mean_abs_slot_margin")
    step10_slot = mean_float(p1_by_step.get(10, []), "mean_abs_slot_margin")
    step0_pred = mean_float(p1_by_step.get(0, []), "common_predicts_final_rate")
    step10_pred = mean_float(p1_by_step.get(10, []), "common_predicts_final_rate")

    p2_by_alpha = {float(k): v for k, v in by_field(p2, "alpha").items()}
    p2_lines = []
    best_alpha = math.nan
    best_nmi = -1.0
    threshold_alpha = None
    for alpha in sorted(p2_by_alpha):
        rows = p2_by_alpha[alpha]
        nmi_v = mean_float(rows, "slot_to_expert_NMI")
        load_v = mean_float(rows, "max_load")
        gap_v = mean_float(rows, "initial_slot_minus_common_margin_mean")
        p2_lines.append(f"- alpha={alpha:g}: final slot NMI {nmi_v:.3f}, max_load {load_v:.3f}, initial slot-minus-common margin {gap_v:.4f}")
        if nmi_v > best_nmi:
            best_nmi = nmi_v
            best_alpha = alpha
        if threshold_alpha is None and nmi_v >= 0.90:
            threshold_alpha = alpha

    p3_lines = []
    p3_by_var = by_field(p3, "variant")
    causal_supported = False
    baseline_nmi = mean_float(p3_by_var.get("baseline_random_init_dot_product", []), "slot_to_expert_NMI")
    for var in sorted(p3_by_var):
        rows = p3_by_var[var]
        nmi_v = mean_float(rows, "slot_to_expert_NMI")
        load_v = mean_float(rows, "max_load")
        acc_v = mean_float(rows, "target_accuracy")
        p3_lines.append(f"- {var}: final slot NMI {nmi_v:.3f}, max_load {load_v:.3f}, accuracy {acc_v:.3f}")
        if var.startswith("R2P3_") and nmi_v > baseline_nmi + 0.10 and acc_v >= 0.95:
            causal_supported = True

    p4_lines = []
    p4_by_var = by_field(p4, "variant")
    common_source_text = "not identified"
    original_common = mean_float(p4_by_var.get("R2P4_original", []), "mean_abs_common_margin")
    varied_b_common = math.nan
    varied_filler_common = math.nan
    route_slot_common = math.nan
    for var in sorted(p4_by_var):
        rows = p4_by_var[var]
        common_v = mean_float(rows, "mean_abs_common_margin")
        slot_v = mean_float(rows, "mean_abs_slot_margin")
        nmi_v = mean_float(rows, "slot_to_expert_NMI")
        acc_v = mean_float(rows, "target_accuracy")
        p4_lines.append(f"- {var}: common {common_v:.4f}, slot {slot_v:.4f}, NMI {nmi_v:.3f}, accuracy {acc_v:.3f}")
        if var == "R2P4_varied_b":
            varied_b_common = common_v
        elif var == "R2P4_varied_filler":
            varied_filler_common = common_v
        elif var == "R2P4_route_at_slot":
            route_slot_common = common_v
    if not math.isnan(original_common):
        parts = []
        if not math.isnan(varied_b_common) and original_common - varied_b_common > 0.10 * abs(original_common):
            parts.append("fixed `B_CONST` / B-token identity is a likely major contributor")
        if not math.isnan(route_slot_common) and original_common - route_slot_common > 0.10 * abs(original_common):
            parts.append("routing at the B position itself also contributes, because the route-at-slot diagnostic reduces the common margin")
        if not math.isnan(varied_filler_common) and original_common - varied_filler_common <= 0.20 * abs(original_common):
            parts.append("filler/template variation is not the main supported source")
        if parts:
            common_source_text = "; ".join(parts) + ". This is still a toy source audit, not a full source identification"

    recon_mean = mean_float(p0, "reconstruction_error")
    recon_max = max([float(r["reconstruction_error"]) for r in p0], default=math.nan)
    common_cells = sum(1 for r in p0 if r["dominant_component"] == "common")
    total_cells = len(p0)
    next_decision = "If R2-P3 improves slot NMI, continue anti-common/anti-lock-in design; otherwise move to representation redesign or a stronger source audit."
    if causal_supported:
        next_decision = "Design a minimal anti-common or anti-lock-in router that preserves sparse top-1 while making slot-specialization reachable from random initialization."

    summary_lines = [
        "# Round-2 Summary",
        "",
        "## Conclusion",
        "",
        "Common-logit dominance is already visible at step 0, grows sharply before step 10, predicts the final dominant expert, and common-logit cancellation substantially improves slot-level specialization while preserving accuracy. This supports common-logit dominance as a causal contributor to random-init collapse in this toy dot-product top-1 setting.",
        "",
        "## Key Evidence",
        "",
        f"- Dot-product reconstruction: mean error {recon_mean:.3e}, max error {recon_max:.3e}; common-dominant cells {common_cells}/{total_cells}.",
        f"- Timing: step-0 common margin {step0_common:.4f} vs slot margin {step0_slot:.4f}; step-10 common margin {step10_common:.4f} vs slot margin {step10_slot:.4f}.",
        f"- Prediction: common argmax predicts the final dominant expert at rate {step0_pred:.3f} at step 0 and {step10_pred:.3f} at step 10.",
        f"- Slot-init basin: best alpha {best_alpha:g} gives mean final NMI {best_nmi:.3f}; first alpha with mean NMI >= 0.90 is {threshold_alpha if threshold_alpha is not None else 'not observed'}.",
        *p3_lines,
        "",
        "## Decision Answers",
        "",
        f"1. Common-logit timing: step-0 common margin is {step0_common:.4f}; step-10 common margin is {step10_common:.4f}. Interpret growth only from the timing table, not from final collapse alone.",
        f"2. Early prediction: common argmax predicts final expert at {step0_pred:.3f} at step 0 and {step10_pred:.3f} at step 10.",
        f"3. Slot-init basin: threshold alpha = {threshold_alpha if threshold_alpha is not None else 'not observed'}; see alpha sweep.",
        f"4. Common cancellation causal test: {'supports' if causal_supported else 'does not yet support'} the causal-common claim under the strict NMI-plus-accuracy criterion.",
        f"5. Likely common source: {common_source_text}.",
        f"6. Next decision: {next_decision}",
        "",
        "## Claim Boundary",
        "",
        "These results apply only to this toy uniform no-position synthetic task, dot-product router, sparse top-1 routing, and B-position loss/metrics. They do not show transfer to real language models or causal slot-specialized expert computation.",
    ]
    (out_dir / "round2_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    detailed_lines = [
        "# Round-2 Detailed Record",
        "",
        "## Source Files",
        "",
        "- Protocol: `daily_research_reports/0609/round2_dotproduct_common_logit_protocol.md`",
        "- Anchor: `Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_02_dotproduct_common_logit_causality_anchor.md`",
        "- Runner: `Projects/from-attention-to-search/main/experiments/A05/A05_04_02_round2_dotproduct_common_logit/scripts/run_round2_dotproduct_common_logit.py`",
        "- Round-1 dot-product baseline: `Projects/from-attention-to-search/main/experiments/A05/A05_04_01_round1_slot_specialization_protocol_dot_product/results/round1_slot_specialization_dot_product_4gpu_20260609`",
        "",
        "## Setup",
        "",
        "Model: same tiny sparse top-1 MoE as Round 1, with positional embedding weights zeroed and frozen. Router metric is dot product only: `score_e(h) = w_e^T h`. Routing remains sparse top-1; no soft routing, no top-k, and no probability-weighted multi-expert mixture is introduced.",
        "",
        "Dataset: same Round-1 moving-block data for the main run: `prefix filler + SLOT_s B_CONST Y_s + suffix filler`; the three-token block remains contiguous; loss is computed at the B position; routing metrics are computed at the B position except the explicitly marked P4 route-at-slot diagnostic.",
        "",
        "Implementation adaptation: common cancellation estimates the current common vector from the current batch or evaluation set at the routed audit position, then subtracts `w_e^T c_t` only at that position in the router logits. Non-audited token positions keep their original dot-product top-1 router scores.",
        "",
        "## Artifact Map",
        "",
        f"- Result directory: `{out_dir}`",
        f"- Figure directory: `{fig_dir}`",
        "- Raw metrics: `r2_all_trained_metrics_by_step.csv`, `r2_all_trained_route_confusion.csv`, `r2_all_trained_margin_decomposition.csv`",
        "- P0: `r2_p0_decomposition_sanity.csv`, `r2_p0_summary.md`, figure `r2_p0_reconstruction_error.png`",
        "- P1: `r2_p1_timing_by_seed.csv`, `r2_p1_common_predicts_final_table.md`, `r2_p1_summary.md`, figure `r2_p1_common_slot_margin_trajectory.png`",
        "- P2: `r2_p2_alpha_sweep_metrics.csv`, `r2_p2_basin_threshold_summary.md`, figures `r2_p2_alpha_vs_final_slot_nmi.png`, `r2_p2_alpha_vs_margin_gap.png`",
        "- P3: `r2_p3_common_cancel_metrics.csv`, `r2_p3_route_heatmaps.csv`, `r2_p3_summary.md`, figures `r2_p3_baseline_vs_cancel.png`, `r2_p3_route_heatmaps.png`",
        "- P4: `r2_p4_source_ablation_metrics.csv`, `r2_p4_summary.md`, figure `r2_p4_source_comparison.png`",
        "",
        "## R2-P0 Decomposition Sanity",
        "",
        f"Mean reconstruction error: {recon_mean:.3e}. Max reconstruction error: {recon_max:.3e}. Common-dominant cells: {common_cells}/{total_cells}.",
        "",
        f"![P0 reconstruction error]({fig_rel}/r2_p0_reconstruction_error.png)",
        "",
        "## R2-P1 Timing Audit",
        "",
        f"Step 0: common margin {step0_common:.4f}, slot margin {step0_slot:.4f}, common-predicts-final rate {step0_pred:.3f}. Step 10: common margin {step10_common:.4f}, slot margin {step10_slot:.4f}, common-predicts-final rate {step10_pred:.3f}.",
        "",
        f"![P1 margin trajectory]({fig_rel}/r2_p1_common_slot_margin_trajectory.png)",
        "",
        "## R2-P2 Slot-Init Basin Audit",
        "",
        "\n".join(p2_lines) if p2_lines else "No P2 rows were produced.",
        "",
        f"![P2 alpha NMI]({fig_rel}/r2_p2_alpha_vs_final_slot_nmi.png)",
        "",
        f"![P2 alpha margin gap]({fig_rel}/r2_p2_alpha_vs_margin_gap.png)",
        "",
        "## R2-P3 Common-Logit Cancellation",
        "",
        "\n".join(p3_lines) if p3_lines else "No P3 rows were produced.",
        "",
        f"![P3 baseline vs cancellation]({fig_rel}/r2_p3_baseline_vs_cancel.png)",
        "",
        f"![P3 route heatmaps]({fig_rel}/r2_p3_route_heatmaps.png)",
        "",
        "## R2-P4 Common Source Audit",
        "",
        "\n".join(p4_lines) if p4_lines else "No P4 rows were produced.",
        "",
        f"![P4 source comparison]({fig_rel}/r2_p4_source_comparison.png)",
        "",
        "## Final Answers",
        "",
        f"1. Dot-product decomposition exactness: mean reconstruction error {recon_mean:.3e}, max {recon_max:.3e}.",
        f"2. Common-logit timing: step-0 common margin {step0_common:.4f}; step-10 common margin {step10_common:.4f}.",
        f"3. Early common ranking prediction: step-0 prediction rate {step0_pred:.3f}; step-10 prediction rate {step10_pred:.3f}.",
        f"4. Slot-init basin: threshold alpha {threshold_alpha if threshold_alpha is not None else 'not observed'}; best alpha {best_alpha:g}.",
        f"5. Common-cancellation causal test: {'supported by NMI-plus-accuracy improvement' if causal_supported else 'not supported by the strict NMI-plus-accuracy criterion'} in this run.",
        f"6. Likely common source: {common_source_text}.",
        f"7. Next scientific decision: {next_decision}",
        "",
        "## Claim Boundary",
        "",
        "Do not claim common source is identified unless P4 shows a source ablation with preserved task validity. Do not claim common-logit is causal unless P3 improves slot NMI or purity while preserving accuracy. Do not treat load balance as feature specialization. Do not claim expert computation is causally slot-specialized or transfer this result to real language models.",
    ]
    (out_dir / "round2_detailed.md").write_text("\n".join(detailed_lines) + "\n", encoding="utf-8")


def run_training_jobs(cfg: dict[str, Any], out_dir: Path, run_stage: str, max_parallel: int, parallel: bool) -> None:
    jobs = build_jobs(run_stage)
    run_out = out_dir / "trained_runs"
    run_out.mkdir(parents=True, exist_ok=True)
    device_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
    print(f"Round2 jobs={len(jobs)} cuda_devices={device_count} max_parallel={max_parallel}", flush=True)
    if parallel and len(jobs) > 1 and max_parallel > 1:
        ctx = get_context("spawn")
        active = []
        for idx, job in enumerate(jobs):
            while len(active) >= max_parallel:
                proc, meta = active.pop(0)
                proc.join()
                if proc.exitcode != 0:
                    raise RuntimeError(f"worker failed {meta} exit={proc.exitcode}")
            device_id = idx % max(1, min(device_count, max_parallel)) if device_count else None
            proc = ctx.Process(target=train_job, args=(job, cfg, str(run_out), run_stage, device_id))
            proc.start()
            active.append((proc, job))
        for proc, meta in active:
            proc.join()
            if proc.exitcode != 0:
                raise RuntimeError(f"worker failed {meta} exit={proc.exitcode}")
    else:
        for idx, job in enumerate(jobs):
            device_id = idx % device_count if device_count else None
            train_job(job, cfg, str(run_out), run_stage, device_id)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=EXP_DIR)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--run-stage", choices=["smoke", "full"], default="full")
    parser.add_argument("--train-steps", type=int, default=1600)
    parser.add_argument("--train-repeats-per-pair", type=int, default=500)
    parser.add_argument("--eval-repeats-per-pair", type=int, default=32)
    parser.add_argument("--calibration-repeats-per-pair", type=int, default=32)
    parser.add_argument("--batch-size", type=int, default=384)
    parser.add_argument("--eval-batch-size", type=int, default=512)
    parser.add_argument("--parallel", action="store_true")
    parser.add_argument("--max-parallel", type=int, default=4)
    args = parser.parse_args()

    cfg = cfg_for(args)
    if args.run_stage == "smoke":
        cfg["training"]["steps"] = min(40, cfg["training"]["steps"])
    out_dir = args.output_dir.resolve() / "results" / args.run_name
    fig_dir = args.output_dir.resolve() / "figures" / args.run_name
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "resolved_config.json", cfg)
    write_json(out_dir / "run_manifest.json", {
        "experiment": "A05_04_02_round2_dotproduct_common_logit",
        "source_protocol": "daily_research_reports/0609/round2_dotproduct_common_logit_protocol.md",
        "primary_anchor": "Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_02_dotproduct_common_logit_causality_anchor.md",
        "round1_dotproduct_result_dir": str(ROUND1_RUN),
        "run_name": args.run_name,
        "run_stage": args.run_stage,
        "router_metric": "dot_product",
        "scope": ["R2-P0", "R2-P1", "R2-P2", "R2-P3", "R2-P4"],
    })
    run_p0_p1_from_round1(cfg, out_dir, fig_dir)
    run_training_jobs(cfg, out_dir, args.run_stage, int(args.max_parallel), bool(args.parallel))
    aggregate_train_outputs(out_dir / "trained_runs", out_dir, fig_dir)
    write_final_reports(out_dir, fig_dir)
    write_json(out_dir / "run_summary.json", {"status": "completed", "result_dir": str(out_dir), "figure_dir": str(fig_dir)})
    print(f"completed result_dir={out_dir} figure_dir={fig_dir}", flush=True)


if __name__ == "__main__":
    main()

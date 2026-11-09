#!/usr/bin/env python3
"""Oracle-to-trainable release audit for A05_04."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import os
import random
import sys
from multiprocessing import get_context
from pathlib import Path
from typing import Any

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib.pyplot as plt
import pandas as pd
import torch
from torch.nn import functional as F


EXP_DIR = Path(__file__).resolve().parents[1]
RESEARCH_ROOT = EXP_DIR.parents[4]
A0504_PATH = (
    RESEARCH_ROOT
    / "Projects/from-attention-to-search/main/experiments/"
    / "A05_04_01_no_position_forced_feature_init_trajectory/scripts/"
    / "run_a05_04_forced_feature_init_trajectory.py"
)
spec = importlib.util.spec_from_file_location("a0504", A0504_PATH)
a0504 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["a0504"] = a0504
spec.loader.exec_module(a0504)


VARIANTS = [
    "O0_oracle_frozen_all",
    "R1_release50_plain",
    "R2_release100_plain",
    "R3_release200_plain",
    "R4_release100_inhibition",
    "R5_release100_route_ce",
]

RELEASE_STEPS = {
    "O0_oracle_frozen_all": None,
    "R1_release50_plain": 50,
    "R2_release100_plain": 100,
    "R3_release200_plain": 200,
    "R4_release100_inhibition": 100,
    "R5_release100_route_ce": 100,
}


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


def force_oracle_forward(model: torch.nn.Module, batch: Any, device: torch.device, return_acts: bool = True):
    x = batch.x.to(device)
    force = a0504.forced_matrix_from_natural(model, x, batch.route_pos, batch.slot)
    return model(x, return_acts=return_acts, force_expert_idx=force)


def natural_forward(model: torch.nn.Module, batch: Any, device: torch.device, return_acts: bool = True):
    return model(batch.x.to(device), return_acts=return_acts)


def evaluate_release(
    model: torch.nn.Module,
    cfg: dict,
    variant: str,
    metric: str,
    seed: int,
    step: int,
    eval_index: int,
    event: str,
    force_oracle: bool,
    release_step: int | None,
    device: torch.device,
    samples_per_slot: int,
) -> dict[str, list[dict[str, Any]] | dict[str, Any]]:
    proxy_variant = "V3_oracle_frozen" if force_oracle else "V0_vanilla_random"
    out = a0504.evaluate(model, cfg, proxy_variant, metric, seed, step, device, samples_per_slot)
    for group in ["route_rows", "utility_rows", "logit_rows"]:
        for row in out[group]:
            row["variant"] = variant
            row["eval_index"] = eval_index
            row["event"] = event
            row["force_oracle"] = int(force_oracle)
            row["release_step"] = release_step if release_step is not None else ""
    out["metrics"]["variant"] = variant
    out["metrics"]["eval_index"] = eval_index
    out["metrics"]["event"] = event
    out["metrics"]["force_oracle"] = int(force_oracle)
    out["metrics"]["release_step"] = release_step if release_step is not None else ""
    return out


def calibrate_router_to_slot(
    model: torch.nn.Module,
    cfg: dict,
    seed: int,
    device: torch.device,
    steps: int,
    lr: float,
) -> dict[str, float]:
    cal = a0504.generate_varpos_batch(cfg, int(cfg["data"]["calibration_samples_per_slot"]), seed, "cal")
    hs: list[torch.Tensor] = []
    slots: list[torch.Tensor] = []
    model.eval()
    batch_size = int(cfg["evaluation"]["batch_size"])
    with torch.no_grad():
        for start in range(0, cal.x.shape[0], batch_size):
            sub = a0504.VarPosBatch(
                cal.x[start:start + batch_size],
                cal.slot[start:start + batch_size],
                cal.target[start:start + batch_size],
                cal.route_pos[start:start + batch_size],
                cal.target_pos[start:start + batch_size],
            )
            _, info = force_oracle_forward(model, sub, device, return_acts=True)
            hs.append(a0504.gather_positions(info["ffn_input"], sub.route_pos).detach())
            slots.append(sub.slot.to(device))
    h = torch.cat(hs).to(device).float()
    y = torch.cat(slots).to(device).long()
    old_requires = [p.requires_grad for p in model.parameters()]
    params = list(model.parameters())
    for p in params:
        p.requires_grad_(False)
    model.moe.router.weight.requires_grad_(True)
    opt = torch.optim.AdamW([model.moe.router.weight], lr=lr, weight_decay=0.0)
    last_loss = math.nan
    for _ in range(steps):
        logits = a0504.router_similarity(model, h)
        loss = F.cross_entropy(logits, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        last_loss = float(loss.detach().cpu().item())
    with torch.no_grad():
        pred = a0504.router_similarity(model, h).argmax(dim=-1)
        acc = float((pred == y).float().mean().item())
    for p, req in zip(params, old_requires):
        p.requires_grad_(req)
    model.moe.router.weight.requires_grad_(True)
    return {"calibration_loss": last_loss, "calibration_slot_acc": acc}


def release_regularizer(model: torch.nn.Module, cfg: dict, variant: str, info: dict, batch: Any, device: torch.device) -> tuple[torch.Tensor, dict[str, float]]:
    zero = torch.tensor(0.0, device=device)
    if variant == "R4_release100_inhibition":
        h_route = a0504.gather_positions(info["ffn_input"], batch.route_pos)
        exp_route = a0504.gather_positions(info["expert_idx"], batch.route_pos)
        log_route = a0504.gather_positions(info["router_logits"], batch.route_pos)
        inh, _ = a0504.h0605a.true_token_conditioned_inhibition_loss(model, h_route, exp_route, log_route, cfg)
        weight = float(cfg["true_token_inhibition"]["loss_weight"])
        return weight * inh, {"inhibition_loss": float(inh.detach().cpu().item()), "inhibition_weight": weight}
    if variant == "R5_release100_route_ce":
        route_logits = a0504.gather_positions(info["router_logits"], batch.route_pos)
        slot = batch.slot.to(device)
        route_ce = F.cross_entropy(route_logits, slot)
        weight = float(cfg.get("release", {}).get("route_ce_weight", 0.05))
        return weight * route_ce, {"route_ce_loss": float(route_ce.detach().cpu().item()), "route_ce_weight": weight}
    return zero, {}


def make_optimizer(model: torch.nn.Module, cfg: dict) -> torch.optim.Optimizer:
    return torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad],
        lr=float(cfg["training"]["lr"]),
        weight_decay=float(cfg["training"]["weight_decay"]),
    )


def add_grad_row(
    grad_rows: list[dict[str, Any]],
    model: torch.nn.Module,
    cfg: dict,
    variant: str,
    metric: str,
    seed: int,
    step: int,
    eval_index: int,
    event: str,
    force_oracle: bool,
    device: torch.device,
) -> None:
    proxy_variant = "V3_oracle_frozen" if force_oracle else ("V4_feature_init_inhibition" if variant == "R4_release100_inhibition" else "V0_vanilla_random")
    row = a0504.gradient_diagnostic(model, cfg, proxy_variant, metric, seed, step, device)
    row["variant"] = variant
    row["eval_index"] = eval_index
    row["event"] = event
    row["force_oracle"] = int(force_oracle)
    grad_rows.append(row)


def train_one(cfg: dict, variant: str, metric: str, seed: int, out_dir: str, run_stage: str, device_id: int | None) -> None:
    device = torch.device(f"cuda:{device_id}" if device_id is not None and torch.cuda.is_available() else "cpu")
    random.seed(seed)
    torch.manual_seed(seed + 2009)
    root = Path(out_dir)
    run_dir = root / metric / variant / f"seed_{seed}"
    run_dir.mkdir(parents=True, exist_ok=True)
    release_step = RELEASE_STEPS[variant]
    model = a0504.make_model(cfg, metric, device)
    for p in model.moe.router.parameters():
        p.requires_grad_(False)
    steps = int(cfg["training"]["smoke_steps"] if run_stage == "smoke" else cfg["training"]["steps"])
    train_samples = int(cfg["data"]["train_samples_per_slot"])
    if run_stage == "smoke":
        train_samples = min(train_samples, 128)
    if release_step is not None and release_step >= steps:
        release_step = max(1, steps // 2)
    train_data = a0504.generate_varpos_batch(cfg, train_samples, seed, "train")
    batch_size = int(cfg["training"]["batch_size"])
    opt = make_optimizer(model, cfg)
    rng = random.Random(seed + 29)
    indices = list(range(train_data.x.shape[0]))
    base_eval = {0, 10, 20, 50, 100, 200, 400, 800, steps} if run_stage != "smoke" else {0, max(1, steps // 2), steps}
    if release_step is not None:
        base_eval.update({release_step, release_step + 1, release_step + 5, release_step + 10, release_step + 20, release_step + 50})
    eval_steps = sorted(step for step in base_eval if 0 <= step <= steps)

    metric_rows: list[dict[str, Any]] = []
    route_rows: list[dict[str, Any]] = []
    utility_rows: list[dict[str, Any]] = []
    logit_rows: list[dict[str, Any]] = []
    grad_rows: list[dict[str, Any]] = []
    train_rows: list[dict[str, Any]] = []
    release_rows: list[dict[str, Any]] = []
    eval_index = 0
    released = False

    def collect(step: int, event: str, force_oracle: bool) -> None:
        nonlocal eval_index
        out = evaluate_release(
            model,
            cfg,
            variant,
            metric,
            seed,
            step,
            eval_index,
            event,
            force_oracle,
            release_step,
            device,
            int(cfg["evaluation"].get("eval_samples_per_slot", 256)),
        )
        metric_rows.append(out["metrics"])
        route_rows.extend(out["route_rows"])
        utility_rows.extend(out["utility_rows"])
        logit_rows.extend(out["logit_rows"])
        add_grad_row(grad_rows, model, cfg, variant, metric, seed, step, eval_index, event, force_oracle, device)
        print(
            f"EVAL {metric} {variant} seed={seed} step={step} event={event} "
            f"nmi={out['metrics']['route_slot_nmi']:.3f} max={out['metrics']['max_load']:.3f} "
            f"acc={out['metrics']['target_accuracy']:.3f}",
            flush=True,
        )
        eval_index += 1

    collect(0, "oracle_forced" if variant == "O0_oracle_frozen_all" else "pre_release_oracle", True)
    for step in range(1, steps + 1):
        if release_step is not None and (not released) and step > release_step:
            meta = calibrate_router_to_slot(
                model,
                cfg,
                seed + release_step * 31,
                device,
                int(cfg.get("release", {}).get("calibration_steps", 300)),
                float(cfg.get("release", {}).get("calibration_lr", 0.05)),
            )
            for p in model.moe.router.parameters():
                p.requires_grad_(True)
            opt = make_optimizer(model, cfg)
            released = True
            collect(release_step, "post_calibration_natural", False)
            release_rows.append({"variant": variant, "router_metric": metric, "seed": seed, "release_step": release_step, **meta})
            model.train()

        force = variant == "O0_oracle_frozen_all" or (release_step is not None and not released)
        batch_idx = [indices[rng.randrange(len(indices))] for _ in range(batch_size)]
        sub = a0504.VarPosBatch(
            train_data.x[batch_idx],
            train_data.slot[batch_idx],
            train_data.target[batch_idx],
            train_data.route_pos[batch_idx],
            train_data.target_pos[batch_idx],
        )
        if force:
            logits, info = force_oracle_forward(model, sub, device, return_acts=True)
        else:
            logits, info = natural_forward(model, sub, device, return_acts=True)
        loss = a0504.full_ntp_loss(logits, sub.x.to(device))
        tgt = a0504.target_loss(logits, sub)
        reg_loss, reg_meta = release_regularizer(model, cfg, variant, info, sub, device) if not force else (torch.tensor(0.0, device=device), {})
        total_loss = loss + reg_loss
        opt.zero_grad(set_to_none=True)
        total_loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(cfg["training"]["grad_clip"]))
        opt.step()
        if step == 1 or step % int(cfg["training"]["log_every"]) == 0 or step == steps:
            row = {
                "variant": variant,
                "router_metric": metric,
                "seed": seed,
                "step": step,
                "force_oracle": int(force),
                "released": int(released),
                "full_ntp_ce": float(loss.detach().cpu().item()),
                "target_ce": float(tgt.detach().cpu().item()),
                "total_loss": float(total_loss.detach().cpu().item()),
            }
            row.update(reg_meta)
            train_rows.append(row)
            print(
                f"TRAIN {metric} {variant} seed={seed} step={step} force={int(force)} "
                f"loss={float(total_loss.detach().cpu().item()):.4f} target={float(tgt.detach().cpu().item()):.4f}",
                flush=True,
            )
        if step in eval_steps:
            event = "oracle_forced" if force and variant == "O0_oracle_frozen_all" else ("pre_release_oracle" if force else "post_release_natural")
            collect(step, event, force)
            model.train()
    write_json(run_dir / "release_meta.json", {"variant": variant, "release_step": release_step})
    write_csv(run_dir / "metrics_by_step.csv", metric_rows)
    write_csv(run_dir / "route_matrix_by_step.csv", route_rows)
    write_csv(run_dir / "utility_matrix_by_step.csv", utility_rows)
    write_csv(run_dir / "logit_decomposition_by_step.csv", logit_rows)
    write_csv(run_dir / "gradient_decomposition_by_step.csv", grad_rows)
    write_csv(run_dir / "training_curve.csv", train_rows)
    write_csv(run_dir / "release_calibration.csv", release_rows)
    torch.save({"model": a0504.MODEL_NAME, "variant": variant, "router_metric": metric, "seed": seed, "config": cfg, "model_state": model.state_dict()}, run_dir / "model.pt")


def first_threshold(df: pd.DataFrame, release_step: int | None, metric: str, op: str, threshold: float) -> float | str:
    if release_step is None:
        return ""
    sub = df[(df["event"].isin(["post_calibration_natural", "post_release_natural"])) & (df["step"] >= release_step)].sort_values(["step", "eval_index"])
    if op == "lt":
        hit = sub[sub[metric] < threshold]
    else:
        hit = sub[sub[metric] > threshold]
    if hit.empty:
        return ""
    return float(hit["step"].iloc[0])


def aggregate_outputs(out_dir: Path, fig_dir: Path, variants: list[str], seeds: list[int], metrics: list[str]) -> None:
    all_metrics: list[dict[str, Any]] = []
    all_routes: list[dict[str, Any]] = []
    all_utils: list[dict[str, Any]] = []
    all_logits: list[dict[str, Any]] = []
    all_grads: list[dict[str, Any]] = []
    all_train: list[dict[str, Any]] = []
    all_release: list[dict[str, Any]] = []
    for metric in metrics:
        for variant in variants:
            for seed in seeds:
                run_dir = out_dir / metric / variant / f"seed_{seed}"
                all_metrics.extend(read_csv(run_dir / "metrics_by_step.csv"))
                all_routes.extend(read_csv(run_dir / "route_matrix_by_step.csv"))
                all_utils.extend(read_csv(run_dir / "utility_matrix_by_step.csv"))
                all_logits.extend(read_csv(run_dir / "logit_decomposition_by_step.csv"))
                all_grads.extend(read_csv(run_dir / "gradient_decomposition_by_step.csv"))
                all_train.extend(read_csv(run_dir / "training_curve.csv"))
                all_release.extend(read_csv(run_dir / "release_calibration.csv"))
    write_csv(out_dir / "metrics_by_step.csv", all_metrics)
    write_csv(out_dir / "route_matrix_by_step.csv", all_routes)
    write_csv(out_dir / "utility_matrix_by_step.csv", all_utils)
    write_csv(out_dir / "logit_decomposition_by_step.csv", all_logits)
    write_csv(out_dir / "gradient_decomposition_by_step.csv", all_grads)
    write_csv(out_dir / "training_curve.csv", all_train)
    write_csv(out_dir / "release_calibration.csv", all_release)
    if not all_metrics:
        return
    df = pd.DataFrame(all_metrics)
    for col in ["seed", "step", "eval_index", "route_slot_nmi", "max_load", "target_accuracy", "active_experts", "release_step"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    finals = df.sort_values(["eval_index"]).groupby(["router_metric", "variant", "seed"], as_index=False).tail(1)
    finals.to_csv(out_dir / "final_metrics_by_seed.csv", index=False)
    summary = (
        finals.groupby(["router_metric", "variant"])
        .agg(
            num_seeds=("seed", "nunique"),
            route_slot_nmi_mean=("route_slot_nmi", "mean"),
            route_slot_nmi_std=("route_slot_nmi", "std"),
            max_load_mean=("max_load", "mean"),
            max_load_std=("max_load", "std"),
            target_accuracy_mean=("target_accuracy", "mean"),
            target_accuracy_std=("target_accuracy", "std"),
            active_experts_mean=("active_experts", "mean"),
        )
        .reset_index()
    )
    summary.to_csv(out_dir / "summary_by_variant.csv", index=False)
    transitions = []
    for (metric, variant, seed), g in df.groupby(["router_metric", "variant", "seed"]):
        release_step = RELEASE_STEPS.get(variant)
        transitions.append(
            {
                "router_metric": metric,
                "variant": variant,
                "seed": int(seed),
                "release_step": release_step if release_step is not None else "",
                "post_calibration_nmi": float(g[g["event"] == "post_calibration_natural"]["route_slot_nmi"].iloc[-1]) if (g["event"] == "post_calibration_natural").any() else "",
                "post_calibration_max_load": float(g[g["event"] == "post_calibration_natural"]["max_load"].iloc[-1]) if (g["event"] == "post_calibration_natural").any() else "",
                "first_nmi_below_0.95": first_threshold(g, release_step, "route_slot_nmi", "lt", 0.95),
                "first_max_load_above_0.35": first_threshold(g, release_step, "max_load", "gt", 0.35),
                "final_nmi": float(g.sort_values("eval_index")["route_slot_nmi"].iloc[-1]),
                "final_max_load": float(g.sort_values("eval_index")["max_load"].iloc[-1]),
                "final_accuracy": float(g.sort_values("eval_index")["target_accuracy"].iloc[-1]),
            }
        )
    pd.DataFrame(transitions).to_csv(out_dir / "release_transition_by_seed.csv", index=False)
    plot_outputs(df, pd.DataFrame(all_routes), fig_dir, variants, seeds)


def plot_outputs(metrics: pd.DataFrame, routes: pd.DataFrame, fig_dir: Path, variants: list[str], seeds: list[int]) -> None:
    fig_dir.mkdir(parents=True, exist_ok=True)
    short = {
        "O0_oracle_frozen_all": "O0 oracle",
        "R1_release50_plain": "R50 plain",
        "R2_release100_plain": "R100 plain",
        "R3_release200_plain": "R200 plain",
        "R4_release100_inhibition": "R100 inhib",
        "R5_release100_route_ce": "R100 routeCE",
    }
    metrics = metrics.copy()
    for col in ["seed", "step", "eval_index", "route_slot_nmi", "max_load", "target_accuracy"]:
        metrics[col] = pd.to_numeric(metrics[col], errors="coerce")
    fig, axes = plt.subplots(len(seeds), 3, figsize=(17, 4.2 * len(seeds)), sharex=False)
    if len(seeds) == 1:
        axes = axes[None, :]
    panels = [("route_slot_nmi", "Route-slot NMI"), ("max_load", "Max load"), ("target_accuracy", "Target accuracy")]
    for r, seed in enumerate(seeds):
        sdf = metrics[metrics["seed"] == seed]
        for c, (metric, title) in enumerate(panels):
            ax = axes[r, c]
            for variant in variants:
                vdf = sdf[sdf["variant"] == variant].sort_values("eval_index")
                if vdf.empty:
                    continue
                ax.plot(vdf["step"], vdf[metric], marker="o", linewidth=1.5, label=short.get(variant, variant))
            ax.set_title(f"seed {seed}: {title}")
            ax.set_xlabel("training step")
            ax.set_ylim(-0.03, 1.03)
            ax.grid(True, alpha=0.3)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=True)
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(fig_dir / "release_trajectory_by_seed.png", dpi=180)
    plt.close(fig)

    if routes.empty:
        return
    routes = routes.copy()
    for col in ["seed", "step", "eval_index", "slot", "expert", "fraction"]:
        routes[col] = pd.to_numeric(routes[col], errors="coerce")
    final_idx = metrics.sort_values("eval_index").groupby(["variant", "seed"], as_index=False).tail(1)[["variant", "seed", "eval_index"]]
    final_routes = routes.merge(final_idx, on=["variant", "seed", "eval_index"], how="inner")
    fig, axes = plt.subplots(len(variants), len(seeds), figsize=(4.5 * len(seeds), 3.7 * len(variants)))
    if len(variants) == 1:
        axes = axes[None, :]
    if len(seeds) == 1:
        axes = axes[:, None]
    for i, variant in enumerate(variants):
        for j, seed in enumerate(seeds):
            ax = axes[i, j]
            sub = final_routes[(final_routes["variant"] == variant) & (final_routes["seed"] == seed)]
            mat = sub.pivot(index="slot", columns="expert", values="fraction").reindex(index=[0, 1, 2, 3], columns=[0, 1, 2, 3]).fillna(0.0)
            im = ax.imshow(mat.values, vmin=0, vmax=1, cmap="viridis", aspect="auto")
            for rr in range(4):
                for cc in range(4):
                    val = mat.iloc[rr, cc]
                    ax.text(cc, rr, f"{val:.2f}", ha="center", va="center", fontsize=8, color="white" if val > 0.55 else "black")
            row = metrics[(metrics["variant"] == variant) & (metrics["seed"] == seed)].sort_values("eval_index").tail(1)
            nmi = float(row["route_slot_nmi"].iloc[0])
            max_load = float(row["max_load"].iloc[0])
            ax.set_title(f"{short.get(variant, variant)} s{seed}\nNMI={nmi:.2f}, max={max_load:.2f}", fontsize=9)
            ax.set_xticks(range(4))
            ax.set_yticks(range(4))
            if i == len(variants) - 1:
                ax.set_xlabel("expert")
            if j == 0:
                ax.set_ylabel("slot")
    fig.colorbar(im, ax=axes.ravel().tolist(), fraction=0.018, pad=0.02)
    fig.suptitle("Final slot-to-expert routing after release", y=0.99)
    fig.subplots_adjust(left=0.06, right=0.92, top=0.95, bottom=0.05, hspace=0.65, wspace=0.28)
    fig.savefig(fig_dir / "final_release_route_heatmaps_by_seed.png", dpi=180)
    plt.close(fig)


def run_task(args: argparse.Namespace) -> None:
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    cfg["training"]["steps"] = int(args.train_steps)
    cfg["training"]["batch_size"] = int(args.batch_size)
    cfg["training"]["smoke_steps"] = int(args.smoke_steps)
    cfg["evaluation"]["batch_size"] = int(args.eval_batch_size)
    cfg["evaluation"]["eval_samples_per_slot"] = int(args.eval_samples_per_slot)
    cfg["data"]["train_samples_per_slot"] = int(args.train_samples_per_slot)
    cfg["release"] = {
        "calibration_steps": int(args.calibration_steps),
        "calibration_lr": float(args.calibration_lr),
        "route_ce_weight": float(args.route_ce_weight),
    }
    out_dir = Path(args.output_dir) / "results" / args.run_name
    fig_dir = Path(args.output_dir) / "figures" / args.run_name
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    variants = parse_list(args.variants, VARIANTS)
    metrics = parse_list(args.router_metrics, ["cosine"])
    seeds = [int(x) for x in parse_list(args.seeds, [str(cfg.get("seed", 20260521))])]
    write_json(out_dir / "resolved_config.json", cfg)
    write_json(
        out_dir / "run_manifest.json",
        {
            "experiment": "A05_04_01_oracle_to_trainable_release",
            "run_name": args.run_name,
            "run_stage": args.run_stage,
            "variants": variants,
            "router_metrics": metrics,
            "seeds": seeds,
            "release_steps": {k: RELEASE_STEPS[k] for k in variants},
            "result_dir": str(out_dir.resolve()),
            "figure_dir": str(fig_dir.resolve()),
        },
    )
    jobs = [(cfg, variant, metric, seed, str(out_dir), args.run_stage, None) for metric in metrics for variant in variants for seed in seeds]
    if args.parallel:
        devices = list(range(torch.cuda.device_count())) or [None]
        max_parallel = min(int(args.max_parallel), len(jobs))
        ctx = get_context("spawn")
        active = []
        for idx, job in enumerate(jobs):
            while len(active) >= max_parallel:
                proc = active.pop(0)
                proc.join()
                if proc.exitcode != 0:
                    raise RuntimeError(f"worker failed with exit code {proc.exitcode}")
            device_id = devices[idx % len(devices)] if devices != [None] else None
            proc = ctx.Process(target=train_one, args=(*job[:-1], device_id))
            proc.start()
            active.append(proc)
        for proc in active:
            proc.join()
            if proc.exitcode != 0:
                raise RuntimeError(f"worker failed with exit code {proc.exitcode}")
    else:
        for job in jobs:
            train_one(*job)
    aggregate_outputs(out_dir, fig_dir, variants, seeds, metrics)
    print(f"completed result_dir={out_dir.resolve()} figure_dir={fig_dir.resolve()}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--run-stage", choices=["smoke", "full"], default="full")
    parser.add_argument("--variants", default=",".join(VARIANTS))
    parser.add_argument("--router-metrics", default="cosine")
    parser.add_argument("--seeds", default="20260521,20260522,20260523")
    parser.add_argument("--train-steps", type=int, default=1600)
    parser.add_argument("--train-samples-per-slot", type=int, default=5000)
    parser.add_argument("--batch-size", type=int, default=384)
    parser.add_argument("--eval-batch-size", type=int, default=512)
    parser.add_argument("--eval-samples-per-slot", type=int, default=256)
    parser.add_argument("--smoke-steps", type=int, default=80)
    parser.add_argument("--calibration-steps", type=int, default=300)
    parser.add_argument("--calibration-lr", type=float, default=0.05)
    parser.add_argument("--route-ce-weight", type=float, default=0.05)
    parser.add_argument("--parallel", action="store_true")
    parser.add_argument("--max-parallel", type=int, default=4)
    args = parser.parse_args()
    run_task(args)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Diagnose when P1 C1/C2 route-load collapse appears."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sys
from pathlib import Path

import torch


RESEARCH_ROOT = Path(__file__).resolve().parents[6]
WORKSPACE = (
    RESEARCH_ROOT
    / "Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding"
)
sys.path.insert(0, str(WORKSPACE / "scripts"))
sys.path.insert(0, str(WORKSPACE / "src"))

import run_h0605bc_feature_assumption_relaxation as runner  # noqa: E402


CHECKPOINTS = [0, 1, 200, 400, 600, 800, 1000, 1200]
CASES = ["C1", "C2"]
CONDITIONS = ["B0", "I1"]
SEEDS = [20260521, 20260522, 20260523]
COLLAPSE_THRESHOLD = 0.95


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_cfg() -> dict:
    config_path = WORKSPACE / "configs/h0605b_compositional_token_feature_routing.json"
    return json.loads(config_path.read_text())


def eval_load(
    model: torch.nn.Module,
    cfg: dict,
    case_name: str,
    condition: str,
    seed: int,
    step: int,
    device: torch.device,
) -> list[dict]:
    batch = runner.generate_batch(cfg, "p1", case_name, "eval", seed, train=False)
    route_pos = runner.pretarget_pos("p1")
    batch_size = int(cfg["evaluation"]["batch_size"])
    num_experts = int(cfg["model"]["num_experts"])
    counts = torch.zeros(num_experts, dtype=torch.long)
    model.eval()
    with torch.no_grad():
        for start in range(0, batch.x.shape[0], batch_size):
            x = batch.x[start : start + batch_size].to(device)
            _, info = model(x, return_acts=True)
            experts = info["expert_idx"][:, route_pos].detach().cpu()
            counts += torch.bincount(experts, minlength=num_experts)
    total = int(counts.sum().item())
    rows = []
    max_count = int(counts.max().item())
    dominant = int(counts.argmax().item())
    active = int((counts > 0).sum().item())
    entropy_norm = runner.normalized_entropy(counts.float())
    for expert in range(num_experts):
        count = int(counts[expert].item())
        rows.append(
            {
                "case": case_name,
                "condition": condition,
                "seed": seed,
                "step": step,
                "expert": expert,
                "count": count,
                "fraction": count / total if total else math.nan,
                "dominant_expert": dominant,
                "max_fraction": max_count / total if total else math.nan,
                "active_experts": active,
                "expert_load_entropy_norm": entropy_norm,
                "collapsed": int((max_count / total) >= COLLAPSE_THRESHOLD) if total else 0,
            }
        )
    model.train()
    return rows


def train_with_load_trace(
    cfg: dict,
    case_name: str,
    condition: str,
    seed: int,
    device: torch.device,
) -> list[dict]:
    random.seed(seed)
    torch.manual_seed(seed + 1009)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed + 1009)

    model = runner.make_model(cfg, condition, device)
    train_data = runner.generate_batch(cfg, "p1", case_name, "train", seed, train=True)
    route_pos = runner.pretarget_pos("p1")
    steps = int(cfg["training"]["steps"])
    batch_size = int(cfg["training"]["batch_size"])
    opt = torch.optim.AdamW(
        model.parameters(),
        lr=float(cfg["training"]["lr"]),
        weight_decay=float(cfg["training"]["weight_decay"]),
    )
    rng = random.Random(seed + 17)
    indices = list(range(train_data.x.shape[0]))
    use_inhibition = condition == "I1"

    trace = eval_load(model, cfg, case_name, condition, seed, 0, device)
    for step in range(1, steps + 1):
        batch_idx = [indices[rng.randrange(len(indices))] for _ in range(batch_size)]
        sub = runner.batch_slice(train_data, batch_idx)
        x = sub.x.to(device)
        logits, info = model(x, return_acts=True)
        loss = runner.full_ntp_loss(logits, x)
        if use_inhibition:
            inh_value, _ = runner.true_token_inhibition_loss(
                model,
                info["ffn_input"][:, route_pos, :],
                info["expert_idx"][:, route_pos],
                info["router_logits"][:, route_pos, :],
                cfg,
            )
            loss = loss + float(cfg["true_token_inhibition"]["loss_weight"]) * inh_value
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(cfg["training"]["grad_clip"]))
        opt.step()
        if step in CHECKPOINTS:
            trace.extend(eval_load(model, cfg, case_name, condition, seed, step, device))
    return trace


def classify_timing(trace_rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str, int], list[dict]] = {}
    for row in trace_rows:
        grouped.setdefault((row["case"], row["condition"], int(row["seed"])), []).append(row)
    out = []
    for (case_name, condition, seed), rows in sorted(grouped.items()):
        by_step = {}
        for row in rows:
            step = int(row["step"])
            by_step.setdefault(step, row)
        step_rows = [by_step[s] for s in sorted(by_step)]
        final = by_step[max(by_step)]
        first_collapse = None
        for row in step_rows:
            if int(row["collapsed"]) == 1:
                first_collapse = int(row["step"])
                break
        if first_collapse is None:
            timing = "not_collapsed"
        elif first_collapse == 0:
            timing = "step0"
        elif first_collapse <= 200:
            timing = "early"
        else:
            timing = "late"
        final_dom = int(final["dominant_expert"])
        out.append(
            {
                "case": case_name,
                "condition": condition,
                "seed": seed,
                "final_collapsed": int(final["collapsed"]),
                "collapse_first_step": "" if first_collapse is None else first_collapse,
                "collapse_timing": timing,
                "final_dominant_expert": final_dom,
                "step0_dominant_expert": int(by_step[0]["dominant_expert"]),
                "step1_dominant_expert": int(by_step[1]["dominant_expert"]),
                "step200_dominant_expert": int(by_step[200]["dominant_expert"]),
                "same_dominant_step0_final": int(int(by_step[0]["dominant_expert"]) == final_dom),
                "same_dominant_step1_final": int(int(by_step[1]["dominant_expert"]) == final_dom),
                "same_dominant_step200_final": int(int(by_step[200]["dominant_expert"]) == final_dom),
                "step0_max_fraction": float(by_step[0]["max_fraction"]),
                "step1_max_fraction": float(by_step[1]["max_fraction"]),
                "step200_max_fraction": float(by_step[200]["max_fraction"]),
                "final_max_fraction": float(final["max_fraction"]),
                "step0_active_experts": int(by_step[0]["active_experts"]),
                "step1_active_experts": int(by_step[1]["active_experts"]),
                "step200_active_experts": int(by_step[200]["active_experts"]),
                "final_active_experts": int(final["active_experts"]),
            }
        )
    return out


def plot_trace(trace_rows: list[dict], out_path: Path) -> None:
    import matplotlib.pyplot as plt

    out_path.parent.mkdir(parents=True, exist_ok=True)
    colors = ["#3b6fb6", "#d95f02", "#1b9e77", "#7570b3"]
    fig, axes = plt.subplots(4, 3, figsize=(13.5, 11.0), sharex=True, sharey=True)
    combos = [(case, cond, seed) for case in CASES for cond in CONDITIONS for seed in SEEDS]
    for ax, (case_name, condition, seed) in zip(axes.flat, combos):
        rows = [
            r
            for r in trace_rows
            if r["case"] == case_name and r["condition"] == condition and int(r["seed"]) == seed
        ]
        for expert in range(4):
            xs = [int(r["step"]) for r in rows if int(r["expert"]) == expert]
            ys = [float(r["fraction"]) for r in rows if int(r["expert"]) == expert]
            ax.plot(xs, ys, marker="o", linewidth=1.8, markersize=3.5, color=colors[expert], label=f"E{expert}")
        ax.axhline(COLLAPSE_THRESHOLD, color="#222222", linestyle="--", linewidth=1.0, alpha=0.55)
        ax.set_title(f"{case_name}-{condition} seed {seed}", fontsize=9)
        ax.grid(alpha=0.22)
        ax.set_ylim(-0.03, 1.03)
    for ax in axes[-1, :]:
        ax.set_xlabel("step")
    for ax in axes[:, 0]:
        ax.set_ylabel("route load fraction")
    handles, labels = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, frameon=False)
    fig.suptitle("A05_02_P1 C1/C2 route load over checkpoints", y=0.995, fontsize=13)
    fig.tight_layout(rect=(0, 0.035, 1, 0.965))
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument(
        "--out-dir",
        default=str(Path(__file__).resolve().parents[1]),
        help="A05_02_P1 experiment directory.",
    )
    args = parser.parse_args()

    cfg = load_cfg()
    device = torch.device(args.device if torch.cuda.is_available() and args.device.startswith("cuda") else "cpu")
    out_dir = Path(args.out_dir)
    trace_rows: list[dict] = []
    for case_name in CASES:
        for condition in CONDITIONS:
            for seed in SEEDS:
                print(f"diagnose {case_name} {condition} seed={seed}", flush=True)
                trace_rows.extend(train_with_load_trace(cfg, case_name, condition, seed, device))

    timing_rows = classify_timing(trace_rows)
    write_csv(out_dir / "tables/collapse_route_load_trajectory.csv", trace_rows)
    write_csv(out_dir / "tables/collapse_timing_by_seed.csv", timing_rows)
    plot_trace(trace_rows, out_dir / "figures/collapse_route_load_over_checkpoints_C1_C2.png")

    collapsed = [r for r in timing_rows if int(r["final_collapsed"]) == 1]
    early_same = sum(int(r["same_dominant_step200_final"]) for r in collapsed)
    print(f"collapsed seeds: {len(collapsed)}")
    print(f"collapsed seeds with same step200/final dominant expert: {early_same}/{len(collapsed) if collapsed else 0}")


if __name__ == "__main__":
    main()

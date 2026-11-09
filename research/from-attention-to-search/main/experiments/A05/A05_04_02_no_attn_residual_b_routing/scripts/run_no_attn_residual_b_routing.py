#!/usr/bin/env python3
"""No-attention-residual audit for B-position top-1 MoE routing."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import os
import random
import sys
from collections import defaultdict
from multiprocessing import get_context
from pathlib import Path
from types import MethodType
from typing import Any

import torch

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

EXP_DIR = Path(__file__).resolve().parents[1]
RESEARCH_ROOT = EXP_DIR.parents[4]
ROUND1_EXP = RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A05/A05_04_01_round1_slot_specialization_protocol_dot_product"
ROUND1_RUN = ROUND1_EXP / "results/round1_slot_specialization_dot_product_4gpu_20260609"
ROUND1_SCRIPT = ROUND1_EXP / "scripts/run_round1_slot_specialization_protocol_dot_product.py"

spec1 = importlib.util.spec_from_file_location("round1dot", ROUND1_SCRIPT)
round1 = importlib.util.module_from_spec(spec1)
assert spec1.loader is not None
sys.modules["round1dot"] = round1
spec1.loader.exec_module(round1)

SEEDS = [20260521, 20260522, 20260523, 20260524, 20260525, 20260526, 20260527, 20260528]
VARIANT = "NoAttnResidual_B_baseline"
ROUTER_METRIC = "dot_product"


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


def mean_float(rows: list[dict[str, Any]], key: str) -> float:
    vals = [float(row[key]) for row in rows if row.get(key, "") != ""]
    return sum(vals) / len(vals) if vals else float("nan")


def cfg_for(args: argparse.Namespace) -> dict[str, Any]:
    cfg = round1.default_cfg()
    cfg["model"]["router_metric"] = ROUTER_METRIC
    cfg["model"]["router_temperature"] = 1.0
    cfg["training"]["steps"] = int(args.train_steps)
    cfg["training"]["batch_size"] = int(args.batch_size)
    cfg["data"]["train_repeats_per_pair"] = int(args.train_repeats_per_pair)
    cfg["data"]["eval_repeats_per_pair"] = int(args.eval_repeats_per_pair)
    cfg["evaluation"]["batch_size"] = int(args.eval_batch_size)
    cfg["intervention"] = {
        "name": "no_attention_residual_into_router_input",
        "standard_router_input": "LN(x + attention_output)",
        "intervened_router_input": "LN(attention_output)",
        "post_moe_residual_kept": True,
    }
    return cfg


def install_no_attn_residual_forward(model: torch.nn.Module) -> None:
    def forward_no_attn_residual(
        self: torch.nn.Module,
        idx: torch.Tensor,
        return_acts: bool = False,
        ablate_expert: int | None = None,
        force_expert_idx: torch.Tensor | None = None,
    ):
        bsz, width = idx.shape
        pos = torch.arange(width, device=idx.device).unsqueeze(0).expand(bsz, width)
        x = self.token_emb(idx) + self.pos_emb(pos)
        mask = torch.triu(torch.ones(width, width, device=idx.device, dtype=torch.bool), diagonal=1)
        attn_out, _ = self.attn(x, x, x, attn_mask=mask, need_weights=False)
        x = self.ln1(self.dropout(attn_out))
        moe_input = x
        moe_out, info = self.moe(x, ablate_expert=ablate_expert, force_expert_idx=force_expert_idx)
        hidden = self.ln2(x + self.dropout(moe_out))
        logits = self.lm_head(hidden)
        if return_acts:
            info["ffn_input"] = moe_input
            info["hidden"] = hidden
        return logits, info

    model.forward = MethodType(forward_no_attn_residual, model)


def make_model(cfg: dict[str, Any], device: torch.device) -> torch.nn.Module:
    model = round1.make_model(cfg, ROUTER_METRIC, device)
    install_no_attn_residual_forward(model)
    return model


def eval_steps_for(cfg: dict[str, Any], run_stage: str) -> list[int]:
    steps = int(cfg["training"]["steps"] if run_stage == "full" else min(40, cfg["training"]["steps"]))
    return sorted({0, 1, 2, 5, 10, 20, 50, steps})


def train_one(cfg: dict[str, Any], seed: int, out_root: str, run_stage: str, device_id: int | None) -> None:
    device = torch.device(f"cuda:{device_id}" if device_id is not None and torch.cuda.is_available() else "cpu")
    random.seed(seed)
    torch.manual_seed(seed + 4404)
    run_dir = Path(out_root) / ROUTER_METRIC / VARIANT / f"seed_{seed}"
    ckpt_dir = run_dir / "checkpoint_artifacts"
    run_dir.mkdir(parents=True, exist_ok=True)
    model = make_model(cfg, device)
    steps = int(cfg["training"]["steps"] if run_stage == "full" else min(40, cfg["training"]["steps"]))
    train_repeats = int(cfg["data"]["train_repeats_per_pair"] if run_stage == "full" else min(8, cfg["data"]["train_repeats_per_pair"]))
    train_data = round1.balanced_dataset(cfg, train_repeats, seed, "train")
    batch_size = int(cfg["training"]["batch_size"])
    opt = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad],
        lr=float(cfg["training"]["lr"]),
        weight_decay=float(cfg["training"]["weight_decay"]),
    )
    rng = random.Random(seed + 404)
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
        out = round1.eval_model(model, cfg, VARIANT, ROUTER_METRIC, seed, step, device, artifact)
        out["metrics"]["direct_attention_residual_enabled"] = 0
        out["metrics"]["post_moe_residual_kept"] = 1
        metric_rows.append(out["metrics"])
        route_rows.extend(out["route_rows"])
        acc_slot_rows.extend(out["accuracy_by_slot_rows"])
        acc_pos_rows.extend(out["accuracy_by_block_start_rows"])
        probe_rows.append(out["p2_probe_row"])
        margin_rows.extend(out["p3_margin_rows"])
        print(
            f"EVAL {VARIANT} seed={seed} step={step} "
            f"nmi={out['metrics']['slot_to_expert_NMI']:.3f} "
            f"max={out['metrics']['max_load']:.3f} "
            f"acc={out['metrics']['target_accuracy']:.3f}",
            flush=True,
        )

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
        logits, _ = model(sub.x.to(device), return_acts=True)
        loss = round1.target_loss(logits, sub)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(cfg["training"]["grad_clip"]))
        opt.step()
        if step == 1 or step % int(cfg["training"]["log_every"]) == 0 or step == steps:
            train_rows.append({
                "variant": VARIANT,
                "router_metric": ROUTER_METRIC,
                "seed": seed,
                "step": step,
                "target_ce": float(loss.detach().cpu().item()),
            })
        if step in eval_steps:
            collect(step)
            model.train()

    write_json(run_dir / "init_meta.json", {
        "seed": seed,
        "variant": VARIANT,
        "direct_attention_residual_enabled": False,
        "post_moe_residual_kept": True,
    })
    write_csv(run_dir / "metrics_by_step.csv", metric_rows)
    write_csv(run_dir / "route_confusion_by_step.csv", route_rows)
    write_csv(run_dir / "accuracy_by_slot.csv", acc_slot_rows)
    write_csv(run_dir / "accuracy_by_block_start.csv", acc_pos_rows)
    write_csv(run_dir / "p2_probe_metrics_by_checkpoint.csv", probe_rows)
    write_csv(run_dir / "p3_margin_decomposition_by_checkpoint.csv", margin_rows)
    write_csv(run_dir / "training_curve.csv", train_rows)


def aggregate(out_dir: Path, fig_dir: Path, run_name: str, run_stage: str) -> None:
    raw = out_dir / "raw"
    metrics: list[dict[str, Any]] = []
    routes: list[dict[str, Any]] = []
    margins: list[dict[str, Any]] = []
    train_rows: list[dict[str, Any]] = []
    for path in sorted(raw.glob(f"{ROUTER_METRIC}/{VARIANT}/seed_*/metrics_by_step.csv")):
        metrics.extend(read_csv(path))
    for path in sorted(raw.glob(f"{ROUTER_METRIC}/{VARIANT}/seed_*/route_confusion_by_step.csv")):
        routes.extend(read_csv(path))
    for path in sorted(raw.glob(f"{ROUTER_METRIC}/{VARIANT}/seed_*/p3_margin_decomposition_by_checkpoint.csv")):
        margins.extend(read_csv(path))
    for path in sorted(raw.glob(f"{ROUTER_METRIC}/{VARIANT}/seed_*/training_curve.csv")):
        train_rows.extend(read_csv(path))

    write_csv(out_dir / "metrics_by_step.csv", metrics)
    write_csv(out_dir / "route_confusion_by_step.csv", routes)
    write_csv(out_dir / "margin_decomposition_by_step.csv", margins)
    write_csv(out_dir / "training_curve.csv", train_rows)

    max_step: dict[tuple[str, str, str], int] = {}
    for row in metrics:
        key = (row["router_metric"], row["variant"], row["seed"])
        max_step[key] = max(max_step.get(key, -1), int(row["step"]))
    finals = [row for row in metrics if int(row["step"]) == max_step[(row["router_metric"], row["variant"], row["seed"])]]
    write_csv(out_dir / "final_metrics_by_seed.csv", finals)

    reference = []
    for row in read_csv(ROUND1_RUN / "final_metrics_by_seed.csv"):
        if row.get("router_metric") == ROUTER_METRIC and row.get("variant") == "P1_clean_baseline":
            reference.append(row)
    write_csv(out_dir / "reference_round1_p1_clean_baseline_final_metrics.csv", reference)

    make_figures(out_dir, fig_dir)
    write_reports(out_dir, fig_dir, run_name, run_stage, finals, reference)


def make_figures(out_dir: Path, fig_dir: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig_dir.mkdir(parents=True, exist_ok=True)
    finals = read_csv(out_dir / "final_metrics_by_seed.csv")
    reference = read_csv(out_dir / "reference_round1_p1_clean_baseline_final_metrics.csv")
    groups = [
        ("Round1_P1_standard", reference),
        (VARIANT, finals),
    ]
    fig, ax = plt.subplots(figsize=(7, 4))
    xs = list(range(len(groups)))
    nmis = [mean_float(rows, "slot_to_expert_NMI") for _, rows in groups]
    loads = [mean_float(rows, "max_load") for _, rows in groups]
    ax.bar([x - 0.18 for x in xs], nmis, width=0.36, label="slot NMI")
    ax.bar([x + 0.18 for x in xs], loads, width=0.36, label="max load")
    ax.set_xticks(xs, [name for name, _ in groups], rotation=15, ha="right")
    ax.set_ylim(0, 1.05)
    ax.set_title("Final routing: standard residual vs no attention residual")
    ax.legend()
    fig.tight_layout()
    fig.savefig(fig_dir / "final_routing_standard_vs_no_attn_residual.png", dpi=180)
    plt.close(fig)


def format_group(name: str, rows: list[dict[str, Any]]) -> str:
    if not rows:
        return f"- {name}: no rows."
    return (
        f"- {name}: NMI {mean_float(rows, 'slot_to_expert_NMI'):.3f}, "
        f"max_load {mean_float(rows, 'max_load'):.3f}, "
        f"active_experts {mean_float(rows, 'active_experts'):.3f}, "
        f"accuracy {mean_float(rows, 'target_accuracy'):.3f}"
    )


def write_reports(
    out_dir: Path,
    fig_dir: Path,
    run_name: str,
    run_stage: str,
    finals: list[dict[str, Any]],
    reference: list[dict[str, Any]],
) -> None:
    figure_rel = Path(os.path.relpath(fig_dir / "final_routing_standard_vs_no_attn_residual.png", out_dir))
    summary = "\n".join([
        "# A05_04_02 No-Attention-Residual B-Routing Summary",
        "",
        "## Conclusion",
        "",
        "Pending full-run interpretation. This run tests whether removing the direct attention-block residual into the router input improves B-position slot specialization.",
        "",
        "## Purpose",
        "",
        "Test whether `x_B` in `h_B = LN(x_B + attention_output_B)` is a major common source for dot-product top-1 routing collapse.",
        "",
        "## How",
        "",
        "- Data: original `SLOT_s B_CONST Y_s` task.",
        "- Intervention: use `h = LN(attention_output)` as the MoE/router input.",
        "- Kept fixed: no positional encoding, dot-product router, sparse top-1 routing, B-position loss and routing metrics, post-MoE residual.",
        "",
        "## Metrics",
        "",
        format_group("Round1_P1_standard_reference", reference),
        format_group(VARIANT, finals),
        "",
        "## Figure",
        "",
        f"![Final routing]({figure_rel})",
        "",
        "## Claim Boundary",
        "",
        "This removes only the attention-block residual into the router input, not every residual connection. A positive result supports the direct B residual as a causal contributor, but does not identify the full common source.",
    ])
    (out_dir / "summary.md").write_text(summary + "\n", encoding="utf-8")

    detailed = "\n".join([
        "# A05_04_02 No-Attention-Residual B-Routing Detailed Record",
        "",
        "## 0. Quick Recap",
        "",
        "Purpose: test whether direct residual identity at the B-routed position causes common-logit dominance.",
        "",
        "Hypothesis: removing `x_B` from the router input should reduce collapse and improve route-slot NMI.",
        "",
        "Experiment logic: keep the original B task, but replace `LN(x + attention_output)` with `LN(attention_output)` before the MoE/router.",
        "",
        "Conclusion: see `summary.md` after full run.",
        "",
        "Evidence: `final_metrics_by_seed.csv`, `metrics_by_step.csv`, `route_confusion_by_step.csv`, `margin_decomposition_by_step.csv`.",
        "",
        "## Source Files",
        "",
        "- Protocol: `protocol_for_approval.md`",
        "- Runner: `scripts/run_no_attn_residual_b_routing.py`",
        "- Reference Round-1 run: `A05_04_01_round1_slot_specialization_protocol_dot_product/results/round1_slot_specialization_dot_product_4gpu_20260609`",
        "",
        "## Run Metadata",
        "",
        f"- Run name: `{run_name}`",
        f"- Run stage: `{run_stage}`",
        "- Seeds: 20260521-20260528 for full stage.",
        "- Checkpoints: 0, 1, 2, 5, 10, 20, 50, final.",
        "",
        "## Intervention",
        "",
        "- Standard router input: `h = LN(x + attention_output)`.",
        "- Intervened router input: `h = LN(attention_output)`.",
        "- Post-MoE residual is kept: `hidden = LN(h + MoE(h))`.",
        "",
        "## Final Aggregate",
        "",
        format_group("Round1_P1_standard_reference", reference),
        format_group(VARIANT, finals),
        "",
        "## Artifact Map",
        "",
        "- Final metrics: `final_metrics_by_seed.csv`",
        "- Step metrics: `metrics_by_step.csv`",
        "- Route confusion: `route_confusion_by_step.csv`",
        "- Margin decomposition: `margin_decomposition_by_step.csv`",
        "- Training curve: `training_curve.csv`",
        "- Reference metrics: `reference_round1_p1_clean_baseline_final_metrics.csv`",
        f"- Figure dir: `{fig_dir}`",
        "- Raw per-seed outputs: `raw/dot_product/NoAttnResidual_B_baseline/seed_<seed>/`",
    ])
    (out_dir / "detailed.md").write_text(detailed + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=str(EXP_DIR))
    parser.add_argument("--run-name", default="no_attn_residual_b_routing_4gpu_20260610")
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
        "experiment": "A05_04_02_no_attn_residual_b_routing",
        "primary_anchor": "Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_02_dotproduct_common_logit_causality_anchor.md",
        "run_name": args.run_name,
        "run_stage": args.run_stage,
        "scope": ["NoAttnResidual_B_baseline"],
        "source_protocol": "main/experiments/A05/A05_04_02_no_attn_residual_b_routing/protocol_for_approval.md",
    })

    seeds = SEEDS[:1] if args.run_stage == "smoke" else SEEDS
    raw_dir = out_dir / "raw"
    if args.parallel and int(args.max_parallel) > 1:
        ctx = get_context("spawn")
        worker_args = [(cfg, seed, str(raw_dir), args.run_stage, idx % int(args.max_parallel)) for idx, seed in enumerate(seeds)]
        with ctx.Pool(processes=int(args.max_parallel)) as pool:
            pool.starmap(train_one, worker_args)
    else:
        for idx, seed in enumerate(seeds):
            train_one(cfg, seed, str(raw_dir), args.run_stage, idx % max(1, int(args.max_parallel)))

    aggregate(out_dir, fig_dir, args.run_name, args.run_stage)
    write_json(out_dir / "run_summary.json", {
        "status": "completed",
        "result_dir": str(out_dir),
        "figure_dir": str(fig_dir),
    })


if __name__ == "__main__":
    main()

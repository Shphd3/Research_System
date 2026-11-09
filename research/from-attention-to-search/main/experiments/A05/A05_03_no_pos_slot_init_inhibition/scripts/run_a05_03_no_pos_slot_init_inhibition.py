#!/usr/bin/env python3
"""Run A05_03 no-position slot-init / inhibition supplement.

This wrapper reuses the H0605a runner but forces positional embeddings to zero
and freezes them for every model construction, including slot-init calibration.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from multiprocessing import get_context
from pathlib import Path
from typing import Any

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import torch


EXP_DIR = Path(__file__).resolve().parents[1]
RESEARCH_ROOT = EXP_DIR.parents[4]
WORKSPACE = (
    RESEARCH_ROOT
    / "Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding"
)

sys.path.insert(0, str(WORKSPACE / "scripts"))
sys.path.insert(0, str(WORKSPACE / "src"))

import run_h0605a_true_token_conditioned_inhibition_replay as runner  # noqa: E402


DEFAULT_CONDITIONS = [
    "R0-dot",
    "S0-dot",
    "R1-dot",
    "S1-dot",
    "R0-cos",
    "S0-cos",
    "R1-cos",
    "S1-cos",
]

_ORIGINAL_MAKE_CONDITION_MODEL = runner.make_condition_model


def parse_list(raw: str | None, default: list[str]) -> list[str]:
    if not raw:
        return default
    return [part.strip() for part in raw.replace(" ", ",").split(",") if part.strip()]


def write_json(path: Path, obj: dict[str, Any]) -> None:
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


def safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def mean_std(vals: list[float]) -> tuple[float, float]:
    vals = [v for v in vals if not math.isnan(v)]
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) == 1:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / len(vals)
    return mean, math.sqrt(var)


def make_no_pos_condition_model(condition: str, cfg: dict, device: torch.device) -> torch.nn.Module:
    model = _ORIGINAL_MAKE_CONDITION_MODEL(condition, cfg, device)
    if not hasattr(model, "pos_emb"):
        raise AttributeError("expected SparseTinyTransformer.pos_emb for no-position ablation")
    with torch.no_grad():
        model.pos_emb.weight.zero_()
    model.pos_emb.weight.requires_grad_(False)
    return model


def install_no_position_patch() -> None:
    runner.make_condition_model = make_no_pos_condition_model


def train_no_pos_condition_seed(
    cfg: dict,
    condition: str,
    mode: str,
    seed: int,
    run_stage: str,
    out_dir: str,
    device_id: int | None,
    trajectory: bool = False,
) -> None:
    install_no_position_patch()
    runner.train_condition_seed(cfg, condition, mode, seed, run_stage, out_dir, device_id, trajectory)


def apply_overrides(cfg: dict, args: argparse.Namespace) -> dict:
    cfg = json.loads(json.dumps(cfg))
    if args.train_steps:
        cfg["training"]["steps"] = int(args.train_steps)
    if args.smoke_steps:
        cfg["training"]["smoke_steps"] = int(args.smoke_steps)
    if args.train_samples_per_slot:
        cfg["data"]["train_samples_per_slot"] = int(args.train_samples_per_slot)
    if args.eval_samples_per_slot:
        cfg["data"]["eval_samples_per_slot"] = int(args.eval_samples_per_slot)
    if args.batch_size:
        cfg["training"]["batch_size"] = int(args.batch_size)
    if args.eval_batch_size:
        cfg["evaluation"]["batch_size"] = int(args.eval_batch_size)
    if args.variants_per_key:
        cfg.setdefault("feature_key_eval", {})["variants_per_key"] = int(args.variants_per_key)
    return cfg


def aggregate_slot_feature_rows(result_dir: Path) -> list[dict[str, Any]]:
    raw = read_csv(result_dir / "feature_key_route_matrix.csv")
    grouped: dict[tuple[str, str, int, int, int, int], int] = defaultdict(int)
    for row in raw:
        key = (
            row["mode"],
            row["condition"],
            int(row["seed"]),
            int(row["step"]),
            int(row["slot"]),
            int(row["expert"]),
        )
        grouped[key] += int(float(row["count"]))
    denom: dict[tuple[str, str, int, int, int], int] = defaultdict(int)
    for (mode, condition, seed, step, slot, expert), count in grouped.items():
        denom[(mode, condition, seed, step, slot)] += count
    rows: list[dict[str, Any]] = []
    for (mode, condition, seed, step, slot, expert), count in sorted(grouped.items()):
        total = denom[(mode, condition, seed, step, slot)]
        rows.append(
            {
                "mode": mode,
                "condition": condition,
                "seed": seed,
                "step": step,
                "slot": slot,
                "expert": expert,
                "count": count,
                "fraction": count / total if total else math.nan,
            }
        )
    return rows


def final_feature_metrics_by_seed(result_dir: Path) -> list[dict[str, Any]]:
    rows = read_csv(result_dir / "feature_key_consistency_by_seed.csv")
    max_step: dict[tuple[str, str, int], int] = {}
    for row in rows:
        key = (row["mode"], row["condition"], int(row["seed"]))
        max_step[key] = max(max_step.get(key, -1), int(row["step"]))
    out = []
    for row in rows:
        key = (row["mode"], row["condition"], int(row["seed"]))
        if int(row["step"]) == max_step.get(key, -1):
            out.append(dict(row))
    return out


def write_decision_tables(result_dir: Path, table_dir: Path, conditions: list[str]) -> None:
    table_dir.mkdir(parents=True, exist_ok=True)
    seed_rows = read_csv(result_dir / "summary_by_seed.csv")
    final_feature = final_feature_metrics_by_seed(result_dir)
    feature_by_key = {
        (row["mode"], row["condition"], int(row["seed"])): row
        for row in final_feature
    }

    decision_rows: list[dict[str, Any]] = []
    for row in seed_rows:
        key = (row["mode"], row["condition"], int(row["seed"]))
        frow = feature_by_key.get(key, {})
        decision_rows.append(
            {
                "mode": row["mode"],
                "condition": row["condition"],
                "seed": int(row["seed"]),
                "router_metric": "cosine" if row["condition"].endswith("-cos") else "dot_product",
                "slot_init": int(row["condition"].startswith("S")),
                "inhibition": int(row["condition"].split("-", 1)[0].endswith("1")),
                "nmi_route_slot_final_eval": safe_float(row.get("nmi_route_slot")),
                "route_slot_nmi_feature_eval": safe_float(row.get("route_slot_nmi_feature_eval")),
                "route_feature_key_nmi": safe_float(row.get("route_feature_key_nmi")),
                "feature_key_consistency": safe_float(row.get("feature_key_consistency")),
                "expert_load_max_fraction": safe_float(row.get("expert_load_max_fraction")),
                "active_experts": safe_float(row.get("active_experts")),
                "target_accuracy_feature_eval": safe_float(row.get("target_accuracy_feature_eval")),
                "within_slot_main_expert_diversity": safe_float(row.get("within_slot_main_expert_diversity")),
                "final_step": int(float(frow.get("step", 0))) if frow else "",
            }
        )
    write_csv(table_dir / "primary_metrics_by_seed.csv", decision_rows)

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in decision_rows:
        grouped[row["condition"]].append(row)
    summary_rows: list[dict[str, Any]] = []
    for condition in conditions:
        rows = grouped.get(condition, [])
        if not rows:
            continue
        out: dict[str, Any] = {
            "condition": condition,
            "num_seeds": len(rows),
            "router_metric": rows[0]["router_metric"],
            "slot_init": rows[0]["slot_init"],
            "inhibition": rows[0]["inhibition"],
        }
        for field in [
            "route_slot_nmi_feature_eval",
            "route_feature_key_nmi",
            "feature_key_consistency",
            "expert_load_max_fraction",
            "active_experts",
            "target_accuracy_feature_eval",
            "within_slot_main_expert_diversity",
        ]:
            vals = [safe_float(r[field]) for r in rows]
            mean, std = mean_std(vals)
            out[f"{field}_mean"] = mean
            out[f"{field}_std"] = std
            valid = [v for v in vals if not math.isnan(v)]
            out[f"{field}_min"] = min(valid) if valid else math.nan
            out[f"{field}_max"] = max(valid) if valid else math.nan
        summary_rows.append(out)
    write_csv(table_dir / "primary_metrics_summary.csv", summary_rows)


def plot_slot_heatmaps(result_dir: Path, fig_dir: Path, conditions: list[str], seeds: list[int]) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:
        print(f"slot heatmap skipped: {exc}", flush=True)
        return

    slot_rows = aggregate_slot_feature_rows(result_dir)
    table_dir = result_dir / "tables"
    write_csv(table_dir / "slot_route_matrix_by_step_from_feature_eval.csv", slot_rows)
    if not slot_rows:
        return

    metrics = {
        (row["mode"], row["condition"], int(row["seed"]), int(row["step"])): row
        for row in read_csv(result_dir / "feature_key_consistency_by_seed.csv")
    }
    modes = sorted({row["mode"] for row in slot_rows})
    final_step: dict[tuple[str, str, int], int] = {}
    for row in slot_rows:
        key = (row["mode"], row["condition"], int(row["seed"]))
        final_step[key] = max(final_step.get(key, -1), int(row["step"]))

    heat_dir = fig_dir / "slot_level_heatmaps"
    heat_dir.mkdir(parents=True, exist_ok=True)
    by_key: dict[tuple[str, str, int, int], list[dict[str, Any]]] = defaultdict(list)
    for row in slot_rows:
        by_key[(row["mode"], row["condition"], int(row["seed"]), int(row["step"]))].append(row)

    def matrix_for(key: tuple[str, str, int, int]) -> torch.Tensor:
        rows = by_key.get(key, [])
        max_slot = max([int(r["slot"]) for r in rows], default=3)
        max_expert = max([int(r["expert"]) for r in rows], default=3)
        mat = torch.zeros(max_slot + 1, max_expert + 1)
        for r in rows:
            mat[int(r["slot"]), int(r["expert"])] = float(r["fraction"])
        return mat

    def metric_text(mode: str, condition: str, seed: int, step: int) -> str:
        row = metrics.get((mode, condition, seed, step), {})
        if not row:
            return ""
        return (
            f"NMI={safe_float(row.get('route_slot_nmi_feature_eval')):.3f}, "
            f"max={safe_float(row.get('expert_load_max_fraction')):.3f}, "
            f"acc={safe_float(row.get('target_accuracy_feature_eval')):.3f}"
        )

    for mode in modes:
        for condition in conditions:
            for seed in seeds:
                steps = [0]
                fstep = final_step.get((mode, condition, seed))
                if fstep is not None and fstep >= 0 and fstep not in steps:
                    steps.append(fstep)
                for step in steps:
                    key = (mode, condition, seed, step)
                    if key not in by_key:
                        continue
                    mat = matrix_for(key)
                    fig, ax = plt.subplots(figsize=(4.2, 3.4))
                    im = ax.imshow(mat.numpy(), cmap="viridis", vmin=0.0, vmax=1.0, aspect="auto")
                    ax.set_title(f"{condition} seed {seed} step {step}\n{metric_text(mode, condition, seed, step)}", fontsize=9)
                    ax.set_xlabel("Expert")
                    ax.set_ylabel("Slot")
                    ax.set_xticks(range(mat.shape[1]))
                    ax.set_yticks(range(mat.shape[0]))
                    for i in range(mat.shape[0]):
                        for j in range(mat.shape[1]):
                            val = float(mat[i, j])
                            ax.text(j, i, f"{val:.2f}", ha="center", va="center", color="white" if val > 0.45 else "black", fontsize=8)
                    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
                    fig.tight_layout()
                    fname = f"{mode}_{condition}_seed_{seed}_step_{step}.png".replace("/", "_")
                    fig.savefig(heat_dir / fname, dpi=180)
                    plt.close(fig)

        # One overview figure per mode and step class, preserving seed-level panels.
        for step_name in ["step0", "final"]:
            keys: list[tuple[str, str, int, int]] = []
            for condition in conditions:
                for seed in seeds:
                    step = 0 if step_name == "step0" else final_step.get((mode, condition, seed), -1)
                    key = (mode, condition, seed, step)
                    if step >= 0 and key in by_key:
                        keys.append(key)
            if not keys:
                continue
            n_rows = len(conditions)
            n_cols = len(seeds)
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(3.2 * n_cols, 2.65 * n_rows), squeeze=False)
            for ax in axes.ravel():
                ax.axis("off")
            for r, condition in enumerate(conditions):
                for c, seed in enumerate(seeds):
                    step = 0 if step_name == "step0" else final_step.get((mode, condition, seed), -1)
                    key = (mode, condition, seed, step)
                    ax = axes[r][c]
                    ax.axis("on")
                    if key not in by_key:
                        ax.set_title(f"{condition} seed {seed}\nmissing", fontsize=8)
                        ax.set_xticks([])
                        ax.set_yticks([])
                        continue
                    mat = matrix_for(key)
                    ax.imshow(mat.numpy(), cmap="viridis", vmin=0.0, vmax=1.0, aspect="auto")
                    ax.set_title(f"{condition} s{seed}\n{metric_text(mode, condition, seed, step)}", fontsize=7)
                    ax.set_xticks(range(mat.shape[1]))
                    ax.set_yticks(range(mat.shape[0]))
                    ax.tick_params(labelsize=7)
                    for i in range(mat.shape[0]):
                        for j in range(mat.shape[1]):
                            val = float(mat[i, j])
                            ax.text(j, i, f"{val:.2f}", ha="center", va="center", color="white" if val > 0.45 else "black", fontsize=6)
            fig.suptitle(f"No-position slot-level route heatmaps ({mode}, {step_name})", fontsize=12)
            fig.tight_layout(rect=[0, 0, 1, 0.985])
            fig.savefig(heat_dir / f"{mode}_slot_level_heatmaps_{step_name}.png", dpi=180)
            plt.close(fig)


def run_task(args: argparse.Namespace) -> None:
    install_no_position_patch()
    cfg = apply_overrides(runner.load_json(args.config), args)
    if args.run_stage == "smoke":
        cfg["trajectory"]["eval_samples_per_slot"] = min(64, int(cfg.get("trajectory", {}).get("eval_samples_per_slot", 256)))

    modes = parse_list(args.modes, ["multi_b_primary"])
    conditions = parse_list(args.conditions, DEFAULT_CONDITIONS)
    seeds = [int(v) for v in parse_list(args.seeds, [str(v) for v in cfg["seeds"]])]
    if args.run_stage == "smoke":
        seeds = seeds[:1]

    output_dir = Path(args.output_dir).resolve()
    result_dir = output_dir / "results" / args.run_name
    fig_dir = output_dir / "figures" / args.run_name
    table_dir = result_dir / "tables"
    result_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    table_dir.mkdir(parents=True, exist_ok=True)

    write_json(result_dir / "resolved_config.json", cfg)
    write_json(
        result_dir / "run_manifest.json",
        {
            "experiment": "A05_03_no_pos_slot_init_inhibition",
            "run_name": args.run_name,
            "position_intervention": "pos_emb.weight is zeroed and frozen from initialization for all models",
            "config": str(Path(args.config).resolve()),
            "modes": modes,
            "conditions": conditions,
            "seeds": seeds,
            "run_stage": args.run_stage,
            "trajectory": bool(args.trajectory),
            "result_dir": str(result_dir),
            "figure_dir": str(fig_dir),
        },
    )

    audits = [runner.data_audit(cfg, mode) for mode in modes]
    write_json(result_dir / "data_audit.json", {"audits": audits})
    if not all(a["distinct_targets_per_b"] and a["scheme_b_no_single_position_identifies_slot"] and a["vocab_sufficient"] for a in audits):
        raise RuntimeError(f"data audit failed: {audits}")

    device_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
    max_parallel = int(args.max_parallel or max(1, device_count))
    jobs = [(mode, condition, seed) for mode in modes for condition in conditions for seed in seeds]
    print(
        f"RUN_NAME={args.run_name} stage={args.run_stage} jobs={len(jobs)} "
        f"cuda_devices={device_count} max_parallel={max_parallel}",
        flush=True,
    )

    if args.parallel and len(jobs) > 1 and max_parallel > 1:
        ctx = get_context("spawn")
        active: list[tuple[Any, tuple[str, str, int]]] = []
        for job_idx, (mode, condition, seed) in enumerate(jobs):
            while len(active) >= max_parallel:
                proc, meta = active.pop(0)
                proc.join()
                if proc.exitcode != 0:
                    raise RuntimeError(f"worker failed {meta} exit={proc.exitcode}")
            device_id = job_idx % max(1, min(device_count, max_parallel)) if device_count else None
            proc = ctx.Process(
                target=train_no_pos_condition_seed,
                args=(cfg, condition, mode, seed, args.run_stage, str(result_dir), device_id, args.trajectory),
            )
            proc.start()
            active.append((proc, (mode, condition, seed)))
        for proc, meta in active:
            proc.join()
            if proc.exitcode != 0:
                raise RuntimeError(f"worker failed {meta} exit={proc.exitcode}")
    else:
        for job_idx, (mode, condition, seed) in enumerate(jobs):
            device_id = job_idx % device_count if device_count else None
            train_no_pos_condition_seed(cfg, condition, mode, seed, args.run_stage, str(result_dir), device_id, args.trajectory)

    runner.aggregate_run(result_dir, fig_dir, modes, conditions, seeds)
    write_decision_tables(result_dir, table_dir, conditions)
    plot_slot_heatmaps(result_dir, fig_dir, conditions, seeds)
    print(f"completed result_dir={result_dir} figure_dir={fig_dir}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=EXP_DIR)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--run-stage", choices=["smoke", "full"], default="full")
    parser.add_argument("--modes", default="")
    parser.add_argument("--conditions", default="")
    parser.add_argument("--seeds", default="")
    parser.add_argument("--parallel", action="store_true")
    parser.add_argument("--max-parallel", type=int, default=0)
    parser.add_argument("--trajectory", action="store_true")
    parser.add_argument("--train-steps", type=int, default=0)
    parser.add_argument("--smoke-steps", type=int, default=0)
    parser.add_argument("--train-samples-per-slot", type=int, default=0)
    parser.add_argument("--eval-samples-per-slot", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=0)
    parser.add_argument("--eval-batch-size", type=int, default=0)
    parser.add_argument("--variants-per-key", type=int, default=0)
    args = parser.parse_args()
    run_task(args)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Summarize A06_02_02 freeze-split results into compact decision tables."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()

    run_dir = args.run_dir
    results = run_dir / "results"
    tables = run_dir / "tables"
    tables.mkdir(parents=True, exist_ok=True)

    trajectory = pd.read_csv(results / "trajectory_metrics.csv")
    gradients = pd.read_csv(results / "gradient_metrics.csv")
    replay = pd.read_csv(results / "replay_metrics.csv")
    fractions = pd.read_csv(results / "replay_fraction_summary.csv")

    grad0 = (
        gradients[gradients["after_backward_step"] == 0]
        .groupby("variant")[["router_grad_norm", "expert_grad_norm", "other_grad_norm"]]
        .mean()
        .reset_index()
    )
    grad0.to_csv(tables / "gradient_freeze_sanity.csv", index=False)

    traj_rows = []
    for variant, sub in trajectory[trajectory["layer"] == 5].groupby("variant"):
        by_step = sub.groupby("step").mean(numeric_only=True)
        row = {"variant": variant, "layer": 5}
        for step in [0, 10, 300]:
            if step in by_step.index:
                for metric in ["common_margin", "raw_max_load", "centered_max_load", "delta_max_load", "dominance_ratio"]:
                    row[f"{metric}_step{step}"] = float(by_step.loc[step, metric])
        if 0 in by_step.index and 10 in by_step.index:
            row["common_margin_delta_0_10"] = row["common_margin_step10"] - row["common_margin_step0"]
            row["raw_max_load_delta_0_10"] = row["raw_max_load_step10"] - row["raw_max_load_step0"]
        traj_rows.append(row)
    traj_summary = pd.DataFrame(traj_rows)
    normal = traj_summary[traj_summary["variant"] == "normal"].iloc[0]
    traj_summary["common_margin_suppression_vs_normal_L5"] = 1.0 - (
        traj_summary["common_margin_delta_0_10"] / normal["common_margin_delta_0_10"]
    )
    traj_summary["raw_load_suppression_vs_normal_L5"] = 1.0 - (
        traj_summary["raw_max_load_delta_0_10"] / normal["raw_max_load_delta_0_10"]
    )
    traj_summary.to_csv(tables / "trajectory_l5_step_summary.csv", index=False)

    replay_rows = []
    for (variant, layer), sub in replay[replay["layer"].isin([3, 4, 5])].groupby(["variant", "layer"]):
        seed_rows = []
        for seed, ssub in sub.groupby("model_seed"):
            def val(a_step: int, b_step: int, metric: str) -> float:
                row = ssub[(ssub["replay_a_step"] == a_step) & (ssub["replay_b_step"] == b_step)]
                return float(row.iloc[0][metric])

            actual = val(10, 10, "common_margin") - val(0, 0, "common_margin")
            gate = val(10, 0, "common_margin") - val(0, 0, "common_margin")
            hidden = val(0, 10, "common_margin") - val(0, 0, "common_margin")
            interaction = actual - gate - hidden
            seed_rows.append(
                {
                    "variant": variant,
                    "model_seed": seed,
                    "layer": layer,
                    "A_actual": actual,
                    "A_gate": gate,
                    "A_hidden": hidden,
                    "A_interaction": interaction,
                    "raw_load_delta_0_10": val(10, 10, "raw_max_load") - val(0, 0, "raw_max_load"),
                    "centered_load_delta_0_10": val(10, 10, "centered_max_load") - val(0, 0, "centered_max_load"),
                    "delta_max_load_delta_0_10": val(10, 10, "delta_max_load") - val(0, 0, "delta_max_load"),
                }
            )
        replay_rows.extend(seed_rows)
    replay_by_seed = pd.DataFrame(replay_rows)
    replay_by_seed.to_csv(tables / "replay_decomposition_by_seed_l3_l5.csv", index=False)
    replay_mean = replay_by_seed.groupby(["variant", "layer"]).mean(numeric_only=True).reset_index()
    normal_l5 = replay_mean[(replay_mean["variant"] == "normal") & (replay_mean["layer"] == 5)].iloc[0]
    replay_mean["common_margin_suppression_vs_normal_L5"] = float("nan")
    replay_mean["raw_load_suppression_vs_normal_L5"] = float("nan")
    mask_l5 = replay_mean["layer"] == 5
    replay_mean.loc[mask_l5, "common_margin_suppression_vs_normal_L5"] = 1.0 - (
        replay_mean.loc[mask_l5, "A_actual"] / normal_l5["A_actual"]
    )
    replay_mean.loc[mask_l5, "raw_load_suppression_vs_normal_L5"] = 1.0 - (
        replay_mean.loc[mask_l5, "raw_load_delta_0_10"] / normal_l5["raw_load_delta_0_10"]
    )
    replay_mean.to_csv(tables / "replay_decomposition_mean_l3_l5.csv", index=False)

    fractions[fractions["layer"].isin([3, 4, 5])].to_csv(tables / "replay_fraction_l3_l5.csv", index=False)
    print(
        {
            "gradient_freeze_sanity": str(tables / "gradient_freeze_sanity.csv"),
            "trajectory_l5_step_summary": str(tables / "trajectory_l5_step_summary.csv"),
            "replay_decomposition_mean_l3_l5": str(tables / "replay_decomposition_mean_l3_l5.csv"),
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

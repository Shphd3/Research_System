from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    bottlenecks = pd.read_csv(args.run / "bottlenecks.csv")
    lofo = pd.read_csv(args.run / "leave_one_family_out_summary.csv")
    fixed = pd.read_csv(args.run / "fixed_c_bottlenecks.csv")
    cells = pd.read_csv(args.run / "cells.csv")
    overlap = pd.read_csv(args.run / "overlap_excluded_bottlenecks.csv")

    fixed_sign = (
        fixed.groupby(["regime", "panel", "layer"], as_index=False)
        .agg(fixed_c_sign_stable=("sign_stable_across_c", "all"))
    )
    matrix = (
        bottlenecks[
            [
                "regime",
                "panel",
                "layer",
                "observed",
                "simultaneous_lcb",
                "worst_task",
                "bootstrap_se",
            ]
        ]
        .merge(
            lofo[["regime", "panel", "layer", "sign_stable"]].rename(
                columns={"sign_stable": "lofo_sign_stable"}
            ),
            on=["regime", "panel", "layer"],
            validate="one_to_one",
        )
        .merge(fixed_sign, on=["regime", "panel", "layer"], validate="one_to_one")
    )
    matrix["simultaneously_robust"] = matrix["simultaneous_lcb"] > 0
    matrix.to_csv(args.output / "robustness_matrix.csv", index=False)

    cells["task_group"] = np.where(
        cells["task"].eq("P"),
        "parent",
        np.where(cells["task"].eq("J"), "joint", "conditional_fine"),
    )
    task_groups = (
        cells.groupby(["regime", "panel", "layer", "task_group"], as_index=False)
        .agg(
            mean_balanced_accuracy=("balanced_accuracy", "mean"),
            mean_q05_margin=("margin_q05", "mean"),
            minimum_task_q05_margin=("margin_q05", "min"),
            mean_nonpositive_margin_rate=("nonpositive_margin_rate", "mean"),
        )
    )
    task_groups.to_csv(args.output / "task_group_summary.csv", index=False)

    common_rows = []
    for regime in ("POOLED_MATCHED_A", "POOLED_FULL_A"):
        for layer in sorted(matrix["layer"].unique()):
            current = matrix[(matrix["regime"] == regime) & (matrix["layer"] == layer)]
            common_rows.append(
                {
                    "regime": regime,
                    "layer": int(layer),
                    "C4B_observed": float(
                        current.loc[current["panel"] == "C4B", "observed"].iloc[0]
                    ),
                    "C4B_lcb": float(
                        current.loc[current["panel"] == "C4B", "simultaneous_lcb"].iloc[0]
                    ),
                    "C5B_observed": float(
                        current.loc[current["panel"] == "C5B", "observed"].iloc[0]
                    ),
                    "C5B_lcb": float(
                        current.loc[current["panel"] == "C5B", "simultaneous_lcb"].iloc[0]
                    ),
                    "both_panels_simultaneously_robust": bool(
                        current["simultaneously_robust"].all()
                    ),
                }
            )
    pd.DataFrame(common_rows).to_csv(
        args.output / "common_boundary_by_layer.csv", index=False
    )

    same_cross_rows = []
    for regime, same_panel, cross_panel in (
        ("C4A", "C4B", "C5B"),
        ("C5A", "C5B", "C4B"),
    ):
        for layer in sorted(matrix["layer"].unique()):
            current = matrix[(matrix["regime"] == regime) & (matrix["layer"] == layer)]
            same = current[current["panel"] == same_panel].iloc[0]
            cross = current[current["panel"] == cross_panel].iloc[0]
            same_cross_rows.append(
                {
                    "regime": regime,
                    "layer": int(layer),
                    "same_bank_panel": same_panel,
                    "same_bank_observed": float(same.observed),
                    "same_bank_lcb": float(same.simultaneous_lcb),
                    "cross_bank_panel": cross_panel,
                    "cross_bank_observed": float(cross.observed),
                    "cross_bank_lcb": float(cross.simultaneous_lcb),
                }
            )
    pd.DataFrame(same_cross_rows).to_csv(
        args.output / "same_bank_vs_cross_bank.csv", index=False
    )

    observed = bottlenecks[["regime", "panel", "layer", "observed"]]
    overlap_audit = overlap.merge(
        observed, on=["regime", "panel", "layer"], validate="one_to_one"
    )
    overlap_audit["delta_after_exclusion"] = (
        overlap_audit["bottleneck"] - overlap_audit["observed"]
    )
    overlap_audit["sign_preserved"] = (
        np.sign(overlap_audit["bottleneck"]) == np.sign(overlap_audit["observed"])
    )
    overlap_audit.to_csv(args.output / "overlap_exclusion_audit.csv", index=False)


if __name__ == "__main__":
    main()

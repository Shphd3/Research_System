from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    cells = pd.read_csv(args.run / "cells.csv")
    predictions = pd.read_csv(args.run / "predictions.csv")
    confusions = pd.read_csv(args.run / "confusions.csv")
    bottlenecks = pd.read_csv(args.run / "bottlenecks.csv")
    models = json.loads((args.run / "models.json").read_text(encoding="utf-8"))

    rows: list[dict[str, object]] = []
    for (panel, layer), group in predictions.groupby(["panel", "layer"], sort=True):
        bottleneck = bottlenecks[
            (bottlenecks["panel"] == panel) & (bottlenecks["layer"] == layer)
        ].iloc[0]
        for label, selector in (
            ("P", group["task"] == "P"),
            ("J", group["task"] == "J"),
            ("pooled_F", group["task"].str.startswith("F_")),
        ):
            selected = group[selector]
            rows.append(
                {
                    "panel": panel,
                    "layer": layer,
                    "task_group": label,
                    "accuracy": float(selected["correct"].mean()),
                    "margin_q05": float(np.quantile(selected["margin"], 0.05)),
                    "nonpositive_margin_rate": float((selected["margin"] <= 0).mean()),
                    "bottleneck_task": bottleneck["worst_task"],
                    "bottleneck_q05": float(bottleneck["observed"]),
                    "bottleneck_lower_bound": float(bottleneck["lower_bound"]),
                }
            )
    pd.DataFrame(rows).to_csv(args.output / "task_group_summary.csv", index=False)

    fine = cells[(cells["panel"] == "C5") & cells["task"].str.startswith("F_")].copy()
    parent_names = {
        0: "mathematics",
        1: "physics",
        2: "chemistry",
        3: "biology",
        4: "computer science",
        5: "economics",
        6: "medicine",
        7: "linguistics",
    }
    fine["parent_name"] = fine["parent_id"].astype(int).map(parent_names)
    fine[
        [
            "layer",
            "task",
            "parent_id",
            "parent_name",
            "balanced_accuracy",
            "margin_q05",
            "nonpositive_margin_rate",
        ]
    ].to_csv(args.output / "c5_conditional_fine_summary.csv", index=False)

    strict_rows = []
    for (panel, layer), group in predictions.groupby(["panel", "layer"], sort=True):
        row = group.loc[group["margin"].idxmin()]
        strict_rows.append(
            {
                "panel": panel,
                "layer": layer,
                "minimum_margin": float(row["margin"]),
                "task": row["task"],
                "true_name": row["true_name"],
                "predicted_name": row["predicted_name"],
                "record_id": row["record_id"],
                "tasks_with_any_nonpositive_margin": int(
                    (group.groupby("task")["margin"].min() <= 0).sum()
                ),
            }
        )
    pd.DataFrame(strict_rows).to_csv(args.output / "strict_minima.csv", index=False)

    errors = confusions[
        (confusions["panel"] == "C5")
        & (confusions["true_class"] != confusions["predicted_class"])
        & (confusions["count"] > 0)
    ].copy()
    errors = (
        errors.sort_values(
            ["layer", "task", "count", "true_name", "predicted_name"],
            ascending=[True, True, False, True, True],
        )
        .groupby(["layer", "task"], sort=True)
        .head(5)
    )
    errors.to_csv(args.output / "c5_top_directed_confusions.csv", index=False)

    model_frame = pd.DataFrame(models)
    model_frame["cv_nll_strictly_decreases_with_c"] = model_frame["cv_nll_by_c"].map(
        lambda mapping: all(
            value_b < value_a
            for (_, value_a), (_, value_b) in zip(
                sorted((float(key), float(value)) for key, value in mapping.items()),
                sorted((float(key), float(value)) for key, value in mapping.items())[1:],
            )
        )
    )
    model_frame[
        [
            "layer",
            "task",
            "task_kind",
            "selected_c",
            "converged",
            "weight_r90",
            "weight_effective_rank",
            "cv_nll_strictly_decreases_with_c",
        ]
    ].to_csv(args.output / "model_selection_summary.csv", index=False)


if __name__ == "__main__":
    main()

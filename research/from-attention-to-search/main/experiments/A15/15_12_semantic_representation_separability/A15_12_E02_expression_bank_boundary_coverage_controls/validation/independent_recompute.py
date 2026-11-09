from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


EXPECTED_COUNTS = {
    "models": 240,
    "cells": 480,
    "predictions": 138240,
    "bottlenecks": 48,
    "paired_differences": 36,
    "leave_one_family_out_rows": 720,
    "leave_one_family_out_summary": 48,
    "fixed_c_task_cells": 1440,
    "fixed_c_bottlenecks": 144,
    "fixed_c100_reference_conformance": 120,
    "overlap_excluded_cells": 360,
    "overlap_excluded_bottlenecks": 36,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def close(left: float, right: float, tolerance: float = 1e-10) -> bool:
    return bool(np.isclose(left, right, rtol=0.0, atol=tolerance))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    run = args.run.resolve()
    completion = json.loads((run / "completion_audit.json").read_text(encoding="utf-8"))
    if completion.get("passed") is not True:
        raise RuntimeError("the run has no passed completion audit")

    artifact_mismatches: list[dict[str, object]] = []
    for item in completion["artifacts"]:
        path = run / item["path"]
        if not path.is_file():
            artifact_mismatches.append({"path": item["path"], "reason": "missing"})
            continue
        if path.stat().st_size != int(item["bytes"]):
            artifact_mismatches.append({"path": item["path"], "reason": "bytes"})
        if sha256(path) != item["sha256"]:
            artifact_mismatches.append({"path": item["path"], "reason": "sha256"})

    predictions = pd.read_csv(run / "predictions.csv")
    cells = pd.read_csv(run / "cells.csv")
    bottlenecks = pd.read_csv(run / "bottlenecks.csv")
    paired = pd.read_csv(run / "paired_raw_margin_differences.csv")
    lofo = pd.read_csv(run / "leave_one_family_out.csv")
    lofo_summary = pd.read_csv(run / "leave_one_family_out_summary.csv")
    fixed_cells = pd.read_csv(run / "fixed_c_task_cells.csv")
    fixed_bottlenecks = pd.read_csv(run / "fixed_c_bottlenecks.csv")
    conformance = pd.read_csv(run / "fixed_c100_reference_conformance.csv")
    overlap_cells = pd.read_csv(run / "overlap_excluded_cells.csv")
    overlap_bottlenecks = pd.read_csv(run / "overlap_excluded_bottlenecks.csv")
    models = json.loads((run / "models.json").read_text(encoding="utf-8"))

    actual_counts = {
        "models": len(models),
        "cells": len(cells),
        "predictions": len(predictions),
        "bottlenecks": len(bottlenecks),
        "paired_differences": len(paired),
        "leave_one_family_out_rows": len(lofo),
        "leave_one_family_out_summary": len(lofo_summary),
        "fixed_c_task_cells": len(fixed_cells),
        "fixed_c_bottlenecks": len(fixed_bottlenecks),
        "fixed_c100_reference_conformance": len(conformance),
        "overlap_excluded_cells": len(overlap_cells),
        "overlap_excluded_bottlenecks": len(overlap_bottlenecks),
    }

    cell_order = [
        (str(row.regime), str(row.panel), int(row.layer))
        for row in bottlenecks.itertuples(index=False)
    ]
    observed_mismatches: list[dict[str, object]] = []
    for row in bottlenecks.itertuples(index=False):
        current = predictions[
            (predictions["regime"] == row.regime)
            & (predictions["panel"] == row.panel)
            & (predictions["layer"] == row.layer)
        ]
        task_values = {
            task: float(
                np.quantile(
                    task_rows["margin"].to_numpy(float), 0.05, method="linear"
                )
            )
            for task, task_rows in current.groupby("task", sort=True)
        }
        worst_task = min(task_values, key=lambda task: (task_values[task], task))
        if worst_task != row.worst_task or not close(task_values[worst_task], row.observed):
            observed_mismatches.append(
                {
                    "regime": row.regime,
                    "panel": row.panel,
                    "layer": int(row.layer),
                    "expected_task": worst_task,
                    "stored_task": row.worst_task,
                    "recomputed": task_values[worst_task],
                    "stored": float(row.observed),
                }
            )

    with np.load(run / "bootstrap_draws.npz") as bootstrap:
        draws = np.asarray(bootstrap["normalized_draws"], dtype=np.float64)
        if draws.shape != (10000, 48):
            raise RuntimeError(f"unexpected normalized bootstrap shape: {draws.shape}")
        observed = bottlenecks["observed"].to_numpy(float)
        standard_errors = np.std(draws, axis=0, ddof=1)
        if np.any(standard_errors <= np.finfo(np.float64).eps):
            raise RuntimeError("zero bootstrap standard error")
        centered = (draws - observed[np.newaxis, :]) / standard_errors[np.newaxis, :]
        min_studentized = np.min(centered, axis=1)
        global_q = min(float(np.quantile(min_studentized, 0.05, method="linear")), 0.0)
        recomputed_lcb = observed + global_q * standard_errors
        lcb_max_abs_error = float(
            np.max(np.abs(recomputed_lcb - bottlenecks["simultaneous_lcb"].to_numpy(float)))
        )
        se_max_abs_error = float(
            np.max(np.abs(standard_errors - bottlenecks["bootstrap_se"].to_numpy(float)))
        )
        paired_mismatches: list[dict[str, object]] = []
        for row in paired.itertuples(index=False):
            key = f"paired__{row.treatment}_minus_C4A__{row.panel}__block_{row.layer}"
            values = np.asarray(bootstrap[key], dtype=np.float64)
            lower = float(np.quantile(values, 0.025, method="linear"))
            upper = float(np.quantile(values, 0.975, method="linear"))
            if not close(lower, row.ci_lower) or not close(upper, row.ci_upper):
                paired_mismatches.append(
                    {
                        "key": key,
                        "recomputed": [lower, upper],
                        "stored": [float(row.ci_lower), float(row.ci_upper)],
                    }
                )

    conformance_columns = [
        column
        for column in conformance.columns
        if column.startswith("abs_") or column.endswith("_abs_error")
    ]
    conformance_max_abs_error = (
        float(conformance[conformance_columns].to_numpy(float).max())
        if conformance_columns
        else 0.0
    )
    overlap_sign_changes = int(
        (
            np.sign(overlap_bottlenecks["bottleneck"].to_numpy(float))
            != np.sign(
                overlap_bottlenecks.merge(
                    bottlenecks[["regime", "panel", "layer", "observed"]],
                    on=["regime", "panel", "layer"],
                    validate="one_to_one",
                )["observed"].to_numpy(float)
            )
        ).sum()
    )

    checks = {
        "completion_passed": completion.get("passed") is True,
        "artifact_hashes": not artifact_mismatches,
        "counts": actual_counts == EXPECTED_COUNTS,
        "observed_bottlenecks": not observed_mismatches,
        "bootstrap_lcb": lcb_max_abs_error <= 1e-10,
        "bootstrap_se": se_max_abs_error <= 1e-10,
        "paired_intervals": not paired_mismatches,
        "fixed_c100_conformance": bool(conformance.get("passed", pd.Series([True])).all()),
        "overlap_sign_stability": overlap_sign_changes == 0,
        "cell_order_count": len(cell_order) == len(set(cell_order)) == 48,
    }
    receipt = {
        "passed": all(checks.values()),
        "checks": checks,
        "run": str(run),
        "completion_audit_sha256": sha256(run / "completion_audit.json"),
        "registered_artifact_count": len(completion["artifacts"]),
        "artifact_mismatches": artifact_mismatches,
        "expected_counts": EXPECTED_COUNTS,
        "actual_counts": actual_counts,
        "observed_mismatches": observed_mismatches,
        "studentized_global_q": global_q,
        "lcb_max_abs_error": lcb_max_abs_error,
        "se_max_abs_error": se_max_abs_error,
        "paired_mismatches": paired_mismatches,
        "fixed_c100_max_abs_error": conformance_max_abs_error,
        "overlap_sign_changes": overlap_sign_changes,
        "robust_cell_count": int((bottlenecks["simultaneous_lcb"] > 0).sum()),
    }
    args.output.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    if not receipt["passed"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()

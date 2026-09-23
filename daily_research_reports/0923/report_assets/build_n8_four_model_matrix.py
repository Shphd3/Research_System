#!/usr/bin/env python3
"""Curate the recovered exact-15B/17B N8 four-model descriptive matrix."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RUN = Path("/data/250010109/MoE_Router/experiments/20260923_sae_n8_15b17b_matrix/runs/full_2x5090_20260923T032900Z")
ANALYSIS = RUN / "analysis_cpu_recovery_20260923T040000Z"
HERE = Path("/data/250010109/Research_System/daily_research_reports/0923")
FIGURE = HERE / "figures/n8_15b17b_four_model_matrix.png"
TABLE = HERE / "tables/n8_15b17b_four_model_matrix.csv"
MANIFEST = HERE / "report_assets/n8_15b17b_four_model_matrix_manifest.json"
MODELS = ("Dense", "S7", "Fresh S7", "SALL")
CASES = {
    "15B": ("15b_dense", "15b_s7_original", "15b_s7_fresh", "15b_sall"),
    "17B": ("17b_dense", "17b_s7_reweighted", "17b_s7_fresh", "17b_sall"),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    receipt = json.loads((RUN / "recovery_receipt.json").read_text())
    assert receipt["status"] == receipt["analysis_status"] == "PASS"
    metrics = json.loads((ANALYSIS / "primary_metrics.json").read_text())
    atoms = json.loads((ANALYSIS / "atom_reuse.json").read_text())
    rows = []
    for coordinate, cases in CASES.items():
        for label, case in zip(MODELS, cases):
            result = metrics[case]["a_mean"]
            geometry = result["geometry"]
            rows.append({"checkpoint": coordinate, "model": label, "case": case,
                         "accuracy_pct": 100 * result["probe"]["test_accuracy"],
                         "effective_dimension": geometry["effective_dimension"],
                         "top16_variance_share": geometry["q16"],
                         "between_within": geometry["between_within"],
                         "atom_reuse_192": None if atoms[case] is None else atoms[case]["reuse"]})
    import csv
    TABLE.parent.mkdir(exist_ok=True)
    with TABLE.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if value is None else value for key, value in row.items()})
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(2, 2, figsize=(11.8, 7.2))
    specifications = (
        (axes[0, 0], "accuracy_pct", "N8 test accuracy (%)", (0, 100)),
        (axes[0, 1], "between_within", "Between / within scatter", (0, 0.52)),
        (axes[1, 0], "effective_dimension", "Effective dimension", (0, 24)),
        (axes[1, 1], "atom_reuse_192", "Atom reuse, 192 records", (0, 0.75)),
    )
    x = np.arange(len(MODELS))
    width = .35
    for ax, key, ylabel, ylim in specifications:
        for offset, (coordinate, color) in enumerate((("15B", "#4C78A8"), ("17B", "#F58518"))):
            subset = [r for r in rows if r["checkpoint"] == coordinate]
            values = [float("nan") if row[key] is None else row[key] for row in subset]
            ax.bar(x + (offset - .5) * width, values, width, label=coordinate, color=color)
        ax.set_xticks(x, MODELS)
        ax.set_ylabel(ylabel)
        ax.set_ylim(*ylim)
        ax.grid(axis="y", alpha=.17)
        ax.set_axisbelow(True)
    axes[0, 0].legend(frameon=False, loc="lower left")
    fig.suptitle("N8 representation readout at exact 15B and 17B", weight="bold")
    fig.text(.5, .02,
             "Native layer-8 mean: 1,600 test records. Atom reuse: a separate 192-record panel; historical batch-4 values except 17B SALL batch-8.",
             ha="center", fontsize=8, color="#555555")
    fig.tight_layout(rect=[0, .05, 1, .94])
    FIGURE.parent.mkdir(exist_ok=True)
    fig.savefig(FIGURE, dpi=180)
    plt.close(fig)
    manifest = {
        "status": "PASS", "figure": str(FIGURE), "figure_sha256": sha(FIGURE),
        "table": str(TABLE), "table_sha256": sha(TABLE),
        "source_metrics": str(ANALYSIS / "primary_metrics.json"),
        "source_metrics_sha256": sha(ANALYSIS / "primary_metrics.json"),
        "source_atoms": str(ANALYSIS / "atom_reuse.json"),
        "source_atoms_sha256": sha(ANALYSIS / "atom_reuse.json"),
        "recovery_receipt": str(RUN / "recovery_receipt.json"),
        "claim_boundary": "Post-result descriptive fixed-checkpoint N8 readout; the 192-record atom panel uses mixed batch shapes and is not exact support replication.",
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(FIGURE)


if __name__ == "__main__":
    main()

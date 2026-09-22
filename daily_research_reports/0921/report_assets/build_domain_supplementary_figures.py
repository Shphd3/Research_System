#!/usr/bin/env python3
"""Render post-hoc N8 supplementary figures from the sealed local result package."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


RESULT = Path("/data/250010109/MoE_Router/experiments/20260921_sae_domain_supplementary_analysis/runs/full_local_cpu_20260921T0645Z")
OUTPUT = Path("/data/250010109/Research_System/daily_research_reports/0921/figures")
COLORS = {"Dense": "#4C78A8", "SALL": "#F58518", "S7": "#54A24B", "TF-IDF": "#B279A2"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def save(fig, name: str, entries: list[dict]) -> None:
    path = OUTPUT / name
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    entries.append({"file": path.name, "sha256": sha256(path)})


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    readout_path = RESULT / "readout" / "domain_readout_metrics.json"
    observer_path = RESULT / "observer" / "observer_and_layer_metrics.json"
    readout = json.loads(readout_path.read_text())
    observer = json.loads(observer_path.read_text())
    entries = []

    rows = readout["paired_readout"]
    labels = [f"L{layer} {pool}" for layer in (4, 8) for pool in ("mean", "last")]
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    y = np.arange(len(labels))
    for offset, (case, label, color) in enumerate((("21b_sall_original", "SALL-Dense", COLORS["SALL"]),
                                                   ("21b_s7_reweighted", "S7-Dense", COLORS["S7"]))):
        chosen = []
        for layer in (4, 8):
            for pool in ("mean", "last"):
                chosen.append(next(row for row in rows if row["layer"] == layer and row["pooling"] == pool
                                   and row["contrast"].startswith(case)))
        point = np.asarray([row["point"] * 100 for row in chosen])
        low = np.asarray([row["ci95_percentile"][0] * 100 for row in chosen])
        high = np.asarray([row["ci95_percentile"][1] * 100 for row in chosen])
        position = y + (-0.10 if offset == 0 else 0.10)
        ax.errorbar(point, position, xerr=np.vstack([point - low, high - point]), fmt="o", color=color,
                    capsize=3, label=label)
    ax.axvline(0, color="black", linewidth=1)
    ax.set_yticks(y, labels)
    ax.set_xlabel("N8 balanced-accuracy difference (percentage points)")
    ax.set_title("Frozen 21B N8 readout: paired record bootstrap")
    ax.legend(frameon=False)
    ax.grid(axis="x", alpha=0.2)
    save(fig, "domain_supp_01_paired_readout.png", entries)

    conditions = {(row["case"], row["layer"], row["pooling"], row["transform"]): row
                  for row in readout["conditions"]}
    names = ["Dense", "SALL", "S7", "TF-IDF"]
    accuracy = [conditions[("21b_dense", 8, "mean", "registered_global_rms")]["test_balanced_accuracy"] * 100,
                conditions[("21b_sall_original", 8, "mean", "registered_global_rms")]["test_balanced_accuracy"] * 100,
                conditions[("21b_s7_reweighted", 8, "mean", "registered_global_rms")]["test_balanced_accuracy"] * 100,
                readout["lexical_and_surface_baselines"]["tfidf_1_2gram"]["test_balanced_accuracy"] * 100]
    geom = next(row for row in readout["geometry_bootstrap"] if row["layer"] == 8 and row["pooling"] == "mean")
    fig = plt.figure(figsize=(12, 4.3), constrained_layout=True)
    grid = fig.add_gridspec(1, 4, width_ratios=(2.2, 1, 1, 1), wspace=0.45)
    accuracy_axis = fig.add_subplot(grid[0, 0])
    accuracy_axis.bar(names, accuracy, color=[COLORS[name] for name in names])
    accuracy_axis.set_ylabel("Balanced accuracy (%)")
    accuracy_axis.set_title("Source-category readout")
    accuracy_axis.set_ylim(0, 100)
    accuracy_axis.axhline(12.5, color="gray", linestyle="--", linewidth=1, label="8-way chance")
    accuracy_axis.legend(frameon=False)
    metrics = ["B", "W", "B_over_W"]
    metric_labels = ["Between B", "Within W", "B/W"]
    points = [geom["point"][metric] for metric in metrics]
    low = [geom["ci95_percentile"][metric][0] for metric in metrics]
    high = [geom["ci95_percentile"][metric][1] for metric in metrics]
    for index, (metric_label, point, lower, upper) in enumerate(zip(metric_labels, points, low, high), start=1):
        axis = fig.add_subplot(grid[0, index])
        axis.errorbar(point, 0, xerr=[[point - lower], [upper - point]], fmt="o",
                      color=COLORS["SALL"], capsize=3)
        axis.axvline(0, color="black", linewidth=1)
        axis.set_yticks([])
        axis.set_title(f"Δ {metric_label}")
        axis.grid(axis="x", alpha=0.2)
    fig.suptitle("Layer 8 mean: readout and SALL-Dense geometry deltas", fontsize=14)
    save(fig, "domain_supp_02_readout_lexical_geometry.png", entries)

    obs = observer["observer_conditions"]
    names = [f"SALL L4", "SALL L8", "S7 L8"]
    candidate = [row["atom_analysis"]["candidate_group_probe"]["test_balanced_accuracy"] * 100 for row in obs]
    highfreq = [row["atom_analysis"]["high_frequency_group_probe"]["test_balanced_accuracy"] * 100 for row in obs]
    random_q = [row["atom_analysis"]["random_control"]["test_balanced_accuracy_quantiles"] for row in obs]
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    x = np.arange(3)
    ax.bar(x - 0.18, candidate, width=0.36, color=COLORS["SALL"], label="fit-selected 8 atoms")
    ax.bar(x + 0.18, highfreq, width=0.36, color="#9D755D", label="8 high-frequency atoms")
    for index, quantiles in enumerate(random_q):
        ax.vlines(index, quantiles[0] * 100, quantiles[2] * 100, color="black", linewidth=4, alpha=0.45)
        ax.scatter(index, quantiles[1] * 100, color="black", s=18, zorder=4)
    ax.axhline(12.5, color="gray", linestyle="--", linewidth=1)
    ax.set_xticks(x, names)
    ax.set_ylabel("8-way test balanced accuracy (%)")
    ax.set_title("Fixed 192-record observer panel: atom-group readout")
    ax.legend(frameon=False)
    save(fig, "domain_supp_03_atom_groups.png", entries)

    matrix_rows = [row for row in observer["same_model_layer_cka"]["same_model_matrices"]
                   if row["pooling"] == "mean" and row["estimator"] == "u_corrected"]
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    for row, name in zip(matrix_rows, ("Dense", "SALL", "S7")):
        matrix = row["matrix_human_layers_1_to_8"]
        adjacent = [matrix[index][index + 1] for index in range(7)]
        ax.plot(range(1, 8), adjacent, marker="o", color=COLORS[name], label=name)
    ax.set_xlabel("Earlier layer in adjacent pair")
    ax.set_ylabel("U-corrected linear CKA")
    ax.set_title("Within-model adjacent-layer structure, N8 mean pooling")
    ax.set_xticks(range(1, 8), [f"{index}→{index+1}" for index in range(1, 8)])
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    save(fig, "domain_supp_04_same_model_cka.png", entries)

    manifest = {"status": "PASS", "post_hoc_exploratory": True,
                "result_root": str(RESULT),
                "source_files": {str(readout_path): sha256(readout_path), str(observer_path): sha256(observer_path)},
                "figures": entries}
    manifest_path = OUTPUT / "domain_supplementary_figure_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "figures": len(entries), "manifest": str(manifest_path)}))


if __name__ == "__main__":
    main()

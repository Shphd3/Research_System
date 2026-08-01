#!/usr/bin/env python3
"""Aggregate and visualize the native layerwise MoE output spectra."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr


EXPERIMENT_DIR = Path(__file__).resolve().parent
RAW_DIR = EXPERIMENT_DIR / "results/native_layer_spectra"
TABLE_DIR = EXPERIMENT_DIR / "tables"
FIGURE_DIR = EXPERIMENT_DIR / "figures"


def total_variation(left: np.ndarray, right: np.ndarray) -> float:
    return float(0.5 * np.abs(left - right).sum())


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    summaries = pd.concat(
        [pd.read_csv(RAW_DIR / f"{model}_summary.csv") for model in ["lb", "decommon"]],
        ignore_index=True,
    ).sort_values(["model", "layer"])
    spectra = pd.concat(
        [pd.read_csv(RAW_DIR / f"{model}_spectrum.csv") for model in ["lb", "decommon"]],
        ignore_index=True,
    ).sort_values(["model", "layer", "spectral_rank"])

    old = pd.read_csv(TABLE_DIR / "layer_metrics.csv")[["model", "layer", "native_effective_rank", "native_rank90"]]
    check = summaries.merge(old, on=["model", "layer"], how="left", validate="one_to_one")
    max_effective_rank_error = float(
        np.abs(check.effective_rank - check.native_effective_rank).max()
    )
    max_rank90_error = int(np.abs(check.rank90 - check.native_rank90).max())
    if max_effective_rank_error > 0.01 or max_rank90_error != 0:
        raise RuntimeError(
            f"Native-spectrum replay mismatch: erank={max_effective_rank_error}, rank90={max_rank90_error}"
        )

    probability = {
        (model, int(layer)): group.normalized_energy.to_numpy(dtype=np.float64)
        for (model, layer), group in spectra.groupby(["model", "layer"], sort=True)
    }
    comparison_rows = []
    for layer in sorted(summaries.layer.unique()):
        lb = probability[("lb", int(layer))]
        decommon = probability[("decommon", int(layer))]
        comparison_rows.append(
            {
                "layer": int(layer),
                "cross_model_spectrum_tv": total_variation(lb, decommon),
                "lb_adjacent_spectrum_tv": (
                    np.nan if layer == 1 else total_variation(probability[("lb", int(layer - 1))], lb)
                ),
                "decommon_adjacent_spectrum_tv": (
                    np.nan
                    if layer == 1
                    else total_variation(probability[("decommon", int(layer - 1))], decommon)
                ),
            }
        )
    comparisons = pd.DataFrame(comparison_rows)

    model_stats = {}
    for model, group in summaries.groupby("model", sort=False):
        rho_erank, p_erank = spearmanr(group.layer, group.effective_rank)
        rho_top1, p_top1 = spearmanr(group.layer, group.top1_energy)
        min_row = group.loc[group.effective_rank.idxmin()]
        max_row = group.loc[group.effective_rank.idxmax()]
        model_stats[model] = {
            "spearman_layer_effective_rank": float(rho_erank),
            "spearman_layer_effective_rank_p": float(p_erank),
            "spearman_layer_top1_energy": float(rho_top1),
            "spearman_layer_top1_energy_p": float(p_top1),
            "minimum_effective_rank_layer": int(min_row.layer),
            "minimum_effective_rank": float(min_row.effective_rank),
            "maximum_effective_rank_layer": int(max_row.layer),
            "maximum_effective_rank": float(max_row.effective_rank),
            "layer12_effective_rank": float(group.loc[group.layer == 12, "effective_rank"].iloc[0]),
            "layer12_top1_energy": float(group.loc[group.layer == 12, "top1_energy"].iloc[0]),
            "centered_variance_layer1": float(group.loc[group.layer == 1, "total_centered_variance"].iloc[0]),
            "centered_variance_layer12": float(group.loc[group.layer == 12, "total_centered_variance"].iloc[0]),
        }
    audit = {
        "replay_check": {
            "max_effective_rank_abs_error": max_effective_rank_error,
            "max_rank90_abs_error": max_rank90_error,
        },
        "cross_model": {
            "median_spectrum_tv": float(comparisons.cross_model_spectrum_tv.median()),
            "maximum_spectrum_tv": float(comparisons.cross_model_spectrum_tv.max()),
            "maximum_spectrum_tv_layer": int(
                comparisons.loc[comparisons.cross_model_spectrum_tv.idxmax(), "layer"]
            ),
            "minimum_spectrum_tv": float(comparisons.cross_model_spectrum_tv.min()),
            "minimum_spectrum_tv_layer": int(
                comparisons.loc[comparisons.cross_model_spectrum_tv.idxmin(), "layer"]
            ),
        },
        "models": model_stats,
        "claim_boundary": "Descriptive same-input checkpoint audit; not a causal LB-versus-decommon comparison.",
    }

    summaries.to_csv(TABLE_DIR / "native_layer_spectral_summary.csv", index=False)
    spectra.to_csv(TABLE_DIR / "native_layer_spectral_distribution.csv", index=False)
    comparisons.to_csv(TABLE_DIR / "native_layer_spectral_comparison.csv", index=False)
    (RAW_DIR / "audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")

    colors = {"lb": "#2463a6", "decommon": "#d45b2c"}
    labels = {"lb": "LB=0.01, no-center", "decommon": "running-center, LB=0"}
    fig, axes = plt.subplots(3, 2, figsize=(13.5, 12), constrained_layout=True)

    heatmaps = []
    all_log = []
    for model in ["lb", "decommon"]:
        matrix = (
            spectra[spectra.model == model]
            .pivot(index="layer", columns="spectral_rank", values="normalized_energy")
            .sort_index()
            .to_numpy()
        )
        log_matrix = np.log10(np.clip(matrix, 1e-10, None))
        heatmaps.append((model, log_matrix))
        all_log.append(log_matrix)
    vmin = float(np.quantile(np.concatenate([value.ravel() for value in all_log]), 0.02))
    vmax = float(max(value.max() for value in all_log))
    for axis, (model, matrix) in zip(axes[0], heatmaps):
        image = axis.imshow(
            matrix,
            aspect="auto",
            origin="lower",
            extent=[1, matrix.shape[1], 0.5, matrix.shape[0] + 0.5],
            cmap="magma",
            vmin=vmin,
            vmax=vmax,
        )
        axis.set_title(f"{labels[model]}: full normalized spectrum")
        axis.set_xlabel("Spectral rank (1 = largest)")
        axis.set_ylabel("MoE layer")
        axis.set_yticks(range(1, 13))
    colorbar = fig.colorbar(image, ax=axes[0, :], shrink=0.86, pad=0.02)
    colorbar.set_label("log10 normalized spectral energy")

    for model, group in summaries.groupby("model", sort=False):
        axes[1, 0].plot(
            group.layer, group.effective_rank, marker="o", linewidth=2, color=colors[model], label=labels[model]
        )
        axes[1, 1].plot(
            group.layer, 100 * group.top1_energy, marker="o", linewidth=2, color=colors[model], label=labels[model]
        )
        axes[2, 0].plot(
            group.layer, group.rank90, marker="o", linewidth=2, color=colors[model], label=labels[model]
        )
    axes[1, 0].set_title("Effective rank is non-monotonic across depth")
    axes[1, 0].set_ylabel("Effective rank (directions)")
    axes[1, 1].set_title("Largest-direction energy reveals local spectral spikes")
    axes[1, 1].set_ylabel("Top-1 spectral energy (%)")
    axes[2, 0].set_title("Directions required for 90% energy")
    axes[2, 0].set_ylabel("90%-energy rank (directions)")
    for axis in [axes[1, 0], axes[1, 1], axes[2, 0]]:
        axis.set_xlabel("MoE layer")
        axis.set_xticks(range(1, 13))
        axis.grid(alpha=0.25)
    axes[1, 0].legend(frameon=False)

    axes[2, 1].plot(
        comparisons.layer,
        comparisons.cross_model_spectrum_tv,
        marker="o",
        linewidth=2,
        color="#513c78",
        label="same-layer cross-model",
    )
    axes[2, 1].plot(
        comparisons.layer,
        comparisons.lb_adjacent_spectrum_tv,
        marker=".",
        linewidth=1.5,
        color=colors["lb"],
        label="LB adjacent layers",
    )
    axes[2, 1].plot(
        comparisons.layer,
        comparisons.decommon_adjacent_spectrum_tv,
        marker=".",
        linewidth=1.5,
        color=colors["decommon"],
        label="decommon adjacent layers",
    )
    axes[2, 1].set_title("Normalized spectrum distance")
    axes[2, 1].set_xlabel("MoE layer")
    axes[2, 1].set_ylabel("Total variation (0 to 1)")
    axes[2, 1].set_xticks(range(1, 13))
    axes[2, 1].grid(alpha=0.25)
    axes[2, 1].legend(frameon=False, fontsize=9)

    fig.suptitle(
        "Native sparse-MoE output spectra on identical held-out tokens\n"
        "Centered token-by-feature matrices; eigenvalue energy normalized within each layer",
        fontsize=15,
    )
    fig.savefig(FIGURE_DIR / "native_layer_spectra.png", dpi=180)
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

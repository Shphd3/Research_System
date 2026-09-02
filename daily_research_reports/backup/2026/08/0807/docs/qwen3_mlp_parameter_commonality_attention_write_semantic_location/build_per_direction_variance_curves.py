from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from scipy.signal import savgol_filter


ROOT = Path(__file__).resolve().parents[4]
EXPERIMENT = (
    ROOT
    / "Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active"
    / "a15_01_09_e01_qwen3_mlp_parameter_commonality_attention_write_semantic_location"
)
SEMANTIC_RUN = (
    EXPERIMENT
    / "runs/a15-01-09-e01-s-20260807T061000Z/semantic"
)
FIGURE = Path(__file__).resolve().parent / "figures/figure5_per_direction_raw_variance_curves.png"
SELECTED_FIGURE = (
    Path(__file__).resolve().parent
    / "figures/figure5b_selected_layers_log10_per_direction_variance.png"
)
SMOOTHED_FIGURE = (
    Path(__file__).resolve().parent
    / "figures/figure5c_four_layers_smoothed_log10_per_direction_variance.png"
)
TEN_LAYER_FIGURE = (
    Path(__file__).resolve().parent
    / "figures/figure5d_ten_layers_smoothed_log10_per_direction_variance.png"
)
ARRAYS = Path(__file__).resolve().parent / "tables/per_direction_raw_variance.npz"

sys.path.insert(0, str(EXPERIMENT))
from common import CACHE, cube_from_rows, load_json, variance_per_direction  # noqa: E402


def main() -> None:
    rows = load_json(CACHE / "semantic_state_rows.json")
    layers = np.arange(1, 37)
    coarse = np.empty((36, 4096), dtype=np.float64)
    fine = np.empty((36, 4096), dtype=np.float64)

    for layer in layers:
        payload = torch.load(
            SEMANTIC_RUN / "projection_parts" / f"layer_{layer:02d}.pt",
            map_location="cpu",
            weights_only=False,
        )
        projection = payload["operators"]["native"]["projection"]
        cube = cube_from_rows(projection, rows)
        variances = variance_per_direction(cube)
        coarse[layer - 1] = variances["coarse"].double().numpy()
        fine[layer - 1] = variances["fine"].double().numpy()

    if np.any(coarse < 0) or np.any(fine < 0):
        raise RuntimeError("variance must be non-negative")
    if coarse.shape != (36, 4096) or fine.shape != (36, 4096):
        raise RuntimeError({"coarse": coarse.shape, "fine": fine.shape})

    ARRAYS.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        ARRAYS,
        layers=layers,
        local_parameter_rank=np.arange(1, 4097),
        coarse_raw_between_variance=coarse,
        fine_raw_between_variance=fine,
    )

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "figure.dpi": 160,
        }
    )
    cmap = plt.get_cmap("turbo")
    norm = Normalize(vmin=1, vmax=36)
    ranks = np.arange(1, 4097)
    positive = np.concatenate([coarse[coarse > 0], fine[fine > 0]])
    y_low = float(positive.min() * 0.8)
    y_high = float(positive.max() * 1.2)

    fig, axes = plt.subplots(2, 1, figsize=(13.2, 8.6), sharex=True, constrained_layout=True)
    for ax, values, title in (
        (axes[0], coarse, "Coarse semantic between-class variance"),
        (axes[1], fine, "Fine semantic between-class variance"),
    ):
        for layer, curve in zip(layers, values, strict=True):
            ax.plot(ranks, curve, color=cmap(norm(layer)), lw=0.65, alpha=0.82, rasterized=True)
        ax.set_yscale("log")
        ax.set_ylim(y_low, y_high)
        ax.set_ylabel("raw variance (log axis)")
        ax.set_title(title, loc="left", fontweight="bold")
        ax.grid(True, which="major", axis="y", color="#DDDDDD", lw=0.65, alpha=0.8)
        ax.spines[["top", "right"]].set_visible(False)
    axes[1].set_xlabel("local MLP parameter rank (1=largest parameter eigenvalue, 4096=smallest)")
    axes[1].set_xlim(1, 4096)
    axes[1].set_xticks([1, 512, 1024, 1536, 2048, 2560, 3072, 3584, 4096])
    colorbar = fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), ax=axes, fraction=0.018, pad=0.015)
    colorbar.set_label("Transformer block")
    colorbar.set_ticks([1, 6, 12, 18, 24, 30, 36])
    fig.suptitle(
        "Per-direction raw semantic variance in each layer's local MLP parameter spectrum\n"
        "4096 directions retained; no band averaging, smoothing, or cross-layer averaging",
        fontsize=14,
        fontweight="bold",
    )
    FIGURE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE, dpi=220, bbox_inches="tight")
    plt.close(fig)

    selected_layers = np.asarray([1, 12, 25, 35])
    selected_colors = plt.get_cmap("Blues")(np.asarray([0.38, 0.56, 0.74, 0.92]))
    fig, axes = plt.subplots(2, 1, figsize=(13.2, 8.6), sharex=True, constrained_layout=True)
    for ax, values, title in (
        (axes[0], coarse, "Coarse semantic between-class variance"),
        (axes[1], fine, "Fine semantic between-class variance"),
    ):
        for layer, color in zip(selected_layers, selected_colors, strict=True):
            curve = np.log10(values[layer - 1])
            ax.plot(ranks, curve, color=color, lw=0.8, alpha=0.9, label=f"block {layer}", rasterized=True)
        ax.set_ylabel("log10(raw variance)")
        ax.set_title(title, loc="left", fontweight="bold")
        ax.grid(True, axis="y", color="#DDDDDD", lw=0.65, alpha=0.8)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].legend(frameon=False, ncol=4, loc="lower right")
    axes[1].set_xlabel("local MLP parameter rank (1=largest parameter eigenvalue, 4096=smallest)")
    axes[1].set_xlim(1, 4096)
    axes[1].set_xticks([1, 512, 1024, 1536, 2048, 2560, 3072, 3584, 4096])
    fig.suptitle(
        "Selected-layer per-direction log10 raw semantic variance\n"
        "4096 directions retained; no band averaging or smoothing",
        fontsize=14,
        fontweight="bold",
    )
    fig.savefig(SELECTED_FIGURE, dpi=220, bbox_inches="tight")
    plt.close(fig)

    comparison_layers = np.asarray([1, 12, 25, 35])
    comparison_colors = plt.get_cmap("Blues")(np.asarray([0.38, 0.56, 0.74, 0.94]))
    fig, axes = plt.subplots(2, 1, figsize=(12.8, 8.2), sharex=True, constrained_layout=True)
    for ax, values, title in (
        (axes[0], coarse, "Coarse semantic between-class variance"),
        (axes[1], fine, "Fine semantic between-class variance"),
    ):
        for layer, color in zip(comparison_layers, comparison_colors, strict=True):
            logged = np.log10(values[layer - 1])
            smoothed = savgol_filter(logged, window_length=129, polyorder=3, mode="interp")
            ax.plot(ranks, smoothed, color=color, lw=1.8, label=f"block {layer}")
        ax.set_ylabel("smoothed log10(raw variance)")
        ax.set_title(title, loc="left", fontweight="bold")
        ax.grid(True, axis="y", color="#DDDDDD", lw=0.65, alpha=0.8)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].legend(frameon=False, ncol=4, loc="lower right")
    axes[1].set_xlabel("local MLP parameter rank (1=largest parameter eigenvalue, 4096=smallest)")
    axes[1].set_xlim(1, 4096)
    axes[1].set_xticks([1, 512, 1024, 1536, 2048, 2560, 3072, 3584, 4096])
    fig.suptitle(
        "Four-layer comparison of per-direction log10 raw semantic variance\n"
        "Savitzky-Golay smoothing: 129 ranks, polynomial order 3",
        fontsize=14,
        fontweight="bold",
    )
    fig.savefig(SMOOTHED_FIGURE, dpi=220, bbox_inches="tight")
    plt.close(fig)

    ten_layers = np.asarray([1, 5, 9, 13, 17, 21, 25, 29, 33, 36])
    ten_colors = plt.get_cmap("Blues")(np.linspace(0.34, 0.96, len(ten_layers)))
    fig, axes = plt.subplots(2, 1, figsize=(12.8, 8.4), sharex=True, constrained_layout=True)
    for ax, values, title in (
        (axes[0], coarse, "Coarse semantic between-class variance"),
        (axes[1], fine, "Fine semantic between-class variance"),
    ):
        for layer, color in zip(ten_layers, ten_colors, strict=True):
            logged = np.log10(values[layer - 1])
            smoothed = savgol_filter(logged, window_length=129, polyorder=3, mode="interp")
            ax.plot(ranks, smoothed, color=color, lw=1.35, alpha=0.96, label=f"block {layer}")
        ax.set_ylabel("smoothed log10(raw variance)")
        ax.set_title(title, loc="left", fontweight="bold")
        ax.grid(True, axis="y", color="#DDDDDD", lw=0.65, alpha=0.8)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].legend(frameon=False, ncol=10, loc="lower center", columnspacing=1.0, handlelength=2.2)
    axes[1].set_xlabel("local MLP parameter rank (1=largest parameter eigenvalue, 4096=smallest)")
    axes[1].set_xlim(1, 4096)
    axes[1].set_xticks([1, 512, 1024, 1536, 2048, 2560, 3072, 3584, 4096])
    fig.suptitle(
        "Ten-layer comparison of per-direction log10 raw semantic variance\n"
        "lighter = shallower; darker = deeper; Savitzky-Golay window 129, order 3",
        fontsize=14,
        fontweight="bold",
    )
    fig.savefig(TEN_LAYER_FIGURE, dpi=220, bbox_inches="tight")
    plt.close(fig)

    print(
        {
            "figure": str(FIGURE),
            "selected_log10_figure": str(SELECTED_FIGURE),
            "four_layer_smoothed_figure": str(SMOOTHED_FIGURE),
            "ten_layer_smoothed_figure": str(TEN_LAYER_FIGURE),
            "arrays": str(ARRAYS),
            "coarse_min_max": [float(coarse.min()), float(coarse.max())],
            "fine_min_max": [float(fine.min()), float(fine.max())],
        }
    )


if __name__ == "__main__":
    main()

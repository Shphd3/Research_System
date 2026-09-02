from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize


EXPERIMENT_CODE = Path(
    "/data/250010109/Research_System/Projects/from-attention-to-search/"
    "XingyuD/MoE_Routing_Experiments/active/"
    "a15_08_03_e01_function_admitted_update_spectral_rank_analysis"
)
sys.path.insert(0, str(EXPERIMENT_CODE))

from common import RUN_ROOT  # noqa: E402
from finalize import normalized_variance_density, smooth_curve  # noqa: E402


SELECTED_LAYERS = (2, 6, 10, 14, 18, 24, 25, 28, 32, 36)
SMOOTHING_WIDTH = 129
OUTPUT_DIR = Path(
    "/data/250010109/Research_System/daily_research_reports/backup/2026/08/0817/"
    "docs/candidate_figures"
)


def main() -> None:
    spectral = np.load(RUN_ROOT / "arrays/spectral_profiles.npz")
    layers = spectral["layers"].astype(int)
    splits = spectral["splits"].astype(str)
    profiles = spectral["mean_response_direction_energy"]
    confirmation_index = int(np.flatnonzero(splits == "confirmation")[0])
    hidden = int(profiles.shape[-1])
    normalized_rank = (np.arange(hidden, dtype=np.float64) + 0.5) / hidden

    colormap = plt.get_cmap("viridis")
    layer_norm = Normalize(vmin=min(SELECTED_LAYERS), vmax=max(SELECTED_LAYERS))
    figure, axis = plt.subplots(figsize=(10.8, 6.0))

    for layer in SELECTED_LAYERS:
        layer_index = int(np.flatnonzero(layers == layer)[0])
        density = normalized_variance_density(profiles[layer_index, confirmation_index])
        curve = smooth_curve(density, SMOOTHING_WIDTH)

        if layer in (24, 28):
            linewidth, linestyle, alpha = 3.0, "-", 1.0
            label = f"L{layer:02d} (function +)"
        elif layer == 25:
            linewidth, linestyle, alpha = 2.4, "--", 1.0
            label = "L25 (unresolved)"
        else:
            linewidth, linestyle, alpha = 1.45, "-", 0.78
            label = f"L{layer:02d}"

        axis.plot(
            normalized_rank,
            np.maximum(curve, np.finfo(np.float64).tiny),
            color=colormap(layer_norm(layer)),
            linewidth=linewidth,
            linestyle=linestyle,
            alpha=alpha,
            label=label,
        )

    axis.set_yscale("log")
    axis.set_xlim(0.0, 1.0)
    axis.grid(True, which="both", alpha=0.18)
    axis.set_xlabel("normalized Mean-Response rank (strong -> weak parameter response)")
    axis.set_ylabel(r"normalized residual-update variance density, $4096p_{\ell j}$ (log)")
    axis.set_title(
        "Residual-update variance in the frozen Mean-Response basis\n"
        "CONFIRMATION; 129-rank moving average for display only"
    )
    axis.legend(ncol=2, frameon=False, fontsize=9, loc="best")
    figure.tight_layout()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = OUTPUT_DIR / "common_basis_mean_response_variance_curves_selected_layers"
    figure.savefig(stem.with_suffix(".png"), dpi=220, bbox_inches="tight")
    figure.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()

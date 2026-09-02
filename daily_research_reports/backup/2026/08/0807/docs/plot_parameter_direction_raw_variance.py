from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable


ROOT = Path(__file__).resolve().parents[3]
WORKER = (
    ROOT
    / "Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active"
    / "a15_01_09_e01_qwen3_mlp_parameter_commonality_attention_write_semantic_location"
)
SEMANTIC_RUN = (
    WORKER
    / "runs/a15-01-09-e01-s-20260807T061000Z/semantic"
)
OUTPUT = ROOT / "daily_research_reports/backup/2026/08/0807/figures/parameter_direction_raw_semantic_variance.png"

sys.path.insert(0, str(WORKER))
from common import CACHE, cube_from_rows, load_json, variance_per_direction  # noqa: E402


def main() -> None:
    rows = load_json(CACHE / "semantic_state_rows.json")
    metrics = json.loads((SEMANTIC_RUN / "analysis/semantic_layer_metrics.json").read_text(encoding="utf-8"))
    layers = np.arange(1, 37)
    direction_variance = {"coarse": [], "fine": []}
    maximum_validation_error = 0.0

    for layer in layers:
        payload = torch.load(
            SEMANTIC_RUN / "projection_parts" / f"layer_{layer:02d}.pt",
            map_location="cpu",
            weights_only=False,
        )
        projection = payload["operators"]["native"]["projection"]
        cube = cube_from_rows(projection, rows)
        variances = variance_per_direction(cube)
        for role in ("coarse", "fine"):
            values = variances[role].double().cpu().numpy()
            direction_variance[role].append(values)
            expected = np.asarray(
                metrics[str(layer)]["operators"]["native"]["full"]["roles"][role]["raw_per_direction"],
                dtype=np.float64,
            )
            reconstructed = values.reshape(16, 256).mean(axis=1)
            relative_error = np.max(np.abs(reconstructed - expected) / np.maximum(np.abs(expected), 1e-30))
            maximum_validation_error = max(maximum_validation_error, float(relative_error))

    values_by_role = {role: np.stack(values) for role, values in direction_variance.items()}
    if maximum_validation_error > 1e-3:
        raise RuntimeError({"band_reconstruction_max_relative_error": maximum_validation_error})

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
        }
    )
    colors = plt.get_cmap("turbo")
    norm = Normalize(vmin=1, vmax=36)
    ranks = np.arange(1, 4097)
    fig, axes = plt.subplots(1, 2, figsize=(14.2, 5.4), sharex=True, sharey=True, constrained_layout=True)

    for ax, role in zip(axes, ("coarse", "fine"), strict=True):
        for index, layer in enumerate(layers):
            ax.plot(
                ranks,
                values_by_role[role][index],
                color=colors(norm(layer)),
                lw=0.62,
                alpha=0.72,
                rasterized=True,
            )
        ax.axvline(256.5, color="#555555", lw=0.8, ls="--")
        ax.axvline(2048.5, color="#555555", lw=0.8, ls="--")
        ax.text(128, 0.98, "head", transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=9)
        ax.text(1152, 0.98, "middle", transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=9)
        ax.text(3072, 0.98, "tail", transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=9)
        ax.set_yscale("log")
        ax.set_xlim(1, 4096)
        ax.set_xticks([1, 256, 1024, 2048, 3072, 4096])
        ax.set_xlabel("local MLP parameter rank (largest eigenvalue first)")
        ax.set_title(f"{role}: raw between-class variance", loc="left", fontweight="bold")
        ax.grid(True, which="major", axis="y", color="#DDDDDD", lw=0.6, alpha=0.7)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("variance at each individual parameter direction (log scale)")

    colorbar = fig.colorbar(
        ScalarMappable(norm=norm, cmap=colors),
        ax=axes,
        fraction=0.025,
        pad=0.02,
        ticks=[1, 6, 12, 18, 24, 25, 30, 35, 36],
    )
    colorbar.set_label("Transformer block")
    fig.suptitle(
        "Raw post-o_proj semantic variance along every local MLP parameter direction\n"
        "4096 directions per layer; no band averaging, smoothing, or layer averaging",
        fontsize=14,
        fontweight="bold",
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(
        json.dumps(
            {
                "figure": str(OUTPUT),
                "layers": 36,
                "directions_per_layer": 4096,
                "maximum_band_reconstruction_relative_error": maximum_validation_error,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

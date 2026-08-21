from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


EXP1_ROOT = Path(
    "/data/250010109/MoE_Router/experiments/"
    "20260816_a15_08_02_e01_layerwise_conditional_fine_added_accessibility/"
    "runs/a15-08-02-e01-20260816-full"
)
OUTPUT_ROOT = Path(
    "/data/250010109/Research_System/daily_research_reports/0817/docs/"
    "candidate_figures"
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def render_cumulative_vs_incremental() -> None:
    capability = [
        row
        for row in read_rows(EXP1_ROOT / "tables/capability_guards.csv")
        if row["object"].startswith("Z_")
    ]
    primary = [
        row
        for row in read_rows(EXP1_ROOT / "tables/layerwise_primary.csv")
        if row["eligibility"] == "ELIGIBLE"
    ]

    layers = np.asarray([int(row["layer"]) for row in capability])
    x_accuracy = 100 * np.asarray(
        [float(row["x_confirmation_accuracy"]) for row in capability]
    )
    z_accuracy = 100 * np.asarray(
        [float(row["confirmation_accuracy"]) for row in capability]
    )

    primary_layers = np.asarray([int(row["layer"]) for row in primary])
    matched_excess = np.asarray([float(row["matched_excess"]) for row in primary])
    simultaneous_lcb = np.asarray([float(row["sim_lcb"]) for row in primary])
    simultaneous_ucb = np.asarray([float(row["sim_ucb"]) for row in primary])
    errors = np.vstack(
        [matched_excess - simultaneous_lcb, simultaneous_ucb - matched_excess]
    )

    admitted = {24, 28}
    unresolved = {25}

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(12.5, 8.0),
        sharex=True,
        gridspec_kw={"height_ratios": [1.05, 1.0], "hspace": 0.12},
    )
    fig.suptitle(
        "Late cumulative fine accessibility and local per-block added accessibility",
        fontsize=16,
    )

    top = axes[0]
    top.plot(
        layers,
        x_accuracy,
        color="#7f8c8d",
        linestyle="--",
        marker="o",
        markersize=3.8,
        linewidth=1.8,
        label=r"$X_\ell$: pre-Attention state",
    )
    top.plot(
        layers,
        z_accuracy,
        color="#2b6cb0",
        marker="o",
        markersize=4.2,
        linewidth=2.2,
        label=r"$Z_\ell$: post-Attention state",
    )
    for layer in sorted(admitted):
        index = int(np.where(layers == layer)[0][0])
        top.scatter(
            layer,
            z_accuracy[index],
            s=95,
            color="#d94841",
            edgecolor="white",
            linewidth=1.2,
            zorder=5,
        )
    top.axvspan(23.5, 36.5, color="#2b6cb0", alpha=0.055)
    top.text(
        24.1,
        18,
        "late-stage cumulative rise",
        color="#2b6cb0",
        fontsize=10,
        va="bottom",
    )
    top.set_ylabel("Confirmation fine accuracy (%)")
    top.set_ylim(0, 105)
    top.grid(alpha=0.22)
    top.legend(loc="lower right", frameon=False, ncol=2)

    bottom = axes[1]
    bottom.errorbar(
        primary_layers,
        matched_excess,
        yerr=errors,
        fmt="o-",
        color="#4c78a8",
        markersize=3.6,
        linewidth=1.4,
        elinewidth=1.0,
        capsize=2.5,
        label="matched excess with simultaneous 95% interval",
    )
    bottom.axhline(0, color="black", linewidth=1.1)

    for layer in sorted(admitted):
        index = int(np.where(primary_layers == layer)[0][0])
        bottom.scatter(
            layer,
            matched_excess[index],
            s=105,
            color="#d94841",
            edgecolor="white",
            linewidth=1.2,
            zorder=5,
        )
        bottom.annotate(
            f"L{layer} confirmed",
            (layer, matched_excess[index]),
            xytext=(0, 12),
            textcoords="offset points",
            ha="center",
            color="#b73530",
            fontsize=9.5,
        )

    for layer in sorted(unresolved):
        index = int(np.where(primary_layers == layer)[0][0])
        bottom.scatter(
            layer,
            matched_excess[index],
            s=90,
            facecolor="white",
            edgecolor="#f28e2b",
            linewidth=2,
            zorder=5,
        )
        bottom.annotate(
            "L25 unresolved",
            (layer, matched_excess[index]),
            xytext=(24, -23),
            textcoords="offset points",
            ha="left",
            color="#c86f16",
            fontsize=9.5,
        )

    bottom.set_xlabel("Transformer block")
    bottom.set_ylabel("Per-block matched excess T\n(nats / example)")
    bottom.set_xlim(1.4, 36.6)
    bottom.set_xticks(np.arange(2, 37, 2))
    bottom.set_ylim(-0.09, 0.18)
    bottom.grid(alpha=0.22)
    bottom.legend(loc="lower left", frameon=False)

    fig.text(
        0.5,
        0.01,
        "Cumulative readability can rise while only a few blocks have confirmed "
        "added accessibility.",
        ha="center",
        fontsize=10.5,
    )
    fig.subplots_adjust(left=0.105, right=0.985, top=0.91, bottom=0.105)

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    stem = OUTPUT_ROOT / "conclusion1_cumulative_vs_incremental"
    fig.savefig(stem.with_suffix(".png"), dpi=220)
    fig.savefig(stem.with_suffix(".pdf"))
    plt.close(fig)

    key_layers = {23, 24, 25, 28, 30, 36}
    with (OUTPUT_ROOT / "conclusion1_key_data.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "layer",
                "x_confirmation_accuracy",
                "z_confirmation_accuracy",
                "matched_excess",
                "sim_lcb",
                "sim_ucb",
                "verdict",
            ]
        )
        primary_by_layer = {int(row["layer"]): row for row in primary}
        for row in capability:
            layer = int(row["layer"])
            if layer not in key_layers:
                continue
            result = primary_by_layer[layer]
            verdict = (
                "confirmed"
                if layer in admitted
                else "unresolved"
                if layer in unresolved
                else "not_confirmed"
            )
            writer.writerow(
                [
                    layer,
                    row["x_confirmation_accuracy"],
                    row["confirmation_accuracy"],
                    result["matched_excess"],
                    result["sim_lcb"],
                    result["sim_ucb"],
                    verdict,
                ]
            )


if __name__ == "__main__":
    render_cumulative_vs_incremental()

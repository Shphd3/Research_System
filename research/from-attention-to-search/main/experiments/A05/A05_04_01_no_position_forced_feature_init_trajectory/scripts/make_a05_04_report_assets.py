#!/usr/bin/env python3
"""Create compact report assets for A05_04."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


VARIANT_ORDER = [
    "V0_vanilla_random",
    "V1_random_balanced_init",
    "V2_feature_init_trainable",
    "V3_oracle_frozen",
    "V4_feature_init_inhibition",
]

SHORT = {
    "V0_vanilla_random": "V0 vanilla",
    "V1_random_balanced_init": "V1 balanced init",
    "V2_feature_init_trainable": "V2 feature init",
    "V3_oracle_frozen": "V3 oracle frozen",
    "V4_feature_init_inhibition": "V4 init + inhibition",
}


def save_seed_trajectory(metrics: pd.DataFrame, out: Path) -> None:
    seeds = sorted(metrics["seed"].unique())
    fig, axes = plt.subplots(len(seeds), 3, figsize=(16, 4.2 * len(seeds)), sharex=True)
    if len(seeds) == 1:
        axes = axes[None, :]
    ycols = [
        ("max_load", "Max load"),
        ("route_slot_nmi", "Route-slot NMI"),
        ("target_accuracy", "Target accuracy"),
    ]
    for row, seed in enumerate(seeds):
        sdf = metrics[metrics["seed"] == seed]
        for col, (metric, title) in enumerate(ycols):
            ax = axes[row, col]
            for variant in VARIANT_ORDER:
                vdf = sdf[sdf["variant"] == variant].sort_values("step")
                if vdf.empty:
                    continue
                ax.plot(vdf["step"], vdf[metric], marker="o", linewidth=1.8, label=SHORT[variant])
            ax.set_title(f"seed {seed}: {title}")
            ax.set_xlabel("step")
            ax.set_ylim(-0.03, 1.03)
            ax.grid(True, alpha=0.3)
            if col == 0:
                ax.set_ylabel(metric)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=True)
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(out, dpi=180)
    plt.close(fig)


def save_final_bar(finals: pd.DataFrame, out: Path) -> None:
    finals = finals.copy()
    finals["variant"] = pd.Categorical(finals["variant"], VARIANT_ORDER, ordered=True)
    finals = finals.sort_values(["variant", "seed"])
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5), sharex=True)
    metrics = [
        ("route_slot_nmi", "Final route-slot NMI"),
        ("max_load", "Final max load"),
        ("active_experts", "Final active experts"),
    ]
    xlabels = [f"{SHORT[v]}\n{s}" for v, s in zip(finals["variant"], finals["seed"])]
    for ax, (metric, title) in zip(axes, metrics):
        ax.bar(range(len(finals)), finals[metric])
        ax.set_title(title)
        ax.set_xticks(range(len(finals)))
        ax.set_xticklabels(xlabels, rotation=80, ha="right", fontsize=7)
        ax.grid(True, axis="y", alpha=0.3)
        if metric != "active_experts":
            ax.set_ylim(0, 1.05)
    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)


def save_final_heatmap_grid(route: pd.DataFrame, metrics: pd.DataFrame, out: Path) -> None:
    final_step = int(metrics["step"].max())
    data = route[route["step"] == final_step]
    seeds = sorted(data["seed"].unique())
    fig, axes = plt.subplots(len(VARIANT_ORDER), len(seeds), figsize=(4.6 * len(seeds), 4.0 * len(VARIANT_ORDER)))
    for r, variant in enumerate(VARIANT_ORDER):
        for c, seed in enumerate(seeds):
            ax = axes[r, c]
            mat = (
                data[(data["variant"] == variant) & (data["seed"] == seed)]
                .pivot(index="slot", columns="expert", values="fraction")
                .reindex(index=[0, 1, 2, 3], columns=[0, 1, 2, 3])
                .fillna(0.0)
            )
            im = ax.imshow(mat.values, vmin=0, vmax=1, cmap="viridis", aspect="auto")
            for i in range(4):
                for j in range(4):
                    val = mat.iloc[i, j]
                    ax.text(j, i, f"{val:.2f}", ha="center", va="center", color="white" if val > 0.55 else "black", fontsize=8)
            row = metrics[(metrics["variant"] == variant) & (metrics["seed"] == seed) & (metrics["step"] == final_step)]
            nmi = float(row["route_slot_nmi"].iloc[0])
            max_load = float(row["max_load"].iloc[0])
            ax.set_title(f"{SHORT[variant]} s{seed}\nNMI={nmi:.2f}, max={max_load:.2f}", fontsize=9)
            ax.set_xticks(range(4))
            ax.set_yticks(range(4))
            if r == len(VARIANT_ORDER) - 1:
                ax.set_xlabel("expert")
            if c == 0:
                ax.set_ylabel("slot")
    fig.colorbar(im, ax=axes.ravel().tolist(), fraction=0.018, pad=0.02)
    fig.suptitle("Final slot-to-expert route matrix by seed", y=0.99)
    fig.subplots_adjust(left=0.06, right=0.92, top=0.95, bottom=0.05, hspace=0.65, wspace=0.28)
    fig.savefig(out, dpi=180)
    plt.close(fig)


def save_tables(metrics: pd.DataFrame, finals: pd.DataFrame, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    cols = [
        "variant",
        "seed",
        "step",
        "route_slot_nmi",
        "max_load",
        "load_entropy_norm",
        "active_experts",
        "target_accuracy",
        "probe_slot_from_h",
        "route_utility_match",
        "common_ratio",
    ]
    finals[cols].to_csv(out_dir / "final_slot_specialization_by_seed.csv", index=False)

    steps = [0, 10, 20, 50, 100, 400, 800, 1600]
    timeline = metrics[metrics["step"].isin(steps)][cols]
    timeline.to_csv(out_dir / "slot_specialization_timeline_by_seed.csv", index=False)

    first_collapse = []
    for (variant, seed), group in metrics.groupby(["variant", "seed"]):
        g = group.sort_values("step")
        hit = g[g["max_load"] >= 0.95]
        first = int(hit["step"].iloc[0]) if not hit.empty else None
        first_collapse.append(
            {
                "variant": variant,
                "seed": seed,
                "first_step_max_load_ge_0.95": first,
                "final_nmi": float(g["route_slot_nmi"].iloc[-1]),
                "final_max_load": float(g["max_load"].iloc[-1]),
                "final_accuracy": float(g["target_accuracy"].iloc[-1]),
            }
        )
    pd.DataFrame(first_collapse).to_csv(out_dir / "collapse_timing_by_seed.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result-dir", required=True)
    parser.add_argument("--figure-dir", required=True)
    parser.add_argument("--table-dir", required=True)
    args = parser.parse_args()

    result_dir = Path(args.result_dir)
    figure_dir = Path(args.figure_dir)
    table_dir = Path(args.table_dir)
    figure_dir.mkdir(parents=True, exist_ok=True)

    metrics = pd.read_csv(result_dir / "metrics_by_step.csv")
    finals = pd.read_csv(result_dir / "final_metrics_by_seed.csv")
    route = pd.read_csv(result_dir / "route_matrix_by_step.csv")

    save_seed_trajectory(metrics, figure_dir / "trajectory_by_seed.png")
    save_final_bar(finals, figure_dir / "final_slot_specialization_by_seed.png")
    save_final_heatmap_grid(route, metrics, figure_dir / "final_slot_route_heatmaps_by_seed.png")
    save_tables(metrics, finals, table_dir)


if __name__ == "__main__":
    main()

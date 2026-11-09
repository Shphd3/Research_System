#!/usr/bin/env python3
"""Create seed-level figures from A05_03 result CSV files."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


EXP_DIR = Path(__file__).resolve().parents[1]
TABLE_DIR = EXP_DIR / "tables"
FIG_DIR = EXP_DIR / "figures"


def label(row: pd.Series) -> str:
    return f"{row['pattern']}\n{row['intervention']}\n{int(row['seed'])}"


def plot_seed_trajectories(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True)
    patterns = ["repeated", "distributed_complex"]
    interventions = ["baseline_full_hidden", "logit_common_offset_cancel"]

    for ax, pattern in zip(axes[:, 0], patterns):
        for intervention in interventions:
            sub = df[(df["pattern"] == pattern) & (df["intervention"] == intervention)]
            grouped = sub.groupby("step")["max_load"]
            mean = grouped.mean()
            for seed, seed_df in sub.groupby("seed"):
                linestyle = "-" if intervention == "baseline_full_hidden" else "--"
                ax.plot(
                    seed_df["step"],
                    seed_df["max_load"],
                    linestyle=linestyle,
                    alpha=0.35,
                    linewidth=1.2,
                    label=f"{intervention} seed {seed}",
                )
            ax.plot(
                mean.index,
                mean.values,
                linestyle="-" if intervention == "baseline_full_hidden" else "--",
                linewidth=2.8,
                label=f"{intervention} mean",
            )
        ax.axhline(0.95, color="tab:red", linestyle=":", linewidth=1.2)
        ax.set_title(f"{pattern}: max load by seed")
        ax.set_ylabel("max load")
        ax.grid(alpha=0.25)
        ax.legend(fontsize=7, ncol=2)

    for ax, pattern in zip(axes[:, 1], patterns):
        for intervention in interventions:
            sub = df[(df["pattern"] == pattern) & (df["intervention"] == intervention)]
            grouped = sub.groupby("step")["target_accuracy"]
            mean = grouped.mean()
            for seed, seed_df in sub.groupby("seed"):
                linestyle = "-" if intervention == "baseline_full_hidden" else "--"
                ax.plot(
                    seed_df["step"],
                    seed_df["target_accuracy"],
                    linestyle=linestyle,
                    alpha=0.35,
                    linewidth=1.2,
                )
            ax.plot(
                mean.index,
                mean.values,
                linestyle="-" if intervention == "baseline_full_hidden" else "--",
                linewidth=2.8,
                label=f"{intervention} mean",
            )
        ax.set_title(f"{pattern}: target accuracy by seed")
        ax.set_ylabel("target accuracy")
        ax.grid(alpha=0.25)
        ax.legend(fontsize=7)

    for ax in axes[-1, :]:
        ax.set_xlabel("step")

    fig.tight_layout()
    fig.savefig(FIG_DIR / "p3_seed_level_training_load_accuracy.png", dpi=180)
    plt.close(fig)


def plot_final_seed_comparison(df: pd.DataFrame) -> None:
    final_df = df[df["step"] == df["step"].max()].copy()
    final_df = final_df.sort_values(["pattern", "seed", "intervention"])

    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
    x = range(len(final_df))
    colors = final_df["intervention"].map(
        {
            "baseline_full_hidden": "tab:blue",
            "logit_common_offset_cancel": "tab:orange",
        }
    )

    axes[0].bar(x, final_df["max_load"], color=colors)
    axes[0].axhline(0.95, color="tab:red", linestyle=":", linewidth=1.2)
    axes[0].set_ylabel("final max load")
    axes[0].set_title("P3 final load by pattern / seed / intervention")
    axes[0].grid(axis="y", alpha=0.25)

    axes[1].bar(x, final_df["target_accuracy"], color=colors)
    axes[1].set_ylabel("final target accuracy")
    axes[1].set_title("P3 final accuracy by pattern / seed / intervention")
    axes[1].grid(axis="y", alpha=0.25)

    axes[1].set_xticks(list(x))
    axes[1].set_xticklabels([label(row) for _, row in final_df.iterrows()], rotation=75, ha="right")
    axes[1].set_ylim(0.9, 1.01)
    axes[1].set_xlabel("condition")

    fig.tight_layout()
    fig.savefig(FIG_DIR / "p3_seed_final_comparison.png", dpi=180)
    plt.close(fig)


def main() -> None:
    df = pd.read_csv(TABLE_DIR / "p3_training_metrics_by_step.csv")
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    plot_seed_trajectories(df)
    plot_final_seed_comparison(df)


if __name__ == "__main__":
    main()

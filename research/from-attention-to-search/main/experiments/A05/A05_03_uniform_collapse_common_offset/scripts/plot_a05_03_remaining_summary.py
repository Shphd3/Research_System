#!/usr/bin/env python3
"""Create compact summary figures for A05_03 P4-P7 remaining protocols."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


EXP_DIR = Path(__file__).resolve().parents[1]
TABLE_DIR = EXP_DIR / "tables"
FIG_DIR = EXP_DIR / "figures"


def plot_variant_heatmap(summary: pd.DataFrame) -> None:
    rows = []
    for _, row in summary[summary["protocol"].isin(["P4", "P5", "P6"])].iterrows():
        rows.append(
            {
                "condition": f"{row['protocol']} / {row['variant']}",
                "pattern": row["pattern"],
                "final_max_load_mean": row["final_max_load_mean"],
                "collapse_rate": row["final_collapse_rate"],
            }
        )
    df = pd.DataFrame(rows)
    pivot = df.pivot_table(index="condition", columns="pattern", values="final_max_load_mean")
    collapse = df.pivot_table(index="condition", columns="pattern", values="collapse_rate")
    fig, axes = plt.subplots(1, 2, figsize=(12, max(5, 0.42 * len(pivot))), sharey=True)
    im0 = axes[0].imshow(pivot.values, vmin=0.25, vmax=1.0, cmap="viridis", aspect="auto")
    axes[0].set_title("Mean final max load")
    axes[0].set_xticks(range(len(pivot.columns)), pivot.columns, rotation=20, ha="right")
    axes[0].set_yticks(range(len(pivot.index)), pivot.index, fontsize=7)
    fig.colorbar(im0, ax=axes[0], fraction=0.04)
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            axes[0].text(j, i, f"{pivot.values[i, j]:.2f}", ha="center", va="center", color="white", fontsize=7)

    im1 = axes[1].imshow(collapse.values, vmin=0.0, vmax=1.0, cmap="magma", aspect="auto")
    axes[1].set_title("Final collapse rate")
    axes[1].set_xticks(range(len(collapse.columns)), collapse.columns, rotation=20, ha="right")
    fig.colorbar(im1, ax=axes[1], fraction=0.04)
    for i in range(collapse.shape[0]):
        for j in range(collapse.shape[1]):
            axes[1].text(j, i, f"{collapse.values[i, j]:.2f}", ha="center", va="center", color="white", fontsize=7)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "remaining_protocol_variant_heatmap.png", dpi=180)
    plt.close(fig)


def plot_selected_methods(training: pd.DataFrame) -> None:
    selected = [
        ("P4", "I0_default", "baseline"),
        ("P4", "I4_residual_subspace_orthogonal", "P4 I4 init"),
        ("P5", "P5B_logit_common_offset_cancel", "P5 logit cancel"),
        ("P6", "P6A_aux_load_balance_warmup", "P6 aux warmup"),
    ]
    final_step = training["step"].max()
    final_df = training[training["step"] == final_step].copy()
    rows = []
    for protocol, variant, label in selected:
        sub = final_df[(final_df["protocol"] == protocol) & (final_df["variant"] == variant)]
        for _, row in sub.iterrows():
            rows.append(
                {
                    "method": label,
                    "pattern": row["pattern"],
                    "seed": int(row["seed"]),
                    "max_load": row["max_load"],
                    "target_accuracy": row["target_accuracy"],
                }
            )
    df = pd.DataFrame(rows)
    df["x_label"] = df["pattern"] + "\n" + df["seed"].astype(str)
    x_labels = sorted(df["x_label"].unique())
    methods = [x[2] for x in selected]
    width = 0.18
    x = list(range(len(x_labels)))
    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
    for idx, method in enumerate(methods):
        vals = []
        accs = []
        for xl in x_labels:
            item = df[(df["x_label"] == xl) & (df["method"] == method)]
            vals.append(float(item["max_load"].iloc[0]) if len(item) else float("nan"))
            accs.append(float(item["target_accuracy"].iloc[0]) if len(item) else float("nan"))
        offset = (idx - 1.5) * width
        axes[0].bar([v + offset for v in x], vals, width=width, label=method)
        axes[1].bar([v + offset for v in x], accs, width=width, label=method)
    axes[0].axhline(0.95, color="tab:red", linestyle=":", linewidth=1)
    axes[0].set_ylabel("final max load")
    axes[0].set_title("Selected methods: final routing by seed")
    axes[0].grid(axis="y", alpha=0.25)
    axes[0].legend(ncol=2, fontsize=8)
    axes[1].set_ylabel("target accuracy")
    axes[1].set_ylim(0.9, 1.01)
    axes[1].set_title("Selected methods: target accuracy by seed")
    axes[1].set_xticks(x, x_labels, rotation=35, ha="right")
    axes[1].grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "remaining_selected_methods_by_seed.png", dpi=180)
    plt.close(fig)


def plot_p7_aggregate(p7: pd.DataFrame) -> None:
    grouped = p7.groupby(["pattern", "variant"], as_index=False).agg(
        route_utility_match_rate=("route_utility_match_rate", "mean"),
        best_expert_max_fraction=("best_expert_max_fraction", "mean"),
        router_expert_max_fraction=("router_expert_max_fraction", "mean"),
    )
    labels = [f"{r.pattern}\n{r.variant}" for r in grouped.itertuples()]
    x = range(len(labels))
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    cols = [
        ("route_utility_match_rate", "Router-best utility match"),
        ("best_expert_max_fraction", "Utility-best expert max fraction"),
        ("router_expert_max_fraction", "Router expert max fraction"),
    ]
    for ax, (col, title) in zip(axes, cols):
        ax.bar(x, grouped[col])
        ax.set_ylim(0, 1.05)
        ax.set_ylabel(col)
        ax.set_title(title)
        ax.grid(axis="y", alpha=0.25)
    axes[-1].set_xticks(list(x), labels, rotation=35, ha="right")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "remaining_p7_utility_aggregate.png", dpi=180)
    plt.close(fig)


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    summary = pd.read_csv(TABLE_DIR / "remaining_training_summary_by_condition.csv")
    training = pd.read_csv(TABLE_DIR / "remaining_training_metrics_by_step.csv")
    p7 = pd.read_csv(TABLE_DIR / "remaining_p7_forced_utility_summary.csv")
    plot_variant_heatmap(summary)
    plot_selected_methods(training)
    plot_p7_aggregate(p7)


if __name__ == "__main__":
    main()

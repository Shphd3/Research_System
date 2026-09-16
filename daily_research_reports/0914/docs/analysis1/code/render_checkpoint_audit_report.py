#!/usr/bin/env python3
"""Render the three reader-facing figures for the completed checkpoint audit."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
DOC_ROOT = HERE.parent
SOURCE_ROOT = Path(
    "/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/"
    "runs/checkpoint_audit_2x5090_0p5_1_3_5_10b_20260913T125500Z/full"
)
LABELS = ["0.5B", "1B", "3B", "5B", "10B"]
SLUGS = ["0p5b", "1b", "3b", "5b", "10b"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    figure_dir = DOC_ROOT / "figures"
    table_dir = DOC_ROOT / "tables"
    figure_dir.mkdir(parents=True, exist_ok=True)
    table_dir.mkdir(parents=True, exist_ok=True)

    receipt_path = SOURCE_ROOT / "audit_receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("status") != "PASS" or receipt.get("scope") != "FULL_FIXED_HELDOUT":
        raise RuntimeError("full fixed-heldout audit receipt is not PASS")
    summaries = []
    for label, slug in zip(LABELS, SLUGS):
        path = SOURCE_ROOT / "checkpoints" / slug / "summary.json"
        row = json.loads(path.read_text(encoding="utf-8"))
        if row["checkpoint_label"] != label or row["evaluation_tokens"] != 114_987_008:
            raise RuntimeError(f"invalid checkpoint summary: {path}")
        summaries.append(row)

    nmse = np.array([row["reconstruction_normalized_mse"] for row in summaries])
    raw_mse = np.array([row["mean_raw_mse"] for row in summaries])
    mean_active = np.array([row["mean_active_features_per_token"] for row in summaries])
    dead = np.array([row["dead_features"] for row in summaries])
    coverage = np.array([row["feature_coverage_fraction"] for row in summaries])
    spearman = np.asarray(receipt["similarity"]["frequency_spearman"])
    jsd = np.asarray(receipt["similarity"]["frequency_js_divergence"])

    with (table_dir / "first_stage_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["checkpoint", "normalized_mse", "raw_mse", "mean_active", "coverage", "dead_features", "spearman_vs_0p5b", "jsd_vs_0p5b"])
        for i, label in enumerate(LABELS):
            writer.writerow([label, nmse[i], raw_mse[i], mean_active[i], coverage[i], int(dead[i]), spearman[0, i], jsd[0, i]])

    x = np.arange(len(LABELS))
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2))
    schematic_x = np.linspace(0, 1, len(LABELS))
    axes[0].plot(x, 1.0 - 0.55 * schematic_x, marker="o")
    axes[0].set_title("Expected: reconstruction burden falls")
    axes[0].set_ylabel("Qualitative expectation (no units)")
    axes[1].plot(x, np.ones_like(x), marker="o", color="#d95f02")
    axes[1].set_title("Expected: Top-K activity stays fixed")
    axes[2].plot(x, 0.75 + 0.23 * schematic_x, marker="o", color="#1b9e77")
    axes[2].set_title("Expected: broad coverage is retained")
    for ax in axes:
        ax.set_xticks(x, LABELS)
        ax.set_xlabel("Training tokens")
        ax.grid(alpha=.25)
        ax.text(.5, -.29, "WORKING SCHEMATIC — NOT MEASURED", transform=ax.transAxes, ha="center", fontsize=9, color="crimson")
    fig.suptitle("Working expectation for an increasingly stable online SAE", fontsize=14)
    fig.tight_layout()
    fig.savefig(figure_dir / "first_stage_hypothesis.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(14.2, 4.3))
    axes[0].plot(x, nmse, marker="o", linewidth=2)
    for i, value in enumerate(nmse):
        axes[0].annotate(f"{value:.3f}", (i, value), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=8)
    axes[0].set_title("Observed reconstruction N-MSE")
    axes[0].set_ylabel("Normalized MSE")
    axes[1].bar(x, dead, color="#d95f02")
    axes[1].set_title("Observed dead features in 115M-token window")
    axes[1].set_ylabel("Count out of 30,000")
    adjacent = np.array([spearman[i, i + 1] for i in range(4)])
    axes[2].plot(np.arange(4), adjacent, marker="o", color="#1b9e77", linewidth=2)
    axes[2].set_xticks(np.arange(4), ["0.5→1", "1→3", "3→5", "5→10"])
    axes[2].set_ylim(0, 1)
    axes[2].set_title("Adjacent activation-rank similarity")
    axes[2].set_ylabel("Spearman correlation")
    for ax in axes:
        if ax is not axes[2]:
            ax.set_xticks(x, LABELS)
        ax.set_xlabel("Checkpoint transition" if ax is axes[2] else "Training tokens")
        ax.grid(axis="y", alpha=.25)
    fig.suptitle("Observed SAE health dynamics on the same 114,987,008 held-out tokens", fontsize=14)
    fig.tight_layout()
    fig.savefig(figure_dir / "first_stage_observed.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(14.2, 4.3))
    delta_nmse = nmse - nmse[0]
    axes[0].axhline(0, color="black", linewidth=1)
    axes[0].bar(x, delta_nmse, color=np.where(delta_nmse <= 0, "#1b9e77", "#d95f02"))
    axes[0].set_title("Difference from 0.5B: normalized error")
    axes[0].set_ylabel("Δ normalized MSE")
    axes[1].plot(x, raw_mse / raw_mse[0], marker="o", color="#7570b3", linewidth=2)
    axes[1].axhline(1, color="black", linewidth=1)
    axes[1].set_title("Raw error scale relative to 0.5B")
    axes[1].set_ylabel("Raw MSE ratio")
    axes[2].plot(x, spearman[0], marker="o", color="#e7298a", label="Spearman")
    axes[2].plot(x, jsd[0], marker="s", color="#66a61e", label="JSD")
    axes[2].set_title("Distribution difference from 0.5B")
    axes[2].set_ylabel("Similarity / divergence")
    axes[2].legend(frameon=False)
    for ax in axes:
        ax.set_xticks(x, LABELS)
        ax.set_xlabel("Training tokens")
        ax.grid(axis="y", alpha=.25)
    fig.suptitle("Where the measured trajectory differs from a simple monotone-stabilization picture", fontsize=14)
    fig.tight_layout()
    fig.savefig(figure_dir / "first_stage_difference.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    manifest = {
        "source_root": str(SOURCE_ROOT),
        "source_receipt_sha256": sha256(receipt_path),
        "checkpoint_summary_sha256": {
            label: sha256(SOURCE_ROOT / "checkpoints" / slug / "summary.json")
            for label, slug in zip(LABELS, SLUGS)
        },
        "outputs": {
            path.name: sha256(path)
            for path in sorted(list(figure_dir.glob("first_stage_*.png")) + [table_dir / "first_stage_metrics.csv"])
        },
    }
    (table_dir / "first_stage_source_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

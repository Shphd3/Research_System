#!/usr/bin/env python3
"""Aggregate the two completed counterfactual audits and render one decision figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
TABLES = ROOT / "tables"
FIGURES = ROOT / "figures"


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    frame = pd.concat(
        [pd.read_csv(RESULTS / "lb_layer_metrics.csv"), pd.read_csv(RESULTS / "decommon_layer_metrics.csv")],
        ignore_index=True,
    ).sort_values(["model", "layer"])
    frame.to_csv(TABLES / "layer_metrics.csv", index=False)

    summaries = []
    for model, group in frame.groupby("model", sort=True):
        summaries.append(
            {
                "model": model,
                "layers": len(group),
                "eligible_layers": int(group.eligible.astype(bool).sum()),
                "center_flip_median": group.center_flip_rate.median(),
                "center_flip_max": group.center_flip_rate.max(),
                "raw_center_flip_median": group.raw_center_flip_rate.median(),
                "shuffle_flip_median": group.shuffle_flip_rate.median(),
                "sparse_cka_center_median": group.sparse_cka_center.median(),
                "sparse_cka_center_flip_only_median": group.sparse_cka_center_flip_only.median(),
                "sparse_cka_center_flip_only_min": group.sparse_cka_center_flip_only.min(),
                "r_value_median": group.r_value.median(),
                "flip_adjusted_r_median": group.flip_adjusted_r.median(),
                "sparse_frobenius_center_median": group.sparse_frobenius_center.median(),
                "sparse_frobenius_shuffle_median": group.sparse_frobenius_shuffle.median(),
                "spectrum_tv_center_median": group.spectrum_tv_center.median(),
                "spectrum_tv_shuffle_median": group.spectrum_tv_shuffle.median(),
                "spectrum_tv_ratio_median": group.spectrum_tv_ratio.median(),
                "principal_angle_center_median_deg": group.principal_angle_mean_center_deg.median(),
                "principal_angle_shuffle_median_deg": group.principal_angle_mean_shuffle_deg.median(),
                "block_cka_center_median": group.block_cka_center.median(),
                "final_hidden_cka_center_median": group.final_hidden_cka_center.median(),
                "center_logit_kl_median": group.center_logit_kl.median(),
                "shuffle_logit_kl_median": group.shuffle_logit_kl.median(),
                "logit_kl_ratio_median": group.logit_kl_ratio.median(),
                "center_nll_delta_median": group.center_nll_delta.median(),
                "center_nll_delta_max_abs": group.center_nll_delta.abs().max(),
                "shuffle_nll_delta_median": group.shuffle_nll_delta.median(),
                "all_load_exact": bool(group.load_exact.astype(bool).all()),
                "all_noop_pass": bool(group.noop_pass.astype(bool).all()),
                "all_shared_invariant": bool((group.shared_invariance_max_abs == 0).all()),
                "all_expert_outputs_finite": bool(group.expert_bank_all_finite.astype(bool).all()),
            }
        )
    summary = pd.DataFrame(summaries)
    summary.to_csv(TABLES / "model_summary.csv", index=False)

    model_verdicts = {
        model: json.loads((RESULTS / f"{model}_verdict.json").read_text())
        for model in ["lb", "decommon"]
    }
    verdict_values = {item["verdict"] for item in model_verdicts.values()}
    combined = {
        "verdict": "insufficient" if verdict_values != {"support_h0"} and verdict_values != {"reject_h0"} else verdict_values.pop(),
        "reason": "No layer reached the preregistered 20% centered-flip gate in either model.",
        "model_verdicts": model_verdicts,
        "secondary_observation": (
            "Global spectra and final outputs changed little, but flip-only sparse-output CKA was far below "
            "the 0.90 equivalence guard; changed-token expert outputs are not interchangeable."
        ),
    }
    (RESULTS / "combined_verdict.json").write_text(json.dumps(combined, indent=2, sort_keys=True) + "\n")

    colors = {"lb": "#31688e", "decommon": "#b73779"}
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.5), constrained_layout=True)
    for model, group in frame.groupby("model", sort=True):
        group = group.sort_values("layer")
        axes[0, 0].plot(group.layer, group.center_flip_rate, marker="o", label=model, color=colors[model])
        axes[0, 1].plot(
            group.layer,
            group.sparse_cka_center_flip_only,
            marker="o",
            label=model,
            color=colors[model],
        )
        axes[1, 0].plot(group.layer, group.spectrum_tv_ratio, marker="o", label=model, color=colors[model])
        axes[1, 1].plot(
            group.layer,
            group.center_nll_delta.abs(),
            marker="o",
            label=f"{model} centered",
            color=colors[model],
        )
        axes[1, 1].plot(
            group.layer,
            group.shuffle_nll_delta.abs(),
            marker="x",
            linestyle="--",
            label=f"{model} shuffle",
            color=colors[model],
            alpha=0.75,
        )

    axes[0, 0].axhline(0.20, color="black", linestyle="--", linewidth=1, label="20% gate")
    axes[0, 0].set_title("Centered route flip rate")
    axes[0, 0].set_ylabel("Fraction of tokens")
    axes[0, 0].set_ylim(0, 0.23)

    axes[0, 1].axhline(0.90, color="black", linestyle="--", linewidth=1, label="H0 guard")
    axes[0, 1].set_title("Sparse-output CKA on flipped tokens")
    axes[0, 1].set_ylabel("Linear CKA")
    axes[0, 1].set_ylim(0.25, 1.0)

    axes[1, 0].set_title("Global spectrum change / shuffle")
    axes[1, 0].set_ylabel("TV-distance ratio")
    axes[1, 0].set_yscale("log")

    axes[1, 1].set_title("Held-out NLL change")
    axes[1, 1].set_ylabel("Absolute nat/token")
    axes[1, 1].set_yscale("log")

    for axis in axes.flat:
        axis.set_xlabel("MoE layer")
        axis.set_xticks(range(1, 13))
        axis.grid(alpha=0.2)
        axis.legend(fontsize=8)

    fig.suptitle("Router-output counterfactual: weak global treatment, strong changed-token effect", fontsize=14)
    fig.savefig(FIGURES / "router_output_counterfactual.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()

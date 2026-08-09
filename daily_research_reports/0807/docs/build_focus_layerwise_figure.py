from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from matplotlib.colors import TwoSlopeNorm
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[3]
WORKER = (
    ROOT
    / "Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active"
    / "a15_01_09_e01_qwen3_mlp_parameter_commonality_attention_write_semantic_location"
)
RUNS = WORKER / "runs"
SEMANTIC_RUN = RUNS / "a15-01-09-e01-s-20260807T061000Z"
RESPONSE_RUN = RUNS / "a15-01-09-e01-r-20260807T061000Z"
OUT_FIGURE = ROOT / "daily_research_reports/0807/figures/focus_layerwise_semantic_granularity.png"
OUT_Q_FIGURE = ROOT / "daily_research_reports/0807/figures/focus_post_o_proj_q_heatmaps.png"
OUT_TABLE = ROOT / "daily_research_reports/0807/docs/focus_layerwise_semantic_granularity.csv"
OUT_AUDIT = ROOT / "daily_research_reports/0807/docs/focus_layerwise_semantic_granularity_audit.json"
Q_TABLE = (
    ROOT
    / "daily_research_reports/0807/docs/qwen3_post_o_proj_full_attention_semantic_variance_atlas"
    / "tables/band_metrics.csv"
)

sys.path.insert(0, str(WORKER))
from bootstrap_metrics import bootstrap_plan  # noqa: E402
from common import CACHE, cube_from_rows, load_json, percentile_interval  # noqa: E402


LAYERS = np.arange(1, 37)
EARLY = np.arange(0, 12)
LATE = np.arange(24, 35)


def layer_array(metrics: dict, role: str, field: str) -> np.ndarray:
    return np.asarray(
        [metrics[str(layer)]["operators"]["native"]["full"]["roles"][role][field] for layer in LAYERS],
        dtype=float,
    )


def keyed_array(values: dict | list) -> np.ndarray:
    if isinstance(values, dict):
        return np.asarray([values[str(layer)] for layer in LAYERS], dtype=float)
    return np.asarray(values, dtype=float)


def contrast(values: np.ndarray) -> float:
    return float(np.median(values[LATE]) - np.median(values[EARLY]))


def trend_audit(values: np.ndarray) -> dict[str, float | int]:
    rho, p_value = spearmanr(LAYERS, values)
    return {
        "early_median": float(np.median(values[EARLY])),
        "late_median": float(np.median(values[LATE])),
        "late_minus_early": contrast(values),
        "block_36": float(values[-1]),
        "spearman_rho": float(rho),
        "spearman_p": float(p_value),
        "adjacent_increases": int(np.sum(np.diff(values) > 0)),
        "adjacent_comparisons": 35,
    }


@torch.inference_mode()
def bootstrap_layer_statistics(
    projected_cube: torch.Tensor,
    plan: dict[str, np.ndarray],
    batch_size: int = 16,
) -> dict[str, np.ndarray]:
    x = projected_cube.reshape(8, 8, 8, projected_cube.shape[-1]).to(device="cuda:0", dtype=torch.float32)
    centers = (torch.arange(16, device="cuda:0", dtype=torch.float64) + 0.5) / 16
    outputs = {key: [] for key in ("fair_gap", "coarse_centroid", "fine_centroid")}
    for start in range(0, len(plan["parents"]), batch_size):
        stop = min(start + batch_size, len(plan["parents"]))
        parents = torch.from_numpy(plan["parents"][start:stop]).to("cuda:0")
        children = torch.from_numpy(plan["children"][start:stop]).to("cuda:0")
        expressions = torch.from_numpy(plan["expressions"][start:stop]).to("cuda:0")
        batch = stop - start
        parent_index = parents[:, :, None, None].expand(batch, 8, 8, 8)
        child_index = children[:, :, :, None].expand(batch, 8, 8, 8)
        selected = x[parent_index, child_index, expressions]
        child_means = selected.mean(dim=3)
        coarse_means = child_means.mean(dim=2)
        coarse_deviation = coarse_means - coarse_means.mean(dim=1, keepdim=True)
        fine_deviation = child_means - child_means.mean(dim=2, keepdim=True)
        variances = {
            "coarse": coarse_deviation.double().square().mean(dim=1),
            "fine": fine_deviation.double().square().mean(dim=(1, 2)),
        }
        outputs["fair_gap"].append(
            torch.log(
                variances["fine"].sum(dim=1).clamp_min(1e-30)
                / variances["coarse"].sum(dim=1).clamp_min(1e-30)
            ).cpu()
        )
        for role in ("coarse", "fine"):
            band_variance = variances[role].reshape(batch, 16, 256).mean(dim=2)
            share = band_variance / band_variance.sum(dim=1, keepdim=True).clamp_min(1e-30)
            outputs[f"{role}_centroid"].append((share * centers).sum(dim=1).cpu())
    return {key: torch.cat(chunks).numpy() for key, chunks in outputs.items()}


def bootstrap_fair_gap_and_centroids(
    parts: Path,
    n_bootstrap: int = 2000,
) -> tuple[dict[str, list[float]], dict[str, np.ndarray]]:
    rows = load_json(CACHE / "semantic_state_rows.json")
    plan = bootstrap_plan(n_bootstrap, 1701)
    layerwise_bootstrap = {key: [] for key in ("fair_gap", "coarse_centroid", "fine_centroid")}
    for layer in LAYERS:
        payload = torch.load(
            parts / "projection_parts" / f"layer_{layer:02d}.pt",
            map_location="cpu",
            weights_only=False,
        )
        projection = payload["operators"]["native"]["projection"]
        cube = cube_from_rows(projection, rows)
        layer_statistics = bootstrap_layer_statistics(cube, plan)
        for key in layerwise_bootstrap:
            layerwise_bootstrap[key].append(layer_statistics[key])
    boot = {key: np.stack(values) for key, values in layerwise_bootstrap.items()}
    intervals = {}
    for key, matrix in boot.items():
        boot_contrast = np.median(matrix[LATE], axis=0) - np.median(matrix[EARLY], axis=0)
        intervals[key] = percentile_interval(boot_contrast)
    raw_delta_boot = boot["fine_centroid"] - boot["coarse_centroid"]
    intervals["raw_delta"] = percentile_interval(
        np.median(raw_delta_boot[LATE], axis=0) - np.median(raw_delta_boot[EARLY], axis=0)
    )
    return intervals, boot


def shade_windows(ax: plt.Axes) -> None:
    ax.axvspan(0.5, 12.5, color="#4C78A8", alpha=0.07, lw=0)
    ax.axvspan(24.5, 35.5, color="#F58518", alpha=0.07, lw=0)
    ax.axvline(35.5, color="#777777", lw=0.8, ls="--", alpha=0.8)


def main() -> None:
    semantic_metrics = json.loads(
        (SEMANTIC_RUN / "semantic/analysis/semantic_layer_metrics.json").read_text(encoding="utf-8")
    )
    semantic_summary = json.loads(
        (SEMANTIC_RUN / "semantic/analysis/semantic_summary.json").read_text(encoding="utf-8")
    )
    response_summary = json.loads(
        (RESPONSE_RUN / "response/analysis/response_summary.json").read_text(encoding="utf-8")
    )

    coarse_between = layer_array(semantic_metrics, "coarse", "between_trace")
    fine_between = layer_array(semantic_metrics, "fine", "between_trace")
    coarse_noise = layer_array(semantic_metrics, "coarse", "expression_trace")
    fine_noise = layer_array(semantic_metrics, "fine", "expression_trace")
    if not np.allclose(coarse_noise, fine_noise, rtol=0, atol=0):
        raise RuntimeError("coarse and fine must use exactly the same expression-noise denominator")
    coarse_separability = coarse_between / coarse_noise
    fine_separability = fine_between / coarse_noise
    fair_gap = np.log(fine_separability / coarse_separability)

    coarse_centroid = layer_array(semantic_metrics, "coarse", "raw_centroid")
    fine_centroid = layer_array(semantic_metrics, "fine", "raw_centroid")
    raw_delta = fine_centroid - coarse_centroid
    gain_input_delta = keyed_array(response_summary["delta_input_gain"]["layerwise_delta_centroid"])
    nonlinear_delta = keyed_array(response_summary["mlp_response"]["layerwise_delta_centroid"])
    raw_log_share = np.asarray(
        [
            semantic_metrics[str(layer)]["operators"]["native"]["full"]["raw_fine_coarse_log_share"]
            for layer in LAYERS
        ],
        dtype=float,
    )

    q_frame = pd.read_csv(Q_TABLE)
    q_frame = q_frame[q_frame["split"].eq("confirmation")]
    q_matrices = {
        role: q_frame[q_frame["role"].eq(role)]
        .pivot(index="layer", columns="band_index", values="q")
        .sort_index()
        .sort_index(axis=1)
        .to_numpy()
        for role in ("coarse", "fine")
    }
    q_log10 = {role: np.log10(np.maximum(matrix, 1e-30)) for role, matrix in q_matrices.items()}
    q_log_ratio = np.log(np.maximum(q_matrices["fine"], 1e-30) / np.maximum(q_matrices["coarse"], 1e-30))
    q_layer_median = {role: np.median(matrix, axis=1) for role, matrix in q_log10.items()}

    bootstrap_ci95, bootstrap_values = bootstrap_fair_gap_and_centroids(
        SEMANTIC_RUN / "semantic", n_bootstrap=2000
    )
    gap_ci95 = bootstrap_ci95["fair_gap"]

    leave_one_parent = []
    for omitted in range(8):
        values = []
        for layer in LAYERS:
            record = semantic_metrics[str(layer)]["operators"]["native"]["leave_one_parent"][omitted]
            roles = record["roles"]
            values.append(np.log(roles["fine"]["between_trace"] / roles["coarse"]["between_trace"]))
        leave_one_parent.append(contrast(np.asarray(values)))

    audit = {
        "definitions": {
            "separability": "S_l,g = tr(B_l,g) / tr(W_l,expr)",
            "fair_gap": "Q_l = log(S_l,fine / S_l,coarse) = log(tr(B_l,fine) / tr(B_l,coarse))",
            "raw_rank_centroid": "C_l,g = sum_k p_l,g,k * (k-0.5)/16",
            "fine_specific_location": "DeltaC_l = C_l,fine - C_l,coarse",
            "early": "blocks 1-12",
            "late": "blocks 25-35; block 36 reported separately",
        },
        "fair_gap": {
            **trend_audit(fair_gap),
            "late_minus_early_bootstrap_ci95": gap_ci95,
            "design_late_minus_early": None,
            "confirmation_late_minus_early": None,
            "leave_one_parent_late_minus_early": leave_one_parent,
        },
        "coarse_raw_centroid": trend_audit(coarse_centroid),
        "fine_raw_centroid": trend_audit(fine_centroid),
        "raw_fine_minus_coarse": {
            **trend_audit(raw_delta),
            "registered_ci95": semantic_summary["operators"]["native"]["raw"]["T_ci95"],
        },
        "gain_weighted_input_fine_minus_coarse": {
            **trend_audit(gain_input_delta),
            "registered_ci95": response_summary["delta_input_gain"]["T_ci95"],
        },
        "nonlinear_response_fine_minus_coarse": {
            **trend_audit(nonlinear_delta),
            "registered_ci95": response_summary["mlp_response"]["T_ci95"],
        },
        "source_files": {
            "semantic_metrics": str(
                (SEMANTIC_RUN / "semantic/analysis/semantic_layer_metrics.json").relative_to(ROOT)
            ),
            "semantic_summary": str((SEMANTIC_RUN / "semantic/analysis/semantic_summary.json").relative_to(ROOT)),
            "response_summary": str(
                (RESPONSE_RUN / "response/analysis/response_summary.json").relative_to(ROOT)
            ),
            "post_o_proj_q_band_metrics": str(Q_TABLE.relative_to(ROOT)),
        },
        "background_normalized_q": {
            role: {
                "block_24_to_25_delta_median_log10_q": float(q_layer_median[role][24] - q_layer_median[role][23]),
                "early_median_log10_q": float(np.median(q_layer_median[role][EARLY])),
                "late_median_log10_q": float(np.median(q_layer_median[role][LATE])),
                "adjacent_increases": int(np.sum(np.diff(q_layer_median[role]) > 0)),
            }
            for role in ("coarse", "fine")
        },
    }
    audit["coarse_raw_centroid"]["late_minus_early_bootstrap_ci95"] = bootstrap_ci95["coarse_centroid"]
    audit["fine_raw_centroid"]["late_minus_early_bootstrap_ci95"] = bootstrap_ci95["fine_centroid"]
    audit["raw_fine_minus_coarse"]["local_reanalysis_ci95"] = bootstrap_ci95["raw_delta"]

    for section in ("design", "confirmation"):
        values = []
        for layer in LAYERS:
            roles = semantic_metrics[str(layer)]["operators"]["native"][section]["roles"]
            values.append(np.log(roles["fine"]["between_trace"] / roles["coarse"]["between_trace"]))
        audit["fair_gap"][f"{section}_late_minus_early"] = contrast(np.asarray(values))

    OUT_AUDIT.parent.mkdir(parents=True, exist_ok=True)
    OUT_AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    rows = zip(
        LAYERS,
        coarse_separability,
        fine_separability,
        fair_gap,
        coarse_centroid,
        fine_centroid,
        raw_delta,
        gain_input_delta,
        nonlinear_delta,
        strict=True,
    )
    with OUT_TABLE.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "layer",
                "S_coarse_common_noise",
                "S_fine_common_noise",
                "Q_log_fine_over_coarse",
                "C_raw_coarse",
                "C_raw_fine",
                "DeltaC_raw",
                "DeltaC_gain_weighted_actual_mlp_input",
                "DeltaC_nonlinear_mlp_response",
            ]
        )
        writer.writerows(rows)

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "legend.fontsize": 9,
            "figure.dpi": 160,
        }
    )
    OUT_FIGURE.parent.mkdir(parents=True, exist_ok=True)

    q_values = np.concatenate([q_log10["coarse"].ravel(), q_log10["fine"].ravel()])
    q_low, q_high = np.quantile(q_values, [0.02, 0.98])
    ratio_limit = max(float(np.quantile(np.abs(q_log_ratio), 0.98)), 1e-6)
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 5.2), constrained_layout=True)
    for ax, role in zip(axes[:2], ("coarse", "fine"), strict=True):
        image_q = ax.imshow(
            q_log10[role],
            aspect="auto",
            origin="lower",
            extent=[0.5, 16.5, 0.5, 36.5],
            cmap="viridis",
            vmin=q_low,
            vmax=q_high,
            interpolation="nearest",
        )
        ax.set_title(f"{role}: log10 q", loc="left", fontweight="bold")
        ax.axhline(24.5, color="white", lw=1.2, ls="--")
    image_ratio = axes[2].imshow(
        q_log_ratio,
        aspect="auto",
        origin="lower",
        extent=[0.5, 16.5, 0.5, 36.5],
        cmap="RdBu_r",
        norm=TwoSlopeNorm(vmin=-ratio_limit, vcenter=0, vmax=ratio_limit),
        interpolation="nearest",
    )
    axes[2].set_title("log(q_fine / q_coarse)", loc="left", fontweight="bold")
    axes[2].axhline(24.5, color="#333333", lw=1.2, ls="--")
    for ax in axes:
        ax.set_xticks([1, 4, 8, 12, 16], ["F1", "F4", "F8", "F12", "F16"])
        ax.set_yticks([1, 6, 12, 18, 24, 25, 30, 35, 36])
        ax.set_xlabel("DCLM covariance band  (F1=head, F16=tail)")
        ax.set_ylabel("Transformer block")
    fig.colorbar(image_q, ax=axes[:2], fraction=0.025, pad=0.025, label="log10 background-normalized variance q")
    fig.colorbar(image_ratio, ax=axes[2], fraction=0.05, pad=0.025, label="natural-log ratio")
    fig.suptitle("Post-o_proj layerwise semantic variance normalized by DCLM background", fontsize=14, fontweight="bold")
    fig.savefig(OUT_Q_FIGURE, bbox_inches="tight", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9.5, 5.0), constrained_layout=True)
    shade_windows(ax)
    ax.plot(LAYERS, coarse_centroid, color="#4C78A8", marker="o", ms=3.4, lw=1.8, label="coarse")
    ax.plot(LAYERS, fine_centroid, color="#E45756", marker="o", ms=3.4, lw=1.8, label="fine")
    ax.set_title("Raw post-o_proj variance moves to later local MLP parameter ranks", loc="left", fontweight="bold")
    ax.set_ylabel(r"rank centroid $C_\ell$  (0=head, 1=tail)")
    ax.set_xlabel("Transformer block (each layer has its own sorted parameter basis)")
    ax.set_xlim(1, 36)
    ax.set_xticks([1, 6, 12, 18, 24, 25, 30, 35, 36])
    ax.legend(frameon=False, loc="upper left")
    raw_ci = semantic_summary["operators"]["native"]["raw"]["T_ci95"]
    ax.text(
        0.98,
        0.04,
        f"early → late median\ncoarse {np.median(coarse_centroid[EARLY]):.3f} → {np.median(coarse_centroid[LATE]):.3f}\n"
        f"fine      {np.median(fine_centroid[EARLY]):.3f} → {np.median(fine_centroid[LATE]):.3f}\n"
        f"difference of shifts {contrast(raw_delta):+.4f}, 95% CI [{raw_ci[0]:+.4f}, {raw_ci[1]:+.4f}]",
        transform=ax.transAxes,
        va="bottom",
        ha="right",
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#CCCCCC", "alpha": 0.9},
    )
    ax.grid(True, axis="y", color="#DDDDDD", lw=0.7, alpha=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(OUT_FIGURE, bbox_inches="tight", dpi=200)
    plt.close(fig)

    print(
        json.dumps(
            {
                "q_figure": str(OUT_Q_FIGURE),
                "parameter_figure": str(OUT_FIGURE),
                "table": str(OUT_TABLE),
                "audit": str(OUT_AUDIT),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

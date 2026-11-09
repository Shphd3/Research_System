#!/usr/bin/env python3
"""A07_E01 high-dimensional uniform centered-M4 audit.

The uniform-sphere quadratic form x^T H x can be evaluated from the eigenvalues
of H by sampling z_i^2 / sum_j z_j^2 with z ~ N(0, I). This keeps the run
faithful to the protocol while avoiding repeated dense quadratic products.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


EXPERIMENT_DIR = Path(__file__).resolve().parent
TABLE_DIR = EXPERIMENT_DIR / "tables"
FIGURE_DIR = EXPERIMENT_DIR / "figures"

GLOBAL_SEED = 20260617
DIMS = [2, 4, 8, 16, 32, 64, 128, 256, 512]
N_SEEDS = 100
N_EVAL = 20_000
N_CALIB = 5_000
EPS_DEGENERATE = 1e-10
LOW_MARGIN_EPS = 1e-4
RANKS = [1, 2, 4, 8, 16, 32, 64, 128]

CONDITIONS = [
    "random_gaussian",
    "equal_isotropic",
    "unequal_isotropic",
    "random_anisotropic",
    "separated_low_rank",
    "near_identical",
    "spiked_traceless_counterexample",
    "balanced_spectrum_control",
]


@dataclass(frozen=True)
class ConditionSpectrum:
    condition: str
    d: int
    seed: int
    raw_diff_eigs: np.ndarray
    centered_diff_eigs: np.ndarray
    g1_spectrum: np.ndarray
    g2_spectrum: np.ndarray
    low_rank_mode: str


def rng_for(*parts: int) -> np.random.Generator:
    seed = GLOBAL_SEED
    for part in parts:
        seed = (seed * 6364136223846793005 + int(part) + 1442695040888963407) % (2**63 - 1)
    return np.random.default_rng(seed)


def center_eigs(eigs: np.ndarray) -> np.ndarray:
    return eigs - float(np.mean(eigs))


def spectral_stats(centered_eigs: np.ndarray) -> Dict[str, float]:
    fro = float(np.linalg.norm(centered_eigs))
    op = float(np.max(np.abs(centered_eigs))) if centered_eigs.size else 0.0
    if fro < 1e-14:
        return {
            "r3": 0.0,
            "operator_to_frobenius": 0.0,
            "frobenius": 0.0,
            "operator": 0.0,
        }
    r3 = float(np.sum(np.abs(centered_eigs) ** 3) / (np.sum(centered_eigs**2) ** 1.5))
    return {
        "r3": r3,
        "operator_to_frobenius": op / fro,
        "frobenius": fro,
        "operator": op,
    }


def random_gaussian_like_spectrum(d: int, seed: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Fast spectrum proxy for iid Gaussian expert response matrices.

    Exact Wishart eigendecompositions for every seed and dimension are much
    slower than the rest of this static audit. This proxy keeps the properties
    needed for A07_E01's decision: positive response spectra, unequal trace
    budgets, and spread-out centered score differences.
    """
    rng = rng_for(17, d, seed)
    g1 = np.sort(rng.lognormal(mean=-0.5 * 0.45**2, sigma=0.45, size=d))[::-1]
    g2 = np.sort(rng.lognormal(mean=-0.5 * 0.45**2, sigma=0.45, size=d))[::-1]
    trace_bias = rng.normal(scale=0.15 / math.sqrt(d))
    g1 = g1 * (1.0 + trace_bias)
    g2 = g2 * (1.0 - trace_bias)
    raw = g1 - g2
    centered = center_eigs(raw)
    return raw, centered, g1, g2


def make_spectrum(condition: str, d: int, seed: int) -> ConditionSpectrum:
    rng = rng_for(31, d, seed, CONDITIONS.index(condition))
    if condition == "random_gaussian":
        raw, centered, g1, g2 = random_gaussian_like_spectrum(d, seed)
        mode = "gaussian_like_spectrum_proxy"
    elif condition == "equal_isotropic":
        g1 = np.ones(d)
        g2 = np.ones(d)
        raw = g1 - g2
        centered = center_eigs(raw)
        mode = "commuting_exact"
    elif condition == "unequal_isotropic":
        g1 = np.full(d, 1.2)
        g2 = np.full(d, 0.8)
        raw = g1 - g2
        centered = center_eigs(raw)
        mode = "commuting_exact"
    elif condition == "random_anisotropic":
        g1 = np.sort(rng.lognormal(mean=0.0, sigma=0.7, size=d))[::-1]
        g2 = np.sort(rng.lognormal(mean=0.0, sigma=0.7, size=d))[::-1]
        raw = g1 - g2
        centered = center_eigs(raw)
        mode = "commuting_spectrum_model"
    elif condition == "separated_low_rank":
        k = max(1, min(d // 8, 16))
        g1 = np.full(d, 0.2)
        g2 = np.full(d, 0.2)
        g1[:k] += 3.0
        g2[k : 2 * k] += 3.0
        raw = g1 - g2
        centered = center_eigs(raw)
        mode = "commuting_exact"
    elif condition == "near_identical":
        base = np.sort(rng.lognormal(mean=0.0, sigma=0.5, size=d))[::-1]
        noise = 0.01 * rng.normal(size=d)
        g1 = base
        g2 = np.maximum(base + noise, 1e-6)
        raw = g1 - g2
        centered = center_eigs(raw)
        mode = "commuting_spectrum_model"
    elif condition == "spiked_traceless_counterexample":
        raw = np.full(d, -1.0)
        raw[0] = float(d - 1)
        centered = center_eigs(raw)
        g1 = np.maximum(centered, 0.0) + 1.0
        g2 = np.maximum(-centered, 0.0) + 1.0
        mode = "difference_constructed"
    elif condition == "balanced_spectrum_control":
        vals = rng.lognormal(mean=0.0, sigma=0.3, size=d // 2)
        centered = np.concatenate([vals, -vals])
        if centered.size < d:
            centered = np.concatenate([centered, np.array([0.0])])
        rng.shuffle(centered)
        raw = centered.copy()
        g1 = np.maximum(centered, 0.0) + 1.0
        g2 = np.maximum(-centered, 0.0) + 1.0
        mode = "difference_constructed"
    else:
        raise ValueError(condition)
    return ConditionSpectrum(condition, d, seed, raw, centered, g1, g2, mode)


def sample_sphere_weights(d: int, n: int, rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(n, d))
    z2 = z * z
    return z2 / np.sum(z2, axis=1, keepdims=True)


def scores_from_eigs(weights: np.ndarray, eigs: np.ndarray) -> np.ndarray:
    return weights @ eigs


def metric_row(
    spec: ConditionSpectrum,
    method: str,
    scores_eval: np.ndarray,
    scores_calib: np.ndarray | None,
    threshold: float = 0.0,
) -> Dict[str, float | int | str]:
    shifted = scores_eval - threshold
    margin = np.abs(shifted)
    selected = shifted > 0
    load1 = float(np.mean(selected))
    stats = spectral_stats(spec.centered_diff_eigs)
    return {
        "condition": spec.condition,
        "d": spec.d,
        "seed": spec.seed,
        "method": method,
        "load1": load1,
        "load_error": abs(load1 - 0.5),
        "mean_margin": float(np.mean(margin)),
        "median_margin": float(np.median(margin)),
        "low_margin_fraction": float(np.mean(margin < LOW_MARGIN_EPS)),
        "degeneracy_rate": float(np.mean(np.abs(shifted) < EPS_DEGENERATE)),
        "threshold": threshold,
        "calib_load_error": np.nan
        if scores_calib is None
        else abs(float(np.mean((scores_calib - threshold) > 0)) - 0.5),
        "r3": stats["r3"],
        "operator_to_frobenius": stats["operator_to_frobenius"],
        "centered_frobenius": stats["frobenius"],
        "centered_operator": stats["operator"],
    }


def top_r_diff_spectrum(spec: ConditionSpectrum, r: int, weighted: bool) -> np.ndarray:
    r = min(r, spec.d)
    if weighted:
        g1 = np.zeros(spec.d)
        g2 = np.zeros(spec.d)
        g1[:r] = spec.g1_spectrum[:r]
        g2[:r] = spec.g2_spectrum[:r]
    else:
        g1 = np.zeros(spec.d)
        g2 = np.zeros(spec.d)
        g1[:r] = 1.0
        g2[:r] = 1.0
    return center_eigs(g1 - g2)


def low_rank_rows(spec: ConditionSpectrum, weights_eval: np.ndarray, full_centered_scores: np.ndarray) -> List[Dict[str, float | int | str]]:
    rows: List[Dict[str, float | int | str]] = []
    full_labels = full_centered_scores > 0
    full_margin = float(np.mean(np.abs(full_centered_scores)))
    for r in RANKS:
        if r > spec.d:
            continue
        for weighted in [True, False]:
            approx_eigs = top_r_diff_spectrum(spec, r, weighted=weighted)
            approx_scores = scores_from_eigs(weights_eval, approx_eigs)
            labels = approx_scores > 0
            margin = np.abs(approx_scores)
            rows.append(
                {
                    "condition": spec.condition,
                    "d": spec.d,
                    "seed": spec.seed,
                    "rank": r,
                    "method": "weighted_top_r" if weighted else "unweighted_top_r",
                    "low_rank_mode": spec.low_rank_mode,
                    "load_error": abs(float(np.mean(labels)) - 0.5),
                    "mean_margin": float(np.mean(margin)),
                    "margin_retention_vs_full": np.nan if full_margin < 1e-14 else float(np.mean(margin) / full_margin),
                    "agreement_with_centered_m4": float(np.mean(labels == full_labels)),
                    "rank_energy_fraction": float(
                        np.sum(np.abs(approx_eigs)) / max(np.sum(np.abs(spec.centered_diff_eigs)), 1e-14)
                    ),
                }
            )
    return rows


def aggregate(df: pd.DataFrame, group_cols: List[str]) -> pd.DataFrame:
    numeric = [
        "load_error",
        "mean_margin",
        "median_margin",
        "low_margin_fraction",
        "degeneracy_rate",
        "calib_load_error",
        "r3",
        "operator_to_frobenius",
        "centered_frobenius",
        "centered_operator",
    ]
    agg = df.groupby(group_cols, dropna=False)[numeric].agg(["mean", "median", "std"]).reset_index()
    agg.columns = ["_".join([str(c) for c in col if c]) for col in agg.columns.to_flat_index()]
    counts = df.groupby(group_cols, dropna=False).size().reset_index(name="n")
    return counts.merge(agg, on=group_cols, how="left")


def make_figures(metric_summary: pd.DataFrame, spectral_df: pd.DataFrame, low_rank_summary: pd.DataFrame, hist_scores: pd.DataFrame) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    plot_df = metric_summary[metric_summary["condition"].isin(["random_gaussian", "spiked_traceless_counterexample", "balanced_spectrum_control"])]
    for (condition, method), sub in plot_df.groupby(["condition", "method"]):
        if method not in ["raw_m4", "centered_m4", "calibrated_m4"]:
            continue
        ax.plot(sub["d"], sub["load_error_mean"], marker="o", label=f"{condition} / {method}")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("dimension d")
    ax.set_ylabel("mean load error")
    ax.set_title("Load error versus dimension")
    ax.legend(fontsize=7, ncol=2)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "load_error_vs_dimension.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(spectral_df["r3"], spectral_df["centered_load_error"], s=12, alpha=0.45)
    ax.set_xlabel("spectral spread r3 (lower is more spread)")
    ax.set_ylabel("centered M4 load error")
    ax.set_title("Centered load error versus spectral spread")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "load_error_vs_spectral_spread.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 6))
    lr = low_rank_summary[
        (low_rank_summary["condition"].isin(["random_anisotropic", "separated_low_rank"]))
        & (low_rank_summary["method"] == "weighted_top_r")
    ]
    for (condition, d), sub in lr.groupby(["condition", "d"]):
        if d not in [32, 128, 512]:
            continue
        ax.plot(sub["rank"], sub["agreement_with_centered_m4_mean"], marker="o", label=f"{condition} d={d}")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("rank r")
    ax.set_ylabel("agreement with full centered M4")
    ax.set_title("Weighted top-r proxy agreement versus rank")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "agreement_vs_rank.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(hist_scores["score"], bins=80, alpha=0.85)
    ax.axvline(0.0, color="black", linewidth=1.0)
    ax.set_xlabel("centered M4 score difference")
    ax.set_ylabel("count")
    ax.set_title("Spiked traceless counterexample score histogram (d=128, seed=0)")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "spiked_counterexample_hist.png", dpi=180)
    plt.close(fig)


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    metric_rows: List[Dict[str, float | int | str]] = []
    low_rank_all: List[Dict[str, float | int | str]] = []
    spectral_rows: List[Dict[str, float | int | str]] = []
    hist_scores: pd.DataFrame | None = None

    for d in DIMS:
        for seed in range(N_SEEDS):
            rng = rng_for(101, d, seed)
            weights_eval = sample_sphere_weights(d, N_EVAL, rng)
            weights_calib = sample_sphere_weights(d, N_CALIB, rng)

            specs = [make_spectrum(condition, d, seed) for condition in CONDITIONS]
            raw_mat = np.stack([spec.raw_diff_eigs for spec in specs], axis=1)
            centered_mat = np.stack([spec.centered_diff_eigs for spec in specs], axis=1)
            raw_eval = weights_eval @ raw_mat
            raw_calib = weights_calib @ raw_mat
            centered_eval = weights_eval @ centered_mat
            centered_calib = weights_calib @ centered_mat

            for j, spec in enumerate(specs):
                metric_rows.append(metric_row(spec, "raw_m4", raw_eval[:, j], raw_calib[:, j]))
                metric_rows.append(metric_row(spec, "centered_m4", centered_eval[:, j], centered_calib[:, j]))
                threshold = float(np.median(raw_calib[:, j]))
                metric_rows.append(metric_row(spec, "calibrated_m4", raw_eval[:, j], raw_calib[:, j], threshold=threshold))

                stats = spectral_stats(spec.centered_diff_eigs)
                spectral_rows.append(
                    {
                        "condition": spec.condition,
                        "d": d,
                        "seed": seed,
                        "r3": stats["r3"],
                        "operator_to_frobenius": stats["operator_to_frobenius"],
                        "centered_load_error": abs(float(np.mean(centered_eval[:, j] > 0)) - 0.5),
                        "centered_mean_margin": float(np.mean(np.abs(centered_eval[:, j]))),
                    }
                )
                low_rank_all.extend(low_rank_rows(spec, weights_eval, centered_eval[:, j]))

                if spec.condition == "spiked_traceless_counterexample" and d == 128 and seed == 0:
                    hist_scores = pd.DataFrame({"score": centered_eval[:, j]})

    metric_df = pd.DataFrame(metric_rows)
    low_rank_df = pd.DataFrame(low_rank_all)
    spectral_df = pd.DataFrame(spectral_rows)

    metric_summary = aggregate(metric_df, ["condition", "d", "method"])
    spectral_summary = (
        spectral_df.groupby(["condition", "d"], dropna=False)
        .agg(
            n=("r3", "size"),
            r3_mean=("r3", "mean"),
            r3_median=("r3", "median"),
            operator_to_frobenius_mean=("operator_to_frobenius", "mean"),
            operator_to_frobenius_median=("operator_to_frobenius", "median"),
            centered_load_error_mean=("centered_load_error", "mean"),
            centered_load_error_median=("centered_load_error", "median"),
            centered_mean_margin_mean=("centered_mean_margin", "mean"),
            centered_mean_margin_median=("centered_mean_margin", "median"),
        )
        .reset_index()
    )
    low_rank_summary = (
        low_rank_df.groupby(["condition", "d", "rank", "method", "low_rank_mode"], dropna=False)
        .agg(
            n=("load_error", "size"),
            load_error_mean=("load_error", "mean"),
            load_error_median=("load_error", "median"),
            mean_margin_mean=("mean_margin", "mean"),
            agreement_with_centered_m4_mean=("agreement_with_centered_m4", "mean"),
            margin_retention_vs_full_mean=("margin_retention_vs_full", "mean"),
            rank_energy_fraction_mean=("rank_energy_fraction", "mean"),
        )
        .reset_index()
    )
    calibration_summary = metric_summary[metric_summary["method"] == "calibrated_m4"].copy()

    metric_df.to_csv(TABLE_DIR / "high_dim_metric_per_seed.csv", index=False)
    metric_summary.to_csv(TABLE_DIR / "high_dim_metric_summary.csv", index=False)
    spectral_df.to_csv(TABLE_DIR / "spectral_spread_per_seed.csv", index=False)
    spectral_summary.to_csv(TABLE_DIR / "spectral_spread_summary.csv", index=False)
    low_rank_df.to_csv(TABLE_DIR / "low_rank_approximation_per_seed.csv", index=False)
    low_rank_summary.to_csv(TABLE_DIR / "low_rank_approximation_summary.csv", index=False)
    calibration_summary.to_csv(TABLE_DIR / "calibration_summary.csv", index=False)

    if hist_scores is None:
        hist_scores = pd.DataFrame({"score": []})
    make_figures(metric_summary, spectral_df, low_rank_summary, hist_scores)

    print(f"wrote {TABLE_DIR}")
    print(f"wrote {FIGURE_DIR}")


if __name__ == "__main__":
    main()

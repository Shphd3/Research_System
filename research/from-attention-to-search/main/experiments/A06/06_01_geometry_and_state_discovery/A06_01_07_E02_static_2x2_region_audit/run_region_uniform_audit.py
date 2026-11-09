#!/usr/bin/env python3
"""2D region-uniform and radial-input audit for A06_E02."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


EXPERIMENT_DIR = Path(__file__).resolve().parent
TABLE_DIR = EXPERIMENT_DIR / "tables"
FIGURE_DIR = EXPERIMENT_DIR / "figures"

N_SEEDS = 100
N_SAMPLES = 20_000
GLOBAL_SEED = 20260617
LOW_MARGIN = 1e-4
DEGENERATE = 1e-10
SINGULAR_GAP = 1e-8


@dataclass(frozen=True)
class ExpertPair:
    condition: str
    seed: int
    a1: np.ndarray
    a2: np.ndarray


@dataclass(frozen=True)
class Distribution:
    name: str
    x: np.ndarray
    second_moment: np.ndarray
    proof_role: str


def rotation(theta: float) -> np.ndarray:
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def random_orthogonal(rng: np.random.Generator) -> np.ndarray:
    theta = rng.uniform(0.0, 2.0 * math.pi)
    mat = rotation(theta)
    if rng.random() < 0.5:
        mat[:, 0] *= -1.0
    return mat


def stable_condition_offset(condition: str) -> int:
    return {
        "C1_random_unconstrained": 11,
        "C2_orthogonal_equal_singular": 23,
        "C3_orthogonal_unequal_singular": 37,
        "C4_near_identical": 41,
        "C5_separated_anisotropic": 53,
    }[condition]


def make_pair(condition: str, seed: int) -> ExpertPair:
    rng = np.random.default_rng(GLOBAL_SEED + 1009 * seed + stable_condition_offset(condition))
    if condition == "C1_random_unconstrained":
        a1 = rng.normal(size=(2, 2))
        a2 = rng.normal(size=(2, 2))
    elif condition == "C2_orthogonal_equal_singular":
        a1 = random_orthogonal(rng) @ np.eye(2) @ random_orthogonal(rng).T
        a2 = random_orthogonal(rng) @ np.eye(2) @ random_orthogonal(rng).T
    elif condition == "C3_orthogonal_unequal_singular":
        sigma = np.diag([2.0, 0.5])
        a1 = random_orthogonal(rng) @ sigma @ random_orthogonal(rng).T
        a2 = random_orthogonal(rng) @ sigma @ random_orthogonal(rng).T
    elif condition == "C4_near_identical":
        sigma = np.diag([2.0, 0.5])
        base = random_orthogonal(rng) @ sigma @ random_orthogonal(rng).T
        a1 = base
        a2 = base + 0.01 * rng.normal(size=(2, 2))
    elif condition == "C5_separated_anisotropic":
        theta = rng.uniform(0.0, 2.0 * math.pi)
        sigma = np.diag([2.0, 0.5])
        a1 = np.eye(2) @ sigma @ rotation(theta).T
        a2 = np.eye(2) @ sigma @ rotation(theta + math.pi / 2.0).T
    else:
        raise ValueError(condition)
    return ExpertPair(condition, seed, a1, a2)


def svd_parts(a: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    u, s, vt = np.linalg.svd(a, full_matrices=True)
    return u, s, vt.T


def sample_distributions(n: int, seed: int) -> List[Distribution]:
    rng = np.random.default_rng(seed)
    theta_grid = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    unit_circle = np.stack([np.cos(theta_grid), np.sin(theta_grid)], axis=1)

    theta = rng.uniform(0.0, 2.0 * math.pi, size=n)
    radius = np.sqrt(rng.uniform(0.0, 1.0, size=n))
    uniform_disk = np.stack([radius * np.cos(theta), radius * np.sin(theta)], axis=1)

    theta = rng.uniform(0.0, 2.0 * math.pi, size=n)
    r0 = 0.5
    radius = np.sqrt(rng.uniform(r0 * r0, 1.0, size=n))
    annulus = np.stack([radius * np.cos(theta), radius * np.sin(theta)], axis=1)

    centered_square = rng.uniform(-1.0, 1.0, size=(n, 2))

    # A radially symmetric stress test: most mass is very close to the origin.
    is_inner = rng.uniform(0.0, 1.0, size=n) < 0.85
    theta = rng.uniform(0.0, 2.0 * math.pi, size=n)
    radius = np.empty(n)
    radius[is_inner] = 0.12 * np.sqrt(rng.uniform(0.0, 1.0, size=is_inner.sum()))
    radius[~is_inner] = np.sqrt(rng.uniform(0.7 * 0.7, 1.0, size=(~is_inner).sum()))
    near_origin_mixture = np.stack([radius * np.cos(theta), radius * np.sin(theta)], axis=1)

    theta = rng.uniform(0.0, 2.0 * math.pi, size=n)
    radius = 0.75 * np.sqrt(rng.uniform(0.0, 1.0, size=n))
    shifted_disk = np.stack([0.35 + radius * np.cos(theta), radius * np.sin(theta)], axis=1)

    centered_rectangle = np.stack(
        [rng.uniform(-1.5, 1.5, size=n), rng.uniform(-0.5, 0.5, size=n)], axis=1
    )

    return [
        Distribution("unit_circle", unit_circle, 0.5 * np.eye(2), "proof_baseline"),
        Distribution("uniform_disk", uniform_disk, 0.25 * np.eye(2), "radial_symmetric_uniform_region"),
        Distribution("annulus", annulus, ((1.0 + r0 * r0) / 4.0) * np.eye(2), "radial_symmetric_region"),
        Distribution("centered_square", centered_square, (1.0 / 3.0) * np.eye(2), "centered_region_with_90deg_symmetry"),
        Distribution("near_origin_mixture", near_origin_mixture, second_moment(near_origin_mixture), "radial_low_margin_stress"),
        Distribution("shifted_disk", shifted_disk, second_moment(shifted_disk), "symmetry_breaking_control"),
        Distribution("centered_rectangle", centered_rectangle, np.diag([1.5 * 1.5 / 3.0, 0.5 * 0.5 / 3.0]), "anisotropic_region_control"),
    ]


def second_moment(x: np.ndarray) -> np.ndarray:
    return (x.T @ x) / x.shape[0]


def normalize(vec: np.ndarray) -> np.ndarray | None:
    norm = float(np.linalg.norm(vec))
    if norm < 1e-12:
        return None
    return vec / norm


def prototype(v: np.ndarray, s: np.ndarray) -> np.ndarray | None:
    return normalize(s[0] * v[:, 0] + s[1] * v[:, 1])


def score(
    method: str,
    x: np.ndarray,
    a: np.ndarray,
    v: np.ndarray,
    s: np.ndarray,
    second: np.ndarray,
) -> Tuple[np.ndarray | None, str]:
    if method == "M1_signed_prototype":
        if abs(float(s[0] - s[1])) <= SINGULAR_GAP:
            return None, "undefined_equal_singular_values"
        m = prototype(v, s)
        if m is None:
            return None, "undefined_prototype"
        return x @ m, "ok"
    if method == "M2_unsigned_prototype":
        if abs(float(s[0] - s[1])) <= SINGULAR_GAP:
            return None, "undefined_equal_singular_values"
        m = prototype(v, s)
        if m is None:
            return None, "undefined_prototype"
        return (x @ m) ** 2, "ok"
    if method == "M3_top1_projection":
        if abs(float(s[0] - s[1])) <= SINGULAR_GAP:
            return None, "undefined_equal_singular_values"
        return (x @ v[:, 0]) ** 2, "ok"
    if method == "M3_fullspan_control":
        return np.sum((x @ v[:, :2]) ** 2, axis=1), "ok"

    g = a.T @ a
    if method == "M4_raw":
        return np.einsum("ni,ij,nj->n", x, g, x), "ok"
    if method == "M4_trace_centered":
        h = g - 0.5 * np.trace(g) * np.eye(2)
        return np.einsum("ni,ij,nj->n", x, h, x), "ok"
    if method == "M4_distribution_centered":
        mean_response = float(np.trace(g @ second))
        return np.einsum("ni,ij,nj->n", x, g, x) - mean_response, "ok"
    raise ValueError(method)


def route_stats(q1: np.ndarray, q2: np.ndarray) -> Dict[str, float]:
    diff = q1 - q2
    assign = diff >= 0.0
    margin = np.where(assign, diff, -diff)
    return {
        "load1": float(assign.mean()),
        "load_error": float(abs(assign.mean() - 0.5)),
        "mean_margin": float(margin.mean()),
        "median_margin": float(np.median(margin)),
        "low_margin_fraction": float((margin < LOW_MARGIN).mean()),
        "degeneracy_rate": float((np.abs(diff) < DEGENERATE).mean()),
        "diff_std": float(diff.std()),
    }


def run() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    conditions = [
        "C1_random_unconstrained",
        "C2_orthogonal_equal_singular",
        "C3_orthogonal_unequal_singular",
        "C4_near_identical",
        "C5_separated_anisotropic",
    ]
    methods = [
        "M1_signed_prototype",
        "M2_unsigned_prototype",
        "M3_top1_projection",
        "M3_fullspan_control",
        "M4_raw",
        "M4_trace_centered",
        "M4_distribution_centered",
    ]
    distributions = sample_distributions(N_SAMPLES, GLOBAL_SEED + 77)

    dist_rows = []
    for dist in distributions:
        radii = np.linalg.norm(dist.x, axis=1)
        dist_rows.append(
            {
                "distribution": dist.name,
                "proof_role": dist.proof_role,
                "n": len(dist.x),
                "mean_radius": float(radii.mean()),
                "mean_radius_sq": float((radii**2).mean()),
                "second_xx": float(dist.second_moment[0, 0]),
                "second_yy": float(dist.second_moment[1, 1]),
                "second_xy": float(dist.second_moment[0, 1]),
            }
        )

    rows = []
    for condition in conditions:
        for seed in range(N_SEEDS):
            pair = make_pair(condition, seed)
            _, s1, v1 = svd_parts(pair.a1)
            _, s2, v2 = svd_parts(pair.a2)
            trace_bias = 0.5 * float(np.trace(pair.a1.T @ pair.a1 - pair.a2.T @ pair.a2))
            for dist in distributions:
                for method in methods:
                    q1, st1 = score(method, dist.x, pair.a1, v1, s1, dist.second_moment)
                    q2, st2 = score(method, dist.x, pair.a2, v2, s2, dist.second_moment)
                    status = "ok" if st1 == "ok" and st2 == "ok" else f"{st1}/{st2}"
                    if status == "ok":
                        stats = route_stats(q1, q2)
                    else:
                        stats = {
                            "load1": np.nan,
                            "load_error": np.nan,
                            "mean_margin": np.nan,
                            "median_margin": np.nan,
                            "low_margin_fraction": np.nan,
                            "degeneracy_rate": np.nan,
                            "diff_std": np.nan,
                        }
                    rows.append(
                        {
                            "condition": condition,
                            "seed": seed,
                            "distribution": dist.name,
                            "proof_role": dist.proof_role,
                            "method": method,
                            "status": status,
                            "trace_bias": trace_bias,
                            **stats,
                        }
                    )

    df = pd.DataFrame(rows)
    dist_df = pd.DataFrame(dist_rows)
    df.to_csv(TABLE_DIR / "per_seed_region_metrics.csv", index=False)
    dist_df.to_csv(TABLE_DIR / "distribution_summary.csv", index=False)

    summary = (
        df.groupby(["condition", "distribution", "proof_role", "method"], dropna=False)
        .agg(
            n=("seed", "count"),
            load_error_mean=("load_error", "mean"),
            load_error_median=("load_error", "median"),
            load_error_std=("load_error", "std"),
            mean_margin_mean=("mean_margin", "mean"),
            mean_margin_median=("mean_margin", "median"),
            low_margin_fraction_mean=("low_margin_fraction", "mean"),
            degeneracy_rate_mean=("degeneracy_rate", "mean"),
            trace_bias_abs_mean=("trace_bias", lambda x: float(np.mean(np.abs(x)))),
        )
        .reset_index()
    )

    unit = summary[summary["distribution"] == "unit_circle"][
        ["condition", "method", "mean_margin_mean", "load_error_mean"]
    ].rename(
        columns={
            "mean_margin_mean": "unit_circle_mean_margin",
            "load_error_mean": "unit_circle_load_error",
        }
    )
    summary = summary.merge(unit, on=["condition", "method"], how="left")
    summary["margin_ratio_to_unit_circle"] = summary["mean_margin_mean"] / summary[
        "unit_circle_mean_margin"
    ].replace(0.0, np.nan)
    summary["load_error_delta_from_unit_circle"] = (
        summary["load_error_mean"] - summary["unit_circle_load_error"]
    )
    summary.to_csv(TABLE_DIR / "region_metric_summary.csv", index=False)

    make_figures(summary)


def make_figures(summary: pd.DataFrame) -> None:
    plot_conditions = [
        "C1_random_unconstrained",
        "C3_orthogonal_unequal_singular",
        "C4_near_identical",
        "C5_separated_anisotropic",
    ]
    plot_methods = ["M4_raw", "M4_trace_centered", "M4_distribution_centered"]
    dist_order = [
        "unit_circle",
        "uniform_disk",
        "annulus",
        "centered_square",
        "near_origin_mixture",
        "shifted_disk",
        "centered_rectangle",
    ]

    fig, axes = plt.subplots(2, 2, figsize=(12, 7), sharey=True)
    for ax, condition in zip(axes.ravel(), plot_conditions):
        sub = summary[(summary["condition"] == condition) & (summary["method"].isin(plot_methods))]
        for method in plot_methods:
            msub = sub[sub["method"] == method].set_index("distribution").reindex(dist_order)
            ax.plot(dist_order, msub["load_error_mean"], marker="o", label=method)
        ax.axhline(0.05, color="black", linestyle="--", linewidth=0.8)
        ax.set_title(condition)
        ax.tick_params(axis="x", rotation=40)
        ax.set_ylabel("load error")
    axes[0, 0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "m4_load_error_by_region.png", dpi=170)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(12, 7), sharey=False)
    for ax, condition in zip(axes.ravel(), plot_conditions):
        sub = summary[(summary["condition"] == condition) & (summary["method"].isin(plot_methods))]
        for method in plot_methods:
            msub = sub[sub["method"] == method].set_index("distribution").reindex(dist_order)
            ax.plot(dist_order, msub["mean_margin_mean"], marker="o", label=method)
        ax.set_title(condition)
        ax.tick_params(axis="x", rotation=40)
        ax.set_ylabel("mean margin")
    axes[0, 0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "m4_margin_by_region.png", dpi=170)
    plt.close(fig)

    c5 = summary[(summary["condition"] == "C5_separated_anisotropic") & (summary["method"].isin(plot_methods))]
    pivot = c5.pivot(index="distribution", columns="method", values="margin_ratio_to_unit_circle").reindex(dist_order)
    fig, ax = plt.subplots(figsize=(9, 4))
    pivot.plot(kind="bar", ax=ax)
    ax.axhline(1.0, color="black", linewidth=0.8)
    ax.set_ylabel("margin ratio to unit circle")
    ax.set_title("C5 margin scaling by input region")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "c5_margin_ratio_by_region.png", dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    run()

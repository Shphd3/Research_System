#!/usr/bin/env python3
"""Static 2D expert-geometry metric audit for A06_E01.

This script implements the approved protocol:
two 2x2 experts, uniform 2D inputs, four metric families, natural routing,
load calibration, sign sensitivity, degenerate controls, and partition figures.
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

N_SEEDS = 100
N_S1 = 10_000
N_DISK = 10_000
EPS_MARGIN = 1e-6
EPS_DEGENERATE = 1e-6
EPS_SINGULAR_GAP = 1e-8
ACCEPT_NATURAL_LOAD_ERROR = 0.05
ACCEPT_CALIBRATED_LOAD_ERROR = 0.02
GLOBAL_SEED = 20260616


@dataclass(frozen=True)
class ExpertPair:
    condition: str
    seed: int
    a1: np.ndarray
    a2: np.ndarray


def rotation(theta: float) -> np.ndarray:
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def random_orthogonal(rng: np.random.Generator) -> np.ndarray:
    theta = rng.uniform(0.0, 2.0 * math.pi)
    mat = rotation(theta)
    if rng.random() < 0.5:
        mat[:, 0] *= -1.0
    return mat


def make_pair(condition: str, seed: int) -> ExpertPair:
    rng = np.random.default_rng(GLOBAL_SEED + 1009 * seed + hash(condition) % 997)
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
        v1 = rotation(theta)
        v2 = rotation(theta + math.pi / 2.0)
        a1 = np.eye(2) @ sigma @ v1.T
        a2 = np.eye(2) @ sigma @ v2.T
    else:
        raise ValueError(f"unknown condition: {condition}")
    return ExpertPair(condition=condition, seed=seed, a1=a1, a2=a2)


def svd_parts(a: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    u, s, vt = np.linalg.svd(a, full_matrices=True)
    return u, s, vt.T


def sample_s1(n: int) -> np.ndarray:
    theta = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    return np.stack([np.cos(theta), np.sin(theta)], axis=1)


def sample_disk(n: int, rng: np.random.Generator) -> np.ndarray:
    theta = rng.uniform(0.0, 2.0 * math.pi, size=n)
    radius = np.sqrt(rng.uniform(0.0, 1.0, size=n))
    return np.stack([radius * np.cos(theta), radius * np.sin(theta)], axis=1)


def normalize(vec: np.ndarray) -> np.ndarray | None:
    norm = float(np.linalg.norm(vec))
    if norm < 1e-12:
        return None
    return vec / norm


def prototype(v: np.ndarray, s: np.ndarray, signs: Tuple[int, int]) -> np.ndarray | None:
    signed = s[0] * signs[0] * v[:, 0] + s[1] * signs[1] * v[:, 1]
    return normalize(signed)


def score_metric(
    metric: str,
    x: np.ndarray,
    a: np.ndarray,
    v: np.ndarray,
    s: np.ndarray,
    signs: Tuple[int, int] = (1, 1),
) -> Tuple[np.ndarray | None, str]:
    if metric == "M1_signed_prototype":
        if abs(float(s[0] - s[1])) <= EPS_SINGULAR_GAP:
            return None, "undefined_prototype_equal_singular_values"
        m = prototype(v, s, signs)
        if m is None:
            return None, "undefined_prototype"
        return x @ m, "ok"
    if metric == "M2_unsigned_prototype":
        if abs(float(s[0] - s[1])) <= EPS_SINGULAR_GAP:
            return None, "undefined_prototype_equal_singular_values"
        m = prototype(v, s, signs)
        if m is None:
            return None, "undefined_prototype"
        return (x @ m) ** 2, "ok"
    if metric == "M3_top1_projection":
        if abs(float(s[0] - s[1])) <= EPS_SINGULAR_GAP:
            return None, "undefined_top_direction_equal_singular_values"
        return (x @ v[:, 0]) ** 2, "ok"
    if metric == "M3_fullspan_control":
        return np.sum((x @ v[:, :2]) ** 2, axis=1), "ok"
    if metric == "M4_matrix_response":
        g = a.T @ a
        return np.einsum("ni,ij,nj->n", x, g, x), "ok"
    raise ValueError(f"unknown metric: {metric}")


def route_stats(q1: np.ndarray, q2: np.ndarray, threshold: float = 0.0) -> Dict[str, float]:
    diff = q1 - q2
    assign1 = diff >= threshold
    load1 = float(assign1.mean())
    raw_margin = np.where(assign1, diff, -diff)
    return {
        "load1": load1,
        "load_error": abs(load1 - 0.5),
        "mean_margin": float(raw_margin.mean()),
        "median_margin": float(np.median(raw_margin)),
        "min_margin": float(raw_margin.min()),
        "low_margin_fraction": float((raw_margin < EPS_MARGIN).mean()),
        "degeneracy_rate": float((np.abs(diff) < EPS_DEGENERATE).mean()),
        "diff_std": float(diff.std()),
        "threshold": float(threshold),
    }


def natural_validity(metric: str, status: str, stats: Dict[str, float], singular_gap_ok: bool) -> Tuple[bool, str]:
    if status != "ok":
        return False, status
    if metric == "M3_fullspan_control":
        return False, "fullspan_control_expected_degenerate"
    if metric == "M3_top1_projection" and not singular_gap_ok:
        return False, "top_direction_undefined"
    if stats["degeneracy_rate"] >= 0.95 or stats["diff_std"] <= EPS_DEGENERATE:
        return False, "degenerate_scores"
    if stats["mean_margin"] <= EPS_MARGIN:
        return False, "non_positive_margin"
    if stats["load_error"] <= ACCEPT_NATURAL_LOAD_ERROR:
        return True, "natural_load_and_margin_valid"
    return False, "natural_load_imbalanced"


def calibrated_validity(status: str, stats: Dict[str, float]) -> Tuple[bool, str]:
    if status != "ok":
        return False, status
    if stats["degeneracy_rate"] >= 0.95 or stats["diff_std"] <= EPS_DEGENERATE:
        return False, "degenerate_scores"
    if stats["load_error"] > ACCEPT_CALIBRATED_LOAD_ERROR:
        return False, "calibrated_load_imbalanced"
    if stats["mean_margin"] <= EPS_MARGIN:
        return False, "margin_not_preserved"
    return True, "calibrated_load_margin_preserved"


def sign_sensitivity(
    metric: str,
    x: np.ndarray,
    pair: ExpertPair,
    v1: np.ndarray,
    s1: np.ndarray,
    v2: np.ndarray,
    s2: np.ndarray,
) -> Dict[str, float | str]:
    if metric not in {"M1_signed_prototype", "M2_unsigned_prototype"}:
        return {
            "condition": pair.condition,
            "seed": pair.seed,
            "metric": metric,
            "sign_sensitivity_mean": np.nan,
            "sign_sensitivity_max": np.nan,
            "n_variants": 0,
            "status": "not_applicable",
        }

    base_q1, st1 = score_metric(metric, x, pair.a1, v1, s1, (1, 1))
    base_q2, st2 = score_metric(metric, x, pair.a2, v2, s2, (1, 1))
    if st1 != "ok" or st2 != "ok":
        return {
            "condition": pair.condition,
            "seed": pair.seed,
            "metric": metric,
            "sign_sensitivity_mean": np.nan,
            "sign_sensitivity_max": np.nan,
            "n_variants": 0,
            "status": f"{st1}/{st2}",
        }
    base_assign = base_q1 >= base_q2
    changes: List[float] = []
    sign_options = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for signs1 in sign_options:
        for signs2 in sign_options:
            if signs1 == (1, 1) and signs2 == (1, 1):
                continue
            q1, st1 = score_metric(metric, x, pair.a1, v1, s1, signs1)
            q2, st2 = score_metric(metric, x, pair.a2, v2, s2, signs2)
            if st1 == "ok" and st2 == "ok":
                changes.append(float(((q1 >= q2) != base_assign).mean()))
    return {
        "condition": pair.condition,
        "seed": pair.seed,
        "metric": metric,
        "sign_sensitivity_mean": float(np.mean(changes)) if changes else np.nan,
        "sign_sensitivity_max": float(np.max(changes)) if changes else np.nan,
        "n_variants": len(changes),
        "status": "ok" if changes else "no_valid_variants",
    }


def angle_of(vec: np.ndarray) -> float:
    return float(math.degrees(math.atan2(vec[1], vec[0])) % 180.0)


def run_audit() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    metrics = [
        "M1_signed_prototype",
        "M2_unsigned_prototype",
        "M3_top1_projection",
        "M3_fullspan_control",
        "M4_matrix_response",
    ]
    conditions = [
        "C1_random_unconstrained",
        "C2_orthogonal_equal_singular",
        "C3_orthogonal_unequal_singular",
        "C4_near_identical",
        "C5_separated_anisotropic",
    ]

    x_s1 = sample_s1(N_S1)
    disk_rng = np.random.default_rng(GLOBAL_SEED + 17)
    x_disk = sample_disk(N_DISK, disk_rng)

    metric_rows: List[Dict[str, float | int | str | bool]] = []
    condition_rows: List[Dict[str, float | int | str]] = []
    sign_rows: List[Dict[str, float | int | str]] = []
    calibration_rows: List[Dict[str, float | int | str | bool]] = []

    for condition in conditions:
        for seed in range(N_SEEDS):
            pair = make_pair(condition, seed)
            _, s1, v1 = svd_parts(pair.a1)
            _, s2, v2 = svd_parts(pair.a2)
            gap1 = float(abs(s1[0] - s1[1]))
            gap2 = float(abs(s2[0] - s2[1]))
            dominant_angle = abs(angle_of(v1[:, 0]) - angle_of(v2[:, 0]))
            dominant_angle = min(dominant_angle, 180.0 - dominant_angle)
            condition_rows.append(
                {
                    "condition": condition,
                    "seed": seed,
                    "s1_0": float(s1[0]),
                    "s1_1": float(s1[1]),
                    "s2_0": float(s2[0]),
                    "s2_1": float(s2[1]),
                    "gap1": gap1,
                    "gap2": gap2,
                    "dominant_direction_angle_deg": dominant_angle,
                    "matrix_distance_fro": float(np.linalg.norm(pair.a1 - pair.a2)),
                    "g_distance_fro": float(np.linalg.norm(pair.a1.T @ pair.a1 - pair.a2.T @ pair.a2)),
                }
            )

            for metric in metrics:
                q1, status1 = score_metric(metric, x_s1, pair.a1, v1, s1)
                q2, status2 = score_metric(metric, x_s1, pair.a2, v2, s2)
                status = "ok" if status1 == "ok" and status2 == "ok" else f"{status1}/{status2}"
                singular_gap_ok = gap1 > EPS_SINGULAR_GAP and gap2 > EPS_SINGULAR_GAP

                if status == "ok":
                    natural = route_stats(q1, q2)
                    threshold = float(np.median(q1 - q2))
                    calibrated = route_stats(q1, q2, threshold=threshold)
                    nat_valid, nat_reason = natural_validity(metric, status, natural, singular_gap_ok)
                    cal_valid, cal_reason = calibrated_validity(status, calibrated)
                    metric_valid = bool(nat_valid or cal_valid)
                    reason = nat_reason if nat_valid else cal_reason

                    dq1, _ = score_metric(metric, x_disk, pair.a1, v1, s1)
                    dq2, _ = score_metric(metric, x_disk, pair.a2, v2, s2)
                    disk_stats = route_stats(dq1, dq2) if dq1 is not None and dq2 is not None else {}
                else:
                    natural = {
                        "load1": np.nan,
                        "load_error": np.nan,
                        "mean_margin": np.nan,
                        "median_margin": np.nan,
                        "min_margin": np.nan,
                        "low_margin_fraction": np.nan,
                        "degeneracy_rate": np.nan,
                        "diff_std": np.nan,
                        "threshold": 0.0,
                    }
                    calibrated = dict(natural)
                    nat_valid, nat_reason = False, status
                    cal_valid, cal_reason = False, status
                    metric_valid = False
                    reason = status
                    disk_stats = {}

                sign_row = sign_sensitivity(metric, x_s1, pair, v1, s1, v2, s2)
                sign_rows.append(sign_row)
                sign_mean = sign_row.get("sign_sensitivity_mean", np.nan)
                sign_max = sign_row.get("sign_sensitivity_max", np.nan)

                metric_rows.append(
                    {
                        "condition": condition,
                        "seed": seed,
                        "metric": metric,
                        "status": status,
                        "metric_validity": metric_valid,
                        "validity_reason": reason,
                        "natural_validity": nat_valid,
                        "natural_validity_reason": nat_reason,
                        "calibrated_validity": cal_valid,
                        "calibrated_validity_reason": cal_reason,
                        "natural_load1": natural["load1"],
                        "natural_load_error": natural["load_error"],
                        "natural_mean_margin": natural["mean_margin"],
                        "natural_median_margin": natural["median_margin"],
                        "natural_min_margin": natural["min_margin"],
                        "natural_low_margin_fraction": natural["low_margin_fraction"],
                        "natural_degeneracy_rate": natural["degeneracy_rate"],
                        "natural_diff_std": natural["diff_std"],
                        "calibration_threshold": calibrated["threshold"],
                        "calibrated_load1": calibrated["load1"],
                        "calibrated_load_error": calibrated["load_error"],
                        "calibrated_mean_margin": calibrated["mean_margin"],
                        "calibrated_median_margin": calibrated["median_margin"],
                        "calibrated_low_margin_fraction": calibrated["low_margin_fraction"],
                        "disk_natural_load_error": disk_stats.get("load_error", np.nan),
                        "disk_natural_mean_margin": disk_stats.get("mean_margin", np.nan),
                        "sign_sensitivity_mean": sign_mean,
                        "sign_sensitivity_max": sign_max,
                        "gap1": gap1,
                        "gap2": gap2,
                        "dominant_direction_angle_deg": dominant_angle,
                    }
                )
                calibration_rows.append(
                    {
                        "condition": condition,
                        "seed": seed,
                        "metric": metric,
                        "status": status,
                        "threshold": calibrated["threshold"],
                        "natural_load_error": natural["load_error"],
                        "calibrated_load_error": calibrated["load_error"],
                        "natural_mean_margin": natural["mean_margin"],
                        "calibrated_mean_margin": calibrated["mean_margin"],
                        "margin_delta_cal_minus_nat": calibrated["mean_margin"] - natural["mean_margin"]
                        if status == "ok"
                        else np.nan,
                        "calibrated_validity": cal_valid,
                        "calibrated_validity_reason": cal_reason,
                    }
                )

    metric_df = pd.DataFrame(metric_rows)
    condition_df = pd.DataFrame(condition_rows)
    sign_df = pd.DataFrame(sign_rows)
    calibration_df = pd.DataFrame(calibration_rows)

    metric_df.to_csv(TABLE_DIR / "metric_summary.csv", index=False)
    condition_df.to_csv(TABLE_DIR / "condition_summary.csv", index=False)
    sign_df.to_csv(TABLE_DIR / "sign_sensitivity.csv", index=False)
    calibration_df.to_csv(TABLE_DIR / "calibration_summary.csv", index=False)

    aggregate = (
        metric_df.groupby(["condition", "metric"], dropna=False)
        .agg(
            n=("seed", "count"),
            valid_rate=("metric_validity", "mean"),
            natural_valid_rate=("natural_validity", "mean"),
            calibrated_valid_rate=("calibrated_validity", "mean"),
            natural_load_error_mean=("natural_load_error", "mean"),
            natural_load_error_median=("natural_load_error", "median"),
            natural_mean_margin_mean=("natural_mean_margin", "mean"),
            natural_degeneracy_rate_mean=("natural_degeneracy_rate", "mean"),
            calibrated_load_error_mean=("calibrated_load_error", "mean"),
            calibrated_mean_margin_mean=("calibrated_mean_margin", "mean"),
            sign_sensitivity_mean=("sign_sensitivity_mean", "mean"),
            sign_sensitivity_max=("sign_sensitivity_max", "mean"),
        )
        .reset_index()
    )
    aggregate.to_csv(TABLE_DIR / "aggregate_metric_summary.csv", index=False)

    decision_rows = []
    for metric, group in metric_df.groupby("metric", dropna=False):
        row = {
            "metric": metric,
            "overall_valid_rate": float(group["metric_validity"].mean()),
            "sign_sensitivity_mean": float(group["sign_sensitivity_mean"].mean()),
            "natural_load_error_mean": float(group["natural_load_error"].mean()),
            "natural_mean_margin_mean": float(group["natural_mean_margin"].mean()),
        }
        for condition in [
            "C1_random_unconstrained",
            "C2_orthogonal_equal_singular",
            "C3_orthogonal_unequal_singular",
            "C4_near_identical",
            "C5_separated_anisotropic",
        ]:
            sub = group[group["condition"] == condition]
            short = condition.split("_", 1)[0].lower()
            row[f"{short}_valid_rate"] = float(sub["metric_validity"].mean())
            row[f"{short}_natural_degeneracy_rate"] = float(sub["natural_degeneracy_rate"].mean())
            row[f"{short}_natural_load_error"] = float(sub["natural_load_error"].mean())
            row[f"{short}_natural_mean_margin"] = float(sub["natural_mean_margin"].mean())
        decision_rows.append(row)
    decision = pd.DataFrame(decision_rows)
    decision.to_csv(TABLE_DIR / "metric_decision_summary.csv", index=False)

    make_figures(metrics, conditions)


def make_figures(metrics: Iterable[str], conditions: Iterable[str]) -> None:
    central = [
        ("C2_orthogonal_equal_singular", 0),
        ("C3_orthogonal_unequal_singular", 0),
        ("C4_near_identical", 0),
        ("C5_separated_anisotropic", 0),
    ]
    grid_lin = np.linspace(-1.1, 1.1, 250)
    gx, gy = np.meshgrid(grid_lin, grid_lin)
    grid = np.stack([gx.ravel(), gy.ravel()], axis=1)
    mask = np.linalg.norm(grid, axis=1) <= 1.0
    grid_unit = grid[mask]

    for condition, seed in central:
        pair = make_pair(condition, seed)
        _, s1, v1 = svd_parts(pair.a1)
        _, s2, v2 = svd_parts(pair.a2)
        for metric in metrics:
            q1, st1 = score_metric(metric, grid_unit, pair.a1, v1, s1)
            q2, st2 = score_metric(metric, grid_unit, pair.a2, v2, s2)
            fig, ax = plt.subplots(figsize=(5.0, 5.0))
            ax.set_aspect("equal")
            ax.set_xlim(-1.1, 1.1)
            ax.set_ylim(-1.1, 1.1)
            ax.set_title(f"{metric}\n{condition}")
            ax.set_xlabel("x1")
            ax.set_ylabel("x2")
            circle = plt.Circle((0, 0), 1.0, edgecolor="black", facecolor="none", linewidth=1.0)
            ax.add_patch(circle)
            if st1 == "ok" and st2 == "ok":
                assign = q1 >= q2
                diff = q1 - q2
                if float(np.std(diff)) <= EPS_DEGENERATE or float((np.abs(diff) < EPS_DEGENERATE).mean()) >= 0.95:
                    ax.text(0.0, 0.0, "degenerate scores", ha="center", va="center")
                else:
                    colors = np.where(assign, "#2d6cdf", "#f28e2b")
                    ax.scatter(grid_unit[:, 0], grid_unit[:, 1], c=colors, s=2, alpha=0.55, linewidths=0)
                    low = np.abs(diff) < np.percentile(np.abs(diff), 3.0)
                    ax.scatter(grid_unit[low, 0], grid_unit[low, 1], c="black", s=2, alpha=0.35, linewidths=0)
            else:
                ax.text(0.0, 0.0, f"invalid:\n{st1}/{st2}", ha="center", va="center")
            fig.tight_layout()
            out = FIGURE_DIR / f"partition_{metric}_{condition}.png"
            fig.savefig(out, dpi=160)
            plt.close(fig)


if __name__ == "__main__":
    run_audit()

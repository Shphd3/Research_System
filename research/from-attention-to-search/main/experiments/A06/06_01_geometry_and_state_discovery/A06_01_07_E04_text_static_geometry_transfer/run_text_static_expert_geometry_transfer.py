#!/usr/bin/env python3
"""A07_E02 semi-real text-facing static expert-geometry transfer audit.

This run uses controlled text-like hidden-state distributions rather than a
frozen transformer. The construction includes corpus-slice, position, token
frequency, and common-direction factors so the static metrics can be tested
against non-uniform, non-isotropic hidden states.
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
D = 128
N_CALIB = 12_000
N_EVAL = 24_000
LAYERS = ["early", "middle", "late"]
POSITIONS = ["controlled", "natural"]
RANKS = [1, 2, 4, 8, 16, 32, 64]
LOW_MARGIN_EPS = 1e-4


@dataclass(frozen=True)
class DatasetSplit:
    h: np.ndarray
    corpus: np.ndarray
    position: np.ndarray
    frequency: np.ndarray
    syntax: np.ndarray
    utility_label: np.ndarray


def rng_for(*parts: int) -> np.random.Generator:
    seed = GLOBAL_SEED
    for part in parts:
        seed = (seed * 6364136223846793005 + int(part) + 1442695040888963407) % (2**63 - 1)
    return np.random.default_rng(seed)


def normalize(v: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(v))
    return v / max(n, 1e-12)


def make_basis(rng: np.random.Generator, n: int, d: int) -> np.ndarray:
    q, _ = np.linalg.qr(rng.normal(size=(d, n)))
    return q.T


def make_expert_spectra(rng: np.random.Generator, d: int) -> Tuple[np.ndarray, np.ndarray]:
    # Positive spectra with several strong directions and a long tail.
    base = np.linspace(2.8, 0.25, d)
    g1 = base.copy()
    g2 = base.copy()
    g1[:10] += np.linspace(2.0, 0.8, 10)
    g2[10:20] += np.linspace(2.0, 0.8, 10)
    g1 += 0.05 * rng.lognormal(mean=0.0, sigma=0.4, size=d)
    g2 += 0.05 * rng.lognormal(mean=0.0, sigma=0.4, size=d)
    return g1, g2


def make_geometry() -> Dict[str, np.ndarray]:
    rng = rng_for(1)
    basis = make_basis(rng, D, D)
    g1, g2 = make_expert_spectra(rng, D)
    # Keep G diagonal in the shared basis; hidden states are generated in the
    # same coordinates so top-r score behavior is auditable.
    return {
        "basis": basis,
        "g1": g1,
        "g2": g2,
        "common": normalize(basis[0] + 0.35 * basis[1]),
        "utility_axis": normalize(np.mean(basis[:10], axis=0) - np.mean(basis[10:20], axis=0)),
        "slice_axes": basis[20:23],
        "position_axes": basis[23:25],
        "freq_axis": basis[25],
        "syntax_axes": basis[26:30],
    }


def generate_split(
    n: int,
    layer: str,
    position_mode: str,
    geom: Dict[str, np.ndarray],
    rng: np.random.Generator,
) -> DatasetSplit:
    d = geom["basis"].shape[1]
    corpus = rng.integers(0, 3, size=n)
    position = rng.integers(0, 2, size=n) if position_mode == "natural" else np.zeros(n, dtype=int)
    frequency = rng.choice(3, size=n, p=[0.55, 0.30, 0.15])
    syntax = rng.integers(0, 4, size=n)
    utility_label = rng.integers(0, 2, size=n)

    layer_common = {"early": 2.4, "middle": 1.6, "late": 0.9}[layer]
    layer_utility = {"early": 0.35, "middle": 0.65, "late": 0.9}[layer]
    pos_strength = 0.9 if position_mode == "natural" else 0.25

    h = rng.normal(scale=0.65, size=(n, d))
    h += layer_common * rng.normal(size=(n, 1)) * geom["common"]
    h += layer_utility * (2 * utility_label[:, None] - 1) * geom["utility_axis"]
    h += 0.55 * geom["slice_axes"][corpus]
    h += pos_strength * geom["position_axes"][position]
    h += (frequency[:, None] - 1.0) * 0.6 * geom["freq_axis"]
    h += 0.35 * geom["syntax_axes"][syntax]
    return DatasetSplit(h=h, corpus=corpus, position=position, frequency=frequency, syntax=syntax, utility_label=utility_label)


def fit_preprocess(calib: np.ndarray) -> Dict[str, np.ndarray]:
    mean = calib.mean(axis=0)
    centered = calib - mean
    _, _, vt = np.linalg.svd(centered, full_matrices=False)
    common = vt[0]
    std = centered.std(axis=0) + 1e-6
    return {"mean": mean, "common": common, "std": std}


def apply_preprocess(h: np.ndarray, fit: Dict[str, np.ndarray], variant: str) -> np.ndarray:
    if variant == "raw":
        return h
    centered = h - fit["mean"]
    if variant == "mean_centered":
        return centered
    if variant == "common_removed":
        c = fit["common"]
        return centered - (centered @ c)[:, None] * c
    if variant == "whitened_diag":
        return centered / fit["std"]
    raise ValueError(variant)


def full_scores(x: np.ndarray, g1: np.ndarray, g2: np.ndarray, center: Tuple[float, float]) -> np.ndarray:
    return (x * x) @ (g1 - g2) - (center[0] - center[1])


def top_r_scores(x: np.ndarray, g1: np.ndarray, g2: np.ndarray, r: int, weighted: bool, center: Tuple[float, float]) -> np.ndarray:
    diff = np.zeros_like(g1)
    if weighted:
        diff[:r] = g1[:r] - g2[:r]
    else:
        diff[:r] = 0.0
        diff[:r] = (g1[:r] > 0).astype(float) - (g2[:r] > 0).astype(float)
    return (x * x) @ diff - (center[0] - center[1])


def prototype_scores(x: np.ndarray, g1: np.ndarray, g2: np.ndarray, unsigned: bool) -> np.ndarray:
    m1 = normalize(np.sqrt(g1) * np.sign(np.arange(len(g1)) + 1))
    m2 = normalize(np.sqrt(g2) * np.sign(np.arange(len(g2)) + 2))
    s1 = x @ m1
    s2 = x @ m2
    if unsigned:
        return s1 * s1 - s2 * s2
    return s1 - s2


def evaluate_scores(scores: np.ndarray, threshold: float, utility: np.ndarray, full_labels: np.ndarray) -> Dict[str, float]:
    shifted = scores - threshold
    labels = shifted > 0
    margin = np.abs(shifted)
    util_match = np.mean(labels == utility.astype(bool))
    return {
        "load1": float(np.mean(labels)),
        "load_error": abs(float(np.mean(labels)) - 0.5),
        "mean_margin": float(np.mean(margin)),
        "low_margin_fraction": float(np.mean(margin < LOW_MARGIN_EPS)),
        "agreement_with_full_centered_M4": float(np.mean(labels == full_labels)),
        "utility_match": float(util_match),
        "threshold": float(threshold),
    }


def nmi_discrete(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a)
    b = np.asarray(b)
    total = len(a)
    if total == 0:
        return 0.0
    av, ai = np.unique(a, return_inverse=True)
    bv, bi = np.unique(b, return_inverse=True)
    joint = np.zeros((len(av), len(bv)))
    for i, j in zip(ai, bi):
        joint[i, j] += 1
    joint /= total
    pa = joint.sum(axis=1, keepdims=True)
    pb = joint.sum(axis=0, keepdims=True)
    nz = joint > 0
    mi = float(np.sum(joint[nz] * np.log(joint[nz] / (pa @ pb)[nz])))
    ha = -float(np.sum(pa[pa > 0] * np.log(pa[pa > 0])))
    hb = -float(np.sum(pb[pb > 0] * np.log(pb[pb > 0])))
    return 0.0 if ha + hb == 0 else 2 * mi / (ha + hb)


def run_condition(layer: str, position_mode: str, geom: Dict[str, np.ndarray]) -> Tuple[List[Dict[str, float | str | int]], List[Dict[str, float | str | int]], List[Dict[str, float | str | int]]]:
    rng = rng_for(7, LAYERS.index(layer), POSITIONS.index(position_mode))
    calib = generate_split(N_CALIB, layer, position_mode, geom, rng)
    eval_split = generate_split(N_EVAL, layer, position_mode, geom, rng)
    fit = fit_preprocess(calib.h)

    rows: List[Dict[str, float | str | int]] = []
    breakdown: List[Dict[str, float | str | int]] = []
    sensitivity: List[Dict[str, float | str | int]] = []

    g1, g2 = geom["g1"], geom["g2"]
    preprocess_variants = ["raw", "mean_centered", "common_removed", "whitened_diag"]

    full_centered_labels_by_variant: Dict[str, np.ndarray] = {}
    score_cache: Dict[Tuple[str, str, int], np.ndarray] = {}

    for variant in preprocess_variants:
        x_cal = apply_preprocess(calib.h, fit, variant)
        x_eval = apply_preprocess(eval_split.h, fit, variant)
        raw_cal_1 = (x_cal * x_cal) @ g1
        raw_cal_2 = (x_cal * x_cal) @ g2
        empirical_center = (float(np.mean(raw_cal_1)), float(np.mean(raw_cal_2)))

        full_eval = full_scores(x_eval, g1, g2, empirical_center)
        full_cal = full_scores(x_cal, g1, g2, empirical_center)
        full_threshold = 0.0
        full_labels = full_eval > full_threshold
        full_centered_labels_by_variant[variant] = full_labels

        methods: List[Tuple[str, np.ndarray, np.ndarray, int]] = [
            ("full_empirical_centered_m4", full_eval, full_cal, 0),
            ("quantile_calibrated_m4", full_scores(x_eval, g1, g2, (0.0, 0.0)), full_scores(x_cal, g1, g2, (0.0, 0.0)), 0),
            ("M1_signed_prototype", prototype_scores(x_eval, g1, g2, unsigned=False), prototype_scores(x_cal, g1, g2, unsigned=False), 0),
            ("M2_unsigned_prototype", prototype_scores(x_eval, g1, g2, unsigned=True), prototype_scores(x_cal, g1, g2, unsigned=True), 0),
        ]
        for r in RANKS:
            center_r = (float(np.mean((x_cal * x_cal) @ np.r_[g1[:r], np.zeros(D - r)])), float(np.mean((x_cal * x_cal) @ np.r_[g2[:r], np.zeros(D - r)])))
            methods.append((f"weighted_top_r_{r}", top_r_scores(x_eval, g1, g2, r, True, center_r), top_r_scores(x_cal, g1, g2, r, True, center_r), r))

        for method, eval_scores, cal_scores, rank in methods:
            threshold = float(np.median(cal_scores)) if method == "quantile_calibrated_m4" else 0.0
            metrics = evaluate_scores(eval_scores, threshold, eval_split.utility_label, full_labels)
            labels = (eval_scores - threshold) > 0
            row = {
                "layer": layer,
                "position_mode": position_mode,
                "preprocess": variant,
                "method": method,
                "rank": rank,
                **metrics,
                "corpus_nmi": nmi_discrete(labels.astype(int), eval_split.corpus),
                "position_nmi": nmi_discrete(labels.astype(int), eval_split.position),
                "frequency_nmi": nmi_discrete(labels.astype(int), eval_split.frequency),
                "syntax_nmi": nmi_discrete(labels.astype(int), eval_split.syntax),
            }
            rows.append(row)
            score_cache[(variant, method, rank)] = labels.astype(int)

            for pos in np.unique(eval_split.position):
                mask = eval_split.position == pos
                breakdown.append(
                    {
                        "layer": layer,
                        "position_mode": position_mode,
                        "preprocess": variant,
                        "method": method,
                        "rank": rank,
                        "slice": f"position_{pos}",
                        "n": int(mask.sum()),
                        "load_error": abs(float(labels[mask].mean()) - 0.5),
                        "mean_margin": float(np.mean(np.abs(eval_scores[mask] - threshold))),
                    }
                )

    for method in ["full_empirical_centered_m4", "quantile_calibrated_m4", "weighted_top_r_16", "weighted_top_r_32", "M2_unsigned_prototype"]:
        for base_variant in ["mean_centered", "raw"]:
            key_a = (base_variant, method, 16 if method.endswith("_16") else 32 if method.endswith("_32") else 0)
            key_b = ("common_removed", method, 16 if method.endswith("_16") else 32 if method.endswith("_32") else 0)
            if key_a in score_cache and key_b in score_cache:
                sensitivity.append(
                    {
                        "layer": layer,
                        "position_mode": position_mode,
                        "method": method,
                        "base_preprocess": base_variant,
                        "route_change_after_common_removal": float(np.mean(score_cache[key_a] != score_cache[key_b])),
                    }
                )

    return rows, breakdown, sensitivity


def make_figures(summary: pd.DataFrame, rank_df: pd.DataFrame, sensitivity: pd.DataFrame) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    plot = summary[(summary["preprocess"].isin(["raw", "mean_centered", "common_removed"])) & (summary["method"].isin(["full_empirical_centered_m4", "quantile_calibrated_m4", "weighted_top_r_16", "weighted_top_r_32", "M2_unsigned_prototype"]))]
    labels = []
    x = np.arange(len(plot))
    ax.scatter(plot["load_error"], plot["mean_margin"], alpha=0.7)
    for _, row in plot.iterrows():
        labels.append(f"{row['method']} / {row['preprocess']}")
    ax.set_xlabel("load error")
    ax.set_ylabel("mean margin")
    ax.set_title("Load-margin tradeoff by method and preprocessing")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "load_margin_by_method.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 6))
    rank_plot = (
        rank_df.groupby(["preprocess", "layer", "rank"], dropna=False)["agreement_with_full_centered_M4"]
        .mean()
        .reset_index()
    )
    for (preprocess, layer), sub in rank_plot.groupby(["preprocess", "layer"]):
        if preprocess not in ["mean_centered", "common_removed"] or layer != "middle":
            continue
        ax.plot(sub["rank"], sub["agreement_with_full_centered_M4"], marker="o", label=f"{preprocess} / {layer}")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("rank r")
    ax.set_ylabel("agreement with full centered M4")
    ax.set_title("Agreement versus weighted top-r rank")
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "agreement_vs_rank.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 6))
    sens_plot = sensitivity.groupby("method", as_index=False)["route_change_after_common_removal"].mean()
    ax.bar(sens_plot["method"], sens_plot["route_change_after_common_removal"])
    ax.set_ylabel("route change after common removal")
    ax.set_title("Common-direction sensitivity")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "common_control_effect.png", dpi=180)
    plt.close(fig)


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    geom = make_geometry()

    rows: List[Dict[str, float | str | int]] = []
    breakdown: List[Dict[str, float | str | int]] = []
    sensitivity: List[Dict[str, float | str | int]] = []
    for layer in LAYERS:
        for position_mode in POSITIONS:
            r, b, s = run_condition(layer, position_mode, geom)
            rows.extend(r)
            breakdown.extend(b)
            sensitivity.extend(s)

    df = pd.DataFrame(rows)
    breakdown_df = pd.DataFrame(breakdown)
    sensitivity_df = pd.DataFrame(sensitivity)
    summary = (
        df.groupby(["method", "preprocess", "rank"], dropna=False)
        .agg(
            n=("load_error", "size"),
            load_error=("load_error", "mean"),
            mean_margin=("mean_margin", "mean"),
            low_margin_fraction=("low_margin_fraction", "mean"),
            agreement_with_full_centered_M4=("agreement_with_full_centered_M4", "mean"),
            utility_match=("utility_match", "mean"),
            corpus_nmi=("corpus_nmi", "mean"),
            position_nmi=("position_nmi", "mean"),
            frequency_nmi=("frequency_nmi", "mean"),
            syntax_nmi=("syntax_nmi", "mean"),
        )
        .reset_index()
    )
    utility = (
        df.groupby(["method", "preprocess", "rank"], dropna=False)
        .agg(
            utility_match=("utility_match", "mean"),
            agreement_with_full_centered_M4=("agreement_with_full_centered_M4", "mean"),
            load_error=("load_error", "mean"),
            mean_margin=("mean_margin", "mean"),
        )
        .reset_index()
    )
    rank_df = df[df["method"].str.startswith("weighted_top_r_")].copy()
    rank_df["rank"] = rank_df["rank"].astype(int)

    df.to_csv(TABLE_DIR / "text_static_metric_per_condition.csv", index=False)
    summary.to_csv(TABLE_DIR / "text_static_metric_summary.csv", index=False)
    breakdown_df.to_csv(TABLE_DIR / "layer_position_breakdown.csv", index=False)
    sensitivity_df.to_csv(TABLE_DIR / "common_sensitivity.csv", index=False)
    utility.to_csv(TABLE_DIR / "utility_match.csv", index=False)
    make_figures(summary, rank_df, sensitivity_df)
    print(f"wrote {TABLE_DIR}")
    print(f"wrote {FIGURE_DIR}")


if __name__ == "__main__":
    main()

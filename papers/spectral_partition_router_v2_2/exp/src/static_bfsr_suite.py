"""Experiment utilities for V2.2 static feature-level specialization.

The suite is deliberately small and auditable.  Valid routers fit only on
calibration features.  Synthetic feature labels are used for the invalid oracle
upper bound and for evaluation metrics, not by the primary BFSR-Cluster method.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, mutual_info_score, normalized_mutual_info_score


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
LATEX = ROOT.parent / "latex"
TABLES = LATEX / "tables"
FIGURES = LATEX / "figures"


METHOD_LABELS = {
    "oracle_equal": "OracleFeature",
    "oracle_mass": "OracleFeature-mass",
    "bfsr_cluster_equal": "BFSR-Cluster",
    "bfsr_cluster_mass": "BFSR-Cluster-mass",
    "quantile_spr": "Quantile-SPR",
    "random_linear": "Random linear",
}


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def unit_rows(x: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    return x / (np.linalg.norm(x, axis=1, keepdims=True) + eps)


def exact_labels(n: int, k: int, r: np.random.Generator, probs: np.ndarray | None = None) -> np.ndarray:
    if probs is None:
        labels = np.arange(n) % k
        r.shuffle(labels)
        return labels.astype(int)
    return r.choice(k, size=n, p=probs).astype(int)


def paired_axis_centers(k: int, d: int, separation: float, seed: int) -> np.ndarray:
    """Construct balanced centers whose empirical second moment is isotropic.

    The clean default uses K=2d paired directions.  For K<2d we use the first
    K/2 pairs, which remains centered but is lower-rank before adding isotropic
    noise.  The experiment diagnostics report the resulting covariance.
    """
    if k % 2 != 0:
        raise ValueError("paired_axis_centers requires an even number of feature families")
    if k > 2 * d:
        raise ValueError("paired_axis_centers requires k <= 2d")
    r = rng(seed)
    q, _ = np.linalg.qr(r.normal(size=(d, d)))
    centers = []
    for axis in range(k // 2):
        centers.append(separation * q[:, axis])
        centers.append(-separation * q[:, axis])
    return np.stack(centers, axis=0)


@dataclass
class Dataset:
    name: str
    x_cal: np.ndarray
    f_cal: np.ndarray
    x_hold: np.ndarray
    f_hold: np.ndarray
    centers: np.ndarray | None = None
    probs: np.ndarray | None = None


def make_isotropic_null(n_cal: int, n_hold: int, d: int, k: int, seed: int) -> Dataset:
    r = rng(seed)
    x_cal = r.normal(size=(n_cal, d))
    x_hold = r.normal(size=(n_hold, d))
    return Dataset(
        name="isotropic_null",
        x_cal=x_cal,
        f_cal=exact_labels(n_cal, k, r),
        x_hold=x_hold,
        f_hold=exact_labels(n_hold, k, r),
    )


def make_feature_mixture(
    n_cal: int,
    n_hold: int,
    d: int,
    k: int,
    separation: float,
    noise: float,
    seed: int,
    probs: np.ndarray | None = None,
) -> Dataset:
    r = rng(seed)
    centers = paired_axis_centers(k, d, separation, seed + 1009)
    f_cal = exact_labels(n_cal, k, r, probs)
    f_hold = exact_labels(n_hold, k, r, probs)
    x_cal = centers[f_cal] + noise * r.normal(size=(n_cal, d))
    x_hold = centers[f_hold] + noise * r.normal(size=(n_hold, d))
    return Dataset(
        name="feature_mixture",
        x_cal=x_cal,
        f_cal=f_cal,
        x_hold=x_hold,
        f_hold=f_hold,
        centers=centers,
        probs=probs,
    )


def apply_anisotropic_distortion(x: np.ndarray, condition_number: float, seed: int) -> np.ndarray:
    r = rng(seed)
    d = x.shape[1]
    q, _ = np.linalg.qr(r.normal(size=(d, d)))
    scales = np.geomspace(condition_number, 1.0, d)
    return x @ (q @ np.diag(scales) @ q.T)


def distorted_dataset(base: Dataset, condition_number: float, seed: int, name: str) -> Dataset:
    return Dataset(
        name=name,
        x_cal=apply_anisotropic_distortion(base.x_cal, condition_number, seed),
        f_cal=base.f_cal.copy(),
        x_hold=apply_anisotropic_distortion(base.x_hold, condition_number, seed),
        f_hold=base.f_hold.copy(),
        centers=None if base.centers is None else apply_anisotropic_distortion(base.centers, condition_number, seed),
        probs=base.probs,
    )


def imbalanced_probs(k: int, strength: float = 1.4) -> np.ndarray:
    weights = strength ** np.arange(k)
    weights = weights / weights.sum()
    # Shuffle deterministically so imbalance is not aligned with paired axes.
    r = rng(424242 + k)
    perm = r.permutation(k)
    probs = np.empty(k)
    probs[perm] = weights
    return probs


@dataclass
class Normalizer:
    mean: np.ndarray
    matrix: np.ndarray

    def apply(self, x: np.ndarray) -> np.ndarray:
        return (x - self.mean) @ self.matrix


def fit_normalizer(x: np.ndarray, mode: str, ridge: float = 1e-5) -> Normalizer:
    mean = x.mean(axis=0)
    d = x.shape[1]
    if mode == "raw":
        return Normalizer(mean=np.zeros(d), matrix=np.eye(d))
    if mode == "center":
        return Normalizer(mean=mean, matrix=np.eye(d))
    if mode != "whiten":
        raise ValueError(f"unknown normalizer mode: {mode}")
    xc = x - mean
    cov = np.cov(xc, rowvar=False)
    vals, vecs = np.linalg.eigh(cov)
    vals = np.maximum(vals, ridge)
    matrix = vecs @ np.diag(1.0 / np.sqrt(vals)) @ vecs.T
    return Normalizer(mean=mean, matrix=matrix)


def covariance_diagnostics(x: np.ndarray) -> dict[str, float]:
    cov = np.cov(x - x.mean(axis=0), rowvar=False)
    vals = np.linalg.eigvalsh(cov)
    vals = np.maximum(vals, 1e-12)
    scaled = vals / vals.mean()
    return {
        "cov_cond": float(vals.max() / vals.min()),
        "cov_effective_rank": float(vals.sum() ** 2 / np.square(vals).sum()),
        "cov_op_norm_scaled_minus_i": float(np.max(np.abs(scaled - 1.0))),
    }


def cluster_accuracy_up_to_permutation(true: np.ndarray, pred: np.ndarray) -> float:
    true_vals = np.unique(true)
    pred_vals = np.unique(pred)
    mat = np.zeros((len(true_vals), len(pred_vals)), dtype=int)
    true_index = {v: i for i, v in enumerate(true_vals)}
    pred_index = {v: i for i, v in enumerate(pred_vals)}
    for t, p in zip(true, pred, strict=True):
        mat[true_index[t], pred_index[p]] += 1
    row, col = linear_sum_assignment(-mat)
    return float(mat[row, col].sum() / len(true))


def assign_equal_number(k: int, e: int, masses: np.ndarray | None = None) -> np.ndarray:
    if k % e != 0:
        raise ValueError("equal-number assignment requires K divisible by E")
    assignment = np.empty(k, dtype=int)
    order = np.arange(k)
    if masses is not None:
        # Stable order makes high/low mass families distributed across experts.
        order = np.argsort(-masses, kind="mergesort")
    for pos, cluster in enumerate(order):
        assignment[cluster] = pos % e
    return assignment


def assign_mass_aware(masses: np.ndarray, e: int) -> np.ndarray:
    order = np.argsort(-masses, kind="mergesort")
    expert_mass = np.zeros(e)
    assignment = np.empty(len(masses), dtype=int)
    for cluster in order:
        expert = int(np.argmin(expert_mass))
        assignment[cluster] = expert
        expert_mass[expert] += masses[cluster]
    return assignment


class BFSRClusterRouter:
    def __init__(self, k: int, e: int, normalizer_mode: str = "whiten", assignment: str = "equal", seed: int = 0):
        self.k = k
        self.e = e
        self.normalizer_mode = normalizer_mode
        self.assignment = assignment
        self.seed = seed
        self.normalizer: Normalizer | None = None
        self.kmeans: KMeans | None = None
        self.cluster_to_expert: np.ndarray | None = None

    def fit(self, x_cal: np.ndarray) -> "BFSRClusterRouter":
        self.normalizer = fit_normalizer(x_cal, self.normalizer_mode)
        z = self.normalizer.apply(x_cal)
        self.kmeans = KMeans(n_clusters=self.k, n_init=8, max_iter=200, random_state=self.seed)
        clusters = self.kmeans.fit_predict(z)
        masses = np.bincount(clusters, minlength=self.k).astype(float)
        masses = masses / masses.sum()
        if self.assignment == "mass":
            self.cluster_to_expert = assign_mass_aware(masses, self.e)
        else:
            self.cluster_to_expert = assign_equal_number(self.k, self.e, masses=None)
        return self

    def predict_clusters(self, x: np.ndarray) -> np.ndarray:
        if self.normalizer is None or self.kmeans is None:
            raise RuntimeError("router is not fitted")
        return self.kmeans.predict(self.normalizer.apply(x))

    def predict(self, x: np.ndarray) -> np.ndarray:
        if self.cluster_to_expert is None:
            raise RuntimeError("router is not fitted")
        return self.cluster_to_expert[self.predict_clusters(x)]


class OracleFeatureRouter:
    def __init__(self, k: int, e: int, assignment: str = "equal"):
        self.k = k
        self.e = e
        self.assignment = assignment
        self.family_to_expert: np.ndarray | None = None

    def fit(self, f_cal: np.ndarray) -> "OracleFeatureRouter":
        masses = np.bincount(f_cal, minlength=self.k).astype(float)
        masses = masses / masses.sum()
        if self.assignment == "mass":
            self.family_to_expert = assign_mass_aware(masses, self.e)
        else:
            self.family_to_expert = assign_equal_number(self.k, self.e, masses=None)
        return self

    def predict_from_labels(self, f: np.ndarray) -> np.ndarray:
        if self.family_to_expert is None:
            raise RuntimeError("router is not fitted")
        return self.family_to_expert[f]


class RandomLinearRouter:
    def __init__(self, e: int, d: int, normalizer_mode: str = "whiten", seed: int = 0):
        self.e = e
        self.d = d
        self.normalizer_mode = normalizer_mode
        self.seed = seed
        self.normalizer: Normalizer | None = None
        self.rows = unit_rows(rng(seed).normal(size=(e, d)))

    def fit(self, x_cal: np.ndarray) -> "RandomLinearRouter":
        self.normalizer = fit_normalizer(x_cal, self.normalizer_mode)
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        if self.normalizer is None:
            raise RuntimeError("router is not fitted")
        z = self.normalizer.apply(x)
        return np.argmax(z @ self.rows.T, axis=1)


@dataclass
class TreeNode:
    experts: tuple[int, ...]
    direction: np.ndarray | None = None
    threshold: float | None = None
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


class QuantileSPRRouter:
    """Mass-only baseline: recursive random projections and quantile splits."""

    def __init__(self, e: int, normalizer_mode: str = "whiten", seed: int = 0):
        self.e = e
        self.normalizer_mode = normalizer_mode
        self.seed = seed
        self.r = rng(seed)
        self.normalizer: Normalizer | None = None
        self.root: TreeNode | None = None

    def fit(self, x_cal: np.ndarray) -> "QuantileSPRRouter":
        self.normalizer = fit_normalizer(x_cal, self.normalizer_mode)
        z = self.normalizer.apply(x_cal)
        self.root = self._fit_node(z, np.arange(len(z)), tuple(range(self.e)))
        return self

    def _fit_node(self, z: np.ndarray, idx: np.ndarray, experts: tuple[int, ...]) -> TreeNode:
        node = TreeNode(experts=experts)
        if len(experts) == 1:
            return node
        left_n = len(experts) // 2
        direction = unit_rows(self.r.normal(size=(1, z.shape[1])))[0]
        proj = z[idx] @ direction
        rho = left_n / len(experts)
        threshold = float(np.quantile(proj, rho, method="linear"))
        mask = proj <= threshold
        if mask.all() or (~mask).all():
            order = np.argsort(proj, kind="mergesort")
            mask = np.zeros_like(proj, dtype=bool)
            mask[order[: max(1, int(round(rho * len(order))))]] = True
        node.direction = direction
        node.threshold = threshold
        node.left = self._fit_node(z, idx[mask], tuple(experts[:left_n]))
        node.right = self._fit_node(z, idx[~mask], tuple(experts[left_n:]))
        return node

    def predict(self, x: np.ndarray) -> np.ndarray:
        if self.normalizer is None or self.root is None:
            raise RuntimeError("router is not fitted")
        z = self.normalizer.apply(x)
        routes = np.empty(len(z), dtype=int)
        self._predict_node(z, np.arange(len(z)), self.root, routes)
        return routes

    def _predict_node(self, z: np.ndarray, idx: np.ndarray, node: TreeNode, routes: np.ndarray) -> None:
        if len(idx) == 0:
            return
        if len(node.experts) == 1:
            routes[idx] = node.experts[0]
            return
        assert node.direction is not None and node.threshold is not None
        mask = z[idx] @ node.direction <= node.threshold
        assert node.left is not None and node.right is not None
        self._predict_node(z, idx[mask], node.left, routes)
        self._predict_node(z, idx[~mask], node.right, routes)


def entropy_from_counts(counts: np.ndarray) -> float:
    p = counts.astype(float)
    p = p[p > 0] / p.sum()
    return float(-np.sum(p * np.log(p)))


def usage_metrics(routes: np.ndarray, e: int) -> dict[str, float]:
    counts = np.bincount(routes, minlength=e).astype(float)
    usage = counts / counts.sum()
    target = 1.0 / e
    return {
        "loadcv": float(usage.std(ddof=0) / usage.mean()),
        "max_mass_error": float(np.max(np.abs(usage - target))),
        "usage_entropy": entropy_from_counts(counts),
        "min_usage": float(usage.min()),
        "max_usage": float(usage.max()),
    }


def contingency(labels: np.ndarray, routes: np.ndarray, k: int, e: int) -> np.ndarray:
    mat = np.zeros((k, e), dtype=int)
    for f, g in zip(labels, routes, strict=True):
        mat[int(f), int(g)] += 1
    return mat


def specialization_metrics(routes: np.ndarray, labels: np.ndarray, k: int, e: int) -> dict[str, float]:
    mat = contingency(labels, routes, k, e)
    row_sums = mat.sum(axis=1)
    nonempty = row_sums > 0
    row_probs = np.divide(mat[nonempty], row_sums[nonempty, None], where=row_sums[nonempty, None] > 0)
    family_consistency = float(np.mean(row_probs.max(axis=1)))
    split_rate = float(np.mean((row_probs > 0.05).sum(axis=1) > 1))
    mi = float(mutual_info_score(labels, routes))
    h_g = entropy_from_counts(np.bincount(routes, minlength=e))
    return {
        "family_consistency": family_consistency,
        "feature_split_rate": split_rate,
        "expert_info_fraction": float(mi / h_g) if h_g > 1e-12 else 0.0,
        "nmi": float(normalized_mutual_info_score(labels, routes)),
    }


def evaluate_routes(
    exp_id: str,
    dataset: str,
    method: str,
    seed: int,
    routes: np.ndarray,
    labels: np.ndarray,
    k: int,
    e: int,
    extra: dict[str, float] | None = None,
) -> dict[str, float | str | int]:
    row: dict[str, float | str | int] = {
        "exp_id": exp_id,
        "dataset": dataset,
        "method": method,
        "method_label": METHOD_LABELS.get(method, method),
        "seed": seed,
    }
    row.update(usage_metrics(routes, e))
    row.update(specialization_metrics(routes, labels, k, e))
    if extra:
        row.update(extra)
    return row


def evaluate_cluster_recovery(router: BFSRClusterRouter, x: np.ndarray, labels: np.ndarray) -> dict[str, float]:
    clusters = router.predict_clusters(x)
    return {
        "cluster_acc": cluster_accuracy_up_to_permutation(labels, clusters),
        "cluster_ari": float(adjusted_rand_score(labels, clusters)),
    }


def aggregate(rows: list[dict[str, object]], group_cols: list[str]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    num_cols = [
        col
        for col in df.columns
        if col not in set(group_cols + ["method_label"]) and pd.api.types.is_numeric_dtype(df[col])
    ]
    agg = df.groupby(group_cols)[num_cols].agg(["mean", "std"]).reset_index()
    agg.columns = ["_".join([c for c in col if c]) for col in agg.columns.to_flat_index()]
    return agg.reset_index(drop=True)


def save_csv(df: pd.DataFrame, name: str) -> Path:
    path = RESULTS / f"{name}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def format_float(x: float | int | str, ndigits: int = 3) -> str:
    if isinstance(x, str):
        return x
    if pd.isna(x):
        return "--"
    return f"{float(x):.{ndigits}f}"


def write_latex_table(path: Path, caption: str, label: str, columns: list[str], rows: Iterable[Iterable[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    align = "l" * 2 + "r" * max(0, len(columns) - 2)
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        f"\\begin{{tabular}}{{{align}}}",
        "\\toprule",
        " & ".join(columns) + r" \\",
        "\\midrule",
    ]
    for row in rows:
        lines.append(" & ".join(str(x) for x in row) + r" \\")
    lines += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def plot_e3(df: pd.DataFrame) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig, ax1 = plt.subplots(figsize=(5.2, 3.2))
    ax2 = ax1.twinx()
    x = df["separation"].to_numpy()
    ax1.plot(x, df["cluster_acc_mean"], marker="o", color="#2b6cb0", label="Cluster accuracy")
    ax2.plot(x, df["family_consistency_mean"], marker="s", color="#c05621", label="Family consistency")
    ax1.set_xlabel("Feature-family separation")
    ax1.set_ylabel("Cluster accuracy")
    ax2.set_ylabel("Family consistency")
    ax1.set_ylim(0, 1.05)
    ax2.set_ylim(0, 1.05)
    ax1.grid(True, alpha=0.25)
    lines = ax1.get_lines() + ax2.get_lines()
    ax1.legend(lines, [line.get_label() for line in lines], loc="lower right", frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "e3_recoverability_sweep.png", dpi=220)
    plt.close(fig)


def plot_e4(df: pd.DataFrame) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    subset = df[df["method"] == "bfsr_cluster_equal"].copy()
    display = {
        "null_distorted": "Null",
        "structured_distorted": "Structured",
    }
    labels = [f"{display.get(row.dataset, row.dataset)}\n{row.normalizer}" for row in subset.itertuples()]
    vals = subset["expert_info_fraction_mean"].to_numpy()
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    ax.bar(np.arange(len(vals)), vals, color=["#718096", "#2f855a", "#718096", "#2f855a"][: len(vals)])
    ax.set_xticks(np.arange(len(vals)))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Expert information fraction")
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "e4_spectral_normalization.png", dpi=220)
    plt.close(fig)


def plot_e5(df: pd.DataFrame) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    labels = df["method_label"].tolist()
    vals = df["loadcv_mean"].to_numpy()
    ax.bar(np.arange(len(vals)), vals, color="#4a5568")
    ax.set_xticks(np.arange(len(vals)))
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_ylabel("LoadCV")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "e5_frequency_ablation.png", dpi=220)
    plt.close(fig)

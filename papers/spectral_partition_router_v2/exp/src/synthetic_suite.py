"""Synthetic experiment utilities for Spectral Partition Router v2.

The suite is intentionally self-contained: it builds synthetic feature
populations, calibrates routers only from unlabeled features and optional
expert weights, evaluates held-out routing metrics, and writes report-ready
figures/tables for the V2 paper as a self-contained experiment suite.
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
from sklearn.metrics import normalized_mutual_info_score

from .registry import EXPERIMENTS, ROOT


METHOD_LABELS = {
    "vanilla": "Vanilla linear",
    "simplex": "Simplex prototype",
    "proto_svd": "Expert-SVD top-1",
    "proto_mpi": "MPI one-step top-1",
    "spr_fixed": "SPR-Fixed",
    "spr_local": "SPR-Local",
    "spr_expert": "SPR-Expert",
    "spr_expert_mpi": "SPR-Expert-MPI",
    "balanced": "Balanced assignment",
    "lb_control": "Load-balance control",
    "frozen_spr": "Frozen-SPR",
    "spr_init_linear": "SPR-init-linear",
    "slow_update_spr": "SlowUpdate-SPR",
}


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def unit_rows(x: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    return x / (np.linalg.norm(x, axis=1, keepdims=True) + eps)


def unit_vector(x: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    return x / (np.linalg.norm(x) + eps)


def regular_simplex(e: int, d: int) -> np.ndarray:
    """Return e approximately simplex vertices embedded in R^d."""
    if e > d + 1:
        z = rng(7919 + e * 13 + d).normal(size=(e, d))
        return unit_rows(z)
    h = np.eye(e) - np.ones((e, e)) / e
    u, _, _ = np.linalg.svd(h, full_matrices=False)
    coords = u[:, : e - 1]
    out = np.zeros((e, d))
    out[:, : e - 1] = coords
    return unit_rows(out)


def center_whiten_fit(x: np.ndarray, eps: float = 1e-5) -> tuple[np.ndarray, np.ndarray]:
    mu = x.mean(axis=0)
    xc = x - mu
    cov = np.cov(xc, rowvar=False)
    vals, vecs = np.linalg.eigh(cov)
    vals = np.maximum(vals, eps)
    mat = vecs @ np.diag(1.0 / np.sqrt(vals)) @ vecs.T
    return mu, mat


def center_whiten_apply(x: np.ndarray, mu: np.ndarray, mat: np.ndarray) -> np.ndarray:
    return (x - mu) @ mat


def sample_gaussian(r: np.random.Generator, n: int, d: int) -> np.ndarray:
    return r.normal(size=(n, d))


def sample_spherical(r: np.random.Generator, n: int, d: int) -> np.ndarray:
    x = r.normal(size=(n, d))
    x = unit_rows(x)
    return np.sqrt(d) * x


def sample_axis_jitter(r: np.random.Generator, n: int, d: int, noise: float = 0.02) -> np.ndarray:
    idx = r.integers(0, d, size=n)
    signs = r.choice([-1.0, 1.0], size=n)
    x = np.zeros((n, d))
    x[np.arange(n), idx] = signs * np.sqrt(d)
    x += noise * r.normal(size=(n, d))
    return x


def sample_sparse_mixture(r: np.random.Generator, n: int, d: int, k: int = 4) -> np.ndarray:
    x = np.zeros((n, d))
    for i in range(n):
        idx = r.choice(d, size=min(k, d), replace=False)
        vals = r.choice([-1.0, 1.0], size=len(idx))
        x[i, idx] = vals
    x = unit_rows(x) * np.sqrt(d)
    x += 0.03 * r.normal(size=(n, d))
    return x


def sample_paired_dirs(r: np.random.Generator, n: int, d: int) -> np.ndarray:
    q, _ = np.linalg.qr(r.normal(size=(d, d)))
    idx = r.integers(0, d, size=n)
    signs = r.choice([-1.0, 1.0], size=n)
    radii = 0.8 + 0.4 * r.beta(2.0, 5.0, size=n)
    x = signs[:, None] * q[idx] * (np.sqrt(d) * radii[:, None])
    x += 0.025 * r.normal(size=(n, d))
    return x


def make_latent_features(
    r: np.random.Generator,
    n: int,
    d: int,
    k: int,
    separation: float = 2.2,
    noise: float = 0.55,
    directions: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if directions is None:
        directions = regular_simplex(k, d)
    labels = np.arange(n) % k
    r.shuffle(labels)
    x = separation * directions[labels] + noise * r.normal(size=(n, d))
    return x, labels, directions


def covariance_stats(x: np.ndarray) -> tuple[float, float]:
    cov = np.cov(x, rowvar=False)
    vals = np.linalg.eigvalsh(cov)
    vals = np.maximum(vals, 1e-12)
    cond = float(vals.max() / vals.min())
    eff_rank = float((vals.sum() ** 2) / np.square(vals).sum())
    return cond, eff_rank


@dataclass
class RouteResult:
    routes: np.ndarray
    margins: np.ndarray


class LinearRouter:
    def __init__(self, rows: np.ndarray):
        self.rows = unit_rows(rows)

    def route(self, x: np.ndarray) -> RouteResult:
        scores = x @ self.rows.T
        routes = np.argmax(scores, axis=1)
        part = np.partition(scores, -2, axis=1)
        margins = part[:, -1] - part[:, -2]
        return RouteResult(routes=routes, margins=margins)


class BalancedAssignment:
    """Batch-level forced-count control, intentionally not a feature router."""

    def __init__(self, e: int, direction: np.ndarray):
        self.e = e
        self.direction = unit_vector(direction)

    def route(self, x: np.ndarray) -> RouteResult:
        order = np.argsort(x @ self.direction, kind="mergesort")
        routes = np.empty(len(x), dtype=int)
        splits = np.array_split(order, self.e)
        for expert, idx in enumerate(splits):
            routes[idx] = expert
        return RouteResult(routes=routes, margins=np.full(len(x), np.nan))


@dataclass
class TreeNode:
    experts: tuple[int, ...]
    direction: np.ndarray | None = None
    threshold: float | None = None
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


class SPRTree:
    def __init__(
        self,
        e: int,
        policy: str,
        r: np.random.Generator,
        prototypes: np.ndarray | None = None,
        n_candidates: int = 24,
        max_local_samples: int = 2048,
    ):
        self.e = e
        self.policy = policy
        self.r = r
        self.prototypes = None if prototypes is None else unit_rows(prototypes)
        self.n_candidates = n_candidates
        self.max_local_samples = max_local_samples
        self.root: TreeNode | None = None

    def fit(self, x: np.ndarray) -> "SPRTree":
        idx = np.arange(len(x))
        self.root = self._fit_node(x, idx, tuple(range(self.e)))
        return self

    def route(self, x: np.ndarray) -> RouteResult:
        if self.root is None:
            raise RuntimeError("SPRTree must be fitted before routing.")
        routes = np.empty(len(x), dtype=int)
        margins = np.full(len(x), np.inf, dtype=float)
        self._route_many(x, np.arange(len(x)), self.root, routes, margins)
        margins[~np.isfinite(margins)] = np.nan
        return RouteResult(routes=routes, margins=margins)

    def _fit_node(self, x: np.ndarray, idx: np.ndarray, experts: tuple[int, ...]) -> TreeNode:
        node = TreeNode(experts=experts)
        if len(experts) == 1:
            return node
        left_n = len(experts) // 2
        left_experts, right_experts, direction = self._choose_split(x, idx, experts, left_n)
        proj = x[idx] @ direction
        rho = left_n / len(experts)
        threshold = float(np.quantile(proj, rho, method="linear"))
        left_mask = proj <= threshold
        if left_mask.all() or (~left_mask).all():
            order = np.argsort(proj, kind="mergesort")
            left_mask = np.zeros_like(proj, dtype=bool)
            left_mask[order[: max(1, int(round(rho * len(order))))]] = True
        node.direction = direction
        node.threshold = threshold
        node.left = self._fit_node(x, idx[left_mask], left_experts)
        node.right = self._fit_node(x, idx[~left_mask], right_experts)
        return node

    def _choose_split(
        self, x: np.ndarray, idx: np.ndarray, experts: tuple[int, ...], left_n: int
    ) -> tuple[tuple[int, ...], tuple[int, ...], np.ndarray]:
        if self.policy == "expert" and self.prototypes is not None:
            proto = self.prototypes[list(experts)]
            centered = proto - proto.mean(axis=0, keepdims=True)
            if np.linalg.norm(centered) > 1e-10 and len(experts) > 2:
                _, _, vh = np.linalg.svd(centered, full_matrices=False)
                axis = vh[0]
                order = np.argsort(proto @ axis)
            else:
                order = np.arange(len(experts))
            left = tuple(np.array(experts)[order[:left_n]].tolist())
            right = tuple(np.array(experts)[order[left_n:]].tolist())
            q = self.prototypes[list(left)].mean(axis=0) - self.prototypes[list(right)].mean(axis=0)
            if np.linalg.norm(q) > 1e-10:
                return left, right, unit_vector(q)
        left = tuple(experts[:left_n])
        right = tuple(experts[left_n:])
        if self.policy == "local":
            return left, right, self._local_direction(x, idx, left_n / len(experts))
        return left, right, unit_vector(self.r.normal(size=x.shape[1]))

    def _local_direction(self, x: np.ndarray, idx: np.ndarray, rho: float) -> np.ndarray:
        if len(idx) > self.max_local_samples:
            idx = self.r.choice(idx, size=self.max_local_samples, replace=False)
        xs = x[idx]
        best_q = None
        best_score = np.inf
        for _ in range(self.n_candidates):
            q = unit_vector(self.r.normal(size=x.shape[1]))
            proj = xs @ q
            tau = np.quantile(proj, rho, method="linear")
            mask = proj <= tau
            if mask.all() or (~mask).all():
                continue
            score = _weighted_within_variance(xs, mask)
            if score < best_score:
                best_score = score
                best_q = q
        if best_q is None:
            best_q = unit_vector(self.r.normal(size=x.shape[1]))
        return best_q

    def _route_one(self, row: np.ndarray, node: TreeNode, margin: float) -> tuple[int, float]:
        if len(node.experts) == 1:
            return node.experts[0], margin
        assert node.direction is not None and node.threshold is not None
        val = float(row @ node.direction)
        margin = min(margin, abs(val - node.threshold))
        if val <= node.threshold:
            assert node.left is not None
            return self._route_one(row, node.left, margin)
        assert node.right is not None
        return self._route_one(row, node.right, margin)

    def _route_many(
        self,
        x: np.ndarray,
        idx: np.ndarray,
        node: TreeNode,
        routes: np.ndarray,
        margins: np.ndarray,
    ) -> None:
        if len(idx) == 0:
            return
        if len(node.experts) == 1:
            routes[idx] = node.experts[0]
            return
        assert node.direction is not None and node.threshold is not None
        proj = x[idx] @ node.direction
        margins[idx] = np.minimum(margins[idx], np.abs(proj - node.threshold))
        left_mask = proj <= node.threshold
        assert node.left is not None and node.right is not None
        self._route_many(x, idx[left_mask], node.left, routes, margins)
        self._route_many(x, idx[~left_mask], node.right, routes, margins)


def _weighted_within_variance(x: np.ndarray, mask: np.ndarray) -> float:
    total = 0.0
    for part in (mask, ~mask):
        xp = x[part]
        if len(xp) == 0:
            return np.inf
        mu = xp.mean(axis=0)
        total += len(xp) * float(np.mean(np.sum((xp - mu) ** 2, axis=1)))
    return total / len(x)


def make_expert_weights(
    r: np.random.Generator,
    prototypes: np.ndarray,
    hidden: int = 32,
    signal: float = 3.0,
    noise: float = 0.25,
) -> np.ndarray:
    e, d = prototypes.shape
    weights = []
    for i in range(e):
        right = unit_vector(r.normal(size=hidden))
        w = signal * np.outer(prototypes[i], right)
        w += noise * r.normal(size=(d, hidden))
        weights.append(w)
    return np.stack(weights, axis=0)


def svd_prototypes(weights: np.ndarray) -> np.ndarray:
    vecs = []
    for w in weights:
        u, _, _ = np.linalg.svd(w, full_matrices=False)
        vecs.append(u[:, 0])
    return unit_rows(np.stack(vecs, axis=0))


def mpi_prototypes(weights: np.ndarray, r: np.random.Generator, steps: int = 1) -> np.ndarray:
    vecs = []
    for w in weights:
        v = unit_vector(r.normal(size=w.shape[0]))
        for _ in range(steps):
            v = unit_vector(w @ (w.T @ v))
        vecs.append(v)
    return unit_rows(np.stack(vecs, axis=0))


def prototype_set(kind: str, e: int, d: int, r: np.random.Generator) -> tuple[np.ndarray, np.ndarray | None]:
    if kind == "symmetric":
        q, _ = np.linalg.qr(r.normal(size=(d, d)))
        proto = unit_rows(regular_simplex(e, d) @ q)
        return proto, proto
    if kind == "clustered":
        q, _ = np.linalg.qr(r.normal(size=(d, d)))
        centers = unit_rows(regular_simplex(max(2, e // 2), d) @ q)
        proto = []
        labels = []
        for i in range(e):
            c = i % len(centers)
            proto.append(unit_vector(centers[c] + 0.22 * r.normal(size=d)))
            labels.append(c)
        return unit_rows(np.stack(proto)), np.array(labels)
    proto = unit_rows(r.normal(size=(e, d)))
    return proto, None


def build_router(
    method: str,
    x_cal: np.ndarray,
    e: int,
    r: np.random.Generator,
    prototypes: np.ndarray | None = None,
    mpi_proto: np.ndarray | None = None,
    n_candidates: int = 24,
) -> object:
    d = x_cal.shape[1]
    if method == "vanilla":
        return LinearRouter(r.normal(size=(e, d)))
    if method == "simplex":
        return LinearRouter(regular_simplex(e, d))
    if method == "proto_svd":
        if prototypes is None:
            raise ValueError("proto_svd requires prototypes")
        return LinearRouter(prototypes)
    if method == "proto_mpi":
        if mpi_proto is None:
            raise ValueError("proto_mpi requires mpi prototypes")
        return LinearRouter(mpi_proto)
    if method == "spr_fixed":
        return SPRTree(e, "fixed", r, n_candidates=n_candidates).fit(x_cal)
    if method == "spr_local":
        return SPRTree(e, "local", r, n_candidates=n_candidates).fit(x_cal)
    if method == "spr_expert":
        if prototypes is None:
            prototypes = unit_rows(r.normal(size=(e, d)))
        return SPRTree(e, "expert", r, prototypes=prototypes, n_candidates=n_candidates).fit(x_cal)
    if method == "spr_expert_mpi":
        if mpi_proto is None:
            raise ValueError("spr_expert_mpi requires mpi prototypes")
        return SPRTree(e, "expert", r, prototypes=mpi_proto, n_candidates=n_candidates).fit(x_cal)
    if method in {"balanced", "lb_control"}:
        return BalancedAssignment(e, r.normal(size=d))
    if method == "frozen_spr":
        return SPRTree(e, "local", r, n_candidates=n_candidates).fit(x_cal)
    raise ValueError(f"unknown method: {method}")


def usage_metrics(routes: np.ndarray, e: int) -> dict[str, float]:
    counts = np.bincount(routes, minlength=e).astype(float)
    usage = counts / counts.sum()
    target = 1.0 / e
    mean = usage.mean()
    loadcv = float(usage.std(ddof=0) / mean)
    return {
        "loadcv": loadcv,
        "max_abs_error": float(np.max(np.abs(usage - target))),
        "max_min_ratio": float((usage.max() + 1e-12) / (usage.min() + 1e-12)),
        "min_usage": float(usage.min()),
        "max_usage": float(usage.max()),
    }


def margin_p05(margins: np.ndarray) -> float:
    finite = margins[np.isfinite(margins)]
    if len(finite) == 0:
        return float("nan")
    return float(np.quantile(finite, 0.05))


def purity_score(routes: np.ndarray, labels: np.ndarray) -> float:
    total = 0
    for route in np.unique(routes):
        lab = labels[routes == route]
        if len(lab) == 0:
            continue
        total += np.bincount(lab).max()
    return float(total / len(labels))


def within_cell_variance(x: np.ndarray, routes: np.ndarray) -> float:
    total = 0.0
    for route in np.unique(routes):
        xr = x[routes == route]
        if len(xr) == 0:
            continue
        mu = xr.mean(axis=0)
        total += len(xr) * float(np.mean(np.sum((xr - mu) ** 2, axis=1)))
    return total / len(x)


def center_alignment(x: np.ndarray, routes: np.ndarray, prototypes: np.ndarray) -> float:
    vals = []
    for expert in range(len(prototypes)):
        xe = x[routes == expert]
        if len(xe) == 0:
            continue
        c = unit_vector(xe.mean(axis=0))
        vals.append(abs(float(c @ unit_vector(prototypes[expert]))))
    if not vals:
        return float("nan")
    return float(np.mean(vals))


def prototype_spread(prototypes: np.ndarray) -> float:
    p = unit_rows(prototypes)
    sims = p @ p.T
    iu = np.triu_indices(len(p), k=1)
    return float(1.0 - np.mean(np.abs(sims[iu])))


def evaluate_router(
    method: str,
    router: object,
    x_cal: np.ndarray,
    x_hold: np.ndarray,
    e: int,
    labels_hold: np.ndarray | None = None,
    prototypes: np.ndarray | None = None,
) -> dict[str, float | str]:
    cal = router.route(x_cal)
    hold = router.route(x_hold)
    out: dict[str, float | str] = {"method": method, "method_label": METHOD_LABELS.get(method, method)}
    for prefix, result in (("cal", cal), ("holdout", hold)):
        for key, val in usage_metrics(result.routes, e).items():
            out[f"{prefix}_{key}"] = val
        out[f"{prefix}_margin_p05"] = margin_p05(result.margins)
    out["holdout_gap"] = abs(float(out["holdout_loadcv"]) - float(out["cal_loadcv"]))
    if labels_hold is not None:
        out["route_feature_nmi"] = float(normalized_mutual_info_score(labels_hold, hold.routes))
        out["feature_purity"] = purity_score(hold.routes, labels_hold)
        out["within_cell_var"] = within_cell_variance(x_hold, hold.routes)
    if prototypes is not None:
        out["cell_proto_alignment"] = center_alignment(x_hold, hold.routes, prototypes)
    return out


def write_metrics(rows: list[dict[str, object]], exp_id: str) -> pd.DataFrame:
    spec = EXPERIMENTS[exp_id]
    path = ROOT / spec.metrics_csv
    path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    return df


def result_dir(exp_id: str) -> Path:
    path = ROOT / EXPERIMENTS[exp_id].result_dir
    (path / "figures").mkdir(parents=True, exist_ok=True)
    return path


def ensure_latex_dirs() -> None:
    (ROOT / "latex" / "figures").mkdir(parents=True, exist_ok=True)
    (ROOT / "latex" / "tables").mkdir(parents=True, exist_ok=True)


def save_figure(fig: plt.Figure, exp_id: str, figure_filename: str) -> None:
    ensure_latex_dirs()
    rd = result_dir(exp_id)
    for ext in ("pdf", "png"):
        local = rd / "figures" / figure_filename.replace(".pdf", f".{ext}")
        latex = ROOT / "latex" / "figures" / figure_filename.replace(".pdf", f".{ext}")
        fig.savefig(local, bbox_inches="tight", dpi=180)
        fig.savefig(latex, bbox_inches="tight", dpi=180)
    plt.close(fig)


def aggregate(df: pd.DataFrame, group_cols: list[str], metric_cols: list[str]) -> pd.DataFrame:
    agg = df.groupby(group_cols, dropna=False)[metric_cols].agg(["mean", "std"]).reset_index()
    agg.columns = [
        "_".join([c for c in col if c]).rstrip("_") if isinstance(col, tuple) else col
        for col in agg.columns
    ]
    return agg


def barplot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    hue_col: str | None,
    title: str,
    ylabel: str,
    filename: str,
    exp_id: str,
    rotate: int = 25,
) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    if hue_col is None:
        vals = df.groupby(x_col)[y_col].mean().sort_values()
        ax.bar(vals.index.astype(str), vals.values, color="#4C78A8")
    else:
        pivot = df.pivot_table(index=x_col, columns=hue_col, values=y_col, aggfunc="mean")
        pivot.plot(kind="bar", ax=ax, width=0.82)
        ax.legend(frameon=False, fontsize=8)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("")
    ax.tick_params(axis="x", labelrotation=rotate)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    save_figure(fig, exp_id, filename)


def lineplot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    hue_col: str,
    title: str,
    ylabel: str,
    filename: str,
    exp_id: str,
) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    for label, sub in df.groupby(hue_col):
        sub = sub.sort_values(x_col)
        ax.plot(sub[x_col], sub[y_col], marker="o", linewidth=1.8, label=str(label))
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(x_col.replace("_", " "))
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    save_figure(fig, exp_id, filename)


def write_summary(exp_id: str, title: str, bullets: Iterable[str], df: pd.DataFrame) -> None:
    spec = EXPERIMENTS[exp_id]
    path = ROOT / spec.summary_md
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {exp_id}: {title}",
        "",
        "## What this experiment tests",
        "",
        spec.role,
        "",
        "## Result summary",
        "",
    ]
    lines.extend(f"- {item}" for item in bullets)
    lines.extend(
        [
            "",
            "## Artifact map",
            "",
            f"- Metrics: `{spec.metrics_csv}`",
            f"- Paper table: `{spec.table_tex}`",
            "- Figures:",
        ]
    )
    lines.extend(f"  - `{path}`" for _, path in spec.figures)
    lines.extend(["", "## Rows", "", f"{len(df)} metric rows were written."])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

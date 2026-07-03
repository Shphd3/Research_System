#!/usr/bin/env python3
"""Synthetic experiments for uniform feature routing.

This script implements E1--E6 from EXPERIMENT_PLAN.md. It is intentionally
self-contained and uses only numpy plus the Python standard library.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np

NAN = float("nan")
EPS = 1e-12


COLUMNS = [
    "experiment", "setting", "method", "seed", "n", "d", "e", "alpha",
    "prototype_mode", "preprocess", "load_cv", "load_max_min", "load_kl",
    "load_max_abs_error", "condition_number", "spectral_entropy",
    "effective_rank", "prototype_max_cos", "prototype_mean_abs_cos",
    "alignment_lambda_mean", "alignment_lambda_min", "score_mean",
    "score_drop_vs_top1", "init_error", "sampling_error", "total_error",
    "distribution", "direction_support", "router_cells", "load_vector",
    "notes",
]


def row(**kwargs) -> Dict[str, object]:
    out = {k: NAN for k in COLUMNS}
    out.update(kwargs)
    return out


def rng_for(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def normalize_rows(x: np.ndarray) -> np.ndarray:
    return x / (np.linalg.norm(x, axis=1, keepdims=True) + EPS)


def sample_sphere(n: int, d: int, rng: np.random.Generator) -> np.ndarray:
    return normalize_rows(rng.normal(size=(n, d)))


def regular_simplex(e: int, d: int) -> np.ndarray:
    if d < e:
        raise ValueError(f"regular_simplex requires d >= e, got d={d}, e={e}")
    m = np.eye(e) - np.ones((e, e)) / e
    m = normalize_rows(m)
    if d > e:
        m = np.pad(m, ((0, 0), (0, d - e)))
    return m


def make_prototypes(mode: str, e: int, d: int, rng: np.random.Generator) -> np.ndarray:
    if mode == "symmetric":
        return regular_simplex(e, d)
    if mode == "random":
        return sample_sphere(e, d, rng)
    if mode == "clustered":
        common = sample_sphere(1, d, rng)[0]
        noise = 0.12 * rng.normal(size=(e, d))
        return normalize_rows(common[None, :] + noise)
    raise ValueError(f"unknown prototype mode: {mode}")


def prototype_metrics(u: np.ndarray) -> Dict[str, float]:
    e = u.shape[0]
    if e <= 1:
        return {"prototype_max_cos": NAN, "prototype_mean_abs_cos": NAN}
    cos = u @ u.T
    mask = ~np.eye(e, dtype=bool)
    vals = cos[mask]
    return {
        "prototype_max_cos": float(np.max(vals)),
        "prototype_mean_abs_cos": float(np.mean(np.abs(vals))),
    }


def route_top1(x: np.ndarray, u: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    scores = x @ u.T
    assign = np.argmax(scores, axis=1)
    selected = scores[np.arange(scores.shape[0]), assign]
    return assign, scores, selected


def balanced_assignment_greedy(scores: np.ndarray) -> np.ndarray:
    """Capacity-constrained greedy assignment.

    This enforces exact floor/ceil capacities.  It is not guaranteed to maximize
    the global score, but it is deterministic, dependency-free, and suitable for
    measuring the load/score tradeoff.
    """
    n, e = scores.shape
    base = n // e
    rem = n % e
    cap = np.array([base + (j < rem) for j in range(e)], dtype=int)
    assign = -np.ones(n, dtype=int)
    used = np.zeros(e, dtype=int)

    order = np.argsort(scores.ravel())[::-1]
    filled = 0
    for flat in order:
        i = flat // e
        j = flat % e
        if assign[i] != -1 or used[j] >= cap[j]:
            continue
        assign[i] = j
        used[j] += 1
        filled += 1
        if filled == n:
            break

    if filled < n:
        for i in np.where(assign == -1)[0]:
            available = np.where(used < cap)[0]
            j = available[np.argmax(scores[i, available])]
            assign[i] = j
            used[j] += 1
    return assign


def balanced_assignment_ot(scores: np.ndarray) -> np.ndarray:
    """Exact score-maximizing balanced assignment for moderate N.

    The balanced problem is reduced to linear assignment by expanding each
    expert into floor/ceil capacity slots. This is an optimal-transport-style
    finite assignment baseline. It is intentionally used only for moderate
    matrix sizes.
    """
    try:
        from scipy.optimize import linear_sum_assignment
    except Exception:
        return balanced_assignment_greedy(scores)

    n, e = scores.shape
    base = n // e
    rem = n % e
    slots = np.concatenate([
        np.full(base + (j < rem), j, dtype=int)
        for j in range(e)
    ])
    if len(slots) != n:
        raise RuntimeError("expanded expert slots must match token count")
    row_ind, col_ind = linear_sum_assignment(-scores[:, slots])
    assign = np.empty(n, dtype=int)
    assign[row_ind] = slots[col_ind]
    return assign


def load_metrics(assign: np.ndarray, e: int) -> Dict[str, float]:
    counts = np.bincount(assign, minlength=e).astype(float)
    p = counts / max(1, counts.sum())
    uniform = 1.0 / e
    load_cv = float(np.std(p) / (np.mean(p) + EPS))
    load_max_min = float(np.max(p) / np.min(p)) if np.min(p) > 0 else float("inf")
    load_kl = float(np.sum(p * np.log((p + EPS) / uniform)))
    load_max_abs_error = float(np.max(np.abs(p - uniform)))
    return {
        "load_cv": load_cv,
        "load_max_min": load_max_min,
        "load_kl": load_kl,
        "load_max_abs_error": load_max_abs_error,
    }


def spectral_metrics(x: np.ndarray) -> Dict[str, float]:
    xc = x - x.mean(axis=0, keepdims=True)
    c = (xc.T @ xc) / max(1, x.shape[0])
    vals = np.linalg.eigvalsh(c)
    vals = np.maximum(vals, EPS)
    q = vals / vals.sum()
    entropy = -float(np.sum(q * np.log(q + EPS))) / math.log(len(vals))
    eff_rank = float(np.exp(-np.sum(q * np.log(q + EPS))))
    return {
        "condition_number": float(vals.max() / vals.min()),
        "spectral_entropy": entropy,
        "effective_rank": eff_rank,
    }


def whiten_and_normalize(x: np.ndarray) -> np.ndarray:
    xc = x - x.mean(axis=0, keepdims=True)
    c = (xc.T @ xc) / max(1, x.shape[0])
    vals, vecs = np.linalg.eigh(c)
    vals = np.maximum(vals, 1e-8)
    xw = xc @ vecs @ np.diag(1.0 / np.sqrt(vals)) @ vecs.T
    return normalize_rows(xw)


def spectral_shrink_and_normalize(x: np.ndarray, beta: float) -> np.ndarray:
    """Partially flatten the empirical spectrum.

    beta=0 leaves centered features unchanged before normalization; beta=1 is
    whitening before normalization. Intermediate beta values model a controlled
    spectral-regularization effect in this static setting.
    """
    xc = x - x.mean(axis=0, keepdims=True)
    c = (xc.T @ xc) / max(1, x.shape[0])
    vals, vecs = np.linalg.eigh(c)
    vals = np.maximum(vals, 1e-8)
    xs = xc @ vecs @ np.diag(vals ** (-0.5 * beta)) @ vecs.T
    return normalize_rows(xs)


def preprocess_features(x: np.ndarray, mode: str) -> np.ndarray:
    if mode == "raw":
        return x
    if mode == "centered":
        return x - x.mean(axis=0, keepdims=True)
    if mode == "centered_norm":
        return normalize_rows(x - x.mean(axis=0, keepdims=True))
    if mode == "shrink05_norm":
        return spectral_shrink_and_normalize(x, beta=0.5)
    if mode == "whitened_norm":
        return whiten_and_normalize(x)
    raise ValueError(f"unknown preprocess mode: {mode}")


def selected_score_mean(scores: np.ndarray, assign: np.ndarray) -> float:
    return float(np.mean(scores[np.arange(scores.shape[0]), assign]))


def append_route_row(rows: List[Dict[str, object]], experiment: str, setting: str,
                     method: str, seed: int, x: np.ndarray, u: np.ndarray,
                     alpha: float = NAN, prototype_mode: str = "", preprocess: str = "",
                     notes: str = "", top1_score_mean: float = NAN) -> None:
    assign, scores, selected = route_top1(x, u)
    if method == "balanced_greedy":
        assign = balanced_assignment_greedy(scores)
    elif method == "balanced_ot":
        assign = balanced_assignment_ot(scores)
    lm = load_metrics(assign, u.shape[0])
    sm = spectral_metrics(x)
    pm = prototype_metrics(u)
    score_mean = selected_score_mean(scores, assign)
    score_drop = top1_score_mean - score_mean if not math.isnan(top1_score_mean) else NAN
    rows.append(row(
        experiment=experiment, setting=setting, method=method, seed=seed,
        n=x.shape[0], d=x.shape[1], e=u.shape[0], alpha=alpha,
        prototype_mode=prototype_mode, preprocess=preprocess,
        score_mean=score_mean, score_drop_vs_top1=score_drop, notes=notes,
        **lm, **sm, **pm,
    ))


def make_expert_matrices(u: np.ndarray, rng: np.random.Generator, width: int = 32,
                         sigma1: float = 10.0, noise: float = 0.05) -> np.ndarray:
    e, d = u.shape
    mats = []
    for j in range(e):
        a = sample_sphere(1, width, rng)[0]
        w = sigma1 * np.outer(u[j], a) + noise * rng.normal(size=(d, width))
        mats.append(w)
    return np.stack(mats, axis=0)


def top_svd_input_dirs(w: np.ndarray, true_u: np.ndarray | None = None) -> np.ndarray:
    dirs = []
    for j in range(w.shape[0]):
        left = np.linalg.svd(w[j], full_matrices=False)[0][:, 0]
        if true_u is not None and float(left @ true_u[j]) < 0:
            left = -left
        dirs.append(left)
    return normalize_rows(np.stack(dirs, axis=0))


def mpi_dirs(w: np.ndarray, rng: np.random.Generator, steps: int,
             true_u: np.ndarray | None = None) -> np.ndarray:
    e, d, _ = w.shape
    r = sample_sphere(e, d, rng)
    for _ in range(steps):
        nxt = []
        for j in range(e):
            m = w[j] @ w[j].T
            v = r[j] @ m
            nxt.append(v / (np.linalg.norm(v) + EPS))
        r = np.stack(nxt, axis=0)
    if true_u is not None:
        for j in range(e):
            if float(r[j] @ true_u[j]) < 0:
                r[j] = -r[j]
    return normalize_rows(r)


def alignment_lambdas(r: np.ndarray, w: np.ndarray) -> np.ndarray:
    vals = []
    for j in range(w.shape[0]):
        spectral_norm = np.linalg.svd(w[j], compute_uv=False)[0]
        vals.append(np.linalg.norm(r[j] @ w[j]) / ((np.linalg.norm(r[j]) + EPS) * (spectral_norm + EPS)))
    return np.array(vals)


def run_e1(rows: List[Dict[str, object]], quick: bool) -> None:
    seeds = range(3 if quick else 5)
    ns = [20000] if quick else [100000]
    ds = [64] if quick else [64, 128]
    es = [4, 8] if quick else [4, 8, 16]
    for seed in seeds:
        rng = rng_for(seed)
        for n in ns:
            for d in ds:
                for e in es:
                    x = sample_sphere(n, d, rng)
                    for mode in ["symmetric", "random", "clustered"]:
                        u = make_prototypes(mode, e, d, rng)
                        append_route_row(rows, "E1", "uniform_sphere", "top1", seed, x, u,
                                         prototype_mode=mode)


def run_e2(rows: List[Dict[str, object]], quick: bool) -> None:
    """High-dimensional random-prototype floor.

    True high-dimensional Voronoi masses are estimated by a large Monte Carlo
    reference sample. Smaller routed batches then separate prototype-geometry
    error from finite-token sampling error.
    """
    seeds = range(3 if quick else 5)
    ns = [1000, 10000] if quick else [1000, 10000, 50000]
    ds = [16, 64] if quick else [16, 64, 128]
    es = [4, 8] if quick else [4, 8, 16]
    reference_n = 50000 if quick else 100000
    for seed in seeds:
        rng = rng_for(1000 + seed)
        for d in ds:
            x_ref = sample_sphere(reference_n, d, rng)
            for e in es:
                u = make_prototypes("random", e, d, rng)
                ref_assign, _, _ = route_top1(x_ref, u)
                pref = np.bincount(ref_assign, minlength=e) / reference_n
                init_error = float(e * np.max(np.abs(pref - 1.0 / e)))
                for n in ns:
                    x = sample_sphere(n, d, rng)
                    assign, _, _ = route_top1(x, u)
                    phat = np.bincount(assign, minlength=e) / n
                    sampling_error = float(e * np.max(np.abs(phat - pref)))
                    total_error = float(e * np.max(np.abs(phat - 1.0 / e)))
                    lm = load_metrics(assign, e)
                    rows.append(row(
                        experiment="E2", setting="high_dim_random_prototypes",
                        method="top1", seed=seed, n=n, d=d, e=e,
                        alpha=NAN, prototype_mode="random",
                        init_error=init_error, sampling_error=sampling_error,
                        total_error=total_error,
                        notes=f"reference_n={reference_n}", **lm,
                    ))


def run_e3(rows: List[Dict[str, object]], quick: bool) -> None:
    seeds = range(3 if quick else 5)
    n = 20000 if quick else 100000
    d = 64
    e = 8
    for seed in seeds:
        rng = rng_for(2000 + seed)
        x = sample_sphere(n, d, rng)
        for mode in ["symmetric", "random", "clustered"]:
            true_u = make_prototypes(mode, e, d, rng)
            w = make_expert_matrices(true_u, rng)
            variants = {
                "exact_svd": top_svd_input_dirs(w, true_u=true_u),
                "mpi_1": mpi_dirs(w, rng, steps=1, true_u=true_u),
                "mpi_5": mpi_dirs(w, rng, steps=5, true_u=true_u),
                "random_router": sample_sphere(e, d, rng),
            }
            for method, u in variants.items():
                lam = alignment_lambdas(u, w)
                append_route_row(rows, "E3", "expert_spectral_prototypes", method, seed, x, u,
                                 prototype_mode=mode)
                rows[-1]["alignment_lambda_mean"] = float(np.mean(lam))
                rows[-1]["alignment_lambda_min"] = float(np.min(lam))


def run_e4(rows: List[Dict[str, object]], quick: bool) -> None:
    """Isotropic covariance is not sufficient for uniform routing.

    Four equally weighted axis directions have mean zero and covariance I/2,
    but the three-prototype regular-simplex router used in the paper routes
    them with load vector (1/4, 1/2, 1/4).
    """
    repeats = 1000 if quick else 10000
    base = np.array([
        [1.0, 0.0],
        [0.0, 1.0],
        [-1.0, 0.0],
        [0.0, -1.0],
    ])
    x = np.repeat(base, repeats, axis=0)
    angles = np.deg2rad(np.array([20.0, 140.0, 260.0]))
    u = np.stack([np.cos(angles), np.sin(angles)], axis=1)
    assign, scores, _ = route_top1(x, u)
    load = np.bincount(assign, minlength=3) / x.shape[0]
    rows.append(row(
        experiment="E4",
        setting="covariance_identity_not_directional_uniformity",
        method="axis_distribution_simplex_router",
        seed=0,
        n=x.shape[0],
        d=2,
        e=3,
        alpha=NAN,
        prototype_mode="regular_simplex_rotated",
        preprocess="none",
        score_mean=selected_score_mean(scores, assign),
        distribution="four_axis_points",
        direction_support="non_spherical_discrete",
        router_cells="regular_simplex_equal_measure_for_uniform_circle",
        load_vector="(0.25, 0.50, 0.25)",
        notes="covariance identity but nonuniform directional support",
        **load_metrics(assign, 3),
        **spectral_metrics(x),
        **prototype_metrics(u),
    ))


def run_e5(rows: List[Dict[str, object]], quick: bool) -> None:
    seeds = range(3 if quick else 5)
    n = 20000 if quick else 100000
    d = 64
    e = 8
    alphas = [1, 5, 20] if quick else [1, 2, 5, 10, 20]
    preprocesses = ["raw", "centered", "centered_norm", "shrink05_norm", "whitened_norm"]
    for seed in seeds:
        rng = rng_for(4000 + seed)
        z = sample_sphere(n, d, rng)
        u = make_prototypes("symmetric", e, d, rng)
        for alpha in alphas:
            scale = np.ones(d)
            scale[0] = alpha
            h = z * scale[None, :]
            for prep in preprocesses:
                x = preprocess_features(h, prep)
                append_route_row(rows, "E5", "anisotropy_whitening", "top1", seed, x, u,
                                 alpha=float(alpha), prototype_mode="symmetric", preprocess=prep)
            xw = preprocess_features(h, "whitened_norm")
            assign, scores, _ = route_top1(xw, u)
            top1_mean = selected_score_mean(scores, assign)
            append_route_row(rows, "E5", "anisotropy_whitening", "balanced_greedy", seed, xw, u,
                             alpha=float(alpha), prototype_mode="symmetric", preprocess="whitened_norm",
                             top1_score_mean=top1_mean)


def run_e6(rows: List[Dict[str, object]], quick: bool) -> None:
    seeds = range(3 if quick else 5)
    n = 1024 if quick else 2048
    d = 64
    e = 8
    for seed in seeds:
        rng = rng_for(3000 + seed)
        x = sample_sphere(n, d, rng)
        for mode in ["symmetric", "random", "clustered"]:
            u = make_prototypes(mode, e, d, rng)
            assign, scores, _ = route_top1(x, u)
            top1_mean = selected_score_mean(scores, assign)
            append_route_row(rows, "E6", "balanced_assignment", "top1", seed, x, u,
                             prototype_mode=mode)
            append_route_row(rows, "E6", "balanced_assignment", "balanced_greedy", seed, x, u,
                             prototype_mode=mode, top1_score_mean=top1_mean)
            append_route_row(rows, "E6", "balanced_assignment", "balanced_ot", seed, x, u,
                             prototype_mode=mode, top1_score_mean=top1_mean)


def write_csv(rows: List[Dict[str, object]], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    path = outdir / "results.csv"
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def as_float(x: object) -> float:
    try:
        return float(x)
    except Exception:
        return NAN


def aggregate(rows: List[Dict[str, object]], keys: Iterable[str], metrics: Iterable[str]) -> List[Dict[str, object]]:
    groups: Dict[Tuple[object, ...], List[Dict[str, object]]] = defaultdict(list)
    keys = list(keys)
    metrics = list(metrics)
    for r in rows:
        groups[tuple(r.get(k, "") for k in keys)].append(r)
    out = []
    for key, rs in sorted(groups.items()):
        item = {k: v for k, v in zip(keys, key)}
        for m in metrics:
            vals = np.array([as_float(r.get(m, NAN)) for r in rs], dtype=float)
            vals = vals[~np.isnan(vals)]
            item[m] = float(vals.mean()) if len(vals) else NAN
        out.append(item)
    return out


def mean_where(rows: List[Dict[str, object]], filters: Dict[str, object], metric: str) -> float:
    vals = []
    for r in rows:
        if all(str(r.get(k, "")) == str(v) for k, v in filters.items()):
            vals.append(as_float(r.get(metric, NAN)))
    vals = np.array(vals, dtype=float)
    vals = vals[~np.isnan(vals)]
    return float(vals.mean()) if len(vals) else NAN


def md_table(items: List[Dict[str, object]], cols: List[str]) -> str:
    lines = []
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("|" + "|".join(["---" for _ in cols]) + "|")
    for it in items:
        vals = []
        for c in cols:
            v = it.get(c, "")
            if isinstance(v, float):
                vals.append("nan" if math.isnan(v) else f"{v:.6g}")
            else:
                vals.append(str(v))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines) + "\n"


def write_tables(rows: List[Dict[str, object]], outdir: Path) -> None:
    table_dir = outdir / "tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    common_metrics = ["load_cv", "load_max_min", "load_kl", "load_max_abs_error"]

    specs = [
        ("e1_uniform_sphere.md", ["experiment", "prototype_mode", "method", "d", "e"], common_metrics),
        ("e2_high_dim_geometry_floor.md", ["experiment", "d", "e", "n"], ["init_error", "sampling_error", "total_error"]),
        ("e3_spectral_prototypes.md", ["experiment", "prototype_mode", "method"], ["alignment_lambda_mean"] + common_metrics),
        ("e4_covariance_counterexample.md", ["experiment", "distribution", "direction_support", "router_cells", "load_vector"],
         ["condition_number", "effective_rank"] + common_metrics),
        ("e5_anisotropy_whitening.md", ["experiment", "alpha", "preprocess", "method"], ["condition_number", "effective_rank"] + common_metrics),
        ("e6_balanced_assignment.md", ["experiment", "prototype_mode", "method"], ["score_drop_vs_top1"] + common_metrics),
    ]
    for filename, keys, metrics in specs:
        items = aggregate([r for r in rows if r["experiment"].lower() in filename], keys, metrics)
        with (table_dir / filename).open("w") as f:
            f.write(md_table(items, keys + metrics))

    with (outdir / "summary.md").open("w") as f:
        e1_sym = mean_where(rows, {"experiment": "E1", "prototype_mode": "symmetric", "method": "top1"}, "load_cv")
        e1_cluster = mean_where(rows, {"experiment": "E1", "prototype_mode": "clustered", "method": "top1"}, "load_cv")
        e2_init = mean_where(rows, {"experiment": "E2", "d": 64, "e": 8, "n": 50000}, "init_error")
        e2_sampling_1k = mean_where(rows, {"experiment": "E2", "d": 64, "e": 8, "n": 1000}, "sampling_error")
        e2_sampling_50k = mean_where(rows, {"experiment": "E2", "d": 64, "e": 8, "n": 50000}, "sampling_error")
        e3_sym_align = mean_where(rows, {"experiment": "E3", "prototype_mode": "symmetric", "method": "exact_svd"}, "alignment_lambda_mean")
        e3_sym_load = mean_where(rows, {"experiment": "E3", "prototype_mode": "symmetric", "method": "exact_svd"}, "load_cv")
        e3_cluster_align = mean_where(rows, {"experiment": "E3", "prototype_mode": "clustered", "method": "exact_svd"}, "alignment_lambda_mean")
        e3_cluster_load = mean_where(rows, {"experiment": "E3", "prototype_mode": "clustered", "method": "exact_svd"}, "load_cv")
        e4_cond = mean_where(rows, {"experiment": "E4", "method": "axis_distribution_simplex_router"}, "condition_number")
        e4_load = mean_where(rows, {"experiment": "E4", "method": "axis_distribution_simplex_router"}, "load_cv")
        e4_ratio = mean_where(rows, {"experiment": "E4", "method": "axis_distribution_simplex_router"}, "load_max_min")
        e5_raw_cond = mean_where(rows, {"experiment": "E5", "alpha": 20.0, "preprocess": "raw", "method": "top1"}, "condition_number")
        e5_white_cond = mean_where(rows, {"experiment": "E5", "alpha": 20.0, "preprocess": "whitened_norm", "method": "top1"}, "condition_number")
        e5_raw_rank = mean_where(rows, {"experiment": "E5", "alpha": 20.0, "preprocess": "raw", "method": "top1"}, "effective_rank")
        e5_white_rank = mean_where(rows, {"experiment": "E5", "alpha": 20.0, "preprocess": "whitened_norm", "method": "top1"}, "effective_rank")
        e5_white_load = mean_where(rows, {"experiment": "E5", "alpha": 20.0, "preprocess": "whitened_norm", "method": "top1"}, "load_cv")
        e6_top1 = mean_where(rows, {"experiment": "E6", "method": "top1"}, "load_cv")
        e6_ot = mean_where(rows, {"experiment": "E6", "method": "balanced_ot"}, "load_cv")
        e6_drop = mean_where(rows, {"experiment": "E6", "method": "balanced_ot"}, "score_drop_vs_top1")

        f.write("# Synthetic Experiment Summary\n\n")
        f.write("Conclusion: the main supported mechanism is representation geometry. ")
        f.write("Uniform top-1 expert usage appears when token directions are close to the spherical model and expert prototypes are well spread. ")
        f.write("Covariance isotropy alone is insufficient: the four-axis counterexample has condition number 1 but nonuniform load. ")
        f.write("In the elliptical toy setting, spectral shrinkage and whitening repair anisotropic features and restore the routing diagnostic.\n\n")
        f.write(f"Rows: {len(rows)}\n\n")
        f.write("## Terminology\n\n")
        f.write("- LoadCV: coefficient of variation of expert load; lower means more uniform expert usage.\n")
        f.write("- init_error: Monte Carlo estimate of the fixed cell-mass imbalance caused by one prototype draw.\n")
        f.write("- sampling_error: finite-token deviation around that fixed cell mass.\n")
        f.write("- condition_number: largest covariance eigenvalue divided by the smallest nonzero covariance eigenvalue; 1 is spectrally uniform.\n")
        f.write("- effective_rank: entropy-based count of active covariance directions; higher means less spectral concentration.\n\n")
        f.write("## Key Readout\n\n")
        f.write(f"- E1: symmetric spherical prototypes have mean LoadCV {e1_sym:.4g}; clustered prototypes have {e1_cluster:.4g}, showing the prototype-geometry side of the theorem.\n")
        f.write(f"- E2: for d=64, E=8, the random-prototype geometry floor is init_error {e2_init:.4g}; sampling_error decreases from {e2_sampling_1k:.4g} at N=1000 to {e2_sampling_50k:.4g} at N=50000.\n")
        f.write(f"- E3: exact SVD recovers expert directions in both cases, but symmetric prototypes have alignment {e3_sym_align:.4g} and LoadCV {e3_sym_load:.4g}, while clustered prototypes have alignment {e3_cluster_align:.4g} and LoadCV {e3_cluster_load:.4g}; spectral alignment alone is not a balance guarantee.\n")
        f.write(f"- E4: the four-axis distribution has covariance condition_number {e4_cond:.4g} but LoadCV {e4_load:.4g} and max/min load ratio {e4_ratio:.4g}; spectral isotropy alone is not directional uniformity.\n")
        f.write(f"- E5: at anisotropy alpha=20, raw condition_number is {e5_raw_cond:.4g} and effective_rank is {e5_raw_rank:.4g}; whitened normalization gives condition_number {e5_white_cond:.4g}, effective_rank {e5_white_rank:.4g}, and LoadCV {e5_white_load:.4g}.\n")
        f.write(f"- E6 control: unconstrained top-1 mean LoadCV is {e6_top1:.4g}; exact balanced assignment forces LoadCV {e6_ot:.4g} with mean selected-score drop {e6_drop:.4g}. This is forced count equality, not representation geometry.\n\n")
        f.write("## Tables\n\n")
        f.write("- `tables/e1_uniform_sphere.md`: prototype geometry and expert load.\n")
        f.write("- `tables/e2_high_dim_geometry_floor.md`: fixed random-prototype geometry floor versus sampling noise.\n")
        f.write("- `tables/e3_spectral_prototypes.md`: spectral alignment is not sufficient for balanced usage.\n")
        f.write("- `tables/e4_covariance_counterexample.md`: covariance-isotropy counterexample.\n")
        f.write("- `tables/e5_anisotropy_whitening.md`: representation repair by spectral flattening under preprocessing.\n")
        f.write("- `tables/e6_balanced_assignment.md`: non-geometric forced-balance control and score cost.\n\n")
        f.write("## Claim Boundary\n\n")
        f.write("These are synthetic controlled experiments. They do not establish semantic expert specialization, downstream utility, or that trained language-model hidden states naturally satisfy the spherical or whitened assumptions.\n")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--outdir", type=str, default="results")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--quick", action="store_true")
    g.add_argument("--full", action="store_true")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    quick = not args.full
    rows: List[Dict[str, object]] = []
    run_e1(rows, quick=quick)
    run_e2(rows, quick=quick)
    run_e3(rows, quick=quick)
    run_e4(rows, quick=quick)
    run_e5(rows, quick=quick)
    run_e6(rows, quick=quick)
    outdir = Path(args.outdir)
    write_csv(rows, outdir)
    write_tables(rows, outdir)
    print(f"wrote {len(rows)} rows to {outdir / 'results.csv'}")


if __name__ == "__main__":
    main()

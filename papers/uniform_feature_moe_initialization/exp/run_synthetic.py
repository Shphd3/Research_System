#!/usr/bin/env python3
"""Synthetic experiments for uniform feature routing.

This script implements E1--E5 from EXPERIMENT_PLAN.md.  It is intentionally
self-contained and uses only numpy plus the Python standard library.
"""

from __future__ import annotations

import argparse
import csv
import math
import os
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


def preprocess_features(x: np.ndarray, mode: str) -> np.ndarray:
    if mode == "raw":
        return x
    if mode == "centered":
        return x - x.mean(axis=0, keepdims=True)
    if mode == "centered_norm":
        return normalize_rows(x - x.mean(axis=0, keepdims=True))
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
    if method.startswith("balanced"):
        assign = balanced_assignment_greedy(scores)
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


def circular_voronoi_masses(angles: np.ndarray) -> np.ndarray:
    e = len(angles)
    order = np.argsort(angles)
    sorted_angles = angles[order]
    gaps = np.diff(np.r_[sorted_angles, sorted_angles[0] + 2 * np.pi]) / (2 * np.pi)
    masses_sorted = np.zeros(e)
    for k in range(e):
        masses_sorted[k] = 0.5 * (gaps[k - 1] + gaps[k])
    masses = np.zeros(e)
    masses[order] = masses_sorted
    return masses


def route_circle_random(n: int, angles: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    theta = rng.uniform(0, 2 * np.pi, size=n)
    tokens = np.stack([np.cos(theta), np.sin(theta)], axis=1)
    centers = np.stack([np.cos(angles), np.sin(angles)], axis=1)
    assign, _, _ = route_top1(tokens, centers)
    return assign


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
                    u = make_prototypes("symmetric", e, d, rng)
                    assign, scores, _ = route_top1(x, u)
                    top1_mean = selected_score_mean(scores, assign)
                    append_route_row(rows, "E1", "uniform_sphere", "balanced_greedy", seed, x, u,
                                     prototype_mode="symmetric", top1_score_mean=top1_mean)


def run_e2(rows: List[Dict[str, object]], quick: bool) -> None:
    seeds = range(5 if quick else 20)
    ns = [1000, 10000] if quick else [1000, 10000, 100000]
    es = [4, 8] if quick else [4, 8, 16]
    for seed in seeds:
        rng = rng_for(1000 + seed)
        for e in es:
            angles = rng.uniform(0, 2 * np.pi, size=e)
            p = circular_voronoi_masses(angles)
            init_error = float(e * np.max(np.abs(p - 1.0 / e)))
            for n in ns:
                assign = route_circle_random(n, angles, rng)
                phat = np.bincount(assign, minlength=e) / n
                sampling_error = float(e * np.max(np.abs(phat - p)))
                total_error = float(e * np.max(np.abs(phat - 1.0 / e)))
                lm = load_metrics(assign, e)
                rows.append(row(
                    experiment="E2", setting="circle_random_centers", method="top1",
                    seed=seed, n=n, d=2, e=e, alpha=NAN, prototype_mode="random_circle",
                    init_error=init_error, sampling_error=sampling_error,
                    total_error=total_error, notes="2d Voronoi decomposition", **lm,
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
    seeds = range(3 if quick else 5)
    n = 2048 if quick else 4096
    d = 64
    e = 8
    for seed in seeds:
        rng = rng_for(3000 + seed)
        x = sample_sphere(n, d, rng)
        for mode in ["symmetric", "random", "clustered"]:
            u = make_prototypes(mode, e, d, rng)
            assign, scores, _ = route_top1(x, u)
            top1_mean = selected_score_mean(scores, assign)
            append_route_row(rows, "E4", "balanced_assignment", "top1", seed, x, u,
                             prototype_mode=mode)
            append_route_row(rows, "E4", "balanced_assignment", "balanced_greedy", seed, x, u,
                             prototype_mode=mode, top1_score_mean=top1_mean)


def run_e5(rows: List[Dict[str, object]], quick: bool) -> None:
    seeds = range(3 if quick else 5)
    n = 20000 if quick else 100000
    d = 64
    e = 8
    alphas = [1, 5, 20] if quick else [1, 2, 5, 10, 20]
    preprocesses = ["raw", "centered", "centered_norm", "whitened_norm"]
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


def write_csv(rows: List[Dict[str, object]], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    path = outdir / "results.csv"
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
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
        ("e2_2d_geometry_floor.md", ["experiment", "e", "n"], ["init_error", "sampling_error", "total_error"]),
        ("e3_spectral_prototypes.md", ["experiment", "prototype_mode", "method"], ["alignment_lambda_mean"] + common_metrics),
        ("e4_balanced_assignment.md", ["experiment", "prototype_mode", "method"], ["score_drop_vs_top1"] + common_metrics),
        ("e5_anisotropy_whitening.md", ["experiment", "alpha", "preprocess", "method"], ["condition_number", "effective_rank"] + common_metrics),
    ]
    for filename, keys, metrics in specs:
        items = aggregate([r for r in rows if r["experiment"].lower() in filename], keys, metrics)
        with (table_dir / filename).open("w") as f:
            f.write(md_table(items, keys + metrics))

    with (outdir / "summary.md").open("w") as f:
        f.write("# Synthetic Experiment Summary\n\n")
        f.write(f"Rows: {len(rows)}\n\n")
        f.write("See `tables/` for compact aggregates.\n")


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
    outdir = Path(args.outdir)
    write_csv(rows, outdir)
    write_tables(rows, outdir)
    print(f"wrote {len(rows)} rows to {outdir / 'results.csv'}")


if __name__ == "__main__":
    main()

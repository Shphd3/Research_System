#!/usr/bin/env python3
"""Controlled audit for gradient common versus activation common."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ESTIMATORS = [
    "activation_pca",
    "gradient_intersection",
    "functional_shared",
    "random_control",
]

CRITERIA = [
    "gradient_overlap_reduction",
    "shared_loss_sensitivity",
    "gradient_common_alignment",
    "functional_common_alignment",
]

MISMATCH_REGIMES = [
    "activation_nuisance",
    "unique_variance",
    "functional_gradient_split",
    "entangled_residual",
]


@dataclass(frozen=True)
class RegimeConfig:
    name: str
    grad_hidden_strength: float
    func_hidden_strength: float
    unique_hidden_strength: float
    nuisance_hidden_strength: float
    grad_target_strength: float
    unique_target_strength: float
    shared_target_strength: float
    align_functional_with_gradient: bool
    entangle_unique_with_gradient: float
    description: str


REGIMES = [
    RegimeConfig(
        name="aligned_common",
        grad_hidden_strength=1.8,
        func_hidden_strength=1.2,
        unique_hidden_strength=0.6,
        nuisance_hidden_strength=0.2,
        grad_target_strength=2.0,
        unique_target_strength=0.45,
        shared_target_strength=1.4,
        align_functional_with_gradient=True,
        entangle_unique_with_gradient=0.0,
        description="Activation, functional, and gradient common are intentionally aligned.",
    ),
    RegimeConfig(
        name="activation_nuisance",
        grad_hidden_strength=0.8,
        func_hidden_strength=0.5,
        unique_hidden_strength=0.9,
        nuisance_hidden_strength=3.0,
        grad_target_strength=3.2,
        unique_target_strength=0.35,
        shared_target_strength=0.7,
        align_functional_with_gradient=False,
        entangle_unique_with_gradient=0.0,
        description="High activation variance is nuisance and should not be the optimization common.",
    ),
    RegimeConfig(
        name="unique_variance",
        grad_hidden_strength=0.8,
        func_hidden_strength=0.5,
        unique_hidden_strength=2.8,
        nuisance_hidden_strength=0.25,
        grad_target_strength=3.2,
        unique_target_strength=0.35,
        shared_target_strength=0.7,
        align_functional_with_gradient=False,
        entangle_unique_with_gradient=0.0,
        description="Group-unique directions dominate activation covariance.",
    ),
    RegimeConfig(
        name="functional_gradient_split",
        grad_hidden_strength=0.9,
        func_hidden_strength=2.7,
        unique_hidden_strength=0.9,
        nuisance_hidden_strength=0.2,
        grad_target_strength=2.9,
        unique_target_strength=0.35,
        shared_target_strength=2.2,
        align_functional_with_gradient=False,
        entangle_unique_with_gradient=0.0,
        description="Functional shared common is strong but distinct from gradient common.",
    ),
    RegimeConfig(
        name="entangled_residual",
        grad_hidden_strength=0.9,
        func_hidden_strength=0.5,
        unique_hidden_strength=2.2,
        nuisance_hidden_strength=0.6,
        grad_target_strength=3.1,
        unique_target_strength=0.35,
        shared_target_strength=0.8,
        align_functional_with_gradient=False,
        entangle_unique_with_gradient=0.55,
        description="Unique directions are partly entangled with the gradient-common subspace.",
    ),
]


def orthonormalize(x: np.ndarray) -> np.ndarray:
    q, r = np.linalg.qr(x)
    signs = np.sign(np.diag(r))
    signs[signs == 0] = 1
    return q * signs


def sample_basis(rng: np.random.Generator, d: int, k: int, against: np.ndarray | None = None) -> np.ndarray:
    x = rng.normal(size=(d, k))
    if against is not None:
        x = x - against @ (against.T @ x)
    return orthonormalize(x)[:, :k]


def sample_unique_basis(
    rng: np.random.Generator,
    d: int,
    k: int,
    grad_basis: np.ndarray,
    func_basis: np.ndarray,
    entangle: float,
) -> np.ndarray:
    protected = orthonormalize(np.concatenate([grad_basis, func_basis], axis=1))
    orth = sample_basis(rng, d, k, against=protected)
    if entangle <= 0:
        return orth
    mix = grad_basis @ rng.normal(size=(grad_basis.shape[1], k))
    basis = np.sqrt(max(0.0, 1.0 - entangle**2)) * orth + entangle * mix
    return orthonormalize(basis)[:, :k]


def top_eigvecs_sym(matrix: np.ndarray, k: int) -> np.ndarray:
    sym = 0.5 * (matrix + matrix.T)
    vals, vecs = np.linalg.eigh(sym)
    order = np.argsort(vals)[::-1]
    return vecs[:, order[:k]]


def projector(u: np.ndarray) -> np.ndarray:
    return u @ u.T


def subspace_alignment(true_basis: np.ndarray, estimated_basis: np.ndarray) -> float:
    k = true_basis.shape[1]
    return float(np.linalg.norm(true_basis.T @ estimated_basis, ord="fro") ** 2 / k)


def ridge_mse(x: np.ndarray, y: np.ndarray, ridge: float = 1e-4) -> float:
    xtx = x.T @ x
    xty = x.T @ y
    w = np.linalg.solve(xtx + ridge * np.eye(xtx.shape[0]), xty)
    pred = x @ w
    return float(np.mean((pred - y) ** 2))


def mean_abs_pairwise_cos(matrices: list[np.ndarray]) -> float:
    flats = [m.reshape(-1) for m in matrices]
    values = []
    for i in range(len(flats)):
        for j in range(i + 1, len(flats)):
            denom = np.linalg.norm(flats[i]) * np.linalg.norm(flats[j])
            if denom > 1e-12:
                values.append(abs(float(np.dot(flats[i], flats[j]) / denom)))
    return float(np.mean(values)) if values else 0.0


def compute_group_gradients(h: np.ndarray, y: np.ndarray, groups: np.ndarray, n_groups: int) -> list[np.ndarray]:
    gradients = []
    delta = -y
    for group in range(n_groups):
        idx = groups == group
        gradients.append((delta[idx].T @ h[idx]) / idx.sum())
    return gradients


def estimate_gradient_intersection(gradients: list[np.ndarray], k: int) -> np.ndarray:
    accum = None
    count = 0
    for i in range(len(gradients)):
        for j in range(i + 1, len(gradients)):
            term = gradients[i].T @ gradients[j]
            accum = term if accum is None else accum + term
            count += 1
    if accum is None:
        raise ValueError("Need at least two groups.")
    return top_eigvecs_sym(accum / count, k)


def estimate_functional_shared(h: np.ndarray, y_shared: np.ndarray, k: int) -> np.ndarray:
    cross = h.T @ y_shared / h.shape[0]
    return top_eigvecs_sym(cross @ cross.T, k)


def make_dataset(
    cfg: RegimeConfig,
    seed: int,
    d_hidden: int,
    common_rank: int,
    unique_rank: int,
    nuisance_rank: int,
    n_groups: int,
    samples_per_group: int,
    y_dim: int,
) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)

    grad_basis = sample_basis(rng, d_hidden, common_rank)
    if cfg.align_functional_with_gradient:
        func_basis = grad_basis
    else:
        func_basis = sample_basis(rng, d_hidden, common_rank, against=grad_basis)
    nuisance_basis = sample_basis(
        rng,
        d_hidden,
        nuisance_rank,
        against=orthonormalize(np.concatenate([grad_basis, func_basis], axis=1)),
    )
    unique_bases = [
        sample_unique_basis(
            rng,
            d_hidden,
            unique_rank,
            grad_basis=grad_basis,
            func_basis=func_basis,
            entangle=cfg.entangle_unique_with_gradient,
        )
        for _ in range(n_groups)
    ]

    groups = np.repeat(np.arange(n_groups), samples_per_group)
    n_samples = len(groups)
    z_grad = rng.normal(size=(n_samples, common_rank))
    z_func = rng.normal(size=(n_samples, common_rank))
    z_unique = rng.normal(size=(n_samples, unique_rank))
    z_nuisance = rng.normal(size=(n_samples, nuisance_rank))

    h = cfg.grad_hidden_strength * (z_grad @ grad_basis.T)
    h += cfg.func_hidden_strength * (z_func @ func_basis.T)
    h += cfg.nuisance_hidden_strength * (z_nuisance @ nuisance_basis.T)
    for group in range(n_groups):
        idx = groups == group
        h[idx] += cfg.unique_hidden_strength * (z_unique[idx] @ unique_bases[group].T)
    h += 0.03 * rng.normal(size=h.shape)

    grad_map = rng.normal(size=(common_rank, y_dim))
    func_map = rng.normal(size=(common_rank, y_dim))
    unique_maps = [rng.normal(size=(unique_rank, y_dim)) for _ in range(n_groups)]

    y_grad = z_grad @ grad_map
    y_shared = cfg.shared_target_strength * (z_func @ func_map)
    y_unique = np.zeros((n_samples, y_dim))
    for group in range(n_groups):
        idx = groups == group
        y_unique[idx] = z_unique[idx] @ unique_maps[group]

    y_total = cfg.grad_target_strength * y_grad + cfg.unique_target_strength * y_unique

    return {
        "h": h,
        "groups": groups,
        "grad_basis": grad_basis,
        "func_basis": func_basis,
        "y_shared": y_shared,
        "y_total": y_total,
    }


def score_projector(
    h: np.ndarray,
    p: np.ndarray,
    groups: np.ndarray,
    y_shared: np.ndarray,
    y_total: np.ndarray,
    n_groups: int,
) -> dict[str, float]:
    h_res = h - h @ p
    gradients_full = compute_group_gradients(h, y_total, groups, n_groups)
    gradients_res = compute_group_gradients(h_res, y_total, groups, n_groups)
    overlap_full = mean_abs_pairwise_cos(gradients_full)
    overlap_res = mean_abs_pairwise_cos(gradients_res)

    shared_full = ridge_mse(h, y_shared)
    shared_res = ridge_mse(h_res, y_shared)

    return {
        "gradient_overlap_full": overlap_full,
        "gradient_overlap_residualized": overlap_res,
        "gradient_overlap_reduction": overlap_full - overlap_res,
        "shared_loss_full": shared_full,
        "shared_loss_residualized": shared_res,
        "shared_loss_sensitivity": shared_res - shared_full,
        "projected_norm": float(np.mean(np.sum((h @ p) ** 2, axis=1))),
        "residual_norm": float(np.mean(np.sum(h_res**2, axis=1))),
    }


def run_seed(
    cfg: RegimeConfig,
    seed: int,
    d_hidden: int,
    common_rank: int,
    unique_rank: int,
    nuisance_rank: int,
    n_groups: int,
    samples_per_group: int,
    y_dim: int,
) -> list[dict[str, object]]:
    data = make_dataset(
        cfg,
        seed=seed,
        d_hidden=d_hidden,
        common_rank=common_rank,
        unique_rank=unique_rank,
        nuisance_rank=nuisance_rank,
        n_groups=n_groups,
        samples_per_group=samples_per_group,
        y_dim=y_dim,
    )
    h = data["h"]
    groups = data["groups"]
    grad_basis = data["grad_basis"]
    func_basis = data["func_basis"]
    y_shared = data["y_shared"]
    y_total = data["y_total"]

    gradients = compute_group_gradients(h, y_total, groups, n_groups)
    rng = np.random.default_rng(100_000 + seed)
    bases = {
        "activation_pca": top_eigvecs_sym((h.T @ h) / h.shape[0], common_rank),
        "gradient_intersection": estimate_gradient_intersection(gradients, common_rank),
        "functional_shared": estimate_functional_shared(h, y_shared, common_rank),
        "random_control": sample_basis(rng, d_hidden, common_rank),
    }

    rows = []
    for estimator, basis in bases.items():
        p = projector(basis)
        row: dict[str, object] = {
            "regime": cfg.name,
            "seed": seed,
            "estimator": estimator,
            "gradient_common_alignment": subspace_alignment(grad_basis, basis),
            "functional_common_alignment": subspace_alignment(func_basis, basis),
        }
        row.update(score_projector(h, p, groups, y_shared, y_total, n_groups))
        rows.append(row)
    return rows


def aggregate_scores(rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    estimator_summary: list[dict[str, object]] = []
    comparison_rows: list[dict[str, object]] = []
    regimes = [cfg.name for cfg in REGIMES]

    for regime in regimes:
        regime_rows = [row for row in rows if row["regime"] == regime]
        for estimator in ESTIMATORS:
            est_rows = [row for row in regime_rows if row["estimator"] == estimator]
            out: dict[str, object] = {"regime": regime, "estimator": estimator}
            for metric in CRITERIA:
                values = np.array([float(row[metric]) for row in est_rows])
                out[f"{metric}_mean"] = float(values.mean())
                out[f"{metric}_std"] = float(values.std(ddof=1))
            estimator_summary.append(out)

        seeds = sorted({int(row["seed"]) for row in regime_rows})
        margins = []
        for seed in seeds:
            act = next(
                float(row["gradient_overlap_reduction"])
                for row in regime_rows
                if row["seed"] == seed and row["estimator"] == "activation_pca"
            )
            grad = next(
                float(row["gradient_overlap_reduction"])
                for row in regime_rows
                if row["seed"] == seed and row["estimator"] == "gradient_intersection"
            )
            margins.append(grad - act)

        act_values = [
            float(row["gradient_overlap_reduction"])
            for row in regime_rows
            if row["estimator"] == "activation_pca"
        ]
        grad_values = [
            float(row["gradient_overlap_reduction"])
            for row in regime_rows
            if row["estimator"] == "gradient_intersection"
        ]
        margin_values = np.array(margins)
        comparison_rows.append(
            {
                "regime": regime,
                "activation_pca_gradient_overlap_reduction_mean": float(np.mean(act_values)),
                "gradient_intersection_gradient_overlap_reduction_mean": float(np.mean(grad_values)),
                "gradient_overlap_reduction_advantage_mean": float(margin_values.mean()),
                "gradient_overlap_reduction_advantage_std": float(margin_values.std(ddof=1)),
                "gradient_intersection_seed_win_rate": float(np.mean(margin_values > 0)),
            }
        )

    mismatch_rows = [row for row in comparison_rows if row["regime"] in MISMATCH_REGIMES]
    passed_regimes = [
        row["regime"]
        for row in mismatch_rows
        if float(row["gradient_overlap_reduction_advantage_mean"]) > 0
        and float(row["gradient_intersection_seed_win_rate"]) >= 0.8
    ]

    winner_records = []
    for regime in regimes:
        regime_rows = [row for row in rows if row["regime"] == regime]
        for criterion in CRITERIA:
            means = {}
            for estimator in ESTIMATORS:
                values = [
                    float(row[criterion])
                    for row in regime_rows
                    if row["estimator"] == estimator
                ]
                means[estimator] = float(np.mean(values))
            winner = max(means, key=means.get)
            winner_records.append(
                {
                    "regime": regime,
                    "criterion": criterion,
                    "winner": winner,
                    "winner_mean": means[winner],
                }
            )

    meta = {
        "primary_metric": "gradient_overlap_reduction_advantage",
        "mismatch_regimes": MISMATCH_REGIMES,
        "passed_mismatch_regimes": passed_regimes,
        "n_passed_mismatch_regimes": len(passed_regimes),
        "pass_rule": "at least 3 mismatch regimes with positive mean advantage and seed win rate >= 0.8",
        "pass": len(passed_regimes) >= 3,
        "winner_records": winner_records,
    }
    return estimator_summary, comparison_rows, meta


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot_gradient_overlap(rows: list[dict[str, object]], out: Path) -> None:
    regimes = [cfg.name for cfg in REGIMES]
    x = np.arange(len(regimes))
    width = 0.18
    fig, ax = plt.subplots(figsize=(12, 5.8))
    for idx, estimator in enumerate(ESTIMATORS):
        means = []
        stds = []
        for regime in regimes:
            values = np.array(
                [
                    float(row["gradient_overlap_reduction"])
                    for row in rows
                    if row["regime"] == regime and row["estimator"] == estimator
                ]
            )
            means.append(values.mean())
            stds.append(values.std(ddof=1))
        ax.bar(x + (idx - 1.5) * width, means, width=width, yerr=stds, capsize=2, label=estimator)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Gradient overlap reduction by candidate common operator")
    ax.set_ylabel("Pairwise gradient cosine reduction")
    ax.set_xticks(x)
    ax.set_xticklabels(regimes, rotation=20, ha="right")
    ax.legend(ncol=2, fontsize=9)
    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)


def plot_advantage(comparison_rows: list[dict[str, object]], out: Path) -> None:
    regimes = [cfg.name for cfg in REGIMES]
    means = [
        float(next(row for row in comparison_rows if row["regime"] == regime)["gradient_overlap_reduction_advantage_mean"])
        for regime in regimes
    ]
    stds = [
        float(next(row for row in comparison_rows if row["regime"] == regime)["gradient_overlap_reduction_advantage_std"])
        for regime in regimes
    ]
    colors = ["#777777" if regime == "aligned_common" else "#2ca02c" for regime in regimes]
    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    ax.bar(np.arange(len(regimes)), means, yerr=stds, capsize=3, color=colors)
    ax.axhline(0, color="black", linewidth=0.9)
    ax.set_title("Gradient advantage over activation PCA")
    ax.set_ylabel("P_grad reduction - P_act reduction")
    ax.set_xticks(np.arange(len(regimes)))
    ax.set_xticklabels(regimes, rotation=20, ha="right")
    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)


def plot_winner_matrix(meta: dict[str, object], out: Path) -> None:
    regimes = [cfg.name for cfg in REGIMES]
    estimator_to_id = {estimator: idx for idx, estimator in enumerate(ESTIMATORS)}
    winner_records = meta["winner_records"]
    matrix = np.zeros((len(CRITERIA), len(regimes)))
    for row in winner_records:  # type: ignore[assignment]
        i = CRITERIA.index(str(row["criterion"]))
        j = regimes.index(str(row["regime"]))
        matrix[i, j] = estimator_to_id[str(row["winner"])]

    cmap = plt.get_cmap("tab10", len(ESTIMATORS))
    fig, ax = plt.subplots(figsize=(10.8, 4.8))
    im = ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=-0.5, vmax=len(ESTIMATORS) - 0.5)
    ax.set_title("Criterion winners by regime")
    ax.set_xticks(np.arange(len(regimes)))
    ax.set_xticklabels(regimes, rotation=20, ha="right")
    ax.set_yticks(np.arange(len(CRITERIA)))
    ax.set_yticklabels(CRITERIA)
    for i in range(len(CRITERIA)):
        for j in range(len(regimes)):
            label = ESTIMATORS[int(matrix[i, j])].replace("_", "\n")
            ax.text(j, i, label, ha="center", va="center", fontsize=8, color="white")
    cbar = fig.colorbar(im, ax=ax, ticks=np.arange(len(ESTIMATORS)))
    cbar.ax.set_yticklabels(ESTIMATORS)
    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=Path("."))
    parser.add_argument("--d-hidden", type=int, default=32)
    parser.add_argument("--common-rank", type=int, default=2)
    parser.add_argument("--unique-rank", type=int, default=2)
    parser.add_argument("--nuisance-rank", type=int, default=2)
    parser.add_argument("--n-groups", type=int, default=6)
    parser.add_argument("--samples-per-group", type=int, default=500)
    parser.add_argument("--y-dim", type=int, default=3)
    parser.add_argument("--seeds", type=int, nargs="+", default=list(range(20)))
    args = parser.parse_args()

    outdir = args.outdir
    tables = outdir / "tables"
    figures = outdir / "figures"
    tables.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, object]] = []
    for cfg in REGIMES:
        for seed in args.seeds:
            rows.extend(
                run_seed(
                    cfg,
                    seed=seed,
                    d_hidden=args.d_hidden,
                    common_rank=args.common_rank,
                    unique_rank=args.unique_rank,
                    nuisance_rank=args.nuisance_rank,
                    n_groups=args.n_groups,
                    samples_per_group=args.samples_per_group,
                    y_dim=args.y_dim,
                )
            )

    estimator_summary, comparison_rows, meta = aggregate_scores(rows)

    write_csv(tables / "gradient_vs_activation_scores.csv", rows)
    write_csv(tables / "gradient_vs_activation_estimator_summary.csv", estimator_summary)
    write_csv(tables / "gradient_vs_activation_summary.csv", comparison_rows)
    with (tables / "gradient_vs_activation_winner_summary.json").open("w") as f:
        json.dump(meta, f, indent=2)
    with (tables / "run_config.json").open("w") as f:
        json.dump(
            {
                "d_hidden": args.d_hidden,
                "common_rank": args.common_rank,
                "unique_rank": args.unique_rank,
                "nuisance_rank": args.nuisance_rank,
                "n_groups": args.n_groups,
                "samples_per_group": args.samples_per_group,
                "y_dim": args.y_dim,
                "seeds": args.seeds,
                "regimes": [asdict(cfg) for cfg in REGIMES],
                "estimators": ESTIMATORS,
                "criteria": CRITERIA,
            },
            f,
            indent=2,
        )

    plot_gradient_overlap(rows, figures / "gradient_overlap_reduction_by_regime.png")
    plot_advantage(comparison_rows, figures / "gradient_advantage_by_regime.png")
    plot_winner_matrix(meta, figures / "criterion_winners_by_regime.png")

    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()

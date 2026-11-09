#!/usr/bin/env python3
"""Controlled common-operator identifiability audit.

This script generates synthetic hidden states with a known common projector and
compares several estimator families under mechanism-specific regimes.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass, asdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ESTIMATORS = [
    "activation_pca",
    "group_mean",
    "gradient_intersection",
    "feedback_drift",
    "random_control",
]

PRIMARY_CRITERIA = [
    "subspace_alignment",
    "shared_loss_sensitivity",
    "gradient_overlap_reduction",
]


@dataclass(frozen=True)
class RegimeConfig:
    name: str
    common_strength: float
    unique_strength: float
    noise_strength: float
    mean_common_strength: float
    gradient_common_strength: float
    gradient_unique_strength: float
    feedback_common_strength: float
    feedback_unique_strength: float
    description: str


REGIMES = [
    RegimeConfig(
        name="activation_dominant",
        common_strength=2.4,
        unique_strength=0.7,
        noise_strength=0.08,
        mean_common_strength=0.0,
        gradient_common_strength=1.3,
        gradient_unique_strength=0.7,
        feedback_common_strength=0.4,
        feedback_unique_strength=1.0,
        description="Common has the largest activation variance; PCA should be the known-good estimator.",
    ),
    RegimeConfig(
        name="unique_dominant",
        common_strength=0.8,
        unique_strength=2.5,
        noise_strength=0.08,
        mean_common_strength=0.0,
        gradient_common_strength=2.8,
        gradient_unique_strength=0.45,
        feedback_common_strength=0.5,
        feedback_unique_strength=1.3,
        description="Unique variance dominates activations while shared gradients still intersect on common.",
    ),
    RegimeConfig(
        name="mean_offset",
        common_strength=0.75,
        unique_strength=1.5,
        noise_strength=0.08,
        mean_common_strength=2.6,
        gradient_common_strength=1.0,
        gradient_unique_strength=0.9,
        feedback_common_strength=0.5,
        feedback_unique_strength=1.0,
        description="Common is visible as group-mean structure inside the true common subspace.",
    ),
    RegimeConfig(
        name="gradient_intersection",
        common_strength=0.7,
        unique_strength=1.8,
        noise_strength=0.08,
        mean_common_strength=0.0,
        gradient_common_strength=3.2,
        gradient_unique_strength=0.35,
        feedback_common_strength=0.4,
        feedback_unique_strength=1.4,
        description="Optimization signal is shared even though activation energy is mostly unique.",
    ),
    RegimeConfig(
        name="feedback_drift",
        common_strength=0.6,
        unique_strength=1.7,
        noise_strength=0.08,
        mean_common_strength=0.0,
        gradient_common_strength=1.2,
        gradient_unique_strength=0.9,
        feedback_common_strength=3.0,
        feedback_unique_strength=0.25,
        description="The common subspace is most visible in checkpoint-to-checkpoint feedback drift.",
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
            if denom <= 1e-12:
                continue
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
        raise ValueError("Need at least two groups for gradient intersection.")
    return top_eigvecs_sym(accum / count, k)


def estimate_group_mean(h: np.ndarray, groups: np.ndarray, n_groups: int, k: int) -> np.ndarray:
    means = np.stack([h[groups == group].mean(axis=0) for group in range(n_groups)], axis=0)
    _, _, vt = np.linalg.svd(means, full_matrices=False)
    basis = vt[:k].T
    if basis.shape[1] < k:
        basis = orthonormalize(np.pad(basis, ((0, 0), (0, k - basis.shape[1]))))
    return basis[:, :k]


def make_dataset(
    cfg: RegimeConfig,
    seed: int,
    d_hidden: int,
    common_rank: int,
    unique_rank: int,
    n_groups: int,
    samples_per_group: int,
    y_dim: int,
) -> dict[str, np.ndarray | list[np.ndarray]]:
    rng = np.random.default_rng(seed)
    common_basis = sample_basis(rng, d_hidden, common_rank)
    unique_bases = [sample_basis(rng, d_hidden, unique_rank, against=common_basis) for _ in range(n_groups)]
    noise_basis = sample_basis(rng, d_hidden, min(d_hidden, 8))

    groups = np.repeat(np.arange(n_groups), samples_per_group)
    n_samples = len(groups)
    z_common = rng.normal(size=(n_samples, common_rank))
    z_unique = rng.normal(size=(n_samples, unique_rank))
    z_noise = rng.normal(size=(n_samples, noise_basis.shape[1]))

    h = cfg.common_strength * (z_common @ common_basis.T)
    for group in range(n_groups):
        idx = groups == group
        h[idx] += cfg.unique_strength * (z_unique[idx] @ unique_bases[group].T)

    if cfg.mean_common_strength > 0:
        mean_codes = rng.normal(size=(n_groups, common_rank))
        mean_codes = mean_codes / np.maximum(np.linalg.norm(mean_codes, axis=1, keepdims=True), 1e-9)
        for group in range(n_groups):
            idx = groups == group
            h[idx] += cfg.mean_common_strength * (mean_codes[group] @ common_basis.T)

    h += cfg.noise_strength * (z_noise @ noise_basis.T)
    h += 0.02 * rng.normal(size=h.shape)

    shared_map = rng.normal(size=(common_rank, y_dim))
    y_shared = z_common @ shared_map

    unique_maps = [rng.normal(size=(unique_rank, y_dim)) for _ in range(n_groups)]
    y_rare = np.zeros((n_samples, y_dim))
    for group in range(n_groups):
        idx = groups == group
        y_rare[idx] = z_unique[idx] @ unique_maps[group]

    y_total = cfg.gradient_common_strength * y_shared + cfg.gradient_unique_strength * y_rare

    z_feedback_common = rng.normal(size=(n_samples, common_rank))
    z_feedback_unique = rng.normal(size=(n_samples, unique_rank))
    drift = cfg.feedback_common_strength * (z_feedback_common @ common_basis.T)
    for group in range(n_groups):
        idx = groups == group
        drift[idx] += cfg.feedback_unique_strength * (z_feedback_unique[idx] @ unique_bases[group].T)
    drift += 0.05 * rng.normal(size=drift.shape)

    return {
        "h": h,
        "groups": groups,
        "common_basis": common_basis,
        "drift": drift,
        "y_shared": y_shared,
        "y_rare": y_rare,
        "y_total": y_total,
    }


def score_projector(
    h: np.ndarray,
    p: np.ndarray,
    groups: np.ndarray,
    y_shared: np.ndarray,
    y_rare: np.ndarray,
    y_total: np.ndarray,
    n_groups: int,
) -> dict[str, float]:
    h_res = h - h @ p
    shared_full = ridge_mse(h, y_shared)
    shared_res = ridge_mse(h_res, y_shared)
    rare_full = ridge_mse(h, y_rare)
    rare_res = ridge_mse(h_res, y_rare)

    gradients_full = compute_group_gradients(h, y_total, groups, n_groups)
    gradients_res = compute_group_gradients(h_res, y_total, groups, n_groups)
    overlap_full = mean_abs_pairwise_cos(gradients_full)
    overlap_res = mean_abs_pairwise_cos(gradients_res)

    projected_norm = float(np.mean(np.sum((h @ p) ** 2, axis=1)))
    residual_norm = float(np.mean(np.sum(h_res**2, axis=1)))

    return {
        "shared_loss_full": shared_full,
        "shared_loss_residualized": shared_res,
        "shared_loss_sensitivity": shared_res - shared_full,
        "rare_loss_full": rare_full,
        "rare_loss_residualized": rare_res,
        "rare_loss_sensitivity": rare_res - rare_full,
        "gradient_overlap_full": overlap_full,
        "gradient_overlap_residualized": overlap_res,
        "gradient_overlap_reduction": overlap_full - overlap_res,
        "projected_norm": projected_norm,
        "residual_norm": residual_norm,
    }


def run_seed(
    cfg: RegimeConfig,
    seed: int,
    d_hidden: int,
    common_rank: int,
    unique_rank: int,
    n_groups: int,
    samples_per_group: int,
    y_dim: int,
) -> list[dict[str, float | int | str]]:
    data = make_dataset(
        cfg,
        seed=seed,
        d_hidden=d_hidden,
        common_rank=common_rank,
        unique_rank=unique_rank,
        n_groups=n_groups,
        samples_per_group=samples_per_group,
        y_dim=y_dim,
    )
    h = data["h"]  # type: ignore[assignment]
    groups = data["groups"]  # type: ignore[assignment]
    common_basis = data["common_basis"]  # type: ignore[assignment]
    drift = data["drift"]  # type: ignore[assignment]
    y_shared = data["y_shared"]  # type: ignore[assignment]
    y_rare = data["y_rare"]  # type: ignore[assignment]
    y_total = data["y_total"]  # type: ignore[assignment]

    gradients = compute_group_gradients(h, y_total, groups, n_groups)
    rng = np.random.default_rng(10_000 + seed)
    bases = {
        "activation_pca": top_eigvecs_sym((h.T @ h) / h.shape[0], common_rank),
        "group_mean": estimate_group_mean(h, groups, n_groups, common_rank),
        "gradient_intersection": estimate_gradient_intersection(gradients, common_rank),
        "feedback_drift": top_eigvecs_sym((drift.T @ drift) / drift.shape[0], common_rank),
        "random_control": sample_basis(rng, d_hidden, common_rank),
    }

    rows = []
    for estimator, basis in bases.items():
        p = projector(basis)
        scores = score_projector(h, p, groups, y_shared, y_rare, y_total, n_groups)
        row: dict[str, float | int | str] = {
            "regime": cfg.name,
            "seed": seed,
            "estimator": estimator,
            "subspace_alignment": subspace_alignment(common_basis, basis),
        }
        row.update(scores)
        rows.append(row)
    return rows


def aggregate(rows: list[dict[str, float | int | str]]) -> tuple[list[dict[str, str | float | int]], dict[str, object]]:
    summary_rows = []
    regimes = sorted({str(row["regime"]) for row in rows})
    winner_records: list[dict[str, str | float | int]] = []

    for regime in regimes:
        regime_rows = [row for row in rows if row["regime"] == regime]
        for criterion in PRIMARY_CRITERIA:
            means = {}
            stds = {}
            seed_winners = []
            for estimator in ESTIMATORS:
                values = np.array([float(row[criterion]) for row in regime_rows if row["estimator"] == estimator])
                means[estimator] = float(values.mean())
                stds[estimator] = float(values.std(ddof=1))

            for seed in sorted({int(row["seed"]) for row in regime_rows}):
                seed_rows = [row for row in regime_rows if int(row["seed"]) == seed]
                seed_winners.append(max(seed_rows, key=lambda row: float(row[criterion]))["estimator"])

            ordered = sorted(means, key=lambda est: means[est], reverse=True)
            winner = ordered[0]
            runner_up = ordered[1]
            winner_fraction = seed_winners.count(winner) / len(seed_winners)
            winner_record = {
                "regime": regime,
                "criterion": criterion,
                "winner": winner,
                "winner_mean": means[winner],
                "winner_std": stds[winner],
                "runner_up": runner_up,
                "runner_up_mean": means[runner_up],
                "winner_seed_fraction": winner_fraction,
            }
            winner_records.append(winner_record)
            summary_rows.append(winner_record)

    distinct_winners = sorted({str(row["winner"]) for row in winner_records})
    diversity = len(distinct_winners)
    meta = {
        "primary_criteria": PRIMARY_CRITERIA,
        "criterion_winner_diversity": diversity,
        "distinct_winners": distinct_winners,
        "winner_records": winner_records,
    }
    return summary_rows, meta


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def plot_subspace_alignment(rows: list[dict[str, object]], out: Path) -> None:
    regimes = [cfg.name for cfg in REGIMES]
    width = 0.16
    x = np.arange(len(regimes))
    fig, ax = plt.subplots(figsize=(12, 5.8))
    for idx, estimator in enumerate(ESTIMATORS):
        means = []
        stds = []
        for regime in regimes:
            values = np.array(
                [
                    float(row["subspace_alignment"])
                    for row in rows
                    if row["regime"] == regime and row["estimator"] == estimator
                ]
            )
            means.append(values.mean())
            stds.append(values.std(ddof=1))
        ax.bar(x + (idx - 2) * width, means, width=width, yerr=stds, label=estimator, capsize=2)
    ax.set_title("Subspace alignment to known common projector")
    ax.set_ylabel("Alignment, 1.0 is exact recovery")
    ax.set_xticks(x)
    ax.set_xticklabels(regimes, rotation=20, ha="right")
    ax.set_ylim(0, 1.05)
    ax.legend(ncol=3, fontsize=9)
    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)


def plot_gradient_reduction(rows: list[dict[str, object]], out: Path) -> None:
    regimes = [cfg.name for cfg in REGIMES]
    width = 0.16
    x = np.arange(len(regimes))
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
        ax.bar(x + (idx - 2) * width, means, width=width, yerr=stds, label=estimator, capsize=2)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Gradient overlap reduction after residualizing candidate common")
    ax.set_ylabel("Pairwise gradient cosine reduction")
    ax.set_xticks(x)
    ax.set_xticklabels(regimes, rotation=20, ha="right")
    ax.legend(ncol=3, fontsize=9)
    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)


def plot_winner_matrix(summary_rows: list[dict[str, object]], out: Path) -> None:
    regimes = [cfg.name for cfg in REGIMES]
    estimator_to_id = {estimator: idx for idx, estimator in enumerate(ESTIMATORS)}
    matrix = np.zeros((len(PRIMARY_CRITERIA), len(regimes)))
    for row in summary_rows:
        i = PRIMARY_CRITERIA.index(str(row["criterion"]))
        j = regimes.index(str(row["regime"]))
        matrix[i, j] = estimator_to_id[str(row["winner"])]

    cmap = plt.get_cmap("tab10", len(ESTIMATORS))
    fig, ax = plt.subplots(figsize=(10.5, 4.2))
    im = ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=-0.5, vmax=len(ESTIMATORS) - 0.5)
    ax.set_title("Criterion winners by regime")
    ax.set_xticks(np.arange(len(regimes)))
    ax.set_xticklabels(regimes, rotation=20, ha="right")
    ax.set_yticks(np.arange(len(PRIMARY_CRITERIA)))
    ax.set_yticklabels(PRIMARY_CRITERIA)
    for i in range(len(PRIMARY_CRITERIA)):
        for j in range(len(regimes)):
            estimator = ESTIMATORS[int(matrix[i, j])]
            ax.text(j, i, estimator.replace("_", "\n"), ha="center", va="center", fontsize=8, color="white")
    cbar = fig.colorbar(im, ax=ax, ticks=np.arange(len(ESTIMATORS)))
    cbar.ax.set_yticklabels(ESTIMATORS)
    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=Path("."))
    parser.add_argument("--d-hidden", type=int, default=16)
    parser.add_argument("--common-rank", type=int, default=2)
    parser.add_argument("--unique-rank", type=int, default=2)
    parser.add_argument("--n-groups", type=int, default=6)
    parser.add_argument("--samples-per-group", type=int, default=600)
    parser.add_argument("--y-dim", type=int, default=3)
    parser.add_argument("--seeds", type=int, nargs="+", default=list(range(10)))
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
                    n_groups=args.n_groups,
                    samples_per_group=args.samples_per_group,
                    y_dim=args.y_dim,
                )
            )

    summary_rows, meta = aggregate(rows)

    write_csv(tables / "operator_criterion_scores.csv", rows)
    write_csv(tables / "operator_regime_summary.csv", summary_rows)
    with (tables / "operator_winner_summary.json").open("w") as f:
        json.dump(meta, f, indent=2)
    with (tables / "run_config.json").open("w") as f:
        json.dump(
            {
                "d_hidden": args.d_hidden,
                "common_rank": args.common_rank,
                "unique_rank": args.unique_rank,
                "n_groups": args.n_groups,
                "samples_per_group": args.samples_per_group,
                "y_dim": args.y_dim,
                "seeds": args.seeds,
                "regimes": [asdict(cfg) for cfg in REGIMES],
                "estimators": ESTIMATORS,
                "primary_criteria": PRIMARY_CRITERIA,
            },
            f,
            indent=2,
        )

    plot_subspace_alignment(rows, figures / "subspace_alignment_by_regime.png")
    plot_gradient_reduction(rows, figures / "gradient_overlap_reduction_by_regime.png")
    plot_winner_matrix(summary_rows, figures / "operator_rank_disagreement.png")

    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()

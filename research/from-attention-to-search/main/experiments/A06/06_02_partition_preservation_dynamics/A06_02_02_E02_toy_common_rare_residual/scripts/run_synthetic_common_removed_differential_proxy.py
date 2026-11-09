#!/usr/bin/env python3
"""Synthetic A06_26a--A06_26g common-removed differential proxy audit."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def normalize(x: np.ndarray, axis: int = -1, eps: float = 1e-12) -> np.ndarray:
    return x / (np.linalg.norm(x, axis=axis, keepdims=True) + eps)


def effective_experts(load: np.ndarray) -> float:
    p = load / max(load.sum(), 1e-12)
    return float(np.exp(-(p[p > 0] * np.log(p[p > 0])).sum()))


def nmi(labels: np.ndarray, routes: np.ndarray, n_labels: int, n_routes: int) -> float:
    mat = np.zeros((n_labels, n_routes), dtype=np.float64)
    for y, r in zip(labels, routes):
        mat[int(y), int(r)] += 1.0
    mat /= mat.sum()
    py = mat.sum(axis=1, keepdims=True)
    pr = mat.sum(axis=0, keepdims=True)
    nz = mat > 0
    mi = float((mat[nz] * np.log(mat[nz] / (py @ pr)[nz])).sum())
    hy = float(-(py[py > 0] * np.log(py[py > 0])).sum())
    hr = float(-(pr[pr > 0] * np.log(pr[pr > 0])).sum())
    return 0.0 if hy <= 0 or hr <= 0 else float(mi / math.sqrt(hy * hr))


def ce_loss(logits: np.ndarray, labels: np.ndarray) -> float:
    shifted = logits - logits.max(axis=1, keepdims=True)
    logp = shifted - np.log(np.exp(shifted).sum(axis=1, keepdims=True))
    return float(-logp[np.arange(labels.size), labels].mean())


def evaluate(
    name: str,
    h: np.ndarray,
    labels: np.ndarray,
    rows: np.ndarray,
    common: np.ndarray,
    rare_dirs: np.ndarray,
    input_projector: np.ndarray | None = None,
    row_projector: np.ndarray | None = None,
    step0_margin: np.ndarray | None = None,
) -> dict:
    x = h if input_projector is None else h @ input_projector.T
    w = rows if row_projector is None else rows @ row_projector.T
    logits = x @ w.T
    routes = logits.argmax(axis=1)
    target_logits = logits[np.arange(labels.size), labels]
    masked = logits.copy()
    masked[np.arange(labels.size), labels] = -np.inf
    margin = target_logits - masked.max(axis=1)
    load = np.bincount(routes, minlength=rows.shape[0]).astype(np.float64)
    load /= load.sum()
    common_overlap = float(np.mean((normalize(w) @ common) ** 2))
    rare_alignment = float(np.mean(np.sum(normalize(w) * rare_dirs, axis=1) ** 2))
    sign_flip = np.nan
    if step0_margin is not None:
        base_positive = step0_margin > 0
        if base_positive.any():
            sign_flip = float((margin[base_positive] <= 0).mean())
    return {
        "condition": name,
        "rare_margin_mean": float(margin.mean()),
        "rare_margin_p05": float(np.quantile(margin, 0.05)),
        "proxy_route_nmi": nmi(labels, routes, rows.shape[0], rows.shape[0]),
        "route_accuracy": float((routes == labels).mean()),
        "max_load": float(load.max()),
        "effective_experts": effective_experts(load),
        "empty_experts": int((load == 0).sum()),
        "common_bias_spread": float(np.var(w @ common)),
        "common_overlap": common_overlap,
        "rare_alignment": rare_alignment,
        "synthetic_loss": ce_loss(logits, labels),
        "selected_utility": float((routes == labels).mean()),
        "sign_flip_rate": sign_flip,
    }


def top_eig(mat: np.ndarray, positive: bool = False) -> np.ndarray:
    vals, vecs = np.linalg.eigh((mat + mat.T) / 2.0)
    if positive:
        idxs = np.where(vals > 1e-9)[0]
        idx = int(idxs[np.argmax(vals[idxs])]) if idxs.size else int(np.argmax(vals))
    else:
        idx = int(np.argmax(vals))
    return normalize(vecs[:, idx])


def build_world(args: argparse.Namespace, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    d, e = args.dim, args.experts
    basis = rng.normal(size=(d, e + 1))
    q, _ = np.linalg.qr(basis)
    common = q[:, 0]
    rare_dirs = q[:, 1 : e + 1].T

    labels = np.repeat(np.arange(e), args.samples_per_group)
    rng.shuffle(labels)
    h = (
        args.common_strength * common[None, :]
        + args.rare_strength * rare_dirs[labels]
        + args.noise_std * rng.normal(size=(labels.size, d))
    )

    mats = []
    for expert in range(e):
        noise = args.matrix_noise * rng.normal(size=(d, d))
        noise = (noise + noise.T) / 2.0
        mat = (
            args.common_gain * np.outer(common, common)
            + args.rare_gain * np.outer(rare_dirs[expert], rare_dirs[expert])
            + noise
        )
        mats.append(mat)
    mats = np.stack(mats)
    return {"rng": rng, "common": common, "rare_dirs": rare_dirs, "labels": labels, "h": h, "mats": mats}


def projectors(h: np.ndarray, common: np.ndarray, rng: np.random.Generator) -> dict[str, np.ndarray]:
    d = h.shape[1]
    eye = np.eye(d)
    mean = normalize(h.mean(axis=0))
    centered = h - h.mean(axis=0, keepdims=True)
    _, _, vh = np.linalg.svd(centered, full_matrices=False)
    top_pc = vh[0]
    perturbed = normalize(0.9 * common + 0.1 * normalize(rng.normal(size=d)))
    return {
        "oracle": eye - np.outer(common, common),
        "mean": eye - np.outer(mean, mean),
        "top_pc": eye - np.outer(top_pc, top_pc),
        "perturbed": eye - np.outer(perturbed, perturbed),
    }


def align_rows_to_synthetic_labels(rows: np.ndarray, rare_dirs: np.ndarray) -> np.ndarray:
    aligned = rows.copy()
    for idx in range(aligned.shape[0]):
        if float(aligned[idx] @ rare_dirs[idx]) < 0:
            aligned[idx] *= -1.0
    return normalize(aligned)


def proxy_rows(mats: np.ndarray, pr: np.ndarray, rare_dirs: np.ndarray, rng: np.random.Generator) -> dict[str, np.ndarray]:
    e, d, _ = mats.shape
    mean_mat = mats.mean(axis=0)
    random_rows = normalize(rng.normal(size=(e, d)))
    raw = align_rows_to_synthetic_labels(np.stack([top_eig(mats[i]) for i in range(e)]), rare_dirs)
    residual = align_rows_to_synthetic_labels(np.stack([top_eig(pr @ mats[i] @ pr) for i in range(e)]), rare_dirs)
    diff = align_rows_to_synthetic_labels(np.stack([top_eig(pr @ (mats[i] - mean_mat) @ pr, positive=True) for i in range(e)]), rare_dirs)
    oracle_rare = residual.copy()
    return {
        "V0_vanilla_random": random_rows,
        "V1_row_norm_random": normalize(random_rows),
        "V3_raw_principal_proxy": normalize(raw),
        "V4_residual_principal_proxy": normalize(residual),
        "V5_differential_residual_proxy": normalize(diff),
        "oracle_rare_proxy": normalize(oracle_rare),
    }


def run_seed(args: argparse.Namespace, seed: int) -> dict[str, pd.DataFrame]:
    w = build_world(args, seed)
    rng = w["rng"]
    h, labels, common, rare_dirs, mats = w["h"], w["labels"], w["common"], w["rare_dirs"], w["mats"]
    projs = projectors(h, common, rng)
    pr = projs["oracle"]
    rows = proxy_rows(mats, pr, rare_dirs, rng)
    eye = np.eye(args.dim)
    centered_input = eye - np.outer(normalize(h.mean(axis=0)), normalize(h.mean(axis=0)))

    step10_bias = np.linspace(-1.0, 1.0, args.experts)[:, None] * common[None, :] * args.common_recapture
    ordinary_rows_t10 = normalize(rows["V5_differential_residual_proxy"] + step10_bias)
    diff_step0 = evaluate("V5_differential_residual_proxy", h, labels, rows["V5_differential_residual_proxy"], common, rare_dirs)
    step0_margin = None
    logits0 = h @ rows["V5_differential_residual_proxy"].T
    masked0 = logits0.copy()
    masked0[np.arange(labels.size), labels] = -np.inf
    step0_margin = logits0[np.arange(labels.size), labels] - masked0.max(axis=1)

    a06_26a = []
    for name, row in rows.items():
        if name == "oracle_rare_proxy":
            continue
        a06_26a.append(evaluate(name, h, labels, row, common, rare_dirs))
    a06_26a.append(evaluate("V2_hidden_mean_subtracted_input", h, labels, rows["V0_vanilla_random"], common, rare_dirs, input_projector=centered_input))
    a06_26a_df = pd.DataFrame(a06_26a).assign(seed=seed, experiment="A06_26a")

    a06_26b = []
    for pname, pmat in projs.items():
        r = proxy_rows(mats, pmat, rare_dirs, rng)["V5_differential_residual_proxy"]
        a06_26b.append(evaluate(f"diff_proxy_P_{pname}", h, labels, r, common, rare_dirs))
    a06_26b_df = pd.DataFrame(a06_26b).assign(seed=seed, experiment="A06_26b")

    a06_26c_df = pd.DataFrame(
        [
            evaluate("raw_principal_proxy", h, labels, rows["V3_raw_principal_proxy"], common, rare_dirs),
            evaluate("differential_residual_proxy", h, labels, rows["V5_differential_residual_proxy"], common, rare_dirs),
        ]
    ).assign(seed=seed, experiment="A06_26c")

    a06_26d_df = pd.DataFrame(
        [
            evaluate("raw_principal_proxy_init", h, labels, rows["V3_raw_principal_proxy"], common, rare_dirs),
            evaluate("residual_principal_proxy_init", h, labels, rows["V4_residual_principal_proxy"], common, rare_dirs),
            evaluate("differential_residual_proxy_init", h, labels, rows["V5_differential_residual_proxy"], common, rare_dirs),
            evaluate("diff_plus_hidden_centered_input", h, labels, rows["V5_differential_residual_proxy"], common, rare_dirs, input_projector=centered_input),
            evaluate("diff_plus_oracle_residual_input", h, labels, rows["V5_differential_residual_proxy"], common, rare_dirs, input_projector=pr),
        ]
    ).assign(seed=seed, experiment="A06_26d")

    a06_26e = [
        evaluate("positive_no_recapture_control", h, labels, rows["V5_differential_residual_proxy"], common, rare_dirs, step0_margin=step0_margin),
        evaluate("init_only_ordinary_common_recapture", h, labels, ordinary_rows_t10, common, rare_dirs, step0_margin=step0_margin),
        evaluate("residual_input_during_steps_0_10", h, labels, ordinary_rows_t10, common, rare_dirs, input_projector=pr, step0_margin=step0_margin),
        evaluate("row_projection_after_update", h, labels, ordinary_rows_t10, common, rare_dirs, row_projector=pr, step0_margin=step0_margin),
        evaluate("symmetric_residual_router", h, labels, ordinary_rows_t10, common, rare_dirs, input_projector=pr, row_projector=pr, step0_margin=step0_margin),
    ]
    a06_26e_df = pd.DataFrame(a06_26e).assign(seed=seed, experiment="A06_26e")

    a06_26f_df = pd.DataFrame(
        [
            evaluate("load_only_hidden_centered", h, labels, rows["V0_vanilla_random"], common, rare_dirs, input_projector=centered_input),
            evaluate("raw_principal_proxy", h, labels, rows["V3_raw_principal_proxy"], common, rare_dirs),
            evaluate("preserved_differential_residual_proxy", h, labels, ordinary_rows_t10, common, rare_dirs, input_projector=pr),
        ]
    ).assign(seed=seed, experiment="A06_26f")

    base = rows["V5_differential_residual_proxy"]
    common_update = step10_bias
    rare_update = 0.20 * rare_dirs
    lr_conditions = {
        "ordinary_equal_lr": (1.0, 1.0),
        "scheme1_common_small_rare_base": (0.25, 1.0),
        "scheme1_common_zero_rare_base": (0.0, 1.0),
        "scheme2_common_small_rare_2x": (0.25, 2.0),
        "scheme2_common_small_rare_4x": (0.25, 4.0),
        "scheme2_common_zero_rare_2x": (0.0, 2.0),
        "scheme2_common_zero_rare_4x": (0.0, 4.0),
        "rare_2x_without_common_control": (1.0, 2.0),
    }
    a06_26g = []
    for name, (common_lr, rare_lr) in lr_conditions.items():
        row = normalize(base + common_lr * common_update + rare_lr * rare_update)
        a06_26g.append(evaluate(name, h, labels, row, common, rare_dirs, step0_margin=step0_margin))
        if "scheme2_common_small_rare_4x" == name:
            a06_26g.append(
                evaluate(
                    f"{name}_residual_input",
                    h,
                    labels,
                    row,
                    common,
                    rare_dirs,
                    input_projector=pr,
                    step0_margin=step0_margin,
                )
            )
            a06_26g.append(
                evaluate(
                    f"{name}_row_projected",
                    h,
                    labels,
                    row,
                    common,
                    rare_dirs,
                    row_projector=pr,
                    step0_margin=step0_margin,
                )
            )
    a06_26g_df = pd.DataFrame(a06_26g).assign(seed=seed, experiment="A06_26g")

    return {
        "A06_26a": a06_26a_df,
        "A06_26b": a06_26b_df,
        "A06_26c": a06_26c_df,
        "A06_26d": a06_26d_df,
        "A06_26e": a06_26e_df,
        "A06_26f": a06_26f_df,
        "A06_26g": a06_26g_df,
    }


def plot_metric(df: pd.DataFrame, metric: str, title: str, out: Path) -> None:
    agg = df.groupby("condition")[metric].mean().sort_values()
    fig, ax = plt.subplots(figsize=(10, max(4, 0.32 * len(agg))))
    agg.plot(kind="barh", ax=ax, color="#357ABD")
    ax.set_title(title)
    ax.set_xlabel(metric)
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--dim", type=int, default=64)
    parser.add_argument("--experts", type=int, default=4)
    parser.add_argument("--samples-per-group", type=int, default=2048)
    parser.add_argument("--seeds", type=int, default=8)
    parser.add_argument("--common-strength", type=float, default=4.0)
    parser.add_argument("--rare-strength", type=float, default=1.6)
    parser.add_argument("--noise-std", type=float, default=0.25)
    parser.add_argument("--common-gain", type=float, default=8.0)
    parser.add_argument("--rare-gain", type=float, default=3.0)
    parser.add_argument("--matrix-noise", type=float, default=0.01)
    parser.add_argument("--common-recapture", type=float, default=3.5)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    tables = args.out_dir / "tables"
    figures = args.out_dir / "figures"
    logs = args.out_dir / "logs"
    tables.mkdir(exist_ok=True)
    figures.mkdir(exist_ok=True)
    logs.mkdir(exist_ok=True)

    all_parts: dict[str, list[pd.DataFrame]] = {f"A06_26{suffix}": [] for suffix in "abcdefg"}
    for seed in range(args.seeds):
        seed_parts = run_seed(args, seed)
        for name, df in seed_parts.items():
            all_parts[name].append(df)

    summary_rows = []
    for name, frames in all_parts.items():
        df = pd.concat(frames, ignore_index=True)
        df.to_csv(tables / f"{name.lower()}_metrics.csv", index=False)
        agg = df.groupby("condition").agg(["mean", "std"])
        agg.to_csv(tables / f"{name.lower()}_aggregate.csv")
        for condition, sub in df.groupby("condition"):
            summary_rows.append(
                {
                    "experiment": name,
                    "condition": condition,
                    "rare_margin_mean": float(sub["rare_margin_mean"].mean()),
                    "rare_margin_p05": float(sub["rare_margin_p05"].mean()),
                    "proxy_route_nmi": float(sub["proxy_route_nmi"].mean()),
                    "route_accuracy": float(sub["route_accuracy"].mean()),
                    "sign_flip_rate": float(sub["sign_flip_rate"].mean(skipna=True)),
                    "synthetic_loss": float(sub["synthetic_loss"].mean()),
                    "max_load": float(sub["max_load"].mean()),
                    "effective_experts": float(sub["effective_experts"].mean()),
                    "common_overlap": float(sub["common_overlap"].mean()),
                    "rare_alignment": float(sub["rare_alignment"].mean()),
                    "selected_utility": float(sub["selected_utility"].mean()),
                }
            )

    summary = pd.DataFrame(summary_rows)
    summary.to_csv(tables / "all_experiment_summary.csv", index=False)

    for exp, metric in [
        ("A06_26a", "rare_margin_mean"),
        ("A06_26b", "rare_margin_mean"),
        ("A06_26c", "common_overlap"),
        ("A06_26d", "rare_margin_mean"),
        ("A06_26e", "sign_flip_rate"),
        ("A06_26f", "selected_utility"),
        ("A06_26g", "rare_margin_mean"),
    ]:
        plot_metric(
            summary[summary["experiment"] == exp],
            metric,
            f"{exp} {metric}",
            figures / f"{exp.lower()}_{metric}.png",
        )

    metadata = {
        "config": vars(args) | {"out_dir": str(args.out_dir)},
        "experiments": list(all_parts.keys()),
        "primary_summary": str(tables / "all_experiment_summary.csv"),
    }
    (args.out_dir / "summary.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()

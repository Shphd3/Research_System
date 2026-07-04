#!/usr/bin/env python3
"""Run E1 and E2: static dispatch audits."""

from __future__ import annotations

import argparse

import pandas as pd

from src.registry import describe
from src.synthetic_suite import (
    aggregate,
    barplot,
    build_router,
    covariance_stats,
    evaluate_router,
    make_expert_weights,
    prototype_set,
    rng,
    sample_axis_jitter,
    sample_gaussian,
    sample_paired_dirs,
    sample_sparse_mixture,
    sample_spherical,
    save_figure,
    svd_prototypes,
    unit_rows,
    center_whiten_apply,
    center_whiten_fit,
    write_metrics,
    write_summary,
)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Static dispatch experiments for SPR v2.")
    p.add_argument("--describe", action="store_true")
    p.add_argument("--quick", action="store_true", help="Run a smoke-test subset.")
    p.add_argument(
        "--experiments",
        default="E1,E2",
        help="Comma-separated subset from E1,E2. Default runs both.",
    )
    return p


def stable_seed(*vals: int) -> int:
    out = 1729
    for val in vals:
        out = (out * 1000003 + int(val) * 9176) % (2**32 - 1)
    return out


def e1_configs(quick: bool) -> tuple[list[int], list[int], list[int], list[int], int]:
    if quick:
        return [0], [16], [4], [512], 1024
    return list(range(5)), [32, 64], [4, 8], [2048, 8192, 16384], 8192


def e2_configs(quick: bool) -> tuple[list[int], list[int], list[int], int, int]:
    if quick:
        return [0], [32], [4], 1024, 1024
    return list(range(5)), [64], [4, 8], 8192, 8192


def run_e1(quick: bool) -> pd.DataFrame:
    methods = ["vanilla", "simplex", "spr_fixed", "spr_local", "spr_expert", "balanced"]
    seeds, dims, experts, n_cals, n_holdout = e1_configs(quick)
    rows: list[dict[str, object]] = []
    datasets = {
        "Gaussian": sample_gaussian,
        "Spherical": sample_spherical,
    }
    for seed in seeds:
        for dataset_name, sampler in datasets.items():
            for d in dims:
                for e in experts:
                    for n_cal in n_cals:
                        base = rng(stable_seed(seed, d, e, n_cal, len(dataset_name)))
                        x_cal = sampler(base, n_cal, d)
                        x_hold = sampler(base, n_holdout, d)
                        true_proto, _ = prototype_set("symmetric", e, d, base)
                        weights = make_expert_weights(base, true_proto)
                        proto = svd_prototypes(weights)
                        for method in methods:
                            mr = rng(stable_seed(seed, d, e, n_cal, len(method)))
                            router = build_router(
                                method,
                                x_cal,
                                e,
                                mr,
                                prototypes=proto,
                                n_candidates=6,
                            )
                            record = evaluate_router(method, router, x_cal, x_hold, e)
                            record.update(
                                {
                                    "exp_id": "E1",
                                    "seed": seed,
                                    "dataset": dataset_name,
                                    "d": d,
                                    "E": e,
                                    "n_cal": n_cal,
                                    "n_holdout": n_holdout,
                                    "run_mode": "quick" if quick else "full",
                                }
                            )
                            rows.append(record)
    df = write_metrics(rows, "E1")
    plot_e1(df)
    summarize_e1(df)
    return df


def run_e2(quick: bool) -> pd.DataFrame:
    methods = ["vanilla", "simplex", "spr_fixed", "spr_local", "spr_expert", "balanced"]
    seeds, dims, experts, n_cal, n_holdout = e2_configs(quick)
    samplers = {
        "Axis-jitter": sample_axis_jitter,
        "Sparse-mixture": sample_sparse_mixture,
        "Paired-directions": sample_paired_dirs,
    }
    rows: list[dict[str, object]] = []
    for seed in seeds:
        for dataset_name, sampler in samplers.items():
            for d in dims:
                for e in experts:
                    base = rng(stable_seed(seed, d, e, len(dataset_name)))
                    raw_cal = sampler(base, n_cal, d)
                    raw_hold = sampler(base, n_holdout, d)
                    mu, mat = center_whiten_fit(raw_cal)
                    x_cal = center_whiten_apply(raw_cal, mu, mat)
                    x_hold = center_whiten_apply(raw_hold, mu, mat)
                    cond, eff_rank = covariance_stats(x_cal)
                    true_proto, _ = prototype_set("symmetric", e, d, base)
                    weights = make_expert_weights(base, true_proto)
                    proto = svd_prototypes(weights)
                    for method in methods:
                        mr = rng(stable_seed(seed, d, e, len(method), len(dataset_name)))
                        router = build_router(
                            method,
                            x_cal,
                            e,
                            mr,
                            prototypes=proto,
                            n_candidates=6,
                        )
                        record = evaluate_router(method, router, x_cal, x_hold, e)
                        record.update(
                            {
                                "exp_id": "E2",
                                "seed": seed,
                                "dataset": dataset_name,
                                "d": d,
                                "E": e,
                                "n_cal": n_cal,
                                "n_holdout": n_holdout,
                                "cov_condition": cond,
                                "effective_rank": eff_rank,
                                "run_mode": "quick" if quick else "full",
                            }
                        )
                        rows.append(record)
    df = write_metrics(rows, "E2")
    plot_e2(df)
    summarize_e2(df)
    return df


def plot_e1(df: pd.DataFrame) -> None:
    sub = df[(df["E"] == 8) & (df["d"] == 64)]
    if sub.empty:
        sub = df
    barplot(
        sub,
        "method_label",
        "holdout_loadcv",
        "dataset",
        "E1: held-out load imbalance by router",
        "Holdout LoadCV",
        "e1_loadcv_by_method.pdf",
        "E1",
    )
    gap = (
        df[df["method"].isin(["spr_fixed", "spr_local", "spr_expert"])]
        .groupby(["n_cal", "method_label"], as_index=False)["holdout_gap"]
        .mean()
    )
    from src.synthetic_suite import lineplot

    lineplot(
        gap,
        "n_cal",
        "holdout_gap",
        "method_label",
        "E1: calibration-to-holdout gap shrinks with calibration size",
        "Absolute LoadCV gap",
        "e1_holdout_gap.pdf",
        "E1",
    )


def plot_e2(df: pd.DataFrame) -> None:
    sub = df[df["E"] == 8]
    if sub.empty:
        sub = df
    barplot(
        sub,
        "method_label",
        "holdout_loadcv",
        "dataset",
        "E2: covariance-flat non-spherical data",
        "Holdout LoadCV",
        "e2_non_spherical_loadcv.pdf",
        "E2",
    )
    fig_df = (
        df.groupby(["dataset", "method_label"], as_index=False)
        .agg(cov_condition=("cov_condition", "mean"), holdout_loadcv=("holdout_loadcv", "mean"))
    )
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    for method, subm in fig_df.groupby("method_label"):
        ax.scatter(subm["cov_condition"], subm["holdout_loadcv"], label=method, s=36)
    ax.set_xlabel("Covariance condition number")
    ax.set_ylabel("Holdout LoadCV")
    ax.set_title("E2: flat covariance does not imply balanced prototype cells")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, fontsize=7, ncol=2)
    fig.tight_layout()
    save_figure(fig, "E2", "e2_covariance_vs_load.pdf")


def summarize_e1(df: pd.DataFrame) -> None:
    agg = aggregate(
        df,
        ["method_label"],
        ["cal_loadcv", "holdout_loadcv", "holdout_max_abs_error", "holdout_margin_p05"],
    )
    best_spr = agg[agg["method_label"].str.startswith("SPR")]["holdout_loadcv_mean"].min()
    vanilla = float(agg.loc[agg["method_label"] == "Vanilla linear", "holdout_loadcv_mean"].iloc[0])
    bullets = [
        f"Across the full E1 sweep, the best SPR mean held-out LoadCV is {best_spr:.4f}, versus {vanilla:.4f} for vanilla random linear routing.",
        "Balanced assignment is included only as a forced-count control; its exact batch balance is not a feature-only routing guarantee.",
        "The gap plot records the statistical calibration effect: quantile routers improve as node quantiles receive more calibration samples.",
    ]
    write_summary("E1", "Static uniform dispatch", bullets, df)


def summarize_e2(df: pd.DataFrame) -> None:
    agg = aggregate(df, ["method_label"], ["holdout_loadcv", "holdout_max_abs_error"])
    best_spr = agg[agg["method_label"].str.startswith("SPR")]["holdout_loadcv_mean"].min()
    simplex = float(agg.loc[agg["method_label"] == "Simplex prototype", "holdout_loadcv_mean"].iloc[0])
    cond = float(df["cov_condition"].mean())
    bullets = [
        f"Whitened non-spherical datasets have mean covariance condition number {cond:.3f}, but prototype-only routing still reaches mean held-out LoadCV {simplex:.4f}.",
        f"SPR's best mean held-out LoadCV is {best_spr:.4f}, showing that quantile calibration, not covariance flatness alone, controls mass.",
        "Axis-supported data remains a useful boundary case because deterministic feature routers cannot split truly identical atoms without tie-breaking.",
    ]
    write_summary("E2", "Spectrally flat but non-spherical features", bullets, df)


def main() -> None:
    args = parser().parse_args()
    selected = {item.strip() for item in args.experiments.split(",") if item.strip()}
    if args.describe:
        for exp_id in ("E1", "E2"):
            if exp_id in selected:
                print(describe(exp_id))
                print()
        return
    if "E1" in selected:
        run_e1(args.quick)
    if "E2" in selected:
        run_e2(args.quick)


if __name__ == "__main__":
    main()

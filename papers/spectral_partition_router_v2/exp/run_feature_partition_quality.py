#!/usr/bin/env python3
"""Run E4: feature partition quality audits."""

from __future__ import annotations

import argparse

import pandas as pd

from src.registry import describe
from src.synthetic_suite import (
    aggregate,
    barplot,
    build_router,
    center_whiten_apply,
    center_whiten_fit,
    evaluate_router,
    make_expert_weights,
    make_latent_features,
    prototype_set,
    rng,
    svd_prototypes,
    write_metrics,
    write_summary,
)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Feature partition quality experiments.")
    p.add_argument("--describe", action="store_true")
    p.add_argument("--quick", action="store_true")
    return p


def stable_seed(*vals: int) -> int:
    out = 4547
    for val in vals:
        out = (out * 999983 + int(val) * 8191) % (2**32 - 1)
    return out


def configs(quick: bool) -> tuple[list[int], int, int, int, int, list[tuple[str, float, float]]]:
    if quick:
        return [0], 32, 4, 2048, 2048, [("medium", 2.0, 0.7)]
    return (
        list(range(5)),
        64,
        8,
        32768,
        32768,
        [("weak", 1.35, 0.9), ("medium", 2.0, 0.7), ("strong", 2.8, 0.55)],
    )


def run(quick: bool) -> pd.DataFrame:
    seeds, d, e, n_cal, n_hold, regimes = configs(quick)
    methods = ["vanilla", "simplex", "spr_fixed", "spr_local", "spr_expert", "balanced"]
    rows: list[dict[str, object]] = []
    for seed in seeds:
        for regime_idx, (regime, sep, noise) in enumerate(regimes):
            r = rng(stable_seed(seed, regime_idx, d, e))
            class_dirs, _ = prototype_set("symmetric", e, d, r)
            raw_cal, _, _ = make_latent_features(r, n_cal, d, e, sep, noise, class_dirs)
            raw_hold, labels_hold, _ = make_latent_features(r, n_hold, d, e, sep, noise, class_dirs)
            mu, mat = center_whiten_fit(raw_cal)
            x_cal = center_whiten_apply(raw_cal, mu, mat)
            x_hold = center_whiten_apply(raw_hold, mu, mat)
            weights = make_expert_weights(r, class_dirs, signal=3.4, noise=0.22)
            proto = svd_prototypes(weights)
            for method in methods:
                mr = rng(stable_seed(seed, regime_idx, len(method)))
                router = build_router(
                    method,
                    x_cal,
                    e,
                    mr,
                    prototypes=proto,
                    n_candidates=8 if quick else 32,
                )
                record = evaluate_router(
                    method,
                    router,
                    x_cal,
                    x_hold,
                    e,
                    labels_hold=labels_hold,
                    prototypes=proto,
                )
                record.update(
                    {
                        "exp_id": "E4",
                        "seed": seed,
                        "regime": regime,
                        "separation": sep,
                        "noise": noise,
                        "d": d,
                        "E": e,
                        "n_cal": n_cal,
                        "n_holdout": n_hold,
                        "run_mode": "quick" if quick else "full",
                    }
                )
                rows.append(record)
    df = write_metrics(rows, "E4")
    plot(df)
    summarize(df)
    return df


def plot(df: pd.DataFrame) -> None:
    sub = df[df["regime"] == "medium"]
    plot_df = sub.melt(
        id_vars=["method_label", "seed"],
        value_vars=["route_feature_nmi", "feature_purity"],
        var_name="metric",
        value_name="value",
    )
    barplot(
        plot_df,
        "method_label",
        "value",
        "metric",
        "E4: feature-structure recovery on held-out data",
        "Score",
        "e4_nmi_purity.pdf",
        "E4",
    )
    barplot(
        sub,
        "method_label",
        "within_cell_var",
        None,
        "E4: within-cell variance",
        "Within-cell variance",
        "e4_within_cell_variance.pdf",
        "E4",
    )


def summarize(df: pd.DataFrame) -> None:
    agg = aggregate(
        df[df["regime"] == "medium"],
        ["method_label"],
        ["holdout_loadcv", "route_feature_nmi", "feature_purity", "within_cell_var"],
    )
    local_nmi = float(agg.loc[agg["method_label"] == "SPR-Local", "route_feature_nmi_mean"].iloc[0])
    fixed_nmi = float(agg.loc[agg["method_label"] == "SPR-Fixed", "route_feature_nmi_mean"].iloc[0])
    balanced_nmi = float(agg.loc[agg["method_label"] == "Balanced assignment", "route_feature_nmi_mean"].iloc[0])
    bullets = [
        f"On the medium latent-feature regime, SPR-Local reaches mean route-feature NMI {local_nmi:.4f}, compared with {fixed_nmi:.4f} for SPR-Fixed.",
        f"Balanced assignment has exact count control but only NMI {balanced_nmi:.4f}, so count balance alone is not feature partition quality.",
        "Within-cell variance provides the geometry-side audit: lower variance means the route cell is less arbitrary inside the whitened feature space.",
    ]
    write_summary("E4", "Feature partition quality", bullets, df)


def main() -> None:
    args = parser().parse_args()
    if args.describe:
        print(describe("E4"))
        return
    run(args.quick)


if __name__ == "__main__":
    main()

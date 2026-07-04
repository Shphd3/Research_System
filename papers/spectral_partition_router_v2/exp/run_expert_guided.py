#!/usr/bin/env python3
"""Run E3: expert-weight-guided partitioning."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
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
    mpi_prototypes,
    prototype_set,
    prototype_spread,
    rng,
    sample_gaussian,
    save_figure,
    svd_prototypes,
    unit_rows,
    write_metrics,
    write_summary,
)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Expert-guided SPR experiments.")
    p.add_argument("--describe", action="store_true")
    p.add_argument("--quick", action="store_true")
    return p


def stable_seed(*vals: int) -> int:
    out = 3571
    for val in vals:
        out = (out * 1000003 + int(val) * 65537) % (2**32 - 1)
    return out


def configs(quick: bool) -> tuple[list[int], int, int, int, int]:
    if quick:
        return [0], 32, 4, 2048, 2048
    return list(range(5)), 64, 8, 32768, 32768


def signed_alignment(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean(np.max(np.abs(unit_rows(a) @ unit_rows(b).T), axis=1)))


def run(quick: bool) -> pd.DataFrame:
    seeds, d, e, n_cal, n_hold = configs(quick)
    init_kinds = ["random", "symmetric", "clustered"]
    methods = ["proto_svd", "proto_mpi", "spr_expert", "spr_expert_mpi", "spr_fixed", "spr_local"]
    rows: list[dict[str, object]] = []
    for seed in seeds:
        for init_idx, init_kind in enumerate(init_kinds):
            r = rng(stable_seed(seed, init_idx, d, e))
            true_proto, group_labels = prototype_set(init_kind, e, d, r)
            weights = make_expert_weights(
                r,
                true_proto,
                signal=3.5 if init_kind != "random" else 1.2,
                noise=0.18 if init_kind != "random" else 0.65,
            )
            svd_proto = svd_prototypes(weights)
            mpi_proto = mpi_prototypes(weights, rng(stable_seed(seed, init_idx, 99)), steps=1)
            if init_kind == "random":
                x_cal = sample_gaussian(r, n_cal, d)
                x_hold = sample_gaussian(r, n_hold, d)
            else:
                raw_cal, _, _ = make_latent_features(
                    r, n_cal, d, e, separation=2.0, noise=0.75, directions=true_proto
                )
                raw_hold, _, _ = make_latent_features(
                    r, n_hold, d, e, separation=2.0, noise=0.75, directions=true_proto
                )
                mu, mat = center_whiten_fit(raw_cal)
                x_cal = center_whiten_apply(raw_cal, mu, mat)
                x_hold = center_whiten_apply(raw_hold, mu, mat)
            for method in methods:
                mr = rng(stable_seed(seed, init_idx, len(method)))
                router = build_router(
                    method,
                    x_cal,
                    e,
                    mr,
                    prototypes=svd_proto,
                    mpi_proto=mpi_proto,
                    n_candidates=8 if quick else 24,
                )
                proto_used = mpi_proto if "mpi" in method else svd_proto
                record = evaluate_router(method, router, x_cal, x_hold, e, prototypes=proto_used)
                record.update(
                    {
                        "exp_id": "E3",
                        "seed": seed,
                        "expert_init": init_kind,
                        "d": d,
                        "E": e,
                        "n_cal": n_cal,
                        "n_holdout": n_hold,
                        "prototype_spread": prototype_spread(svd_proto),
                        "mpi_prototype_spread": prototype_spread(mpi_proto),
                        "svd_true_alignment": signed_alignment(svd_proto, true_proto),
                        "mpi_true_alignment": signed_alignment(mpi_proto, true_proto),
                        "has_group_labels": group_labels is not None,
                        "run_mode": "quick" if quick else "full",
                    }
                )
                rows.append(record)
    df = write_metrics(rows, "E3")
    plot(df)
    summarize(df)
    return df


def plot(df: pd.DataFrame) -> None:
    spread = df.drop_duplicates(["seed", "expert_init"])[
        ["expert_init", "prototype_spread", "mpi_prototype_spread"]
    ].melt("expert_init", var_name="source", value_name="spread")
    barplot(
        spread,
        "expert_init",
        "spread",
        "source",
        "E3: spread of expert spectral prototypes",
        "Spread score",
        "e3_prototype_spread.pdf",
        "E3",
        rotate=0,
    )
    fig, ax = plt.subplots(figsize=(6.4, 4.1))
    for method, sub in df.groupby("method_label"):
        ax.scatter(sub["cell_proto_alignment"], sub["holdout_loadcv"], label=method, s=28, alpha=0.75)
    ax.set_xlabel("Cell-to-prototype alignment")
    ax.set_ylabel("Holdout LoadCV")
    ax.set_title("E3: expert alignment and dispatch balance are separate")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, fontsize=7, ncol=2)
    fig.tight_layout()
    save_figure(fig, "E3", "e3_alignment_vs_loadcv.pdf")


def summarize(df: pd.DataFrame) -> None:
    agg = aggregate(df, ["method_label"], ["holdout_loadcv", "cell_proto_alignment", "holdout_margin_p05"])
    spr = float(agg.loc[agg["method_label"] == "SPR-Expert", "holdout_loadcv_mean"].iloc[0])
    proto = float(agg.loc[agg["method_label"] == "Expert-SVD top-1", "holdout_loadcv_mean"].iloc[0])
    align = float(agg.loc[agg["method_label"] == "SPR-Expert", "cell_proto_alignment_mean"].iloc[0])
    bullets = [
        f"SPR-Expert obtains mean held-out LoadCV {spr:.4f}, while prototype-only top-1 routing obtains {proto:.4f}.",
        f"Mean SPR-Expert cell-to-prototype alignment is {align:.4f}; expert weights provide geometry but not the mass guarantee.",
        "The alignment-vs-load plot separates the two effects: aligned prototype cells can still be imbalanced without quantile thresholds.",
    ]
    write_summary("E3", "Expert-weight-guided partitioning", bullets, df)


def main() -> None:
    args = parser().parse_args()
    if args.describe:
        print(describe("E3"))
        return
    run(args.quick)


if __name__ == "__main__":
    main()

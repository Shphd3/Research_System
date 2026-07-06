#!/usr/bin/env python3
"""Run the V2.2 static feature-level dispatch experiments E1--E5."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.static_bfsr_suite import (
    FIGURES,
    METHOD_LABELS,
    RESULTS,
    TABLES,
    BFSRClusterRouter,
    OracleFeatureRouter,
    QuantileSPRRouter,
    RandomLinearRouter,
    aggregate,
    covariance_diagnostics,
    distorted_dataset,
    evaluate_cluster_recovery,
    evaluate_routes,
    fit_normalizer,
    format_float,
    imbalanced_probs,
    make_feature_mixture,
    make_isotropic_null,
    plot_e3,
    plot_e4,
    plot_e5,
    save_csv,
    write_latex_table,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="Run a smaller smoke-test configuration.")
    return parser.parse_args()


def config(quick: bool) -> dict[str, object]:
    if quick:
        return {
            "seeds": [0, 1],
            "n_cal": 1800,
            "n_hold": 3600,
            "d": 16,
            "k": 32,
            "e": 4,
        }
    return {
        "seeds": [0, 1, 2, 3, 4],
        "n_cal": 8000,
        "n_hold": 16000,
        "d": 16,
        "k": 32,
        "e": 4,
    }


def add_diagnostic(rows: list[dict[str, object]], name: str, x, f, k: int, normalizer: str = "raw") -> None:
    if normalizer == "whiten":
        z = fit_normalizer(x, "whiten").apply(x)
    elif normalizer == "center":
        z = fit_normalizer(x, "center").apply(x)
    else:
        z = x
    diag = covariance_diagnostics(z)
    counts = pd.Series(f).value_counts(normalize=True)
    diag.update(
        {
            "dataset": name,
            "normalizer": normalizer,
            "freq_max_min_gap": float(counts.max() - counts.min()),
            "n_families": k,
        }
    )
    rows.append(diag)


def route_all_methods(ds, cfg: dict[str, object], exp_id: str, seed: int) -> list[dict[str, object]]:
    d, k, e = int(cfg["d"]), int(cfg["k"]), int(cfg["e"])
    rows: list[dict[str, object]] = []

    oracle = OracleFeatureRouter(k, e, assignment="equal").fit(ds.f_cal)
    rows.append(
        evaluate_routes(
            exp_id,
            ds.name,
            "oracle_equal",
            seed,
            oracle.predict_from_labels(ds.f_hold),
            ds.f_hold,
            k,
            e,
            {"invalid_oracle": 1.0},
        )
    )

    bfsr = BFSRClusterRouter(k, e, normalizer_mode="whiten", assignment="equal", seed=seed).fit(ds.x_cal)
    extra = evaluate_cluster_recovery(bfsr, ds.x_hold, ds.f_hold)
    rows.append(
        evaluate_routes(
            exp_id,
            ds.name,
            "bfsr_cluster_equal",
            seed,
            bfsr.predict(ds.x_hold),
            ds.f_hold,
            k,
            e,
            extra,
        )
    )

    quantile = QuantileSPRRouter(e, normalizer_mode="whiten", seed=seed + 17).fit(ds.x_cal)
    rows.append(
        evaluate_routes(exp_id, ds.name, "quantile_spr", seed, quantile.predict(ds.x_hold), ds.f_hold, k, e)
    )

    random_linear = RandomLinearRouter(e, d, normalizer_mode="whiten", seed=seed + 31).fit(ds.x_cal)
    rows.append(
        evaluate_routes(
            exp_id,
            ds.name,
            "random_linear",
            seed,
            random_linear.predict(ds.x_hold),
            ds.f_hold,
            k,
            e,
        )
    )
    return rows


def run_e1(cfg: dict[str, object], diagnostics: list[dict[str, object]]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for seed in cfg["seeds"]:
        ds = make_feature_mixture(
            int(cfg["n_cal"]),
            int(cfg["n_hold"]),
            int(cfg["d"]),
            int(cfg["k"]),
            separation=2.5,
            noise=0.55,
            seed=1000 + int(seed),
        )
        add_diagnostic(diagnostics, "E1 clean mixture", ds.x_cal, ds.f_cal, int(cfg["k"]), "raw")
        add_diagnostic(diagnostics, "E1 clean mixture", ds.x_cal, ds.f_cal, int(cfg["k"]), "whiten")
        rows.extend(route_all_methods(ds, cfg, "E1", int(seed)))
    return pd.DataFrame(rows)


def run_e2(cfg: dict[str, object], diagnostics: list[dict[str, object]]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for seed in cfg["seeds"]:
        ds = make_isotropic_null(
            int(cfg["n_cal"]), int(cfg["n_hold"]), int(cfg["d"]), int(cfg["k"]), seed=2000 + int(seed)
        )
        add_diagnostic(diagnostics, "E2 isotropic null", ds.x_cal, ds.f_cal, int(cfg["k"]), "raw")
        rows.extend(route_all_methods(ds, cfg, "E2", int(seed)))
    return pd.DataFrame(rows)


def run_e3(cfg: dict[str, object], diagnostics: list[dict[str, object]]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    separations = [0.45, 0.75, 1.10, 1.60, 2.50]
    k, e = int(cfg["k"]), int(cfg["e"])
    for separation in separations:
        for seed in cfg["seeds"]:
            ds = make_feature_mixture(
                int(cfg["n_cal"]),
                int(cfg["n_hold"]),
                int(cfg["d"]),
                k,
                separation=separation,
                noise=0.65,
                seed=3000 + int(seed) + int(100 * separation),
            )
            if seed == cfg["seeds"][0]:
                add_diagnostic(diagnostics, f"E3 sep={separation}", ds.x_cal, ds.f_cal, k, "raw")
                add_diagnostic(diagnostics, f"E3 sep={separation}", ds.x_cal, ds.f_cal, k, "whiten")
            bfsr = BFSRClusterRouter(k, e, normalizer_mode="whiten", assignment="equal", seed=int(seed)).fit(
                ds.x_cal
            )
            extra = evaluate_cluster_recovery(bfsr, ds.x_hold, ds.f_hold)
            extra["separation"] = separation
            rows.append(
                evaluate_routes(
                    "E3",
                    ds.name,
                    "bfsr_cluster_equal",
                    int(seed),
                    bfsr.predict(ds.x_hold),
                    ds.f_hold,
                    k,
                    e,
                    extra,
                )
            )
    return pd.DataFrame(rows)


def run_e4(cfg: dict[str, object], diagnostics: list[dict[str, object]]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    k, e = int(cfg["k"]), int(cfg["e"])
    for seed in cfg["seeds"]:
        structured = make_feature_mixture(
            int(cfg["n_cal"]),
            int(cfg["n_hold"]),
            int(cfg["d"]),
            k,
            separation=2.2,
            noise=0.55,
            seed=4000 + int(seed),
        )
        null = make_isotropic_null(
            int(cfg["n_cal"]), int(cfg["n_hold"]), int(cfg["d"]), k, seed=4100 + int(seed)
        )
        datasets = [
            distorted_dataset(structured, 80.0, 4200 + int(seed), "structured_distorted"),
            distorted_dataset(null, 80.0, 4300 + int(seed), "null_distorted"),
        ]
        for ds in datasets:
            if seed == cfg["seeds"][0]:
                add_diagnostic(diagnostics, f"E4 {ds.name}", ds.x_cal, ds.f_cal, k, "raw")
                add_diagnostic(diagnostics, f"E4 {ds.name}", ds.x_cal, ds.f_cal, k, "whiten")
            for normalizer in ["raw", "whiten"]:
                bfsr = BFSRClusterRouter(k, e, normalizer_mode=normalizer, assignment="equal", seed=int(seed)).fit(
                    ds.x_cal
                )
                extra = evaluate_cluster_recovery(bfsr, ds.x_hold, ds.f_hold)
                extra["normalizer"] = normalizer
                rows.append(
                    evaluate_routes(
                        "E4",
                        ds.name,
                        "bfsr_cluster_equal",
                        int(seed),
                        bfsr.predict(ds.x_hold),
                        ds.f_hold,
                        k,
                        e,
                        extra,
                    )
                )
    return pd.DataFrame(rows)


def run_e5(cfg: dict[str, object], diagnostics: list[dict[str, object]]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    k, e = int(cfg["k"]), int(cfg["e"])
    probs = imbalanced_probs(k, strength=1.25)
    for seed in cfg["seeds"]:
        ds = make_feature_mixture(
            int(cfg["n_cal"]),
            int(cfg["n_hold"]),
            int(cfg["d"]),
            k,
            separation=2.5,
            noise=0.55,
            seed=5000 + int(seed),
            probs=probs,
        )
        if seed == cfg["seeds"][0]:
            add_diagnostic(diagnostics, "E5 frequency-imbalanced", ds.x_cal, ds.f_cal, k, "raw")
            add_diagnostic(diagnostics, "E5 frequency-imbalanced", ds.x_cal, ds.f_cal, k, "whiten")

        for method, assignment in [("oracle_equal", "equal"), ("oracle_mass", "mass")]:
            oracle = OracleFeatureRouter(k, e, assignment=assignment).fit(ds.f_cal)
            rows.append(
                evaluate_routes(
                    "E5",
                    ds.name,
                    method,
                    int(seed),
                    oracle.predict_from_labels(ds.f_hold),
                    ds.f_hold,
                    k,
                    e,
                    {"invalid_oracle": 1.0},
                )
            )

        for method, assignment in [("bfsr_cluster_equal", "equal"), ("bfsr_cluster_mass", "mass")]:
            bfsr = BFSRClusterRouter(k, e, normalizer_mode="whiten", assignment=assignment, seed=int(seed)).fit(
                ds.x_cal
            )
            extra = evaluate_cluster_recovery(bfsr, ds.x_hold, ds.f_hold)
            rows.append(
                evaluate_routes(
                    "E5",
                    ds.name,
                    method,
                    int(seed),
                    bfsr.predict(ds.x_hold),
                    ds.f_hold,
                    k,
                    e,
                    extra,
                )
            )

        quantile = QuantileSPRRouter(e, normalizer_mode="whiten", seed=int(seed) + 17).fit(ds.x_cal)
        rows.append(
            evaluate_routes("E5", ds.name, "quantile_spr", int(seed), quantile.predict(ds.x_hold), ds.f_hold, k, e)
        )
    return pd.DataFrame(rows)


def write_tables(e1: pd.DataFrame, e2: pd.DataFrame, e3: pd.DataFrame, e4: pd.DataFrame, e5: pd.DataFrame) -> None:
    e1_agg = aggregate(e1, ["exp_id", "method", "method_label"])
    e2_agg = aggregate(e2[e2["method"] != "oracle_equal"], ["exp_id", "method", "method_label"])
    e12 = pd.concat([e1_agg, e2_agg], ignore_index=True)
    method_order = ["oracle_equal", "bfsr_cluster_equal", "quantile_spr", "random_linear"]
    e12["order"] = e12["exp_id"].map({"E1": 0, "E2": 1}) * 10 + e12["method"].map(
        {m: i for i, m in enumerate(method_order)}
    )
    e12 = e12.sort_values("order")
    write_latex_table(
        TABLES / "e1_e2_static_dispatch.tex",
        "Static dispatch sanity and isotropy-alone null. OracleFeature uses latent labels and is an invalid upper bound; the other methods are valid non-cheating routers.",
        "tab:e1_e2_static_dispatch",
        [
            "Exp.",
            "Method",
            "LoadCV $\\downarrow$",
            "Family cons. $\\uparrow$",
            "Split rate $\\downarrow$",
            "Info frac. $\\uparrow$",
            "Cluster acc. $\\uparrow$",
        ],
        [
            [
                row.exp_id,
                row.method_label,
                format_float(row.loadcv_mean),
                format_float(row.family_consistency_mean),
                format_float(row.feature_split_rate_mean),
                format_float(row.expert_info_fraction_mean),
                format_float(getattr(row, "cluster_acc_mean", float("nan"))),
            ]
            for row in e12.itertuples()
        ],
    )

    e3_agg = aggregate(e3, ["separation"])
    e3_agg = e3_agg.sort_values("separation")
    write_latex_table(
        TABLES / "e3_recoverability.tex",
        "Recoverability sweep for BFSR-Cluster. Specialization tracks feature-family recovery rather than spectral isotropy alone.",
        "tab:e3_recoverability",
        ["Separation", "Cluster acc. $\\uparrow$", "Family cons. $\\uparrow$", "Split rate $\\downarrow$", "LoadCV $\\downarrow$"],
        [
            [
                format_float(row.separation, 2),
                format_float(row.cluster_acc_mean),
                format_float(row.family_consistency_mean),
                format_float(row.feature_split_rate_mean),
                format_float(row.loadcv_mean),
            ]
            for row in e3_agg.itertuples()
        ],
    )
    plot_e3(e3_agg)

    e4_agg = aggregate(e4, ["dataset", "normalizer", "method"])
    e4_agg = e4_agg.sort_values(["dataset", "normalizer"])
    write_latex_table(
        TABLES / "e4_spectral_normalization.tex",
        "Spectral normalization ablation. Whitening repairs anisotropic metric distortion on structured data, but does not create feature information on null data.",
        "tab:e4_spectral_normalization",
        ["Data", "Normalizer", "Cluster acc. $\\uparrow$", "Family cons. $\\uparrow$", "Info frac. $\\uparrow$", "LoadCV $\\downarrow$"],
        [
            [
                row.dataset.replace("_", " "),
                row.normalizer,
                format_float(row.cluster_acc_mean),
                format_float(row.family_consistency_mean),
                format_float(row.expert_info_fraction_mean),
                format_float(row.loadcv_mean),
            ]
            for row in e4_agg.itertuples()
        ],
    )
    plot_e4(e4_agg)

    e5_agg = aggregate(e5, ["method", "method_label"])
    order = ["oracle_equal", "oracle_mass", "bfsr_cluster_equal", "bfsr_cluster_mass", "quantile_spr"]
    e5_agg["order"] = e5_agg["method"].map({m: i for i, m in enumerate(order)})
    e5_agg = e5_agg.sort_values("order")
    write_latex_table(
        TABLES / "e5_frequency_ablation.tex",
        "Frequency-uniformity ablation. Equal-number family assignment loses mass balance when feature-family frequencies are non-uniform; mass-aware assignment repairs the mass objective when family masses are estimated.",
        "tab:e5_frequency_ablation",
        ["Method", "LoadCV $\\downarrow$", "Max mass err. $\\downarrow$", "Family cons. $\\uparrow$", "Split rate $\\downarrow$"],
        [
            [
                row.method_label,
                format_float(row.loadcv_mean),
                format_float(row.max_mass_error_mean),
                format_float(row.family_consistency_mean),
                format_float(row.feature_split_rate_mean),
            ]
            for row in e5_agg.itertuples()
        ],
    )
    plot_e5(e5_agg)


def write_distribution_table(diagnostics: pd.DataFrame) -> None:
    agg = diagnostics.groupby(["dataset", "normalizer"], as_index=False).mean(numeric_only=True)
    selected = agg[
        agg["dataset"].isin(
            [
                "E1 clean mixture",
                "E2 isotropic null",
                "E4 structured_distorted",
                "E4 null_distorted",
                "E5 frequency-imbalanced",
            ]
        )
    ].sort_values(["dataset", "normalizer"])
    write_latex_table(
        TABLES / "distribution_diagnostics.tex",
        "Distribution diagnostics. The clean mixture is frequency-uniform and spectrally isotropic up to sampling error. The frequency ablation changes feature-family masses; whitening controls the routing metric before mass-balance comparisons.",
        "tab:distribution_diagnostics",
        ["Data", "Norm.", "Cond. $\\downarrow$", "$\\|\\Sigma-I\\|_{op}$ $\\downarrow$", "Eff. rank $\\uparrow$", "Freq. gap $\\downarrow$"],
        [
            [
                row.dataset,
                row.normalizer,
                format_float(row.cov_cond),
                format_float(row.cov_op_norm_scaled_minus_i),
                format_float(row.cov_effective_rank),
                format_float(row.freq_max_min_gap),
            ]
            for row in selected.itertuples()
        ],
    )


def write_summary(e1: pd.DataFrame, e2: pd.DataFrame, e3: pd.DataFrame, e4: pd.DataFrame, e5: pd.DataFrame) -> None:
    e1_bfsr = aggregate(e1[e1["method"] == "bfsr_cluster_equal"], ["method"]).iloc[0]
    e2_valid = aggregate(e2[e2["method"] != "oracle_equal"], ["method", "method_label"])
    e3_agg = aggregate(e3, ["separation"]).sort_values("separation")
    e4_agg = aggregate(e4, ["dataset", "normalizer", "method"])
    e5_agg = aggregate(e5, ["method", "method_label"])

    e2_max_info = e2_valid["expert_info_fraction_mean"].max()
    low_sep = e3_agg.iloc[0]
    high_sep = e3_agg.iloc[-1]
    structured_raw = e4_agg[(e4_agg["dataset"] == "structured_distorted") & (e4_agg["normalizer"] == "raw")].iloc[0]
    structured_white = e4_agg[
        (e4_agg["dataset"] == "structured_distorted") & (e4_agg["normalizer"] == "whiten")
    ].iloc[0]
    null_white = e4_agg[(e4_agg["dataset"] == "null_distorted") & (e4_agg["normalizer"] == "whiten")].iloc[0]
    equal = e5_agg[e5_agg["method"] == "bfsr_cluster_equal"].iloc[0]
    mass = e5_agg[e5_agg["method"] == "bfsr_cluster_mass"].iloc[0]

    text = f"""# V2.2 Static Dispatch Experiment Summary

## What We Established

The E1--E5 suite supports the static clean-case claim: under frequency-uniform,
globally spectrally isotropic, locally recoverable feature-family data,
BFSR-Cluster builds a balanced and feature-consistent static router without
using latent labels during construction. In E1, BFSR-Cluster reaches LoadCV
{e1_bfsr.loadcv_mean:.3f}, family consistency {e1_bfsr.family_consistency_mean:.3f},
and cluster accuracy {e1_bfsr.cluster_acc_mean:.3f}.

## What The Experiments Show

- E2 confirms the impossibility anchor: when labels are independent of isotropic
  features, the best valid non-cheating method has expert information fraction
  {e2_max_info:.3f}, i.e. spectral isotropy alone does not identify feature
  specialization.
- E3 shows that specialization follows local recoverability. As separation
  increases from {low_sep.separation:.2f} to {high_sep.separation:.2f}, cluster
  accuracy rises from {low_sep.cluster_acc_mean:.3f} to
  {high_sep.cluster_acc_mean:.3f}, and family consistency rises from
  {low_sep.family_consistency_mean:.3f} to {high_sep.family_consistency_mean:.3f}.
- E4 shows that spectral normalization is a metric repair. On anisotropically
  distorted structured data, whitening changes cluster accuracy from
  {structured_raw.cluster_acc_mean:.3f} to {structured_white.cluster_acc_mean:.3f};
  on distorted null data, whitening still leaves expert information fraction at
  {null_white.expert_info_fraction_mean:.3f}.
- E5 shows why frequency uniformity matters for mass balance. On imbalanced
  feature frequencies, with whitening used to keep the routing metric
  controlled, equal-number BFSR has LoadCV {equal.loadcv_mean:.3f} while
  mass-aware BFSR has LoadCV {mass.loadcv_mean:.3f}.

## Full-Run Setup

- Seeds: 0, 1, 2, 3, 4
- Dimension: 16
- Feature families: 32
- Experts: 4
- Calibration examples: 8000
- Holdout examples: 16000
- Feature recovery: k-means with known K, 8 restarts, fitted only on calibration features

## Claim Boundary

These experiments do not test training-time route preservation, learned-router
dynamics, semantic expert identity, automatic selection of K, or real language
model utility. Static utility is intentionally parked as a downstream optional
audit.

## Artifact Map

- Runner: `papers/spectral_partition_router_v2_2/exp/run_static_dispatch_suite.py`
- Source package: `papers/spectral_partition_router_v2_2/exp/src/static_bfsr_suite.py`
- Raw metrics: `papers/spectral_partition_router_v2_2/exp/results/*_raw.csv`
- Aggregates: `papers/spectral_partition_router_v2_2/exp/results/*_aggregate.csv`
- Paper tables: `papers/spectral_partition_router_v2_2/latex/tables/`
- Paper figures: `papers/spectral_partition_router_v2_2/latex/figures/`
"""
    (RESULTS / "summary.md").write_text(text, encoding="utf-8")


def main() -> None:
    args = parse_args()
    cfg = config(args.quick)
    RESULTS.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    diagnostics: list[dict[str, object]] = []
    e1 = run_e1(cfg, diagnostics)
    e2 = run_e2(cfg, diagnostics)
    e3 = run_e3(cfg, diagnostics)
    e4 = run_e4(cfg, diagnostics)
    e5 = run_e5(cfg, diagnostics)

    save_csv(e1, "e1_clean_sanity_raw")
    save_csv(e2, "e2_isotropy_null_raw")
    save_csv(e3, "e3_recoverability_raw")
    save_csv(e4, "e4_spectral_normalization_raw")
    save_csv(e5, "e5_frequency_ablation_raw")

    save_csv(aggregate(e1, ["exp_id", "method", "method_label"]), "e1_clean_sanity_aggregate")
    save_csv(aggregate(e2, ["exp_id", "method", "method_label"]), "e2_isotropy_null_aggregate")
    save_csv(aggregate(e3, ["separation"]), "e3_recoverability_aggregate")
    save_csv(aggregate(e4, ["dataset", "normalizer", "method"]), "e4_spectral_normalization_aggregate")
    save_csv(aggregate(e5, ["method", "method_label"]), "e5_frequency_ablation_aggregate")

    diagnostics_df = pd.DataFrame(diagnostics)
    save_csv(diagnostics_df, "distribution_diagnostics_raw")
    save_csv(diagnostics_df.groupby(["dataset", "normalizer"], as_index=False).mean(numeric_only=True), "distribution_diagnostics_aggregate")

    write_tables(e1, e2, e3, e4, e5)
    write_distribution_table(diagnostics_df)
    write_summary(e1, e2, e3, e4, e5)

    print(f"Wrote results to {RESULTS}")
    print(f"Wrote tables to {TABLES}")
    print(f"Wrote figures to {FIGURES}")


if __name__ == "__main__":
    main()

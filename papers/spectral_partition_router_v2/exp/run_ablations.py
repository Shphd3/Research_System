#!/usr/bin/env python3
"""Run E6: ablation studies."""

from __future__ import annotations

import argparse

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
    lineplot,
    make_expert_weights,
    make_latent_features,
    prototype_set,
    rng,
    save_figure,
    svd_prototypes,
    unit_rows,
    write_metrics,
    write_summary,
)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="SPR v2 ablation experiments.")
    p.add_argument("--describe", action="store_true")
    p.add_argument("--quick", action="store_true")
    return p


def stable_seed(*vals: int) -> int:
    out = 7867
    for val in vals:
        out = (out * 1000037 + int(val) * 24593) % (2**32 - 1)
    return out


def seed_list(quick: bool) -> list[int]:
    return [0] if quick else list(range(5))


def make_problem(
    r: np.random.Generator,
    n_cal: int,
    n_hold: int,
    d: int,
    e: int,
    whiten: bool = True,
    anisotropic: bool = False,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    dirs, _ = prototype_set("symmetric", e, d, r)
    raw_cal, _, _ = make_latent_features(r, n_cal, d, e, 2.0, 0.72, dirs)
    raw_hold, labels_hold, _ = make_latent_features(r, n_hold, d, e, 2.0, 0.72, dirs)
    if anisotropic:
        scales = np.linspace(0.35, 2.2, d)
        raw_cal = raw_cal * scales
        raw_hold = raw_hold * scales
    if whiten:
        mu, mat = center_whiten_fit(raw_cal)
        x_cal = center_whiten_apply(raw_cal, mu, mat)
        x_hold = center_whiten_apply(raw_hold, mu, mat)
        dirs = unit_rows(center_whiten_apply(dirs, np.zeros(d), mat))
    else:
        x_cal = raw_cal - raw_cal.mean(axis=0, keepdims=True)
        x_hold = raw_hold - raw_cal.mean(axis=0, keepdims=True)
    return x_cal, x_hold, labels_hold, dirs


def expert_proto(r: np.random.Generator, dirs: np.ndarray, quality: str) -> np.ndarray:
    if quality == "aligned":
        base = dirs
        signal, noise = 3.4, 0.22
    elif quality == "noisy":
        base = unit_rows(dirs + 0.7 * r.normal(size=dirs.shape))
        signal, noise = 2.0, 0.55
    else:
        base = unit_rows(r.normal(size=dirs.shape))
        signal, noise = 1.2, 0.75
    return svd_prototypes(make_expert_weights(r, base, signal=signal, noise=noise))


def eval_setting(
    *,
    seed: int,
    ablation: str,
    setting: str,
    method: str,
    n_cal: int = 8192,
    n_hold: int = 16384,
    d: int = 64,
    e: int = 8,
    whiten: bool = True,
    anisotropic: bool = False,
    expert_quality: str = "aligned",
    drift_strength: float = 0.0,
    quick: bool = False,
) -> dict[str, object]:
    r = rng(stable_seed(seed, len(ablation), len(setting), d, e, n_cal))
    x_cal, x_hold, labels, dirs = make_problem(r, n_cal, n_hold, d, e, whiten, anisotropic)
    proto = expert_proto(r, dirs, expert_quality)
    if drift_strength > 0:
        drift = r.normal(size=(d, d))
        drift = (drift - drift.T) / (np.linalg.norm(drift, ord="fro") + 1e-12)
        x_hold = x_hold @ (np.eye(d) + drift_strength * drift)
    router = build_router(
        method,
        x_cal,
        e,
        rng(stable_seed(seed, len(method), d, e)),
        prototypes=proto,
        n_candidates=8 if quick else 24,
    )
    record = evaluate_router(method, router, x_cal, x_hold, e, labels_hold=labels, prototypes=proto)
    record.update(
        {
            "exp_id": "E6",
            "seed": seed,
            "ablation": ablation,
            "setting": setting,
            "d": d,
            "E": e,
            "n_cal": n_cal,
            "n_holdout": n_hold,
            "whiten": whiten,
            "expert_quality": expert_quality,
            "drift_strength": drift_strength,
            "run_mode": "quick" if quick else "full",
        }
    )
    return record


def run(quick: bool) -> pd.DataFrame:
    seeds = seed_list(quick)
    rows: list[dict[str, object]] = []
    cal_sizes = [512, 2048] if quick else [512, 2048, 8192, 32768]
    for seed in seeds:
        for n_cal in cal_sizes:
            rows.append(
                eval_setting(seed=seed, ablation="calibration_size", setting=str(n_cal), method="spr_local", n_cal=n_cal, quick=quick)
            )
        for e in ([4] if quick else [4, 6, 8, 12]):
            rows.append(eval_setting(seed=seed, ablation="expert_count", setting=str(e), method="spr_local", e=e, quick=quick))
        for d in ([32] if quick else [16, 32, 64, 128]):
            rows.append(eval_setting(seed=seed, ablation="dimension", setting=str(d), method="spr_local", d=d, quick=quick))
        for method, label in [("spr_fixed", "fixed"), ("spr_local", "local"), ("spr_expert", "expert")]:
            rows.append(eval_setting(seed=seed, ablation="direction_policy", setting=label, method=method, quick=quick))
        for whiten in [True, False]:
            rows.append(
                eval_setting(
                    seed=seed,
                    ablation="whitening",
                    setting="on" if whiten else "off",
                    method="spr_local",
                    whiten=whiten,
                    anisotropic=True,
                    quick=quick,
                )
            )
        for quality in (["aligned"] if quick else ["aligned", "noisy", "random"]):
            rows.append(
                eval_setting(
                    seed=seed,
                    ablation="expert_weight_quality",
                    setting=quality,
                    method="spr_expert",
                    expert_quality=quality,
                    quick=quick,
                )
            )
        for drift in ([0.0] if quick else [0.0, 0.05, 0.15, 0.3]):
            rows.append(
                eval_setting(
                    seed=seed,
                    ablation="feature_drift",
                    setting=f"{drift:.2f}",
                    method="spr_local",
                    drift_strength=drift,
                    quick=quick,
                )
            )
        for setting, method in [("forced_count", "balanced"), ("feature_router", "spr_local")]:
            rows.append(eval_setting(seed=seed, ablation="count_control", setting=setting, method=method, quick=quick))
    df = write_metrics(rows, "E6")
    plot(df)
    summarize(df)
    return df


def plot(df: pd.DataFrame) -> None:
    cal = (
        df[df["ablation"] == "calibration_size"]
        .assign(n_cal_numeric=lambda x: x["setting"].astype(int))
        .groupby(["n_cal_numeric", "method_label"], as_index=False)["holdout_loadcv"]
        .mean()
    )
    lineplot(
        cal,
        "n_cal_numeric",
        "holdout_loadcv",
        "method_label",
        "E6: calibration size controls held-out balance",
        "Holdout LoadCV",
        "e6_calibration_size.pdf",
        "E6",
    )
    policy = df[df["ablation"].isin(["direction_policy", "expert_weight_quality"])]
    barplot(
        policy,
        "setting",
        "route_feature_nmi",
        "ablation",
        "E6: policy and expert-quality ablations",
        "Route-feature NMI",
        "e6_policy_ablation.pdf",
        "E6",
        rotate=20,
    )


def summarize(df: pd.DataFrame) -> None:
    cal = aggregate(df[df["ablation"] == "calibration_size"], ["setting"], ["holdout_loadcv"])
    best = float(cal["holdout_loadcv_mean"].min())
    worst = float(cal["holdout_loadcv_mean"].max())
    forced = df[(df["ablation"] == "count_control") & (df["setting"] == "forced_count")]
    feature = df[(df["ablation"] == "count_control") & (df["setting"] == "feature_router")]
    forced_nmi = float(forced["route_feature_nmi"].mean())
    feature_nmi = float(feature["route_feature_nmi"].mean())
    bullets = [
        f"Calibration-size sensitivity is visible: mean held-out LoadCV ranges from {worst:.4f} to {best:.4f} across the tested sizes.",
        f"The forced-count control reaches NMI {forced_nmi:.4f}, while the feature-router control reaches NMI {feature_nmi:.4f}; this keeps count balance separate from feature geometry.",
        "The ablations are boundary evidence: they identify when SPR is statistically reliable, not a guarantee under arbitrary distribution shift.",
    ]
    write_summary("E6", "Ablations", bullets, df)


def main() -> None:
    args = parser().parse_args()
    if args.describe:
        print(describe("E6"))
        return
    run(args.quick)


if __name__ == "__main__":
    main()

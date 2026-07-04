#!/usr/bin/env python3
"""Run E5: controlled MoE training dynamics."""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd
from sklearn.metrics import normalized_mutual_info_score

from src.registry import describe
from src.synthetic_suite import (
    BalancedAssignment,
    LinearRouter,
    SPRTree,
    aggregate,
    build_router,
    center_whiten_apply,
    center_whiten_fit,
    lineplot,
    make_expert_weights,
    make_latent_features,
    margin_p05,
    prototype_set,
    purity_score,
    rng,
    save_figure,
    svd_prototypes,
    unit_rows,
    usage_metrics,
    write_metrics,
    write_summary,
)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Controlled training dynamics experiments.")
    p.add_argument("--describe", action="store_true")
    p.add_argument("--quick", action="store_true")
    return p


def stable_seed(*vals: int) -> int:
    out = 6421
    for val in vals:
        out = (out * 1000033 + int(val) * 31337) % (2**32 - 1)
    return out


def configs(quick: bool) -> tuple[list[int], int, int, int, int, int, int, int]:
    if quick:
        return [0], 24, 4, 1024, 512, 3, 12, 4
    return list(range(5)), 32, 8, 8192, 4096, 4, 80, 10


def make_task(
    r: np.random.Generator,
    n_train: int,
    n_val: int,
    d: int,
    e: int,
    out_dim: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    class_dirs, _ = prototype_set("symmetric", e, d, r)
    raw_train, y_train_labels, _ = make_latent_features(r, n_train, d, e, 2.2, 0.65, class_dirs)
    raw_val, y_val_labels, _ = make_latent_features(r, n_val, d, e, 2.2, 0.65, class_dirs)
    mu, mat = center_whiten_fit(raw_train)
    x_train = center_whiten_apply(raw_train, mu, mat)
    x_val = center_whiten_apply(raw_val, mu, mat)
    maps = r.normal(scale=0.7, size=(e, out_dim, d))
    maps += 0.8 * class_dirs[:, None, :]
    y_train = np.einsum("nod,nd->no", maps[y_train_labels], x_train)
    y_val = np.einsum("nod,nd->no", maps[y_val_labels], x_val)
    y_train += 0.03 * r.normal(size=y_train.shape)
    y_val += 0.03 * r.normal(size=y_val.shape)
    proto_dirs = unit_rows(center_whiten_apply(class_dirs, np.zeros(d), mat))
    return x_train, y_train, y_train_labels, x_val, y_val, y_val_labels, proto_dirs


def drift_basis(r: np.random.Generator, d: int) -> np.ndarray:
    a = r.normal(size=(d, d))
    skew = a - a.T
    return skew / (np.linalg.norm(skew, ord="fro") + 1e-12)


def apply_drift(x: np.ndarray, basis: np.ndarray, strength: float, t: float) -> np.ndarray:
    return x @ (np.eye(x.shape[1]) + strength * t * basis)


def spr_init_linear(x_cal: np.ndarray, e: int, r: np.random.Generator) -> LinearRouter:
    tree = SPRTree(e, "local", r, n_candidates=24).fit(x_cal)
    routes = tree.route(x_cal).routes
    rows = []
    for expert in range(e):
        xe = x_cal[routes == expert]
        if len(xe) == 0:
            rows.append(r.normal(size=x_cal.shape[1]))
        else:
            rows.append(xe.mean(axis=0))
    return LinearRouter(np.stack(rows))


def predict_experts(weights: np.ndarray, x: np.ndarray, routes: np.ndarray) -> np.ndarray:
    pred = np.empty((len(x), weights.shape[1]))
    for expert in range(weights.shape[0]):
        idx = routes == expert
        if idx.any():
            pred[idx] = x[idx] @ weights[expert].T
    return pred


def train_one(
    method: str,
    seed: int,
    quick: bool,
) -> pd.DataFrame:
    seeds, d, e, n_train, n_val, out_dim, epochs, update_freq = configs(quick)
    del seeds
    r = rng(stable_seed(seed, len(method), d, e))
    x_train, y_train, labels_train, x_val, y_val, labels_val, proto_dirs = make_task(
        r, n_train, n_val, d, e, out_dim
    )
    basis = drift_basis(r, d)
    expert_weights = make_expert_weights(r, proto_dirs, signal=3.5, noise=0.18)
    proto = svd_prototypes(expert_weights)
    if method == "vanilla":
        router = build_router("vanilla", x_train, e, rng(stable_seed(seed, 1)))
    elif method == "lb_control":
        router = BalancedAssignment(e, rng(stable_seed(seed, 2)).normal(size=d))
    elif method == "simplex":
        router = build_router("simplex", x_train, e, rng(stable_seed(seed, 3)))
    elif method == "frozen_spr":
        router = SPRTree(e, "local", rng(stable_seed(seed, 4)), n_candidates=24).fit(x_train)
    elif method == "spr_init_linear":
        router = spr_init_linear(x_train, e, rng(stable_seed(seed, 5)))
    elif method == "slow_update_spr":
        router = SPRTree(e, "local", rng(stable_seed(seed, 6)), n_candidates=24).fit(x_train)
    elif method == "spr_expert":
        router = SPRTree(e, "expert", rng(stable_seed(seed, 7)), prototypes=proto, n_candidates=24).fit(x_train)
    else:
        raise ValueError(method)
    params = 0.02 * r.normal(size=(e, out_dim, d))
    lr = 0.045
    drift_strength = 0.16
    initial_routes = router.route(x_val).routes
    rows = []
    for epoch in range(epochs + 1):
        t = epoch / max(1, epochs)
        xt = apply_drift(x_train, basis, drift_strength, t)
        xv = apply_drift(x_val, basis, drift_strength, t)
        if method == "slow_update_spr" and epoch > 0 and epoch % update_freq == 0:
            router = SPRTree(e, "local", rng(stable_seed(seed, epoch, 6)), n_candidates=24).fit(xt)
        train_result = router.route(xt)
        val_result = router.route(xv)
        if epoch > 0:
            for expert in range(e):
                idx = train_result.routes == expert
                if idx.sum() < 4:
                    continue
                pred = xt[idx] @ params[expert].T
                err = pred - y_train[idx]
                grad = (2.0 / idx.sum()) * err.T @ xt[idx]
                params[expert] -= lr * grad
        train_pred = predict_experts(params, xt, train_result.routes)
        val_pred = predict_experts(params, xv, val_result.routes)
        train_loss = float(np.mean((train_pred - y_train) ** 2))
        val_loss = float(np.mean((val_pred - y_val) ** 2))
        usage = usage_metrics(val_result.routes, e)
        rows.append(
            {
                "exp_id": "E5",
                "seed": seed,
                "method": method,
                "method_label": {
                    "vanilla": "Vanilla linear",
                    "lb_control": "Linear + load-balance",
                    "simplex": "Simplex init",
                    "frozen_spr": "Frozen-SPR",
                    "spr_init_linear": "SPR-init-linear",
                    "slow_update_spr": "SlowUpdate-SPR",
                    "spr_expert": "SPR-Expert",
                }[method],
                "epoch": epoch,
                "d": d,
                "E": e,
                "n_train": n_train,
                "n_val": n_val,
                "train_loss": train_loss,
                "val_loss": val_loss,
                "holdout_loadcv": usage["loadcv"],
                "holdout_max_abs_error": usage["max_abs_error"],
                "route_feature_nmi": float(normalized_mutual_info_score(labels_val, val_result.routes)),
                "feature_purity": purity_score(val_result.routes, labels_val),
                "route_flip_rate": float(np.mean(val_result.routes != initial_routes)),
                "holdout_margin_p05": margin_p05(val_result.margins),
                "specialization_score": purity_score(val_result.routes, labels_val),
                "run_mode": "quick" if quick else "full",
            }
        )
    return pd.DataFrame(rows)


def run(quick: bool) -> pd.DataFrame:
    seeds, *_ = configs(quick)
    methods = [
        "vanilla",
        "lb_control",
        "simplex",
        "frozen_spr",
        "spr_init_linear",
        "slow_update_spr",
        "spr_expert",
    ]
    frames = [train_one(method, seed, quick) for seed in seeds for method in methods]
    df = pd.concat(frames, ignore_index=True)
    write_metrics(df.to_dict("records"), "E5")
    plot(df)
    summarize(df)
    return df


def plot(df: pd.DataFrame) -> None:
    loss = df.groupby(["epoch", "method_label"], as_index=False)["val_loss"].mean()
    lineplot(loss, "epoch", "val_loss", "method_label", "E5: validation loss", "Validation MSE", "e5_loss_curves.pdf", "E5")
    nmi = df.groupby(["epoch", "method_label"], as_index=False)["route_feature_nmi"].mean()
    lineplot(nmi, "epoch", "route_feature_nmi", "method_label", "E5: route-feature agreement", "NMI", "e5_route_nmi.pdf", "E5")
    flip = df.groupby(["epoch", "method_label"], as_index=False)["route_flip_rate"].mean()
    lineplot(flip, "epoch", "route_flip_rate", "method_label", "E5: route flips under representation drift", "Flip rate", "e5_flip_rate.pdf", "E5")
    margin = df.groupby(["epoch", "method_label"], as_index=False)["holdout_margin_p05"].mean()
    lineplot(margin, "epoch", "holdout_margin_p05", "method_label", "E5: lower-tail route margin", "Margin p05", "e5_margin_p05.pdf", "E5")


def summarize(df: pd.DataFrame) -> None:
    final = df[df["epoch"] == df["epoch"].max()]
    agg = aggregate(
        final,
        ["method_label"],
        ["val_loss", "holdout_loadcv", "route_feature_nmi", "route_flip_rate", "holdout_margin_p05"],
    )
    frozen_loss = float(agg.loc[agg["method_label"] == "Frozen-SPR", "val_loss_mean"].iloc[0])
    vanilla_loss = float(agg.loc[agg["method_label"] == "Vanilla linear", "val_loss_mean"].iloc[0])
    slow_flip = float(agg.loc[agg["method_label"] == "SlowUpdate-SPR", "route_flip_rate_mean"].iloc[0])
    bullets = [
        f"At the final epoch, Frozen-SPR validation MSE is {frozen_loss:.4f}, compared with {vanilla_loss:.4f} for vanilla fixed linear routing.",
        f"SlowUpdate-SPR's final route flip rate under controlled drift is {slow_flip:.4f}; this measures adaptation, not semantic expert discovery.",
        "The training audit supports the limited claim that geometry-aware partitions can make the controlled expert task easier when the latent feature classes match the routing geometry.",
    ]
    write_summary("E5", "Controlled MoE training dynamics", bullets, df)


def main() -> None:
    args = parser().parse_args()
    if args.describe:
        print(describe("E5"))
        return
    run(args.quick)


if __name__ == "__main__":
    main()

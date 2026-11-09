#!/usr/bin/env python3
"""Controlled feedback-common preservation bridge."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


INTERVENTIONS = [
    "step0",
    "full_drift",
    "feedback_only",
    "residual_only",
    "random_feedback_only",
    "random_residual_only",
]

MAIN_FEEDBACK_REGIMES = ["common_feedback", "mixed_feedback_residual"]


@dataclass(frozen=True)
class RegimeConfig:
    name: str
    feedback_strength: float
    residual_strength: float
    nuisance_strength: float
    description: str


REGIMES = [
    RegimeConfig(
        name="common_feedback",
        feedback_strength=4.0,
        residual_strength=0.0,
        nuisance_strength=0.0,
        description="Shared feedback drift should collapse routing and be removable.",
    ),
    RegimeConfig(
        name="mixed_feedback_residual",
        feedback_strength=3.6,
        residual_strength=1.0,
        nuisance_strength=0.25,
        description="Shared feedback plus residual drift; feedback should explain the main drop.",
    ),
    RegimeConfig(
        name="residual_drift_control",
        feedback_strength=0.0,
        residual_strength=2.0,
        nuisance_strength=0.25,
        description="Group-specific residual drift should not be explained by feedback common.",
    ),
    RegimeConfig(
        name="nuisance_drift_control",
        feedback_strength=0.0,
        residual_strength=0.0,
        nuisance_strength=4.0,
        description="Activation nuisance drift should not collapse through the common-margin channel.",
    ),
    RegimeConfig(
        name="weak_feedback",
        feedback_strength=1.8,
        residual_strength=0.5,
        nuisance_strength=0.2,
        description="Smaller feedback drift tests sensitivity and denominator stability.",
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


def nmi(labels: np.ndarray, preds: np.ndarray) -> float:
    labels = labels.astype(int)
    preds = preds.astype(int)
    label_values = np.unique(labels)
    pred_values = np.unique(preds)
    contingency = np.zeros((len(label_values), len(pred_values)), dtype=float)
    label_index = {value: idx for idx, value in enumerate(label_values)}
    pred_index = {value: idx for idx, value in enumerate(pred_values)}
    for label, pred in zip(labels, preds):
        contingency[label_index[label], pred_index[pred]] += 1
    contingency /= contingency.sum()
    px = contingency.sum(axis=1)
    py = contingency.sum(axis=0)

    mi = 0.0
    for i in range(contingency.shape[0]):
        for j in range(contingency.shape[1]):
            pxy = contingency[i, j]
            if pxy > 0 and px[i] > 0 and py[j] > 0:
                mi += pxy * np.log(pxy / (px[i] * py[j]))

    hx = -float(np.sum(px[px > 0] * np.log(px[px > 0])))
    hy = -float(np.sum(py[py > 0] * np.log(py[py > 0])))
    denom = hx + hy
    return float(2.0 * mi / denom) if denom > 1e-12 else 0.0


def route_stats(h: np.ndarray, router: np.ndarray, labels: np.ndarray) -> dict[str, float]:
    logits = h @ router.T
    preds = logits.argmax(axis=1)
    counts = np.bincount(preds, minlength=router.shape[0])
    return {
        "proxy_route_nmi": nmi(labels, preds),
        "route_max_load": float(counts.max() / counts.sum()),
        "active_experts": int(np.count_nonzero(counts)),
    }


def make_problem(
    cfg: RegimeConfig,
    seed: int,
    d_hidden: int,
    n_groups: int,
    samples_per_group: int,
    center_strength: float,
    common_gate_strength: float,
    step0_noise: float,
) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    centers = sample_basis(rng, d_hidden, n_groups).T * center_strength
    center_basis = orthonormalize(centers.T)
    common_dir = sample_basis(rng, d_hidden, 1, against=center_basis)[:, 0]
    nuisance_basis = sample_basis(
        rng,
        d_hidden,
        min(4, d_hidden - n_groups - 1),
        against=orthonormalize(np.concatenate([center_basis, common_dir[:, None]], axis=1)),
    )

    labels = np.repeat(np.arange(n_groups), samples_per_group)
    h0 = centers[labels] + step0_noise * rng.normal(size=(len(labels), d_hidden))
    router = centers.copy()
    router[0] += common_gate_strength * common_dir

    common_scalar = 1.0 + 0.05 * rng.normal(size=(len(labels), 1))
    feedback_drift = cfg.feedback_strength * common_scalar * common_dir[None, :]

    residual_drift = np.zeros_like(h0)
    if cfg.residual_strength > 0:
        residual_noise = rng.normal(size=(n_groups, d_hidden))
        residual_noise = residual_noise - common_dir[None, :] * (residual_noise @ common_dir)[:, None]
        residual_noise = residual_noise / np.maximum(np.linalg.norm(residual_noise, axis=1, keepdims=True), 1e-9)
        residual_drift = cfg.residual_strength * residual_noise[labels]

    nuisance_drift = np.zeros_like(h0)
    if cfg.nuisance_strength > 0:
        z_nuisance = rng.normal(size=(len(labels), nuisance_basis.shape[1]))
        nuisance_drift = cfg.nuisance_strength * (z_nuisance @ nuisance_basis.T)

    drift = feedback_drift + residual_drift + nuisance_drift

    return {
        "h0": h0,
        "drift": drift,
        "router": router,
        "labels": labels,
        "common_dir": common_dir,
    }


def run_seed(
    cfg: RegimeConfig,
    seed: int,
    d_hidden: int,
    n_groups: int,
    samples_per_group: int,
    center_strength: float,
    common_gate_strength: float,
    step0_noise: float,
) -> dict[str, object]:
    data = make_problem(
        cfg,
        seed=seed,
        d_hidden=d_hidden,
        n_groups=n_groups,
        samples_per_group=samples_per_group,
        center_strength=center_strength,
        common_gate_strength=common_gate_strength,
        step0_noise=step0_noise,
    )
    h0 = data["h0"]
    drift = data["drift"]
    router = data["router"]
    labels = data["labels"]
    common_dir = data["common_dir"]

    fb_basis = top_eigvecs_sym((drift.T @ drift) / drift.shape[0], 1)
    p_fb = projector(fb_basis)
    rng = np.random.default_rng(200_000 + seed)
    random_basis = sample_basis(rng, d_hidden, 1)
    p_random = projector(random_basis)

    states = {
        "step0": h0,
        "full_drift": h0 + drift,
        "feedback_only": h0 + drift @ p_fb,
        "residual_only": h0 + drift - drift @ p_fb,
        "random_feedback_only": h0 + drift @ p_random,
        "random_residual_only": h0 + drift - drift @ p_random,
    }

    stats = {name: route_stats(state, router, labels) for name, state in states.items()}
    nmi0 = stats["step0"]["proxy_route_nmi"]
    nmi_full = stats["full_drift"]["proxy_route_nmi"]
    nmi_fb = stats["feedback_only"]["proxy_route_nmi"]
    nmi_res = stats["residual_only"]["proxy_route_nmi"]
    nmi_random_fb = stats["random_feedback_only"]["proxy_route_nmi"]
    nmi_random_res = stats["random_residual_only"]["proxy_route_nmi"]
    full_drop = nmi0 - nmi_full
    denominator_valid = full_drop >= 0.05
    denom = full_drop if denominator_valid else 1.0

    row: dict[str, object] = {
        "regime": cfg.name,
        "seed": seed,
        "step0_proxy_nmi": nmi0,
        "full_drift_proxy_nmi": nmi_full,
        "feedback_only_proxy_nmi": nmi_fb,
        "residual_only_proxy_nmi": nmi_res,
        "random_feedback_only_proxy_nmi": nmi_random_fb,
        "random_residual_only_proxy_nmi": nmi_random_res,
        "full_nmi_drop": full_drop,
        "denominator_valid": denominator_valid,
        "proxy_nmi_drop_explained_by_feedback_common": (nmi0 - nmi_fb) / denom,
        "feedback_removal_rescue_fraction": (nmi_res - nmi_full) / denom,
        "random_drop_explained": (nmi0 - nmi_random_fb) / denom,
        "random_removal_rescue_fraction": (nmi_random_res - nmi_full) / denom,
        "feedback_projector_common_alignment": float(np.linalg.norm(common_dir @ fb_basis) ** 2),
    }
    for intervention, values in stats.items():
        row[f"{intervention}_max_load"] = values["route_max_load"]
        row[f"{intervention}_active_experts"] = values["active_experts"]
    return row


def aggregate(rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    summary_rows: list[dict[str, object]] = []
    intervention_rows: list[dict[str, object]] = []
    regimes = [cfg.name for cfg in REGIMES]

    metrics = [
        "step0_proxy_nmi",
        "full_drift_proxy_nmi",
        "feedback_only_proxy_nmi",
        "residual_only_proxy_nmi",
        "random_feedback_only_proxy_nmi",
        "random_residual_only_proxy_nmi",
        "full_nmi_drop",
        "proxy_nmi_drop_explained_by_feedback_common",
        "feedback_removal_rescue_fraction",
        "random_drop_explained",
        "random_removal_rescue_fraction",
        "feedback_projector_common_alignment",
        "denominator_valid",
    ]

    for regime in regimes:
        regime_rows = [row for row in rows if row["regime"] == regime]
        out: dict[str, object] = {"regime": regime}
        for metric in metrics:
            values = np.array([float(row[metric]) for row in regime_rows])
            out[f"{metric}_mean"] = float(values.mean())
            out[f"{metric}_std"] = float(values.std(ddof=1))
        out["feedback_explain_seed_rate_ge_0_75"] = float(
            np.mean([float(row["proxy_nmi_drop_explained_by_feedback_common"]) >= 0.75 for row in regime_rows])
        )
        out["feedback_rescue_seed_rate_ge_0_75"] = float(
            np.mean([float(row["feedback_removal_rescue_fraction"]) >= 0.75 for row in regime_rows])
        )
        summary_rows.append(out)

        for intervention in INTERVENTIONS:
            values = np.array([float(row[f"{intervention}_proxy_nmi"]) for row in regime_rows])
            intervention_rows.append(
                {
                    "regime": regime,
                    "intervention": intervention,
                    "proxy_nmi_mean": float(values.mean()),
                    "proxy_nmi_std": float(values.std(ddof=1)),
                }
            )

    main_passed = []
    for row in summary_rows:
        if row["regime"] in MAIN_FEEDBACK_REGIMES:
            explain = float(row["proxy_nmi_drop_explained_by_feedback_common_mean"])
            rescue = float(row["feedback_removal_rescue_fraction_mean"])
            random_explain = float(row["random_drop_explained_mean"])
            random_rescue = float(row["random_removal_rescue_fraction_mean"])
            if explain >= 0.75 and rescue >= 0.75 and explain > random_explain + 0.25 and rescue > random_rescue + 0.25:
                main_passed.append(row["regime"])

    controls_ok = True
    for row in summary_rows:
        if row["regime"] in ["residual_drift_control", "nuisance_drift_control"]:
            drop = float(row["full_nmi_drop_mean"])
            explain = float(row["proxy_nmi_drop_explained_by_feedback_common_mean"])
            controls_ok = controls_ok and (drop < 0.15 or explain < 0.5)

    meta = {
        "primary_metric": "proxy_nmi_drop_explained_by_feedback_common",
        "main_feedback_regimes": MAIN_FEEDBACK_REGIMES,
        "passed_main_feedback_regimes": main_passed,
        "n_passed_main_feedback_regimes": len(main_passed),
        "controls_ok": controls_ok,
        "pass_rule": "both main feedback regimes explain>=0.75, rescue>=0.75, and beat random controls by >0.25; negative controls must not show a false feedback explanation",
        "pass": len(main_passed) == len(MAIN_FEEDBACK_REGIMES) and controls_ok,
    }
    return summary_rows, intervention_rows, meta


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot_nmi(intervention_rows: list[dict[str, object]], out: Path) -> None:
    regimes = [cfg.name for cfg in REGIMES]
    x = np.arange(len(regimes))
    width = 0.13
    fig, ax = plt.subplots(figsize=(13, 5.8))
    for idx, intervention in enumerate(INTERVENTIONS[:4]):
        means = []
        stds = []
        for regime in regimes:
            row = next(r for r in intervention_rows if r["regime"] == regime and r["intervention"] == intervention)
            means.append(float(row["proxy_nmi_mean"]))
            stds.append(float(row["proxy_nmi_std"]))
        ax.bar(x + (idx - 1.5) * width, means, width=width, yerr=stds, capsize=2, label=intervention)
    ax.set_title("Proxy-route NMI under drift replay/removal")
    ax.set_ylabel("Proxy-route NMI")
    ax.set_xticks(x)
    ax.set_xticklabels(regimes, rotation=20, ha="right")
    ax.set_ylim(0, 1.05)
    ax.legend(ncol=2, fontsize=9)
    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)


def plot_explain_rescue(summary_rows: list[dict[str, object]], out: Path) -> None:
    regimes = [cfg.name for cfg in REGIMES]
    explain = [float(row["proxy_nmi_drop_explained_by_feedback_common_mean"]) for row in summary_rows]
    rescue = [float(row["feedback_removal_rescue_fraction_mean"]) for row in summary_rows]
    random_explain = [float(row["random_drop_explained_mean"]) for row in summary_rows]
    x = np.arange(len(regimes))
    width = 0.24
    fig, ax = plt.subplots(figsize=(12, 5.2))
    ax.bar(x - width, explain, width=width, label="feedback explain")
    ax.bar(x, rescue, width=width, label="feedback removal rescue")
    ax.bar(x + width, random_explain, width=width, label="random explain")
    ax.axhline(0.75, color="black", linestyle="--", linewidth=0.8)
    ax.set_title("Feedback-common explanation and rescue fractions")
    ax.set_ylabel("Fraction of full NMI drop")
    ax.set_xticks(x)
    ax.set_xticklabels(regimes, rotation=20, ha="right")
    ax.legend(ncol=3, fontsize=9)
    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)


def plot_load(rows: list[dict[str, object]], out: Path) -> None:
    regimes = [cfg.name for cfg in REGIMES]
    x = np.arange(len(regimes))
    width = 0.18
    fig, ax = plt.subplots(figsize=(12, 5.2))
    for idx, intervention in enumerate(["step0", "full_drift", "feedback_only", "residual_only"]):
        means = []
        for regime in regimes:
            vals = [
                float(row[f"{intervention}_max_load"])
                for row in rows
                if row["regime"] == regime
            ]
            means.append(float(np.mean(vals)))
        ax.bar(x + (idx - 1.5) * width, means, width=width, label=intervention)
    ax.set_title("Route max load under drift replay/removal")
    ax.set_ylabel("Max expert load fraction")
    ax.set_xticks(x)
    ax.set_xticklabels(regimes, rotation=20, ha="right")
    ax.set_ylim(0, 1.05)
    ax.legend(ncol=2, fontsize=9)
    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=Path("."))
    parser.add_argument("--d-hidden", type=int, default=32)
    parser.add_argument("--n-groups", type=int, default=8)
    parser.add_argument("--samples-per-group", type=int, default=600)
    parser.add_argument("--center-strength", type=float, default=2.5)
    parser.add_argument("--common-gate-strength", type=float, default=2.2)
    parser.add_argument("--step0-noise", type=float, default=0.25)
    parser.add_argument("--seeds", type=int, nargs="+", default=list(range(20)))
    args = parser.parse_args()

    outdir = args.outdir
    tables = outdir / "tables"
    figures = outdir / "figures"
    tables.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)

    rows = [
        run_seed(
            cfg,
            seed=seed,
            d_hidden=args.d_hidden,
            n_groups=args.n_groups,
            samples_per_group=args.samples_per_group,
            center_strength=args.center_strength,
            common_gate_strength=args.common_gate_strength,
            step0_noise=args.step0_noise,
        )
        for cfg in REGIMES
        for seed in args.seeds
    ]
    summary_rows, intervention_rows, meta = aggregate(rows)

    write_csv(tables / "feedback_bridge_scores.csv", rows)
    write_csv(tables / "feedback_bridge_summary.csv", summary_rows)
    write_csv(tables / "feedback_bridge_intervention_nmi.csv", intervention_rows)
    with (tables / "feedback_bridge_winner_summary.json").open("w") as f:
        json.dump(meta, f, indent=2)
    with (tables / "run_config.json").open("w") as f:
        json.dump(
            {
                "d_hidden": args.d_hidden,
                "n_groups": args.n_groups,
                "samples_per_group": args.samples_per_group,
                "center_strength": args.center_strength,
                "common_gate_strength": args.common_gate_strength,
                "step0_noise": args.step0_noise,
                "seeds": args.seeds,
                "regimes": [asdict(cfg) for cfg in REGIMES],
                "interventions": INTERVENTIONS,
                "main_feedback_regimes": MAIN_FEEDBACK_REGIMES,
            },
            f,
            indent=2,
        )

    plot_nmi(intervention_rows, figures / "feedback_bridge_nmi_by_condition.png")
    plot_explain_rescue(summary_rows, figures / "feedback_explain_rescue_by_regime.png")
    plot_load(rows, figures / "feedback_bridge_max_load_by_condition.png")

    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()

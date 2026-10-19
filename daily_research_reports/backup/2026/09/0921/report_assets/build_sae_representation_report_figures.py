#!/usr/bin/env python3
"""Build the bounded result figures for the 2026-09-21 SAE representation audit.

The script reads only completed PASS JSON artifacts.  It performs no model
loading, probe fitting, resampling, or new statistical test.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np


REPO = Path("/data/250010109/Research_System")
OUT = REPO / "daily_research_reports/0921/figures"
OUT.mkdir(parents=True, exist_ok=True)

E06 = Path("/data/250010109/MoE_Router/experiments/20260920_sae_representation_21b_audit/runs/full_4x5090_retry2_20260921T0200Z/analysis")
E07 = Path("/data/250010109/MoE_Router/experiments/20260920_sae_representation_15b_early_audit/runs/full_15b_4x5090_20260920_wave1/analysis/15b")
E08 = Path("/data/250010109/MoE_Router/experiments/20260920_sae_representation_15b_early_audit/runs/full_early_4x5090_20260920_wave1/analysis")

SOURCES = {
    "e06_primary": E06 / "primary/primary_metrics.json",
    "e06_geometry": E06 / "geometry/geometry_cka.json",
    "e06_observer": E06 / "observer/observer_metrics.json",
    "e06_cost": E06 / "cost/n8_test_nll.json",
    "e06_semantic": E06 / "semantic_controls/p_semantic_controls.json",
    "e07_primary": E07 / "primary/primary_metrics.json",
    "e07_observer": E07 / "observer/observer_metrics.json",
    "e07_cost": E07 / "cost/n8_test_nll.json",
    "e07_semantic": E07 / "semantic_controls/p_semantic_controls.json",
    "e08_trajectory": E08 / "trajectory/trajectory_metrics.json",
}


def load(key: str) -> dict:
    value = json.loads(SOURCES[key].read_text())
    assert value.get("status") == "PASS", (key, value.get("status"))
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


DENSE = "#171717"
SALL = "#009E73"
S7 = "#0072B2"
GRAY = "#64748B"
RED = "#C23B22"
LIGHT = "#D7EDE5"
MODEL_COLOR = {
    "21b_dense": DENSE,
    "21b_sall_original": SALL,
    "21b_s7_reweighted": S7,
    "15b_dense": DENSE,
    "15b_sall_original": SALL,
}
MODEL_NAME = {
    "21b_dense": "Dense",
    "21b_sall_original": "SALL",
    "21b_s7_reweighted": "S7",
    "15b_dense": "Dense",
    "15b_sall_original": "SALL",
}


def style(ax, grid_axis="y"):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis=grid_axis, color="#D7DEE7", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)


def save(fig, stem: str):
    fig.savefig(OUT / f"{stem}.png", dpi=220, bbox_inches="tight", facecolor="white")
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def get_p(rows, case, layer, pooling):
    return next(r for r in rows if r["case"] == case and r["layer"] == layer and r["pooling"] == pooling)


def fig_main_p21b():
    primary = load("e06_primary")
    rows = primary["P_rel_v2"]
    fig, axes = plt.subplots(1, 3, figsize=(15.2, 4.4), gridspec_kw={"width_ratios": [0.92, 1.45, 1.08]})

    # A: registered paired contrast.
    ax = axes[0]
    for y, row in enumerate(primary["paired_primary"]):
        point = 100 * row["point"]
        lo, hi = (100 * x for x in row["ci95_percentile"])
        ax.errorbar(point, y, xerr=[[point - lo], [hi - point]], fmt="o", color=SALL,
                    capsize=5, lw=2.1, ms=7)
        ax.text(hi + 0.35, y, f"{point:+.2f} pp\nHolm p={row['holm_adjusted_p']:.3f}", va="center", fontsize=9)
    ax.axvline(0, color="#334155", lw=1)
    ax.set_yticks([0, 1], ["Layer 4", "Layer 8"])
    ax.invert_yaxis()
    ax.set_xlim(-6.2, 3.1)
    ax.set_xlabel("SALL - Dense accuracy (percentage points)")
    ax.set_title("A | Registered 21B test\nlast content token", loc="left", fontweight="bold")
    style(ax, "x")

    # B: absolute joint-holdout scores under both observation pools.
    ax = axes[1]
    clusters = [(4, "last"), (4, "mean"), (8, "last"), (8, "mean")]
    cases = ["21b_dense", "21b_sall_original", "21b_s7_reweighted"]
    x = np.arange(len(clusters)); width = 0.24
    for j, case in enumerate(cases):
        values = [100 * get_p(rows, case, layer, pool)["test"]["test_joint"]["family_equal_accuracy"]
                  for layer, pool in clusters]
        ax.bar(x + (j - 1) * width, values, width=width, color=MODEL_COLOR[case], label=MODEL_NAME[case])
    ax.axhline(50, color="#475569", ls="--", lw=1, label="chance")
    ax.set_ylim(47, 56)
    ax.set_xticks(x, ["L4 last", "L4 mean", "L8 last", "L8 mean"])
    ax.set_ylabel("P joint-holdout accuracy (%)")
    ax.set_title("B | Pooling changes the observed direction", loc="left", fontweight="bold")
    ax.legend(frameon=False, ncol=2, fontsize=9)
    style(ax)

    # C: seen wording vs unseen wording at the main late layer.
    ax = axes[2]
    x = np.arange(3); width = 0.34
    entity = [100 * get_p(rows, c, 8, "last")["test"]["test_entity"]["family_equal_accuracy"] for c in cases]
    joint = [100 * get_p(rows, c, 8, "last")["test"]["test_joint"]["family_equal_accuracy"] for c in cases]
    ax.bar(x - width / 2, entity, width, color="#94A3B8", label="new entities only")
    ax.bar(x + width / 2, joint, width, color=[MODEL_COLOR[c] for c in cases], label="new entities + wording")
    ax.axhline(50, color="#475569", ls="--", lw=1)
    ax.set_ylim(45, 86)
    ax.set_xticks(x, [MODEL_NAME[c] for c in cases])
    ax.set_ylabel("Layer-8 last-token accuracy (%)")
    ax.set_title("C | The bottleneck is new wording", loc="left", fontweight="bold")
    ax.legend(frameon=False, fontsize=9)
    style(ax)

    fig.suptitle("Native relation accessibility at 21B: the registered SALL improvement is not supported",
                 x=0.02, ha="left", fontsize=14, fontweight="bold")
    fig.text(0.02, -0.01,
             "P_rel_v2 test_joint holds out both entity groups and templates; 40 entity groups are the paired uncertainty units. "
             "Mean pooling and S7 are diagnostics, not replacements for the registered SALL-vs-Dense last-token test.",
             fontsize=9, color="#475569")
    fig.tight_layout(rect=[0, 0.055, 1, 0.91])
    save(fig, "01_21b_native_relation_accessibility")


def fig_trajectory():
    early = load("e08_trajectory")
    p15 = load("e07_primary")["paired_secondary"]
    p21 = load("e06_primary")["paired_primary"]
    c15 = load("e07_cost")["paired_contrasts"][0]
    c21 = load("e06_cost")["paired_contrasts"][0]

    points = {4: [], 8: []}
    nll = []
    for row in early["timepoints"]:
        t = row["tokens_seen"] / 1e9
        for contrast in row["native_p_joint_secondary"]:
            points[contrast["layer"]].append((t, contrast["point"], contrast["ci95_percentile"], "exploratory"))
        n = row["n8_test_nll_sall_minus_dense"]
        nll.append((t, n["mean_record_nll_difference"], n["paired_record_bootstrap_ci95"], "exploratory"))
    for contrast in p15:
        points[contrast["layer"]].append((15, contrast["point"], contrast["ci95_percentile"], "secondary"))
    for contrast in p21:
        points[contrast["layer"]].append((21, contrast["point"], contrast["ci95_percentile"], "primary"))
    nll.extend([
        (15, c15["mean_record_nll_difference"], c15["paired_record_bootstrap_ci95"], "secondary"),
        (21, c21["mean_record_nll_difference"], c21["paired_record_bootstrap_ci95"], "primary"),
    ])

    fig, axes = plt.subplots(1, 3, figsize=(15.2, 4.35))
    for ax, layer in zip(axes[:2], [4, 8]):
        rows = sorted(points[layer])
        x = np.array([r[0] for r in rows]); y = 100 * np.array([r[1] for r in rows])
        lo = 100 * np.array([r[2][0] for r in rows]); hi = 100 * np.array([r[2][1] for r in rows])
        ax.plot(x, y, color=SALL, lw=1.8, alpha=0.7)
        for xx, yy, ll, hh, role in zip(x, y, lo, hi, [r[3] for r in rows]):
            marker = {"exploratory": "o", "secondary": "s", "primary": "D"}[role]
            face = "white" if role == "exploratory" else SALL
            ax.errorbar(xx, yy, yerr=[[yy - ll], [hh - yy]], fmt=marker, mfc=face, mec=SALL,
                        color=SALL, capsize=3.5, ms=6.5, lw=1.4)
        ax.axhline(0, color="#334155", lw=1)
        ax.axvline(9.174, color="#94A3B8", ls=":", lw=1)
        ax.set_xlabel("training tokens (billions)")
        ax.set_ylabel("SALL - Dense P accuracy (pp)")
        ax.set_title(f"{'A' if layer == 4 else 'B'} | Layer {layer}, last token", loc="left", fontweight="bold")
        style(ax)

    ax = axes[2]
    rows = sorted(nll)
    x = np.array([r[0] for r in rows]); y = np.array([r[1] for r in rows])
    lo = np.array([r[2][0] for r in rows]); hi = np.array([r[2][1] for r in rows])
    ax.plot(x, y, color=RED, lw=1.8, alpha=0.7)
    for xx, yy, ll, hh, role in zip(x, y, lo, hi, [r[3] for r in rows]):
        marker = {"exploratory": "o", "secondary": "s", "primary": "D"}[role]
        face = "white" if role == "exploratory" else RED
        ax.errorbar(xx, yy, yerr=[[yy - ll], [hh - yy]], fmt=marker, mfc=face, mec=RED,
                    color=RED, capsize=3.5, ms=6.5, lw=1.4)
    ax.axhline(0, color="#334155", lw=1)
    ax.axvline(9.174, color="#94A3B8", ls=":", lw=1)
    ax.set_xlabel("training tokens (billions)")
    ax.set_ylabel("SALL - Dense NLL (nat / token)\nlower is better")
    ax.set_title("C | Language-prediction cost guard", loc="left", fontweight="bold")
    style(ax)

    legend = [
        Line2D([], [], marker="o", mfc="white", mec=GRAY, color="none", label="0-10B exploratory"),
        Line2D([], [], marker="s", color=GRAY, label="15B secondary"),
        Line2D([], [], marker="D", color=GRAY, label="21B primary"),
        Line2D([], [], color="#94A3B8", ls=":", label="SALL branch at 9.174B"),
    ]
    fig.legend(handles=legend, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.56, 0.955))
    fig.suptitle("The checkpoint trajectory is mixed, not a monotonic semantic improvement",
                 x=0.02, ha="left", fontsize=14, fontweight="bold")
    fig.text(0.02, -0.01,
             "Intervals are pointwise paired bootstrap intervals. Checkpoints are repeated observations from one training lineage, not independent training seeds; "
             "the 10B continuation branch prevents a smooth causal time interpretation.", fontsize=9, color="#475569")
    fig.tight_layout(rect=[0, 0.055, 1, 0.86])
    save(fig, "02_checkpoint_trajectory_and_cost")


def metric(rows, case, layer, pooling, key):
    row = next(r for r in rows if r["case"] == case and r["layer"] == layer and r["pooling"] == pooling)
    return row[key]


def fig_scope_geometry():
    p21 = load("e06_primary")
    p15 = load("e07_primary")
    g21 = load("e06_geometry")
    s21 = load("e06_semantic")
    fig, axes = plt.subplots(2, 2, figsize=(12.4, 8.3))

    # A N8.
    ax = axes[0, 0]
    groups = [("15B", p15["N8_v1"], ["15b_dense", "15b_sall_original"]),
              ("21B", p21["N8_v1"], ["21b_dense", "21b_sall_original", "21b_s7_reweighted"])]
    positions = []; labels = []; values = []; colors = []
    cursor = 0
    for label, rows, cases in groups:
        for case in cases:
            positions.append(cursor); labels.append(f"{label}\n{MODEL_NAME[case]}")
            values.append(100 * metric(rows, case, 8, "mean", "test_accuracy")); colors.append(MODEL_COLOR[case]); cursor += 1
        cursor += 0.55
    ax.bar(positions, values, color=colors, width=0.75)
    ax.set_ylim(70, 90)
    ax.set_xticks(positions, labels)
    ax.set_ylabel("N8 test accuracy (%)")
    ax.set_title("A | Domain organization\nlayer-8 mean", loc="left", fontweight="bold")
    style(ax)

    # B PAWS.
    ax = axes[0, 1]
    positions = []; labels = []; values = []; colors = []; cursor = 0
    for label, rows, cases in [("15B", p15["PAWS_wiki_final"], ["15b_dense", "15b_sall_original"]),
                               ("21B", p21["PAWS_wiki_final"], ["21b_dense", "21b_sall_original", "21b_s7_reweighted"])]:
        for case in cases:
            positions.append(cursor); labels.append(f"{label}\n{MODEL_NAME[case]}")
            values.append(metric(rows, case, 8, "mean", "test_auroc")); colors.append(MODEL_COLOR[case]); cursor += 1
        cursor += 0.55
    ax.bar(positions, values, color=colors, width=0.75)
    ax.axhline(0.5, color="#475569", ls="--", lw=1)
    ax.set_ylim(0.5, 0.70)
    ax.set_xticks(positions, labels)
    ax.set_ylabel("PAWS cosine AUROC")
    ax.set_title("B | Natural-pair similarity\nlayer-8 mean", loc="left", fontweight="bold")
    style(ax)

    # C geometry CKA, same layer at n=512.
    ax = axes[1, 0]
    cka_rows = [r for r in g21["n8_cka_first_pc_and_nested_sizes"]
                if r["pooling"] == "last" and r["layer"] in (4, 8) and r["n"] == 512
                and r["left"] == "21b_dense"]
    names = []; raw = []; removed = []
    for right in ["21b_sall_original", "21b_s7_reweighted"]:
        for layer in [4, 8]:
            row = next(r for r in cka_rows if r["right"] == right and r["layer"] == layer)
            names.append(f"{MODEL_NAME[right]}\nL{layer}")
            raw.append(row["raw"]["u_corrected"])
            removed.append(row["fit_first_pc_removed"]["u_corrected"])
    x = np.arange(4); width = 0.35
    ax.bar(x - width / 2, raw, width, color="#64748B", label="raw")
    ax.bar(x + width / 2, removed, width, color="#CBD5E1", edgecolor="#64748B", label="first PC removed")
    ax.set_ylim(0, 1)
    ax.set_xticks(x, names)
    ax.set_ylabel("U-corrected linear CKA")
    ax.set_title("C | Geometry similarity to Dense\nN8 dev, last token", loc="left", fontweight="bold")
    ax.legend(frameon=False, fontsize=9)
    style(ax)

    # D semantic margin.
    ax = axes[1, 1]
    cases = ["21b_dense", "21b_sall_original", "21b_s7_reweighted"]
    x = np.arange(2); width = 0.24
    for j, case in enumerate(cases):
        vals = []
        for layer in [4, 8]:
            row = next(r for r in s21["semantic_margins"] if r["layer"] == layer and r["pooling"] == "last")
            vals.append(row["test_joint_mean_margin_by_case"][case])
        ax.bar(x + (j - 1) * width, vals, width, color=MODEL_COLOR[case], label=MODEL_NAME[case])
    ax.axhline(0, color="#334155", lw=1)
    ax.set_xticks(x, ["Layer 4", "Layer 8"])
    ax.set_ylabel("cos(same relation, new wording)\n- cos(opposite relation, same wording)")
    ax.set_title("D | Semantic-vs-template distance margin\npositive would favor semantics", loc="left", fontweight="bold")
    ax.legend(frameon=False, fontsize=9)
    style(ax)

    fig.suptitle("Different diagnostics describe different sides of the representation",
                 x=0.02, ha="left", fontsize=14, fontweight="bold")
    fig.text(0.02, 0.005,
             "N8 labels are publication categories; PAWS is an official-split cosine diagnostic; CKA measures relational geometry, not semantic quality. "
             "All 21B semantic margins remain below zero, even when a model is less negative than Dense.", fontsize=9, color="#475569")
    fig.tight_layout(rect=[0, 0.04, 1, 0.94])
    save(fig, "03_scope_geometry_and_semantic_margin")


def fig_sae_observer():
    conditions = []
    for tokens, data in [(15, load("e07_observer")), (21, load("e06_observer"))]:
        for row in data["conditions"]:
            if row["panel"] != "P_rel_v2":
                continue
            if tokens == 15 and row["case"] != "15b_sall_original":
                continue
            conditions.append((tokens, row))
    order = [
        (15, "15b_sall_original", 4), (15, "15b_sall_original", 8),
        (21, "21b_sall_original", 4), (21, "21b_sall_original", 8),
        (21, "21b_s7_reweighted", 8),
    ]
    selected = [next(r for t, r in conditions if (t, r["case"], r["human_layer"]) == key) for key in order]
    labels = ["15B SALL\nL4", "15B SALL\nL8", "21B SALL\nL4", "21B SALL\nL8", "21B S7\nL8"]
    colors = [LIGHT, LIGHT, SALL, SALL, S7]
    edge = [SALL] * 4 + [S7]

    positive = [r["rank_tail_and_fidelity"]["pre_topk_positive_count_quantiles"][1] for r in selected]
    gap = [100 * r["rank_tail_and_fidelity"]["relative_rank32_33_gap_quantiles"][1] for r in selected]
    mass = [100 * r["rank_tail_and_fidelity"]["top32_positive_mass_fraction_quantiles"][1] for r in selected]
    rrmse = [100 * r["rank_tail_and_fidelity"]["pooled_reconstruction_fidelity"]["test_joint/last"]["relative_rms_error"] for r in selected]

    fig, axes = plt.subplots(2, 2, figsize=(12.4, 7.7))
    values = [positive, gap, mass, rrmse]
    titles = [
        "A | Positive pre-TopK scores (median)",
        "B | Relative rank-32 / rank-33 gap (median)",
        "C | Top-32 share of positive score mass (median)",
        "D | P test-joint reconstruction error (last-token RRMSE)",
    ]
    ylabels = ["count out of 30,000", "%", "%", "%"]
    for ax, vals, title, ylabel in zip(axes.ravel(), values, titles, ylabels):
        x = np.arange(len(vals))
        ax.bar(x, vals, color=colors, edgecolor=edge, linewidth=1.2)
        ax.set_xticks(x, labels)
        ax.set_ylabel(ylabel)
        ax.set_title(title, loc="left", fontweight="bold")
        style(ax)
    axes[0, 0].set_yscale("log")
    axes[0, 0].set_ylim(30, 10000)
    axes[0, 1].axhline(10, color="#94A3B8", ls=":", lw=1)
    axes[1, 0].axhline(100, color="#94A3B8", ls=":", lw=1)
    fig.suptitle("Top-K=32 is an imposed budget, not an observed 32-dimensional cutoff",
                 x=0.02, ha="left", fontsize=14, fontweight="bold")
    fig.text(0.02, 0.005,
             "All activation statistics are full encoder scores before Top-K on the same fixed P panel. Rank gaps and mass fractions do not count semantic features. "
             "RRMSE shows that the online dictionary is a partial observer rather than a lossless readout.", fontsize=9, color="#475569")
    fig.tight_layout(rect=[0, 0.04, 1, 0.94])
    save(fig, "04_sae_activation_spectrum_and_fidelity")


def fig_intuition():
    fig, ax = plt.subplots(figsize=(13.4, 7.1))
    ax.set_xlim(0, 13.4); ax.set_ylim(0, 7.1); ax.axis("off")
    ax.text(0.25, 6.72, "Intuition hypothesis: what would a more reusable representation look like?",
            fontsize=16, fontweight="bold")
    ax.text(12.95, 6.75, "HYPOTHESIS, NOT EVIDENCE", ha="right", fontsize=9, color=RED,
            bbox={"boxstyle": "round,pad=.25", "fc": "#FDE8E4", "ec": RED})

    panels = [(0.35, 2.65, 5.9, 3.45, "Reusable semantic organization", "#E8F5F0"),
              (7.1, 2.65, 5.9, 3.45, "Surface / scale reorganization", "#EEF2F7")]
    for x, y, w, h, title, fc in panels:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=.12", fc=fc, ec="#94A3B8", lw=1.3))
        ax.text(x + 0.22, y + h - 0.38, title, fontsize=13, fontweight="bold")

    # Left: color is relation, marker is wording; semantic colors cluster across markers.
    rng = np.random.default_rng(7)
    centers = [(2.0, 4.15), (4.8, 4.65)]
    for rel, (cx, cy), color in zip(["R+", "R-"], centers, [SALL, RED]):
        for k, marker in enumerate(["o", "s", "^"]):
            pts = rng.normal([cx, cy], [0.18, 0.18], size=(4, 2)) + np.array([0.06 * k, -0.05 * k])
            ax.scatter(pts[:, 0], pts[:, 1], marker=marker, s=48, color=color, edgecolor="white", lw=0.5)
        ax.text(cx, cy - 0.7, rel, color=color, ha="center", fontweight="bold")
    ax.plot([3.35, 3.45], [3.25, 5.75], color="#334155", lw=1.5, ls="--")
    ax.text(3.4, 3.05, "one simple reader transfers\nacross wording", ha="center", fontsize=10)

    # Right: marker (wording) clusters, relation colors mix inside them.
    for k, (cx, cy), marker in zip(range(3), [(8.5, 4.1), (10.1, 5.0), (11.7, 4.0)], ["o", "s", "^"]):
        for color, dx in [(SALL, -0.10), (RED, 0.10)]:
            pts = rng.normal([cx + dx, cy], [0.17, 0.17], size=(4, 2))
            ax.scatter(pts[:, 0], pts[:, 1], marker=marker, s=48, color=color, edgecolor="white", lw=0.5)
    ax.text(10.1, 3.05, "large geometry change can still\ntrack wording, scale, or compression", ha="center", fontsize=10)

    # Main path vs observer path.
    y = 1.45
    boxes = [(0.55, y, 1.55, 0.62, "native write a", "#FFFFFF"),
             (3.0, y, 1.75, 0.62, "residual + MLP", "#FFFFFF"),
             (6.1, y, 1.25, 0.62, "SAE", "#FFFFFF"),
             (8.25, y, 1.25, 0.62, "z", "#FFFFFF"),
             (10.25, y, 1.25, 0.62, "a-hat", "#FFFFFF"),
             (12.0, y, 0.85, 0.62, "e", "#FFFFFF")]
    for x, yy, w, h, label, fc in boxes:
        ax.add_patch(FancyBboxPatch((x, yy), w, h, boxstyle="round,pad=.06", fc=fc, ec="#64748B", lw=1.2))
        ax.text(x + w / 2, yy + h / 2, label, ha="center", va="center", fontsize=11, fontweight="bold")
    ax.add_patch(FancyArrowPatch((2.1, y + .31), (3.0, y + .31), arrowstyle="->", mutation_scale=13, lw=1.7, color=DENSE))
    ax.text(2.55, y + .52, "normal model path", ha="center", fontsize=9)
    ax.add_patch(FancyArrowPatch((2.1, y + .16), (6.1, y + .16), arrowstyle="->", mutation_scale=13, lw=1.7, color=SALL,
                                 connectionstyle="arc3,rad=-.18"))
    ax.add_patch(FancyArrowPatch((7.35, y + .31), (8.25, y + .31), arrowstyle="->", mutation_scale=13, lw=1.5, color=SALL))
    ax.add_patch(FancyArrowPatch((9.5, y + .31), (10.25, y + .31), arrowstyle="->", mutation_scale=13, lw=1.5, color=SALL))
    ax.add_patch(FancyArrowPatch((11.5, y + .31), (12.0, y + .31), arrowstyle="->", mutation_scale=13, lw=1.5, color=GRAY))
    ax.text(7.3, 0.72, "P joint probe: reusable access | norm / CKA: geometry | rank tail + reconstruction: observer | intervention: actual use (not run)",
            ha="center", fontsize=10, color="#334155")
    ax.text(7.3, 0.34, "The SAE reconstruction is observed here; it is not fed into the normal MLP path.",
            ha="center", fontsize=10, color=RED)
    save(fig, "05_intuition_hypothesis_map")


def main():
    fig_main_p21b()
    fig_trajectory()
    fig_scope_geometry()
    fig_sae_observer()
    fig_intuition()
    manifest = {
        "status": "PASS",
        "scope": "CPU-only plotting from completed PASS JSON; no new model inference, fitting, resampling, or statistical test",
        "script": str(Path(__file__).resolve()),
        "script_sha256": sha256(Path(__file__).resolve()),
        "sources": {key: {"path": str(path), "sha256": sha256(path)} for key, path in SOURCES.items()},
        "outputs": sorted(str(path) for path in OUT.glob("*.png")) + sorted(str(path) for path in OUT.glob("*.pdf")),
        "colors": {"Dense": DENSE, "SALL": SALL, "S7": S7},
        "claim_boundaries": [
            "P last-token SALL-vs-Dense at 21B is the registered primary; all other plotted comparisons are secondary or diagnostic.",
            "Checkpoints are not independent seeds.",
            "CKA, norm, spectra, and SAE activation tails do not define semantic quality.",
            "The intuition map is a hypothesis diagram, not result evidence.",
        ],
    }
    (OUT / "figure_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()

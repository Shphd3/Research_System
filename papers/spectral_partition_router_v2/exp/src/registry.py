"""Canonical experiment registry for the v2 paper.

This file is intentionally metadata-only. It fixes the mapping between
experiment IDs, runner scripts, result directories, paper tables, and figures.
Runner scripts should read this registry instead of hard-coding output names.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ExperimentSpec:
    exp_id: str
    title: str
    role: str
    runner: str
    result_dir: str
    metrics_csv: str
    summary_md: str
    paper_section_label: str
    table_tex: str
    table_label: str
    figures: Tuple[Tuple[str, str], ...]


EXPERIMENTS = {
    "E1": ExperimentSpec(
        exp_id="E1",
        title="Static uniform dispatch",
        role="Tests whether SPR builds equal-mass cells and generalizes from calibration to holdout.",
        runner="exp/run_static_dispatch.py",
        result_dir="exp/results/e1_static_dispatch",
        metrics_csv="exp/results/e1_static_dispatch/metrics.csv",
        summary_md="exp/results/e1_static_dispatch/summary.md",
        paper_section_label="sec:exp-static-dispatch",
        table_tex="latex/tables/e1_static_dispatch.tex",
        table_label="tab:e1_static_dispatch",
        figures=(
            ("fig:e1_loadcv_by_method", "latex/figures/e1_loadcv_by_method.pdf"),
            ("fig:e1_holdout_gap", "latex/figures/e1_holdout_gap.pdf"),
        ),
    ),
    "E2": ExperimentSpec(
        exp_id="E2",
        title="Spectrally flat but non-spherical features",
        role="Separates covariance flatness from directional geometry and tests quantile calibration.",
        runner="exp/run_static_dispatch.py",
        result_dir="exp/results/e2_non_spherical",
        metrics_csv="exp/results/e2_non_spherical/metrics.csv",
        summary_md="exp/results/e2_non_spherical/summary.md",
        paper_section_label="sec:exp-non-spherical",
        table_tex="latex/tables/e2_non_spherical.tex",
        table_label="tab:e2_non_spherical",
        figures=(
            ("fig:e2_non_spherical_loadcv", "latex/figures/e2_non_spherical_loadcv.pdf"),
            ("fig:e2_covariance_vs_load", "latex/figures/e2_covariance_vs_load.pdf"),
        ),
    ),
    "E3": ExperimentSpec(
        exp_id="E3",
        title="Expert-weight-guided partitioning",
        role="Tests whether expert spectral prototypes choose useful split directions without guaranteeing mass.",
        runner="exp/run_expert_guided.py",
        result_dir="exp/results/e3_expert_guided",
        metrics_csv="exp/results/e3_expert_guided/metrics.csv",
        summary_md="exp/results/e3_expert_guided/summary.md",
        paper_section_label="sec:exp-expert-guided",
        table_tex="latex/tables/e3_expert_guided.tex",
        table_label="tab:e3_expert_guided",
        figures=(
            ("fig:e3_prototype_spread", "latex/figures/e3_prototype_spread.pdf"),
            ("fig:e3_alignment_vs_loadcv", "latex/figures/e3_alignment_vs_loadcv.pdf"),
        ),
    ),
    "E4": ExperimentSpec(
        exp_id="E4",
        title="Feature partition quality",
        role="Tests whether equal-mass cells preserve latent feature structure using evaluation-only labels.",
        runner="exp/run_feature_partition_quality.py",
        result_dir="exp/results/e4_feature_partition",
        metrics_csv="exp/results/e4_feature_partition/metrics.csv",
        summary_md="exp/results/e4_feature_partition/summary.md",
        paper_section_label="sec:exp-feature-partition",
        table_tex="latex/tables/e4_feature_partition.tex",
        table_label="tab:e4_feature_partition",
        figures=(
            ("fig:e4_nmi_purity", "latex/figures/e4_nmi_purity.pdf"),
            ("fig:e4_within_cell_variance", "latex/figures/e4_within_cell_variance.pdf"),
        ),
    ),
    "E5": ExperimentSpec(
        exp_id="E5",
        title="Controlled MoE training dynamics",
        role="Tests whether calibrated partitions are useful and preserved during controlled training.",
        runner="exp/run_training_dynamics.py",
        result_dir="exp/results/e5_training_dynamics",
        metrics_csv="exp/results/e5_training_dynamics/metrics.csv",
        summary_md="exp/results/e5_training_dynamics/summary.md",
        paper_section_label="sec:exp-training-dynamics",
        table_tex="latex/tables/e5_training_dynamics.tex",
        table_label="tab:e5_training_dynamics",
        figures=(
            ("fig:e5_loss_curves", "latex/figures/e5_loss_curves.pdf"),
            ("fig:e5_route_nmi", "latex/figures/e5_route_nmi.pdf"),
            ("fig:e5_flip_rate", "latex/figures/e5_flip_rate.pdf"),
            ("fig:e5_margin_p05", "latex/figures/e5_margin_p05.pdf"),
        ),
    ),
    "E6": ExperimentSpec(
        exp_id="E6",
        title="Ablations",
        role="Audits sensitivity to calibration size, dimension, expert count, policies, and drift.",
        runner="exp/run_ablations.py",
        result_dir="exp/results/e6_ablations",
        metrics_csv="exp/results/e6_ablations/metrics.csv",
        summary_md="exp/results/e6_ablations/summary.md",
        paper_section_label="sec:exp-ablations",
        table_tex="latex/tables/e6_ablations.tex",
        table_label="tab:e6_ablations",
        figures=(
            ("fig:e6_calibration_size", "latex/figures/e6_calibration_size.pdf"),
            ("fig:e6_policy_ablation", "latex/figures/e6_policy_ablation.pdf"),
        ),
    ),
}


def describe(exp_id: str) -> str:
    spec = EXPERIMENTS[exp_id]
    lines = [
        f"{spec.exp_id}: {spec.title}",
        f"role: {spec.role}",
        f"runner: {spec.runner}",
        f"result_dir: {spec.result_dir}",
        f"metrics_csv: {spec.metrics_csv}",
        f"summary_md: {spec.summary_md}",
        f"paper_section_label: {spec.paper_section_label}",
        f"table: {spec.table_label} -> {spec.table_tex}",
        "figures:",
    ]
    for label, path in spec.figures:
        lines.append(f"- {label} -> {path}")
    return "\n".join(lines)


def expected_outputs(exp_id: str) -> Tuple[str, ...]:
    spec = EXPERIMENTS[exp_id]
    return (spec.metrics_csv, spec.summary_md, spec.table_tex) + tuple(
        path for _, path in spec.figures
    )


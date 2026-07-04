# Experiment Registry

This file fixes the paper-facing mapping between experiment IDs, runner
scripts, result directories, tables, and figures. Do not introduce new output
names in runner scripts without updating this registry and
`exp/src/registry.py`.

| ID | Paper subsection | Runner | Result directory | Table label / file | Figure labels / files |
|---|---|---|---|---|---|
| E1 | `sec:exp-static-dispatch` | `exp/run_static_dispatch.py` | `exp/results/e1_static_dispatch/` | `tab:e1_static_dispatch` / `latex/tables/e1_static_dispatch.tex` | `fig:e1_loadcv_by_method` / `latex/figures/e1_loadcv_by_method.pdf`; `fig:e1_holdout_gap` / `latex/figures/e1_holdout_gap.pdf` |
| E2 | `sec:exp-non-spherical` | `exp/run_static_dispatch.py` | `exp/results/e2_non_spherical/` | `tab:e2_non_spherical` / `latex/tables/e2_non_spherical.tex` | `fig:e2_non_spherical_loadcv` / `latex/figures/e2_non_spherical_loadcv.pdf`; `fig:e2_covariance_vs_load` / `latex/figures/e2_covariance_vs_load.pdf` |
| E3 | `sec:exp-expert-guided` | `exp/run_expert_guided.py` | `exp/results/e3_expert_guided/` | `tab:e3_expert_guided` / `latex/tables/e3_expert_guided.tex` | `fig:e3_prototype_spread` / `latex/figures/e3_prototype_spread.pdf`; `fig:e3_alignment_vs_loadcv` / `latex/figures/e3_alignment_vs_loadcv.pdf` |
| E4 | `sec:exp-feature-partition` | `exp/run_feature_partition_quality.py` | `exp/results/e4_feature_partition/` | `tab:e4_feature_partition` / `latex/tables/e4_feature_partition.tex` | `fig:e4_nmi_purity` / `latex/figures/e4_nmi_purity.pdf`; `fig:e4_within_cell_variance` / `latex/figures/e4_within_cell_variance.pdf` |
| E5 | `sec:exp-training-dynamics` | `exp/run_training_dynamics.py` | `exp/results/e5_training_dynamics/` | `tab:e5_training_dynamics` / `latex/tables/e5_training_dynamics.tex` | `fig:e5_loss_curves` / `latex/figures/e5_loss_curves.pdf`; `fig:e5_route_nmi` / `latex/figures/e5_route_nmi.pdf`; `fig:e5_flip_rate` / `latex/figures/e5_flip_rate.pdf`; `fig:e5_margin_p05` / `latex/figures/e5_margin_p05.pdf` |
| E6 | `sec:exp-ablations` | `exp/run_ablations.py` | `exp/results/e6_ablations/` | `tab:e6_ablations` / `latex/tables/e6_ablations.tex` | `fig:e6_calibration_size` / `latex/figures/e6_calibration_size.pdf`; `fig:e6_policy_ablation` / `latex/figures/e6_policy_ablation.pdf` |

## Result Contract

Each experiment directory must contain:

```text
metrics.csv
summary.md
figures/*.pdf
figures/*.png
```

Paper-facing tables are generated separately under `latex/tables/` by
`exp/make_paper_tables.py`.

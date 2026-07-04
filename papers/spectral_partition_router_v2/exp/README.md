# Spectral Partition Router v2 Experiments

This directory contains the execution plan for the v2 paper:

**Spectral Partition Routing for Uniform Feature Dispatch in Mixture-of-Experts**

The target is not generic batch load balancing. The target is **uniform feature dispatch**:

\[
P(g(X)=e)=1/E, \quad e=1,\ldots,E.
\]

A method is considered non-cheating if it may use unlabeled calibration features and model-internal expert weights, but may not use feature labels, task labels, evaluation labels, or current-batch expert counts.

## Core router family

- `SPR-Fixed`: recursive quantile partition using fixed spectral axes.
- `SPR-Local`: recursive quantile partition using unsupervised locality directions.
- `SPR-Expert`: recursive quantile partition using expert-weight-derived spectral prototypes to choose split directions.
- `SPR-init-linear`: use SPR cell centers to initialize a learnable linear top-1 router.
- `Frozen-SPR`: use the calibrated tree as the router throughout training.
- `SlowUpdate-SPR`: recalibrate the tree infrequently with unlabeled moving-window features.

## Required experiment order

1. E1: static equal-mass dispatch on spectrally uniform features.
2. E2: static dispatch on spectrally flat but non-spherical features.
3. E3: expert-weight-guided partitioning.
4. E4: feature partition quality with held-out synthetic feature labels for evaluation only.
5. E5: controlled MoE training dynamics.
6. E6: ablations.

The canonical mapping from experiment IDs to scripts, result directories,
tables, and figures is:

```text
EXPERIMENT_REGISTRY.md
exp/src/registry.py
```

## Output contract

Each completed experiment writes:

```text
exp/results/<experiment_name>/metrics.csv
exp/results/<experiment_name>/summary.md
exp/results/<experiment_name>/figures/*.pdf
exp/results/<experiment_name>/figures/*.png
latex/figures/<paper_figure>.pdf
latex/tables/<paper_table>.tex
```

The current V2 full run has been executed for E1--E6.  All `metrics.csv`
files contain `run_mode=full`; paper-facing figures and tables have been
generated under `latex/figures/` and `latex/tables/`.

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

1. Static equal-mass dispatch on spectrally uniform features.
2. Static dispatch on spectrally flat but non-spherical features.
3. Expert-weight-guided partitioning.
4. Feature partition quality with held-out synthetic feature labels for evaluation only.
5. Controlled MoE training dynamics.
6. Ablations.

## Output contract

Each experiment should write:

```text
results/<experiment_name>/metrics.csv
results/<experiment_name>/summary.md
results/<experiment_name>/figures/*.pdf
results/<experiment_name>/figures/*.png
```

The paper draft intentionally contains no numeric results yet. Codex should fill results only after executing the experiments.

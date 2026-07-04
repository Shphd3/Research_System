# E1: Static uniform dispatch

## What this experiment tests

Tests whether SPR builds equal-mass cells and generalizes from calibration to holdout.

## Result summary

- Across the full E1 sweep, the best SPR mean held-out LoadCV is 0.0340, versus 0.0855 for vanilla random linear routing.
- Balanced assignment is included only as a forced-count control; its exact batch balance is not a feature-only routing guarantee.
- The gap plot records the statistical calibration effect: quantile routers improve as node quantiles receive more calibration samples.

## Artifact map

- Metrics: `exp/results/e1_static_dispatch/metrics.csv`
- Paper table: `latex/tables/e1_static_dispatch.tex`
- Figures:
  - `latex/figures/e1_loadcv_by_method.pdf`
  - `latex/figures/e1_holdout_gap.pdf`

## Rows

720 metric rows were written.

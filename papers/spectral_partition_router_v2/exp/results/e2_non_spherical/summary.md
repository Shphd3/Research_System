# E2: Spectrally flat but non-spherical features

## What this experiment tests

Separates covariance flatness from directional geometry and tests quantile calibration.

## Result summary

- Whitened non-spherical datasets have mean covariance condition number 1.000, but prototype-only routing still reaches mean held-out LoadCV 0.3076.
- SPR's best mean held-out LoadCV is 0.0619, showing that quantile calibration, not covariance flatness alone, controls mass.
- Axis-supported data remains a useful boundary case because deterministic feature routers cannot split truly identical atoms without tie-breaking.

## Artifact map

- Metrics: `exp/results/e2_non_spherical/metrics.csv`
- Paper table: `latex/tables/e2_non_spherical.tex`
- Figures:
  - `latex/figures/e2_non_spherical_loadcv.pdf`
  - `latex/figures/e2_covariance_vs_load.pdf`

## Rows

180 metric rows were written.

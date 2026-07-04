# E4: Feature partition quality

## What this experiment tests

Tests whether equal-mass cells preserve latent feature structure using evaluation-only labels.

## Result summary

- On the medium latent-feature regime, SPR-Local reaches mean route-feature NMI 0.0345, compared with 0.0305 for SPR-Fixed.
- Balanced assignment has exact count control but only NMI 0.0071, so count balance alone is not feature partition quality.
- Within-cell variance provides the geometry-side audit: lower variance means the route cell is less arbitrary inside the whitened feature space.

## Artifact map

- Metrics: `exp/results/e4_feature_partition/metrics.csv`
- Paper table: `latex/tables/e4_feature_partition.tex`
- Figures:
  - `latex/figures/e4_nmi_purity.pdf`
  - `latex/figures/e4_within_cell_variance.pdf`

## Rows

90 metric rows were written.

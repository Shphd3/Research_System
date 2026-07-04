# E3: Expert-weight-guided partitioning

## What this experiment tests

Tests whether expert spectral prototypes choose useful split directions without guaranteeing mass.

## Result summary

- SPR-Expert obtains mean held-out LoadCV 0.0180, while prototype-only top-1 routing obtains 0.1106.
- Mean SPR-Expert cell-to-prototype alignment is 0.8955; expert weights provide geometry but not the mass guarantee.
- The alignment-vs-load plot separates the two effects: aligned prototype cells can still be imbalanced without quantile thresholds.

## Artifact map

- Metrics: `exp/results/e3_expert_guided/metrics.csv`
- Paper table: `latex/tables/e3_expert_guided.tex`
- Figures:
  - `latex/figures/e3_prototype_spread.pdf`
  - `latex/figures/e3_alignment_vs_loadcv.pdf`

## Rows

90 metric rows were written.

# Geometry-Aware Spectral Partition Routing v2.1 Experiments

This folder defines the next experimental iteration after V2.

The V2 result audit showed:

```text
Equal-mass dispatch: mostly solved by recursive quantiles.
Meaningful feature partition: only works when geometry / expert weights are informative.
Training preservation: not solved by naive recalibration.
```

V2.1 therefore studies **geometry-aware, margin-preserved dispatch**.

## Research target

Construct a non-cheating router satisfying three measurable properties:

1. **Equal mass**:
   \[
   P(g(X)=e)=1/E.
   \]
2. **Feature coherence**:
   routes preserve latent feature structure when such structure exists.
3. **Training preservation**:
   routing remains stable under controlled feature drift / optimization.

## Method family

- `SPR-Mass`: recursive quantile split with fixed or seeded random axes.
- `GA-SPR-Local`: quantile split with unlabeled locality-aware directions.
- `GA-SPR-Expert`: quantile split with sign-invariant expert-weight geometry.
- `GA-SPR-ExpertLocal`: expert-guided grouping plus local feature refinement.
- `GA-SPR-MarginUpdate`: margin-aware update / recalibration with route-change budget.

## Required corrections from V2

- Handle SVD sign ambiguity.
- Implement true fixed-basis routing or rename random-axis baseline.
- Add feature-derived tie handling for discrete data.
- Rename forced-count baseline correctly.
- Add true learnable-router baseline if claiming training dynamics.
- Treat slow update as a negative baseline unless margin-aware safeguards are added.

## Output contract

Each experiment should write:

```text
exp/results/<experiment_id>/metrics.csv
exp/results/<experiment_id>/summary.md
latex/tables/<experiment_id>.tex
latex/figures/<experiment_id>_*.pdf
latex/figures/<experiment_id>_*.png
```

Do not put numbers into the paper until the corresponding experiment has been run.

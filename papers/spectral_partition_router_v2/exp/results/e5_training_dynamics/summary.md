# E5: Controlled MoE training dynamics

## What this experiment tests

Tests whether calibrated partitions are useful and preserved during controlled training.

## Result summary

- At the final epoch, Frozen-SPR validation MSE is 12.4721, compared with 12.6132 for vanilla fixed linear routing.
- SlowUpdate-SPR's final route flip rate under controlled drift is 0.8882; this measures adaptation, not semantic expert discovery.
- The training audit supports the limited claim that geometry-aware partitions can make the controlled expert task easier when the latent feature classes match the routing geometry.

## Artifact map

- Metrics: `exp/results/e5_training_dynamics/metrics.csv`
- Paper table: `latex/tables/e5_training_dynamics.tex`
- Figures:
  - `latex/figures/e5_loss_curves.pdf`
  - `latex/figures/e5_route_nmi.pdf`
  - `latex/figures/e5_flip_rate.pdf`
  - `latex/figures/e5_margin_p05.pdf`

## Rows

2835 metric rows were written.

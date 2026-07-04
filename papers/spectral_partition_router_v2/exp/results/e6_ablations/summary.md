# E6: Ablations

## What this experiment tests

Audits sensitivity to calibration size, dimension, expert count, policies, and drift.

## Result summary

- Calibration-size sensitivity is visible: mean held-out LoadCV ranges from 0.0894 to 0.0245 across the tested sizes.
- The forced-count control reaches NMI 0.0123, while the feature-router control reaches NMI 0.0311; this keeps count balance separate from feature geometry.
- The ablations are boundary evidence: they identify when SPR is statistically reliable, not a guarantee under arbitrary distribution shift.

## Artifact map

- Metrics: `exp/results/e6_ablations/metrics.csv`
- Paper table: `latex/tables/e6_ablations.tex`
- Figures:
  - `latex/figures/e6_calibration_size.pdf`
  - `latex/figures/e6_policy_ablation.pdf`

## Rows

130 metric rows were written.

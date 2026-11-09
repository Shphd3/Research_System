# Summary: A01_01 Common Operator Identifiability Full Run

## Conclusion

The controlled full run supports the mechanism-conditioned view of common
operators. The primary metric, `criterion_winner_diversity`, is 4: activation
PCA, group mean, gradient intersection, and feedback drift each win at least
one primary criterion under its matching regime.

This falsifies the local single-estimator route for this controlled setting. A
common operator should not be treated as "the top hidden-state direction" by
default. It must be indexed by the mechanism being tested: activation variance,
mean structure, cross-group gradient redundancy, or feedback drift.

## Primary Metric

`criterion_winner_diversity` counts distinct estimator families that win the
three primary criteria across regimes:

- `subspace_alignment`: recovery of the known common projector \(P_c^*\).
- `shared_loss_sensitivity`: increase in shared-target ridge loss after
  removing \(P h\).
- `gradient_overlap_reduction`: reduction in average pairwise group-gradient
  cosine after removing \(P h\).

Observed value: 4 distinct winners.

Decision: pass for criterion dependence; fail for a universal common estimator.

## Setup

Synthetic hidden states are generated with known \(P_c^*=AA^\top\):

\[
h = s_c A z_c + s_u B_g z_g + s_n N z_n + \epsilon
\]

Configuration: hidden dimension 16, common rank 2, unique rank 2, six groups,
600 samples per group, ten seeds, and five regimes.

Compared estimators:

- activation PCA;
- group mean;
- gradient intersection;
- feedback drift;
- random control.

## Main Result Table

| Regime | Recovery winner | Shared-loss winner | Gradient-overlap winner | Interpretation |
|---|---|---|---|---|
| activation_dominant | activation_pca, 0.9999 | activation_pca, 1.9872 | activation_pca, 0.8260 | PCA works when common is the largest activation-variance object. |
| unique_dominant | gradient_intersection, 0.8378 | gradient_intersection, 1.9441 | gradient_intersection, 0.5401 | PCA fails as universal common when unique variance dominates. |
| mean_offset | group_mean, 0.9995 | activation_pca, 0.4166 | group_mean, 0.1457 | Mean-visible common is near-tied with PCA; do not overclaim this regime. |
| gradient_intersection | gradient_intersection, 0.9214 | gradient_intersection, 1.9600 | gradient_intersection, 0.6880 | Optimization common is recovered by the gradient criterion. |
| feedback_drift | feedback_drift, 1.0000 | feedback_drift, 1.9657 | feedback_drift, 0.0768 | Drift-visible common is a distinct estimator target; overlap effect is smaller. |

Random control never wins a primary aggregate criterion.

## Central Figures

![Criterion winners by regime](figures/operator_rank_disagreement.png)

This figure tests whether the same estimator wins every criterion. It shows
four non-random winner families, so the single-common-estimator hypothesis is
not supported in this controlled audit.

![Subspace alignment by regime](figures/subspace_alignment_by_regime.png)

This figure tests recovery of the known common projector. Recovery depends on
which mechanism makes common visible: activation PCA wins the activation regime,
group mean wins the mean-offset regime, gradient intersection wins the
optimization regimes, and feedback drift wins the feedback regime.

![Gradient overlap reduction by regime](figures/gradient_overlap_reduction_by_regime.png)

This figure tests the optimization criterion. Gradient intersection strongly
reduces cross-group gradient overlap in `unique_dominant` and
`gradient_intersection`, while activation PCA can be neutral or harmful when
activation variance is mostly unique.

## Claim Boundary

This run supports: common is an operator family conditioned on the mechanism
criterion in controlled settings with known \(P_c^*\).

This run does not support: a real-DCLM common operator, a preservation rescue,
layerwise common roles, shared-expert utility, or a residualized MoE method
claim.

Important limitation: `mean_offset` has close competition between group mean
and activation PCA. Its winner pattern should be treated as weak evidence for
mean-specific common, not as a strong estimator ordering.

## Next Decision

Move to `01_03_gradient_common_vs_activation_common_anchor.md`: test whether
the optimization-relevant common in the project records is better modeled by
activation covariance or gradient covariance. Use gradient intersection as the
first candidate for optimization-common tests, but keep activation and feedback
estimators as rival explanations.


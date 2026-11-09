# Detailed Record: A01_01 Common Operator Identifiability Full Run

## 1. Result

The controlled full run supports the hypothesis that common is not a single
criterion-free hidden-state object. The primary metric
`criterion_winner_diversity` is 4, meaning four estimator families win across
the primary criteria and regimes.

Supported interpretation: common should be represented as a family of
operators \(P_c^{m}\) indexed by mechanism \(m\), such as activation variance,
mean structure, gradient redundancy, or feedback drift.

Rejected for this controlled setting: a universal estimator that identifies
common from hidden-state geometry alone.

## 2. Protocol Alignment

Primary anchor:
`Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/01_01_common_operator_identifiability_anchor.md`

Secondary anchor:
`Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/01_02_ground_truth_projector_recovery_anchor.md`

Protocol:
`Projects/from-attention-to-search/main/experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/protocol.md`

Approval status: user requested execution on 2026-06-29.

## 3. Reproduction

Working directory:

```bash
/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run
```

Command:

```bash
python scripts/run_common_operator_full_run.py --outdir .
```

Runtime: local CPU run; no cluster job id.

## 4. Data Generation

Each regime generates synthetic hidden states with known common projector
\(P_c^*=AA^\top\):

\[
h = s_c A z_c + s_u B_g z_g + s_n N z_n + \epsilon
\]

Objects:

- \(A\): orthonormal common basis, rank 2.
- \(B_g\): group-specific unique basis, rank 2.
- \(z_c\): shared latent.
- \(z_g\): group-specific latent.
- \(N z_n\): nuisance noise.
- \(g\): group label.

Shared targets depend on \(z_c\). Rare targets depend on \(z_g\). Group gradients
are computed for a zero linear readout, giving:

\[
G_g=\mathbb{E}[\delta_g h^\top \mid g]
\]

Feedback drift is simulated as a checkpoint-to-checkpoint hidden-state
difference with regime-specific common and unique drift strengths.

## 5. Configuration

| Item | Value |
|---|---|
| hidden dimension | 16 |
| common rank | 2 |
| unique rank | 2 |
| groups | 6 |
| samples per group | 600 |
| seeds | 0-9 |
| regimes | activation_dominant, unique_dominant, mean_offset, gradient_intersection, feedback_drift |
| estimators | activation_pca, group_mean, gradient_intersection, feedback_drift, random_control |

Full configuration is stored in `tables/run_config.json`.

## 6. Metrics

`subspace_alignment` measures recovery of the known common basis:

\[
\mathrm{align}(\hat U,A)=\frac{1}{k}\|A^\top \hat U\|_F^2
\]

`shared_loss_sensitivity` measures how much shared-target ridge loss increases
after removing candidate common:

\[
\Delta L_c(P)=L_c((I-P)h)-L_c(h)
\]

`rare_loss_sensitivity` is the same intervention for rare targets. It is a
guard, not the primary decision metric.

`gradient_overlap_reduction` measures the change in average pairwise
group-gradient cosine:

\[
\Delta C(P)=C(G_g,G_{g'})-C(G_g^r(P),G_{g'}^r(P))
\]

where:

\[
G_g^r(P)=\mathbb{E}[\delta_g ((I-P)h)^\top \mid g]
\]

## 7. Aggregate Results

| Regime | Criterion | Winner | Winner mean | Runner up | Runner-up mean | Winner seed fraction |
|---|---|---|---:|---|---:|---:|
| activation_dominant | subspace_alignment | activation_pca | 0.9999 | gradient_intersection | 0.9751 | 1.0 |
| activation_dominant | shared_loss_sensitivity | activation_pca | 1.9872 | gradient_intersection | 1.7242 | 1.0 |
| activation_dominant | gradient_overlap_reduction | activation_pca | 0.8260 | gradient_intersection | 0.7819 | 1.0 |
| unique_dominant | subspace_alignment | gradient_intersection | 0.8378 | random_control | 0.1758 | 1.0 |
| unique_dominant | shared_loss_sensitivity | gradient_intersection | 1.9441 | group_mean | 0.2955 | 1.0 |
| unique_dominant | gradient_overlap_reduction | gradient_intersection | 0.5401 | random_control | 0.0012 | 1.0 |
| mean_offset | subspace_alignment | group_mean | 0.9995 | activation_pca | 0.9992 | 0.7 |
| mean_offset | shared_loss_sensitivity | activation_pca | 0.4166 | group_mean | 0.4131 | 1.0 |
| mean_offset | gradient_overlap_reduction | group_mean | 0.1457 | activation_pca | 0.1455 | 0.6 |
| gradient_intersection | subspace_alignment | gradient_intersection | 0.9214 | random_control | 0.1758 | 1.0 |
| gradient_intersection | shared_loss_sensitivity | gradient_intersection | 1.9600 | group_mean | 0.3094 | 1.0 |
| gradient_intersection | gradient_overlap_reduction | gradient_intersection | 0.6880 | random_control | -0.0000 | 1.0 |
| feedback_drift | subspace_alignment | feedback_drift | 1.0000 | gradient_intersection | 0.5417 | 1.0 |
| feedback_drift | shared_loss_sensitivity | feedback_drift | 1.9657 | gradient_intersection | 1.5488 | 1.0 |
| feedback_drift | gradient_overlap_reduction | feedback_drift | 0.0768 | gradient_intersection | 0.0349 | 0.9 |

Primary metric:

```json
{
  "criterion_winner_diversity": 4,
  "distinct_winners": [
    "activation_pca",
    "feedback_drift",
    "gradient_intersection",
    "group_mean"
  ]
}
```

## 8. Visualization Results

### Figure 1: Criterion Winners By Regime

![Criterion winners by regime](figures/operator_rank_disagreement.png)

Question answered: Does one estimator win every primary criterion?

Metric definition: winner under `subspace_alignment`,
`shared_loss_sensitivity`, or `gradient_overlap_reduction`, averaged across
seeds within each regime.

Data source: `tables/operator_regime_summary.csv`.

How to read: columns are synthetic regimes; rows are primary criteria; cell
color and text show the winning estimator.

Observed result: four non-random estimator families win. Activation PCA wins
only when activation variance is the designed common signal. Gradient
intersection wins the unique-dominant and gradient-intersection regimes. Group
mean wins two weak mean-offset criteria. Feedback drift wins the feedback-drift
regime.

Take-home: common is criterion-dependent in this controlled audit.

Limitation: the figure shows aggregate winners, not effect-size uncertainty;
use the score table for near ties.

### Figure 2: Subspace Alignment

![Subspace alignment by regime](figures/subspace_alignment_by_regime.png)

Question answered: Which estimator recovers the known common projector
\(P_c^*\)?

Metric definition: \(\|A^\top \hat U\|_F^2/k\), where 1.0 is exact recovery.

Data source: `tables/operator_criterion_scores.csv`.

How to read: bars are seed means and error bars are seed standard deviations.

Observed result: recovery depends on how common is made visible. Activation
PCA recovers activation-dominant common; group mean and PCA both recover the
mean-offset common; gradient intersection recovers optimization-visible common;
feedback drift recovers drift-visible common.

Take-home: even with known \(P_c^*\), estimator validity is regime-conditioned.

Limitation: controlled recovery does not prove real-DCLM recovery.

### Figure 3: Gradient Overlap Reduction

![Gradient overlap reduction by regime](figures/gradient_overlap_reduction_by_regime.png)

Question answered: Which estimator removes redundant cross-group gradient
overlap?

Metric definition: average pairwise group-gradient cosine before
residualization minus after residualization.

Data source: `tables/operator_criterion_scores.csv`.

How to read: positive values mean candidate removal reduced cross-group
gradient overlap; negative values mean it increased overlap.

Observed result: gradient intersection strongly reduces overlap in
`unique_dominant` and `gradient_intersection`. Activation PCA works in
`activation_dominant` but can increase overlap when activation variance is not
the common optimization signal. Feedback drift has a smaller but positive
effect in the feedback regime.

Take-home: optimization-common is closer to gradient geometry than to raw
activation geometry in the non-activation regimes.

Limitation: the metric is a synthetic proxy for optimization interference; it
does not by itself prove training-speed or loss improvement.

## 9. Rival Explanations

R1: A single top activation direction is the common operator.

Status: weakened. Activation PCA wins only when the data generation makes
common the largest activation-variance object. It fails in unique-dominant and
gradient-intersection regimes.

R2: Estimator disagreement is only noise.

Status: weakened. Winner seed fractions are 1.0 for all primary winners except
the near-tied mean-offset and feedback-overlap cases.

R3: Gradient intersection only wins because the target is constructed to favor
it.

Status: partly open. The result validates gradient intersection as a positive
control for optimization-common, not as a universal real-data estimator. The
next anchor must test whether real project records exhibit the same gradient
signature.

R4: Feedback common is only drift magnitude.

Status: open. Feedback drift recovers the known drift-visible common in the
controlled run, but this does not prove feedback common is useful or harmful in
real DCLM.

## 10. Stage-Level Evidence

Generation: complete. Regime configs and random seeds are recorded in
`tables/run_config.json`.

Estimator validation: complete. All estimators return rank-2 projectors and
random control remains below real estimators on primary aggregate winners.

Scoring: complete. Per-seed scores are stored in
`tables/operator_criterion_scores.csv`.

Aggregation: complete. Primary winners are stored in
`tables/operator_regime_summary.csv` and
`tables/operator_winner_summary.json`.

## 11. Artifact Map

| Artifact | Path |
|---|---|
| runner | `scripts/run_common_operator_full_run.py` |
| protocol | `protocol.md` |
| Chinese protocol companion | `protocol_cn.md` |
| summary | `summary.md` |
| detailed record | `detailed.md` |
| run config | `tables/run_config.json` |
| per-seed scores | `tables/operator_criterion_scores.csv` |
| aggregate winner table | `tables/operator_regime_summary.csv` |
| winner summary | `tables/operator_winner_summary.json` |
| criterion winner figure | `figures/operator_rank_disagreement.png` |
| recovery figure | `figures/subspace_alignment_by_regime.png` |
| gradient figure | `figures/gradient_overlap_reduction_by_regime.png` |

## 12. Claim Boundary

Can claim: in a controlled setting with known \(P_c^*\), no single estimator is
the mechanism-free common operator.

Cannot claim: real-DCLM common identification, layerwise common roles,
preservation rescue, shared-expert utility, or residualized MoE improvement.

## 13. Next Decision

Proceed to `01_03_gradient_common_vs_activation_common_anchor.md`. The next
decision should ask whether optimization-relevant common in real or recorded
project artifacts is closer to activation covariance or gradient covariance.

Do not start `01_06_residualized_moe_input_split_anchor.md` until the estimator
boundary is tested beyond synthetic positive controls.


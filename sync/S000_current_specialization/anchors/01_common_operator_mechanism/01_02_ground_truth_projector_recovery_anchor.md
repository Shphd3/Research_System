# Ground-Truth Common Projector Recovery Anchor

Thinking Card source: [01_02_ground_truth_projector_recovery_thinking_card.md](01_02_ground_truth_projector_recovery_thinking_card.md)

## 1. Problem Definition

**Parent problem:** Common/residual split methods require a valid common
operator.

**Sharper subproblem:** Identify which estimator families can recover a known
common subspace under controlled nuisance.

**Decision question:** Which estimator family best recovers $P_c^*$, and is
that estimator also aligned with functional and optimization criteria?

**Not in scope:** Real-DCLM preservation rescue, layerwise estimator selection,
or MoE method construction.

## 2. Physical Priors

**P1:** An estimator that fails a known-$P_c^*$ positive control cannot support
a strong real-data common-operator claim.

**Meaning:** Real-data interpretation requires prior validation in a setting
where the answer is known.

**Could be wrong if:** Real-data common is qualitatively different from any
controlled construction, in which case this positive control is only a weak
screen.

**P2:** Estimator success depends on the mechanism that makes common visible.

**Meaning:** Activation PCA should win when common is high variance; gradient
intersection should win when common is an update intersection; group mean
should win only when common appears as a stable mean offset.

**Could be wrong if:** One estimator recovers $P_c^*$ across all regimes.

## 3. Falsifiable Hypotheses

**H1:** Gradient-intersection common is the most stable estimator for
optimization-relevant common.

**Supported if:** It has low recovery error and high gradient-overlap
reduction across nuisance regimes.

**Weakened if:** It has poor recovery or only wins when the target gradient is
constructed to favor it.

**H2:** Activation PCA is insufficient as a universal common estimator.

**Supported if:** It fails when unique variance or nuisance variance exceeds
common variance.

**Weakened if:** It recovers $P_c^*$ across all regimes.

## 4. Mathematical Model

**Objects:** Orthonormal common basis $A$, group-specific bases $B_g$, latent
variables $z_c,z_g,z_n$, and hidden states $h$.

**Core decomposition:**

$$
h = s_c A z_c + s_u B_g z_g + s_n N z_n + \epsilon
$$

with known:

$$
P_c^* = A A^\top
$$

**Mechanism relation:** Candidate projectors are compared by:

$$
\mathrm{align}(\hat P,P_c^*)=\frac{1}{k}\|A^\top \hat U\|_F^2
$$

**Observable metrics:** Recovery alignment, shared-loss sensitivity,
rare-loss sensitivity, and gradient-overlap reduction.

**Falsifier:** No estimator recovers $P_c^*$ beyond random controls across the
main regimes.

## 5. Computational Realization

**Input objects:** Synthetic hidden states, known common basis, group labels,
shared and rare targets, and simulated checkpoint drift.

**Computed variables:** Projectors from activation PCA, group means,
gradient-intersection matrices, feedback drift means, and random subspaces.

**Algorithm stages:** Generate multiple regimes and seeds; compute all
estimators; score estimator recovery and mechanism criteria; aggregate.

**Stage-local evidence:** Per-regime aggregate tables and figures.

**Expected artifacts:** `tables/operator_criterion_scores.csv`,
`tables/operator_regime_summary.csv`,
`figures/subspace_alignment_by_regime.png`,
`figures/operator_rank_disagreement.png`.

## 6. Minimal Falsification Tests

**Test:** Ground-truth common recovery under nuisance.

**Question:** Which estimator recovers $P_c^*$ under high unique variance,
mean-offset common, gradient-intersection common, and feedback-drift common?

**Intervention / comparison:** Compare estimator families against the known
projector in multiple synthetic regimes.

**Primary metric:** Mean `subspace_alignment` across regimes and seeds.

**Pass / fail / insufficient:** Pass for an estimator if it beats random
controls and remains compatible with gradient/loss guards. Fail if it only
wins one trivial regime or loses to random. Insufficient if regimes do not
separate estimator assumptions.

**Why it decides:** Later real-data analyses need an estimator whose validity
has been tested where the truth is known.

**Failure means:** The estimator operationalization is weakened; it does not
falsify common as a mechanism.

## 7. Current Evidence

**Observation:** Existing project records use several common estimators but do
not compare them against a known $P_c^*$. The A01_01/A01_02 controlled full
run now compares activation PCA, group mean, gradient intersection, feedback
drift, and random controls against known $P_c^*$.

**Measured result:** Recovery winners are regime-dependent: activation PCA
wins `activation_dominant` with alignment 0.9999; group mean wins
`mean_offset` with alignment 0.9995 but is near-tied with activation PCA;
gradient intersection wins `unique_dominant` with alignment 0.8378 and
`gradient_intersection` with alignment 0.9214; feedback drift wins
`feedback_drift` with alignment 1.0000.

**Interpretation:** Estimator recovery is valid only relative to the mechanism
that makes common observable. Gradient intersection is the best positive
control for optimization-visible common, while activation PCA is valid only
when common dominates activation variance.

**Boundary:** This anchor validates estimator families in controlled settings
only.

**Evidence links:** See `01_01_common_operator_identifiability_anchor.md`,
`../../experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/summary.md`,
and
`../../experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/detailed.md`.

## 8. Claim Boundary And Next Decision

**Can claim:** Candidate estimators recover known common structure only under
matching mechanism regimes; no estimator is universally best across all
criteria.

**Cannot claim:** That a recovered controlled estimator will rescue real-DCLM
preservation or improve MoE utility.

**Next decision:** Carry gradient intersection into `01_03` as the primary
optimization-common candidate, with activation PCA and feedback drift retained
as rival explanations.

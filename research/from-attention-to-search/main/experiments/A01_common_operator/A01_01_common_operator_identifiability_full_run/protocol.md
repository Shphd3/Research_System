# Protocol: A01_01 Common Operator Identifiability Full Run

## 0. Approval Snapshot

Approval status: user requested execution in the active goal on 2026-06-29.

Purpose: Test whether common is a single hidden-state geometry object or a
criterion-dependent operator family.

Primary anchor: `01_01_common_operator_identifiability_anchor.md`; secondary
anchor: `01_02_ground_truth_projector_recovery_anchor.md`.

Anchor decision question: Can common be identified from hidden-state geometry
and loss alone, or do different mechanism criteria select different
operators?

Anchor physical prior tested: Hidden-state variance, shared-prediction
causality, and cross-group gradient redundancy are distinct mechanisms.

Anchor core model term tested: Candidate projectors \(P\) applied to hidden
states \(h\) and gradient input factors.

Anchor falsifier: One estimator family wins recovery, shared-loss sensitivity,
and gradient-overlap reduction across all regimes.

Experiment role: root-cause / metric audit.

Primary metric from anchor: `criterion_winner_diversity`.

Claim boundary from anchor: The run can decide estimator criterion dependence
in controlled synthetic regimes; it cannot prove a real-DCLM common operator or
a working MoE method.

Minimal setup: Generate hidden states with known \(P_c^*\) and compare candidate
projectors.

Basic configuration: six groups, hidden dimension 16, common rank 2, ten seeds,
five regimes, 600 samples per group.

Conditions to run: activation-dominant, unique-dominant, mean-offset,
gradient-intersection, and feedback-drift regimes.

Pass: More than one estimator family wins across the main criteria, and the
winner pattern is stable across seeds.

Fail: One estimator family wins all main criteria across regimes.

Insufficient: Estimator scores are near random or unstable across seeds.

Cannot claim: real-DCLM preservation rescue, layerwise common role, shared
expert utility, or residualized MoE improvement.

Approval decision: execute the controlled full run.

## 1. Anchor Alignment

Decision question: Can common be selected by one hidden-state estimator, or is
it mechanism-conditioned?

Physical prior tested: activation common and optimization common can differ.

Core model term tested: \(P h\) and \(G_g^r(P)\).

Falsifier: a single estimator dominates all criteria.

Claim boundary: controlled estimator evidence only.

## 2. Tested Hypothesis

H1: Estimator rankings differ across recovery, shared-loss sensitivity, and
gradient-overlap reduction.

H2: Activation PCA is not a universal common estimator.

H3: Gradient-intersection common is more aligned with optimization-relevant
gradient-overlap reduction than activation PCA in at least one nontrivial
regime.

## 3. Rival Explanations

R1: A single top activation direction is the common operator.

R2: Estimator disagreement is just noise or invalid group labels.

R3: Gradient-intersection common only wins because the synthetic target is
constructed to favor it.

R4: Feedback common is only drift magnitude, not a common operator.

## 4. Data / Model / Algorithm / Objective

Synthetic hidden states are generated as:

\[
h = s_c A z_c + s_u B_g z_g + s_n N z_n + \epsilon
\]

with known \(P_c^*=AA^\top\).

Shared targets depend on \(z_c\) and rare targets depend on \(z_g\). Gradients are
computed for a zero linear readout, so the group-conditioned update has the
outer-product form:

\[
G_g=\mathbb{E}[\delta_g h^\top \mid g]
\]

Candidate projectors:

- activation PCA;
- group mean;
- gradient intersection;
- feedback drift;
- random control.

## 5. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| activation_dominant | P1/H2 | activation variance | known good for PCA | secondary | PCA recovers \(P_c^*\) | PCA fails in its favorable regime | unstable | tables |
| unique_dominant | P1/H2 | unique variance nuisance | tests PCA false positive | primary | PCA no longer dominates every criterion | PCA still wins all criteria | unstable | figures |
| mean_offset | P2 | group/global mean signal | known good for mean estimator | secondary | group mean detects mean common | no estimator detects mean common | unstable | tables |
| gradient_intersection | H1/H3 | cross-group update intersection | tests optimization common | primary | gradient estimator wins overlap reduction | activation wins all criteria | unstable | figures |
| feedback_drift | H1 | training drift common | bridge to preservation question | secondary | feedback estimator wins drift-sensitive criteria | drift estimator random-like | unstable | tables |

Seeds: 0-9.

No training checkpoints are used; this is an estimator audit.

## 6. Primary Metric

Definition: `criterion_winner_diversity` is the number of distinct estimator
families that win recovery alignment, shared-loss sensitivity, and
gradient-overlap reduction across all regimes.

Unit: count of estimator families.

Why it decides: If more than one estimator wins, common cannot be treated as a
single criterion-free hidden-state object.

## 7. Secondary Metrics

- `subspace_alignment`: \(\|A^\top \hat U\|_F^2/k\).
- `shared_loss_sensitivity`: increase in shared-target ridge loss after
  removing \(P h\).
- `rare_loss_sensitivity`: increase in rare-target ridge loss after removing
  \(P h\).
- `gradient_overlap_reduction`: average pairwise group-gradient cosine before
  residualization minus after residualization.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: activation PCA should recover common in `activation_dominant`.

Known bad: random projector should not dominate aggregate metrics.

Known confusing: `mean_offset` may make both activation PCA and group mean look
good if the mean offset has large norm.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| generation | Does the regime contain known common signal? | true basis and latent scales | common norm nonzero | config json | detailed |
| estimator | Are projectors valid rank-k objects? | orthonormal basis checks | projector rank matches k | estimator table | detailed |
| scoring | Do metrics separate criteria? | per-seed scores | non-random winners | criterion table | summary |
| aggregation | Is the conclusion stable? | seed mean/std | winner stable by regime | figures | summary |

## 10. Algorithm Specification

input: regime config and seed.

parameters: hidden dimension 16, common rank 2, groups 6, unique rank 2,
samples per group 600.

intermediate variables: \(A\), \(B_g\), \(h\), \(y_c\), \(y_r\), \(G_g\), candidate
projectors.

steps:

1. Generate hidden states with known \(P_c^*\).
2. Estimate candidate projectors.
3. Fit ridge readouts for shared and rare targets.
4. Score recovery, causal sensitivity, and gradient-overlap reduction.
5. Aggregate over seeds and regimes.

outputs: CSV tables, JSON summary, and figures.

debug artifacts: per-seed score table and run config.

pass conditions: multiple estimator winners across mechanism criteria.

fail conditions: one estimator dominates all criteria.

failure reasons: invalid synthetic task, estimator implementation bug, or
criterion not separable.

## 11. Success / Failure / Insufficient Evidence

Success supports common as a mechanism-conditioned operator family.

Failure supports a single-operator route in controlled settings.

Insufficient evidence requires redesigning the synthetic regimes before using
real data.

## 12. What This Cannot Claim

This run cannot claim that gradient common is the real-DCLM common operator,
that feedback common explains proxy overwrite, or that any residualized MoE
method improves rare-token loss.

## 13. Review Notes And Protocol Changes

Initial protocol created from the 2026-06-29 Pro route and user request to run
the full controlled experiments.


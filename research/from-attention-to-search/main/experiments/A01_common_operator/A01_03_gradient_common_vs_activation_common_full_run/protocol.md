# Protocol: A01_03 Gradient Common Versus Activation Common Full Run

## 0. Approval Snapshot

Approval status: user requested execution in the active goal on 2026-06-29.

Purpose: Decide whether optimization-relevant common is better estimated from
activation covariance or cross-group gradient covariance.

Primary anchor: `01_03_gradient_common_vs_activation_common_anchor.md`.

Anchor decision question: Is optimization-relevant common better explained by
activation covariance or by cross-group gradient covariance?

Anchor physical prior tested: Activation energy and update interference are
different physical objects.

Anchor core model term tested: residualized group gradients
\(G_g^r(P)=\mathbb{E}[\delta_g((I-P)h)^\top\mid g]\).

Anchor falsifier: Activation PCA matches or beats gradient intersection on
gradient-overlap reduction in activation-gradient mismatch regimes.

Experiment role: root-cause / estimator audit.

Primary metric from anchor: `gradient_overlap_reduction_advantage`.

Claim boundary from anchor: controlled activation-gradient mismatch evidence
only; no real-DCLM preservation or method claim.

Minimal setup: Generate controlled hidden states with separable activation
nuisance, functional shared, gradient common, and group-unique components.

Basic configuration: hidden dimension 32, common rank 2, six groups, twenty
seeds, 500 samples per group.

Conditions to run: aligned common, activation nuisance, unique variance,
functional-gradient split, and entangled residual.

Pass: Gradient intersection beats activation PCA on gradient-overlap reduction
in at least three of four mismatch regimes with seed win rate at least 0.8.

Fail: Activation PCA matches or beats gradient intersection in most mismatch
regimes.

Insufficient: Random control wins, metric signs are unstable, or shared-loss
guards show the comparison is dominated by target destruction.

Cannot claim: real-DCLM feedback common, preservation rescue, layerwise common
role, residualized MoE utility, or final estimator for all mechanisms.

Approval decision: execute the controlled full run.

## 1. Anchor Alignment

Decision question: activation common or gradient common for optimization
interference.

Physical prior tested: hidden-state covariance and group-gradient covariance
can select different subspaces.

Core model term tested: group-gradient overlap before and after
residualization.

Falsifier: activation PCA removes gradient overlap as well as gradient
intersection in mismatch regimes.

Claim boundary: controlled estimator mechanism only.

## 2. Tested Hypothesis

H1: Gradient-intersection common gives higher gradient-overlap reduction than
activation PCA when activation variance is nuisance or unique.

H2: Functional shared common can win shared-loss sensitivity while gradient
common wins optimization-overlap reduction.

## 3. Rival Explanations

R1: Activation PCA already captures the optimization common.

R2: Gradient intersection only tracks target scale and not a real subspace.

R3: Functional shared common and gradient common are the same object.

R4: Estimator differences are random or seed-unstable.

## 4. Data / Model / Algorithm / Objective

Hidden states are generated as:

\[
h = s_g A_g z_g + s_f A_f z_f + s_u B_g z_u + s_n A_n z_n + \epsilon
\]

where \(A_g\) is the gradient-common basis, \(A_f\) is the functional shared basis,
\(B_g\) is the group-unique basis, and \(A_n\) is an activation nuisance basis.

Activation PCA estimates:

\[
P_{\mathrm{act}}=\mathrm{TopEig}(\mathbb{E}[hh^\top])
\]

Gradient intersection estimates:

\[
P_{\mathrm{grad}}=\mathrm{TopEig}
\left(
\frac{1}{|G|(|G|-1)}\sum_{g\neq g'}G_g^\top G_{g'}
\right)
\]

Functional shared estimates the input-side subspace most predictive of the
shared target through the cross-covariance \(H^\top Y_c\).

## 5. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| aligned_common | known-good aligned case | R1 | verifies estimators agree when mechanisms align | secondary | both act/grad reduce overlap | no estimator works | unstable | tables |
| activation_nuisance | P1/H1 | high activation energy nuisance | tests PCA false positive | primary | grad beats act | act matches grad | unstable/random | figures |
| unique_variance | P1/H1 | high group-unique activation variance | tests unique variance confound | primary | grad beats act | act matches grad | unstable/random | figures |
| functional_gradient_split | P2/H2 | useful shared common differs from gradient common | separates functional and optimization common | primary | functional wins shared, grad wins overlap | same estimator wins both | unstable | figures |
| entangled_residual | P1/H1 | non-orthogonal residual nuisance | tests robustness under entanglement | primary | grad beats act | act matches grad | unstable/random | tables |

Seeds: 0-19.

No real checkpoints are used; this is a controlled estimator audit.

## 6. Primary Metric

`gradient_overlap_reduction_advantage`:

\[
\Delta_{\mathrm{adv}} =
\Delta C(P_{\mathrm{grad}})-\Delta C(P_{\mathrm{act}})
\]

Unit: cosine-overlap reduction margin.

Why it decides: the question is not whether a direction is large in hidden
space, but whether removing it reduces redundant group updates.

## 7. Secondary Metrics

- `gradient_overlap_reduction`: average pairwise group-gradient cosine before
  residualization minus after residualization.
- `shared_loss_sensitivity`: increase in shared-target ridge loss after
  removing \(P h\).
- `gradient_common_alignment`: recovery of the controlled gradient-common
  basis.
- `functional_common_alignment`: recovery of the controlled functional shared
  basis.
- `criterion_winner`: which estimator wins each criterion per regime.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: in `aligned_common`, activation PCA and gradient intersection
should both have nontrivial reduction.

Known bad: random control should not win aggregate optimization criteria.

Known confusing: in `functional_gradient_split`, gradient intersection may
hurt shared prediction if the gradient-common basis also carries shared target
signal. This should be recorded as a boundary, not hidden.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| generation | Are activation and gradient bases separable when intended? | basis alignments | mismatch regimes have low act/grad alignment | config json | detailed |
| estimator | Are projectors valid rank-k objects? | basis rank checks | rank k and finite scores | score table | detailed |
| scoring | Does residualization change gradient overlap? | per-seed scores | non-random positive reductions | score table | summary |
| aggregation | Is gradient advantage stable? | seed win rates | pass/fail rule applies | summary table | summary |

## 10. Algorithm Specification

input: regime config and seed.

parameters: hidden dimension 32, common rank 2, functional rank 2, unique rank
2, nuisance rank 2, groups 6, samples per group 500.

intermediate variables: \(A_g\), \(A_f\), \(B_g\), \(A_n\), \(h\), shared targets,
gradient targets, candidate projectors.

steps:

1. Generate hidden states under each regime.
2. Estimate activation, gradient, functional, and random projectors.
3. Compute group gradients from zero linear readout residuals.
4. Residualize hidden states by each projector.
5. Score gradient-overlap reduction and shared-loss sensitivity.
6. Aggregate over seeds and regimes.

outputs: CSV tables, JSON summary, and central figures.

debug artifacts: run config, per-seed score table, aggregate summary table.

pass conditions: gradient intersection beats activation PCA in most mismatch
regimes.

fail conditions: activation PCA matches or beats gradient intersection.

failure reasons: activation and gradient objects are not separable,
implementation bug, or gradient common is not the optimization object.

## 11. Success / Failure / Insufficient Evidence

Success supports gradient common as the next optimization estimator.

Failure supports returning to activation common or revising the estimator.

Insufficient evidence requires redesigning the mismatch regimes before moving
to real-data feedback common.

## 12. What This Cannot Claim

This run cannot claim real-DCLM feedback causality, preservation rescue, shared
expert utility, or a residualized MoE improvement.

## 13. Review Notes And Protocol Changes

Initial protocol created from the 2026-06-29 Pro route and the user request to
execute the full common-operator mechanism experiments.


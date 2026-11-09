# Protocol: A06_02_03_E01 Soft-Router Advantage-To-Margin Dynamics

## 0. Approval Snapshot

Approval status: approved by the user's explicit request to restructure and execute the specialization package.

Purpose: test whether controlled expert utility changes the sign of soft-router matched margin pressure.

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Experiment role: root-cause audit. The formula/autograd comparison is an implementation guard.

Minimal setup: four balanced features, orthogonal frozen feature centers with within-feature noise, four fixed class-specialized experts, softmax router, router-only one-step SGD.

Conditions: matched expert utility, identical experts, and permuted expert utility.

Primary metric: positive matched-margin sign rate over feature-seed cells.

Pass: matched utility sign rate at least 0.90; identical update is numerical zero; permuted utility favors the utility-aligned map over the geometry-matched map.

Fail: matched sign rate below 0.75 or either negative control falsely supports geometry-matched pressure.

Insufficient: formula closure fails, step size leaves the local regime, or fewer than 16 seeds complete.

Cannot claim: sparse-router correction, long-run preservation, real-text behavior, or a new router.

## 1. Terminology / Definitions

Definitions follow the primary anchor. `Formula closure error` is the maximum difference between the analytical SGD row update and autograd; it validates implementation but does not decide the mechanism.

## 2. Anchor Alignment

Decision question: Does matched utility, rather than initialized geometry alone, create positive local margin pressure?

Falsifier: utility interventions do not change matched margin direction.

## 3. Tested Hypothesis

Matched utility creates positive matched-margin increments; identical utility removes them; permuted utility redirects them.

## 4. Rival Explanations

- Chain-rule closure alone may be mistaken for evidence.
- Row norms may grow without utility binding.
- A pure route partition may survive while the useful expert identity changes.

## 5. Data / Model / Algorithm / Objective

Generate four orthogonal feature centers in dimension 16. For each feature, sample 256 states with isotropic noise 0.05. Fixed expert outputs are class-logit vectors. Use cross-entropy on the soft mixture output. Update router rows only with plain SGD.

## 6. Conditions, Seeds, And Checkpoints

| Item | Why needed | Evidence | Pass |
| --- | --- | --- | --- |
| matched utility | main mechanism | positive matched-margin sign rate | at least 0.90 |
| identical experts | no-utility guard | maximum update norm | numerical zero |
| permuted utility | geometry/function separation | utility-aligned minus geometry-aligned increment | positive |

Seeds: 0-31. Checkpoints: before and after one SGD step. Learning rates: 0.01 and 0.05 as local-linearity guards.

## 7. Primary Metric

The fraction of feature-seed cells with positive geometry-matched margin change in the matched-utility condition. It decides whether useful expert identity supplies a consistent local reinforcing signal.

## 8. Secondary Metrics

Formula closure error, median margin increment, utility-redirection gap, advantage gap, row-norm change, and per-source-feature contribution.

## 9. Known Good / Known Bad / Known Confusing Cases

Matched utility is known good; identical experts are known bad; permuted utility is known confusing because route purity can remain high while function points elsewhere.

## 10. Stage-Level Profiling Plan

1. Geometry audit: verify orthogonality and initial matched routing.
2. Formula audit: compare analytical and autograd updates.
3. Utility intervention: compute matched and utility-aligned margin pressure.
4. Aggregate only after all 32 seeds complete.

## 11. Algorithm Specification

Inputs: feature centers, sampled states, expert output table, router rows, labels. Outputs: cell-level and aggregate tables plus a condition figure. Failure reasons: incorrect advantage sign convention, optimizer mismatch, or utility intervention not separated from geometry.

Parameter rationale:

| Parameter | Value | Reason | Too small | Too large |
| --- | ---: | --- | --- | --- |
| hidden noise | 0.05 | adds within-feature spread without breaking the known centers | rotation-only test | obscures the controlled binding |
| router init scale | 0.75 | keeps soft probabilities nonsaturated | weak initial identity | vanishing competitor probabilities |
| expert logit strength | 4.0 | creates clear but finite utility separation | advantage becomes numerically weak | cross-entropy saturates |
| router learning rate | 0.01 / 0.05 | two local-step scales guard sign stability | update hard to resolve | leaves the one-step local regime |

## 12. Success / Failure / Insufficient Evidence

Use the thresholds in the approval snapshot without post-hoc changes.

## 13. What This Cannot Claim

No claim about trainable representations, sparse routing, accumulated noise, semantic experts, or expert utility in a trained model.

## 14. Review Notes And Protocol Changes

The daily A06_02_03_E03 draft treated formula correlation as primary evidence. This protocol demotes it to an implementation guard because the equality follows exactly from the frozen soft-router model.

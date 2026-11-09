# Protocol: A06_02_03_E03 Background Bias And Margin Budget

## 0. Approval Snapshot

Approval status: approved by explicit user request.

Purpose: determine whether background-induced margin crossing requires systematic common-direction bias rather than background count alone.

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Minimal setup: length-32 frozen state sequences, four features, ideal router rows, fixed class-specialized experts, weighted top-1 router-only SGD.

Conditions: signal only; boundary-orthogonal zero-mean background; common-state background with balanced targets; common-state background with target-0 bias. Signal positions: 32, 16, 8, 4, 2 of 32.

Primary metric: final margin p05 and crossing rate at matched signal fractions.

Pass: common-biased background has a reproducible crossing threshold and materially lower margins than zero-mean background; signal-only stays positive; additive budget closes.

Fail: zero-mean and biased background behave the same or signal-only collapses.

Insufficient: budget error exceeds tolerance or fewer than 32 seeds complete.

Cannot claim: real-DCLM common causality, AdamW dynamics, hidden drift, or a working intervention.

## 1. Terminology / Definitions

Zero-mean background balances labels and state perturbations so its expected pairwise boundary projection cancels. Common-biased background repeats a shared state and target, creating a nonzero mean update.

## 2. Anchor Alignment

Decision question: Is systematic background bias the finite-margin consumer in the controlled frozen model?

## 3. Tested Hypothesis

At the same background fraction, biased updates cross matched boundaries while zero-mean updates mainly add variance.

## 4. Rival Explanations

Any background amount may be sufficient; stochastic variance may dominate; top-1 competition may collapse signal-only routing.

## 5. Data / Model / Algorithm / Objective

Feature states equal a common component plus an orthogonal feature residual. Signal positions target their sequence feature. Zero-mean background uses balanced targets and symmetric residual perturbations. Common-biased background uses the common state and target class 0. Experts and hidden states are fixed; router rows use plain SGD for 500 steps.

## 6. Conditions, Seeds, And Checkpoints

Background modes: none, boundary-orthogonal zero-mean, common-balanced, common-biased. Signal counts: 32, 16, 8, 4, 2. Seeds: 0-31. Checkpoints: 0, 1, 5, 10, 25, 50, 100, 200, 500.

## 7. Primary Metric

Final p05 of pairwise matched margins and fraction of feature-seed cells that ever cross zero. These metrics decide whether the finite margin buffer is exhausted.

## 8. Secondary Metrics

Signal and background cumulative margin contributions, budget closure error, crossing time, feature-wise asymmetry, route accuracy, and selected-expert changes.

## 9. Known Good / Known Bad / Known Confusing Cases

Signal-only is known good from A06_02_01_E08's qualitative direction. Zero-mean background is the variance guard. High task accuracy is not used as preservation evidence.

## 10. Stage-Level Profiling Plan

Audit data moments; verify initial routing; verify source-gradient additivity; run ratio sweep; locate crossing threshold; aggregate only after all seeds finish.

## 11. Algorithm Specification

For each step, compute signal and background losses with their contribution to the full-position mean, obtain separate router gradients, sum them for the actual SGD update, and accumulate their exact pairwise margin contributions. Reconstruct every fixed-center pairwise margin from the cumulative budget.

Parameter rationale:

| Parameter | Value | Reason | Too small | Too large |
| --- | ---: | --- | --- | --- |
| signal counts | 32/16/8/4/2 | geometric ratio ladder around the expected crossing regime | misses threshold | broad sweep without added decision value |
| router learning rate | 0.1 | makes cumulative pressure measurable while retaining boundary trajectories | no crossing in finite time | skips re-entry dynamics |
| training steps | 500 | distinguishes transient crossing from final recovery | confuses first crossing with failure | unnecessary controlled compute |
| initial row scale | 1.0 | supplies the finite positive buffer under test | starts near boundary | hides background consumption |
| init noise | 0.01 | creates seed variation while preserving initial identity | seeds become rotation duplicates | corrupts the known-good start |

## 12. Success / Failure / Insufficient Evidence

Budget closure is a validity guard. The mechanism is supported only by the matched-ratio biased-versus-zero-mean intervention.

## 13. What This Cannot Claim

No claim about learned hidden states, optimizer normalization, real language, semantic experts, or common subtraction.

## 14. Review Notes And Protocol Changes

The daily draft grouped one-step formula validation and multi-step background budgeting. They are now separated into A06_02_03_E01 and A06_02_03_E03 so the latter is not decided by a chain-rule identity.

After smoke and before the full run, `common_balanced` was added as a secondary guard. It holds the common hidden direction fixed while balancing targets, separating common geometry from target bias. It does not change the primary biased-versus-zero-mean decision rule.

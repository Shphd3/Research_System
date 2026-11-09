# Protocol: A06_02_03_E02 Top-1 Counterfactual Correction Dynamics

## 0. Approval Snapshot

Approval status: approved by explicit user request.

Purpose: test whether weighted top-1 routing corrects wrong assignments through rank-dependent boundary search because unselected expert utilities are unavailable.

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Minimal setup: frozen orthogonal feature states, fixed class-specialized experts, router-only SGD, matched expert initial score rank 1/2/4, soft versus weighted top-1 output.

Primary metric: correction time of the utility-matched expert, stratified by initial rank.

Pass: top-1 has a larger rank-4 versus rank-2 correction penalty than soft routing, and top-1 unselected updates do not align with individual counterfactual utility.

Fail: top-1 correction is as direct and rank-insensitive as soft routing.

Insufficient: correct-init guard fails, fewer than 32 seeds finish, or the top-1 gradient formula does not close.

Cannot claim: permanent lock-in, superiority of soft routing, or production-MoE behavior.

## 1. Terminology / Definitions

Correction time is the first router-only update after which the useful expert is top-1 for a feature center. A censored value means it did not correct within 200 steps.

## 2. Anchor Alignment

The experiment tests whether missing counterfactual comparison, rather than missing gradient altogether, explains weak top-1 correction.

## 3. Tested Hypothesis

Top-1 can reject a bad selected expert but cannot directly identify the best unselected expert; recovery therefore depends on initial rank.

## 4. Rival Explanations

Softmax competition may already distinguish unselected experts; saturation may explain all delays; correct routing may itself be unstable.

## 5. Data / Model / Algorithm / Objective

Use four noiseless orthogonal feature centers and fixed experts whose output \(e\) favors class \(e\). Build router score matrices where the useful expert has exact initial rank 1, 2, or 4. Train only router rows for 200 full-batch SGD steps under soft-mixture or weighted-top-1 output.

## 6. Conditions, Seeds, And Checkpoints

Methods: soft and weighted top-1. Initial ranks: 1, 2, 4. Seeds: 0-31. Record every step from 0 to 200.

## 7. Primary Metric

Median correction time and correction rate by method and initial rank. The main contrast is the rank-4 minus rank-2 penalty for top-1 relative to soft routing.

## 8. Secondary Metrics

Unselected update/utility correlation, boundary-crossing count, matched margin trajectory, selected-expert sequence, and formula closure error.

## 9. Known Good / Known Bad / Known Confusing Cases

Rank-1 is a correct-init guard. Rank-4 is the strongest counterfactual-information stress. A top-1 row update on an unselected expert is not evidence that its own utility was evaluated.

## 10. Stage-Level Profiling Plan

Audit exact ranks; verify one-step formula; measure unselected utility alignment; run 200-step correction; aggregate by rank.

## 11. Algorithm Specification

The score matrix is represented exactly in the orthogonal feature basis, so initial rank is controlled independently for every feature. A boundary event is any change in selected expert. Correction is assessed against the fixed utility map, not a best post-hoc permutation.

Parameter rationale:

| Parameter | Value | Reason | Too small | Too large |
| --- | ---: | --- | --- | --- |
| score scale | 0.5 | creates exact rank separation without severe softmax saturation | ranks become numerically fragile | correction becomes dominated by saturation |
| router learning rate | 0.2 | resolves boundary events within a bounded 200-step run | rank-4 cells may be censored without mechanism failure | skips intermediate boundaries |
| training steps | 200 | covers the rank-4 top-1 correction observed in smoke extrapolation | false permanent-lock claim | unnecessary expansion |
| expert logit strength | 4.0 | makes matched utility observable | weak correction signal | saturated task output |

## 12. Success / Failure / Insufficient Evidence

Use the preregistered contrasts above. Report censored correction explicitly.

## 13. What This Cannot Claim

The result cannot establish long-run MoE specialization or validate a soft-to-sparse method.

## 14. Review Notes And Protocol Changes

This protocol sharpens the earlier phrase "unselected experts receive no gradient": they can receive softmax-competition row updates, but those updates do not depend on their own expert outputs.

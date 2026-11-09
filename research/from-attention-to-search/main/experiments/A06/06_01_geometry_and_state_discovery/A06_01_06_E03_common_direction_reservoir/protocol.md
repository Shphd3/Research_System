# Protocol: A06_01_06_E03 Common Direction Split Reservoir

## 0. Approval Snapshot

Approval status: executed under the user's four-card A08 run request on 2026-06-28.

Purpose: test the r1 split idea: send the converged common projection to a common expert and send residual representation to a long-tail reservoir.

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Anchor decision question: does common/residual forward splitting protect tail learning on nested synthetic data?

Anchor physical prior tested: once the common direction is converged, tail examples should not keep using it for child-specific updates.

Anchor core model term tested: \(h_C=P_Ch\) and \(h_R=(I-P_C)h\).

Anchor falsifier: tail loss improves without reducing tail update concentration, or common loss regresses.

Experiment role: method construction, gated by A06_01_06_E01/A06_01_06_E02.

Primary metric from anchor: tail loss improvement over CE baseline.

Claim boundary from anchor: controlled nested forward-split method only.

Minimal setup: synthetic nested model with CE baseline, update-control baseline, split-forward reservoir, and capacity-matched split guard.

Basic configuration: 8 seeds, same data as A07/A08 nested surface, matched parameter budget where possible.

Conditions to run: `ce_baseline`, `update_suppression_only`, `common_residual_split`, `capacity_matched_split`, `oracle_split`.

Pass: split lowers tail loss, preserves common loss, and lowers \(\alpha_{\mathrm{tail}}\) versus CE.

Fail: split hurts common, does not lower tail loss, or is explained by capacity.

Insufficient: A06_01_06_E01 convergence or A06_01_06_E02 gate-forward direction failed.

Cannot claim: iterative discovery, real-DCLM preservation, or MoE utility.

Approval decision: execute after A06_01_06_E02.

## 1. Anchor Alignment

Decision question: forward split protects tail learning.

Physical prior tested: stable common direction should be removed from reservoir path.

Core model term tested: \(P_C h\) and \((I-P_C)h\).

Falsifier: no functional tail improvement with mechanism guard.

Claim boundary: synthetic method surface.

## 2. Tested Hypothesis

Common/residual split reduces harmful common-subspace absorption and improves tail learning.

## 3. Rival Explanations

Capacity increase, regularization, oracle labels, or common undertraining may explain improvement.

## 4. Data / Model / Algorithm / Objective

Use nested synthetic data. Freeze \(P_C\) after convergence, route \(P_Ch\) to common expert and \((I-P_C)h\) to reservoir expert.

## 5. Conditions, Seeds, And Checkpoints

| Item | Why needed | Evidence |
| --- | --- | --- |
| CE baseline | dense comparison | loss/alpha |
| update suppression only | A07_02 rival | loss/alpha |
| common-residual split | primary method | loss/alpha |
| capacity matched split | capacity rival | loss/load |
| oracle split | upper bound | loss |

## 6. Primary Metric

Tail loss improvement:

\[
\Delta L_{\mathrm{tail}}=L_{\mathrm{tail}}(\mathrm{CE})-L_{\mathrm{tail}}(\mathrm{split}).
\]

## 7. Secondary Metrics

Common loss, tail accuracy, \(\alpha_{\mathrm{tail}}\), route load, expert update norm.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: oracle split should help.

Known bad: capacity-only split should not fully explain the effect.

Known confusing: tail loss improves but common loss regresses.

## 9. Stage-Level Profiling Plan

Audit projector freeze, route split, loss, update fraction, and capacity guard.

## 10. Algorithm Specification, If Nontrivial

input: frozen \(P_C\), nested data, split-forward model.

steps: train baseline and split variants; compute losses and alpha; aggregate.

## 11. Success / Failure / Insufficient Evidence

Success: split improves tail and moves mechanism guard.

Failure: no improvement or wrong mechanism.

Insufficient: upstream convergence failed.

## 12. What This Cannot Claim

No iterative or real-data claim.

## 13. Review Notes And Protocol Changes

This is the first explicit gating mechanism card in A08.

2026-06-28: full run `a08_singular_preservation_full_20260628_2` completed.
Result is insufficient for the mechanism claim because the capacity-matched
random split improves tail loss more than the proposed common/residual split.

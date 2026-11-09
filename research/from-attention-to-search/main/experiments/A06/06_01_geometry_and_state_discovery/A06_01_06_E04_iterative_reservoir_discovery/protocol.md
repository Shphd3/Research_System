# Protocol: A06_01_06_E04 Iterative Reservoir Direction Discovery

## 0. Approval Snapshot

Approval status: executed under the user's four-card A08 run request on 2026-06-28.

Purpose: test whether the r1 split idea can be repeated: freeze an old direction, train the residual reservoir, extract the next nested direction, and continue.

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Anchor decision question: can repeated common/residual extraction discover nested directions sequentially?

Anchor physical prior tested: nested learning contains a hierarchy of directions, not only one common/rare split.

Anchor core model term tested: \(P_{\le k}=\sum_{j=1}^kP_j\) and \(h_{k+1}=(I-P_{\le k})h\).

Anchor falsifier: later directions repeat old directions or old losses regress.

Experiment role: mechanism extension / staged method audit.

Primary metric from anchor: next-level direction alignment after each iteration.

Claim boundary from anchor: controlled sequential discovery only.

Minimal setup: nested synthetic data with known \(A,B,C,D\) directions; run staged extraction for two or three iterations.

Basic configuration: 8 seeds, one-stage baseline, two-stage extraction, three-stage extraction.

Conditions to run: `one_stage_common`, `two_stage_A_then_B`, `three_stage_A_B_C`, `shuffled_residual_guard`.

Pass: each stage discovers a new child direction and preserves old-level loss.

Fail: repeated extraction rediscovers \(A\), old losses regress, or alignment is label leakage.

Insufficient: A06_01_06_E03 split-forward method fails.

Cannot claim: real-data discovered semantic hierarchy.

Approval decision: execute only after A06_01_06_E03 passes.

## 1. Anchor Alignment

Decision question: sequential nested discovery.

Physical prior tested: hierarchy of stable directions.

Core model term tested: cumulative projector and residual.

Falsifier: repeated same direction or old feature forgetting.

Claim boundary: synthetic hierarchy.

## 2. Tested Hypothesis

After freezing \(A\), the residual reservoir can learn \(B|A\); after freezing \(A,B\), it can learn \(C|AB\).

## 3. Rival Explanations

Label leakage, capacity increase, random orthogonalization, or memorization may create apparent discovery.

## 4. Data / Model / Algorithm / Objective

Use known-direction nested data. Train staged residual reservoirs and audit alignment after each stage.

## 5. Conditions, Seeds, And Checkpoints

| Item | Why needed | Evidence |
| --- | --- | --- |
| one-stage common | baseline | \(A\) alignment |
| two-stage | first recursion | \(B|A\) alignment |
| three-stage | second recursion | \(C|AB\) alignment |
| shuffled residual | leakage guard | alignment/loss |

## 6. Primary Metric

Next-level alignment:

\[
A_{k+1}=\|P_{k+1}f_{k+1}\|^2-\max_{j\le k}\|P_{k+1}f_j\|^2.
\]

## 7. Secondary Metrics

Old-level loss retention, tail loss, projector overlap, effective rank.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: first stage should recover \(A\).

Known bad: shuffled residual should not recover the next direction.

Known confusing: old and new directions are not orthogonal in a wide model.

## 9. Stage-Level Profiling Plan

Audit each iteration separately: direction, old loss, new loss, residual norm.

## 10. Algorithm Specification, If Nontrivial

input: known nested directions, frozen projector set, residual model.

steps: train stage, freeze projector, subtract cumulative projection, train next stage, audit.

## 11. Success / Failure / Insufficient Evidence

Success: sequential new directions appear with retention.

Failure: loop repeats common direction or forgets old features.

Insufficient: upstream split fails.

## 12. What This Cannot Claim

No real-data semantic hierarchy claim.

## 13. Review Notes And Protocol Changes

This is the final synthetic batch card before the real-DCLM convergence audit under `A06_01_06`.

2026-06-28: full run `a08_singular_preservation_full_20260628_2` completed.
The learned iterative loop failed. Oracle residual debug conditions were added
after failure to separate learned-projector leakage from residual-objective
failure.

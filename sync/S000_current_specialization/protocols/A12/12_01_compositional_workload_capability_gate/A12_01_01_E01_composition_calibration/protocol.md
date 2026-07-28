# Protocol: A12_01_01_E01 Composition-Learning Calibration

## 0. Approval Snapshot

**Approval status:** approved by the user's explicit instruction to complete the planned anchors and resolve blockers.
**Purpose:** produce one valid learned-composition checkpoint surface.
**Primary anchor:** `../../../../problem_anchors/12_structured_compositional_mtp_workload/12_01_compositional_workload_capability_gate/subanchors/12_01_01_workload_validity_and_learner_guard_anchor.md`.
**Decision question:** does the first bounded repair passing seed-971 screening achieve test answer accuracy `>=0.70` in all five seeds?
**Physical prior:** two-hop composition benefits from sequential computation depth.
**Core model term:** depth first, then training budget, then width.
**Falsifier:** no bounded condition generalizes above threshold.
**Experiment role:** operationalization/calibration.
**Primary metric:** minimum five-seed test answer accuracy.
**Minimal setup:** exact 155-token task with globally disjoint permutation splits and NTP-only training.
**Pass:** minimum test answer accuracy `>=0.70`, minimum format accuracy `>=0.95`, zero target-permutation overlap, and controls valid.
**Fail:** all four stages fail with valid execution.
**Insufficient:** overlap, missing rows, non-finite training, or failed control integrity.
**Cannot claim:** MTP benefit, unique depth causality, capacity mechanism, curriculum, or language transfer.
**Approval decision:** execute the bounded ladder and stop at first valid repair.

## 1. Terminology / Definitions

Calibration means eligibility of the task/model surface. Screening uses validation accuracy on seed 971; confirmation retrains the frozen configuration on seeds 971--975 and judges the independent test split.

## 2. Anchor Alignment

The run changes only model depth, then budget, then width in a fixed order. Data semantics, serialization, NTP loss, optimizer, batch size, and decision threshold stay fixed.

## 3. Tested Hypothesis

The first passing bounded repair yields `5/5` test answer accuracy `>=0.70`.

## 4. Rival Explanations

Memorized permutations, format shortcuts, insufficient optimization, width bottleneck, or invalid controls.

## 5. Data / Model / Algorithm / Objective

- one global pool partitions target $\pi_1$ and $\pi_2$ without cross-split reuse;
- train 512 pairs / 8192 examples; validation 64 / 1024; audit 64 / 1024; test 128 / 2048;
- two target tables plus four distractor tables; atomic vocabulary; length 155;
- NTP-only controlled objective $L_N=L_{format}(h_T)+L_{answer}(h_{T+1})$;
- AdamW `3e-4`, weight decay `0.01`, batch 64; evaluation every 100 steps;
- no auxiliary future loss in calibration.

## 6. Conditions, Seeds, And Checkpoints

| Stage | Condition | Screen rule on seed 971 | Confirmation |
| --- | --- | --- | --- |
| A | 2 layers, width 64, 600 steps | validation answer `>=0.70` | five seeds from scratch |
| B | 2 layers, width 64, 3000 steps | only if A fails | five seeds from scratch |
| C | 3 layers, width 64, 3000 steps | only if B fails | five seeds from scratch |
| D | 3 layers, width 128, 3000 steps | only if C fails | five seeds from scratch |

Seeds: `971--975`. The selected configuration is frozen before confirmation.

## 7. Primary Metric

$$
Q_{cal}=\min_{s\in\{971,\ldots,975\}}A_{answer,test}^{(s)}.
$$

This metric prevents a favorable mean from hiding failed seeds.

## 8. Secondary Metrics

Validation accuracy, format accuracy, training curves, time-to-`0.70`, single-table accuracy, shuffled-label accuracy, and split-overlap counts.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: answer labels recomputed from both target tables. Known bad: shuffled labels and one-target-table replacement should stay below `0.25`. Known confusing: validation success without test generalization.

## 10. Stage-Level Profiling Plan

Audit global split disjointness, screening curve, frozen condition, five-seed confirmation, and shortcut controls.

## 11. Algorithm Specification

Generate all splits once; screen ladder in order; stop at first validation pass; retrain selected configuration for all seeds; evaluate full, one-table-replaced, and shuffled-label controls; write decision artifacts.

## 12. Success / Failure / Insufficient Evidence

Apply section 0 exactly. A screen pass alone is not a result; confirmation and controls are required.

## 13. What This Cannot Claim

No MTP/NTP comparison or mechanism claim.

## 14. Review Notes And Protocol Changes

No post-result ladder expansion is allowed. If all stages fail, the operationalization is rejected.

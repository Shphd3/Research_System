# Protocol: A13_00_01_E04 Width-Only Carrier Capacity Audit

## 0. Approval Snapshot

Approval status: approved under standing autonomous authorization.

Purpose: decide whether width-64 shared representation capacity causes the
remaining seed-sensitive carrier failure.

Primary anchor:
[13_00_01](/Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_01_query_conditioned_relay_carrier_anchor.md)

Experiment role: learner-capacity root-cause audit.

Primary metric: unchanged carrier-eligibility conjunction.

Changed object: representation width `64 -> 128`; FFN remains exactly four
times width (`256 -> 512`) as part of the same registered scale factor.

Held fixed: task, split, masks, one/two-layer conditions, four attention heads,
NTP objective, cosine schedule, optimizer, batch order, seeds, steps,
interventions, and thresholds.

Pass: all carrier gates pass.

Fail: any gate fails; the current query-relay learner realization is then
closed rather than further enlarged.

Insufficient: implementation or execution drift.

Cannot claim: a width scaling law, MTP utility, or external transfer.

Approval decision: execute this final carrier-capacity repair before any
objective comparison.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object | Unit | Decision role | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| width | hidden-vector size at every token | 64 or 128 components | dimensions | tests shared representation capacity | parameter-efficient optimum |
| scale factor | proportionally expand hidden and FFN dimensions | width $\times2$, FFN width $\times2$ | ratio | one capacity intervention | general neural scaling |

## 2. Anchor Alignment

The carrier needs one stable NTP-capable scale. E03 showed reachability at
width 64 but not stable eligibility.

## 3. Tested Hypothesis

Width 128 gives the model enough shared representational capacity to retain
all-position prediction and query-conditioned relay behavior simultaneously.

## 4. Rival Explanations

1. initialization basin persists at any small width;
2. the attention/FFN computation, not capacity, is the bottleneck;
3. patch preservation remains limited by clean capability;
4. a code or mask drift creates a false pass.

## 5. Data / Model / Algorithm / Objective

Identical to E03 except the registered width scale. NTP is the only active
objective.

## 6. Conditions, Seeds, And Checkpoints

Same three conditions, five seeds, and 20-step grid through 3,000.

## 7. Primary Metric

The original six-gate Boolean conjunction. No threshold or seed exclusion is
changed.

## 8. Secondary Metrics

Branch accuracy, threshold steps, NLL, late stability, counterfactuals, and
donor patches.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: every width-64 relay seed reached at least `0.9806` once.

Known bad: one-layer relay is structurally disconnected at any width.

Known confusing: a width-128 pass shows one eligible scale, not that width is
the causal property MTP needs.

## 10. Stage-Level Profiling Plan

Audit resolved configuration, all three trajectories, selector branches, and
the two intervention families before computing the conjunction.

## 11. Algorithm Specification

Use the E03 algorithm with width 128 and FFN width 512. All other inputs,
parameters, steps, and outputs remain fixed.

## 12. Success / Failure / Insufficient Evidence

Pass opens `13_00_02`. Fail closes the current carrier learner and blocks all
objective comparisons.

## 13. What This Cannot Claim

No MTP, composition, code/text, long-context, or MoE conclusion.

## 14. Review Notes And Protocol Changes

Self-review:

- one scale factor changed: yes;
- depth remains one/two layers: yes;
- task unchanged: yes;
- original gates retained: yes;
- declared final repair: yes.

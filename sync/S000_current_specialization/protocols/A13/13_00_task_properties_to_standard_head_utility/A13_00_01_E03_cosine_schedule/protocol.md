# Protocol: A13_00_01_E03 Schedule-Only Carrier Audit

## 0. Approval Snapshot

Approval status: approved under standing autonomous authorization.

Purpose: decide whether non-decaying updates, rather than task invalidity or
budget alone, prevent stable relay acquisition.

Primary anchor:
[13_00_01](/Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_01_query_conditioned_relay_carrier_anchor.md)

Experiment role: learner optimization root-cause audit.

Primary metric: unchanged carrier-eligibility conjunction.

Minimal setup: exact E02 task/model/seeds/budget with one changed object.

Changed object: learning-rate schedule, from constant `0.003` to cosine decay
from `0.003` to `0.0001` over 3,000 steps.

Held fixed: data, masks, layer counts, width, optimizer family and betas, batch
order, seeds, objective, metrics, interventions, and thresholds.

Pass: all original carrier gates pass.

Fail: capability remains seed-dependent or causal-use gates fail after clean
capability.

Insufficient: any non-schedule object drifts or execution is incomplete.

Cannot claim: MTP utility, best optimizer, general convergence, or external
transfer.

Approval decision: execute NTP-only E03; objective comparison remains blocked.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit | Decision role | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| cosine decay | progressively reduce update size | $\eta_t=\eta_{\min}+\frac12(\eta_0-\eta_{\min})(1+\cos(\pi t/T))$ | learning rate | tests persistent-update noise | unique source of noise |
| background gradient | loss gradient from non-answer token predictions | all-position NTP terms outside the answer | parameter gradient | plausible destabilizer | direct causal attribution without gradient intervention |

## 2. Anchor Alignment

Decision question: can the same two-layer NTP learner become a stable valid
carrier under a diminishing update scale?

Falsifier: relay capability and use remain below threshold.

Claim boundary: learner eligibility only.

## 3. Tested Hypothesis

The constant-rate E02 run continued to perturb an already learned state.
Cosine decay preserves acquired relay behavior and raises the multi-seed
carrier verdict to pass.

## 4. Rival Explanations

1. initialization basin rather than update noise;
2. insufficient architectural capacity;
3. intervention interface failure;
4. schedule implementation drift.

## 5. Data / Model / Algorithm / Objective

Identical to E02 except the registered cosine schedule. NTP remains the only
active objective.

## 6. Conditions, Seeds, And Checkpoints

`relay_1L`, `relay_2L`, and `bypass_1L`; seeds 1301--1305; evaluation every 20
steps through step 3,000.

Selector-A and selector-B accuracy are added as debug-only diagnostics. They do
not change any gate.

## 7. Primary Metric

The unchanged Boolean conjunction prevents threshold relaxation after E01/E02.

## 8. Secondary Metrics

Answer NLL, branch-wise accuracy, steps to thresholds, late-window variance,
counterfactuals, and donor patches.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: E02 bypass mean passed.

Known bad: one-layer relay is structurally disconnected.

Known confusing: decay may preserve a local plateau rather than escape it; a
fail would leave initialization/representation acquisition alive.

## 10. Stage-Level Profiling Plan

| Stage | Question | Evidence | Rule | Artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| schedule | was only $\eta_t$ changed? | resolved config and LR column | exact formula | trajectory CSV | training |
| capability | does relay stabilize? | total and selector accuracies | original gates | figure/table | patch |
| use | does answer follow donor state? | patch rates | original gates | audit table | verdict |

## 11. Algorithm Specification

Run the E02 algorithm while setting the optimizer learning rate from the
registered cosine formula before every update. No warmup or other change is
allowed.

## 12. Success / Failure / Insufficient Evidence

Pass authorizes creation of the objective-comparison subanchor and Protocol.
Fail closes this learner realization unless a branch diagnostic identifies one
single representational bottleneck worth a final targeted audit.

## 13. What This Cannot Claim

No objective or workload-type conclusion is allowed.

## 14. Review Notes And Protocol Changes

Self-review:

- one experimental variable changed: yes;
- task complexity unchanged: yes;
- all original gates preserved: yes;
- no MTP condition: yes.

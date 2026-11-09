# Protocol: A13_00_01_E02 Budget-Only Carrier Replay

## 0. Approval Snapshot

Approval status: approved under the researcher's standing autonomous-execution
authorization; self-audited after E01.

Purpose: decide whether E01 failed because its fixed 1,000-step budget ended
during late, seed-dependent task acquisition.

Primary anchor:
[13_00_01](../../../../problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_01_query_conditioned_relay_carrier_anchor.md)

Anchor decision question: is the fixed carrier valid, learnable, and causally
used?

Anchor physical prior tested: two layers are sufficient once optimization has
enough time.

Anchor core model term tested: acquisition of
\(S_1=f_{\theta,1}(A,B,Q)\) and standard-head consumption of \(S_1\).

Anchor falsifier: the same carrier remains below capability after the
registered budget extension.

Experiment role: failure-localizing learner-budget audit.

Primary metric from anchor: the unchanged Boolean carrier verdict.

Claim boundary from anchor: carrier eligibility only; no objective comparison.

Minimal setup: exact E01 replay with maximum steps changed from 1,000 to 3,000.

Basic configuration: all E01 data, masks, model parameters, optimizer
parameters, batches, seeds, metrics, and thresholds remain unchanged.

Conditions to run: `relay_1L`, `relay_2L`, and `bypass_1L`.

Pass: all original carrier gates pass.

Fail: capability or causal-use gates remain below threshold.

Insufficient: the first 1,000 steps do not reproduce E01 or execution is
incomplete.

Cannot claim: MTP utility, optimizer superiority, a general scaling law, or
real-workload transfer.

Approval decision: execute E02; MTP remains blocked.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| budget-only replay | extend training without changing another experimental object | 3,000 versus 1,000 maximum steps | optimization steps | isolates premature stopping | best possible optimizer |
| replay prefix | E02 trajectory through step 1,000 | exact metric sequence versus E01 | equality audit | checks contract identity | hardware-independent determinism |

## 2. Anchor Alignment

Decision question: does more time make the same carrier eligible?

Physical prior tested: two state transitions are sufficient but learned late.

Core model term tested: stable acquisition and use of the relay state.

Falsifier: extended trajectories remain capability-limited.

Claim boundary: NTP-only learner audit.

## 3. Tested Hypothesis

E01 ended before stable acquisition. With no other change, 3,000 steps make the
two-layer relay and one-layer bypass controls pass, after which
counterfactuals and donor patches pass as consequences of clean capability.

## 4. Rival Explanations

1. constant-learning-rate instability rather than insufficient time;
2. the two-layer architecture cannot robustly learn the relay;
3. the intervention interface remains invalid even after capability;
4. the E02 implementation does not replay E01.

## 5. Data / Model / Algorithm / Objective

Identical to [E01 protocol](../A13_00_01_E01_query_conditioned_relay_carrier/protocol.md).
The only changed value is `max_steps: 1000 -> 3000`.

## 6. Conditions, Seeds, And Checkpoints

The three E01 conditions and seeds 1301--1305 are replayed. Evaluation remains
every 20 steps. E02 checkpoints through step 1,000 must exactly reproduce E01
research metrics.

| Item | Anchor clause tested | Rival explanation | Why needed | Evidence role | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| replay prefix | contract identity | implementation drift | validates comparison | guard | exact metric replay | mismatch | missing E01 row | replay table |
| extended capability | learner budget | premature stopping | main question | primary | original gates pass | gates fail | incomplete run | trajectory |
| extended interventions | standard-head relay use | interface failure | closes carrier | primary guard | original gates pass | below threshold | invalid donors | audit table |

## 7. Primary Metric

The unchanged carrier conjunction is primary. No post-E01 threshold is relaxed.

False-positive cost remains higher than false-negative cost because an
ineligible carrier would invalidate later objective claims.

## 8. Secondary Metrics

Answer NLL, steps to `0.90`/`0.95`, late-window variance, counterfactual rates,
and donor-patch rates.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: four E01 bypass seeds reached exact accuracy.

Known bad: one-layer relay stayed at chance in every E01 seed.

Known confusing: an eventual pass shows budget sufficiency, not that 3,000
steps are optimal or compute-matched to a real workload.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| replay | is E01 reproduced? | first 1,000 steps | exact research metrics | prefix comparison | extension |
| extension | do trajectories cross and retain capability? | steps 1,020--3,000 | original thresholds | curves | interventions |
| use | does relay content control the answer? | capable final models | original thresholds | patch table | verdict |

## 11. Algorithm Specification

Input, model, data, batches, and algorithm are exactly E01. Train to step 3,000,
evaluate every 20 steps, then repeat the same counterfactual and donor-patch
audits.

Outputs: trajectory, replay audit, final metrics, intervention tables, summary,
and one decision figure.

Failure reasons: `prefix_mismatch`, `budget_still_insufficient`,
`optimization_instability`, `relay_nonuse`, or `execution_incomplete`.

## 12. Success / Failure / Insufficient Evidence

Pass opens the objective-comparison subanchor. Fail localizes the remaining
problem to optimization stability or architecture; the next test may change
one optimizer parameter, but must not change the task.

## 13. What This Cannot Claim

No MTP, code, text, long-context, composition, or MoE claim is allowed.

## 14. Review Notes And Protocol Changes

Self-review:

- one changed variable: yes, maximum steps only;
- original thresholds preserved: yes;
- original seeds and batches preserved: yes;
- MTP blocked: yes.

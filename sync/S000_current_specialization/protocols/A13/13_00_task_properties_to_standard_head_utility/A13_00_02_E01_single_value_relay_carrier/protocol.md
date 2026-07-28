# Protocol: A13_00_02_E01 Single-Value Relay Carrier

## 0. Approval Snapshot

Approval status: approved under standing autonomous authorization.

Purpose: validate relay necessity without query-conditioned binding.

Primary anchor:
[13_00_02](/Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_02_single_value_relay_carrier_anchor.md)

Experiment role: operationalization and carrier-validity audit.

Primary metric: six-gate single-relay eligibility conjunction.

Changed task property relative to the closed carrier: the answer is always
`value-A`; the selector no longer determines whether A or B is chosen.

Held fixed: sequence length and token marginals, split, graph, model
architecture, width-64 cosine learner, NTP objective, seeds, steps, metrics,
and thresholds.

Pass: all six gates pass.

Fail: any compliant gate fails.

Insufficient: label construction, counterfactual pairing, or execution is
invalid.

Cannot claim: MTP utility or query-conditioned composition.

Approval decision: execute NTP-only carrier validation.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object | Unit | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| single-value relay | move one early token through an intermediate state | $Y=A$ under the relay mask | task condition | isolates relay necessity | composition |
| nuisance | input that must not affect the answer | value $B$ and selector $Q$ | token | detects shortcut sensitivity | natural-language irrelevance |

## 2. Anchor Alignment

Decision question: is relay alone a valid, learnable, standard-head-used
carrier?

Falsifier: capability without correct relay donor control, or capability floor
after query binding is removed.

Claim boundary: carrier only.

## 3. Tested Hypothesis

The fixed width-64 two-layer NTP learner reliably copies $A$ through the relay,
ignores $B,Q$, and follows donor relay content.

## 4. Rival Explanations

Direct bypass, nuisance shortcut, triple lookup, generic learner failure, or
non-specific patch damage.

## 5. Data / Model / Algorithm / Objective

All 512 $(A,B,Q)$ triples are retained. The only label rule is $Y=A$. The same
409/103 split, sparse masks, width-64 model, cosine schedule, and all-position
NTP objective are used.

## 6. Conditions, Seeds, And Checkpoints

`relay_1L`, `relay_2L`, `bypass_1L`; seeds 1301--1305; checkpoints every 20
steps through 3,000.

## 7. Primary Metric

The same conservative six-gate conjunction used in `13_00_01`, with the
selected counterfactual mapped to $A$ and the nuisance counterfactual to $B$.

## 8. Secondary Metrics

Answer NLL, threshold steps, nuisance-conditioned accuracy, late stability,
and donor-patch rates.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: one-layer bypass directly reads $A$.

Known bad: one-layer relay cannot receive $A$ at the answer.

Known confusing: copying is deliberately not composition; success is only a
base carrier.

## 10. Stage-Level Profiling Plan

Audit labels and split, exact graph reachability, three training trajectories,
$A$/$B$ counterfactuals, and in-distribution donor patches.

## 11. Algorithm Specification

Use the registered runner with `task_mode=copy`. All training and audit steps
match E03.

## 12. Success / Failure / Insufficient Evidence

Pass opens the objective-by-relay comparison. Fail blocks it and closes the
current two-layer carrier family.

## 13. What This Cannot Claim

No query composition, code, text, long-context, planning, or MoE conclusion.

## 14. Review Notes And Protocol Changes

Self-review:

- task simplified, not enlarged: yes;
- relay graph unchanged: yes;
- NTP only: yes;
- all original validity gates retained: yes.

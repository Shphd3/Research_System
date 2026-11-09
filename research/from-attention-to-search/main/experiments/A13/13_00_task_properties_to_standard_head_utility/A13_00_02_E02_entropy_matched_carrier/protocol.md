# Protocol: A13_00_02_E02 Entropy-Matched Carrier Confirmation

## 0. Approval Snapshot

Approval status: approved under standing autonomous authorization.

Purpose: confirm carrier validity on the exact sequence that will later make
shared-aux and Next-2 auxiliary target sets equal in irreducible boundary
entropy.

Primary anchor:
[13_00_02](../../../../problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_02_single_value_relay_carrier_anchor.md)

Experiment role: metric/control validity audit.

Primary metric: unchanged six-gate carrier conjunction.

Changed object relative to E01: serialization only.

```text
E01: [BOS] [A] [B] [random selector] [RELAY] [ANSWER] [A]
E02: [BOS] [FIXED] [A] [B] [RELAY] [ANSWER] [A]
```

Why needed: shared-aux predicts positions \(x_1,\ldots,x_5\), while Next-2
predicts \(x_2,\ldots,x_6\). E02 makes excluded \(x_1\) and included \(x_6\) both
deterministic from their intended states, preventing an extra irreducible
random target from favoring one condition.

Held fixed: single-value label rule, sequence length, value/nuisance marginals,
relay and bypass masks, model, NTP objective, schedule, seeds, budget, metrics,
and thresholds.

Pass: all original carrier gates pass.

Fail: any gate fails.

Insufficient: duplicated token sequences, split leakage, invalid
counterfactual pairs, or execution drift.

Cannot claim: equality of realized gradient norms/difficulty or any MTP
utility.

Approval decision: run NTP-only confirmation; objective comparison remains
blocked until pass.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object | Unit | Decision role | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| boundary target | target present in one auxiliary label set but not the other | shared-only \(x_1\) and MTP-only \(x_6\) | token | removes conditional-entropy mismatch | realized optimization equality |
| entropy matched | both boundary targets have zero Bayes uncertainty | fixed \(x_1\) and relay-determined \(x_6=A\) | nats, both 0 | narrows objective claim | equal gradient magnitude |

## 2. Anchor Alignment

Decision question: is the comparison-ready serialization still a valid
single-state relay carrier?

Falsifier: any original gate fails after serialization.

## 3. Tested Hypothesis

Moving \(A\) one position later and replacing the random selector with a fixed
marker preserves two-layer relay capability and standard-head causal use.

## 4. Rival Explanations

The E01 pass depended on the old position, duplicate examples appear after
removing selector variation, or donor/counterfactual construction becomes
invalid.

## 5. Data / Model / Algorithm / Objective

Enumerate 256 unique \((A,B)\) pairs. Evaluation iff
\((A+2B)\bmod5=0\). Use the fixed seven-token sequence, the original masks,
width-64 learner, cosine schedule, and NTP-only loss.

## 6. Conditions, Seeds, And Checkpoints

The original three carrier conditions, seeds 1301--1305, and 20-step grid
through 3,000.

## 7. Primary Metric

Original six-gate conjunction; no threshold change.

## 8. Secondary Metrics

Answer NLL, threshold steps, nuisance-\(B\) invariance, and donor follow.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: E01 single-value relay passed all gates.

Known bad: one-layer relay remains structurally disconnected.

Known confusing: zero Bayes entropy does not mean the answer target is as easy
to optimize as a fixed marker.

## 10. Stage-Level Profiling Plan

Audit unique serialized rows, split disjointness, graph reachability,
trajectories, \(A/B\) counterfactuals, and donor patches.

## 11. Algorithm Specification

Use the registered runner with `task_mode=copy_matched`; no objective other
than NTP may be activated.

## 12. Success / Failure / Insufficient Evidence

Pass freezes this exact data/model surface for objective comparison. Fail
returns to carrier design and blocks MTP.

## 13. What This Cannot Claim

No objective effect or workload transfer.

## 14. Review Notes And Protocol Changes

Self-review:

- one serialization factor changed: yes;
- duplicated q variants removed: yes;
- auxiliary objectives still blocked: yes;
- original gates retained: yes.

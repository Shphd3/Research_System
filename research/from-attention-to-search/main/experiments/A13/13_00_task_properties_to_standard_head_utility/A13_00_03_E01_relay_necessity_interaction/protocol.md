# Protocol: A13_00_03_E01 Relay-Necessity Objective Interaction

## 0. Approval Snapshot

Approval status: approved under standing autonomous authorization.

Purpose: test whether relay necessity amplifies the finite-budget
standard-head benefit of Next-2 auxiliary supervision.

Primary anchor:
[13_00_03](../../../../problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_03_relay_necessity_objective_interaction_anchor.md)

Experiment role: first objective comparison after carrier validation.

One changed factor: auxiliary target content/horizon within each path, followed
by a registered interaction across relay-required and bypass-available paths.

## 1. Terminology / Definitions

| Term | Plain meaning | Computation | Unit | Decision role | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| answer NLL | penalty assigned by the ordinary head to the correct answer | \(-\log p_1(Y)\) | nats per example | primary learning curve | internal causal mechanism |
| AULC | average height of the answer-NLL learning curve | trapezoid area from step 0 to 1,000 divided by 1,000 | nats | finite-budget utility | wall-clock efficiency |
| \(U_r\) | shared-aux answer loss minus Next-2 answer loss on path \(r\) | paired AULC difference | nats | information/horizon contrast | pure semantic-content effect |
| \(\Delta_{\mathrm{relay}}\) | increase in \(U\) caused by requiring the relay | \(U_{\mathrm{relay}}-U_{\mathrm{bypass}}\) | nats | primary task-property interaction | workload transfer |

## 2. Anchor Alignment

Decision question: does structural relay necessity amplify useful earlier
answer credit?

Primary falsifier: a non-positive relay interaction with all carrier guards
still valid.

## 3. Tested Hypothesis

Both mean \(U_{\mathrm{relay}}\) and mean \(\Delta_{\mathrm{relay}}\) are at least
0.02 nats, their paired bootstrap 95% lower bounds are positive, and at least
seven of eight paired seeds are positive.

## 4. Rival Explanations

1. Later standard-head NTP credit is already sufficient.
2. General auxiliary regularization, not future content, causes any gain.
3. The Next-2 all-position background is noisier and cancels the source signal.
4. One objective/path cell fails to learn or stops using the relay.
5. An auxiliary-target entropy mismatch creates an artificial gain.

## 5. Data / Model / Algorithm / Objective

Use 256 unique \((A,B)\) pairs, with 204 train and 52 held-out pairs under
\((A+2B)\bmod5=0\). Sequence:

```text
[BOS] [FIXED] [A] [B] [RELAY] [ANSWER] [A]
```

Use width 64, two layers, four heads, FFN width 256, zero dropout, tied
standard-head embeddings, AdamW, cosine learning rate from 0.003 to 0.0001,
batch 256, and gradient clipping at 1.

Objectives:

1. `NTP`: six ordinary next-token terms.
2. `shared_aux`: ordinary NTP plus five auxiliary next-token terms, averaged
   with equal nominal objective weight.
3. `info_mtp`: ordinary NTP plus five auxiliary Next-2 terms, with the same
   weight and trainable parameters as `shared_aux`.

## 6. Conditions, Seeds, And Checkpoints

Paths: `relay`, `bypass`.

Objectives: `NTP`, `shared_aux`, `info_mtp`.

Paired registered seeds: 1401--1408.

Train through 3,000 steps; evaluate every 20 steps. Freeze the primary AULC
horizon at 1,000 steps. Do not select a different horizon after seeing
objective results.

## 7. Primary Metric

For every seed,

\[
U_r
=
\operatorname{AULC}_{\mathrm{SA},r}
-
\operatorname{AULC}_{\mathrm{MTP},r},
\qquad
\Delta_{\mathrm{relay}}
=
U_{\mathrm{relay}}-U_{\mathrm{bypass}}.
\]

Primary pass requires:

- all capability and relay-use guards pass;
- bootstrap lower 95% bounds for mean \(U_{\mathrm{relay}}\) and mean
  \(\Delta_{\mathrm{relay}}\) are above zero;
- both mean effects are at least 0.02 nats;
- at least seven of eight paired seeds are positive for each.

## 8. Secondary Metrics

Final standard-head answer accuracy/NLL, NTP-to-MTP system contrast,
auxiliary accuracy at the relay, initial shared-trunk gradient norms/cosines,
and relay donor interventions.

None may override the primary metric.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: the exact NTP relay and bypass carrier passed in
`A13_00_02_E02`.

Known bad: one-layer relay is structurally disconnected and is not part of
this comparison.

Known confusing: a positive local auxiliary gradient does not imply positive
full-objective utility; final saturation can hide a finite-budget difference.

## 10. Stage-Level Profiling Plan

Record per-seed standard-head trajectories, final capability, auxiliary
performance, shared-trunk gradient diagnostics, input/data audit, donor-patch
causal use, paired effects, bootstrap intervals, and rendered learning curves.

## 11. Algorithm Specification

For each paired seed, instantiate the same model before each objective/path
condition, replay the same mini-batch index stream, optimize the registered
full objective, and evaluate only the ordinary standard head for the primary
metric.

## 12. Success / Failure / Insufficient Evidence

Pass, fail, and insufficient follow the anchor definitions exactly. If a
capability or relay-use guard fails, no objective ranking is interpreted.

## 13. What This Cannot Claim

The contrast does not establish pure information-content causality independent
of prediction horizon, standard-MTP architecture equivalence, code or language
advantage, long-context scaling, composition, planning, MoE value, or training
compute superiority.

## 14. Review Notes And Protocol Changes

Self-review before execution:

- carrier passed on the exact serialization: yes;
- auxiliary label-count and Bayes-entropy sums matched: yes;
- shared-aux is the primary control and NTP secondary: yes;
- target horizon frozen before results: yes;
- seeds and thresholds registered before results: yes;
- exactly one interaction decision: yes.

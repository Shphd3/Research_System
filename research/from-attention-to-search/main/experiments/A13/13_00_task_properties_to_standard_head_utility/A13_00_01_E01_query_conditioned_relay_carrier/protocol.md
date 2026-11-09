# Protocol: A13_00_01_E01 Query-Conditioned Relay Carrier

## 0. Approval Snapshot

Approval status: approved under the researcher's standing autonomous-execution
authorization of 2026-07-16; self-audit required before interpretation.

Purpose: decide whether one fixed minimal carrier is structurally valid,
learnable by a two-layer NTP model, and causally used by the standard head.

Primary anchor:
[13_00_01](../../../../problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_01_query_conditioned_relay_carrier_anchor.md)

Anchor decision question: can a two-layer NTP Transformer solve held-out
query-conditioned selection only through the registered relay?

Anchor physical prior tested: forming a relay and consuming it require two
successive state transitions under the frozen attention graph.

Anchor core model term tested: \(S_1=f_{\theta,1}(A,B,Q)\) followed by
\(\hat Y=g_{\theta,2}(S_1)\).

Anchor falsifier: a capable two-layer model whose answer does not follow an
in-distribution relay-state patch.

Experiment role: operationalization and carrier-validity audit.

Primary metric from anchor: Boolean carrier eligibility
\(C_{\mathrm{eligible}}=\bigwedge_j G_j\).

Claim boundary from anchor: carrier eligibility only; no MTP comparison.

Minimal setup: 16 value tokens, 7-token sequence, width 64, one/two layers,
five registered seeds.

Basic configuration: AdamW, fixed split, fixed sparse mask, all-position NTP,
standard-head answer evaluation.

Conditions to run: `relay_1L`, `relay_2L`, and `bypass_1L`.

Pass: all six registered gates pass.

Fail: at least one gate gives a decisive negative result under a compliant run.

Insufficient: implementation replay, split audit, intervention pairing, or
training completion is invalid.

Cannot claim: any NTP/MTP difference, general Transformer capability, long
context, code, natural language, planning, or MoE value.

Approval decision: execute Stage 0 only. Objective comparison remains blocked
until this record is closed as `pass`.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| relay | the only state the answer may read in the relay condition | layer-1 hidden vector at position 4 | 64-dimensional vector | isolates formation and use | semantic meaning |
| held-out triple | a value-pair/selector combination absent from training | \((A,B,Q)\) split by a frozen hash rule | exact set membership | prevents triple lookup | general algorithm learning |
| donor patch | replace one example's relay state with another in-distribution relay state | layer-1 position-4 tensor replacement | follow rate | tests standard-head causal use | exclusive use of one coordinate |
| carrier eligibility | serial validity verdict | conjunction of \(G_1,\ldots,G_6\) | Boolean | blocks invalid objective comparisons | MTP utility |

## 2. Anchor Alignment

Decision question: carrier validity and learner eligibility only.

Physical prior tested: two transitions are necessary and sufficient under the
registered graph.

Core model term tested: formation \(f_{\theta,1}\) and consumption
\(g_{\theta,2}\).

Falsifier: two-layer capability without donor-patch control.

Claim boundary: synthetic, two-layer, fixed-mask, NTP-only.

## 3. Tested Hypothesis

The two-layer relay model learns held-out query-conditioned selection and its
ordinary answer follows the layer-1 relay content. The one-layer relay model
cannot solve the task, while the one-layer bypass control can.

## 4. Rival Explanations

1. direct answer reachability;
2. train/evaluation triple overlap;
3. fixed output or ignored selector;
4. generic one-layer learner or output-interface failure;
5. intervention damage rather than content-specific causal control;
6. implementation mismatch between the registered and executed masks.

## 5. Data / Model / Algorithm / Objective

Data sequence:

```text
[BOS] [value-A] [value-B] [selector] [RELAY] [ANSWER] [selected-value]
```

The target is \(A\) for selector 0 and \(B\) for selector 1. All 512 triples are
enumerated. A frozen deterministic split assigns approximately 80% to training
and 20% to evaluation while preserving every value and selector in both.

The model is a pre-layer-normalized causal Transformer with tied token
embedding/standard-head weights. The same mask is used in every layer.
`RELAY` reads positions 1, 2, 3, and itself. Relay-required `ANSWER` reads only
positions 4 and 5. Bypass `ANSWER` additionally reads positions 1, 2, and 3.

Training activates only

\[
\mathcal L_{\mathrm{NTP}}
=
\frac{1}{6}\sum_{t=0}^{5}
\operatorname{CE}(p_1(h_t),x_{t+1}).
\]

The answer metric uses only \(p_1(h_5)\).

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence role | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `relay_1L` | two transitions are necessary | shortcut mask | structural negative control | primary guard | all seeds \(\le0.15\) | stable \(>0.15\) | mask mismatch | trajectory figure |
| `relay_2L` | two transitions are sufficient | carrier capability | eligibility | primary | mean \(\ge0.95\), 4/5 \(\ge0.90\) | powered low accuracy | incomplete run | trajectory figure |
| `bypass_1L` | learner/interface works | generic capacity rival | positive control | primary guard | mean \(\ge0.95\), 4/5 \(\ge0.90\) | powered low accuracy | incomplete run | trajectory figure |
| counterfactual audit | answer uses selected value and selector | fixed-output rival | semantic behavior guard | primary guard | both rates \(\ge0.90\) | either below | too few valid pairs | audit table |
| donor patch | answer uses relay content | damage/readability rival | causal-use guard | primary guard | follow \(\ge0.90\), preserve \(\ge0.95\) | either below | invalid donors | audit table |

Registered seeds: `1301, 1302, 1303, 1304, 1305`.

Implementation-only smoke seed: `1299`; it cannot enter the verdict.

Checkpoints: step 0 and every 20 optimization steps through step 1000.

## 7. Primary Metric

\(C_{\mathrm{eligible}}\) is `pass` only when every gate in the anchor passes.
False positives are more costly than false negatives because an invalid pass
would contaminate every later objective comparison. A fail removes only this
carrier, not general MTP.

## 8. Secondary Metrics

- answer negative log-likelihood in nats;
- steps to `0.90` and `0.95` held-out accuracy;
- selected-value counterfactual follow rate;
- unselected-value invariance rate;
- same-label donor preservation rate;
- different-label donor follow rate;
- condition-wise prediction histograms.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: one-layer bypass should learn because the answer directly sees all
needed tokens.

Known bad: one-layer relay sees only the constant input relay embedding at its
single answer transition.

Known confusing: held-out triples reuse individual values by design. This
tests unseen combinations, not unseen token identities or broad compositional
generalization.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| generator | are labels and splits exact? | exhaustive triples | no overlap; balanced marginals | split JSON | model |
| mask | is relay the unique path? | allowed-edge matrix | exact reachability matches condition | mask JSON/PNG | training |
| training | are controls and test scale behaving as predicted? | trajectories | registered capability thresholds | CSV/PNG | intervention |
| counterfactual | does input behavior follow the selected value? | paired held-out examples | registered follow/invariance rates | CSV | patch |
| patch | does the standard head follow relay content? | in-distribution donors | registered donor rates | CSV | verdict |

## 11. Algorithm Specification

input: exhaustive triples, condition, seed.

parameters: width 64; heads 4; layers 1 or 2; batch 256; AdamW learning rate
`0.003`; betas `(0.9,0.95)`; weight decay `0.01`; gradient clip `1.0`; 1000
steps; dropout 0.

intermediate variables: layer-1 relay state, standard-head answer logits,
counterfactual pairs, same/different-label donor indices.

steps:

1. enumerate and audit the frozen split;
2. instantiate the fixed attention graph and verify reachability;
3. train every condition/seed for the fixed budget;
4. evaluate the standard answer trajectory;
5. run counterfactual input pairs on `relay_2L`;
6. cache layer-1 relay states and run in-distribution donor patches;
7. compute every registered gate before any interpretation.

outputs: run manifest, trajectories CSV, gate JSON, intervention CSV, summary
JSON, and one decision figure.

debug artifacts: split/mask audit, per-seed curves, prediction histograms, donor
pair counts.

pass conditions: all registered gates pass.

fail conditions: any decisive gate fails.

failure reasons: `split_invalid`, `mask_bypass`, `learner_floor`,
`interface_failure`, `counterfactual_failure`, `relay_nonuse`, or
`implementation_noncompliance`.

## 12. Success / Failure / Insufficient Evidence

Success authorizes only the objective-by-relay comparison. Failure triggers one
failure decomposition. A repair is permitted only if it targets a verified
implementation, learner, or intervention defect without changing the task
property. Otherwise the carrier is closed.

## 13. What This Cannot Claim

This experiment cannot compare objectives, prove a general depth law, establish
multi-evidence joint computation, or transfer to code, text, planning,
long-context retrieval, or MoE.

## 14. Review Notes And Protocol Changes

Self-review before execution:

- one question: yes;
- NTP only: yes;
- one/two-layer boundary: yes;
- fixed task across conditions: yes;
- known-good and known-bad controls: yes;
- objective comparison blocked: yes.

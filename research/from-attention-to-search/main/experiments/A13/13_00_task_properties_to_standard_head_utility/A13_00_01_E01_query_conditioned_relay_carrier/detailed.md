# Detailed: A13_00_01_E01 Query-Conditioned Relay Carrier

Primary anchor:
[13_00_01](../../../../problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_01_query_conditioned_relay_carrier_anchor.md)

Protocol: [protocol.md](protocol.md)

Summary: [summary.md](summary.md)

## 0. Quick Recap

Purpose: validate a minimal carrier before comparing NTP and MTP.

Hypothesis: two layers learn and causally use the relay; one relay layer fails;
one bypass layer succeeds.

Experiment logic: the same tokens and labels are evaluated under an exact
relay graph and a direct bypass graph.

Conclusion: the structure passed, but the 1,000-step capability gate failed.

Evidence: two-layer relay mean accuracy `0.7243`; one-layer relay `0.0641`;
one-layer bypass `0.9320`.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| standard-head answer | the prediction used at inference | main-head logits at input position 5 | accuracy or NLL | functional endpoint | internal algorithm |
| relay patch | replace the layer-1 position-4 state with an in-distribution donor | full 64-dimensional state replacement | donor-follow rate | tests causal content use | coordinate-level mechanism |
| capability floor | the tested model does not reliably solve the task | accuracy below the registered gate | fraction correct | blocks objective interpretation | why all Transformers fail |

## 2. Anchor Link And Decision Point

This run tests only `13_00_01`. A fail blocks `13_00_02`; no objective
comparison is permitted.

## 3. Protocol Compliance Audit

approved conditions match actual conditions: yes.

primary metric exists: yes, all six gates were computed.

central figures/tables exist: yes.

seeds/checkpoints recorded: yes, five seeds and 51 checkpoints per condition.

known good/bad/confusing cases reviewed: yes.

success/failure/insufficient-evidence criteria applied: yes.

Execution note: the first formal process completed all training and CSV writes
but failed when serializing a NumPy Boolean into JSON. The serializer was
repaired without changing the task or run contract. A full same-contract replay
reproduced every research metric exactly; only elapsed-time fields differed.
The replay wrote `summary.json` successfully, then hit the same type conversion
in terminal printing. That final print path was also repaired. The completed
CSV and JSON artifacts are valid; neither print defect affected training.

## 4. Setup

Research question: is the fixed carrier eligible?

Data construction: exhaustive \((A,B,Q)\) triples, with
\(Y=A\) for \(Q=0\) and \(Y=B\) for \(Q=1\).

Train / eval split: evaluation iff \((A+2B+Q)\bmod5=0\); 409/103 triples; no
overlap; all value identities and both selectors occur in both splits.

Model: width 64, four attention heads, FFN width 256, pre-layer norm, tied
standard unembedding, inactive auxiliary head.

Input representation: learned token and position embeddings.

Loss: all-position next-token cross-entropy.

Optimizer: AdamW, learning rate `0.003`, betas `(0.9,0.95)`, weight decay
`0.01`, gradient clip `1.0`.

Training: batch 256, 1,000 steps, evaluation every 20 steps, FP32.

Seeds: 1301--1305.

Conditions: `relay_1L`, `relay_2L`, `bypass_1L`.

Changed variables: layer count and answer attention access.

Held fixed: all other registered objects.

Known limitation: the bypass task is structurally easier; it is an interface
positive control, not a difficulty-matched objective comparison.

## 5. Metrics And Decision Rules

The primary Boolean gate and exact thresholds are in [protocol.md](protocol.md).
Answer NLL is in nats per held-out example. Counterfactual and patch rates are
fractions over 103 held-out recipients.

## 6. Main Results

### Decision evidence

| Seed | relay 1L | relay 2L | bypass 1L |
| ---: | ---: | ---: | ---: |
| 1301 | 0.0680 | 0.9320 | 1.0000 |
| 1302 | 0.0583 | 0.7573 | 1.0000 |
| 1303 | 0.0583 | 0.7476 | 1.0000 |
| 1304 | 0.0680 | 0.6117 | 1.0000 |
| 1305 | 0.0680 | 0.5728 | 0.6602 |
| mean | 0.0641 | 0.7243 | 0.9320 |

### Stage-level profiling evidence

- `relay_1L` stayed at chance in every seed.
- four bypass seeds reached exact accuracy between 120 and 260 steps; seed
  1305 was still learning at step 1,000.
- the best relay seed first crossed `0.95` at step 720 but later fluctuated;
  seeds 1304 and 1305 were still rising late.

### Failed or ambiguous evidence

Counterfactual and patch aggregates cannot be read as independent mechanism
failures because most clean checkpoints did not pass capability. In seed 1301,
the different-label donor-follow rate was `1.0`, showing that the proposed
intervention is capable of producing content-specific control once the model
is sufficiently learned.

## 7. Visualization Results

### Carrier capability and structural depth controls

![Carrier capability and structural depth controls](figures/carrier_trajectory.png)

Purpose: separate graph depth from generic learner failure.

Setup: five seeds, three registered conditions, 1,000 steps.

Metric definition: fraction of 103 held-out answers predicted correctly by the
ordinary head.

How to read: chance is `0.0625`; the registered capability gate is `0.95`.

Expected if supported: relay 1L stays at chance; relay 2L and bypass 1L reach
the gate.

Observed result: only the negative depth control fully matched the prediction.

Take-home: the graph is behaving as intended, but the learner budget is not yet
an eligible comparison surface.

Remaining uncertainty: insufficient steps versus unstable optimization.

What this figure does not prove: that budget extension will solve the carrier.

Anchor update implication: test budget before altering optimizer or workload.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| data | zero overlap; balanced identities/selectors | passed | none | triple leakage |
| graph | exact reachability matches all three conditions | passed | none | hidden direct path |
| depth negative | relay 1L mean `0.0641` | passed | none | accidental one-layer relay |
| interface positive | 4/5 exact; one seed `0.6602` | failed threshold | late/unstable acquisition | universal interface impossibility |
| relay capability | mean `0.7243`; one seed `0.9320` | failed | budget or optimization stability | immediate carrier eligibility |
| input counterfactual | aggregate below gate | unclear downstream | clean capability absent | no independent mechanism verdict |
| relay patch | aggregate below gate; one capable seed follows donor perfectly | unclear downstream | clean capability absent | intervention impossibility |

Falsified physical prior: none.

Falsified mathematical model: none.

Falsified operationalization / proxy: carrier eligibility at the registered
1,000-step budget.

Falsified implementation: terminal JSON/print serialization only; repaired and
replayed.

Falsified metric: none, although patch preservation must always be interpreted
relative to clean capability.

Remaining rivals: insufficient training budget and constant-learning-rate
instability.

Final causal path:

```text
carrier fail
-> data leak and graph shortcut falsified
-> generic interface impossibility weakened by 4/5 exact bypass seeds
-> verified bottleneck: unstable two-layer acquisition within 1,000 steps
-> next targeted test: budget only
```

## 9. Full Experiment Record

Runtime: `48.97` seconds for the same-contract replay on one H100 GPU.

Formal output:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/a13_00_01_e01_query_relay_full_replay_20260716`

## 10. Interpretation

The E01 failure is useful: unlike A12 E04, the task itself and the intended
path survived direct audit. The remaining failure is narrower—this exact
learner/optimizer/budget does not yet provide a stable capability surface. A
budget-only replay can now decide whether the failure is premature stopping or
a more persistent optimization problem.

## 11. Claim Boundary

Supported: structural validity and the one-layer depth impossibility under the
fixed mask.

Weakened: eligibility within 1,000 steps.

Unresolved: stable two-layer capability and standard-head relay use after
capability.

Cannot claim: any objective effect.

## 12. Next Decision

Run E02 with only the maximum step budget changed to 3,000.

## 13. Links And Artifact Map

anchor:
[13_00_01](../../../../problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_01_query_conditioned_relay_carrier_anchor.md)

protocol: [protocol.md](protocol.md)

summary: [summary.md](summary.md)

code workspace:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

runner:
`active/synthetic_data_understanding/scripts/run_a13_query_conditioned_relay.py`

config:
`active/synthetic_data_understanding/configs/a13_00_01_e01_query_conditioned_relay_carrier.json`

result dir:
`active/synthetic_data_understanding/outputs/a13_00_01_e01_query_relay_full_replay_20260716`

figure dir: [figures](figures)

key tables:
[final metrics](tables/final_metrics.csv),
[counterfactual audit](tables/counterfactual_audit.csv), and
[relay patch audit](tables/relay_patch_audit.csv).

repro command:

```bash
python active/synthetic_data_understanding/scripts/run_a13_query_conditioned_relay.py \
  --config active/synthetic_data_understanding/configs/a13_00_01_e01_query_conditioned_relay_carrier.json \
  --output active/synthetic_data_understanding/outputs/a13_00_01_e01_query_relay_full_replay_20260716 \
  --device cuda:0
```

job id: local GPU process; no cluster job.

# Detailed: A13_00_01_E04 Width-Only Carrier Capacity Audit

Primary anchor:
[13_00_01](../../../../problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_01_query_conditioned_relay_carrier_anchor.md)

Protocol: [protocol.md](protocol.md)

Summary: [summary.md](summary.md)

## 0. Quick Recap

Purpose: test width insufficiency.

Conclusion: width 128 worsened relay capability; close the carrier.

Evidence: relay mean `0.6194`, bypass mean `0.9534`, relay 1L `0.0583`.

## 1. Terminology / Definitions

Definitions are in [summary.md](summary.md) and [protocol.md](protocol.md).

## 2. Anchor Link And Decision Point

E04 is the registered final repair for `13_00_01`.

## 3. Protocol Compliance Audit

Only the width scale changed: yes.

Original task, seeds, schedule, and gates retained: yes.

All artifacts and interventions completed: yes.

Failure criteria applied: yes.

## 4. Setup

Width 128, FFN 512, four heads, one/two layers, NTP only, cosine schedule,
3,000 steps, seeds 1301--1305. Runtime was `144.88` seconds on one H100.

## 5. Metrics And Decision Rules

Unchanged six-gate carrier conjunction.

## 6. Main Results

| Seed | relay 2L final | relay 2L best | bypass 1L final |
| ---: | ---: | ---: | ---: |
| 1301 | 0.2621 | 0.3107 | 0.7670 |
| 1302 | 1.0000 | 1.0000 | 1.0000 |
| 1303 | 0.6505 | 0.6893 | 1.0000 |
| 1304 | 0.8252 | 0.8544 | 1.0000 |
| 1305 | 0.3592 | 0.4854 | 1.0000 |

## 7. Visualization Results

![Width-128 carrier trajectories](figures/carrier_trajectory.png)

Purpose: test whether a wider shared state stabilizes query-conditioned relay.

Metric: held-out answer accuracy.

Observed: no; performance became more seed-dependent.

Take-home: increasing capacity is not a valid carrier repair.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | Interpretation |
| --- | --- | --- | --- |
| graph/data | unchanged and valid | pass | task plumbing remains correct |
| one-layer relay | chance | pass | no hidden bypass |
| one-layer bypass | mean above gate | pass | output interface works |
| two-layer relay | mean `0.6194` | fail | wider learner not eligible |
| intervention | donor follow `0.7922` | fail downstream | clean capability absent |

Falsified explanation: missing width as a monotonic repair.

Remaining bottleneck: the first carrier requires query binding in addition to
relay transport.

Final causal path:

```text
query-conditioned carrier failure
-> budget extension insufficient
-> cosine schedule nearly repairs but remains unstable
-> width increase worsens
-> stop learner tuning
-> separate relay from query binding
```

## 9. Full Experiment Record

Raw result:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/a13_00_01_e04_width_capacity_20260716`

## 10. Interpretation

This negative sequence updates the research design: query-conditioned
selection is not a harmless carrier detail. It is a separate task property and
must not be present in the baseline used to ask whether relay necessity alone
amplifies MTP.

## 11. Claim Boundary

No general NTP, MTP, Transformer, code, or composition conclusion.

## 12. Next Decision

Validate a single-value relay carrier.

## 13. Links And Artifact Map

runner:
`active/synthetic_data_understanding/scripts/run_a13_query_conditioned_relay.py`

config:
`active/synthetic_data_understanding/configs/a13_00_01_e04_width_capacity.json`

tables:
[final](tables/final_metrics.csv),
[counterfactual](tables/counterfactual_audit.csv),
[patch](tables/relay_patch_audit.csv).

figure: [trajectory](figures/carrier_trajectory.png).

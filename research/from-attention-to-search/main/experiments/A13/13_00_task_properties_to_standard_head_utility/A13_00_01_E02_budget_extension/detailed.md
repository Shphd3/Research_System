# Detailed: A13_00_01_E02 Budget-Only Carrier Replay

Primary anchor:
[13_00_01](../../../../problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_01_query_conditioned_relay_carrier_anchor.md)

Protocol: [protocol.md](protocol.md)

Summary: [summary.md](summary.md)

## 0. Quick Recap

Purpose: test the budget-insufficiency explanation of E01.

Hypothesis: the unchanged carrier passes by 3,000 steps.

Conclusion: rejected; mean relay accuracy was `0.8097`.

Evidence: exact E01 prefix replay, passing bypass control, persistent
seed-dependent relay plateaus and late fluctuations.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object | Unit | Decision role | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| exact prefix replay | E02 matches E01 through step 1,000 | equality of seed/condition/checkpoint research metrics | Boolean | validates one-variable change | bitwise runtime equality |
| plateau | accuracy stops improving over a long interval | trajectory pattern | fraction correct | localizes learner failure | unique optimization cause |

## 2. Anchor Link And Decision Point

E02 remains inside the carrier subanchor. No objective comparison is
admissible.

## 3. Protocol Compliance Audit

approved conditions match actual conditions: yes.

primary metric exists: yes.

central figures/tables exist: yes.

seeds/checkpoints recorded: yes.

known good/bad/confusing cases reviewed: yes.

failure criteria applied: yes.

Prefix replay: all 765 rows through step 1,000 match E01 exactly on seed,
condition, layer, path, step, accuracy, answer NLL, and all-position NLL.

## 4. Setup

All E01 settings are retained. Only maximum training steps changed from 1,000
to 3,000. Runtime was `141.31` seconds on one H100 GPU.

## 5. Metrics And Decision Rules

Unchanged from E01. Final clean capability must precede interpretation of
counterfactual or patch aggregates.

## 6. Main Results

| Seed | relay 1L | relay 2L | bypass 1L | best relay 2L |
| ---: | ---: | ---: | ---: | ---: |
| 1301 | 0.0583 | 0.9126 | 1.0000 | 0.9709 |
| 1302 | 0.0583 | 0.7573 | 1.0000 | 0.7767 |
| 1303 | 0.0680 | 0.7573 | 1.0000 | 0.7767 |
| 1304 | 0.0583 | 0.9515 | 1.0000 | 1.0000 |
| 1305 | 0.0583 | 0.6699 | 0.7573 | 0.6699 |

The data and graph gates remain passed. The bypass mean now crosses its
registered threshold. The relay capability gate still fails.

## 7. Visualization Results

### Extended carrier trajectories

![Extended carrier trajectories](figures/carrier_trajectory.png)

Purpose: test budget sufficiency.

Setup: exact E01 contract with 2,000 additional updates.

Metric: held-out answer accuracy, fraction correct.

Expected if supported: every capable condition stabilizes above `0.95`.

Observed: only two relay seeds approached or reached the gate; three plateaued.

Take-home: update count is not the only bottleneck.

Remaining uncertainty: persistent step-size noise versus initialization basin.

What this does not prove: that the constant learning rate is the cause.

Anchor update implication: schedule is the next isolated variable.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| replay | 765/765 rows match | pass | none | implementation drift |
| structural controls | relay 1L chance; bypass mean above gate | pass | none | mask leak and generic interface floor |
| relay capability | mean `0.8097` | fail | persistent seed dependence | budget-only explanation |
| late stability | capable seeds fluctuate after crossing | fail | non-decaying updates remain large | stable convergence at constant rate |
| causal audits | below gate with clean capability absent | unclear | downstream | independent non-use conclusion |

Falsified physical prior: none.

Falsified mathematical model: none.

Falsified operationalization: constant-rate 3,000-step learner eligibility.

Falsified implementation: none.

Falsified metric: none.

Remaining rivals: constant learning-rate background noise and initialization
basins.

Final causal path:

```text
E01 capability failure
-> exact longer replay
-> bypass succeeds and relay partially improves
-> budget-only explanation rejected
-> non-decaying optimization becomes the next isolated rival
```

## 9. Full Experiment Record

Raw result directory:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/a13_00_01_e02_budget_extension_20260716`

## 10. Interpretation

The correct update is not “make the task easier” or “try MTP.” The task has a
known structural path and at least two successful two-layer trajectories. The
remaining uncertainty is whether standard NTP can acquire that path reliably
under a stabilizing schedule.

## 11. Claim Boundary

No objective, code, language, long-context, or MoE claim is supported.

## 12. Next Decision

Change only the learning-rate schedule and rerun the same 3,000-step matrix.

## 13. Links And Artifact Map

runner:
`active/synthetic_data_understanding/scripts/run_a13_query_conditioned_relay.py`

config:
`active/synthetic_data_understanding/configs/a13_00_01_e02_budget_extension.json`

tables:
[final](tables/final_metrics.csv),
[counterfactual](tables/counterfactual_audit.csv),
[patch](tables/relay_patch_audit.csv).

figure: [carrier trajectory](figures/carrier_trajectory.png).

repro command:

```bash
python active/synthetic_data_understanding/scripts/run_a13_query_conditioned_relay.py \
  --config active/synthetic_data_understanding/configs/a13_00_01_e02_budget_extension.json \
  --output active/synthetic_data_understanding/outputs/a13_00_01_e02_budget_extension_20260716 \
  --device cuda:0
```

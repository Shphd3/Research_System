# Protocol: A06_01_01_E06 Common-Centered Residual Geometry Diagnostic

## 0. Approval Snapshot

Approval status:
Approved for implementation and full run by the user's active sequential-anchor objective on 2026-06-21.

Purpose:
Diagnose why load imbalance remains after A06_01_01_E05 hidden common-centering in the initialized synthetic hidden-state setting.

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Anchor decision question:
After hidden common-centering, what explains the remaining step-0 load imbalance: residual hidden anisotropy, router-direction cell geometry, random-context / position structure, or finite-sample noise?

Anchor physical prior tested:
Removing the global hidden common component removes the feature-shared effective bias term, but the residual hidden states may still be anisotropic or structured by context and position.

Anchor core model term tested:
The residual replay score \(z^C_{i,e}=w_e^\top r_i\) with \(r_i=h_i-c\).

Anchor falsifier:
The named residual sources are weakened if residual load is fully explained by finite-sample noise, or if whitening, isotropic controls, and context / position controls do not change or explain residual \(L\).

Experiment role:
Root-cause audit, not method construction.

Primary metric from anchor:
Load imbalance \(L=m\max_e |p_e-1/m|\) under common-centered replay.

Claim boundary from anchor:
Initialized synthetic hidden-state replay only. No training, no real text, no semantic specialization, no router method.

Minimal setup:
Reuse the A06_01_01_E05 synthetic `(slot,target)` construction and final-router hidden-state extraction; rerun extraction if hidden states were not persisted.

Basic configuration:
`seq_len=32`, 4 uniform `(slot,target)` pairs, 4 experts, randomized pair start, random background tokens independent of pair id, route at last slot position.

Conditions to run:
`centered_replay`, `centered_whitened_replay`, `matched_isotropic_replay`, `context_position_stratified_replay`, and `sample_count_guard`.

Pass:
One named residual source explains the common-centered residual \(L\) with matched controls and valid audits.

Fail:
Residual \(L\) is indistinguishable from finite-sample floor, or controls do not separate any named residual source.

Insufficient:
Hidden states / router rows are mismatched, whitening changes model state, isotropic controls are not matched, strata are too sparse, or sample-count guard is missing.

Cannot claim:
Training collapse, real-text routing, semantic expert specialization, expert utility, or a deployable initialization method.

Approval decision:
Approved. Execute after reusing the A06_01_01_E05 synthetic hidden-state sweep contract and before entering A06_01_02_E01.

## 1. Anchor Alignment

Decision question:
Which residual source explains the remaining load after common-centering?

Physical prior tested:
Zero-mean residual hidden states can still have nonuniform routing cells because their covariance, context structure, or router-direction geometry may be non-isotropic.

Core model term tested:
\(z^C_{i,e}=w_e^\top(h_i-c)\) and the distribution \(P_r\) of residual states.

Falsifier:
The residual load shrinks to finite-sample floor, or all named residual controls fail to explain it.

Claim boundary:
Synthetic initialized hidden-state replay only.

## 2. Tested Hypotheses

H1:
Residual covariance anisotropy contributes if whitening \(r_i\) reduces \(L\) relative to centered replay.

H2:
Router-direction cell geometry contributes if matched isotropic residual samples have lower \(L\) than real residuals under the same router rows.

H3:
Context / position structure contributes if conditional load shifts systematically with pair start, local context, or background-token factors.

H4:
Finite-sample noise explains the residual if bootstrap / larger-sample estimates drive residual \(L\) toward zero.

## 3. Rival Explanations

R1:
The residual is only finite-sample measurement noise.

Separated by:
Bootstrap and larger-sample guard.

R2:
The residual is caused by covariance anisotropy.

Separated by:
Whitening and covariance spectrum.

R3:
The residual is caused by router-direction cells rather than real hidden structure.

Separated by:
Matched isotropic residual control with the same router rows.

R4:
The residual is caused by non-feature context or pair position.

Separated by:
Context / position-conditioned load tables and shuffle controls.

## 4. Data / Model / Algorithm / Objective

Data:
Same uniform synthetic `(slot,target)` task as A06_01_01_E05.

Model:
Initialized dot-product top-1 synthetic Transformer-MoE. No training.

Algorithm:
Replay router scores on extracted hidden states and controlled residual variants.

Objective:
No optimization objective. This is a diagnostic replay.

## 5. Conditions, Seeds, And Checkpoints

Seeds:
Use A06_01_01_E05 seeds unless a smoke run uses fewer:
`20260521,20260522,20260523,20260524,20260525,20260526,20260527,20260528`.

Checkpoints:
Initialization / step 0 only.

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `centered_replay` | baseline after A06_01_01_E05 | \(w_e^\top r_i\) | defines residual load | primary | baseline exists | missing | wrong hidden states | `tables/results.csv` |
| `centered_whitened_replay` | H1 | residual covariance anisotropy | tests whether anisotropy drives residual \(L\) | primary | lower \(L\) | unchanged \(L\) | invalid whitening | `figures/residual_load_by_condition.png` |
| `matched_isotropic_replay` | H2 | router-direction cell geometry | separates real residual distribution from isotropic baseline | primary | real residual higher than isotropic | similar \(L\) | norm/dimension mismatch | `tables/isotropic_control.csv` |
| `context_position_stratified_replay` | H3 | context / position structure | tests non-feature conditioning | secondary | systematic conditional shifts | no shifts | sparse strata | `tables/context_position_load.csv` |
| `sample_count_guard` | H4 | finite-sample floor | separates observed load from stable cell floor | primary | residual shrinks to zero | stable nonzero floor | no larger / bootstrap sample | `tables/bootstrap_floor.csv` |

## 6. Primary Metric

Primary metric:
\(L=m\max_e |p_e-1/m|\).

Why it decides:
The question is why common-centered top-1 load remains nonuniform. \(L\) directly measures the residual expert-load deviation to be explained.

Important metric split:
Following `daily_research_reports/0618/docs/theoretical_analysis.md`, observed residual load should be separated into true residual cell geometry and finite-sample noise whenever possible.

## 7. Secondary Metrics

- max load;
- active experts;
- per-expert load;
- covariance spectrum;
- whitened residual norm distribution;
- route agreement between centered and controlled replays;
- conditional loads by pair start and context;
- margin distribution.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good:
A06_01_01_E05 established that common-centering reduces \(L\) but leaves residual load.

Known bad:
Treating centered residual load as a method result without separating finite-sample noise.

Known confusing:
Whitening can change hidden norm scale and margin. It should be read as a diagnostic control, not a router proposal.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| state audit | Are A06_01_01_E05 hidden states and router rows reproduced or recovered? | tensor shapes | all seeds/depths present | `tables/state_audit.csv` | detailed |
| centered replay | Does residual load reproduce A06_01_01_E05 `RC/NC` scale? | condition table | comparable \(L\) | `tables/results.csv` | summary |
| whitening audit | Is whitening numerically stable? | eigenvalue spectrum | no singular / invalid transform | `tables/whitening_audit.csv` | detailed |
| isotropic control | Are isotropic samples dimension/norm/sample matched? | control audit | matched stats | `tables/isotropic_audit.csv` | detailed |
| context / position | Are strata populated enough? | strata counts | sufficient counts | `tables/strata_audit.csv` | detailed |
| finite-sample floor | Is residual \(L\) stable with sample count? | bootstrap / larger sample | floor estimate exists | `tables/bootstrap_floor.csv` | summary |

## 10. Algorithm Specification

input:
Synthetic batches, initialized model, final-router rows, hidden states at route position, pair start and background-token metadata.

parameters:
`num_pairs=4`, `num_experts=4`, `num_layers in {1,2,4}`, readout mode matching A06_01_01_E05, residual controls listed above.

intermediate variables:
\(h_i\), \(c\), \(r_i\), \(\Sigma_r\), whitened residuals, matched isotropic residuals, assignments, loads.

steps:
1. Reproduce or recover A06_01_01_E05 hidden states and router rows.
2. Compute residuals \(r_i=h_i-c\).
3. Replay centered baseline.
4. Whiten residuals and replay.
5. Generate matched isotropic residual controls and replay.
6. Compute context / position-conditioned loads.
7. Bootstrap or increase sample count to estimate finite-sample floor.
8. Aggregate results and write figures/tables.

outputs:
`summary.md`, `detailed.md`, condition tables, residual geometry figures.

debug artifacts:
state, whitening, isotropic, strata, and bootstrap audits.

pass conditions:
The primary metric exists for every condition and at least one named residual source is separated.

fail conditions:
No named source explains residual load, or residual load is finite-sample floor.

failure reasons:
Wrong hidden extraction, invalid whitening, unmatched isotropic controls, sparse strata, missing sample-count guard.

## 11. Success / Failure / Insufficient Evidence

Support residual anisotropy:
Whitening reduces \(L\) and the covariance spectrum is non-isotropic.

Support router-direction cell geometry:
Matched isotropic residuals produce lower \(L\) than real residuals under the same router rows.

Support context / position:
Conditional loads show systematic shifts beyond noise.

Support finite-sample explanation:
Bootstrap / larger sample drives \(L\) near zero.

Insufficient evidence:
Any validity audit fails or the controls conflict without a clear boundary.

## 12. What This Cannot Claim

This protocol cannot claim:

- training collapse is explained;
- feature-level specialization is achieved;
- real-text routing behaves the same way;
- residual control is a deployable router method;
- load balance alone proves specialization.

## 13. Review Notes And Protocol Changes

2026-06-21:
The protocol was approved by the user's explicit active objective requiring the three anchors to be executed sequentially with full runs and closure. No scientific question, primary metric, or condition set was changed at approval time.

Open for user review:

- Confirm whether the first run should use only `post_ln` or both A06_01_01_E05 readouts.
- Confirm whether to include `num_layers=1,2,4` or focus on the primary readout first.
- Confirm how to define local context / background-token factors without creating too many sparse strata.
- Confirm whether A06_01_01_E06 must be completed before A06_01_02_E01 is approved.

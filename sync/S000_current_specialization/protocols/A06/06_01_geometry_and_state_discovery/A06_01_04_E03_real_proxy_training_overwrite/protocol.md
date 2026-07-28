# Protocol: A06_01_04_E03 Real-DCLM Proxy-Init Training Preservation

## 0. Approval Snapshot

Approval status: A06_01_04_E02 supported with boundary; pre-approved by explicit user goal after dependency passes.
Purpose: decide whether proxy-center initialization survives early DCLM top-1 training.
Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/subanchors/06_01_04_real_proxy_initialization_overwrite_anchor.md`
Anchor decision question: does real-DCLM proxy-center initialization preserve proxy routing through early training?
Anchor physical prior tested: good initialization may define a basin, but DCLM hidden drift may override it.
Anchor core model term tested: $NMI(q_i,a_i(t))$, $L_t$, and common-margin trajectory.
Anchor falsifier: high step-0 proxy_route_NMI collapses by step 10/50 while LM loss is acceptable.
Experiment role: training-dynamics diagnostic.
Primary metric from anchor: proxy_route_NMI at step 10 and 50.
Claim boundary from anchor: early small-model DCLM training only.
Minimal setup: DCLM top-1 MoE, checkpoints 0--300, random vs proxy-center init.
Basic configuration: train conditions under same schedule; audit exact router inputs and proxy assignments.
Conditions to run: random, equal-norm random, raw-center proxy init, residual-center proxy init as common-bias comparison, label-shuffled proxy guard if budget allows.
Pass: proxy init preserves proxy_route_NMI and does not worsen LM loss or common/load spike.
Fail: proxy routing collapses or worsens step-10 common/load concentration.
Insufficient: A06_01_04_E02 failed, no exact gate audit, no LM loss guard, or missing checkpoints.
Cannot claim: long-run pretraining, semantic specialization, or expert utility.
Approval decision: execute only after A06_01_04_E02 passes.

## 1. Anchor Alignment

This protocol tests training preservation, the real-data counterpart of A06_02_01_E01.

## 2. Tested Hypothesis

H1: raw-center proxy init preserves proxy_route_NMI through early training.
H2: proxy-center init reduces common/load amplification relative to random.
H3: preservation does not harm LM loss.

## 3. Rival Explanations

Accuracy-only success, load-only success, early common collapse, and proxy-init overfitting.

## 4. Data / Model / Algorithm / Objective

Data/model match A06_01_01 DCLM setup. Objective is standard next-token LM loss. Router initialization differs by condition. Metrics are audited on fixed DCLM splits with A06_01_04_E01 proxy labels.

## 5. Conditions, Seeds, And Checkpoints

Seeds: `0,1,2`; checkpoints: `0,1,2,3,5,10,20,50,100,300`; layers: 3--5 primary. Main initialization uses step-0 raw-center equal-norm rows because A06_01_04_E02 found this is the strongest actual raw-input bridge. Residual-center equal-norm is included as a common-bias comparison.

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| random | baseline | ordinary top-1 | floor | trajectory | worse | same/better | missing | figure |
| equal-norm random | row-norm guard | A06_01_01_E04 | guard | trajectory | worse | same/better | missing | table |
| raw-center proxy init | main | basin preservation | main | NMI/loss | preserved | collapse | no dep | figure |
| residual-center proxy init | common-bias comparison | residual bridge | tests A06_01_04_E02 boundary | NMI/loss/common | preserved | raw collapse | no dep | figure |
| label-shuffled guard | false proxy | leakage/artifact | guard | NMI/loss | low | high | missing | table |

## 6. Primary Metric

proxy_route_NMI at steps 10 and 50. It decides because A06_01_01 localized early DCLM route concentration to this window.

## 7. Secondary Metrics

LM loss, raw/centered load, active experts, common/residual margin, replay decomposition, route-change rate.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: A06_02_01_E01 synthetic preservation.
Known bad: random DCLM early route concentration from A06_01_01.
Known confusing: LM loss success with proxy_route_NMI collapse.

## 9. Stage-Level Profiling Plan

Dependency audit, training integrity audit, checkpoint completeness, exact gate-input audit, proxy trajectory, common/load replay.

## 10. Algorithm Specification, If Nontrivial

input: A06_01_04_E01 proxy labels, A06_01_04_E02 raw-center/residual-center init rows, DCLM train/eval stream.
parameters: 300 steps, checkpoints listed above, same optimizer as A06_01_01.
steps: initialize model/router; train; save checkpoints; collect exact gate inputs; compute proxy routing; replay common/residual margins.
outputs: trajectory tables, replay tables, figures.
failure reasons: dependency fail, training divergence, proxy collapse, common amplification, loss degradation.

## 11. Success / Failure / Insufficient Evidence

Support: proxy_route_NMI remains high through step 10/50, LM loss acceptable, common/load no worse than random.
Weaken: collapse, loss penalty, or worse common/load spike.
Insufficient: missing dependency, checkpoint, or exact gate audit.

## 12. What This Cannot Claim

No semantic feature claim, no expert utility claim, no long-run scaling claim.

## 13. Review Notes And Protocol Changes

2026-06-22: conditional protocol created as real-data training counterpart to A06_02_01_E01.
2026-06-22: updated after A06_01_04_E02 full01. Main condition is raw-center equal-norm; residual-center equal-norm is a common-bias comparison, not the main method.

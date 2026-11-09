# Protocol: A06_01_03_E01 Label-Free Common / Residual-Control Router

## 0. Approval Snapshot

Approval status:
Approved for a step-0 hidden-state replay gate by the user's active sequential-anchor objective on 2026-06-21. The previous blocking dependency is resolved: A06_01_01_E06 supports residual covariance / structured residual geometry, and A06_01_02_E01 proves oracle feature-centroid reachability.

Purpose:
Test whether a label-free router-side common / residual-control intervention can move random-init routing toward the A06_01_02_E01 oracle-reachable feature partition at step 0.

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Anchor decision question:
Can a label-free router-side common / residual-control intervention move random-init dot-product sparse top-1 MoE toward feature-level specialization while preserving accuracy?

Anchor physical prior tested:
The router should not make top-1 decisions from feature-independent common components; experts can receive full hidden states while router scores use common-controlled inputs.

Anchor core model term tested:
Raw score \(z_e=w_e^\top h\) versus controlled score \(z'_e=w_e^\top \phi(h)\), where \(\phi(h)\) is label-free common-centering, projection, or residual-path router input.

Anchor falsifier:
If label-free controls improve load but not feature_NMI, or improve NMI only through label / oracle leakage, then they are not valid label-free specialization methods.

Experiment role:
Method construction candidate, gated by prior mechanism and oracle positive-control results.

Primary metric from anchor:
feature_NMI / slot_NMI with accuracy constraint.

Claim boundary from anchor:
Minimal synthetic setting only. No real LM transfer, no final deployable router, no expert utility claim.

Minimal setup:
Use the same A06_01_01_E05/A06_01_01_E06/A06_01_02_E01 initialized synthetic hidden-state replay surface. Experts are not trained in this gate; the audit is router-input-only and step-0. Accuracy preservation is parked for a follow-up only if a label-free control improves NMI at step 0.

Basic configuration:
Baseline raw router, equal-norm guard, label-free calibration/batch common-centering, projection / whitening residual controls, and the A06_01_02_E01 oracle feature-centroid upper bound for gap measurement.

Conditions to run:
`baseline_raw_router`, `equal_norm_router_rows`, `heldout_batch_mean_router`, `calibration_mean_router`, `projection_top1_router`, `whitened_residual_router`, and `oracle_feature_centroid_upper`.

Pass:
At least one label-free control improves held-out feature_NMI by at least `+0.25` absolute over baseline, reaches at least `50%` of the oracle gap, does not merely improve load, and avoids many-to-one feature merge.

Fail:
Controls improve load only, leak labels, or fail to improve feature_NMI while the oracle upper bound succeeds.

Insufficient:
Feature labels leak into a label-free condition, expert input changes along with router input, or only load balance is reported.

Cannot claim:
Real LM transfer, final deployability, expert causal utility, or that initialization alone solves final collapse.

Approval decision:
Approved for step-0 replay. Training / accuracy preservation remains out of scope unless this gate finds a viable label-free NMI improvement.

## 1. Anchor Alignment

Decision question:
Can label-free common / residual router controls improve feature-level routing from random initialization?

Physical prior tested:
Common-logit bias is a removable router-side nuisance term, and router input can be controlled without removing task information from expert input.

Core model term tested:
\(z'_e=w_e^\top \phi(h)\) for label-free \(\phi\).

Falsifier:
Load improves without NMI, accuracy drops, label leakage occurs, or label-free variants fail despite oracle success.

Claim boundary:
Minimal synthetic method candidate only.

## 2. Tested Hypotheses

H1:
Batch or EMA common-centering improves feature_NMI and reduces common margin while preserving accuracy.

H2:
Residual-path router input improves feature_NMI and slot margin while preserving expert computation.

H3:
Projection-based common removal is seed-unstable or removes feature signal unless constrained.

H4:
Anti-lockin training control may still be needed if early NMI improves but final routing reconcentrates.

## 3. Rival Explanations

R1:
The intervention only improves load, not specialization.

Separated by:
Primary feature_NMI / purity and many-to-one merge metrics.

R2:
The intervention uses hidden labels.

Separated by:
Label-leakage audit for every variant.

R3:
Accuracy is preserved only because expert input changed or task information was removed.

Separated by:
Router-input-only intervention audit; experts receive full hidden state by default.

R4:
The method only delays top-1 lock-in.

Separated by:
Early-window vs full-training control and route-lock step.

## 4. Data / Model / Algorithm / Objective

Data:
Minimal synthetic uniform feature setting with fixed feature identity definition.

Model:
Sparse top-1 dot-product MoE. Experts receive full hidden states unless a condition explicitly says otherwise.

Algorithm:
Modify router scoring input through label-free common or residual control.

Objective:
Train or replay only according to the approved minimal setting. The first read should separate step-0 routing from early training if both are included.

## 5. Conditions, Seeds, And Checkpoints

Dependency gate:
A06_01_01_E06 and A06_01_02_E01 are closed. This run must include a dependency audit row pointing to those results.

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `baseline_raw_router` | baseline | raw \(w^\top h\) | defines random-init behavior | primary | baseline exists | missing | wrong setup | `tables/results.csv` |
| `equal_norm_router_rows` | guard | row-norm effect | protects against A06_01_01_E04 confound | secondary | no main NMI effect | dominates result | changes method claim | `tables/results.csv` |
| `heldout_batch_mean_router` | H1 | batch common estimate | strongest label-free batch common control | primary | NMI up | load only improves | uses labels | `figures/nmi_load_by_condition.png` |
| `calibration_mean_router` | H1 | held-out-free calibration common estimate | tests deployable common estimate | primary | NMI up | load only improves | uses labels | `tables/results.csv` |
| `projection_top1_router` | H3 | top-PC removal | tests projection control | secondary | stable NMI | removes feature signal | no projection audit | `tables/projection_audit.csv` |
| `whitened_residual_router` | A06_01_01_E06 boundary | covariance control | tests label-free residual covariance control with random rows | primary | NMI up and load not only | load-only effect | invalid whitening | `tables/whitening_audit.csv` |
| `oracle_feature_centroid_upper` | A06_01_02_E01 upper bound | oracle feature centroids | bounds label-free controls | primary | oracle succeeds | oracle fails | leaks into label-free | `tables/oracle_gap.csv` |

## 6. Primary Metric

Primary metric:
feature_NMI / slot_NMI with accuracy constraint.

Why it decides:
The method should move routing toward feature-level specialization. Load balance alone is not enough because a balanced router can still ignore the intended feature.

Accuracy constraint:
Not measured in this step-0 replay gate. This run can only decide whether a label-free router-input control is worth training. Accuracy preservation is required in a later training/basin protocol if this gate passes.

## 7. Secondary Metrics

- max load;
- active experts;
- per-feature route purity;
- common margin;
- slot margin;
- many-to-one merge count;
- route-lock step;
- final route heatmap;
- oracle gap.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good:
Oracle common-cancel / slot-init upper bounds can improve NMI in prior evidence.

Known bad:
Reporting load balance as specialization.

Known confusing:
Projection can remove task-relevant feature signal together with common directions.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| dependency audit | Are A06_01_01_E06/A06_01_02_E01 resolved or bypassed? | anchor/protocol status | dependency clear | `tables/dependency_audit.csv` | detailed |
| label-free audit | Does any variant use labels? | implementation flags | no labels in label-free variants | `tables/label_leakage_audit.csv` | detailed |
| router/expert split | Did only router input change? | model audit | expert input full hidden | `tables/input_path_audit.csv` | detailed |
| step-0 read | Does NMI improve before training? | NMI/load/margin | NMI up with accuracy intact | `tables/step0_results.csv` | summary |
| early training | Does routing remain stable? | trajectory | no reconcentration | `tables/trajectory.csv` | summary |
| oracle gap | How close are label-free controls to upper bound? | condition table | small gap | `tables/oracle_gap.csv` | summary |

## 10. Algorithm Specification

input:
Synthetic feature batches, model, router hidden states, label-free common estimates, optional oracle common for upper bound.

parameters:
common-estimate mode, early-window length, EMA decay, projection rank, residual-path definition, accuracy tolerance.

intermediate variables:
\(h_i\), \(\hat c\), \(\phi(h_i)\), scores, assignments, NMI, load, margins, accuracy.

steps:
1. Run baseline raw router.
2. Run oracle common-cancel upper bound.
3. Run each label-free common / residual-control variant.
4. Audit label leakage and router/expert input separation.
5. Compute NMI, load, margin, accuracy, and route heatmaps.
6. If training is included, track early-window and full-training trajectories.

outputs:
`summary.md`, `detailed.md`, condition tables, route heatmaps, NMI/load figures.

debug artifacts:
dependency, label-leakage, input-path, projection, and oracle-gap audits.

pass conditions:
At least one label-free variant improves feature_NMI by `+0.25` over baseline and closes at least `50%` of the oracle gap without label leakage or load-only failure.

fail conditions:
No label-free variant improves NMI, or improvements depend on labels, load-only effects, or accuracy loss.

failure reasons:
Common estimate poor, residual control removes feature signal, top-1 lock-in persists, or oracle target itself fails.

## 11. Success / Failure / Insufficient Evidence

Support method candidate:
Label-free variant improves held-out feature_NMI, does not rely on labels, and closes a substantial oracle gap at step 0.

Weaken method candidate:
Only oracle works, or label-free variants improve load without NMI.

Insufficient evidence:
Label leakage, changed expert input, missing accuracy, missing oracle upper bound, or unresolved dependency gate.

## 12. What This Cannot Claim

This protocol cannot claim:

- real LM transfer;
- trained expert utility;
- final deployability;
- full collapse solution;
- load balance equals specialization.

## 13. Review Notes And Protocol Changes

2026-06-21:
A06_01_01_E06 and A06_01_02_E01 are closed, so the dependency gate is resolved. The approved first run is a step-0 replay gate on the A06 synthetic hidden-state surface:

- feature label is the four uniform `(slot,target)` `pair_id`;
- no labels may be used in label-free controls;
- A06_01_02_E01 oracle feature-centroid construction is included only as a non-label-free upper bound;
- accuracy / training is parked unless step-0 label-free NMI improves;
- pass requires absolute NMI improvement of at least `+0.25` over baseline and at least `50%` oracle-gap closure.

# Protocol: A06_01_02_E01 Feature-Level Initialization Positive Control

## 0. Approval Snapshot

Approval status:
Approved for implementation and full run by the user's active sequential-anchor objective on 2026-06-21. A06_01_01_E06 dependency is satisfied and shows residual covariance / structured residual geometry remains active after common-centering.

Purpose:
Test whether feature-level routing specialization is reachable at initialization under oracle residual-geometry centers in the synthetic setting.

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Anchor decision question:
Given uniform discrete features and initialized hidden states, can an oracle feature-centroid / residual-geometry initialization produce feature-level top-1 routing specialization at step 0 while keeping load balanced?

Anchor physical prior tested:
If feature information is present in common-controlled residual hidden geometry, expert centers aligned with feature residual centroids should route each feature consistently to a distinct expert.

Anchor core model term tested:
Oracle residual feature centroid \(r_f=\mu_f-c\) and equal-norm expert centers aligned with those residual centroids.

Anchor falsifier:
If oracle residual-centroid centers do not produce high feature_NMI with acceptable load and margin, initialization-only feature-level specialization is not reachable under the tested hidden geometry.

Experiment role:
Operationalization / positive-control reachability test. This is not a label-free method.

Primary metric from anchor:
feature_NMI / slot_NMI, read with load imbalance \(L\) and routing margin.

Claim boundary from anchor:
Synthetic oracle positive control only. No label-free method, no real text, no expert utility, no final router design.

Minimal setup:
Use the same uniform synthetic feature setting and extracted initialized hidden states. Use feature labels only for oracle construction and evaluation.

Basic configuration:
4 uniform `(slot,target)` pair features (`pair_id`), 4 experts, one expert per feature, held-out centroid construction / evaluation split, equal-norm centers unless norm is explicitly tested.

Conditions to run:
`random_gaussian_init`, `equal_norm_random_direction`, `raw_feature_centroid_init`, `common_centered_feature_centroid_init`, and `common_centered_whitened_feature_centroid_init` as the A06_01_01_E06-informed residual-geometry guard. `residual_spherical_code_init` is parked unless the centroid geometry is degenerate.

Pass:
Oracle residual-centroid initialization gives `feature_NMI >= 0.95`, load imbalance `L <= 0.05`, and positive held-out margin at step 0. Whitened residual-centroid initialization is allowed to define the stronger oracle upper bound if it improves margins without hurting NMI / load.

Fail:
Oracle residual-centroid initialization still merges features, has severe load imbalance, or has near-zero margin.

Insufficient:
No train/eval split for centroid construction, feature distribution not uniform, only load is reported, or labels leak into a claimed label-free condition.

Cannot claim:
A label-free initialization method, training stability beyond tested checks, expert causal specialization, real-text transfer, or final MoE solution.

Approval decision:
Approved. Execute after A06_01_01_E06 closure and before A06_01_03_E01 label-free method construction.

## 1. Anchor Alignment

Decision question:
Can oracle feature-residual centers make feature-level routing reachable at initialization?

Physical prior tested:
Feature information is present in residual hidden geometry after common control.

Core model term tested:
Residual feature centroid \(r_f=\mu_f-c\) and equal-norm expert center \(w_{\pi(f)}=\alpha r_f/\|r_f\|\).

Falsifier:
Oracle centers fail to produce high feature_NMI, balanced load, and positive margin.

Claim boundary:
Positive control only.

## 2. Tested Hypotheses

H1:
Oracle residual-centroid initialization can produce feature-level specialization.

H2:
Common-centered feature centroids outperform raw feature centroids.

H3:
Equal-norm centers improve load without destroying feature_NMI or margin.

H4:
Optional short training preserves the positive-control basin only if step-0 margin is adequate.

## 3. Rival Explanations

R1:
High NMI is only label leakage from using evaluation examples to build centroids.

Separated by:
Calibration / evaluation split for centroid construction.

R2:
Good load is not real specialization.

Separated by:
Read feature_NMI, per-feature purity, and margin, not load alone.

R3:
Raw common component, not residual feature geometry, drives apparent success.

Separated by:
Raw-centroid vs residual-centroid comparison.

R4:
Positive control is fragile and not a basin.

Separated by:
Optional short-training check only after step-0 result is valid.

## 4. Data / Model / Algorithm / Objective

Data:
Same synthetic uniform feature / slot setting as A06_01_01_E05 and A06_01_01_E06.

Model:
Initialized dot-product top-1 synthetic MoE. Step-0 replay is primary.

Algorithm:
Construct oracle router centers from feature labels / centroids, then replay routing on held-out hidden states.

Objective:
No optimization for the primary test. Optional short training is a secondary basin check.

## 5. Conditions, Seeds, And Checkpoints

Seeds:
Use A06_01_01_E05 seeds unless the approved protocol narrows the first run.

Checkpoints:
Initialization / step 0. Optional short training checkpoints only after step-0 positive control is read.

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `random_gaussian_init` | baseline | ordinary random router | defines failure baseline | primary | baseline exists | missing | wrong setup | `tables/results.csv` |
| `equal_norm_random_direction` | norm guard | row norm | protects against norm confound | secondary | load guard exists | no guard | directions changed incorrectly | `tables/results.csv` |
| `raw_feature_centroid_init` | H2 | raw centroid \(\mu_f\) | tests common contamination | primary | weaker than residual if common matters | matches residual | label leakage | `figures/route_heatmap_by_condition.png` |
| `common_centered_feature_centroid_init` | H1 | residual centroid \(r_f\) | tests reachability | primary | high NMI, balanced load, positive margin | feature merge / low margin | no held-out eval | `figures/route_heatmap_by_condition.png` |
| `common_centered_whitened_feature_centroid_init` | H1 / A06_01_01_E06 boundary | whitened residual centroid | tests whether A06_01_01_E06 covariance control improves oracle reachability | secondary | high NMI, balanced load, stronger margin | destroys NMI or load | invalid whitening | `tables/margin_by_condition.csv` |
| `residual_spherical_code_init` | H3 | balanced residual centers | parked unless centroid geometry is degenerate | secondary | balanced and high margin | destroys NMI | geometry not clean | parked |
| short training check | H4 | basin stability | parked for follow-up after step-0 closure | secondary | NMI preserved with accuracy | collapses | changes too many variables | parked |

## 6. Primary Metric

Primary metric:
feature_NMI / slot_NMI.

Why it decides:
The question is feature-level routing specialization, not only balanced load. NMI measures whether feature identity predicts expert assignment.

Required co-metrics:
Load imbalance \(L\) and routing margin must be read with NMI. High NMI with collapsed load or tiny margin is not sufficient.

Pass thresholds for this approved run:

- `feature_NMI >= 0.95`;
- `L <= 0.05`;
- `margin_p05 > 0`;
- centroid construction and evaluation are separated within every seed / depth / readout.

## 7. Secondary Metrics

- per-feature route purity;
- load imbalance \(L\);
- max load;
- routing margin by feature;
- route heatmap;
- target accuracy if training is run;
- agreement with oracle assignment.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good:
Prior slot-init positive controls suggest feature signal may be present.

Known bad:
Calling oracle centroid construction label-free.

Known confusing:
High load balance without feature_NMI is not specialization.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| feature split | Are centroid-construction and evaluation samples separated? | split manifest | no eval leakage | `tables/split_audit.csv` | detailed |
| centroid audit | Are raw and residual centroids well-defined? | centroid norms / cosines | no degenerate centroids | `tables/centroid_audit.csv` | detailed |
| step-0 replay | Does oracle init route features cleanly? | NMI / heatmap | high NMI and balanced load | `tables/results.csv` | summary |
| margin audit | Is routing robust enough to be meaningful? | margin distribution | positive margin | `tables/margin_by_condition.csv` | summary |
| optional basin check | Does short training preserve routing? | NMI trajectory | no immediate collapse | `tables/trajectory.csv` | detailed |

## 10. Algorithm Specification

input:
Initialized hidden states, feature labels, train/eval split, router rows or constructed centers.

parameters:
number of features, number of experts, center norm \(\alpha\), centroid construction mode.

intermediate variables:
\(\mu_f\), \(c\), \(r_f\), normalized centers, scores, assignments, NMI, \(L\), margins.

steps:
1. Extract or reproduce hidden states.
2. Split samples into centroid-construction and evaluation sets.
3. Compute raw and residual feature centroids.
4. Construct equal-norm oracle centers.
5. Replay top-1 routing on held-out hidden states.
6. Compute NMI, load, margin, and route heatmaps.
7. Optionally run a short-training basin check after step-0 approval.

outputs:
`summary.md`, `detailed.md`, route heatmaps, margin tables.

debug artifacts:
split, centroid, replay, margin, and optional trajectory audits.

pass conditions:
Residual-centroid oracle reaches high NMI, balanced load, and positive margin.

fail conditions:
Oracle centers merge features, collapse load, or have near-zero margin.

failure reasons:
No feature separability, common contamination, label leakage, insufficient margin, or task setup mismatch.

## 11. Success / Failure / Insufficient Evidence

Support reachability:
`feature_NMI >= 0.95`, `L <= 0.05`, and `margin_p05 > 0` under residual-centroid oracle centers on held-out evaluation samples.

Weaken reachability:
Oracle residual centers fail despite valid data and split audits.

Insufficient evidence:
No held-out evaluation, no margin, feature distribution not uniform, or only load is reported.

## 12. What This Cannot Claim

This protocol cannot claim:

- label-free initialization;
- real-text transfer;
- expert utility;
- final training stability;
- deployable router design.

## 13. Review Notes And Protocol Changes

2026-06-21:
A06_01_01_E06 closed before this run and supports residual covariance / structured residual geometry as the main post-common residual source. The A06_01_02_E01 protocol is therefore approved with these changes:

- feature identity is fixed to the four uniform `(slot,target)` pair ids;
- the first run is step-0 reachability only, with short training parked;
- pass thresholds are fixed at `feature_NMI >= 0.95`, `L <= 0.05`, and `margin_p05 > 0`;
- `common_centered_whitened_feature_centroid_init` is added as an A06_01_01_E06-informed oracle guard.

# Protocol: A06_01_03_E02 Label-Free Feature Discovery Initialization

## 0. Approval Snapshot

Approval status: Approved by user and executed on 2026-06-22.
Purpose: decide whether label-free route-position clustering can recover pseudo-feature centers at step 0.
Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`
Anchor decision question: can clustering without `pair_id` improve held-out feature_NMI over A06_01_03_E01 controls and toward A06_01_02_E01 oracle?
Anchor physical prior tested: feature structure may require multi-center discovery, not one global common/projection/whitening control.
Anchor core model term tested: \(r_i=h_i-c_{\text{calib}}\), centers \(\nu_k\), rows \(w_e=\alpha\nu_e/\|\nu_e\|\).
Anchor falsifier: load improves but NMI does not; labels leak; clusters are nuisance-aligned.
Experiment role: operationalization / proxy test.
Primary metric from anchor: held-out `feature_NMI`.
Claim boundary from anchor: step-0 synthetic hidden-state replay only.
Minimal setup: A06 replay surface with `slot_token_len=4`; four uniform pair features; four experts; calibration/evaluation split; no training.
Basic configuration: repeated `SLOT_s` span of length 4, route position at the last slot token (`pair_start + 3`); fit centers on calibration route-position states only; `pair_id` is evaluation-only.
Conditions to run: `baseline_raw_router`, `equal_norm_router_rows`, `calibration_mean_router`, clustering methods `route_kmeans_residual_K4` / `route_spherical_kmeans_residual_K4`, graph method `route_spectral_residual_K4`, sparse-atom method `route_dictionary_residual_K4`, `oracle_feature_centroid_upper`; optional all-hidden guard.
Pass: one label-free route-position method has `NMI_delta_vs_baseline >= 0.25` and `oracle_gap_fraction >= 0.50`, without leakage or many-to-one merge.
Fail: load-only improvement, baseline-like NMI, nuisance alignment, or label leakage.
Insufficient: missing held-out split, oracle, leakage audit, or feature_NMI.
Cannot claim: training stability, real DCLM transfer, expert utility, semantic specialization, final router method.
Approval decision: executed; see `summary.md` and `detailed.md`.

## 1. Anchor Alignment

The protocol directly tests the anchor model \(h_i=c+r_i\): learn centers from calibration residuals, initialize equal-norm router rows, and judge held-out feature_NMI. The claim boundary is step-0 synthetic replay.

## 2. Tested Hypothesis

H1: route-position residual discovery recovers pseudo-feature centers. Supported if clustering, spectral clustering, or dictionary learning passes the NMI/oracle-gap gate; weakened if they only improve load or merge features.

## 3. Rival Explanations

- Load-only effect: check feature_NMI and route heatmap.
- Label leakage: check leakage audit.
- Nuisance clustering: check position/context NMI guard.
- Oracle unavailable: run oracle upper bound on the same split.

## 4. Data / Model / Algorithm / Objective

Data: A06 synthetic hidden-state replay with `slot_token_len=4`, balanced by pair. Each example contains a repeated four-token `SLOT_s` span followed immediately by `TARGET_s`; background tokens are independent of pair id. Model: initialized Transformer-MoE replay, four experts, no training. Algorithm: fit clustering / spectral / dictionary centers on calibration residuals at the last slot position and route held-out states. Objective: routing replay only.

## 5. Conditions, Seeds, And Checkpoints

Full run: `slot_token_len=4`; seeds `20260521..20260528`; depths `{1,2,4}`; readouts `{post_ln, pre_ln_replay}`; 4096 samples per pair split 50/50.

| Item | Why needed | Evidence |
| --- | --- | --- |
| `baseline_raw_router` | random floor | `tables/discovery_summary.csv` |
| `equal_norm_router_rows` | row-norm guard | `tables/discovery_summary.csv` |
| `calibration_mean_router` | A06_01_03_E01 load-only baseline | `tables/discovery_summary.csv` |
| `route_kmeans_residual_K4` | Euclidean center test | `figures/nmi_by_method.png` |
| `route_spherical_kmeans_residual_K4` | primary angular center test | `figures/nmi_by_method.png` |
| `route_spectral_residual_K4` | graph-structure center test | `figures/nmi_by_method.png` |
| `route_dictionary_residual_K4` | sparse-atom direction test | `figures/nmi_by_method.png` |
| `oracle_feature_centroid_upper` | oracle gap | `tables/oracle_gap.csv` |
| optional all-hidden guard | nuisance scope check | `tables/nuisance_guard.csv` |

## 6. Primary Metric

Held-out `feature_NMI = NMI(pair_id, routed_expert)`. It decides because A06_01_03_E01 showed load can improve while feature routing fails. Pass threshold: `NMI_delta_vs_baseline >= 0.25` and `oracle_gap_fraction >= 0.50`.

## 7. Secondary Metrics

Load \(L\), max load, margin p05, feature purity, many-to-one merge count, oracle-gap fraction, cluster occupancy, nuisance NMI, route heatmap.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: oracle centroid high NMI and \(L=0\). Known bad: A06_01_03_E01 calibration mean improves load but should fail NMI. Known confusing: all-hidden clusters may be nuisance clusters.

## 9. Stage-Level Profiling Plan

| Stage | Rule | Artifact |
| --- | --- | --- |
| split audit | balanced held-out split required | `tables/split_audit.csv` |
| leakage audit | no labels in discovery | `tables/leakage_audit.csv` |
| discovery audit | no empty center | `tables/cluster_audit.csv` |
| held-out routing | apply NMI gate | `tables/discovery_summary.csv` |
| oracle gap | oracle succeeds | `tables/oracle_gap.csv` |

## 10. Algorithm Specification, If Nontrivial

Input: calibration/eval hidden states at the last slot position for `slot_token_len=4`. Parameters: `K=4`, norm scale \(\alpha\), clustering seed. Steps: compute \(c_{\text{calib}}\) and residuals; fit k-means / spherical k-means without labels; convert centers to rows; evaluate held-out NMI/load/margin and audits. Outputs: `summary.md`, `detailed.md`, tables and figures. Failure reasons: no recoverable centers, nuisance geometry, label leakage, implementation mismatch.

## 11. Success / Failure / Insufficient Evidence

Support: one route-position label-free method family passes. Partial support: NMI improves but misses oracle-gap threshold. Weaken: all families are load-only or baseline-like. Insufficient: missing held-out split, oracle, leakage audit, or NMI.

## 12. What This Cannot Claim

No claim about training, real text, expert utility, semantic specialization, final router design, or all label-free methods.

## 13. Review Notes And Protocol Changes

2026-06-22: compressed to the minimal A06_01_03_E02 gate, step-0 route-position center discovery.
2026-06-22: main run fixed to `slot_token_len=4` after slot-length robustness showed the A06_01_01_E05-A06_01_03_E01 boundary is stable for repeated slots.
2026-06-22: full run includes clustering, spectral clustering, and dictionary-learning discovery families.

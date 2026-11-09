# Detailed: A06_01_03_E01 Label-Free Common / Residual-Control Router

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol:
`protocol.md`

Summary:
`summary.md`

## 0. Quick Recap

Purpose:
Test whether label-free common / residual router-input controls can recover the A06_01_02_E01 oracle-reachable feature partition from random router rows.

Conclusion:
No. The tested controls improve load but do not improve feature_NMI enough to pass the step-0 gate.

Evidence:
0 of 336 label-free condition cells pass. Full-sweep mean NMI moves only from `0.2302` baseline to `0.2353` under calibration mean centering and `0.2350` under held-out batch mean centering, while oracle feature-centroid upper bound reaches `1.0`.

## 1. Protocol Compliance Audit

approved conditions match actual conditions:
Yes. The run includes baseline, equal-norm, batch mean, calibration mean, projection, whitening, and oracle upper-bound conditions.

primary metric exists:
Yes. `feature_NMI` and oracle-gap fraction are in `tables/aggregate_by_condition.csv`.

central figures/tables exist:
Yes. Curated tables and figures are copied into this experiment directory.

seeds/checkpoints recorded:
Yes. Eight seeds, depths 1/2/4, readouts `post_ln` and `pre_ln_replay`. Step 0 only.

label-free audit:
Yes. Label-free controls do not use `pair_id` labels for control. The oracle upper bound is explicitly marked non-label-free.

success/failure criteria applied:
Yes. No label-free row reaches `+0.25` NMI improvement or `50%` oracle-gap closure.

## 2. Setup

Data:
Four uniform `(slot,target)` pair features. Feature label is `pair_id` for metrics only.

Model:
Initialized Transformer-MoE replay surface reused from A06_01_01_E05/A06_01_01_E06/A06_01_02_E01. Four random router rows. No training.

Split:
Calibration / evaluation split is balanced by pair id.

Run command:

```bash
python scripts/run_a06_07_label_free_common_residual_control_router.py \
  --config configs/a06_07_label_free_common_residual_control_router.json \
  --run-name a06_07_full_20260621_1 \
  --run-stage full \
  --device cuda
```

## 3. Conditions

`baseline_raw_router`:
Raw random router score \(w_e^\top h\).

`equal_norm_router_rows`:
Normalize random router row norms.

`heldout_batch_mean_router`:
Subtract the held-out batch mean from routed hidden states. This is a strong transductive label-free common estimate.

`calibration_mean_router`:
Subtract a calibration-set mean, then evaluate on held-out samples.

`projection_top1_router`:
Subtract calibration mean and remove the top principal component.

`whitened_residual_router`:
Subtract calibration mean, whiten residual covariance, and score with the same random router rows.

`oracle_feature_centroid_upper`:
Non-label-free A06_01_02_E01 oracle upper bound.

## 4. Primary Evidence

Full-sweep means:

| Condition | Feature NMI | NMI delta | Oracle gap fraction | Load \(L\) |
| --- | ---: | ---: | ---: | ---: |
| baseline raw | 0.2302 | 0.0000 | 0.0000 | 0.6867 |
| equal-norm rows | 0.2298 | -0.0004 | -0.0003 | 0.6834 |
| calibration mean | 0.2353 | 0.0051 | 0.0053 | 0.2837 |
| held-out batch mean | 0.2350 | 0.0048 | 0.0048 | 0.2828 |
| projection top-1 | 0.1628 | -0.0674 | -0.0937 | 0.2881 |
| whitened residual | 0.0150 | -0.2152 | -0.2949 | 0.0860 |
| oracle feature centroid | 1.0000 | 0.7698 | 1.0000 | 0.0000 |

Primary readout (`num_layers=1`, `post_ln`):

| Condition | Feature NMI | NMI delta | Oracle gap fraction | Load \(L\) |
| --- | ---: | ---: | ---: | ---: |
| baseline raw | 0.1978 | 0.0000 | 0.0000 | 0.5610 |
| calibration mean | 0.2100 | 0.0122 | 0.0136 | 0.2640 |
| held-out batch mean | 0.2090 | 0.0112 | 0.0123 | 0.2576 |
| projection top-1 | 0.1321 | -0.0657 | -0.0875 | 0.2873 |
| whitened residual | 0.0120 | -0.1857 | -0.2528 | 0.1103 |
| oracle feature centroid | 1.0000 | 0.8022 | 1.0000 | 0.0000 |

Interpretation:
Common-centering controls the A06_01_01_E05/A06_01_01_E06 load mechanism but does not discover the A06_01_02_E01 feature partition. Whitening overcontrols covariance and removes feature-discriminative structure for random rows.

## 5. Visualization Results

### NMI By Condition

![NMI by condition](figures/nmi_by_condition.png)

Purpose:
Check whether label-free controls improve feature routing.

Observed result:
Label-free conditions remain near baseline or below it; oracle reaches 1.0.

Take-home:
The tested label-free controls fail the specialization gate.

### Load Versus Oracle Gap

![Load and oracle gap](figures/load_oracle_gap_by_condition.png)

Purpose:
Separate load balance from feature specialization.

Observed result:
Load improves strongly under common-centering and whitening, but oracle-gap fraction remains near zero or negative.

Take-home:
Load balance is not specialization.

### Route Heatmap

![Route heatmap](figures/route_heatmap_by_condition.png)

Purpose:
Inspect whether routes form one-feature-one-expert maps.

Observed result:
Oracle is one-hot. Label-free controls are mixed or many-to-one.

Take-home:
The negative result is structural.

## 6. Failure Interpretation

Observation:
Mean centering reduces load from `0.6867` to about `0.283`, but NMI changes by only about `+0.005`.

Interpretation:
Global common-control removes a nuisance load term but does not create feature-aligned router directions.

Observation:
Whitening gives the lowest label-free load (`0.0860`) but NMI collapses to `0.0150`.

Interpretation:
Covariance control can erase or scramble feature-relevant structure when router rows remain random.

Observation:
Oracle feature centroids still reach NMI `1.0`.

Interpretation:
The target remains reachable; the failure is specifically the tested label-free controls.

## 7. Artifact Map

Code workspace:
`Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/`

Runner:
`scripts/run_a06_07_label_free_common_residual_control_router.py`

Config:
`configs/a06_07_label_free_common_residual_control_router.json`

Raw result dir:
`results/a06_07_label_free_common_residual_control_router/a06_07_full_20260621_1/`

Raw figure dir:
`figures/a06_07_label_free_common_residual_control_router/a06_07_full_20260621_1/`

Curated project experiment dir:
`Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_03_E01_common_residual_controls/`

Curated tables:

- `tables/aggregate_by_condition.csv`
- `tables/route_heatmap.csv`
- `tables/label_leakage_audit.csv`
- `tables/projection_audit.csv`
- `tables/whitening_audit.csv`
- `tables/split_audit.csv`
- `tables/dependency_audit.csv`
- `tables/router_audit.csv`

Curated figures:

- `figures/nmi_by_condition.png`
- `figures/load_oracle_gap_by_condition.png`
- `figures/route_heatmap_by_condition.png`

## 8. Claim Boundary

Can claim:
The tested label-free global common / residual controls do not approximate the A06_01_02_E01 oracle partition at step 0. They mostly improve load, not feature specialization.

Cannot claim:
This does not rule out learned feature discovery, clustering, dictionary learning, anti-lockin training, or real DCLM experiments.

## 9. Next Decision

Do not advance simple global common-centering, top-PC removal, or whitening as the method candidate. The next method should add a feature-discovery mechanism or a training anti-lockin mechanism, and any real DCLM run should use this negative result as a warning that load-only routing metrics are insufficient.

# Detailed: A06_01_02_E01 Feature-Level Initialization Positive Control

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol:
`protocol.md`

Summary:
`summary.md`

## 0. Quick Recap

Purpose:
Test whether feature-level routing is reachable at initialization when oracle feature labels are allowed for router-center construction.

Hypothesis:
If pair-feature information is present in hidden states, feature centroids should produce one-feature-one-expert routing on held-out samples.

Conclusion:
Supported. Raw, common-centered, and common-centered whitened feature centroids all reach `feature_NMI=1.0`, `L=0`, and positive margins across all 48 seed/depth/readout cells.

Boundary:
This is an oracle positive control only. It does not provide a label-free method or training-stability claim.

## 1. Protocol Compliance Audit

approved conditions match actual conditions:
Yes. The run includes random Gaussian, equal-norm random, raw centroid, common-centered centroid, and common-centered whitened centroid conditions.

primary metric exists:
Yes. `feature_NMI` appears in `tables/aggregate_by_condition.csv` and `tables/results.csv` in the raw result directory.

central figures/tables exist:
Yes. Figures and curated tables are copied into this experiment directory.

seeds/checkpoints recorded:
Yes. Eight seeds, depths 1/2/4, readouts `post_ln` and `pre_ln_replay`. Step 0 only.

held-out split audited:
Yes. Every seed/depth/readout has 2048 calibration and 2048 held-out evaluation samples per pair.

success/failure/insufficient-evidence criteria applied:
Yes. Pass means `feature_NMI >= 0.95`, `L <= 0.05`, and `margin_p05 > 0`.

## 2. Setup

Data:
Four uniform `(slot,target)` pair features. Feature identity is `pair_id`. Pair start is randomized and background tokens are independent of pair id.

Model:
Initialized Transformer-MoE replay surface from A06_01_01_E05/A06_01_01_E06. Four experts. No training.

Split:
Per seed / depth / readout / pair id, 2048 samples construct centroids and 2048 samples evaluate routing.

Run command:

```bash
python scripts/run_a06_06_feature_level_initialization_positive_control.py \
  --config configs/a06_06_feature_level_initialization_positive_control.json \
  --run-name a06_06_full_20260621_1 \
  --run-stage full \
  --device cuda
```

## 3. Conditions

`random_gaussian_init`:
Use the initialized final-router rows.

`equal_norm_random_direction`:
Normalize initialized router rows to equal norm. This tests whether row norm alone explains the baseline failure.

`raw_feature_centroid_init`:
Set one expert center per raw hidden feature centroid \(\mu_f\) and score raw held-out hidden states.

`common_centered_feature_centroid_init`:
Set one expert center per residual feature centroid \(r_f=\mu_f-c\) and score held-out residual states.

`common_centered_whitened_feature_centroid_init`:
Whiten calibration residual states, construct feature centroids in whitened residual space, and score whitened held-out residual states.

## 4. Primary Evidence

Primary readout (`num_layers=1`, `post_ln`):

| Condition | NMI | \(L\) | Margin p05 | Min margin |
| --- | ---: | ---: | ---: | ---: |
| random Gaussian | 0.1978 | 0.5610 | 0.0289 | 0.000043 |
| equal-norm random | 0.1964 | 0.5610 | 0.0303 | 0.000091 |
| raw feature centroid | 1.0000 | 0.0000 | 3.2198 | 2.4057 |
| common-centered feature centroid | 1.0000 | 0.0000 | 3.8216 | 2.9159 |
| common-centered whitened centroid | 1.0000 | 0.0000 | 1.2040 | 1.1142 |

All oracle centroid rows pass the threshold. Random and equal-norm random baselines fail on NMI and load.

## 5. Full Sweep Evidence

Across all 48 seed/depth/readout cells:

| Condition | NMI min | Max \(L\) | Min margin p05 | Pass all cells |
| --- | ---: | ---: | ---: | --- |
| raw feature centroid | 1.0000 | 0.0000 | 2.4437 | yes |
| common-centered feature centroid | 1.0000 | 0.0000 | 3.2882 | yes |
| common-centered whitened centroid | 1.0000 | 0.0000 | 1.1283 | yes |

Baseline ranges:

- random Gaussian: mean NMI `0.2302`, max NMI `0.4125`, mean $L=0.6867`;
- equal-norm random: mean NMI `0.2298`, max NMI `0.4176`, mean $L=0.6834`.

Interpretation:
Feature routing is reachable, and the result is not explained by row-norm equalization. However, the raw centroid oracle also succeeds, so the run does not establish common-centering as necessary for oracle reachability.

## 6. Visualization Results

### Feature NMI By Condition

![Feature NMI by condition](figures/feature_nmi_by_condition.png)

Purpose:
Test feature-routing reachability at step 0.

Observed result:
Centroid conditions reach perfect NMI; random baselines do not.

Take-home:
The target partition is geometrically reachable under oracle labels.

Remaining uncertainty:
No label-free construction has been tested.

### Load And Margin Guard

![Load and margin guard](figures/load_margin_by_condition.png)

Purpose:
Check whether the NMI result also has balanced load and positive margins.

Observed result:
Centroid conditions have perfect load balance and positive margin. Common-centered centroid has the largest primary p05 margin, but raw centroid already passes.

Take-home:
The oracle partition is robust at step 0.

Remaining uncertainty:
No training basin claim.

### Route Heatmap

![Route heatmap by condition](figures/route_heatmap_by_condition.png)

Purpose:
Inspect pair-to-expert assignments.

Observed result:
Centroid conditions show clean one-hot feature-to-expert routing.

Take-home:
High NMI corresponds to real one-feature-one-expert assignment, not a metric artifact.

### Margin Distribution

![Margin distribution by condition](figures/margin_distribution_by_condition.png)

Purpose:
Inspect the distributional margin guard.

Observed result:
Oracle centroid margins are well above zero; random baselines have near-zero lower-tail margins.

Take-home:
The pass is not caused by fragile ties.

## 7. Known Good / Known Bad / Known Confusing Cases

Known good:
Prior forced-oracle runs showed slot routing can be perfectly learnable. This run reproduces reachability under the current A06 hidden-state replay framing.

Known bad avoided:
The run uses held-out evaluation, so centroid construction does not reuse the exact evaluated samples.

Known confusing:
Raw centroid success means common-centering is not necessary for oracle reachability in this simplified synthetic setting. A06_01_01_E06 still matters for random initialized load and label-free control boundaries.

## 8. Artifact Map

Code workspace:
`Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/`

Runner:
`scripts/run_a06_06_feature_level_initialization_positive_control.py`

Config:
`configs/a06_06_feature_level_initialization_positive_control.json`

Raw result dir:
`results/a06_06_feature_level_initialization_positive_control/a06_06_full_20260621_1/`

Raw figure dir:
`figures/a06_06_feature_level_initialization_positive_control/a06_06_full_20260621_1/`

Curated project experiment dir:
`Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_02_E01_oracle_partition_reachability/`

Curated tables:

- `tables/aggregate_by_condition.csv`
- `tables/route_heatmap.csv`
- `tables/split_audit.csv`
- `tables/centroid_audit.csv`
- `tables/router_audit.csv`
- `tables/replay_audit.csv`
- `tables/whitening_audit.csv`

Curated figures:

- `figures/feature_nmi_by_condition.png`
- `figures/load_margin_by_condition.png`
- `figures/route_heatmap_by_condition.png`
- `figures/margin_distribution_by_condition.png`

Not copied:
Raw `margin_by_condition.csv` has about 1.97 million rows and remains in the raw result directory.

## 9. Claim Boundary

Can claim:
Feature-level routing specialization is reachable at initialization under oracle feature-centroid construction in this synthetic hidden-state setting.

Cannot claim:
Label-free initialization, training stability, expert utility, semantic specialization in real text, or DCLM transfer.

## 10. Next Decision

Proceed to A06_01_03_E01. The next question is no longer whether the target partition exists; it is whether a label-free common/residual-control construction can recover a similar partition without using `pair_id` labels.

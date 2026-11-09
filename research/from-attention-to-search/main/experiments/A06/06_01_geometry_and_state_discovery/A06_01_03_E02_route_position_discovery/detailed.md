# Detailed: A06_01_03_E02 Label-Free Feature Discovery Initialization

## 0. Quick Recap

Purpose:
test whether label-free discovery can construct pseudo-feature centers after A06_01_02_E01 showed oracle reachability and A06_01_03_E01 weakened global controls.

Hypothesis:
route-position residual hidden states contain a recoverable four-center feature partition.

Experimental idea:
fit clustering / spectral / dictionary centers on calibration hidden states without labels, convert centers to equal-norm router rows, and evaluate held-out `feature_NMI`.

Conclusion:
k-means and spherical k-means fully support the hypothesis in this synthetic setting; spectral and dictionary are unstable side evidence.

Evidence:
k-means and spherical k-means each pass 48/48 full-grid cells with mean `feature_NMI=1.0` and load $L=0.0`.

## Protocol Compliance Audit

Approved protocol:
`protocol.md`

Compliance:

| Requirement | Status | Evidence |
| --- | --- | --- |
| `slot_token_len=4` | pass | `run_config.json`, `route_audit.csv` |
| route at last slot token | pass | `route_audit.csv` |
| four uniform pair features | pass | `split_audit.csv`, generator audit |
| held-out split balanced by pair | pass | 192/192 split rows have 2048 calibration and 2048 eval per pair |
| no label leakage for label-free methods | pass | `leakage_audit.csv`, zero label-free leakage rows |
| oracle upper bound included | pass | oracle centroid NMI `1.0`, load `0.0` |
| clustering + two other families | pass | k-means/spherical, spectral, dictionary |

## Data / Model / Evaluation

Data:
synthetic sequences with four `(slot,target)` pair ids. Each example places four copies of `SLOT_s` at a random valid position and places `TARGET_s` immediately after the slot span. Background tokens are sampled independently of pair id.

Route position:
`pair_start + slot_token_len - 1`.

Model:
initialized Transformer-MoE replay with four experts. No training is performed.

Full grid:
8 seeds, 3 depths, 2 readouts, 9 conditions = 432 condition rows.

Primary metric:
held-out `feature_NMI`.

Secondary metrics:
load $L$, oracle-gap fraction, feature purity, dominant expert count, margin p05, route heatmap, cluster occupancy, pair-start nuisance NMI.

## Conditions

| Condition | Role |
| --- | --- |
| `baseline_raw_router` | random floor |
| `equal_norm_router_rows` | row-norm guard |
| `calibration_mean_router` | A06_01_03_E01 load-only baseline |
| `route_kmeans_residual_K4` | Euclidean residual clustering |
| `route_spherical_kmeans_residual_K4` | angular residual clustering |
| `route_spectral_residual_K4` | graph-structure discovery |
| `route_dictionary_residual_K4` | sparse-atom discovery |
| `route_dictionary_residual_K8_top4_guard` | overcomplete dictionary guard |
| `oracle_feature_centroid_upper` | non-label-free upper bound |

## Main Results

Primary readout (`num_layers=1`, `post_ln`, mean over 8 seeds):

| Condition | Feature NMI | Oracle gap | Load $L$ | Pass |
| --- | ---: | ---: | ---: | ---: |
| baseline raw | 0.1894 | 0.0000 | 0.5767 | 0/8 |
| equal-norm random | 0.1884 | -0.0009 | 0.5800 | 0/8 |
| calibration mean | 0.2072 | 0.0199 | 0.2691 | 0/8 |
| k-means residual K4 | 1.0000 | 1.0000 | 0.0000 | 8/8 |
| spherical k-means residual K4 | 1.0000 | 1.0000 | 0.0000 | 8/8 |
| spectral residual K4 | 0.5482 | 0.4280 | 0.4666 | 1/8 |
| dictionary residual K4 | 0.4723 | 0.3343 | 0.4944 | 0/8 |
| dictionary K8 top4 guard | 0.3994 | 0.2480 | 0.5132 | 0/8 |
| oracle centroid | 1.0000 | 1.0000 | 0.0000 | upper |

Full-grid pass counts:

| Method | Pass cells |
| --- | ---: |
| k-means residual K4 | 48/48 |
| spherical k-means residual K4 | 48/48 |
| spectral residual K4 | 13/48 |
| dictionary residual K4 | 8/48 |
| dictionary K8 top4 guard | 0/48 |

Interpretation:
the route-position residual representation is not merely anisotropic; it contains a clean four-center feature partition. However, not every label-free discovery assumption works. The reliable family here is simple residual clustering.

## Nuisance And Leakage Guards

Split:
all 192 split rows are balanced at 2048 calibration / 2048 evaluation per pair.

Leakage:
label-free conditions have zero `uses_pair_labels_for_control=true` rows.

Cluster nuisance:
for the primary readout, k-means and spherical k-means have cluster-pair NMI `1.0` and pair-start NMI about `0.0024`. This supports feature alignment rather than position alignment.

Spectral warning:
sklearn reports disconnected nearest-neighbor graphs in spectral clustering. This matches the observed instability and weakens spectral as a main method family.

## Visualization Results

### Feature NMI By Method

![Feature NMI by method](figures/nmi_by_method.png)

Purpose:
compare feature alignment across baseline, global control, discovery methods, and oracle.

How to read:
higher NMI means route assignments better match pair id.

Observed result:
k-means and spherical k-means reach oracle NMI; spectral and dictionary remain partial.

Take-home:
multi-center residual clustering closes the A06_01_02_E01-to-A06_01_03_E01 construction gap.

Remaining uncertainty:
this does not prove training preservation.

### Load Versus Oracle Gap

![Load versus oracle gap](figures/load_oracle_gap_by_method.png)

Purpose:
separate load control from feature specialization.

Observed result:
calibration mean reduces load but barely closes the NMI gap; clustering closes the gap and balances load.

Take-home:
the clustering pass is not a load-only false positive.

### Route Heatmap By Method

![Route heatmap by method](figures/route_heatmap_by_method.png)

Purpose:
check one-to-one feature-to-expert routing.

Observed result:
k-means methods show clean one-to-one assignments; non-passing methods mix or merge features.

Take-home:
the pass is compositionally clean in the tested four-feature setting.

## Artifact Map

Code workspace:
`Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding`

Runner:
`scripts/run_a06_08_label_free_feature_discovery_initialization.py`

Config:
`configs/a06_08_label_free_feature_discovery_initialization.json`

Command:
```bash
python scripts/run_a06_08_label_free_feature_discovery_initialization.py \
  --config configs/a06_08_label_free_feature_discovery_initialization.json \
  --run-name a06_08_discovery_full_20260622_1 \
  --run-stage full \
  --seeds 20260521,20260522,20260523,20260524,20260525,20260526,20260527,20260528 \
  --num-layers 1,2,4 \
  --router-input-norm post_ln,pre_ln_replay
```

Result dir:
`active/synthetic_data_understanding/results/a06_08_label_free_feature_discovery_initialization/a06_08_discovery_full_20260622_1`

Figure dir:
`active/synthetic_data_understanding/figures/a06_08_label_free_feature_discovery_initialization/a06_08_discovery_full_20260622_1`

Curated local copies:
`figures/`, `tables/`

Job id:
local/container run, no ACP job.

## Claim Boundary

Can claim:
label-free residual clustering recovers the feature partition in the current synthetic initialized hidden-state setting.

Cannot claim:
training stability, real data, semantic features, functional expert utility, or reliability of spectral/dictionary discovery.

## Next Decision

Run A06_02_01_E01 using `route_kmeans_residual_K4` as the best pseudo-center initialization.

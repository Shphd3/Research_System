# Detailed: A06_01_03_E03 Synthetic-To-Realistic Proxy Bridge

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol:
`protocol.md`

## Conclusion

A06_01_03_E03 now cleanly separates two facts.

First, the old discovery failure was a positional-geometry artifact: learned absolute `pos_emb` plus discrete slot starts can make residual k-means cluster by position. After removing learned absolute `pos_emb`, C0-C3 route-position discovery is perfect and C4 all-position discovery mostly passes.

Second, the previous mixed preservation trajectory was an implementation-confounded result: pseudo centers were discovered in one random model and then used to initialize a fresh random training model. That result was deleted and replaced by a same-model rerun. In the same-model rerun, C0-C3 discovery and preservation both pass across 8/8 seeds.

## Run Record

Canonical run:

- job id: `pt-vcl6tl57`;
- job name: `ats-a0616-same-model-audit-full`;
- run name: `a06_16_proxy_bridge_no_pos_same_model_audit_full_20260623_1`;
- code workspace: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding`;
- runner: `scripts/run_a06_16_synthetic_to_realistic_proxy_bridge.py`;
- submit script: `scripts/submit_a06_16_synthetic_to_realistic_proxy_bridge_4gpu_acp.sh`;
- config: `configs/a06_16_synthetic_to_realistic_proxy_bridge_no_pos_full.json`;
- run stage: `full`;
- seeds: `20260623` through `20260630`;
- cells: C0-C4;
- GPUs: 4 ACP shard workers in one 4-GPU job;
- aggregate log: `logs/acp/a06_16_proxy_bridge_no_pos_same_model_audit_full_20260623_1_aggregate_runtime_20260623_120937.log`.

Raw results:

`results/a06_16_synthetic_to_realistic_proxy_bridge/a06_16_proxy_bridge_no_pos_same_model_audit_full_20260623_1`

Raw figures:

`figures/a06_16_synthetic_to_realistic_proxy_bridge/a06_16_proxy_bridge_no_pos_same_model_audit_full_20260623_1`

Curated project-local copies:

`Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_03_E03_no_position_proxy_bridge`

## Protocol Compliance Audit

Approved conditions were run:

- C0 clean;
- C1 mild nuisance;
- C2 moderate nuisance;
- C3 weak feature plus nuisance;
- C4 all-position scope.

The corrected run satisfies the important implementation contract:

- no learned absolute positional embedding;
- route position is the final slot token;
- slot length is 4;
- feature, nuisance, and slot start are balanced;
- C0-C3 preservation reuses the discovery model state;
- C4 uses torch/GPU k-means for all-position clustering.

Primary metric exists: `first_failed_stage` in `stage_contract_table.csv`.

Central figures and audit tables exist:

- `figures/effective_geometry_by_cell.png`;
- `figures/bridge_first_failed_stage.png`;
- `figures/nmi_trajectory_by_bridge_cell.png`;
- `tables/discovery_heatmap.csv`;
- `tables/training_heatmap.csv`;
- `tables/training_mapping_change.csv`;
- `tables/discovery_feature_distance.csv`;
- `tables/training_feature_distance.csv`;
- `tables/discovery_feature_pca.csv`;
- `tables/training_feature_pca.csv`;
- `tables/discovery_router_alignment.csv`;
- `tables/training_router_alignment.csv`;
- `tables/c4_merge_audit.csv`.

## Data And Model

Data:

- sequence length: 32;
- feature slot length: 4;
- legal slot starts: 2, 10, 18;
- route position: `slot_start + 3`;
- target token is at `route_pos + 1`;
- 4 features, 4 nuisance ids, 4 experts;
- feature, nuisance id, and slot start are uniformly balanced.

Model:

- one-layer causal Transformer + top-1 MoE;
- `d_model=128`;
- `n_heads=4`;
- `ffn_dim=256`;
- `num_experts=4`;
- `router_metric=dot_product`;
- learned absolute `pos_emb` is zeroed and frozen.

Router normalization boundary:

- pseudo initialization normalizes discovered centers to equal router-row norm;
- the actual router forward pass uses dot product, not cosine normalization;
- in this rerun, same-model preservation keeps the partition stable despite ordinary dot-product training.

## Discovery Results

| Cell | Oracle NMI | Pseudo NMI | Slot-start NMI | Nuisance NMI | n |
| --- | ---: | ---: | ---: | ---: | ---: |
| C0 clean | 1.000 | 1.000 | 0.000 | 0.000 | 8 |
| C1 mild nuisance | 1.000 | 1.000 | 0.000 | 0.000 | 8 |
| C2 moderate nuisance | 1.000 | 1.000 | 0.000 | 0.000 | 8 |
| C3 weak feature + nuisance | 1.000 | 1.000 | 0.000 | 0.000 | 8 |
| C4 all-position | 1.000 | 0.871 | 0.000 | 0.000 | 8 |

Interpretation:

C0-C3 route-position discovery is solved in this controlled no-pos bridge. C4 is mostly solved but has a route-position boundary failure in one seed.

## Same-Model Preservation Results

| Cell | Final feature NMI | Final target acc | Final load imbalance | Mapping changes |
| --- | ---: | ---: | ---: | ---: |
| C0 clean | 1.000 | 1.000 | 0.000 | 0/32 |
| C1 mild nuisance | 1.000 | 1.000 | 0.000 | 0/32 |
| C2 moderate nuisance | 1.000 | 1.000 | 0.000 | 0/32 |
| C3 weak feature + nuisance | 1.000 | 1.000 | 0.000 | 0/32 |

Interpretation:

The same-model preservation audit falsifies the earlier interpretation that C0-C3 training was the bottleneck. The model keeps the discovered feature-to-expert partition through training. The previous mixed final NMI came from cross-model center transfer, not from same-model training collapse.

## C4 Merge Audit

C4 all-position clustering is the remaining weak point. `c4_merge_audit.csv` shows the merged feature pairs:

| Seed | Merged features | Centroid cosine | Centroid euclidean |
| ---: | --- | ---: | ---: |
| 20260623 | 1,2 | -0.108 | 13.777 |
| 20260624 | 1,3 | -0.256 | 14.557 |
| 20260626 | 0,1 | -0.259 | 14.927 |
| 20260628 | 0,1 / 0,3 / 1,3 | -0.295 / -0.374 / -0.299 | 16.260 / 16.442 / 15.257 |
| 20260629 | 0,2 | -0.391 | 16.382 |
| 20260630 | 0,1 | -0.295 | 15.548 |

Interpretation:

The merged features are not consistently adjacent feature ids, and their route-position centroids are not especially close by cosine. The failure looks like an all-position clustering allocation issue: k-means fits all token positions, but only route-position assignments are evaluated. It is not nuisance alignment and not slot-start alignment.

## Visualization Results

### Effective Geometry By Cell

![Effective geometry by cell](figures/effective_geometry_by_cell.png)

Purpose: verify that the nuisance knobs change hidden-state geometry.

How to read: higher \(\rho_{\mathrm{eff}}\) means feature center strength dominates nuisance center strength.

Observed result: C0/C1 have high \(\rho_{\mathrm{eff}}\) around 586/562; C2/C3 drop to about 26/25.

Take-home: the bridge still creates harder hidden geometry when nuisance cues are strengthened.

Remaining uncertainty: this does not test RoPE or real language.

### Step-0 Discovery

![Bridge first failed stage](figures/bridge_first_failed_stage.png)

Purpose: test whether pseudo residual k-means recovers feature identity before training.

Observed result: C0-C3 pseudo feature NMI is 1.0; C4 all-position pseudo NMI averages 0.871.

Take-home: route-position discovery is reliable; all-position discovery is mostly reliable but not fully closed.

### Same-Model Preservation

![NMI trajectory by bridge cell](figures/nmi_trajectory_by_bridge_cell.png)

Purpose: test whether same-model training preserves feature routing.

Observed result: C0-C3 remain at feature NMI 1.0 through 1600 steps.

Take-home: training preservation is not the bottleneck in the corrected no-pos slot-end bridge.

## Artifact Map

Key tables:

- `tables/discovery_table.csv`: oracle, pseudo, random, shuffled discovery metrics;
- `tables/stage_contract_table.csv`: first-failed-stage decision per seed/cell;
- `tables/training_trajectory.csv`: checkpoint NMI, accuracy, load, margin;
- `tables/discovery_heatmap.csv`: step-0 feature-to-expert assignments;
- `tables/training_heatmap.csv`: checkpoint feature-to-expert assignments;
- `tables/training_mapping_change.csv`: step0-to-checkpoint dominant expert changes;
- `tables/*_feature_distance.csv`: centroid cosine and Euclidean distances;
- `tables/*_feature_pca.csv`: centroid PCA coordinates;
- `tables/*_router_alignment.csv`: feature centroid to router-row alignment;
- `tables/c4_merge_audit.csv`: C4 merged feature-pair audit.

## Claim Boundary

Can claim:

- no-pos C0-C3 route-position discovery succeeds;
- no-pos C0-C3 same-model preservation succeeds;
- C4 all-position discovery mostly succeeds but still has a boundary failure;
- the old preservation failure interpretation was caused by a cross-model implementation confound.

Cannot claim:

- RoPE behavior;
- learned absolute position robustness;
- real-DCLM preservation;
- whole-slot compositional semantics;
- utility binding.

## Next Decision

The natural next decision is no longer "fix preservation" inside this controlled no-pos bridge. The next anchor should choose one boundary to attack:

- all-position robustness: why C4 k-means merges whole features;
- RoPE/position encoding: whether positional information reintroduces clustering confounds;
- whole-slot composition: remove feature-specific slot-end token shortcuts;
- real-DCLM preservation: return to the real proxy line with the synthetic bridge boundary now clarified.

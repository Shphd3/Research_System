---
experiment_id: A06_01_03_E04_all_position_pool_audit
anchor_id: A06_01_03_E04_all_position_pool_audit
status: result_updated
run_name: a06_17_route_relevant_pool_audit_full_20260623_1
job_id: pt-9mt77o49
canonical_language: en
---

# A06_01_03_E04 Detailed: All-Position Route-Relevant Feature Discovery

## Question

A06_01_03_E03 left one boundary: route-position clustering works, but all-position clustering can merge features. A06_01_03_E04 asks whether this happens because the clustering pool contains many hidden states that are not route-relevant.

Primary metric: held-out route-position `feature_NMI`.

Why this metric decides the question: the router decision is evaluated at the last token of the feature slot. If a center set cannot separate features at that position, it is not a valid feature-level router initialization.

## Exact Setup

- Model: one-layer Transformer + top-1 MoE from A06_01_03_E03.
- Positional embedding: disabled.
- Cell: `C4_all_position_scope`.
- Sequence length: 32.
- Feature slot length: 4.
- Route position: slot offset 3, the last token in the feature slot.
- Slot starts: 2, 10, 18.
- Feature / nuisance / slot-start distribution: strict balanced Cartesian product.
- Features / experts: 4 / 4.
- Full seeds: `20260623` to `20260630`.
- Calibration samples per `(feature, nuisance, slot_start)`: 256.
- Evaluation samples per `(feature, nuisance, slot_start)`: 256.
- K-means: torch/GPU residual k-means, K=4, 20 restarts, 80 max iterations.

## Conditions

| Pool | Fit object | Label use during fitting |
| --- | --- | --- |
| `oracle_route_upper_bound` | route states grouped by true feature | yes, upper bound only |
| `route_only` | route states only | no |
| `all_position` | all 32 sequence positions | no |
| `slot_mixed` | all four feature-slot offsets | no |
| `slot_offset_0/1/2/3` | one slot offset at a time | no |
| `role_balanced_all` | equal route, slot-nonroute, nuisance, and neutral groups | no |
| `non_slot_no_target` | outside the feature slot and target token | no |

Every fitted center set is evaluated on held-out route-position hidden states.

## Main Result

| Pool | Mean feature NMI | Min | Max | Perfect seeds | Mean active experts |
| --- | ---: | ---: | ---: | ---: | ---: |
| oracle route upper bound | 1.000 | 1.000 | 1.000 | 8/8 | 4.00 |
| route only | 1.000 | 1.000 | 1.000 | 8/8 | 4.00 |
| all position | 0.797 | 0.637 | 1.000 | 1/8 | 2.75 |
| slot mixed | 0.900 | 0.866 | 1.000 | 2/8 | 3.25 |
| slot offset 0 | 0.688 | 0.507 | 0.865 | 0/8 | 3.50 |
| slot offset 1 | 0.801 | 0.665 | 0.998 | 1/8 | 3.25 |
| slot offset 2 | 0.793 | 0.671 | 0.993 | 1/8 | 3.50 |
| slot offset 3 | 1.000 | 1.000 | 1.000 | 8/8 | 4.00 |
| role-balanced all | 0.854 | 0.637 | 1.000 | 1/8 | 3.00 |
| non-slot no-target | 0.664 | 0.346 | 0.887 | 0/8 | 3.25 |

Source: `tables/pool_comparison_aggregate.csv`.

Interpretation: the feature partition is fully available at the route position and recoverable without labels, but it is not recovered reliably when k-means is fit on every hidden state.

## Failure Decomposition

All-position failure is a feature merge, not nuisance routing.

- all-position mean `nuisance_NMI=0.0`;
- all-position mean `slot_start_NMI=0.0`;
- all-position `feature_purity=1.0`;
- all-position mean active experts is 2.75, with three seeds using only two experts.

This means complete feature classes are routed together rather than being mixed sample-by-sample.

All-position fit population is dominated by non-route states:

| Role in all-position fit pool | Fraction |
| --- | ---: |
| neutral | 0.812 |
| route slot offset 3 | 0.031 |
| slot offset 0 | 0.031 |
| slot offset 1 | 0.031 |
| slot offset 2 | 0.031 |
| nuisance | 0.031 |
| target | 0.031 |

Role-balanced sampling raises route states to 25%, but does not fully recover route NMI. Therefore the problem is not only occupancy imbalance; different position roles have different geometries and should not be forced into one k-means objective.

The merged pairs are not consistently the closest route-feature centroids. In all-position failures, merged-pair Euclidean closeness ranks range from 1 to 6. This weakens the rival explanation that route geometry itself is insufficient.

## Visualization Results

![A06_01_03_E04 pool feature NMI](figures/pool_feature_nmi.png)

Purpose: compare which hidden-state pool produces centers that separate features at the route position.

Setup: every pool is clustered without feature labels except the oracle upper bound; all center sets are evaluated on held-out route-position hidden states.

How to read: higher bars and orange points mean better feature partition recovery. Error bars show seed range.

Observed result: oracle, route-only, and slot offset 3 are perfect across all seeds. All-position and role-balanced all-position are seed-sensitive and often collapse features.

Take-home: route-relevant state selection is necessary before clustering.

Remaining uncertainty: this does not yet define a label-free selector for real data.

![A06_01_03_E04 feature NMI by seed and pool](figures/pool_feature_nmi_heatmap.png)

Purpose: check whether the pool effect is seed-stable.

How to read: yellow means high feature NMI; green/blue means failure or partial merge.

Observed result: route-only and slot offset 3 are always yellow. All-position, slot-mixed, role-balanced, and non-slot pools vary by seed.

Take-home: the route state is the reliable object; mixed-role clustering is not.

Remaining uncertainty: non-slot states contain some feature information through attention, but this information is not clean enough for route initialization.

## Artifact Map

Code workspace:

`Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding`

Runner:

`scripts/run_a06_17_all_position_route_relevant_feature_discovery.py`

Config:

`configs/a06_17_all_position_route_relevant_feature_discovery.json`

Submit script:

`scripts/submit_a06_17_all_position_route_relevant_feature_discovery_4gpu_acp.sh`

Run:

- run name: `a06_17_route_relevant_pool_audit_full_20260623_1`
- ACP job id: `pt-9mt77o49`
- submit log: `logs/acp/a06_17_route_relevant_pool_audit_full_20260623_1_submit_20260623_165101.log`
- result dir: `active/synthetic_data_understanding/results/a06_17_all_position_route_relevant_feature_discovery/a06_17_route_relevant_pool_audit_full_20260623_1`
- figure dir: `active/synthetic_data_understanding/figures/a06_17_all_position_route_relevant_feature_discovery/a06_17_route_relevant_pool_audit_full_20260623_1`

Curated project-local copies:

- `tables/pool_comparison.csv`
- `tables/pool_comparison_aggregate.csv`
- `tables/pool_heatmap.csv`
- `tables/pool_mapping_audit.csv`
- `tables/cluster_role_composition.csv`
- `tables/cluster_position_composition.csv`
- `tables/merge_audit.csv`
- `tables/route_feature_distance.csv`
- `tables/route_feature_pca.csv`
- `figures/pool_feature_nmi.png`
- `figures/pool_feature_nmi_heatmap.png`

Repro command:

```bash
cd /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
A0617_ALLOW_REAL_SUBMIT=1 bash scripts/submit_a06_17_all_position_route_relevant_feature_discovery_4gpu_acp.sh
```

## Claim Boundary

Supported claim: in the controlled no-position bridge, all hidden states are not a valid proxy population for feature-level router initialization. Route-position states are valid and label-free k-means recovers them perfectly.

Not supported yet: real-language feature discovery, RoPE robustness, whole-slot semantic composition, or a practical DCLM initialization method.

## Next Decision

The next anchor should test a label-free route-relevant state selector. The concrete research move is: identify route-like hidden states first, then cluster only those states for feature initialization.

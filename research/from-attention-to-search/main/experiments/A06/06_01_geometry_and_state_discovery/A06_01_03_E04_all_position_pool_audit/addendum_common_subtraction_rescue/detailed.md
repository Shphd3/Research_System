# Addendum Detailed: Training-Time Common Subtraction Rescue Audit

Parent experiment: `../summary.md`

Summary: `summary.md`

## Decision

Training-time common subtraction does not rescue the exact A06_01_03_E04
all-position failure seeds. The failed two-expert merge remains unchanged
through step 800 under raw, fixed-common, and dynamic-common router inputs.

## Setup

- Cell: A06_01_03_E04 C4 all-position scope.
- Seeds: `20260623`, `20260625`, `20260626`.
- Initializer: exact A06_01_03_E04 all-position residual k-means offset.
- Model: one-layer Transformer + top-1 MoE.
- Positional embedding: disabled.
- Route position: last token of the feature slot.
- Feature slot length: 4.
- Training objective: route-position target cross-entropy.
- Training steps: 800.

## Conditions

| Condition | Router input | Initial router rows |
|---|---|---|
| `raw_allpos_init` | raw post-attention router input | raw all-position cluster centers |
| `fixed_common_allpos_init` | \(h-c_0\) | residual all-position centers |
| `dynamic_common_allpos_init` | \(h-\bar h_{\mathrm{batch}}(t)\) | residual all-position centers |

## Result Table

| Condition | Step-0 NMI | Step-800 NMI | Step-800 max load | Step-800 active experts | Step-800 target acc |
|---|---:|---:|---:|---:|---:|
| raw all-position init | 0.637 | 0.637 | 0.75 | 2.0 | 1.0 |
| fixed common subtraction | 0.637 | 0.637 | 0.75 | 2.0 | 1.0 |
| dynamic common subtraction | 0.637 | 0.637 | 0.75 | 2.0 | 1.0 |

All three seeds have identical qualitative behavior: the merged feature
partition is preserved while target accuracy reaches 1.0.

## Visualization Results

### Feature NMI Trajectory

![Feature NMI trajectory](figures/feature_nmi_trajectory.png)

Purpose: test whether common subtraction changes the route-position feature
partition during training.

Observed result: all conditions remain at `feature_NMI=0.6369`.

Take-home: common subtraction does not rescue feature specialization.

### Max Load Trajectory

![Max load trajectory](figures/max_load_trajectory.png)

Purpose: test whether common subtraction changes the load collapse associated
with the merged partition.

Observed result: all conditions remain at max load `0.75`.

Take-home: the intervention does not change the two-expert merged route
allocation.

## Artifact Map

Code workspace:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/`

Runner:
`scripts/run_a06_17_common_subtraction_rescue_addendum.py`

Config:
`configs/a06_17_common_subtraction_rescue_addendum.json`

Run name:
`a06_17_common_subtraction_rescue_exact_full_20260629`

Local logs:

- `logs/local/a06_17_common_subtraction_rescue_exact_full_20260629_shard0.log`
- `logs/local/a06_17_common_subtraction_rescue_exact_full_20260629_shard1.log`
- `logs/local/a06_17_common_subtraction_rescue_exact_full_20260629_aggregate.log`

Curated tables:

- `tables/trajectory.csv`
- `tables/trajectory_aggregate.csv`
- `tables/init_audit.csv`
- `tables/heatmap.csv`
- `tables/mapping_audit.csv`
- `tables/balance_audit.csv`

Curated figures:

- `figures/feature_nmi_trajectory.png`
- `figures/max_load_trajectory.png`

## Claim Boundary

This addendum only tests exact A06_01_03_E04 all-position failure seeds in the
controlled no-position bridge. It does not prove that common subtraction is
useless in every setup. It does show that, after the all-position center
fitting step has already merged features, fixed or dynamic common subtraction
is not enough to recover a feature-specialized route partition.


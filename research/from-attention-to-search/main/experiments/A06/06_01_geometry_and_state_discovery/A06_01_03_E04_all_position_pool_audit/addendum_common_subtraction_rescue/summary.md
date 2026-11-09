# Addendum Summary: Training-Time Common Subtraction Rescue Audit

Parent experiment: `../summary.md`

Parent anchor:
`../../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

## Purpose

This addendum tests a narrow rival explanation for A06_01_03_E04. A06_01_03_E04 concluded
that all-position clustering fails because it fits the wrong hidden-state
population. The rival explanation is that the failed all-position seeds might
be rescued if common router-input components are subtracted throughout
training.

## Exact Setup

- Controlled A06_01_03_E04 no-position C4 all-position scope.
- Failed all-position seeds: `20260623`, `20260625`, `20260626`.
- Initializer: exact A06_01_03_E04 all-position residual k-means seed offset.
- Model: one-layer Transformer + top-1 MoE.
- Feature slot length 4; route position is the last slot token.
- Training steps: 800.
- Conditions:
  - `raw_allpos_init`: raw router input after all-position initialization.
  - `fixed_common_allpos_init`: subtract step-0 all-position mean from router
    input throughout training.
  - `dynamic_common_allpos_init`: subtract current batch all-position mean from
    router input during training and evaluation.

## Primary Metric

Primary metric: held-out route-position `feature_NMI(t)`.

This decides the addendum because the question is whether common subtraction
rescues feature specialization, not whether it changes margins or task
accuracy.

## Result

**Verdict: not rescued.**

All three failed seeds remain in the same two-expert feature-merge partition
for all conditions and all checkpoints.

| Condition | Step-0 NMI | Step-800 NMI | Step-800 max load | Step-800 active experts | Step-800 target acc |
|---|---:|---:|---:|---:|---:|
| raw all-position init | 0.637 | 0.637 | 0.75 | 2.0 | 1.0 |
| fixed common subtraction | 0.637 | 0.637 | 0.75 | 2.0 | 1.0 |
| dynamic common subtraction | 0.637 | 0.637 | 0.75 | 2.0 | 1.0 |

The model learns the target, and route margins increase, but the feature
partition does not change. Common subtraction does not turn the failed
all-position basin into a feature-specialized basin.

## Key Figures

### Figure: Feature NMI Trajectory

![Feature NMI trajectory](figures/feature_nmi_trajectory.png)

What this tests: whether fixed or dynamic common subtraction rescues failed
all-position initialization.

Observed result: all curves stay exactly at `feature_NMI=0.6369`.

Take-home: subtracting common during training does not recover the missing
feature centers.

### Figure: Max Load Trajectory

![Max load trajectory](figures/max_load_trajectory.png)

What this tests: whether common subtraction at least changes load in the
failed basin.

Observed result: all conditions remain at max load `0.75`, using only two
experts.

Take-home: in this exact failure basin, common subtraction does not even alter
the merged allocation.

## Interpretation

The failure is not a simple common-bias effect that can be rescued after
all-position clustering has already merged features. Once all-position k-means
initializes a two-expert merged partition, training with fixed or dynamic
common-subtracted router inputs preserves the merge while learning the target.

This supports the original A06_01_03_E04 interpretation: the first wrong choice is
the center-fitting population. The next step remains route-relevant state
selection before clustering.

## Claim Boundary

Can claim:

- In these exact A06_01_03_E04 all-position failure seeds, training-time common
  subtraction does not rescue feature specialization.
- The result supports sample-pool mismatch over common-bias rescue as the
  local explanation.

Cannot claim:

- Real-DCLM behavior.
- RoPE behavior.
- That common subtraction never helps in other initializations.
- Expert utility.

## Artifacts

- `tables/trajectory.csv`
- `tables/trajectory_aggregate.csv`
- `tables/init_audit.csv`
- `tables/heatmap.csv`
- `figures/feature_nmi_trajectory.png`
- `figures/max_load_trajectory.png`


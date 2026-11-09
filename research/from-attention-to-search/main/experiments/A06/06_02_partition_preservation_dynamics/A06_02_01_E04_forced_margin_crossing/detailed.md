# Detailed: A06_02_01_E04 Margin Crossing Causal Stress

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol: `protocol.md`

## Executive Judgment

The experiment separates two claims:

1. **Static geometry claim:** margin predicts the frozen-router switch
   boundary. This is supported.
2. **Training crossing claim:** the current stress settings can force
   preservation failure. This is not supported; the stress lowers margin but
   does not cross the boundary.

Therefore A06_02_01_E04 strengthens the geometric interpretation but does not yet
provide a training failure threshold.

The forced-crossing addendum completes the local causal chain post hoc:
explicit router-row interpolation toward the nearest competitor makes dynamic
margin negative and destroys the original matched expert region.

## Protocol Compliance

The run executed the three planned stages:

- Stage 1 static boundary-directed crossing calibration;
- Stage 2 margin weakening through row-norm reduction and random-row mixing;
- Stage 3 drift amplification through `lr_mult = 3.0`.

The run used C0-C3, 4 seeds, and the seven protocol conditions. No unplanned
condition was added after seeing results.

## Data Construction

The setup matches the corrected A06 no-position bridge:

- sequence length `32`;
- feature slot length `4`;
- slot starts `[2, 10, 18]`;
- route position is the last token in the feature slot;
- next token after the slot is the target token;
- target depends only on feature identity;
- feature, nuisance, and slot start are sampled uniformly by construction;
- no B token is used;
- learned absolute positional embedding is disabled.

## Model And Training

Model: one-layer Transformer, top-1 selected-gate sparse MoE, 4 experts,
`d_model = 128`, 4 attention heads, no dropout, dot-product router.

Training: slot-end target cross-entropy, 1600 steps, AdamW, base learning rate
`0.0008`, LR stress `0.0024`, checkpoints
`0, 1, 2, 5, 10, 20, 50, 100, 200, 400, 800, 1600`.

## Conditions

| Condition | Meaning |
|---|---|
| `oracle_base_lr1x` | oracle center baseline guard |
| `pseudo_base_lr1x` | pseudo center baseline |
| `pseudo_norm0p5_lr1x` | same pseudo direction, half row norm |
| `pseudo_mix0p25_lr1x` | pseudo row mixed 25% with random direction |
| `pseudo_mix0p50_lr1x` | pseudo row mixed 50% with random direction |
| `pseudo_base_lr3x` | pseudo baseline with 3x LR drift stress |
| `pseudo_norm0p5_lr3x` | half-norm pseudo with 3x LR drift stress |

## Complete Result Table

| Condition | Static center switch ratio | Any-sample switch ratio | Majority switch ratio | Preserve fraction at predicted ratio 1 | Final feature NMI | Final min dynamic margin | Max boundary consumption | Dynamic switch rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| oracle_base_lr1x | 1.039 | 1.000 | 1.077 | 0.511 | 1.000 | 3.361 | 0.502 | 0.000 |
| pseudo_base_lr1x | 1.039 | 1.000 | 1.077 | 0.511 | 1.000 | 3.467 | 0.516 | 0.000 |
| pseudo_norm0p5_lr1x | 1.045 | 1.000 | 1.077 | 0.511 | 1.000 | 2.115 | 0.522 | 0.000 |
| pseudo_mix0p25_lr1x | 1.066 | 1.000 | 1.069 | 0.508 | 1.000 | 3.281 | 0.521 | 0.000 |
| pseudo_mix0p50_lr1x | 1.055 | 0.998 | 1.063 | 0.507 | 1.000 | 2.509 | 0.569 | 0.000 |
| pseudo_base_lr3x | 1.039 | 1.000 | 1.077 | 0.511 | 1.000 | 1.535 | 0.697 | 0.000 |
| pseudo_norm0p5_lr3x | 1.045 | 1.000 | 1.077 | 0.511 | 1.000 | 0.701 | 0.718 | 0.000 |

## Forced-Crossing Addendum

After the main run, we reran two representative conditions and performed a
post-hoc router-row intervention. For each matched expert row \(w_e\), we moved
it toward the nearest competitor row \(w_j\):

\[
w_e'(\alpha)=(1-\alpha)w_e+\alpha w_j.
\]

This addendum is not a new training method. It is a causal geometry audit:
force the router boundary to cross the feature region and check whether the
original route assignment breaks.

| Condition | First alpha margin negative | First alpha NMI < 0.95 | Preserve frac alpha 0.0 | Preserve frac alpha 0.5 | Preserve frac alpha 0.75 | Preserve frac alpha 1.25 |
|---|---:|---:|---:|---:|---:|---:|
| pseudo_base_lr1x | 0.578 | 0.656 | 1.000 | 0.797 | 0.312 | 0.000 |
| pseudo_norm0p5_lr3x | 0.578 | 0.656 | 1.000 | 0.806 | 0.310 | 0.031 |

Important interpretation: NMI is permutation-invariant. If all features switch
consistently to different experts, NMI can remain nonzero. Therefore the
decisive preservation metric for this addendum is matched-region preserve
fraction, not NMI alone.

## Per-Cell Final Stress Readout

The most stressed condition, `pseudo_norm0p5_lr3x`, remained preserved in every
cell:

| Cell | Final NMI | Min dynamic margin | Max boundary consumption |
|---|---:|---:|---:|
| C0_clean | 1.000 | 0.572 | 0.640 |
| C1_mild_nuisance | 1.000 | 0.873 | 0.705 |
| C2_moderate_nuisance | 1.000 | 0.722 | 0.759 |
| C3_weak_feature_nuisance | 1.000 | 0.639 | 0.768 |

## Visualization Results

### Static crossing ratio by condition

![Static crossing ratio](figures/static_center_switch_ratio_by_condition.png)

**Purpose:** verify whether the nearest-boundary distance predicts the frozen
router switch point.

**Observed result:** all conditions switch near `1.0`.

**Take-home:** margin is a reliable static geometric ruler here.

**Remaining uncertainty:** static crossing does not determine whether training
will naturally cross the same boundary.

### Boundary consumption trajectory

![Boundary consumption trajectory](figures/boundary_consumption_trajectory.png)

**Purpose:** measure how much of the initial margin buffer is consumed during
training.

**Observed result:** high-LR conditions consume more buffer, especially
`pseudo_norm0p5_lr3x`, but average max consumption stays below 1.

**Take-home:** training stress moved toward the boundary but did not cross it.

### Dynamic margin trajectory

![Dynamic margin trajectory](figures/dynamic_margin_trajectory.png)

**Purpose:** guard against frozen-boundary artifacts by measuring the actual
dynamic router margin.

**Observed result:** stress lowers dynamic margin; the strongest condition has
mean final minimum margin `0.701`, still positive.

**Take-home:** no dynamic margin crossing occurred.

### Feature NMI trajectory

![Feature NMI trajectory](figures/feature_nmi_trajectory.png)

**Purpose:** test whether feature-specialized routing fails.

**Observed result:** all conditions keep feature NMI at `1.0`.

**Take-home:** this stress run did not create preservation failure.

### Forced crossing dynamic margin

![Forced crossing dynamic margin](figures/forced_crossing_dynamic_margin.png)

**Purpose:** check whether post-hoc row interpolation forces the router across
the feature boundary.

**Observed result:** dynamic margin crosses below zero around alpha
`0.5-0.75`.

**Take-home:** the forced intervention creates the missing crossing event.

### Forced crossing feature NMI

![Forced crossing feature NMI](figures/forced_crossing_feature_nmi.png)

**Purpose:** measure whether feature clustering under route assignments
degrades after forced boundary crossing.

**Observed result:** NMI drops below `0.95` around alpha `0.656` on average,
but can remain nonzero because NMI ignores expert identity permutation.

**Take-home:** NMI is useful but not sufficient for preservation identity.

## Failure / Partial-Support Analysis

The static part of the anchor passes. The training part is partial support:
the direction of stress is right because margins shrink and boundary
consumption grows, but the stress is not strong enough to produce the causal
failure event.

## Artifact Map

Code:
`../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_17_04_margin_crossing_causal_stress.py`

Config:
`../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_17_04_margin_crossing_causal_stress.json`

Raw result directory:
`../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_17_04_margin_crossing_causal_stress/a06_17_04_margin_crossing_full_20260629_1/`

Curated tables:

- `tables/static_crossing_aggregate.csv`
- `tables/condition_final_stress_aggregate.csv`
- `tables/stress_metric_aggregate.csv`
- `tables/condition_final_stress.csv`
- `tables/forced_crossing_aggregate.csv`
- `tables/forced_crossing_threshold_aggregate.csv`
- `tables/forced_crossing_preserve_frac_aggregate.csv`

Curated figures:

- `figures/static_center_switch_ratio_by_condition.png`
- `figures/boundary_consumption_trajectory.png`
- `figures/dynamic_margin_trajectory.png`
- `figures/feature_nmi_trajectory.png`
- `figures/dynamic_switch_rate_trajectory.png`
- `figures/forced_crossing_dynamic_margin.png`
- `figures/forced_crossing_feature_nmi.png`
- `figures/forced_crossing_center_switch_rate.png`

## Claim Boundary

Can claim: margin is a valid static geometric switch ruler in the controlled
no-position bridge. The tested training stress settings reduce but do not
exhaust the margin buffer. A forced post-hoc boundary crossing breaks the
original feature-to-expert preservation region.

Cannot claim: exact training failure limit, real-DCLM preservation, semantic
features, utility, or that margin alone is sufficient under arbitrary
training drift.

## Next Decision

Move from mechanism to method design. The next anchor should ask whether a
label-free initialization can be selected by positive margin and whether a
candidate that lacks sufficient margin should be rejected before training.

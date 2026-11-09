# Summary: A06_02_01_E06 Margin-Budget Preservation Audit

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol: `protocol.md`

## Result Snapshot

**Decision: supported for the controlled no-position bridge.**

The full run supports the margin-budget interpretation: pseudo-center and
oracle-center initialization preserve feature routing because their pairwise
feature-to-expert margins remain positive. Random, equal-norm random, and
label-shuffled guards do not have a valid positive-margin partition, and they
show negative margins, sign flips, low matched preserve fraction, and higher
common-share routing.

The audit does **not** show that margin budget already explains real-DCLM
failure. It gives the diagnostic that should be applied next to real-DCLM:
measure whether real-DCLM proxy routing is erased because there is no
step-0 residual margin, because early training consumes the margin, or because
common directions overwrite residual feature terms.

## Exact Setup

- Controlled A06 no-position bridge.
- One-layer Transformer + top-1 MoE, 4 experts, `d_model=128`.
- 4 feature ids, 4 nuisance ids, feature slot length 4.
- Slot starts move across `[2, 10, 18]`.
- Route/evaluation position is the last token of the feature slot.
- No learned absolute positional embedding and no B token.
- Training objective: slot-end target cross-entropy.
- Full run: 8 seeds x C0-C3 cells x 5 conditions x 1600 steps.
- Conditions: `pseudo_center_init`, `oracle_center_init`,
  `random_gaussian_init`, `equal_norm_random_init`,
  `label_shuffled_center_guard`.
- Checkpoints: `0, 1, 2, 5, 10, 20, 50, 100, 200, 400, 800, 1600`.

Run name:
`a06_21_margin_budget_full_20260629_1`.

Coverage:

- `margin_budget_metrics_by_step.csv`: 1920 rows.
- Pair-level source: 23,040 rows; its execution location and SHA-256 are recorded
  in [Detailed](detailed.md). The aggregate decision tables remain beside this Summary.
- Decomposition identity max error: `1.37e-6`, below the `1e-4` tolerance.

## Primary Metric

Primary metric: feature-route normalized mutual information, abbreviated as
feature NMI. It measures whether top-1 expert assignments still separate the
fixed feature ids.

Mechanism metrics:

- current pairwise margin `gamma_t_min`;
- pairwise sign flip rate;
- cluster-aware margin;
- matched preserve fraction;
- common-share term;
- drift attribution terms.

## Key Evidence

### Early Step 5

| Condition | Feature NMI | Preserve frac min | Min margin | Sign flip | Cluster-aware margin | Common share | Max load |
|---|---:|---:|---:|---:|---:|---:|---:|
| Pseudo-center | 1.000 | 1.000 | 5.868 | 0.000 | 4.545 | 0.031 | 0.250 |
| Oracle-center | 1.000 | 1.000 | 5.882 | 0.000 | 4.537 | 0.031 | 0.250 |
| Random Gaussian | 0.816 | 0.162 | -0.678 | 0.182 | -1.949 | 0.343 | 0.483 |
| Equal-norm random | 0.808 | 0.140 | -0.671 | 0.187 | -1.936 | 0.339 | 0.488 |
| Label-shuffled center | 0.869 | 0.094 | -0.342 | 0.245 | -0.436 | 0.314 | 0.461 |

### Early Step 10

| Condition | Feature NMI | Preserve frac min | Min margin | Sign flip | Cluster-aware margin | Common share | Max load |
|---|---:|---:|---:|---:|---:|---:|---:|
| Pseudo-center | 1.000 | 1.000 | 5.688 | 0.000 | 4.532 | 0.038 | 0.250 |
| Oracle-center | 1.000 | 1.000 | 5.771 | 0.000 | 4.537 | 0.037 | 0.250 |
| Random Gaussian | 0.823 | 0.157 | -1.394 | 0.229 | -2.517 | 0.357 | 0.484 |
| Equal-norm random | 0.827 | 0.171 | -1.420 | 0.229 | -2.521 | 0.359 | 0.481 |
| Label-shuffled center | 0.869 | 0.094 | -0.685 | 0.286 | -0.857 | 0.323 | 0.461 |

### Final Step 1600

| Condition | Feature NMI | Preserve frac min | Min margin | Sign flip | Cluster-aware margin | Common share | Max load |
|---|---:|---:|---:|---:|---:|---:|---:|
| Pseudo-center | 1.000 | 1.000 | 3.555 | 0.000 | 3.264 | 0.076 | 0.250 |
| Oracle-center | 1.000 | 1.000 | 3.726 | 0.000 | 3.460 | 0.071 | 0.250 |
| Random Gaussian | 0.823 | 0.156 | -2.919 | 0.320 | -3.200 | 0.389 | 0.484 |
| Equal-norm random | 0.832 | 0.188 | -2.874 | 0.320 | -3.106 | 0.387 | 0.477 |
| Label-shuffled center | 0.869 | 0.094 | -1.392 | 0.289 | -1.445 | 0.422 | 0.461 |

## Interpretation

The decisive evidence is not only that pseudo-center and oracle-center have
NMI `1.0`. They also have:

- positive current margins;
- zero sign flips;
- positive cluster-aware margins;
- matched preserve fraction `1.0`;
- low common share;
- balanced load.

The guard conditions show the opposite pattern. Random and equal-norm random
learn the task but do not preserve a clean feature-to-expert identity.
Label-shuffled center has moderately high NMI, but its matched preserve
fraction is only about `0.094` at the final step; it is not preserving the
intended feature-to-expert mapping.

The drift attribution refines the mechanism. In pseudo-center and
oracle-center runs, the largest negative contribution comes from feature-center
drift, not router-boundary drift. But the initial margin is large enough, so
the margin remains positive and routing stays preserved. This means:

```text
feature drift exists
but it does not cause collapse
unless it exhausts the positive margin buffer
```

Common overwrite is not the supported explanation for successful center-init
preservation in this controlled bridge. Center-init common share remains low
(`0.071-0.076` final). Guard conditions have higher common share, but because
they already lack a valid positive-margin partition, this audit cannot claim
that common share alone caused their failure.

## Central Figures

### Feature NMI Trajectory

![Feature NMI trajectory](figures/feature_nmi_trajectory.png)

What this tests: whether route assignments remain aligned with feature ids.

Observed result: pseudo-center and oracle-center remain at `1.0`; random,
equal-norm random, and label-shuffled guards do not reach clean preservation.

Take-home: center initialization preserves the controlled feature partition.

### Current Margin Trajectory

![Current margin trajectory](figures/current_margin_trajectory.png)

What this tests: whether feature centers stay inside their intended expert
regions.

Observed result: pseudo-center and oracle-center keep positive current margins;
random, equal-norm random, and label-shuffled guards have negative margins.

Take-home: margin is the cleanest mechanism coordinate in this audit.

### Sign Flip Trajectory

![Sign flip trajectory](figures/sign_flip_rate_trajectory.png)

What this tests: whether pairwise feature-expert margins cross zero.

Observed result: center-init conditions have zero sign flips. Guard conditions
show persistent sign flips.

Take-home: sign flips distinguish preserved partition identity from merely
moderate NMI.

### Common Share Trajectory

![Common share trajectory](figures/common_share_trajectory.png)

What this tests: whether router margins are dominated by the common component
rather than residual feature directions.

Observed result: center-init common share remains low. Guard conditions have
higher common share.

Take-home: common dominance is a useful guard, but this controlled audit does
not prove common overwrite as the cause of center-init failure.

### Final Drift Attribution

![Final drift attribution](figures/final_drift_attribution.png)

What this tests: which margin-decomposition term contributes negative margin
pressure.

Observed result: in center-init runs, negative pressure is mostly
feature-center drift, with smaller interaction drift. Router drift is not the
main negative term.

Take-home: preservation is not active tracking. It is positive margin surviving
feature-center drift.

## Claim Boundary

Can claim:

- In the controlled no-position bridge, margin-budget diagnostics explain why
  pseudo-center and oracle-center preserve routing.
- Positive current margin, zero sign flips, and positive cluster-aware margin
  are better preservation diagnostics than NMI alone.
- Feature-center drift can be large enough to consume some margin while still
  staying inside the positive-margin basin.

Cannot claim:

- real-DCLM early failure is already explained;
- common subtraction will fix preservation;
- high NMI proves expert utility;
- synthetic feature partitions are semantic features.

## Next Decision

Apply the same audit to real-DCLM A06_01_04_E03-style proxy-init training. The next
question should be:

```text
Does real-DCLM proxy routing fail because step-0 residual margin is already
weak, because early training consumes that margin, or because common directions
overwrite residual feature terms?
```

If saved hidden states and router rows are missing for A06_01_04_E03, rerun only the
minimal snapshot collection needed for this margin decomposition.

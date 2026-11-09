# Detailed: A06_02_01_E06 Margin-Budget Preservation Audit

## 1. Protocol Compliance

Protocol: `protocol.md`.

Status: completed.

The full audit ran the approved controlled bridge configuration:

- 8 seeds: `20260623` to `20260630`;
- 4 cells: C0-C3;
- 5 conditions;
- 12 checkpoints through step 1600;
- route-position hidden states and router rows collected at every checkpoint;
- pairwise margin decomposition computed for every feature/competitor pair.

Coverage:

| Table | Rows |
|---|---:|
| `margin_budget_metrics_by_step.csv` | 1920 |
| `margin_budget_by_pair.csv` | 23040 |
| `discovery_summary.csv` | 32 |

Both shards completed. Snapshot inventory is in
`tables/snapshot_inventory.csv`.

Decomposition identity audit:

\[
\gamma_{f,e}(t)
=
\gamma_{f,e}(0)
+
\Delta u_{f,e}(t)^\top \mu_f(0)
+
u_{f,e}(0)^\top \Delta\mu_f(t)
+
\Delta u_{f,e}(t)^\top \Delta\mu_f(t).
\]

Maximum absolute reconstruction error across the full run:

```text
1.37e-6
```

This is below the protocol tolerance `1e-4`.

## 2. Setup

Experiment workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
```

Mainline experiment folder:

```text
Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_01_E06_margin_budget_audit
```

Run name:

```text
a06_21_margin_budget_full_20260629_1
```

Script:

```text
scripts/run_a06_21_margin_budget_preservation_audit.py
```

Config:

```text
configs/a06_21_margin_budget_preservation_audit.json
```

Local execution:

```text
CUDA_VISIBLE_DEVICES=0 python scripts/run_a06_21_margin_budget_preservation_audit.py \
  --config configs/a06_21_margin_budget_preservation_audit.json \
  --run-name a06_21_margin_budget_full_20260629_1 \
  --run-stage full \
  --shard-index 0 \
  --num-shards 2 \
  --device cuda

CUDA_VISIBLE_DEVICES=1 python scripts/run_a06_21_margin_budget_preservation_audit.py \
  --config configs/a06_21_margin_budget_preservation_audit.json \
  --run-name a06_21_margin_budget_full_20260629_1 \
  --run-stage full \
  --shard-index 1 \
  --num-shards 2 \
  --device cuda

python scripts/run_a06_21_margin_budget_preservation_audit.py \
  --config configs/a06_21_margin_budget_preservation_audit.json \
  --run-name a06_21_margin_budget_full_20260629_1 \
  --aggregate-only
```

Logs copied to:

```text
logs/a06_21_margin_budget_full_20260629_1_shard0.log
logs/a06_21_margin_budget_full_20260629_1_shard1.log
```

## 3. Metric Definitions

**Feature NMI:** normalized mutual information between feature id and top-1
expert assignment.

**Matched preserve fraction:** fraction of tokens from each feature that still
route to the step-0 matched expert. This is stricter than NMI because it keeps
the original feature-to-expert identity fixed.

**Current margin:** for feature \(f\) and competitor \(e\),

\[
\gamma_{f,e}(t)=
\left(w_{a(f)}(t)-w_e(t)\right)^\top\mu_f(t).
\]

The summary reports the minimum over feature/competitor pairs.

**Sign flip:** whether a pairwise current margin is non-positive:

\[
\gamma_{f,e}(t)\leq 0.
\]

**Cluster-aware margin:** center margin minus a robust token-radius penalty:

\[
\tilde{\gamma}_{f,e}(t)
=
\gamma_{f,e}(t)-\|u_{f,e}(t)\|\rho_f^{0.95}(t).
\]

**Common share:** fraction of absolute margin contribution coming from the
common center term:

\[
\frac{|u^\top c|}{|u^\top c|+|u^\top r_f|+\epsilon}.
\]

**Actual consumption ratio:** \((\gamma(0)-\gamma(t))/|\gamma(0)|\). It is useful
only when the initial margin is a valid positive buffer. It is not the main
metric for random or label-shuffled guards, where the initial margin can
already be negative or close to zero.

## 4. Result Tables

### Step 5

| Condition | Feature NMI | Preserve frac min | Min margin | Sign flip | Cluster-aware margin | Common share | Max load |
|---|---:|---:|---:|---:|---:|---:|---:|
| Pseudo-center | 1.000 | 1.000 | 5.868 | 0.000 | 4.545 | 0.031 | 0.250 |
| Oracle-center | 1.000 | 1.000 | 5.882 | 0.000 | 4.537 | 0.031 | 0.250 |
| Random Gaussian | 0.816 | 0.162 | -0.678 | 0.182 | -1.949 | 0.343 | 0.483 |
| Equal-norm random | 0.808 | 0.140 | -0.671 | 0.187 | -1.936 | 0.339 | 0.488 |
| Label-shuffled center | 0.869 | 0.094 | -0.342 | 0.245 | -0.436 | 0.314 | 0.461 |

### Step 10

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

## 5. Correlation Audit

Feature NMI correlations across all rows:

| Metric | Correlation with feature NMI |
|---|---:|
| Sign flip rate | -0.611 |
| Current min margin | 0.595 |
| Cluster-aware margin | 0.629 |
| Common share | -0.721 |
| Max load | -0.869 |

At steps 5/10 only:

| Metric | Correlation with feature NMI |
|---|---:|
| Sign flip rate | -0.621 |
| Current min margin | 0.633 |
| Cluster-aware margin | 0.637 |
| Common share | -0.749 |
| Max load | -0.888 |

Interpretation: current margin, sign flips, and cluster-aware margin behave as
expected. Actual consumption ratio is not a stable cross-condition correlate
because negative or tiny initial margins in invalid guard conditions make the
ratio ill-conditioned.

## 6. Visualization Results

### Feature NMI Trajectory

![Feature NMI trajectory](figures/feature_nmi_trajectory.png)

Purpose: tests whether route assignments remain aligned with feature ids.

Observed result: pseudo-center and oracle-center remain at `1.0`; random and
equal-norm random stay around `0.82`; label-shuffled center stays around
`0.87`.

Take-home: feature NMI alone is not enough because label-shuffled center has
moderate NMI but does not preserve the intended matched expert identity.

### Current Margin Trajectory

![Current margin trajectory](figures/current_margin_trajectory.png)

Purpose: tests whether feature centers remain inside their matched expert
regions.

Observed result: pseudo-center and oracle-center keep positive current
margins; all guard conditions have negative margins.

Take-home: current margin is the clearest diagnostic of preservation in this
controlled bridge.

### Sign Flip Trajectory

![Sign flip trajectory](figures/sign_flip_rate_trajectory.png)

Purpose: tests whether pairwise margins cross zero.

Observed result: center-init conditions have zero sign flips; guards show
persistent sign flips.

Take-home: sign flips separate true preservation from moderately high NMI.

### Common Share Trajectory

![Common share trajectory](figures/common_share_trajectory.png)

Purpose: tests whether margins are dominated by common directions.

Observed result: center-init common share remains low; guard conditions are
higher.

Take-home: common share is a useful guard. It does not by itself prove common
overwrite because invalid guard conditions already lack positive margin.

### Final Drift Attribution

![Final drift attribution](figures/final_drift_attribution.png)

Purpose: decomposes negative margin pressure into router drift, feature-center
drift, and interaction drift.

Observed result: center-init negative pressure is dominated by feature-center
drift, but the current margin remains positive.

Take-home: router-center active tracking is unnecessary. Preservation means
the positive margin buffer survives drift.

### Debug Figure: Final NMI Versus Actual Consumption

![Final NMI versus actual consumption](figures/final_nmi_vs_actual_consumption.png)

This figure is kept as a debug plot. It should not be used as central
evidence because actual consumption ratio becomes ill-conditioned when the
initial margin is negative or close to zero.

## 7. Failure Decomposition

**Not a step-0 bridge failure for center init:** pseudo-center and oracle-center
start and remain clean.

**Not active tracking:** this audit inherits A06_02_01_E02; router rows do not need
to follow centers. A06_02_01_E06 adds that current margins remain positive despite
feature-center drift.

**Not norm-only:** label-shuffled center has center-like scale but negative
margin and poor matched preserve fraction.

**Common overwrite not established as cause in this bridge:** common share is
low in preserved center-init conditions. It is higher in guard conditions, but
those conditions are already invalid from step 0.

**Feature-center drift is real but not sufficient for collapse:** center-init
conditions show feature-drift negative pressure, yet margin stays positive and
sign flips stay zero.

## 8. Artifact Map

Project anchor:

```text
Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md
```

Protocol / result:

```text
Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_01_E06_margin_budget_audit/protocol.md
Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_01_E06_margin_budget_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_01_E06_margin_budget_audit/detailed.md
```

Code workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
```

Script and config:

```text
scripts/run_a06_21_margin_budget_preservation_audit.py
configs/a06_21_margin_budget_preservation_audit.json
```

Curated tables:

```text
tables/margin_budget_metrics_by_step.csv
tables/margin_budget_metric_aggregate.csv
tables/early_step_margin_budget_aggregate.csv
tables/final_condition_overall_aggregate.csv
tables/condition_final_margin_budget.csv
tables/condition_final_margin_budget_aggregate.csv
tables/drift_attribution_final.csv
tables/common_residual_final.csv
tables/snapshot_inventory.csv
```

Curated figures:

```text
figures/feature_nmi_trajectory.png
figures/current_margin_trajectory.png
figures/sign_flip_rate_trajectory.png
figures/common_share_trajectory.png
figures/final_drift_attribution.png
figures/actual_consumption_ratio_trajectory.png
figures/final_nmi_vs_actual_consumption.png
```

Raw output location:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_21_margin_budget_preservation_audit/a06_21_margin_budget_full_20260629_1
```

The 23,040-row pair-level table remains at that execution location under
`tables/margin_budget_by_pair.csv`, SHA-256
`44f3b496bc1abbf55a9ec2616f24ea5b77161226529a03029a7b18d79ee88ecd`.
Its byte-identical mainline copy was removed during the 2026-09-24 storage
cleanup; the aggregate tables above remain here.

## 9. Claim Boundary And Next Decision

Can claim:

- margin-budget diagnostics explain controlled center-init preservation;
- current margin, sign flip, and cluster-aware margin are useful preservation
  diagnostics;
- positive initial/current margin matters more than exact center equality.

Cannot claim:

- real-DCLM failure is explained;
- common subtraction is a fix;
- utility follows from NMI;
- semantic experts have been found.

Next decision:

Run the same margin-budget audit on real-DCLM proxy-init training. If A06_01_04_E03
did not save hidden-state and router-row vectors, rerun a minimal A06_01_04_E03
snapshot collection rather than a broad new method sweep.

---
experiment_id: A06_02_01_E03_feature_drift_margin
anchor_id: A06_02_01_E03_feature_drift_margin
status: completed
run_name: a06_17_03_feature_drift_margin_boundary_full_20260629_011201
job_id: local-two-gpu
canonical_language: en
---

# Detailed: A06_02_01_E03 Feature Drift Margin Boundary

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol:
`protocol.md`

Summary:
`summary.md`

## 0. Quick Recap

Purpose: quantify the observed margin boundary behind A06_02_01_E02 preservation.

Hypothesis: correct center initialization preserves routing because feature
centers drift within the initial expert-boundary safety buffer.

Experiment logic: rerun the A06_02_01_E02 bridge and compute per-feature
step-0 boundary distance, frozen-boundary consumption, dynamic margin, and
switch flags at every snapshot.

Conclusion: supported for the observed trajectory. Center-init runs consume
only part of the initial buffer and keep positive dynamic margins; random
guards show negative margin and switches.

## 1. Anchor Link And Decision Point

Decision question: do feature switches or margin failures occur when
feature-center drift consumes the initial distance to the nearest expert
boundary?

Decision after run: observed center-init preservation is inside the margin
buffer. The result supports using boundary consumption and dynamic margin as
future design metrics.

## 2. Protocol Compliance Audit

| Check | Status | Evidence |
| --- | --- | --- |
| Conditions | passed | pseudo, oracle, random |
| Cells | passed | C0-C3 |
| Seeds | passed | 20260623-20260630 |
| Snapshots | passed | 0, 1, 2, 5, 10, 20, 50, 100, 200, 400, 800, 1600 |
| Boundary metrics | passed | `boundary_by_step.csv` |
| Aggregate tables | passed | `boundary_metric_aggregate.csv`, `condition_final_boundary_aggregate.csv` |
| Figures | passed | six central PNGs |

## 3. Setup

Code workspace:
`../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding`

Runner:
`scripts/run_a06_17_03_feature_drift_margin_boundary.py`

Base config:
`configs/a06_17_02_router_center_tracking_preservation.json`

Run:
`a06_17_03_feature_drift_margin_boundary_full_20260629_011201`

Execution: local two-GPU run with two shards.

## 4. Metrics And Decision Rules

For each feature \(f\), the matched expert \(e(f)\) and nearest competitor
\(j^*(f)\) are fixed at step 0. The step-0 boundary normal is
\(n_f(0)=w_{e(f)}(0)-w_{j^*(f)}(0)\).

Initial boundary distance:

\[
d_f(0)=\frac{n_f(0)^\top \mu_f(0)}{\|n_f(0)\|+\epsilon}.
\]

Frozen-boundary distance:

\[
d_f^{\mathrm{frozen}}(t)=
\frac{n_f(0)^\top \mu_f(t)}{\|n_f(0)\|+\epsilon}.
\]

Boundary consumption:

\[
B_f(t)=1-\frac{d_f^{\mathrm{frozen}}(t)}{d_f(0)+\epsilon}.
\]

Dynamic margin:

\[
M_f(t)=\min_{j\neq e(f)}
(w_{e(f)}(t)-w_j(t))^\top \mu_f(t).
\]

Pass: preserved features have \(B_f(t)<1\), positive frozen distance, positive
dynamic margin, and no switch.

Fail: switches occur despite strongly positive frozen distance and dynamic
margin, or preserved routing holds with negative dynamic margin.

## 5. Main Results

Final-step aggregate over all C0-C3 cells and 8 seeds:

| Condition | Feature NMI mean | Feature NMI min | Boundary consumption max mean | Worst max consumption | Dynamic margin min mean | Worst dynamic margin | Dynamic switch rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Pseudo-center | 1.000 | 1.000 | 0.530 | 0.693 | 3.417 | 1.838 | 0.000 |
| Oracle-center | 1.000 | 1.000 | 0.523 | 0.691 | 3.573 | 2.312 | 0.000 |
| Random Gaussian | 0.783 | 0.000 | 21.697 | 376.255 | -3.646 | -4.662 | 0.375 |

Important detail: Euclidean drift ratio can exceed 1 in preserved center-init
runs. This does not contradict the boundary result because much of that drift
is not along the nearest-boundary normal. Signed boundary distance is the
decision metric.

Worst center-init cases still preserved:

- highest boundary consumption: 0.693;
- lowest frozen boundary distance: 2.405;
- lowest dynamic margin: 1.838;
- dynamic switch rate: 0.

## 6. Visualization Results

### Boundary Consumption Trajectory

![Boundary consumption trajectory](figures/boundary_consumption_trajectory.png)

Purpose: show whether observed drift consumes the initial boundary buffer.

Observed result: center-init runs stay below 1; random is unstable.

Take-home: preservation does not approach the frozen boundary in the observed
trajectory.

Remaining uncertainty: this does not test artificial perturbations beyond the
observed training drift.

### Dynamic Margin Trajectory

![Dynamic margin trajectory](figures/dynamic_margin_trajectory.png)

Purpose: check whether current router rows still give the matched feature a
positive margin.

Observed result: center-init runs keep positive margins; random guard has
negative margins.

Take-home: dynamic router geometry remains safe in center-init runs.

### Dynamic Switch Rate

![Dynamic switch rate](figures/dynamic_switch_rate_trajectory.png)

Purpose: detect actual feature-center expert switches.

Observed result: center-init switch rate remains zero; random has nonzero
switch rate.

Take-home: observed feature centers do not switch experts after correct center
initialization.

### Final Boundary Consumption Versus Margin

![Final boundary consumption versus margin](figures/final_boundary_consumption_vs_margin.png)

Purpose: relate final boundary consumption to final dynamic margin.

Observed result: center-init points stay in the positive-margin region.

Take-home: drift consumes part of the buffer but not enough to cross.

## 7. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | What this rules out |
| --- | --- | --- | --- |
| Positive control | center-init feature NMI 1.0 | passed | preservation failure in rerun |
| Boundary audit | max consumption below 0.70 for center-init | passed | observed drift crossing the step-0 boundary |
| Dynamic margin audit | worst center dynamic margin 1.838 | passed | hidden switch under current router |
| Random guard | negative margins and switch rate 0.375 | passed | task success as feature preservation |

Remaining rival explanations: feature-cloud tails may cross before centers.
This run audits feature centers only, not all within-feature points.

## 8. Full Experiment Record

Command pattern:

```bash
cd /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
RUN_NAME=a06_17_03_feature_drift_margin_boundary_full_20260629_011201
CUDA_VISIBLE_DEVICES=0 python scripts/run_a06_17_03_feature_drift_margin_boundary.py \
  --config configs/a06_17_02_router_center_tracking_preservation.json \
  --run-name "$RUN_NAME" --run-stage full --shard-index 0 --num-shards 2 --device cuda &
CUDA_VISIBLE_DEVICES=1 python scripts/run_a06_17_03_feature_drift_margin_boundary.py \
  --config configs/a06_17_02_router_center_tracking_preservation.json \
  --run-name "$RUN_NAME" --run-stage full --shard-index 1 --num-shards 2 --device cuda &
wait
python scripts/run_a06_17_03_feature_drift_margin_boundary.py \
  --config configs/a06_17_02_router_center_tracking_preservation.json \
  --run-name "$RUN_NAME" --run-stage full --num-shards 2 --aggregate-only --device cpu
```

Raw logs remain in the code workspace:

- `logs/local/a06_17_03_feature_drift_margin_boundary_full_20260629_011201_shard0.log`
- `logs/local/a06_17_03_feature_drift_margin_boundary_full_20260629_011201_shard1.log`
- `logs/local/a06_17_03_feature_drift_margin_boundary_full_20260629_011201_aggregate.log`

## 9. Interpretation

A06_02_01_E03 sharpens A06_02_01_E02. A06_02_01_E02 said preservation was not active
tracking and was better explained by positive margin. A06_02_01_E03 now says the
observed feature-center drift does not exhaust that margin. Even the worst
preserved feature keeps substantial signed distance and positive dynamic
margin.

This means the preservation mechanism can be stated geometrically:

```text
correct center init -> large step-0 boundary buffer -> observed drift consumes
only part of buffer -> no center switch
```

## 10. Claim Boundary

Can claim: observed controlled bridge preservation is consistent with
margin-buffer geometry.

Cannot claim: exact maximum perturbation tolerance, within-feature tail safety,
real-DCLM behavior, expert utility, or semantic specialization.

## 11. Next Decision

Use initial boundary distance and dynamic margin as gates for future
label-free center search. A candidate center set should not advance to
training preservation unless it gives sufficient positive boundary buffer.

## 12. Links And Artifact Map

anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

protocol:
`protocol.md`

summary:
`summary.md`

runner:
`../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_17_03_feature_drift_margin_boundary.py`

key tables:

- `tables/boundary_by_step.csv`
- `tables/boundary_metrics_by_step.csv`
- `tables/boundary_metric_aggregate.csv`
- `tables/condition_final_boundary_aggregate.csv`

figures:

- `figures/boundary_consumption_trajectory.png`
- `figures/dynamic_margin_trajectory.png`
- `figures/dynamic_switch_rate_trajectory.png`
- `figures/final_boundary_consumption_vs_margin.png`

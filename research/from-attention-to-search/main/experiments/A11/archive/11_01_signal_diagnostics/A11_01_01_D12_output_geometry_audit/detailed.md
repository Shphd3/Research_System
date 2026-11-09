# A11_08b Output-Geometry Dynamics Audit Detailed Report

## 0. Quick Recap

Purpose: test whether A11_08's output-row geometry is only a step-0 construction or remains explanatory during early training.

Hypothesis: if output geometry is a hidden-update mechanism, freezing output heads should preserve the `aligned_h3_h4` greater than `low_conflict_h3_h4` separation in hidden semantic velocity.

Experiment idea: run the same A11_08 clean decision-only K=4 setup with two variants, `trainable_heads` and `frozen_heads`, and record output geometry, head drift, hidden velocity, margins, guarded recovery, and local guards over time.

Conclusion: supported for hidden semantic velocity. Frozen heads preserve the aligned greater than low/conflict gap in 5/5 seeds. Trainable heads drift, so training curves require current-geometry interpretation.

Evidence: frozen early AUC `G_hidden_ref` is `0.002660` for aligned and `0.000184` for low/conflict; shared-only is `0`, single-h3 is positive; final Y1/Y2 accuracy is `1.0/1.0`.

## 1. Protocol Compliance

| Requirement | Status | Evidence |
| --- | --- | --- |
| clean `tau=3` / general-K decision-only setup | pass | config uses `general_k_readout_margin`, `decision_only` |
| seeds 971-975 | pass | run manifest and tables |
| conditions: shared, single, aligned, low/conflict | pass | all present |
| variants: trainable heads and frozen heads | pass | `head_variant` column |
| no broader ablation | pass | only required conditions and variants |
| output geometry over time | pass | `cos_34`, `head_drift` in `curve_metrics.csv` |
| current/ref hidden velocity | pass | `G_hidden_current`, `G_hidden_ref` |
| current/ref margins | pass | `M_Z_current`, `M_Z_ref` |
| guarded recovery | pass | `Q_eval` |
| Y1/Y2 local guards | pass | `Y1/Y2_loss`, `Y1/Y2_accuracy` |

## 2. Metric Definitions

Reference direction:

$$
v_z^{ref}=v_z^{cur}(0).
$$

Current direction:

$$
v_z^{cur}(t)=\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}(t)-\bar u_j(t)).
$$

Hidden velocities:

$$
G_{ref}^{hidden}(t)=\frac1m\sum_z v_z^{ref\top}(-\nabla_{h_z}L_K(t)),
$$

$$
G_{current}^{hidden}(t)=\frac1m\sum_z v_z^{cur}(t)^\top(-\nabla_{h_z}L_K(t)).
$$

Margins:

$$
M_Z^{ref}(t)=\frac1m\sum_z v_z^{ref\top}h_z(t),
$$

$$
M_Z^{current}(t)=\frac1m\sum_z v_z^{cur}(t)^\top h_z(t).
$$

Output cosine:

$$
\cos_{34}(t)=\frac1m\sum_z
\cos(u_{S_z}^{(3)}(t)-\bar u_3(t),u_{T_z}^{(4)}(t)-\bar u_4(t)).
$$

Head drift:

$$
D_u(t)=\left(\sum_{j,z}\|u_z^{(j)}(t)-u_z^{(j)}(0)\|^2\right)^{1/2}.
$$

Guarded recovery:

$$
Q_{eval}(t)=\min\{A_{decoder}(t),A_{probe}(t),C_{swap}(t)\}.
$$

## 3. Results

### 3.1 One-Step Guard

At step 0, both trainable and frozen variants reproduce the A11_08 geometry:

| Condition | `G_pred_batch_scaled` | `G_hidden` |
| --- | ---: | ---: |
| `shared_only_k4` | 0.000000 | 0.000000 |
| `single_h3` | 0.003816 | 0.003816 |
| `aligned_h3_h4` | 0.015262 | 0.015262 |
| `low_conflict_h3_h4` | 0.000954 | 0.000954 |

This confirms that the audit starts from the intended geometry.

### 3.2 Frozen-Head Dynamics

| Condition | early AUC `G_hidden_ref` | early AUC `M_Z_ref` | final `M_Z_ref` | final `Q` |
| --- | ---: | ---: | ---: | ---: |
| `shared_only_k4` | 0.000000 | 0.000 | 0.000 | 0.250 |
| `single_h3` | 0.000783 | 0.758 | 1.198 | 0.400 |
| `aligned_h3_h4` | 0.002660 | 3.238 | 5.189 | 0.500 |
| `low_conflict_h3_h4` | 0.000184 | 0.128 | 0.180 | 0.500 |

Per-seed aligned greater than low/conflict:

| Metric | Count |
| --- | ---: |
| early AUC `G_hidden_ref` | 5 / 5 |
| early AUC `G_hidden_current` | 5 / 5 |
| early AUC `M_Z_ref` | 2 / 5 |
| final `M_Z_ref` | 3 / 5 |
| final `Q` | 0 / 5 |

Interpretation: the primary velocity mechanism is stable across seeds. Margin and final recovery are secondary and less stable.

### 3.3 Trainable-Head Dynamics

| Condition | `cos_34(0)` | `cos_34(2000)` | `D_u(2000)` | final `M_Z_ref` | final `M_Z_current` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `aligned_h3_h4` | 1.000 | 1.000 | 1.862 | 2.923 | 6.993 |
| `low_conflict_h3_h4` | -1.000 | -0.268 | 2.194 | 0.487 | 6.532 |

Interpretation: low/conflict does not become fully aligned, but the output heads move substantially. Current-geometry margin can become large even when reference margin stays small.

## 4. Visualization Results

No standalone figure is required for this audit. The central evidence is tabular and lives in:

```text
tables/condition_summary.csv
tables/efficiency_by_seed.csv
tables/curve_metrics.csv
```

How to read the main table: compare `aligned_h3_h4` against `low_conflict_h3_h4` within the same `head_variant`. The decisive row is frozen-head early AUC `G_hidden_ref/current`.

## 5. Decision

Supported:

```text
In controlled clean decision-only training, output-row geometry remains an
effective hidden semantic velocity mechanism when output heads are frozen.
```

Not supported:

```text
Every seed shows stronger final Q or final margin for aligned.
Trainable-head training curves can be explained by initial geometry alone.
```

## 6. Artifact Map

```text
code workspace:
  /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments
runner:
  active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py
config:
  active/synthetic_data_understanding/configs/a11_08b_output_geometry_dynamics_audit.json
submit script:
  active/synthetic_data_understanding/scripts/submit_a11_03_04_semantic_efficiency_4gpu.sh
job id:
  pt-yppwndnm
run name:
  a11_08b_output_geometry_dynamics_full_20260709_1225
result dir:
  active/synthetic_data_understanding/results/a11_08b_output_geometry_dynamics_audit/a11_08b_output_geometry_dynamics_full_20260709_1225
log dir:
  active/synthetic_data_understanding/logs/acp/a11_08b_output_geometry_dynamics_full_20260709_1225
primary tables:
  tables/condition_summary.csv
  tables/efficiency_by_seed.csv
  tables/one_step_summary.csv
  tables/output_geometry.csv
```

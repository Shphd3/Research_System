# A11_08b Output-Geometry Dynamics Audit Summary

## Conclusion

A11_08b supports the hidden-velocity mechanism behind A11_08, with an important boundary. With frozen output heads, `aligned_h3_h4` keeps a much larger hidden semantic velocity than `low_conflict_h3_h4` across 5/5 seeds. Therefore the A11_08 geometry result is not only a step-0 artifact for the primary velocity metric.

The boundary is that trainable heads drift substantially. In the trainable `low_conflict_h3_h4` condition, `cos_34` moves from `-1.000` to `-0.268`, and current-geometry margin becomes large. Thus trainable learning curves must be interpreted with current output geometry recorded; initial geometry alone is not enough for curve-level claims.

## Terminology / Definitions

| Metric | Formula | Measures | Decision role | Cannot prove |
| --- | --- | --- | --- | --- |
| Output cosine `cos_34(t)` | $$\frac1m\sum_z \cos(u_{S_z}^{(3)}(t)-\bar u_3(t),u_{T_z}^{(4)}(t)-\bar u_4(t))$$ | whether horizon-3 and horizon-4 semantic rows are aligned or conflicting | detects head-geometry repair | hidden information by itself |
| Head drift `D_u(t)` | $$\left(\sum_{j,z}\|u_z^{(j)}(t)-u_z^{(j)}(0)\|^2\right)^{1/2}$$ | output-row movement from initialization | separates static geometry from co-adaptation | whether hidden state learned |
| Reference hidden velocity `G_hidden_ref(t)` | $$\frac1m\sum_z v_z^{ref\top}(-\nabla_{h_z}L_K(t))$$ | loss-gradient movement along the initial A11_08 semantic direction | primary mechanism metric | final recovery |
| Current hidden velocity `G_hidden_current(t)` | $$\frac1m\sum_z v_z^{cur}(t)^\top(-\nabla_{h_z}L_K(t))$$ | loss-gradient movement along current output geometry | tests current-head supervision | initial-geometry causality |
| Reference margin `M_Z_ref(t)` | $$\frac1m\sum_z v_z^{ref\top}h_z(t)$$ | accumulated hidden signal in the initial direction | secondary dynamics metric | stable recovery in every seed |
| Current margin `M_Z_current(t)` | $$\frac1m\sum_z v_z^{cur}(t)^\top h_z(t)$$ | accumulated hidden signal in current geometry | detects co-adapted readout | initial mechanism alone |
| Guarded recovery `Q_eval(t)` | $$\min\{A_{decoder}(t),A_{probe}(t),C_{swap}(t)\}$$ | conservative branch recovery | secondary recovery metric | direct supervision alone |
| Y1/Y2 local guard | CE and accuracy on `A_SHARED`, `C_SHARED` | local next-token quality | rules out local damage | full LM quality |

## Setup

```text
run name: a11_08b_output_geometry_dynamics_full_20260709_1225
job id: pt-yppwndnm
scope: clean decision-only
K: 4
conditions: shared_only_k4, single_h3, aligned_h3_h4, low_conflict_h3_h4
variants: trainable_heads, frozen_heads
seeds: 971, 972, 973, 974, 975
steps: 2000
eval every: 100
```

## Main Results

Frozen-head early dynamics:

| Condition | early AUC `G_hidden_ref` | early AUC `M_Z_ref` | early AUC `Q` | final `M_Z_ref` | final `Q` | final Y1/Y2 acc |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `shared_only_k4` | 0.000000 | 0.000 | 0.250 | 0.000 | 0.250 | 1.0 / 1.0 |
| `single_h3` | 0.000783 | 0.758 | 0.392 | 1.198 | 0.400 | 1.0 / 1.0 |
| `aligned_h3_h4` | 0.002660 | 3.238 | 0.478 | 5.189 | 0.500 | 1.0 / 1.0 |
| `low_conflict_h3_h4` | 0.000184 | 0.128 | 0.428 | 0.180 | 0.500 | 1.0 / 1.0 |

Seed support:

```text
frozen early_AUC_G_hidden_ref: aligned > low/conflict in 5 / 5 seeds
frozen early_AUC_G_hidden_current: aligned > low/conflict in 5 / 5 seeds
frozen early_AUC_M_Z_ref: aligned > low/conflict in 2 / 5 seeds
frozen final_Q: aligned > low/conflict in 0 / 5 seeds
```

Output geometry dynamics:

| Variant | Condition | `cos_34(0)` | `cos_34(2000)` | `D_u(2000)` |
| --- | --- | ---: | ---: | ---: |
| frozen | `aligned_h3_h4` | 1.000 | 1.000 | 0.000 |
| frozen | `low_conflict_h3_h4` | -1.000 | -1.000 | 0.000 |
| trainable | `aligned_h3_h4` | 1.000 | 1.000 | 1.862 |
| trainable | `low_conflict_h3_h4` | -1.000 | -0.268 | 2.194 |

## Judgment

Supported:

```text
Frozen-head output geometry remains an effective mechanism for hidden semantic
velocity. The A11_08 aligned-versus-low/conflict separation is not merely a
trainable-head step-0 artifact.
```

Boundary:

```text
Final Q and margin are not seed-stable enough to claim universal faster
recovery. Trainable-head curves must be interpreted through current geometry
because output rows drift, especially in low/conflict.
```

Next decision:

```text
Proceed to A11_09 next-K inclusion law using frozen heads as the clean theorem
test surface.
```

## Artifacts

```text
config: Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a11_08b_output_geometry_dynamics_audit.json
result dir: Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_08b_output_geometry_dynamics_audit/a11_08b_output_geometry_dynamics_full_20260709_1225
main tables:
  tables/condition_summary.csv
  tables/efficiency_by_seed.csv
  tables/one_step_summary.csv
  tables/output_geometry.csv
  tables/general_k_falsifier_summary.csv
```

# Protocol: A11_01_01_E01 Next-K Inclusion Law

## 0. Approval Snapshot

Approval status: approved by user on 2026-07-09 for immediate execution after 11_08b.

Purpose: test whether next-K semantic velocity turns on when K first includes an informative future target and whether adding another informative target changes velocity by the predicted vector increment.

Primary anchor: `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_01_informative_horizon_supervision/subanchors/11_01_01_information_and_geometry_controls_anchor.md`.

Experiment role: minimal theorem-mechanism test after the 11_08b output-geometry dynamics audit. This is not a broader K sweep.

## 1. Setup

Use the A11_08 clean decision-only construction with frozen prediction heads:

```text
seeds: 971, 972, 973, 974, 975
objective scope: decision_only
head variant: frozen_heads
conditions: K2_active, K3_active, K4_active
data regimes: shared_only_k4, single_h3, aligned_h3_h4, low_conflict_h3_h4
```

K conditions:

```text
K2_active: active horizons [1, 2]
K3_active: active horizons [1, 2, 3]
K4_active: active horizons [1, 2, 3, 4]
```

## 2. Metrics

Informative horizon set:

$$
\mathcal I_K=\{j\le K:Y_j\text{ is a one-to-one code of }Z\}.
$$

Aggregate semantic direction:

$$
v_z^{(K)}=\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j).
$$

Primary hidden semantic velocity:

$$
G_K^{hidden}(t)=\frac1m\sum_z v_z^{(K)\top}(-\nabla_{h_z}L_K(t)).
$$

Readout margins:

$$
M_Z^{ref/current}(t)=\frac1m\sum_z v_z^{ref/current}(t)^\top h_z(t).
$$

Guarded recovery:

$$
Q_{eval}(t)=\min\{A_{decoder}(t),A_{probe}(t),C_{swap}(t)\}.
$$

Local guards: Y1/Y2 cross-entropy loss and accuracy.

## 3. Falsifiable Predictions

| Hypothesis | Comparison | Support | Weakens |
| --- | --- | --- | --- |
| K below informative horizon is zero | `single_h3`: K2 | `G_hidden` near zero | stable positive signal |
| first informative horizon turns on | `single_h3`: K3 > K2 | positive gap in `G_hidden` and `M_Z` | no gap |
| uninformative added horizon adds no semantic increment | `single_h3`: K4 approx K3 | small K4-K3 gap | large unexplained increase |
| aligned second informative horizon amplifies | `aligned_h3_h4`: K4 > K3 | positive vector increment | no increase |
| low/conflict second horizon weakens | `low_conflict_h3_h4`: K4 increment below aligned | aligned K4-K3 > low/conflict K4-K3 | low/conflict matches aligned |
| shared-only guard | `shared_only_k4`: all K | near-zero semantic metrics | leakage / metric contamination |

## 4. Required Outputs

```text
curve_metrics.csv
condition_summary.csv
efficiency_by_seed.csv
one_step_metrics.csv
one_step_summary.csv
output_geometry.csv
general_k_falsifier_summary.csv
local_loss_guard_summary.csv
run_manifest.json
```

## 5. Decision Boundary

Can decide: whether controlled frozen-head decision-prefix dynamics obey the next-K inclusion law.

Cannot decide: natural-language MTP benefit, all-position indirect transfer, MoE route utility, or universal monotonicity of K.

# A11_01_01_E01 Next-K Inclusion Law Detailed Report

## 0. Quick Recap

Purpose: test whether increasing K changes direct semantic velocity only when the newly included horizon is informative.

Hypothesis: K below the first informative horizon gives zero semantic velocity; K at the first informative horizon turns on; adding an uninformative horizon gives no direct semantic increment; adding an informative horizon changes velocity by the vector increment.

Experiment idea: run K2/K3/K4 under frozen-head clean decision-only training on four regimes: shared-only, single informative H3, aligned H3+H4, and low/conflict H3+H4.

Conclusion: supported for one-step hidden semantic velocity. Curve metrics are consistent for aligned and low/conflict, but multi-step recovery remains secondary and non-monotonic.

Evidence: one-step `G_hidden` is `0, 0.003816, 0.003816` for single-H3; `0, 0.003816, 0.015262` for aligned H3+H4; `0, 0.003816, 0.000954` for low/conflict H3+H4.

## 1. Protocol Compliance

| Requirement | Status | Evidence |
| --- | --- | --- |
| compare K2/K3/K4 | pass | conditions `K2_active`, `K3_active`, `K4_active` |
| clean decision-only | pass | config objective scope |
| frozen heads after 11_08b | pass | `head_variant=frozen_heads` |
| seeds 971-975 | pass | run manifest and tables |
| no broader ablation | pass | only required regimes and K values |
| output geometry and hidden velocity recorded | pass | `curve_metrics.csv`, `one_step_summary.csv` |
| local Y1/Y2 guards | pass | final Y1/Y2 accuracy is 1.0 |

## 2. Metric Definitions

Informative horizon set:

\[
\mathcal I_K=\{j\le K:Y_j\text{ one-to-one encodes }Z\}.
\]

Aggregate direction:

\[
v_z^{(K)}=\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j).
\]

Hidden semantic velocity:

\[
G_K^{hidden}=\frac1m\sum_z v_z^{(K)\top}(-\nabla_{h_z}L_K).
\]

Predicted vector increment:

\[
G_{K+1}-G_K=
\frac1{m^2}\sum_z(2v_z^{(K)\top}a_{K+1,z}+\|a_{K+1,z}\|^2).
\]

Readout margin:

\[
M_Z=\frac1m\sum_z v_z^\top h_z.
\]

Guarded recovery:

\[
Q_{eval}=\min\{A_{decoder},A_{probe},C_{swap}\}.
\]

## 3. One-Step Evidence

At `eta=0.0003`:

| Regime | K2 `G_hidden` | K3 `G_hidden` | K4 `G_hidden` | K3-K2 | K4-K3 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `shared_only_k4` | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `single_h3` | 0.000000 | 0.003816 | 0.003816 | 0.003816 | -0.000000 |
| `aligned_h3_h4` | 0.000000 | 0.003816 | 0.015262 | 0.003816 | 0.011447 |
| `low_conflict_h3_h4` | 0.000000 | 0.003816 | 0.000954 | 0.003816 | -0.002862 |

Per-seed direction:

| Regime | Comparison | Positive seeds | Meaning |
| --- | --- | ---: | --- |
| `single_h3` | K3-K2 | 5 / 5 | first informative horizon turns on |
| `single_h3` | K4-K3 | 0 / 5 | shared H4 adds no increment |
| `aligned_h3_h4` | K4-K3 | 5 / 5 | aligned informative H4 amplifies |
| `low_conflict_h3_h4` | K4-K3 | 0 / 5 | low/conflict informative H4 weakens |

## 4. Curve Evidence

| Regime | Condition | early AUC `G_hidden_ref` | early AUC `M_Z_ref` | early AUC `Q` | final `G_hidden_ref` | final `M_Z_ref` | final `Q` |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `shared_only_k4` | K2 | 0.000000 | 0.000 | 0.250 | 0.000000 | 0.000 | 0.250 |
| `shared_only_k4` | K3 | 0.000000 | 0.000 | 0.250 | 0.000000 | 0.000 | 0.250 |
| `shared_only_k4` | K4 | 0.000000 | 0.000 | 0.250 | 0.000000 | 0.000 | 0.250 |
| `single_h3` | K2 | 0.000000 | 0.000 | 0.250 | 0.000000 | 0.000 | 0.250 |
| `single_h3` | K3 | 0.000666 | 1.397 | 0.475 | 0.000527 | 2.771 | 0.550 |
| `single_h3` | K4 | 0.000783 | 0.758 | 0.392 | 0.000738 | 1.198 | 0.400 |
| `aligned_h3_h4` | K4 | 0.002660 | 3.238 | 0.478 | 0.002414 | 5.189 | 0.500 |
| `low_conflict_h3_h4` | K4 | 0.000184 | 0.128 | 0.428 | 0.000151 | 0.180 | 0.500 |

Curve interpretation:

```text
The one-step inclusion law is the clean decision evidence. Multi-step curves
can be affected by extra shared losses even when they add no direct semantic
direction. Therefore final Q and margin are secondary.
```

## 5. Visualization Results

No standalone figure is required. The central evidence is the one-step and curve tables:

```text
tables/one_step_summary.csv
tables/one_step_metrics.csv
tables/condition_summary.csv
tables/efficiency_by_seed.csv
```

How to read the main table: read each row left to right as K increases. A valid inclusion law has zero before informative coverage, a positive turn-on at first coverage, no increment for shared added horizons, and direction-dependent increment for second informative horizons.

## 6. Hypothesis Updates

| Hypothesis | Verdict | Update |
| --- | --- | --- |
| K < tau gives near-zero direct semantic velocity | supported | K2 is zero in `single_h3` and all shared-only cases |
| K = tau turns on semantic velocity | supported | K3-K2 positive in 5/5 seeds |
| added uninformative horizon gives no direct semantic increment | supported for one-step velocity | `single_h3` K4-K3 is zero |
| added informative horizon follows vector increment | supported | aligned increment positive; low/conflict increment negative |
| larger K is the causal object | weakened | same K size can help, do nothing, or hurt depending on information and direction |

## 7. Claim Boundary

Can claim:

```text
Controlled frozen-head decision-only next-K prediction obeys a direct semantic
velocity inclusion law.
```

Cannot claim:

```text
Natural-language MTP benefit.
All-position indirect transfer obeys this clean law.
Final recovery Q is monotonic in K.
K larger is universally better or universally worse.
```

## 8. Artifact Map

```text
code workspace:
  /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments
runner:
  active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py
config:
  active/synthetic_data_understanding/configs/a11_09_next_k_inclusion_law.json
submit script:
  active/synthetic_data_understanding/scripts/submit_a11_03_04_semantic_efficiency_4gpu.sh
job id:
  pt-9an690sp
run name:
  a11_09_next_k_inclusion_law_full_20260709_1228
result dir:
  active/synthetic_data_understanding/results/a11_09_next_k_inclusion_law/a11_09_next_k_inclusion_law_full_20260709_1228
log dir:
  active/synthetic_data_understanding/logs/acp/a11_09_next_k_inclusion_law_full_20260709_1228
primary tables:
  tables/one_step_summary.csv
  tables/one_step_metrics.csv
  tables/condition_summary.csv
  tables/efficiency_by_seed.csv
  tables/output_geometry.csv
```

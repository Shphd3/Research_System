# Detailed Record: H0604a Feature-Key Routing Stability Center-Only

## 0. Quick Recap

目的：

检查同一个具体 feature key \((slot_id,b_id)\) 是否稳定 route 到同一个 expert。

假设：

如果 router 学到 feature-key-stable routing，则同一 \((s,i)\) 的多个 eval variants 应满足 \(\max_e P(e\mid s,i)\) 接近 1。

实验思路：

复用 05_01 uniform multi-B synthetic 和 H0603 center-only 条件，不加入 `Feature Separation Objective`，不加入 supervised token margin。比较 random init / slot init / center separation only，并用 expert load entropy 排除 collapse false positive。

结论：

H0604a supports the advisor's weak toy claim: under the operational feature key \((slot_id,b_id)\), same-feature route consistency is high across conditions. FeatureKeyConsistency is near 0.99 even in random NTP-only baselines.

This is not enough for specialization. FeatureKeyConsistency does not distinguish non-collapsed specialization from deterministic lock-in or collapse. Center separation only has no decisive independent gain; `S0-dot` equals `S1-dot` and `S0-cos` equals `S1-cos` on the compact metrics.

证据：

S1-cos 的平均 FeatureKeyConsistency 为 0.9991，但 seed `20260522` 的 load entropy norm 为 0、max load 为 1.0000。R0-dot/R1-dot 也出现 single-expert collapse seed。高 consistency 不能单独支持 specialization。

Filtered non-collapse read:

Dropping collapse / near-collapse seeds, `S0-cos` and `S1-cos` are the best slot-aligned conditions, but they remain identical. This supports cosine router + slot init as the strongest current non-collapsed route structure, not center separation as an independent mechanism.

## 1. Run Identity

Job:

```text
pt-8o1hoskg
display name: ats-h0604a-feature-key-4gpu
status: SUCCEEDED
```

Run name:

```text
h0604a_feature_key_routing_stability_4gpu_20260603
```

Code workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
```

Runner:

```text
scripts/run_h0604a_feature_key_routing_stability.py
```

Config:

```text
configs/h0604a_feature_key_routing_stability_center_only.json
```

Runtime log:

```text
logs/acp/h0604a_feature_key_routing_stability_4gpu_20260603_runtime_20260603_162533.log
```

Raw result dir:

```text
results/h0604a_feature_key_routing_stability_center_only/h0604a_feature_key_routing_stability_4gpu_20260603/
```

Raw figure dir:

```text
figures/h0604a_feature_key_routing_stability_center_only/h0604a_feature_key_routing_stability_4gpu_20260603/
```

Curated result dir:

```text
Projects/from-attention-to-search/main/experiments/H0604a_feature_key_routing_stability_center_only/
```

## 2. Data / Model / Training

Base data:

```text
uniform multi-B synthetic
slots = 4
B identities = 256
feature keys = 4 * 256 = 1024
sequence = [r_start, C_s, B_i, Y_{s,i}, r_end]
```

Feature key:

\[
f=(s,i)=(slot\_id,b\_id)
\]

Eval variants:

```text
variants_per_key = 16
variant_positions = [0, 6, 24, 31]
nuisance_tokens = [1300, 1301, 1302, 1303, 1304, 1305, 1306, 1307]
```

Each variant preserves `slot_id`, `b_id`, and target \(Y_{s,i}\).

Model:

```text
SparseTinyTransformer
d_model = 128
n_heads = 4
ffn_dim = 256
num_experts = 4
router bias = False
```

Training:

```text
steps = 1600
batch_size = 384
seeds = 20260521, 20260522, 20260523
lr = 0.0008
weight_decay = 0.01
grad_clip = 1.0
```

Feature-key checkpoints:

```text
step 0
step 800
step 1600
```

## 3. Conditions

| Code | Router | Init | Extra loss | 05_01 equivalent |
|---|---|---|---|---|
| R0-dot | dot | random | NTP only | C0 |
| R1-dot | dot | random | center separation only | D0 |
| S0-dot | dot | slot init | NTP only | C1 |
| S1-dot | dot | slot init | center separation only | D1 |
| R0-cos | cosine | random | NTP only | C3 |
| R1-cos | cosine | random | center separation only | K0 |
| S0-cos | cosine | slot init | NTP only | C4 |
| S1-cos | cosine | slot init | center separation only | K1 |

No condition uses feature separation objective or supervised token margin.

## 4. Primary Metric And Collapse Guard

Primary metric:

\[
\mathrm{consistency}(s,i)=\max_e P(e\mid s,i)
\]

Aggregate:

\[
\mathrm{FeatureKeyConsistency}
=
\frac{1}{|\mathcal{F}|}
\sum_{(s,i)}
\max_e P(e\mid s,i)
\]

Collapse guard:

\[
P(e)=\frac{1}{|\mathcal{F}|R}\sum_{s,i,r}\mathbf{1}[\mathrm{route}(s,i,r)=e]
\]

Report normalized expert-load entropy:

\[
H(E)/\log E
\]

Interpretation rule:

High FeatureKeyConsistency with low load entropy is collapse, not specialization.

## 5. Decision Metrics

Compact table:

```text
tables/h0604a_decision_metrics_compact.csv
```

| Condition | FKC mean | FKC >= .95 | Load H norm mean | Load H norm min | Max load max | Route-slot NMI | Route-B NMI | Target acc |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| R0-dot | 0.9987 | 0.9948 | 0.3796 | 0.0000 | 1.0000 | 0.3456 | 0.0326 | 0.9968 |
| R1-dot | 0.9982 | 0.9925 | 0.3413 | 0.0000 | 1.0000 | 0.2975 | 0.0427 | 0.9976 |
| S0-dot | 0.9942 | 0.9733 | 0.5386 | 0.1131 | 0.9711 | 0.4516 | 0.0680 | 0.9989 |
| S1-dot | 0.9942 | 0.9733 | 0.5386 | 0.1131 | 0.9711 | 0.4516 | 0.0680 | 0.9989 |
| R0-cos | 0.9945 | 0.9727 | 0.4643 | 0.2701 | 0.8762 | 0.3132 | 0.0984 | 0.9983 |
| R1-cos | 0.9889 | 0.9528 | 0.4670 | 0.2614 | 0.8823 | 0.3182 | 0.0909 | 0.9952 |
| S0-cos | 0.9991 | 0.9964 | 0.5796 | 0.0000 | 1.0000 | 0.5711 | 0.0102 | 0.9999 |
| S1-cos | 0.9991 | 0.9964 | 0.5796 | 0.0000 | 1.0000 | 0.5711 | 0.0102 | 0.9999 |

Observation:

FeatureKeyConsistency is high for every condition. Center separation only does not improve over the corresponding NTP-only baseline:

- S1-dot equals S0-dot on the compact metrics.
- S1-cos equals S0-cos on the compact metrics.
- R1-dot is not better than R0-dot.
- R1-cos is not better than R0-cos.

Interpretation:

The main hypothesis is weakened. Stable routing for the same \((s,i)\) is too easy to satisfy in this setup and does not imply feature-level specialization.

## 5.1 Non-Collapse Filtered Read

Collapse / near-collapse filter used for interpretation:

```text
active_experts > 1
expert_load_max_fraction < 0.95
expert_load_entropy_norm >= 0.2
```

Filtered result:

| Condition | Kept seeds | FeatureKeyConsistency | Load entropy norm | Max load | Feature route-slot NMI | Target acc |
|---|---:|---:|---:|---:|---:|---:|
| R0-dot | 2/3 | 0.9981 | 0.5694 | 0.5925 | 0.5183 | 0.9998 |
| R1-dot | 2/3 | 0.9973 | 0.5120 | 0.6440 | 0.4462 | 1.0000 |
| S0-dot | 2/3 | 0.9948 | 0.7513 | 0.5514 | 0.6355 | 0.9995 |
| S1-dot | 2/3 | 0.9948 | 0.7513 | 0.5514 | 0.6355 | 0.9995 |
| R0-cos | 3/3 | 0.9945 | 0.4643 | 0.6680 | 0.3132 | 0.9983 |
| R1-cos | 3/3 | 0.9889 | 0.4670 | 0.6360 | 0.3182 | 0.9952 |
| S0-cos | 2/3 | 0.9986 | 0.8694 | 0.4067 | 0.8566 | 0.9998 |
| S1-cos | 2/3 | 0.9986 | 0.8694 | 0.4067 | 0.8566 | 0.9998 |

Interpretation:

1. same-feature consistency remains high after collapse filtering;
2. `S0-cos` / `S1-cos` are the best non-collapsed slot-aligned conditions;
3. `S1-cos` does not improve over `S0-cos`, so center separation has no independent gain here;
4. feature-key consistency is a weak consistency result, not functional specialization.

## 5.2 Hypothesis-To-Evidence Map

| Hypothesis / rival | Primary artifact | Deciding metric | What the artifact can explain | What it cannot claim |
|---|---|---|---|---|
| H1: same operational feature routes to one expert | `figures/feature_key_consistency_histogram.png`; `tables/feature_key_consistency_by_condition.csv` | FeatureKeyConsistency; fraction of keys with \(\max_e P(e\mid f)\ge 0.95\) | Whether each feature key \((slot_id,b_id)\) has a stable main expert | Functional specialization, non-collapse, or expert utility |
| Rival R1: high consistency is collapse | `figures/expert_load_distribution.png`; `tables/expert_load_by_seed.csv` | expert-load entropy norm; max load fraction; active experts | Whether high consistency is all-to-one or near-all-to-one routing | Which feature axis explains non-collapsed routing |
| H2: center separation only has independent gain | `tables/h0604a_decision_metrics_compact.csv`; S0/S1 and R0/R1 pairs | difference between center-only and NTP-only under same router/init | Whether center separation improves routing beyond baseline | Whether another anti-collapse or assignment-discovery objective could work |
| H3: cosine + slot init is the best current non-collapsed structure | filtered table in Section 5.1; `figures/route_slot_heatmap_step0_final.png` | filtered route-slot NMI; load entropy; max load | Which condition gives the clearest valid slot-aligned routing | Utility binding or real-data robustness |
| R2: stable feature assignment is only checkpoint lock-in | `figures/checkpoint_feature_drift.png`; `tables/checkpoint_feature_drift.csv` | main-expert drift from step 0/mid/final | Whether feature main experts keep changing during training | Whether the stable final map is a useful specialization |
| Open: routed feature is slot, \(B_i\), or \((slot,B_i)\) | next feature-axis audit on route logs | NMI(route; slot), NMI(route; B_i), NMI(route; slot+B_i), per-expert composition | Which operational feature the router binds to | Route-utility binding before the feature axis is fixed |

## 6. Seed-Level Collapse Cases

Important seed-level observations:

| Condition | Seed | FeatureKeyConsistency | Load entropy norm | Max load | Interpretation |
|---|---:|---:|---:|---:|---|
| R0-dot | 20260522 | 1.0000 | 0.0000 | 1.0000 | single-expert collapse |
| R1-dot | 20260522 | 1.0000 | 0.0000 | 1.0000 | single-expert collapse |
| S0-cos | 20260522 | 1.0000 | 0.0000 | 1.0000 | single-expert collapse |
| S1-cos | 20260522 | 1.0000 | 0.0000 | 1.0000 | single-expert collapse |
| S0-dot | 20260522 | 0.9932 | 0.1131 | 0.9711 | near collapse |
| S1-dot | 20260522 | 0.9932 | 0.1131 | 0.9711 | near collapse |

Interpretation:

These cases are decisive against using \(\max_e P(e\mid s,i)\) alone. Collapse produces perfect or near-perfect feature-key consistency.

## 7. Figures

### 7.1 Feature-Key Consistency

![Feature-key consistency histogram](figures/feature_key_consistency_histogram.png)

Interpretation:

Most feature keys are near consistency 1 across all conditions. This does not distinguish random baselines from slot-init or center-only conditions.

Hypothesis link:

This supports H1, the weak same-feature consistency claim. It cannot support specialization without Section 7.2 because collapse can also produce consistency 1.

### 7.2 Expert Load

![Expert load distribution](figures/expert_load_distribution.png)

Interpretation:

Expert load reveals the false positives hidden by feature-key consistency. Several seed-condition pairs route all or nearly all keys to one expert.

Hypothesis link:

This tests Rival R1. If load entropy is low or max load is near 1, high feature consistency is weak lock-in / collapse, not specialization.

### 7.3 Feature-Key Main Expert Map

![Feature-key route heatmap](figures/feature_key_route_heatmap.png)

Interpretation:

The map shows whether stable routing is structured or collapsed. Stable assignment is not equivalent to diverse or slot-aligned assignment.

Hypothesis link:

This is the composition visual. It helps distinguish structured many-to-one routing from all-to-one collapse, but it does not by itself decide whether the structure is slot, \(B_i\), or \((slot,B_i)\).

### 7.4 Checkpoint Drift

![Checkpoint feature drift](figures/checkpoint_feature_drift.png)

Interpretation:

Most feature-key main experts stabilize from step 800 to final. This only means the final map is stable; it does not say the map is non-collapsed.

Hypothesis link:

This tests whether training keeps changing the assigned main expert. It cannot validate the feature axis or expert utility.

### 7.5 Route-Slot Reference Figures

![Route-slot NMI trajectory](figures/route_slot_nmi_trajectory.png)

![Route-slot heatmap step0 final](figures/route_slot_heatmap_step0_final.png)

Interpretation:

Route-slot evidence remains a secondary diagnostic. It shows that slot-level alignment varies widely by seed and does not follow directly from feature-key consistency.

Hypothesis link:

This checks whether the route map is slot-aligned. It motivates the next audit because a high feature-key consistency score can coexist with weak or collapsed route-slot structure.

## 8. Artifact Map

Curated tables:

```text
tables/h0604a_decision_metrics_compact.csv
tables/feature_key_consistency_by_condition.csv
tables/feature_key_consistency_by_seed.csv
tables/feature_key_route_matrix.csv
tables/expert_load_by_condition.csv
tables/expert_load_by_seed.csv
tables/checkpoint_feature_drift.csv
tables/summary_by_condition.csv
tables/summary_by_seed.csv
```

Curated figures:

```text
figures/feature_key_consistency_histogram.png
figures/expert_load_distribution.png
figures/feature_key_route_heatmap.png
figures/checkpoint_feature_drift.png
figures/route_slot_nmi_trajectory.png
figures/route_slot_heatmap_step0_final.png
figures/multi_b_primary_decision_metrics.png
```

Repro command:

```text
python scripts/run_h0604a_feature_key_routing_stability.py \
  --config configs/h0604a_feature_key_routing_stability_center_only.json \
  --run-name h0604a_feature_key_routing_stability_4gpu_20260603 \
  --run-stage full \
  --conditions R0-dot,R1-dot,S0-dot,S1-dot,R0-cos,R1-cos,S0-cos,S1-cos \
  --parallel \
  --max-parallel 4 \
  --trajectory
```

ACP job:

```text
pt-8o1hoskg
```

## 9. Claim Boundary

Can claim:

Under the advisor's weak toy definition, same-feature consistency is basically true in H0604a.

Can claim:

Feature-key consistency alone is not a valid specialization metric in this setup because random baselines and collapsed runs can score near 1.

Can claim:

Center separation only did not improve feature-key consistency over NTP-only baselines.

Can claim:

Cosine router + slot init gives the best non-collapsed slot-aligned routing in this diagnostic, but it does not establish functional specialization.

Cannot claim:

Cannot claim all unsupervised assignment methods fail.

Cannot claim real-data robustness.

Cannot claim expert utility specialization.

Cannot claim that feature-key routing is meaningless; only that it is insufficient without load/diversity guards.

## 10. Next Decision

The next step is not route-utility binding yet. The next step is feature-axis audit on existing H0604a route logs/checkpoints.

Minimal next direction:

Compute the same routing audit for three candidate feature labels:

1. `slot`;
2. `B_i`;
3. `slot+B_i`.

Metrics:

1. \(\mathrm{mean}_f \max_e P(route=e\mid feature=f)\);
2. `NMI(route; slot)`;
3. `NMI(route; B_i)`;
4. `NMI(route; slot+B_i)`;
5. load entropy / max load;
6. per-expert composition table.

Decision logic:

1. If route aligns mostly with slot, slot is a valid operational feature for the next stage.
2. If route aligns mostly with \(B_i\), the previous slot-specialization claim is too strong.
3. If route aligns mostly with \((slot,B_i)\), the actual routed feature is atomic predictive state, not slot alone.
4. If consistency is high but load entropy is low, this is weak lock-in / collapse, not specialization.
5. If non-collapsed slot or slot+B_i structure exists, then proceed to utility-binding diagnostic.
6. If frequency is later varied, do it only after the feature axis is fixed.

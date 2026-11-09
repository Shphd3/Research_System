# Execution Plan: E2-B Prototype / Center Gating

## 1. Run Goal

在均匀 all-trigram synthetic data 上，用 cosine prototype router 替换 ordinary linear router，并比较 no-LB / LB / prototype aux 对 one-to-one feature-expert routing 的影响。

## 2. Data Construction

使用：

```text
data_uniform_all_trigram_v1000/four_feature_uniform_all_trigram_v1000_tokens.txt
```

固定 feature mapping：

```text
ABC -> expert 0
DEF -> expert 1
GHI -> expert 2
JKL -> expert 3
```

## 3. Model / Training / Evaluation Setup

Router logits:

$$
s_{t,e} = \tau \cdot \frac{z_t^\top c_e}{\|z_t\|\|c_e\|}
$$

训练 variants：

```text
prototype_no_aux_no_lb
prototype_no_aux_lb
prototype_aux_0_1_no_lb
prototype_aux_1_0_no_lb
prototype_aux_1_0_lb
```

默认 full run:

```text
steps = 10000
seeds = 20260513-20260517
```

## 4. Configs And Commands

Smoke:

```bash
python scripts/train_moe_prototype_center_gating.py \
  --run-config configs/e2_b_prototype_center_gating_uniform_all_trigram_v1000.json \
  --variants prototype_aux_1_0_no_lb \
  --seeds 20260513 \
  --steps 500 \
  --out-dir outputs/e2_b_prototype_center_gating_smoke
```

Full:

```bash
python scripts/train_moe_prototype_center_gating.py \
  --run-config configs/e2_b_prototype_center_gating_uniform_all_trigram_v1000.json
```

Plot:

```bash
python scripts/plot_router_gating_variants.py \
  --mode prototype \
  --out-dir outputs/e2_b_prototype_center_gating \
  --fig-dir figures/e2_b_prototype_center_gating
```

## 5. Metrics And Artifacts

Core:

```text
router_variant_summary.csv
routing_matrix_p_expert_given_feature.csv
feature_readback_table.csv
expert_load_table.csv
ablation_delta_table.csv
```

Prototype-specific:

```text
prototype_norm_table.csv
prototype_cosine_matrix.csv
feature_centroid_to_prototype_cosine.csv
```

## 6. Pass / Fail Criteria

Strong support: no-aux prototype beats ordinary linear router, or `prototype_aux_1_0_no_lb` reaches fixed-label accuracy $\ge 0.98$, NMI $\ge 0.95$, with high readback and strong ablation drop.

Weak support: only aux prototype succeeds.

Failure: aux prototype cannot form fixed diagonal.

## 7. Result Location

Raw ignored outputs:

```text
outputs/e2_b_prototype_center_gating/
figures/e2_b_prototype_center_gating/
```

Mainline report folder:

```text
versions/E2_B_prototype_center_gating/
```

# Execution Plan: E2-C Contrastive Router Loss

## 1. Run Goal

在均匀 all-trigram synthetic data 上，训练 contrastive router representation，判断 feature cluster pressure 是否能诱导 one-to-one expert routing。

## 2. Data Construction

使用：

```text
data_uniform_all_trigram_v1000/four_feature_uniform_all_trigram_v1000_tokens.txt
```

Contrastive labels 只表示同 feature / 不同 feature，不固定 expert id。

## 3. Model / Training / Evaluation Setup

Router representation:

$$
r_t = \mathrm{normalize}(W_p h_t)
$$

Supervised contrastive loss:

$$
L_{\text{supcon}}
=
-\frac{1}{N}
\sum_i
\frac{1}{|P(i)|}
\sum_{p\in P(i)}
\log
\frac{\exp(r_i^\top r_p/T)}
{\sum_{a\neq i}\exp(r_i^\top r_a/T)}
$$

Variants:

```text
contrastive_no_aux_no_lb
contrastive_no_aux_lb
contrastive_aux_0_1_no_lb
contrastive_aux_1_0_no_lb
contrastive_aux_1_0_lb
```

## 4. Configs And Commands

Smoke:

```bash
python scripts/train_moe_contrastive_router_loss.py \
  --run-config configs/e2_c_contrastive_router_loss_uniform_all_trigram_v1000.json \
  --variants contrastive_aux_1_0_no_lb \
  --seeds 20260513 \
  --steps 500 \
  --out-dir outputs/e2_c_contrastive_router_loss_smoke
```

Full:

```bash
python scripts/train_moe_contrastive_router_loss.py \
  --run-config configs/e2_c_contrastive_router_loss_uniform_all_trigram_v1000.json
```

Plot:

```bash
python scripts/plot_router_gating_variants.py \
  --mode contrastive \
  --out-dir outputs/e2_c_contrastive_router_loss \
  --fig-dir figures/e2_c_contrastive_router_loss
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

Contrastive-specific:

```text
router_representation_probe_table.csv
router_representation_centroid_cosine.csv
router_representation_samples.csv
feature_to_expert_best_permutation_table.csv
```

## 6. Pass / Fail Criteria

Strong support: contrastive aux reaches NMI $\ge 0.95$, best permutation accuracy $\ge 0.98$, high readback, and strong ablation drop.

Weak support: representation clusters but routing remains mixed.

Failure: contrastive loss drops but routing and representation do not improve, or readback collapses.

## 7. Result Location

Raw ignored outputs:

```text
outputs/e2_c_contrastive_router_loss/
figures/e2_c_contrastive_router_loss/
```

Mainline report folder:

```text
versions/E2_C_contrastive_router_loss/
```

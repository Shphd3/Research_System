# Execution Plan: E2-D Router Supervision Diagnostic

## 1. Run Goal

在均匀频率 all-trigram 数据上，给 router 加真实 feature label 辅助监督，判断当前 MoE 是否能形成固定对角的 clean specialization。

## 2. Data Construction

使用已生成数据：

```text
data_uniform_all_trigram_v1000/four_feature_uniform_all_trigram_v1000_tokens.txt
```

Feature mapping 固定为：

| feature | relation | feature id | count |
|---|---|---:|---:|
| ABC | `[1,2] -> 22` | 0 | 3900 |
| DEF | `[3,4] -> 23` | 1 | 3900 |
| GHI | `[6,7] -> 20` | 2 | 3900 |
| JKL | `[8,9] -> 21` | 3 | 3900 |

Router supervision 只取 prefix-end position：

```text
[1,2] -> 22 supervises position 2 with label 0
[3,4] -> 23 supervises position 4 with label 1
[6,7] -> 20 supervises position 7 with label 2
[8,9] -> 21 supervises position 9 with label 3
```

## 3. Model / Training / Evaluation Setup

模型：

```text
1-layer causal Transformer
d_model = 64
n_heads = 4
num_experts = 4
expert_ffn_dim = 128
top-1 routing
```

训练：

```text
steps = 10000
batch_size = 128
feature_router_batch_size = 128
seq_len = 32
lr = 0.0006
seeds = 20260513, 20260514, 20260515, 20260516, 20260517
```

每步：

```text
1. sample random NTP batch
2. compute L_NTP
3. sample balanced feature-router batch
4. compute router CE at prefix-end position
5. optimize L_NTP + lambda * L_router-feature
```

## 4. Configs And Commands

Config:

```text
configs/e2_d_router_supervision_uniform_all_trigram_v1000.json
```

Smoke:

```bash
python scripts/train_moe_router_supervision_diagnostic.py \
  --run-config configs/e2_d_router_supervision_uniform_all_trigram_v1000.json \
  --variants router_aux_lam_1_0 \
  --seeds 20260513 \
  --steps 500 \
  --out-dir outputs/e2_d_router_supervision_diagnostic_smoke
```

Full run:

```bash
python scripts/train_moe_router_supervision_diagnostic.py \
  --run-config configs/e2_d_router_supervision_uniform_all_trigram_v1000.json
```

Plot:

```bash
python scripts/plot_router_supervision_diagnostic.py \
  --out-dir outputs/e2_d_router_supervision_diagnostic \
  --fig-dir figures/e2_d_router_supervision_diagnostic
```

## 5. Metrics And Artifacts

保留 E2 原有输出：

```text
routing_matrix_p_expert_given_feature.csv
expert_purity_p_feature_given_expert.csv
feature_readback_table.csv
expert_load_table.csv
ablation_delta_table.csv
alignment_summary_table.csv
seed_stability_table.csv
```

新增：

```text
router_feature_accuracy_table.csv
router_feature_ce_table.csv
router_supervision_confusion_matrix.csv
```

图：

```text
router_feature_accuracy_by_lambda.png
router_feature_ce_by_lambda.png
routing_matrix_by_lambda.png
feature_readback_by_lambda.png
expert_load_by_lambda.png
ablation_delta_by_lambda.png
ntp_loss_and_router_aux_loss.png
```

## 6. Pass / Fail Criteria

Strong pass:

- `router_aux_lam_1_0` 或 `router_aux_lam_5_0` 的 router feature accuracy $\ge 0.98$；
- NMI $\ge 0.95$；
- routing matrix 接近固定对角；
- feature readback 不崩坏；
- dominant expert ablation 有明显 probability drop。

Weak pass:

- router accuracy 高，但 ablation weak。

Failure:

- `router_aux_lam_5_0` 仍无法让 router feature accuracy / NMI 接近 1。

## 7. Failure Modes To Check

- feature prefix-end position 是否和训练监督位置一致；
- feature id 是否固定映射到 expert id；
- router logits 是否来自 MoE router 的同一位置；
- auxiliary loss 是否进入 optimizer；
- evaluation 是否使用同一 prefix-end 位置。

## 8. Result Location

Ignored raw outputs:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/e2_d_router_supervision_diagnostic/
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/e2_d_router_supervision_diagnostic/
```

Mainline report:

```text
Projects/from-attention-to-search/main/experiments/E0_E3_synthetic_data_understanding/stages/E2_moe_feature_separation/versions/E2_D_router_supervision_diagnostic/
```

# Detailed Notes: E2-B Prototype / Center Gating

## Run Object

数据：均匀 all-trigram synthetic corpus。

| feature | relation | count |
|---|---|---:|
| ABC | `[1,2] -> 22` | 3900 |
| DEF | `[3,4] -> 23` | 3900 |
| GHI | `[6,7] -> 20` | 3900 |
| JKL | `[8,9] -> 21` | 3900 |

模型：tiny causal Transformer + top-1 MoE FFN。E2-B 只替换 router：

$$
z_t=\mathrm{LN}(h_t)
$$

$$
s_{t,e}=\tau \cdot \cos(z_t,c_e)
$$

$$
e_t=\arg\max_e s_{t,e}
$$

expert FFN 仍接收原始 hidden state $h_t$。

## Variants

| variant | loss | role |
|---|---|---|
| `prototype_no_aux_no_lb` | $L_{\mathrm{NTP}}$ | center router 自然路由 |
| `prototype_no_aux_lb` | $L_{\mathrm{NTP}}+0.01L_{\mathrm{LB}}$ | center router + 负载均衡 |
| `prototype_aux_0_1_no_lb` | $L_{\mathrm{NTP}}+0.1L_{\mathrm{proto}}$ | 弱 feature-to-prototype 监督 |
| `prototype_aux_1_0_no_lb` | $L_{\mathrm{NTP}}+1.0L_{\mathrm{proto}}$ | 主诊断 |
| `prototype_aux_1_0_lb` | $L_{\mathrm{NTP}}+L_{\mathrm{proto}}+0.01L_{\mathrm{LB}}$ | 检查 LB 是否破坏固定分工 |

其中 $L_{\mathrm{proto}}$ 是 prefix-end 位置的 feature label CE，固定映射为 ABC/DEF/GHI/JKL -> expert 0/1/2/3。

## Metric Meaning

`readback_probability`：模型在 feature prefix 后预测目标 token 的平均概率。

`NMI`：真实 feature label 与 expert id 的一致性，越高越说明路由按 feature 分开。

`best_permutation_accuracy`：允许 expert id 任意置换后，feature 到 expert 的最佳一对一准确率。

`fixed_label_accuracy`：是否严格符合 ABC->0、DEF->1、GHI->2、JKL->3。

`expert_load_entropy`：expert 使用是否均衡，最大值约为 $\log 4=1.386$。

`ablation_drop`：删除 dominant expert 后 target probability 下降多少，越高说明该 expert 对 feature readback 更有因果贡献。

## Artifact Paths

Ignored workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
  outputs/e2_b_prototype_center_gating/
  figures/e2_b_prototype_center_gating/
```

Mainline report figures:

```text
Projects/from-attention-to-search/main/experiments/E0_E3_synthetic_data_understanding/stages/E2_moe_feature_separation/versions/E2_B_prototype_center_gating/figures/
```

## Figure Notes

- `routing_matrix_by_variant.png`: supervised prototype variants become clean diagonal; no-aux variants remain mixed.
- `best_permutation_accuracy_by_variant.png`: no-aux variants stay near 0.51-0.53; supervised variants reach 1.0.
- `ablation_delta_by_variant.png`: supervised variants strongly increase dominant expert causal contribution.
- `feature_centroid_to_prototype_heatmap.png`: feature centroid and prototype alignment becomes clear under prototype supervision.

## Reliability Notes

The result is reliable for this diagnostic because all variants use the same data, model size, seeds, training length, and evaluation position. The only intended changes are router geometry, LB coefficient, and prototype supervision coefficient.

The strong supervised result also matches E2-D: when true feature signal is supplied, the code path can produce clean specialization. Therefore the negative no-aux result should be interpreted as insufficient natural routing pressure, not as an obvious implementation failure.

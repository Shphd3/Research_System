# Detailed Notes: E2-C Contrastive Router Loss

## Run Object

数据：均匀 all-trigram synthetic corpus。

| feature | relation | count |
|---|---|---:|
| ABC | `[1,2] -> 22` | 3900 |
| DEF | `[3,4] -> 23` | 3900 |
| GHI | `[6,7] -> 20` | 3900 |
| JKL | `[8,9] -> 21` | 3900 |

模型：tiny causal Transformer + top-1 MoE FFN。E2-C 新增 router representation：

$$
r_t=\mathrm{normalize}(W_ph_t)
$$

router logits:

$$
s_t=W_rr_t+b_r
$$

top-1 route:

$$
e_t=\arg\max_e s_{t,e}
$$

expert FFN 仍接收原始 hidden state $h_t$。

## Variants

| variant | loss | role |
|---|---|---|
| `contrastive_no_aux_no_lb` | $L_{\mathrm{NTP}}$ | projection router 自然路由 |
| `contrastive_no_aux_lb` | $L_{\mathrm{NTP}}+0.01L_{\mathrm{LB}}$ | projection router + 负载均衡 |
| `contrastive_aux_0_1_no_lb` | $L_{\mathrm{NTP}}+0.1L_{\mathrm{supcon}}$ | 弱 contrastive pressure |
| `contrastive_aux_1_0_no_lb` | $L_{\mathrm{NTP}}+1.0L_{\mathrm{supcon}}$ | 主诊断 |
| `contrastive_aux_1_0_lb` | $L_{\mathrm{NTP}}+L_{\mathrm{supcon}}+0.01L_{\mathrm{LB}}$ | 检查 LB 是否帮助 cluster-to-expert 分配 |

E2-C 不使用固定 expert id CE。成功标准允许 expert permutation，因此重点看 NMI 和 best-permutation accuracy。

## Metric Meaning

`probe_accuracy`：从 router representation $r_t$ 线性预测 feature label 的准确率。它回答“这个表示里是否有 feature 信息”。

`NMI`：feature label 与 expert id 的一致性。它回答“路由是否按 feature 分”。

`best_permutation_accuracy`：允许 expert 编号重排后的 feature-expert 一对一程度。

`fixed_label_accuracy`：是否刚好匹配 ABC->0、DEF->1、GHI->2、JKL->3。E2-C 不以它为成功标准。

`expert_load_entropy`：expert 使用是否均衡，最大值约为 $\log 4=1.386$。

`ablation_drop`：删除 dominant expert 后 target probability 下降多少。

## Main Numbers

| variant | probe acc | NMI | best-perm acc | load entropy |
|---|---:|---:|---:|---:|
| contrastive_no_aux_no_lb | 1.0000 | 0.4382 | 0.5073 | 0.8807 |
| contrastive_no_aux_lb | 1.0000 | 0.1363 | 0.3132 | 1.3855 |
| contrastive_aux_0_1_no_lb | 1.0000 | 0.5294 | 0.5002 | 0.7750 |
| contrastive_aux_1_0_no_lb | 1.0000 | 0.6920 | 0.6189 | 0.7913 |
| contrastive_aux_1_0_lb | 1.0000 | 0.4192 | 0.4498 | 1.3856 |

## Artifact Paths

Ignored workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
  outputs/e2_c_contrastive_router_loss/
  figures/e2_c_contrastive_router_loss/
```

Mainline report figures:

```text
Projects/from-attention-to-search/main/experiments/E0_E3_synthetic_data_understanding/stages/E2_moe_feature_separation/versions/E2_C_contrastive_router_loss/figures/
```

## Figure Notes

- `router_representation_pca_by_feature_and_expert.png`: feature information is visible in router representation, but expert colors do not become clean one-to-one.
- `routing_matrix_by_variant.png`: contrastive variants improve alignment over LB baseline but remain mixed.
- `best_permutation_accuracy_by_variant.png`: strongest variant reaches about 0.62, far below clean specialization.
- `contrastive_loss_curve.png`: contrastive loss quickly reaches a plateau around 3.434.

## Reliability Notes

The key comparison is reliable because all variants use the same uniform data, model size, feature positions, seeds, and evaluation metrics. The only intended changes are contrastive coefficient and LB coefficient.

The result should be read together with E2-D and E2-B: explicit feature CE can produce clean routing, but contrastive representation clustering cannot. This isolates the failure more precisely to the step from separable representation to expert boundary, not to data construction or MoE code.

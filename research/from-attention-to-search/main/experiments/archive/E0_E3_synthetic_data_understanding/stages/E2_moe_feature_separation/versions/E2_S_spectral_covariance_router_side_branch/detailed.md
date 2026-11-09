# Detailed Notes: E2-S Spectral Covariance Router Side Branch

## Run Setup

数据固定为 all-trigram v1000 corpus：

| feature | relation | target count |
|---|---|---:|
| ABC | `[1,2] -> 22` | 10000 |
| DEF | `[3,4] -> 23` | 5000 |
| GHI | `[6,7] -> 20` | 500 |
| JKL | `[8,9] -> 21` | 100 |

模型为 1-layer causal Transformer + 4-expert top-1 MoE FFN。训练参数：

```text
steps = 10000
batch_size = 128
seq_len = 32
d_model = 64
n_heads = 4
expert_ffn_dim = 128
seeds = 20260513-20260517
```

`full_hidden_lb` 使用 LB loss，`lb_coef=0.01`。所有 spectral projection routers 都不加 LB loss。

运行工作区：

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
```

## $\mu$ And Covariance Audit

这里的 $\mu$ 是 global hidden mean，不是 feature-conditioned mean。每个 covariance source 使用自己的 $\mu$：

$$
\mu_{\text{source}} = \mathbb{E}[h]
$$

$$
C_{\text{source}} = \mathbb{E}[(h-\mu_{\text{source}})(h-\mu_{\text{source}})^T]
$$

| source | mu norm | cov trace | effective rank | top-1 var | top-10 var |
|---|---:|---:|---:|---:|---:|
| trained_dense_cov | 2.989 | 53.831 | 54.607 | 0.048 | 0.338 |
| random_init_cov | 1.186 | 62.593 | 51.124 | 0.050 | 0.375 |
| shuffled_dense_cov | 2.151 | 57.128 | 55.165 | 0.047 | 0.327 |

解释：trained dense covariance 的 $\mu$ 更大，但谱并不是强低秩结构；top-10 方差占比约 0.34，说明没有明显“只靠头部方向”的解释。

## Projection Separability

所有主要 projection 的 feature probe accuracy 都达到 1.0。这说明 feature 在这些空间中都容易线性读出，因此 probe 不是充分判据。

更有区分度的是 Fisher ratio：

| source | variant | Fisher ratio |
|---|---|---:|
| trained_dense_cov | `midlate_25_90_raw_no_lb` | 82.144 |
| trained_dense_cov | `midlate_25_90_whiten_no_lb` | 85.968 |
| trained_dense_cov | `random_matched_42_no_lb` | 92.720 |
| random_init_cov | `midlate_25_90_raw_no_lb` | 102.246 |
| shuffled_dense_cov | `midlate_25_90_raw_no_lb` | 41.127 |

解释：trained midlate 并没有超过同维随机子空间，也没有超过 random-init midlate。这个结果直接削弱 H-S1/H-S2。

## Router Evaluation

报告数字从明细表重新聚合：

| source | variant | readback | NMI | purity | load entropy | ablation drop |
|---|---|---:|---:|---:|---:|---:|
| none | `full_hidden_lb` | 0.948 | 0.809 | 0.945 | 1.386 | 0.457 |
| none | `full_hidden_no_lb` | 0.910 | 0.819 | 0.946 | 1.218 | 0.503 |
| trained_dense_cov | `midlate_25_90_raw_no_lb` | 0.948 | 0.429 | 0.691 | 1.306 | 0.515 |
| trained_dense_cov | `midlate_25_90_whiten_no_lb` | 0.946 | 0.443 | 0.688 | 1.317 | 0.519 |
| trained_dense_cov | `random_matched_42_no_lb` | 0.950 | 0.797 | 0.873 | 1.216 | 0.554 |
| random_init_cov | `midlate_25_90_raw_no_lb` | 0.940 | 0.546 | 0.754 | 1.270 | 0.326 |
| shuffled_dense_cov | `midlate_25_90_raw_no_lb` | 0.928 | 0.453 | 0.701 | 1.189 | 0.403 |

主要观察：

- readback 基本都能成功，说明 projection router 没有破坏 NTP feature learning。
- trained midlate raw/whiten 的 NMI 只有 0.43/0.44，明显低于 full-hidden router 的 0.81/0.82。
- random matched 42-dim 的 NMI 为 0.80，接近 full-hidden control，强于 midlate。
- spectral midlate no-LB 没有 collapse；load entropy 约 1.31，接近均衡上限 $\log 4 \approx 1.386$，但均衡不等于 feature alignment。

## Figure Index

Report figures are copied beside this file:

```text
figures/mu_norm_by_source.png
figures/covariance_spectrum_by_source.png
figures/cumulative_variance_by_source.png
figures/feature_probe_accuracy_by_band_trained_dense_cov.png
figures/feature_probe_accuracy_by_band_random_init_cov.png
figures/feature_probe_accuracy_by_band_shuffled_dense_cov.png
figures/fisher_ratio_by_projection.png
figures/pc_feature_alignment_heatmap.png
figures/readback_by_projection.png
figures/routing_nmi_by_projection.png
figures/routing_matrix_midlate_vs_full_lb_vs_random.png
figures/expert_load_by_projection.png
figures/dominant_ablation_by_projection.png
figures/force_routing_by_projection.png
```

Ignored raw outputs:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/e2_s_spectral_covariance_router/
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/e2_s_spectral_covariance_router/
```

## Failure Mode

这不是“统计量完全无效”的简单失败，因为 projection 中确实能线性读出 feature，也能支持 readback。更准确的失败模式是：

```text
feature information exists in the projection,
but middle-to-late covariance projection does not make the learned router more feature-aligned than full hidden or random matched projection.
```

因此 E2-S 不支持“谱中后段天然代表 router 语义子空间”的版本。后续如果要继续，需要更精确地定义统计量：global covariance 可能太粗，feature-conditioned covariance 或去掉 token/frequency shortcut 后的 residual covariance 更值得测试。

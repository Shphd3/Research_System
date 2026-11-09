# Detailed Notes: E2-S Uniform Frequency Control

## Purpose

本实验检查一个可能的混淆因素：E2-S long-tail 结果中，spectral midlate router 没有明显改善 routing alignment，是否只是因为 `500/100` 的低频 features 太难、太容易被背景和高频 feature 淹没。

因此这里保持 planted feature 总数不变：原来总数为 `10000+5000+500+100=15600`，现在均分成四个 feature，每个 `3900`。

## Run Setup

模型结构：

```text
1-layer causal Transformer
d_model = 64
n_heads = 4
MoE FFN = 4 top-1 experts
expert_ffn_dim = 128
router_input = variant-specific projection
expert_input = original hidden state
```

训练设置：

```text
steps = 10000
batch_size = 128
seq_len = 32
seeds = 20260513, 20260514, 20260515, 20260516, 20260517
```

数据设置：

| feature | relation | count |
|---|---|---:|
| ABC | `[1,2] -> 22` | 3900 |
| DEF | `[3,4] -> 23` | 3900 |
| GHI | `[6,7] -> 20` | 3900 |
| JKL | `[8,9] -> 21` | 3900 |

运行工作区：

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
```

配置文件：

```text
configs/e1_uniform_all_trigram_v1000.json
configs/e2_s_spectral_covariance_router_uniform_all_trigram_v1000.json
```

主要输出：

```text
outputs/e2_s_spectral_covariance_router_uniform/
figures/e2_s_spectral_covariance_router_uniform/
```

## Metric Meaning

`readback`：在 feature prefix 位置预测目标 token 的概率。越高说明模型越能读回 planted relation。

`NMI`：feature label 与 expert id 的一致性。越高说明不同 feature 越倾向进入不同 expert 或不同 expert 分布。

`purity`：每个 expert 内部由单一 feature 主导的程度。越高说明 expert 更“纯”。

`load entropy`：expert 使用是否均匀。4 个 expert 的均匀上限是 $\log 4 \approx 1.386$。高 entropy 表示不 collapse，但不等于 feature alignment。

`ablation drop`：删除 dominant expert 后 target probability 的下降。越高说明该 expert 对 feature prediction 更有因果贡献。

`probe accuracy`：只用 projection hidden 线性预测 feature label 的准确率。它检验信息是否存在，不检验 router 是否使用该信息。

## $\mu$ And Covariance Audit

这里的 $\mu$ 是 global hidden mean，不是 feature-conditioned mean。

| source | tokens | mu norm | hidden norm | centered norm | cov trace | effective rank | top-1 var | top-5 var | top-10 var |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| trained_dense_cov | 250000 | 4.464 | 8.016 | 6.614 | 44.333 | 52.850 | 0.050 | 0.214 | 0.360 |
| random_init_cov | 250000 | 1.185 | 8.000 | 7.910 | 62.596 | 51.221 | 0.050 | 0.220 | 0.375 |
| shuffled_dense_cov | 250000 | 3.679 | 7.978 | 7.068 | 50.110 | 53.432 | 0.051 | 0.207 | 0.351 |

解释：trained dense 的 $\mu$ 最大，说明训练后 hidden space 的全局均值结构更强。但三个 source 的 top explained variance 很接近，因此不能只凭谱形状断言 trained covariance 有独特语义结构。

## Main Result Table

| source | variant | readback | NMI | purity | load entropy | ablation drop | dominant best rate | dominant advantage | probe acc | Fisher |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| none | `full_hidden_lb` | 0.994 | 0.645 | 0.608 | 1.386 | 0.433 | 0.650 | 0.143 | 1.000 | 150.530 |
| none | `full_hidden_no_lb` | 0.995 | 0.637 | 0.645 | 1.249 | 0.467 | 0.850 | 0.256 | 1.000 | 150.530 |
| trained_dense_cov | `pca_full_coord_no_lb` | 0.996 | 0.451 | 0.518 | 1.141 | 0.531 | 0.700 | 0.417 | 1.000 | 150.530 |
| trained_dense_cov | `top_0_25_raw_no_lb` | 0.994 | 0.374 | 0.453 | 1.000 | 0.350 | 0.650 | 0.376 | 1.000 | 150.657 |
| trained_dense_cov | `topdrop_25_100_raw_no_lb` | 0.996 | 0.639 | 0.682 | 1.214 | 0.565 | 0.650 | 0.326 | 1.000 | 150.420 |
| trained_dense_cov | `mid_25_75_raw_no_lb` | 0.996 | 0.522 | 0.500 | 1.069 | 0.619 | 0.850 | 0.394 | 1.000 | 186.816 |
| trained_dense_cov | `midlate_25_90_raw_no_lb` | 0.997 | 0.661 | 0.651 | 1.206 | 0.580 | 0.950 | 0.403 | 1.000 | 166.092 |
| trained_dense_cov | `midlate_25_90_whiten_no_lb` | 0.997 | 0.688 | 0.649 | 1.214 | 0.676 | 0.900 | 0.405 | 1.000 | 142.706 |
| trained_dense_cov | `tail_50_100_raw_no_lb` | 0.995 | 0.439 | 0.500 | 0.964 | 0.643 | 0.950 | 0.415 | 1.000 | 79.375 |
| trained_dense_cov | `random_matched_42_no_lb` | 0.996 | 0.641 | 0.641 | 1.025 | 0.615 | 0.700 | 0.473 | 1.000 | 150.558 |
| random_init_cov | `midlate_25_90_raw_no_lb` | 0.996 | 0.562 | 0.565 | 1.247 | 0.496 | 0.800 | 0.378 | 1.000 | 112.157 |
| random_init_cov | `midlate_25_90_whiten_no_lb` | 0.996 | 0.617 | 0.610 | 1.227 | 0.496 | 0.750 | 0.355 | 1.000 | 96.729 |
| shuffled_dense_cov | `midlate_25_90_raw_no_lb` | 0.997 | 0.705 | 0.699 | 1.164 | 0.678 | 0.900 | 0.400 | 1.000 | 64.323 |
| shuffled_dense_cov | `midlate_25_90_whiten_no_lb` | 0.996 | 0.724 | 0.728 | 1.171 | 0.567 | 0.850 | 0.407 | 1.000 | 59.103 |

## Why The Result Is Reliable

第一，所有 variants 使用同一批 feature、同一训练步数、同一 seed set，因此差异主要来自 router input 和 covariance source。

第二，`full_hidden_lb`、`full_hidden_no_lb`、trained covariance、random-init covariance、shuffled covariance 同时存在，能区分三件事：

- 是否只是 LB loss 造成 routing 对齐；
- 是否只是任意低维投影都能工作；
- 是否 trained sequential covariance 比 random/shuffled covariance 更有解释力。

第三，结果不是只看单一指标。readback 检查任务是否学会，NMI/purity 检查 routing 是否按 feature 对齐，load entropy 检查是否 collapse，ablation drop 检查 expert 是否有因果贡献，probe accuracy/Fisher ratio 检查投影空间中是否含 feature 信息。

第四，关键结论来自控制组比较：如果 trained midlate 的提升是真正的 sequential feature 语义证据，它应该明显强于 shuffled covariance。但实际 shuffled covariance 的 NMI 更高，所以不能做强 claim。

## Figure Index

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

## Bottom Line

均匀频率控制说明：长尾频率确实压低了 E2-S spectral router 的表现；但是频率均匀后，强结果也不专属于 trained covariance midlate projection。因此当前最稳妥的解释是：

```text
feature frequency affects routing alignment,
but global covariance midlate projection is still not a clean semantic routing statistic.
```

# R1 结果：E1/E2 Synthetic Router Retrieval

实验卡：`../E1_E2_E15_E25_synthetic_router_retrieval/purpose_card.md`

本页只保留汇报主线：**E1 NTP 训练后的 router bucket 是否能作为 block2 KV candidate index**。详细过程与补充图见实验目录报告：

```text
detailed.md
```

## 1. 核心假设

```text
TransformerBlock1 -> Router/MoE/H-MoE -> TransformerBlock2
```

router 在 block2 前面，因此历史 token 的 bucket/path assignment 理论上可以作为 block2 attention 的 KV 候选索引。

要验证的是：

```text
router top-K buckets 是否能召回 full dense attention 的 high-mass KV，
并在候选内 exact QK rerank 后接近 full attention output。
```

## 2. Setup 为什么有意义

- E1 用 NTP CE 训练，测试 LM-style 训练后 router 是否自然产生检索信号。
- E2 不再训练，只分析 E1 checkpoint 的 block2 dense attention。
- 对照是同候选数 random/local，以及 oracle same-count 上界。
- `K=16` 选中全部 16 个 bucket/path，是 full-prefix sanity check；真正看 `K=1/2/4/8`。

## 3. 关键图

图目录：

```text
figures/R1_synthetic_router_retrieval_0512_nocap/
```

优先看三张：

- ![E2 recall/mass/L2](figures/R1_synthetic_router_retrieval_0512_nocap/e2_nocap_topk_recall_mass_l2_prefix_ge128.png)
- ![E2 candidate ratio](figures/R1_synthetic_router_retrieval_0512_nocap/e2_nocap_candidate_ratio_prefix_ge128.png)
- ![E2 delta vs random](figures/R1_synthetic_router_retrieval_0512_nocap/e2_nocap_router_delta_vs_random_prefix_ge128.png)
- ![E2 rank-K-only recall/mass](figures/R1_synthetic_router_retrieval_0512_nocap/e2_rank_k_only_recall_mass_prefix_ge128.png)

SAE 诊断图：

- ![Flat vs H-MoE bucket path shared scale](figures/R1_synthetic_router_retrieval_0512_nocap/bucket_to_path_flat_vs_hmoe_shared_scale.png)
- ![MoE SAE activation matrix](figures/R1_synthetic_router_retrieval_0512_nocap/sae_e1/flat_lb_on/sae_activation_matrix_tokens_x_top_features.png)
- ![H-MoE SAE activation matrix](figures/R1_synthetic_router_retrieval_0512_nocap/sae_e1/hmoe_lb_off/sae_activation_matrix_tokens_x_top_features.png)

数据分布诊断图：

- ![Zipf rank frequency](figures/R1_synthetic_router_retrieval_0512_nocap/data_distribution_diagnostics/zipf_rank_frequency_atom_token_rule.png)
- ![Hidden spectrum](figures/R1_synthetic_router_retrieval_0512_nocap/data_distribution_diagnostics/hidden_state_spectral_decomposition.png)
- ![PCA outer path](figures/R1_synthetic_router_retrieval_0512_nocap/data_distribution_diagnostics/hidden_state_pca_outer_path.png)

## 4. 关键结果

E2 使用 `prefix_len >= 128` 的稳定 KV 区间，并让 random/local/oracle 与 router 使用相同 candidate_count。

NTP 数据分布：

| Diagnostic | Value | Interpretation |
|---|---:|---|
| atom rank-frequency Zipf fit | alpha 0.70, R2 0.81 | latent atoms 有长尾，但受 global/path/noise 混合影响，不是单一纯 Zipf |
| NTP token rank-frequency Zipf fit | alpha 1.88, R2 0.74 | next-token label 有长尾，接近语言式 heavy-tail，但尾部截断明显 |
| path entropy | 1.000 | path 近似均匀，这是为了控制 16 path 覆盖，不是自然语言 topic 频率 |
| covariance effective rank | 43.9 / 64 | `h_t` 是宽谱高维分布，不是少数 PC 主导 |
| top-32 PCs variance | 0.833 | 有谱衰减，但不是低秩清晰簇 |
| path between-trace ratio | 0.000065 | path 层级在均值/PCA 空间很弱 |

因此：数据在 feature/token 频率上有 long-tail，但层级主要存在于稀疏 atom co-activation 和 metadata 中，而不是明显的 path-separated PCA cluster。这会让 router 更难学出干净 bucket。

模型规模：

| Variant | Total params | Router params | Expert params | Active params/token proxy |
|---|---:|---:|---:|---:|
| MoE+LB | 155,856 | 1,040 | 67,072 | 92,976 |
| H-MoE | 156,116 | 1,300 | 67,072 | 93,236 |

H-MoE 比 MoE+LB 多 260 个总参数，active proxy 差约 0.28%，因此本轮对比基本不是参数量驱动。

| Variant | K | Candidate ratio | Router recall | Random recall | Router mass | Random mass | Router L2 | Random L2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MoE+LB | 4 | 0.295 | 0.519 | 0.302 | 0.587 | 0.304 | 0.255 | 0.438 |
| MoE+LB | 8 | 0.541 | 0.738 | 0.541 | 0.780 | 0.535 | 0.131 | 0.280 |
| H-MoE | 4 | 0.324 | 0.509 | 0.326 | 0.588 | 0.324 | 0.264 | 0.416 |
| H-MoE | 8 | 0.593 | 0.702 | 0.600 | 0.751 | 0.600 | 0.164 | 0.233 |

Rank-K-only 诊断，即只看“排名第 K 的单个 bucket/path”：

| Variant | rank K | Bucket ratio | Single-bucket recall | Single-bucket mass |
|---|---:|---:|---:|---:|
| MoE+LB | 1 | 0.084 | 0.210 | 0.280 |
| MoE+LB | 2 | 0.076 | 0.137 | 0.138 |
| MoE+LB | 4 | 0.065 | 0.072 | 0.072 |
| MoE+LB | 8 | 0.061 | 0.047 | 0.042 |
| H-MoE | 1 | 0.095 | 0.240 | 0.310 |
| H-MoE | 2 | 0.078 | 0.119 | 0.132 |
| H-MoE | 4 | 0.081 | 0.066 | 0.069 |
| H-MoE | 8 | 0.059 | 0.043 | 0.033 |

SAE 诊断：

| Variant | bucket-path purity | bucket-rule purity | bucket-path entropy | SAE-path purity | SAE-rule purity |
|---|---:|---:|---:|---:|---:|
| MoE+LB | 0.155 | 0.204 | 0.928 | 0.257 | 0.330 |
| H-MoE | 0.161 | 0.191 | 0.908 | 0.264 | 0.363 |

其中 `bucket_to_path_flat_vs_hmoe_shared_scale.png` 使用同一色标和同一行归一化 $P(path \mid bucket)$。H-MoE 的 path purity 只从 0.155 到 0.161，entropy 从 0.928 到 0.908，说明它略有结构化趋势，但不是清晰 path 分发。

## 5. 结论

```text
E1 NTP 后的 router bucket 确实包含粗粒度 KV retrieval signal；
router top-K 明显强于同候选数 random/local。
```

但：

```text
这个 signal 不够干净，也不够高效。
K=8 已经需要约 54%-59% prefix candidate；
SAE 显示 bucket 内 path/rule 语义高度混杂。
```

对主假设的判定：

```text
弱支持：router 有粗粒度检索信号。
不支持：当前普通 MoE/H-MoE router bucket 已经是干净、高效、可直接使用的 KV index。
```

## 6. 可能冲突点

- `K=16` 是 full-prefix sanity check，不能作为检索成功证据。
- K=8 的 recall/mass 已经明显强于 random，但 candidate ratio 过高，不能过度宣称 sparse retrieval。
- rank-K-only 显示前几个 bucket 贡献明显更高，说明 router ranking 有信号；但后续 bucket 很快接近低贡献区，说明 bucket 本身并不干净。
- SAE 稀疏性还不够强，SAE 只用于错误诊断，不作为机制证明。

## 7. 下一步

- 不把 R1 作为 DCLM 正向证据。
- 下一步应设计更干净的 router/index objective 或 candidate selection。
- E1.5/E2.5 作为机制对照继续分析，但不进入本次 E1/E2 主闭环。

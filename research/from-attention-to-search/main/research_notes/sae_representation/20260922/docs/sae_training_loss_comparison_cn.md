# 约 22B 历史模型与 fresh S7 \(\lambda_{rec}=0.1\) 的训练损失比较

> 快照时间：2026-09-22 16:26 UTC。比较对象是 Dense、M2 主路径瓶颈、原版 SALL，以及从零训练的 fresh S7 \(\lambda_{rec}=0.1\)。旧的 15.466B 后分叉 S7 不属于这个纯从零训练条件，因此没有混入。

## 直接结果

fresh S7 在本快照已经到 **22,376,256,000** 个有效预测词元。因此四模型现在具有严格共同的 **22B** 比较点，不需要外推。

在共同终点之前最后 2B（20B–22B）上，对原始逐更新 \(L_{LM}\) 做精确词元加权平均，排序为：

| 排名 | 模型 | 最后共同 2B 的 \(L_{LM}\) | 相对 Dense | 相对 Dense 百分比 |
|---:|---|---:|---:|---:|
| 1 | M2：末层 MLP 前串联 SAE，\(\lambda_{rec}=1\) | **3.241236206019** | **-10.169714 millinat** | -0.312779% |
| 2 | SALL：8 层 Attention 输出旁路，\(\lambda_{rec}=1\) | **3.244100622945** | **-7.305297 millinat** | -0.224681% |
| 3 | fresh S7：第 8 层 Attention 输出旁路，\(\lambda_{rec}=0.1\) | **3.247963893468** | **-3.442026 millinat** | -0.105863% |
| 4 | Dense | **3.251405919739** | 0 | 0 |

因此，确切的当前训练损失结论是：

1. **fresh S7 \(\lambda_{rec}=0.1\) 在精确 22B 比 Dense 更低**：20B–22B 平均低 **3.442026 millinat**；把这 2B 切成 20 个互不重叠的 100M 区块，S7 在 **20/20** 个区块都低于 Dense，区块差值范围是 **-4.455535 到 -1.513962 millinat**。
2. **但 fresh S7 仍高于 SALL 和 M2**：20B–22B 中，S7 比 SALL 高 **3.863271 millinat**，比 M2 高 **6.727687 millinat**。
3. 22B 前最后 100M 的瞬时窗口仍是同一排序：M2 3.233487416、SALL 3.235429375、S7 3.241679210、Dense 3.243193172。该窗口更易受语料波动影响，所以主比较采用最后 2B。

![训练 LM loss 完整比较](../../../../../../../daily_research_reports/backup/2026/09/0922/figures/sae_training_loss_comparison/training_lm_loss_22b_models_plus_fresh_s7.png)

读图方式：A 展示四条轨迹至 22B；B 放大 10B–22B 共同区间；C 画 100M 词元尾随均值相对 Dense 的差，低于零即训练 LM loss 更低；D 是 20B–22B 的原始 loss 精确均值，不是平滑值。

## 四模型在精确 22B 的比较

采用 20B–22B 的原始 \(L_{LM}\) 词元加权平均：

| 排名 | 模型 | 20B–22B 的 \(L_{LM}\) | 相对 Dense |
|---:|---|---:|---:|
| 1 | M2 | **3.241236206019** | **-10.169714 millinat** |
| 2 | SALL | **3.244100622945** | **-7.305297 millinat** |
| 3 | fresh S7 \(\lambda_{rec}=0.1\) | **3.247963893468** | **-3.442026 millinat** |
| 4 | Dense | **3.251405919739** | 0 |

## 比较对象与 loss 定义

| 模型 | 架构 | 优化目标 | 是否能直接比较 total loss |
|---|---|---|---|
| Dense | 原生 8 层 Dense LM | \(L_{LM}\) | 否；它没有 SAE 项 |
| M2 | 最后一层 `norm2` 后、MLP 前经过 SAE 重构，MLP 使用重构值 | \(L_{LM}+L_{rec}\) | 否；SAE 位于主路径 |
| SALL | 八层原生 Attention 输出各接一个旁路 SAE；重构不回主路径 | \(L_{LM}+L_{rec}+\frac{1}{32}L_{AuxK}\) | 否；有 8 个 SAE 且重构项定义为跨层均值 |
| fresh S7 | 第 8 层原生 Attention 输出接一个旁路 SAE；重构不回主路径 | \(L_{LM}+0.1L_{rec}+\frac{1}{32}L_{AuxK}\) | 否；系数与 SAE 数量不同 |

所以图和所有排名只比较全局归一化的训练语言损失 \(L_{LM}\)；把 total loss 画在同一标尺上会把不同辅助目标及其系数误当成模型质量差异。

## 可比性审计

四条轨迹共享：seed 17、长度 2048、同一数据清单（SHA-256 `8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d`）、每次优化更新 262,144 个有效预测词元，以及相同的 LM 学习率、AdamW betas、weight decay 和 warmup。主横轴因此使用累计有效预测词元。

- **最严格的旁路比较是 fresh S7 对 Dense。** Dense 的 8 卡 sampler 显式复现 4 卡参考样本顺序；fresh S7 使用原生 4 卡参考顺序。两者全局 batch、逐更新样本顺序和初始化时 LM 推理路径匹配，区别是 S7 的旁路训练约束。
- **M2 是有效的模型训练比较，但不是插件式旁路对照。** 它让 MLP 消费 SAE 重构，因此训练和推理主路径都不同。
- **SALL 是预算和数据分布匹配的描述性比较，不是最严格的逐更新配对。** 它前段使用 8 卡原生 sampler，逐更新样本顺序不同于 4 卡参考顺序；不能把 SALL−Dense 的每一个 millinat 全部因果归于“八个 SAE”。
- 硬件数变化都保持了相同有效全局 batch；SALL 续训段从 8 卡切到 4 卡时也保持 262,144 词元/更新。

## 证据边界

这是**单 seed、训练集语言损失**结果。它确切回答“在相同累计训练词元下，记录到的训练 \(L_{LM}\) 谁更低”，但不能直接推出 held-out perplexity、通用能力、语义表征质量，或 SAE 机制的跨 seed 因果平均效应。尤其是 M2 的最低 loss 不能证明主路径 SAE 更优；SALL 的第二名也不能在其样本顺序偏差未消除时被解释为纯 SAE 数量效应。

## 可复现文件

- 图：[`training_lm_loss_22b_models_plus_fresh_s7.png`](../../../../../../../daily_research_reports/backup/2026/09/0922/figures/sae_training_loss_comparison/training_lm_loss_22b_models_plus_fresh_s7.png)
- 当前共同终点精确表：[`latest_common_endpoint_summary.csv`](../../../../../../../daily_research_reports/backup/2026/09/0922/tables/sae_training_loss_comparison/latest_common_endpoint_summary.csv)
- 最后 2B 的 20 个非重叠 100M 区块：[`latest_2b_nonoverlap_100m_blocks.csv`](../../../../../../../daily_research_reports/backup/2026/09/0922/tables/sae_training_loss_comparison/latest_2b_nonoverlap_100m_blocks.csv)
- 四模型 22B 表：[`historical_only_22b_summary.csv`](../../../../../../../daily_research_reports/backup/2026/09/0922/tables/sae_training_loss_comparison/historical_only_22b_summary.csv)
- 固定词元点表：[`landmark_trailing_100m_means.csv`](../../../../../../../daily_research_reports/backup/2026/09/0922/tables/sae_training_loss_comparison/landmark_trailing_100m_means.csv)
- 源快照哈希与口径：[`comparison_manifest.json`](../../../../../../../daily_research_reports/backup/2026/09/0922/tables/sae_training_loss_comparison/comparison_manifest.json)
- 构图程序：[`build_training_loss_comparison.py`](../../../../../../../daily_research_reports/backup/2026/09/0922/report_assets/build_training_loss_comparison.py)

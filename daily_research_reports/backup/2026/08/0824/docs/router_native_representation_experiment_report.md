---
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
date: 2026-08-24
experiment: A15_08_09_E03_native_router_representation_controls
canonical_summary: ../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E03_native_router_representation_controls/summary.md
---

# 原生 Router 输入表征实验简报

## 目的

检验 E02 中 $R_U$ 单独路由失败，是否意味着 Qwen3-30B-A3B 原本送入 MoE gate 的表征也没有稳定类别信息。

原生 Router 输入定义为

$$G_\ell=X_\ell+U_\ell,$$

它是每层 attention 残差相加并经过 post-attention RMSNorm 后，真正输入该层 MoE gate 的 2,048 维 hidden state。

## 数据与方法

- 复用 E02 的 19,200 行数据、8 个 parent classes 和最后一个 `Answer:` token。
- 不重新运行模型：直接从已验证的全层 $(X,U)$ 抽取构造 $G$。
- TRAIN 计算逐层类内、类间方差；TRAIN 拟合 ridge、DEV 冻结最佳层。
- 冻结 Block 42 后，用五种子 L2 logistic probe 评估两个 TEST 面板；机会水平为 12.5%。

## 结果图

![原生 Router 输入的类内/类间方差与准确率](../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E03_native_router_representation_controls/figures/native_router_input_variance.png)

蓝线是每维类内方差，橙线是每维类间方差；二者使用对数纵轴。绿线是仅用于选层的 DEV balanced accuracy，黑色虚线是冻结的 Block 42。

## 确切结果

| 指标 | Same-template TEST | New-template TEST |
| --- | ---: | ---: |
| Ordinary accuracy | 77.90% | 75.43% |
| Balanced accuracy | 77.90% | 75.43% |
| 95% 区间 | [77.20%, 78.60%] | [74.70%, 76.16%] |
| 5% 低尾 margin | -2.1440 | -2.8559 |

五个种子全部收敛；标签置换控制通过。H5 判定为 `Pass`。

Block 42 的类内方差为 0.054919，类间方差为 0.002217，类间/类内比只有 0.04038。全 48 层最大比值也只有 0.07449。

## 结论

原生 Router 输入中存在很强、跨模板稳定的线性类别信息。因此，E02 的负结论只能限定为“构造出来的 $R_U$ 不能单独稳健路由”，不能扩大成“模型的 Router 输入没有类别结构”。

但总体类内方差仍远大于类间方差，5% 低尾 margin 也显著为负。这说明：高平均准确率可以由少量对齐的判别方向产生，并不要求整个高维空间形成全局正间隔。

本实验不能证明 Qwen 原 gate 使用了这八类信息，也不能证明它对应专家效用。


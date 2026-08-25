---
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
date: 2026-08-24
experiment: A15_08_09_E03_native_router_representation_controls
canonical_summary: ../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E03_native_router_representation_controls/summary.md
---

# 相邻层 Router 输入差分实验简报

## 目的

原生 Router 输入 $G_\ell$ 累积了此前所有层的信息。为了观察相邻层之间新出现的变化，本实验使用

$$\Delta G_\ell=G_\ell-G_{\ell-1},\qquad \ell=2,\ldots,48.$$

Block 1 没有真实的前一层 Router 输入，因此不补零、不纳入扫描。

## 数据与方法

- 沿用与原生表征实验完全相同的数据、标签、token 和划分。
- 从同一份 E02 全层抽取按需计算 $\Delta G$，不重新运行 30B 模型。
- TRAIN 计算类内/类间方差并拟合 ridge；DEV 从 Block 2--48 冻结 Block 41。
- 在 Block 41 运行五种子 L2 logistic probe 和标签置换控制，再评估两个 TEST 面板。

## 结果图

![相邻层 Router 输入差分的类内/类间方差与准确率](../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E03_native_router_representation_controls/figures/adjacent_router_delta_variance.png)

图中橙色类间方差在深层明显增大，但始终低于蓝色类内方差。DEV 准确率在中后层快速上升，冻结层为 Block 41。

## 确切结果

| 指标 | Same-template TEST | New-template TEST |
| --- | ---: | ---: |
| Ordinary accuracy | 76.40% | 71.21% |
| Balanced accuracy | 76.40% | 71.21% |
| 95% 区间 | [75.66%, 77.14%] | [70.48%, 71.95%] |
| 5% 低尾 margin | -2.6626 | -4.2588 |

五个种子全部收敛；标签置换控制通过。H5 判定为 `Pass`。

Block 41 的类内方差为 0.014476，类间方差为 0.000720，类间/类内比为 0.04971。最大方差比出现在 Block 45，为 0.06160，但最大 DEV 准确率出现在 Block 41；两个选层标准并不等价。

## 结论

即使把上一层的原生 Router 输入减掉，相邻层变化仍保留很强的跨模板线性类别信息。这排除了“只有此前累计状态可读、层间变化完全没有类别信息”这一解释。

但 $\Delta G$ 的新模板准确率低于完整 $G$，且低尾 margin 更负。因此它包含可用类别信号，却没有自然形成 E02 定理所要求的全体样本正间隔空间。

本实验不能把相邻层差分解释成某一个 attention/MLP 模块独立创造的信息，也不能证明真实 gate 或专家使用了这部分信号。


---
experiment_id: A15_02_02_E01_natural_hierarchy_role_localization
status: completed
verdict: fail_universal_semantic_hierarchy_spectral_mapping
date: 2026-08-01
---

# 真实粗细概念 token 的频谱位置：结果摘要

## 结论

**我们没有发现一个可跨当前 MoE 与 Qwen3-8B 复现的“粗语义属于某一谱带、细语义属于另一谱带”的固定映射。**

直接看不同词构成的概念集合时，粗概念与细概念确实呈现稳定不同的谱画像：两者的绝对激活能量都主要位于 covariance 谱头；相对普通文本 token 校正后，粗概念在多数中后层反而比细概念更富集于 middle/tail。可是，当词汇固定为同一个中位概念（例如同一个 `algebra` 分别充当 `mathematics` 的子类和 `linear algebra` 的父类）后，差异没有跨模型通过顺序护栏。因此，集合画像差异目前不能归因于语义层级本身；词汇组成、短语长度和上下文仍是更强解释。

## 实验回答什么

我们测试：在真实学科语义链中，概念由粗到细的角色是否稳定对应模型表征 covariance 谱中的不同位置。

- 语义层级：`mathematics → algebra → linear algebra` 等 32 条三层学科链。
- 模型层：当前 12 层 LB-80k MoE 与 36 层 Qwen3-8B 的逐层表征。
- 频谱层级：每层 covariance 的方向按方差从大到小排序；F1 是最高方差的前 \(1/12\)，F12 是最低方差的后 \(1/12\)。

这是冻结模型的表征审计，没有微调或继续训练。MoE 读取部署线性 Gate 的真实输入；Qwen3-8B 没有 MoE Router，读取相同计算位置的 post-attention、pre-MLP 归一化表征，作为大模型表示对照。

## 数据与主要比较

语料包含 32 条语义链、12 个 calibration 模板和 4 个独立 evaluation 模板，共 512 句；每句明确标注 root、mid-child、mid-parent、leaf 四个 span。示例：

> In an academic taxonomy, mathematics includes algebra as a major field, while algebra in turn includes linear algebra as a specialized field.

covariance 只用 384 条 calibration 句中的 9,180 个普通内容 token 拟合；结论来自 128 条 evaluation 句、每模型 512 个标注 occurrence。两个 tokenizer 的 2,048 个 span 均精确映射，失败数为 0；同一句两个 `algebra` 的 token-id 序列完全一致。

## 指标的人话含义

1. **投影能量占比：**一个 token 去均值后的激活能量有多少百分比落在某段谱方向。它回答“能量实际在哪里”，但天然受谱头的大方差支配。
2. **频带富集：**该 token 在某频带的能量占比，相对于所有 calibration token 在该频带的平均占比高多少。对数富集为 0 表示与普通 token 相同；\(+0.69\) 约表示 2 倍，\(-0.69\) 约表示一半。
3. **同词角色差：**同一句中，同一个中位概念作为父类和子类时的富集差。它消除了词汇身份和 subword 长度，是判断“语义角色本身是否改变谱位置”的主指标。

## 决定性结果

### 1. 绝对能量：粗、细概念都主要落在谱头

H/M/T 分别占方向秩的 \(1/12\)、\(4/12\)、\(7/12\)。下表给出概念 token 去均值激活能量的百分比：

| 模型与层 | 粗概念 H/M/T | 细概念 H/M/T |
| --- | --- | --- |
| MoE L1 | 72.07 / 27.58 / 0.35 | 71.55 / 28.17 / 0.29 |
| MoE L6 | 70.59 / 26.23 / 3.18 | 75.79 / 22.07 / 2.14 |
| MoE L12 | 73.25 / 24.64 / 2.12 | 76.60 / 21.92 / 1.48 |
| Qwen L1 | 91.14 / 7.95 / 0.92 | 92.89 / 6.39 / 0.73 |
| Qwen L18 | 64.51 / 23.02 / 12.47 | 70.56 / 19.01 / 10.44 |
| Qwen L36 | 84.69 / 10.27 / 5.04 | 89.06 / 7.58 / 3.36 |

![按方差秩排列的粗细概念投影能量](figures/rank_ordered_projection_profile.png)

图中横轴从最高方差方向走向最低方差方向，纵轴是每个等秩区间承担的 token 激活能量；阴影为按 32 条语义链重采样的 95% 区间。

### 2. 集合画像：粗概念相对更偏 middle/tail，但这不是纯语义证据

相对于普通 calibration token，Qwen 的 9 个观测层均表现为粗概念在 H 上低于细概念、在 M/T 上高于细概念；MoE 中对应关系分别为 10/12、10/12、12/12 层。这个描述性模式跨模型一致，但 root 与 leaf 是不同词，无法排除词频、短语长度和词汇身份。

![当前 MoE 的层-粗细粒度-谱带画像](figures/layer_granularity_spectral_atlas_lb80k.png)

![Qwen3-8B 的层-粗细粒度-谱带画像](figures/layer_granularity_spectral_atlas_qwen3_8b.png)

### 3. 同词角色审计：没有跨模型固定映射

共检验 315 个“模型 × 层 × 频带”单元。19 个单元在旧的宽松规则下看似超过零与随机 rank 对照；加入 Protocol 已要求的顺序交互护栏后：

- 只剩 MoE L1 的 F7、F9、F11 三个细尾带通过，方向均为“同一中位概念作为子类时更富集”；
- Qwen3-8B 没有任何通过单元；
- 没有任何效应跨两个模型相应深度复现，因此总假设判为 **Fail**。

Qwen L1 的粗 T 候选是最清楚的反例：child-first 模板差为 \(-0.833\)，parent-first 仅为 \(-0.024\)，两种顺序的交互 95% 区间为 \([-0.885,-0.743]\)。这说明其表面差异主要由 occurrence 顺序或左侧上下文控制，不能解释为层级角色。

![同一概念作为父类与子类的频带差](figures/same_concept_role_spectral_heatmap.png)

图中 `x` 表示超过零和随机 rank、但未通过顺序交互护栏的候选；`*` 表示通过严格单模型护栏。跨模型总判定仍为 Fail。

## 认识更新

1. **真实粗、细概念都主要使用高方差谱头，而不是粗概念只在 head、细概念只在 tail。**
2. **粗概念集合在 middle/tail 的相对富集高于细概念集合，但当前不能把该差异解释成语义层级，因为同词角色对照不跨模型成立。**
3. **covariance rank 仍然是表征能量坐标，不是已经验证的“语义抽象度坐标”；同一频带不能仅凭方差排名被命名为粗语义或细语义频带。**
4. **若要建立“层 × 粗细粒度 × 频带”功能图谱，必须同时控制词汇身份、因果模型可见的左上下文和 occurrence 位置；只比较 `mathematics` 与 `linear algebra` 会产生过强结论。**

## 结论边界与下一决策

本实验可以描述真实概念集合在两种训练好模型中的谱能量画像，并否定一个跨模型固定的层级角色—covariance rank 映射。它不能证明层级语义不在表征中，也不能回答这些方向是否被 Router 功能性使用或能否改善专家分发。

唯一下一决策是：是否构造独立、位置匹配的自然百科关系句，使同一目标概念在相同左上下文长度下分别被明确标记为父类和子类，并以关系完成后的同一 probe 位置复核；只有该对照跨模型通过，才把 covariance 频带升级为层级语义候选坐标。

完整证据见 [detailed.md](detailed.md)，数值表见 [role_contrast_summary.csv](tables/role_contrast_summary.csv) 与 [layer_granularity_spectral_atlas.csv](tables/layer_granularity_spectral_atlas.csv)。

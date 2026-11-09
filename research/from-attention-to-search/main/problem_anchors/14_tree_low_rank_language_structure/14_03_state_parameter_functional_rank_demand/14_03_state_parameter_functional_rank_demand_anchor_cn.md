---
anchor_id: 14_03_state_parameter_functional_rank_demand
line: 14_tree_low_rank_language_structure
status: candidate_for_human_review
canonical_language: en
canonical: 14_03_state_parameter_functional_rank_demand_anchor.md
depends_on: 14_02_relation_reuse_root_effective_rank
protocol_status: not_created
---

# A14_03：更高的任务状态功能秩是否要求更多参数功能方向？

研究线基础：[A14_00 条件低秩层次结构](../14_00_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure_anchor_cn.md)。上游决策：[A14_02 ROOT 功能秩](../14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor_cn.md)。

## 1. 问题定义

这个候选主 anchor 只问一个条件式问题：

> 在规则结构、暴露次数、输出分布、模型能力和 held-out 任务效用匹配后，一个确实需要更高任务状态功能秩的条件，是否也因果地需要已注册参数算子的更大功能子空间？

该问题依赖 A14_02。只有 A14_02 先建立稳定且任务充分的状态秩差异，A14_03 才有资格进入协议阶段。

本文区分：

- **共现频率**：一条确切关系或活动模式在训练数据中的共同出现次数；
- **任务状态功能秩**：在容许误差内保持 held-out 任务效用所需的最小状态子空间维数；
- **参数功能秩**：在同一容许误差内保持任务效用所需的已注册参数算子最小保留秩。

低共现只是条件变量，不是高秩的预设原因。

## 2. 物理先验

1. 真正被行为需要的状态方向，必须能由某些参数 Jacobian 或算子子空间控制，但该参数实现未必唯一。
2. 暴露频率改变估计机会，但不决定代数秩。
3. 只有删除后损害 held-out 任务效用的参数方向，才算功能上必要。

## 3. 可证伪假设

### 主假设

在已预注册且能力匹配的条件中，若一个条件具有更高的状态功能秩，那么把参数算子限制到低状态秩条件所需的最小功能秩时，高状态秩条件应承受更大的效用损失；允许其使用更多参数方向后，该损失应得到选择性恢复。

### 最强竞争解释

参数秩主要反映优化冗余、参数化自由度、函数数量或训练不足，而不是必要的状态容量，因此状态功能秩与参数功能秩可以在因果上脱钩。

### 裁定

- **通过**：状态秩差异稳定；共同的低参数秩上限选择性损害高状态秩条件；提高参数秩后跨预注册随机种子恢复。
- **失败**：状态秩差异稳定，但共同秩上限没有选择性损害，或更多参数方向不能选择性恢复。
- **证据不足**：A14_02 未建立状态差异、能力守卫失败、已注册算子被其他部分补偿，或效应不稳定。

## 4. 数学模型

对条件 \(m\)，定义任务状态功能秩：

\[
k_H(m;\epsilon_H)
=
\min\left\{
k:
\mathcal L_H(m,k)-\mathcal L_{\mathrm{full}}(m)
\le \epsilon_H
\right\},
\]

其中 \(\mathcal L_H(m,k)\) 表示把已注册根状态限制在校准得到的 \(k\) 维子空间后，模型在 held-out 数据上的损失。

对预注册参数算子 \(B\)，定义参数功能秩：

\[
k_B(m;\epsilon_B)
=
\min\left\{
k:
\mathcal L_B(m,k)-\mathcal L_{\mathrm{full}}(m)
\le \epsilon_B
\right\}.
\]

设 \(m_{\mathrm{lo}}\) 和 \(m_{\mathrm{hi}}\) 是预注册的低、高状态功能秩条件，并令

\[
k_{\mathrm{cap}}=k_B(m_{\mathrm{lo}};\epsilon_B).
\]

候选主指标是共同秩上限带来的差分代价：

\[
D_{\mathrm{cap}}
=
\left[
\mathcal L_B(m_{\mathrm{hi}},k_{\mathrm{cap}})
-\mathcal L_{\mathrm{full}}(m_{\mathrm{hi}})
\right]
-
\left[
\mathcal L_B(m_{\mathrm{lo}},k_{\mathrm{cap}})
-\mathcal L_{\mathrm{full}}(m_{\mathrm{lo}})
\right].
\]

\(D_{\mathrm{cap}}>0\) 仍不足以单独通过；还必须验证提高算子保留秩能选择性恢复高状态秩条件。

## 5. 计算实现

未来协议应继承 A14_02 的匹配条件和 checkpoint，并且：

1. 预注册状态干预、参数算子、容许误差和比较条件；
2. 只用 calibration 数据估计状态与参数功能秩；
3. 在 held-out 数据上检验共同秩上限代价与恢复；
4. 加入随机等秩子空间和能力匹配对照；
5. 报告其他层或算子补偿的诊断。

首个候选参数对象是 QK 组合打分算子，而不是分别读取原始 \(W_Q\)、\(W_K\) 谱。该选择在协议审核前仍是 AI 提议。

## 6. 最小证伪测试

1. **前置测试**：A14_02 必须先建立 held-out、任务充分的状态秩差异。
2. **共同秩上限测试**：把低状态秩条件的参数秩上限同时施加到两个条件。
3. **选择性恢复测试**：只增加允许的算子秩，检验高状态秩条件是否恢复。
4. **随机子空间对照**：区分功能方向和一般维数。
5. **训练不足对照**：只有能力匹配后才解释参数方向需求。

## 7. 当前证据

A14_01/E08 只提供受限的复合变量证据：共享条件的参数空间压缩明显强于状态空间压缩，而参数秩与状态秩的相关性弱且不显著。这只说明值得做因果检验，不支持本假设。

A14_02 尚未建立本问题所需的状态秩前提。A09 的 common/rare Router 工作研究的是另一个问题，不能作为状态秩要求参数秩的证据。

## 8. 声称边界与下一决策

即使结果为正，也只适用于已注册任务、条件、状态干预和参数算子。不能据此声称低共现普遍导致高秩、自然语言全局低秩，或 MoE Router 必然必要。

**唯一下一决策：**先审核 A14_02 及其协议；只有 A14_02 建立稳定且任务充分的状态秩差异后，才把 A14_03 提升为实验协议。

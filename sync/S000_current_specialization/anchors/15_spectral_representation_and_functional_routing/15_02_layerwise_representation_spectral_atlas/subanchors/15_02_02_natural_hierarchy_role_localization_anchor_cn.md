---
anchor_id: 15_02_02_natural_hierarchy_role_localization
parent_anchor: 15_02_layerwise_representation_spectral_atlas
status: completed_e02_pass_layer_specific_role_selectivity
thinking_card: 15_02_02_natural_hierarchy_role_localization_thinking_card_cn.md
---

# A15_02_02 真实层级概念的频谱位置

Thinking Card source: [Thinking Card](15_02_02_natural_hierarchy_role_localization_thinking_card_cn.md)

## 1. Problem Definition

当前唯一决策问题：在冻结 Qwen3-8B 中，每层 covariance 基底由独立自然语料拟合时，同一个中位概念作为父级或子级，是否稳定落在不同的 covariance 谱位置？实验必须把“实际投影能量”和“除去每个方向背景方差后的方向选择性”分开。

Head、middle、tail 只表示本层背景方差由高到低的相对秩区间；不同层的同名频带不等于编码相同语义。

## 2. Physical Priors

高背景方差会机械抬高 head 的原始投影。若语义角色确实偏好某个方向，该差异应在逐方向除以背景方差后仍存在，并通过同词同位置、多模板、语义链重采样和 calibration 半分验证。若差异只由背景尺度、词汇或位置造成，raw 差异会在白化后消失或随模板变化。

## 3. Falsifiable Hypotheses

- H1：父减子在至少一个粗或细频带存在稳定的白化差异。
- 最强 rival：只存在 raw head 差异，白化后没有稳定选择性。
- 第二 rival：效应只出现在孤立层或单一模板，不构成深度规律。
- Pass：独立基底有效，效应同时通过链级 bootstrap、链标签置换、多模板、tail 阈值敏感性及相邻层或预注册末层复现。
- Fail：数据和基底门通过，但没有稳定频带效应。
- Insufficient：token 配对、basis 稳定、重构、能量守恒或 tail 稳定性失败。

## 4. Mathematical Model

独立自然 calibration 表征定义

$$
\Sigma_\ell=U_\ell\Lambda_\ell U_\ell^\top.
$$

目标状态中心化后 $x=h-\mu_\ell$，第 $i$ 个方向的投影为 $a_i=u_i^\top x$。原始能量为 $a_i^2$；除去背景方差后的能量为

$$
q_i=\frac{a_i^2}{\lambda_i+\epsilon}.
$$

等秩频带内按方向数取平均；主指标是 32 条语义链上的父减子配对差。Raw 回答实际能量，白化量回答超出背景方差的方向选择性；二者都不等于专家效用。

## 5. Computational Realization

冻结本地 `/data/share/Qwen3-8B`，读取 embedding 输出与全部 decoder block 输出的 residual state。固定 128 篇 DCLM held-out 自然文档、共 65,536 token 拟合每层 covariance。保留原 32 条学科层级链，用四种模板构造同目标词、同 token 序列、同绝对位置、等长度的父/子最小对。频谱分解只离线执行。

## 6. Minimal Falsification Tests

决定证据是层 × 频带的同概念父减子 raw/white 图谱。必须通过 token/span/位置配对、关系先于目标、covariance 重构与能量守恒、half-split projector overlap、父子标签置换、多模板一致性、特征值 floor 敏感性，以及末层反转的链级复现。

## 7. Current Evidence

E01 使用模板内 calibration、九个 Qwen 深度和频带富集指标；Qwen 没有严格通过的同词父/子单元，因而否定了跨模型普遍 rank 映射。见 [E01 中文摘要](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_02_E01_natural_hierarchy_role_localization/summary_cn.md)。

E02 使用 128 篇独立 DCLM 自然文档、65,536 token 拟合 Qwen3-8B 全部 37 个表征位置的 covariance，并在原 32 条链上测试 128 个同词、同 token span、同绝对位置、等长度的父/子最小对。配对、replay、数值重构、half-split、多模板、语义链、标签置换和特征值 floor 护栏全部通过。

结果为：**层特异白化角色选择性 Pass，统一“父级=head”规则 Fail。** block 5--19 中有 10 层稳定表现为子级白化 head 更强，block 25--32 的 8 层全部稳定表现为父级白化 head 更强。父/子配对倍数在 block 10、29、36 分别为 0.961、1.080、0.915。所有 raw/white H/M/T 比较都没有通过预注册的“最后一层单独反转”判据。见 [E02 中文摘要](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_02_E02_qwen3_independent_role_atlas/summary_cn.md)。

## 8. Claim Boundary And Next Decision

E02 只建立 Qwen3-8B 内部、层特异的表征关联；不能证明 covariance rank 因果产生语义、深层执行组合、某频带应指导 Router 或能改善专家训练，也不能建立跨模型、语言、自然语料或概念体系的普遍映射。

唯一下一决策是：是否用独立模型或独立自然语料基底，复核早中层“子级更 head”和晚层“父级更 head”的两段画像。只有外部复现的层 × 频带坐标才有资格进入另行批准的功能效用检验。

---
anchor_id: 15_02_07_matched_semantic_complexity
status: closed_insufficient_complex_specific_effect
canonical_language: en
companion_language: zh
parent_anchor: 15_02_layerwise_representation_spectral_atlas
updated: 2026-08-09
---

# A15_02_07 匹配语义复杂度在逐层 MLP 参数谱中的位置


## 1. 问题定义

**决策问题：**

> 在冻结 Qwen3-8B 中，分别使用公平匹配的 taxonomy 和受控 composition 任务时，attention 引起的实际 MLP 输入增量，是否使复杂目标随深度越来越占据本层 MLP 参数谱的较后秩，并提供条件新增的线性信息？

实际 MLP 输入增量为 \(\Delta n_\ell=RMSNorm_\ell(x_\ell+a_\ell)-RMSNorm_\ell(x_\ell)\)。每层 MLP 输入侧参数算子为 \(K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}+W_{up,\ell}^{\top}W_{up,\ell}\)，按参数增益由高到低排序。不同层相同 rank 不代表同一个向量。

两个语义对象分别裁定：

- **TAX：**匹配的八分类跨 parent 简单任务，对比 parent 内八分类 conditional-fine 任务。
- **COMP：**一步检索 \(V\to C\)，对比两步组合 \(U\to V\to C\)；上下文与终点 code 相同。

问题包含两项：H1 问复杂相对简单的类别间方差位于哪里；H2 问 \(\Delta n_\ell\) 是否提供旧 MLP 输入之外的线性信息。二者不能互相补救。

## 2. 物理先验

1. 若深层 attention 写入增加了复杂区别，那么已经看到旧 MLP 输入的冻结读出，在加入 \(\Delta n_\ell\) 修正后应继续改善。
2. 若该区别越来越分配到本层低参数增益方向，复杂减简单的归一化秩重心应从早层向晚层增加。
3. 若深度只改变共同尺度、归一化几何或本地 rank 占用，简单与复杂曲线会一起移动，而二者之差接近零。

这些都是冻结模型的表征假设，不能推出 attention 创造信息、MLP 原生使用或 Router 收益。

## 3. 可证伪假设

**H1——复杂特异的本地参数秩后移。**每个分支内，复杂减简单的归一化本地秩重心，从抽样早层到抽样晚层增加。

**H2——条件新增线性信息。**先拟合并冻结旧 MLP 输入的线性读出，再只拟合 \(\Delta n_\ell\) 的输出修正；该修正对复杂目标的未参与拟合数据损失改善大于简单目标，而且复杂减简单的改善从早层到晚层增加。

**最强竞争解释。**公平匹配消除了类别数、类中心精度和模型能力混淆，但深度仍只产生所有目标共有的几何移动，或写入的信息对旧状态是线性冗余的。即使增量单独可读，H1/H2 仍会接近零。

TAX 与 COMP 独立裁定。只用增量拟合读出的 `Disc(\Delta n)` 是辅助证据，不能建立 H2。

## 4. 数学模型

对分支 \(d\) 和条件 \(q\in\{simple,complex\}\)，令 \(B_{\ell,d,q}\) 为 \(\Delta n_\ell\) 的平衡类别间协方差。在本层参数基底 \(K_\ell=V_\ell\Gamma_\ell V_\ell^{\top}\) 中归一化逐方向方差，并计算秩重心 \(m_{\ell,d,q}\)。令

\[
R_{\ell,d}=m_{\ell,d,complex}-m_{\ell,d,simple},
\]

H1 指标为

\[
T_{rank,d}=\operatorname{median}_{\ell\in\{25,29,33\}}R_{\ell,d}
-\operatorname{median}_{\ell\in\{1,5,9\}}R_{\ell,d}.
\]

H2 先在 \(n_\ell^{old}\) 上拟合正则化线性读出并冻结，再只拟合 \(\Delta n_\ell\) 的 logit 修正。条件信息增益为

\[
CIG_{\ell,d,q}=CE^{conf}_{base}-CE^{conf}_{base+\Delta n}.
\]

令 \(G_{\ell,d}=CIG_{\ell,d,complex}-CIG_{\ell,d,simple}\)，再作相同的抽样晚层减早层对比，得到 \(T_{CIG,d}\)。两项都是分支内部的差分之差：H1 不能证明可访问性，H2 不能定位参数谱位置。

## 5. 计算实现

- **冻结模型与层：**Qwen3-8B 的 1/5/9/13/17/21/25/29/33/36 层。
- **TAX：**1,920 条文本；八对八分类任务；每个 leaf 在 TRAIN、DEVELOPMENT、CONFIRMATION 各 10 种表达。简单与复杂都用八个标签和相同类中心数。
- **COMP：**3,072 条记录；64 个独立映射 episode、八个终点 code、两个条件、三个数据部分。修订后任务的 restricted-choice 能力为 simple 0.9902、complex 0.7578，均通过门槛。
- **信息角色：**TRAIN 拟合读出，DEVELOPMENT 选正则强度，未参与选择的 CONFIRMATION 产生 H1/H2。TAX 任务和 COMP episode 组是成对重采样单位；层和方向不是独立重复。
- **图：**十层 raw 与归一化逐方向方差曲线必须同时展示；平滑只改善可读性，裁定只使用未平滑数值。

TAX 与 COMP 不合并。完整数据身份、Protocol 修订、hash 和证据血缘保留在各自 detailed record。

## 6. 最小证伪测试

每个分支分别使用：

- **H1 Pass：**CONFIRMATION 的 \(T_{rank}>0\)、成对 bootstrap 95% 下界 \(>0\)，且 DEVELOPMENT 的 \(T_{rank}>0\)。
- **H2 Pass：**CONFIRMATION 的 \(T_{CIG}>0\)，且成对 bootstrap 95% 下界 \(>0\)。
- **Fail：**有效性检查通过，但对应区间上界低于零。
- **Insufficient：**区间跨零、DEVELOPMENT 反转 H1 所需方向，或数据/能力/可靠性门失败。

联合语义精细化机制要求同一分支的 H1 与 H2 都 Pass。简单与复杂共同移动、增量单独可读，或平滑图看似有序，都不能替代注册结果。

## 7. 当前证据

两个已批准 full run 均完成并通过有效性检查，但没有一个分支支持联合机制。

| 分支 | H1：复杂特异参数秩后移 | H2：条件新增线性信息 | 裁定 |
|---|---|---|---|
| TAX | \(-0.004690\)，区间 \([-0.012182,0.009295]\) | \(-1.09\times10^{-7}\) nats/example，区间 \([-4.30\times10^{-7},5.92\times10^{-7}]\) | 均 insufficient |
| COMP | \(+0.002114\)，区间 \([-0.002384,0.005226]\)；DEVELOPMENT 为 \(-0.003608\) | \(+0.018523\) nats/example，区间 \([-0.050412,0.081052]\) | 均 insufficient |

[TAX 结果](../../../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_07_E01_matched_taxonomy_full/summary.md)说明：匹配类别数与类中心精度后仍没有稳定的 fine-specific 效应。[COMP 结果](../../../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_07_E02_controlled_composition_full/summary.md)说明：增量在晚层单独可读，但没有稳定的 complex-specific 后移，也没有证明相对旧状态新增线性信息。

保留下来的观察是所有目标共有的：简单与复杂的秩重心都随深度明显后移，而二者之差很小且不单调。

## 8. Claim 边界与下一决策

- **问题：**在分别匹配的 TAX 与 COMP 数据中，复杂目标是否随深度越来越占据较后的本地 MLP 参数秩，并获得条件新增的线性可访问性？
- **直接结果：**没有一个注册分支支持联合结论。所有 H1/H2 区间都跨零，且 COMP H1 在 DEVELOPMENT 与 CONFIRMATION 间反号。
- **更新判断：**当前不支持把复杂度特异的语义精细化表述为稳定参数秩后移或线性新增信息。保留对象是所有目标共有的逐层后移和谱形变化。
- **不能声称：**这些结果不能证明不存在非线性信息，不能证明 tail 有功能、MLP 原生使用了该空间、跨层存在共享语义向量，也不能证明 nonlinear Router 会受益。fine 绝对可读性较低本身不等于非线性编码。
- **唯一下一决策：**将 A15_04 设为 close-out gate，只允许在现有固定样本集合上做一次几何重分析：检验共同后移是否比等维随机、head 和 middle 空间更强地对齐跨层共享参数 tail。通过后才另立功能检验；未通过则关闭 tail 功能解释。本闭环不授权新数据、复现、干预或 Router 实验。

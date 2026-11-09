---
anchor_id: 15_08_02_layerwise_conditional_fine_added_accessibility
status: COMPLETED_PASS_LAYERS_24_28
canonical_companion: 15_08_02_layerwise_conditional_fine_added_accessibility_anchor.md
parent_anchor: ../15_08_target_conditioned_layer_innovation_anchor_cn.md
parent_line: 15_spectral_representation_and_functional_routing
execution_authority: APPROVED_AND_COMPLETED_FULL_FROZEN_ALL_LAYER_RUN
created: 2026-08-16
updated: 2026-08-16
---

# A15_08_02：逐层 conditional-fine 新增可访问性

父问题见 [A15_08](../15_08_target_conditioned_layer_innovation_anchor_cn.md)。英文正式 Anchor 见 [Canonical Anchor](15_08_02_layerwise_conditional_fine_added_accessibility_anchor.md)。执行合同草案见 [E01 Protocol](../../../../experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_02_E01_layerwise_conditional_fine_added_accessibility/protocol.md)。

## 1. Problem Definition

最终研究路线希望找到一个对逐层新增细粒度信息敏感、并可服务后续分发的低维空间。本子 Anchor 只负责它之前的功能门：

> 对冻结 Qwen3-8B 的所有合格层，同一 token 的归一化 attention transition 中，哪些层在完全相同的旧状态分支和目标无关同预算对照之外，增加了留出表达上的父类内 child 可访问性？

任务固定为 **conditional-fine**：已知父类，在父类内部八选一预测 child。预测单位是一个冻结的 decision-token occurrence。“新增可访问性”只表示注册线性读出族中的留出交叉熵下降，不表示 Shannon 信息创造、知识存储、模型原生使用或 Router 效益。

科学总体是按前向顺序排列的全部 block，不再预选单层 smoke 或先筛最佳层。第 25 层只提供另一目标上提取与度量曾可合格的既有证据，不构成本 taxonomy 的预测。block 1 仍被记录；若固定 decision token 上的旧状态为结构性常数，则标为不合格，预期正式集合为 blocks 2--36。

## 2. Physical Priors

1. **同层精确相减。**同一个 token、block 和 post-attention RMSNorm 下，无写入状态与实际状态位于同一坐标，因此差分有明确物理含义。
2. **同一 \(X\) 的双分支隔离。**所有分支冻结并复用由同一个 \(X_\ell\) 得到的 base logits，真分支与对照分支只允许新增 correction 输入不同。
3. **先功能、后压缩。**协方差谱、PCA、公共基或聚类只能描述更新几何，不能证明更新增加目标可访问性；只有本 Anchor 通过后才能进入低秩分析。

## 3. Falsifiable Hypotheses

**H-CF — 层局部 conditional-fine 新增可访问性。**至少一个合格 block 的目标对齐 residual-update 增益，在全层同时校正后仍超过 duplicate-\(X\) correction 容量和目标无关同预算更新错配。`AI_PROPOSAL`：用 64 个 mismatch bank、它们的 q95 和 familywise 95% 同时区间把这一研究者判断实例化。

**最强竞争解释 R-CAP — 没有新增输入的 correction 容量。**第二分支改善只是因为 old-only 读出欠拟合，或任意同维 correction 都增加容量。若该解释成立，复制 \(X\) 或样本错配更新能够取得同等改善。

其他竞争解释包括表达/模板泄漏、父类不平衡、任务本身不可做、旧状态结构性常数、张量身份错误和不同层 old-state loss 余量不同。仅原始增益为正不能排除这些解释。

“深层累计表征更能区分细类”和“新增表征低秩”是研究动机，不在本 Anchor 中被联合裁定。本 Anchor 不要求收益随深度单调，也不注册低秩 verdict。

## 4. Mathematical Model

在第 \(\ell\) 个 block 的冻结 decision token，令 \(h_\ell\) 为输入 residual，\(a_\ell\) 为 output projection 后的 attention write，\(N_\ell\) 为同一个 post-attention RMSNorm：

\[
X_\ell=N_\ell(h_\ell),\qquad
Z_\ell=N_\ell(h_\ell+a_\ell),\qquad
U_\ell=Z_\ell-X_\ell.
\]

只用 TRAIN 做分组交叉拟合：

\[
R_{U,\ell}=U_\ell-\widehat m^U_\ell(X_\ell).
\]

对父类 \(p\) 拟合 old-state base 并冻结 logits：

\[
s^0_{\ell,i}=b_{\ell,p(i)}(X_{\ell,i}).
\]

所有新增分支都复用完全相同的 \(s^0\)：

\[
s^{true}_{\ell,i}=s^0_{\ell,i}+q^{true}_{\ell,p(i)}(R_{U,\ell,i}),
\]

\[
s^{dupX}_{\ell,i}=s^0_{\ell,i}+q^{dupX}_{\ell,p(i)}(X_{\ell,i}),
\]

\[
s^{mis,b}_{\ell,i}=s^0_{\ell,i}+q^{mis,b}_{\ell,p(i)}(\widetilde R^{,b}_{U,\ell,i}).
\]

\(\widetilde R^{,b}_{U}\) 是每个父类内部的平衡、样本级重新配对，不是固定 child 标签换名，也不能使用 CONFIRMATION 信息。duplicate-\(X\)、mismatch bank 以及下面取较强对照的保守定义均为 `AI_PROPOSAL`，用于把研究者提出的“同一 \(X\) 双分支”要求变成可证伪合同。

对分支 \(v\) 定义父类等权留出增益：

\[
G^v_\ell=\mathbb E_{conf}
\left[CE(s^0_\ell,Y)-CE(s^v_\ell,Y)\right]
\quad\text{nats/example}.
\]

保守的逐层同预算净收益为

\[
T_\ell=G^{true}_\ell-
\max\left\{G^{dupX}_\ell,q_{0.95,b}(G^{mis,b}_\ell)\right\}.
\]

唯一主要科学输出是

\[
\mathcal L^+=\left\{\ell:\operatorname{LCB}^{sim}_{0.95}(T_\ell)>0\right\}.
\]

无论点估计为正、零或负，每个合格层都必须保留在有符号曲线上。

## 5. Computational Realization

1. 冻结本地 Qwen3-8B、tokenizer、prompt、最后一个 `Classification:` decision token、conditional-fine taxonomy 与父类内八分类 ridge 族。
2. 全层拟合复用现有平衡 TAX 的 TRAIN/DEVELOPMENT 表达。`AI_PROPOSAL`：正式裁定前另生成并冻结 640 条新 CONFIRMATION：8 父类 × 每类 8 child × 每 child 10 个表达/内容家族，且与 TRAIN/DEVELOPMENT 互斥。
3. residualizer 和读出只用 TRAIN 拟合；DEVELOPMENT 只选冻结正则和做诊断；所有层、对照映射、图规则和区间规则冻结后，CONFIRMATION 标签只打开一次。
4. `AI_PROPOSAL`：真更新、duplicate-\(X\) 和 64 个 mismatch correction 使用同样输入维度、训练行数、父类权重、正则网格与选择预算；允许每个分支在 DEVELOPMENT 上选自己的最优 ridge，避免人为削弱对照。
5. 获得一次明确的完整执行授权后，先运行不依赖模型结果的 known cases 和身份 preflight；通过后，同一次执行直接提取 blocks 1--36，并按前向顺序拟合合格的 blocks 2--36。研究者已于 2026-08-16 明确取消单层 smoke。
6. `AI_PROPOSAL`：主图横轴为 1--36；若 block 1 结构性不合格则在 x=1 明示 NA；其余层全部绘制有符号 \(T_\ell\)、同时 95% 区间和零线，并突出 \(\mathcal L^+\)，不得过滤其余层。
7. 本 Anchor 下不执行 PCA、协方差特征分解、公共基、聚类、最小检索秩、Router 训练或专家评估。

## 6. Minimal Falsification Tests

在能力、数据、身份、泄漏和记录 guards 全部有效时：

**Pass — `CONDITIONAL_FINE_ADDED_ACCESSIBILITY_FOUND`：**\(\mathcal L^+\) 非空。Pass 只准入集合中的具体层进入后续低秩研究。

**Fail — `NO_REGISTERED_LAYER_EXCEEDS_MATCHED_CONTROLS`：**每个合格层的 \(T_\ell\) 同时 95% 置信上界都不大于零。它只关闭当前模型、taxonomy、线性 residual-update 定义，不能证明不存在非线性或模型原生信息。

**Insufficient：**没有层通过，但至少一个关键区间跨零；或者任务能力、分支身份、数据独立性、对照有效性、提取或 provenance guard 失败。

preflight 没有科学 verdict。任何数据、身份、known-case、拟合或对照 guard 失败，都必须在打开 CONFIRMATION 前停止；只有完整全层确认评估才能给出 Pass、Fail 或 Insufficient。

## 7. Current Evidence

1. [A15_02_05](../../../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_05_E01_balanced_taxonomy_attention_write_atlas/summary.md) 得到可复现 conditional-fine residual，但没有稳定的 fine-specific 本地秩后移；几何不能回答条件新增性。
2. [A15_02_07 TAX](../../../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_07_E01_matched_taxonomy_full/summary.md) 得到更新可读性，却没有当前严格的同一 \(X\) 条件增益门。它支持复用 taxonomy，不继承正结论。
3. [A15_07](../../15_07_layerwise_conditional_fine_discriminant_directions/15_07_layerwise_conditional_fine_discriminant_directions_anchor_cn.md) 提出低秩 conditional-fine 判别方向，但因必须先完成功能新增门而暂停且未运行。
4. [A15_08_E04](../../../../experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/summary.md) 在 block 25 的受控两跳目标上得到合格的局部 added accessibility，而 rank two 只保留 full point gain 的 33.24%。它验证测量纪律，不验证本 taxonomy 假设。
5. [A15_08_01_E02](../../../../experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_01_E02_layerwise_long_range_gain_and_representation_rank_blocks_2_36/summary.md) 表明有利的 depth interaction 不能替代有符号绝对收益；该实验中 remote two-hop 的绝对收益反而下降。本继承问题因此直接画逐层同预算净收益。

6. [A15_08_02_E01](../../../../experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_02_E01_layerwise_conditional_fine_added_accessibility/summary.md) 已于 2026-08-16 完成全部 block 的冻结确认。block 1 因固定 decision token 的旧状态恒定而按规则记为结构性 N/A；blocks 2--36 全部进入同一同时校正。注册 verdict 为 `CONDITIONAL_FINE_ADDED_ACCESSIBILITY_FOUND`，且

\[
\mathcal L^+=\{24,28\}.
\]

block 24 的 \(T_{24}=0.1087\)、同时 95% 区间 \([0.0526,0.1649]\)；block 28 的 \(T_{28}=0.0653\)、区间 \([0.0239,0.1067]\)。block 25 虽有正点估计 \(T_{25}=0.0693\)，但区间 \([-0.0073,0.1460]\) 跨零，不能准入。能力、同一 base logits、64 个 mismatch bank、张量身份和重建 guards 全部通过。

## 8. Claim Boundary And Next Decision

本实验最多证明：对一个冻结模型、一个 conditional-fine taxonomy、一个 decision token、一个同层归一化 attention transition 和一个注册线性读出族，某些具名层相对完全相同的旧状态 base 以及注册目标无关同预算对照，增加了留出 child 可访问性。

即使 Pass，也不能证明收益随深度单调、表征低秩、存在跨层共享空间、形成语义聚类、MLP 原生使用、专家专门化、Router 有效、因果必要性或自然语言普适性。这些都需要独立后续实验。

**唯一下一决策：**是否把已准入的 blocks 24、28 及其后续确认的 rank-256 功能保留空间送入独立的冻结干预或 Router 效用实验。该决策不属于本 Anchor，也不会由本结果自动授权。

**完成条件：已满足。**冻结 Protocol、全层表格、同时区间、两张主图、运行收据和 artifact manifest 均已归档于 [A15_08_02_E01](../../../../experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_02_E01_layerwise_conditional_fine_added_accessibility)。

**恢复动作：**无需重跑本实验。后续只能把 blocks 24、28 称为本任务、本读出族下的功能准入层；block 25 仍是未决层，其几何不能获得“新增细类信息”解释。

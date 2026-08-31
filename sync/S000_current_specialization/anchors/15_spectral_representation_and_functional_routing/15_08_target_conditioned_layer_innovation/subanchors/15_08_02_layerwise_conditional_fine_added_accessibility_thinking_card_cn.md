---
card_id: 15_08_02_layerwise_conditional_fine_added_accessibility
owner: researcher
status: COMPLETED_PASS_LAYERS_24_28
parent_anchor: ../15_08_target_conditioned_layer_innovation_anchor_cn.md
created: 2026-08-16
updated: 2026-08-16
---

# Thinking Card：逐层 conditional-fine 新增可访问性

## 研究者当前判断

1. 最终目标仍是找到一个对各层新增细粒度信息敏感、并可用于后续分发的低维空间。
2. 当前公认的两个假设是：深层累计表征更能区分同一粗类内部的细类；完成这种区分所需的新增表征可以由低秩空间保留。
3. 但低秩分析必须排在功能门之后：先证明某层更新在同一旧状态之外增加了细类可访问性，再研究承载该增益的最小维数。协方差、PCA、公共基或聚类都不能替代这道功能门。
4. 第 25 层只提供既有状态提取与 added-accessibility 度量证据，不再作为单独 smoke 或选择层；后续获执行授权后直接按前向顺序处理所有 block。
5. block 1 仍执行结构检查；若固定 decision token 上的 $X_1$ 为结构性常数，则在全层结果中明确标为不合格，不能被静默删除或伪装成零收益。预期可裁定集合为 blocks 2--36。
6. 全层结果必须按层从前向后完整呈现。图中展示每层**有符号**收益、零线和置信区间，并标出置信下界大于零的层；不能只画正值或删除不符合预期的层。
7. old-only 与 old-plus-update 两个分支必须使用完全相同的 $X_\ell$、同一冻结 base logits 和同一批样本；新增分支只能多一个由候选更新产生的同预算 correction。

以上 1--7 来自 [0816 sync](/daily_research_reports/0816/docs/sync.md) 与研究者 2026-08-16 的明确指示，不是 AI 自行扩展的研究方向。

## 当前唯一机制问题

在已知父类、预测父类内部 child 的任务上，第 $\ell$ 层同一 decision token 的 attention transition 是否在旧状态 $X_\ell$ 之外，增加了未见表达上的 child 可访问性？

同层对象固定为

$$
X_\ell=N_\ell(h_\ell),\qquad
Z_\ell=N_\ell(h_\ell+a_\ell),\qquad
U_\ell=Z_\ell-X_\ell,
$$

$$
R_{U,\ell}=U_\ell-\widehat{\mathbb E}_{lin}[U_\ell\mid X_\ell].
$$

$R_{U,\ell}$ 只是“旧状态在线性预测器下不能预测的更新”；只有它在留出数据上给同一 $X_\ell$ base 带来超过同预算目标无关对照的交叉熵下降，才可称为本实验意义下的新增细类可访问性。

## 最强竞争解释

正收益可能不是更新携带了目标相关新增量，而只是：

- 第二个 correction 分支增加了参数容量；
- old-only 读出未充分拟合，复制 $X_\ell$ 也能继续降低损失；
- 更新与细类的相关性来自模板、表达或样本配对捷径；
- 更深层 old state 的损失余量不同，使原始增益不能直接跨层比较。

因此所有真更新分支必须与“同一 $X$ 的 duplicate-$X$ correction”和“同维、同训练预算的父类内样本错配更新”比较。

## 什么证据会改变判断

- 若所有合格层的真更新分支都不能超过目标无关/duplicate-$X$ 对照，则认识更新为“当前线性定义下没有层级新增细类证据”。
- 若若干层的原始增益为正、但不超过同预算对照，则认识更新为“存在 correction headroom，尚无新增细类证据”。
- 若部分层超过同预算对照，则只准入这些具名层进入后续低秩分析；不能把一个正层外推为所有层或单调深度规律。
- 只有全新、未用于选择的 CONFIRMATION 上，全层同时校正后的正收益集合非空，才支持“至少一个层的更新增加了 conditional-fine 可访问性”。

## AI_PROPOSAL：为使判断可执行而补充的冻结项

1. 使用既有 8 父类 × 8 child TAX taxonomy 的 TRAIN/DEVELOPMENT 表达完成全层拟合；正式裁定前另生成并冻结一份表达、模板和内容家族互斥的新 CONFIRMATION bank。
2. 把每层主量定义为真更新增益超过 duplicate-$X 与 64 个父类内平衡样本错配更新的较强者；全层用同一次 max-statistic 同时校正。
3. block 1 仍提取和记录，但若其固定 decision token 的 $X_1$ 结构性常数检查复现，则标为 `STRUCTURALLY_INELIGIBLE`；正式曲线覆盖 blocks 2--36，并在 x=1 明示 NA，而非静默删除或写成零。

## 结果更新与唯一下一决策

全层功能实验已完成：block 1 结构性 N/A，blocks 2--36 全部完成同一确认评估，功能准入集合为 $\mathcal L^+=\{24,28\}$；block 25 的同时区间跨零，保持未决。这个结果否定“越深每层新增越多”的整体叙事，只支持局部具名层。

唯一下一决策是：是否把 blocks 24、28 及后续得到的 rank-256 功能保留空间送入独立的冻结干预或 Router 效用检验。当前结果不自动授权训练或路由实验。

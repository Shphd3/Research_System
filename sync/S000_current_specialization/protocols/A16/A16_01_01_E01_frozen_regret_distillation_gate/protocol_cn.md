---
experiment_id: A16_01_01_E01_frozen_regret_distillation_gate
anchor_id: 16_01_01_regret_distilled_conditional_innovation
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-12
design_frozen_at: 2026-08-12
resource_profile: 5090-8-spot
primary_metric: document_paired_heldout_expert_choice_regret
---

# Protocol：A16_01_01_E01 冻结模型的效用蒸馏准入门

## 0. Approval Snapshot

**目的：** 判断真实同层增量去除旧状态可预测部分后，是否保留可泛化的专家相对效用。

**实验角色：** 长训练前的功能准入门。

**处理与对照：** 在同一冻结 Native-LB 10B checkpoint 上比较 Native、Raw-Utility、Conditional-Utility 和 Conditional-Haar-Utility。只改变残差化与 rank-56 特征框架；backbone、experts、Native Gate、功能文档、教师 loss、拟合预算与确认集保持一致。

**主指标：** 目标 token 局部 expert-choice regret，单位 nat/token；先在每个文档内对八个位置和四层平均，再做文档配对 bootstrap。

**Pass：** seed 17 和 seed 29 分别满足 Conditional 相对 Native、Raw、Haar 三个 regret 差的 95% 上界都小于零。**Fail：** 合格完整证据未满足任一必要比较。**Insufficient：** checkpoint、split、强制专家局部性、cross-fit、数值、artifact 或恢复身份失败。

**已批准范围：** Protocol、实现、单元测试、单卡 smoke、一个覆盖全 arm 的 8×5090 smoke，以及两个完整冻结 gate 任务。只有本实验 Pass，E02 才可无需再次审批自动提交。

**不能声称：** Pass 不证明 30B NLL、长期专家专业化、语义新增或冻结局部教师之外的效用。

## 1. Terminology / Definitions

- $x$：本层 Attention 写入前的归一化 token 状态。
- $u$：Attention 写入后实际 Router 输入减去 $x$。
- $r=u-Ax$：不能由 $x$ 线性预测的标准化增量。
- 局部强制 expert：只直接改变注册 token 在注册层的 sparse expert；其余位置与层继续由 Native Router 策略决定，因此下游 route 可以因隐藏状态变化而响应，并非冻结为基线 route ID。候选 expert 统一沿用 Native winner 的 top-1 mixture 权重，从而比较匹配 mixture scale 下的 expert 功能。
- regret：Router 选择 expert 的强制 loss 减去八个 expert 的最小强制 loss。
- 教师：$q_e\propto\exp[-(\ell_e-\min_j\ell_j)/0.1]$。

## 2. Anchor Alignment

父实验到 20B 未建立两 seed 的 Trainable 优势，之前所有 expert-utility 门也失败。本实验修复监督对象而不更换表示对象：保留 Native Router，只让 dormant rank-56 分支直接学习专家相对效用。最强竞争解释是条件残差没有泛化效用，或任意同维旁路都等价。

## 3. Tested Hypothesis

用 $r$ 做直接效用蒸馏，能够在两个 seed 上同时降低相对 Native、Raw-Utility 与 Conditional-Haar 的 held-out regret。

## 4. Rival Explanations

| 竞争解释 | 区分比较 |
| --- | --- |
| Native 已用尽可访问效用 | Conditional vs Native |
| 只需要效用监督，不需要残差化 | Conditional vs Raw |
| 任意 rank-56 视角都有效 | Conditional vs Haar |
| 全局最佳 expert 偏置即可 | intercept-only 与文档打乱教师 guard |
| 教师干预无效 | route replay 与 target-locality 测试 |

## 5. Data Construction And Provenance

使用冻结 A16 E2 bank：384 个独立 DCLM 文档，每文档 256 token；FIT、DEVELOPMENT、CONFIRMATION 各 128 个完整文档，每文档八个固定目标位置。tensor 与 manifest SHA-256 必须分别为 `827129cdf5b1d44af06a034b607e40c98d5353ac8e5276b994b906c917479fd5` 和 `0a8a00d2370735821bb553fcc5f27a8c7c0006a749e4d5b4628c8df2ee6f0192`。

seed 17 只用自己的 Native `checkpoint-12716`，模型 hash 为 `3d7c945006bfcc93f3c071089e086c9a0d9e13766c23d17af50e09fac2f7946e`；seed 29 对应 hash 为 `c89ce4d8d78109fe27c44d89c80e96fa6334ae4ed4ea0cbf68aad39f4573998c`。禁止跨 seed 加载。

FIT 参与标准化、residualizer 和分支拟合；DEVELOPMENT 只在注册 ridge 候选中选择；所有选择与 artifact hash 冻结后，CONFIRMATION 只打开一次。

## 6. Learning Task And Permitted Supervision

对每个目标 token 和层，用 Native logits 加一个低秩分支预测八个专家的相对效用分布。唯一允许的监督是局部强制 expert loss 向量；taxonomy label、终点 NLL、confirmation 结果和未来层状态都禁止进入拟合。

## 7. Model / Architecture And Frozen Variants

用 FIT 统计标准化 $x,u$。Conditional 条件在 FIT 内按文档五折拟合 $u\approx xA$，部署只保存 $C=AP$，计算 $f=uP-xC$。Raw 使用 $f=uP$。Conditional 学习 rank-56 $P$；Haar 使用 seed 固定的同维正交 $P$。所有条件形状一致，模型与专家参数不收梯度。

## 8. Training Objective And Optimization

教师温度固定 $0.1$ nat。用确定性 ridge reduced-rank 解最小化 $KL(q\|\operatorname{softmax}(z))$。residualizer 与 utility ridge 候选固定为 `$10^{-4},10^{-3},10^{-2},10^{-1},1,10`；DEVELOPMENT regret 选择，完全相同时选更小 ridge。rank 固定 56，不能由结果选择。

## 9. Conditions, Seeds, And Checkpoints

| 条件 | 特征 | 作用 |
| --- | --- | --- |
| Native | 无新增分支 | 基线 |
| Raw-Utility | 标准化 $u$ 的学习 rank-56 视角 | 残差化对照 |
| Conditional-Utility | 标准化 $u-Ax$ 的学习 rank-56 视角 | 主处理 |
| Conditional-Haar | 标准化 $u-Ax$ 的固定 Haar rank-56 视角 | 维度与容量对照 |

两个 seed 都在各自冻结 Native 10B state 内完成全部条件。

## 10. Primary Metric And Frozen Analysis Plan

$$R=\ell_{\arg\max_e z_e}-\min_e\ell_e.$$

每文档先对四层与八位置平均。每个 seed 对 128 confirmation 文档计算 Conditional 减 comparator，做 2,000 次配对文档 bootstrap，报告双侧 percentile 95% 区间；Pass 使用上界小于零。token、层和位置不能伪装成独立样本。缺少任一注册文档则该 seed 为 Insufficient。

## 11. Secondary Metrics And Guards

报告逐层 regret、oracle top-1 agreement、到 $q$ 的 KL、residual prediction $R^2$、feature/logit RMS、相对 Native 的 route flip、expert share、intercept-only 与 shuffled teacher。它们只能解释主结果，不能挽救主指标 Fail。

## 12. Known Good / Known Bad / Known Confusing Cases

合成的单条件残差教师必须能被恢复并超过 Native/Haar；打乱 loss 不得通过；KL 下降但 regret 不下降不构成功能准入；单层趋势不能替代注册聚合结果。

## 13. Scientific Procedure And Stage Contracts

| 阶段 | 目标 | 操作 | 放大条件 | 产物 |
| --- | --- | --- | --- | --- |
| P0 | provenance | hash/schema/split/局部性审核 | 全通过 | `preflight.json` |
| P1 | 算法 | 合成数据 red/green 单测 | 全套通过 | test receipt |
| P2 | 真实小路径 | 提取、蒸馏、安装、保存恢复 | no-op/tamper/gradient guard 通过 | 单卡 receipt |
| P3 | 分布式路径 | seed17 全 arm 8×5090 smoke | rank 一致且可重建 | distributed receipt |
| P4 | 科学门 | 两 seed 全 bank | typed verdict | regret arrays/decision JSON |

## 14. Algorithm, Output, And Provenance Contract

不可变 utility artifact 存储 checkpoint/bank hash、seed、FIT 标准化、residualizer ridge、$P,C$、初始 $B$、冻结教师 $B_T$、Native Gate snapshot、条件标签、层号与整体 SHA-256。只有该 artifact 可初始化 E02。新输出不能覆盖 A16_01_E01。

## 15. Success / Failure / Insufficient Evidence

- Pass：三个注册聚合 regret 对比在两个 seed 均通过。
- Fail：合格完整证据未通过，包括没有共同方向优势。
- Insufficient：provenance、split、干预、数值、分布式或 artifact 身份失败。

## 16. What This Cannot Claim

不能证明在线训练收益、全局专家专业化、固定局部干预以外的效用、跨尺度普遍性，或 residualization 等于语义新增。

## 17. Block Confirmation, Freeze, And Amendment Ledger

A-G 均由用户 2026-08-12 的明确执行指令确认，跨块一致性为 PASS。科学正文在 P1 前冻结。启动后若改变数据、温度、residualizer、rank、条件、主聚合或 verdict，必须追加 amendment 并审计 eligibility。Git、graph、sync、commit、push 未授权。

### Amendment 2026-08-12-A：部署 logits 的同前向测量

首轮真实执行在打开 CONFIRMATION 前由 Native replay 守卫停止：两个 seed 各有 7/8192 个近边界样本因 BF16 状态差分与不同 batch 形状重算而改变 winner。审计确认 Router 对象仍为 $x+u$，并非科学对象失配。执行合同据此只修复测量路径：$x,u$、部署 Native logits 与 winner 必须在同一个 batch-size-1 Native forward 中联合捕获；保存的 winner 必须是保存 logits 的精确共同最大值。由 $x+u$ 与 Gate 权重重构 logits 降为数值诊断，不能替代部署 logits。数据、条件、监督、rank、主指标、阈值和 verdict 均不变；旧尝试保留为 Insufficient 工程证据，新 schema 与新 worker hash 必须在新 evidence root 全量重提。

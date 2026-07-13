# MTP 五个核心问题的当前答案

## 0. 执行摘要

**上层问题：** 在长程组合任务上，MTP 相对 NTP 的作用、容量边界和课程机制目前能够被证据支持到什么程度？

**统一机制解释：**

1. MTP 的局部作用由额外未来梯度相对标准梯度的方向决定，但该关系只有在任务已学会后才具有任务解释。

$$
\Delta L_N^{joint-NTP}
=-\eta\lambda g_N^\top g_A+O(\eta^2).
$$

2. 在受控线性模型中，独立任务因素超过共享表示秩时会发生结构性竞争；课程只能改变优化路径，不能创造缺失的表示维度。

$$
r<r_{required}\Rightarrow\text{factor displacement},
\qquad
r\ge r_{required}\Rightarrow\text{simultaneous representation possible}.
$$

**主要结果：**

1. 原始序列任务尚未形成有效神经实验表面：所有深度、训练时长、宽度和显式 pair-token 修复都停留在八分类机会水平附近。
2. 低秩竞争在 oracle-factor 线性模型中得到因果支持：rank 1 的 MTP 标准损失代价为 `0.9084--1.0218`，rank 2 时消失到数值零。
3. 等辅助剂量课程不能修复结构性 rank-1 瓶颈，真实模型/真实数据迁移因此仍无资格启动；Router 保持 parked。

**证据说明：**

1. `3L-128d-3000` 的 train 答案准确率 `0.1249`、validation `0.1211`；显式 pair-token 的五 seed test 为 `0.1274--0.1353`。
2. A11_24 在 `5/5` seed 上满足 rank-1 penalty 和未来因子改善，rank-2 最大绝对 gap 仅 `1.23e-13`。
3. A11_25 rank-1 课程标准收益仅 `-0.00213` 到 `+0.000134`，Pareto pass 为 `0/5`；rank 2 两种 schedule 都接近零损失。

**结论边界：** 当前支持的是局部梯度公式和线性低秩机制，不支持“小模型 Transformer 已因容量而受损”、大模型 MTP 优势、神经课程收益、真实长文本迁移或 Router 方法。

**执行动作：** 停止继续调从头训练的小序列模型；下一步只选择一个已有两跳能力的预训练小模型或显式结构化神经桥，先通过任务 gate，再测 rank/safe-update 指标能否预测标准主头 MTP/NTP 差异。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算 | 为什么重要 | 不能证明什么 |
|---|---|---|---|---|
| 工作负载 | 模型必须完成的真实计算 | 多个远程证据联合决定答案 | 定义方法要解决的问题 | MTP 自动有效 |
| NTP | 下一词元预测 | 标准主头预测紧邻词元 | 公平基线 | 长程变量形成 |
| MTP | 多词元预测 | 额外预测更远未来词元 | 提供直接未来梯度 | 标准主头一定改善 |
| 任务 gate | 模型已学会任务的资格条件 | held-out 答案准确率门槛 | 防止解释随机梯度 | 通用能力阈值 |
| 结构性秩竞争 | 表示方向不足导致因素互相挤占 | 显式 rank 1 对比 rank 2 | 因果测试容量假设 | Transformer 全局容量 |
| Pareto 改善 | 标准目标变好且未来目标不变差 | 标准 loss gain 与 auxiliary MSE cost | 排除少学辅助目标的假改善 | 真实课程泛化 |

## 2. 机制解释与建模

**核心模型：**

1. 局部梯度模型只比较同起点的一步更新：

$$
\theta_N'=\theta-\eta g_N,qquad
\theta_M'=\theta-\eta(g_N+\lambda g_A).
$$

负内积只表示联合更新相对 NTP-only 留下更高标准损失，不代表损失相对更新前绝对上升。

2. 组合 workload 的潜变量关系是：

$$
B=\pi_1(A),\qquad Y=\pi_2(B).
$$

单表不足、双表充分是数据性质；模型是否学会必须另测。

3. 低秩模型把局部因素 $u$ 和未来因素 $z$ 压进 rank-$r$ 的共享表示。rank 1 只能优先保留一个独立方向；rank 2 可以同时保留两个。

**被合并的问题：**

1. workload 与长程语义如何定义；
2. MTP/NTP 应比较哪个最终量；
3. 小模型为何可能更差、大模型为何可能更好；
4. 课程为何可能有效；
5. 当前证据能否迁移到真实模型并支持 Router。

## 3. 主要结果

**一句话总结：** 容量竞争在受控线性模型中成立，但神经序列桥没有学会任务，因此大模型、课程、真实迁移和 Router 结论尚未建立。

### 结果 1：序列校准失败发生在训练拟合阶段，而非只发生在泛化阶段

**来源结果：** A11_23 与 A11_23b。  
**机制对应：** 任务 gate。  
**指标或条件定义：** 八分类机会水平 `0.125`，操作通过线 `0.70`。  
**证据说明：** 原始序列最强条件 train `0.1249`；显式绑定五 seed test 最高 `0.1353`。  
**边界：** 不能断言预训练 Transformer 或结构化模型无法组合。

![显式绑定校准曲线](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_23b_explicit_binding_calibration/figures/curves.png)

### 结果 2：显式表示秩决定受控模型中 MTP 是否损害标准目标

**来源结果：** A11_24。  
**机制对应：** 结构性表示竞争。  
**指标或条件定义：** MTP-minus-NTP 标准 test loss。  
**证据说明：** rank 1 gap `0.9084--1.0218`，同时未来 MSE 在 5/5 改善；rank 2 gap 约零。  
**边界：** 这是 oracle-factor 线性模型，不能用参数量直接外推到 LLM。

![秩条件下的 MTP 干扰](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_24_task_rank_competition/figures/rank_phase.png)

### 结果 3：课程不能修复结构性秩不足，只可能处理优化路径问题

**来源结果：** A11_25 与 A11_26 gate。  
**机制对应：** 表示维度与训练顺序的边界。  
**指标或条件定义：** 等辅助剂量下的 Pareto pass。  
**证据说明：** rank 1 pass `0/5`；rank 2 静态/课程均为数值零；真实迁移因 neural task gate 失败而 parked。  
**边界：** 不否定预训练神经网络中的非凸路径、有限预算或优化器状态收益。

![等剂量课程 Pareto 检验](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_25_curriculum_rank_boundary/figures/pareto.png)

## 4. 执行动作

**下一步动作：** 使用一个已知具备两跳能力的预训练小模型或显式两阶段神经组合器，先验证 held-out task gate，再在同一 checkpoint 上测局部梯度、任务 Jacobian 谱参与率和安全更新比例。

**目的：** 建立“线性 rank 机制”到“可学习神经模型”的中间桥，决定大模型与课程问题是否值得继续。

**完成判据：** `5/5` seed/task split 通过答案门槛；结构指标能预注册地预测标准主头 MTP/NTP 差异；否则停止容量解释，不进入 Router。

## 5. 证据索引

| 结果 | 来源 | 主要证据 | 支持什么 | 不能证明什么 |
|---|---|---|---|---|
| 结果 1 | A11_23/23b | train/test 均近 `0.125` | neural surface 无效 | 所有模型不能组合 |
| 结果 2 | A11_24 | rank-1 gap 约 `0.963`，rank-2 约零 | 线性 rank 因果 | LLM 尺度律 |
| 结果 3 | A11_25/26 | Pareto `0/5`，transfer gate=0 | 课程/迁移边界 | 神经课程无效 |

## 6. 来源索引

**Included anchors：** [A11_23](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_23_composition_calibration_anchor_cn.md)、[A11_23b](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_23b_explicit_binding_calibration_anchor_cn.md)、[A11_24](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_24_task_rank_competition_anchor_cn.md)、[A11_25](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_25_curriculum_rank_boundary_anchor_cn.md)、[A11_26](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_26_scale_real_transfer_gate_anchor_cn.md)。  
**Included protocols：** [A11_23](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_23_composition_calibration/protocol_cn.md)、[A11_23b](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_23b_explicit_binding_calibration/protocol_cn.md)、[A11_24](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_24_task_rank_competition/protocol_cn.md)、[A11_25](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_25_curriculum_rank_boundary/protocol_cn.md)。  
**Included summaries：** [A11_23](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_23_composition_calibration/summary.md)、[A11_23b](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_23b_explicit_binding_calibration/summary.md)、[A11_24](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_24_task_rank_competition/summary.md)、[A11_25](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_25_curriculum_rank_boundary/summary.md)。  
**Included detailed records：** [A11_23](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_23_composition_calibration/detailed.md)、[A11_23b](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_23b_explicit_binding_calibration/detailed.md)、[A11_24](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_24_task_rank_competition/detailed.md)、[A11_25](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_25_curriculum_rank_boundary/detailed.md)。  
**Included figures：** calibration curves、rank phase、curriculum Pareto。  
**Excluded material and reason：** Router 与真实 benchmark 未运行，因为 neural transfer gate 未通过。

## 7. 补充材料

### 给导师的五个具体回复

1. **工作负载是什么？** 目标是“多个远程证据单独不足、联合后按结构组合才能确定答案”的任务；当前置换数据严格实现了联合必要性，但小型从头训练 Transformer 尚未学会它，所以该数据还不是有效的神经机制实验表面。
2. **MTP 与 NTP 怎么比较？** 最终必须比较相同标准主头、相同标准目标和匹配训练预算下的答案 loss/accuracy；辅助头、probe 和梯度只用于解释为什么变化，不能替代最终结果。
3. **为什么小模型可能更差、大模型可能更好？** 受控线性实验表明，当共享表示只有一个方向却要承载两个独立因素时，MTP 会把标准方向挤掉；增加到两个方向后代价消失。但这只证明 rank 机制，大模型是否具有更高“任务相关安全容量”仍需神经桥验证。
4. **课程学习为什么可能有效？** 课程不能创造缺失的表示维度；本实验中 rank 1 的等剂量课程 `0/5` 改善。它只能在容量已足够时，通过非凸路径、有限预算或优化器状态缓解早期冲突。
5. **什么是长程语义和组合关系？** 长程语义是局部窗口无法替代、对无关改写稳定、对关键远程证据干预敏感的任务变量；组合关系是多个证据经过明确中间变量或算子得到答案。当前只完成了合成定义和线性机制，尚未完成自然语言验证。

### 30 秒汇报

> 我们完成了 planned anchors。原始和显式绑定的序列任务都停在随机水平，说明当前小型从头 Transformer 不是有效机制表面；但在剥离检索与绑定后的线性模型中，rank 1 时 MTP 标准损失比 NTP 高约 0.96，rank 2 时差异消失，支持结构性秩竞争。等辅助剂量课程在 rank 1 上 0/5 改善，说明课程不能补出缺失维度。所以下一步不是 Router，也不是直接跑真实 benchmark，而是用已有两跳能力的预训练小模型建立 neural bridge，再验证任务相关 rank 和安全更新比例。

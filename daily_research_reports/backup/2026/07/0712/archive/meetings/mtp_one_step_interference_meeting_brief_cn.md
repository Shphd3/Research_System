# MTP 的局部梯度作用是否解释标准 NTP 退化

## 0. 执行摘要

**研究问题：** 第二未来词元监督对标准自回归目标的一步影响能否被定量解释，并据此进入容量与课程学习研究？

**机制解释：**

1. 在相同 checkpoint 和 batch 上，联合更新相对 NTP-only 更新造成的标准损失差，一阶上由两个梯度的内积决定。

$$
\Delta_{obs}
=L_N\!\left(\theta-\eta(g_N+\lambda g_A)\right)
-L_N(\theta-\eta g_N)
=-\eta\lambda g_N^\top g_A+O(\eta^2).
$$

2. 该局部公式只有在模型先学会组合任务后，才有资格被解释为“任务相关的 MTP 干扰”。本实验预注册的资格门槛是：

$$
A_{answer}^{val}\ge0.70.
$$

**主要结果：**

1. 小步长下，一阶梯度公式准确预测了联合更新相对 NTP-only 更新的标准损失差。
2. 单层模型没有学会两跳组合，因此“任务相关 MTP 干扰”仍是证据不足，而不是已成立机制。
3. 容量、课程与尺度问题尚未开启；唯一下一步是先建立一个已知可学习的组合 checkpoint，再原样复跑本审计。

**证据说明：**

1. 相对参数步长 $10^{-5}$ 下，预测—实测斜率为 `1.0174`，Pearson 相关为 `0.9990`，符号一致率为 `1.0000`，中位归一化残差为 `0.1012`。
2. seeds `971--975` 的验证格式准确率均为 `1.0`，但八分类答案准确率均为 `0.125`，与随机猜测相同。
3. A11_01--A11_20 已有完整 protocol/summary/detailed；A11_21 明确停放；A11_22 已闭环但结论为证据不足；A11_23--A11_26 尚未开启。

**结论边界：** 当前只支持受控两位置目标下的小步长局部微分关系，不支持完整语料 NTP、长期 MTP 退化、容量尺度律、课程机制或真实语言收益。

**执行动作：** 保持数据、目标、seed 和有限差分方法不变，只修复组合架构的可学习性；`5/5` seed 的 held-out 答案准确率达到 `0.70` 后，复跑同一 A11_22 审计。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算方式 | 单位或公式 | 为什么影响当前判断 | 不能证明什么 |
|---|---|---|---|---|---|
| 下一词元预测（NTP） | 用当前位置预测紧邻的下一个词元 | 本实验只在两个受控位置计算标准损失 | 交叉熵，nat | 是两条件共享基线 | 完整语料的 all-token NTP 性能 |
| 多词元预测（MTP） | 同一隐藏状态同时预测多个未来词元 | 本实验只增加第二未来答案损失 $L_A$ | 交叉熵，nat | 产生额外共享参数梯度 | 普遍 MTP 效果 |
| 受控标准目标 $L_N$ | NTP 与 MTP 都优化的共同目标 | 决策位置格式损失加下一位置答案损失 | nat | 保证比较公平 | benchmark 性能 |
| 辅助目标 $L_A$ | MTP 独有的直接未来答案监督 | 用决策状态和 tied standard unembedding 预测答案 | nat | 定义额外梯度 $g_A$ | 独立 MTP head 的行为 |
| 一步损失差 $\Delta_{obs}$ | 加入辅助梯度后，相对 NTP-only 多留下多少标准损失 | 两个同起点模型做配对一步更新 | nat | 直接观察局部帮助或损害 | 完整训练收敛 |
| 校准门槛 | checkpoint 是否已学会组合任务的操作标准 | held-out 八分类答案准确率至少 `0.70` | 概率 | 决定机制解释资格 | 理论必要条件或通用阈值 |
| 机会水平 | 完全猜测时的答案准确率 | $1/8$ | `0.125` | 判断任务是否学会 | 数据永远不可学 |

## 2. 机制解释与建模

**核心模型：**

1. 两个比较条件从相同参数出发，只改变是否加入辅助梯度。

$$
g_N=\nabla_\theta L_N,\qquad
g_A=\nabla_\theta L_A,
$$

$$
\theta_N'=\theta-\eta g_N,qquad
\theta_M'=\theta-\eta(g_N+\lambda g_A).
$$

2. 若 $L_N$ 在当前参数附近二阶可微，则完整的二阶展开为：

$$
\Delta_{obs}
=-\eta\lambda g_N^\top g_A
+\eta^2\lambda g_N^\top H_Ng_A
+\frac{\eta^2\lambda^2}{2}g_A^\top H_Ng_A
+O(\eta^3),
$$

其中 $H_N=\nabla_\theta^2L_N(\theta)$。因此：

- $g_N^\top g_A<0$：联合更新后的 $L_N$ 高于 NTP-only 更新后的 $L_N$；
- $g_N^\top g_A>0$：联合更新在一阶上帮助 NTP-only；
- 两者都不等价于 $L_N$ 相对更新前绝对上升或下降。

3. 合成任务要求复合两个独立置换：

$$
B=\pi_1(A),\qquad Y=\pi_2(B).
$$

随机置换构造保证给定查询时，单独任一张表不能确定答案，两张表联合完全决定答案。

若两张置换表独立且均匀采样，则该性质可写为：

$$
I(Y;\pi_1\mid A)=0,\qquad
I(Y;\pi_2\mid A)=0,
$$

$$
I(Y;\pi_1,\pi_2\mid A)=H(Y\mid A)=\log 8.
$$

这只证明数据生成分布具有“单证据不足、联合证据充分”；它不证明序列距离本身造成困难，也不证明 Transformer 已学会组合。

**符号含义：**

- $\theta$：共享模型参数；$\eta$：一步更新尺度；$\lambda=1$：辅助损失权重。
- $g_N,g_A$：共同目标与辅助目标对同一参数的梯度。
- $H_N$：共同目标在当前 checkpoint 的局部 Hessian。

**机制链条：**

1. 先要求 checkpoint 学会组合任务，否则梯度不是“已学习任务中的冲突”。
2. 再用配对有限差分判断一阶内积是否预测真实一步差异。
3. 只有二者同时通过，才测容量；只有找到低容量损害区，才测课程。

**理论检查与修正：**

- 梯度余弦只给方向，不给真实损失量级；主指标必须是有限差分一致性。
- `0.70` 是预注册操作门槛，不是信息论定理。
- 低秩竞争只在白化线性输入、平方损失、最优线性读出和固定秩约束下可直接推导。此时共享子空间选择

$$
M_\lambda=T_N^\top T_N+\lambda T_A^\top T_A
$$

的前 $r$ 个特征方向；只有辅助方向挤出标准方向时才构成可证明的表征竞争。该结论不能直接外推到 Transformer。

- Transformer 的“容量”只能先定义为任务和 checkpoint 相关的局部量，例如联合 Jacobian 谱参与率

$$
r_{joint}=\frac{(\operatorname{tr}K)^2}{\operatorname{tr}(K^2)},qquad
K=J_{joint}J_{joint}^\top,
$$

以及一阶安全更新比例

$$
S_{safe}=\frac{\|P_{\ker J_N}g_A\|^2}{\|g_A\|^2}.
$$

二者都依赖任务、数据、checkpoint 和数值零空间阈值，不能称为全局模型容量。

- 若优化问题凸、最终目标相同且都收敛到同一全局最优解，课程顺序不应改变最终解。因此课程收益只能来自有限训练预算、非凸路径依赖、优化器状态或表征锁定；实验必须匹配总更新量和辅助损失剂量。

## 3. 主要结果

**一句话总结：** 一阶局部公式通过，但任务校准失败，因此当前没有得到 MTP 在已学会组合任务上造成干扰的结论。

### 结果 1：小步长下，一阶项准确预测配对的一步标准损失差

**机制对应：** 检验 $\Delta_{obs}=-\eta\lambda g_N^\top g_A+O(\eta^2)$。

**指标或条件定义：** 主指标是 $\Delta_{obs}$ 对 $\Delta_{pred}$ 的过原点回归斜率；相关、符号一致率和归一化残差为有效性守卫。

**证据说明：**

- $10^{-5}$：斜率 `1.0174`、相关 `0.9990`、符号一致率 `1.0000`、残差 `0.1012`。
- 步长增至 $10^{-4}$ 后，斜率变为 `1.3202`、残差升至 `1.0676`，说明大步长已不能忽略曲率。

![一步损失预测与实测一致性](../../../../../../../Projects/from-attention-to-search/main/experiments/A12/archive/12_02_capacity_diagnostics/A12_02_01_D01_ineligible_one_step_interference/figures/prediction_fidelity.png)

**解释：** 最小步长点接近恒等线，且误差随步长增加，符合局部 Taylor 展开的预期。

**边界：** 只支持共享读出、受控目标和当前 checkpoint 附近的局部关系。

**来源：** A11_22 summary、detailed、`step_size_summary.csv` 与主图。

### 结果 2：任务校准失败，阻止局部公式升级为 MTP 学习机制

**机制对应：** 任务梯度解释要求 checkpoint 先通过组合能力门槛。

**指标或条件定义：** held-out 八分类答案准确率；预注册门槛 `0.70`，机会水平 `0.125`。

**证据说明：**

- 五个 seed 的答案准确率全部为 `0.125`；
- 同时格式准确率全部为 `1.0`，说明模型学会局部格式，却没有学会两跳答案。

**解释：** 数值微分可以正确，但当前梯度仍来自未掌握组合函数的模型，不能用于解释学会任务后的容量竞争。

**边界：** 不能判定失败来自层数不足、优化不足还是其他表达瓶颈；也不能断言数据不可学。

**来源：** `checkpoint_guards.csv` 与 A11_22 detailed。

### 结果 3：后续 anchors 必须继续门控，而不是被视为已得到结果

**机制对应：** 容量解释依赖校准后的稳定干扰区；课程解释依赖已确认的低容量损害区。

**指标或条件定义：** “闭环”表示具有 anchor、protocol、summary、detailed 和结果回写；“停放”表示问题保留但没有获批运行。

**证据说明：**

- A11_01--A11_20（含 `02b/08b/14b`）均已闭环；
- A11_21 未获批运行，明确停放；
- A11_22 已闭环，正式 verdict 为证据不足；
- A11_23--A11_26 尚未开启，不存在实验结论。

**解释：** 前置守卫失败后继续测有效秩或课程，会把“任务没学会”误归因成容量或训练顺序。

**边界：** 停放不等于否定容量、课程或尺度机制。

**来源：** A11 anchor index、当前 MTP story、A11_22 anchor/protocol/summary/detailed。

## 4. 执行动作

**下一步动作：** 为同一置换数据建立一个最小、已知能表示两步关系复合的校准模型；除模型可表达性外，不改变损失、数据、seed 和有限差分判据。

**目的：** 区分“原模型没有学会组合”与“学会后确实存在任务相关梯度干扰”。

**完成判据：** `5/5` seed 的 held-out 答案准确率至少 `0.70`；随后 A11_22 在相同步长下重新满足斜率、相关、符号与残差阈值，并补齐 shuffled-gradient 负对照。

## 5. 证据索引

| 结果 | 证据 | 主要指标或图 | 支持什么 | 不能证明什么 | 来源 |
|---|---|---|---|---|---|
| 结果 1 | 480 条配对有限差分记录 | 斜率 `1.0174`、相关 `0.9990`、主图 | 小步长局部公式 | 长期 MTP 效果 | A11_22 summary/detailed |
| 结果 2 | 5 个 checkpoint 校准表 | 答案准确率 `0.125` | 当前任务未学会 | 失败根因 | `checkpoint_guards.csv` |
| 结果 3 | Anchor/实验文件审计 | P/S/D 完整性与门控状态 | 研究次序 | 后续机制为假 | anchor index/story |

## 6. 来源索引

**Anchor：** [A11_22 中文 Anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_22_one_step_ntp_interference_anchor_cn.md)  
**Protocol：** [A11_22 中文 Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_22_one_step_ntp_interference/protocol_cn.md)  
**Summary：** [A11_22 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_22_one_step_ntp_interference/summary.md)  
**Detailed：** [A11_22 Detailed](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_22_one_step_ntp_interference/detailed.md)  
**Story：** [MTP 干扰、容量与课程学习](/data/250010109/Research_System/Projects/from-attention-to-search/main/stories/11_long_horizon_mtp_objective/02_mtp_interference_capacity_curriculum_cn.md)  
**Figures：** [预测一致性图](../../../../../../../Projects/from-attention-to-search/main/experiments/A12/archive/12_02_capacity_diagnostics/A12_02_01_D01_ineligible_one_step_interference/figures/prediction_fidelity.png)

## 7. 补充材料

### 对核心问题的精确答复

| 问题 | 当前答复 | 状态与边界 |
|---|---|---|
| MTP 与 NTP 应比较什么？ | 最终量必须是相同标准主头和相同标准目标的损失/答案性能；辅助头、probe 和梯度只解释机制。 | 定义已固定；当前只覆盖两个受控位置 |
| 为什么 Next-2 可能更差？ | 当 $g_N^\top g_A<0$ 时，联合一步更新相对 NTP-only 留下更高标准损失；二阶项决定有限步偏差。 | 局部公式支持；学会任务后的解释未通过 |
| 为什么大模型可能更好？ | 候选解释是更高任务相关局部可调秩与更大的安全辅助更新比例，而不是参数量本身。 | 未验证，不是当前结论 |
| 容量如何量化？ | 候选量是联合 Jacobian 谱参与率、干预响应秩和阈值化安全更新比例；必须报告对数据/checkpoint/阈值的敏感性。 | 仅完成定义，尚未测量 |
| 课程为何可能有效？ | 只能通过有限预算、非凸路径或优化器状态产生；必须等更新预算、等辅助剂量，并测早期干扰/子空间位移。 | 未验证 |
| 什么是长程语义？ | 给定局部窗口后仍由远处证据不可替代地决定、对干扰改写不变、对关键证据干预敏感的任务变量。 | 操作定义；未证明自然语言普适性 |

### 30 秒口述

> 当前得到的是一个严格的局部结论：在相对步长 $10^{-5}$ 下，梯度内积预测联合更新相对 NTP-only 的标准损失差，斜率 1.017、相关 0.999。但五个模型的两跳答案准确率都只有 0.125，所以这还不是“学会任务后的 MTP 干扰”证据。容量和课程暂不测；下一步只把同一任务校准到五个 seed 都超过 0.70，再原样复跑并补齐负对照。

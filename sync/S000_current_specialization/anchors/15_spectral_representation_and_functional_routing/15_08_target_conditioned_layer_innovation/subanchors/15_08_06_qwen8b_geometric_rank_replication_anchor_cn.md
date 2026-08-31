---
anchor_id: 15_08_06_qwen8b_geometric_rank_replication
status: EXECUTED_AWAITING_HUMAN_JUDGMENT
thinking_card: 15_08_06_qwen8b_geometric_rank_replication_thinking_card_cn.md
parent_anchor: ../15_08_target_conditioned_layer_innovation_anchor_cn.md
depends_on: 15_08_05_aligned_geometric_rank_scale_anchor_cn.md
created: 2026-08-18
updated: 2026-08-18
---

# A15_08_06：Qwen3-8B 是否复现对齐后的层间差谱宽？

Thinking Card source: [15_08_06_qwen8b_geometric_rank_replication_thinking_card_cn.md](15_08_06_qwen8b_geometric_rank_replication_thinking_card_cn.md)

## 1. Problem Definition

Qwen3-0.6B 的对齐实验已经表明：百万 token 下，完整 block 相邻差 CAR 与公共500维空间中的 Attention 相邻差 ZX 呈宽谱，而线性去旧后的 $R_U$ 更集中。当前唯一问题是：

> 只把模型换为 Qwen3-8B，并保持数据、对象、估计器和 $r_{90}$ 规则不变时，三种对象的归一化几何秩是否发生材料性变化？

这是模型尺度稳健性检查，不检验语义、功能秩、聚类或 Router 效用。若发生材料性变化，模型尺度仍是解释冲突的活跃变量；若没有，则对象定义和 token 覆盖成为更直接的解释。

## 2. Physical Priors

协方差秩属于具名随机向量与样本总体。hidden width 从1024扩大到4096会直接扩大绝对可用方向数，因此跨模型只能优先比较 $r_{90}/d_{object}$。若相同计算对象在不同规模模型中都由大量异质 token 变化构成，归一化谱宽应保持同一量级；若宽谱依赖小模型容量约束，8B会出现材料性偏移。

## 3. Falsifiable Hypotheses

**H-SCALE-STABLE：**三种对象在8B上的层中位 $r_{90}/d$ 与已冻结0.6B参考值的绝对差均小于0.03。

**R-SCALE-SHIFT：**至少一种对象的绝对差达到0.10。介于两者之间或任何方法不收敛，记为 `MIXED_OR_INSUFFICIENT`。

宽谱的辅助描述固定为：CAR 与 ZX 的层中位 $r_{90}/d$ 均至少为0.40；这只表示90%方差需要至少40%的对象维数，不表示功能高秩。

## 4. Mathematical Model

对 block $l$，令 $H_l$ 为完整 block 输出，$a_l$ 为 Attention `o_proj` write，$h_l$ 为 Attention 写入前 residual，$N_l$ 为 post-Attention RMSNorm：

$$
X_l=N_l(h_l),\quad U_l=N_l(h_l+a_l)-N_l(h_l),\quad
R_{U,l}=U_l-\widehat{\mathbb E}_{lin}[U_l\mid X_l].
$$

三个对象为 $D_l^{CAR}=H_{l+1}-H_l$、$D_l^{ZX}=Q_{500}^{\top}(a_{l+1}-a_l)$ 与 $R_{U,l}$。对中心化 covariance 的降序能量份额 $p_j$，定义

$$
r_{90}=\min\{r:\sum_{j\le r}p_j\ge0.9\}.
$$

跨模型比较量是层中位 $r_{90}/d_{object}$ 的差。该量只度量方差分散程度。

## 5. Computational Realization

在本地 Qwen3-8B 的36个 block 上，使用与0.6B实验相同且互不重叠的 DCLM TRAIN、DEVELOPMENT 和 EVALUATION token 分区。TRAIN 只构造 ZX 末层 PCA-500参考基并拟合每层 $X\to U$ 岭回归；DEVELOPMENT 只选正则；EVALUATION 只计算三种对象的谱。4096维 sufficient statistics 可以在 GPU 计算后移到 CPU 保存，存储位置不改变 covariance、岭回归或谱算法。

## 6. Minimal Falsification Tests

在1,048,576个 EVALUATION token 上得到三种对象全部层的完整谱，并要求524,288到1,048,576 token 的层中位 $r_{90}/d$ 变化不超过0.02。随后比较8B与冻结的0.6B参考值：CAR 0.5625、ZX 0.5940、$R_U$ 0.4350586。全都小于0.03为 `MODEL_SCALE_INVARIANT`；任一达到0.10为 `MODEL_SCALE_SHIFT`；其他情况为 `MIXED_OR_INSUFFICIENT`。

## 7. Current Evidence

Qwen3-8B 的同口径实验已在1,048,576个 EVALUATION token上完成并通过收敛门。层中位 $r_{90}/d$ 为 CAR 0.58838、ZX 0.65000、$R_U$ 0.32410；相对0.6B分别变化+0.02588、+0.05600、-0.11096。CAR与ZX在8B上仍满足注册的宽谱描述，但 $R_U$ 的归一化秩下降达到0.10阈值，因此主 verdict 为 `MODEL_SCALE_SHIFT`。$R_U$ 的绝对中位 $r_{90}$ 仍为1327.5，不能称为小维度空间。

CAR 的层中位 $r_{90}=2410/4096$，但目标 blocks 7与17各出现 $r_{90}=1$ 的局部奇异谱。去除每段 position 0 后，block 7恢复到867，block 17仍为1；CAR总体中位保持2410。这表明边界效应解释block 7异常的一部分，但不能解释block 17，也不改变总体宽谱结果。

## 8. Claim Boundary And Next Decision

当前证据支持“CAR/ZX的宽谱跨模型复现”，同时否定“三种对象的归一化秩都与模型尺度无关”；尺度变化集中在经过线性去旧的 $R_U$。这不能被解释为8B新增信息功能上更低秩，因为绝对方向数增加、岭回归选择和模型宽度同时变化。

唯一下一决策是：是否把 $R_U$ 的跨模型下降视为表示几何变化，还是先用匹配残差化强度审计它是否由 $X\to U$ 预测器口径造成。完成条件是比较两模型的预测解释率与固定正则敏感性；恢复动作是在该审计后再决定是否进入功能秩实验。

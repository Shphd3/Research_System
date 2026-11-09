# MTP 干扰、容量与课程学习

归档的合并前快照。下文保留当时状态，不代表当前结论边界。

## 当前状态

- 本文是中文 companion；英文 canonical 为 `20260713_mechanism_pre_consolidation.md`。
- 本文现在是 A11 研究线的 current primary synthesis。
- workload-first story 保留为背景；当前暂时冻结 workload 扩展，优先回答信息性 Next-2 监督为什么会帮助或损害共享标准目标。

## 1. 研究问题

当前不问“MTP 是否普遍优于 NTP”，而问：

> 在同一共享模型中加入信息性的第二未来词元目标后，什么可观测机制决定标准自回归目标改善还是恶化？

候选因果链为：

$$
\text{任务已学会}
\rightarrow
\text{局部梯度相互作用}
\rightarrow
\text{任务相关可用容量}
\rightarrow
\text{跨位置使用}
\rightarrow
\text{标准主头性能}.
$$

每个箭头需要独立 anchor。表征 probe 或局部导数不能替代最终标准主头指标。

## 2. 定义

| 对象 | 具体含义 | 操作定义 | 边界 |
|---|---|---|---|
| 受控标准目标 $L_N$ | 本实验中 NTP 与 Next-2 都必须改善的两位置损失 | 格式 CE 加下一状态答案 CE | 不是完整语料 all-token NTP 或 benchmark 分数 |
| 辅助目标 $L_A$ | 直接第二未来答案监督 | 决策状态上的答案 CE | 不能证明后续使用 |
| 局部干扰 | 加入 $g_A$ 后标准损失多变化多少 | 配对克隆的一步更新 | 不是完整训练 |
| 任务校准 | checkpoint 已学会组合 | held-out 答案准确率至少 `0.70` | 不解释为何学会 |
| 任务相关容量 | 同时承载和调整标准/辅助函数的独立方向 | 后续有效秩与安全更新量 | 不等于参数量 |
| 课程机制 | 渐进增加辅助权重产生的路径差异 | 静态与等剂量 schedule 比较 | 不能只看最终分数 |

## 3. 核心数学模型

$$
g_N=\nabla_\theta L_N,\qquad g_A=\nabla_\theta L_A.
$$

$$
\theta_N'=\theta-\eta g_N,qquad
\theta_M'=\theta-\eta(g_N+\lambda g_A).
$$

$$
L_N(\theta_M')-L_N(\theta_N')
=-\eta\lambda\langle g_N,g_A\rangle+O(\eta^2).
$$

该式预测局部差异。只有 checkpoint 已学会留出组合函数时，才能将其提升为任务机制解释。

严格地说，若 $L_N$ 二阶可微，则：

$$
\Delta_{obs}
=-\eta\lambda g_N^\top g_A
+\eta^2\lambda g_N^\top H_N g_A
+\frac{\eta^2\lambda^2}{2}g_A^\top H_N g_A
+O(\eta^3).
$$

因此负内积只表示联合更新比 NTP-only 更新留下更高的 $L_N$，不等于损失相对更新前绝对上升。

后续容量模型只在线性共享表征、白化输入、平方损失和最优线性读出的简化条件下成立。设 $T_N,T_A$ 是标准任务和辅助任务从输入到目标的线性映射，共享表征秩不超过 $r$，最优子空间由下式的前 $r$ 个特征方向决定：

$$
M_\lambda=T_N^\top T_N+\lambda T_A^\top T_A.
$$

若辅助方向的特征值进入前 $r$ 维并挤出标准任务方向，才形成可证明的低秩竞争。该结论不能直接外推到 Transformer。

Transformer 中可测的容量候选量必须分别定义：

$$
r_{joint}=\frac{(\operatorname{tr}K)^2}{\operatorname{tr}(K^2)},
\qquad K=J_{joint}J_{joint}^\top,
$$

表示当前数据与 checkpoint 附近联合任务 Jacobian 谱的参与率；以及

$$
S_{safe}=\frac{\|P_{\ker J_N}g_A\|^2}{\|g_A\|^2},
$$

表示辅助梯度中一阶上不改变受保护标准输出的比例。实际计算必须用阈值近似零空间，并报告阈值敏感性；二者都不是全局模型容量。

课程学习的理论边界是：若问题为凸优化、训练到同一全局最优解且最终目标相同，课程顺序不应改变最终解。因此课程收益只能来自有限训练预算、非凸路径依赖、优化器状态或表征锁定；后续实验必须等总辅助损失剂量与总更新量。

任务校准通过前，不测有效秩，也不进入课程实验。

## 4. A11_22 证据

A11_22 使用精确双置换任务 $Y=\pi_2(\pi_1(A))$、单层因果 Transformer、5 个 seed 和 1024 条 audit 样本上的配对有限差分。

在独立均匀置换分布下，$I(Y;\pi_1\mid A)=I(Y;\pi_2\mid A)=0$，而 $I(Y;\pi_1,\pi_2\mid A)=\log 8$。这验证数据的联合必要性，不代表模型已经学会该关系，也不把词元距离自动等同于长程语义。

相对步长 $10^{-5}$ 下：

- 预测—实测斜率：`1.0174`；
- Pearson 相关：`0.9990`；
- 符号一致率：`1.0000`；
- 中位归一化残差：`0.1012`。

因此，小步长一阶数值关系得到支持。但五个 seed 的验证答案准确率均为机会水平 `0.125`，正式结论仍是“任务机制证据不足”。

梯度符号也不是普遍负值：4 个 seed 的辅助方向有害，1 个有益。理论必须解释状态依赖，而不能预设 MTP 梯度必然冲突。

## 5. 核心问题的更新答复

### 为什么 Next-2 可能让标准 NTP 变差？

局部上，负梯度内积预测“联合更新相对 NTP-only 更新”的正标准损失差。该方程数值成立，但尚未证明它在学会组合任务后仍解释退化。

### 为什么大模型可能更好？

候选解释是更高的任务相关局部可调秩，以及更多一阶上不扰动受保护标准输出的辅助更新方向。目前没有实验支持；“参数更多”本身不是机制答案。

### 容量是什么？

不再只用参数量表示。候选观测量是联合任务 Jacobian 谱参与率、干预响应表征秩和安全辅助更新比例；它们都是任务、数据、checkpoint 与阈值相关的局部量，不是模型的全局容量。

### 课程学习为什么可能有用？

候选机制是路径依赖：先稳定标准子空间，再逐渐增加辅助权重。在线性凸且充分收敛的情形下，课程不应改变最终最优解；所以有效实验必须等剂量、等更新预算，并显示有限预算或非凸训练中的早期干扰/子空间位移下降。目前未验证。

### 什么是长程语义组合？

在本研究线中，它是依赖联合必要远程证据、对干扰变化不变、对任务证据干预敏感的任务变量。当前合成实例是精确关系复合；自然语言有效性不在当前 claim 内。

## 6. Anchor 次序与门控

| Anchor | 唯一问题 | 状态 | 开启条件 |
|---|---|---|---|
| A11_22 一步干扰 | 一阶项能否在学会任务的 checkpoint 预测标准损失差？ | 数值部分支持；校准失败，整体证据不足 | 完成已知可学习的任务校准 |
| A11_23 校准修复 | 深度、时长或宽度能否学会原序列任务？ | weakened：最强条件 train `0.1249`、validation `0.1211` | 已关闭 |
| A11_23b 显式绑定 | 原子 pair token 能否修复绑定？ | weakened：5-seed test `0.1274--0.1353` | 已关闭 |
| A11_24 任务秩竞争 | 显式 rank 是否控制 MTP 标准损失代价？ | supported：rank 1 gap `0.9084--1.0218`，rank 2 约零 | 已关闭 |
| A11_25 课程边界 | 等辅助剂量课程能否修复 rank-1 结构瓶颈？ | weakened：Pareto pass `0/5` | 已关闭 |
| A11_26 尺度/真实迁移 | 是否已有资格进入预训练模型/真实数据？ | parked：神经任务 gate 未通过 | 等待神经桥 |
| A11_27 标准主头因果利用 | 能力固定后，信息性 Next-2 是否增强共同 NTP 主头对组合变量的因果利用？ | 设计完成；协议草案 | 审批协议，再通过共享任务门槛 |

“按顺序完成 anchors”意味着执行这些门控，不是在前置守卫失败后伪造后续结果记录。

历史完成性审计：A11_01--A11_20（含 `02b/08b/14b`）均已有 protocol、summary 和 detailed；A11_21 明确停放；A11_22 证据不足；A11_23/23b/24/25 已完成上述判定；A11_26 由 transfer gate 正式停放；A11_27 只有设计，尚无结果。Router 不在当前 MTP 实验链。

## 7. Claim Boundary

当前只支持局部一阶有限差分关系。不支持 MTP 损害已学会的组合函数、有效秩解释尺度、课程修复容量竞争或机制迁移到自然语言。

## 8. 唯一下一决策

停止继续调小型从头训练序列模型。下一决策是审批或修正 A11_27；若批准，先用其共享 Qwen3-0.6B NTP 校准阶段通过两跳任务门槛，再克隆 NTP 与信息性 Next-2。第一个下游问题是标准主头的因果利用，不再用私有第二头或探针替代。在此之前不进入 Router 或真实 MTP 方法设计。

## 来源

- Anchor：`../../../../problem_anchors/11_long_horizon_mtp_objective/11_22_one_step_ntp_interference_anchor_cn.md`
- Protocol：`../../../../experiments/A11/A11_22_one_step_ntp_interference/protocol_cn.md`
- Summary：`../../../../experiments/A11/A11_22_one_step_ntp_interference/summary.md`
- Detailed：`../../../../experiments/A11/A11_22_one_step_ntp_interference/detailed.md`
- Active anchor：`../../../../problem_anchors/11_long_horizon_mtp_objective/11_27_standard_head_causal_representation_use_anchor_cn.md`
- Draft protocol：`../../../../experiments/A11/A11_27_standard_head_causal_representation_use/protocol_cn.md`

# A14_01：关系复用是否把 QK 功能压缩转化为任务充分的状态压缩？


研究线基础：[A14_00 条件低秩层次结构](../14_00_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure_anchor_cn.md)。

## 1. Problem Definition

**父问题：**A14 研究一个全局高容量的层级系统，何时能支持任务条件下的低维计算，同时不重新打开已经被真实证据否定的“全局共享线性传播”主张。

**唯一决策问题：**在受控 ABCD 次词预测任务中，`share16` 是否比 `random_unshared` 只需要更小的、可泛化到未见 B 上下文且能保留任务损失的 attention-update 子空间，从而在 QK 功能压缩与概率活动树的“低维局部源”前提之间建立状态侧桥梁？

| 术语 | 普通中文含义 | 具体对象 / 计算 | 决策作用 | 不能证明 |
| --- | --- | --- | --- | --- |
| share 条件 | 一套 A→C 映射能跨多少 B 上下文复用 | `share16/share4/share2/random_unshared` | 受控复合条件 | 纯频率效应；独立规则数量也同时变化 |
| QK 功能算子 | 决定 attention score 的参数对象 | \(B_{QK}=W_Q^\top W_K\)，方向按实际代码约定核对 | 参数侧压缩诊断 | hidden state 一定压缩 |
| 任务相关状态 | 在 B 末端直接用于预测第一个 C token 的内部更新 | attention residual update \(g_{i,t}\)；raw residual 只作守卫 | 状态侧主对象 | 整个语言的语义表示 |
| held-out 功能状态秩 | 在训练上下文上拟合子空间后，保留未见上下文任务损失所需的最小维数 | \(k_H(s;\epsilon)\) | 主要状态压缩量 | 严格秩或非线性内在维度 |
| 参数—状态桥 | 同一条件下同时出现非平凡 QK 压缩和任务充分状态压缩 | 参数/状态联合证据，加随机子空间与跨 B 守卫 | 连接学长实验和 A14 局部状态前提 | 优化机制或自然语言外推 |

本 anchor 不会把 share 条件直接称作“频率”。当前生成器同时改变 exact relation 复用、跨上下文复用、独立规则数量与函数复杂度。

## 2. Physical Priors

1. **复用先验：**若同一个 A→C 函数跨多个 B 被调用，模型可能比逐 B 记忆独立 lookup 规则复用更少任务方向。
2. **参数到状态先验：**QK 参数谱只有在改变预测所使用的状态时，才与 A14 的低维活动源有关。
3. **任务充分性先验：**重构误差小不够；投影后的状态必须在未见 B 上保持 C-token 效用。
4. **局部而非全局先验：**一个局部状态可复用，不要求所有规则、模式和任务的并集低维。

这些都是经验先验。概率活动树定理仍是独立成立的条件数学定理。

## 3. Falsifiable Hypotheses

**主要假设：**在 full-model 能力匹配时，`share16` 在校准 B 上拟合的状态子空间能够以比 `random_unshared` 更小的归一化秩保留未见 B 的 C-token loss，并满足预注册的非平凡维度预算。

**最强替代解释：**现有 Q/K 删谱结果完全来自更少的独立 lookup 表或参数化特异的谱。预测相关 attention update 并未更低维、不能跨 B 迁移，或投影后丢失任务效用。

**Pass：**来源、能力和实现守卫全部通过；`random_unshared - share16` 的功能状态秩差为正且分层配对 bootstrap 置信区间下界大于零；`share16` 满足非平凡预算；同秩随机空间不能保留相同效用。

**Fail：**守卫通过，但主差值不为正、`share16` 超出预算，或低维投影不能保留 held-out utility。

**Insufficient：**无法恢复原始 checkpoint 或生成器语义；参数侧现象不能复现；B-disjoint 划分或 intervention replay 失败；数值或样本守卫不能稳定选秩。

## 4. Mathematical Model

令 \(s\) 表示 share 条件，\(g_i^s\in\mathbb R^d\) 表示样本 \(i\) 在 B 末端的 attention residual update。按 B identity 划分 calibration/test，只用 calibration 状态拟合均值 \(\mu_s\) 和主方向 \(U_{s,k}\)。对 test 状态进行仿射投影：

\[
\Pi_{s,k}(g)
=
\mu_s+U_{s,k}U_{s,k}^{\top}(g-\mu_s).
\]

设 \(L_s^{full}\) 是 held-out 第一个 C token 的完整模型交叉熵，\(L_s^{(k)}\) 是只把注册 attention update 替换为 \(\Pi_{s,k}(g)\) 后的交叉熵。对预注册容忍度 \(\epsilon\)，定义：

\[
k_H(s;\epsilon)
=
\min\{k:L_s^{(k)}-L_s^{full}\le\epsilon\}.
\]

主要比较量为：

\[
C_H
=
\frac{k_H(\texttt{random\_unshared};\epsilon)
-k_H(\texttt{share16};\epsilon)}{d}.
\]

参数侧使用 \(B_{QK}=W_Q^\top W_K\)，并类似定义保留 held-out C-token loss 的最小功能秩 \(k_{QK}(s;\epsilon)\)。它是次要指标，因为 A14 当前缺少的是任务状态，而不是另一个参数谱指标。

## 5. Computational Realization

- 首先恢复研究者提供的 NTP 实验所使用的 ABCD 生成器、checkpoint 指纹、matched-fit 规则和四个 share 条件；来源守卫未通过前不得形成证据。
- 主设置采用现有证据最干净的 64 维、单层、单头模型与 3 个 seed。`share16` 和 `random_unshared` 是主要比较；`share4/share2` 只作剂量趋势诊断。
- A/B/C/D 边际频率、样本数、A→C 距离、序列长度、模型、优化器和 matched-fit 规则与源实验一致。
- 按 B identity 而不是样本行划分 calibration/test；只在 calibration B 上拟合仿射子空间，在未见 B 上干预和测 loss。
- 主状态为 B 末端的 attention residual update。raw residual、能量有效秩和关系条件梯度对齐只作诊断。
- 每个 \(k\) 都与同秩 Haar 随机子空间及 shuffled-state control 比较。
- 重新计算组合 QK 算子的功能秩曲线，并把源实验的 \(W_Q/W_K\) 单矩阵删谱作为来源复现诊断。
- 不训练 Router、MoE 或自然语言模型。

## 6. Minimal Falsification Tests

| 检验 | 必要性 | 预注册解释 |
| --- | --- | --- |
| 来源复现 | 确认继承现象在实际 artifact 上存在 | 失败则证据不足 |
| 能力匹配 | 排除欠训练导致低秩 | 所有主运行满足源实验 matched-fit |
| B-disjoint 迁移 | 区分可复用状态与训练集 PCA | calibration 拟合、未见 B 测效用 |
| 功能投影 | 区分能量集中与有用压缩 | 干预后的首个 C-token loss |
| 同秩随机空间 | 排除“任意小空间都可以” | 学得空间必须优于随机空间 |
| `share16` 对 `random_unshared` | 决定性复合条件对照 | 主指标 \(C_H\) |
| `share4/share2` | 查看中间条件是否有序 | 仅诊断；不覆盖主判决 |

主证伪条件是：来源、能力和实现均通过，但 `share16` 没有 held-out 功能状态秩优势。

## 7. Current Evidence

来源记录报告了 64 维设置下 350/750/1100/1200 的 matched-fit 中位步数，以及 `share16` 更强的 Q/K 尾删鲁棒性。公开来源仓库没有原始生成器、训练代码和 checkpoint，因此预注册的来源与精确重放硬门无法通过。

依据冻结合同完成了一次可追溯的独立重建。12/12 个 condition-seed 运行通过能力门。`share16` 的状态功能秩为 13/10/10，`random_unshared` 为 16/13/12；三个归一化配对差均为正，5000 次分层 bootstrap 的 95% 区间为 \([0.0260,0.0521]\)。所有 `share16` 运行均满足 16/64 预算；学得子空间通过、同秩随机空间失败；交换 calibration/test B 后方向不反转。

但是参数效应明显大于状态效应：`share16` 与 `random_unshared` 的平均组合 QK 功能秩为 29.7 与 50.7，平均状态功能秩仅为 11.0 与 13.7。12 个 condition-seed 点上的相关性弱且不显著（Spearman \(\rho=0.247,p=0.438\)）。中间条件也不单调，`share4` 的状态秩略低于 `share16`。

独立重建还没有复现来源记录中“V/O 几乎不受影响”的定位。因此**正式预注册判定是证据不足**；独立重建只能作为“极端复合条件存在小幅状态秩差”的有条件证据。完整结果见 [E08 中文摘要](../../../experiments/A14/14_00_tree_low_rank_language_structure/historical_support/legacy_line_experiments/A14_E08_relation_reuse_state_bridge/summary_cn.md)。

## 8. Claim Boundary And Next Decision

**独立重建允许声称：**在这套明确记录的实现中，高复用/低规则数量复合条件相对 `random_unshared` 具有小而一致的 held-out attention-update 功能秩优势，以及更大的组合 QK 功能秩优势。

**仍不能声称：**精确复现了来源实验；关系频率单独导致低秩；存在单调复用—秩定律；梯度对齐已被证明；自然语言是树；NTP 普遍产生低秩语义；完整 hidden space 全局低秩；MoE Router 应按该几何路由。

由于来源 artifact 缺失，原始来源重放合同仍未被裁决。独立重建现注册为一条**有边界的 standalone evidence**，但不能静默升级成原实验复现或纯频率结论。

**唯一下一决策：**本 anchor 完成交接；由 [A14_02](../14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor_cn.md) 审核 exact frequency、规则复用与 lookup 基数的正交实验。Router 实验仍不属于本 anchor。

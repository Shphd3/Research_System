# 关系复用是否把 QK 功能压缩转化为任务充分的状态压缩？

本卡保存研究者在 2026-07-22 讨论中已经明确表达的判断。AI 提出的术语修正与实验操作化单列在审计记录中，尚待研究者逐项批准。

## Human Draft

**Phenomenon / 现象：**

在学长的受控 NTP 实验中，`share16` 到 `random_unshared` 同时改变了 A→C 关系跨 B 上下文的复用程度和需要学习的独立映射规则数量。复用较多、规则较少的条件学得更快，也更耐受 $W_Q/W_K$ 尾部奇异方向删除。我们希望知道，这种参数侧功能压缩是否在预测 C 时形成了一个跨上下文可复用、且保留任务效用的低维内部状态，从而为概率活动树的“低维局部源”前提提供经验桥梁。

**Mechanism guess / 机制猜想：**

当同一个 A→C 功能关系在多个 B 上下文中被重复调用时，NTP 的训练更新可能反复强化少数共同的 QK 功能方向；这些共同方向进一步使 B 末端用于预测 C 的 attention update 集中到少量可复用方向。若把该更新投影到这些方向后，未见 B 上下文中的 C-token loss 仍能保留，则这种低维状态可能作为条件活动树中的局部任务状态。

**Strongest rival explanation / 最强替代解释：**

`share16` 只需要较少的独立 lookup 表，函数本身更简单；即使模型采用死记硬背，也可能只需较少参数方向。因此现有删谱结果可能由“独立规则数量较少”解释，而不是由跨上下文关系复用、梯度对齐或树状语义机制解释。另一项替代解释是：Q/K 的单矩阵谱只是参数化现象，任务相关 hidden state 并未更低维。

**Most uncertain point / 最不确定之处：**

参数侧的 QK 删谱鲁棒性，是否真的对应状态侧“跨上下文可复用且任务充分”的低维几何；这是当前理论与实验之间缺失的箭头。

**Evidence that would change my mind / 改变判断的证据：**

如果 `share16` 在未见 B 上下文上所需的最小任务保持状态秩并不低于 `random_unshared`，或低能量投影虽然重构状态却显著损害 C-token loss，我会放弃“当前 QK 压缩已经形成概率树所需低维局部状态”的解释。若该桥接成立，但在独立控制关系重复次数与规则数量后只随规则数量变化，我会把机制改写为函数复杂度压缩，而不是频率或复用效应。

**Current next decision / 当前唯一决策：**

是否批准 A14_E08 先做参数—状态桥接审计：在现有 ABCD 合成 NTP 设置中，测量未见 B 上下文上的任务保持状态秩，并把“频率与规则数量的因果分离”保留为桥接通过后的下一张独立协议。

## Optional Formalization

**Key variables / 关键变量：**

- `share setting`：`share16/share4/share2/random_unshared`；这是复用程度与独立规则数量的复合变量，不命名为纯频率。
- $B_{QK}=W_Q^\top W_K$：决定 attention score 的组合双线性算子。
- $g_{i,t}$：B 末端、用于预测第一个 C token 的 attention residual update。
- $k_H(\epsilon)$：在校准 B 上拟合低维仿射子空间后，使未见 B 上的 C-token loss 增量不超过 $\epsilon$ 所需的最小状态秩。
- $k_{QK}(\epsilon)$：在相同 loss 容忍度下，组合 QK 算子所需的最小功能秩。

**Causal relation / 因果方向：**

候选链为：关系跨上下文复用与较低规则复杂度 → QK 功能方向集中 → 任务相关 attention update 集中 → 条件状态可以低维保留任务效用。E08 只裁决后两项是否连接，不裁决第一项的独立因果来源。

**Primary observable metric / 主要观测指标：**

$$
C_H
=
\frac{k_H(\texttt{random\_unshared};\epsilon)}{d}
-
\frac{k_H(\texttt{share16};\epsilon)}{d}.
$$

它衡量 no-reuse 复合条件相对 high-reuse 复合条件多需要多少比例的任务保持状态维度。

**Pass / fail / insufficient evidence：**

- **Pass：**`share16` 的 held-out 任务保持状态秩显著低于 `random_unshared`，达到预注册的非平凡维度预算，且同秩随机子空间不能同样保留 loss。
- **Fail：**能力与实现守卫通过，但主差值不为正，或低维投影不能保留未见 B 的任务效用。
- **Insufficient：**原始 checkpoint/数据生成器不可恢复，基础删谱现象不能复现，校准与测试 B 不独立，或样本数/数值谱不足以稳定选择维数。

## AI Audit Record

**Judgments to preserve / 必须保留的人的判断：**

1. 当前先解释学长实验与概率树理论之间的状态桥，不直接设计 Router。
2. 我们关注的是活动树根或局部任务状态矩阵的有效/功能秩，不把参数矩阵秩和表示秩混为一谈。
3. “学会”最终以 held-out downstream utility 为准，而不只看训练拟合或谱形状。
4. 死记硬背少量 lookup 规则是必须保留的最强替代解释。

**Unclear definitions / 未定义对象：**

原讨论中的“频率”混合了 exact relation 重复次数、跨 B 上下文复用和独立映射规则数量；“hidden state”也尚未指定为 raw residual 还是任务直接使用的 attention update。

**Hidden assumptions / 隐含假设：**

同一低维状态空间必须能从校准 B 泛化到未见 B；投影后保留能量还必须保留 C-token loss；原始 share 条件的 full-model 能力必须匹配。

**Metric mismatch / 指标错配：**

单看 $W_Q$ 或 $W_K$ 的谱具有参数化依赖；单看 hidden-state 奇异值只测能量，不测任务必要性；负载均衡或专家使用率也不能验证本机制。

**Candidate correction proposed by AI / AI 候选修正：**

以 $B_{QK}$ 作为参数侧主对象，以 B 末端 attention update 作为状态侧主对象，以 held-out loss-preserving rank 作为主要状态指标；raw residual、谱有效秩和梯度对齐只作诊断。E08 先检查桥接是否存在，随后再用正交设计分离 exact frequency 与独立规则数量。

**Human decision on the proposal / 人的最终确认：**

待审核。研究者需要重点裁定：状态对象、$\epsilon=0.02$ 的任务容忍度、$k_H/d\le0.25$ 的非平凡预算，以及“先桥接、后做频率×规则复杂度因果分离”的顺序。

## Boundary

本文件不是结果记录。即使 E08 通过，也只能在当前受控 ABCD-NTP 设置中建立参数压缩与任务相关状态压缩的经验桥；不能证明自然语言是树、NTP 普遍产生低秩语义、概率树在真实 LLM 中成立，或 MoE Router 必须采用该空间。

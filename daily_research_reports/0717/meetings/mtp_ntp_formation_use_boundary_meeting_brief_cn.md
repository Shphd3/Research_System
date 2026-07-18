# MTP 相比 NTP 改变了什么：从提前监督到标准头使用

## 执行摘要

**核心结论：** MTP 相比 NTP 已经确定的优势，不是“最终一定更准”，而是更早的任务相关信用分配：当紧邻 next-token 目标尚未包含任务变量、但更远 future target 已包含它时，MTP 能直接训练较早的共享状态；NTP 只能在稍后状态获得同一任务信号。切断直接信息的建模实验进一步表明，这类提前监督在所训练状态成为答案必经通道时能够提高普通主头的有限预算学习效率。当前只是机制隔离，并没有完成NTP和MTP真实任务对比。

构造的数据关系：

A ──×──→ ANSWER

A ──→ RELAY hidden state ──→ ANSWER ──→ 预测A

**认识更新：**

**两种最小建模：**

| 建模 | 最小序列与信息路径 | 训练差异 | 它回答什么 |
|---|---|---|---|
| **A11：Branch 信息纳入模型** | `BR_z ... U03 A_SHARED S_z`；答案位置 `A_SHARED` 可以直接读取开头的 `BR_z`，所以 `U03` 不是必经状态 | 在 `U03`，NTP 只预测共同的下一词元 `A_SHARED`；MTP 还能提前预测携带分支信息的 `S_z` | MTP 是否比 NTP 在同一较早状态多出任务相关的直接梯度；不回答普通主头是否必须使用 `U03` |
| **A13：Relay 信息转化模型** | `[BOS] [FIXED] [A] [B] [RELAY] [ANSWER] [A]`；必须中继时路径为 $A\rightarrow Relay\rightarrow Answer$，允许绕行时另有 $A\rightarrow Answer$ | 在相同路径内，只把 Relay 的辅助目标从无关变量 $B$ 改为答案变量 $A$ | 当提前监督内容与答案相关、且 Relay 被普通主头实际使用时，是否产生有限预算收益；不是纯 NTP 对纯 MTP 比较 |

1. **MTP 比 NTP 强在“更早的直接信用路径”。** 预测范围 $K$ 首次覆盖携带新增任务信息的未来位置时，MTP 在更早 hidden state 上产生 NTP 同位置没有的直接一阶语义更新；关键不是 $K$ 的数值，而是新目标是否包含任务信息，以及新增梯度方向是对齐、无关还是冲突。
2. **更早形成信息不等于完整目标受益，更不等于普通主头使用。** 全位置 MTP 的其他位置与 horizon 梯度可能增强或抵消这条直接路径；A11 中 `U03` 已包含可读的 Branch 信息，但答案可以绕开它，因此没有建立相对匹配辅助头的稳定强答案控制增量。
3. **在直接答案路径被切断、普通主头只能通过 Relay hidden state 获得答案变量的受控任务中，答案相关的 MTP 式提前监督，相比同规模的无关监督，能够提高普通主头的有限预算学习效率。** A13 在硬中继载体中只把 Relay 的辅助目标从无关变量 $B$ 改为答案变量 $A$，必须中继时普通主头损失改善为 `0.2315` nat，允许直接读取时仅为 `0.0181` nat，交互为 `0.2134` nat，8/8 种子同方向；这证明任务相关提前监督的受控充分条件，但不是纯 NTP 对纯 MTP 的最终比较。

---

**研究问题：** MTP 相对 NTP 新增的较早未来监督，究竟增加了什么训练信号；该信号在什么任务结构下能够转化为普通 next-token 主头的实际收益？

**我的初始判断：** MTP 引入更远目标的监督，会使 hidden state 包含更多长程语义信息，并自然改善普通 next-token 主头的长程推理能力。

**本次结果：** A11 建立了信息性未来目标带来的较早直接一阶梯度及其共享参数可达性，同时否定了“直接梯度必然成为完整目标增益”和“信息形成必然成为标准头使用”。A13 随后建立了一个更窄的正结果：当答案相关变量只能经 Relay 到达普通主头时，在 Relay 上施加答案相关的提前监督，比同规模监督无关变量显著提高前 1,000 步的学习效率；所有条件最终均达到准确率 `1.0`，因此差别是有限预算学习速度，而不是最终可学习性。

**机制解释：** NTP 并非永远看不到答案，而是在更晚位置通过普通答案损失间接训练早期状态；MTP 则能把未来答案监督直接附着到更早状态。该短信用路径只有在方向与最终答案一致、完整目标背景不抵消、信息能够运输且普通主头确实读取该状态时，才可能成为功能收益。A11 解决了“是否存在更早直接信号”，A13 解决了“任务相关性与状态必要性是否让这种信号具有主头价值”；梯度强度、硬注意力造成的额外任务难度，以及标准 MTP 相对匹配 NTP 控制的净收益仍待裁决。

**决定性证据：**

1. A11 全位置路径分解中，MTP 较早直接路径的一阶参数更新均值为 `0.002617`，大于 NTP 稍后语义路径的 `0.001438`，5/5 种子成立；但完整 MTP 净更新仅 4/5 为正，证明局部优势可被背景梯度抵消。
2. 信息性 MTP 相对 matched shared-aux（第二个辅助头重复 next-token 目标，用于匹配头数和损失项）的强答案控制增量为 `0.01675<0.10`，0/5 种子达到注册阈值；这否定了 A11 载体上的稳定强使用增量，而不是否定所有弱影响或一般 MTP。
3. A13 的任务相关 Relay 监督交互为 `0.2134` nat，95% 区间 `[0.1646, 0.2585]`，8/8 种子为正；替换第一层 Relay hidden state 后，普通主头 100% 跟随供体标签，证明该硬中继载体中的 Relay 被实际使用。

**结论边界：** 当前可以声称：MTP 在受控模型中比 NTP 多出一条更早、任务相关的直接信用路径；当这种提前监督落在答案必经且被普通主头使用的状态上时，它可以产生有限预算收益。不能声称：标准 MTP 已经普遍优于纯 NTP，或已经证明代码、自然语言、长上下文、组合推理与 MoE Router 收益。A13 的主要对照是“普通 NTP 加答案相关辅助目标”与“普通 NTP 加无关辅助目标”；无关变量 $B$ 是因果内容控制，不是标准 NTP 目标。硬稀疏注意力可能增加任务难度与提升空间，训练过程中的有效梯度大小也尚未解耦。

**执行动作：** 下一步只在当前载体上完成一个软中继三条件审计：连续削弱而非立即切断直接 $A\rightarrow ANSWER$ 路径，并比较 NTP-only、matched shared-aux 与 informative-MTP。若 informative-MTP 相对 matched shared-aux 的收益随实测 Relay 因果依赖平滑增加，且不能由梯度剂量或基线难度解释，则支持把该机制映射到更真实任务；若收益只在硬切断时出现，则停止外推；若路径强度未形成有序依赖或不存在共同可学、未饱和窗口，则判为证据不足。

**来源：** [A11 shared-parameter path decomposition](../../../Projects/from-attention-to-search/main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E02_all_position_path_decomposition/summary.md)；[A11 standard-head causal-use result](../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/summary.md)；[A11 source-information audit](../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/summary.md)；[A13 task-relevant relay result](../../../Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_05_E01_task_relevant_target/summary.md)。

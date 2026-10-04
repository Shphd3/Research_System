> 历史阅读副本。科学内容与原始快照相同；仅解析原上下文相对链接。当前设计另见候选目录的现行Anchor。

# 临时 Anchor：有限专家预算下的共同计算与特异学习

更新：2026-10-03。仍是同一个逐步细化的问题，不建立正式项目或新 Focus。[用户授权原文记录](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/receipts/user_authorization.json)；[旧设计快照](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/history/20261002_before_capacity_refinement/reading/anchor_cn.md)。旧结果保持原边界，不改写为新设计的结果。

## 1. 问题定义

研究者的目标是：利用分开学习，提高有限模型的有效学习容量；让小的特异专家复用共同处理，接近较大 Dense 的学习效果。本轮先问一个可测的问题：在固定四域序列、参数和 token 预算下，显式 common，以及“common 之后再 specialized”的计算，能否改善新知识习得与旧知识保持？

对象是从随机初始化训练的因果语言模型。每条文本的已知领域选择一名专家。这是带领域信息的机制实验，尚未解决可学习路由。这里还没有测量“最大容量”：我们测固定预算下的损失与保持，没有定义可接受损失阈值，也没有找到饱和点。

独立状态：`task_state=IN_PROGRESS`；`question_state=OPEN`；`design_state=FROZEN_WITH_PRE_RESULT_ANALYSIS_AMENDMENTS`；`result_state=NOT_RUN`。用户明确授权 AI 选择有界实现与实验方案，并免除再次审批；这不等于研究者预先确认科学结论。可接受 Dense 差距、容量饱和定义仍为 `Unknown`。

## 2. 物理先验

训练时有 NTP 目标，可以用目标组织学习；旧的“更新前表征能否预测响应”不再作为学习分配的前置条件。自然语言领域可能共享结构，但结构上共享一个模块，不等于它已学到可复用的共同知识。common 既可能节省重复存储，也可能向旧领域传递漂移。解释后者之前，必须确认未选中专家的参数和优化器状态都没有变化。

有限数据下的共享收益也可能来自样本汇聚降低估计方差，而非表达族扩大；[统计玩具模型](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/capacity_mathematics_cn.md)给出精确条件。它不是本轮NTP机制的确认，也不改实验合同。

文献提供条件性依据：[DeepSeekMoE](https://arxiv.org/html/2401.06066v1) 的实验支持其配置中的共享专家隔离；[OLMoE](https://arxiv.org/html/2409.02060v1) §4.1.3/图6的匹配消融中，共享专家略差。两者都不是本轮串行机制的证明。[Progressive Networks](https://arxiv.org/pdf/1606.04671) 说明旧特征可以进入新计算，但它扩充网络；[PackNet](https://arxiv.org/pdf/1711.05769) 则提示要区分旧知识复用和剩余可用容量。

## 3. 可证伪假设

H1，共享：common_parallel 相比 private_active，能用较少总 FFN 参数获得相近或更低的新旧领域损失。通过把 common 通道复制进各个 private_active 专家，两者初始函数匹配。若一致变差，或收益仅由牺牲旧域换得，则不支持这一版本的共享收益。

H2，耦合：common_serial 相比 common_parallel，在参数量和名义 FFN 乘法量相同的条件下改善习得或保持。它检验整个计算变化；仍不能把有效非线性深度或优化差异排除，从而直接归因为“共同知识”。

H3，漂移：新领域训练后，旧领域专家保持不变。分别回滚 common 和其余共享主干，可以分解旧域损失变化的传递路径。不能预设变化一定有害；帮助与伤害都要记录。

主要替代解释包括欠训练、参数或计算预算、初始函数差异、领域记忆、主干漂移、领域顺序和串行深度。两个 seed/order 组合只能检查联合条件下是否重复，不能分别估计 seed 效应与顺序效应。

## 4. 数学模型

先定义对象：r 是 Attention 后的残差，z=RMSNorm(r)；C 是每个领域都使用的 SwiGLU；E_d 是领域 d 的私有 SwiGLU。并行计算为 r+C(z)+E_d(z)。串行计算为 r+C(z)+E_d(z+C(z))。专家接收两者的和，不是分别接收 z 与 C(z)。这条残差提供直接输入路径，但不保证相加后的映射可逆或不丢信息。

E 个专家、common 宽度 c、私有宽度 p、隐藏维度 h 时，每层 FFN 总参数为 3h(c+Ep)，单 token 激活参数为 3h(c+p)。private_active 的各专家宽度为 c+p；private_total 为 p+c/E。E 固定且 c>0 时，private-only 无法同时匹配总参数与激活参数。因此两种对照都有必要；Dense 也分别匹配激活宽度和总宽度。全模型统计还包括各臂相同的 embedding 与 Attention。

在线性例子 W_d=C+E_d 中，只有确实存在可复用结构，共享存储才有意义。串行残差展开为 (I+E_d)(I+C)=I+C+E_d+E_d C。如果 I+C 可逆，E_d(I+C) 可以吸收到秩不变的私有映射中。因此线性串行不必扩大函数类。非线性网络的好处需要实验给出，不能把通道宽度直接当作语义秩。

对旧域 i，固定未改变的 E_i。用 0 表示阶段前、1 表示阶段后，定义 L_ab=L(C_a,T_b,E_i)，其中 T 包括 embedding、Attention 与归一化等其余共享参数。有限分解为

\[
\phi_C=\tfrac12[(L_{10}-L_{00})+(L_{11}-L_{01})],\qquad
\phi_T=\tfrac12[(L_{01}-L_{00})+(L_{11}-L_{10})].
\]

两项之和严格等于 L_11-L_00；另报交互 L_11-L_10-L_01+L_00。保留四个原始损失。这是对有限参数干预的对称分配，不是唯一语义因果解释，也不是可实际走出的训练路径。

进一步解释：可逆性只保证信息保留，不保证有限专家函数族对非线性复合封闭。[线性等价与非线性反例](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/capacity_mathematics_cn.md)给出精确条件，并把表示、学习、保持与更新路径的经验义务分开。

## 5. 计算实现

六臂、数据和预算以 [Protocol](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/history/20261003_before_routing_refinement/reading/protocol_cn.md) 为准。模型八层，h=256，4 个 Q head、2 个 KV head，词表 embedding 与输出权重绑定，所有臂统一加入领域嵌入；没有 SAE、没有学习路由。c=256、p=384、E=4。约 300M 模型是用户允许的后续选项，不自动加入本轮。

先做 512 次四域混合更新，再依次做四个单域阶段，各 1024 次。每次更新 8192 个有效预测目标，固定终点为 37,748,736 次 token 暴露。六臂均执行两个配对 seed/order 组合。训练只使用一台 8×RTX5090 SPOT；每个 GPU 独立执行一条轨迹，空出的 GPU 接下一条。

## 6. 最小反驳实验

一组实验包含六个条件、两个配对组合，以及保留检查点上的有限干预。主要比较为 serial 对 parallel、parallel 对 private_active，以及 common 对两种 Dense 和 private_total。不同资源坐标分别报告。

读取完整“领域×阶段”验证矩阵、自己阶段的学习增益、后续遗忘、终点宏平均损失与仅终点评估的 test。保留每个领域，避免平均后抵消伤害。解释回滚之前，先验证旧专家参数与优化器状态未变。

同一问题另外包含两项预先登记的有限诊断：保持前向不变、只截断选定层经过专家的common梯度路径；以及保留真实领域输入、交换expertbank评价功能匹配。它们分别检验局部更新路径与当前状态的专家分工，不替代长期容量判断。精确约定见Protocol §17的训练结果前修订。

## 7. 当前证据

本次更新时，新训练实验为 `NOT RUN`。[前一轮有限更新结果](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/source_transfer_addendum_cn.md) 只说明旧模型和旧面板的行为，不构成 common 专家容量证据。数据准备与独立重读检查通过；实现检查及指定硬件 Smoke 仍是训练前门槛。[执行目录](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity) 保存原始证据。

## 8. 结论边界与下一决定

固定终点损失更低，只支持有界性能比较。回滚 common 改变损失，只说明对这些有限参数变化敏感，不能直接称作普遍共同知识。四域各占一个专家，没有耗尽专家槽位。此轮不自动给出方法优劣总判定、最大容量、可学习路由或长期转移结论。

下一步先判断差距来自习得不足、保持不足，还是共享漂移；再决定是否需要深度匹配对照，或“更多领域、少量专家”的容量实验。这些下一步属于 `AI 建议`。当前工作继续放在临时目录。

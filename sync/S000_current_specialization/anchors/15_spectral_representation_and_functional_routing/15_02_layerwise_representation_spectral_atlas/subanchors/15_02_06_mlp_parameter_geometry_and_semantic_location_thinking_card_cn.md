# A15_02_06 Thinking Card：MLP 参数共同子空间与 attention write 的粗细语义位置

状态：研究者于 2026-08-07 确认判断，并批准 Anchor、Protocol、实现、smoke、多个单节点 8×5090 full run、分析、结果记录与当日 `focus.md`。

## 我的判断

- **具体现象：**不加 residual 的 attention 输出可以作为本层写入量；加上 residual 后，MLP 同时接收历史状态和本层写入。若各层 MLP 都要处理反复出现的共同信息，其高增益输入子空间可能跨层更一致；较低增益的 middle/tail 部分可能容纳更具层特异性的更新。
- **机制猜想：**MLP 的参数谱 head 是跨层共享的 common 子空间，而 middle/tail 较少共享。细粒度语义相对粗粒度语义，可能随层深增加而把更大比例的 attention write 方差放到本层 MLP 参数谱的较后秩位置。
- **有效性要求：**原始 attention write 在参数方向上的投影只描述几何位置；只有该位置在参数增益加权、实际 MLP 输入增量，以及非线性 MLP 响应中仍存在，才能称为“MLP 有效响应”。
- **最强替代解释：**参数 head 对齐可能来自初始化、优化尺度或 RMSNorm 权重，而不是 common 语义；细/粗的相对后移也可能只是归一化后的微小尾部比例变化，经过参数增益或 MLP 非线性后消失。
- **最不确定的一环：**`post-o_proj` 写入位于 residual 坐标，而原始 MLP 参数的右奇异方向位于 RMSNorm 后的输入坐标；若忽略这一步，投影可能物理错配。
- **什么证据会改变判断：**head 子空间不比 middle/tail 更跨层对齐；细相对粗的秩重心不随深度后移；或原始写入后移不能在 RMSNorm 坐标匹配、增益加权与实际 MLP 响应中复现。
- **当前唯一决策：**复用已审核的 512 条粗/细层级数据，在冻结 Qwen3-8B 上完成参数共同性、attention write、MLP 输入增量和 MLP 响应的逐层审计；不把词频、组合深度或 Router 功能纳入本实验。

## AI 审核

- **必须纠正的定义：**每层横轴只能表示该层自身按增益排序的参数秩；“同一秩跨层移动”不是同一向量的轨迹。跨层共同性必须用等秩投影子空间的重合度单独测量。
- **必须纠正的统计量：**粗、细都使用同一组平衡样本和同一个表达噪声分母；参数位置使用各自总类别间方差归一化后的谱份额，不能再比较分母含义不同的旧 $D_{fine}/D_{coarse}$。
- **最小反例：**若原始 attention write 在 tail 相对富集，但增益加权和实际 MLP 响应均为 head，则只能说 tail 存在几何信号，不能说 MLP 有效使用 tail。
- **AI 建议：**pursue；将 raw geometry、gain-weighted response 和 nonlinear response 分层判定。

## 我的确认

- 保留以上判断、替代解释与 claim boundary。
- A--G 实验块已审批；允许按冻结的 `5090-8-spot` 资源元组并行执行完整实验。


# Thinking Card — 信息性未来位置监督 Anchor

> Migrated from [11_01_informative_horizon_supervision_anchor_cn.md](11_01_informative_horizon_supervision_anchor_cn.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**现象：** 预测更多未来词元有时会更早产生任务信号，但单纯增加预测跨度并不稳定有效。

**机制判断：** 只有当新增未来位置包含局部上下文无法替代的任务信息时，它才会直接更新当前位置。多个信息性目标的作用取决于输出方向相加后是增强还是抵消。

**核心观测：** 隐藏语义速度，即当前位置沿正确任务方向的一步移动量。

**决策：** 关闭“直接监督何时出现”这一问题；不再把预测跨度本身当成原因。

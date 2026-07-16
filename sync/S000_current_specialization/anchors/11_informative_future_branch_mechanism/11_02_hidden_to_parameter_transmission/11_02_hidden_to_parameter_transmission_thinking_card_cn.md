# Thinking Card — 隐藏状态到参数传递 Anchor

> Migrated from [11_02_hidden_to_parameter_transmission_anchor_cn.md](11_02_hidden_to_parameter_transmission_anchor_cn.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**现象：** 损失函数可以在隐藏状态上指向正确方向，但共享参数未必能够实现这次移动。

**机制判断：** 任务方向必须经过隐藏状态对参数的雅可比传递；其他语言模型损失会产生有正有负的背景项，可能增强也可能抵消直接信号。

**核心观测：** 参数语义速度，即一次共享参数更新预计造成的任务 margin 变化。

**决策：** 受控模型中参数传递前提成立；在完整全位置训练中，净方向并不保证每次都为正。

# Thinking Card — 组合工作负载与能力门槛 Anchor

> Migrated from [12_01_compositional_workload_capability_gate_anchor_cn.md](12_01_compositional_workload_capability_gate_anchor_cn.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**现象：** 上下文很长不等于任务真的需要长程推理。目标任务必须满足：知道局部内容后，远程证据仍不可替代，而且模型必须经过中间状态把证据按顺序组合。

**机制判断：** 两张完整的一一映射表可以隔离这一计算骨架，并排除简单词频和唯一答案词捷径；但只有模型先学会任务，才有资格比较训练目标。

**核心观测：** 完整上下文的 held-out 答案准确率，同时用单表和证据干预作保护。

**决策：** 接受数据建模；停止继续调当前从零训练的小模型；先获得一个能完成任务的共享检查点。

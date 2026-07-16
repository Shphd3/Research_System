# Thinking Card — 标准主头对中间组合状态的因果使用

> Migrated from [12_03_standard_head_causal_use_anchor_cn.md](12_03_standard_head_causal_use_anchor_cn.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**现象：** A11 说明信息性未来监督可以更早形成任务信号，但探针能读出或私有未来头准确，并不能说明普通下一词元主头使用了中间组合状态。

**机制判断：** 同一个共享检查点先学会深度二任务后，信息性 Next-2 会增强中间状态 $B$ 的分量；该分量穿过共有格式词元后，在标准主头中因果控制 $Y=\pi_2(B)$。

**关键变量：** 任务门槛准确率、交叉拟合中间状态子空间、反事实标准头效应、匹配随机子空间效应和干净标准头准确率。

**核心观测：** 从 NTP 到信息性 Next-2，标准头中由 $B$ 子空间特异产生的反事实控制增加多少。

**决策：** 共享能力门槛通过后才测试因果使用；否则停止，不解释探针或补丁。

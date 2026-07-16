# Thinking Card — 跨位置标准预测头使用边界 Anchor

> Migrated from [11_03_cross_position_standard_head_use_boundary_anchor_cn.md](11_03_cross_position_standard_head_use_boundary_anchor_cn.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**现象：** MTP 可以在当前位置形成有用方向，却没有改善一个词元之后的标准答案预测。

**机制判断：** 真正使用还要求信息穿过中间词元。跨位置状态转移可能把原本有用的方向旋转成不利方向，而单纯更换输出头并不会造成这一变化。

**核心观测：** 状态转移前后的标准头有用性，以及最终的保守 held-out 行为分数。

**决策：** 当前位置形成不是标准头收益的充分条件；停止在该代理任务上继续枚举桥接词或训练长度。

# Thinking Card — 干扰、容量与课程学习边界 Anchor

> Migrated from [12_02_interference_capacity_curriculum_boundary_anchor_cn.md](12_02_interference_capacity_curriculum_boundary_anchor_cn.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**现象：** 在受限共享表征中，额外未来监督可能让未来因子学得更好，同时使标准目标变差。

**机制判断：** 一步影响由梯度交互决定；持续权衡可以由任务相关表示秩不足造成。训练顺序无法创造一个结构上缺失的独立方向。

**核心观测：** 在受控秩干预下的标准损失差，并用未来因子误差确认 MTP 确实获得了额外信息。

**决策：** 在线性模型中，结构性秩竞争是一个充分机制；课程学习不能修复结构缺秩；暂不推断 Transformer 尺度规律。

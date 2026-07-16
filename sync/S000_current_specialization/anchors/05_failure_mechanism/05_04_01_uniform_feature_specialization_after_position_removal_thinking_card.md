# Thinking Card — Minimal Anchor Handwrite Draft

> Migrated from [05_04_01_uniform_feature_specialization_after_position_removal_anchor.md](05_04_01_uniform_feature_specialization_after_position_removal_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

父问题：为什么普通 sparse top-1 MoE router 不能稳定形成 feature-to-expert specialization？

当前子问题：在去掉显式 position-common 因素后，为什么 uniform slot 数据训练后仍然发生 expert collapse？

核心假设：slot 信息可能存在，但 top-1 router 的训练动态会被 non-slot component 或 early expert advantage 锁定，从而不按 slot 分发。

最小测试：构造 no-position / random-position slot task，追踪 route、logit margin、hidden component 和 router gradient trajectory。

当前边界：只研究 synthetic uniform slot setting；不声称解决真实 LM 的 specialization。

下一步决策：判断 collapse 是 missing slot signal、residual common bias，还是 top-1 training lock-in。

# Thinking Card — 2x2 Top-1 Router Lock-In Anchor

> Migrated from [02_ntp_style_top1_router_lockin_anchor.md](02_ntp_style_top1_router_lockin_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

目的：用最小 2 feature / 2 expert / top-1 NTP-style proxy 审查 router 为什么不能稳定形成 route-pattern specialization。

物理建模 / 假设：top-1 routing 对早期 router 几何非常敏感；如果不同 token 在 step 0/10 被分到同一个 expert，selected gate 会放大这个选择，并让未选 expert starvation。

最小实验：固定 $h_A=e_1,h_B=e_2$，2 experts，linear top-1 router，next-token CE；审查 early trajectory、success dynamics、router bias。

当前结论：失败 seed 在 step 0 已 collapse，不是训练中 drift；成功 seed 在 step 0 split 后会稳定保持并形成 counterfactual CE advantage；去掉 router bias 将 random-init split 从 3/10 提高到 6/10，但不能保证 specialization。

结论边界：只 claim 当前最小 top-1 NTP-style proxy 的 route-pattern dynamics；不 claim full LM、attention 场景或 utility-aligned specialization。

下一步：测试一个 anti-lock-in 机制，优先 structured router initialization，其次 exploration noise 或 load-balancing。

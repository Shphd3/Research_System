# Meeting Brief

## Meeting Summary

结论：

在去除坍缩的 best S0/S1-cos 条件下，router 的主要 route axis 更像 slot，而不是 B_i；exact (slot, B_i) 仍然是 same-feature consistency 的 atomic key。

最小理由：

1. H0604a 显示 exact (slot, B_i) consistency 很高，说明 weak same-feature route consistency 基本成立。
2. H0604b 在去掉坍缩的seeds后显示，S0/S1-cos 的 NMI(route; slot) 高，而 NMI(route; B_i) 接近 0，说明当前最佳非坍缩 routing 更像 slot-aligned，而不是 identity-aligned。

当前解释：

Observation: exact (slot, B_i) 稳定性高；best non-collapsed routing 主要携带 slot 信息。
Interpretation: slot 可以作为下一步 diagnostic 的 operational feature axis。
Boundary: 这不是 expert utility specialization，也不能说明 center separation 有独立因果增益。

## Meeting Preparation

**Question:**

在当前 uniform multi-B synthetic 中，router 实际绑定的是 slot、B_i，还是 composite key = (slot, B_i)？

**Why this matters?**

在导师给出的最简 setting 中，我们依赖三个假设：

1. 一个 token 中的 feature 是 single feature；
2. feature 分布是 uniform；
3. 不考虑多个 feature 进入同一个 expert 后的关系。

我们这次先处理第一个假设。
如果 feature axis 本身不清楚，后续讨论 specialization、utility binding 或 Zipf 都没有稳定对象。

**Hypothesis:**

在当前 non-collapsed 条件下，router 的主要 route axis 更可能是 slot，而不是 B_i；但 exact (slot, B_i) 仍是 same-feature consistency 的 atomic key。

**Evidence:**

1. H0604a: exact (slot, B_i) consistency 高，支持 weak same-feature route consistency。
2. H0604b: collapse-filtered S0/S1-cos 中，NMI(route; slot) 高，NMI(route; B_i) 低，支持 slot-aligned route axis。
3. Collapse guard: high consistency 可能由 collapse 造成，所以 consistency 不能单独作为 specialization 证据。

**Boundaries:**

当前结论只覆盖：

* uniform multi-B synthetic；
* collapse-filtered runs；
* S0/S1-cos best conditions；
* route assignment 层面的 feature-axis audit。

**Cannot claim yet:**

* 不能 claim expert utility specialization；
* 不能 claim center separation independently caused specialization；
* 不能 claim Zipf / high-frequency robustness；
* 不能 claim real-data generalization；
* 不能 claim 同一 expert 内多个 slot features 已经有 meaningful relation。

**Next Decision:**

下一步不进入 route-utility binding，也不进入 Zipf。
下一步只放松第三个假设：

当多个 slot features 进入同一个 expert 后，它们之间是什么关系？

**Next Iteration:**

Run same-expert feature composition audit.

核心问题：

Given non-collapsed slot-aligned routing, do multiple slot features routed into the same expert share any geometric, predictive, or training-dynamic relation?

需要区分：

1. arbitrary bucket；
2. collapse / near-collapse；
3. geometry-based grouping；
4. predictive-target grouping；
5. training-dynamic grouping。

# Thinking Card — NTP Zipf Feature Write-In And Router Factor Attribution

> Migrated from [04_ntp_zipf_feature_factorization_anchor.md](04_ntp_zipf_feature_factorization_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

父问题：

```text
端侧 MoE swapping 需要 feature-level expert specialization：高频/共享计算应常驻，低频/差异化 feature 应由更小的 dynamic unique expert 处理。
```

当前子问题：

```text
在受控 NTP 任务中，Zipfian feature frequency 是否会让模型优先写入 / 路由到 high-frequency component，而使 tail/unique/slot feature 不能稳定形成 route-utility binding？
```

为什么要问这个问题：

```text
上一轮 slot-context 实验显示：slot 信息在 hidden state 中可见，oracle routing 可行，但 ordinary top-1 routing 在 multi-B 中不能稳定绑定 slot feature 与 utility-best expert。

H-MoE/common path 实验显示：common_flat 有弱帮助，但 two-level hierarchy 本身没有稳定超过 common_flat；因此不能声称 H-MoE 结构已经解决 gating problem。

linear FFN/KV toy 显示：在非 NTP 的最小线性任务中，Zipf frequency 会让 head feature 先写入 W、tail feature underfit，reweight 可以恢复；但这个 toy 不能直接证明 NTP/Transformer/MoE 中的 router 也按这个机制失败。
```

决策问题：

```text
下一步应该做 architecture 深化，还是先做 NTP factor attribution，判断到底是 common component、head-frequency component、B identity，还是 slot/target feature 在控制 routing 和 expert utility？
```

任务构造：

```text
构造一个有 ground-truth factors 的 NTP synthetic：
slot context + B-family + B_i -> target Y_{slot, family, i}

其中 factors 明确分为：
common context / head-frequency unique / B-family or B-identity / slot-target feature / tail unique feature。

比较 uniform 与 Zipf frequency；训练 ordinary flat MoE、common_flat、以及可选 high-frequency-removed leaf router。
```

当前结果 / 预期结果：

```text
已有结果不能直接证明 NTP 下的 Zipf router failure。
当前预期是：如果 linear FFN toy 的机制能迁移到 NTP，那么 Zipf NTP 中应出现 head/tail expert write-in 差异、router logit 被 high-frequency component 控制、tail/slot route-utility binding 下降；reweight 或 high-frequency removal 应减弱这些现象。

如果 NTP 中没有这些现象，则 linear FFN toy 只说明一个底层优化现象，不能继续作为 H-MoE/gating story 的直接证据。
```

结论边界：

```text
这个 anchor 只判断 NTP 训练中 frequency-driven factor dominance 是否真实影响 routing 与 expert utility。
它不能直接证明真实语料 specialization，也不能直接证明系统侧 swapping 收益。
```

下一步：

```text
先做 NTP factor attribution，而不是继续加 hierarchy 深度。
若 attribution 显示 router 主要被 high-frequency/common/head factors 控制，再测试 high-frequency-removed leaf router。
若 attribution 显示 tail/slot feature 根本没有写入 expert function，则优先考虑 reweight / tail-write-in pressure，而不是只改 router。
```

---

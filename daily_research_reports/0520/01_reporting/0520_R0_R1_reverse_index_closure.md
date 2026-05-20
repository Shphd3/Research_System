# 0520 Closure Brief: R0/R1 Reverse Index 诊断

## 1. Core Purpose And Hypothesis

目的：验证 MoE expert bucket 能不能作为 attention 的 KV 候选集合。

核心假设：

```text
如果 expert bucket 是好的 Reverse Index，
那么 restricted attention 只看 same-bucket KV 时，
CE 应该明显小于 random same-count KV。
```

## 2. Closure Decision

结论是中间支持：

```text
router bucket 有检索信号，但 one-feature-one-expert 不是 Reverse Index 的充分条件。
```

## 3. Key Evidence

旧 R0/R1 说明：把 feature 强行分到不同 expert 后，same-bucket RI 比 random 更好，但仍远不如 local / same-feature oracle。

修正版 post-attention R0/R1 说明：same-bucket KV 在 uniform / zipf 上都显著优于 random same-count KV。

关键反例：

| data | model | NMI | RI $\Delta CE$ | random $\Delta CE$ |
|---|---:|---:|---:|---:|
| uniform | P1 oracle feature-router | 1.000 | 1.425 | 2.982 |
| uniform | P2 clean inhibition | 0.459 | -0.001 | 2.553 |
| zipf | P1 oracle feature-router | 1.000 | 0.892 | 2.646 |
| zipf | P0 natural router | 0.398 | 0.297 | 2.894 |

P1 的 NMI 最好，但 CE 不是最好，所以 NMI 不能作为 RI 成功指标。

## 4. Claim Boundary

可以说：

```text
post-attention router bucket 明显优于 random KV，说明 bucket 有检索信号。
```

不能说：

```text
one-feature-one-expert 已经解决 Reverse Index。
```

也不能说：

```text
当前方法已经能替代 dense attention 或带来真实加速。
```

## 5. Next Decision

下一步做 candidate generator tournament：

```text
bucket
local
same-feature oracle
dense top-M oracle
bucket + local
hidden/key/value nearest neighbors
```

评价中心从 `NMI` 转到：

```text
CE delta
attention mass retained
target probability drop
candidate budget
```

## 6. 30s Explanation

我这轮直接测 expert bucket 能不能当 KV 检索索引。结果是 same-bucket KV 明显比随机 KV 好，说明 router bucket 有检索信号；但最干净的 one-feature-one-expert 模型 CE 反而不是最好。所以现在的判断是：feature 分开不是 Reverse Index 的充分条件，下一步要系统比较候选生成器，而不是只追求更高 NMI。

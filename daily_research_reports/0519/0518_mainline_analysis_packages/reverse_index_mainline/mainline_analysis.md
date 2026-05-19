# Mainline B: Reverse Index / Attention-MoE Compatibility

## 一句话结论

Reverse index 的核心疑问不是“router 是否 clean”，而是“query 选择的 expert buckets 是否覆盖 dense attention 真正需要的历史 KV，并且这种覆盖能以更低 memory access 保持 NTP loss”。

## Decision Question

在 2-layer Transformer + MoE 中，仅第二层 attention 使用 reverse index 时：

```text
Does MoE-derived candidate selection preserve layer2 dense-attention behavior and NTP loss under matched candidate budget?
```

## 当前阶段设计

### Stage 1: Routing analysis

```text
1-layer Transformer + MoE
Gate input = attention output
Expert input = unchanged hidden
Goal = understand classification boundary
```

### Stage 2: Reverse index method judgment

```text
2-layer Transformer + MoE
Only layer2 attention uses reverse index
Compare full-attn vs RI on same trained checkpoint and RI-trained checkpoint
```

## 关键逻辑条件

对 layer2 query $q_t$，dense attention 的 high-mass keys 为 $H_t$。一个 reverse index 方法成立，需要：

```text
CandidateBuckets(t) contains most j in H_t
```

仅有 `same feature -> same expert` 不够。需要验证：

```text
feature / expert bucket overlap with H_t
attention mass retained
attention output reconstruction
final logits / NTP loss
memory access cost
```

## 为什么之前方法逻辑链差一环

之前方法隐含链条是：

```text
feature-aligned routing
-> same feature keys in same bucket
-> attention wants same-feature keys
-> RI works
```

断点在第三步：attention 不一定按人工 feature 取 KV。它可能按：

```text
locality
token identity
hidden cosine similarity
value similarity
position/head pattern
query-specific previous attention source
```

因此下一步必须做 source decomposition。

## 两种 reverse-index 判断方式

### A. 前向算两遍 / second-layer MoE guide

用途：analysis upper bound。先用 full layer2 attention 得到 gate / bucket，再用 bucket 做 RI，测试“若已知第二层 route，bucket 是否有用”。

边界：这不能直接 claim speedup，因为要先算 full attention 或多一次前向。

### B. 上一层 MoE / layer1 signal guide

用途：valid acceleration candidate。用 layer1 attention output / layer1 MoE route 指导 layer2 attention candidate。

边界：可能 signal 不够，需要测 layer1 signal 到 layer2 high-mass KV 的 predictiveness。

## Source Decomposition

对每个 query t，取 dense layer2 attention top/mass keys，然后问：这些 key 由什么解释？

Candidate generators:

```text
Local window
same token id
same synthetic feature
same layer1 expert bucket
same layer2 expert bucket two-pass
nearest hidden cosine
nearest key cosine
nearest value cosine
random same-count
oracle top attention
```

Metrics:

```text
recall@budget
attention mass retained
attention output error
logit KL / target logit delta
NTP loss delta
candidate count / memory bytes / bucket switches
```

## Claim Strength

当前 `supervised feature routing -> RI poor` 是 weakly supported，因为代码和 metric 需要复查。`feature routing is not sufficient for RI` 是 plausible，但要在新 model setting + NTP loss metric 下复验。

## What cannot be claimed

不能说 reverse index 不可能；不能说 MoE bucket 无用；不能说 local baseline 强就代表长上下文没价值；不能说 full-attn train + RI infer 的失败等价于 RI train 的失败。

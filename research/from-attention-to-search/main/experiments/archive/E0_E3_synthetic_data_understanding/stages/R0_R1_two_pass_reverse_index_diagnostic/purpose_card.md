# Purpose Card: R0/R1 Two-Pass Reverse Index Diagnostic

## 1. Purpose / Main Reason

本实验直接测试 Reverse Index 的最小可行问题：

```text
如果用 router bucket 给历史 KV 建索引，当前 query 只看同 bucket KV，
能否比 random same-count KV 更接近 dense attention，并降低 CE 损失？
```

重点不是证明加速，而是判断 router bucket 是否有检索价值。

## 2. Mainline Position

E4 研究的是 router 是否能形成 feature-aligned expert assignment。R0/R1 进一步问：

```text
即使 feature 被分到不同 expert，这种 bucket 是否真的覆盖 layer2 dense attention 需要的 KV？
```

这是进入真正 Reverse Index 前的 sanity / diagnostic。

## 3. Known Narrative / Premise

前序结果显示：

- natural router 不一定按 feature 分；
- soft feature signal 可以把 feature 分到不同 expert；
- 但 high NMI 不能等价为可检索 KV index；
- Reverse Index 的关键指标应是 CE delta、attention mass retained、attention output reconstruction，而不是 router NMI。

## 4. Experiment Purpose

比较三种模型在 uniform 与 Zipf 数据上的 two-pass RI 效果：

```text
M0: natural router + LB
M1: soft feature-router regularization, lambda=0.05
M2: stronger soft feature-router regularization, lambda=0.20
```

核心判据：

```text
ri_same_bucket 是否比 random_same_count 有更低 CE delta。
```

## 5. Hypothesis And Sub-Hypotheses

主假设：

```text
H-RI: 如果 feature-aligned router bucket 是有效 KV index，
那么 soft feature-router regularization 应提高 routing NMI，
并使 same-bucket RI 的 CE delta 明显低于 random same-count。
```

细化假设：

- H-RI1: M1/M2 会把四个人工 feature 分到不同 expert。
- H-RI2: 如果 bucket 有检索价值，`ri_same_bucket` 的 attention mass retained 和 CE delta 应优于 `random_same_count`。
- H-RI3: 如果 feature bucket 不是 attention source，NMI 提高也不会带来接近 local / same-feature oracle 的 CE。
- H-RI4: Zipf 下低频 feature 可能削弱 bucket 的检索稳定性。

## 6. Experiment Object

模型为 2-layer diagnostic Transformer：

```text
layer1 attention_output -> router -> expert bucket
layer2 full attention    -> dense teacher
```

RI candidate 使用 layer1 router bucket，评估时重算 layer2 restricted exact attention。

## 7. Experiment Paradigm

每个 query 位置先跑 full attention，记录 dense layer2 attention teacher；然后用不同 candidate generators 重算 restricted attention：

```text
random same-count
ri same-bucket
ri top2 buckets
local same-count
same token
same feature oracle
oracle dense top-M
```

## 8. Expected Outcomes And Hypothesis Update Logic

如果 H-RI 成立：

```text
soft feature routing 会显著降低 RI CE delta，并接近 local / same-feature oracle。
```

如果只提高 NMI，不降低 CE：

```text
feature-aligned expert assignment 不足以作为 Reverse Index。
```

如果 same-feature oracle 好而 RI bucket 弱：

```text
attention 可能确实需要 feature-relevant KV，但当前 router bucket 不是合适 candidate generator。
```

## 9. What This Can Prove

可以证明：

```text
在当前 toy setting 中，feature-aligned router bucket 是否比 random KV 更适合作为 layer2 attention candidate。
```

## 10. What This Cannot Prove

不能证明：

- 真实长上下文任务可加速；
- two-pass diagnostic 本身可省算力；
- feature-aligned routing 等于真实 semantic retrieval；
- 当前失败能否通过 train-time RI 自动修复。

## 11. Result

见 `summary.md`。

## 12. Conclusion

见 `summary.md`。

## 13. Next Step

若 RI same-bucket 不接近 local / same-feature oracle，则下一步不是继续提高 NMI，而是做 candidate generator tournament 与 RI train/infer mismatch。

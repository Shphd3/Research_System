# Daily Card - 0520

## 1. Today's Purpose

把 E4 的 router failure-mode 线整理成可执行的下一步：先完成 raw-attention C0-C7，再用 E4.1 shortcut controls 判断 one-feature-one-expert 是否真的来自上下文关系，最后决定是否进入 Reverse Index。

## 2. Mainline Anchor

当前主线问题不是“router 能不能分得好看”，而是：

```text
router assignment、router boundary、expert utility、NTP readback 是否同时一致。
```

只有这四者同时成立，才可以把 MoE routing 接到 Reverse Index。

## 3. Task Conclusions

### Task 1: C0-C7 任务梳理

Did:

整理 E4 raw-attention setting 下 C0-C7 的作用。

Conclusion:

- C0 是普通 linear router baseline；
- C1/C2 检查 center router 和 center repulsion 是否足够；
- C3/C4 是旧 CE-margin inhibition；
- C5/C6 是 clean expert inhibition，检查 loser experts 是否能被反向排斥而不污染 shared path；
- C7a-C7e 是 Dingyi-style oracle-init prototype router，检查 feature cluster 初始化是否能稳定转成 expert routing。

### Task 2: E4.1 shortcut-controlled Oracle-MoE

Did:

规划 E4.1：在 `shared_prefix_end_uniform`、`shared_target_uniform`、`crossed_factorial_uniform` 上复验关键 C variants。

Conclusion:

E4.1 是进入 Reverse Index 前的必要控制。它判断 E4 的 routing 是否真按 relation-level feature，而不是按 prefix-end token、target token 或 attention source shortcut。

### Task 3: Reverse Index 使用顺序

Did:

阅读 `reverse_index_mainline` 的 R0-R4 逻辑。

Conclusion:

E4/E4.1 不能直接证明 Reverse Index 可用。完成 E4.1 后应先做 R1 dense attention source decomposition，判断 layer2 attention high-mass KV 到底由 feature、expert bucket、locality、token、hidden/key/value similarity 中哪个变量解释。

### Task 4: R0/R1 Two-Pass RI Diagnostic

Did:

训练 2-layer diagnostic Transformer，在 uniform 和 Zipf 数据上比较 natural router、soft feature-router regularization $\lambda=0.05$、soft feature-router regularization $\lambda=0.20$，并做 two-pass RI candidate evaluation。

Conclusion:

soft regularization 可以把 feature-expert NMI 推到 1.0；M1 的 same-bucket RI 在 CE delta 上优于 random same-count，但仍远弱于 local / same-feature oracle。结论是：one-feature-one-expert 有检索信号，但不足以作为 Reverse Index candidate generator。

### Task 5: Corrected Post-Attention Two-Pass RI

Did:

按照 `full attention -> post-attention router/MoE -> logits` 的结构重做 RI 诊断。第一遍记录 full attention 与 expert bucket，第二遍只让 query attend 到同 bucket KV，再比较 CE。

Conclusion:

post-attention RI bucket 在 uniform / Zipf 上都显著优于 random same-count KV；但 oracle feature-router `P1` 虽然 `NMI=1.0`，RI CE 反而差于 natural / clean-inhibition router。结论更新为：bucket 有 RI 信号，但 one-feature-one-expert 不是 RI 候选质量的充分条件。

## 4. Mainline Update

今天新增 corrected post-attention R0/R1 two-pass RI 结果。主线判据被明确为：

```text
feature assignment + boundary alignment + expert utility + readback
```

并且 RI 判断必须看：

```text
CE delta over random, not only NMI / recall.
```

具体更新：

```text
post-attention router buckets contain useful KV candidate signal above random,
but one-feature-one-expert assignment is not sufficient for good Reverse Index.
```

## 5. What I Cannot Claim Yet

- 不能说 E4 的 one-feature-one-expert 是 relation-level feature routing；
- 不能说 Dingyi-style oracle-init 一定优于普通 router，raw-attn full run 还未完成；
- 不能说 feature-aligned routing 会带来 Reverse Index 检索收益；
- 不能把 high NMI 单独当成 functional specialization。
- 不能说当前 same-bucket RI 已经足以替代 dense attention。

## 6. Next Decision

1. 不再单纯追求更高 feature-expert NMI。
2. Reverse Index 下一步做 candidate generator tournament：`local`、`same-feature`、`bucket`、`local+bucket`、`nearest hidden/key/value`。
3. 再做 RI train/infer mismatch：`full-train + RI-infer` vs `RI-train + RI-infer`。
4. E4.1 shortcut controls 仍是 router 机制线的必要控制。

## 7. 30s Explanation

我们现在有了 corrected post-attention two-pass RI 结果：same-bucket KV 明显好于 random same-count KV，说明 router bucket 确实有检索信号；但 oracle one-feature-one-expert 的 RI CE 反而不如 natural / inhibition router。所以 Reverse Index 不能只看 NMI，下一步要用 CE delta 和 attention mass 比较候选生成器。

## 8. Recording / Class Notes

None.

## 9. Small Thought Parking Lot

突然想到的点：

Reverse Index 的真正上界不是 feature oracle，而是 dense attention top-M oracle。

为什么看起来重要：

如果 feature bucket 召回差但 attention top-M oracle 好，说明失败点在 candidate generator，不是 sparse attention 本身。

是否阻塞当前 25 分钟任务：否

回看时间：完成 E4.1 后。

# Result Summary: R0/R1 Two-Pass Reverse Index Diagnostic

## Purpose And Hypothesis

本实验测试：如果用 router bucket 给 layer2 历史 KV 做 candidate selection，`ri_same_bucket` 是否比 `random_same_count` 更接近 dense attention，并降低 CE。

核心假设是：如果 feature-aligned router bucket 是有效 Reverse Index，那么 soft feature-router regularization 提高 feature-expert NMI 后，也应降低 same-bucket RI 的 CE delta。

## Observation

Soft feature-router regularization 成功把 feature 分到 expert：

| dataset | model | feature-expert NMI |
|---|---:|---:|
| uniform | M0 natural | 0.612 |
| uniform | M1 soft 0.05 | 1.000 |
| uniform | M2 soft 0.20 | 1.000 |
| zipf | M0 natural | 0.712 |
| zipf | M1 soft 0.05 | 1.000 |
| zipf | M2 soft 0.20 | 1.000 |

但 CE 指标显示：clean feature routing 只带来有限 RI 改善，且远弱于 local / same-feature oracle。

主指标：

$$
\Delta CE = CE_{\text{candidate attention}} - CE_{\text{full attention}}
$$

| dataset | model | random $\Delta CE$ | RI same-bucket $\Delta CE$ | RI better than random |
|---|---:|---:|---:|---:|
| uniform | M0 | +0.608 | +0.534 | +0.074 |
| uniform | M1 | +0.182 | +0.034 | +0.148 |
| uniform | M2 | +0.425 | +0.204 | +0.222 |
| zipf | M0 | +0.211 | +0.248 | -0.037 |
| zipf | M1 | +0.134 | +0.030 | +0.104 |
| zipf | M2 | +0.386 | +0.290 | +0.095 |

对照项显示 local / same-feature oracle 更接近 full attention：

| dataset | model | local $\Delta CE$ | same-feature oracle $\Delta CE$ | dense top-M oracle $\Delta CE$ |
|---|---:|---:|---:|---:|
| uniform | M1 | +0.001 | +0.001 | -0.000 |
| zipf | M1 | +0.000 | +0.001 | -0.000 |

## Interpretation

M1 是当前最有用的 soft regularization：它把 NMI 提到 1.0，并让 same-bucket RI 相比 random 明显变好。

但这不是 Reverse Index 成功的强证据。原因是：

- RI same-bucket 的 CE delta 仍明显高于 local 和 same-feature oracle；
- M2 更强正则并没有继续改善 CE，反而比 M1 更差；
- Zipf natural M0 中 same-bucket CE 比 random 还差，说明自然 bucket 不稳定；
- NMI 从 0.6/0.7 到 1.0 并不等价于 attention KV candidate 质量足够。

当前更合理的解释是：

```text
feature-aligned routing 可以改善 bucket 候选，但 dense layer2 attention 需要的 KV 不完全由 expert bucket 覆盖。
```

## Limitation

本实验是 two-pass diagnostic，不是加速实验。full attention 被用于 teacher 评估，所以不能 claim latency speedup。

本实验使用 synthetic feature labels 训练 M1/M2 的 soft router regularization；这只能作为 toy diagnostic，不是现实语言可用方法。

## Key Figures

![Uniform CE Delta](figures/fig_uniform_ce_delta_baselines.png)

Uniform 下，M1 的 RI same-bucket 比 random 明显更低 CE，但仍不接近 local / same-feature oracle。

![Zipf CE Delta](figures/fig_zipf_ce_delta_baselines.png)

Zipf 下，M1 仍优于 random；M0 的 same-bucket 反而弱于 random。

![Uniform RI Improvement](figures/fig_uniform_ri_ce_improvement_vs_random.png)

Uniform 下，M1/M2 都比 random 好，但 M2 更强正则未带来更低绝对 CE。

![Zipf RI Improvement](figures/fig_zipf_ri_ce_improvement_vs_random.png)

Zipf 下，M1 是最好折中；M2 的 feature separation 更强但 CE 变差。

## Claim Update

Supported:

- soft feature-router regularization 可以强制 feature-expert assignment；
- feature-aligned bucket 比 random same-count 更有 candidate signal，尤其 M1；
- CE delta 是比 NMI 更关键的 RI 判断指标。

Weakened:

- clean one-feature-one-expert routing 不足以证明 Reverse Index 可用；
- 更强 feature separation 不一定更好，M2 的 CE 明显差于 M1；
- natural router bucket 在 Zipf 下不可靠。

Still unclear:

- local / same-feature oracle 为什么能接近 full attention；
- train-time RI 是否能让模型适应 bucket restriction；
- hybrid generator，如 local + bucket，是否能同时降低 candidate count 和 CE。

## What Cannot Be Claimed

不能 claim：

- Reverse Index 已经成功；
- feature-aligned expert bucket 足以替代 dense attention；
- NMI=1.0 就能带来有效 KV retrieval；
- 当前 two-pass diagnostic 有速度收益。

## Next Decision

下一步不应继续单纯提高 feature-expert NMI。

优先做：

1. Candidate generator tournament：`local`、`same-feature`、`bucket`、`local+bucket`、`nearest hidden/key/value`。
2. R3 train/inference mismatch：比较 full-train + RI-infer 与 RI-train + RI-infer。
3. 重点汇报 CE delta over random，而不是只汇报 recall 或 NMI。

# Result Summary: R4 Attention-Output Router Retrieval

### Purpose And Hypothesis

R4 检查：当 router 使用 block1 attention output、不含 residual 进行 routing 时，reverse index 是否比 R3 更接近 block2 dense attention 的 KV 检索结构。

### Observation

两组 full run 已完成：

- uniform: `pt-hmaan5mc`, 4 GPU, 07:07:07-07:10:20 UTC。
- longtail: `pt-inv9rx4o`, 4 GPU, 07:09:31-07:12:32 UTC。

主要结果：

| Data | Variant | Best valid CE | Feature prob | Router NMI | K=1 recall | K=1 mass | K=1 L2 | K=1 CE delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| uniform | NTP only | 6.631 | 0.999 | 0.720 | 0.273 | 0.390 | 1.161 | 0.701 |
| uniform | NTP + RouterFeatureCE | 6.629 | 0.994 | 1.000 | 0.308 | 0.380 | 1.100 | 2.311 |
| longtail | NTP only | 6.685 | 0.961 | 0.187 | 0.286 | 0.286 | 1.242 | 0.301 |
| longtail | NTP + RouterFeatureCE | 6.683 | 0.982 | 1.000 | 0.324 | 0.453 | 1.125 | 2.868 |

对照组上，local same-count 的 K=1 CE delta 很小：uniform 约 0.124，longtail 约 0.069。说明当前 NTP 输出质量仍更依赖局部 KV，而不是 feature bucket。

### Interpretation

R4 削弱了“换成上一层 attention output 做 route 就能形成有效 reverse index”的假设。

关键点：

- RouterFeatureCE 可以把 attention-output router 强行变成 one-feature-one-index：Router NMI = 1.0。
- 但 feature-aligned bucket 的 sparse CE 明显不好，尤其 K=1/K=2 时 CE delta 大。
- NTP-only 分支反而在 CE delta 上更温和，但它的 router-feature alignment 不稳定，不能说明形成了干净 index。

因此，R4 与 R3 一致：feature specialization 本身不足以推出 KV retrieval usefulness。

### Limitation

- 这是 E-series all-trigram toy NTP，`seq_len=32`，不能外推到真实长上下文。
- 这里只比较 attention-output routing 与 RouterFeatureCE，不代表所有 memory router。
- 本轮每个数据分布 2 seeds，是快速支线判定，不是最终统计结论。

### Key Figures

- Uniform retrieval quality:
  ![R4 uniform retrieval](figures/r4_uniform_topk_retrieval_quality.png)

- Longtail retrieval quality:
  ![R4 longtail retrieval](figures/r4_longtail_topk_retrieval_quality.png)

- Training / readback / alignment:
  ![R4 training readback alignment](figures/r4_training_readback_alignment.png)

### Claim Update

可说：

```text
在当前 E-series all-trigram 设置中，将 router 输入改成 block1 attention output 并不能把 feature-aligned MoE bucket 变成高质量 block2 KV reverse index。
```

不能说：

```text
MoE/router 一般不能做 KV index；真实长上下文下 reverse index 不可能有效。
```

### Decision

下一步不应继续只强化 one-feature-one-expert。更关键的问题是诊断 block2 attention 到底按什么变量取 KV：locality、token identity、hidden similarity、value similarity，还是 feature identity。

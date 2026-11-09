# Result Summary: R0/R1 Post-Attention MoE Two-Pass RI

## Observation

本轮已经完成：`uniform / zipf` 两个数据集，`P0/P1/P2` 三个模型，每个 3 个 seed，共 18 个 run。每个 run 都生成了 checkpoint 和 RI summary。

模型代号：

| 代号 | 含义 |
|---|---|
| `P0` | post-attention natural router + LB |
| `P1` | post-attention oracle feature-router，强制 one-feature-one-expert |
| `P2` | post-attention clean inhibition + LB |

核心 CE 结果：

| data | model | NMI | RI ΔCE | random ΔCE | RI 优于 random | RI mass | random mass |
|---|---:|---:|---:|---:|---:|---:|---:|
| uniform | P0 | 0.501 | 0.230 | 2.922 | 2.693 | 0.697 | 0.410 |
| uniform | P1 | 1.000 | 1.425 | 2.982 | 1.557 | 0.643 | 0.386 |
| uniform | P2 | 0.459 | -0.001 | 2.553 | 2.554 | 0.712 | 0.417 |
| zipf | P0 | 0.398 | 0.297 | 2.894 | 2.597 | 0.670 | 0.421 |
| zipf | P1 | 1.000 | 0.892 | 2.646 | 1.754 | 0.655 | 0.396 |
| zipf | P2 | 0.409 | 0.344 | 2.682 | 2.338 | 0.638 | 0.424 |

`RI ΔCE` 是 same-bucket restricted attention 相对 full attention 的 CE 增量，越小越好。`random ΔCE` 是同样候选数量下随机 KV 的 CE 增量。

## Interpretation

第一，post-attention RI 明显优于 random same-count KV。所有设置下 `RI ΔCE` 都远小于 `random ΔCE`，说明 expert bucket 确实提供了候选信号。

第二，`P1` 虽然达到 one-feature-one-expert 的 `NMI=1.0`，但 RI CE 最差：uniform 下 `RI ΔCE=1.425`，zipf 下 `RI ΔCE=0.892`。这说明 feature-pure routing 不等于好的 RI 候选生成器。

第三，`P2` 在 uniform 上几乎无 CE 损失，zipf 上也优于 random 很多，但没有达到 clean feature assignment。当前更强的信号是：RI 更依赖 functional bucket 是否保留 attention 所需 KV，而不是是否按人工 feature 纯分配。

## Limitation

本实验仍是 synthetic toy setting。`same-feature oracle` 和 `oracle_dense_top_m` 只是上界诊断，不是实际可用 router。`P2` 的 uniform 负 CE 增量接近 0，应理解为评估噪声范围内的“无明显退化”，不是 restricted attention 优于 full attention 的机制性证明。

ACP 作业状态显示为 `SUSPENDED`，但 18 个 checkpoint、18 个 RI summary 和聚合表均已完整落盘，因此本地结果分析可用。

## Key Figures

![uniform CE delta](figures/fig_uniform_mean_ntp_loss_delta_mean.png)

![zipf CE delta](figures/fig_zipf_mean_ntp_loss_delta_mean.png)

![uniform attention mass](figures/fig_uniform_mean_attention_mass_retained_mean.png)

![zipf attention mass](figures/fig_zipf_mean_attention_mass_retained_mean.png)

## Claim Update

可以说：

```text
在 corrected post-attention two-pass RI 诊断中，router bucket 比 random same-count KV 明显更有用；但 one-feature-one-expert 并不是 RI 好候选的充分条件。
```

不能说：

```text
只要训练出 clean feature-expert specialization，就能得到可靠 Reverse Index。
```

## Decision

下一步 RI 不应只继续追求更高 NMI。更应该比较 candidate generator：natural bucket、inhibition bucket、local、same-feature oracle、dense top-M oracle，并分析哪些 bucket 真正保留 full attention 需要的 KV。

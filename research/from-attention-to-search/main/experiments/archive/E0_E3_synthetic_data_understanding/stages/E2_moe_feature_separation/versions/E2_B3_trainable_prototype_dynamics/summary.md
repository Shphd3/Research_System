# Result Summary: E2-B3 Trainable Prototype Dynamics

## Observation

E2-B3 修正了 E2-B / E2-B2 的关键问题：旧 hard top-1 prototype routing 中，NTP loss 不会反传到 prototype centers。修正后使用 gate-value top-1：

$$
y_t=p_{t,e^*}\mathrm{Expert}_{e^*}(h_t)
$$

本轮 3 variants × 3 seeds 已完成。自然版第一步已经有非零 prototype 梯度，说明梯度链路成立：

| variant | first prototype grad | final prototype movement |
|---|---:|---:|
| natural NTP | 0.0050 | 1.6864 |
| center separation | 0.0706 | 1.4910 |
| supervised CE | 4.1205 | 1.3043 |

最终 routing 结果：

| variant | readback | NMI | ARI | best-perm acc | fixed-label acc | load entropy | ablation drop |
|---|---:|---:|---:|---:|---:|---:|---:|
| natural NTP | 0.9957 | 0.5772 | 0.3333 | 0.5000 | 0.3333 | 0.0860 | 0.7457 |
| center separation | 0.9955 | 0.1924 | 0.1111 | 0.3333 | 0.2500 | 0.0618 | 0.7594 |
| supervised CE | 0.9969 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0233 | 0.4044 |

Prototype center geometry:

| variant | mean offdiag cosine | max offdiag cosine | min offdiag cosine |
|---|---:|---:|---:|
| natural NTP | -0.1328 | 0.4913 | -0.7192 |
| center separation | -0.2497 | -0.0007 | -0.6422 |
| supervised CE | -0.3167 | -0.1627 | -0.4527 |

## Interpretation

这次修正后的结论更强：

```text
prototype centers 在 NTP 下确实收到梯度并发生明显移动；
但自然梯度没有把 centers 演化成四个 feature centers。
```

Center separation 把 centers 分开了，max offdiag cosine 从 natural 的 `0.4913` 压到 `-0.0007`，但 NMI 反而从 `0.5772` 降到 `0.1924`。这说明：

```text
centers 彼此远离，不等于 feature clusters 被分配到不同 centers。
```

Supervised CE 达到 `NMI=1.0`，说明模型结构、prototype centers、expert 数量、route 位置都能支持 clean specialization。失败不来自代码链路或模型容量，而来自自然 NTP / center-separation objective 没有提供 feature-to-expert assignment pressure。

## Limitation

本轮只跑 3 seeds，但三组之间差异很大，足够作为纠错后的判断。`expert_load_entropy` 是全 token load，不是 feature-prefix load；supervised CE 只约束 feature-prefix 位置，因此全 token load 仍可能集中。

## Key Figures

![prototype grad](figures/prototype_grad_norm_over_steps.png)

![prototype movement](figures/prototype_delta_from_init_over_steps.png)

![routing matrix](figures/routing_matrix_by_variant.png)

![prototype cosine](figures/prototype_cosine_heatmap.png)

![feature centroid to prototype](figures/feature_centroid_to_prototype_heatmap.png)

## Claim Update

可以更新为：

```text
在修正为可反传的 gate-value top-1 prototype router 后，
natural NTP 确实能移动 expert centers，
但仍不能自然形成 clean one-feature-one-expert。
```

E2-B2 的“center separation 不足以产生 clean assignment”仍成立，但现在证据更可靠：它是在 NTP 能反传到 prototype 的条件下得到的。

不能说：

- prototype centers 没有收到梯度；
- center separation 完全无用；
- 真实语言中无监督 center-based router 一定无效。

## Decision

E2-B3 替代 E2-B2 作为 prototype center dynamics 的可信版本。下一步若继续追求现实可用的一对一路由，不能只做 center repulsion，需要 assignment-level pressure，例如 entropy-balanced clustering、mutual-information-style assignment，或让任务本身使 feature-to-expert 独占变成 loss 上的必要解。

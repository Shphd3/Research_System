# Result Summary: E2-B2 Prototype Center Separation

## Correction Note

This result is superseded by `E2_B3_trainable_prototype_dynamics`.

E2-B2 used hard top-1 prototype routing where expert output was not multiplied
by the selected gate probability. Therefore natural $L_{\text{NTP}}$ did not
reliably backpropagate into prototype centers. E2-B3 fixes this with gate-value
top-1 routing and should be used as the claim-safe version for prototype center
dynamics.

## Observation

E2-B2 已完成 3 variants × 3 seeds。实验不使用 feature label supervision，只在 prototype router 上加入 center separation loss。

结果：

| variant | readback | NMI | ARI | best-perm acc | fixed-label acc | load entropy | ablation drop |
|---|---:|---:|---:|---:|---:|---:|---:|
| prototype_center_sep_0_1_no_lb | 0.9952 | 0.4843 | 0.2980 | 0.5077 | 0.2493 | 1.1363 | 0.3629 |
| prototype_center_sep_1_0_no_lb | 0.9948 | 0.4875 | 0.3077 | 0.5238 | 0.2487 | 1.1414 | 0.3980 |
| prototype_center_sep_1_0_lb | 0.9949 | 0.5783 | 0.3793 | 0.5284 | 0.2381 | 1.3862 | 0.4060 |

Prototype centers 的 off-diagonal cosine 已经被压到非正：

| variant | mean offdiag cosine | max offdiag cosine | min offdiag cosine |
|---|---:|---:|---:|
| prototype_center_sep_0_1_no_lb | -0.0755 | -0.0127 | -0.2424 |
| prototype_center_sep_1_0_no_lb | -0.0756 | -0.0127 | -0.2424 |
| prototype_center_sep_1_0_lb | -0.0221 | -0.0011 | -0.1440 |

训练日志中 final `center_sep_loss = 0.0`，说明 center separation 目标本身被满足。

## Interpretation

这个实验给出一个清楚结论：

```text
把 expert centers 撑开，可以避免 center collapse；
但不能自动产生 clean feature-to-expert assignment。
```

与 E2-B no-aux prototype baseline 相比，center separation 没有把 NMI 推到接近 1。LB 版本让 load entropy 接近 $\log 4$，并把 NMI 提到 0.5783，但仍远低于 supervised prototype aux 的 `NMI = 1.0`。

因此，当前缺失的不是“centers 是否彼此分开”，而是：

```text
feature clusters 是否被目标函数推向不同 centers。
```

## Limitation

本轮只跑 3 seeds，不是 5 seeds full sweep。但三个 seeds 已足够判断该机制没有出现接近 clean 的趋势。

当前 center separation loss 使用 margin $m=0$，只惩罚正余弦相似度。它不能排除更复杂的无监督 assignment objective，例如 mutual information 或 entropy-balanced cluster assignment。

## Key Figures

![routing matrix](figures/routing_matrix_by_variant.png)

![prototype cosine](figures/prototype_cosine_heatmap.png)

![best permutation](figures/best_permutation_accuracy_by_variant.png)

![ablation delta](figures/ablation_delta_by_variant.png)

## Claim Update

E2-B2 强化了 E2-B / E2-C / E3 的主线判断：

```text
representation geometry pressure 或 center geometry pressure 本身不足以保证 one-feature-one-expert；
要实现 clean routing，需要 assignment-level pressure。
```

可以说：

- center separation 是实际可用的无监督几何正则；
- 它能让 prototype centers 分开；
- 但在当前 synthetic NTP setting 中，它不能替代 feature-to-expert assignment supervision。

不能说：

- 所有无监督 router geometry 方法都无效；
- center separation 对真实 MoE 没价值；
- one-to-one routing 在所有设置中都必须监督。

## Decision

E2-B2 不需要扩展到 5 seeds。下一步如果继续追求实际可用 one-to-one，应该从单纯 center repulsion 转向 assignment-level objective，例如：

```text
maximize I(feature-like cluster; expert)
minimize H(expert | cluster)
maximize H(expert)
```

在 synthetic setting 中，可先用 feature label 做诊断；真实数据中则需要先定义可操作的 cluster / motif / semantic family。

# Result Summary: H0522b CB Context B Routing Seq32

Hypothesis purpose card:

The legacy purpose card was removed; this summary is the surviving result
source.

## Observation

本地两卡 run 已完成：

```text
h0522b_cb_context_b_routing_seq32_local2gpu_20260522
```

模型学会了主要 signal classes：

| Class | Mean accuracy |
|---|---:|
| A-only | 1.0000 |
| B-only | 1.0000 |
| AB-composite | 0.9997 |
| CB-composite | 1.0000 |

主指标是 `B source-token routing distribution across contexts per seed`。

`B_in_B_only / B_in_AB / B_in_CB` 在 3/4 seeds 中 dominant expert 完全一致；seed `20260524` 中三者分到不同 dominant expert。

## Interpretation

这更支持：

```text
B identity anchor 很强，left context 有调制，但不是跨 seed 稳定主导因素。
```

它削弱了一个强说法：

```text
AB 或 CB 语义上下文稳定决定 B source-token routing。
```

## Limitation

这个实验仍然不能证明 router 没有 context feature。它只能说明：在这个平衡 AB/CB 频率的设置下，B 的 identity trace 仍然很强；context effect 是 seed-dependent。

## Key Figures

![B context routing by seed](figures/b_context_routing_horizontal_by_seed.png)

这张图是主图：每个 seed 下比较 `B_in_B_only`、`B_in_AB`、`B_in_CB` 的 expert distribution。

![Source role routing by seed](figures/source_role_routing_matrix_by_seed_row.png)

这张图给出完整 source-role routing，对照 A/C/background roles。

## Claim Update

Supported:

```text
B source-token routing has a strong identity anchor.
```

Weakened:

```text
AB context stably rewrites B routing into an AB-specific expert.
```

Still unclear:

```text
whether stronger anti-identity tasks can force function-level routing.
```

## What Cannot Be Claimed

不能说 left context 完全无影响，因为 seed `20260524` 出现明显 context split。

## Next Decision

下一步若继续追 context-conditioned feature，需要做 anti-identity 控制，而不是继续只加更多 `XB` composite。

## Post-Hoc Subspace Analysis

追加分析读取同一批 checkpoint，不重新训练。目的只有一个：解释 seed `20260524` 为什么 `B_in_B_only / B_in_AB / B_in_CB` 能分开，并检查其他三个 seed 的 expert 是否更对齐 B identity。

结论：

```text
20260524 的 B-context hidden centroid 确实更分开，且 E1/E2 对 context
directions 的 top-4 SVD projection 很高；但 router-boundary alignment 很弱，
所以不能直接说 router boundary 稳定学到了 AB/CB feature。
```

关键图：

![B-position hidden PCA centroids](figures/subspace_analysis/b_context_hidden_pca_centroids_by_seed.png)

![B context centroid cosine](figures/subspace_analysis/b_context_centroid_cosine_by_seed.png)

![B context expert subspace projection](figures/subspace_analysis/b_context_expert_subspace_projection_rank4_by_seed.png)

![B context router boundary alignment](figures/subspace_analysis/b_context_router_boundary_alignment_by_seed.png)

# Result Summary: E2.1 Router Input Geometry Diagnostic

## Purpose And Hypothesis

E2.1 的目的，是解释 E2 中 MoE 为什么有 feature-expert alignment，却没有形成 clean one-feature-one-expert separation。

核心假设拆成三类：

- H2.1a：embedding 可分，但 router input 已经混合；
- H2.1b：router input 可分，但 router boundary 没有按 feature-difference direction 切分；
- H2.1c：多个 expert 都能预测同一 feature，因此没有独占 expert 的优化压力。

## Observation

E2.1 直接读取 E2 trained checkpoints，不重新训练：

```text
dataset = four_feature_all_trigram_v1000
model = 1-layer Transformer with 4-expert top-1 MoE FFN
variants = moe_top1_no_lb / moe_top1_lb
seeds = 20260513-20260517
features = ABC / DEF / GHI / JKL
position = prefix-end token for [A,B]->C
```

Feature 定义：

| Feature | Relation | Target count |
|---|---|---:|
| ABC | `[1,2] -> 22` | 10000 |
| DEF | `[3,4] -> 23` | 5000 |
| GHI | `[6,7] -> 20` | 500 |
| JKL | `[8,9] -> 21` | 100 |

Embedding geometry：

| Variant | Mean off-diagonal abs cosine | Max off-diagonal abs cosine |
|---|---:|---:|
| no-LB | 0.108 | 0.348 |
| LB | 0.109 | 0.376 |

Router input geometry：

| Variant | Mean centroid cosine | Fisher ratio mean | Fisher ratio range |
|---|---:|---:|---:|
| no-LB | 0.203 | 123.220 | 55.277-306.048 |
| LB | 0.214 | 104.152 | 52.645-199.311 |

Router boundary alignment:

| Variant | Mean abs alignment with dominant boundary | Max abs alignment |
|---|---:|---:|
| no-LB | 0.129 | 0.266 |
| LB | 0.109 | 0.176 |

Router margin / entropy:

| Feature | no-LB margin | no-LB entropy | LB margin | LB entropy |
|---|---:|---:|---:|---:|
| ABC | 0.374 | 1.301 | 0.250 | 1.365 |
| DEF | 0.234 | 1.334 | 0.094 | 1.372 |
| GHI | 0.139 | 1.338 | 0.182 | 1.366 |
| JKL | 0.348 | 1.334 | 0.226 | 1.359 |

Hidden-vs-routing similarity correlation:

| Variant | Correlation |
|---|---:|
| no-LB | 0.220 |
| LB | 0.175 |

Force-routing：

| Feature | no-LB dominant advantage | LB dominant advantage |
|---|---:|---:|
| ABC | 0.269 | 0.117 |
| DEF | 0.228 | 0.127 |
| GHI | 0.286 | 0.218 |
| JKL | 0.251 | 0.475 |

## Interpretation

E2.1 更支持 H2.1b 和 H2.1c，而不是 H2.1a。

Embedding 近似可分；router input centroid 也没有混成一团，Fisher ratio 很高，PCA 也显示 feature clusters 仍然存在。因此“不分开”不是因为 feature identity 在 router input 中消失。

但是 router boundary 与 feature-difference direction 的 alignment 很低，router entropy 接近 $\log(4)=1.386$，margin 也不大。这说明 router 没有强烈使用 feature-difference direction 来做 one-feature-one-expert 切分。

Force-routing 同时显示多个 expert 可以预测同一 feature，且 dominant expert 通常只是“更好”，不是唯一能预测。这支持 expert capacity sharing：当前 NTP loss 下，共享 expert 是可行解，clean one-feature-one-expert 不是必要解。

## Limitation

E2.1 使用 toy all-trigram corpus 和 tiny MoE。它说明这个 controlled setting 中的 imperfect separation 来自 router boundary choice 与 capacity sharing，但不能推出真实 LLM expert 的语义机制。

Boundary alignment 只分析线性 router weight direction；它不能解释 expert 内部所有非线性计算。

## Key Figures

![Embedding cosine](figures/embedding_token_cosine_heatmap.png)

![Router input centroid cosine](figures/router_input_centroid_cosine_heatmap.png)

![Router input PCA](figures/router_input_pca_by_feature_and_expert.png)

![Router boundary alignment](figures/router_boundary_alignment_heatmap.png)

![Router margin](figures/router_margin_by_feature.png)

![Router entropy](figures/router_entropy_by_feature.png)

![Hidden vs routing similarity](figures/hidden_vs_routing_similarity_scatter.png)

![Force routing probability](figures/force_routing_probability_by_expert.png)

![Dominant vs best forced expert](figures/dominant_vs_best_forced_expert.png)

![Dominant advantage](figures/dominant_advantage_by_feature.png)

## Claim Update

Supported:

- feature identity remains available in router input space;
- router boundary is weakly aligned with feature-difference directions;
- routing confidence is modest, especially under LB;
- multiple experts can support the same feature prediction;
- imperfect E2 separation is better explained by router boundary choice and expert capacity sharing than by representation collapse.

Weakened:

- “feature hidden states are mixed before routing” is not supported by this run;
- “one feature should map to one expert” is too strong for this setup.

Still unclear:

- whether stronger router regularization could force feature-aligned boundaries;
- whether top-2 routing would explicitly expose expert sharing;
- which expert-internal directions causally support feature readback.

## What Cannot Be Claimed

不能声称真实 LLM expert 也这样分工；不能声称 spectral direction 等于 semantic direction；不能声称 MoE router 已可用于 KV retrieval。

## Next Decision

下一步不应直接追求 one-feature-one-expert，而应测试 expert sharing 的机制：做 top-2 routing 或 direction-level expert ablation，判断共享 expert 中哪些方向对 feature readback 有因果作用。

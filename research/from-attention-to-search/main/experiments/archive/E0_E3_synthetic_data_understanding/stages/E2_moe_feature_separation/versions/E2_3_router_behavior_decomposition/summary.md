# Result Summary: E2.3 Router Behavior Decomposition

## Purpose And Hypothesis

E2.3 的目的，是解释 E2 中的反常现象：模型内部的 feature representation 已经可分，但 learned router 没有自然形成 clean one-feature-one-expert。

本轮加入 shared-B control，避免原始数据中每个 feature 都有独特 prefix-end token 的捷径。新数据为：

| Feature | Rule | Count | Control point |
|---|---|---:|---|
| ABC | `[1,2] -> 22` | 10000 | 与 DEF 共享 `B=2` |
| DEF | `[3,2] -> 23` | 5000 | 与 ABC 共享 `B=2` |
| GHI | `[6,7] -> 20` | 500 | 与 JKL 共享 `B=7` |
| JKL | `[8,7] -> 21` | 100 | 与 GHI 共享 `B=7` |

核心假设：

```text
如果 router 只是看 prefix-end token B，那么 shared-B 后 feature-expert alignment 应明显崩掉；
如果 router 使用更完整的 hidden representation，那么 shared-B 后仍能读回 feature，并且 expert choice 应更像由 full hidden / router-specific directions 解释。
```

## Observation

训练设置：

```text
dataset = shared_b_all_trigram_v1000
variants = moe_top1_no_lb / moe_top1_lb
seeds = 20260513-20260517
steps = 10000
```

### 1. Shared-B 数据仍可被 MoE 读回

| Variant | ABC | DEF | GHI | JKL |
|---|---:|---:|---:|---:|
| no-LB | 0.998 | 0.996 | 0.968 | 0.791 |
| LB | 0.999 | 0.995 | 0.963 | 0.821 |

这说明共享 `B` token 后，模型仍能学习 `[A,B]->C` 关系；它不是只靠单个 `B` token 完成预测。

### 2. Alignment 下降但仍高于随机

| Variant | NMI | ARI | Random NMI | Random ARI |
|---|---:|---:|---:|---:|
| no-LB | 0.683 | 0.693 | 0.0004 | 0.0000 |
| LB | 0.404 | 0.334 | 0.0004 | 0.0000 |

相比原始 unique-B 版本，shared-B 后 routing alignment 变弱，尤其 LB 更弱。但 alignment 仍显著高于 random routing。

### 3. Router input 仍然可分，但 boundary alignment 仍弱

| Variant | Mean Fisher ratio | Dominant boundary abs alignment |
|---|---:|---:|
| no-LB | 95.693 | 0.157 |
| LB | 96.671 | 0.104 |

shared-B 后，feature centroids 仍明显可分；但 router boundary 仍没有强烈沿 feature-difference direction 切分。

### 4. B-token-only 不是主要解释

专家选择预测准确率：

| Predictor | no-LB | LB |
|---|---:|---:|
| majority baseline | 0.430 | 0.404 |
| B-token-only | 0.478 | 0.449 |
| feature-only | 0.711 | 0.529 |
| A+B-token | 0.711 | 0.522 |
| PCA-only | 0.958 | 0.911 |
| router-projection | 0.974 | 0.944 |
| full-hidden | 0.963 | 0.947 |
| combined | 0.980 | 0.955 |
| feature-linear-probe | 1.000 | 1.000 |

`B-token-only` 只略高于 majority baseline，远低于 feature/A+B/full-hidden/router-projection。说明 shared-B control 成功削弱了“router 只看 B token”的解释。

### 5. 最强解释来自 hidden / PCA / router projection

Permutation importance 中，打乱 PCA 和 router-projection 对 combined predictor 伤害最大：

| Variant | Feature drop | B-token drop | PCA drop | Router-projection drop | Difficulty drop |
|---|---:|---:|---:|---:|---:|
| no-LB | 0.019 | 0.004 | 0.204 | 0.314 | 0.125 |
| LB | 0.039 | 0.040 | 0.396 | 0.278 | 0.080 |

这说明 learned expert choice 不是主要由单一 feature label 或 B token 解释，而是更接近 hidden geometry 与 router 权重敏感方向共同决定。

### 6. Expert path 仍然重要，但 clean oracle routing 不是更优解

| Variant | learned | feature oracle | random expert expectation | mean expert output | zero expert output |
|---|---:|---:|---:|---:|---:|
| no-LB | 0.938 | 0.781 | 0.715 | 0.857 | 0.379 |
| LB | 0.944 | 0.787 | 0.762 | 0.902 | 0.418 |

`zero expert output` 明显降低 readback，说明 expert path 有用；但人为规定 one-feature-one-expert 的 `feature oracle` 反而低于 learned routing，说明 clean feature partition 不是当前 NTP loss 下的自然最优解。

## Interpretation

E2.3 支持一个更精确的结论：

```text
shared-B 后，router 不是简单依赖 B-token shortcut；
feature identity 在 hidden space 中可被完美线性读出；
但 learned router 的 expert choice 更强地由 full hidden、PCA coordinates、router projection 等方向解释，
而不是由人工 feature label 本身解释。
```

所以当前最稳妥 claim 是：

```text
representation separability does not automatically become clean router specialization.
```

中文表述：

```text
模型内部能区分这些上下文规则，不等于 router 会按这些规则干净分 expert。
```

## Limitation

- `target_token` 仍与 feature 一一对应，所以本轮只排除了 `B_token` shortcut，没有排除 target-token shortcut。
- `PCA-only` 解释力强，说明 router choice 与高方差 hidden geometry 有关；这与 E2.1 的“boundary alignment 弱”不矛盾，因为 PCA 可预测 expert 不等于 router boundary 等于 feature centroid difference。
- `feature oracle` 使用人为固定映射，不代表最优 oracle；它只检验“强行 one-feature-one-expert 是否比 learned routing 更好”。
- 结果仍只适用于 controlled toy trigram NTP，不能外推到真实 LLM expert 语义分工。

## Key Figures

![Training loss](figures/moe_ntp_loss_comparison.png)

![Routing matrix](figures/routing_matrix_heatmap_no_lb_vs_lb.png)

![Feature readback](figures/feature_readback_no_lb_vs_lb.png)

![Router input PCA](figures/router_input_pca_by_feature_and_expert.png)

![Router boundary alignment](figures/router_boundary_alignment_heatmap.png)

![Predictor accuracy](figures/predictor_accuracy_by_variable_group.png)

![Feature vs token explanation](figures/feature_vs_token_explanation.png)

![Conditional importance](figures/conditional_importance_bar.png)

![Projection intervention](figures/feature_subspace_vs_router_subspace_projection.png)

![Routing counterfactual](figures/learned_vs_oracle_vs_random_routing_readback.png)

## Claim Update

Supported:

- shared-B control 仍能训练出 high feature readback；
- B-token-only 不能解释 expert choice；
- feature identity 可从 router input hidden state 中线性读出；
- expert choice 更强地由 full hidden、PCA coordinates 与 router projection 解释；
- learned routing 优于人为 one-feature-one-expert oracle；
- expert path 对 readback 有贡献，但 clean feature partition 不是必要解。

Weakened:

- “E2 的 routing alignment 只是 B-token shortcut”被削弱；
- “feature representation 可分会自然导致 clean one-feature-one-expert”继续被削弱；
- “人工 feature label 本身就是 router 的主要划分依据”被削弱。

Still unclear:

- target-token shortcut 是否仍参与 routing；
- router 使用的 PCA / router-projection 方向具体对应什么计算；
- shared-target control 下是否会出现不同结论；
- 真实语言 repeated context features 是否有类似结构。

## Decision

E2.3 完成后，下一步不应继续扩大 feature 数量。更有判别力的下一步是 E2.4 shared-target / crossed-target control：

```text
[1,2] -> 22
[3,4] -> 22
```

用来判断 router 是否按 target token、context relation、还是 hidden geometry 划分。

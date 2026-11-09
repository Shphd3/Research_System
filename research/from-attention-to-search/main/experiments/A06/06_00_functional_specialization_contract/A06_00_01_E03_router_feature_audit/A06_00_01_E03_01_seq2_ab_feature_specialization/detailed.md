# Detailed Report: H0521 AB Feature Specialization

## TL;DR

本轮回答的问题是：如果 A-only、B-only、AB-composite 被分到同一个 expert，它们共享的是 feature，还是更粗的 router cell。结果是：MoE 能完成任务，但 router 没有把 A/B/AB 分成干净 expert bucket；AB-dominant expert 3 同时接收大量 A-only、B-only 和 background。最重要的 ablation delta 又很小，所以结论要克制：这轮支持 mixed router assignment，不足以证明强 shared functional expert。

## Setup

数据构造：

```text
A-only:       [A, r] -> y_A
B-only:       [r, B] -> y_B
AB-composite: [A, B] -> y_AB
background:  [r_i, r_j] -> r_k
```

其中 \(r, r_i, r_j, r_k\) 均来自非特殊 background token。background 沿用之前 synthetic 实验原则：非 planted feature prefix，target 是普通随机背景 token。

模型：

- dense tiny Transformer baseline；
- no-load-balance top-1 MoE tiny Transformer；
- 4 seeds: `20260521, 20260522, 20260523, 20260524`。

ACP run:

```text
job id: pt-527v9od5
job name: ats-h0521-ab-feature-specialization-4gpu-guaranteed
state: SUCCEEDED
runtime log: active/attention_search_hier_kv/logs/acp/h0521_ab_feature_specialization_4gpu_guaranteed_20260521_20260521_104425.log
result dir: active/synthetic_data_understanding/results/h0521_ab_feature_specialization/h0521_ab_feature_specialization_4gpu_guaranteed_20260521/
figure dir: active/synthetic_data_understanding/figures/h0521_ab_feature_specialization/h0521_ab_feature_specialization_4gpu_guaranteed_20260521/
```

## How To Read The Metrics

`class-specific expert ablation delta CE` 是主指标。它问的是：mask 掉 expert `e` 后，某个 class 的 prediction loss 是否显著变差。如果某 expert 只服务 AB-composite，那么 mask 它应该主要伤害 AB，而不应该同样伤害 A/B/background。

`routing matrix` 只是 assignment 证据。它说明样本被分到哪里，但不能单独证明 expert 对预测有功能作用。

`hidden probe accuracy` 检查 representation 是否保留 class 信息。如果 probe 很高但 routing 混合，说明 class 信息还在 hidden state 中，只是 router boundary 没有按这些 class 干净切分。

## Main Results

### Task Learnability

| Model | A-only acc | B-only acc | AB acc | Background acc |
|---|---:|---:|---:|---:|
| dense | 1.000 | 1.000 | 1.000 | 0.010 |
| MoE | 1.000 | 1.000 | 1.000 | 0.008 |

background 是随机 next token，所以低 accuracy 是预期的，不代表任务失败。A/B/AB 都被学会，说明诊断有效。

### Routing Assignment

| Class | E0 | E1 | E2 | E3 |
|---|---:|---:|---:|---:|
| AB-composite | 0.000 | 0.000 | 0.250 | 0.750 |
| A-only | 0.312 | 0.087 | 0.203 | 0.397 |
| B-only | 0.254 | 0.246 | 0.000 | 0.500 |
| background | 0.249 | 0.231 | 0.206 | 0.314 |

解释：E3 是 AB-dominant，但同时接收大量 B-only、A-only 和 background；这不是干净 AB expert。

![Routing matrix](figures/routing_matrix.png)

### Primary Ablation Metric

| Expert | AB delta CE | A delta CE | B delta CE | background delta CE |
|---|---:|---:|---:|---:|
| E0 | 0.000 | 0.078 | 0.005 | -0.193 |
| E1 | 0.000 | 0.015 | 0.004 | -0.174 |
| E2 | 0.000 | 0.022 | 0.000 | -0.132 |
| E3 | 0.001 | 0.014 | 0.016 | -0.189 |

解释：没有 expert 对 AB-composite 表现出强 ablation necessity。即使 E3 接收 75% AB，mask E3 后 AB delta CE 也只有 `0.001`。因此，routing assignment 混合成立，但强功能混合还没有被证明。

![Expert ablation delta](figures/ablation_delta.png)

### Same-Expert Commonality

E3 内部平均 composition：

| Expert | signal fraction | A count | B count | AB count | background count |
|---|---:|---:|---:|---:|---:|
| E3 | 0.690 | 635.5 | 800.0 | 1200.0 | 503.0 |

解释：E3 的共同性不是 `AB feature`，更像“包含预测相关 signal、且在 router projection 上落入同一 cell”的 mixed/predictive-signal bucket。

![Within-expert composition](figures/within_expert_composition.png)

### Representation Check

| Model | hidden probe class accuracy |
|---|---:|
| dense | 0.9998 |
| MoE | 0.9995 |

解释：hidden state 中仍然保留 A/B/AB/background class 信息。因此 routing 混合不是因为 representation 完全不可分，而是 router projection / top-1 boundary 没有按这些 class 干净切开。

## From Result To Judgment

Observed:

```text
MoE learns A/B/AB -> routing matrix mixes A/B/AB/background -> hidden probe can decode class -> expert ablation is weak.
```

Interpretation:

```text
ordinary top-1 router 更像在 mixed hidden geometry 上划 cell，而不是先解出 atomic/composite feature 再路由。
```

Boundary:

```text
不能说 expert function 已经强混合，因为 ablation delta 没有显示强 causal necessity。
```

Decision:

```text
expert bucket 不能直接当干净 feature index；下一步应先增强 expert-path necessity test。
```

## Not Proven

- 不能证明真实语言 MoE 一定如此；
- 不能证明 top-k / load balance / soft routing 无效；
- 不能证明 expert function 强混合；
- 不能证明 Reverse Index 完全不可行；
- 不能用 routing heatmap 单独推出 KV retrieval 质量。

## Next Step

下一步实验应该只回答一个更窄问题：

```text
当 expert path 被设计成更必要时，mixed router assignment 是否会变成 mixed functional dependency？
```

可执行方向：

- 减弱 residual bypass，让 expert path 对 prediction 更必要；
- 做 stricter counterfactual routing，而不是只把 selected expert output 置零；
- 保留同一 A/B/AB/background 数据构造，避免引入新变量。


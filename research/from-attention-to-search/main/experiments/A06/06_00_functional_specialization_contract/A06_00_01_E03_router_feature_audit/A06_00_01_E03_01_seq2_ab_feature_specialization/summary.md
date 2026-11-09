# Result Summary: H0521 AB Feature Specialization

Hypothesis purpose card:

The legacy purpose card was removed; this summary is the surviving result
source.

## Observation

最重要指标是 `class-specific expert ablation delta CE`：mask 某个 expert 后，分别看 A-only、B-only、AB-composite、background 的交叉熵增加多少。它决定我们能否说某个 expert 在功能上主要服务某个 feature class。

本轮 4 seeds 结果显示：dense baseline 和 no-load-balance top-1 MoE 都能学会 A/B/AB 规则；但 MoE expert bucket 没有形成干净的 A/B/AB feature-level specialization。

| Metric | Result |
|---|---:|
| dense A/B/AB accuracy | `1.0 / 1.0 / 1.0` |
| MoE A/B/AB accuracy | `1.0 / 1.0 / 1.0` |
| MoE class-expert NMI | `0.459` |
| dense hidden probe class accuracy | `0.9998` |
| MoE hidden probe class accuracy | `0.9995` |

关键 routing 现象：expert 3 是 AB-dominant cell，但不是 AB-only cell。

| Class | E0 | E1 | E2 | E3 |
|---|---:|---:|---:|---:|
| AB-composite | 0.000 | 0.000 | 0.250 | 0.750 |
| A-only | 0.312 | 0.087 | 0.203 | 0.397 |
| B-only | 0.254 | 0.246 | 0.000 | 0.500 |
| background | 0.249 | 0.231 | 0.206 | 0.314 |

在 expert 3 内部，平均每个 seed 接收 `AB=1200`, `B=800`, `A=635.5`, `background=503` 个 eval 样本。它更像一个偏向 predictive-signal 的 mixed router cell，而不是 AB-specific expert。

注意：下面表格和原始 routing matrix 图是跨 seed 平均后的展示。由于 expert id 有 permutation symmetry，assignment 结论应优先看 per-seed 横排图，再看哪些现象跨 seed 稳定。

## Interpretation

这轮支持的是 assignment-level bundle routing：router 把 A/B/AB/background 共同投进一些混合 expert cell，尤其 E3 同时承载 AB、B、A 和部分 background。

但 primary ablation metric 不支持“强功能依赖的 shared expert”这个更强说法。最大的平均 ablation delta 只有 A-only 对 E0 的 `+0.078 CE`；AB-composite 对任何 expert 的 delta 都接近 0。也就是说，当前模型虽然 routing 混合，但预测功能不强依赖单个 expert path，可能由 residual / attention / lm head 共同完成。

## Limitation

这轮证明的是 controlled synthetic setup 下的普通 top-1 MoE routing 行为，不等价于真实语言 MoE。并且当前 tiny Transformer 有 residual path，expert ablation 可能低估 expert 功能必要性。

## Key Figures

主 routing 图：

![Routing matrix by seed](figures/routing_matrix_by_seed_row.png)

平均 routing 图只做辅助展示：

![Routing matrix average](figures/routing_matrix.png)

![Expert ablation delta](figures/ablation_delta.png)

![Within-expert composition](figures/within_expert_composition.png)

## Claim Update

Supported:

```text
ordinary no-load-balance top-1 MoE 在这个 A/B/AB setup 中没有形成干净 feature-level expert bucket；
同一个 expert 的共同性更像 router projection 上的 mixed/predictive-signal cell。
```

Weakened:

```text
“expert bucket 可以直接作为干净 feature index”的假设进一步变弱。
```

Still unclear:

```text
expert function 是否真的混合，当前 ablation 不够强；需要更强的 expert-path necessity test。
```

## Next Decision

下一步不要直接进入 Reverse Index 对齐。先做一个更窄的 H0521 follow-up：增强 expert-path necessity，例如去掉/减弱 residual expert bypass，或把 ablation 从 zero selected expert 改成更严格的 counterfactual routing，以判断 mixed router cell 是否也对应 mixed functional expert。

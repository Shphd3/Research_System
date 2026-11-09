# Result Summary: H0522 SVD Feature Mixing Seq32

Hypothesis purpose card:

The legacy purpose card was removed; this summary is the surviving result
source.

## Observation

最重要指标是 `ProjectionScore` 加 `expert mask delta CE`：前者看 AB-dominant expert 的主子空间是否只承载 AB interaction，后者看 mask 该 expert 后是否主要伤害 AB-composite。

4 个 seed 的模型都学会了 A/B/AB 任务：A-only accuracy `1.0000`，B-only mean accuracy `0.9999`，AB-composite mean accuracy `0.9999`。background class 的 target 是随机 background token，因此 accuracy 接近 chance，不作为任务学会与否的指标，只作为 hidden reference class。

AB-composite 在 prediction position 有高度 dominant expert：

| seed | AB-dominant expert | P(expert \| AB) |
|---:|---:|---:|
| 20260521 | E0 | 0.981 |
| 20260522 | E2 | 0.971 |
| 20260523 | E2 | 1.000 |
| 20260524 | E1 | 0.996 |

但该 expert 不是 AB-specific。rank 4 下，AB-dominant expert 同时强投影到 A、B 和 AB interaction：

| Metric | mean | min | max |
|---|---:|---:|---:|
| `ProjScore(v_A)` | 0.986 | 0.983 | 0.989 |
| `ProjScore(v_B)` | 0.991 | 0.987 | 0.994 |
| `ProjScore(v_AB_int)` | 0.803 | 0.679 | 0.899 |

更关键的是，random matched 和 global baseline 的投影也同样高，说明这些方向是 prediction-position hidden space 的全局低维结构，不是 AB expert 独有的专门化。

Mask AB-dominant expert 的功能损伤不稳定：

| seed | \(\Delta CE\) A-only | \(\Delta CE\) B-only | \(\Delta CE\) AB-composite |
|---:|---:|---:|---:|
| 20260521 | 0.333 | 0.048 | 0.001 |
| 20260522 | 0.033 | 0.000 | 0.003 |
| 20260523 | 0.280 | 0.028 | 0.003 |
| 20260524 | 0.038 | 0.336 | 0.754 |

Only seed `20260524` shows strong AB-composite damage. The cross-seed intersection does not support a stable AB-only functional expert.

## Interpretation

这轮支持 H：ordinary top-1 MoE 的 AB-dominant expert 更像 mixed bucket，而不是 clean composite-feature specialist。

原因是两层证据一致：

1. representation 上，AB-dominant expert 的子空间包含 A/B/AB interaction 多方向，而且不优于 random/global baseline；
2. function 上，mask AB-dominant expert 的损伤不稳定，不是跨 seed 稳定主要伤害 AB-composite。

## Limitation

这轮只分析 prediction-position routing，不直接回答 source-token bucket 能不能做 KV retrieval index。它补强的是“普通 expert bucket 不干净”的判断，不是 Reverse Index 的最终实验。

`v_AB_int` 的 norm 约为 `2.10-2.56`，明显小于 `v_A/v_B` 的 `10-11`。因此不能说“模型没有 AB interaction”，只能说在当前 router-input hidden space 中，AB interaction 不是 dominant, expert-specific 的独立方向。

## Key Figures

Prediction-position routing shows AB-composite is routed to a dominant expert in every seed, but the expert id is seed-local and cannot be semantically matched across seeds.

![Prediction routing by seed](figures/routing_prediction_by_seed.png)

The key projection figure shows AB-dominant expert does not beat random matched or global baselines.

![AB expert projection vs baselines](figures/ab_expert_projection_vs_baselines_rank4_by_seed.png)

The mask figure shows functional damage is not cross-seed stable AB-only damage.

![AB expert ablation by seed](figures/ab_expert_ablation_delta_loss_by_seed.png)

## Claim Update

Supported:

```text
在 seq_len=32 synthetic setup 中，ordinary top-1 MoE 的 prediction-position AB-dominant expert 不是稳定、干净的 AB composite specialist。
```

Weakened:

```text
把 ordinary top-1 expert bucket 直接当作 feature-level index candidate 的路线继续变弱。
```

Still unclear:

```text
经过 anti-shortcut 数据构造、router 约束或训练目标改变后，是否能形成更干净的 rule/function expert。
```

## What Cannot Be Claimed

- 不能声称 MoE routing 一般无用；
- 不能声称真实语言模型没有 expert specialization；
- 不能从 prediction-position SVD 直接推出 source-token KV retrieval 失败；
- 不能把单个 seed 的 AB ablation strong effect 当作跨 seed 结论。

## Next Decision

下一步应进入 anti-shortcut router factor audit：显式平衡 token identity、source position、target token 和 rule/function，再判断 router score / expert id 到底由哪个 factor 主导。

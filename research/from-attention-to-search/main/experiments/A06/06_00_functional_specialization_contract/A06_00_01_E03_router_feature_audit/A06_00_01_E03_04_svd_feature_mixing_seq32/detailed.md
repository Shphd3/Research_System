# Detailed Report: H0522 SVD Feature Mixing Seq32

## TL;DR

这轮在已训练 H0521b `seq_len=32` MoE 上做 post-training diagnostic。结论是：AB-composite 在 prediction position 确实有 dominant expert，但这个 expert 不是稳定的 AB interaction specialist。它的主子空间同时包含 A、B、AB interaction，并且这种高投影不优于 random matched / global baseline；mask 该 expert 的 class-wise loss damage 也不跨 seed 稳定指向 AB-composite。

## 这轮在回答什么

问题不是“模型能不能做对 synthetic task”。模型已经能做对。

这轮问的是：

```text
AB-composite 被 routed 到某个 expert 时，这个 expert 是 AB feature specialist，
还是只是收纳 mixed hidden geometry 的 bucket？
```

## 指标怎么读

最重要指标：

```text
ProjectionScore(v_A, S_e), ProjectionScore(v_B, S_e), ProjectionScore(v_AB_int, S_e)
```

它回答：某个 expert 接收的 hidden states 的 top SVD subspace 是否包含某个 feature direction。

真正决定判断的是 baseline 对比：

```text
AB expert projection vs random matched bucket vs global hidden subspace
```

如果 AB expert 高，但 random/global 也高，说明方向是全局 hidden geometry，不是 expert-specific specialization。

功能指标：

```text
Delta CE = CE(mask expert e) - CE(base)
```

它回答：mask 某 expert 后哪个 class 的 loss 上升。如果 AB expert 真是 functional AB specialist，应主要伤害 AB-composite。

## 实验设置

Run command:

```bash
CUDA_VISIBLE_DEVICES=0,1 python Projects/from-attention-to-search/main/experiments/H0521_router_feature_specialization/H0522_svd_feature_mixing_seq32/scripts/analyze_h0522_svd_feature_mixing_seq32.py --n-eval-per-class 4096 --motif-position 15
```

Run summary:

```text
devices: cuda:0, cuda:1
n_eval_per_class: 4096
motif_position: 15
seeds: 20260521, 20260522, 20260523, 20260524
```

Checkpoint source:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0521b_seq32_contiguous_ab/h0521b_seq32_contiguous_ab_4gpu_20260521/
```

Analyzed checkpoint:

```text
moe_top1_no_lb/seed_*/model.pt
```

Evaluation classes:

| Class | Motif | Target role |
|---|---|---|
| background | no A/B token | random background token |
| A-only | `[A, r]` | `y_A` |
| B-only | `[r, B]` | `y_B` |
| AB-composite | `[A, B]` | `y_AB` |

Router input:

```text
ffn_input at prediction position p*=31
```

## 主要结果

### 1. Task sanity

| Class | Mean accuracy |
|---|---:|
| A-only | 1.0000 |
| B-only | 0.9999 |
| AB-composite | 0.9999 |
| background | 0.0078 |

background target 是随机 background token，所以 chance-level accuracy 是预期现象。它在本实验中的作用是定义 \(\mu_0\)，不是证明模型要预测随机背景。

### 2. Prediction routing

![Prediction routing by seed](figures/routing_prediction_by_seed.png)

AB-composite 在每个 seed 都有 dominant expert，但 expert id 只在 seed 内有意义：

| seed | AB-dominant expert | fraction |
|---:|---:|---:|
| 20260521 | E0 | 0.981 |
| 20260522 | E2 | 0.971 |
| 20260523 | E2 | 1.000 |
| 20260524 | E1 | 0.996 |

### 3. Feature direction geometry

Feature direction norms:

| seed | \(\|v_A\|\) | \(\|v_B\|\) | \(\|v_{AB}^{raw}\|\) | \(\|v_{AB}^{int}\|\) |
|---:|---:|---:|---:|---:|
| 20260521 | 11.193 | 10.184 | 11.177 | 2.562 |
| 20260522 | 11.168 | 11.043 | 11.466 | 2.294 |
| 20260523 | 10.775 | 10.831 | 11.144 | 2.101 |
| 20260524 | 10.313 | 10.967 | 10.958 | 2.404 |

`v_AB_raw` 与 `v_A + v_B` 的 cosine 是 `0.994-0.998`。所以 raw AB direction 主要是 A+B，不应被解释成 interaction。

### 4. AB expert projection vs baselines

![AB expert projection vs baselines](figures/ab_expert_projection_vs_baselines_rank4_by_seed.png)

rank 4 下，AB expert 对 A/B/AB interaction 都有高投影；但 random matched 和 global baseline 同样高，甚至略高。

这说明：

```text
高 projection score 本身不等于 expert specialization。
```

本轮更合理的解释是：prediction-position hidden states 的 class directions 本来就处在低维全局子空间里，AB expert 没有展示出独有的 AB subspace。

### 5. Expert mask functional ablation

![AB expert ablation by seed](figures/ab_expert_ablation_delta_loss_by_seed.png)

| seed | mask AB expert | \(\Delta CE\) A-only | \(\Delta CE\) B-only | \(\Delta CE\) AB-composite |
|---:|---:|---:|---:|---:|
| 20260521 | E0 | 0.333 | 0.048 | 0.001 |
| 20260522 | E2 | 0.033 | 0.000 | 0.003 |
| 20260523 | E2 | 0.280 | 0.028 | 0.003 |
| 20260524 | E1 | 0.038 | 0.336 | 0.754 |

只有 seed `20260524` 支持“mask AB expert mainly hurts AB”。其他 3 个 seed 主要不支持这个判断。

## 从结果到判断

推理链：

```text
AB-composite has dominant expert
-> but AB expert subspace contains A/B/AB directions
-> and the same directions are present in random/global baselines
-> and expert mask does not stably hurt AB-composite across seeds
-> therefore AB-dominant expert is not a stable clean AB specialist
```

## 这轮没有证明什么

这轮没有证明 ordinary MoE 永远不能形成 specialization。

它证明的是更窄的一点：

```text
在当前 H0521b seq_len=32 synthetic setup 和 no-load-balance top-1 MoE 中，
已经训练出的 AB-dominant prediction expert 不能被解释为稳定、干净、可复用的 AB feature specialist。
```

## Output Map

Tables:

```text
tables/class_metrics.csv
tables/routing_prediction_by_seed.csv
tables/routing_prediction_summary_by_seed.csv
tables/feature_direction_norms.csv
tables/svd_projection_scores.csv
tables/expert_ablation_delta_loss.csv
tables/ab_expert_deep_dive.csv
```

Figures:

```text
figures/routing_prediction_by_seed.png
figures/ab_expert_projection_by_seed.png
figures/ab_expert_projection_vs_baselines_rank4_by_seed.png
figures/ab_expert_ablation_delta_loss_by_seed.png
```

Script:

```text
scripts/analyze_h0522_svd_feature_mixing_seq32.py
```

Run summary:

```text
run_summary.json
```

## Next Step

进入 anti-shortcut router factor audit。下一轮必须显式平衡 token identity、source position、target token 和 rule/function，否则很容易把 shortcut routing 误判成 feature specialization。


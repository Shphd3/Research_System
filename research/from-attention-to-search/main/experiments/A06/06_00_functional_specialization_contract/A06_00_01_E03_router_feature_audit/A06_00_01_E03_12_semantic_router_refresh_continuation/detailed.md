# Detailed Report: H0528a Semantic Router Refresh Continuation

## 0. 摘要

这个 continuation 实验回答：

> 如果不是固定 step-0 semantic boundary，而是在 trained checkpoint 的 current hidden states 上重新构造 semantic router，并给 experts 400-step adaptation window，是否能恢复 task CE、保持 B-context semantic routing，并形成 AB-specific functional expert？

答案是：

```text
task CE 可以恢复；
step-0 B-context NMI 可以提高；
但 semantic routing 继续衰减，S_AB 没有稳定跨 source 提升。
```

所以它不推翻 H0528a，只是把结论从“semantic route 不可用”细化为：

```text
semantic route 可以作为可适应的 routing intervention；
但没有 route-function alignment objective 时，它不会稳定保持，也不会自动变成 functional specialization。
```

## 1. 实验设置

Runner:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0528a_semantic_router_refresh_continuation.py
```

Config:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0528a_semantic_router_refresh_continuation.json
```

SCO job:

```text
pt-7w0hs9uf
```

Raw result dir:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0528a_semantic_router_refresh_continuation/h0528a_refresh_continuation_4gpu_20260525
```

Runtime log:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/h0528a_refresh_continuation_4gpu_20260525_runtime_20260525_005442.log
```

Source checkpoints:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0528a_route_swap_and_frozen_semantic_router/h0528a_route_swap_frozen_semantic_4gpu_20260524
```

Conditions:

```text
source_conditions: learned_random, semantic_init_learned
continuation_conditions: baseline_continue, refresh_freeze_continue, refresh_trainable_continue
seeds: 20260521, 20260522, 20260523, 20260524
steps: 400
eval_steps: 0, 50, 100, 200, 400
```

## 2. Refresh Construction

每个 source checkpoint 都先收集当前 model 的 `ffn_input` hidden states。这里的 `ffn_input` 是 MoE router 在当前 checkpoint forward 时实际看到的 hidden representation。

然后按 B-context role 构造 semantic router：

```text
B_in_B_only
B_in_AB
B_in_CB
```

构造方式：

```text
centroid per B-context role
global mean
covariance + 0.001 * I
direction = inv(cov) @ (centroid - global_mean)
normalize direction
router row = 8.0 * direction
bias = - row dot global_mean
unused expert bias = -8.0
```

这一步不是聚类，也不是恢复旧初始化 router；它是在 trained checkpoint 的 current hidden geometry 上重建 router weight/bias。

## 3. Audit

### 3.1 Source artifact

`source_checkpoint_audit.csv` 显示 8/8 source checkpoints 存在。

### 3.2 Refresh 是否提高 B-context NMI

| Source condition | Baseline B-context NMI | Refreshed B-context NMI | Gain |
|---|---:|---:|---:|
| `learned_random` | `0.0414` | `0.2015` | `+0.1601` |
| `semantic_init_learned` | `0.0446` | `0.2923` | `+0.2477` |

解释：refresh construction 通过；如果这一步没提高 NMI，本实验就没有资格进入 full run。

### 3.3 Gradient / sparse dispatch audit

| Condition | Router weight grad | Router weight delta | Passed |
|---|---:|---:|---:|
| `baseline_continue` | `0.028841` | `0.018101` | `1.0` |
| `refresh_freeze_continue` | `0.000000` | `0.000000` | `1.0` |
| `refresh_trainable_continue` | `0.774117` | `0.018093` | `1.0` |

所有条件：

```text
active_experts_per_token_min = 1
active_experts_per_token_max = 1
full_soft_mixture = False
selected_gate_renormalized = False
dispatch_mode = top1_selected_gate_sparse
```

## 4. Task CE Recovery

主指标：

```text
G_refresh = CE(refresh after 400 steps) - CE(baseline_continue after 400 steps)
```

| Source | Refresh condition | Baseline final CE | Refresh final CE | `G_refresh` |
|---|---|---:|---:|---:|
| `learned_random` | `refresh_freeze_continue` | `0.0009` | `0.0005` | `-0.0004` |
| `learned_random` | `refresh_trainable_continue` | `0.0009` | `0.0008` | `-0.0001` |
| `semantic_init_learned` | `refresh_freeze_continue` | `0.0014` | `0.0004` | `-0.0010` |
| `semantic_init_learned` | `refresh_trainable_continue` | `0.0014` | `0.0006` | `-0.0008` |

![Task CE trajectory](figures/refresh_task_ce_trajectory.png)

这张图说明：refresh 后继续训练可以恢复 task CE；route intervention 不是简单地让任务失败。

## 5. B-context Routing Retention

| Source | Refresh condition | Step-0 NMI | Final NMI | Decay |
|---|---|---:|---:|---:|
| `learned_random` | `refresh_freeze_continue` | `0.2172` | `0.0705` | `0.1467` |
| `learned_random` | `refresh_trainable_continue` | `0.2172` | `0.0546` | `0.1626` |
| `semantic_init_learned` | `refresh_freeze_continue` | `0.2983` | `0.1232` | `0.1750` |
| `semantic_init_learned` | `refresh_trainable_continue` | `0.2983` | `0.1018` | `0.1964` |

![B-context NMI trajectory](figures/refresh_b_context_nmi_trajectory.png)

这张图说明：current-geometry refresh 能建立 early semantic routing，但 continuation 过程中 B-context NMI 显著衰减。

![Final B-context routing heatmap](figures/refresh_final_b_context_routing_heatmap.png)

这张图说明：final B-only / AB / CB routing 仍没有稳定保持 refresh 时的 semantic partition。

## 6. Functional Specialization

AB-specific margin:

```text
S_AB = max_e [Delta L_AB,e - max(Delta L_A,e, Delta L_B,e, Delta L_CB,e)]
```

| Source | Condition | Mean `S_AB` | Strong seeds |
|---|---|---:|---:|
| `learned_random` | `baseline_continue` | `0.0745` | `2/4` |
| `learned_random` | `refresh_freeze_continue` | `0.0868` | `1/4` |
| `learned_random` | `refresh_trainable_continue` | `0.0954` | `2/4` |
| `semantic_init_learned` | `baseline_continue` | `0.0113` | `0/4` |
| `semantic_init_learned` | `refresh_freeze_continue` | `0.0049` | `0/4` |
| `semantic_init_learned` | `refresh_trainable_continue` | `0.0011` | `0/4` |

![S_AB trajectory](figures/refresh_S_AB_trajectory.png)

这张图说明：`learned_random` source 的 refresh 有小幅局部提升，但没有跨 source 稳定出现；`semantic_init_learned` source 基本没有 AB-specific margin。

![Final class expert ablation heatmap](figures/refresh_final_class_expert_ablation_heatmap.png)

这张图说明：final class x expert ablation 没有显示一致的 AB-specific causal expert。

## 7. 对 H0528a 的更新

这个实验直接处理了旧限制：

```text
旧 frozen semantic router 固定 step-0 boundary；
本实验在 trained checkpoint current hidden states 上 refresh router，并给 adaptation window。
```

结果说明：

1. semantic refresh 确实提高 step-0 B-context NMI；
2. task CE 可以恢复；
3. B-context semantic routing 仍衰减；
4. `S_AB` 不稳定，尤其 `semantic_init_learned` source 下完全没有稳定提升；
5. trainable continuation 没有保持 semantic basin，符合 NTP 会继续拉走 semantic route 的解释。

所以 H0528a 的结论不改变：

```text
semantic separability 不是 functional specialization 的充分条件。
```

但 claim 边界更精确：

```text
不能说 semantic refresh 完全不可用；
只能说在没有 route-function alignment objective 的情况下，
semantic refresh + 400-step adaptation 不足以稳定产生 functional specialization。
```

## 8. Artifact Map

Curated tables:

```text
main/experiments/H0521_router_feature_specialization/H0528a_semantic_router_refresh_continuation/tables/
```

Curated figures:

```text
main/experiments/H0521_router_feature_specialization/H0528a_semantic_router_refresh_continuation/figures/
```

Raw result dir:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0528a_semantic_router_refresh_continuation/h0528a_refresh_continuation_4gpu_20260525
```

Raw figure dir:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/h0528a_semantic_router_refresh_continuation/h0528a_refresh_continuation_4gpu_20260525
```

Repro command:

```bash
H0528A_REFRESH_ALLOW_REAL_SUBMIT=1 \
RUN_NAME=h0528a_refresh_continuation_4gpu_20260525 \
JOB_NAME=ats-h0528a-refresh-continuation-4gpu \
bash scripts/submit_h0528a_semantic_router_refresh_continuation_4gpu_acp.sh
```

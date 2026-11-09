# Detailed Report: H0528a Route Swap and Frozen Semantic Router

## 0. 摘要

这轮实验回答的是：

> 如果 final hidden state 里有可恢复的 semantic route，为什么 learned top-1 sparse router 没有选择它？

结果显示，问题比“router 没选中正确 semantic boundary”更深。`semantic_current` route 能更好分开 B-context hidden states，但替换 learned router 后 task CE 明显变差；从训练开始固定 semantic router 也能学会任务，但没有产生稳定 AB-specific functional expert。

因此当前最安全结论是：

```text
hidden geometry separability 不等于 functional route。
NTP objective 下 routing、semantic partition、expert causal utility 可以脱钩。
```

## 1. 实验设置

Runner:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0528a_route_swap_and_frozen_semantic_router.py
```

Config:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0528a_route_swap_and_frozen_semantic_router.json
```

SCO job:

```text
pt-cikqoqlb
```

Runtime log:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/h0528a_route_swap_frozen_semantic_4gpu_20260524_runtime_20260524_182110.log
```

## 2. Stage A: Route-Swap Diagnostic

Stage A 不重新训练。它加载 H0527a final checkpoints，然后临时替换 router：

```text
trained_final: checkpoint learned router
semantic_current: final hidden states 上的 B-context prototype router
source_identity_current: final hidden states 上的 A/B/C source-identity prototype router
```

每次替换后，用原 experts 和 output head 重新评估 task CE、expert ablation、`S_AB` 和 routing NMI。

### 2.1 核心指标

| Metric | Mean | 解释 |
|---|---:|---|
| `G_sem_signal_ce` | `+1.8624` | semantic route 比 trained route 的 signal CE 高很多 |
| `Q_sem_S_AB` | `-0.1068` | semantic route 没有提高 AB-specific functional specialization |
| `A_learn_sem` | `0.0358` | learned route 几乎不对齐 semantic route |
| trained B-context NMI | `0.0453` | learned route 基本不按 B-context 分 |
| semantic B-context NMI | `0.2605` | semantic route 确实更能分开 B-context |

这组结果说明：

```text
semantic route 是 geometry 上可恢复的；
但它不是当前 trained experts 的可用 functional route。
```

![Route swap semantic gap and gain](figures/route_swap_semantic_gap_and_gain.png)

这张图说明：semantic route swap 通常显著伤 CE，且没有稳定提高 `S_AB`。

![Route swap B-context heatmap](figures/route_swap_b_context_heatmap.png)

这张图说明：semantic route 更能按 B-context 分发 token，但 routing 结构本身没有保证功能可用。

## 3. Stage B: Frozen Semantic Router Training

Stage B 按用户要求不等待 Stage A 审核，直接训练：

```text
learned_random
semantic_init_learned
frozen_semantic_router
```

`frozen_semantic_router` 不是旧 hard argmax；它仍使用：

```text
y(h) = p_s(h) E_s(h)
```

但 router weight/bias 固定不训练：

```text
router.weight.requires_grad = False
router.bias.requires_grad = False
```

hidden representation、experts 和 output head 继续训练。

## 4. Stage B 结果

### 4.1 任务学习

| Condition | Signal CE mean | Signal acc mean |
|---|---:|---:|
| `learned_random` | `0.0023` | `0.9996` |
| `semantic_init_learned` | `0.0008` | `0.9999` |
| `frozen_semantic_router` | `0.0014` | `0.9998` |

解释：三个条件都学会了 signal classes，所以 specialization 失败不能归因于 task 没学会。

### 4.2 AB-specific functional specialization

| Condition | `S_AB` by seed | Mean | Strong seeds |
|---|---|---:|---:|
| `learned_random` | `[-0.0002, 0.0000, 0.7449, 0.0003]` | `0.1863` | `1/4` |
| `semantic_init_learned` | `[0.0000, 0.0000, 0.0000, 0.2876]` | `0.0719` | `1/4` |
| `frozen_semantic_router` | `[0.0000, 0.0000, 0.0000, 0.0000]` | `0.0000` | `0/4` |

解释：固定 semantic router 没有诱导出 AB-specific single-expert functional specialization。

![Frozen training S_AB trajectory](figures/frozen_training_S_AB_trajectory.png)

这张图说明：frozen semantic condition 没有形成稳定正 `S_AB`。

![Frozen training class expert ablation heatmap](figures/frozen_training_class_expert_ablation_heatmap.png)

这张图说明：final class x expert ablation 没有显示 frozen semantic router 产生清楚 AB-specific causal expert。

### 4.3 B-context routing

Final B-context routing NMI：

| Condition | Step-0 mean | Final mean |
|---|---:|---:|
| `learned_random` | `0.0019` | `0.0437` |
| `semantic_init_learned` | `0.2469` | `0.0468` |
| `frozen_semantic_router` | `0.2469` | `0.0909` |

解释：frozen semantic router 保留了一点 B-context routing，但多数 seed 中 step-0 semantic structure 仍然衰减。原因是 router 固定不等于 route assignment 固定；hidden states 仍会训练并漂移。

![Frozen training B-context routing heatmap](figures/frozen_training_b_context_routing_heatmap.png)

这张图说明：固定 semantic router 也没有稳定保持清楚的 B-only / AB / CB route separation。

## 5. 从结果到判断

Stage A：

```text
semantic_current NMI 高于 trained_final
-> final hidden state 中存在可恢复 semantic direction
```

但：

```text
semantic_current CE 明显高于 trained_final
semantic_current S_AB 不高于 trained_final
-> 这条 semantic direction 没有和 trained experts 的功能计算对齐
```

Stage B：

```text
frozen_semantic_router task acc 接近 1
-> 固定 router 不阻止任务学习
```

但：

```text
frozen_semantic_router S_AB = 0/4 seeds
-> 固定 semantic boundary 本身不足以产生 AB-specific functional expert
```

所以本实验把 failure mode 从“semantic route 可行但没被 learned router 选择”修正为：

```text
NTP objective 下，semantic route、routing assignment 和 expert functional contribution 没有 identifiability pressure。
```

## 6. 不能证明什么

本实验不能证明：

```text
真实语言 MoE 一定同样失败。
online / EMA prototype router 一定无效。
load-balance、top-2、z-loss 后仍然失败。
distributed multi-expert function 不存在。
```

尤其注意：

```text
frozen semantic router 固定的是初始 boundary，不是在线追踪 final hidden geometry 的 router。
```

因此它不能否定所有 cluster/prototype router，只是否定“固定 step-0 semantic boundary 足以解决 specialization”的强说法。

## 7. Artifact Map

Result dir:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0528a_route_swap_and_frozen_semantic_router/h0528a_route_swap_frozen_semantic_4gpu_20260524
```

Figure dir:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/h0528a_route_swap_and_frozen_semantic_router/h0528a_route_swap_frozen_semantic_4gpu_20260524
```

Curated tables:

```text
main/experiments/H0521_router_feature_specialization/H0528a_route_swap_and_frozen_semantic_router/tables/
```

Curated figures:

```text
main/experiments/H0521_router_feature_specialization/H0528a_route_swap_and_frozen_semantic_router/figures/
```

Repro command:

```bash
H0528A_ALLOW_REAL_SUBMIT=1 \
RUN_NAME=h0528a_route_swap_frozen_semantic_4gpu_20260524 \
JOB_NAME=ats-h0528a-route-swap-frozen-4gpu \
bash scripts/submit_h0528a_route_swap_and_frozen_semantic_router_4gpu_acp.sh
```

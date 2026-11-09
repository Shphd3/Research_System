# Summary: H0528a Semantic Router Refresh Continuation

## 0. 结论

semantic refresh 补上了旧实验的限制：它确实能在 current hidden geometry 上提高 step-0 B-context routing NMI，而且 400-step continuation 后 task CE 基本恢复。

但它没有改变 H0528a 的核心结论：

```text
semantic separability 不是 functional specialization 的充分条件。
即使在 current hidden state 上 refresh semantic router，并给 experts adaptation window，
B-context semantic routing 仍会明显衰减，AB-specific functional expert 也没有稳定出现。
```

最强的假设更新是：

```text
问题不是单纯 step-0 boundary 过期；
而是 NTP continuation 下 route assignment、semantic boundary、expert utility 仍缺少绑定机制。
```

## 1. 关键结果

### 1.1 Refresh audit

| Source condition | Baseline B-context NMI | Refreshed B-context NMI | Gain |
|---|---:|---:|---:|
| `learned_random` | `0.0414` | `0.2015` | `+0.1601` |
| `semantic_init_learned` | `0.0446` | `0.2923` | `+0.2477` |

解释：refresh construction 有效，确实在 current hidden geometry 上恢复了更 semantic 的 B-context router。

### 1.2 Task CE recovery

| Source | Refresh condition | `G_refresh` |
|---|---|---:|
| `learned_random` | `refresh_freeze_continue` | `-0.0004` |
| `learned_random` | `refresh_trainable_continue` | `-0.0001` |
| `semantic_init_learned` | `refresh_freeze_continue` | `-0.0010` |
| `semantic_init_learned` | `refresh_trainable_continue` | `-0.0008` |

解释：400-step adaptation 后 task CE 基本恢复；semantic route 和 task learning 不是完全不兼容。

### 1.3 B-context semantic routing retention

| Source | Refresh condition | Step-0 NMI | Final NMI | Decay |
|---|---|---:|---:|---:|
| `learned_random` | `refresh_freeze_continue` | `0.2172` | `0.0705` | `0.1467` |
| `learned_random` | `refresh_trainable_continue` | `0.2172` | `0.0546` | `0.1626` |
| `semantic_init_learned` | `refresh_freeze_continue` | `0.2983` | `0.1232` | `0.1750` |
| `semantic_init_learned` | `refresh_trainable_continue` | `0.2983` | `0.1018` | `0.1964` |

解释：refresh 后的 semantic routing 在 continuation 中明显衰减；router 可训练与否都没有稳定保持 B-context semantic route。

### 1.4 AB-specific functional specialization

| Source | Condition | Mean `S_AB` | Strong seeds |
|---|---|---:|---:|
| `learned_random` | `baseline_continue` | `0.0745` | `2/4` |
| `learned_random` | `refresh_freeze_continue` | `0.0868` | `1/4` |
| `learned_random` | `refresh_trainable_continue` | `0.0954` | `2/4` |
| `semantic_init_learned` | `baseline_continue` | `0.0113` | `0/4` |
| `semantic_init_learned` | `refresh_freeze_continue` | `0.0049` | `0/4` |
| `semantic_init_learned` | `refresh_trainable_continue` | `0.0011` | `0/4` |

解释：`learned_random` source 下 refresh 有小幅局部提升，但不跨 source 稳定；`semantic_init_learned` source 下没有形成 AB-specific functional expert。

## 2. 关键图

![B-context NMI trajectory](figures/refresh_b_context_nmi_trajectory.png)

这张图说明：refresh 的 step-0 semantic routing 在 400-step continuation 中显著衰减。

![Task CE trajectory](figures/refresh_task_ce_trajectory.png)

这张图说明：refresh 后 task CE 可以恢复到接近 baseline，failure 不是简单的任务学不会。

![S_AB trajectory](figures/refresh_S_AB_trajectory.png)

这张图说明：semantic refresh 没有形成稳定跨 source 的 AB-specific functional specialization。

![Final ablation heatmap](figures/refresh_final_class_expert_ablation_heatmap.png)

这张图说明：final class x expert ablation 没有显示一致的 AB-specific causal expert。

![Final B-context routing heatmap](figures/refresh_final_b_context_routing_heatmap.png)

这张图说明：final B-only / AB / CB routing 仍不是稳定 semantic partition。

## 3. 判断

这个 continuation 解决了旧 H0528a 的一个弱点：不是只固定 step-0 boundary，而是在 trained checkpoint 的 current hidden states 上重建 router。

结果显示：

```text
current-geometry semantic route 可恢复；
experts 可以适应到低 CE；
但 semantic routing 不稳定保持，functional specialization 不稳定形成。
```

因此 H0528a 结论不需要反转，只需要收紧：

```text
semantic route 不是完全不可用；
但没有 explicit route-function binding 时，它不会自然变成稳定的 functional expert specialization。
```

## 4. 结果路径

Runner:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0528a_semantic_router_refresh_continuation.py
```

Config:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0528a_semantic_router_refresh_continuation.json
```

Curated tables:

```text
main/experiments/H0521_router_feature_specialization/H0528a_semantic_router_refresh_continuation/tables/
```

Curated figures:

```text
main/experiments/H0521_router_feature_specialization/H0528a_semantic_router_refresh_continuation/figures/
```

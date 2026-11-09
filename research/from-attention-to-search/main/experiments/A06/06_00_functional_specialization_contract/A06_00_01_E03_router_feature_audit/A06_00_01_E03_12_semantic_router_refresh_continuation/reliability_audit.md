# Reliability Audit: H0528a Semantic Router Refresh Continuation

## 1. Audit 结论

实验通过可靠性检查：

```text
source checkpoints 存在；
refreshed semantic router 提高 step-0 B-context NMI；
baseline_continue 和 refresh_trainable_continue 有 router grad / delta；
refresh_freeze_continue router grad / delta 为 0；
所有条件仍是 top-1 selected-gate sparse dispatch；
没有 full soft mixture；
没有 selected gate renormalization。
```

因此本实验可以解释 current hidden geometry 上 semantic refresh + adaptation window 的效果。

## 2. Source Checkpoint Audit

8/8 checkpoints 存在：

```text
learned_random x 4 seeds
semantic_init_learned x 4 seeds
```

Source dir:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0528a_route_swap_and_frozen_semantic_router/h0528a_route_swap_frozen_semantic_4gpu_20260524
```

## 3. Refresh NMI Audit

| Source condition | Baseline B-context NMI | Refreshed B-context NMI | Gain |
|---|---:|---:|---:|
| `learned_random` | `0.0414` | `0.2015` | `+0.1601` |
| `semantic_init_learned` | `0.0446` | `0.2923` | `+0.2477` |

解释：refresh construction 没有失败；它确实把 router 重新居中到 current hidden state 中更 B-context semantic 的方向。

## 4. Gradient / Freeze Audit

| Condition | Router weight grad | Router bias grad | Router weight delta | Router bias delta | Passed |
|---|---:|---:|---:|---:|---:|
| `baseline_continue` | `0.028841` | `0.003851` | `0.016454` | `0.001486` | `1.0` |
| `refresh_freeze_continue` | `0.000000` | `0.000000` | `0.000000` | `0.000000` | `1.0` |
| `refresh_trainable_continue` | `0.774117` | `0.052588` | `0.018081` | `0.001642` | `1.0` |

`refresh_freeze_continue` 的 `router_logits.grad` 和 `router_probs.grad` 仍非空，说明 selected-gate path 仍在计算图中；只是 router 参数被冻结。

## 5. Sparse Dispatch Audit

所有 continuation conditions：

```text
active_experts_per_token_min = 1
active_experts_per_token_max = 1
full_soft_mixture = False
selected_gate_renormalized = False
dispatch_mode = top1_selected_gate_sparse
```

因此实验不是 soft mixture，也不是旧 hard argmax no-gate。

## 6. 已知限制

1. `S_AB` 是 single-expert ablation margin，不排除 distributed computation。
2. 400-step adaptation window 证明“短窗口不足以稳定诱导功能分工”，不能否定更长训练或 explicit regularizer。
3. Refresh router 只使用 B-context role prototypes；它不是 online EMA prototype router。
4. 实验仍是 AB/CB synthetic setup，不能外推到真实语言 MoE。

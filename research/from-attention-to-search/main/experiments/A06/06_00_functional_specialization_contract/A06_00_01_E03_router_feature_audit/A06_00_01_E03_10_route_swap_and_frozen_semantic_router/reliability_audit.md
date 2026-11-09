# Reliability Audit: H0528a Route Swap and Frozen Semantic Router

## 1. Audit 结论

实验实现通过基本可靠性检查：

```text
route swap 使用 H0527a final checkpoints；
frozen_semantic_router 的 router weight/bias 不在 optimizer 中；
frozen_semantic_router 的 router weight/bias grad = 0，delta = 0；
所有条件 active experts per token = 1；
所有条件 full_soft_mixture = False；
所有条件 selected_gate_renormalized = False。
```

因此本实验可以解释 top-1 sparse selected-gate 条件下的 route-function mismatch。

## 2. 训练前 audit

来自：

```text
main/experiments/H0521_router_feature_specialization/H0528a_route_swap_and_frozen_semantic_router/tables/training_condition_audit.csv
```

| Condition | Router grad | Router delta | Router frozen | Passed |
|---|---:|---:|---:|---:|
| `learned_random` | `0.043502` | `0.018101` | `0` | `1` |
| `semantic_init_learned` | `0.023592` | `0.017244` | `0` | `1` |
| `frozen_semantic_router` | `0.000000` | `0.000000` | `1` | `1` |

注意：`frozen_semantic_router` 中 `router_logits.grad` 和 `router_probs.grad` 仍然非空。这表示 router output 仍在计算图中，hidden representation / experts 仍能通过 selected-gate path 训练；只是 router 参数本身不更新。

## 3. Sparse dispatch audit

所有条件：

```text
active_experts_per_token_min = 1
active_experts_per_token_max = 1
full_soft_mixture = False
selected_gate_renormalized = False
dispatch_mode = top1_selected_gate_sparse
```

这保证本实验不是 soft mixture，也不是旧 hard argmax no-gate path。

## 4. Stage A artifact audit

Route swap 加载的是 H0527a final checkpoints：

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0527a_router_initialization_trajectory/h0527a_router_initialization_4gpu_20260524
```

`route_swap_artifact_availability.csv` 中 8/8 checkpoints 存在。

## 5. 已知限制

1. `semantic_current` 是 post-hoc diagnostic router，不是训练中在线更新的 router。
2. `frozen_semantic_router` 固定的是 step-0 semantic boundary；hidden states 训练后仍可漂移穿过这条边界。
3. `S_AB=0` 说明没有 AB-specific single-expert ablation margin，但不排除 distributed computation。
4. 实验仍是 synthetic AB/CB setup，不能外推到真实语言 MoE。

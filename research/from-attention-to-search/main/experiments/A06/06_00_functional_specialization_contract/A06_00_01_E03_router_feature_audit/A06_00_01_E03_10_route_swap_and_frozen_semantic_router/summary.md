# Summary: H0528a Route Swap and Frozen Semantic Router

## 0. 结论

本实验削弱了 strong `H_objective_mismatch`：

```text
semantic route 确实能更好分开 B-context hidden states，
但它不是当前 trained experts 的可用功能路由；
从训练开始固定 semantic router 也没有产生稳定 AB-specific functional expert。
```

更安全的更新是：

```text
router failure mode 不是单纯“learned router 没选到正确 semantic boundary”，
而是 NTP objective 下 route-function alignment 不可识别：
hidden geometry 可分、routing assignment、expert functional contribution 三者可以彼此脱钩。
```

## 1. 最重要结果

Stage A route swap：

| Metric | Mean |
|---|---:|
| `G_sem = CE(semantic_current) - CE(trained_final)` | `+1.8624` |
| `Q_sem = S_AB(semantic_current) - S_AB(trained_final)` | `-0.1068` |
| `A_learn_sem = NMI(trained route, semantic route)` | `0.0358` |
| trained B-context NMI | `0.0453` |
| semantic-current B-context NMI | `0.2605` |

解释：`semantic_current` 更能分开 B-context routing，但直接替换 learned router 会明显伤 task CE，并且没有提高 `S_AB`。

Stage B frozen training：

| Condition | Signal CE mean | Signal acc mean | Mean `S_AB` | Strong seeds |
|---|---:|---:|---:|---:|
| `learned_random` | `0.0023` | `0.9996` | `0.1863` | `1/4` |
| `semantic_init_learned` | `0.0008` | `0.9999` | `0.0719` | `1/4` |
| `frozen_semantic_router` | `0.0014` | `0.9998` | `0.0000` | `0/4` |

解释：frozen semantic router 可以学会任务，但没有形成 AB-specific functional expert。

## 2. 决策

继续研究 router failure，但不要把下一步设成“只做 semantic/prototype router”。当前证据说明 semantic separability 不是 sufficient condition。

更合理的下一步是：

```text
设计同时约束 route assignment 和 functional utility 的 router objective。
```

最小后续可以是：

```text
load-balance / entropy / exploration + route-function alignment audit
```

或者：

```text
prototype/cluster teacher + functional regularizer，而不是纯 geometry router。
```

## 3. 关键路径

The legacy purpose card was removed; this summary is the surviving result
source.

Detailed report:

```text
main/experiments/H0521_router_feature_specialization/H0528a_route_swap_and_frozen_semantic_router/detailed.md
```

Figures:

```text
main/experiments/H0521_router_feature_specialization/H0528a_route_swap_and_frozen_semantic_router/figures/
```

Tables:

```text
main/experiments/H0521_router_feature_specialization/H0528a_route_swap_and_frozen_semantic_router/tables/
```

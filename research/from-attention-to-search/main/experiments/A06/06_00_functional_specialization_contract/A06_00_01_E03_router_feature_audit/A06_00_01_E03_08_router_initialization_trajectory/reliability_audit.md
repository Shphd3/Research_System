# Reliability Audit: H0527a Router Initialization Trajectory

## 1. Validity Gates

| Gate | Result |
|---|---|
| SCO 4-GPU job submitted | pass, `pt-rc74x1rq` |
| Job completed | pass, `SUCCEEDED` |
| `top1_selected_gate` sparse dispatch | pass |
| Active experts per token | pass, min = max = 1 |
| Full soft mixture absent | pass |
| Router weight gradient nonzero | pass |
| Router bias gradient nonzero | pass |
| Router parameter delta after one step nonzero | pass |
| Semantic init improves step-0 B-context NMI | pass |

## 2. Audit Numbers

| Condition | Router weight grad | Router bias grad | Router weight delta | Router bias delta | Step-0 B-context NMI |
|---|---:|---:|---:|---:|---:|
| random_init | 0.043502 | 0.003369 | 0.018101 | 0.001601 | 0.0045 |
| semantic_context_init | 0.023592 | 0.000910 | 0.017244 | 0.001205 | 0.3124 |

## 3. Implementation Boundary

The semantic condition uses `whitened_centroid` initialization:

```text
roles: B_in_B_only, B_in_AB, B_in_CB
prototype scale: 8.0
covariance regularization: 0.001
unused expert bias: -8.0
```

This is still a router initialization intervention only. It does not add load-balance loss, z-loss, top-2 routing, capacity constraints, or expert regularization.

## 4. Raw Artifact Boundary

Raw logs, checkpoints, and full result directories remain under:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0527a_router_initialization_trajectory/
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/
```

Only curated figures, tables, and report documents are promoted into:

```text
main/experiments/H0521_router_feature_specialization/H0527a_router_initialization_trajectory/
```

## 5. Residual Risk

The experiment did not run H0527b first, even though the purpose card originally recommended it. This is acceptable only because H0527a included a direct step-0 B-context NMI audit showing that the semantic init condition changed the intended routing signal. It still cannot explain why that signal decays; H0527b remains necessary for hidden-geometry diagnosis.

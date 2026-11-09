# Result Summary: H0527a Router Initialization Trajectory

Hypothesis purpose card:

The legacy purpose card was removed; this summary is the surviving result
source.

## Observation

主结论：semantic/context prototype initialization 可以在 step 0 提高 B-context routing NMI，但训练到 1600 steps 后，这个 routing prior 基本被抹平；final \(S_{AB}\) 没有跨 seed 稳定增强。

Validity audit passed:

| Condition | Router weight grad | Router delta | Step-0 B-context NMI | Sparse audit |
|---|---:|---:|---:|---:|
| random_init | 0.043502 | 0.018101 | 0.0045 | pass |
| semantic_context_init | 0.023592 | 0.017244 | 0.3124 | pass |

Primary metric:

| Condition | Seed 20260521 | Seed 20260522 | Seed 20260523 | Seed 20260524 | Mean |
|---|---:|---:|---:|---:|---:|
| random_init | -0.0002 | 0.0000 | 0.7449 | 0.0003 | 0.1863 |
| semantic_context_init | 0.0000 | 0.0000 | 0.0000 | 0.2876 | 0.0719 |

Task learned in both conditions:

| Condition | A-only acc | B-only acc | AB acc | CB acc |
|---|---:|---:|---:|---:|
| random_init | 1.0000 | 0.9997 | 0.9992 | 0.9997 |
| semantic_context_init | 0.9998 | 1.0000 | 0.9998 | 1.0000 |

## Interpretation

Result:

```text
semantic_context_init is a valid causal intervention on initial routing, but it does not produce stable final AB-specific functional specialization.
```

The initial semantic routing signal decays:

| Condition | Step-0 B-context NMI | Final B-context NMI |
|---|---:|---:|
| random_init | 0.0019 | 0.0437 |
| semantic_context_init | 0.2469 | 0.0468 |

Semantic init also makes routing more confident and lower entropy:

| Condition | Final load entropy | Final selected probability |
|---|---:|---:|
| random_init | 1.0940 | 0.6298 |
| semantic_context_init | 0.7770 | 0.9610 |

This supports the H0527a hypothesis: random initialization is not the decisive cause of H0526's unstable functional specialization. The stronger candidate mechanism is training dynamics / router objective / expert feedback erasing or overriding the semantic prior.

## Limitation

This run intentionally did not add load-balance loss, top-2 routing, z-loss, capacity constraints, or representation changes. It only tests whether semantic/context initialization alone stabilizes functional specialization.

## Key Figures

![S_AB trajectory by init](figures/S_AB_trajectory_by_init.png)

这张图说明：semantic initialization 没有让 mean \(S_{AB}\) 在训练后稳定高于 random initialization。

![Context routing NMI trajectory by init](figures/context_routing_nmi_trajectory_by_init.png)

这张图说明：semantic initialization 的 step-0 B-context routing 优势在训练过程中快速衰减，final 接近 random init。

![Final B context routing heatmap](figures/init_vs_final_b_context_routing_heatmap.png)

这张图说明：final B-only / AB / CB source-token routing 仍然是 seed-dependent，不能单独作为 functional specialization 证据。

![Class expert ablation delta by init](figures/class_expert_ablation_delta_by_init.png)

这张图说明：AB-specific CE delta 没有跨 seed 稳定出现；semantic init 只在 seed `20260524` 出现中等 AB-specific delta。

![Router movement from init](figures/router_prototype_cosine_trajectory.png)

这张图说明：router weights 在训练中持续离开初始状态，semantic prior 不是固定边界。

## Claim Update

Supported:

```text
Semantic/context router initialization is not sufficient to produce stable AB-specific functional expert specialization in this top-1 sparse setup.
```

Weakened:

```text
H0526 instability is mainly caused by random router initialization.
```

Still unclear:

```text
Whether load-balance loss, router objective shaping, or hidden-geometry changes can preserve context-aware routing while producing functional specialization.
```

## Decision

Do not keep sweeping initialization variants. The next decisive step should be H0527b hidden-geometry audit or a single-variable load-balance/objective intervention, with \(S_{AB}\) and ablation delta still as primary evidence.

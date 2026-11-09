# Result Summary: H0528a Router Prior Decay Audit

Hypothesis purpose card:

The legacy purpose card was removed; this summary is the surviving result
source.

## Observation

主结论：H0527a 的 semantic prior 衰减不是因为 final hidden states 完全不含 B-context boundary。相反，final hidden states 中仍可由 `recentered_current` semantic router 恢复 B-context structure；问题是 trained router 基本不用这条 boundary，而且 forced-routing utility margin 很小。

Artifact boundary:

```text
H0527a 只保存 final model.pt，没有保存 200/400/800/1200 的 model checkpoint。
因此 H0528a 做的是 step-0 router reconstruction + final-checkpoint offline audit。
```

Primary metric:

| Condition | Frozen-init NMI | Recentered-current NMI | Trained-final NMI | Unused semantic gap |
|---|---:|---:|---:|---:|
| random_init | 0.0419 | 0.2126 | 0.0452 | 0.1674 |
| semantic_context_init | 0.0475 | 0.3040 | 0.0422 | 0.2618 |

Forced-routing utility margin is small:

| Condition | B_in_AB margin | B_in_B_only margin | B_in_CB margin |
|---|---:|---:|---:|
| random_init | 0.0060 | 0.0024 | 0.0001 |
| semantic_context_init | 0.0034 | 0.0095 | 0.0012 |

## Interpretation

Result pattern:

```text
frozen-init low, recentered-current high, trained-final low, utility margin small
```

Interpretation:

```text
The original semantic initialization boundary becomes stale, but a fresh semantic boundary is still recoverable from final hidden states. The trained router does not track it, and the task loss gives only weak expert-utility margin for preserving this B-context assignment.
```

This supports H0528a Case C with a representation-drift component:

```text
semantic routing is recoverable, but under the current NTP loss expert utility is underdetermined; initialization changes assignment but does not create a stable functional attractor.
```

## Limitation

This is an offline audit over final checkpoints, not a new training intervention. It cannot prove that a router alignment loss, load-balance loss, top-2 routing, or a functional regularizer would succeed.

The forced-routing utility uses the model's selected-gate path with `gate_mode = router_prob`; it tests utility under the actual gated sparse path, not pure expert-only utility with gate fixed to 1.

## Key Figures

![Router NMI comparison](figures/router_nmi_comparison.png)

这张图说明：final hidden states 中 `recentered_current` router 能恢复 B-context structure，但 trained router 的 B-context NMI 很低。

![Unused semantic gap by seed](figures/unused_semantic_gap_by_seed.png)

这张图说明：unused semantic gap 在几乎所有 seed 中为正，semantic condition 中尤其明显。

![B-context routing heatmap](figures/b_context_routing_heatmap_by_variant.png)

这张图说明：recentered router 产生更结构化的 B-context routing，而 trained router 接近低语义区分。

![Forced utility margin](figures/forced_utility_margin_heatmap.png)

这张图说明：强制路由到最佳 expert 与第二佳 expert 的 CE 差距很小，task loss 对固定 B-context expert assignment 的偏好弱。

## Claim Update

Supported:

```text
H0527a semantic prior decays because static init boundary becomes stale and trained router does not track a recoverable current semantic boundary.
```

Also supported:

```text
Expert utility margin is small, so the task loss has weak reason to preserve a fixed semantic expert assignment.
```

Weakened:

```text
The final representation simply lost all B-context semantic information.
```

Still unclear:

```text
Whether a pure expert-only forced utility audit with gate fixed to 1 would reveal stronger expert differences than the actual selected-gate path.
```

## Decision

Do not jump directly to another initialization variant. The next sharp test should distinguish:

```text
expert utility truly underdetermined
vs
router-prob gate suppresses forced expert utility.
```

Minimum next step:

```text
Repeat final forced utility with gate_mode = one, or design a functional regularizer only if expert-only utility margin exists.
```

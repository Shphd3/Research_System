# Result Summary: H0526 Top-1 Sparse Router Failure Mode

Hypothesis purpose card:

The legacy purpose card was removed; this summary is the surviving result
source.

## Observation

Primary conclusion: C1 `top1_selected_gate` is a valid trainable top-1 sparse router and learns the task, but does **not** reliably form stable AB-specific functional expert specialization.

Validity audit:

| Condition | Router weight grad | Router bias grad | Router logits grad | Router weight delta | Active experts / token | Pass |
|---|---:|---:|---|---:|---:|---:|
| hard top-1 no-gate | 0.000000 | 0.000000 | None | 0.000000 | 1 | 0 |
| top-1 selected gate | 0.043496 | 0.003369 | nonzero | 0.018101 | 1 | 1 |

Task readback:

| Class | Mean accuracy |
|---|---:|
| A-only | 1.0000 |
| B-only | 0.9998 |
| AB-composite | 0.9997 |
| CB-composite | 0.9991 |

Primary research metric:

| Seed | \(S_{AB}\) | Best AB-specific expert |
|---:|---:|---:|
| 20260521 | -0.0006 | 3 |
| 20260522 | 0.0064 | 0 |
| 20260523 | 0.7093 | 2 |
| 20260524 | 0.0014 | 0 |

Only seed `20260523` shows a strong AB-specific margin. The other three seeds are near zero.

## Interpretation

Result:

```text
top-1 selected-gate sparse MoE can learn the AB/CB task, but no-load-balance training does not yield stable class-specific functional expert specialization across seeds.
```

Main failure mode:

```text
unstable functional specialization / route-function mismatch, with moderate load imbalance.
```

This is not an implementation failure: the router has gradient, parameters update, and each token activates exactly one expert.

## Limitation

This run tests only no-load-balance top-1 selected gate. It does not test load-balance loss, z-loss, top-2 routing, capacity limits, or real data.

## Key Figures

![Class expert ablation delta heatmap](figures/class_expert_ablation_delta_heatmap.png)

This figure shows class-by-expert loss delta. Only seed `20260523` has a strong AB-specific expert; other seeds do not.

![B context routing by seed](figures/b_context_routing_by_seed.png)

This figure shows B-source routing under B-only / AB / CB contexts. Routing split/same patterns vary, so routing alone cannot decide success.

![Load trajectory by seed](figures/load_trajectory_by_seed.png)

This figure shows load entropy remains nonzero but seed-dependent; the run has moderate imbalance rather than total collapse.

## Claim Update

Supported:

```text
Selected-gate top-1 sparse routing gives router task-loss gradients while keeping one active expert per token.
```

Weakened:

```text
No-load-balance top-1 sparse router naturally forms stable functional specialization in this AB/CB setup.
```

Still unclear:

```text
Whether adding load-balance loss stabilizes ablation-defined specialization.
```

## What Cannot Be Claimed

Cannot claim sparse MoE generally fails.

Cannot claim same-route or split-route is success/failure without ablation.

Cannot claim top-2, Switch with auxiliary losses, or real-language MoE has the same behavior.

## Next Decision

Do not continue by reading routing heatmaps alone. The next minimum experiment should add one factor only:

```text
top-1 selected gate + load-balance loss
```

Decision metric should remain class-specific ablation delta and \(S_{AB}\).

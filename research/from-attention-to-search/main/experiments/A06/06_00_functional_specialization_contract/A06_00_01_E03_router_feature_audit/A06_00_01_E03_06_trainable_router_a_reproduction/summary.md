# Result Summary: H0525a Trainable-Router A Reproduction

## Observation

Corrected A passes the trainable-router validity audit, but does **not** reproduce H0524a's same/split pattern.

Most important metric: final `B_in_B_only` vs `B_in_AB` dominant expert.

| Seed | Init B-only / AB | Final B-only / AB | Final same |
|---:|---|---|---:|
| 20260521 | 2 / 2 | 2 / 2 | 1 |
| 20260522 | 0 / 0 | 2 / 2 | 1 |
| 20260523 | 2 / 0 | 0 / 0 | 1 |
| 20260524 | 2 / 2 | 1 / 1 | 1 |

H0524a expected `20260524` to split. In corrected A, all four seeds route B-only and AB B source-tokens to the same final dominant expert.

## Interpretation

The valid trainable-router version changes the core H0524a outcome: the old split seed disappears.

Result:

```text
router is trainable, but B-only / AB split is not reproduced.
```

Interpretation:

```text
H0524a/H0524b's split pattern was likely dominated by fixed random router boundaries and hidden-state movement under those boundaries, not by trainable router optimization trajectory.
```

## Limitation

This run tests a soft-mixture MoE, not sparse top-k with load balancing. It validates a differentiable router path, but it does not prove that every trainable sparse router would remove the split.

## Key Figures

![Router gradient audit](figures/router_gradient_audit.png)

This figure shows `moe_soft_mixture` has nonzero router gradient and router step delta, while hard top-1 remains zero/None.

![Router weight delta over training](figures/router_weight_delta_over_training.png)

This figure shows router parameters continue changing during corrected A training for every seed.

![B-context routing by seed](figures/b_context_routing_by_seed.png)

This figure shows final B-only / AB / CB routing under corrected A; B-only and AB are same-route in all four seeds.

![Init vs final B routing by seed](figures/init_vs_final_b_routing_by_seed.png)

This figure shows initialization and final routing are not identical, but the final corrected A pattern has no split seed.

![Class metrics by seed](figures/class_metrics_by_seed.png)

This figure shows the signal classes are learned, so routing conclusions are not from an untrained model.

## Claim Update

Supported:

```text
H0525a is a valid trainable-router corrected A run: router gradients and router parameter deltas are nonzero.
```

Weakened:

```text
H0524a/H0524b can explain trainable router optimization trajectory.
```

Current claim boundary:

```text
The previous split result should be treated as a fixed-router-boundary artifact unless reproduced by a trainable sparse-router variant.
```

## Decision

Do **not** continue to B trajectory from H0524b as originally planned.

Next decision should be redesign, not trajectory extension: either test a sparse trainable router with selected continuous gate weights / auxiliary router loss, or return to factor attribution under the corrected model.

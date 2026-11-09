# Reliability Audit: H0525a Trainable-Router A Reproduction

## Conclusion

H0525a passes implementation validity, but fails A reproduction.

## 1. Router Gradient Path

Direct audit confirms:

| Check | hard top-1 | `moe_soft_mixture` |
|---|---:|---:|
| optimizer contains router weight | true | true |
| optimizer contains router bias | true | true |
| router weight grad norm | 0.000000 | 0.075563 |
| router bias grad norm | 0.000000 | 0.006685 |
| router logits grad | None | nonzero |
| router probs grad | None | nonzero |
| router weight delta after step | 0.000000 | 0.018102 |

![Router gradient audit](figures/router_gradient_audit.png)

This figure confirms the new variant has a real router gradient path and the old hard top-1 path remains a valid negative control.

## 2. Training-Time Router Delta

Final router weight deltas:

```text
20260521: 1.737050
20260522: 1.745191
20260523: 1.681612
20260524: 1.683998
```

![Router weight delta over training](figures/router_weight_delta_over_training.png)

This figure confirms the corrected A router is not fixed during training.

## 3. Task Success

Signal-class accuracy is near perfect:

```text
A-only:       0.999844
B-only:       1.000000
AB-composite: 0.999844
CB-composite: 0.999375
```

![Class metrics by seed](figures/class_metrics_by_seed.png)

This figure shows the routing result is evaluated after the model learned the motif targets.

## 4. Primary Reproduction Check

H0524a reproduction target:

```text
3/4 same-route, seed 20260524 split
```

H0525a corrected result:

```text
4/4 same-route, no split seed
```

![B-context routing by seed](figures/b_context_routing_by_seed.png)

This figure shows the corrected final routing pattern no longer contains the H0524a split seed.

## 5. Reliability Judgment

Valid:

```text
The experiment tests a trainable-router condition.
```

Invalidated:

```text
Using H0524a/H0524b as evidence for trainable router optimization trajectory.
```

Decision:

```text
Do not continue B trajectory from the hard top-1 setup. Treat the old split as likely fixed-boundary artifact until a trainable sparse-router variant reproduces it.
```

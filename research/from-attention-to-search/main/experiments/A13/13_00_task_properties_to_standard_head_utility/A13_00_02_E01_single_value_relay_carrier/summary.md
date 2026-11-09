# A13_00_02_E01 Summary

## Direct Result

**Pass:** removing query-conditioned selection produced a valid single-value
relay carrier. Across five registered seeds, two-layer relay and one-layer
bypass both reached 1.000 held-out answer accuracy; the structurally
disconnected one-layer relay stayed at 0.0583, near the \(1/16=0.0625\) chance
level. Both input counterfactuals and relay-state donor interventions scored
1.000.

![Carrier learning trajectories](figures/carrier_trajectory.png)

## What Changed

The failed query-conditioned carrier required the relay to bind two values to
a delayed selector. E01 keeps the same path but makes the answer always equal
to early value \(A\). The pass therefore shows that state formation, transport,
and ordinary-head use are learnable; query-conditioned binding was the extra
bottleneck.

## Remaining Guard

The random selector in this serialization is an unpredictable shared-aux
boundary target, while the Next-2-only answer target is predictable. Reading an
objective comparison here could therefore confuse lower auxiliary-target
entropy with useful earlier supervision.

## Next Decision

Revalidate the same carrier after replacing the random selector with a fixed
marker and removing duplicate selector variants.

# V2.1 Problem Statement

## Main question

In a spectrally normalized route-relevant feature space, can we construct a non-cheating MoE router that has three properties?

1. **Equal mass**: every expert receives probability mass `1/E`.
2. **Feature coherence**: when latent feature structure exists, routes preserve it.
3. **Preservation**: routes remain stable under controlled training drift.

## Why this is different from V2

V2 showed that recursive quantiles can solve equal-mass dispatch. V2.1 asks what additional structure and method design are required for a good router.

## Mild assumptions to test

V2.1 does not assume arbitrary isotropic distributions are solvable. It tests explicit mild assumptions:

- globally spectrally normalized features;
- local clusterability or feature coherence;
- expert weights aligned with feature geometry;
- low boundary mass;
- bounded drift relative to routing margin.

## Main method hypothesis

```text
Quantiles provide mass.
Local/expert geometry provides feature coherence.
Margins provide preservation.
```

# V2.2 Problem Statement: Static Good Dispatch under Spectral Isotropy

## 1. Main question

In a spectrally isotropic route-relevant feature space, can we construct a non-cheating static MoE router whose feature-space partition is not only equal-mass, but also feature-coherent and useful for a controlled static learning objective?

The question is deliberately static.  It does not include representation drift, route preservation, or dynamic router updates.

## 2. Why the old v2.1 scope was premature

The previous v2.1 scope used:

```text
equal mass + feature coherence + preservation
```

This is conceptually correct as a long-term decomposition, but it combines two stages:

1. **Static dispatch**: what partition should be constructed in the first place?
2. **Training preservation**: will training keep that partition stable?

V2.2 handles only Stage 1.  Preservation should be a later paper or later section after static good dispatch is understood.

## 3. What spectral isotropy can and cannot explain

### 3.1 What it cannot explain

Spectral isotropy alone does not imply a good router.

It does not imply:

- equal-mass routing by an arbitrary prototype router;
- semantic feature partition;
- expert specialization;
- downstream utility.

Recursive quantiles also do not mathematically require spectral isotropy to equalize mass.  Therefore the causal chain is not:

```text
spectral isotropy -> equal mass
```

### 3.2 What it can explain

Spectral isotropy is still important in the controlled research setting because it removes global anisotropic confounds:

```text
no single high-variance direction should dominate routing geometry
```

It makes feature distances, local neighborhoods, prototype directions, and split objectives interpretable in a shared normalized geometry.  Under additional local feature structure, this gives a clean setting in which to test whether a router can recover coherent feature cells.

The revised causal chain is:

```text
spectral normalization -> clean global metric
local feature structure / expert alignment -> informative split directions
quantile thresholds -> equal mass
static expert compatibility -> controlled utility
```

## 4. Static good dispatch

Let `X in R^d` be the route-relevant feature and `g: R^d -> {1,...,E}` a deterministic router.  Let:

```text
C_e = {x : g(x)=e}
```

### Target A: equal mass

```text
P(g(X)=e)=1/E for every expert e.
```

This is the mass target.  It is necessary but not sufficient.

### Target B: feature coherence

When there is latent feature identity `F`, the route should be informative about `F`:

```text
I(g(X); F) high
purity high
within-cell variance low
between-cell separation high
```

The router may not use `F` during construction.  `F` is an evaluation-only variable.

### Target C: static utility / expert compatibility

A coherent partition should help a controlled static learning task when the task structure is feature-dependent, or it should align cells with model-internal expert geometry when such geometry exists.

Possible audits:

```text
cell-to-expert prototype alignment
static hard-routing regression loss
expert specialization score after fitting experts with frozen routes
```

No training-time route preservation claim is made.

## 5. Non-cheating rule

A router is non-cheating if, after calibration, routing a token uses only:

- the current route-relevant feature;
- stored calibration statistics from unlabeled features;
- optional model-internal expert weights.

It may not use:

- latent feature labels during construction;
- task labels / next-token answers during routing construction;
- evaluation labels;
- current-batch expert counts;
- post-hoc assignment to underfilled experts as the main method.

Balanced assignment remains a control, not the method.

## 6. Required middle-regime assumptions

V2.2 should not assume arbitrary isotropic distributions are solvable.  It should test a ladder of explicit assumptions.

### Assumption A: global spectral isotropy

After centering and optional spectral normalization:

```text
Cov(tilde X) approximately sigma^2 I
```

This removes high-variance confounds.

### Assumption B: balanced feature frequency

Latent features, when present, are frequency-balanced or close to balanced:

```text
P(F=f) approximately 1/K
```

This matches the advisor's clean-case instruction that both feature frequency and representation geometry are uniform.

### Assumption C: local feature structure

Features have local coherence after spectral normalization:

```text
X | F=f = mu_f + epsilon
```

with separated centers or separated local manifolds.

### Assumption D: optional expert alignment

Expert weights may provide model-internal directions or subspaces aligned with feature geometry:

```text
v_e approximately aligned with a feature direction / feature group
```

This is optional.  If expert weights are random or noisy, the expert-guided variant should not claim benefit.

### Assumption E: regularity for deterministic splitting

The projection distributions should be sufficiently continuous, or discrete atoms / ties must be explicitly handled and reported.

## 7. Falsifiable hypotheses

### H1: isotropy alone is insufficient

On isotropic but unstructured features, routers can equalize mass but should not achieve meaningful route-feature agreement.

### H2: local feature structure is necessary for coherence

On globally isotropic but locally clusterable features, locality-aware or expert-aligned split directions should improve NMI / purity relative to random-axis quantile splits.

### H3: quantiles are the mass mechanism

If split directions are held fixed, changing from raw thresholds to quantile thresholds should reduce LoadCV.  This should hold beyond isotropic distributions.

### H4: spectral normalization is a metric-cleaning mechanism

In anisotropically distorted feature mixtures, raw local geometry should degrade; whitening or spectral shrinkage should recover the coherent partition if the underlying local structure is preserved.

### H5: expert guidance helps only with alignment

Expert-guided routing should improve coherence and expert compatibility only when expert weights are aligned with feature geometry.  Random expert weights should not help.

### H6: static utility follows coherence only when the task is feature-dependent

On controlled tasks with feature-dependent target maps, coherent routes should improve static expert fitting.  On feature-independent tasks, good mass/coherence should not automatically improve loss.

## 8. Success criterion for v2.2

V2.2 is successful if it establishes the following bounded claim:

```text
In a globally spectrally isotropic but locally structured feature distribution,
a non-cheating static router can construct equal-mass and feature-coherent cells.
Quantiles provide mass; spectral normalization provides the clean metric;
local or expert-aligned geometry provides coherence; static utility appears only when the task or experts match the feature structure.
```

It should not claim:

- spectral isotropy alone gives semantic routing;
- equal mass implies feature coherence;
- expert weights always help;
- static dispatch solves training preservation;
- synthetic static utility implies real language-model utility.

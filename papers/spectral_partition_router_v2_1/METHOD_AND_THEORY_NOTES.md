# V2.1 Method and Theory Notes

## 1. Why V2.1 exists

V2 solved one precise target:

\[
P(g(X)=e)=1/E.
\]

This is equal-mass dispatch. It is important but insufficient.

V2.1 asks for a better router with three properties:

1. **Equal mass**: each expert receives equal feature probability mass.
2. **Feature coherence**: routing agrees with latent feature structure when such structure exists.
3. **Preservation**: routing remains stable under controlled training drift.

The key insight is:

```text
Quantiles give mass.
Geometry gives feature meaning.
Margins give preservation.
```

---

## 2. Main assumptions

V2.1 should not claim that covariance isotropy alone is enough for good routing.

The useful middle assumptions are:

### Assumption A: Spectral normalization

\[
\mathrm{Cov}(\tilde X)\approx \sigma^2 I.
\]

This removes anisotropy as a confound.

### Assumption B: Local feature structure

There may exist latent feature groups:

\[
X = \mu_F + \epsilon.
\]

Labels `F` are not used by the method, only by evaluation.

### Assumption C: Expert alignment prior

Expert weights may contain principal directions aligned with feature geometry:

\[
v_e \approx \mu_f / \|\mu_f\|.
\]

This is optional but important for meaningful partition.

### Assumption D: Low boundary mass

A useful partition should not cut through too much probability mass:

\[
P(m(X)\le \gamma)
\]

should be small.

### Assumption E: Bounded drift

Training drift should be smaller than route margin for most examples.

---

## 3. Correct theory hierarchy

### Theorem 1: Recursive quantile equal mass

If every tree node splits mass in proportion to child expert counts, every leaf has mass `1/E`.

### Proposition 2: Atom impossibility

If an atom has probability greater than `1/E`, no deterministic feature-only router can split it uniformly without sending identical features to different experts.

### Proposition 3: Coherence requires projected separation

If a split direction separates latent groups with error `epsilon`, then the split disagrees with the latent group at probability at most `epsilon`.

### Proposition 4: Expert directions help only if aligned

If an expert-guided direction is close to an ideal feature-separating direction, split disagreement is bounded by the low-margin mass.

### Theorem 5: Preservation requires margin

If feature drift is smaller than the tree margin, the route does not change.

---

## 4. What to fix from V2 implementation

1. SVD sign ambiguity.
2. Random-axis vs fixed-basis naming.
3. Deterministic feature-derived tie handling.
4. Forced-count baseline naming.
5. True learnable-router baseline if claiming training dynamics.
6. Margin-aware update instead of naive slow update.

---

## 5. What V2.1 should claim after experiments

Allowed claims if supported:

- GA-SPR preserves equal-mass dispatch.
- Expert-guided GA-SPR improves feature coherence when expert weights align with feature geometry.
- Margin-aware updates reduce route flips compared with naive recalibration.

Forbidden claims:

- isotropy alone gives semantic routing;
- equal mass implies feature specialization;
- expert weights always help;
- margin-aware update solves arbitrary training dynamics;
- controlled synthetic results imply real LLM utility.

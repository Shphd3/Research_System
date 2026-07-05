# V2.2 Experiment Plan: Static Good Dispatch

## 0. Purpose

V2.2 tests static good dispatch under a precise scope:

```text
spectrally isotropic route-relevant features
+ optional local feature structure
+ optional expert alignment
=> equal-mass, feature-coherent, statically useful dispatch
```

Training preservation, route drift, slow updates, and learned-router dynamics are out of scope.

---

## 1. Implementation fixes inherited from V2

Before experiments:

1. Rename ambiguous methods:
   - `spr_fixed` -> `c_spr_random_axis` unless a true basis is implemented;
   - `lb_control` -> `balanced_assignment_control`;
   - remove `slow_update_spr` from v2.2.
2. Implement true fixed basis:
   - coordinate;
   - orthogonal random;
   - Hadamard if available.
3. Implement projective expert prototypes:
   - `P_e = v_e v_e^T`;
   - projective distance `1 - trace(P_i P_j)`;
   - projective expert grouping.
4. Implement feature-derived tie handling:
   - lexicographic projection keys;
   - tie rate;
   - max atom mass;
   - exact split possible flag.
5. Separate calibration and holdout metrics.
6. Use labels only for evaluation.

---

## 2. Shared metrics

### Mass metrics

- calibration LoadCV;
- holdout LoadCV;
- max absolute usage error;
- calibration-to-holdout gap;
- max/min usage ratio.

### Coherence metrics

- route-feature NMI;
- feature purity;
- weighted within-cell variance;
- between-cell center separation;
- margin p05.

### Spectral metrics

- covariance condition number;
- effective rank;
- top eigenvalue ratio;
- anisotropy score before / after normalization.

### Expert compatibility metrics

- cell-prototype alignment;
- nearest-neighbor prototype cosine;
- max pairwise prototype cosine;
- effective prototype rank;
- expert group agreement.

### Static utility metrics

- frozen-route expert fitting train loss;
- validation loss;
- per-feature loss variance;
- expert specialization score.

---

## 3. E1: Equal-mass sanity and method health

### Goal

Verify that C-SPR variants preserve the V2 mass result after naming, tie, and prototype fixes.

### Data

- isotropic Gaussian;
- spherical features;
- whitened continuous mixture;
- discrete / atom-supported boundary cases.

### Methods

- Vanilla random linear;
- regular simplex top-1;
- C-SPR-RandomAxis;
- C-SPR-FixedBasis;
- C-SPR-Local;
- C-SPR-Expert;
- C-SPR-ExpertLocal;
- Balanced assignment control.

### Hypothesis

Quantile-based C-SPR variants should have low calibration LoadCV and low holdout LoadCV under stable calibration distributions.

### Falsifier

If quantile variants have high calibration LoadCV in continuous data, the implementation is wrong.

---

## 4. E2: Isotropy-alone null anchor

### Goal

Show that spectral isotropy alone does not create feature coherence.

### Data

1. `X ~ N(0, I)` with random labels independent of `X`.
2. `X` uniformly spherical with random labels independent of `X`.
3. Optional: labels assigned by a random hash unrelated to local geometry.

### Methods

C-SPR variants and baselines.

### Expected result

- LoadCV can be low for quantile methods.
- NMI and purity should be near random.

### Interpretation

This is not a method failure.  It confirms that feature coherence is not identifiable from isotropy alone.

---

## 5. E3: Globally isotropic but locally structured features

### Goal

Test the middle-regime assumption:

```text
global spectrum isotropic + local feature structure
```

### Data

Balanced latent feature mixture:

```text
F uniform in {1,...,K}
Z | F=f = separation * mu_f + noise
X = whiten(Z)
```

Vary:

- separation;
- noise;
- number of feature groups `K`;
- dimension `d`;
- expert count `E`;
- class balance.

### Methods

- C-SPR-RandomAxis;
- C-SPR-FixedBasis;
- C-SPR-Local;
- C-SPR-Expert with random experts;
- C-SPR-Expert with aligned experts;
- Balanced assignment control;
- optional balanced k-means / graph partition baseline as an upper unsupervised baseline.

### Hypothesis

C-SPR-Local or C-SPR-ExpertLocal should improve NMI / purity relative to mass-only variants when local structure is sufficiently separated.

### Falsifier

If C-SPR-Local does not improve over random-axis even under strong separation, the local objective is too weak or the candidate direction set is insufficient.

---

## 6. E4: Expert alignment ladder

### Goal

Test whether expert weights help only when they contain aligned geometry.

### Data

Use the isotropic local mixture from E3.

Expert settings:

1. aligned expert prototypes;
2. partially aligned prototypes;
3. noisy aligned prototypes;
4. random prototypes;
5. clustered but misaligned prototypes.

### Methods

- Expert-SVD top-1;
- projective expert top-1 / nearest-subspace audit;
- C-SPR-Expert;
- C-SPR-ExpertLocal;
- C-SPR-Local.

### Hypothesis

Expert-guided C-SPR should improve cell-prototype alignment and feature NMI only when expert geometry is aligned with feature geometry.

### Falsifier

If random expert weights improve NMI consistently, the method may be leaking labels or the synthetic data / metric is flawed.

---

## 7. E5: Spectral normalization causal ablation

### Goal

Show the correct causal role of spectral normalization.

### Data

Start from an isotropic local mixture `Z`, then apply elliptical distortion:

```text
X = A Z
```

with controlled condition number.

Compare:

- raw distorted features;
- centered normalized only;
- shrinkage-normalized;
- whitened;
- oracle original `Z`.

### Hypothesis

Raw anisotropic geometry should degrade local coherence; whitening should recover coherence when the underlying local structure is preserved.

### Falsifier

If whitening does not help even when the distortion is the only change, either the local objective is not using the restored metric or the synthetic construction is not recoverable.

---

## 8. E6: Static utility audit

### Goal

Test whether coherent static routing improves a controlled frozen-route expert fitting task.

### Task A: feature-dependent target

```text
Y = A_F X + noise
```

Each latent feature group has its own target map.

### Task B: feature-independent target

```text
Y = A X + noise
```

All features share the same target map.

### Methods

- random linear;
- C-SPR-RandomAxis;
- C-SPR-Local;
- C-SPR-ExpertLocal;
- balanced assignment control;
- oracle feature route upper bound.

### Hypothesis

Coherent routes should improve Task A but not necessarily Task B.

### Falsifier

If coherent routes do not improve Task A relative to incoherent equal-mass routes, either coherence is insufficient, expert capacity is mismatched, or the task does not actually require feature-specialized experts.

---

## 9. E7: Failure modes

### Cases

- no local structure;
- high overlap / low separation;
- unbalanced feature frequency;
- large atoms exceeding `1/E`;
- random expert weights;
- calibration / holdout distribution shift;
- dimension too low for required feature separation;
- expert count mismatched with feature count.

### Required output

For each failure mode, report which assumption was violated:

```text
global isotropy
balanced feature frequency
local structure
expert alignment
regularity / no large atoms
calibration stability
static task-feature compatibility
```

---

## 10. Paper tables to generate after runs

Do not manually enter numbers.  Generate:

```text
latex/tables/e1_equal_mass.tex
latex/tables/e2_isotropy_null.tex
latex/tables/e3_local_structure.tex
latex/tables/e4_expert_alignment.tex
latex/tables/e5_spectral_normalization.tex
latex/tables/e6_static_utility.tex
latex/tables/e7_failures.tex
```

Suggested figures:

```text
latex/figures/e2_isotropy_null_nmi.pdf
latex/figures/e3_nmi_vs_separation.pdf
latex/figures/e4_alignment_ladder.pdf
latex/figures/e5_whitening_recovery.pdf
latex/figures/e6_static_utility_loss.pdf
```

# V2.2 Research Plan: From Spectral Isotropy to Static Good Dispatch

## 0. Research goal

The next research stage is not training preservation.  The goal is to close the static dispatch problem:

```text
Given spectrally isotropic route-relevant features,
define what a good static dispatch means,
identify what extra assumptions are needed beyond isotropy,
and construct / test a non-cheating router under those assumptions.
```

The correct research output is a paper framework plus experiments that make every unclear point falsifiable.

---

## 1. Core judgment

V2 solved equal-mass dispatch.  But equal mass is too weak.

V2.2 should answer a sharper question:

```text
When global spectrum is isotropic, can local feature structure be partitioned coherently and evenly across experts?
```

This requires a middle condition:

```text
globally isotropic but locally structured features
```

This is more language-like than fully spherical randomness, because language features are not arbitrary points on a sphere; they are local patterns / families / slots that may collectively produce a flat spectrum.

---

## 2. Claim hierarchy

### Claim 1: mass

Recursive node-local quantiles give equal probability mass.

Status from V2:

```text
mostly solved
```

Remaining work:

- fix naming;
- tie / atom handling;
- calibration vs holdout separation;
- make it clear that isotropy is not required for this theorem.

### Claim 2: coherence

Routes should preserve latent feature structure when such structure exists.

Status:

```text
not solved by V2 fixed/local baselines
conditioned positive result from expert-guided V2
```

Need to test:

- no-structure isotropic null;
- isotropic local mixture;
- expert-aligned mixture;
- noisy / random expert geometry.

### Claim 3: static utility

A coherent partition should improve a controlled static expert-fitting task only when the target function is feature-dependent.

Status:

```text
not cleanly separated yet
```

Need to test:

- feature-dependent target maps;
- feature-independent target maps;
- frozen route expert fitting;
- balanced assignment as control.

### Removed claim: preservation

Training preservation is explicitly out of v2.2.  Do not include route drift, slow update, hysteresis, dynamic recalibration, or learned-router preservation claims in the main story.

---

## 3. Hypothesis-to-anchor map

Every hypothesis below has a matching negative or boundary anchor.

| ID | Hypothesis | Anchor / falsifier | Primary metrics |
|---|---|---|---|
| H1 | Spectral isotropy alone is insufficient for coherence. | Isotropic Gaussian or spherical features with independent random labels. | NMI, purity near random. |
| H2 | Quantiles are the mass mechanism. | Same directions with non-quantile thresholds should have worse LoadCV. | LoadCV, max error. |
| H3 | Local structure enables coherent static dispatch. | Globally whitened mixture with separated centers. | NMI, purity, within-cell variance. |
| H4 | Local objective fails when structure is absent or too overlapping. | Isotropic unstructured and low-separation mixtures. | NMI collapse, margin low. |
| H5 | Expert guidance helps only when expert weights align with feature geometry. | Random/noisy expert weights should not improve NMI or compatibility. | NMI, cell-prototype alignment. |
| H6 | Spectral normalization causally removes anisotropic confounds. | Compare raw anisotropic distorted features vs whitened features. | covariance condition, NMI, LoadCV. |
| H7 | Static utility requires feature-dependent targets. | Feature-independent target should not reward coherent dispatch. | validation MSE, specialization. |
| H8 | Balanced assignment is not a good feature dispatch. | It has exact mass but low NMI / poor locality. | LoadCV=0, NMI low. |

---

## 4. Research work packages

### WP0: scope reset

Goal:

```text
remove preservation from current paper scope
```

Actions:

- create v2.2 folder;
- rewrite problem statement around static good dispatch;
- replace `equal mass + coherence + preservation` with `equal mass + coherence + static utility`;
- keep preservation only as future work.

Completion criterion:

```text
The abstract, introduction, problem statement, method, and experiment plan contain no preservation claim.
```

### WP1: formalize the feature assumption

Goal:

```text
make spectral isotropy causally relevant without overclaiming it
```

Candidate assumption:

```text
balanced isotropic local mixture
```

Formal version:

```text
F uniform in {1,...,K}
X | F=f = mu_f + epsilon_f
Cov(X) approximately sigma^2 I after centering / whitening
centers or local manifolds are separated
```

Key design decision:

- do not assume full spherical uniformity;
- do not assume arbitrary covariance isotropy;
- assume a feature-like local structure that can be audited.

Completion criterion:

```text
At least one theorem / proposition links projected separation to route-feature coherence.
```

### WP2: define C-SPR method family

Goal:

```text
construct static good dispatch with separated mechanisms
```

Variants:

- C-SPR-RandomAxis: mass-only baseline;
- C-SPR-FixedBasis: deterministic clean mass baseline;
- C-SPR-Local: local feature geometry;
- C-SPR-Expert: expert geometry;
- C-SPR-ExpertLocal: combined geometry.

Implementation requirements:

- node-local quantiles;
- correct fixed-basis implementation;
- sign-invariant projective expert prototypes;
- feature-derived tie handling;
- balanced assignment only as control.

Completion criterion:

```text
Each method has a clear causal role and a matching ablation.
```

### WP3: static experiment anchors

Run anchors in this order:

1. **A0 clean V1 sanity**: spherical features + simplex cells.
2. **A1 isotropic null**: no local structure.
3. **A2 isotropic local mixture**: feature coherence should be possible.
4. **A3 anisotropic distortion**: raw geometry should fail.
5. **A4 whitening recovery**: normalization should recover the local mixture metric.
6. **A5 expert alignment sweep**: aligned / noisy / random expert weights.
7. **A6 static utility**: feature-dependent vs feature-independent tasks.
8. **A7 failure modes**: atoms, ties, unbalanced frequencies, overlapping groups.

Completion criterion:

```text
Every positive result has a matched negative control.
```

### WP4: paper writing

Paper sections:

1. Introduction.
2. Static Good Dispatch Problem.
3. Why Spectral Isotropy Is Not Enough.
4. Isotropic Local Feature Structure.
5. Coherent Spectral Partition Routing.
6. Theory.
7. Experiments.
8. Discussion and Limitations.

Completion criterion:

```text
The paper explicitly states what is solved and what is not solved.
```

### WP5: decision gate

After experiments, decide which claim is supported.

#### Green result

```text
C-SPR-Local / ExpertLocal improves coherence on isotropic local mixtures,
expert guidance helps only when aligned,
whitening recovers performance after anisotropic distortion,
static utility improves only for feature-dependent tasks.
```

Then v2.2 can claim static good dispatch under explicit assumptions.

#### Yellow result

```text
equal mass works, but coherence improves only under expert alignment.
```

Then make expert alignment the central condition and downgrade local-only claims.

#### Red result

```text
coherence does not improve even in controlled isotropic local mixtures.
```

Then the method is only a mass router; revise toward a different partition objective, such as graph-based balanced clustering or supervised / self-supervised feature discovery.

---

## 5. Methodological discipline

The research process should follow this rule:

```text
mechanism -> assumption -> falsifiable anchor -> experiment -> updated claim
```

Do not proceed by adding complexity until the current failure mode is identified.

For each experiment, write before running:

1. what hypothesis it tests;
2. what result would support it;
3. what result would falsify it;
4. which assumption is violated if it fails.

---

## 6. Immediate next actions

1. Implement v2.2 C-SPR code in a separate folder; do not mutate v2 or old v2.1.
2. Run E1/E2/E3 first; do not run training.
3. Build the assumption ladder before any static utility task.
4. Use labels only for evaluation.
5. Insert experimental numbers only after generated tables and figures exist.

---

## 7. Final intended claim

The intended v2.2 claim is:

```text
For globally spectrally isotropic but locally structured route-relevant features,
static good dispatch can be decomposed into mass, coherence, and static utility.
Recursive quantiles provide mass.  Spectral normalization provides the clean metric.
Local or expert-aligned geometry provides coherence when the corresponding assumption holds.
Static utility appears only when the downstream expert task respects the same feature structure.
```

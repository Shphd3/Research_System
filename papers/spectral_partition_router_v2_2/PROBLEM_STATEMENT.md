# V2.2 Problem Statement: Static Feature-Family Dispatch under Spectral Isotropy

## 1. Main question

We close the following static clean-case problem before studying training dynamics:

> Given a route-relevant feature distribution whose aggregate spectrum is isotropic and whose feature families occur with uniform frequency, can we construct a label-free, batch-independent static router that assigns feature families to experts in a balanced and specialization-preserving way?

The target is **feature-family dispatch**, not merely equal token counts.

A valid solution must specify:

```text
controlled feature distribution
definition of good static dispatch
identifiability assumptions
routing mechanism that uses the assumptions causally
matched positive and negative anchors
```

## 2. Scope

This paper addresses the advisor's simplest mathematical case: feature frequency is uniform, the representation spectrum is uniform, and the static dispatch problem is stated, proved, and experimentally audited before moving to non-uniform spectra or real training dynamics.

Out of scope:

```text
training preservation
representation drift
slow router updates
hysteresis
learned-router dynamics
large-singular-value non-uniform spectra
real language-model hidden states
downstream task utility
automatic selection of K
```

## 3. Controlled feature model

Let:

```text
F in {1,...,K}     latent route-relevant feature family
X in R^d           hidden representation / route-relevant feature vector
E                  number of experts
G = g(X)           expert selected by a static router
```

The controlled distribution is:

\[
F \sim \mathrm{Unif}(\{1,\ldots,K\}),
\qquad
X \mid F=k = \mu_k + \epsilon.
\]

Assumptions:

### A1. Frequency uniformity

Each feature family appears with equal probability:

\[
\Pr(F=k)=1/K.
\]

This is the clean-case mass condition.

### A2. Global spectral isotropy

After centering and optional whitening, the aggregate representation is approximately isotropic:

\[
\operatorname{Cov}(\widetilde X) \approx I_d.
\]

This is the clean-case metric condition.  It removes global anisotropic directions but does not create feature identity.

### A3. Local feature recoverability

The feature families are not arbitrary labels.  They leave recoverable local structure in representation space.  For example, there exists an unsupervised estimator \(\widehat h(X)\) such that, up to a permutation of family names,

\[
\Pr(\widehat h(X) \neq F) \leq \eta.
\]

This condition is necessary.  Without it, feature-family dispatch is unidentifiable.

## 4. Why spectral isotropy alone is insufficient

Spectral isotropy is a global second-order condition.  It does not define which examples belong to the same feature family.

Null anchor:

\[
X \sim \mathcal N(0,I_d),
\qquad
F \perp X,
\qquad
F \sim \mathrm{Unif}(\{1,\ldots,K\}).
\]

For any deterministic router \(g(X)\),

\[
I(g(X);F)=0.
\]

Thus no label-free feature-only router can recover feature-family dispatch from isotropy alone.

The solvable middle regime is:

```text
globally isotropic aggregate representation
+ locally recoverable feature families
+ uniform feature-family frequencies
```

## 5. Definition of static good dispatch

A static router \(g:\mathbb R^d\to\{1,\ldots,E\}\) is good in this paper if it satisfies:

### O1. Balanced expert mass

\[
\Pr(g(X)=e) \approx 1/E.
\]

### O2. Feature-family consistency

Each feature family should be routed mostly to one expert:

\[
C_{\mathrm{fam}} = \frac1K\sum_{k=1}^K \max_e \Pr(G=e\mid F=k)
\]

should be high.

### O3. Low feature split rate

A coherent feature family should not be cut into many experts by a mass-balancing rule.

### O4. Informative expert identity

The selected expert should carry information about feature-family identity:

\[
I(G;F)/H(G)
\]

should be high in structured data and near zero in the isotropy-only null.

For `K > E`, ordinary class purity is not a primary metric because one expert must receive multiple feature families.

## 6. Calibration protocol

Allowed during router construction:

```text
calibration features X
feature mean/covariance
unsupervised clustering of X
estimated cluster masses
optional model-internal expert geometry, if explicitly tested
```

Not allowed during router construction:

```text
latent feature labels F
task labels Y
next-token answers
evaluation labels
current-batch expert counts
batch-level forced assignment as the main method
```

Latent labels \(F\) are used only for synthetic data generation, oracle upper bounds, and evaluation.

## 7. Main method target

The method should use the assumptions causally:

```text
spectral normalization
-> clean metric for feature recovery

recoverable local feature families
-> cluster/prototype recovery

uniform family frequencies
-> balanced family-to-expert assignment gives mass balance
```

This leads to:

```text
BFSR: Balanced Feature-Specializing Routing
```

Quantile routing is retained as a mass-only baseline, not as the main causal mechanism.

## 8. Stage completion criterion

This stage is complete if the paper can state:

```text
Under globally spectrally isotropic, frequency-uniform, locally recoverable
feature-family distributions, BFSR constructs balanced static feature-family
dispatch by recovering feature families and assigning them to experts under a
balanced constraint.  When local recoverability is removed, the method fails in
predictable ways.
```

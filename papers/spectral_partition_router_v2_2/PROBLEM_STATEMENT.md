# V2.2 Problem Statement: Static Feature-Level Specialization under Spectral Isotropy

## 1. Main question

We want to close the following static problem before studying training dynamics:

> Given a route-relevant feature distribution whose global spectrum is isotropic and whose feature families occur with uniform frequency, can we construct a non-cheating static router that assigns feature families to experts in a balanced and specialized way?

The target is **feature-level specialization**, not merely equal token counts.

A valid solution should answer four questions:

1. What is the controlled feature distribution?
2. What does "good dispatch" mean in this distribution?
3. Which assumptions make good dispatch identifiable?
4. Which routing mechanism uses those assumptions causally?

## 2. Why this scope

The advisor's clean-case requirement is to first finish the simplest mathematical setting: feature frequency is uniform, the representation spectrum is uniform, and the resulting MoE dispatch problem should be stated, proved, and experimentally audited before moving to non-uniform spectra or real training dynamics.

This paper therefore excludes:

```text
training preservation
representation drift
slow router updates
hysteresis
learned-router dynamics
large-singular-value non-uniform spectrum
```

Those are later-stage problems.

## 3. Controlled feature model

Let

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

The assumptions are:

### A1. Frequency uniformity

Each feature family appears with equal probability:

\[
\Prob(F=k)=1/K.
\]

This is the frequency part of the clean case.

### A2. Global spectral isotropy

After centering and optional population whitening, the aggregate representation is approximately isotropic:

\[
\Cov(\widetilde X) \approx I_d.
\]

This is the spectral part of the clean case. It removes global anisotropic directions and defines a clean metric.

### A3. Local feature recoverability

The feature families are not arbitrary labels. They leave recoverable local structure in representation space. For example, there exists an unsupervised estimator \(\widehat h(X)\) such that

\[
\Prob(\widehat h(X) \neq F) \leq \eta
\]

up to a permutation of feature-family names.

This assumption is necessary. Without it, feature-level specialization is unidentifiable.

### A4. Downstream static utility compatibility

This is not part of the current stage claim. A later static-utility audit may
test whether a downstream objective depends on the feature family. A typical
controlled target is:

\[
Y = a_F^\top X + \xi,
\]

or another family-conditioned rule. If the target is independent of \(F\), then feature specialization should not improve learning. This belongs after the static dispatch definition has been closed.

## 4. Why spectral isotropy alone is not enough

Spectral isotropy is a global second-order condition. It does not define which tokens should be grouped together.

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

Thus no feature-specializing router can be recovered from \(X\). This proves that isotropy alone cannot be the causal source of good routing.

The correct middle regime is:

```text
globally isotropic distribution
+ locally recoverable feature families
+ uniform feature-family frequencies
```

## 5. Definition of static good dispatch

A static router \(g:\R^d\to\{1,\ldots,E\}\) is good in this paper if it satisfies the following objectives.

### O1. Balanced expert mass

\[
\Prob(g(X)=e) \approx 1/E.
\]

This is required, but it is not sufficient.

### O2. Feature-family consistency

Each feature family should be routed consistently:

\[
H(G\mid F) \text{ is small.}
\]

Because \(K\) can be larger than \(E\), one expert may receive several feature families. The primary metric is therefore per-family route consistency, not route-to-feature purity.

### O3. Non-trivial specialization

The router should retain useful information about feature identity:

\[
I(G;F) \text{ is large relative to } H(G).
\]

This prevents solutions that are balanced but feature-agnostic.

### O4. Parked downstream utility

Feature-dependent expert learning is a later optional audit. It is not required for the current static dispatch claim.

## 6. Non-cheating rules

Allowed during router construction:

```text
unlabeled calibration features X
feature mean/covariance
unsupervised clustering of X
model-internal expert weights, if used as an experimental condition
estimated cluster masses
```

Forbidden during router construction:

```text
latent feature labels F
task labels Y
next-token answers
evaluation labels
current-batch expert counts
batch-level forced assignment as the main method
```

Latent labels \(F\) and targets \(Y\) are allowed only for synthetic data generation and evaluation.

## 7. Main method target

The method should use the assumptions causally:

```text
spectral normalization
-> clean metric for feature recovery

recoverable local feature families
-> cluster/prototype recovery

uniform family frequencies
-> balanced family-to-expert assignment gives mass balance

downstream feature-dependent objective
-> optional later static utility audit
```

This leads to the main method family:

```text
BFSR: Balanced Feature-Specializing Routing
```

Quantile routing is retained as a baseline or optional calibration tool, not as the main causal mechanism.

## 8. What this paper should prove or falsify

The paper should prove or experimentally test:

1. **Impossibility anchor**: isotropy without feature recoverability cannot yield feature specialization.
2. **Mass theorem**: if feature families are uniform and assigned evenly to experts, expert mass is balanced.
3. **Robustness theorem**: if feature-family recovery error is at most \(\eta\), then mass and specialization degrade by controlled amounts.
4. **Frequency-uniformity anchor**: equal-number family assignment balances expert mass only when feature-family frequencies are uniform; mass-aware assignment is needed when frequencies are non-uniform.
5. **Negative controls**: random routing and quantile-only dispatch can balance usage or route ordinary geometry without solving feature-family consistency.

## 9. Stage completion criterion

This stage is complete when we can state:

```text
Under globally spectrally isotropic, frequency-uniform, locally recoverable feature-family distributions, a static non-cheating router can achieve balanced feature-level specialization by recovering feature families and assigning them evenly to experts.
When local recoverability or feature-frequency uniformity is removed, the method fails in predictable ways.
```

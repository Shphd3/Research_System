# V2.2 Method and Theory Notes

## 1. Research object

V2.2 studies **static feature-level specialization** under a clean controlled regime:

```text
feature-family frequencies are uniform
global representation spectrum is isotropic
local feature families are recoverable
router is fixed before expert training
```

It does not study training preservation.

## 2. Why the main method should not be quantile-first

Recursive quantile routing is a strong mechanism for equal mass. However, in the current problem it is not the most causal method.

The new target is not simply:

```text
make each expert receive 1/E probability mass
```

The new target is:

```text
make each expert specialize on coherent feature families,
while keeping expert mass balanced.
```

If feature families are frequency-uniform, then the natural mass mechanism is **balanced assignment of feature families to experts**. This uses the given condition directly:

```text
uniform family frequencies
+ equal number or equal total mass of families per expert
-> balanced expert usage
```

Quantile routing may split a feature family across a threshold. That can produce balanced counts while damaging specialization. Therefore quantile-only routing is best treated as a baseline or fallback, not as the main method.

## 3. Main method: BFSR

Name:

```text
BFSR: Balanced Feature-Specializing Routing
```

Purpose:

```text
recover feature families in a spectrally normalized metric,
then assign recovered families to experts under a balanced constraint.
```

### 3.1 Inputs

Calibration features:

\[
\{x_i\}_{i=1}^n \subset \R^d.
\]

Number of experts:

\[
E.
\]

Number of feature families:

\[
K.
\]

In controlled experiments \(K\) is known from data construction. Later experiments may estimate \(K\), but this is not necessary for the first clean case.

Optional expert-side geometry:

\[
\{w_e\}_{e=1}^E
\]

or expert spectral prototypes.

### 3.2 Step 1: spectral normalization

Estimate feature mean and covariance on calibration data:

\[
\widehat \mu = \frac{1}{n}\sum_i x_i,
\qquad
\widehat \Sigma = \frac{1}{n}\sum_i (x_i-\widehat\mu)(x_i-\widehat\mu)^\top.
\]

Normalize:

\[
\widetilde x_i = (\widehat\Sigma + \lambda I)^{-1/2}(x_i-\widehat\mu).
\]

This step is not a mass guarantee. It repairs the metric so that high-variance directions do not dominate feature recovery.

### 3.3 Step 2: recover feature families

Run unsupervised clustering in normalized space:

\[
\widehat h:\R^d\to\{1,\ldots,K\}.
\]

Possible implementations:

```text
spherical k-means
Gaussian mixture model with shared covariance
spectral clustering on a nearest-neighbor graph
nearest-prototype assignment from recovered centers
```

The first implementation should use spherical k-means or standard k-means after whitening, because the controlled feature family is center-based.

### 3.4 Step 3: estimate recovered family mass

For each recovered family \(c\), estimate:

\[
\widehat p_c = \frac{1}{n}\sum_i \mathbf 1\{\widehat h(\widetilde x_i)=c\}.
\]

In the ideal clean case, \(\widehat p_c \approx 1/K\).

### 3.5 Step 4: assign feature families to experts

Find an assignment

\[
a:\{1,\ldots,K\}\to\{1,\ldots,E\}
\]

such that each expert receives equal recovered family mass:

\[
\sum_{c:a(c)=e}\widehat p_c \approx 1/E.
\]

Possible objectives:

#### Unsupervised locality objective

Group related feature families together:

\[
\min_a \sum_{e=1}^E \sum_{c:a(c)=e} \widehat p_c
\left\|\widehat\mu_c - \bar \mu_e\right\|^2
\]

subject to balanced recovered mass.

#### Expert-aligned objective

If expert-side prototypes \(u_e\) exist, assign feature families to compatible experts:

\[
\max_a \sum_{c=1}^K \widehat p_c
\langle \widehat\mu_c, u_{a(c)}\rangle
\]

subject to balanced recovered mass.

For sign-ambiguous spectral prototypes, use projective similarity:

\[
P_c = \frac{\widehat\mu_c \widehat\mu_c^\top}{\|\widehat\mu_c\|^2},
\qquad
P_e = u_e u_e^\top,
\qquad
s(c,e)=\mathrm{tr}(P_cP_e).
\]

### 3.6 Step 5: route new tokens

For a new token feature \(x\):

```text
normalize x -> x_tilde
recover family c_hat = h_hat(x_tilde)
route to expert g(x) = a(c_hat)
```

This gives a fixed non-cheating router.

## 4. Method variants

### BFSR-OracleFeature

Uses true feature family \(F\) to build the family-to-expert assignment.

Purpose: upper bound / sanity check only. Not a valid non-cheating method.

### BFSR-Cluster

Uses unsupervised recovered feature family \(\widehat h(X)\). This is the primary non-cheating method.

### BFSR-ExpertAligned

Uses recovered feature families plus expert-side geometry to assign families to experts.

Purpose: test whether model-internal expert geometry can give feature-to-expert identity.

### BFSR-RandomGroup

Assigns recovered feature families to experts uniformly subject to the same balance constraint.

Purpose: tests whether feature recovery alone is enough or whether assignment geometry matters.

### Quantile-SPR baseline

Uses projection quantiles to equalize mass.

Purpose: shows that equal mass can be achieved without feature-level specialization.

### BalancedAssignment control

Forces equal counts inside the current batch.

Purpose: negative control. It is not a valid feature-distribution router because it uses current-batch counts.

## 5. Theory components

### Theorem 1: Isotropy-alone non-identifiability

Let

\[
X\sim\mathcal N(0,I_d),
\qquad F\sim\mathrm{Unif}(\{1,\ldots,K\}),
\qquad F\perp X.
\]

For any deterministic router \(g(X)\),

\[
I(g(X);F)=0.
\]

Therefore spectral isotropy alone cannot imply feature specialization.

Proof sketch: since \(g(X)\) is measurable with respect to \(X\), and \(F\perp X\), we have \(F\perp g(X)\).

### Theorem 2: Balanced family assignment gives balanced expert mass

Assume:

1. \(F\sim\mathrm{Unif}(\{1,\ldots,K\})\).
2. \(K\) is divisible by \(E\).
3. The router assigns exactly \(K/E\) feature families to each expert.
4. The router is feature-consistent: \(g(X)=a(F)\).

Then

\[
\Prob(g(X)=e)=1/E
\]

for every expert \(e\).

Proof:

\[
\Prob(g(X)=e)
=\sum_{k:a(k)=e}\Prob(F=k)
=\frac{K/E}{K}
=\frac1E.
\]

### Theorem 3: Robust mass under feature recovery error

Assume the ideal feature assignment \(a(F)\) is balanced, and the recovered family predictor satisfies

\[
\Prob(\widehat h(X)\neq F)\leq\eta.
\]

Define

\[
g(X)=a(\widehat h(X)).
\]

Then for each expert \(e\),

\[
\left|\Prob(g(X)=e)-1/E\right|\leq \eta.
\]

Proof sketch: \(g(X)\neq a(F)\) can happen only when \(\widehat h(X)\neq F\). Total variation between the expert distribution induced by \(a(F)\) and \(a(\widehat h(X))\) is at most \(\eta\).

### Theorem 4: Specialization under feature recovery

Under the same condition,

\[
\Prob(G \neq a(F))\leq\eta.
\]

Therefore feature-family consistency degrades at most with feature recovery error. Standard Fano-type bounds can translate this into lower bounds on mutual information or upper bounds on conditional entropy.

### Downstream proposition: static utility requires feature-dependent target

If

\[
Y\perp F\mid X
\]

and the expert class has no feature-conditioned advantage, then feature-family dispatch should not improve Bayes risk over a sufficiently expressive shared model.

If instead

\[
Y = a_F^\top X + \xi
\]

and experts have limited capacity, then routing by \(F\) can reduce approximation error relative to incoherent partitions that mix many different \(a_F\)'s inside each expert.

This proposition is parked for a downstream optional utility audit. It is not part of the current static dispatch claim.

## 6. Causal map

```text
A1: uniform feature-family frequency
    -> mass balance through equal family/mass assignment

A2: spectral isotropy / whitening
    -> clean metric for feature recovery and expert geometry

A3: local feature recoverability
    -> high route-feature mutual information

A4: feature-dependent target or aligned expert geometry
    -> downstream utility / expert-identity audit, not current-stage evidence
```

Each assumption has a falsifying anchor:

```text
remove A1 -> mass imbalance unless assignment uses estimated masses
remove A2 -> anisotropic confound dominates clustering
remove A3 -> specialization impossible
remove A4 -> no downstream utility expected, but the static dispatch claim is unchanged
```

## 7. What to avoid claiming

Do not claim:

```text
spectral isotropy alone gives good routing
quantile balancing gives feature specialization
load balance implies expert specialization
static dispatch solves training preservation
synthetic utility proves real LLM utility
```

Do claim, if supported:

```text
in globally isotropic, frequency-uniform, locally recoverable feature distributions,
BFSR achieves balanced static feature-level specialization
by recovering feature families and assigning them to experts under a balanced constraint.
```

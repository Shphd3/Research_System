# V2.2 Method and Theory Notes

## 1. Research object

V2.2 studies **static feature-family dispatch** under a clean controlled regime:

```text
feature-family frequencies are uniform
global representation spectrum is isotropic
local feature families are recoverable
router is fixed after calibration
```

It does not study training preservation or downstream task utility.

## 2. Why quantile routing is not the main method

Recursive quantile routing is a strong mechanism for equal mass.  It is not the most causal mechanism for V2.2 because the target is not simply:

```text
make each expert receive 1/E probability mass
```

The target is:

```text
keep feature families intact while assigning a balanced collection of families to experts
```

If feature-family frequencies are uniform, the natural mass mechanism is:

```text
uniform family frequencies
+ equal number of families per expert
-> balanced expert usage
```

Quantile routing may cut through one feature family.  It therefore remains a mass-only baseline.

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

### Step 1: spectral normalization

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

This is metric repair, not a mass guarantee.

### Step 2: recover feature families

Run unsupervised clustering in normalized space:

\[
\widehat h:\mathbb R^d\to\{1,\ldots,K\}.
\]

The first implementation uses k-means with known \(K\) in the controlled synthetic suite.

### Step 3: estimate recovered family mass

For each recovered family \(c\), estimate:

\[
\widehat p_c = \frac{1}{n}\sum_i \mathbf 1\{\widehat h(\widetilde x_i)=c\}.
\]

### Step 4: assign recovered families to experts

Find an assignment

\[
a:\{1,\ldots,K\}\to\{1,\ldots,E\}
\]

such that each expert receives equal recovered family mass:

\[
\sum_{c:a(c)=e}\widehat p_c \approx 1/E.
\]

In the clean uniform-frequency case, equal-number assignment is sufficient when \(K\) is divisible by \(E\).  Under frequency imbalance, mass-aware assignment is required.

### Step 5: route new examples

For a new feature \(x\):

```text
normalize x -> x_tilde
recover family c_hat = h_hat(x_tilde)
route to expert g(x) = a(c_hat)
```

## 4. Method variants

### BFSR-Cluster

Uses recovered feature families from clustering.  This is the primary label-free method.

### OracleFeature

Uses true feature labels during construction.  This is a non-admissible upper bound.

### Quantile-SPR

Uses projection quantiles to equalize mass.  This is a baseline for showing that mass balance is not feature-family dispatch.

### Random linear top-1

Ordinary static router baseline.

### BalancedAssignment

Forces equal counts inside the current batch.  It is excluded from main tables because it is not a fixed distributional router.

## 5. Theory components

### Theorem 1: isotropy-alone non-identifiability

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

Therefore spectral isotropy alone cannot imply feature-family dispatch.

### Theorem 2: balanced family assignment gives balanced expert mass

Assume:

```text
F is uniform over K feature families
K is divisible by E
each expert receives K/E families
routes are feature-consistent: g(X)=a(F)
```

Then

\[
\Pr(g(X)=e)=1/E.
\]

### Theorem 3: robust mass under feature recovery error

After aligning recovered family ids with true family ids, suppose

\[
\Pr(\widehat h(X)\neq F)\leq\eta.
\]

If \(g(X)=a(\widehat h(X))\) and \(a(F)\) is balanced, then

\[
\left|\Pr(g(X)=e)-1/E\right|\leq \eta.
\]

### Theorem 4: specialization under feature recovery

Under the same condition,

\[
\Pr(G \neq a(F))\leq\eta.
\]

Thus feature-family dispatch degrades with feature recovery error.

## 6. Causal map

```text
A1: uniform feature-family frequency
    -> equal-number family assignment gives mass balance

A2: spectral isotropy / whitening
    -> clean metric for feature recovery

A3: local feature recoverability
    -> high family consistency and information fraction
```

Each assumption has a falsifying anchor:

```text
remove A1 -> equal-number assignment loses mass balance
remove A2 -> anisotropic distortion harms clustering until whitening
remove A3 -> isotropy-only null has near-zero information fraction
```

## 7. Valid claim

If the experiments support the assumptions, the valid claim is:

```text
In globally isotropic, frequency-uniform, locally recoverable feature-family
distributions, BFSR achieves balanced static feature-family dispatch by recovering
families and assigning them to experts under a balanced constraint.
```

Do not claim downstream learning improvement, learned-router superiority, route preservation, real hidden-state applicability, or automatic K selection from the current V2.2 results.

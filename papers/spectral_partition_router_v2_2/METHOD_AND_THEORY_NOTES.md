# V2.2 Method and Theory Notes

## 1. Research object

V2.2 studies static good dispatch, not training preservation.

The target is a non-cheating router that produces cells with:

```text
equal probability mass
feature coherence
static expert compatibility / controlled utility
```

The central correction from V2 is:

```text
quantiles alone solve mass, not feature meaning.
spectral isotropy alone cleans geometry, but does not create feature meaning.
local feature structure or expert alignment is needed for coherent dispatch.
```

## 2. Method name

Use the working name:

```text
C-SPR: Coherent Spectral Partition Routing
```

C-SPR is a static router family.  It keeps the recursive quantile mass layer from SPR, but changes the scientific claim:

```text
Mass comes from quantiles.
Coherence comes from split-direction selection under local structure.
Expert compatibility comes from optional expert-weight geometry.
```

## 3. Feature setting

Let `X in R^d` be the route-relevant feature.  The controlled representation is:

```text
tilde X = B(X - mu)
Cov(tilde X) approximately sigma^2 I
```

The useful middle regime is:

```text
F ~ Uniform({1,...,K})
tilde X | F=f = mu_f + epsilon
```

where the global covariance is isotropic but the distribution has local structure.

This is different from a fully spherical feature distribution.  A spherical Gaussian has no recoverable discrete feature identity unless one is injected independently, in which case no unsupervised router should recover it.

## 4. Static good dispatch definition

A router `g` induces cells:

```text
C_e = {x : g(x)=e}
```

### 4.1 Equal mass

```text
P(C_e)=1/E
```

### 4.2 Feature coherence

When latent feature labels `F` exist for evaluation:

```text
NMI(g(X), F) high
purity high
within-cell variance low
cell-center separation high
```

### 4.3 Expert compatibility

When expert weights provide model-internal geometry, cell geometry should align with expert geometry:

```text
cell-prototype alignment high
cell-to-expert assignment stable under sign-invariant prototype representation
```

### 4.4 Static utility

For a controlled static expert-fitting task:

```text
Y = A_F X + noise
```

with `F` hidden from the router, a coherent route should improve frozen-route expert fitting relative to incoherent equal-mass routes.

## 5. C-SPR construction

### Step 1: spectral normalization

Estimate `mu` and a spectral normalization matrix `B` from unlabeled calibration features.

Options:

```text
identity if already isotropic
whitening
spectral shrinkage
rank-clipped whitening for numerical stability
```

Report covariance condition number and effective rank before and after normalization.

### Step 2: recursive mass tree

At node `N`, with expert set `E_N`, split experts into `E_L` and `E_R` and set:

```text
rho_N = |E_L| / |E_N|
```

Given a direction `q_N`, split by the node-local quantile:

```text
q_N^T tilde X <= tau_N
```

where `tau_N` is the `rho_N` quantile of the node projection.

### Step 3: choose split directions for coherence

The method should compare several direction policies.

#### C-SPR-RandomAxis

Seeded random axes.  This is a mass-only baseline.

#### C-SPR-FixedBasis

A deterministic orthogonal / coordinate / Hadamard basis.  This is a stronger clean baseline than random axes.

#### C-SPR-Local

Choose directions using unlabeled feature geometry.  For candidate directions `q`, compute the quantile split and score:

```text
J_local(q) = - within_cell_variance(q) + eta * margin_tail(q)
```

where `margin_tail(q)` penalizes thresholds through high-density regions.

#### C-SPR-Expert

Use expert weights only as model-internal geometry.  For each expert matrix `W_e`, define a sign-invariant spectral projector:

```text
v_e = top left singular vector of W_e
P_e = v_e v_e^T
```

Group experts using projective distance:

```text
d(e,j) = 1 - trace(P_e P_j) = 1 - (v_e^T v_j)^2
```

Then choose feature split directions that align resulting cells with the two expert subspace groups.

#### C-SPR-ExpertLocal

Combine expert guidance and local feature geometry:

```text
J(q) = - L_local(q) + lambda * Align_expert(q) + eta * Margin(q)
```

The quantile threshold still provides mass.

## 6. Theory hierarchy

### Theorem 1: recursive quantile equal mass

If every internal node splits feature probability mass in proportion to the number of experts assigned to its children, every leaf cell has probability mass `1/E`.

This theorem does not require spectral isotropy.  It is the mass theorem.

### Proposition 2: isotropy-alone non-identifiability

If `X` is isotropic and has no feature-dependent structure, then no unlabeled geometric router can recover meaningful feature labels.  If an evaluation label `F` is independent of `X`, then `I(g(X);F)=0` for every deterministic router `g`.

This is the null anchor: isotropy alone should not produce feature coherence.

### Assumption 3: isotropic local mixture

At a node, suppose the feature population contains two latent groups `G in {L,R}` with the target mass ratio, and there exists a direction `q*` and threshold `tau*` such that the projected tails are small:

```text
P(q*^T X > tau* | G=L) <= epsilon
P(q*^T X <= tau* | G=R) <= epsilon
```

### Proposition 4: projected separation gives coherent split

Under the above projected separation, the node split disagrees with the latent binary grouping with probability at most `epsilon`.

For a tree, total route-feature error is bounded by the accumulated node errors along the path.

### Proposition 5: expert alignment transfers coherence

If an expert-derived direction `q` is within `delta` of an ideal separating direction `q*`, and `||X|| <= R`, then the split can disagree with the ideal split only on samples whose ideal margin is at most `delta R`.

Therefore expert weights help only if they are aligned with feature-separating directions and the feature distribution has low boundary mass around the ideal threshold.

### Proposition 6: spectral normalization is a confound-removal step

In an elliptically distorted local mixture:

```text
X = A Z
```

where `Z` is an isotropic local mixture and `A` has large condition number, raw Euclidean / inner-product geometry is dominated by `A`.  Population whitening recovers the geometry of `Z` up to an orthogonal transform.  Thus spectral normalization can causally improve local partition quality by restoring the metric in which local structure is expressed.

This proposition is the correct causal role of spectral isotropy: it repairs or defines the metric, not the mass guarantee.

## 7. Why this answers the advisor's clean-case request

The advisor asked for the simplest case where:

```text
feature frequency is uniform
representation / spectral space is uniform
```

V2.2 makes this precise as:

```text
balanced latent feature families
spectrally normalized global covariance
local feature structure in the normalized space
```

This is a better static target than arbitrary covariance isotropy because it is both close to feature-like language assumptions and falsifiable.

## 8. Claim boundary

Allowed claims after successful experiments:

- C-SPR constructs equal-mass cells by quantile calibration.
- Spectral normalization removes anisotropic metric confounds.
- Local or expert-aligned split directions improve feature coherence when local structure exists.
- Expert guidance helps only when expert weights are aligned with feature geometry.
- Static utility improves only when the task or expert geometry is feature-dependent.

Forbidden claims:

- spectral isotropy alone gives good routing;
- equal mass implies feature coherence;
- random expert weights create useful partitions;
- static good dispatch solves training preservation;
- controlled synthetic tasks establish real LLM routing utility.

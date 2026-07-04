# Spectral Partition Routing: Method Learning Guide

This guide explains the v2 method from first principles. It is written for auditing the paper, the implementation, and future experiments.

---

## 1. What problem are we solving?

We are not starting from ordinary MoE load balancing. We are defining and solving a more specific construction problem:

> Given unlabeled route-relevant features in a spectrally uniform representation space, construct a router that partitions the feature distribution uniformly across experts without labels or batch-level capacity forcing.

Let

\[
X\in\mathbb{R}^d
\]

be the hidden feature that should be routed, and let there be `E` experts. A router is a function

\[
g:\mathbb{R}^d\rightarrow\{1,\ldots,E\}.
\]

The router induces feature cells

\[
C_e=\{x:g(x)=e\}.
\]

The target is

\[
P(C_e)=P(g(X)=e)=1/E.
\]

This is **uniform feature dispatch**.

---

## 2. What does non-cheating mean?

A method is non-cheating if it constructs and applies the router without using information that directly tells it the desired assignment.

Allowed:

- unlabeled route-relevant features;
- feature mean and covariance;
- projection quantiles;
- unsupervised locality objectives;
- model-internal expert weights;
- expert spectral prototypes from SVD or power iteration.

Forbidden:

- feature labels during router construction;
- task labels or next-token answers during router construction;
- evaluation labels during router construction;
- current-batch expert counts;
- post-hoc assignment to underfilled experts as the main method.

Key distinction:

```text
Allowed: estimate thresholds once from unlabeled calibration features, then route each new feature independently.
Forbidden: inspect the current batch and force each expert to receive N/E examples.
```

---

## 3. Why not just use load balancing?

Load balancing asks whether the count of routed tokens is uniform in a finite batch. A capacity assignment can force this:

\[
\sum_i A_{ie}=N/E.
\]

But this does not define a stable feature-space partition. It may send nearby or identical features to different experts only because an expert has remaining capacity.

Uniform feature dispatch instead asks for a fixed feature function:

\[
g(x)
\]

so that each cell has equal probability mass under the feature distribution.

---

## 4. Why quantiles solve the equal-mass part

Start with a one-dimensional scalar random variable

\[
T\in\mathbb{R}.
\]

Let its CDF be

\[
F(t)=P(T\le t).
\]

The `rho`-quantile is

\[
\tau=F^{-1}(\rho).
\]

If `F` is continuous, then

\[
P(T\le \tau)=\rho.
\]

So a threshold at a quantile controls the exact probability mass on each side.

For high-dimensional features, choose a direction

\[
q\in\mathbb{S}^{d-1}
\]

and project

\[
T=q^\top X.
\]

Then a quantile threshold on `T` gives a prescribed-mass split of the high-dimensional feature distribution.

---

## 5. The recursive partition idea

A single quantile split creates two cells. To get `E` experts, build a tree.

At a node `N`, suppose the node owns:

- a feature subpopulation `P_N`;
- a set of experts `E_N`.

Split the experts into two groups:

\[
\mathcal{E}_L,\mathcal{E}_R.
\]

The left probability mass should be proportional to the number of experts on the left:

\[
\rho_N=\frac{|\mathcal{E}_L|}{|\mathcal{E}_L|+|\mathcal{E}_R|}.
\]

Choose a split direction

\[
q_N.
\]

Project node features:

\[
T_N=q_N^\top X.
\]

Set threshold

\[
\tau_N=F_N^{-1}(\rho_N).
\]

Then split:

\[
C_L=\{x:q_N^\top x\le \tau_N\},
\]

\[
C_R=\{x:q_N^\top x>\tau_N\}.
\]

Repeat until each leaf has one expert.

If each node split has the correct mass, then every final leaf has mass `1/E`.

---

## 6. What does spectral uniformity do?

Spectral uniformity means that after centering and optional normalization,

\[
\mathrm{Cov}(X)\approx \sigma^2 I.
\]

This means there is no dominant high-variance direction.

Important:

```text
Quantile routing does not mathematically require spectral uniformity.
```

Quantiles can equalize mass for many distributions. In this project, spectral uniformity is the controlled feature setting requested by the research problem. It removes anisotropy as a confound and gives a clean space in which to study feature dispatch.

Correct interpretation:

```text
Spectral uniformity defines the controlled representation regime.
Quantile thresholds provide equal-mass dispatch.
Split directions determine geometry and expert alignment.
```

---

## 7. How do we choose the split direction q?

The quantile threshold controls probability mass. The direction `q` controls what kind of feature geometry the split captures.

### 7.1 SPR-Fixed

Use predetermined directions, such as:

- fixed random orthogonal axes;
- Hadamard-like axes;
- Fourier-like axes.

This is the cleanest construction. It is deterministic and does not depend on labels or expert weights.

Strength:

- simple;
- easy to audit;
- pure non-cheating construction.

Weakness:

- may create slab-like cells with weak feature locality.

### 7.2 SPR-Local

Choose `q` using unlabeled feature geometry. A practical approach:

1. sample many candidate directions;
2. compute the quantile split for each;
3. calculate within-cell variance;
4. choose the direction that minimizes within-cell variance.

Objective:

\[
\mathcal{L}_{local}(q)
=\sum_{b\in\{L,R\}}P(C_b)\,\mathbb{E}[\|X-\mu_b\|^2\mid X\in C_b].
\]

This is still non-cheating because it uses no labels.

### 7.3 SPR-Expert

Use expert weights to guide the partition.

For expert matrix `W_e`, define its input-side spectral prototype:

\[
v_e\in\arg\max_{\|v\|=1}\|v^\top W_e\|_2^2.
\]

This is the top eigenvector of

\[
W_eW_e^\top.
\]

At a tree node, split expert prototypes into two groups. Then choose a feature split direction from the difference between the group prototypes.

Simple signed-vector version:

\[
q_N=\frac{\bar v_L-\bar v_R}{\|\bar v_L-\bar v_R\|}.
\]

However, SVD directions have sign ambiguity. A more robust implementation should use either:

1. router-row inherited signs;
2. deterministic orientation by a fixed anchor;
3. sign-invariant projective prototypes
   \[
   P_e=v_ev_e^\top.
   \]

For exact SVD prototypes from expert weights alone, the projective approach is preferred.

---

## 8. Why expert weights are allowed

Expert weights are part of the model, not labels. They can tell us something about expert identity or expert geometry.

Expert weights should be interpreted as a source of split directions, not as a replacement for quantile calibration.

Key separation:

```text
Expert weights choose geometry.
Quantiles guarantee mass.
```

If expert weights are poorly spread or uninformative, SPR-Expert may produce low-quality geometry, but the quantile thresholds still provide equal-mass cells on the calibration distribution.

---

## 9. Continuous vs discrete features

The clean theorem assumes that the scalar projection

\[
T=q^\top X
\]

has a continuous CDF.

If the distribution is discrete, exact deterministic splitting may be impossible at some thresholds.

Example problem:

- many identical features have exactly the same projection value;
- the target quantile threshold falls inside this atom;
- a deterministic feature-only router must send identical features to the same side;
- exact mass may be impossible.

Solutions:

1. Use feature-derived tie-breaking keys, such as lexicographic projections:
   \[
   (q_1^\top x,q_2^\top x,\ldots,q_L^\top x).
   \]
2. Accept approximate mass and report atom/tie error.
3. Allow stochastic tie-breaking, but then the router is no longer deterministic.
4. If a single atom has probability greater than `1/E`, exact deterministic uniform dispatch is impossible without splitting identical features.

This must be handled explicitly in implementation and experiments.

---

## 10. How SPR is used in training

### 10.1 Frozen-SPR

Calibrate the tree once and keep it fixed.

Use when testing whether a stable equal-mass feature partition is useful.

### 10.2 SPR-init-linear

Use SPR to initialize a standard linear router.

For each leaf expert, compute cell center:

\[
c_e=\mathbb{E}[X\mid g_{SPR}(X)=e].
\]

Initialize router row:

\[
r_e=\frac{c_e}{\|c_e\|}.
\]

Then train the linear top-1 router normally.

This tests whether a learned router can preserve an SPR-discovered partition.

### 10.3 SlowUpdate-SPR

Periodically recalibrate thresholds using moving-window features.

This tests whether SPR can handle representation drift.

---

## 11. What should experiments prove?

The experiments should be organized by claim.

### Claim 1: Equal-mass dispatch

Question:

```text
Can SPR make P(g(X)=e) close to 1/E on calibration and holdout features?
```

Metrics:

- calibration LoadCV;
- holdout LoadCV;
- max absolute usage error;
- calibration-to-holdout gap.

### Claim 2: Robustness beyond spherical features

Question:

```text
If covariance is flat but directions are not spherical, do prototype routers fail while SPR still balances mass?
```

Metrics:

- covariance condition number;
- effective rank;
- LoadCV by method.

### Claim 3: Expert-weight guidance

Question:

```text
Can expert weights guide feature cells without replacing quantile mass control?
```

Metrics:

- expert prototype spread;
- router-expert alignment;
- LoadCV;
- margin;
- leaf/prototype-group agreement.

### Claim 4: Feature partition quality

Question:

```text
Does the partition preserve latent feature groups, when such groups exist in synthetic data?
```

Metrics:

- route-feature NMI;
- feature purity;
- within-cell variance;
- margin p05.

Labels may be used only for evaluation.

### Claim 5: Training preservation

Question:

```text
Does a calibrated feature partition survive controlled MoE training?
```

Metrics:

- training loss;
- validation loss;
- route flip rate;
- margin p05;
- route-feature NMI over time;
- representation drift.

---

## 12. Key implementation invariants

A correct SPR implementation must satisfy:

1. Quantiles are computed within each node, not globally.
2. Node split ratios follow child expert counts.
3. Prediction uses stored thresholds only.
4. Holdout data are never used to recalibrate thresholds.
5. Labels are never used during fitting.
6. Expert weights are used only for direction/grouping, not for per-batch balancing.
7. Tie handling is deterministic and feature-derived, or the impossibility is reported.
8. Expert SVD sign ambiguity is handled.
9. Balanced assignment is never reported as the main method.
10. Calibration and holdout metrics are reported separately.

---

## 13. What the method does not claim

SPR does not claim:

- to discover semantic experts in general;
- to improve downstream performance automatically;
- to solve arbitrary nonuniform hidden representations;
- to make standard linear routers preserve partitions during training;
- to make expert weights alone sufficient for uniform dispatch.

SPR claims:

```text
Given a calibration feature distribution, recursive quantile partitioning constructs equal-mass feature cells without labels or batch-level capacity forcing.
```

Everything beyond that must be tested experimentally.

---

## 14. One-sentence summary

Spectral Partition Routing separates the problem into three parts:

```text
quantiles give uniform mass;
split directions give geometry;
training margins decide preservation.
```

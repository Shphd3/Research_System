# Experiment Plan: Spectral Partition Router v2

## 0. Research question

Given unlabeled route-relevant features in a spectrally uniform representation space, can we construct a practical router that partitions the feature distribution uniformly across experts without labels or batch-level capacity forcing?

The central object is a fixed router

\[
g: \mathbb{R}^d \rightarrow \{1,\ldots,E\}
\]

with induced feature cells

\[
C_e = \{x:g(x)=e\}
\]

and target

\[
P(C_e)=1/E.
\]

## 1. Non-cheating rule

Allowed:

- unlabeled calibration features;
- feature mean and covariance;
- projection quantiles;
- unsupervised locality objectives;
- model-internal expert weights;
- expert spectral prototypes from SVD or power iteration.

Forbidden:

- feature labels during router construction;
- task targets during router construction;
- evaluation labels during router construction;
- current-batch expert counts;
- balanced assignment as the main method.

Balanced assignment may appear only as a forced-count control.

---

## 1.1 Executed full-run configuration

The current paper results are produced by the completed V2 full run, not by
`--quick` smoke tests.  Every generated `metrics.csv` contains
`run_mode=full`.

- E1: five seeds; Gaussian and spherical data; `d in {32, 64}`;
  `E in {4, 8}`; `n_cal in {2048, 8192, 16384}`; `n_holdout = 8192`.
- E2: five seeds; axis-jitter, sparse-mixture, and paired-direction data;
  `d = 64`; `E in {4, 8}`; `n_cal = n_holdout = 8192`.
- E3: five seeds; `d = 64`; `E = 8`; random, symmetric, and clustered expert
  initializations; SVD and one-step MPI prototype extraction.
- E4: five seeds; `d = 64`; `E = 8`; weak, medium, and strong latent-feature
  regimes; evaluation labels are hidden from router construction.
- E5: five seeds; `d = 32`; `E = 8`; hard-routed linear experts trained for
  80 epochs on the controlled class-conditioned regression task.
- E6: five seeds; calibration-size, expert-count, dimension, direction-policy,
  whitening, expert-quality, count-control, and feature-drift ablations.

Paper-facing outputs are generated under:

```text
exp/results/e*/metrics.csv
exp/results/e*/summary.md
latex/figures/
latex/tables/
```

---

## 2. Routers to implement

### 2.1 Vanilla linear top-1

Random linear router rows:

\[
a(x)=\arg\max_e r_e^\top x.
\]

This is the standard baseline.

### 2.2 Linear + load-balancing loss

Use standard top-1 routing with a load-balancing auxiliary term during training. This distinguishes feature partition from ordinary MoE load balancing.

### 2.3 Simplex prototype router

Use regular-simplex rows when `E <= d+1`:

\[
a(x)=\arg\max_e u_e^\top x.
\]

This is a fixed geometric baseline.  It is useful when the data geometry happens
to align with the simplex axes, but it has no quantile mass guarantee.

### 2.4 SPR-Fixed

Build a recursive quantile tree using fixed directions, such as fixed random orthogonal axes or Hadamard-like axes.

At node `n`:

1. Select fixed direction `q_n`.
2. Compute projections `t = X_node @ q_n`.
3. Split at the empirical quantile matching left/right expert count ratio.
4. Recurse until one expert per leaf.

### 2.5 SPR-Local

At node `n`:

1. Sample candidate directions.
2. For each direction, compute the quantile split.
3. Score the split by weighted within-cell variance.
4. Use the best direction.

This is unsupervised and uses no labels.

### 2.6 SPR-Expert

At node `n`:

1. Compute expert spectral prototype for each expert:
   \[
   v_e = \arg\max_{\|v\|=1}\|v^\top W_e\|_2^2.
   \]
2. Split expert prototypes into left/right groups.
3. Let
   \[
   q_n = \frac{\bar v_L - \bar v_R}{\|\bar v_L - \bar v_R\|}.
   \]
4. Split features by the quantile of `X_node @ q_n` matching the expert group sizes.

Important: expert weights choose geometry; quantiles guarantee mass.

### 2.7 Frozen-SPR

Use calibrated SPR tree throughout training.

### 2.8 SPR-init-linear

Use SPR cell centers to initialize a standard linear router:

\[
r_e = \frac{c_e}{\|c_e\|},\quad c_e = \mathbb{E}[X\mid g_{SPR}(X)=e].
\]

Then train the linear router normally.

### 2.9 SlowUpdate-SPR

Recalibrate thresholds and optionally directions every `T` steps using an unlabeled moving window.

---

## 3. Experiment A: Static equal-mass dispatch

### Goal

Verify that SPR constructs equal-mass feature cells and generalizes from calibration to holdout.

### Data

- Gaussian: `X ~ N(0, I_d)`.
- Spherical: sample Gaussian and normalize to unit sphere.

Suggested sweep:

```text
d in {16, 64, 256}
E in {4, 8, 16}
n_cal in {1_000, 10_000, 100_000}
n_holdout = 100_000
seeds = 5
```

### Methods

- vanilla linear top-1;
- simplex prototype;
- SPR-Fixed;
- SPR-Local;
- SPR-Expert with synthetic random experts;
- balanced assignment control.

### Metrics

- calibration LoadCV;
- holdout LoadCV;
- maximum absolute usage error;
- max/min load ratio;
- calibration-to-holdout gap;
- margin p05.

### Expected outcomes

- SPR methods should be exactly or nearly balanced on calibration and close on holdout.
- Vanilla random linear router should show seed-level geometry variance.
- Balanced assignment should be exact on the routed batch but is marked as forced-count control.

---

## 4. Experiment B: Spectrally flat but non-spherical features

### Goal

Show that covariance flatness alone does not make fixed prototype routers reliable, while SPR still gives equal-mass dispatch.

### Data

Use distributions with zero mean and flat covariance but non-spherical support:

1. Axis distribution:
   \[
   X \in \{\pm e_1,\ldots,\pm e_d\}.
   \]
2. Symmetric sparse mixtures.
3. Mixtures of paired directions with equalized covariance.

### Methods

Same as Experiment A.

### Metrics

Same as Experiment A, plus covariance condition number and effective rank.

### Expected outcomes

- Condition number can be close to 1 while prototype routing is imbalanced.
- SPR quantile calibration should still produce equal-mass feature cells.

---

## 5. Experiment C: Expert-weight-guided partitioning

### Goal

Use expert weights as an important non-cheating source of partition geometry.

### Expert initialization settings

1. Standard Xavier / Gaussian expert matrices.
2. Controlled symmetric expert principal directions.
3. Controlled clustered expert principal directions.
4. Expert matrices after optional warmup in a toy MoE.

### Prototype extraction

- exact SVD;
- one-step MPI approximation;
- multi-step power iteration for audit only.

### Methods

- expert-SVD prototype top-1;
- MPI-style prototype top-1;
- SPR-Expert using exact SVD prototypes;
- SPR-Expert using MPI prototypes;
- SPR-Fixed and SPR-Local.

### Metrics

- expert prototype pairwise cosine distribution;
- expert prototype spread score;
- router-expert alignment;
- LoadCV;
- margin p05;
- agreement between expert prototype groups and SPR leaves.

### Expected outcomes

- Standard expert initialization may be approximately spread in expectation but is not guaranteed to yield uniform cells in one seed.
- Expert prototypes alone do not guarantee equal-mass dispatch.
- SPR-Expert should preserve equal-mass dispatch while aligning cells with expert-weight geometry.

---

## 6. Experiment D: Feature partition quality

### Goal

Test whether equal-mass feature cells are geometrically meaningful, not just count-balanced.

### Data

Construct latent feature classes for evaluation only:

\[
F \in \{1,\ldots,K\},\quad X = \mu_F + \epsilon.
\]

Then globally whiten or otherwise normalize so that covariance is close to identity. The router must not use `F`.

### Methods

- vanilla linear top-1;
- simplex prototype;
- SPR-Fixed;
- SPR-Local;
- SPR-Expert;
- balanced assignment control.

### Metrics

- LoadCV;
- feature purity;
- route-feature NMI;
- within-cell variance;
- margin p05;
- cell-center separation.

### Expected outcomes

- SPR-Fixed should balance but may have weak feature purity.
- SPR-Local should improve locality and purity.
- SPR-Expert should improve alignment when expert weights contain meaningful directions.

---

## 7. Experiment E: Controlled MoE training dynamics

### Goal

Compare training behavior of vanilla linear routers and SPR-style routers when the feature distribution is designed to be spectrally uniform.

### Task

Use a controlled supervised task with latent feature classes hidden from methods:

\[
Y = A_F X + \epsilon.
\]

Each feature class requires a different transformation. Experts are small MLPs or linear maps.

### Router variants

- vanilla linear top-1;
- linear top-1 + load-balancing loss;
- simplex initialization;
- Frozen-SPR;
- SPR-init-linear;
- SlowUpdate-SPR;
- SPR-Expert.

### Metrics

- training loss;
- validation loss;
- LoadCV;
- route-feature NMI;
- feature purity;
- route flip rate;
- margin p05;
- expert specialization score;
- representation drift.

### Expected outcomes

- Frozen-SPR should preserve dispatch by construction.
- SPR-init-linear tests whether a learnable linear router can preserve an SPR partition.
- SlowUpdate-SPR tests adaptation under feature drift.
- Load-balancing loss may balance counts without preserving feature partitions.

---

## 8. Experiment F: Ablations

Required ablations:

- calibration size;
- expert count;
- dimension;
- non-power-of-two `E`;
- direction policy;
- whitening on/off;
- expert-weight quality;
- update frequency for SlowUpdate-SPR;
- atom/tie handling;
- feature drift strength.

---

## 9. Tables to produce

1. Static equal-mass dispatch summary.
2. Spectrally flat non-spherical counterexample summary.
3. Expert-weight-guided routing audit.
4. Feature partition quality.
5. Training dynamics.
6. Ablations.

Paper tables are generated only from completed `metrics.csv` files. Do not
enter result numbers by hand.

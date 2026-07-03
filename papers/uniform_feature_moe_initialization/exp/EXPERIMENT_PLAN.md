# Experiment Plan: Uniform Feature Routing from Spectral Expert Prototypes

## 0. Scientific target

The paper claims a controlled theorem, not a training-dynamics result:

```text
uniform feature geometry
+ uniformly spread expert spectral prototypes
=> uniform expected top-1 expert load
```

It also claims three boundaries:

1. random prototypes are balanced only in expectation over initializations, not in one realized model;
2. strict finite-token load uniformity requires balanced assignment;
3. MPI/expert-SVD alignment supplies expert-side prototypes but does not by itself guarantee that those prototypes are uniformly spread.

The experiments below map one-to-one to these claims.

---

## E1. Uniform sphere with controlled prototype geometry

### Question

If token features are uniformly distributed on the high-dimensional sphere, does prototype geometry determine expert load?

### Data

Generate token features:

```math
z_i \sim \mathrm{Unif}(\mathbb S^{d-1}).
```

Use:

- quick: `N=20000`, `d in {64}`, `E in {4,8}`, `seeds=3`;
- full: `N=100000`, `d in {64,128}`, `E in {4,8,16}`, `seeds=5`.

### Prototype modes

1. `symmetric`: regular-simplex prototypes, padded to dimension `d`.
2. `random`: independent random unit prototypes.
3. `clustered`: prototypes generated around one common direction.
4. `balanced_symmetric`: same scores as `symmetric`, but assignment is capacity-constrained.

### Metrics

- expert load vector;
- load coefficient of variation, `load_cv`;
- max/min load ratio;
- KL-to-uniform;
- max absolute load error;
- prototype pairwise cosine statistics.

### Pass condition

- `symmetric` has low load error, consistent with finite-token sampling.
- `clustered` has larger load error.
- `balanced_symmetric` has exact or near-exact empirical load balance.

---

## E2. Two-dimensional random-centroid geometry floor

### Question

Does increasing token count remove random-center load imbalance?

### Data

Tokens are unit-circle features:

```math
x_i=(\cos\theta_i,\sin\theta_i).
```

Centroids are random unit vectors. For sorted centroid gaps `G_j`, the true Voronoi mass is:

```math
p_j = (G_{j-1}+G_j)/2.
```

### Sweep

- `E in {4,8,16}`;
- `N in {1000, 10000, 100000}`;
- `seeds=20` for full, `seeds=5` for quick.

### Metrics

Record:

```math
init_error = E \max_j |p_j - 1/E|,
```

```math
sampling_error = E \max_j |\hat p_j - p_j|,
```

```math
total_error = E \max_j |\hat p_j - 1/E|.
```

### Pass condition

- sampling error decreases with `N`;
- initialization error does not decrease with `N`;
- total error approaches initialization error for large `N`.

This experiment directly implements the theoretical decomposition in `theoretical_analysis.md`.

---

## E3. Expert spectral prototypes: exact SVD vs MPI approximation

### Question

Can expert principal singular directions serve as router prototypes, and does MPI recover them?

### Expert construction

For each expert, construct an expert matrix with a prescribed input-side top singular direction `v_e`:

```math
W_e = \sigma_1 v_e a_e^\top + \sigma_0 \Xi_e,
```

where `a_e` is a random unit vector and `Xi_e` is small Gaussian noise.

Prototype modes for `v_e`:

1. `symmetric`;
2. `random`;
3. `clustered`.

### Router variants

1. `exact_svd`: compute the top input-side singular direction of `W_e`.
2. `mpi_1`: one power-then-retract step from random router rows.
3. `mpi_5`: five power-then-retract steps.
4. `random_router`: random router rows.

### Metrics

Alignment:

```math
\lambda_e = \frac{\|r_e^\top W_e\|_2}{\|r_e\|_2 \|W_e\|_2}.
```

Routing:

- load CV;
- KL-to-uniform;
- max/min load ratio;
- average alignment lambda;
- prototype spread.

### Pass condition

- `exact_svd` recovers the prescribed prototype geometry.
- `mpi_1` improves alignment over `random_router`.
- high alignment does not guarantee load uniformity when the recovered expert directions are clustered.

This is the key bridge to the MPI/advisor intuition.

---

## E4. Strict finite-token balanced assignment

### Question

If top-1 routing is imbalanced in one finite sample, can explicit balanced assignment enforce uniform load?

### Methods

Use the same score matrix:

```math
S_{ie}=\langle z_i,u_e\rangle.
```

Compare:

1. unconstrained top-1 assignment;
2. exact balanced assignment for small `N` using `scipy.optimize.linear_sum_assignment` if available;
3. greedy balanced assignment fallback for larger `N`.

### Recommended setting

- quick: `N=2048`, `d=64`, `E=8`, `seeds=3`;
- full: `N=4096`, `d=64`, `E=8`, `seeds=5`.

### Metrics

- load vector;
- load CV;
- max/min load ratio;
- average selected score;
- score drop relative to top-1.

### Pass condition

- balanced assignment achieves exact or near-exact load uniformity;
- report the score cost of enforcing strict balance.

---

## E5. Nonuniform feature spectrum and whitening recovery

### Question

What happens when token features are frequency-uniform but spectrally anisotropic?

### Data

Start from uniform sphere features `z_i`. Generate anisotropic features:

```math
h_i = D z_i,
```

where

```math
D = \mathrm{diag}(\alpha, 1, \ldots, 1).
```

Sweep:

```text
alpha in {1, 2, 5, 10, 20}
```

### Router prototype

Use symmetric prototypes.

### Preprocessing variants

1. `raw`;
2. `centered`;
3. `centered_norm`;
4. `whitened_norm`;
5. `whitened_balanced`.

### Metrics

- covariance condition number;
- spectral entropy;
- effective rank;
- load CV;
- max/min load ratio;
- KL-to-uniform.

### Pass condition

- raw routing worsens as spectral condition number increases;
- whitening reduces condition number and restores routing balance;
- balanced assignment gives strict load uniformity even in finite samples.

---

## E6. Optional training-preservation bridge

### Status

Do not run this tonight unless E1--E5 are finished.

### Purpose

Training dynamics answer a different question:

```text
initial uniform assignment -> preserved assignment after optimization?
```

This requires a margin argument. Existing A06 results already support the claim that preservation depends on positive lower-tail margin.

### Optional variants

1. residual on/off in a small synthetic Transformer-MoE;
2. residual on + centering;
3. residual on + whitening;
4. route-center initialization;
5. expert-SVD/MPI initialization.

### Metrics

- feature NMI;
- matched preserve fraction;
- margin p05;
- sign-flip rate;
- task loss or accuracy;
- hidden-state condition number by layer.

### Claim boundary

This experiment should be discussed as a nonuniform-spectrum and margin-preservation bridge, not as evidence for the ideal uniform theorem.

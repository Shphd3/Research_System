# Codex Tasks for V2.2 Static Feature-Level Specialization

## Goal

Implement the static V2.2 experiment suite for **BFSR: Balanced Feature-Specializing Routing**.

Do not implement training preservation, slow updates, hysteresis, or route-drift experiments in this folder.

## 1. New / revised experiment folder

Use or create:

```text
papers/spectral_partition_router_v2_2/exp/
```

Suggested structure:

```text
exp/src/data.py
exp/src/normalization.py
exp/src/cluster.py
exp/src/routers.py
exp/src/assignment.py
exp/src/metrics.py
exp/src/static_training.py
exp/run_e1_clean_sanity.py
exp/run_e2_isotropy_null.py
exp/run_e3_recoverability_sweep.py
exp/run_e4_spectral_normalization_ablation.py
exp/run_e5_frequency_ablation.py
exp/run_e6_expert_alignment.py
exp/run_e7_static_utility.py
exp/results/
```

## 2. Data generators

### Task 2.1: isotropic null generator

Implement:

```python
make_isotropic_null(n, d, K, seed)
```

Returns:

```text
X: N x d standard Gaussian
F: uniform random labels independent of X
```

Expected diagnostics:

```text
Cov(X) condition number near 1
NMI between any feature-only non-cheating router and F near 0
```

### Task 2.2: isotropic feature-family mixture

Implement:

```python
make_isotropic_feature_mixture(n, d, K, separation, noise, seed)
```

Requirements:

```text
F uniform over K feature families
X | F=k = mu_k + eps
centers approximately centered
aggregate covariance approximately isotropic after whitening
features recoverable when separation is high
```

Implementation suggestion:

```text
sample K raw centers
center them
optionally orthogonalize / whiten the center covariance
scale by separation
add isotropic Gaussian noise
whiten final calibration features when requested
```

Return true centers and labels for evaluation.

### Task 2.3: anisotropic distortion

Implement:

```python
apply_anisotropic_distortion(X, condition_number, seed)
```

Use a random orthogonal basis and controlled singular values.

### Task 2.4: frequency imbalance

Implement:

```python
make_frequency_imbalanced_mixture(..., imbalance_strength, seed)
```

Use non-uniform categorical probabilities for F.

### Task 2.5: static targets

Implement:

```python
make_feature_dependent_target(X, F, target_dim_or_noise, seed)
make_feature_independent_target(X, noise, seed)
```

The feature-dependent target should require different local predictors for different F.

## 3. Normalization

Implement:

```python
fit_spectral_normalizer(X_cal, ridge=1e-5)
apply_spectral_normalizer(X, normalizer)
```

Return diagnostics:

```text
condition number before / after
operator norm ||Cov-I|| before / after
```

## 4. Feature-family recovery

Implement:

```python
fit_feature_clusters(X_cal_norm, K, method='kmeans', seed=0)
predict_feature_cluster(model, X_norm)
```

Start with k-means. Make seed deterministic and expose number of restarts.

Metrics:

```python
cluster_accuracy_up_to_permutation(F_true, C_pred)
adjusted_rand_index(F_true, C_pred)
cluster_purity(F_true, C_pred)
```

## 5. Balanced family-to-expert assignment

Implement assignment functions over recovered families.

### Task 5.1: equal-number assignment

```python
assign_families_equal_number(cluster_ids, E, objective='locality', centers=None, seed=0)
```

When K divisible by E, assign exactly K/E families to each expert.

### Task 5.2: mass-aware assignment

```python
assign_families_mass_aware(cluster_masses, E, centers=None, expert_prototypes=None, objective='locality')
```

Approximate equal mass per expert.

### Task 5.3: expert-aligned assignment

```python
assign_families_expert_aligned(centers, expert_prototypes, cluster_masses, E)
```

Use cosine similarity or projective similarity. For sign-ambiguous prototypes, use:

```python
P = outer(v, v) / ||v||^2
score = trace(P_c @ P_e)
```

## 6. Routers

Implement router classes with a common interface:

```python
router.fit(X_cal, optional_metadata)
router.predict(X)
```

### Required routers

```text
BFSROracleFeatureRouter      # upper bound; uses F during fit
BFSRClusterRouter            # primary non-cheating method
BFSRExpertAlignedRouter      # uses recovered clusters + expert geometry
BFSRRandomGroupRouter        # recovered clusters + random balanced assignment
QuantileSPRRouter            # baseline from previous code if available
VanillaLinearTop1Router      # static random/learned-free linear top-1
RandomRouter                 # lower bound
BalancedAssignmentControl    # batch-count control; not valid main method
```

Important:

```text
BFSROracleFeatureRouter must be clearly marked invalid for non-cheating claims.
BalancedAssignmentControl must not be presented as a distributional router.
```

## 7. Metrics

Implement:

```python
load_cv(routes, E)
max_mass_error(routes, E)
usage_entropy(routes, E)
nmi(routes, F)
purity(routes, F)
conditional_entropy_route_given_feature(routes, F)
mutual_information_route_feature(routes, F)
feature_split_rate(routes, F)
within_expert_feature_diversity(routes, F)
```

Also implement report helpers that output CSV and LaTeX tables.

## 8. Static utility training

Implement fixed-route expert training:

```python
train_fixed_route_experts(X_train, y_train, routes_train, E, model='linear', ridge_or_epochs=...)
evaluate_fixed_route_experts(X_val, y_val, routes_val, experts)
```

Start with ridge regression / linear experts to avoid optimization noise. Later add small MLP experts if needed.

Return:

```text
validation loss
per-feature validation loss
per-expert sample counts
```

## 9. Experiment scripts

### E1 clean sanity

Script:

```text
run_e1_clean_sanity.py
```

Data:

```text
high-separation isotropic feature-family mixture
K divisible by E
```

Output:

```text
mass + specialization metrics for all methods
```

### E2 isotropy null

Script:

```text
run_e2_isotropy_null.py
```

Data:

```text
isotropic Gaussian + independent labels
```

Output:

```text
NMI / purity should be near zero for valid methods
```

### E3 recoverability sweep

Script:

```text
run_e3_recoverability_sweep.py
```

Sweep:

```text
separation
noise
```

Output:

```text
cluster accuracy vs NMI vs LoadCV
```

### E4 spectral normalization ablation

Script:

```text
run_e4_spectral_normalization_ablation.py
```

Compare:

```text
raw
centered only
whitened
```

On:

```text
structured distorted mixture
null distorted data
```

### E5 frequency ablation

Script:

```text
run_e5_frequency_ablation.py
```

Compare:

```text
equal-number assignment
mass-aware assignment
quantile baseline
```

### E6 expert alignment

Script:

```text
run_e6_expert_alignment.py
```

Compare expert prototypes:

```text
aligned
noisy aligned
random
adversarial/permuted
```

### E7 static utility

Script:

```text
run_e7_static_utility.py
```

Compare:

```text
feature-dependent target
feature-independent target
```

## 10. Reporting files

Write outputs to:

```text
exp/results/e1_clean_sanity.csv
exp/results/e2_isotropy_null.csv
exp/results/e3_recoverability_sweep.csv
exp/results/e4_spectral_normalization_ablation.csv
exp/results/e5_frequency_ablation.csv
exp/results/e6_expert_alignment.csv
exp/results/e7_static_utility.csv
```

Generate table fragments:

```text
latex/tables/table_distribution_diagnostics.tex
latex/tables/table_dispatch_metrics.tex
latex/tables/table_recovery_metrics.tex
latex/tables/table_static_utility.tex
```

Generate figures if useful:

```text
latex/figures/recoverability_sweep.pdf
latex/figures/normalization_ablation.pdf
latex/figures/static_utility.pdf
```

## 11. Success checks

Before considering the experiment suite usable, verify:

```text
E1: OracleFeature has near-perfect NMI and LoadCV.
E2: valid methods have NMI near zero.
E3: BFSR-Cluster tracks cluster recovery.
E4: whitening helps structured distorted data but not null data.
E5: equal-number assignment fails under frequency imbalance as expected.
E7: utility gains appear only for feature-dependent targets.
```

## 12. Do not do

Do not implement in V2.2:

```text
SlowUpdate-SPR
Margin-aware update
Hysteresis update
Route-change budget
full trainable router MoE dynamics
```

Those belong to the later training-preservation stage.

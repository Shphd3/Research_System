# Experiment Plan for V2.1: Geometry-Aware Spectral Partition Routing

## 0. Purpose

V2.1 tests whether we can move from equal-mass dispatch to **good feature dispatch**.

Good feature dispatch has three targets:

| Target | Definition | Primary metrics |
|---|---|---|
| Equal mass | `P(g(X)=e)=1/E` | LoadCV, max error, holdout gap |
| Feature coherence | routes preserve latent feature structure | NMI, purity, within-cell variance |
| Preservation | routes survive training / drift | flip rate, margin p05, val loss |

V2 solved the first target under stable calibration assumptions. V2.1 studies the additional assumptions and method changes needed for the second and third targets.

---

## 1. Implementation fixes before experiments

### 1.1 Sign-invariant expert prototypes

Implement:

```python
projective_svd_prototypes(weights) -> projectors  # P_e = v_e v_e.T
projective_distance(P_i, P_j) -> 1 - trace(P_i @ P_j)
projective_group_split(projectors, num_left)
projective_split_direction(projectors_left, projectors_right, X_node=None)
```

Preferred rule:

1. Use projective distances to group experts.
2. Use expert projector contrast to propose a candidate subspace.
3. Orient / select the final feature split direction using unlabeled node features, not labels.

### 1.2 Fixed-basis baseline

Separate two baselines:

```text
SPR-RandomAxis: seeded random direction per node.
SPR-FixedBasis: deterministic orthogonal basis reused by tree depth / node id.
```

### 1.3 Feature-derived tie handling

Implement lexicographic keys:

```python
key(x) = (q_1.T @ x, q_2.T @ x, ..., q_L.T @ x)
```

Use this for deterministic tie handling. Report:

```text
tie_rate
max_atom_mass
exact_split_possible
```

### 1.4 Correct forced-count baseline name

Rename current `Linear + load-balance` if it uses `BalancedAssignment`:

```text
Balanced assignment control
```

Implement a real auxiliary-loss router only if needed for training experiments.

---

## 2. Experiment A: Equal-mass sanity after fixes

### Goal

Verify that fixes preserve the V2 equal-mass claim.

### Data

- Gaussian isotropic features.
- Spherical features.
- Whitened continuous mixture.

### Methods

- Vanilla linear router.
- Simplex prototype router.
- SPR-RandomAxis.
- SPR-FixedBasis.
- GA-SPR-Local.
- GA-SPR-Expert.
- Balanced assignment control.

### Metrics

- calibration LoadCV;
- holdout LoadCV;
- max abs usage error;
- calibration-to-holdout gap;
- margin p05;
- node sample minimum.

### Expected result

Quantile methods should preserve low calibration and held-out imbalance. This confirms implementation health.

---

## 3. Experiment B: Assumption ladder

### Goal

Show which assumptions are needed beyond spectral isotropy.

### Data regimes

#### B1: Isotropic unstructured

```text
X ~ N(0, I)
```

No latent structure should be recoverable.

#### B2: Isotropic clusterable

```text
F uniform in {1,...,K}
X = mu_F + eps
then globally whiten to Cov(X) ≈ I
```

#### B3: Expert-aligned isotropic

Same as B2, but expert weights contain principal directions aligned with `mu_F`.

#### B4: Low-margin / overlapping

Same as B2, but clusters overlap so route margin is small.

### Methods

- SPR-RandomAxis.
- SPR-FixedBasis.
- GA-SPR-Local.
- GA-SPR-Expert.
- GA-SPR-ExpertLocal.
- Balanced assignment control.

### Metrics

- LoadCV;
- NMI;
- purity;
- within-cell variance;
- margin p05;
- center-prototype alignment.

### Expected interpretation

- Equal mass should be easy for quantile methods.
- Feature coherence should be high only in B2/B3 when structure exists and the split policy can find it.
- B1 should not produce meaningful NMI; this is not a failure.
- B4 should expose preservation risk through low margin.

---

## 4. Experiment C: Expert-guided geometry after sign fix

### Goal

Test whether expert weights provide useful geometry after removing SVD sign ambiguity.

### Expert settings

1. Standard Xavier/Gaussian experts.
2. Controlled aligned experts.
3. Controlled noisy experts.
4. Controlled random experts.
5. Strongly clustered experts.

### Methods

- Expert-SVD top-1 with oriented vectors.
- Expert-projector top-1 / nearest-subspace audit.
- MPI-row top-1 if oriented rows are available.
- GA-SPR-Expert with projective prototypes.
- GA-SPR-ExpertLocal.
- GA-SPR-Local.

### Metrics

- LoadCV;
- NMI;
- purity;
- cell-prototype alignment;
- nearest-neighbor prototype cosine;
- max pairwise prototype cosine;
- effective prototype rank;
- margin p05.

### Expected result

Expert weights should improve feature coherence only when they are aligned with feature geometry. Quantiles should still provide mass.

---

## 5. Experiment D: Margin-aware update vs naive update

### Goal

Replace negative SlowUpdate-SPR with a controlled preservation method.

### Methods

- Frozen GA-SPR.
- Naive SlowUpdate-SPR.
- Margin-aware update GA-SPR.
- Hysteresis GA-SPR.
- Route-change-budget GA-SPR.

### Update rules

Margin-aware update accepts a recalibration only if:

```text
estimated route flip rate on a validation buffer <= beta
margin p05 after update >= gamma
holdout LoadCV does not exceed tolerance
```

Hysteresis rule:

```text
points within old boundary band keep old route unless new margin is larger than h
```

### Metrics

- route flip rate;
- LoadCV;
- NMI over time;
- margin p05;
- validation loss;
- number of accepted updates;
- route-change budget used.

### Expected result

Naive update should remain unstable; margin-aware update should reduce flips while retaining most of the mass benefit.

---

## 6. Experiment E: Controlled training with true baselines

### Goal

Test whether geometry-aware dispatch improves controlled hard-routing expert training and compare against true router baselines.

### Task

Latent feature classes with class-dependent targets:

```text
Y = A_F X + noise
```

Feature labels are hidden from router construction and training.

### Required baselines

- Fixed vanilla linear top-1.
- Trainable linear top-1 router.
- Trainable linear top-1 + load-balancing auxiliary loss.
- Balanced assignment control.
- Frozen GA-SPR.
- GA-SPR-init-linear.
- GA-SPR-Expert.
- Margin-aware GA-SPR update.

### Metrics

- train loss;
- validation loss;
- LoadCV;
- NMI;
- purity;
- flip rate;
- margin p05;
- representation drift;
- expert specialization score.

### Expected result

Expert-guided and margin-aware methods should outperform mass-only methods when expert or feature geometry is aligned. If not, the result defines the boundary of the method.

---

## 7. Experiment F: Failure modes

### Goal

Characterize cases where the problem is not identifiable or the method should fail.

### Cases

- No latent structure.
- Large atoms exceeding `1/E`.
- Expert weights random and unaligned.
- High feature drift with low initial margins.
- Calibration distribution differs from holdout distribution.

### Required output

For each failure mode, state which assumption is violated:

```text
equal-mass regularity
feature clusterability
expert alignment
low-boundary-mass
bounded drift
```

---

## 8. Paper tables to generate later

Do not generate numbers manually. After experiments, create:

```text
latex/tables/e1_equal_mass.tex
latex/tables/e2_assumption_ladder.tex
latex/tables/e3_expert_guided.tex
latex/tables/e4_margin_update.tex
latex/tables/e5_training.tex
latex/tables/e6_failures.tex
```

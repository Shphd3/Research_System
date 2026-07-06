# V2.2 Experiment Plan and Executed Result Map

## 0. Current Stage Claim

This experiment suite supports the static clean-case paper:

```text
Under globally spectrally isotropic, frequency-uniform, locally recoverable
feature-family distributions, BFSR can construct a balanced and
feature-consistent static dispatch without using latent labels during router
construction.
```

The current stage does **not** test:

```text
training-time preservation
learned-router dynamics
expert semantic identity
feature-dependent utility
automatic selection of K
```

Static utility is parked as a downstream optional audit.

## 1. Terminology / Definitions

LoadCV:
plain meaning: coefficient of variation of expert usage.
concrete computation: standard deviation of expert probabilities divided by their mean.
why it matters: tests expert mass balance.
what it cannot prove: feature specialization or expert utility.

Family consistency:
plain meaning: whether each true feature family is routed mostly to one expert.
concrete computation: average over families of \(\max_e P(G=e\mid F=k)\).
why it matters: primary specialization metric when \(K\ge E\).
what it cannot prove: semantic expert identity or training preservation. It also has a random floor near \(1/E\), so the null experiment is judged primarily by expert information fraction.

Feature split rate:
plain meaning: fraction of feature families split across multiple experts.
concrete computation: a family is split when more than one expert receives at least 5% of that family's samples.
why it matters: detects whether mass-balanced routing cuts through feature families.
what it cannot prove: downstream utility.

Expert information fraction:
plain meaning: how much the selected expert tells us about the feature family.
concrete computation: \(I(G;F)/H(G)\).
why it matters: detects feature-agnostic balanced routing.
what it cannot prove: one-to-one feature/expert semantics when \(K>E\).

Cluster accuracy:
plain meaning: feature-family recovery quality.
concrete computation: clustering accuracy after best permutation matching between recovered cluster ids and true family ids.
why it matters: tests the local recoverability assumption.
what it cannot prove: mass balance by itself.

## 2. Methods

Primary method:

```text
BFSR-Cluster:
1. fit spectral normalizer on calibration X
2. recover K clusters by k-means without labels
3. assign recovered families to experts under equal-number or mass-aware balance
4. route holdout examples by recovered family identity
```

Minimal baselines:

```text
OracleFeature       invalid upper bound; uses true F
Quantile-SPR        mass-only baseline; can balance mass while splitting families
Random linear       ordinary static top-1 router lower bound
```

BalancedAssignment is not used in the main result tables because it is a
current-batch count control, not a fixed distributional router.

## 3. Executed Experiments

Full-run setting:

```text
seeds: 0,1,2,3,4
d: 16
K: 32
E: 4
calibration examples: 8000
holdout examples: 16000
```

### E1. Clean mass and specialization sanity

Question:
Can BFSR solve the positive clean case when feature families are frequency-uniform, spectrally isotropic, and locally recoverable?

Primary judgment:
BFSR-Cluster reaches LoadCV 0.003, family consistency 0.990, and cluster accuracy 0.986.

Interpretation:
The positive clean case is solvable without using labels during router construction.

### E2. Isotropy-alone null

Question:
Can valid non-cheating methods recover feature specialization when \(X\sim N(0,I)\) and \(F\perp X\)?

Primary judgment:
Valid methods have expert information fraction around 0.002.

Interpretation:
Spectral isotropy alone does not identify feature-family dispatch.

### E3. Recoverability sweep

Question:
Does specialization track local feature recoverability?

Primary judgment:
As separation rises from 0.45 to 2.50, cluster accuracy rises from 0.063 to 0.942 and family consistency rises from 0.294 to 0.956.

Interpretation:
Specialization is caused by recoverable local feature structure, not by isotropy alone.

### E4. Spectral normalization ablation

Question:
Does whitening repair anisotropic metric distortion, and does it avoid creating fake specialization in null data?

Primary judgment:
On distorted structured data, whitening raises cluster accuracy from 0.250 to 0.958. On distorted null data, expert information fraction remains around 0.002 after whitening.

Interpretation:
Spectral normalization is metric repair. It does not manufacture feature identity.

### E5. Frequency-uniformity ablation

Question:
Is uniform feature frequency the reason equal-number family assignment gives balanced expert mass?

Primary judgment:
On imbalanced feature frequencies, equal-number BFSR has LoadCV 0.149 while mass-aware BFSR has LoadCV 0.029. OracleFeature shows the theorem boundary more sharply: equal-number LoadCV 0.500 vs mass-aware LoadCV 0.024.

Interpretation:
Uniform frequency is the clean-case mass mechanism. When it is removed, mass-aware assignment is required.

## 4. Artifact Map

```text
runner:
papers/spectral_partition_router_v2_2/exp/run_static_dispatch_suite.py

source:
papers/spectral_partition_router_v2_2/exp/src/static_bfsr_suite.py

result summary:
papers/spectral_partition_router_v2_2/exp/results/summary.md

raw and aggregate CSVs:
papers/spectral_partition_router_v2_2/exp/results/

paper tables:
papers/spectral_partition_router_v2_2/latex/tables/

paper figures:
papers/spectral_partition_router_v2_2/latex/figures/
```

## 5. Parked Downstream Audits

The following experiments are intentionally not part of the current claim:

```text
expert alignment ladder
static utility audit
training-time preservation
learned-router dynamics
```

They should be opened only after the static dispatch story is accepted.

# V2.2 Experiment Plan and Executed Result Map

## 0. Current Stage Claim

The E1--E5 suite supports the following narrow static claim:

```text
Under globally spectrally isotropic, frequency-uniform, locally recoverable
feature-family distributions, BFSR can construct a balanced and
feature-consistent static dispatch using only calibration features.
```

The current stage does **not** test:

```text
training-time preservation
learned-router dynamics
semantic expert identity
feature-dependent utility
automatic selection of K
real language-model hidden states
```

Static utility is reserved for a downstream audit.

## 1. Metrics and Interpretation

### LoadCV

Plain meaning: coefficient of variation of expert usage.

Computation: standard deviation of expert probabilities divided by their mean.

What it tests: expert mass balance.

What it cannot prove: feature specialization or task utility.

### Family consistency

Plain meaning: whether each true feature family is routed mostly to one expert.

Computation:

```text
mean over families of max_e P(G=e | F=k)
```

What it tests: primary feature-family preservation when `K >= E`.

What it cannot prove: one-to-one semantic expert identity.  It also has a random
floor near `1/E`, with a finite-sample upward bias because it takes a maximum
over experts.

### Feature split rate

Plain meaning: fraction of feature families split across multiple experts.

Computation: a family is split when more than one expert receives at least 5% of
that family's samples.

What it tests: whether a mass-balanced router cuts through coherent feature
families.

### Expert information fraction

Plain meaning: how much selected expert identity tells us about feature-family
identity.

Computation:

```text
I(G;F) / H(G)
```

What it tests: feature-agnostic versus feature-informative routing.

Why it matters: it is the decisive metric in the isotropy-only null because
family consistency has a random floor.

### Cluster accuracy

Plain meaning: quality of recovered feature families.

Computation: clustering accuracy after best permutation matching between
recovered cluster ids and true family ids.

What it tests: local recoverability.

## 2. Methods

Primary method:

```text
BFSR-Cluster:
1. fit spectral normalizer on calibration X
2. recover K clusters by k-means without labels
3. assign recovered families to experts under equal-number or mass-aware balance
4. route holdout examples by recovered family identity
```

Baselines:

```text
OracleFeature       non-admissible upper bound; uses true F
Quantile-SPR        mass-only baseline; can balance mass while splitting families
Random linear       ordinary static top-1 router lower bound
```

BalancedAssignment is not used in the main result tables because it is a
current-batch count control, not a fixed distributional router.

## 3. Full-Run Setting

```text
seeds: 0,1,2,3,4
d: 16
K: 32
E: 4
calibration examples: 8000
holdout examples: 16000
```

## 4. Executed Experiments

### E1. Clean mass and specialization sanity

Question: Can BFSR solve the positive clean case when feature families are
frequency-uniform, spectrally isotropic, and locally recoverable?

Primary result: BFSR-Cluster reaches LoadCV 0.003, family consistency 0.990, and
cluster accuracy 0.986.

Interpretation: the positive clean case is solvable with a label-free
calibration-time router.

### E2. Isotropy-alone null

Question: Can admissible label-free methods recover feature-family dispatch when
`X ~ N(0,I)` and `F` is independent of `X`?

Primary result: admissible label-free methods have expert information fraction
around 0.002.

Interpretation: spectral isotropy alone does not identify feature-family
dispatch.

### E3. Recoverability sweep

Question: Does specialization track local feature recoverability?

Primary result: as separation rises from 0.45 to 2.50, cluster accuracy rises
from 0.063 to 0.942 and family consistency rises from 0.294 to 0.956.

Interpretation: specialization is controlled by recoverable local feature
structure, not by isotropy alone.

### E4. Spectral normalization ablation

Question: Does whitening repair anisotropic metric distortion, and does it avoid
creating artificial specialization in null data?

Primary result: on distorted structured data, whitening raises cluster accuracy
from 0.250 to 0.958.  On distorted null data, expert information fraction remains
around 0.002 after whitening.

Interpretation: spectral normalization is metric repair.  It does not manufacture
feature identity.

### E5. Frequency-uniformity ablation

Question: Is uniform feature frequency the reason equal-number family assignment
gives balanced expert mass?

Primary result: on imbalanced feature frequencies, equal-number BFSR has LoadCV
0.149 while mass-aware BFSR has LoadCV 0.029.  OracleFeature shows the theorem
boundary more sharply: equal-number LoadCV 0.500 versus mass-aware LoadCV 0.024.

Interpretation: uniform frequency is the clean-case mass mechanism.  When it is
removed, mass-aware assignment is required.

## 5. Artifact Map

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

## 6. Reliability Notes

The results are reliable for the narrow static-dispatch claim because the suite
includes:

```text
held-out evaluation
five random seeds
oracle upper bound
isotropy-only null
recoverability sweep
raw-vs-whitened metric ablation
frequency-uniformity ablation
```

The results are not sufficient for:

```text
claiming better downstream learning
claiming real-language feature routing
claiming learned-router superiority
claiming training-time preservation
claiming automatic K discovery
```

## 7. Parked Downstream Audits

The following experiments should be opened only after the static dispatch story
is accepted:

```text
expert alignment ladder
static utility audit
training-time preservation
learned-router dynamics
real hidden-state feature audit
```

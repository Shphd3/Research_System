# V2.2 Experiment Plan: Static Feature-Level Specialization

## 0. Purpose

This experiment plan supports the V2.2 static paper.

It tests whether a non-cheating router can achieve feature-level specialization under:

```text
globally spectrally isotropic features
uniform feature-family frequencies
recoverable local feature families
fixed static routing
```

Excluded:

```text
training preservation
representation drift
slow router updates
hysteresis
learned-router dynamics
```

## 1. Methods

### Primary methods

#### BFSR-Cluster

```text
1. whiten / spectrally normalize X
2. recover K feature families by clustering
3. assign recovered families to experts with balanced mass constraint
4. route each token by nearest recovered feature family
```

This is the main non-cheating method.

#### BFSR-ExpertAligned

Same as BFSR-Cluster, but family-to-expert assignment uses expert-side geometry when available.

### Anchors and controls

#### BFSR-OracleFeature

Uses true feature family labels during routing construction.

Purpose: upper bound only. Not a valid non-cheating method.

#### BFSR-RandomGroup

Uses recovered families but assigns them randomly to experts under balance.

Purpose: separates feature recovery from assignment quality.

#### Quantile-SPR

Uses projection quantiles for mass balance.

Purpose: shows whether mass balance alone is enough.

#### Vanilla linear top-1

Static linear router baseline.

#### Random router

Lower bound.

#### BalancedAssignment

Forces equal counts in the current batch.

Purpose: batch-count control, not a valid distributional router.

## 2. Metrics

### Mass metrics

```text
LoadCV
max absolute expert-mass error
expert usage entropy
```

### Feature-specialization metrics

```text
NMI(G,F)
purity(G,F)
H(G|F)
I(G;F)
feature split rate
within-expert number of feature families
```

### Feature-recovery metrics

```text
cluster accuracy up to permutation
Adjusted Rand Index
cluster purity
```

### Static utility metrics

```text
validation loss
per-feature validation loss
loss gap vs Quantile-SPR
loss gap vs BFSR-RandomGroup
loss gap vs BalancedAssignment
```

### Distribution diagnostics

```text
covariance condition number
operator norm ||Cov-I||
feature center separation
estimated feature-family mass imbalance
```

## 3. Data generators

### G1. Isotropic null generator

```text
X ~ N(0, I_d)
F ~ Uniform({1,...,K}) independent of X
```

Purpose: prove isotropy alone is insufficient.

Expected:

```text
all non-cheating methods have low NMI / purity
LoadCV can be low for balancing methods
static utility should not improve from feature specialization
```

### G2. Isotropic feature-family mixture

```text
F ~ Uniform({1,...,K})
X | F=k = mu_k + eps
```

where centers are constructed to be globally balanced:

```text
mean center approximately 0
aggregate covariance approximately isotropic after normalization
```

Purpose: positive clean case.

Sweep:

```text
center separation: low / medium / high
noise variance: low / medium / high
K/E ratio: 1, 2, 4
```

Expected:

```text
BFSR-OracleFeature upper bound succeeds
BFSR-Cluster approaches OracleFeature as separation increases
Quantile-SPR balances mass but may split feature families
```

### G3. Anisotropically distorted feature-family mixture

Start from G2, then apply:

```text
X_raw = A X
```

where A has a controlled condition number.

Compare:

```text
raw space routing
whitened / spectrally normalized routing
```

Purpose: test the causal role of spectral normalization as metric repair.

Expected:

```text
raw anisotropic space hurts clustering and feature specialization
normalization restores performance when local structure is recoverable
normalization does not create specialization in null data
```

### G4. Frequency imbalance generator

```text
P(F=k) not equal
```

Purpose: test whether uniform frequency is the mass mechanism.

Expected:

```text
equal-number family assignment no longer guarantees mass balance
mass-aware family assignment can partially repair balance
```

### G5. Feature-dependent static target

```text
Y = a_F^T X + noise
```

or a feature-conditioned classification target.

Purpose: test static learning utility.

Expected:

```text
coherent feature routing improves fixed-route expert learning
improvement increases when expert capacity is limited
```

### G6. Feature-independent static target

```text
Y = a^T X + noise
```

with no dependence on F.

Purpose: negative utility control.

Expected:

```text
BFSR should not get a systematic utility advantage
```

## 4. Experiments

## E1. Clean mass and specialization sanity

### Question

When feature families are uniform, isotropic, and easily recoverable, does balanced family assignment produce balanced and specialized routing?

### Data

```text
G2 with high separation
K divisible by E
```

### Methods

```text
BFSR-OracleFeature
BFSR-Cluster
BFSR-RandomGroup
Quantile-SPR
Vanilla linear top-1
Random router
BalancedAssignment
```

### Metrics

```text
LoadCV
NMI
purity
cluster recovery accuracy
feature split rate
```

### Expected outcome

```text
OracleFeature: near-perfect balance and specialization
BFSR-Cluster: close to OracleFeature if clustering succeeds
BFSR-RandomGroup: balanced and specialized, but assignment geometry may be arbitrary
Quantile-SPR: balanced but lower feature consistency if thresholds split families
BalancedAssignment: perfect batch balance but low stable feature specialization
```

### Results

```text
TODO: fill after running experiments.
```

### Interpretation

```text
TODO: fill after running experiments.
```

## E2. Isotropy-alone null anchor

### Question

Can any non-cheating method recover feature specialization when labels are independent of isotropic features?

### Data

```text
G1
```

### Methods

Same as E1 except OracleFeature is reported only as an invalid upper bound.

### Expected outcome

```text
all valid non-cheating methods have NMI near 0
methods may still differ in LoadCV
```

### Results

```text
TODO: fill after running experiments.
```

### Interpretation

```text
TODO: this should support the claim that spectral isotropy alone is insufficient.
```

## E3. Feature recoverability sweep

### Question

Does feature specialization track local feature recoverability?

### Data

```text
G2 with separation / noise sweep
```

### Methods

```text
BFSR-OracleFeature
BFSR-Cluster
BFSR-RandomGroup
Quantile-SPR
Vanilla linear top-1
```

### Metrics

```text
cluster accuracy
NMI
purity
LoadCV
```

### Expected outcome

```text
as separation increases:
cluster recovery improves
BFSR-Cluster NMI improves
mass remains controlled if family assignment remains balanced
```

### Results

```text
TODO: fill after running experiments.
```

### Interpretation

```text
TODO: relate performance to local recoverability, not isotropy alone.
```

## E4. Spectral normalization causal ablation

### Question

Does spectral normalization repair an anisotropic metric, and does it avoid creating fake specialization in null data?

### Data

```text
G3: distorted structured mixture
G1 with matched anisotropic distortion
```

### Conditions

```text
raw X
centered only X
whitened X
```

### Methods

```text
BFSR-Cluster
Quantile-SPR
Vanilla linear top-1
```

### Expected outcome

```text
on structured distorted data: whitening improves cluster recovery and NMI
on null data: whitening does not create NMI
```

### Results

```text
TODO: fill after running experiments.
```

### Interpretation

```text
TODO: support spectral normalization as metric repair.
```

## E5. Frequency uniformity ablation

### Question

Is frequency uniformity the reason equal family assignment gives balanced expert mass?

### Data

```text
G4 with controlled frequency imbalance
```

### Methods

```text
BFSR-OracleFeature equal-number assignment
BFSR-OracleFeature mass-aware assignment
BFSR-Cluster equal-number assignment
BFSR-Cluster mass-aware assignment
Quantile-SPR
```

### Expected outcome

```text
equal-number assignment works only when feature frequencies are uniform
mass-aware assignment repairs some imbalance if masses are estimated well
```

### Results

```text
TODO: fill after running experiments.
```

### Interpretation

```text
TODO: clarify whether uniform frequency is a causal condition for mass.
```

## E6. Expert alignment ladder

### Question

Does expert-side geometry help only when it is aligned with feature-family geometry?

### Data

```text
G2 with medium/high separation
```

### Expert conditions

```text
aligned expert prototypes
noisy aligned expert prototypes
random expert prototypes
adversarial / permuted expert prototypes
```

### Methods

```text
BFSR-ExpertAligned
BFSR-RandomGroup
BFSR-Cluster locality assignment
```

### Expected outcome

```text
aligned experts improve assignment utility / compatibility
random experts should not give comparable gains
```

### Results

```text
TODO: fill after running experiments.
```

### Interpretation

```text
TODO: distinguish feature recovery from expert identity assignment.
```

## E7. Static utility audit

### Question

Does feature-specializing routing improve fixed-route expert learning only when the target is feature-dependent?

### Data

```text
G5 feature-dependent target
G6 feature-independent target
```

### Expert training setup

```text
router fixed before training
experts trained only on routed samples
capacity-limited experts
same optimization budget across methods
```

### Methods

```text
BFSR-OracleFeature
BFSR-Cluster
BFSR-ExpertAligned
BFSR-RandomGroup
Quantile-SPR
Vanilla linear top-1
BalancedAssignment
```

### Metrics

```text
validation loss
per-feature loss
LoadCV
NMI
```

### Expected outcome

```text
feature-dependent target: coherent BFSR variants should improve loss
feature-independent target: no systematic BFSR advantage
```

### Results

```text
TODO: fill after running experiments.
```

### Interpretation

```text
TODO: connect utility to feature dependence and expert capacity.
```

## 5. Minimal table templates

### Table 1: Distribution diagnostics

| Dataset | Cond(Cov) | ||Cov-I|| | K | E | Sep | Freq imbalance |
|---|---:|---:|---:|---:|---:|---:|
| TODO | TODO | TODO | TODO | TODO | TODO | TODO |

### Table 2: Static dispatch metrics

| Dataset | Method | LoadCV | Max mass err | NMI | Purity | Split rate |
|---|---|---:|---:|---:|---:|---:|
| TODO | TODO | TODO | TODO | TODO | TODO | TODO |

### Table 3: Feature recovery

| Dataset | Method | Cluster acc | ARI | Cluster purity |
|---|---|---:|---:|---:|
| TODO | TODO | TODO | TODO | TODO |

### Table 4: Static utility

| Dataset | Method | Val loss | Per-feature loss std | LoadCV | NMI |
|---|---|---:|---:|---:|---:|
| TODO | TODO | TODO | TODO | TODO | TODO |

## 6. Execution order

Run in this order:

```text
E1 clean sanity
E2 isotropy null
E3 recoverability sweep
E4 spectral normalization ablation
E5 frequency ablation
E6 expert alignment ladder
E7 static utility audit
```

Do not run E7 before E1--E4 are understood. Utility results are hard to interpret without first proving that the static router is actually balanced and feature-specializing.

## 7. Required reporting style

Every experiment report should include:

```text
Question
Assumption tested
Expected outcome
Result
Interpretation
Failure explanation, if any
```

Do not report a positive result without the matched negative anchor.

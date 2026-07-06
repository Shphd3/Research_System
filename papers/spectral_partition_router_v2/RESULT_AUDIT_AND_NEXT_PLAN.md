# V2 Result Audit and Next Plan

## 0. Audit scope

This audit checks the current V2 paper, shared implementation, run scripts, result summaries, and paper tables under:

```text
papers/spectral_partition_router_v2/
```

Reviewed files include:

```text
latex/paper.tex
latex/tables/*.tex
exp/src/synthetic_suite.py
exp/run_static_dispatch.py
exp/run_expert_guided.py
exp/run_feature_partition_quality.py
exp/run_training_dynamics.py
exp/run_ablations.py
exp/results/*/summary.md
```

---

## 1. Current bottom line

The current V2 implementation and results support the following narrow claim:

> Recursive quantile routing can construct equal-mass feature cells on calibration data and substantially reduce held-out usage imbalance relative to random linear or prototype-only routers in controlled synthetic distributions.

The current results do **not** yet support the stronger claim:

> We have constructed a generally good MoE router that both dispatches features meaningfully and preserves that partition throughout realistic training.

The method is not wrong, but the current problem relaxation is broad. Quantile thresholds solve equal mass. They do not automatically solve feature meaningfulness or training preservation. Expert-weight guidance helps only when expert weights carry a useful geometric prior.

---

## 2. Does the implementation match the theory?

### 2.1 What is implemented correctly

The implementation is structurally consistent with the recursive quantile theory:

- `SPRTree.fit` recursively builds a tree from calibration features.
- Each node splits its expert set into left/right subsets.
- The split ratio is `left_n / len(experts)`, matching the theory.
- The threshold is computed from the node-local projection distribution, not globally.
- Prediction uses stored directions and thresholds, not recalibrated holdout quantiles.
- Balanced assignment is implemented separately as a forced-count control.

Relevant implementation locations:

```text
SPRTree.fit / _fit_node / _route_many in exp/src/synthetic_suite.py
```

### 2.2 Main implementation issues to fix

#### Issue 1: Expert-SVD sign ambiguity is not handled

`svd_prototypes` returns the first left singular vector of each expert matrix. This vector has arbitrary sign:

\[
v_e \equiv -v_e.
\]

`SPRTree._choose_split(policy="expert")` directly averages signed prototype vectors:

\[
q = \mathrm{mean}(v_e:e\in E_L)-\mathrm{mean}(v_e:e\in E_R).
\]

This can make SPR-Expert depend on SVD sign conventions. Current synthetic expert weights may make signs stable enough, but this is not a valid general implementation.

**Fix:** implement one of:

1. router-row inherited orientation when prototypes come from router rows or MPI rows;
2. deterministic anchor orientation;
3. sign-invariant projective prototypes
   \[
   P_e=v_ev_e^\top.
   \]

For exact SVD expert-weight prototypes, use projective prototypes by default.

#### Issue 2: `SPR-Fixed` is random-axis, not a fixed orthogonal spectral basis

The current fixed policy falls back to

```python
unit_vector(self.r.normal(size=x.shape[1]))
```

at each node. This is a deterministic random axis given the seed, but it is not the planned fixed orthogonal / Hadamard / Fourier basis.

**Fix:** rename current policy to `SPR-RandomAxis`, or implement true `SPR-FixedBasis` with stored orthogonal axes.

#### Issue 3: Discrete / atom-supported data need explicit tie handling

The theory assumes continuous scalar projections. Some experiments use finite-support or near-discrete distributions. The current code uses `np.quantile(..., method="linear")` and a fallback when one side is empty. It does not fully solve deterministic feature-level ties.

**Fix:** implement lexicographic feature-derived tie keys and report tie/atom rates. Do not use sample index to split identical features if the method is meant to be feature-only deterministic.

#### Issue 4: The training baseline called `Linear + load-balance` is actually forced balanced assignment

In `run_training_dynamics.py`, method `lb_control` is implemented as:

```python
router = BalancedAssignment(...)
```

This is not a trainable linear router with a load-balancing auxiliary loss. It is a batch-level forced-count control.

**Fix:** rename the table row to `Balanced assignment control`, or implement a real linear router trained with an auxiliary load-balancing loss.

#### Issue 5: Training dynamics are not full MoE router training dynamics

The current E5 trains only expert linear maps under routes produced by fixed or periodically recalibrated routers. Vanilla linear routing is fixed; the router itself is not learned by gradient descent. Therefore E5 is a controlled hard-routing expert-training audit, not a full MoE training-dynamics experiment.

**Fix:** state this explicitly in the paper, or implement a second training experiment with a learnable router.

#### Issue 6: The `clustered` expert prototype setting is not strongly clustered by the reported spread metric

The E3 table reports prototype spread around 0.875--0.894 across clustered, random, and symmetric settings. This means the current `clustered` construction is not sharply separated by the current spread metric.

**Fix:** strengthen clustered prototype construction or add more diagnostic spread metrics, such as maximum pairwise cosine, nearest-neighbor cosine, group concentration, and effective prototype rank.

---

## 3. Do the results match the theory?

### 3.1 Equal-mass dispatch: mostly yes

E1 supports the equal-mass construction. In the main full-run setting, SPR variants have zero calibration LoadCV and held-out LoadCV around 0.024--0.041, while vanilla random linear routing is around 0.069--0.072 and random-linear full-sweep summary is 0.0855.

Interpretation:

- The calibration balance follows the construction.
- The held-out gap reflects finite calibration and deployment sampling error.
- This matches the quantile theory.

### 3.2 Spectrally flat non-spherical data: yes, with boundary cases

E2 shows that whitening can give condition number 1 and effective rank 64, while prototype-only routing remains imbalanced. This supports the claim that covariance flatness is not enough for prototype routers.

However, SPR performance is not uniformly excellent: on paired-directions data, SPR LoadCV can be around 0.18--0.21, worse than its Gaussian/spherical behavior. This does not violate the continuous quantile theorem; it shows the boundary where finite support, near ties, and calibration/holdout mismatch matter.

Interpretation:

- Quantile calibration helps.
- Continuous-density assumptions and tie handling matter.
- The paper should not imply SPR solves all covariance-flat distributions equally well.

### 3.3 Expert-weight guidance: yes, but conditional

E3 supports the separation:

```text
Expert weights choose geometry.
Quantiles control mass.
```

SPR-Expert has much lower LoadCV than expert-SVD top-1 while preserving high cell-to-prototype alignment. This matches the method design.

But the positive result is conditional: expert weights are synthetically constructed to contain useful principal directions. Standard or noisy expert weights are not guaranteed to be useful.

### 3.4 Feature partition quality: only partially solved

E4 is the most important negative/diagnostic result.

- SPR-Fixed and SPR-Local have low LoadCV but very low route-feature NMI.
- SPR-Expert reaches much higher NMI.
- Balanced assignment has exact count balance but almost no feature agreement.

Interpretation:

- Equal-mass dispatch is solved.
- Meaningful feature partition is not solved by quantiles alone.
- Expert-guided geometry can help if expert weights align with latent feature geometry.

This means the problem has split into two layers:

1. equal-mass dispatch;
2. meaningful / useful feature partition.

V2 solves layer 1 and conditionally improves layer 2.

### 3.5 Training dynamics: promising only in the expert-guided controlled case

E5 shows:

- SPR-Expert reaches the best final validation MSE and highest NMI.
- Frozen-SPR and SPR-init-linear improve only modestly or inconsistently.
- SlowUpdate-SPR has very high route flip rate and worse loss.

Interpretation:

- Expert-guided SPR can help when expert weights encode the right geometry.
- Naive recalibration is unsafe.
- Training preservation is not solved by equal-mass dispatch.
- The current training task is controlled and synthetic, not full MoE router learning.

---

## 4. Are we solving the advisor's task?

The meeting instruction was to close the simplest mathematical case: if feature / spectral space is uniform, write a self-contained theory and experiments; nonuniform large-singular-value cases come later.

V1 solved a strong special case:

```text
spherical feature directions + equal-measure prototype cells -> uniform top-1 usage
```

V2 operationalizes a broader version:

```text
spectrally uniform unlabeled features -> construct equal-probability feature cells by quantile routing
```

This is consistent with the advisor's direction because the original wording did not define what “uniformly distribute features to experts” meant. V2 defines it as equal-mass feature-space partition.

However, if the intended goal is a **good router**, we need a stronger definition than equal-mass dispatch.

---

## 5. What is still unclear in the current problem statement?

The phrase “good dispatch” is still underdefined.

Currently, we have three different targets:

### Target A: Equal-mass dispatch

\[
P(g(X)=e)=1/E.
\]

This is solved by recursive quantiles under standard regularity conditions.

### Target B: Meaningful feature partition

Routes should align with latent feature structure when such structure exists.

Possible metrics:

- route-feature NMI;
- purity;
- within-cell variance;
- cell-center separation;
- expert-prototype alignment.

This is not solved by quantiles alone.

### Target C: Training preservation and utility

The partition should survive training and help the task.

Possible metrics:

- route flip rate;
- margin p05;
- validation loss;
- representation drift;
- expert specialization score.

This is not solved by static calibration alone.

**Next definition needed:** decide whether the paper's main method is only for Target A, or claims progress on Targets A+B, or Targets A+B+C.

---

## 6. Did we relax the V1 assumptions too much?

Yes, if the goal includes meaningful partition and training preservation.

V1 had strong assumptions:

```text
spherical directions + equal-measure cells
```

V2 relaxed to:

```text
spectrally uniform covariance + unlabeled feature distribution
```

For equal-mass dispatch, this relaxation is fine because quantile calibration can handle general distributions.

For meaningful feature dispatch, this relaxation is too broad. Spectral isotropy alone permits many distributions with no useful cluster or feature structure. A method cannot recover feature meaning from isotropy alone.

A milder and more productive relaxation should add one of the following assumptions.

### Option 1: Clusterable isotropic features

After whitening, features are isotropic globally but have latent local structure:

\[
X = \mu_F + \epsilon,
\]

with balanced latent features and separated centers.

### Option 2: Expert-aligned isotropic features

Expert weights provide prototypes correlated with latent feature directions:

\[
\langle v_e, \mu_f\rangle
\]

contains useful assignment information.

### Option 3: Low-boundary-mass partitionability

There exists a tree partition with equal mass and positive margin lower tail:

\[
P(\mathrm{dist}(X,\partial C_{g(X)})\le \epsilon)
\]

is small.

### Option 4: Stable representation dynamics

During training, feature drift is bounded by the routing margin:

\[
\|\Delta X\| < m(x)
\]

for most examples.

These assumptions are mild compared with V1's spherical-uniform prototype condition, but strong enough to make “good dispatch” identifiable.

---

## 7. Recommended next research direction

Do not abandon V2. Split it into two claims.

### Claim 1: Equal-mass feature dispatch

This is the current proven construction.

Method:

```text
recursive quantile routing
```

Status:

```text
mostly solved, but needs discrete/tie/sign fixes
```

### Claim 2: Geometry-aware dispatch

This is the next method contribution.

Method direction:

```text
SPR-Expert with sign-invariant expert prototypes + local quantile refinement
```

Target:

```text
equal mass + high feature NMI/purity + low route flip rate
```

This claim should be studied under a mild additional assumption:

```text
expert weights or feature geometry contain a useful alignment prior
```

### Claim 3: Training-preserved dispatch

This should be a later section or separate paper-level extension.

Needed method changes:

- avoid naive SlowUpdate-SPR;
- use margin-aware threshold updates;
- update only when the estimated distribution shift exceeds statistical noise;
- add hysteresis / buffer zones near thresholds;
- optionally distill tree routes into a trainable linear router with route-preservation loss.

---

## 8. Concrete method fixes for v2.1

### Fix 1: Rename / separate routers

Current names should be clarified:

- `SPR-Fixed` -> `SPR-RandomAxis` unless a true fixed orthogonal basis is implemented.
- `Linear + load-balance` -> `Balanced assignment control` unless a true auxiliary-loss baseline is implemented.
- `SlowUpdate-SPR` -> `Naive SlowUpdate-SPR` because current results show it is unstable.

### Fix 2: Implement sign-invariant SPR-Expert

Add:

```python
projective_svd_prototypes(weights) -> P_e = v_e v_e.T
projective_group_split(P_e)
projective_split_direction(P_left, P_right)
```

or orient each SVD vector by a deterministic anchor.

### Fix 3: Implement deterministic feature-derived tie handling

Use lexicographic projections:

```python
key(x) = (q_1^T x, q_2^T x, ..., q_L^T x)
```

Report tie rate and atom mass.

### Fix 4: Add margin-aware recalibration

Replace naive slow updates with:

```text
only recalibrate if distribution shift is large;
do not change routes for examples inside a hysteresis band unless confidence is high;
track route-change budget.
```

### Fix 5: Add a true learnable-router training baseline

Current E5 does not train the router. Add:

```text
linear top-1 router with gradient updates + load-balance auxiliary loss
linear router initialized from SPR cells + route preservation regularizer
```

---

## 9. Immediate paper update recommendation

The current paper should be updated in wording before further use:

1. Say “controlled hard-routing expert training” instead of “MoE training dynamics” unless router learning is implemented.
2. Mark E4/E5 results as showing that equal-mass dispatch is not sufficient for feature specialization.
3. Emphasize that SPR-Expert is the meaningful positive direction, not SPR-Fixed/Local alone.
4. State that V2 currently solves equal-mass dispatch and conditionally improves feature quality when expert weights provide aligned geometry.
5. State that training preservation remains open; SlowUpdate-SPR is a negative result.

---

## 10. Final assessment

Current V2 answers this question:

> Can we non-cheatingly construct equal-mass feature dispatch in a controlled spectrally uniform setting?

Answer:

```text
Yes, under continuous / stable calibration assumptions, recursive quantile routing solves this.
```

Current V2 does **not** fully answer:

> Can we construct a generally good router whose feature partition is meaningful and preserved through training?

Answer:

```text
Not yet. The results show this requires additional structure: expert-weight alignment, feature clusterability, and margin-preserving training dynamics.
```

The next research step should therefore be:

```text
Move from equal-mass dispatch to geometry-aware, margin-preserved dispatch under mild, explicit assumptions.
```

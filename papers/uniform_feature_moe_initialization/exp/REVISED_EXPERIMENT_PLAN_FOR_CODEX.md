# Revised Experiment Plan For Codex Review

Paper: `papers/uniform_feature_moe_initialization/latex/paper.tex`

Purpose: align experiments with the revised story:

```text
uniform feature routing is a controlled representation-geometry question,
not a capacity-counting question and not an MPI result by itself.
```

The main theorem is a sufficient condition:

```text
spherical token directions + equal-measure expert prototype cells
=> uniform expected unconstrained top-1 expert usage.
```

## 0. Current status

The current synthetic suite has produced 481 rows and supports the main story:

- E1: prototype geometry controls load under uniform sphere features.
- E2: random prototype imbalance is a geometry floor, not finite-token noise.
- E3: spectral expert prototypes are centers, not balance guarantees.
- E4: covariance isotropy is not directional uniformity.
- E5: whitening repairs the elliptical toy representation.
- E6: balanced assignment is a non-geometric control.

Do not replace these experiments. The optional short-sequence bridge remains
parked because it would change the paper from a controlled geometry paper into
a training-dynamics paper.

---

## 1. Required paper-facing experiments

### E1. Uniform sphere + prototype geometry

Keep as main result.

Claim supported:

```text
Under directional uniformity, expert prototype cell geometry controls natural top-1 usage.
```

Required report:

- symmetric top-1;
- random top-1;
- clustered top-1;
- LoadCV, max/min load, max absolute load error.

No change needed unless reproducing results.

---

### E2. High-dimensional random-prototype geometry floor

Keep as main result.

Claim supported:

```text
More routed examples reduce sampling error, not the fixed cell-mass imbalance of one prototype realization.
```

Required report:

- init_error;
- sampling_error;
- total_error;
- sweep over routed batch size N.

No change needed unless reproducing results.

---

### E3. Expert spectral prototypes

Keep as main result, but interpret carefully.

Correct claim:

```text
Exact SVD or MPI can recover expert-side centers. This does not guarantee load balance unless the recovered centers are well spread.
```

Required report:

- exact SVD, MPI-1, MPI-5, random rows;
- symmetric, random, clustered prescribed expert singular directions;
- alignment lambda;
- LoadCV and max/min load.

Important writing rule:

Do not claim MPI solves uniform feature routing. MPI only supplies a center-construction principle.

---

### E4. Covariance-isotropy counterexample

Keep as main result.

Correct claim:

```text
Hidden spectral uniformity is a second-order diagnostic, not a sufficient condition for uniform top-1 usage.
```

Required report:

- four-axis distribution;
- covariance condition number;
- effective rank;
- load vector;
- LoadCV and max/min load ratio.

Important writing rule:

Do not claim covariance identity generally implies spherical directional
uniformity. E4 is the negative counterpart to E5.

---

### E5. Elliptical anisotropy + whitening

Keep as main result.

Correct claim:

```text
In the controlled elliptical toy model, whitening recovers the spherical direction condition used by the theorem.
```

Required report:

- raw;
- centered + normalized;
- partial spectral shrinkage beta=0.5;
- whitened + normalized;
- condition number;
- effective rank;
- LoadCV diagnostic.

Important writing rule:

Do not claim covariance identity generally implies directional uniformity. This experiment only supports the elliptical toy proposition.

---

### E6. Balanced assignment control

Keep as a control. It can remain in the main text because it prevents a common misunderstanding.

Correct claim:

```text
Capacity assignment can force count equality, but it is not a representation-geometric explanation.
```

Required report:

- unconstrained top-1 LoadCV;
- greedy balanced assignment LoadCV and score drop;
- exact balanced assignment LoadCV and score drop.

If space is tight, move the detailed table to appendix, but keep one sentence in the main paper.

---

## 2. Executed audit: E4 covariance-isotropy counterexample

### Why this was needed

The paper contains a formal counterexample showing that covariance identity does
not imply directional uniformity or uniform load. The E4 experiment mirrors this
proposition.

### Claim supported

```text
Hidden spectral uniformity is a second-order diagnostic, not a sufficient condition for uniform top-1 usage.
```

### Construction

Use a 2D token distribution with equal mass on four axis points:

```text
(1,0), (0,1), (-1,0), (0,-1)
```

This distribution has:

```text
mean = 0
covariance = I / 2
```

Use three regular-simplex prototypes at angles:

```text
20 degrees, 140 degrees, 260 degrees
```

These prototypes have equal-measure cells under the continuous uniform circle distribution, but the four-point isotropic distribution routes as:

```text
0 degrees   -> prototype 20 degrees
90 degrees  -> prototype 140 degrees
180 degrees -> prototype 140 degrees
270 degrees -> prototype 260 degrees
```

So loads are:

```text
(1/4, 1/2, 1/4)
```

instead of:

```text
(1/3, 1/3, 1/3)
```

### Implementation status

Implemented in `run_synthetic.py`:

```python
run_e4(rows, quick)
```

Output row:

```text
experiment = E4
setting = covariance_identity_not_directional_uniformity
method = axis_distribution_simplex_router
n = 40000
d = 2
e = 3
condition_number = 1
load_cv = 0.353553
notes = covariance identity but nonuniform directional support
```

### Expected numeric values

For load vector `(1/4, 1/2, 1/4)`:

- mean load = `1/3`;
- LoadCV is approximately `0.353553`;
- max/min load ratio = `2.0`.

### Required output table

Create:

```text
results/tables/e4_covariance_counterexample.md
```

Template:

| Distribution | Covariance condition no. | Direction support | Router cells | Load vector | LoadCV |
|---|---:|---|---|---|---:|
| Four axis points | 1.0 | non-spherical discrete | regular simplex | (0.25, 0.50, 0.25) | 0.3536 |

### Pass condition

The experiment must show condition number 1 but nonuniform load.

---

## 3. Optional later bridge: short-sequence / residual audit

Do not run this tonight unless E1--E6 are complete.

### Purpose

This is not the main proof. It diagnoses why short next-token prediction features may fail the uniform assumptions.

### Variants

- small Transformer-MoE with residual connections on;
- residual connections off or reduced;
- residual on + centering;
- residual on + whitening;
- route-position features only;
- all-position features.

### Metrics

- hidden covariance condition number by layer;
- effective rank by layer;
- directional concentration diagnostics;
- LoadCV under fixed symmetric router;
- feature NMI if feature labels are available;
- margin p05 if training preservation is tested.

### Correct claim boundary

This bridge can show that short-context hidden states are not naturally uniform. It should not be used as evidence against the ideal theorem.

---

## 4. Codex acceptance checklist

Before handing results back:

1. Existing E1--E6 tables reproduce the current summary.
2. E4 is added to `results.csv` and has its own table.
3. E4 shows condition number 1 and LoadCV about 0.3536.
4. No text claims that MPI solves uniform routing by itself.
5. No text claims that covariance identity implies spherical directional uniformity.
6. E6 remains described as a control, not the main mechanism.
7. The paper's main theorem is stated as a sufficient condition.

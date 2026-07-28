---
protocol_id: A06_01_07_E03_high_dimensional_static_geometry
anchor_id: A06_2x2_expert_geometry_gate
status: executed_after_user_request
created: 2026-06-16
canonical_language: en
---

# Protocol A06_01_07_E03: High-Dimensional Uniform Centered-M4 Generalization

## Purpose

Test whether the 2D centered-M4 uniform-load result generalizes to high-dimensional uniform features as an approximate or calibrated result, and identify when it fails.

## Decision Question

For `x ~ Unif(S^{d-1})`, can centered/calibrated M4 route two high-dimensional experts with near-uniform load while preserving positive score margin?

## Hypotheses

H1: Raw M4 can be imbalanced when experts have different average response energy.

H2: Centered M4 reduces load imbalance by removing average response energy.

H3: In high dimension, centered M4 is near-balanced only when the centered score-difference spectrum is sufficiently spread out.

H4: Quantile calibration can enforce balance, but it is only useful if the selected-expert margin remains nontrivial.

## Setup

Expert matrices:

$$
A_1,A_2 \in \mathbb{R}^{m\times d}
$$

Default:

```text
d in {2, 4, 8, 16, 32, 64, 128, 256, 512}
m = d
seeds = 100 or more per condition
samples_per_seed = at least 20,000 sphere samples
```

Input distribution:

```text
primary: x ~ Unif(S^{d-1})
secondary: x ~ Unif(unit ball)
optional finite design: normalized Gaussian samples
```

Expert conditions:

1. `random_gaussian`: iid Gaussian expert matrices with standard scaling.
2. `equal_isotropic`: `G_1` and `G_2` proportional to identity.
3. `unequal_isotropic`: different trace budgets but no directional difference.
4. `random_anisotropic`: random matrices with unequal singular values.
5. `separated_low_rank`: experts with separated dominant subspaces.
6. `near_identical`: `A_2 = A_1 + epsilon noise`.
7. `spiked_traceless_counterexample`: centered difference dominated by one eigenvalue.
8. `balanced_spectrum_control`: positive and negative eigenvalues paired or nearly paired.

## Methods

M4 raw:

$$
q_e(x)=x^TG_ex.
$$

M4 centered:

$$
\tilde q_e(x)=x^TG_ex-\frac{1}{d}\mathrm{tr}(G_e).
$$

M4 quantile-calibrated:

$$
q^{cal}_e(x)=x^TG_ex-\tau_e,
$$

where thresholds are fit on a calibration split only.

M3 top-r weighted projection:

$$
q^{(r)}_e(x)=\sum_{k=1}^{r}\sigma_{e,k}^2(v_{e,k}^Tx)^2-c_{e,r}.
$$

M3 top-r unweighted projection:

$$
q^{(r,unw)}_e(x)=\sum_{k=1}^{r}(v_{e,k}^Tx)^2-c_{e,r}.
$$

Baselines:

- best linear halfspace split fit to M4 labels;
- signed prototype if a sign convention is provided;
- random balanced assignment.

## Metrics

Primary:

```text
natural_load_error
calibrated_load_error
natural_mean_margin
calibrated_mean_margin
low_margin_fraction
M4_centered_oracle_agreement
spectral_spread_r3 = sum |lambda|^3 / (sum lambda^2)^(3/2)
operator_to_frobenius = ||H0||op / ||H0||F
```

Secondary:

```text
degeneracy_rate
margin_quantiles
finite_sample_load_std
rank_energy_captured
low_rank_margin_retention
isotropic_failure_accuracy
near_identical_confidence_flag
```

## Procedure

1. Generate expert pairs for each dimension, condition, and seed.
2. Compute `G_e = A_e^T A_e`.
3. Compute raw and centered score functions.
4. Estimate thresholds for calibrated M4 on a calibration split.
5. Sample uniform sphere features and a secondary unit-ball set.
6. Route every feature under each method.
7. Record load, margin, degeneracy, and agreement with centered M4.
8. Compute eigenvalues of centered score-difference matrix `H0`.
9. Record spectral-spread diagnostics.
10. Plot load error versus dimension and versus spectral-spread statistics.
11. For top-r methods, sweep `r` and record approximation quality.
12. Write `summary.md` and `detailed.md` with support/weaken/insufficient-evidence labels.

## Success Criteria

Supports centered/calibrated M4 if:

```text
centered M4 reduces load error relative to raw M4;
load error decreases when spectral spread improves;
calibration enforces balance without margin collapse;
spiked counterexample fails as predicted;
near-identical experts show low margin rather than false confidence;
M3 top-r approaches centered M4 as rank increases.
```

## Failure Criteria

Weakens centered/calibrated M4 if:

```text
centered M4 load remains unstable under non-spiky random experts;
quantile calibration destroys margin;
load error does not track spectral-spread diagnostics;
M3 top-r balances load but fails to approximate M4 decisions;
prototype baselines dominate M4 in margin and stability.
```

## Insufficient Evidence

Evidence is insufficient if:

```text
only d=2 or one high dimension is tested;
only load is reported;
margin is omitted;
raw and centered scores are mixed;
thresholds are fit and evaluated on the same samples without a split;
spiked and near-identical controls are omitted.
```

## Expected Artifacts

```text
tables/high_dim_metric_summary.csv
tables/spectral_spread_summary.csv
tables/low_rank_approximation_summary.csv
tables/calibration_summary.csv
figures/load_error_vs_dimension.png
figures/load_error_vs_spectral_spread.png
figures/margin_vs_rank.png
figures/spiked_counterexample_partition_or_hist.png
summary.md
detailed.md
```

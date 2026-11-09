# A06_01_01_E04 Detailed Record: High-Dimensional Gaussian Gate Norm Variation

## 1. Purpose

This experiment tests one anchor clause:
in a pure high-dimensional Gaussian dot-product top-1 gate, does row-norm variation explain the extra true decision-cell imbalance beyond normalized random direction geometry?

The experiment is a mechanism audit. It is not a method design, training run, or architecture proposal.

## 2. Anchor And Protocol

Anchor:
`Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol:
`Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_01_E04_gate_norm_variation/protocol.md`

Anchor decision question:
Does removing only row-norm variation reduce the Gaussian-scaled gate's true decision-cell imbalance toward the normalized-direction baseline?

## 3. Model And Conditions

Gate row decomposition:
\[
w_e=\rho_e u_e,\quad z_e=\rho_e u_e^\top x
\]

Observed load decomposition:
\[
\hat p_e-\frac{1}{m}
=
\left(p_e-\frac{1}{m}\right)
+
\left(\hat p_e-p_e\right)
\]

Conditions:

| Condition | Score | Role |
|---|---|---|
| `normalized_directions` | \(u_e^\top x\) | direction-only baseline |
| `gaussian_scaled` | \(\rho_e u_e^\top x\) | standard Gaussian row scale |
| `norm_controlled_gaussian` | \(\bar\rho u_e^\top x\) | same directions, equal row norms |

The decisive intervention is the pair `gaussian_scaled` versus `norm_controlled_gaussian`, because it changes only row-norm variation while keeping directions matched.

## 4. Local Run Configuration

| Field | Value |
|---|---|
| dimensions | 32, 128, 512 |
| experts | 8, 32 |
| seeds | 8 |
| true-cell Monte Carlo tokens | 50,000 per seed |
| observed token counts | 4,096 and 32,768 |
| observed repetitions | 3 |
| input distribution | Gaussian vectors normalized to unit length |
| batch size | 5,000 |

Command:

```powershell
python 'Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_01_E04_gate_norm_variation/scripts/run_norm_variation_gate.py' --out-dir 'Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_01_E04_gate_norm_variation'
```

Runtime:
The local run completed successfully and wrote all planned tables and figures.

## 5. Metrics

Primary metric:
`true_cell_imbalance = m * max_e abs(p_e - 1/m)`.

Secondary metrics:

| Metric | Meaning |
|---|---|
| `observed_load_error` | finite-token load deviation from uniform |
| `sampling_error` | finite-token deviation from estimated true cell probability |
| `row_norm_cv` | coefficient of variation of gate row norms |
| `max_abs_direction_corr` | largest absolute pairwise direction correlation |

Primary metric boundary:
The true-cell estimate is Monte Carlo based, so the numbers are approximate. The conclusion relies on large paired gaps across all tested settings, not on tiny differences.

## 6. Main Table

Mean true-cell imbalance by condition:

| d | m | gaussian_scaled | norm_controlled | normalized | mean paired delta |
|---:|---:|---:|---:|---:|---:|
| 32 | 8 | 0.3647 | 0.1667 | 0.1667 | 0.1981 |
| 32 | 32 | 1.1910 | 0.2686 | 0.2686 | 0.9224 |
| 128 | 8 | 0.1537 | 0.1023 | 0.1023 | 0.0514 |
| 128 | 32 | 0.5725 | 0.1588 | 0.1588 | 0.4137 |
| 512 | 8 | 0.0968 | 0.0588 | 0.0588 | 0.0380 |
| 512 | 32 | 0.3120 | 0.0854 | 0.0854 | 0.2266 |

Paired-delta range:

| d | m | min delta | max delta | mean Gaussian row_norm_cv |
|---:|---:|---:|---:|---:|
| 32 | 8 | 0.0494 | 0.5213 | 0.1035 |
| 32 | 32 | 0.5882 | 1.2736 | 0.1211 |
| 128 | 8 | 0.0056 | 0.0962 | 0.0464 |
| 128 | 32 | 0.2342 | 0.7558 | 0.0582 |
| 512 | 8 | 0.0074 | 0.1046 | 0.0277 |
| 512 | 32 | 0.1459 | 0.3456 | 0.0315 |

Interpretation:
Every tested group has positive paired delta. Removing row-norm variation reduces the fixed true-cell imbalance, and the controlled condition collapses to the normalized-direction baseline.

## 7. Sampling Noise Check

Sampling error decreased when observed tokens increased from 4,096 to 32,768. This matches the anchor decomposition:

\[
\hat p_e-\frac{1}{m}
=
\left(p_e-\frac{1}{m}\right)
+
\left(\hat p_e-p_e\right)
\]

The true-cell floor remains the primary object. Observed finite-token loads approach that floor as sampling error shrinks.

## 8. Visualization Results

### True Cell Imbalance

![True cell imbalance by condition](figures/true_cell_imbalance_by_condition.png)

Purpose:
Test whether the fixed top-1 decision-cell imbalance changes when only row-norm variation is removed.

Setup:
Matched Gaussian directions are scored under original Gaussian row norms and equalized row norms.

How to read:
At each dimension, compare the `gaussian_scaled` line with `norm_controlled_gaussian`.

Observed result:
`gaussian_scaled` is consistently higher; `norm_controlled_gaussian` overlaps `normalized_directions`.

Take-home:
The row-norm term \(\rho_e\) is a causal contributor to the extra Gaussian fixed floor in this gate-only setting.

Remaining uncertainty:
The result does not establish how training, data distribution, attention, residual state, or expert utility interact with this initialization imbalance.

### Sampling Error

![Sampling error by tokens](figures/sampling_error_by_tokens.png)

Purpose:
Check whether finite-token noise shrinks with token count.

Setup:
Observed loads were estimated at 4,096 and 32,768 tokens and compared against the Monte Carlo true-cell estimate.

How to read:
Lower sampling error at higher token count means observed imbalance is less dominated by finite-token noise.

Observed result:
Sampling error decreases with observed token count across conditions.

Take-home:
The result separates sampling noise from the fixed decision-cell imbalance.

Remaining uncertainty:
The true-cell estimates still have finite Monte Carlo precision; a larger run can tighten the numeric values but is unlikely to change the paired direction of the effect.

## 9. Artifact Map

Script:
`scripts/run_norm_variation_gate.py`

Raw row-level table:
`tables/results.csv`

Aggregated table:
`tables/aggregate_by_condition.csv`

Paired comparison table:
`tables/paired_gaussian_vs_norm_controlled.csv`

Figures:
`figures/true_cell_imbalance_by_condition.png`
`figures/sampling_error_by_tokens.png`

## 10. Failure Modes And Boundaries

Possible failure mode:
Monte Carlo precision could slightly perturb small deltas, especially for `(d=128,m=8)` and `(d=512,m=8)`.

Why it does not overturn the current decision:
The paired delta is positive in every tested group, and the strongest settings are large relative to sampling noise and Monte Carlo uncertainty.

Not tested:
Trained routers, non-uniform inputs, attention-derived hidden states, residual streams, semantic expert specialization, downstream loss, or any final routing method.

## 11. Anchor Update Recommendation

Update the anchor from "row-norm variation is plausible but not causally isolated" to:
row-norm variation is supported as a causal contributor to the extra Gaussian fixed gate-only imbalance under the tested high-dimensional uniform-input setting.

Next decision:
Decide whether row-norm variation should become a required diagnostic baseline before interpreting trained-router load imbalance as semantic or data-driven specialization.

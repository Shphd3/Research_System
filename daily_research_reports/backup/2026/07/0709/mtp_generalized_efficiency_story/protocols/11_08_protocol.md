# Protocol: 11_08 General-K Readout-Margin Dynamics

Status: proposed daily protocol.  
Anchor: `../anchors/11_08_general_k_readout_margin_dynamics_anchor.md`.

## 1. Purpose

Test whether the general-K one-step readout-margin velocity follows the theory:

$$
G_K=\frac1{m^2}\sum_z\left\|\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j)\right\|^2.
$$

The goal is not to show larger K always helps. The goal is to decide when adding future horizons increases, leaves unchanged, or reduces readout-effective semantic velocity.

## 2. Dataset

Use branch-delayed decision-prefix data:

```text
BR_z F00 ... F{L-1} U00 U01 U02 U03 Y1 Y2 ... YK STOP
```

Create regimes:

| Regime | Future targets | Purpose |
|---|---|---|
| shared-only | all added horizons shared | tests zero contribution |
| single-informative | one horizon `S_z` | recovers K=2/K=3 theorem |
| aligned-informative | multiple horizons use same branch ordering | tests additive amplification |
| permuted / weakly aligned | later horizon uses branch permutation | tests partial alignment |
| conflicting | later horizon reverses / conflicts with earlier direction when possible | tests non-monotonicity |
| noisy | later horizon independent of Z | tests useless auxiliary target |

## 3. Conditions

Use fixed architecture with heads for max K.

```text
K1_fixed_full_head
K2_active
K3_active
...
Kmax_active
```

Use decision-only loss first.

Primary initialization:

```text
identical_branch / branch-collapsed
```

## 4. Required Metrics

### 4.1 Theorem-predicted velocity

Compute from output rows:

```text
predicted_G_K = mean_z ||sum_{j in I_K} lambda_j (u_{j,z} - mean_z u_{j,z})||^2 / m^2
```

### 4.2 Observed one-step velocity

After one controlled step:

```text
Delta_M_K_over_eta
Delta_E_Z_over_eta2
Delta_local_CE
Delta_native_informative_accuracy
```

### 4.3 Alignment diagnostics

For newly added horizon `r`:

```text
alignment_increment = mean_z 2 <v_z^(K), a_{r,z}> + ||a_{r,z}||^2
pairwise_centered_cosine(j,r)
```

### 4.4 Guarded recovery

Short curve diagnostics:

```text
Q(t)
AUC_Q_early
native informative-horizon accuracy
branch-swap consistency
```

## 5. Procedure

1. Generate each regime.
2. For each K and seed, initialize the same model.
3. Audit leakage at step 0:

```text
Q(0) near chance
M_K(0) near 0
E_Z(0) near 0
native informative accuracy near chance
```

4. Compute predicted `G_K` from active output rows.
5. Clone model and apply one decision-only SGD step using each active K.
6. Record observed `Delta_M_K/eta`.
7. Run a short 0-2000 step curve only after one-step diagnostics are interpretable.

## 6. Pass / Fail

### Support

```text
observed Delta_M_K/eta tracks predicted_G_K
shared/noisy horizons add no semantic margin
aligned horizons increase velocity
conflicting horizons show reduced or non-monotone velocity
local targets are preserved
```

### Weaken

```text
observed velocities do not correlate with predicted_G_K
uninformative horizons create semantic margin without leakage explanation
K always improves regardless of constructed conflict
local losses degrade under larger K
```

## 7. Output Artifacts

Required:

```text
summary.md
detailed.md
predicted_vs_observed_margin.csv
alignment_increment.csv
one_step_metrics.csv
short_curve_metrics.csv
figures/predicted_vs_observed_G.png
figures/K_velocity_by_regime.png
figures/local_guard.png
run_config.json
```

## 8. Interpretation Boundary

If this protocol passes, the claim is:

```text
General-K MTP semantic efficiency depends on readout-direction alignment of informative horizons, not K itself.
```

It still does not prove natural-language benefit or all-position dynamics.

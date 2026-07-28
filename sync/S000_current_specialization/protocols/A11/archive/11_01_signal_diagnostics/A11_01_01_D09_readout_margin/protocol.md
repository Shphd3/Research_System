# Protocol: A11_06 Readout-Effective Margin Efficiency

Status: completed; result recorded in `summary.md` and `detailed.md`.  
Anchor: `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_06_readout_effective_margin_efficiency_anchor.md`.

## 1. Purpose

Test the first-order efficiency mechanism behind long-horizon MTP:

```text
Does the informative K=3 target create positive one-step readout-effective semantic margin growth at the decision prefix, while K=1/K=2 do not?
```

This protocol is intentionally smaller than all-position learning curves. It isolates the direct objective mechanism before indirect transfer appears.

## 2. Dataset

Use clean `tau=3` branch-delayed data:

```text
BR_z F00 ... F{L-1} U00 U01 U02 U03 A_SHARED C_SHARED S_z STOP
```

Decision prefix stops after:

```text
BR_z F00 ... F{L-1} U00 U01 U02 U03
```

Targets:

```text
Y1 = A_SHARED
Y2 = C_SHARED
Y3 = S_z
```

Information relation:

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=0,\qquad I(Z;Y_3\mid Y_1,Y_2)=H(Z).
$$

## 3. Model Conditions

Use the existing A11 one-layer Transformer implementation.

Conditions:

| Condition | Active decision-prefix loss | Role |
|---|---|---|
| `K1_fixed_3head` | `L1` only | non-covering NTP baseline with matched heads |
| `K2_active` | `L1 + lambda2 L2` | non-covering MTP baseline |
| `K3_active` | `L1 + lambda2 L2 + lambda3 L3` | covering condition |

Primary initialization:

```text
identical_branch / branch-collapsed initialization
```

Random initialization is allowed only as a boundary diagnostic, not as the primary speed claim.

## 4. Metrics

### 4.1 Readout-effective semantic margin

For branch `z`, collect decision-prefix state `h_z=h_T(z)`.

Let `u_z` be the output row for target token `S_z` in the horizon-3 head. Define:

$$
\bar u=\frac1m\sum_z u_z.
$$

Define:

$$
M_Z=\frac1m\sum_z (u_z-\bar u)^\top h_z.
$$

Primary one-step metric:

$$
\Delta M_Z/\eta.
$$

### 4.2 Branch separation energy

$$
E_Z=\frac{1}{2m^2}\sum_{z,z'}\|h_z-h_{z'}\|^2.
$$

Secondary one-step metric:

$$
\Delta E_Z/\eta^2.
$$

### 4.3 Guarded recovery

For short training curves, compute:

$$
Q(t)=\min\{A(t),P(t),S(t)\}.
$$

Where:

- `A(t)`: informative-horizon prediction accuracy from `h_T`;
- `P(t)`: frozen probe accuracy `h_T -> Z`;
- `S(t)`: branch-swap consistency.

### 4.4 Local guard

Report:

```text
Y1 accuracy / CE
Y2 accuracy / CE
Delta local CE after one step
```

## 5. One-Step Diagnostic

For each seed and condition:

1. Initialize the model.
2. Verify leakage gates:

```text
Q(0) near chance
M_Z(0) near 0
E_Z(0) near 0
native informative-horizon accuracy near chance
```

3. Clone the initial model for each condition.
4. Compute decision-prefix losses on the same full structured batch.
5. Apply exactly one controlled SGD step:

$$
\theta^+=\theta-\eta\nabla_\theta L_K.
$$

Use a small step-size grid:

```text
eta in {1e-4, 3e-4, 1e-3}
```

The primary theorem comparison should be stable across at least two small `eta` values.

6. Record:

```text
Delta_M_over_eta
Delta_E_over_eta2
Delta_Q
Delta_Y1_CE
Delta_Y2_CE
Delta_native_h3_accuracy
||grad_L1||, ||grad_L2||, ||grad_L3||
```

## 6. Optional Gradient Projection Diagnostics

Compute loss-component gradients separately before the update:

```text
g1 = grad L1
g2 = grad L2
g3 = grad L3
```

Compute:

```text
<grad M_Z, g1>, <grad M_Z, g2>, <grad M_Z, g3>
<grad E_Z, g1>, <grad E_Z, g2>, <grad E_Z, g3>
cos(g1,g3)
norm ratios ||g3||/||g1||
```

Do not treat cosine sign alone as a decision metric.

## 7. Short Training Curve

After the one-step diagnostic, run a short decision-only curve:

```text
steps: 0 to 2000
eval interval: 50 or 100
seeds: 971, 972, 973, 974, 975
```

Report:

```text
M_Z(t)
E_Z(t)
Q(t)
T_0.9
AUC_Q over early window
Y1/Y2 local guard
native horizon-3 accuracy
```

## 8. Pass / Fail Criteria

### Pass

A11_06 supports the one-step efficiency mechanism if:

```text
K3 Delta_M_over_eta > 0 and clearly above K1/K2
K1/K2 Delta_M_over_eta near 0
K3 Delta_E_over_eta2 > K1/K2
local Y1/Y2 CE does not degrade materially
short curve shows earlier M_Z/Q movement for K3
leakage gate passes
```

### Weaken

The mechanism is weakened if:

```text
K3 does not improve Delta_M_Z over K1/K2
K1/K2 show the same margin growth without a leakage explanation
local CE worsens materially
Q(0) is saturated, making speed uninterpretable
```

### Insufficient Evidence

If one-step metrics pass but short curves do not separate, claim only first-order margin advantage, not multi-step efficiency.

## 9. Output Artifacts

Required:

```text
summary.md
detailed.md
metrics_one_step.csv
metrics_short_curve.csv
condition_summary.csv
figures/margin_one_step.png
figures/margin_curves.png
figures/q_curves.png
figures/local_guard.png
run_config.json
```

`summary.md` should answer first with `Delta_M_over_eta`, not final Q.

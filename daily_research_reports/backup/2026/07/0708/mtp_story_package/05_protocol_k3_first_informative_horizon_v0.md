# Protocol B: K=3 First-Informative-Horizon Experiment

Version: v0  
Linked anchor: `04_anchor_k3_first_informative_horizon_v0.md`

---

## 1. Goal

Test whether semantic learning improves exactly when next-$K$ covers the first informative horizon $\tau$.

---

## 2. Dataset

### 2.1 Clean tau=3 regime

Template:

```text
BR_z F00 F01 ... F{L-1} U00 U01 A_SHARED C_SHARED S_z STOP
```

Evaluation prefix stops after:

```text
BR_z F00 F01 ... F{L-1} U00 U01
```

Targets:

```text
offset 1 = A_SHARED
offset 2 = C_SHARED
offset 3 = S_z
```

Information structure:

$$
I(Z;Y_1)=0,
$$

$$
I(Z;Y_2\mid Y_1)=0,
$$

$$
I(Z;Y_3\mid Y_1,Y_2)>0.
$$

Thus $\tau=3$.

---

## 3. Controls

### 3.1 Tau=2 positive control

```text
BR_z ... U00 U01 A_SHARED S_z STOP
```

Confirms the existing K=2 mechanism.

### 3.2 Redundant horizon-3 control

```text
BR_z ... U00 U01 A_SHARED S_z T_z STOP
```

Here $Y_2$ already reveals $Z$, so $Y_3$ should add little new semantic information beyond K=2.

### 3.3 Noisy horizon-3 control

```text
BR_z ... U00 U01 A_SHARED C_SHARED NOISE_r STOP
```

Here $Y_3\perp Z$. K=3 should not improve branch-specific semantic prediction.

### 3.4 Leakage control

Randomize filler and shared context while ensuring no branch identity is encoded in token positions, token frequencies, or local template variants.

---

## 4. Model conditions

Use the same base architecture with heads up to horizon 3. Change only active losses.

| condition | active horizons | expected in tau=3 clean regime |
|---|---:|---|
| K=1 / NTP | 1 | no direct semantic supervision |
| fixed K=1 with 3 heads | 1 | capacity control |
| K=2 | 1,2 | still no direct semantic supervision |
| K=3 | 1,2,3 | direct semantic supervision |
| separate-expert K=3 | 1,2,3 | optional interference diagnostic |

---

## 5. Suggested default settings

| parameter | value |
|---|---:|
| num_branches | 4 or 8 |
| filler_length | 16, 32, 64 |
| shared_context_length | 2 or 4 |
| vocab_size | 96 to 160 |
| layers | 1 |
| d_model | 64 or 128 |
| attention_heads | 1 or 2 |
| batch_size | 128 or 256 |
| steps | 10k to 30k |
| learning_rate | 1e-3 or 3e-4 |
| seeds | at least 5 |
| lambda_2, lambda_3 | 0.25, 0.5, 1.0 |

---

## 6. Metrics

### 6.1 Informative-horizon metrics

```text
native_head3_accuracy
native_head3_target_probability
worst_branch_head3_probability
branch_swap_consistency_for_Sz
```

For K=1/K=2 models that do not train head3, use a matched frozen evaluation decoder/probe for fairness.

### 6.2 Representation metrics

```text
frozen_probe_hT_to_Z_accuracy
frozen_probe_hT_to_Z_cross_entropy
branch_representation_separation
```

### 6.3 Guarded semantic score

$$
Q_K(t)=\min\{A_K(t),P_K(t),S_K(t)\}.
$$

Here $A_K(t)$ uses horizon 3:

```text
A_K(t) = accuracy of h_T -> S_z
```

### 6.4 Local guards

```text
Y1_accuracy
Y1_loss
Y2_accuracy
Y2_loss
global_next_token_loss
```

K=3 must not win by damaging shared local prediction.

### 6.5 Gradient diagnostics

Compute:

```text
cosine_L1_L3_by_parameter_group
cosine_L2_L3_by_parameter_group
norm_ratio_L3_L1
rho_13 = <g1 + lambda3 g3, g1> / ||g1||^2
U3 = cos(grad branch recovery, grad L3)
```

The key diagnostic is $U_3>0$ in the clean tau=3 regime.

---

## 7. Expected result patterns

### Strong support for first-informative-horizon theory

```text
K=1: Q low
K=2: Q low or similar to K=1
K=3: Q high
K=3 reaches threshold earlier or uniquely reaches threshold
Y1/Y2 local guards pass
U3 positive
```

### Leakage or shortcut warning

```text
K=2 Q high in tau=3 clean regime
```

Inspect:

```text
Y2 accidentally branch-specific
token frequency leakage
position leakage
branch-specific filler leakage
initial embedding leakage
```

### Optimization failure

```text
K=3 has direct target but Q remains low
```

Interpretation: objective-level theorem holds, but model/optimizer cannot use the supervision under current settings. Test larger d_model, lambda schedule, or separate experts.

---

## 8. Required plots

1. $Q_1(t),Q_2(t),Q_3(t)$ on same axis.
2. head-3 / evaluation-horizon-3 accuracy over steps.
3. branch-swap consistency over steps.
4. frozen probe accuracy over steps.
5. local $Y_1,Y_2$ losses over steps.
6. $U_3(t)$ over steps.
7. gradient cosines by parameter group.

---

## 9. Output table

```text
seed
condition
regime
T_0.9
AUC_Q
final_Q
Y1_acc_final
Y2_acc_final
head3_acc_final
probe_acc_final
swap_final
U3_mean_early
U3_mean_mid
cos_L1_L3_attention_mean
cos_L2_L3_attention_mean
```

---

## 10. Decision rule

Proceed to general NextK theorem/experiment if:

1. tau=2: K=2 beats K=1.
2. tau=3: K=3 beats K=1 and K=2.
3. Redundant/noisy controls do not show false positives.
4. Local guards pass.

If this holds, the main story becomes:

> MTP improves long-horizon semantic learning when its horizon covers the first future token or token set that reveals the early semantic variable.


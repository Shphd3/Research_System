# Protocol A: K=2 Semantic Efficiency Curves

Version: v0  
Linked anchor: `02_anchor_k2_semantic_efficiency_v0.md`

---

## 1. Goal

Test whether next-two prediction learns the early semantic variable faster or more robustly than NTP / fixed next-one in the K=2 construction.

---

## 2. Dataset

### 2.1 Clean branch-specific regime

Template:

```text
BR_z F00 F01 ... F{L-1} U00 U01 A_SHARED S_z STOP
```

Evaluation prefix stops after:

```text
BR_z F00 F01 ... F{L-1} U00 U01
```

Targets:

```text
offset 1 = A_SHARED
offset 2 = S_z
```

Information:

$$
I(Z;Y_1)=0,
\qquad
I(Z;Y_2\mid Y_1)>0.
$$

### 2.2 Redundant control

```text
BR_z ... U00 U01 S_z T_z STOP
```

Here $Y_1=S_z$, and $Y_2=T_z$ is determined once $Y_1$ is known. This tests whether the second-token target adds new semantic information.

### 2.3 Noisy control

```text
BR_z ... U00 U01 A_SHARED NOISE_r STOP
```

Here $Y_2\perp Z$. This tests whether auxiliary future loss can be useless or noisy.

---

## 3. Model conditions

Use matched architecture whenever possible.

| condition | active loss | purpose |
|---|---|---|
| NTP baseline | ordinary next-token | rollout/local baseline |
| fixed next-one with two heads | offset 1 only | controls extra head capacity |
| shared-trunk next-two | offset 1 + offset 2 | main MTP condition |
| shared-attention separate-expert next-two | offset 1 + offset 2 | tests whether expert separation reduces conflict |

For the first pass, fixed next-one vs shared-trunk next-two is mandatory; separate expert is optional.

---

## 4. Suggested default settings

| parameter | value |
|---|---:|
| num_branches | 4 |
| filler_length | 16, 32, 64 |
| shared_context_length | 2 or 4 |
| vocab_size | 64 to 128 |
| layers | 1 |
| d_model | 64 or 128 |
| attention_heads | 1 or 2 |
| batch_size | 128 or 256 |
| steps | 5k, 10k, 20k |
| learning_rate | 1e-3 or 3e-4 |
| seeds | at least 5 |
| lambda_2 | 0.25, 0.5, 1.0 |

---

## 5. Training variants

Run both:

1. **Decision-only objective**: loss only at the selected prefix state. This matches the theorem.
2. **All-position objective**: LM-style losses at all valid positions. This tests robustness to background local losses.

---

## 6. Logged metrics

### 6.1 Local metrics

```text
Y1_accuracy_structured
Y1_loss_structured
global_next_token_loss
```

These are local guards.

### 6.2 Semantic prediction metrics

```text
native_head2_accuracy
native_head2_target_probability
worst_branch_head2_probability
branch_swap_consistency
branch_suffix_exact_match
```

### 6.3 Representation metrics

```text
frozen_probe_hT_to_Z_accuracy
frozen_probe_hT_to_Z_cross_entropy
branch_representation_separation
```

Probe must be evaluated on frozen model states with the same probe capacity across conditions.

### 6.4 Guarded semantic score

Compute

```text
Q(t) = min(native_or_eval_informative_accuracy, frozen_probe_accuracy, branch_swap_consistency)
```

Recommended thresholds:

```text
theta = 0.9
consecutive_evals = 3
```

Report:

```text
T_theta
AUC_Q
final_Q
```

### 6.5 Gradient diagnostics

At profiling intervals, compute separate gradients for $L_1$ and $L_2$ without changing training.

```text
cosine_L1_L2_embedding
cosine_L1_L2_attention
cosine_L1_L2_mlp
norm_ratio_L2_L1
rho = <g1 + lambda g2, g1> / ||g1||^2
```

Also compute gradient usefulness:

$$
U_2=\frac{\langle \nabla_{\theta_s}R_\phi,\nabla_{\theta_s}L_2\rangle}{\|\nabla_{\theta_s}R_\phi\|\|\nabla_{\theta_s}L_2\|}.
$$

Positive $U_2$ means descending $L_2$ locally reduces branch-recovery loss.

---

## 7. Expected outcomes

### Strong support

```text
next-two reaches Q>=0.9 earlier than fixed next-one
next-two has higher AUC_Q
Y1 accuracy remains matched
U2 is positive in clean regime
noisy control head2 remains near chance
```

### Weak support

```text
next-two final Q is higher, but time-to-threshold is not clearly better
```

This supports representation benefit but not strong efficiency.

### Failure

```text
fixed next-one matches next-two on Q(t)
or next-two wins only by hurting Y1 loss
or noisy control also shows high Q
```

---

## 8. Required plots

1. $Q(t)$ over steps.
2. native head-2 accuracy over steps.
3. frozen probe accuracy over steps.
4. branch-swap consistency over steps.
5. $Y_1$ loss / accuracy over steps.
6. gradient usefulness $U_2(t)$.
7. gradient cosine by parameter group.

---

## 9. Output table

Report per regime and condition:

```text
seed
condition
regime
T_0.9
AUC_Q
final_Q
Y1_acc_final
Y1_loss_final
head2_acc_final
probe_acc_final
swap_final
U2_mean_early
U2_mean_mid
cos_L1_L2_attention_mean
```

---

## 10. Decision rule

Proceed to K=3 if:

1. K=2 theorem pattern is replicated;
2. semantic score is guarded by prediction + probe + branch-swap;
3. local loss guard passes;
4. noisy and redundant controls behave differently from clean branch-specific regime.


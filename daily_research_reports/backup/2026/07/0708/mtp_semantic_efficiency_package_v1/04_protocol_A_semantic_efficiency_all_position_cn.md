# Protocol A: Semantic Efficiency Under All-Position Training

Status: draft v1
Anchor: Direct Supervision to Semantic Efficiency Bridge
Purpose: test whether MTP's direct long-horizon supervision becomes faster/stabler learning

---

## 1. Question

在受控 all-position LM-style training 中，覆盖第一个语义显现位置 `tau` 的 MTP 是否比 NTP / non-covering K 更快、更稳地让 `h_T` 恢复早期语义变量 `Z`，并且不损害本地 next-token 学习？

---

## 2. Core claim tested

理论已证明：

\[
K\ge\tau,
\quad
Y_\tau=S_Z,
\quad
\mathbb E[-\log q_\tau(S_Z\mid h_T)]\le\varepsilon
\Rightarrow
I(h_T;Z)\ge H(Z)-\varepsilon.
\]

本 protocol 测试额外问题：

> 这个直接表示要求是否转化为更快或更稳定的学习？

---

## 3. Dataset regimes

### Regime 1: K=2 clean, tau=2

Template:

```text
BR_z F00 ... F{L-1} U00 U01 U02 U03 A_SHARED S_z STOP
```

Decision prefix ends after `U03`.

Targets:

```text
Y1 = A_SHARED
Y2 = S_z
```

Information structure:

\[
I(Z;Y_1)=0,
\]

\[
I(Z;Y_2\mid Y_1)=H(Z).
\]

### Regime 2: K=3 clean, tau=3

Template:

```text
BR_z F00 ... F{L-1} U00 U01 U02 U03 A_SHARED C_SHARED S_z STOP
```

Targets:

```text
Y1 = A_SHARED
Y2 = C_SHARED
Y3 = S_z
```

Information structure:

\[
I(Z;Y_1)=0,
\]

\[
I(Z;Y_2\mid Y_1)=0,
\]

\[
I(Z;Y_3\mid Y_1,Y_2)=H(Z).
\]

### Controls

#### Noisy informative horizon

Replace `S_z` with random noise independent of `Z`:

```text
Y_tau = NOISE_r,  NOISE_r ⟂ Z
```

Expected: no valid semantic recovery.

#### Redundant earlier target

Make an earlier target already reveal `Z`:

```text
Y2 = S_z, Y3 = T_z
```

Expected: K=2 should already recover `Z`; K=3 should not be interpreted as new first-informative-horizon evidence.

---

## 4. Model conditions

Use identical architecture whenever possible.

| Condition | Active horizons | Purpose |
|---|---:|---|
| K1_fixed_multihead | 1 | NTP-like baseline with same extra heads |
| K2_active | 1,2 | next-two |
| K3_active | 1,2,3 | next-three / covering tau=3 |
| optional standard LM | 1 with ordinary LM head | rollout baseline |

Critical comparisons:

```text
Tau=2: K1 vs K2
Tau=3: K1 vs K2 vs K3
```

Architecture default:

```text
one-layer causal Transformer
one attention head or two heads
d_model = 64
same tokenizer / vocab / optimizer / schedule
same future heads present in fixed baselines
```

---

## 5. Training scope

Primary scope: all-position LM-style objective.

\[
L_K^{all}=\sum_t\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_t),X_{t+j}).
\]

Reason: this tests the boundary where NTP can learn indirectly through other positions.

Decision-only can be kept as a sanity check but should not be the main efficiency claim.

---

## 6. Default run parameters

| Parameter | Default |
|---|---:|
| num branches | 4 |
| filler length | 16, 64 |
| shared context length | 4 |
| training steps | 15000 or 30000 |
| eval interval | 250 or 500 |
| seeds | 971, 972, 973, 974, 975 |
| init | identical_branch + random |
| lambda_2 | 0.25, 0.5, 1.0 |
| lambda_3 | 0.25, 0.5, 1.0 |
| optimizer | AdamW |
| learning rate | 1e-3 and 3e-4 |

Do not sweep too many knobs at once. First decide the clean setting.

---

## 7. Primary metric

Define guarded semantic recovery score:

\[
Q_K(t)=\min\{A_K(t),P_K(t),S_K(t)\}.
\]

Where:

```text
A_K(t): informative-horizon prediction accuracy from h_T
P_K(t): frozen evaluation probe accuracy h_T -> Z
S_K(t): branch-swap consistency
```

Reason for min:

- probe alone can be false positive;
- native head alone can hide shortcut;
- branch-swap guards causal sensitivity to `Z`.

### Time-to-threshold

\[
T_\theta(K)=\inf\{t:Q_K(t)\ge\theta \text{ for } r \text{ consecutive checkpoints}\}.
\]

Recommended:

```text
theta = 0.9
r = 3
```

### Early AUC

\[
\operatorname{AUC}_Q(K)=\frac{1}{T_{max}}\int_0^{T_{max}}Q_K(t)dt.
\]

Use checkpoint average in implementation.

---

## 8. Local-loss guard

MTP counts as better only if it does not damage local learning.

Report:

```text
Y1 accuracy / CE at decision prefix
Y2 accuracy / CE when Y2 is shared or local
global next-token CE
structured-position next-token CE
```

Pass guard:

\[
L_{local}^{MTP}\le L_{local}^{NTP}+\epsilon_{local}.
\]

Recommended:

```text
epsilon_local = 0.02 CE or task-specific 1-2% relative tolerance
```

If MTP improves `Q` but fails local guard, claim tradeoff, not efficiency.

---

## 9. Gradient usefulness diagnostic

At profiling checkpoints, compute on the same batch:

\[
g_1=\nabla_\theta L_1,
\]

\[
g_\tau=\nabla_\theta L_\tau.
\]

Fit or maintain evaluation branch-recovery loss:

\[
R_\phi=\operatorname{CE}(s_\phi(h_T),Z).
\]

Compute:

\[
U_\tau=\langle\nabla_\theta R_\phi,g_\tau\rangle.
\]

Interpretation:

```text
U_tau > 0: descending informative future loss reduces semantic recovery loss
U_tau <= 0: target may be informative but update is not helping h_T recover Z
```

Also compute local compatibility:

\[
c_{1\tau}=\frac{\langle g_1,g_\tau\rangle}{\|g_1\|\|g_\tau\|}.
\]

and preservation:

\[
\rho=\frac{\langle g_1+\lambda_\tau g_\tau,g_1\rangle}{\|g_1\|^2}.
\]

Negative `c` is not automatically bad; interpret with local guard and `U_tau`.

---

## 10. Required plots

```text
Q_K(t) by condition
A_K(t), P_K(t), S_K(t) separately
T_theta by condition
AUC_Q by condition
Y1/Y2 local guard curves
U_tau over training
c_1tau and rho over training
seed-level spaghetti plots for Q_K(t)
```

---

## 11. Pass / fail criteria

### Strong support

```text
covering K reaches T_theta earlier than all non-covering conditions
covering K has higher AUC_Q
local guard passes
U_tau > 0 for the informative horizon
noisy control stays low under guarded Q
redundant control behaves according to earlier informative target
```

Claim:

> MTP's direct supervision becomes a learning-efficiency advantage in this controlled LM-style task.

### Partial support

```text
covering K final Q high, but T_theta and AUC not better
```

Claim:

> Representation requirement holds; efficiency not established.

### Boundary / failure

```text
NTP or non-covering K matches covering K on T_theta, AUC_Q, final Q, and local guard
```

Claim:

> In this controlled setup, indirect NTP/shared-parameter transfer is sufficient; MTP's advantage is not observed as efficiency.

### Harmful tradeoff

```text
MTP improves Q but worsens Y1/Y2 local losses
```

Claim:

> MTP adds useful long-horizon signal but with optimization interference; may motivate expert separation or scheduling.

---

## 12. Required output artifacts

```text
metrics_by_checkpoint.csv
condition_summary.csv
seed_summary.csv
gradient_profile.csv
local_guard.csv
branch_swap.csv
probe_results.csv
run_config.json
learning_curves.png
summary.md
detailed.md
```

`summary.md` should state direct conclusion and primary metric first.
`detailed.md` should contain complete tables, controls, and failure decomposition.

# Anchor: Direct Supervision to Semantic Efficiency Bridge

Status: draft v1
Role: next-decision anchor
Question type: controlled mechanism + efficiency adjudication

---

## researcher judgment record

**Phenomenon.**
MTP 在 K=2/K=3 的受控任务中能把未来 branch-specific token 的监督直接打到当前 prefix state `h_T` 上。NTP 在全位置训练中也可能间接恢复 `Z`，所以现在不能只问“能不能学”，要问“是否更高效、更稳定、更可用地学”。

**Mechanism guess.**
MTP 覆盖第一个语义显现位置 `tau` 时，future-token gradient `g_tau` 直接降低语义恢复损失 `R_phi(h_T,Z)`；如果这个梯度不严重冲突于 next-token gradient `g_1`，则 MTP 应该比 NTP 更快达到 guarded semantic recovery。

**Key variables.**

```text
Z: early semantic variable / branch key
h_T: prefix hidden state
Y_j: j-th future token
tau: first informative horizon
K: active MTP horizon
R_phi: semantic recovery loss from h_T to Z
g_tau: informative future-token gradient
Q(t): guarded semantic recovery score
```

**Causal relation.**

```text
K >= tau
-> active loss includes CE(q_tau(.|h_T), S_Z)
-> h_T receives direct Z-dependent gradient
-> if <grad R_phi, g_tau> > 0 and local guard passes
-> faster / more stable semantic recovery
```

**Primary metric.**

```text
T_theta(K): first step where Q_K(t) >= theta for r consecutive checkpoints
```

Secondary:

```text
AUC_Q(K)
local Y1/Y2 loss guard
gradient usefulness <grad R_phi, g_tau>
representation margin / output alignment
```

**Rival explanations.**

1. NTP all-position losses indirectly recover `Z` through shared parameters.
2. Probe is high but native prediction does not use `Z`.
3. MTP improves `Z` only by hurting local next-token learning.
4. Random initialization or position leakage reveals branch identity.
5. Future token is redundant or noisy, not a true long-horizon semantic target.

**Decision rule.**

Support efficiency claim only if covering-MTP beats NTP/non-covering K on `T_theta` or AUC while preserving local loss and passing branch-swap / native informative prediction guards.

---

## 1. Decision question

Does MTP's direct future-token supervision translate into faster, more stable, and more usable long-horizon semantic representation learning than NTP under controlled LM-style training?

More concretely:

> When `Y_tau=S_Z` is the first future token that reveals early semantic variable `Z`, does next-`K` with `K>=tau` reach guarded semantic recovery faster or with higher early AUC than NTP / `K<tau`, without degrading local next-token learning?

---

## 2. Parent problem and current position

Parent problem:

```text
How to prove MTP is better than NTP for learning long-horizon semantic information?
```

Current position:

1. K=2 proof shows direct representation requirement.
2. K=3 first-informative-horizon shows the mechanism generalizes beyond next2 in decision-only scope.
3. All-position control shows NTP/non-covering K can indirectly recover `Z`, so the stronger claim “only covering MTP can learn” is false in LM-style training.
4. Therefore the next claim must be efficiency and usability, not possibility.

---

## 3. Definitions

| Term | Plain meaning | Concrete object | Why it matters | Cannot prove |
|---|---|---|---|---|
| `Z` | early semantic variable | branch key `B` | target long-horizon information | natural-language semantics by itself |
| `h_T` | prefix state | state after shared local context | carrier of early semantic info | whole-model knowledge |
| `Y_j` | future token | `X_{T+j}` | active target for horizon `j` | full suffix semantics |
| `tau` | first informative horizon | `min{j:I(Z;Y_j|Y_<j)>0}` | decides whether K covers semantic target | fixed in real language |
| covering | MTP includes `tau` | `K>=tau` | direct `Z` supervision exists | optimization success |
| semantic recovery | can recover `Z` from `h_T` | probe / native head / swap | primary evidence | downstream utility |
| local guard | local next-token not hurt | Y1/Y2 loss/acc | rules out tradeoff | all performance preservation |

---

## 4. Core mathematical model

Early variable:

\[
Z\sim \operatorname{Unif}\{1,\ldots,m\}.
\]

Prefix state:

\[
h_T=f_\theta(X_{\le T}).
\]

Future tokens:

\[
Y_j=X_{T+j}.
\]

First informative horizon:

\[
\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}.
\]

Clean deterministic target:

\[
Y_\tau=S_Z,
\]

with one-to-one map `Z -> S_Z`.

Next-K objective:

\[
L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j).
\]

---

## 5. Known theorem layer

### Theorem A: Direct representation requirement

If `K>=tau`, `Y_tau=S_Z`, and

\[
\mathbb E[-\log q_\tau(S_Z\mid h_T)]\le \varepsilon,
\]

then

\[
I(h_T;Z)\ge H(Z)-\varepsilon.
\]

Meaning:

> Successful covering-MTP forces current state `h_T` to contain early semantic variable `Z`.

### Theorem B: Non-covering targets need not force `Z`

If

\[
I(Z;Y_{1:K})=0,
\]

then a `Z`-blind `h_T` can be Bayes-optimal for those active targets.

Meaning:

> If the active horizon never reaches a token that needs `Z`, the objective has no direct semantic requirement on `h_T`.

---

## 6. New bridge layer: from direct supervision to efficiency

Define semantic recovery loss:

\[
R_\phi(\theta)=\operatorname{CE}(s_\phi(h_T(\theta)),Z).
\]

Define gradients:

\[
g_1=\nabla_\theta L_1,
\qquad
g_\tau=\nabla_\theta L_\tau.
\]

MTP update:

\[
g_{MTP}=g_1+\lambda_\tau g_\tau.
\]

### Proposition C: First-order semantic efficiency gain

If

\[
\langle\nabla_\theta R_\phi,g_\tau\rangle\ge \gamma>0,
\]

then, for small `eta`, MTP reduces semantic recovery loss more than NTP by approximately

\[
\eta\lambda_\tau\gamma.
\]

This is the minimal theorem that links direct supervision to efficiency.

### Local preservation condition

If

\[
\langle g_1,g_\tau\rangle\ge -\rho\|g_1\|^2/\lambda_\tau,
\qquad \rho<1,
\]

then the combined MTP update still preserves local next-token progress to first order.

---

## 7. Falsifiable hypotheses

### H1: Faster acquisition

Covering MTP has smaller time-to-threshold:

\[
T_\theta(K\ge\tau)<T_\theta(K<\tau).
\]

### H2: More stable early learning

Covering MTP has higher early area:

\[
\operatorname{AUC}_Q(K\ge\tau)>\operatorname{AUC}_Q(K<\tau).
\]

### H3: More usable representation

Covering MTP improves at least two of:

```text
future-token logit margin
branch-output alignment
linear probe margin
branch-swap consistency
route NMI with Z
route margin
```

### H4: Local learning preserved

MTP does not degrade local prediction:

```text
Y1/Y2 loss and accuracy match NTP/non-covering K within epsilon_local
```

### H5: Gradient usefulness

The informative future-token gradient has positive semantic-recovery projection:

\[
\langle\nabla R_\phi,g_\tau\rangle>0.
\]

---

## 8. Minimal tests

This anchor owns two protocols.

### Protocol A: Semantic efficiency under all-position training

Decides whether direct supervision yields faster/stabler recovery.

Primary metric:

```text
T_theta and AUC_Q
```

### Protocol B: Representation form, gradient usefulness, and gateability

Decides whether the recovered information is easier to discover, more output-facing, and more gateable.

Primary metric:

```text
output-facing branch margin + route_NMI / route margin + gradient usefulness
```

---

## 9. Supported / weakened / insufficient outcomes

### Supported

```text
covering MTP reaches Q threshold earlier or has higher AUC_Q
local guard passes
gradient usefulness positive
representation margin/alignment better
noisy and redundant controls do not give false positives
```

Claim:

> MTP's direct semantic supervision translates into more efficient and more usable long-horizon semantic representation learning in this controlled setting.

### Weakened

```text
covering MTP final Q high, but T_theta and AUC match NTP
```

Claim:

> Direct representation requirement holds, but efficiency advantage is not established.

### Falsified for efficiency

```text
NTP/non-covering K matches MTP on Q(t), T_theta, AUC, representation margin, and local guard
```

Claim:

> In this setup, NTP's indirect path is efficient enough; MTP's deterministic advantage remains only a target-level representation constraint.

### Harmful tradeoff

```text
MTP improves Q but degrades Y1/Y2 local loss
```

Claim:

> MTP trades local learning for long-horizon representation; not a clean efficiency win.

---

## 10. Claim boundary

Can claim after current theory:

```text
MTP has direct representation-supervision advantage when it covers the first informative future token.
```

Can claim after this anchor passes:

```text
In controlled all-position training, that direct supervision yields faster/stabler and more usable long-horizon semantic representation under guarded metrics.
```

Cannot claim:

```text
MTP always beats NTP.
NTP cannot learn long-horizon semantics.
Larger K is always better.
Synthetic branch results prove natural-language gains.
Gateability proves real MoE expert utility.
```

---

## 11. Exactly one next decision

Run the two protocols needed to decide:

> Does MTP's proven direct long-horizon semantic supervision become an efficiency and representation-usability advantage under controlled LM-style training?

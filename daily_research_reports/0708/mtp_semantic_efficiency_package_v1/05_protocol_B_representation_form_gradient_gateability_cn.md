# Protocol B: Representation Form, Gradient Usefulness, and Gateability

Status: draft v1
Anchor: Direct Supervision to Semantic Efficiency Bridge
Purpose: test whether MTP makes long-horizon semantic information more discoverable, readout-effective, stable, and gateable

---

## 1. Question

MTP 学到的长程语义信息是否比 NTP 更容易在表征空间中发现、更稳定地固定，并且更容易被输出头或 MoE gate 使用？

This protocol targets the user's directions 2 and 3:

1. representation form: is `Z` more discoverable and stable in `h_T`?
2. gradient usefulness: does the informative future-token loss make `Z` more useful to the model without hurting next-token learning?
3. gateability: can the recovered `Z` support MoE-like routing surfaces?

---

## 2. Input runs

Use checkpoints from Protocol A.

Required conditions:

```text
K1_fixed_multihead
K2_active in tau=2
K1/K2/K3 in tau=3
noisy control
redundant control
```

Required scopes:

```text
all-position LM-style training
optionally decision-only for mechanism sanity
```

Do not run a new broad training sweep before analyzing these checkpoints.

---

## 3. Main objects

| Object | Meaning | Measurement |
|---|---|---|
| `h_T` | prefix state | hidden vector after shared local context |
| `Z` | early semantic variable | branch label |
| `S_Z` | informative future token | target at horizon tau |
| output direction | direction selecting suffix token | `w_{S_z}-w_{S_z'}` |
| gate direction | linear route row | learned linear classifier or MoE gate row |
| semantic margin | how separable branches are | logit / probe / gate margins |

---

## 4. Representation-discoverability metrics

### 4.1 Frozen probe accuracy and CE

Train a linear probe:

\[
s_\phi(h_T)\to Z.
\]

Report:

```text
probe_accuracy
probe_CE
probe_margin
```

Probe margin:

\[
M_{probe}=\mathbb E[\ell_Z(h_T)-\max_{z'\ne Z}\ell_{z'}(h_T)].
\]

### 4.2 Probe sample efficiency

Train probes with different numbers of labeled examples:

```text
n = 4, 8, 16, 32, 64, all per branch
```

If MTP representation is easier to discover, it should need fewer probe examples to reach the same accuracy.

Metric:

```text
probe_T_theta_data: minimum labeled examples needed for probe acc >= theta
```

### 4.3 Stability over training

For each checkpoint, compute branch means:

\[
\mu_z(t)=\mathbb E[h_T\mid Z=z].
\]

Branch separation:

\[
D_h(t)=\frac{1}{m(m-1)}\sum_{z\ne z'}\|\mu_z(t)-\mu_{z'}(t)\|^2.
\]

Sign-flip / assignment stability:

```text
train a linear probe at checkpoint t
measure whether class ordering / separating direction remains stable at t+1
```

Report:

```text
branch_mean_drift
probe_direction_cosine_between_checkpoints
classification_sign_flip_rate
```

---

## 5. Readout-effective representation metrics

Probe accuracy alone is insufficient. `Z` must be useful for predicting the future semantic token.

### 5.1 Future-token logit margin

For each branch `z`:

\[
M_{out}(z)=\ell_{S_z}(h_z)-\max_{y\ne S_z}\ell_y(h_z).
\]

Report:

```text
mean_output_margin
worst_branch_output_margin
margin_std_across_branches
```

### 5.2 Branch-output alignment

For two branches `z,z'`:

\[
\Delta h_{z,z'}=\mu_z-\mu_{z'}.
\]

Output separating direction:

\[
\Delta w_{z,z'}=w_{S_z}-w_{S_{z'}}.
\]

Alignment:

\[
A_{out}=\frac{\langle \Delta h_{z,z'},\Delta w_{z,z'}\rangle}{\|\Delta h_{z,z'}\|\|\Delta w_{z,z'}\|}.
\]

Report mean and worst-pair alignment.

Interpretation:

```text
high probe + low output alignment = Z exists but not output-effective
high probe + high output alignment = Z is usable for future prediction
```

### 5.3 Native-vs-evaluation gap

Compare:

```text
native informative-head accuracy
evaluation decoder/probe-to-S_z accuracy
branch-swap consistency
```

If probe is high but native head or branch-swap low, representation is not yet useful.

---

## 6. Gradient usefulness metrics

At profiling checkpoints compute:

\[
g_j=\nabla_\theta L_j.
\]

Semantic recovery loss:

\[
R_\phi=\operatorname{CE}(s_\phi(h_T),Z).
\]

Main gradient usefulness:

\[
U_j=\langle\nabla_\theta R_\phi,g_j\rangle.
\]

Interpretation under gradient descent:

```text
U_j > 0 means L_j update helps lower branch-recovery loss
U_j < 0 means L_j update locally hurts branch recovery
```

Local compatibility:

\[
c_{1j}=\frac{\langle g_1,g_j\rangle}{\|g_1\|\|g_j\|}.
\]

Preservation:

\[
\rho_j=\frac{\langle g_1+\lambda_jg_j,g_1\rangle}{\|g_1\|^2}.
\]

Compute by parameter group:

```text
embedding
attention
MLP / expert
head_j
```

Do not use negative cosine alone as harm evidence. It must be interpreted with local guard and `U_j`.

---

## 7. Gateability metrics

This is a proxy bridge to MoE / nested-learning relevance.

### 7.1 Linear gate from h_T to Z

Train a top-1 linear gate:

\[
r(h_T)=\arg\max_e W_g h_T.
\]

Evaluate:

```text
route_NMI_with_Z
route_accuracy_to_Z
max_load
load_entropy
route_margin
```

### 7.2 Margin and sign flip

Gate margin:

\[
M_{gate}=\ell_{route=Z}(h_T)-\max_{e\ne Z}\ell_e(h_T).
\]

Sign flip rate:

```text
fraction of examples crossing gate boundary across adjacent checkpoints
```

MTP should ideally show:

```text
higher route NMI
larger route margin
lower sign flip rate
matched local loss
```

### 7.3 Common/local conflict guard

Because the broader MoE line cares about routing collapse and common components, also measure:

```text
all-position route NMI vs decision-prefix route NMI
common-subtracted route NMI if a common operator is defined
route load balance
LM loss
```

Boundary:

```text
This does not prove real expert utility.
It only shows that MTP makes the controlled semantic variable more routeable.
```

---

## 8. Expected outcomes

### Outcome A: MTP gives usable semantic representation

Pattern:

```text
MTP > NTP on probe margin
MTP > NTP on output alignment
MTP > NTP on output margin
MTP > NTP on route_NMI and route margin
U_tau > 0
local guard passes
```

Claim:

> MTP makes long-horizon semantic information more discoverable, more readout-effective, and more gateable in this controlled setting.

### Outcome B: MTP stores Z but not usefully

Pattern:

```text
probe high
native informative-head / branch-swap / output margin low
```

Claim:

> MTP improves hidden recoverability but not readout-effective semantics.

### Outcome C: MTP helps Z but conflicts locally

Pattern:

```text
probe/output/gate metrics improve
local Y1/Y2 loss worsens
c_1tau strongly negative
rho low or negative
```

Claim:

> MTP provides useful semantic signal but creates shared-trunk interference; consider expert separation or schedule.

### Outcome D: NTP matches MTP

Pattern:

```text
NTP/non-covering K matches MTP on probe, output margin, gateability, and local guard
```

Claim:

> In this setup, indirect NTP learning forms an equally usable representation; MTP's advantage remains only direct target-level supervision.

---

## 9. Required plots and tables

```text
probe accuracy vs labeled examples
probe margin over training
output margin over training
branch-output alignment over training
route_NMI over training
route margin over training
sign flip rate over training
U_tau over training
local loss guard over training
parameter-group gradient cosine heatmap
```

Tables:

```text
final representation table by condition
best checkpoint representation table
seed mean/std
control regime table
```

---

## 10. Pass / fail criteria

### Pass for direction 2

MTP has better discoverability/stability:

```text
lower probe sample requirement
higher probe margin
lower sign flip
higher branch separation
```

### Pass for direction 3

MTP has more useful semantics:

```text
higher output margin
higher branch-output alignment
higher route_NMI / route margin
U_tau > 0
local guard passes
```

### Fail / boundary

If metrics improve only in probe but not output/gate/swap:

```text
claim hidden recoverability only, not usable semantic representation
```

If noisy target also improves route/gate metrics:

```text
metric surface invalid; revise controls before claim
```

---

## 11. Output artifacts

```text
representation_metrics.csv
probe_sample_efficiency.csv
output_alignment.csv
gateability_metrics.csv
gradient_usefulness.csv
condition_summary.md
detailed.md
figures/*.png
```

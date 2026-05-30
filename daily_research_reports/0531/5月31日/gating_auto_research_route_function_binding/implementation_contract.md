# Implementation Contract: Route-Function Binding Auto Research

## 1. Required objects

```text
Sample metadata:
  slot_id
  family_id
  b_identity_id
  frequency_rank
  distribution_weight
  target_token_id

Model outputs:
  target_logits
  router_logits
  router_probs
  selected_expert
  expert_target_logits or expert_loss_by_expert
  hidden_state_at_B

Artifacts:
  checkpoints
  per-step metrics
  per-sample metadata + route + utility
  curated tables
  figures
```

## 2. Data generator algorithm

Input:

```text
num_slots S
num_families G
num_b_identities N
num_experts E
seq_len
slot_code_type {repeated, distributed}
distribution {uniform, zipf, zipf_reweight}
zipf_alpha
heldout_b_fraction
seed
```

Steps:

```text
1. Create slot codes C_s.
2. Create family tokens F_g.
3. Create B identity tokens B_i.
4. Define target token Y_{s,g,i} or Y_{s,i}; choose one mapping and write it in config.
5. Sample B_i by selected distribution.
6. Build sequence [common prefix, slot code, family token, B_i, target].
7. Store metadata for every sample.
8. Split train/valid/heldout by B identity and perturbation pairs.
```

Pass conditions:

```text
same B_i under different slot has different target;
same slot under different B_i has same target factor class or controlled target mapping;
heldout B identities exist;
frequency counts match requested distribution;
metadata fully reconstructs generation factors.
```

Fail conditions:

```text
target can be predicted from B identity alone in the slot test;
slot factor does not affect target;
frequency distribution not verified;
metadata missing for factor attribution.
```

## 3. 2x2 NTP sanity algorithm

Objects:

```text
features: x0=[1,0], x1=[0,1]
targets: y0=A, y1=B
gate: W_g in R^{2x2}
expert utility matrix: R[e,y]=P_e(y|x)
```

Loss:

$$
L=-\frac{1}{2}\sum_i \log \sum_e g_e(x_i)R[e,y_i].
$$

Gate gradient:

$$
\frac{\partial L_i}{\partial z_e}=g_e-\rho_e,
\quad
\rho_e=\frac{g_eR[e,y_i]}{\sum_k g_kR[k,y_i]}.
$$

Required cases:

```text
complementary: R=[[0.99,0.01],[0.01,0.99]]
identical: R=[[0.50,0.50],[0.50,0.50]]
same_best: R=[[0.99,0.99],[0.01,0.01]]
weak_complementary: R=[[0.60,0.40],[0.40,0.60]]
```

Outputs:

```text
tables/2x2_ntp_sanity.csv
figures/2x2_gate_margin_curve.png
```

## 4. Factor attribution algorithm

Inputs:

```text
hidden_state_at_B: H
router_logits: L
metadata factors: slot, family, identity, frequency_rank, common_condition
```

Methods:

```text
1. Fit linear probes from factor one-hot / embeddings to router logits.
2. Compute R2 per factor and combined factor set.
3. Compute MI / NMI between selected_expert and each factor.
4. Estimate factor subspace P_F using class means or probe directions.
5. Remove factor subspace from h and recompute route logits if router is linear, or run a forward hook if available.
6. Report route flip rate after removing each factor.
```

Pass conditions:

```text
R2 and removal flip identify a dominant factor with stable results across seeds.
```

Fail conditions:

```text
no factor explains route above random controls;
selected route NMI and logit R2 disagree without explanation;
factor removal invalidates model computation.
```

## 5. Expert utility algorithm

Forced expert CE:

```text
For each feature f and expert e:
  force route to e at target position;
  compute CE on samples with feature f.
```

Ablation utility:

```text
For each feature f and expert e:
  ablate expert e at target position or zero its contribution;
  compute ΔCE = CE_ablate - CE_full.
```

Assignment-utility agreement:

```text
For each sample:
  route = selected_expert
  utility_best = argmin_e forced_CE[feature, e]
  agreement = route == utility_best up to global permutation if needed
```

Permutation matching:

```text
Use Hungarian matching on validation forced_CE or route-feature count matrix.
Report both raw and permutation-matched metrics.
```

## 6. Residual router implementation

Common subspace:

```text
Compute mean hidden state by common condition or global top principal components.
P_C = top-k PCA directions or supervised common probe directions.
h_res = h - P_C h.
```

Frequency subspace:

```text
Compute head-rank mean / PCA directions from top frequency samples.
P_H = top-k directions.
h_leaf = h - P_H h.
```

Controls:

```text
random subspace with same rank;
slot subspace removal as negative control;
identity subspace removal;
matched parameter count baseline.
```

## 7. Consistency regularization implementation

Pair construction:

```text
same_feature_pairs: same slot, different B identity / common / family.
different_feature_pairs: same B identity/family if possible, different slot.
```

Loss:

$$
L=L_{NTP}+\lambda_{same}L_{same}+\lambda_{diff}L_{diff}+\lambda_{lb}L_{load}.
$$

Debug:

```text
report number of valid pairs;
report same-feature route consistency;
report different-feature route separation;
verify target labels are not leaked into inference input.
```

## 8. Responsibility binding implementation

Responsibility target:

$$
\rho_e=\frac{g_eP_e(y|x)}{\sum_k g_kP_k(y|x)}.
$$

Loss:

$$
L_{bind}=\operatorname{CE}(\operatorname{stopgrad}(\rho), g).
$$

Safeguards:

```text
load balance;
minimum route entropy during warmup;
feature-balanced batches;
track early collapse;
do not let binding target update before experts have nontrivial utility.
```

## 9. Stability metrics

Training stability:

```text
route_flip_rate(t,t+Δ) after permutation matching;
assignment NMI across checkpoints;
expert utility diagonal consistency across checkpoints.
```

Inference stability:

```text
same-feature augmentation consistency;
different-feature separation;
heldout B identity route-feature NMI;
route confidence calibration.
```

Seed stability:

```text
match feature-expert assignments across seeds with Hungarian algorithm;
report mean and worst seed-pair agreement.
```

## 10. Required final artifact map

```text
anchor:
execution_plan:
summary:
detailed:
code workspace:
runner:
configs:
key code files:
data manifest:
result dir:
figure dir:
key tables:
logs/checkpoints:
repro command:
job id:
commit hash:
```

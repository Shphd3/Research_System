# A06_01 Protocol: Common-Filtered Expert-Spectrum Router Initialization

## 0. Goal

Test whether the advisor-style idea, "initialize the router from expert high-singular/high-gain directions," becomes useful when common directions in the initial router-input representation are removed or isolated.

The protocol has three linked phases:

1. **Audit:** Are expert high-gain directions distinct, common-dominated, residual-aligned, or utility-predictive?
2. **Implementation:** Can the spectrum/residual scores be converted into actual linear top-1 router weights?
3. **Training:** Do the initialized routers change the 0--300 step early-training path, especially step-10 common-logit amplification and gate-hidden interaction?

## 1. Fixed Experimental Contract

### Model

```text
model_family: Qwen-style decoder-only MoE
initialization: random
num_hidden_layers: 6
hidden_size: 512
num_attention_heads: 8
num_key_value_heads: 4
num_experts: 8
expert_hidden_dim: 2048
router_type: bias-free linear gate
top_k: 1
use_shared_expert: false
lambda_lb: 0.0
norm_topk_prob: false
pretrained: false
```

### Data

```text
data: DCLM packed text
train_sequences: 32768
init_sequences: 8192     # used to estimate C, residual geometry, and spectrum-to-linear assignments
audit_sequences: 8192    # disjoint from init_sequences; used for reported metrics
sequence_length: 256 input tokens + shifted next-token targets
padding: none
```

### Training

```text
max_train_steps: 300
learning_rate: 3e-4
seeds: 0, 1, 2
checkpoints: 0, 1, 2, 3, 5, 10, 20, 50, 100, 200, 300
hardware: 4-GPU ACP run
execution: full run, not smoke
```

### Audit object

```text
H_l: exact tensor entering the active linear gate at layer l
W_l: linear gate matrix at layer l
E_{l,e}: expert e in layer l
c_l: mean router input over init/audit tokens
C_l: rank-q common subspace estimated from H_l, q in {1, 4, 8}
r_i = (I - P_C) h_i
```

Every reported router logit must satisfy:

```text
max_abs(H_l W_l^T - logged_router_logits) = 0.0 or numerically negligible
```

## 2. Expert-Spectrum Definition

The expert is a gated FFN, not a single linear matrix. The primary feasible implementation uses an input-side effective linear approximation.

For expert `e` in layer `l`, define the input-side energy matrix:

```math
G_{l,e} = W_{gate,l,e}^T W_{gate,l,e} + W_{up,l,e}^T W_{up,l,e}.
```

Let:

```math
S_{l,e,k} = span(top-k eigenvectors of G_{l,e}).
```

Use:

```text
k in {1, 4, 8, ceil(0.01 * hidden_size)}
primary k = ceil(0.01 * hidden_size)
```

Secondary validation, if runtime allows:

```text
sampled_local_jacobian_svd on layers 3--5, subset of init tokens
```

This secondary audit checks whether the input-stack approximation agrees with the actual local Jacobian direction.

## 3. Phase A: Spectrum / Common / Utility Audit

### A1. Spectrum-common overlap

Question:

```text
Are expert top high-gain directions mostly common directions, residual directions, or distinct expert-specific directions?
```

For each layer `l`, expert `e`, and k:

```math
overlap(S_{l,e}, C_l) = ||S_{l,e}^T C_l||_F^2 / k.
```

Report:

```text
mean_overlap_with_C
max_overlap_with_C
inter_expert_overlap = mean_{e!=f} ||S_e^T S_f||_F^2 / k
common_contamination_ratio
```

Interpretation:

```text
High overlap(S_e, C): raw spectrum is likely common-contaminated.
Low overlap + high inter-expert diversity: spectrum may contain expert-specific routing signal.
```

### A2. Raw vs residual spectrum score audit

For token input `h_i`:

```math
s_e^raw(h_i) = ||P_{S_e} h_i||^2
s_e^res(h_i) = ||P_{S_e} (I - P_C) h_i||^2.
```

Report:

```text
oracle_raw_load
oracle_residual_load
fraction_assignments_changed_by_filtering
raw_score_common_margin
residual_score_common_margin
raw_vs_residual_top1_agreement
```

Interpretation:

```text
If raw score produces high common-margin/load and residual score changes assignments, common filtering is necessary.
```

### A3. Forced-routing utility correlation

Question:

```text
Does spectrum score predict whether a token benefits from expert e?
```

Procedure:

```text
Use a fixed subset from the audit split.
For each sampled token, layer, and expert e:
  force routing at layer l to expert e;
  run the forward pass with only that routing change;
  record next-token loss or local output utility.
```

Utility:

```math
u_{i,e} = - loss_{i,e}^{forced}
```

Metrics:

```text
spearman_corr(s_e^raw, u_e)
spearman_corr(s_e^res, u_e)
top1_spectrum_matches_top1_utility
mean_utility_gap_between_spectrum_top1_and_random
```

Interpretation:

```text
Positive residual-spectrum utility correlation supports expert-spectrum routing.
No correlation weakens the method even if load improves.
```

## 4. Phase B: Router Initialization Variants

All variants use the same non-router model initialization for a given seed. Router rows are normalized to match the default gate row norm:

```text
target_row_norm = mean row norm of default random gate at initialization
```

All variants are initialized layer-by-layer. For layer `l`, compute `H_l` using already-initialized earlier layers, estimate `C_l`, construct the layer-l gate, then continue to the next layer.

### V0: random_init

Default Qwen-style random gate. Baseline.

### V1: common_orthogonal_random_init

Project random router rows away from the estimated common subspace:

```math
w_e <- (I - P_C) w_e^{random}
```

Then normalize row norms.

Purpose:

```text
Test whether common control alone helps without expert spectrum.
```

### V2: representation_residual_init

Use only initial representation geometry.

Procedure:

```text
Compute residuals r_i = (I - P_C) h_i.
Cluster residuals into E clusters or use residual PCA directions.
Set router rows to residual cluster centroids / spread directions.
Normalize row norms.
```

Purpose:

```text
Test whether initial representation geometry alone is sufficient.
```

### V3: raw_spectrum_linear_init

Direct expert-spectrum initialization.

For each expert:

```math
q_e^{raw} = normalize( sum_{j=1}^{k} sigma_{e,j} * sign(mean_i h_i^T v_{e,j}) * v_{e,j} )
w_e <- q_e^{raw}
```

Purpose:

```text
Closest direct implementation of the advisor's raw top-spectrum idea.
```

### V4: common_filtered_spectrum_linear_init

Common-filtered version of V3.

```math
q_e^{res} = normalize((I - P_C) q_e^{raw})
w_e <- q_e^{res}
```

Additionally report:

```text
var_e(w_e^T c)
```

Purpose:

```text
Test advisor-style expert-spectrum initialization after common removal.
```

### V5: hybrid_spectrum_to_linear_init

This is the primary implementation candidate.

Step 1: compute oracle residual-spectrum assignment:

```math
a_i = argmax_e ||P_{S_e}(I - P_C)h_i||^2.
```

Step 2: compress oracle assignment into a linear router:

```math
w_e = normalize(mean_{i: a_i=e} r_i).
```

Fallback for empty assignments:

```text
use q_e^{res} from V4.
```

Optional stronger version:

```text
fit a ridge / linear classifier from r_i to a_i, then use classifier rows as router weights.
```

Report:

```text
oracle_to_linear_top1_agreement
empty_assignment_count
linear_init_train_accuracy_on_init_features
```

Purpose:

```text
Bridge the quadratic subspace score into the current linear top-1 router.
```

## 5. Phase C: Full 0--300 Step Training Comparison

### Conditions

Run full training for:

```text
V0 random_init
V1 common_orthogonal_random_init
V2 representation_residual_init
V3 raw_spectrum_linear_init
V4 common_filtered_spectrum_linear_init
V5 hybrid_spectrum_to_linear_init
```

Each condition:

```text
seeds: 0, 1, 2
checkpoints: 0, 1, 2, 3, 5, 10, 20, 50, 100, 200, 300
4-GPU DDP
same data contract as A06_02
```

### Primary metrics

Report for all layers, with late-layer summary for layers 3--5:

```text
common_margin
residual_margin
dominance_ratio
raw_max_load
centered_max_load
delta_max_load
effective_experts
routing_entropy
LM loss
```

### Replay decomposition

For each variant, compute:

```math
Z_{a,b}=H_b W_a^T
A_actual = common_margin(W10,H10) - common_margin(W0,H0)
A_gate = common_margin(W10,H0) - common_margin(W0,H0)
A_hidden = common_margin(W0,H10) - common_margin(W0,H0)
A_interaction = A_actual - A_gate - A_hidden
```

Primary comparison:

```text
late-layer mean A_actual
late-layer mean A_interaction
step10 raw_max_load_delta
step10 effective_experts
step10 and step300 LM loss
```

### Step-0 implementability metrics

For each variant at step 0:

```text
raw_max_load
centered_max_load
common_margin
residual_margin
empty_expert_count
effective_experts
var_e(w_e^T c)
row_norm_mean / row_norm_std
```

### Utility metrics

For V0, V3, V4, V5:

```text
forced-routing utility correlation at step 0
forced-routing utility correlation at step 10
spectrum_top1_matches_utility_top1
```

## 6. Success / Weakening / Redirection Criteria

### Supported

Expert-spectrum initialization is supported if:

```text
1. expert subspaces are distinct;
2. common-filtered spectrum score has higher utility correlation than raw score;
3. V4 or V5 reduces late-layer step10 A_actual and A_interaction vs V0;
4. LM loss is not worse by more than 5% at step 300;
5. effective experts increase without only moving collapse to another metric.
```

### Raw-spectrum failure, filtered success

Interpretation:

```text
Advisor intuition is directionally right, but raw top-spectrum is common-contaminated.
Next method: common-filtered residual-spectrum routing.
```

### Representation-only success

If V2 beats V4/V5:

```text
Initial representation geometry matters more than expert spectrum in this setup.
Anchor should shift toward representation-aware common-controlled initialization.
```

### All spectrum variants fail

If V3/V4/V5 fail utility correlation and do not reduce A_interaction:

```text
Expert top spectrum is not a supported routing prior in this setting.
Do not claim expert singular directions are useful features.
```

### Load-only improvement

If a variant improves max_load but not utility correlation or replay interaction:

```text
This is load balancing, not supported specialization or mechanism improvement.
```

## 7. Required Artifacts

Write these files:

```text
config/run_config.json
config/source_manifest.json
results/spectrum_common_overlap.csv
results/oracle_spectrum_assignment.csv
results/forced_utility_correlation.csv
results/step0_init_metrics.csv
results/trajectory_metrics.csv
results/replay_metrics.csv
results/replay_fraction_summary.csv
results/variant_summary.csv
figures/step10_common_margin_by_variant.png
figures/step10_raw_max_load_by_variant.png
figures/replay_A_interaction_by_variant.png
summary.md
detailed.md
```

`summary.md` must answer:

```text
Which variant reduces step-10 common amplification?
Does expert spectrum predict forced-routing utility?
Did common filtering help relative to raw spectrum?
Is the result a method improvement, a load-only improvement, or a failed prior?
```

## 8. Main Claim Boundary

Can claim if supported:

```text
In this small random-initialized Qwen-style DCLM top-1 MoE setting, common-filtered expert-spectrum initialization changes the early routing path relative to random initialization.
```

Cannot claim:

```text
expert singular directions are semantic features;
this solves MoE collapse;
load balance equals specialization;
results transfer to pretrained large MoEs;
common filtering alone is sufficient;
expert-output feedback has been fully explained.
```

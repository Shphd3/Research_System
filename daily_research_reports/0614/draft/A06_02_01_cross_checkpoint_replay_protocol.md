# A06_02_01 Cross-Checkpoint Replay and Freeze-Split Protocol

## Goal

Decompose early common-logit amplification in real-text sparse top-1 MoE into three causal paths:

1. gate-weight update;
2. hidden-state producer drift;
3. expert-output feedback / selected-path co-adaptation.

This protocol extends the previous real-text audit to a full 300-step trajectory and uses cross-checkpoint replay before heavier freeze interventions.

## Decision Question

In real DCLM top-1 MoE, is the step-10 / early common-logit amplification mainly produced by gate update, hidden-state drift, expert-output feedback, or their interaction?

## Setup

Keep the previous real-text audit contract:

```text
data: DCLM packed text
model: small random-initialized Qwen-style decoder-only MoE
router: linear bias-free sparse top-1
top_k: 1
use_shared_expert: false
lambda_lb: 0.0
norm_topk_prob: false
audit object: exact tensor passed into the active linear gate
training length: 300 optimizer steps
fixed audit batch: yes
```

The audit batch must be fixed across all checkpoints and variants.

## Checkpoints

Required checkpoints:

```text
0, 1, 2, 3, 5, 10, 20, 50, 100, 200, 300
```

Minimum acceptable if runtime is tight:

```text
0, 1, 10, 50, 100, 300
```

## Saved Objects

For each seed, layer, checkpoint, and fixed audit batch, save:

```text
H_t: exact router input hidden states
W_t: gate weight matrix
Z_t = H_t W_t^T: active router logits
route_ids_t: top-1 selected expert IDs
c_t = mean_i H_t[i]
R_t = H_t - c_t
LM loss
router gradient norm
expert gradient norm
hidden norm / common norm
```

Sanity check:

```text
max_abs(H_t W_t^T - logged_router_logits) <= 1e-6
```

If this fails, the replay decomposition is invalid.

## Phase A: Normal 300-Step Trajectory

### Question

Does the previous step-10 amplification reproduce over a longer 300-step trajectory?

### Metrics

Primary:

```text
common_margin_t
residual_margin_t
dominance_ratio_t = common_margin_t / residual_margin_t
raw_max_load_t
centered_max_load_t
delta_max_load_t = raw_max_load_t - centered_max_load_t
```

Secondary:

```text
routing_entropy_t
active_experts_ratio_t
dominant_expert_persistence_t
cos(c_t, c_0)
subspace_overlap(C_t, C_0)
LM loss
```

### Expected Pattern

The expected baseline pattern is not monotonic. The previous run suggests:

```text
step 0: common component is a load-bias source, but not the dominant margin source.
step 10: common-logit concentration spikes strongly.
step 300: route concentration may relax but remains biased.
```

## Phase B: Cross-Checkpoint Gate-Hidden Replay

### Question

Where does amplification live: in gate weights, hidden states, or their interaction?

### Replay Definition

For every pair of checkpoints `(a, b)`:

```text
Z_{a,b} = H_b W_a^T
```

Compute the same metrics on `Z_{a,b}` as in Phase A.

### Main Replay Conditions

```text
W0_H0      = initial baseline
W10_H10    = actual early amplified state
W300_H300  = late trajectory state
W10_H0     = gate-update-only replay
W0_H10     = hidden-drift-only replay
W10_cH10   = actual gate with centered H10
W0_cH10    = initial gate with centered H10
W10_cH0    = updated gate with centered H0
```

Here `cH_t = H_t - mean_i H_t[i]`.

### Amplification Fractions

Use `common_margin` as the primary scalar `M`, because `dominance_ratio` can explode when residual margin becomes small.

```text
A_actual = M(W10, H10) - M(W0, H0)
A_gate   = M(W10, H0)  - M(W0, H0)
A_hidden = M(W0, H10)  - M(W0, H0)

F_gate   = A_gate   / A_actual
F_hidden = A_hidden / A_actual
F_interaction = 1 - F_gate - F_hidden
```

Also report the same fractions for:

```text
raw_max_load
centered_max_load
delta_max_load
log dominance_ratio
```

## Phase C: Freeze-Split Runs

Run these only after Phase B, unless implementation is already available.

### Variant 1: normal_train

```text
all parameters train
```

Purpose: reproduce the baseline 300-step trajectory.

### Variant 2: freeze_gate

```text
gate weights fixed at W0
all other trainable parameters unchanged
```

Question: Is gate update necessary for step-10 amplification?

Expected interpretation:

```text
if amplification is suppressed: gate update is necessary.
if amplification persists: hidden drift / expert feedback can create concentration under fixed gate.
```

### Variant 3: freeze_experts

```text
expert MLP weights fixed at initialization
gate and non-expert parameters train
```

Question: Is expert-output co-adaptation necessary?

Expected interpretation:

```text
if amplification is suppressed: selected expert updates contribute to feedback.
if amplification persists: gate / hidden producer path is sufficient.
```

### Variant 4: freeze_hidden_producer

Implementation depends on model code. Preferred target:

```text
freeze embeddings, attention, layernorms, and upstream blocks that produce each audited MoE gate input
train gate and experts where possible
```

Question: Can gate/expert learning amplify common logits when the router-input distribution is mostly fixed?

If exact freeze is hard, replace with replay-only evidence from Phase B and mark this variant as not implemented.

### Optional Variant 5: block_expert_output_feedback

Candidate implementations:

```text
A. use frozen expert outputs but allow gate training;
B. detach expert output before residual addition;
C. replace MoE output with zero / dense fallback only for diagnostic runs.
```

This is diagnostic only. It may alter LM loss and should not be interpreted as a deployable method.

## Supported / Weakened Outcomes

### Outcome A: gate-update dominant

Supported if:

```text
W10_H0 reproduces most W10_H10 common_margin amplification.
freeze_gate suppresses step-10 dominance_ratio and raw_max_load.
```

Interpretation:

```text
gate update is sufficient and necessary for the early common-logit jump.
```

### Outcome B: hidden-drift dominant

Supported if:

```text
W0_H10 reproduces most W10_H10 amplification.
freeze_hidden_producer suppresses amplification.
```

Interpretation:

```text
upstream representation drift creates a more common-dominated router input.
```

### Outcome C: expert-feedback dominant

Supported if:

```text
freeze_experts or block_expert_output_feedback strongly suppresses amplification,
while W10_H0 and W0_H10 alone are both insufficient.
```

Interpretation:

```text
selected expert outputs participate in the amplification loop.
```

### Outcome D: interaction dominant

Supported if:

```text
W10_H0 and W0_H10 each explain only a minority of amplification,
but W10_H10 is large.
```

Interpretation:

```text
early concentration requires co-adaptation between gate update and representation drift.
```

### Outcome E: centering removes the spike

Supported if:

```text
W10_cH10 sharply lowers raw_max_load and common_margin relative to W10_H10.
```

Interpretation:

```text
the step-10 concentration remains common-channel mediated.
```

### Outcome F: centering fails

Supported if:

```text
W10_cH10 remains concentrated.
```

Interpretation:

```text
mean common removal is insufficient; inspect higher-rank common subspace, position buckets, or residual anisotropy.
```

## Insufficient Evidence Conditions

The experiment is insufficient if any of the following holds:

```text
1. H_t is not the exact active gate input.
2. The audit batch changes across checkpoints or variants.
3. Only max_load is reported without common-logit decomposition.
4. shared expert is enabled.
5. load-balance loss is enabled unless explicitly tested.
6. reconstruction error between replay logits and router logits is non-negligible.
7. only one seed/layer is reported.
8. Phase B and Phase C disagree but no implementation sanity check is provided.
```

## Deliverables

```text
summary.md: decision-level result, one table per phase
detailed.md: full metric tables, replay heatmaps, seed/layer breakdown
figures/: trajectory curves, W_a H_b replay heatmaps, freeze comparison plots
run_config.json: exact model/data/router/training config
source_manifest.json: code checksum and patch list
```

## Minimal Report Table

| Question | Metric | Support | Weaken |
|---|---|---|---|
| Is step-10 amplification reproduced? | common_margin, raw_max_load | spike near step 10 | flat trajectory |
| Does gate update explain it? | F_gate, freeze_gate | high F_gate + freeze suppresses | low F_gate + freeze no effect |
| Does hidden drift explain it? | F_hidden, freeze_hidden_producer | high F_hidden + freeze suppresses | low F_hidden + freeze no effect |
| Does expert feedback matter? | freeze_experts / block feedback | suppression | no effect |
| Is it common-channel mediated? | W10_cH10 | centering suppresses | centering fails |

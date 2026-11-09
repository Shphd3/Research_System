# Implementation Resolution: Real-Text Common-Logit Audit

Source protocol:

- `daily_research_reports/0611/draft/06_protocol_1.md`

Primary anchor lineage:

- `Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_02_dotproduct_common_logit_causality_anchor.md`

## 1. Decision

The full experiment is allowed after the source runner is patched to make the
router surface match the protocol exactly.

The main run must use:

- no shared expert path;
- actual linear gate input as `h_i`;
- non-oracle hidden-state gating reference;
- `top_k = 1`;
- `lambda_lb = 0.0`;
- dedicated small random-init config;
- DCLM packed-stream manifest with 257-token span and 256-token input;
- all 256 input tokens counted as valid;
- exact audit checkpoints from a callback or custom short loop;
- source identity from git hash when available, otherwise checksums.

## 2. Required Source Patch

Patch `/data/250010109/MoE_Router/src/model/qwen3_moe` and
`/data/250010109/MoE_Router/train_qwen3_moe.py` with three explicit controls.

### 2.1 Shared Expert Switch

Add config and CLI field:

```text
use_shared_expert = false for main audit
```

Implementation contract:

- if `use_shared_expert=false`, do not instantiate `shared_expert`, or return a
  zero tensor in its place;
- log `use_shared_expert=false`;
- preflight must fail if `use_shared_expert` is missing or true for the main
  audit.

Reason:
The always-on shared path is a non-routed computation channel and contaminates
expert-underuse interpretation.

### 2.2 Router Input Capture

Define `h_i` as the exact tensor passed into the active linear gate:

```text
router_input_for_metrics = input tensor to self.gate(...)
router_logits_for_metrics = self.gate(router_input_for_metrics)
```

For the main audit, force:

```text
router_type = linear
router_center_input = false
router_aux_gate = false
router_acp_transform = false
gating_reference = hidden_states
moe_type = moe
```

Then `h_i` is the post-attention, post-`post_attention_layernorm` hidden state
inside the MoE block, immediately before the linear gate.

Implementation contract:

- store or stream per-layer `router_input_for_metrics` in fp32 accumulation;
- store or stream the corresponding linear gate weight `W`;
- verify `router_logits == h @ W.T` with max reconstruction error threshold
  `<= 1e-5` in fp32;
- record layer id, model seed, step, and token count for every metric row.

### 2.3 Exact Audit Checkpoints

Do not rely on checkpoint save interval for Phase 3.

Implementation contract:

- use a short training loop or callback that runs the audit at
  `[0, 1, 10, 50, 100, 300]`;
- step 0 audit must happen after random initialization and before the first
  optimizer update;
- step 1 audit must happen after exactly one optimizer step;
- save audit metrics even if no model checkpoint is written.

## 3. Dedicated Config

Create a dedicated config directory, not the existing 16-layer H512 config.

Main config:

```text
hidden_size = 512
num_hidden_layers = 6
num_attention_heads = 8
num_key_value_heads = 8 or 4, but record exact value
head_dim = 64
intermediate_size = 2048 or explicitly recorded dense MLP fallback
moe_intermediate_size = 2048
attention_dropout = 0.0
torch_dtype = bfloat16
vocab_size = 151936
```

Fallback config:

```text
hidden_size = 256
num_hidden_layers = 4
num_attention_heads = 4
num_key_value_heads = 4 or 2, but record exact value
moe_intermediate_size = 1024
```

Validity rule:
Changing to fallback does not invalidate Phase 1/2 if it is recorded before
the run, but Phase 3/4 must not mix main and fallback configs in the same
summary curve.

## 4. Data Manifest

Use deterministic DCLM packed-stream samples:

```text
span_length = 257
input_length = 256
target_length = 256
sample_stride = 257
```

Each sample row must record:

```json
{
  "dataset": "DCLM-bin",
  "shard_path": "...",
  "loader_sample_index": 0,
  "start_token_offset": 0,
  "global_token_offset": 0,
  "span_length": 257,
  "input_token_start_delta": 0,
  "input_token_count": 256,
  "target_token_start_delta": 1,
  "target_token_count": 256,
  "sample_stride": 257
}
```

Audit split:

```text
samples 0..8191
```

Training split:

```text
samples 8192..40959
```

All 256 input positions are valid tokens. Do not drop token id 0 as padding.

## 5. Metric Definitions

Primary decomposition:

```text
c = mean_i h_i
r_i = h_i - c
common_logit_e = w_e^T c
residual_logit_i,e = w_e^T r_i
```

Primary metrics:

```text
common_margin = top1(common_logit) - top2(common_logit)
residual_margin = mean_i[top1(residual_logit_i) - top2(residual_logit_i)]
dominance_ratio = common_margin / max(residual_margin, 1e-8)
common_winner_agreement = mean_i[argmax_e(w_e^T h_i) == argmax_e(w_e^T c)]
max_load
routing_entropy
active_experts
active_experts_ratio
gini_load
```

Centered counterfactual:

```text
h_centered = h_i - c
route_centered = argmax_e w_e^T h_centered
```

## 6. Additional Issues And Fixed Solutions

### 6.1 Top-1 Expert Output Weighting

Issue:
Current code multiplies expert output by the selected softmax probability.
For route assignment this is harmless, but for Phase 3 training dynamics it is
the differentiable path by which task loss reaches the router logits.

Solution:
For the main early-training audit, keep `norm_topk_prob=false` with `top_k=1`
and record:

```text
top1_expert_output_weight = selected_softmax_probability
```

Reason:
If `norm_topk_prob=true` with `top_k=1`, the selected probability is divided by
itself, so the expert output weight becomes constant 1. Since top-1 expert
selection is discrete, this removes the main differentiable task-loss gradient
to the router. That would turn Phase 3 into a nearly frozen-router audit and
would not test ordinary early training dynamics.

Boundary:
Phase 1 and Phase 2 route-assignment metrics use logits and argmax only, so
they are not affected by expert-output probability weighting.

This is intentional: the non-selected router logits should receive gradients
through the softmax denominator. That is the ordinary differentiable update
path for a linear softmax router before the discrete top-1 dispatch.

### 6.2 Real Gate Scale vs Virtual Router Scale

Issue:
Phase 2 samples virtual routers with `N(0, 1/d)`, while the real gate uses the
model initializer. These scales are not automatically identical.

Solution:
Record both:

```text
real_gate_weight_std_per_layer
virtual_router_std = 1 / sqrt(d)
```

Report Phase 2 as a scale-controlled geometry probe. For comparability, include
one virtual setting whose sampled weight standard deviation matches each
layer's real gate weight standard deviation.

### 6.3 LayerNorm Location

Issue:
The hidden state before the MoE block and the actual gate input differ because
the decoder applies `post_attention_layernorm`.

Solution:
Only use the tensor captured at the linear gate input. Do not use
`output_hidden_states` from the model API as `h_i` unless a reconstruction test
proves it is the same tensor.

### 6.4 Multihead MoE Exclusion

Issue:
`moe_type=multihead` changes the routing input dimension and expert-label
shape.

Solution:
Main run must set:

```text
moe_type = moe
moe_head_num ignored
```

### 6.5 Position Aggregation Rule

Issue:
In a language-modeling sequence, every input token position is routed. Choosing
only one position would make the result depend on an arbitrary probe location.

Solution:
Primary Phase 1/2 metrics aggregate over all 256 input positions for every
sample:

```text
positions = 0..255
valid_token_mask = all ones
```

Diagnostics must also report position buckets:

```text
bucket_0 = positions 0..63
bucket_1 = positions 64..127
bucket_2 = positions 128..191
bucket_3 = positions 192..255
```

Optional diagnostic:
compute per-position common vectors `c_p = mean_batch h_{batch,p}` to separate
global common bias from position-specific routing bias. This is diagnostic
only; the primary claim uses all routed input tokens.

### 6.6 Baseline 3 Cost

Issue:
Full covariance-matched zero-mean Gaussian can be expensive.

Solution:
Keep Baseline 3 optional. If run, use a recorded low-rank covariance
approximation with a fixed rank and seed. Do not make Baseline 3 required for
Phase 1/2 support.

## 7. Preflight Pass Conditions

Before full run, preflight must show:

```text
data path exists
manifest span_length = 257
sample_stride = 257
linear router bias = false
use_shared_expert = false
gating_reference = hidden_states
router_type = linear
router_center_input = false
router_aux_gate = false
router_acp_transform = false
top_k = 1
lambda_lb = 0.0
norm_topk_prob = false for Phase 3/4 main early-training audit
dedicated config path recorded
audit checkpoint callback available
source identity recorded by git hash or checksum
```

## 8. Recommendation

Proceed in two implementation steps:

1. Patch the source and write a tiny smoke run that audits one batch, one layer,
   one seed, and verifies `router_logits == h @ W.T`.
2. After the smoke passes, run Phase 1 and Phase 2 first. Start Phase 3/4 only
   after the checkpoint callback produces exact step audits.

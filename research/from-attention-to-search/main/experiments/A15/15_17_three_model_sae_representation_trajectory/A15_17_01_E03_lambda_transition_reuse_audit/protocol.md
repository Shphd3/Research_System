# Protocol: A15_17_01_E03 Lambda-Transition Reuse Audit

> Document status: `APPROVED_FOR_DIRECT_FULL_EXECUTION`.
> Scientific status: measurement is approved; the mechanism judgment remains
> with the researcher after the result is read.

## 0. Approval and scope

- Primary Anchor: `15_17_01_sae_shared_direction_reuse_anchor.md`.
- This is a bounded follow-up under the same Anchor, not a new training run.
- The researcher explicitly requested the exact 15B checkpoint before the
  reconstruction-coefficient reduction and the exact 17B checkpoint after it,
  followed by one read-only full run on four RTX5090 GPUs.
- Execution tuple: `5090-4-spot` with `shphd-lite-0911` and the registered
  mounted SM120 runtime. No fallback, retry, checkpoint mutation, training,
  commit, or push is authorized.
- A separate remote Smoke is not submitted in this scope. The direct full run
  must fail closed on its own GPU, loader, numerical, alignment, and
  immutability guards; this is recorded as `NOT_RUN_DIRECT_FULL_USER_REQUEST`,
  not as a Smoke PASS.

## 1. Purpose and question

The purpose is to test whether the observed conjunction of lower native
effective dimension and higher model-local activation reuse is present across
the coefficient-transition boundary:

```text
15B, lambda_rec=1.0, before the fork boundary
        versus
17B, lambda_rec=0.1, after the fork boundary
```

The comparison is a temporal training-history contrast. It is not an isolated
causal estimate of changing `lambda_rec`.

## 2. Hypothesis and rival

### Hypothesis

On the fixed 192-record N8 panel, the post-transition checkpoint should have

1. a larger mean cosine between record-level normalized Top-32 usage profiles,
   and
2. a smaller participation-ratio effective dimension of the same-panel native
   attention-write vectors.

The registered necessary-condition branch is passed only when the paired
2,000-draw bootstrap 95% interval for `post - pre` reuse is entirely above zero
and post effective dimension is lower as a point-estimate gate.

### Strongest rival and boundary

Low dimension can arise from decoder-direction collinearity, coefficient
covariance, or ordinary training-stage drift without increased same-ID support
reuse. The two checkpoints also differ in microbatch partition, gradient
accumulation, CE chunking, optimizer/RNG history, and token coordinate. A
positive branch therefore supports a recurring association only; it does not
identify coefficient reduction as the cause.

## 3. Frozen model identities

| Case | Checkpoint | Tokens | Optimizer step | `lambda_rec` | Role |
|---|---|---:|---:|---:|---|
| `15b_pre_lambda1` | `/data/250010109/MoE_Router/experiments/20260916_attention_output_sidecar_last_50b/runs/formal50b_last_attention_4h100/milestones/token_015000000000` | 15,000,000,000 | 57,224 | 1.0 | requested pre-transition milestone |
| `17b_post_lambda0p1` | `/data/250010109/MoE_Router/experiments/20260917_attention_output_sidecar_last_reweighted_resume/runs/formal50b_last_attention_lambda0p1_mbs16_fork_4h100/milestones/token_017000000000` | 17,000,000,000 | 64,854 | 0.1 | requested post-transition milestone |

The exact fork source is step 59,000 at 15,465,567,744 tokens. Thus the
requested 15B checkpoint is 0.465567744B tokens before the exact boundary and
the requested 17B checkpoint is 1.534432256B tokens after it. Both models have
the same initial tensor/backbone identity, model source hashes, training-data
manifest, tokenizer, layer-7 sidecar site, width 30,000, and native Top-32
configuration. Both nominally preserve 262,144 tokens per optimizer update,
but their microbatch/accumulation/CE-chunk settings differ.

## 4. Data and extraction

- Input: the frozen 192-record N8 panel in the execution manifest; 256 valid
  body tokens per record; 49,152 valid tokens per model; no labels or semantic
  categories enter the executable analysis.
- Native site: `blocks[7].attn.o`, after the attention output projection and
  before residual addition.
- For each valid token, use the model-native encoder's returned Top-32 IDs and
  values. Repeat the same forward pass to test exact read-only reproducibility.
- Pool native attention writes by the fixed body-token mean for each record.
- Use BF16 forward/native encoding, FP32 pooling, and FP64 CPU/GPU statistics.
- Four workers process the same ordered panel in two shards per case; no DDP,
  optimizer update, or checkpoint write is allowed.

## 5. Metrics and decision rule

For record \(i\), let \(u_i\) be the 30,000-dimensional vector of selected-atom
frequencies across its 256 tokens, normalized by `256 x 32`. The primary
contrast is the mean off-diagonal cosine difference

\[
\Delta R = R_{post} - R_{pre}.
\]

The uncertainty unit is the record ID: resample the same 192 IDs for both
conditions 2,000 times with seed `20260922`, and use the percentile 95%
interval. No cross-model atom-ID alignment is performed.

For native means \(a_i\), report

\[
d_{eff}=\frac{\operatorname{tr}(\Sigma)^2}
{\operatorname{tr}(\Sigma^2)},
\]

where covariance is centered over the 192 records. The direction of the
dimension contrast is descriptive and has no separately estimated interval.

### Registered outcome branches

- `POST_HIGHER_REUSE_AND_LOWER_DIMENSION`: CI lower bound `> 0` and
  \(d_{post}<d_{pre}\); necessary-condition pass, not causality.
- `REUSE_INCREASE_WITHOUT_LOWER_DIMENSION`: CI lower bound `> 0` but the
  dimension gate is not met.
- `PRE_HIGHER_REUSE`: CI upper bound `< 0`.
- `LOWER_DIMENSION_WITHOUT_REUSE_INCREASE`: post dimension is lower but the
  reuse CI is not entirely positive.
- `UNRESOLVED_REUSE_DIFFERENCE`: interval includes zero.
- `INSUFFICIENT`: any identity, finite-value, alignment, loader, or artifact
  guard fails.

No branch establishes semantics, utility, downstream performance, or isolated
coefficient causality.

## 6. Required guards and artifacts

The run must leave four worker receipts and native-support arrays, checkpoint
manifest verification, exact panel alignment, finite Top-32 values, zero
non-tie Top-32 disagreements, CPU/GPU Gram and effective-dimension agreement,
exact repeat-forward pooled means, unchanged model state/version/dictionary,
paired bootstrap tables, concentration curves, decision figures, an artifact
hash manifest, and a terminal execution receipt. Missing or ambiguous guards
make the affected result `INSUFFICIENT`.

Execution workspace:
`/data/250010109/MoE_Router/experiments/20260922_s7_lambda_transition_reuse_audit`

The machine-readable freeze is in that workspace's `manifests/` directory;
the submission must use the frozen assets and a unique run root.

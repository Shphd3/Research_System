# Protocol: A15_17_01_E04 Exact-15B Lambda Reuse Comparison

> Document status: `APPROVED_FOR_DIRECT_FULL_EXECUTION`.
> Scientific status: the comparison is approved; mechanism judgment remains
> with the researcher after the result is read.

## 0. Approval and scope

- Primary Anchor: `15_17_01_sae_shared_direction_reuse_anchor.md`.
- This is a same-architecture supporting comparison under the existing Anchor.
- The researcher explicitly requested comparison of the two distinct exact-15B
  S7 models: one trained with `lambda_rec=0.1` and one trained with
  `lambda_rec=1.0`.
- Execution tuple: one `5090-4-spot` node, `shphd-lite-0911`, registered
  mounted SM120 runtime. No fallback, retry, checkpoint mutation, training,
  commit, or push is authorized.
- A separate remote Smoke is not submitted in this direct-full scope. The full
  run must fail closed on GPU identity, checkpoint loader, input alignment,
  numerical, and immutability guards. This is recorded as
  `NOT_RUN_DIRECT_FULL_USER_REQUEST`, not as Smoke PASS.

## 1. Purpose and question

The purpose is to compare the two different exact-15B S7 models at the same
nominal token coordinate:

```text
S7, lambda_rec=1.0, exact 15B
versus
S7, lambda_rec=0.1, exact 15B
```

This removes the 15B-versus-17B endpoint difference used in E03 and keeps the
S7 observation site and architecture fixed. It remains a training-history
contrast because the two runs use different microbatch partitions and have
different optimizer/RNG trajectories.

## 2. Hypothesis and rival

### Hypothesis under the current mechanism

If reducing the reconstruction coefficient produces the proposed shared-atom
route to low native dimension, the `lambda_rec=0.1` model should have

1. higher cross-record cosine similarity of normalized Top-32 usage profiles;
2. lower participation-ratio effective dimension of the same-panel native
   attention-write vectors.

The registered primary contrast is `lambda=0.1 minus lambda=1.0`. The analysis
is two-sided and will report the opposite direction without forcing a positive
result.

### Strongest rival and boundary

Native low dimension may arise from decoder-direction collinearity, coefficient
covariance, residual covariance, or ordinary trajectory differences without
increased same-ID support reuse. The two runs match nominal effective tokens
per source update, initial state identity, data, tokenizer, architecture, and
CE chunking, but use microbatch/accumulation `(32,1)` versus `(2,16)` and do
not establish isolated coefficient causality.

## 3. Frozen model identities

| Case | Checkpoint | Tokens | Optimizer step | `lambda_rec` | Role |
|---|---|---:|---:|---:|---|
| `15b_lambda1` | `/data/250010109/MoE_Router/experiments/20260916_attention_output_sidecar_last_50b/runs/formal50b_last_attention_4h100/milestones/token_015000000000` | 15,000,000,000 | 57,224 | 1.0 | exact-15B S7 coefficient-1 model |
| `15b_lambda0p1` | `/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_015000000000` | 15,000,000,000 | 57,224 | 0.1 | exact-15B S7 coefficient-0.1 model |

Both checkpoints are complete exact-15B milestones with the same initial tensor
and backbone hashes, model source hashes, data manifest, tokenizer, layer-7
sidecar site, width 30,000, K=32, CE chunk size 128, and nominal 262,144
source-training tokens per update. Their microbatch partitions and resulting
training/RNG histories differ.

## 4. Data and extraction

- Input: the frozen 192-record N8 panel; 256 valid body tokens per record;
  49,152 valid tokens per model; no labels enter the executable analysis.
- Native site: `blocks[7].attn.o`, after attention output projection and before
  residual addition.
- For each valid token, use native encoder Top-32 IDs and values. Repeat the
  same forward pass to test exact read-only reproducibility.
- Pool native attention writes by the fixed body-token mean for each record.
- Use BF16 forward/native encoding, FP32 pooling, and FP64 statistics.
- Four independent workers process two shards per condition; no DDP,
  optimizer update, or checkpoint write is allowed.

## 5. Metrics and registered decision rule

For record \(i\), let \(u_i\) be the 30,000-dimensional normalized frequency
vector of selected atom IDs across its 256 tokens and 32 selected slots. The
primary contrast is

\[
\Delta R=R_{\lambda=0.1}-R_{\lambda=1.0},
\]

where \(R\) is the mean off-diagonal cosine between record usage profiles.

The uncertainty unit is the record ID: use 2,000 paired bootstrap draws over
the same 192 records with seed `20260922`. No cross-model atom-ID alignment is
performed.

For native means \(a_i\), report

\[
d_{eff}=\frac{\operatorname{tr}(\Sigma)^2}
{\operatorname{tr}(\Sigma^2)},
\]

with centered covariance over the same 192 records.

### Registered outcome branches

- `LAMBDA01_HIGHER_REUSE_AND_LOWER_DIMENSION`: CI lower bound `> 0` and
  \(d_{0.1}<d_1\); necessary-condition pass, not causality.
- `REUSE_INCREASE_WITHOUT_LOWER_DIMENSION`: CI lower bound `> 0` but the
  dimension gate is not met.
- `LAMBDA1_HIGHER_REUSE`: CI upper bound `< 0`.
- `LOWER_DIMENSION_WITHOUT_REUSE_INCREASE`: \(d_{0.1}<d_1\) but the reuse CI is
  not entirely positive.
- `UNRESOLVED_REUSE_DIFFERENCE`: interval includes zero.
- `INSUFFICIENT`: any identity, alignment, finite-value, loader, or artifact
  guard fails.

No branch establishes semantic quality, utility, downstream performance, or an
isolated causal effect of `lambda_rec`.

## 6. Required guards and artifacts

The run must leave four worker receipts and native-support arrays, checkpoint
manifest verification, exact panel alignment, finite Top-32 values, zero
non-tie Top-32 disagreements, CPU/GPU Gram and effective-dimension agreement,
exact repeat-forward pooled means, unchanged model state/version/dictionary,
paired bootstrap tables, concentration curves, decision figures, an artifact
hash manifest, and a terminal execution receipt. Missing or ambiguous guards
make the measurement `INSUFFICIENT`.

Execution workspace:
`/data/250010109/MoE_Router/experiments/20260922_s7_15b_lambda_compare_reuse_audit`

## Amendment A1 — 2026-09-22T16:28:20Z — researcher-requested two-card engineering Smoke

The first direct-full submission `pt-qyze07hl` was observed by the researcher
as unsuccessful; the verified platform state is `SUSPENDED` with its worker
`Deleted` and no completed application receipt. The researcher then explicitly
requested a separate two-card task to test whether the checkpoint-loading and
native-extraction path can run successfully.

This amendment authorizes **engineering validation only**, not a second
scientific full run and not a replacement for the four-card direct-full
comparison. Use the registered `5090-2-spot` profile and the same image/runtime.
GPU 0 loads `15b_lambda0p1`; GPU 1 loads `15b_lambda1`. Each worker processes
the frozen four smoke batches (16 records, 4,096 body tokens), and checks
checkpoint-manifest loading, native Top-32 extraction, repeated-forward pooled
means, finite positive selected values, input alignment and model/dictionary
immutability. No reuse contrast, bootstrap, effective-dimension verdict or
semantic interpretation is produced.

The two-card task passes only when both worker receipts and the terminal receipt
are complete with zero optimizer updates and all named guards pass. A pass is
runtime evidence, not a scientific result or evidence that the suspended
four-card job would have completed. A failure is preserved as an engineering
diagnostic and does not change the registered E04 scientific branches. The
existing four-card direct-full authorization remains unchanged; no automatic
retry, fallback, checkpoint mutation, training, commit or push is authorized.

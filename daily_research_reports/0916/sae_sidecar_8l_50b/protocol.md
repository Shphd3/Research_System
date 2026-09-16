# Protocol: A8L raw final-Attention-output SAE sidecar 50B

## 0. Approval Snapshot

- Document status: **APPROVED_FOR_IMPLEMENTATION_AND_4H100_SMOKE_THEN_PASS_GATED_50B_SUBMISSION**
- Approval source: researcher messages on 2026-09-16 confirming raw Attention output,
  no sidecar Norm, implementation, Smoke, and a Smoke-PASS-gated full-run submission.
- Experiment role: method construction and training-trajectory collection.
- Purpose: construct one eight-layer model whose final Attention output receives a
  live SAE reconstruction gradient without changing the native LM forward path.
- Condition: one final-layer sidecar; no C/T arms and no second SAE.
- Primary engineering metric: every registered Smoke gate passes.
- Scientific result: `UNKNOWN`; this Protocol does not register semantic-success
  thresholds or treat reconstruction quality as semantic evidence.
- Approved execution: isolated implementation; one four-H100 reserved Smoke; only
  after Smoke `PASS`, submit one fresh 50B run on the same four-H100 reserved profile.
- Unauthorized here: first-layer implementation/Smoke, any eight-5090 run, extra
  conditions/seeds, publication, commit, or push.
- Cannot claim: semantic formation, functional specialization, long-run stability,
  or natural AuxK effectiveness from Smoke or submission health.

## 1. Definitions And Question Boundary

Let `x_7` be the input to Python `blocks[7]`, the eighth Transformer block. Let

$$a_7=\operatorname{Attention}_7(\operatorname{Norm1}_7(x_7))$$

denote the Attention module return after output projection `W_O` and before the
residual addition. The native main path remains

$$r_7=x_7+a_7,\qquad x_8=r_7+\operatorname{MLP}_7(\operatorname{Norm2}_7(r_7)).$$

The SAE sidecar reads `a_7` directly. There is no sidecar normalization and the
SAE reconstruction is not consumed by the main path or inference logits.

The local engineering question is whether this exact computation graph can be
trained, counted, logged, checkpointed, and resumed correctly at the frozen scale.
It is not yet a scientific test of domain-semantic improvement.

## 2. Data And Supervision

- Data: `/data/250010109/training_data_views/dclm_pair_v1/train`.
- Manifest SHA-256:
  `8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d`.
- Tokenizer vocabulary: `/data/share/Qwen3-0.6B-Base`; pretrained model weights
  are not loaded.
- Formal data exposure: fixed 30B continuous prefix, cycled to exactly
  50,000,000,000 valid next-token prediction targets.
- SAE positions: deterministic seed-17 sampling of one eighth of eligible target
  positions. No semantic labels enter training.

## 3. Architecture And Objective

- Backbone: eight layers; hidden1024; FFN3072; Q16/KV8; head dimension128;
  context2048; vocabulary151936; tied embeddings; RoPE theta1e6.
- SAE: one width-30000 Top-32 nonnegative dictionary; no identity skip; no side
  Norm; AuxK256; 10M sampled-position dead window; activity threshold1e-3.
- Parameters: backbone281,431,040; SAE61,471,024; total342,902,064.
- Initialization: fresh random seed17; do not resume from Smoke, serial SAE, or
  retired C/T checkpoints.

For sampled raw Attention outputs $a_i$, the objective is

$$L=L_{\mathrm{LM}}+L_{\mathrm{rec}}+\frac{1}{32}L_{\mathrm{AuxK}}.$$

The SAE encoder input in $L_{\mathrm{rec}}$ is live. Its target copy and target
energy denominator are detached. AuxK receives a detached input and detached
main-reconstruction residual, so it updates SAE parameters only. Global LM loss
uses the valid-target denominator; both SAE terms use the global sampled-position
denominator.

Gradient ownership:

- LM loss: native backbone and tied output weight; no SAE gradient.
- Reconstruction: SAE plus block-7 Attention/Norm1 and all upstream computation;
  no block-7 Norm2/MLP or final-model-Norm gradient.
- AuxK: SAE only.

## 4. Optimization, Coordinates, And Checkpoints

- Four ranks, sequence2048, microbatch2/GPU, gradient accumulation16; nominal
  complete-update global target count262144, with actual non-ignore masks authoritative.
- LM AdamW: lr3e-4, betas(.9,.95), epsilon1e-8, matrix weight decay.1.
- SAE AdamW group: lr3e-4, betas(.9,.999), no weight decay.
- Linear warmup for1000 LM and10 SAE updates, then constant; independent clip1.0.
- Primary curve coordinate: cumulative valid prediction tokens; update secondary.
- Permanent checkpoints: 0/.5/1/3/5/10/15/17/19/.../49/50B. Additional
  .1/.3/7/13B snapshots occur after the first complete update reaching the target.
  Recovery every1000 updates, retaining the latest two.
- TensorBoard under each run's `tensorboard/`, rank0 only, with global LM/total,
  raw and weighted reconstruction/AuxK, both coordinates, learning rates, gradient
  norms, valid-token count, SAE sample count, activity, and throughput.

## 5. Smoke And Scale-Up Rule

Resource: one node, four H100 80GB GPUs, `h100-4-reserved`, image
`shphd-lite-0911`. Smoke runs eight logical updates; it saves at update4,
intentionally exits, resumes in an independent process, and verifies update5.
Full-size forced-dead-mask CUDA qualification is separate from natural activity.

Required gates:

1. `sae_input` equals the actual `blocks[7].attn` return, with no side Norm.
2. Changing SAE parameters leaves LM logits unchanged.
3. LM, reconstruction, and AuxK gradients have exactly the registered owners.
4. Four-rank parameters, activity state, denominators, token/sample counts, and
   required scalars are synchronized and finite.
5. TensorBoard/JSONL tags and token/update coordinates satisfy the repository
   observability contract.
6. Model, optimizer, scheduler, RNG, data/sampling cursor, SAE activity buffers,
   and both coordinates restore; next-update replay passes.
7. `smoke_verification.json` is `PASS` and no failure artifact exists.

Any failed or missing gate stops scale-up. If all pass, submit one fresh 50B job
on `h100-4-reserved` without another approval prompt. Observe only scheduling,
four ranks, first finite update, durable logs/checkpoints, and immediate failure;
then stop polling while the job runs.

After that full-run submission, this reserved H100 resource is unavailable to the
first-layer variant. Its later Smoke may use only `5090-2-spot` and requires its
own isolated implementation and evidence; it is not authorized by this Protocol.

## 6. Artifacts And Failure Boundary

- Execution package:
  `/data/250010109/MoE_Router/experiments/20260916_attention_output_sidecar_last_50b`
- Smoke config: `configs/smoke_4h100_last_attention.json`
- Formal config: `configs/formal_4h100_last_attention_50b.json`
- Smoke run: `runs/smoke_last_attention_4h100_v1`
- Formal run: `runs/formal50b_last_attention_4h100`
- Submission entry point:
  `/data/250010109/Research_System/templates/execution/acp_submit_template.sh`

Failure artifacts are retained. No resource fallback, scale reduction, condition
substitution, resubmission, old C/T launcher, or stale checkpoint reuse is allowed.
Smoke PASS is engineering evidence only; full-run submission is not completion.

## 7. Confirmation And Freeze Ledger

| Block | State | Grounding |
|---|---|---|
| A question/claim boundary | CONFIRMED | method-construction scope; scientific result remains unknown |
| B data/provenance | CONFIRMED | inherited frozen manifest and researcher-approved 50B contract |
| C learning task | CONFIRMED | next-token LM plus unsupervised raw-`a_7` reconstruction |
| D architecture | CONFIRMED | researcher selected raw Attention output and rejected side Norm |
| E objective/optimization | CONFIRMED | live reconstruction, detached target/denominator, SAE-only AuxK; inherited optimizer |
| F decision evidence | CONFIRMED | Smoke gates control scale-up; no semantic verdict |
| G execution/reproducibility | CONFIRMED | 4H100 Smoke then PASS-gated 4H100 50B; first-layer variant excluded |

Cross-block consistency: **PASS**. The raw hook, gradient contract, data/optimizer
contract, four-rank batch, Smoke gates, and approved scale-up lead to one
unambiguous engineering decision.

Design frozen and execution approved: 2026-09-16, before the first new submission.

Superseded history: the earlier post-`Norm2` C/T and two/eight-RTX5090 design in
this file's prior revision is retired and must not be executed. Source history
remains in the earlier package and the 05 architecture-confirmation prompt.

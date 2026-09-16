# Native eight-layer Dense LM baseline: authorized 10B execution scope

Approved by the researcher's 2026-09-13 instruction in Codex conversation
`01a094cb-8104-7ab0-80d9-354a7a1c0aea`. This record fixes an operationally
matched representation-evolution baseline. It does not define the later
scientific analysis or make a mechanism claim from training loss.

## Comparison contract

- Random-initialized eight-layer Qwen3-style Dense LM: vocabulary 151,936,
  hidden size 1,024, FFN size 3,072, 16 query heads, 8 KV heads, head dimension
  128, context 2,048, tied input/output embeddings, and seed 17.
- No SAE is instantiated, optimized, checkpointed, or used in the forward
  path. In the final block, `post-norm2 -> native MLP`. The exact post-`norm2`
  tensor is exported as `final_block_post_norm2_native_pre_mlp_input`.
- Match the active SAE run's LM initialization, LM optimizer, peak LR `3e-4`,
  1,000-update linear warmup, weight decay, global batch of 262,144 prediction
  tokens, tokenizer, context length, and first 10B training-token trajectory.
- The eight-rank sampler must partition each logical batch from the submitted
  four-rank SAE topology rather than silently changing its global sample set.
  Each metric row records a topology-independent global sample-and-mask hash.
  Boundary masks at 0.5B, 1B, 3B, 5B, and 10B preserve the four-rank reference
  rank's contiguous eligible prefix before splitting it across two 5090 ranks.
- Use the same fixed readable 30,000,000,000-token source view. Stop the
  baseline at exactly 10,000,000,000 trained prediction tokens; it therefore
  never reaches the source-cycle boundary.
- Permanently retain complete checkpoints at 0, 0.5B, 1B, 3B, 5B, and 10B.
  Each checkpoint includes model, AdamW, scheduler, cursor/counters, all-rank
  RNG, model config, contract identity, file sizes, and hashes. Retain the two
  latest 1,000-step recovery checkpoints separately.
- Write TensorBoard events under each run's `tensorboard/` directory. The
  primary coordinate is cumulative globally counted non-ignored prediction
  tokens and the secondary coordinate is optimizer update. Required tags are
  `tokens/train_lm_loss`, `updates/train_lm_loss`,
  `tokens/train_total_loss`, `updates/train_total_loss`,
  `updates/learning_rate`, `progress/tokens_seen`,
  `progress/optimizer_step`, and
  `progress/effective_tokens_per_update`. LM loss is the global sum of
  next-token cross-entropies divided by the global non-ignored target count;
  the native baseline has no auxiliary objective, so total loss equals LM
  loss. `sae_reconstruction` is `NOT_APPLICABLE` because no SAE exists.
  Initial/final validation loss, LM gradient norm, step time, and valid-token
  throughput are retained as diagnostics. Each independent process writes an
  explicitly named TensorBoard segment beginning at its restored update and
  token coordinates. `metrics.jsonl` remains the counted source.
- The effective global batch is fixed at 262,144 valid prediction tokens per
  complete update. Warmup is 1,000 updates, equivalently 262,144,000 tokens;
  validation is at 0 and the final reached token target; checkpoints and stop
  points are the token milestones listed above. All later matched comparisons
  must use the same token counter, denominator, validation view, and milestone
  coordinates.

## Execution and gates

- Transitional Smoke profile: `5090-4-spot`, one node, four processes,
  `n12lp.nn.i10a.4`, SPOT quota, normal priority. Its micro-batch 2 and 16
  accumulation steps reproduce the submitted SAE run's native four-rank global
  batch directly.
- Formal profile: `5090-8-spot`, one node, eight processes,
  `n12lp.nn.i10a.8`, SPOT quota, normal priority. Check live capacity only after
  the four-GPU Smoke passes; the formal sampler then uses the audited
  four-to-eight-rank partition without changing the logical global batch.
- Required image: current default `shphd-lite-0911`. The historical
  `ngc-pytorch-25-06` image is prohibited for new jobs and is retained in the
  registry only to preserve earlier-run provenance. Because the base image's
  PyTorch 2.3 / CUDA 12.4 build is not expected to contain RTX 5090 SM120
  kernels, the job first checks it and, when needed, activates an isolated
  `/data` PyTorch 2.8 / CUDA 12.8 runtime layer. The layer is published
  atomically, is reused unchanged by the formal run, and never modifies the
  base image.
- Submit through `templates/execution/acp_submit_template.sh`; preserve its
  expanded receipt and the durable pod log.
- First run the 100-update engineering Smoke in the current image and resolved
  runtime layer. Require four RTX 5090 devices,
  correct parameter count with zero SAE parameters, finite LM loss and
  gradients, parameter updates, synchronized replicas, exact save/reload/replay,
  correct global-batch hashes, all required finite TensorBoard tags on exact
  token/update coordinates, coordinate continuity across a restored segment,
  complete terminal receipts, and measured steady throughput.
- Submit the separate 10B run on the identical profile only if every Smoke gate
  passes. Its run directory must be new and its entrypoint must auto-resume only
  that directory after a SPOT interruption.

## Evidence boundary

Smoke success qualifies implementation and timing only. Full-run training loss
and checkpoint existence do not establish semantic formation or a causal SAE
effect. The later representation analysis must load matched token milestones,
apply the same fixed evaluation panel and position semantics to both conditions,
and report the native pre-MLP representation separately from the SAE input,
reconstruction, sparse code, and final LM state.

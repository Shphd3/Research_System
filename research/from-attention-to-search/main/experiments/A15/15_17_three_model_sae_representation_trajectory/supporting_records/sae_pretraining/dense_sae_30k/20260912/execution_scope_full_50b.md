# Eight-layer Dense LM / SAE bottleneck: authorized 50B pretraining scope

Scope approved by the researcher's 2026-09-12 instruction in conversation
`01a094cb-8104-7ab0-80d9-354a7a1c0aea`, after review of the successful
four-H100 bottleneck Smoke. This record owns the execution boundary only and
does not define a semantic hypothesis or turn training diagnostics into a
scientific result.

## Fixed contract

- Use execution-envelope defaults `h100-4-reserved` and `shphd-lite-0911`, one
  node and four processes, through the repository ACP submission template.
- Train the random-initialized eight-layer Dense LM and width-30,000 Top-K-32
  SAE architecture qualified by job `pt-qzfqbsgv`.
- In the final block, `post-norm2 -> SAE reconstruction -> MLP`; logits remain
  the output. LM loss traverses the SAE into preceding blocks. The separately
  sampled reconstruction objective reads detached inputs and updates SAE
  parameters only.
- Fix the readable source prefix at 30,000,000,000 uint32 token IDs. Full
  sequence and four-rank balance expose 29,999,996,928 distinct prediction
  positions per pass; deterministic cycling supplies the requested total of
  exactly 50,000,000,000 trained prediction tokens.
- Global full-update batch is 262,144 prediction tokens. Token-boundary masks
  make every permanent milestone exact, including the final partial update.
- Permanently retain complete checkpoints at 0, 0.5B, 1B, 3B, 5B, 10B, 15B,
  30B and 50B prediction tokens. Each contains paired LM/SAE state, optimizer,
  scheduler, cursor/counters, all-rank RNG and checksummed manifest. Keep the
  latest two 1,000-step recovery checkpoints separately.
- Preserve the Smoke optimizer settings: LM and SAE peak LR `3e-4`, separate
  AdamW groups and clipping, LM warmup 1,000 steps, SAE warmup 10 steps,
  reconstruction weight 1.0 and reconstruction sampling rate 1/8. After
  warmup, LR remains constant. This is a declared training choice, not an
  empirical claim of optimality.
- Remove the Smoke wall-time cap. Stop only at the exact 50B budget, a
  synchronized failure, an external termination request, or a 60 GiB
  run-directory storage violation. A termination request saves a complete
  recovery checkpoint and exits incomplete.

## Evaluation and evidence boundary

Training-time held-out LM evaluation uses `model.forward_features`, so it
includes the same SAE-mediated final MLP path as training, with eval mode,
inference mode and no optimizer update. Checkpoint analysis independently
validates and loads the complete paired checkpoint before exporting the exact
post-`norm2` SAE input, reconstruction, Top-K indices/values and final LM
state. Initial/final panels are engineering fixtures; later checkpoint
evaluation is a separate researcher-selected analysis stage.

Submission is accepted only after local regression, config validation, an ACP
dry run and the previous GPU Smoke gate. After live submission, monitor at
least five minutes for resource identity, startup, finite losses, nonzero
LM/SAE gradients, progress and durable logging. Five healthy minutes establish
startup only, not full-run completion or scientific success.

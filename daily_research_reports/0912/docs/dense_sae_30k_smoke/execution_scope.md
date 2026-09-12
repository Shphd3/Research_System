# Dense LM / 30,000-feature SAE: engineering implementation and four-H100 smoke

Scope approved by the researcher's current request in task
`01a09440-1c43-7161-865e-ed044ef15ca3`: reuse/adapt existing training code and
optimizer configuration, expand SAE to 30,000, calculate parameters, and
submit a four-card smoke. This supersedes the previous read-only restriction
for this implementation and smoke only. No formal pretraining, scientific
hypothesis, semantic criterion, Focus/Anchor transition or long-run budget is
approved here. Like the prior four-H100 implementation acceptance in
`Projects/decommon-router-training/results/implementation_smokes/20260724_remote_4gpu_idle_full_pipeline/protocol.md`,
this is an engineering check with no mechanism Anchor.

## Fixed execution scope

- Execution workspace: `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining`.
- Config: `configs/smoke_4h100_sae30k.json` in that workspace; its resolved
  source/config/data hash is captured by the runner and paired checkpoints.
- Resource profile: `h100-4-reserved`; image: envelope default; activation:
  the workspace's `scripts/runtime.sh`. Resolve through
  `docs/execution_envelope.md` and the repository ACP submit template.
- Random-initialized native Qwen3-style Dense LM: 10 layers, d=1024,
  FFN=3072, query/KV heads=16/8, head_dim=128, vocab=151936, tied embeddings,
  context=2048. No pretrained LM or SAE weights are loaded to initialize it.
- Post-final-RMSNorm detached SAE observer: width=30000, Top-K=32, existing
  normalized reconstruction objective, one update per LM update, independent
  uniform sampling of approximately 1/8 valid training positions. No feedback,
  bottleneck, router, MoE, distillation, AuxK or semantic loss.
- Parameters: LM 312,892,928; SAE 61,471,024; combined 374,363,952. SAE count
  is 2*1024*30000 + 30000 + 1024. Meta-device construction verifies the count.
- Reused optimizer settings: LM AdamW LR=3e-4, betas=(0.9,0.95), epsilon=1e-8,
  matrix weight decay=0.1; bias/norm decay=0 is an explicit adaptation.
  SAE AdamW LR=3e-4, betas=(0.9,0.999), decay=0 from the old E16 SAE trainer.
  Separate LM/SAE clipping at 1.0. Source four-H100 LM warmup=1000 steps;
  source E16 SAE warmup=10 steps. The smoke ends in LM warmup and selects no
  formal-run decay endpoint.
- Data: existing frozen DCLM train/validation view with its manifest and
  tokenizer fingerprint. Keep train and validation disjoint by source path.
  This is not a document-level contamination or semantic-panel certification.
- Four ranks × 2 sequences × 2048 positions × 16 accumulated microbatches:
  262,144 effective next-token targets/update. Preserve the source global
  batch while adapting local batch/context to the Dense model.
- At most 100 logical optimizer updates = 26,214,400 valid prediction tokens,
  plus one repeated next-step update solely to verify checkpoint replay.
- Save paired step 0, step 50, and final step; complete optimizer/scheduler,
  rank RNG and dedicated sampling/loader Generator states; checksummed manifest
  published last. The reusable checkpoint code retains rolling-save support.
- Four fixed held-out batches per rank for initial/final LM loss; 16 held-out
  token windows for representation export and four-way cross-readout wiring.
  These windows have no semantic labels and do not train the SAE.
- Trainer wall bound 3500 seconds; shell hard bound 3600 seconds plus at most
  60 seconds to terminate. No automatic resubmission or formal continuation.
  Storage bound 20 GiB under this run directory, excluding shared dataset links.

## Engineering acceptance

Before submission: CPU tests must establish correct aligned targets, causal
masking, matched backbone gradients AND optimizer deltas with/without the
observer, separate clipping, counted unequal accumulation, full CPU
checkpoint/optimizer/Generator replay and immutable panel extraction.
Two CPU Gloo ranks must match the equivalent global batch.

PASS means 100 logical updates complete with finite LM/SAE losses and finite
validation; LM and SAE weights update; replicas remain synchronized; the
four-rank checkpoint next-step replay matches inputs, sampling RNG, losses and
the recorded bounded state probe; required paired checkpoint, activation,
analysis, execution and terminal receipts exist; storage remains within cap.
The GPU state probe samples 16 values from each tensor and is not a claim of
exhaustive bitwise GPU equivalence; CPU tests compare complete state tensors.
Step time, p50/p95, memory, I/O and losses are engineering diagnostics only.

FAIL means a required check or stage fails, a nonfinite value/OOM occurs,
or checkpoint/receipt/contract integrity fails. Stop and preserve failure
artifacts. INSUFFICIENT means the platform never provides the registered node,
the registered environment/data is unavailable, or the time limit prevents
completion. Neither authorizes silently changing profile, model, sample rate
or scientific scope.

This smoke cannot establish semantic/class formation, SAE width superiority,
convergence, full-run stability, downstream capability or a mechanism. The
researcher retains all those judgments and the next formal-run decision.

## Durable artifacts

The execution workspace run directory owns resolved configuration/source hashes,
parameter counts, metrics.jsonl, checksummed checkpoints, initial/final
validation and r/h/sparse-z/reconstruction NPZs, cross_readout.json,
resume_check.json, execution_certificate.json, smoke_receipt.json,
terminal_receipt.json, and any rank failure records. The repository submission
template stores the expanded image/profile tuple, accepted job ID/output and
durable pod log. The current Codex task is the sole monitoring owner.

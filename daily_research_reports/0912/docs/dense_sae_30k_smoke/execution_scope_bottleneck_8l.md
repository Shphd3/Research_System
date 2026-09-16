# Eight-layer Dense LM / SAE-mediated bottleneck: four-H100 engineering smoke

Scope approved by the researcher's 2026-09-12 request in conversation
`01a094cb-8104-7ab0-80d9-354a7a1c0aea`: implement the confirmed strong causal
intervention, reduce the Dense LM to eight layers, and run one bounded smoke.
This is engineering qualification only. It does not authorize the 50B full run,
select a long-run learning-rate schedule, or establish a scientific result.

## Fixed execution scope

- Workspace: `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining`.
- Resource: execution-envelope defaults `h100-4-reserved` and
  `shphd-lite-0911`, submitted only through the repository ACP template and
  activated with the workspace `scripts/runtime.sh`.
- Random-initialized eight-layer Dense LM: hidden size 1,024, FFN 3,072,
  16 query heads, 8 KV heads, head dimension 128, vocabulary 151,936, tied
  embeddings and context 2,048. No pretrained LM or SAE weights are loaded.
- Causal intervention: in the final Transformer block, the post-`norm2` tensor
  passes through the width-30,000, Top-K-32 SAE and the final MLP consumes its
  reconstruction. The residual connection remains the native Transformer
  residual; logits remain the only model output.
- LM loss traverses the all-token mediated SAE branch, updating the final MLP,
  SAE and preceding representation-producing blocks. A separate SAE pass reads
  a detached approximately one-eighth sample of valid pre-MLP tensors; its
  normalized reconstruction objective updates SAE parameters only.
- The Smoke keeps unit reconstruction weight, existing separate LM/SAE AdamW
  parameter groups and clipping, and the existing warmups. This qualifies
  wiring and bounded stability only; it does not select the formal-run
  reconstruction weight, sampling rule or LR decay.
- Global batch remains 262,144 valid prediction tokens per update. The run is
  capped at 100 logical updates, 3,500 trainer seconds, 3,600 shell seconds and
  20 GiB. It saves complete step-0, replay-boundary and final checkpoints.
- Existing frozen DCLM view and held-out engineering panel are reused. The
  proposed exact 30B data view, 50B traversal and permanent full-run milestones
  are not part of this Smoke.

## Acceptance

Local CPU qualification must show that LM loss gives nonzero gradients to the
SAE and the pre-bottleneck blocks, while reconstruction loss gives gradients to
SAE parameters and none to LM parameters. It must retain aligned targets,
causality, unequal-count normalization, complete checkpoint/recovery equality,
panel immutability and two-rank Gloo consistency.

GPU PASS requires 100 logical updates with finite LM/reconstruction losses and
validation, changed LM and SAE parameters, synchronized replicas, successful
registered replay, complete checksummed checkpoints, correct execution and
terminal receipts, and storage within the cap. Record throughput, memory and
checkpoint duration because the old detached-observer measurements do not
transfer to this all-token bottleneck.

FAIL preserves artifacts and stops on failed gradients, nonfinite values, OOM,
checkpoint/replay mismatch or missing receipt. INSUFFICIENT covers unavailable
registered resources/environment/data or expiry before the bounded trajectory.
Neither status authorizes a different profile, model, objective or automatic
resubmission.

This Smoke cannot establish semantic formation, interpretability, SAE-width
superiority, convergence, downstream capability or 50B stability.

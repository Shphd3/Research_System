# Dense SAE checkpoint audit: execution record

Updated at: 2026-09-13T13:26:17Z

Execution scope: [execution_scope.md](execution_scope.md).

## Pre-execution audit

The five requested milestone checkpoints exist at exactly 0.5B, 1B, 3B, 5B
and 10B tokens. All 25 payload/RNG files were independently rehashed against
their complete manifests in this task; sizes and SHA-256 values match. The
separate step-zero checkpoint was also verified but is not an evaluation input.

The new analysis code does not alter the active trainer or checkpoints. It
uses contiguous disjoint rank partitions, globally reduces reconstruction and
activation counts, and writes results only after a checkpoint's complete
fixed-corpus pass. The five checkpoints share the same held-out sample order,
metric definitions and fixed 20 feature IDs.

Local qualification passed 31 pytest cases, including four new checkpoint
audit tests, plus Python compilation and shell syntax. The new tests freeze the
requested checkpoint set and selected-feature cardinality, prove exact sample
partition coverage, verify stable top-activation ranking, and render all twelve
expected plot files from synthetic summaries.

## First submission attempt

The default-profile dry run resolved exactly `h100-4-reserved`, one
`n6ls.iu.i40.4` node, four H100 80GB ranks, reserved quota, normal priority and
the current `shphd-lite-0911` image. The live create request at
2026-09-13T11:21:51Z was rejected before scheduling with
`MEMBER_QUOTA_EXCEEDED`: the member quota had zero remaining GPUs and CPUs,
versus four GPUs and 88 CPU cores requested. No audit job ID or remote run was
created, so no GPU Smoke or full evaluation result exists.

The durable failed-create receipt is
`/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/acp_receipts/submit-dense-sae-ckpt-audit-0p5-1-3-5-10b-20260913T112032Z-20260913T112149Z.json`.
The pre-GPU source snapshot is execution
`handoff/dense_sae_checkpoint_audit_pre_gpu_20260913T112032Z.tar.gz`, SHA-256
`81ef09117031321f3bc3a54245fef63d478752a3758fd29227084f5d9872829b`.

That failed attempt did not authorize an automatic fallback. The researcher
subsequently authorized an audit-specific exception of either two H100 or two
RTX 5090 GPUs under SPOT quota.

## Authorized two-H100 submission

The implementation was adapted only at the inference topology boundary so
that the replicated four-rank training state can be evaluated by two ranks;
optimizer and RNG state are not restored. The fixed corpus, checkpoint set,
feature set, metric definitions and output contract are unchanged. The full
local regression then passed 32 of 32 tests. The adapted pre-GPU source
snapshot is
`handoff/dense_sae_checkpoint_audit_2h100_pre_gpu_20260913T123907Z.tar.gz`,
SHA-256
`38cca353e1ae8f48217df39588dac094cd5b4c4efd2921b190867b3b17e90929`.

ACP job `pt-0sut3gk4` was created at 2026-09-13T12:39:33Z with the exact tuple
`h100-2-spot`, `share-space`, `share-cluster`, one `n6ls.iu.i40.2` node, two
H100 80GB GPUs, two inference ranks, SPOT quota, normal priority, and image key
`shphd-lite-0911`. Its durable submission receipt is
`/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/acp_receipts/submit-dense-sae-ckpt-audit-2h100-0p5-1-3-5-10b-20260913T123907Z-20260913T123932Z.json`.

At 2026-09-13T12:46:23Z the job remained platform-side `STARTING`; its sole
worker was `Pending` without a host or pod IP. Therefore the container had not
yet begun the five-checkpoint Smoke, and no Smoke or scientific audit result
was claimed. No duplicate fallback job was submitted.

The H100 worker was still `Pending` at 2026-09-13T12:54:42Z, more than fifteen
minutes after creation, with no host IP, pod log, run directory or Smoke
artifact. The researcher had explicitly authorized either two H100 or two RTX
5090 GPUs under SPOT for this audit. The exact existing two-5090 workerspec was
independently observed as `n12lp.nn.i10a.2` (two GPUs, 28 CPU cores, 120 GiB),
and the resolved `5090-2-spot` tuple passed a dry run. Job `pt-0sut3gk4` was
therefore stopped at 2026-09-13T12:55:20Z while still pre-execution; it entered
`SUSPENDING` and produced no evaluation evidence.

The 5090 runner preserves the same two-rank audit and first activates the
already qualified mounted PyTorch 2.8/CUDA 12.8 SM120 runtime layer. Shell
syntax and envelope resolution passed. The updated pre-GPU snapshot is
`handoff/dense_sae_checkpoint_audit_2gpu_pre_gpu_20260913T125131Z.tar.gz`,
SHA-256
`fe460a91da9b407c78812be6b3e8460b9b75495f234242a1db2fb0f29e6d8db9`.

ACP job `pt-p5mlwlqn` was submitted at 2026-09-13T12:55:21Z with
`5090-2-spot`, `computing-cluster-5090-01g`, one `n12lp.nn.i10a.2` node, two
RTX 5090 32GB GPUs, two ranks, SPOT quota, normal priority and the current
`shphd-lite-0911` image. Its receipt is
`/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/acp_receipts/submit-dense-sae-ckpt-audit-2x5090-0p5-1-3-5-10b-20260913T125500Z-20260913T125520Z.json`.
At 2026-09-13T12:57:26Z the worker had a host assignment but the job remained
`STARTING`; the container had not yet written a pod log, so Smoke remained
pending and no audit result was claimed.

The 5090 job entered `RUNNING` at 2026-09-13T13:02:06Z. Runtime qualification
showed exactly two RTX 5090 GPUs and the mounted PyTorch 2.8.0/CUDA 12.8 layer
with `sm_120` support. The five-checkpoint Smoke completed at
2026-09-13T13:10:24Z with status `PASS`: the same eight sequences and 16,384
tokens were used at every checkpoint, all required metrics were finite, and
all twelve expected figures plus the selected-feature text report were
created. These small-sample values are engineering evidence only.

The same process then began the full fixed-heldout audit. At the final bounded
supervision snapshot, 2026-09-13T13:26:17Z, the job remained `RUNNING` and the
0.5B and 1B checkpoints had each completed exactly 114,987,008 evaluation
tokens. Their completion times were 13:18:12Z and 13:25:27Z, respectively.
With three checkpoints remaining and an observed interval of about 7.25
minutes per completed checkpoint, the evidence-based remaining estimate was
22--25 minutes, or approximately 13:48--13:51Z if uninterrupted. This estimate
excludes a SPOT interruption. Continuous polling stopped at the researcher's
request; the remote job was left running. Full figures and scientific
interpretation remain unavailable until the full audit receipt exists.

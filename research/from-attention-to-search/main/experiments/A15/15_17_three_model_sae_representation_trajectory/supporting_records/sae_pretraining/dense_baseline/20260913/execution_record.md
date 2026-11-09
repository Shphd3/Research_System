# Native Dense LM baseline: execution record

Updated at: 2026-09-13

The researcher authorized an isolated eight-RTX5090 Smoke followed, on passing
all gates, by a separate 10B formal run. Raw code, logs, checkpoints, metrics,
and TensorBoard events live under
`/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining`.

## Local qualification

The isolated native baseline is complete. It contains 281,431,040 LM
parameters and zero SAE parameters. The final MLP consumes the exact native
post-`norm2` tensor exported for later comparison. The seed-17 initialization
matches all 90 non-SAE tensors in the active SAE run's complete step-zero
checkpoint exactly.

Local checks passed: 30 pytest cases, two-rank Gloo execution, exact parameter
count, four-to-eight-rank global-batch and boundary-mask equivalence, 10B
milestone arithmetic, shell syntax, checkpoint replay, and TensorBoard event
readback. The code-only pre-Smoke snapshot is
`handoff/dense_baseline_10b_pre_smoke_source_20260913T075335Z.tar.gz` in the
execution package, SHA-256
`bb1f9a9605e7bb117832c9322c5e6e2b932008112d6df9362d52c0ea500e6001`.

## Remote gate

The eight-5090 profile was reactivated by the researcher. New jobs are bound to
the current default `shphd-lite-0911`; `ngc-pytorch-25-06` is now rejected by
the resolver for new submissions and retained only as old-run provenance. The
latest image will be checked first. If its bundled PyTorch cannot execute SM120,
the job installs and atomically publishes an isolated PyTorch 2.8 / CUDA 12.8
layer under `/data/250010109/dependency_packages/`, then performs the full
eight-device BF16 and NCCL preflight. The formal run must reuse the exact layer
qualified by Smoke.

## Four-RTX5090 transitional gate

The researcher replaced the initial eight-GPU Smoke request with a four-GPU
transition test. All new jobs used the current `shphd-lite-0911` image; the old
NGC image was not used. The image's bundled PyTorch lacked the required SM120
support, so an isolated mounted PyTorch 2.8.0 / CUDA 12.8 layer was qualified
on all four RTX 5090 devices. TensorBoard 2.9.0 came from the current image;
the redundant network installation was removed after the first attempt exposed
intermittent package-index DNS failures.

Preserved attempts:

- `pt-tmnk1da7`: `FAILED` before training while redundantly fetching
  TensorBoard dependencies. Its durable log is retained; the already complete
  SM120 PyTorch layer was validated on all four GPUs and atomically published.
- `pt-5ajlkh4o`: `FAILED` before optimizer step 1 because an eight-rank-only
  configuration guard rejected the newly authorized four-rank Smoke. Four-rank
  BF16/NCCL preflight passed. The guard was narrowed so only an engineering
  Smoke may use four ranks; formal training remains fixed at eight ranks.
- `pt-faiypkhi`: `SUCCEEDED` for 100 updates and qualified the model,
  checkpoint, throughput, memory, and four-rank data path. Its TensorBoard
  events used the earlier update-only labels, so this run is preserved but is
  not the final observability/comparison qualification.
- `pt-kky1ihlb`: final `SUCCEEDED` Smoke using one node, four
  `n12lp.nn.i10a.4` RTX 5090 devices, SPOT quota and normal priority. Platform
  time was 2026-09-13 09:53:12--10:05:12 UTC. The trainer deliberately stopped
  at update 50 with a complete recovery checkpoint, then a distinct four-rank
  process resumed the same run through update 100.

The final run directory is
`/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/smoke_4x5090_observability_final_20260913T094622Z`.
Its receipt is `PASS`: 100 unique logical updates, 26,214,400 exact prediction
tokens, 101 physical updates including one discarded checkpoint replay, two
process starts, no rolled-back update, synchronized replicas, zero SAE
parameters, and terminal exit 0. LM loss was 12.149334 at update 1 and 8.761664
at update 100; validation LM loss was 12.151213 initially and 8.647088 finally.
Median/p95 update time was 2.229/2.307 seconds, steady throughput was 117,126
valid tokens/s, and peak allocated/reserved memory was 9.80/10.82 GB per rank.

The step-50 recovery check reproduced the next loss exactly at 10.320968, used
the same global sample/mask identity and had a sampled-state maximum difference
of about 1.19e-7. TensorBoard contains two explicitly named process segments.
Its independent audit passed all eight required token/update tags, finite-value
checks, exact coordinate maps and equality to the 100 counted JSONL records.
All 15 files in the step-0, step-50 and step-100 checkpoint manifests were
rehashed: 7,880,573,935 bytes matched their recorded sizes and SHA-256 values.

The submitted observability source snapshot is
`handoff/dense_baseline_10b_observability_pre_smoke_source_20260913T094622Z.tar.gz`
(SHA-256 `38d524167fbbeb1c539fb5acca59773c9d3883656db45fc8ef3f9bce46bed336`).
The post-pass package snapshot, including the clarified README, is
`handoff/dense_baseline_10b_4gpu_observability_smoke_pass_source_20260913T100725Z.tar.gz`
(SHA-256 `25d9977e2f8cde645b8be30e925e2232a9607618ff064bcc03e7b0719217c4c6`).
All earlier snapshots and Smoke evidence remain preserved.

## Formal readiness and timing boundary

After the final four-GPU gate passed, the researcher explicitly authorized the
matched eight-GPU formal submission and requested that this task end without
startup supervision. Job `pt-79x53njx`, named
`dense-native-baseline-8x5090-10b-full-20260913T102944Z`, was accepted by ACP at
2026-09-13 10:29:46 UTC with status `SUBMITTED`. The resolved tuple is one
`n12lp.nn.i10a.8` node, eight RTX 5090 32GB ranks, SPOT quota, normal priority,
cluster `computing-cluster-5090-01g`, and the current `shphd-lite-0911` image at
`registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423`.
The prohibited historical NGC image was not used.

The designated formal run directory is
`/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z`.
It had not yet materialized at task close, which is consistent with a submitted
job that has not been startup-supervised.
Its submission receipt is
`/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/acp_receipts/submit-dense-native-baseline-8x5090-10b-full-20260913T102944Z-20260913T102944Z.json`.
The submitted config remains fixed at eight ranks, 10,000,000,000 prediction
tokens from the frozen 30B data view, no wall-time cap, complete milestones at
0, 0.5B, 1B, 3B, 5B and 10B, a global batch of 262,144 tokens, and the required
TensorBoard contract. Submission success proves only that ACP accepted the job;
per the researcher's instruction, no startup or runtime state was queried in
this task.

The four-GPU steady rate projects 23.72 hours of optimizer-update time to 10B;
checkpoint, validation and startup overhead make about 24.1--24.6 hours a
reasonable uninterrupted four-GPU operational estimate. There is no measured
eight-GPU throughput yet. Assuming 1.7--1.9x scaling while preserving the
global batch gives 12.5--14.0 hours of training-core time and about 12.8--14.3
hours including expected checkpoint and validation overhead, with 13.5 hours
as the central planning estimate. Queueing and SPOT preemption/recovery are
excluded. A later measured eight-GPU rate should replace this inference.

No scientific result is owned by this record.

## 2026-09-14 continuation readiness

The formal job remained `RUNNING`, so no second Dense job was submitted.
Operational continuation tooling was prepared under execution
`continuation` without modifying the frozen `dense_sae`, `scripts`, config,
data or training-contract hash. The wrapper requires the existing complete
resume pointer, runs the original eight-RTX5090 launcher, requests a
synchronized checkpoint/exit after 113,400 seconds, and writes a segment
receipt. It also permanently retains the first complete recovery checkpoint at
or after 7B and 9B; the trainer's exact 0/0.5/1/3/5/10B milestones remain
unchanged. Each promoted checkpoint is rehashed before atomic publication.

The Dense workspace's 30 tests, Python compilation, shell syntax and dry-run
passed. All 28 frozen Python/shell source hashes and the config still match the
active run's recorded contract. The wrapper is a recovery path only and must
not be launched while the current formal process remains active.

## 2026-09-14 10B-to-50B continuation submission

The researcher changed the cumulative Dense target to 50B and explicitly
authorized an eight-RTX5090 continuation from the exact complete 10B milestone.
The parent trajectory remains immutable. A child continuation contract and
launcher record the parent contract explicitly; the first segment restores
model, AdamW, LambdaLR, counters, data cursor, and all eight rank RNG states.
Later segments restore the child run's own full checkpoint.

The LR schedule is identical and continuous: 1,000-update linear warmup then
constant `3e-4`, with no target-budget-dependent decay. The rehashed parent
state is update 38,150 / 10B tokens with scheduler `last_epoch=38150`; both
optimizer groups and scheduler `_last_lr` equal `3e-4`. Effective global batch
remains 262,144 valid prediction tokens.

Local qualification passed all 30 tests, shell syntax and wrapper dry-run. A
dedicated preflight rehashed all nine 10B checkpoint files and passed the
lineage, full-state, scheduler, fixed-data, fixed-optimizer and batch checks.
Permanent child milestones are 15B, every 2B from 17B to 49B, and exact 50B;
the original 0/0.5/1/3/5/10B milestones remain preserved.

ACP accepted job `pt-8c1eoe8g`, display name
`dense-native-baseline-8x5090-50b-cont-full-20260914T130243Z`, on the resolved
`5090-8-spot` profile and `shphd-lite-0911` image. Its child run directory is
`runs/full_50b_continue_from_10b_8x5090_20260914T130243Z`; the first segment
requests synchronized checkpoint-and-exit after 31h30m. At the final startup
observation it remained `STARTING` with zero assigned replicas, so successful
runtime restore and the first post-10B update were not yet established.

# Dense LM / 30,000-feature SAE engineering smoke: execution record

Updated at: 2026-09-12T10:45:00Z

Execution scope: [execution_scope.md](execution_scope.md). This is an engineering
record, not a scientific experiment result or formal-pretraining approval.

## Implementation and local qualification

The isolated execution package is
`/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining`.
Its `README.md` describes adaptations and entrypoints;
`docs/reuse_sources.json` records the 19 copied sources and their original
SHA-256 identities. Original source files remained unchanged at submission.

The reused packed-data, frozen-view, tokenizer and atomic-checkpoint code comes
from `Research_System/Projects/decommon-router-training`. The DDP trainer uses
that project's AdamW settings and accumulation pattern, adapted for independent
Dense-LM and SAE parameter groups and gradient clipping. The 0912 Dense/SAE
reference supplies the model and fixed-position analysis; the E16 SAE trainer
supplies width 30,000, k=32 and its optimizer settings. Old router, MoE, teacher,
AuxK, outlier filtering and MLP-input capture are not part of this run.

Meta-device construction confirms 312,892,928 LM parameters and 61,471,024 SAE
parameters, 374,363,952 total. SAE width is 30,000; LM hidden size is 1,024.

`runs/local_checks/receipt.json` records successful local qualification and the
source hashes sent to the remote job: 16 pytest cases, a two-rank CPU Gloo
comparison with the equivalent global batch, exact parameter counting, and a
standalone checkpoint-to-activation CLI roundtrip. The tests include aligned
targets, causality, matched backbone gradients and updates with/without the
detached observer, unequal accumulation, complete CPU optimizer/RNG recovery,
and the tiny end-to-end smoke outputs.

The first direct checks encountered the existing ONNX/protobuf import conflict.
The process-local `scripts/runtime.sh` applies the existing Python-protobuf
compatibility setting and mounted tokenizer dependency layer. Re-running through
this runtime passed; no base-environment package installation was performed.

## Submitted run and evidence map

- Job: `pt-i9ohovsb`, submitted 2026-09-12T08:01:48Z.
- Run directory: `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/runs/smoke_4h100_sae30k_20260912080130`.
- Submission entrypoint: `Research_System/templates/execution/acp_submit_template.sh`,
  resolving the current execution envelope; accepted profile `h100-4-reserved`,
  one four-GPU worker, reserved quota, normal priority.
- Image key: `shphd-lite-0911`; expanded URL, mounted storage and exact startup
  command are in the run's `run_receipt.json` and submission receipt.
- Configuration: execution package `configs/smoke_4h100_sae30k.json`.
- Activation: `scripts/runtime.sh`, with existing mounted layer
  `/data/250010109/dependency_packages/hf_transformers_qwen3`.
- Exact remote command: `bash scripts/run_smoke_4h100.sh /data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/runs/smoke_4h100_sae30k_20260912080130`.
- Durable pod logs: execution package `acp_receipts/pod/`, this job-name prefix.
- Monitoring owner: Codex task `01a09440-1c43-7161-865e-ed044ef15ca3`.

First attempt: **FAILED**, shell exit 1 at 2026-09-12T08:07:51Z, before the first
optimizer update. The durable pod log and runtime certificate confirm four
H100 devices and the intended runtime. CUDA reported an out-of-bounds index in
the bounded parameter probe. CPU reproduction confirms that float32
`linspace` rounds embedding index 155582463 up to 155582464, equal to the tensor
size. This affected instrumentation before evaluation/training, not the data
or loss computation. `index_failure_reproduction.json`, the hash-verified
`engine_submitted.py`, four rank failures and the terminal receipt remain in
the first run directory.

The repair replaces floating-point index spacing with exact integer arithmetic
in `dense_sae/engine.py`. A regression test exercises the actual full embedding
size through a zero-stride tensor without allocating another large model.
All 17 local tests pass; `runs/local_checks/probe_fix_receipt.json` records the
new hashes. Only the engine probe and regression test changed from the initial
qualified source set. Model, optimizer, data, losses, counts and profile remain
the same.

Diagnosed repair attempt: job **`pt-ro6ijc54`**, submitted through the same
envelope/template, with run directory
`/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/runs/smoke_4h100_sae30k_fix_20260912080957`.
The exact command is in its `run_receipt.json`; an outer 3500-second timeout
leaves room for the first attempt's approximately 52-second runtime within the
original one-hour runtime scope (termination grace remains explicit). This is
a diagnosed implementation correction under the researcher's implementation
and smoke request, not a scripted retry or expansion of the training budget.
The preceding job performed zero training updates. No concurrent duplicate job
is retained and no formal run is started.

Repaired runtime result: **PASS**, completed 2026-09-12T08:16:16Z; shell exit 0
at 08:16:21Z. All eight registered runtime gates passed. Independent artifact
verification passed at 08:20:56Z, with platform state **SUCCEEDED**. The run's
`artifact_verification.json` records all three checkpoints' file sizes and
SHA-256 verification, four rank RNG files per checkpoint, source/config/scope/
data identity, exact token counters, panel identity and finite exported arrays.

| Engineering measurement | Observed value | Meaning and boundary |
| --- | --- | --- |
| Logical updates / prediction tokens | 100 / 26,214,400 | Complete bounded trajectory; 101 physical updates include one discarded replay |
| SAE sampled positions | 3,276,800 | Global 1/8 count, restored correctly across replay |
| Warm-step throughput | 144,730 valid token/s across four GPUs | Excludes preceding data fetch; first ten updates excluded |
| Step duration p50 / p95 | 1.794 / 1.898 s | Maximum-rank synchronized update time |
| End-to-end runtime / throughput | 319.18 s / 82,131 unique token/s | Includes setup, validation, checkpoint save/load, replay and analysis; excludes scheduling and the first failed attempt |
| Peak allocated / reserved GPU memory | 11.983 / 12.742 GiB per rank | Maximum across the four devices; not a full-training capacity guarantee |
| Final checkpoint save | 25.99 s | Registered writing/checksum path |
| Run storage at trainer completion | 9.764 GiB | Under 20 GiB; subsequent small receipts are additional |
| Fixed held-out LM loss | 12.1965 initially; 8.67935 finally | Finite diagnostic on 65,536 targets each; no convergence/capability claim |
| Four-rank next-step replay | PASS; equal LM loss; sampled-state maximum difference 1.19e-7 | Identical inputs/RNG, losses and the documented bounded state sample |

Initial and final fixed-panel outputs contain `raw_h`, `h`, `reconstruction`
arrays [16,1024], `indices`/`values` [16,32], and position/sample/token IDs.
In the plan's notation r is named `raw_h` by the reused collector. Four-way
cross-readout and feature statistics exist as unlabeled engineering outputs.
The three verified checkpoints occupy 1,497,841,878 bytes at step 0 and
4,492,853,130 bytes each at steps 50 and 100, including rank RNG files.
These observations establish that a 30,000-feature SAE fits and runs in this
configuration; they do not establish superiority over 8,192 or another width.

## Acceptance and interpretation boundary

The job is capped at 100 logical updates plus one recovery replay, and one hour
of runtime. The runner owns `smoke_receipt.json`; the shell owns
`terminal_receipt.json`. Completion requires both, the durable pod log and the
registered output/contract checks. GPU recovery compares inputs, sampling RNG,
losses and a bounded sample from state tensors; the CPU tests compare complete
state tensors. These are different levels of numerical verification.

Per-update timing excludes the preceding data-fetch interval; end-to-end timing
includes loading, validation, checkpoints and analysis. This observer-only smoke
does not measure overhead against a separate no-SAE GPU condition. For the
source used by this GPU Smoke, external process restart of the entire
orchestration was not qualified. That frozen source should use the qualified
fresh-directory command and internal replay. The later **Local post-handoff
audit and repair** section records a CPU-only external-process repair; it does
not retroactively enlarge this GPU qualification.

No claim about semantic formation, optimal SAE width, convergence, downstream
capability or long-run stability follows from this engineering check. Formal
pretraining remains unstarted and requires its own researcher-owned scope.

## Handoff preparation

The researcher requested a code/work-record update and a prompt for a subsequent
Sol task. [Code handoff](code_handoff.md) now owns the actual package/file map,
interfaces, confirmed resume-orchestration gaps, six targeted audits and proposed
local acceptance checks. The source task's
[Sol prompt](../../../../.research/memory/conversations/0912-梳理-sae-动态形成预训练方案/sol_handoff_prompt_cn.md)
and CURRENT continuation point at these owning records.

Preparation rechecked all 30 qualified code/config/test file hashes and the
small terminal/artifact receipts; it did not rerun training, tests or full
checkpoint hashing. The execution package README and training reuse index were
updated. Training logic/configuration and both GPU attempts remain unchanged.
The execution directory is not Git-managed; its `handoff/baseline_manifest.json`
records a code-only archive and exact file identities for comparison before Sol
edits it. No commit, push, external sync or direct task dispatch was performed.

The next receiving task should first address distinct-process resume and its
regression evidence. The historical GPU check sampled model state tensors;
it did not compare complete Adam moments on GPU. The new handoff makes that
coverage limit explicit rather than enlarging the old acceptance claim.

## Local post-handoff audit and repair

The researcher authorized the receiving task to make bounded local repairs and
run CPU checks, while prohibiting GPU submission, formal training, scientific
hypothesis changes, new loss/router/MoE machinery, commit and push. The frozen
handoff archive still has SHA-256
`46dfe8a8d80b88e5855803fc279b79950dc832f80deca9f1e0e03e75e342ce7f`;
all 34 archived files matched before editing. Neither historical GPU run
directory was changed.

Eight source/test files changed in the execution package. `dense_sae/train.py`
now keeps a checksummed immutable step-zero SAE/panel baseline, resolves the
resume path once and requires it to belong to the run, restores rather than
recomputes initial validation/activations, completes or reuses the replay proof
at its boundary, reconciles logical metrics to the checkpoint while preserving
stale rows under `recovery_history/`, and records physical updates plus process
and whole-run wall accounting separately. Graceful local qualification stops
publish a complete recovery checkpoint and exit as incomplete rather than
writing a training failure. The wall bound now applies to the whole resumed run,
not independently to each process.

`dense_sae/engine.py` includes attention, target-eligibility and SAE masks in
the next-batch identity digest. Unequal accumulated counts remain globally
normalized. The built-in sampler gives each rank at least one SAE sample; an
externally supplied update with a rank-local total of zero SAE samples is now
rejected collectively before DDP backward, while an empty individual
microbatch remains allowed when that rank's accumulated count is nonzero.
`collect_activations.py` and `representation_evolution.py` restore caller
training mode after inference. The configuration rejects non-unit SAE loss
weight and bottleneck feedback, which were exposed but unsupported by this
observer-only trainer. No objective or gradient path was added.

The final local receipt is
`/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/runs/local_checks/resume_audit_20260912T0920Z/receipt.json`.
It records 22 passing pytest cases, an exit-0 two-rank Gloo check, the unchanged
parameter count and exit-0 shell syntax checks. Distinct Python-process tests
cover stopping before, at and after the replay boundary; compare complete
model, AdamW and scheduler state; compare logical counters, cursor, next-input
and mask identity; preserve the original panel; and compare both rank RNG files
for a two-rank resumed run. One test also preserves a simulated uncheckpointed
metrics tail while counting its physical work as rolled back. Two exploratory
Gloo attempts were interrupted/timed out because the test harness ran a
single-process reference step while a world-size-two process group remained
live; the corrected symmetric test order passes, so those attempts are not
training failures.

This is CPU qualification of the modified source. The completed four-H100 Smoke
continues to qualify only its frozen baseline hashes; no GPU equivalence,
no-SAE overhead, 20B stability, semantic formation, convergence or capability
claim follows. Formal pretraining remains unstarted.

## Eight-layer SAE-mediated bottleneck implementation and Smoke

The researcher subsequently confirmed a strong causal intervention and
authorized its implementation plus one bounded Smoke. The new owning scope is
[execution_scope_bottleneck_8l.md](execution_scope_bottleneck_8l.md). The
previous detached-observer scope, frozen archive and both historical GPU run
directories remain unchanged.

The model is now an eight-layer, random-initialized Dense LM. Inside the final
block, its post-`norm2` MLP input passes through the Top-K SAE and the final MLP
consumes the reconstruction. The LM loss therefore updates the SAE and has a
gradient path through it into preceding blocks. A second sampled SAE pass uses
a detached pre-MLP tensor for normalized reconstruction loss, so that objective
updates SAE parameters only. The native residual connection remains outside
the MLP branch, and LM logits remain the model output.

Local qualification is recorded at execution
`runs/local_checks/bottleneck_8l_20260912T1033Z/receipt.json`: 23 pytest cases,
two-rank Gloo, parameter accounting and syntax checks passed. Direct gradient
tests establish nonzero LM-loss gradients at the SAE, final MLP and preceding
block, plus zero non-SAE gradients from reconstruction loss alone. The model
has 281,431,040 LM parameters and 61,471,024 SAE parameters, 342,902,064 total.
The pre-change local-repair source snapshot is preserved as
`handoff/dense_sae_pre_bottleneck_20260912T0952Z.tar.gz`, SHA-256
`09a0b3134ab64ee6d9e2fc22255fcc19f7cd737c14e9959aa1b89501e448367b`.
The post-Smoke source snapshot is
`handoff/dense_sae_bottleneck8_smoke_pass_20260912T1045Z.tar.gz`, SHA-256
`46e57c50ee1df3be7d081d4d573a05042458fb161868fd8ed20109352c7a2dbf`.

GPU job `pt-qzfqbsgv` used the registered `h100-4-reserved` profile and
`shphd-lite-0911` image. Platform state was `SUCCEEDED`; terminal exit was 0;
all ten trainer gates and independent artifact verification passed. The run is
execution
`runs/smoke_bottleneck8_4h100_202609121034/`, with durable pod log and exact
submission receipt under execution `acp_receipts/`.

| Engineering measurement | Observed value | Meaning and boundary |
| --- | --- | --- |
| Logical / physical updates | 100 / 101 | 26,214,400 unique prediction tokens; one discarded replay update |
| Reconstruction samples | 3,276,800 | Detached one-eighth sample for reconstruction loss; the LM bottleneck applies to all forward positions |
| Steady throughput | 148,004 valid token/s | Four GPUs; excludes preceding data fetch and checkpoint I/O |
| Step duration p50 / p95 | 1.751 / 1.861 s | Maximum-rank synchronized update time |
| End-to-end runtime / throughput | 307.14 s / 85,350 unique token/s | Includes setup, validation, checkpoints, replay and analysis |
| Peak allocated / reserved | 11.191 / 11.902 GiB per rank | Bounded Smoke observation, not long-run capacity proof |
| Final full-checkpoint save | 23.57 s | Checksummed LM/SAE/AdamW/scheduler/cursor/RNG state |
| Step-0 / trained checkpoint size | 1.372 / 4.115 GB | Each inventory independently size/hash verified |
| Fixed held-out LM loss | 12.1452 initially; 8.69554 finally | Finite engineering diagnostic during warmup only |
| Reconstruction loss | 0.76998 at step 1; 0.06495 at step 100 | Training diagnostic, not semantic-feature evidence |

The analysis exports now identify `h` as the final-block post-`norm2` SAE/MLP
input and `raw_h` as its pre-`norm2` residual; `final_raw_h` and `final_h` retain
the states before the final norm and at the LM head. Panel identity, shapes and
all floating arrays passed independent validation.

The Smoke establishes the requested causal wiring, gradient ownership, bounded
four-H100 execution and complete checkpoint path. It does not select the
formal-run reconstruction coefficient, long-run LR schedule, exact 30B view or
50B traversal, and does not establish semantic formation, interpretability,
convergence, downstream capability or long-run stability. No full run started.

## Formal-run preparation and authorization

The researcher subsequently confirmed the architecture and explicitly
authorized removing the Smoke limits and submitting the formal run. Source
inspection confirms that `SAE(post_norm2)` produces
`mediated_reconstruction`, which is passed as the final block MLP's only input.
The native residual bypass remains. LM loss traverses this path; the separate
detached reconstruction pass restricts reconstruction-loss gradients to SAE.

Checkpoint evaluation was independently exercised against the completed GPU
Smoke checkpoint through the analysis CLI. Complete paired-checkpoint
validation passed; eval/inference mode exported finite `[2,1024]` MLP-input and
SAE-reconstruction arrays plus `[2,32]` sparse codes without optimizer update
or parameter mutation. The receipt is execution
`runs/local_checks/checkpoint_eval_bottleneck8_20260912T1120Z/receipt.json`.

The authorized long-run contract is recorded in
[execution_scope_full_50b.md](execution_scope_full_50b.md). It fixes the 30B
source prefix, exact 50B trained-token budget, permanent
0/0.5/1/3/5/10/15/30/50B complete checkpoints, rolling recovery state and no
Smoke wall cap. These are execution facts; five healthy startup minutes cannot
establish convergence, semantic formation or task utility.

Formal job `pt-x0dxui5n` was accepted at `2026-09-12T11:06:50Z` and entered
`RUNNING` at `11:12:10Z` on the registered single-node four-H100 reserved
profile and default image. The durable pod log is execution
`acp_receipts/pod/dense-sae30k-bottleneck8-50b-full-202609121130-20260912T111212Z.log`;
the run directory is execution `runs/full_50b_bottleneck8_202609121130/`.

The startup monitor covered 320 seconds after `RUNNING`. During that window the
trainer produced the complete step-zero checkpoint and initial evaluation,
then progressed beyond step 110 with finite, nonzero LM and SAE gradients and
no failure artifact. The registered step-50 save/restore/replay passed with
identical loss and a maximum sampled-state difference of `1.19e-7`, after
which logical steps continued. The startup receipt is
`runs/full_50b_bottleneck8_202609121130/startup_monitor_5min.json`. Its status is
`PASS_STARTUP_ONLY`: the formal run remains active and has no result verdict.

## 2026-09-14 segmented continuation after the platform wall limit

The original formal job `pt-x0dxui5n` was suspended by the platform after
32:18:41. Its metrics reached update 64,345 / 16,866,727,424 valid prediction
tokens, while its latest complete recovery checkpoint was update 64,000 /
16,776,287,744 tokens. The latter is the only continuation coordinate.

Read-only inspection found that the main execution tree had subsequently gained
eight checkpoint-analysis Python/shell files. The formal trainer includes every
Python/shell file below `dense_sae/` and `scripts/` in its contract, so resuming
from that later expanded tree would correctly refuse an inexact restore. No
contract check was weakened and no analysis file was removed. Instead, the
preserved submitted archive
`handoff/dense_sae_formal50b_exact_submitted_source_20260912T1130Z.tar.gz`
(SHA-256 `9df2134d680bbe9d3319ba4afc1c2bd093e4b7641d9db7929a895de48a3eacd5`)
was extracted to
`continuation_sources/formal50b_submitted_20260912T1130Z/`. Recomputing its
config, data, execution-scope and 25 source hashes reproduced the original
training contract exactly:
`c114a1a5e6c3ea16980daad3c59034f43f5899bd995b3be99cf0aa7b82056430`.

Operational continuation tooling was added outside the frozen source scan. It
requests a synchronized STOP after 113,400 seconds (31 h 30 min), leaving about
30 minutes before the 32-hour device limit, and promotes the first complete
recovery checkpoint at or after 17B, 19B, ..., 49B into a permanent external
archive. Because recovery checkpoints occur every 1,000 updates, the archived
coordinate may exceed its named threshold by less than 262,144,000 tokens. The
trainer's exact 30B and 50B milestones remain unchanged. Promotions hard-link
when supported, fall back to copying, rehash every manifest file and publish by
atomic directory rename. The archive is outside the trainer's 60 GiB run-root
guard and remains valid after rolling recovery retention.

Qualification before submission passed: 38 tests in the later SAE workspace,
27 tests in the submitted frozen snapshot, Python compilation, shell syntax,
dry-run, a temporary end-to-end promotion/integrity/idempotence fixture, exact
contract recomputation, and a full CPU load of the 4.115 GB latest checkpoint.
The full load restored 96 model tensors, 94 AdamW state entries in three groups,
scheduler epoch 64,000, update/token/data cursors and loader/SAE RNG state.

Continuation job `pt-srfey9kz`, display name
`dense-sae30k-bottleneck8-50b-resume-s2-full-20260914T012152Z`, was submitted
through the execution-envelope template to one `h100-4-reserved` node with four
H100 80 GB devices and image `shphd-lite-0911`. It entered `RUNNING` at
2026-09-14 01:27:04 UTC. Live process inspection confirmed the 113,400-second
timer, checkpoint archiver, four-rank torchrun and explicit `--resume` path.

The resume completed successfully. The stale metrics tail for updates
64,001--64,345 was retained under `recovery_history/`, and the authoritative
metrics ledger restarted with exactly update 64,001 / 16,776,549,888 tokens.
After more than five minutes the run remained healthy with finite, nonzero LM
and SAE losses/gradients and no failure artifact. This is startup and restore
evidence only; the job remains an incomplete formal run, and no scientific
claim follows.

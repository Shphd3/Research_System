# A15_17_01_E04 — Exact-15B Lambda Reuse Comparison

## 1. Question / hypothesis tested

This round tests whether the distinct exact-15B S7 model trained with
`lambda_rec=0.1` has both greater native Top-32 usage-profile reuse and lower
native effective dimension than the distinct exact-15B S7 model trained with
`lambda_rec=1.0`.

The registered contrast is `lambda=0.1 minus lambda=1.0`. The comparison is
descriptive and same-architecture at a matched 15B token coordinate; it is
not an isolated causal estimate of the reconstruction coefficient because the
training runs have different microbatch/accumulation partitions and therefore
different optimization and RNG histories.

## 2. Setup and controlled variables

- Frozen panel: 192 N8 records, 256 valid body tokens per record.
- Native site: `blocks[7].attn.o`, after attention output projection and before
  residual addition.
- Frozen checkpoints: the exact 15B `lambda_rec=1.0` original S7 model and
  exact 15B `lambda_rec=0.1` from-scratch S7 model named in `protocol.md`.
- Matched: architecture, initial state, data manifest, tokenizer, layer-7
  sidecar site, SAE width 30,000, native K=32, CE chunk size 128, and nominal
  262,144 source-training tokens/update.
- Known difference: microbatch/accumulation `(2,16)` versus `(32,1)`.
- Execution: four RTX 5090 workers, read-only forward extraction, no optimizer
  update and no checkpoint write.

## 3. Data and analysis

For each record, the run extracts the normalized native Top-32 usage profile
and the pooled native attention-write vector. It reports the paired bootstrap
95% interval for usage-profile cosine difference over 2,000 draws and the
participation-ratio effective dimension for each model. The exact branch rules
are frozen in `protocol.md`.

## 4. Result

`NOT RUN — direct full submission requested; scientific result pending.`

The separate engineering Smoke is intentionally recorded as
`NOT_RUN_DIRECT_FULL_USER_REQUEST`; this is not a Smoke PASS claim. The full
run must establish its own GPU, loader, alignment, numerical, and
immutability guards before producing a result.

## 5. Insight, claim boundary, and next decision

No scientific judgment is available before the full measurement completes.
The result may support only a same-architecture exact-15B descriptive
contrast, and cannot by itself establish semantic quality, utility, or a
causal effect of `lambda_rec`.

The next decision is to read the completed result against the registered
branches, then decide whether the observed reuse/dimension relation survives a
future control that isolates the remaining microbatch and training-history
confound.

## Execution record

- Protocol: `APPROVED_FOR_DIRECT_FULL_EXECUTION`.
- Execution workspace:
  `/data/250010109/MoE_Router/experiments/20260922_s7_15b_lambda_compare_reuse_audit`.
- The first submission, `pt-qyze07hl`, remained in `STARTING` with its worker
  `Pending` and was explicitly stopped by the researcher request; it reached
  `SUSPENDED` at 2026-09-22 15:33:01 UTC. Its receipt is
  `/data/250010109/MoE_Router/experiments/20260922_s7_15b_lambda_compare_reuse_audit/manifests/submission_receipts/submit-a15-17-01-e04-15b-lambda01-vs-lambda1-full-20260922T143504Z-20260922T143511Z.json`.
- A replacement direct-full submission, `pt-kjvn438a`, was accepted on
  2026-09-22 at 15:33:24 UTC and was `STARTING` with its four-GPU worker still
  `Pending` at the last check. Its receipt is
  `/data/250010109/MoE_Router/experiments/20260922_s7_15b_lambda_compare_reuse_audit/manifests/submission_receipts/submit-a15-17-01-e04-15b-lambda01-vs-lambda1-full-retry-20260922T153322Z-20260922T153322Z.json`.
- The replacement run root is
  `/data/250010109/MoE_Router/experiments/20260922_s7_15b_lambda_compare_reuse_audit/runs/full_4x5090_20260922T153322Z_retry`.

## 2026-09-22T16:28:20Z — two-card engineering Smoke requested

The verified state of the first direct-full task `pt-qyze07hl` is `SUSPENDED`
at `2026-09-22T15:33:01.820123Z`; its worker is `Deleted` and no terminal
application result exists. The researcher requested a separate two-card task to
test runtime success. This is recorded as Amendment A1 in the Protocol and is
not a scientific result.

The two-card scope uses `5090-2-spot`, one exact-15B checkpoint per GPU, and the
same four frozen smoke batches: 16 records / 4,096 body tokens per model. Its
required artifacts are two worker receipts, native-support arrays, identity and
terminal receipts. It does not calculate the full-panel reuse contrast,
bootstrap, effective dimension, or any E04 scientific branch. Submission and
startup evidence will be appended below; until a terminal receipt exists the
Smoke state is `NOT RUN` or `UNKNOWN`, never `PASS`.

## 2026-09-22T16:36:30Z — two-card platform startup failure and revocation

The two-card engineering Smoke submission `pt-84lr8rw6` was explicitly
revoked after the platform event stream showed repeated container startup
failures. Image pulls completed successfully, but containerd repeatedly failed
before the startup script could run:

`failed to create containerd container: failed to mount
/data/containerd/root/tmpmounts/containerd-mount...: failed to mountat: failed
to mount: no such file or directory`.

The same event stream also contained an earlier `pod has unbound immediate
PersistentVolumeClaims` scheduling warning. The job had no Pod IP and no
application log or terminal receipt. Therefore no checkpoint was loaded, no
model forward ran, and no scientific Smoke or E04 measurement exists.

This is classified as a platform-side containerd/PV mount failure on the
selected 5090 node, not a two-card-versus-four-card capacity diagnosis and not
an implementation failure. The image was pulled successfully, which makes
image availability/authentication an unlikely cause. The job stop request was
accepted at `2026-09-22T16:36:07Z`; the platform subsequently reported
`SUSPENDING` with the worker `Terminating`.

The researcher requested one bounded retry with the same 5090-2 spot profile,
image, and `/data` mount, allowing the scheduler to select another worker.
This retry is still engineering-only and cannot be called a Smoke PASS unless
the application reaches its own terminal receipt. If the same pre-application
containerd/PV error recurs, no further automatic retry is justified; the
platform/node/PV issue must be escalated.

## 2026-09-22T16:37:15Z — bounded retry submitted

The revoked job `pt-84lr8rw6` reached platform state `SUSPENDED` at
`2026-09-22T16:37:15Z`. One bounded retry was submitted with the unchanged
`5090-2-spot` profile, image, `/data` PV mount, and engineering Smoke command:

- Job: `pt-inogpk3h`
- Run root:
  `/data/250010109/MoE_Router/experiments/20260922_s7_15b_lambda_compare_reuse_audit/runs/two_card_smoke_2x5090_20260922T163657Z`
- Receipt:
  `.../submit-e04-two-card-retry-20260922T163657Z-20260922T163713Z.json`
- Startup observation: platform `STARTING`, worker `Pending`, scheduler host
  `10.115.73.113`, no Pod IP yet.

This is a scheduling/startup observation only. It is not evidence that the
container was created or that the Smoke passed. No further retry is registered
unless this attempt reaches a terminal platform or application receipt.

## 2026-09-22T16:47:03Z — retry failure diagnosed and execution guard repaired

The retry `pt-inogpk3h` did reach a real Pod on host `10.115.73.113` with Pod
IP `10.120.2.158`; therefore the earlier containerd/PV startup failure did not
recur on this node. It nevertheless ended in platform state `FAILED`, with
terminal receipt status `FAIL`, before any checkpoint or model forward.

The durable Pod log identifies the immediate failure:

`.../detailed.md: FAILED`

The Smoke launcher was validating a shared workspace checksum file after the
run had been frozen. The execution record `detailed.md` was then appended with
the retry status, so a mutable research ledger was incorrectly treated as an
immutable execution input. This was an orchestration/integrity-guard bug, not
a model, GPU, containerd, or checkpoint failure.

The repair is twofold: the launcher now reads the checksum file inside the
specific run root rather than the shared latest-run manifest, and
`detailed.md` is no longer included among the frozen files. The run-specific
freeze still covers the code, manifests, checkpoints, protocol, runtime
activation script, and external dependency manifest. A new two-card attempt
must be prepared after this repair; the failed retry is not a Smoke result.

## 2026-09-22T16:49:00Z — second retry failure diagnosed and run-root contract repaired

The fixed-integrity retry `pt-hjt1nduj` reached `RUNNING` on host
`10.115.73.113` with Pod IP `10.120.7.14`. Its durable log shows that all
34 frozen-file checks passed, the mounted Blackwell runtime passed, and all 12
local unit tests passed. It then stopped before model loading with:

`FileExistsError: .../runs/two_card_smoke_2x5090_20260922T164728Z`.

The preparation step intentionally creates the run root and places the frozen
manifest and source snapshot there, while the runner incorrectly required the
output directory not to exist. This was a second execution-orchestration bug,
not a platform, GPU, checkpoint, or scientific failure. The runner is repaired
to require a prepared run root while rejecting only an existing `stages/` or
terminal receipt. A new prepared run is required before another submission.

## 2026-09-22T16:50:22Z — repaired Smoke resubmitted

After both launcher defects were repaired, the local Python checks and all 12
unit tests passed, and the new run-specific freeze verification returned exit
code 0 with 34 frozen files. The repaired engineering Smoke was submitted as:

- Job: `pt-8t4e2vbi`
- Run root:
  `/data/250010109/MoE_Router/experiments/20260922_s7_15b_lambda_compare_reuse_audit/runs/two_card_smoke_2x5090_20260922T165008Z`
- Receipt:
  `/data/250010109/MoE_Router/experiments/20260922_s7_15b_lambda_compare_reuse_audit/runs/two_card_smoke_2x5090_20260922T165008Z/submit-e04-two-card-final-fixed-20260922T165008Z-20260922T165022Z.json`

The last bounded startup observation found platform state `STARTING`, worker
`Pending`, and scheduler host `10.115.73.43`; no Pod IP or application output
was available yet. This remains an engineering Smoke only and is not a
scientific result or a `SMOKE_PASS` claim.

## 2026-09-22T17:08:01Z — four-card full run submitted after Smoke PASS

The two-card engineering Smoke `pt-8t4e2vbi` completed with platform state
`SUCCEEDED`, terminal receipt `PASS`, and `SMOKE_PASS` status `PASS`. After
refreshing a per-run 27-file freeze manifest and re-running the 12 local unit
tests, the registered direct-full E04 task was submitted:

- Job: `pt-amc9srk8`
- Profile: `5090-4-spot`; image: `shphd-lite-0911`
- Run root:
  `/data/250010109/MoE_Router/experiments/20260922_s7_15b_lambda_compare_reuse_audit/runs/full_4x5090_20260922T170609Z`
- Submission receipt:
  `/data/250010109/MoE_Router/experiments/20260922_s7_15b_lambda_compare_reuse_audit/runs/full_4x5090_20260922T170609Z/submit-e04-full-fixed-20260922T170609Z-20260922T170625Z.json`

The bounded startup check found platform state `RUNNING`, one worker with four
RTX 5090 devices on host `10.115.73.136`, Pod IP `10.120.7.27`, and all frozen
source checks, Blackwell runtime validation, and 12 unit tests passed. The
full run reached `FULL_TARGET_PREFLIGHT_PASS` and created four worker logs.
No scientific result is available yet; polling stops here and the remote full
run continues.

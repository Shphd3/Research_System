# Continuation Brief: paired SAE-bottleneck and native-baseline pretraining

```text
Workstream:     matched representation-evolution training
Problem key:    none (engineering/training continuation)
Role:           PRIMARY
Record:         .research/memory/conversations/0912-sae-llm训练执行/
Continues from: ../0912-梳理-sae-动态形成预训练方案/continuation.md
Supersedes:     continuation_formal_sae_50b_active_superseded_20260912T111830Z.md
Updated at:     2026-09-13T13:26:17Z
Status:         SUPERSEDED
Non-canonical:  points at canonical sources; owns no claim, approval, verdict,
                or next decision.
```

## A. Environment roots

| Root | Path | Readable here? |
| --- | --- | --- |
| Research records | `/data/250010109/Research_System` | yes |
| SAE execution workspace | `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining` | yes; not Git |
| Baseline execution workspace | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining` | yes; not Git |
| Frozen data view | `/data/250010109/training_data_views/dclm_pair_v1` | yes |
| Tokenizer | `/data/share/Qwen3-0.6B-Base` | yes |
| 5090 runtime layer | `/data/250010109/dependency_packages/dense_baseline_torch280_cu128_py310` | yes; immutable after Smoke qualification |

Use each execution workspace's `scripts/runtime.sh`; do not modify the base
image. Never let the two formal jobs share a run directory or checkpoint.

## B. Read list — in order; stop if a required item is absent

| # | Path | Answers which question | Required? |
| --- | --- | --- | --- |
| 1 | `/data/250010109/Research_System/AGENTS.md` | What authority, observability and evidence rules apply? | yes |
| 2 | `/data/250010109/Research_System/docs/training_observability_contract.md` | Which telemetry and token coordinates make later comparison eligible? | yes |
| 3 | `/data/250010109/Research_System/docs/execution_envelope.md` and `docs/training_reuse_index.md` | Which profiles, image, entry point and reused training sources are allowed? | yes |
| 4 | This record's complete `memory.md` | What was requested, changed, submitted and deliberately not monitored? | yes |
| 5 | `daily_research_reports/0912/docs/dense_sae_30k_smoke/execution_scope_full_50b.md` and sibling `execution_record.md` | What is the active SAE run's contract and evidence boundary? | yes |
| 6 | `daily_research_reports/0913/docs/dense_baseline_10b/execution_scope.md` and sibling `execution_record.md` | What is the baseline contract, qualification evidence and submission boundary? | yes |
| 7 | Baseline execution `configs/full_8x5090_baseline_10b.json`, `README.md`, `scripts/run_full_8x5090.sh`, and the formal submission receipt | What exact behavior was submitted and how is same-directory recovery performed? | yes |
| 8 | SAE execution `configs/full_4h100_sae30k_50b.json`, `README.md`, and `scripts/run_full_4h100.sh` | What exact SAE behavior is active and how is it recovered? | yes |
| 9 | `daily_research_reports/0913/docs/dense_sae_checkpoint_audit/execution_scope.md` and sibling `execution_record.md` | What fixed-heldout audit is running, what passed, and where are its outputs? | yes for audit follow-up |

No Focus, Anchor or formal Protocol owns a scientific comparison yet. Do not
reconstruct one from this brief, job names, losses, checkpoints or telemetry.

## C. Authority and boundaries

- Approved execution scope: the researcher authorized the formal native
  baseline submission after the four-RTX5090 Smoke passed; the exact contract
  is owned by `daily_research_reports/0913/docs/dense_baseline_10b/execution_scope.md`.
  The previously authorized SAE 50B contract is owned by the 0912 full-run
  execution scope.
- Current instruction boundary: baseline submission was requested, but startup
  supervision was explicitly not requested in this task. Job acceptance is not
  evidence that it started, is healthy or will complete.
- Long-running supervision boundary: unless the researcher explicitly asks for
  continuous or completion-time monitoring, observe only a short startup or
  Smoke window, report the last verified progress and ETA, stop polling, and
  leave the remote job running. Stopping supervision never authorizes a
  duplicate submission.
- NOT approved: do not create another independent baseline or SAE run; do not
  change architecture, data order, effective global batch, optimizer,
  token-based schedules, checkpoint milestones or loss definitions; do not
  retrofit TensorBoard into the already active SAE run; do not begin
  representation evaluation without a separate approved analysis contract.
- May not claim: no semantic formation, interpretability, convergence,
  downstream capability, SAE benefit/harm or causal representation difference
  follows from Smoke, loss curves, submission state or checkpoint existence.
- Human-owned decision still open: the exact matched-checkpoint representation
  analysis and its scientific interpretation. Until confirmed, preserve the
  runs and report only operational evidence.

## D. Execution prerequisites

- Baseline target is the explicit `5090-8-spot` profile and
  `shphd-lite-0911` image key resolved by `docs/execution_envelope.md`; the old
  `ngc-pytorch-25-06` image is prohibited for new jobs.
- Submission/recovery entry point is baseline execution
  `scripts/run_full_8x5090.sh`, guarded by the approved-scope and passed-Smoke
  flags. It auto-resumes only from that run directory's complete latest
  checkpoint.
- Baseline input/config identity and fixed parameters are owned by
  `configs/full_8x5090_baseline_10b.json` and the 0913 execution scope: frozen
  30B data view, seed 17, eight ranks, 262,144 effective prediction tokens per
  update, exactly 10B trained tokens, and milestones at 0/0.5B/1B/3B/5B/10B.
- The designated baseline formal output is
  `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z`.
  It may not exist until the scheduled pod starts.
  The acceptance receipt is
  `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/acp_receipts/submit-dense-native-baseline-8x5090-10b-full-20260913T102944Z-20260913T102944Z.json`.
- Before any later recovery counts, verify the same profile/image/config/run
  directory, a complete checkpoint manifest, monotonic token/update counters,
  and coordinate-continuous TensorBoard segments. Never silently start fresh.

## E. Action list — in order; every step carries a branch

| # | Action | Verify | If pass | If fail |
| --- | --- | --- | --- | --- |
| 1 | Inspect | When the researcher next asks, query baseline job `pt-79x53njx`, its durable log, metrics, TensorBoard segments, latest checkpoint pointer, and failure/terminal receipts | Leave the same job alone if queued or healthy | Preserve artifacts and diagnose; do not resubmit |
| 2 | Resume | Only after a confirmed interruption, verify a complete latest checkpoint and the exact submitted tuple/config/run directory | Invoke the existing full-run script against the same run directory | Stop and report the identity or checkpoint mismatch |
| 3 | Verify | At each baseline milestone, check exact `tokens_seen`, `complete=true`, expected state/RNG inventory, sizes and hashes | Record operational milestone evidence | Record the incomplete/corrupt state and stop before evaluation |
| 4 | Close | Require exactly 10B tokens, all six baseline milestones, terminal exit 0, platform `SUCCEEDED`, finite required scalars and final observability/artifact audits | Record operational completion only | Keep the run incomplete; a scheduler status or last loss alone is not completion |
| 5 | Finish current SAE audit | On a later researcher status request, inspect existing job `pt-p5mlwlqn` and its full audit/terminal receipts; do not poll it continuously now | Verify all five fixed checkpoints, full token count and required plots, then report | Preserve partial outputs and diagnose; do not resubmit automatically |
| 6 | Compare | Only after the researcher approves an analysis contract, pair native and SAE checkpoints on cumulative valid prediction tokens | Run evaluation without optimizer updates and report its evidence boundary | Mark the comparison ineligible rather than changing alignment rules |

## F. Current state

- Baseline formal job `pt-79x53njx` was accepted at
  2026-09-13T10:29:46Z as `SUBMITTED`; it was deliberately not polled after
  submission. Therefore startup health, runtime throughput and ETA from live
  progress are unknown in this brief.
- Baseline formal run:
  `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z`.
  It had not yet materialized at the final local check.
- Final baseline gate job `pt-kky1ihlb` is `SUCCEEDED`: 100 logical updates,
  26,214,400 tokens, terminal exit 0, exact external-process recovery,
  TensorBoard audit PASS, and hash-verified step-0/50/100 checkpoints. It is an
  engineering qualification, not a scientific comparison.
- Four-GPU steady throughput was 117,126 tokens/s. Assuming 1.7--1.9x
  eight-GPU scaling gives 12.8--14.3 hours including expected checkpoint and
  validation overhead, central estimate 13.5 hours; queueing and SPOT
  interruption are excluded and no eight-GPU rate has yet been measured.
- Separate SAE job `pt-x0dxui5n` was last read as `RUNNING` at about
  2026-09-13T10:04Z, step 45,609 and 11,955,332,096 tokens, with the 10B
  milestone complete and no failure/terminal receipt. This is a time-stamped
  observation, not confirmed-current state.
- Rejected/retracted: do not use the old NGC image; do not use the earlier
  update-only TensorBoard Smoke as final comparison qualification; do not
  submit a second run while the recorded job may still be queued or active.
- Fixed-heldout SAE checkpoint audit job `pt-p5mlwlqn` is running on two RTX
  5090 SPOT GPUs using the current image plus the qualified mounted SM120
  runtime. Its five-checkpoint Smoke passed at 13:10:24Z on the same 16,384
  tokens and produced all required outputs. At the final bounded snapshot
  (13:26:17Z), full evaluations for 0.5B and 1B had each completed exactly
  114,987,008 tokens; 3B, 5B and 10B remained. The observed 7.25-minute
  checkpoint interval implied about 22--25 minutes remaining, excluding SPOT
  interruption. Continuous supervision stopped by researcher instruction; the
  job remains running and no full-result claim exists yet.
- Live concurrency risk: the scheduler/job processes may write their own run
  directories. A successor reads first and never edits active outputs.

## G. Completion contract

- Baseline deliverables: exact 10B terminal state, complete milestone
  checkpoints at 0/0.5B/1B/3B/5B/10B, hashes/manifests, complete metrics and
  TensorBoard coordinates, terminal and independent audit receipts.
- Baseline is operationally done only when all deliverables above and platform
  success agree. `SUBMITTED`, `RUNNING`, a declining loss, or a checkpoint
  directory by itself is not completion.
- SAE remains a separate 50B contract with milestones
  0/0.5B/1B/3B/5B/10B/15B/30B/50B; do not reduce it to match baseline.
- Stop and ask the researcher before changing any scientific comparison,
  architecture, objective, data path or training budget. Never trade a reduced
  contract for a `COMPLETE` label.
- The current audit is complete only when its `full/audit_receipt.json` is
  `PASS`, all five checkpoint summaries each report 114,987,008 tokens, all
  required plots/text exist, terminal exit is zero and platform state agrees.
  Smoke success and two completed checkpoints are not the full audit result.

## H. Reusable assets — reuse before rewriting

| Asset | Path | Reuse for | Verified? |
| --- | --- | --- | --- |
| Baseline formal code/entry | baseline execution `scripts/run_full_8x5090.sh`, `scripts/run_train.sh`, `dense_sae/` | same-directory formal recovery | yes; final Smoke qualified |
| Baseline formal config | baseline execution `configs/full_8x5090_baseline_10b.json` | exact 10B behavior | yes; dry run and submission resolved |
| Qualified source snapshot | baseline execution `handoff/dense_baseline_10b_4gpu_observability_smoke_pass_source_20260913T100725Z.tar.gz` | submitted source provenance | yes; SHA-256 `25d9977e2f8cde645b8be30e925e2232a9607618ff064bcc03e7b0719217c4c6` |
| 5090 runtime layer | `/data/250010109/dependency_packages/dense_baseline_torch280_cu128_py310` | PyTorch 2.8/CUDA 12.8 SM120 runtime | yes; four-GPU BF16/NCCL qualified |
| Final Smoke evidence | baseline execution `runs/smoke_4x5090_observability_final_20260913T094622Z/` | recovery, telemetry, throughput and checkpoint gate | yes; receipt and audits PASS |
| Submission receipt | baseline execution `acp_receipts/submit-dense-native-baseline-8x5090-10b-full-20260913T102944Z-20260913T102944Z.json` | exact accepted job and resolved tuple | yes; exit code 0 |
| SAE formal source/config | SAE execution `handoff/dense_sae_formal50b_exact_submitted_source_20260912T1130Z.tar.gz`; `configs/full_4h100_sae30k_50b.json` | preserve/recover active SAE run | yes; owning 0912 record has hashes |
| Training telemetry contract | `/data/250010109/Research_System/docs/training_observability_contract.md` | later token-aligned eligibility audit | yes |
| Continuation template | `/data/250010109/Research_System/templates/research_process/continuation_brief_template.md` | future continuation rewrites | yes |
| SAE checkpoint-audit run | SAE execution `runs/checkpoint_audit_2x5090_0p5_1_3_5_10b_20260913T125500Z/` | full fixed-heldout reconstruction/activation audit | active; Smoke PASS, full incomplete at last snapshot |
| Audit submission receipt and source snapshot | SAE execution `acp_receipts/submit-dense-sae-ckpt-audit-2x5090-0p5-1-3-5-10b-20260913T125500Z-20260913T125520Z.json`; `handoff/dense_sae_checkpoint_audit_2gpu_pre_gpu_20260913T125131Z.tar.gz` | exact resource tuple and submitted audit source provenance | yes |

Assets are tools and provenance pointers, not scientific evidence. Eligibility
and claims remain owned by the execution records and any later approved
analysis records.

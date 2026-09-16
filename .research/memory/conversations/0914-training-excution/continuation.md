# Continuation Brief: SAE-Mediated formal 50B segment 1 running

```text
Workstream:     SAE-Mediated 50B versus native Dense baseline
Condition:      sae_mediated_live_recon_auxk_sae_only
Role:           PRIMARY
Record:         .research/memory/conversations/0914-training-excution/
Continues from: same record, 2026-09-14T15:39:30Z entry
Updated at:     2026-09-14T15:39:30Z
Status:         CURRENT
Non-canonical:  points at owning sources; owns no scientific verdict.
```

## A. Live run

| Item | Value |
| --- | --- |
| Job | `pt-j5ir9b2h` |
| Run root | `/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk/runs/sae_mediated_formal50b_4h100_20260914T153000Z` |
| Workspace | `/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk` |
| Protocol | `/data/250010109/Research_System/daily_research_reports/0914/sae_mediated_pretraining/protocol.md` |
| Contract SHA-256 | `1be4d158ed2c561e81ea1dfb703c2773c8160715f25d4674401786272f018dfd` |
| Initial backbone SHA-256 | `6bf36f66f9f33784812eb9f33efb672223c703dcea7140f966e1f4e47d0cfb59` |

## B. Frozen execution contract

- Target: 50,000,000,000 globally valid prediction tokens; max step 190749.
- Data: frozen DCLM 30B prefix, seed 17, cycling enabled only to reach 50B.
- Parallelism: four H100, microbatch 2, accumulation 16, ordinary update 262,144 targets.
- Model: 8x1024/3072 Dense backbone plus width-30,000 TopK-32 serial SAE.
- Objective: LM traverses SAE; live main reconstruction uses lambda 1; AuxK coefficient 1/32 is SAE-only.
- Exact Dense-matched milestones: 0/0.5/1/3/5/10/15/17/19/.../49/50B.
- Extra non-boundary snapshots: 0.1/0.3/7/13B, saved after the first full update at or beyond the target.
- Recovery: every 1000 updates, latest two retained; total run storage gate 140 GiB.
- Segmentation: 31h30 per ACP job, always resume the same run root and unchanged contract.

## C. Last verified state

- Segment 1 is RUNNING; startup worker and four GPUs are healthy.
- Last supervised point: step 66 / 17,301,504 valid tokens.
- Replay 50-to-51 passed: LM and SAE losses exact, sampled state maximum difference `5.960464477539063e-08`, one extra physical update recorded.
- Observed throughput: about 130k-146k valid targets/s. Segment 1 is expected to reach roughly 15-16B; complete 50B is approximately 100-105 hours and likely four segments.
- Startup supervision is complete. Leave the job running and do not poll or resubmit without a new request.

## D. Later status/resume procedure

1. Query job `pt-j5ir9b2h`; inspect `metrics.jsonl`, TensorBoard, `latest_checkpoint.json`, `latest_milestone.json`, failure files and segment receipts.
2. Near 2026-09-15 23:05 UTC the timer should create `STOP`, save a complete recovery checkpoint and exit code 75. Verify this before any continuation.
3. Submit the next segment with `continuation/run_formal_50b_segment_31h30.sh` against the exact same run root. Never use a fresh run root for continuation.
4. At 50B require `training_receipt.json`, terminal exit 0, `tensorboard_audit.json`, final checkpoint and endpoint metrics before scientific reading.

## E. Removed mistaken run

- Job `pt-4xpr7b42` was stopped at step 235 and is `SUSPENDED`.
- Its run files, development config and development launcher were deleted.
- Minimal cancellation evidence remains at `audit/cancelled_dev1024_20260914T151639Z.json`; scientific use is NONE.

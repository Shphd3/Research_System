# Detailed: A15_17_01_E02 S7 17B history comparison

Status: NOT RUN at registration 2026-09-22T09:49:21.676604+00:00. [Protocol](protocol.md) owns direct-full scope and user smoke waiver. No result or mechanism judgment yet.

## 1. Question

Does the user-selected same-topology/current-lambda S7 pair differ in model-local support reuse and aligned native geometry? No directional effect assumed.

## 2. Setup

Two exact17B user checkpoints, native layer8,K32,width30000,mean pooling; fixed192×256 N8 panel. Same recorded initial parameter hash, differing lambda history plus microbatch/accumulation/CE chunking. Not a strict single-variable ablation. Full provenance: `/data/250010109/MoE_Router/experiments/20260922_s7_17b_training_history_reuse_audit/manifests/training_lineage_audit.json`.

## 3. Training data

No new training;0 optimizer updates. Frozen source checkpoints only. Historical shared training manifest does not establish identical sampled updates.

## 4. Testing panel

Inherited fixed192-record N8 panel, no labels/no exclusions; record bootstrap2000,seed20260922. Existing-panel exploratory comparison, not sealed confirmation.

## 5. Result / execution

NOT RUN. User explicitly waived new smoke before any submission. Local12 numerical/fingerprint tests pass; engineering-only. Code root `/data/250010109/MoE_Router/experiments/20260922_s7_17b_training_history_reuse_audit`; outputs and receipts will be appended below. Formal result Summary deferred until researcher asks for postrun analysis.

## 6. Boundary / next action

Submit the authorized direct-full job with embedded guards; after accepted submission and bounded startup inspection stop polling. Preserve the job ID for later terminal/independent audit. No fallback/retry, no scientific judgment, no commit/push.

## 7. 2026-09-22T09:51:48.865568+00:00 — Direct full submitted; supervision stopped

Supersedes registration NOT RUN only as execution status, not as a result: `pt-ooc6qhru` accepted, platform `STARTING`; single four-GPU worker Pending with host assigned and no pod IP. No runtime or terminal receipt yet. New smoke was explicitly waived, not passed. Twelve local tests, syntax and local merge-schema regression passed before freeze;49 source/input/contract files frozen and snapshotted. No model forward ran locally and no full scientific statistic was inspected.

[Execution certificate](/data/250010109/MoE_Router/experiments/20260922_s7_17b_training_history_reuse_audit/runs/full_4x5090_20260922T095023Z/execution_certificate.md); [submission receipt](/data/250010109/MoE_Router/experiments/20260922_s7_17b_training_history_reuse_audit/runs/full_4x5090_20260922T095023Z/submit-s7-history17b-full-4x5090-20260922T095023Z-20260922T095041Z.json); [platform startup snapshot](/data/250010109/MoE_Router/experiments/20260922_s7_17b_training_history_reuse_audit/runs/full_4x5090_20260922T095023Z/platform_describe_startup.json). Raw/source evidence stays in execution workspace.

User-requested stop after submission/startup is now honored. No continuing polling, no fallback/resubmission, no new smoke. Researcher will notify when ready for terminal inspection and independent postrun numerical/artifact audit, followed by Purpose/Hypothesis/Analysis method/Conclusion in summary.md and summary_cn.md. No full result is claimed.

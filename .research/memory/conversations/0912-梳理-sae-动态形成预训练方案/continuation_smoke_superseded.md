# Continuation Brief: Dense LM / SAE 30k engineering smoke

```text
Workstream: random-initialized Dense LM with detached final-layer SAE
Problem key: none (engineering stage; no scientific key selected)
Role: PRIMARY
Record: .research/memory/conversations/0912-梳理-sae-动态形成预训练方案/
Continues from: none (same source conversation)
Supersedes: continuation_preparation_superseded.md (Status: SUPERSEDED)
Updated at: 2026-09-12T08:22:48Z
Status: SUPERSEDED
Non-canonical: points at owning sources; owns no claim, approval, verdict or next decision.
```

## A. Environment roots

- Repository: `/data/250010109/Research_System`, readable.
- Execution package: `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining`, readable.
- Evidence: execution package `runs/` and `acp_receipts/pod/`, readable shared storage.
- Data: `/data/250010109/training_data_views/dclm_pair_v1`, readable; tokenizer `/data/share/Qwen3-0.6B-Base`, readable.
- Historical training: `/data/250010109/Research_System/Projects/decommon-router-training`, readable but root-Git-ignored.
- Activate `scripts/runtime.sh` for the existing ONNX/protobuf compatibility setting and mounted tokenizer layer. No base install. Use scoped find/grep because rg is unavailable.

## B. Read list — in order

| Required source | Answers which question |
| --- | --- |
| This directory's entire `memory.md` | What changed within this source task? |
| Repository `AGENTS.md`, `docs/training_reuse_index.md` | What authority and source-reuse rules apply? |
| Repository `daily_research_reports/0912/docs/dense_sae_30k_smoke/execution_scope.md` | What bounded engineering scope is attributed to the researcher request? |
| Sibling `execution_record.md` | What passed or failed; where is the evidence? |
| Execution `README.md`, `docs/reuse_sources.json`, `configs/smoke_4h100_sae30k.json` | What was copied/adapted; what runs? |
| Execution `runs/local_checks/probe_fix_receipt.json` | Which repaired sources passed local tests? |
| Active run `run_receipt.json`, refreshed `platform_status.json`, available runtime/terminal outputs | What is actually executing or complete? |
| Repository `docs/execution_envelope.md` | Who owns resource/image/submission resolution? |

All above sources are required. Active run: execution `runs/smoke_4h100_sae30k_fix_20260912080957`, job `pt-ro6ijc54`. Failed run: `runs/smoke_4h100_sae30k_20260912080130`, job `pt-i9ohovsb`. Absent terminal outputs while a job runs are pending evidence. No formal pretraining Anchor/Protocol exists for this engineering stage; do not reconstruct one from memory. The 0912 design materials and old preparation brief are context, not experimental evidence.

## C. Authority and boundaries

The source task now explicitly requests reuse/adaptation of prior training code, SAE expansion to 30,000 and four-card Smoke. The execution scope records this authorization; earlier read-only instructions no longer prohibit that requested stage. No formal training, additional model/loss/router/MoE module, semantic label definition, scientific hypothesis or mechanism judgment is authorized. Memory and smoke success do not supply those decisions. Preserve failures; do not change profile/model/optimizer/data silently to obtain PASS.

## D. Execution prerequisites

The submitted job is complete: do not submit a duplicate or restart it. Its run receipt owns exact commands, image URL, mount and the reduced outer time bound following the initial failure. Scope/config own update, replay, checkpoint and storage requirements. Read remote-experiment-workflow and sco-control before platform operations. The current Codex source task completed monitoring. Preserve the qualified source hashes and completed outputs.

## E. Action list

| Action | Verify | If pass | If fail |
| --- | --- | --- | --- |
| Read terminal record | pt-ro6ijc54 SUCCEEDED, PASS and exit-0 receipts plus artifact_verification.json | Retain completed engineering evidence | Report mismatch without launching a replacement |
| Validate terminal artifacts | exit 0, smoke PASS/all gates, manifests, counters, source/data hashes and log | Record engineering result | Preserve and report; no silent scope change |
| Update operational record | Facts trace to outputs; scientific boundary retained | Checkpoint this memory/brief | Correct unsupported or stale statements |
| Stop | No formal-run authorization | Await researcher-owned next stage | Do not treat smoke as a scientific claim |

Completion requires `smoke_receipt.json`, `terminal_receipt.json`, registered outputs and durable log. RUNNING/SUCCEEDED alone is insufficient.

## F. Current state

Code and local qualification complete. First job failed before any update: float32 parameter-probe indexing rounded the large embedding's last index out of range. Integer-only indexing fixes the reproduced defect; all 17 local tests pass. Earlier two-rank Gloo/global-batch and standalone collector checks passed; the repair changes no training math. Original failed engine, logs and receipts are retained. Repaired job completed with PASS, exit 0 and SUCCEEDED; all three checkpoint checksums and source/data/panel identities passed independent verification. The execution record owns the measured result and its limits. External CLI --resume needs initial-panel/replay/accounting adaptation before production use; no-SAE GPU overhead comparison remains unqualified. This is a bounded smoke CLI, not a full-run launch.

## G. Completion contract

The requested implementation, parameter accounting, four-GPU smoke terminal result and operational continuity are complete. Both failed and repaired attempts are preserved. Stop now; formal training and scientific analysis criteria require the researcher's next explicit decision.

## H. Reusable assets — inspect before rewriting

| Asset | Location | Reuse and verification |
| --- | --- | --- |
| Current execution package | Execution dense_sae/, configs/, scripts/, tests/ | Implemented and CPU qualified; local/remote receipts own source hashes |
| Prior data/checkpoint framework | Research_System/Projects/decommon-router-training/src/decommon_router/ | Originals preserved; copied hashes in reuse_sources.json |
| Prior optimizer/global batch | Execution docs/reference_4gpu_smoke.json | Dense/observer grouping and clipping adaptations documented |
| SAE/model/analysis reference | Repository daily_research_reports/0912/docs/code/ | Adapted package imports, targets, checkpoints and analysis interfaces |
| Historical 30k SAE config | MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/ | Width/k/optimizer source; old MLP hook/AuxK/weights excluded |
| DCLM view/tokenizer | Roots in A | Manifest/path/size/identity checked; no document-contamination proof |
| Corrected state probes | Execution dense_sae/engine.py; tests/test_pipeline.py | Integer-index regression; never restore float32 linspace |
| Submission/continuation templates | Repository templates/execution/; templates/research_process/continuation_brief_template.md | Current entrypoints; no extra registry or service |

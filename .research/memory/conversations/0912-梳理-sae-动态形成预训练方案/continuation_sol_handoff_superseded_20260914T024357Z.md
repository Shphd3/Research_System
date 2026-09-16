# Continuation Brief: Dense LM / SAE 30k code audit handoff to Sol

```text
Workstream: random-initialized Dense LM with detached final-layer SAE
Problem key: none (engineering continuation)
Role: PRIMARY
Record: .research/memory/conversations/0912-梳理-sae-动态形成预训练方案/
Continues from: none (same source task)
Supersedes: continuation_smoke_superseded.md (Status: SUPERSEDED)
Updated at: 2026-09-12T08:33:00Z
Status: SUPERSEDED by ../0912-sae-llm训练执行/continuation.md
Non-canonical: operational entry point; owns no claim, approval, verdict or scientific next decision.
```

## A. Environment roots

| Root | Path | Readable here? |
| --- | --- | --- |
| Research records | /data/250010109/Research_System | yes |
| Execution package | /data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining | yes; not a Git repository |
| Raw evidence | Execution package runs/ and acp_receipts/pod/ | yes; unchanged |
| Data / tokenizer | /data/250010109/training_data_views/dclm_pair_v1; /data/share/Qwen3-0.6B-Base | yes |

This is a shared-filesystem handoff, not an external export. Missing roots must be reported as unverifiable. Use scripts/runtime.sh for mounted dependencies/protobuf compatibility. No base-environment installation. Source code is archived separately from datasets and checkpoints.

## B. Read list — required, in order

| Source | Answers which question |
| --- | --- |
| Research_System AGENTS.md and docs/training_reuse_index.md | Rules and reusable training sources |
| This continuation and the entire sibling memory.md | Operational transitions of this source task |
| Research_System daily_research_reports/0912/docs/dense_sae_30k_smoke/execution_scope.md and execution_record.md | Prior approved engineering scope and actual evidence boundary |
| Same directory code_handoff.md | Actual file map/interfaces, six audits and acceptance checks |
| Sibling sol_handoff_prompt_cn.md, when forwarded by the researcher | Requested receiving-task engineering work and bounds |
| Execution README.md, docs/reuse_sources.json, configs/smoke_4h100_sae30k.json | What to reuse and what was configured |
| Execution handoff/baseline_manifest.json and referenced archive | Preserved code identities before edits |
| Execution runs/local_checks/probe_fix_receipt.json and successful run artifact_verification.json / smoke_receipt.json / terminal_receipt.json | Exact qualification scope and terminal evidence |

Successful run: execution runs/smoke_4h100_sae30k_fix_20260912080957 (pt-ro6ijc54). Prior failed run: runs/smoke_4h100_sae30k_20260912080130 (pt-i9ohovsb). No formal pretraining Anchor/Protocol was created. Do not invent missing scientific owners from a filename or memory.

## C. Authority and boundaries

The researcher requested preparation for a Sol code handoff. This source task prepared records and a prompt; it has not created or messaged a Sol task. When the researcher forwards the prompt, it requests local source audit, narrow engineering fixes and small CPU tests. No new GPU submission/formal training is included; prior smoke approval is exhausted by the completed stage. No new loss/router/MoE/semantic labels/scientific hypothesis, commit, push or external sync. Canonical scientific decisions remain researcher-owned.

## D. Local execution prerequisites

Preserve the code archive and old run outputs; compare hashes/current changes first. Read applicable AGENTS and source reuse instructions before edits. Activate the existing runtime and disable CUDA for local checks. Reuse checkpoint/data/optimizer components. Do not weaken contract validation to load old checkpoints after source/config changes. Write new qualification artifacts to new local directories. No job needs monitoring or restarting.

## E. Action list — for the researcher-instructed receiving task

| Action | Verify | If pass | If fail |
| --- | --- | --- | --- |
| Identify baseline | Required paths, archived hashes and current source differences | Read targeted code | Report missing/drifted files; preserve changes |
| Reproduce resume gap | Distinct Python processes, fixed contract, immutable step-zero analysis, exact cursor/log/counters | Apply minimum orchestration repair | Distinguish observed failure from missing coverage |
| Audit remaining invariants | Six points in code_handoff.md; source-backed findings | Repair demonstrated defects locally | Keep scientific/budget decisions pending |
| Validate edits | Focused CPU tests, full state and next-input comparisons, no old evidence overwrite | Record modified version and outcomes | Preserve failure; do not submit GPU to bypass it |
| Checkpoint receiving task | Own verified task name and new memory with Continues from; one CURRENT brief | Report handoff completion and stop | Do not append to this source task's memory |

A passing old Smoke is not acceptance of new code. Completion of local repair requires its own tests and evidence. Formal execution remains outside this action list.

## F. Current state

Previous engineering execution is complete with qualified receipts; its result belongs to execution_record.md. Handoff documentation and a code-only archive are complete. All 30 qualified code/config/test file hashes still match; the archive has 34 files including package/provenance documentation. No training logic changed in preparation. Distinct-process resume is the confirmed next implementation gap. The GPU probe only samples model state tensors; complete Adam state and process-level recovery need explicit coverage. The remaining audit points and boundaries are in code_handoff.md rather than duplicated here.

## G. Completion contract

This preparation is complete once paths/links, archive member hashes, preserved qualification and the single CURRENT continuation are verified. The researcher forwards the prompt. The next task finishes local fixes and records their checks, then stops for any GPU/formal or scientific decisions. Do not create a second CURRENT workstream brief without superseding this one, and never overwrite this source task's cumulative memory.

## H. Reusable assets

| Asset | Location | Reuse and verification |
| --- | --- | --- |
| Current Dense/SAE package | Execution dense_sae/, configs/, scripts/, tests/ | Actual starting code; 30 qualified hashes preserved |
| Frozen code snapshot | Execution handoff/baseline_manifest.json and archive | 34 allowlisted files; no raw results, data or environments |
| Data/checkpoint framework ancestry | Execution docs/reuse_sources.json; Research_System/Projects/decommon-router-training | Original copied-source identities and reuse priority |
| Prior optimizer/global-batch config | Execution docs/reference_4gpu_smoke.json | Existing settings; do not invent a replacement schedule |
| Test entrypoints | Execution tests/test_pipeline.py, tests/distributed_smoke.py, scripts/runtime.sh | Reuse tiny CPU fixtures and two-rank counted-step checks |
| Analysis interfaces | Execution dense_sae/analysis/; code_handoff.md | Explicit raw_h/h/sparse-z and panel/checkpoint identities |
| Evidence ledger and prompt | Repository execution_record.md; this record's sol_handoff_prompt_cn.md | Bounded facts and researcher-forwardable request |

Read these assets before rewriting them; source availability is not scientific evidence or execution approval.

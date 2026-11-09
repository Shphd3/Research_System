---
name: remote-experiment-workflow
description: "Inspect experiment status, check startup, or execute an authorized container/SSH/CCI/SCO/ACP experiment. Does not design the research hypothesis."
---

# Remote Experiment Workflow

Connect the requested operation to its Protocol, job and evidence. Paths below
are Research_System-root-relative unless linked. Read only the selected mode.

| Request | Input / reading | Finish with |
|---|---|---|
| Existing-run status | Job ID or execution record; Status below | Verified progress, source/time and failure/unknown |
| Startup / requested monitoring | Submission receipt; [startup.md](references/startup.md) | Bounded startup report or requested monitoring outcome |
| Implementation / Smoke / submit / resume | Owning explore log (exploration lane) or Protocol (formal lane); [execution.md](references/execution.md) | Authorized stage receipt, then startup boundary |
| Completed outputs / recovery | Named run/result records; [artifacts.md](references/artifacts.md) | Verified requested artifacts and evidence links |

Use `PROJECTS.md` only to resolve unknown ownership; no Graph/roadmap preamble.
For explicit SSH/CCI, read [transport.md](references/transport.md). Use
`sco-control` for needed platform commands; the execution envelope governs.
Training/resume or analysis that reads asset payloads uses the
[asset lifecycle](../../../assets/README.md#training-and-analysis-lifecycle).
Completed-training artifact handoff includes registration of actual saved
checkpoints; status-only inspection does not trigger a full asset inventory.

## Status: Inspect The Existing Job

Resolve job/output from its receipt. Inspect relevant durable logs and
progress/completion receipts, plus platform state when needed. Read the
Protocol only for a disputed gate; skip submission/training instructions.
Distinguish scheduled/running, measured progress, engineering completion and
scientific judgment. ACP completion needs the durable pod log and stage outputs,
not a platform success label or scheduling/stream-log line.

Return job ID, last verified progress/time, evidence path and failure/unknown;
ETA requires observed throughput. Stop after answering. A later status request
inspects the same job; it does not resubmit it.

## Boundaries

Existing scoped authorization needs no repeat approval. Protocol drafting is
not execution approval. Full/expensive runs, changed scope and confirmation
access follow existing authorization and frozen gates; never relax a failed
gate. Small in-scope local checks follow root AGENTS without added gates.

Append job ID, status and result paths to the owning explore log. Completion cannot update scientific judgment. Code/raw outputs/checkpoints/logs
stay execution-side; research records stay here. Preserve concurrent work.
Commit/push/publication, Graph edits and collaborator sync are explicit actions
outside this skill.

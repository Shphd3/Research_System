---
name: experiment-card-writer
description: "Use when the user asks to draft or audit an Anchor-aligned protocol.md, or to write or audit summary.md and detailed.md for a completed experiment. Do not use to redefine the research question, operate remote jobs, or publish artifacts."
---

# Experiment Protocol And Result Writer

Write or audit an Anchor-aligned experiment contract or result record. The
Anchor owns the approved question, prior, model, metric, falsifier and boundary;
this Skill must not invent or redefine them. Extra conditions or artifacts must
separate a named rival or protect the primary conclusion, not add a backlog.
Only consequential future questions belong in the project's Parking Lot; ignore
minor extras.

## Inputs And Scope

Start with the named Anchor and experiment folder. Protocol work also uses the
owning Focus; results use the frozen Protocol, actual evidence and the researcher's
judgment. Reuse explicit decisions and authorizations already given in the
session or owning records. Ask only for missing consequential judgment, not a
repeat approval or keyword. User scope and root authorization rules govern;
drafting/design confirmation never independently authorizes execution.

Preserve the existing valid folder layout. New grouped experiments use
`Projects/<project>/main/experiments/A<line>/<anchor_stem>/<experiment_id>/`
with `protocol.md`, `summary.md`, `summary_cn.md`, `detailed.md` and curated
`figures/` / `tables/`. Do not create a parallel Protocol or implementation plan.

## Select One Deliverable

Read applicable contracts completely. Multiple modes apply only when the user
requests their outputs; a result task does not reload Protocol-authoring guides.

| Request | Required reading |
|---|---|
| Protocol draft/revision, audit, confirmation, promotion or amendment | [Focus/alignment](references/protocol_focus_alignment.md), [A–G audit](references/blockwise_protocol_audit.md), and [approval/freeze contract](references/protocol_self_containment_and_freeze.md). |
| Result interpretation, Summary or Detailed write/audit | [Evidence lineage](references/result_evidence_lineage.md); inspect the frozen Protocol as evidence, not as a document to rewrite. |
| Create/revise Detailed, or audit its structure | Additionally [Detailed standard](references/detailed_record_standard.md). |
| Summary delivery, completed-experiment reply or single-experiment meeting brief | Additionally [plain-language delivery](references/plain_language_completion_reply.md). |
| Model-training Protocol | Additionally read the repository's `docs/training_observability_contract.md`; its telemetry, token comparison and batch-matching rules are mandatory. |

## Output And Completion

- Protocol draft: write the single candidate as `DRAFT_NOT_EXECUTABLE`, with
  grounded fields filled and `PROPOSED`/`BLOCKED` choices visible; return only
  decision-critical issues and the A–G ledger. Promotion, execution scope and
  post-start amendment follow the full contracts. Audit-only requests report
  defects and sources without rewriting or promoting the Protocol.
- Results: evidence eligibility and lineage precede interpretation. Preserve
  `NOT RUN`, `UNKNOWN`, `MISSING` and `INELIGIBLE`; never infer results from names,
  expected patterns or partial logs. If human interpretation is missing, still
  complete authorized factual records and lineage; mark that judgment `Unknown`
  or `AI_PROPOSAL` as appropriate, and scaffold only missing interpretation or
  decision fields. Do not finalize human judgment or invent a next decision.
- Summary owns the complete Purpose / Hypothesis / Analysis method / Conclusion
  account and its Chinese companion; Detailed owns full setup, deviations,
  lineage, failures, run record and artifact manifest. Finalization requires
  the chosen contracts' checks, consistent repeated fields and valid links.
- Canonical files are English unless the user chooses otherwise; companions
  preserve all rules, values and boundaries. Use `\(...\)` / `\[...\]`.

With Summary, link it first in chat, then give the verdict, smallest decisive
value, essential figure/read instruction, boundary and next-step rationale.
Label unconfirmed next steps `AI 建议`; repeat the four sections only without
Summary or for an explicitly requested standalone speaking/meeting brief.

After eligible evidence and human judgment agree, follow the result contract's
Anchor/Focus update chain. Final reports, line Stories, placement and operations
belong to their owning Skills; no closure report is created here. Implement,
run, submit, publish, sync, commit or push only within existing authorization;
do not invent extra permission gates for already authorized actions or small
local checks allowed by root rules.

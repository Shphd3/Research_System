---
name: problem-anchor-writer
description: "Use when the user asks to clarify a research question or create, revise, or audit its formal research Anchor. Do not use for experiment protocols, result records, execution, or publication."
---

# Problem Anchor Writer

Clarify or maintain one research decision in its sole canonical Anchor, never
a parallel `design.md` or judgment card. The researcher owns scientific judgment;
AI audits, proposes labeled alternatives and formalizes approved meaning.

## Inputs And Authorization

Use the requested Anchor/question, relevant parent clause, researcher judgment
from this session or active Focus, and only the evidence needed for the change.
Reuse explicit confirmations already given; do not require the researcher to
repeat them in a new form. Ask only for genuinely missing decision-bearing
judgment. `Unknown`, `BLOCKED` and `AI_PROPOSAL` remain valid; passing an AI audit
does not supply human approval. User instructions and existing scope prevail
over workflow preferences; this Skill grants no execution or publication scope.

## Choose The Requested Mode

Read each applicable contract completely; do not load unrelated modes.

| Request | Required reading |
|---|---|
| Clarify a new idea or reopen its question/prior/model | [Judgment review](references/judgment_review.md). Return the short audit before formalization. |
| Create, revise or audit a formal Anchor | [Self-containment contract](references/anchor_self_containment.md). Also read Judgment review when its scientific core is new or reopened. |
| Update current evidence/boundary after results | Self-containment contract plus [result update](references/result_update.md), and the owning result records. |
| Any Anchor fitting a parameterized model from data | Additionally read [learnable design](references/learnable_research_design.md) before judging sections 4–6. A fixed unfitted diagnostic does not trigger it. |
| Import/compare a workflow that calls its design `design.md` | Additionally read [external-method mapping](references/external_method_mapping.md); retain this repository's ownership and sections. |

Read the current Anchor before editing it. An audit is read-only unless revision
was requested; report the smallest decisive defects with their source locations.
Do not reset scientific state because an audit found a proposed correction.

## Output And Completion

- Clarification: preserved judgment, missing definition/assumption, strongest
  rival, separating metric/falsifier, and any labeled proposal or missing input.
- Formal work: update the same eight-section Anchor; one decision question,
  primary metric, main falsifier, conservative boundary and next decision.
  Links audit the locally explained meaning rather than carrying it.
- Apply the selected contracts' complete validation, including grounded claims,
  defined symbols/metrics, existing links, synchronized language companions and
  zero-net-growth for readability rewrites. Do not add top-level sections.
- Preserve English canonical / `_cn.md` companion roles unless the user chooses
  otherwise; translations cannot change model, metrics, thresholds or judgment.
  Use `\(...\)` and `\[...\]` for mathematics.

Finish the requested audit or authorized edit and verify its links/consistency.
If scientific judgment is missing, identify the exact blocked decision and
complete independent auditing; never invent approval, a result or a next action.
Protocols/results, operations and publication belong to their owning workflows.

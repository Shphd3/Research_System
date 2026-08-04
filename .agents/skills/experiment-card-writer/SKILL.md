---
name: experiment-card-writer
description: "Write a complete anchor-aligned protocol.md draft directly into the experiment folder, surface only decision-critical parts for researcher review, promote the same file after block confirmation and consistency, and update summary.md and detailed.md. Use for experiment design, protocol drafting or confirmation, or result documentation after the anchor is clear. Do not redefine the research question or operate remote jobs."
---

# Experiment Protocol And Result Writer

Use this skill after the anchor has been reviewed and approved. The anchor owns
the research design: problem definition, physical priors, hypotheses,
mathematical model, computational realization, minimal falsification tests,
current evidence, claim boundary, and next decision.

The experiment folder owns the draft-to-approved experiment design and evidence:

```text
Projects/<project>/main/experiments/A<anchor_id>/<experiment_id>/
  protocol.md
  summary.md
  detailed.md
  figures/
  tables/
```

## Core Chain

```text
anchor -> protocol.md -> summary.md -> detailed.md -> anchor update
```

Do not run or expand a nontrivial experiment before the protocol is approved.
Do not add broad sweeps, extra seeds, or new diagnostics unless they distinguish
a named rival explanation or protect the validity of the primary conclusion.

## Language And Approval Workflow

For new anchor-indexed experiments, write the English canonical file first and
conduct the decision review in Chinese unless the user asks otherwise:

```text
English protocol.md completed as DRAFT_NOT_EXECUTABLE
-> AI surfaces a concise decision-critical review extract in Chinese
-> researcher confirms or corrects one or many blocks
-> AI revises the same file and its status ledger
-> cross-block consistency audit
-> promote the same protocol.md to DESIGN_CONFIRMED_NOT_EXECUTABLE
-> explicit execution-scope approval
-> run
-> English summary.md and detailed.md as canonical result records
-> optional Chinese companions only when requested or needed for a meeting
```

Rules:

- Write the complete candidate into `protocol.md` before review and mark it
  `DRAFT_NOT_EXECUTABLE`. Keep no chat-only or second planning draft; label
  unsupported choices as assumptions or `BLOCKED`.
- Let one reply confirm or correct any subset; do not split one coherent block
  into approval microsteps.
- Require an unambiguous confirmation for each block; silence does not count.
- Promote it to `DESIGN_CONFIRMED_NOT_EXECUTABLE` only after all blocks and
  cross-block consistency pass.
- A Chinese `protocol_cn.md` companion must not change the canonical design.
- Result records stay in English by default; explain them in Chinese in chat.

## Draft-First Blockwise Audit Gate

Before writing or revising a Protocol, read
[`references/blockwise_protocol_audit.md`](references/blockwise_protocol_audit.md)
completely. Complete the single canonical `protocol.md` first as
`DRAFT_NOT_EXECUTABLE`, then surface only its decision-critical items. Keep all
candidate execution details in that file; promote them only after every block
is `CONFIRMED` and cross-block consistency is `PASS`.

If a correction changes an earlier block, mark it `REOPENED` and re-audit all
dependent blocks. Protocol promotion and execution approval are separate:
implementation, smoke, and full run each require explicit scope approval.

## Protocol Alignment Gate

A protocol is invalid unless it starts with an approval-facing snapshot. The
first page is for the user to confirm purpose and basic setup before any run:

```text
Document status:
Approval status:
Block audit status:
Cross-block consistency:
Execution scope approved:
Purpose:
Primary anchor:
Anchor decision question:
Anchor physical prior tested:
Anchor core model term tested:
Anchor falsifier:
Experiment role:
Primary metric from anchor:
Claim boundary from anchor:
Minimal setup:
Basic configuration:
Conditions to run:
Pass:
Fail:
Insufficient:
Cannot claim:
Approval decision:
```

Keep this snapshot short enough to read before approving the experiment. Put
stage profiling, algorithm details, commands, and artifact maps after the
snapshot.

The protocol may carry detail that the anchor omits, but it must still be
readable. The approval snapshot should answer in plain language:

```text
what one uncertainty this run resolves;
which anchor claim it can change;
which primary metric decides it;
what result makes the run pass, fail, or remain insufficient;
what the run cannot claim.
```

If the snapshot requires a broad condition table to understand the mechanism,
return to the anchor and split the question before writing the protocol.

Each condition, ablation, diagnostic, or visualization must appear in this
table:

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Do not include a condition because it is easy to run. Include it only if it
tests a model term, separates a named rival explanation, or protects the
validity of the primary metric.

Prefer a small protocol with one decisive comparison and explicit guards. Move
nice-to-have diagnostics, exploratory sweeps, and method variants to a later
follow-up unless they are needed to separate a named rival explanation.

The protocol must explicitly say whether it is a root-cause audit, metric
audit, operationalization / proxy test, method construction, or robustness
check. Method construction is not allowed as the first move unless the anchor
already contains a supported mechanism or metric target.

## Protocol Standard

`protocol.md` is the single draft-to-approved experiment design. Create and
complete it before review as `DRAFT_NOT_EXECUTABLE`; never treat proposed or
blocked content as an approved execution contract.

The first page is the approval snapshot; later sections are the audit layer.

```markdown
# Protocol: <experiment_id>

## 0. Approval Snapshot

Document status:
Approval status:
Block audit status:
Cross-block consistency:
Execution scope approved:
Purpose:
Primary anchor:
Anchor decision question:
Anchor physical prior tested:
Anchor core model term tested:
Anchor falsifier:
Experiment role:
Primary metric from anchor:
Claim boundary from anchor:
Minimal setup:
Basic configuration:
Conditions to run:
Pass:
Fail:
Insufficient:
Cannot claim:
Approval decision:

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## 2. Anchor Alignment

Decision question:
Physical prior tested:
Core model term tested:
Falsifier:
Claim boundary:

## 3. Tested Hypothesis

## 4. Rival Explanations

## 5. Data Construction And Provenance

## 6. Learning Task And Permitted Supervision

## 7. Model / Architecture And Frozen Variants

## 8. Training Objective And Optimization

## 9. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | |

## 10. Primary Metric

State why this metric decides the judgment and what false positives or false
negatives would cost when the costs differ.

## 11. Secondary Metrics

## 12. Known Good / Known Bad / Known Confusing Cases

## 13. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## 14. Algorithm Specification, If Nontrivial

input:
parameters:
intermediate variables:
steps:
outputs:
debug artifacts:
pass conditions:
fail conditions:
failure reasons:

## 15. Success / Failure / Insufficient Evidence

## 16. What This Cannot Claim

## 17. Block Confirmation Ledger And Review Notes
```

After writing or changing the Protocol, surface its decision-critical review
extract and stop. Do not implement or run unless the user explicitly approves
that execution scope.

## Terminology And Reader-Ready Setup Rule

Before any result table, figure, or condition label appears in `summary.md` or
`detailed.md`, the setup must define the compared objects in plain language.
This is the local minimal form of a paper-style experimental setup.

Every `summary.md`, `detailed.md`, and meeting-derived result
record must include a `Terminology / Definitions` section near the top when it
uses non-obvious terms, abbreviations, metric names, condition labels, method
names, project shorthand, or plot labels.

Use this definition shape:

```text
Term:
Plain meaning:
Concrete object or computation:
Unit / formula, if metric:
Why it matters for this decision:
What it cannot prove:
```

For `summary.md`, keep it compact but include the decision-relevant fields:

```text
research question
data or data-generating process
model / router / algorithm
loss or objective
conditions being compared, with plain-language labels
which variables changed and which were held fixed
training steps / checkpoints / seeds, when relevant
primary metric definition and unit
script or result path
known setup limitation
```

For `detailed.md`, preserve the complete setup. Any label used in a plot or
table, such as a condition name, metric abbreviation, model variant, or negative
control, must be defined before the result uses it.

## Visualized Result Alignment Gate

A figure is allowed in `summary.md` only if it supports the current claim
boundary or next decision. Before plotting or promoting a central figure, write
a plot contract. Every central figure must be able to answer:

```text
Anchor question:
Protocol question:
Metric shown:
Metric definition:
Metric unit:
Data source:
Aggregation level:
Axis / legend meaning:
Expected pattern if the hypothesis is supported:
Expected pattern if the hypothesis is weakened or incomplete:
What this figure decides:
Observed result:
Allowed claim:
What this figure does not prove:
Anchor update implication:
```

Debug figures that do not support the current conclusion must move to
`detailed.md` under `Debug / Appendix Figures`, or to a viewer appendix titled
`Debug plots not used for the current conclusion`.

`summary.md` should contain only the smallest number of figures needed to
support the primary judgment. `detailed.md` may contain the full evidence
ledger, but it must separate decision evidence, stage-level profiling
evidence, debug-only evidence, and failed or ambiguous evidence.

## Line Synthesis Boundary

This skill owns experiment protocols and result records, not line-level
synthesis. When the user asks for a current understanding report or full-line
synthesis, update the formal story through `research-mainline` after the anchor,
`summary.md`, and `detailed.md` are current. Do not create a separate closure
report.

## Summary Standard

`summary.md` is the first post-result reading path. It should be short enough
to read quickly, but it must include enough visualization-result explanation
that the central figures can be understood without chat history.

Before AI writes or revises the result judgment, the researcher first records
from memory:

```text
Question:
Direct result:
Confirmed:
Weakened or rejected:
Current mechanism and reason:
Cannot claim:
Exactly one next decision:
```

AI then verifies measurements and links, separates observation from
interpretation, and edits the prose. It must not invent the initial judgment or
strengthen it beyond the protocol and evidence. If no human draft exists,
provide this scaffold rather than a finished conclusion.

Write it conclusion-first. The first result block should use the
reader-facing shape:

```text
What we established:
What the experiment shows:
What we do next:
```

Use this shape for supported, weakened, and insufficient-evidence results. Do
not hide uncertainty; put it in the claim boundary and next decision instead of
burying the main result under process history.

Use this structure:

```markdown
# Summary: <experiment_id>

Primary anchor:
Protocol:

## Result Snapshot

Verdict:

What we established:

What the experiment shows:

What we do next:

## Purpose

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## Exact Setup

Research question:
Data construction and provenance:
Learning task and supervision:
Model / architecture:
Training objective and optimization:
Conditions:
Changed variables:
Held fixed:
Seeds / checkpoints:
Paths:
Known limitation:

## Primary Metric

Definition:
Unit:
Why it decides:
False-positive / false-negative cost, if asymmetric:

## Result

## Key Evidence

## Key Figures

### Figure: <plain title>

![<plain title>](figures/<figure>.png)

What this tests:

Anchor question:

Protocol question:

Metric shown:

Metric definition:

Metric unit:

Data source:

Aggregation level:

How to read:

Expected if supported:

Expected if weakened or incomplete:

What this figure decides:

Observed result:

Allowed claim:

What this does not prove:

Anchor update implication:

## Claim Boundary

Can claim:

Cannot claim:

## Next Decision
```

The summary must name the primary metric first and explain why it decides the
current question. Do not make a stronger claim than the protocol's success,
failure, or insufficient-evidence criteria allow.

## Detailed Standard

Before creating or updating `detailed.md`, read
[`references/detailed_record_standard.md`](references/detailed_record_standard.md)
completely. It preserves the full evidence-ledger structure, setup fields,
visualization contract, failure decomposition, and artifact map. The detailed
record must remain layered, auditable, and no stronger than `summary.md` or the
anchor.

## Rules

- Use anchor-indexed experiment folder names under an anchor-family folder:
  `main/experiments/A<anchor_id>/A<anchor_id>_<short_topic>/`.
- Every protocol, summary, and detailed record must link to the primary anchor.
- Do not create separate hypothesis purpose cards.
- Do not create separate implementation-plan files for new work.
- For trajectory, seed, checkpoint, ablation, or before/after claims, separate
  single-observation evidence, change evidence, and summary evidence.
- A negative or ambiguous result must say whether it falsifies the physical
  prior, mathematical model, operationalization/proxy, implementation, metric,
  or none of these.
- A negative or ambiguous result should be framed as the next uncertainty or
  optimization direction, not as an internal failure narrative. Do not use
  customer-facing prose to hide a weakened claim; keep the cannot-claim
  boundary explicit.
- Figures and tables must support a claim boundary or next decision.
- Markdown formulas must use `$...$` or `$$...$$`.

---
name: experiment-card-writer
description: "Create or update anchor-aligned protocol.md, summary.md, and detailed.md experiment records, including approval gates, decision metrics, evidence ledgers, and figure contracts. Use when the user asks for an experiment protocol or result documentation after the anchor is clear. Do not redefine the research question or operate remote jobs."
---

# Experiment Protocol And Result Writer

Use this skill after the anchor has been reviewed and approved. The anchor owns
the research design: problem definition, physical priors, hypotheses,
mathematical model, computational realization, minimal falsification tests,
current evidence, claim boundary, and next decision.

The experiment folder owns the approved experiment design and evidence:

```text
Projects/<project>/main/experiments/A<anchor_id>/<experiment_id>/
  protocol.md
  summary.md
  detailed.md
  figures/
  tables/
```

Legacy planning records may remain in old experiments, but new experiments
should create `protocol.md` as the only experiment design surface by default.

## Core Chain

```text
anchor -> protocol.md -> summary.md -> detailed.md -> anchor update
```

Do not run or expand a nontrivial experiment before the protocol is approved.
Do not add broad sweeps, extra seeds, or new diagnostics unless they distinguish
a named rival explanation or protect the validity of the primary conclusion.

## Language And Approval Workflow

For new anchor-indexed experiments in this repository, protocol approval uses
a Chinese-first workflow unless the user explicitly asks otherwise:

```text
Chinese protocol draft for user audit
-> user approval / correction
-> English canonical protocol.md at the experiment path
-> Chinese companion protocol_cn.md kept beside it
-> run
-> English summary.md and detailed.md as canonical result records
-> optional Chinese companion only when the user asks or when it is needed for
   meeting explanation
```

Rules:

- The Chinese draft must be short and plain enough for the user to audit the
  question, data construction, metrics, pass/fail rules, and claim boundary.
- The English `protocol.md` is the executable contract after approval.
- The Chinese `protocol_cn.md` is a companion, not a separate protocol. It must
  not introduce a different question, metric, condition, or boundary.
- If the user approves running from the Chinese protocol, translate it to the
  English canonical protocol before or during execution, then preserve the
  Chinese version.
- Result records stay in English by default because they are canonical project
  artifacts; explain the result in Chinese in chat when the user asks.

## Protocol Alignment Gate

A protocol is invalid unless it starts with an approval-facing snapshot. The
first page is for the user to confirm purpose and basic setup before any run:

```text
Approval status:
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

`protocol.md` is the approved experiment design. It replaces the older two-file
planning split.

It must align with the research-exploration `experiment_design.md` role:
the first page is the approval snapshot; later sections are the audit layer.

```markdown
# Protocol: <experiment_id>

## 0. Approval Snapshot

Approval status:
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

## 5. Data / Model / Algorithm / Objective

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | |

## 7. Primary Metric

State why this metric decides the judgment and what false positives or false
negatives would cost when the costs differ.

## 8. Secondary Metrics

## 9. Known Good / Known Bad / Known Confusing Cases

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## 11. Algorithm Specification, If Nontrivial

input:
parameters:
intermediate variables:
steps:
outputs:
debug artifacts:
pass conditions:
fail conditions:
failure reasons:

## 12. Success / Failure / Insufficient Evidence

## 13. What This Cannot Claim

## 14. Review Notes And Protocol Changes
```

Stop after writing or changing the protocol unless the user explicitly approves
running or implementing the experiment.

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
Data / model / objective:
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

---
name: experiment-card-writer
description: Use after a research anchor is clear to write protocol.md, summary.md, and detailed.md for an anchor-indexed experiment. New work uses protocol.md as the only experiment design surface, and result documents must include visualization-result explanations.
metadata:
  short-description: Write protocols and result records
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

Every `summary.md`, `detailed.md`, closure report, and meeting-derived result
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

## Closure Report Standard

Use this section only when the user explicitly asks for a closure, current
understanding report, line-level synthesis, or specified anchor-folder summary.
The target path is:

```text
Projects/<project>/main/problem_anchors/<line>/closure/
```

The canonical pair is:

```text
<line>_closure_report.md
<line>_closure_report_cn.md
```

The English file is canonical by default, and the Chinese file is a companion
with the same claims, metrics, boundaries, and next decision. If the user asks
for Chinese as the canonical file, state that explicitly in both files.

The closure report is the reader-facing synthesis of a line, not a replacement
for anchors, protocols, summaries, or detailed records. It should tell the full
advisor-style story first, then place the compact audit structure in the later
part. Link to source artifacts instead of copying their content. Use this
structure:

```markdown
# <Line> Closure Report

## Subtitle

## Abstract

## Terminology / Definitions

## 1. Motivation

## 2. What Must Be Distinguished

## 3. Clean Baseline / Impossibility Result

## 4. Mechanism Model

## 5. Propositions And Proofs

## 6. Controlled Evidence

## 7. Real Evidence / Negative Result

## 8. Reconciliation And Refined Theory

## 9. Next Experiment

## 10. Source Map And Audit Tables

## 11. Claim Boundary

## Appendix. Data / Model / Parameters / Scripts
```

Write conclusion-first. Define every technical object in plain language before
using a shorthand. Separate observation, interpretation, claim, speculation,
and boundary. For mathematical modeling, do not write only intuition: prove the
statements that follow from the model, and label unproved mechanism claims as
assumptions or empirical propositions. The appendix must list data construction
or dataset, model/router/algorithm, loss or objective, seeds, checkpoints,
important parameters, scripts, result directories, and primary metrics.

Do not add a separate `closure/README.md` unless the user explicitly asks for
an index. The closure report itself is the reading entry.

## Summary Standard

`summary.md` is the first post-result reading path. It should be short enough
to read quickly, but it must include enough visualization-result explanation
that the central figures can be understood without chat history.

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

`detailed.md` is the complete evidence ledger. It must be sufficient for a
future reader or AI to audit the run, understand the result, and locate the
artifacts without re-discovering the project.

It may be long, but it must be layered: quick judgment first, full audit after.
It must not create a stronger conclusion than `summary.md` or the anchor.

Use this structure:

```markdown
# Detailed: <experiment_id>

Primary anchor:
Protocol:
Summary:

## 0. Quick Recap

Purpose:
Hypothesis:
Experiment logic:
Conclusion:
Evidence:

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## 2. Anchor Link And Decision Point

## 3. Protocol Compliance Audit

approved conditions match actual conditions:
primary metric exists:
central figures/tables exist:
seeds/checkpoints recorded:
known good/bad/confusing cases reviewed:
success/failure/insufficient-evidence criteria applied:

## 4. Setup

Research question:
Data construction:
Train / eval / probe split:
Model / router / algorithm:
Input representation / position encoding:
Loss / objective:
Optimizer or update rule:
Training steps / tokens / batch size:
Checkpoints:
Seeds:
Conditions and plain-language labels:
Changed variables:
Held fixed:
Script paths:
Result paths:
Known setup limitations:

## 5. Metrics And Decision Rules

## 6. Main Results

Separate:

- decision evidence;
- stage-level profiling evidence;
- debug-only evidence;
- failed or ambiguous evidence.

## 7. Visualization Results

For each central figure or viewer:

### <plain title>

![<plain title>](figures/<figure>.png)

Purpose:
Setup:
Metric definition:
Metric unit:
How to read:
Expected if supported:
Expected if weakened or incomplete:
Observed result:
Take-home:
Remaining uncertainty:
What this figure does not prove:
Anchor update implication:

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| | | | | |

Falsified physical prior:
Falsified mathematical model:
Falsified operationalization / proxy:
Falsified implementation:
Falsified metric:
Remaining rival explanations:

## 9. Full Experiment Record

## 10. Interpretation

## 11. Claim Boundary

## 12. Next Decision

## 13. Links And Artifact Map

anchor:
protocol:
summary:
code workspace:
runner:
config:
key code files:
data / manifest:
result dir:
figure dir:
key tables:
logs / checkpoints:
repro command:
job id:
```

Every central figure must have purpose, setup, how-to-read, observed result,
take-home, and remaining uncertainty. A figure that cannot be explained should
move to an appendix/debug area or be omitted from the main result path.

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

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

## 1. Anchor Alignment

Decision question:
Physical prior tested:
Core model term tested:
Falsifier:
Claim boundary:

## 2. Tested Hypothesis

## 3. Rival Explanations

## 4. Data / Model / Algorithm / Objective

## 5. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | |

## 6. Primary Metric

State why this metric decides the judgment and what false positives or false
negatives would cost when the costs differ.

## 7. Secondary Metrics

## 8. Known Good / Known Bad / Known Confusing Cases

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## 10. Algorithm Specification, If Nontrivial

input:
parameters:
intermediate variables:
steps:
outputs:
debug artifacts:
pass conditions:
fail conditions:
failure reasons:

## 11. Success / Failure / Insufficient Evidence

## 12. What This Cannot Claim

## 13. Review Notes And Protocol Changes
```

Stop after writing or changing the protocol unless the user explicitly approves
running or implementing the experiment.

## Visualized Result Alignment Gate

A figure is allowed in `summary.md` only if it supports the current claim
boundary or next decision. Every central figure must include this alignment
block:

```text
Anchor question:
Protocol question:
Metric shown:
Metric definition:
Data source:
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

## Summary Standard

`summary.md` is the first post-result reading path. It should be short enough
to read quickly, but it must include enough visualization-result explanation
that the central figures can be understood without chat history.

Use this structure:

```markdown
# Summary: <experiment_id>

Primary anchor:
Protocol:

## Purpose

## Exact Setup

## Primary Metric

## Result

## Key Figures

### Figure: <plain title>

![<plain title>](figures/<figure>.png)

What this tests:

Anchor question:

Protocol question:

Metric shown:

Metric definition:

Data source:

How to read:

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

## 1. Anchor Link And Decision Point

## 2. Protocol Compliance Audit

approved conditions match actual conditions:
primary metric exists:
central figures/tables exist:
seeds/checkpoints recorded:
known good/bad/confusing cases reviewed:
success/failure/insufficient-evidence criteria applied:

## 3. Setup

## 4. Metrics And Decision Rules

## 5. Main Results

Separate:

- decision evidence;
- stage-level profiling evidence;
- debug-only evidence;
- failed or ambiguous evidence.

## 6. Visualization Results

For each central figure or viewer:

### <plain title>

![<plain title>](figures/<figure>.png)

Purpose:
Setup:
How to read:
Observed result:
Take-home:
Remaining uncertainty:
What this figure does not prove:
Anchor update implication:

## 7. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| | | | | |

Falsified physical prior:
Falsified mathematical model:
Falsified operationalization / proxy:
Falsified implementation:
Falsified metric:
Remaining rival explanations:

## 8. Full Experiment Record

## 9. Interpretation

## 10. Claim Boundary

## 11. Next Decision

## 12. Links And Artifact Map

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
- Figures and tables must support a claim boundary or next decision.
- Markdown formulas must use `$...$` or `$$...$$`.

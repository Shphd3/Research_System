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
Projects/<project>/main/experiments/<experiment_id>/
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

## Protocol Standard

`protocol.md` is the approved experiment design. It replaces the older two-file
planning split.

It must align with the research-exploration `experiment_design.md` role:

```markdown
# Protocol: <experiment_id>

Primary anchor:
Anchor decision question:
Experiment role:

## 1. Decision Question

## 2. Tested Hypothesis

## 3. Rival Explanations

## 4. Data / Model / Algorithm / Objective

## 5. Conditions, Seeds, And Checkpoints

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

## 13. Approval Status
```

Stop after writing or changing the protocol unless the user explicitly approves
running or implementing the experiment.

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

How to read:

Observed result:

Take-home:

What this does not prove:

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

- Use anchor-indexed experiment folder names: `A<anchor_id>_<short_topic>/`.
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

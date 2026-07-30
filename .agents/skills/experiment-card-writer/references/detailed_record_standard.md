# Detailed Result Record Standard

## Contents

- [Purpose](#purpose)
- [Required structure](#required-structure)
- [Figure and evidence boundary](#figure-and-evidence-boundary)

## Purpose

`detailed.md` is the complete evidence ledger. It must be sufficient for a
future reader or AI to audit the run, understand the result, and locate the
artifacts without re-discovering the project.

It may be long, but it must be layered: quick judgment first, full audit after.
It must not create a stronger conclusion than `summary.md` or the anchor.

## Required structure

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

## Figure and evidence boundary

Every central figure must have purpose, setup, how-to-read, observed result,
take-home, and remaining uncertainty. A figure that cannot be explained should
move to an appendix/debug area or be omitted from the main result path.

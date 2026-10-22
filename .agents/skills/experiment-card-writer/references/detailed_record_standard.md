# Detailed Result Record Standard

Apply `result_evidence_lineage.md` before using this structure.

## Contents

- [Purpose](#purpose)
- [Content coverage and reader organization](#content-coverage-and-reader-organization)
- [Evidence ownership](#evidence-ownership)
- [Figure boundary](#figure-boundary)

## Purpose

`detailed.md` and its explicitly linked appendices own the complete evidence ledger. A future reader or AI must
be able to verify execution against the frozen Protocol, trace every
decision-bearing result, understand failures, and locate artifacts without
re-discovering the project.

It may be long, but it must be layered: the question, comparison, observed result
and eligibility first, full audit afterward. Scientific judgment remains with
the researcher. Explain how the actual experiment works before listing its
provenance fields: input construction, changed/fixed quantities, the purpose
of each control, measurement steps and how to read the result. Use a worked
real example where it helps. A list of parameters and paths is not that explanation. It must not create a stronger conclusion than `summary.md` or
the Anchor.

## Content Coverage And Reader Organization

The checklist below records content ownership; it is not a mandatory fifteen-
section reading order. Combine and order material by what a new reader needs
to understand first. Put full tables, logs and technical audits in linked
appendices under this record, without dropping requested conditions. Do not
create empty sections merely to reproduce the checklist.

```markdown
# Detailed: <experiment_id>

Primary Anchor:
Frozen Protocol and registered revision:
Summary:
Result eligibility:

## 0. Quick Recap

Purpose:
Hypothesis:
Experiment logic:
Direct result:
Eligibility:
Verdict:
Claim boundary:

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## 2. Anchor Link And Decision Point

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Frozen Protocol revision:
Execution scope approved:
Amendments:
Retries and exclusions:
Missing conditions or artifacts:
Post-hoc analyses:

## 4. Actual Setup

Research question:
Data construction and provenance:
Train / development / confirmation split:
Learning task and permitted supervision:
Model / architecture / algorithm:
Input representation / position encoding:
Training objective and constraints:
Optimizer or update rule:
Training steps / tokens / batch size:
Checkpoints:
Seeds:
Conditions and plain-language labels:
Changed variables:
Held fixed:
Code / config / data identities:
Script and result paths:
Known setup limitations:

## 5. Metrics And Registered Decision Rules

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | |

## 7. Main Results

Separate:

- eligible decision evidence;
- bounded evidence;
- stage-level profiling evidence;
- debug-only evidence;
- failed or ambiguous evidence;
- ineligible, missing, and not-run evidence.

## 8. Visualization Results, When Decision-Relevant

### <plain title>

![<plain title>](figures/<figure>.png)

Purpose:
Setup:
Metric definition and unit:
Raw source and lineage row:
Aggregation and uncertainty:
How to read:
Expected under registered outcomes:
Observed result:
Take-home:
Remaining uncertainty:
What this figure does not prove:
Anchor update implication:

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out | What remains live |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Falsified physical prior:
Falsified mathematical model:
Falsified operationalization / proxy:
Falsified implementation:
Falsified metric:
Remaining rival explanations:

## 10. Full Experiment Record

A round retains its registered experimental identity and may span days.
Record its six content fields without converting the main explanation into a
day-by-day execution diary:

1. Question or hypothesis tested.
2. Setup: the exact model or baseline version, and the controlled variables.
3. Training data.
4. Testing or confirmation data, and its split.
5. Result with linked artifacts and metrics, or an explicit `NOT RUN`.
6. Insight, claim-boundary update, and next decision.

A round that records items 1-4 and `NOT RUN` is a **complete** round. A completed
round carries all six. Never fabricate a result; `NOT RUN` is a valid and
complete state. Do not duplicate the full round history into `summary.md` or
into the Focus.

## 11. Interpretation

## 12. Claim Boundary

Can claim:
Cannot claim:

## 13. Next Decision

Decision:
Completion criterion:
Resume action:

## 14. Artifact Manifest

| Artifact | Purpose | Producer / revision | Source inputs | Hash or identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |

## 15. Links

anchor:
protocol:
summary:
code workspace:
runner:
config:
data / manifest:
result dir:
figure dir:
logs / checkpoints:
repro command:
job ids:
```

## Evidence Ownership

- Compare the frozen Protocol with actual execution before interpreting any
  value.
- Record every deviation, amendment, retry, exclusion, missing condition, and
  post-hoc analysis, even when it does not change eligibility.
- Separate raw observations, derived statistics, interpretations, and claims.
- Do not combine eligible and ineligible evidence in one aggregate.
- Do not treat layers, tokens, documents, checkpoints, or arms as independent
  experimental replicates unless the design establishes that independence.
- Make every decision-bearing value trace to a raw artifact, computation,
  aggregation, registered criterion, and bounded claim.
- Keep complete setup, all conditions, run history, and artifact manifests out
  of `summary.md`; Detailed owns them.

## Figure Boundary

Every central figure must have a source table or lineage row, purpose, setup,
metric and unit, aggregation, how-to-read statement, observed result,
take-home, and remaining uncertainty. Move an unexplained or debug-only figure
to a labeled appendix or omit it. Do not create a visualization section when
the decision uses nonvisual evidence.

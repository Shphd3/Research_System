---
name: prism-report
description: Use when the user asks to write, update, consolidate, or prepare a PRISM project report or group-meeting-ready PRISM document from research notes, daily reports, experiments, or mainline checkpoints.
metadata:
  short-description: Write PRISM research reports
---

# PRISM Report

Use this skill to turn research progress into a report that can be shown in meetings. A PRISM report is not a daily log. It is a mainline-facing document that explains the problem, evidence, interpretation, and next decision.

## Inputs

Read, in this order when available:

1. `CURRENT.md`
2. relevant `daily_report.md` or raw daily material
3. experiment cards, result summaries, figures, or logs named by the user
4. previous PRISM/report text if the user is updating an existing report

## Fixed Structure

Use this structure by default:

```markdown
# PRISM Report - [topic/date]

## 1. Report Purpose

State what this report is trying to decide. Do not start with experiment details.

## 2. Research Background

Explain the larger mainline in plain language:
- the north-star goal
- the current hypothesis
- why this stage matters now

## 3. Current Hypothesis

State the hypothesis being tested. If the hypothesis has been weakened or revised, say that directly.

## 4. Modeling / Mechanism

Define the key objects, variables, architecture components, or metrics needed to understand the report.
Only include math that is needed for the argument.

## 5. Empirical Evidence

Organize evidence by claim, not by raw run order.
For each evidence block, write:
- experiment or observation
- what it supports
- what it weakens
- what alternative explanation remains

## 6. Current Interpretation

State the best current explanation. Separate stable conclusions from tentative signals.

## 7. Claims To Downgrade

List claims that should not be made in the meeting or report.

## 8. Next Iteration

State the next smallest experiment, audit, or reading step that can update the mainline.

## 9. Meeting Version

Write a 30 second version and, if useful, a 1 minute version.
```

## Writing Rules

- Write in clear Chinese unless the user asks for English.
- Do not use English labels to hide unclear reasoning.
- Do not write a PRISM report as a chronology.
- Do not overclaim from one experiment.
- Every major section must connect back to the current mainline.
- If evidence is weak, say it is weak and explain what would make it decisive.

## Meeting Defense

When preparing for a group meeting, add:

```markdown
## 10. Likely Questions

### Question 1

Short answer:

Evidence:

How to redirect back to the mainline:
```

Use at most 2-3 likely questions unless the user asks for more.

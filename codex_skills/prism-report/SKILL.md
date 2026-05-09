---
name: prism-report
description: Use when the user asks to write, update, consolidate, or prepare a PRISM project report or group-meeting-ready PRISM document from research notes, daily reports, experiments, or mainline checkpoints.
metadata:
  short-description: Write PRISM research reports
---

# PRISM Report

Use this skill to turn research progress into a report that can be shown in meetings. A PRISM report is not a daily log. It is a mainline-facing document that explains the problem, evidence, interpretation, and next decision.

Default output location for new meeting PRISM work:

```text
daily_research_reports/MMDD/meeting/prism/
```

Do not create new PRISM materials under a root-level `meetings/` folder.

## Inputs

Read, in this order when available:

1. `CURRENT.md`
2. relevant `daily_report.md` or raw daily material
3. experiment cards, result summaries, figures, or logs named by the user
4. previous PRISM/report text if the user is updating an existing report

## Output Format

If the user asks for a PRISM project document, prefer a self-contained LaTeX file in the target `daily_research_reports/MMDD/meeting/prism/` folder, following the existing project style:

- `\documentclass[11pt]{article}`
- `geometry`, `amsmath`, `graphicx`, `hyperref`, `booktabs`, `float`, `caption`, `adjustbox`, `enumitem`
- a `\safeincludegraphics` helper
- compact tables with `\tablesize`
- section order matching the previous PRISM report

If figures are used, copy them into `prism/figures/` and reference them with relative paths such as `figures/name.png`.

## Fixed Structure

Use this structure by default for Markdown drafts:

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

## LaTeX PRISM Structure

For a meeting-ready `.tex` PRISM report, use this section order unless the user provides a newer project template:

```latex
\section{Recent Updates}
\section{Background and Theoretical Critique}
\section{Hypotheses and Mathematical Modeling}
\section{Empirical Study}
\section{Next Iteration}
\subsection{Short oral summary}
```

Inside `Empirical Study`, organize evidence by claim, not chronology. Each evidence subsection should include:

- `\textbf{Hypothesis.}`
- `\textbf{Experiment sketch.}`
- `\textbf{Result.}`
- `\textbf{Interpretation.}`

## Audience Rule

Assume the advisor knows the high-level hypothesis but not the detailed implementation. Before showing metrics, explain in plain language:

- what object is being tested;
- why this controlled experiment is needed;
- what the model is supposed to recover;
- what the reported metric means.

Do not start with tables or architecture names before defining the scientific question.

## Claim Boundary Rule

Every PRISM report must state:

- what the evidence supports;
- what it weakens;
- what it cannot prove;
- the safest current claim.

For synthetic experiments, explicitly separate:

- feature-level specialization;
- function-level specialization;
- routing-level specialization;
- transfer to real hidden states.

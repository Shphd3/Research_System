---
name: handoff-report-writer
description: Use only when evidence must be packaged for a meeting, collaborator, or web-side handoff after the anchor, experiment summary, and detailed result are already updated.
metadata:
  short-description: Write optional research handoff reports
---

# Handoff Report Writer

Use this skill after evidence exists and after the core research documents are
updated. A handoff report is an optional external package. It is not the main
research document and it is not a second closure.

The source of truth remains:

```text
anchor.md = current-state hypothesis, evidence, refined hypothesis, boundary, next decision
summary.md = first post-result reading path
detailed.md = full iteration ledger and artifact map
```

## Core Rule

First apply `research-progress-core`. The report must state:

```text
what was tested
where the evidence is
what passed
what failed
why it failed, if known
what the next concrete test or decision is
```

Do not write a handoff report from chat history alone. Do not use it to replace
anchor backfill, `summary.md`, or `detailed.md`.

## When To Use

Use this only when at least one is true:

- a collaborator or advisor needs a self-contained report;
- a web-side or GitHub-side reader should understand the result without entering
  the project repository;
- a meeting requires an oral report card and artifact map;
- multiple result documents need to be packaged into one handoff.

Do not create a handoff report for every ordinary experiment by default.

## Required Inputs

Read in order:

1. `PROJECTS.md`;
2. project `graph.yaml`, only for navigation;
3. relevant anchor;
4. experiment `summary.md`;
5. experiment `detailed.md`;
6. key figures, tables, and artifact paths needed for reproduction.

## Location

Branch-local meeting or collaborator handoff:

```text
Projects/<project>/<worker>/sync/MMDD_topic/report.md
```

Project-level handoff only when the result is stable enough to share as project
context:

```text
Projects/<project>/sync/MMDD_topic/report.md
```

Root sync handoff for web-side readers should point to the root anchor copy:

```text
sync/<sync_id>/anchors/<category>/<anchor_id>.md
```

## Required Shape

```markdown
# Handoff Report: <topic>

Anchor:
Summary:
Detailed:

## 0. Oral Report Card

目的：

物理建模 / 假设：

最小实验：

结论：

证据：

结论边界：

下一步：

## 1. What Was Tested

## 2. Evidence Location

## 3. What Passed

## 4. What Failed Or Stayed Ambiguous

## 5. Interpretation

## 6. Claim Boundary

## 7. Next Decision

## 8. Key Figures

![<figure title>](figures/<figure>.png)

Supports:

## 9. Artifact / Repro Map

code workspace:
runner:
config:
key code files:
data / manifest:
result dir:
figure dir:
key files:
checkpoints / logs:
repro command:
job id:
```

## Writing Standard

This is a decision report, not a timeline. Keep it shorter than `detailed.md`.
It should package the conclusion and evidence for transfer, not re-run the full
reasoning.

Every important metric must state what question it answers, what failure mode
it catches, and what it cannot prove. Every central figure must have a nearby
one-sentence interpretation.

## Reference Delegation

If the handoff needs more than packaging, do not expand this skill. Load the
relevant `research-progress-core/references/` file instead:

- `profiling_and_evidence.md` when deciding which evidence is sufficient;
- `failure_decomposition.md` when the handoff must explain a bottleneck;
- `goal_audit.md` when the handoff explains a changed metric or goal.

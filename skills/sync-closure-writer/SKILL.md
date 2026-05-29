---
name: sync-closure-writer
description: Use when writing or updating an anchor-based sync closure after experiment evidence exists, especially for meeting/collaborator reports that must summarize result, interpretation, claim boundary, next decision, figures, and artifact maps.
metadata:
  short-description: Write anchor-based sync closures
---

# Sync Closure Writer

Use this after evidence exists. The sync closure is the branch-local or
collaborator-facing report built from an anchor and an experiment `summary.md`.
The experiment `summary.md` now carries the old hypothesis-closure role inside
the experiment folder; sync closure packages that conclusion for meeting or
handoff use.

Default language is Chinese. Keep English for metric names, code identifiers,
paths, and quoted technical terms.

## Required Inputs

Read in order:

1. `PROJECTS.md`;
2. project `graph.yaml`;
3. relevant anchor, usually under a project mainline's `problem_anchors/`
   directory, such as `main/problem_anchors/`;
4. experiment `summary.md`, `detailed.md`, figures, or run tables needed to
   audit the result;
5. code/config/artifact paths for reproduction.

Do not write a sync closure from chat history alone.

## Location

Branch-local meeting or collaborator sync:

```text
Projects/<project>/<worker>/sync/MMDD_topic/report.md
```

Project-level sync only when the result is stable enough to share as project
context:

```text
Projects/<project>/sync/MMDD_topic/report.md
```

Before writing the sync closure, make sure the result has already been
integrated into:

```text
experiment summary.md as the closure-level result document
experiment detailed.md as the complete experiment record
source anchor evidence / claim boundary / next decision
root sync anchor copy
graph.yaml, if the route changed
```

The sync closure is the meeting or collaborator-facing report built from those
updated sources.

## Required Shape

```markdown
# Sync Closure: <topic>

Anchor:
Story:

## 0. Oral Report Card - Fill Before Meeting

目的：

假设 / 问题：

结论：

证据：

## 1. Purpose

## 2. Anchor Question And Physical Prior

## 3. Mathematical / Computational Setup

## 4. Experiment Setup

## 5. Conclusion

## 6. Evidence

## 6.1 Key Figures

![<figure title>](figures/<figure>.png)

Supports:

## 7. Observation

## 8. Interpretation

## 9. Claim Boundary

## 10. Next Decision

## 11. Links

anchor:
summary:
detailed:
source anchor copy:

## 12. Artifact / Repro Map
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

Keep section 0 blank unless the user supplies or confirms wording.

## Writing Standard

This is a decision report, not a chronology.

Separate:

- **Observation:** what was directly measured;
- **Interpretation:** what the observation suggests;
- **Decision:** what should happen next;
- **Boundary:** what cannot be claimed.

Every important metric must state:

- what question it answers;
- what failure mode it catches;
- what it cannot prove;
- which metric dominates the decision when metrics disagree.

Every central figure must be copied into the sync folder's local `figures/`
directory when possible, embedded or linked near the claim it supports, and
given a one-sentence interpretation. A sync closure without important available
figures is incomplete.

Do not use opaque English phrases as story labels. Write the story in one clear
sentence, for example:

```text
This experiment tests whether the measured effect is caused by the proposed
mechanism, rather than by a simpler shortcut or confound in the setup.
```

## Anchor Backfill

Anchor backfill happens before the sync closure. If the result changes the
research state, update:

- current evidence;
- safest claim;
- weakened or strengthened physical prior;
- mathematical object or metric rule;
- computational realization;
- next smallest decision;
- links to `summary.md`, `detailed.md`, and the sync report when available.

Do not duplicate long logs in the anchor. Link the sync closure and curated
result files.

## Relationship To Experiment Reports

- `summary.md`: closure-level result, first reading path, self-contained
  observation / interpretation / limitation / claim update / next decision.
- `detailed.md`: complete experiment record, including setup, seeds, commands,
  job ids, artifact map, curated tables, important figures, failed or partial
  runs when relevant, and evidence walkthrough.
- sync `report.md`: meeting or collaborator-facing packaging of the same
  conclusion. It should not replace `summary.md` or `detailed.md`.

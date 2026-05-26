---
name: sync-closure-writer
description: Use when writing or updating an anchor-based sync closure after experiment evidence exists, especially for meeting/collaborator reports that must summarize result, interpretation, claim boundary, next decision, figures, and artifact maps.
metadata:
  short-description: Write anchor-based sync closures
---

# Sync Closure Writer

Use this after evidence exists. The sync closure is the reporting and
collaboration document built from an anchor. It replaces hypothesis closure as
the default post-result artifact.

Default language is Chinese. Keep English for metric names, code identifiers,
paths, and quoted technical terms.

## Required Inputs

Read in order:

1. `PROJECTS.md`;
2. project `graph.yaml`;
3. relevant anchor, usually under `main_specialization/problem_anchors/` or
   `main/problem_anchors/`;
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

If the result changes the research state, update the source anchor and
`graph.yaml` after writing the sync closure.

## Required Shape

```markdown
# Sync Closure: <topic>

Anchor:

## 0. Oral Report Card - Fill Before Meeting

目的：

假设 / 问题：

结论：

证据：

## 1. Purpose

## 2. Anchor Question And Physical Prior

## 3. Mathematical / Computational Setup

## 4. Experiment Setup

## 5. Observation

## 6. Interpretation

## 7. Claim Boundary

## 8. Next Decision

## 9. Figures / Tables

## 10. Artifact / Repro Map
code workspace:
runner:
config:
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

Every central figure must be embedded or linked near the claim it supports, with
a one-sentence interpretation.

## Anchor Backfill

After the sync closure is written, update the anchor if the result changes:

- current evidence;
- safest claim;
- weakened or strengthened physical prior;
- mathematical object or metric rule;
- computational realization;
- next smallest decision.

Do not duplicate long logs in the anchor. Link the sync closure and curated
result files.

---
name: research-mainline
description: Use when organizing or updating a research project's mainline state: graph, roadmap, anchors, experiment result records, root anchor copies, optional handoff reports, archive state, and project status.
metadata:
  short-description: Maintain compact research mainline
---

# Research Mainline

Use this skill to keep the active research state easy to inspect and act on.
It does not define the research method and does not write detailed templates.

First apply `research-progress-core`. Then use this skill only to decide where
the current state lives, whether the mainline changed, and which surfaces need
to be updated.

## Mainline Goal

The mainline should make these items obvious:

- current research question;
- active anchor;
- strongest current evidence;
- refined hypothesis or current uncertainty;
- claim boundary;
- next decision;
- links to the result records that justify the state.

## Required Surfaces

```text
Projects/<project>/
  graph.yaml
  main/
    roadmap.md
    problem_anchors/
      <anchor_id>.md
    experiments/
      <experiment_id>/
        execution_plan.md
        summary.md
        detailed.md
        figures/
```

Optional surfaces:

```text
Projects/<project>/<worker>/sync/MMDD_topic/report.md
Projects/<project>/sync/MMDD_topic/report.md
Projects/<project>/<worker>/docs/
sync/<sync_id>/anchors/<category>/<anchor_id>.md
daily_research_reports/MMDD/
```

## Naming Rules

Use names to show research level. Do not use one naming scheme for everything.

### Anchor Names

Anchor names should describe a stable research question or hypothesis line, not
a day or one run.

Use:

```text
<mechanism_or_question>_anchor.md
<factor>_<effect>_anchor.md
<problem_axis>_<decision>_anchor.md
```

Examples:

```text
slot_context_dominance_router_specialization_anchor.md
route_function_binding_specialization_anchor.md
frequency_induced_feature_anisotropy_anchor.md
```

Do not create a new anchor for each daily iteration, seed, smoke run, or failed
operationalization. Update the same anchor unless the parent question or
hypothesis line changes.

### Experiment Names

Experiment folders may include date or iteration labels because they are
records of tests:

```text
HMMDD_short_topic/
HMMDDa_short_topic_smoke/
HMMDDb_short_topic_full/
```

Use suffixes only when they distinguish real iteration roles:

```text
smoke
full
followup
ablation
trajectory
seed_sweep
```

### Daily Reports

Daily report folders are date-first because they record work for a day:

```text
daily_research_reports/MMDD/<topic>/
```

Daily reports do not replace anchors or experiment records. If the day changes
the hypothesis, evidence, boundary, or next decision, update the anchor too.

### Handoff Reports

Handoff reports are date/topic packages for external readers:

```text
Projects/<project>/<worker>/sync/MMDD_topic/report.md
Projects/<project>/sync/MMDD_topic/report.md
```

Use them only when a meeting, collaborator, GitHub, or web-side reader needs a
self-contained package.

## Core Artifact Chain

Default chain:

```text
anchor -> execution_plan.md -> summary.md -> detailed.md
-> anchor update -> root anchor copy -> optional handoff report
```

`summary.md` and `detailed.md` are required after an experiment result exists.
The optional handoff report is only for meeting, collaborator, or web-side
transfer.

## File Roles

### `graph.yaml`

Navigation layer only. It points to questions, anchors, evidence, methods,
outputs, and tasks. It does not replace Markdown reasoning.

Before editing an existing graph, use `research-graph-sop` and get the user's
confirmation of the research-state change unless the user explicitly requested
that exact graph edit.

### `roadmap.md`

Compact route and gate logic. Use it for the order of anchors, stop rules, and
high-level project route. Do not put detailed evidence here.

### Anchor

Current-state document. It should contain the current hypothesis, operational
definitions, physical priors, mathematical model, minimal test, current
evidence, refined hypothesis, claim boundary, and next decision.

Anchor body is English. The top `Report Summary（中文，汇报用）` should be short:

```text
目的 / 物理建模或假设 / 最小实验 / 当前结论 / 结论边界 / 下一步
```

Use `problem-anchor-writer` for anchor content rules.

### Experiment Folder

Execution and evidence layer. Each active experiment should map to one primary
anchor and contain:

```text
execution_plan.md
summary.md
detailed.md
figures/ when important figures exist
tables/ when curated tables exist
```

Use `experiment-card-writer` for execution plan, summary, detailed record,
figures, tables, failure analysis, and artifact-map details.

### Root Anchor Copy

Active anchors must be mirrored to root `sync/` when a root category is defined:

```text
sync/<sync_id>/anchors/<category>/<anchor_id>.md
```

The project-local anchor is the source of truth. After updating it, copy it to
the root sync path and verify the files are identical.

### Handoff Report

Optional external package. Use it only when a meeting, collaborator, GitHub, or
web-side reader needs a self-contained report.

Use `handoff-report-writer`. Do not create a handoff report merely because an
experiment finished.

### Daily / Meeting Reports

Daily and meeting reports are derived from updated anchors, `summary.md`, and
`detailed.md`. They should make the closure clear:

```text
question / hypothesis / minimal test / conclusion / evidence / boundary / next decision
```

Do not maintain a separate meeting sub-workflow unless the user explicitly asks.

## Mainline Update Test

A result or discussion updates the mainline only if it changes at least one of:

- active route or next project decision;
- anchor evidence;
- refined hypothesis;
- claim boundary;
- next decision;
- graph navigation after user-confirmed research judgment.

If none changed, write:

```text
No mainline update today.
```

## Archive Rule

Keep active `experiments/` focused on the proposition currently being verified.
Move older, superseded, weakly related, or support-only experiments into
`experiments/archive/` with a short index:

```text
archived folder
why archived
when to consult again
```

Archive evidence instead of deleting it unless the user explicitly asks to
delete it.

## Rules

- Keep mainline thin; put reasoning in anchors and result records.
- Do not promote raw logs, checkpoints, datasets, full run directories, or
  unfiltered generated outputs into mainline paths.
- Do not leave completed anchors with stale evidence, claim boundary, next
  decision, or result links.
- When central figures exist, curated copies should appear in the experiment
  `figures/` folder and be embedded in `summary.md` and `detailed.md`.
- Markdown formulas must use `$...$` or `$$...$$`.

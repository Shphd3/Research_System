---
name: research-mainline
description: Use when organizing or updating a research project's mainline state: graph, roadmap, anchors, experiment result records, explicitly requested root anchor copies, external collaborator repo sync packages, handoff reports, archive state, and project status.
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

Explicit optional surfaces:

```text
Projects/<project>/<worker>/sync/MMDD_topic/report.md
Projects/<project>/sync/MMDD_topic/report.md
Projects/<project>/<worker>/docs/
sync/<sync_id>/anchors/<category>/<anchor_id>.md
daily_research_reports/MMDD/
<external_collaborator_repo>/<agreed_path>/MMDD_topic/
```

Do not update optional sync, external collaborator sync, handoff, graph, commit,
or push surfaces unless the user explicitly asks for that action.

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
01_slot_context_dominance_router_specialization_anchor.md
02_route_function_binding_specialization_anchor.md
03_frequency_induced_feature_anisotropy_anchor.md
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
daily_research_reports/MMDD/<topic>/handoff_report.md
daily_research_reports/MMDD/<topic>/<anchor_id>.md
Projects/<project>/<worker>/sync/MMDD_topic/report.md
Projects/<project>/<worker>/sync/MMDD_topic/<anchor_id>.md
Projects/<project>/sync/MMDD_topic/report.md
Projects/<project>/sync/MMDD_topic/<anchor_id>.md
```

Use them only when the user explicitly asks for a handoff or sync package.
Default handoff output goes in the daily folder and includes a copy of the most
important anchor using its subject-bearing basename, not generic `anchor.md`.
Project sync folders are used only when project/collaborator sync is explicitly
requested.

### External Collaborator Repo Sync Names

External collaborator repo sync means copying a curated research package into a
separate collaborator repository, for example an advisor/senior student's
GitHub repo. It is not root sync and not project-local sync.

Use the collaborator repo's agreed folder convention when one exists. If none
exists, use a date/topic folder:

```text
<external_collaborator_repo>/<agreed_research_sync_path>/MMDD_topic/
  <anchor_id>.md
  summary.md
  detailed.md
  05_report_card.md    # optional, for quick reading
  figures/             # only if referenced by synced docs
  tables/              # only if referenced by synced docs
```

Use subject-bearing filenames. Do not use generic `anchor.md` unless the
external repo already requires it.

## Core Artifact Chain

Default chain:

```text
anchor -> execution_plan.md -> summary.md -> detailed.md
-> anchor update
```

`summary.md` and `detailed.md` are required after an experiment result exists.
Root sync copies, handoff packages, graph edits, commits, and pushes are explicit
follow-up actions only.

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

Current-state document. It should contain the current physical priors,
falsifiable hypothesis, operational definitions, mathematical model, minimal
test, current evidence, refined hypothesis, claim boundary, and next decision.

Anchor body is English. The top `Report Summary（中文，汇报用）` should be short:

```text
目的 / 物理建模或假设 / 最小实验 / 当前结论 / 结论边界 / 下一步
```

This front summary is not `05_report_card.md`. When a result needs
advisor-facing or sync presentation, generate `05_report_card.md` in the daily
or sync package from `templates/reporting/report_card_template.md`.

Use `problem-anchor-writer` for anchor content rules.

### Experiment Folder

Execution and evidence layer. Each active experiment should map to one primary
anchor and contain:

```text
execution_plan.md
summary.md
detailed.md
05_report_card.md, when advisor-facing in daily or sync packages
figures/ when important figures exist
tables/ when curated tables exist
```

Use `experiment-card-writer` for execution plan, summary, detailed record,
figures, tables, failure analysis, and artifact-map details.

### Root Anchor Copy

Root sync is an explicit external-reading surface. Do not update it just
because an anchor changed. When the user asks for root sync, mirror the active
anchor to:

```text
sync/<sync_id>/anchors/<category>/<anchor_id>.md
```

The project-local anchor is the source of truth. When root sync is requested,
copy the anchor to the root sync path and verify the files are identical.

### External Collaborator Repo Sync

Use this only when the user explicitly asks to sync material to a collaborator,
senior student's repo, advisor repo, or another external GitHub repository.

This sync should be a curated package, not a repository mirror. Include only
the smallest files needed for the collaborator to understand the research state:

```text
required:
- copied current anchor with subject-bearing filename
- summary.md
- detailed.md

optional:
- 05_report_card.md, when the collaborator needs a fast advisor-facing summary
- figures/ or tables/, only when referenced by anchor, summary, detailed, or
  report_card
- README.md or index, only when the target repo requires one
- execution_plan.md, only when syncing a proposed run before execution
```

Do not sync:

```text
- raw logs
- checkpoints
- datasets
- full run directories
- unfiltered generated figures/tables
- caches or temporary files
- private daily notes or unconfirmed speculation
- unrelated anchors or old archived evidence
- experiment code changes unless the user explicitly requests code sync
```

Before copying into the external repo:

1. Ask for or identify the target repo path and agreed destination folder.
2. Check the target repo's `git status --short --branch`.
3. Do not overwrite dirty collaborator files unless the user explicitly
   approves that exact overwrite.
4. Convert absolute local links into relative links.
5. Copy only the curated package.
6. Verify every linked figure/table exists inside the copied package.
7. Show the inclusion/exclusion list before commit or push.

Commit and push the external repo only when the user explicitly asks. A request
to "sync files" means copy/update the curated package; it does not imply push.

### Handoff Package

Optional external package. Use it only when the user explicitly asks for a
meeting, collaborator, GitHub, or web-side handoff.

Use `handoff-report-writer`. Do not create a new handoff document merely because
an experiment finished. A handoff package should copy existing anchor,
`summary.md`, `detailed.md`, optional report card, and referenced figures/tables,
then add only a short README or index.

### Daily / Meeting Reports

Daily and meeting reports are derived from updated anchors, `summary.md`, and
`detailed.md`. They should make the closure clear:

```text
question / hypothesis / minimal test / conclusion / evidence / boundary / next decision
```

Daily / meeting report cards should reuse
`templates/reporting/report_card_template.md`. They are derived
from updated anchor, `summary.md`, and `detailed.md`. They do not replace
anchor, summary, detailed, or graph.

For project records, the fixed location and name is:

```text
daily_research_reports/MMDD/<topic>/05_report_card.md
```

Advisor-facing report cards must use the fixed structure in
`templates/reporting/report_card_template.md` and be saved as
`05_report_card.md` in daily or sync packages. The required sections are:

```text
Source Files
Executive Summary
Research Process Update
Terms Used Here
Key Figures
Current Claim
Claim Boundary
Next Step
```

They should be self-contained, brief, and complete enough for an advisor to
understand the question, falsifiable hypothesis, evidence, boundary, and next
decision. Do not put private advisor questions, rehearsal scripts, raw logs,
long tables, or implementation details in the report card.

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
- By default, update only anchor / `summary.md` / `detailed.md` / daily card.
- Do not update root sync, sync to an external collaborator repo, package handoff
  reports, edit `graph.yaml`, commit, or push unless the user explicitly asks.
- Do not promote raw logs, checkpoints, datasets, full run directories, or
  unfiltered generated outputs into mainline paths.
- Do not leave completed anchors with stale evidence, claim boundary, next
  decision, or result links.
- When central figures exist, curated copies should appear in the experiment
  `figures/` folder and be embedded in `summary.md` and `detailed.md`.
- Markdown formulas must use `$...$` or `$$...$$`.

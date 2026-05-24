---
name: research-mainline
description: Use when organizing or updating a research project's mainline, hypothesis purpose cards, experiment folders, result summaries, closures, sync notes, research graph, and project status.
metadata:
  short-description: Maintain compact research mainline
---

# Research Mainline

Use this skill to keep a research project easy to inspect and easy to act on.
The goal is not to store every note. The goal is to make the current question,
hypotheses, evidence, claim boundary, and next decision obvious.

## Required Main Structure

```text
Projects/<project>/main/
  README.md
  current_mainline.md
  consensus.md
  status.md
  hypotheses/
    README.md
    <hypothesis_id>/
      purpose_card.md
      hypothesis_closure.md
      figures/
      source_notes/
  experiments/
    README.md
    <experiment_id>/
      README.md
      execution_plan.md
      summary.md
      detailed.md
      figures/
```

Optional project support surfaces:

```text
Projects/<project>/sync/
Projects/<project>/<worker>/sync/MMDD_topic/
Projects/<project>/<worker>/docs/
Projects/<project>/graph.yaml
results/R001_short_name/
```

## File Roles

### `current_mainline.md`

One-page state:

- one-sentence mainline;
- current safest claim;
- active hypotheses;
- what is not claimable;
- next decision.

### `consensus.md`

Shared knowledge boundary:

- supported premises;
- working hypotheses;
- unclear points;
- not-claimable points;
- assumptions accepted for the next experiment.

Update only after evidence, closure, or meeting feedback changes what can be
treated as known.

### `hypotheses/`

This is the reasoning layer. Each active hypothesis should have:

```text
hypotheses/<hypothesis_id>/purpose_card.md
hypotheses/<hypothesis_id>/hypothesis_closure.md
```

`purpose_card.md` comes before the experiment and must include problem level,
purpose, hypothesis/rivals, mathematical modeling, experiment design, expected
outcomes, and claim boundary.

After the experiment, the same `purpose_card.md` must be updated with result
links and final status. It should contain:

- direct result;
- one-sentence conclusion;
- next decision;
- links to `summary.md`, `detailed.md`, key figures if needed, and
  `hypothesis_closure.md`.

`hypothesis_closure.md` comes after evidence and should be concise,
self-contained, and written from the purpose card.

### `experiments/`

This is the execution and evidence layer. Each experiment should map to one
primary hypothesis.

```text
experiments/<experiment_id>/
  README.md
  execution_plan.md
  summary.md
  detailed.md
  figures/
```

`execution_plan.md` contains concrete configs, commands, metrics, artifacts,
pass/fail criteria, and failure modes.

`summary.md` is the local result synthesis. It must link the hypothesis purpose
card and state observation, interpretation, limitation, claim update, and next
decision.

`detailed.md` stores longer tables, seed notes, command records, failed runs,
and supporting analysis.

Keep the first reading path in `experiments/` narrow. Active experiments should
be the ones most relevant to the proposition currently being verified. Move
older, weakly related, superseded, or purely supporting experiments into
`experiments/archive/` and maintain an `archive/README.md` with:

- archived folder;
- why it was archived;
- when it should be consulted again.

Do not delete evidence just because it is no longer active. Archive it unless
the user explicitly asks to delete it.

### `sync/`

`Projects/<project>/<worker>/sync/MMDD_topic/` is the default branch-local
collaborator or meeting sync surface. Use exactly one primary sync folder per
date for each worker. If the day contains several hypotheses, stages,
diagnostics, or experiment versions, put them as subfolders under that date's
primary sync instead of creating several same-date top-level sync entries.

`Projects/<project>/sync/` is for shared project-level sync after the result is
safe to share as project consensus.

Update sync once per active working day with the smallest shareable outcome:

- what changed;
- why it matters;
- what cannot be claimed;
- what handoff or question remains;
- where the collaborator can find code, config, data/manifest, result folder,
  figure folder, key artifacts, checkpoints, logs, and repro command.

For a given date, maintain one consolidated daily sync as the first reading
path. Put supporting diagnostics, extra figures, version reports, or detailed
artifact maps in subfolders, but keep the daily conclusion, evidence, boundary,
and next decision in one main document.

The top of the main `report.md` should be closure-like rather than purely
procedural: start with a compact researcher-facing summary that the user can
read aloud or edit as their own conclusion. This first section should anchor:
what changed today, the strongest hypothesis update, the key evidence, the
claim boundary, and the next decision. Put detailed experiment sections,
tables, figure walkthroughs, and artifact maps after this front summary.

This front summary is required and must be section `## 0. Closure-Style Daily
Summary`. Treat it like the user-fill judgment card in a hypothesis closure:
write it in the user's voice as compact editable points, or leave clearly marked
slots when the user wants to fill them. Do not bury the user's own summary below
implementation details.

Project-local sync must only reference paths visible inside the project
repository. Do not cite root-level `Research_System` materials such as
`daily_research_reports/`; if such material informed the sync, integrate the
necessary content into the sync itself.

For experiment sync, include a compact `Artifact / Repro Map`. The sync should
let a collaborator understand the result and know where to continue without
asking where the code, data, figures, or outputs live.

Experiment sync should use the same self-contained research-judgment structure
as closures after the front summary:

```markdown
## 0. Closure-Style Daily Summary
## 1. 目的
## 2. 假设
## 3. 数学建模
## 4. 实验设置
## 5. 结论
## 6. 证据
## 7. 结论边界
## 8. 下一步决策
## 9. 结果文档
```

When figures are central evidence, copy the most important report-ready figures
into the sync folder's local `figures/` directory and embed them with one
sentence explaining what each figure supports. Do not leave the sync as dry text
when visual evidence is what makes the claim understandable.

Do not put raw logs, full tables, or unfiltered experiment outputs here.

### `<worker>/docs/`

Use `Projects/<project>/<worker>/docs/` for named material documents that help
write future purpose cards and closures: concept notes, mathematical modeling,
metric guides, figure guides, meeting-derived definitions, and reusable
explanations.

### `graph.yaml`

Use `research-graph-sop` when a project needs a lightweight map of questions,
claims, evidence, methods, sources, outputs, and next tasks. The graph is a
navigation layer; Markdown files remain the reasoning layer.

### root `results/`

Use root-level `results/` only for curated stage-level outcomes that are stable
enough to cite across project mainlines, hypothesis closures, meeting briefs, or
PRISM reports.

Each curated result should be a folder:

```text
results/R001_short_name/
  README.md
  figures/
  tables/
  source_notes/
```

Do not place disconnected raw outputs here. Raw outputs stay under the project
experiment workspace.

## Mainline Update Test

A result or discussion updates the mainline only if it changes one of:

- current safest claim;
- consensus boundary;
- hypothesis status;
- experiment interpretation;
- what cannot be claimed;
- next decision.

If none change, write:

```text
No mainline update today.
```

## Rules

- Prefer fewer, sharper experiments over many weak ones.
- Do not promote raw logs, temporary notes, or exploratory branches into
  `main/`.
- Keep closures self-contained but concise.
- Do not leave completed hypotheses with `TBD` in the purpose card result,
  conclusion, next step, or result document links.
- When figures exist, copy report-ready images into local `figures/` and
  explain what each figure supports.
- Markdown formulas must use `$...$` or `$$...$$`.

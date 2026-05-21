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

### `sync/`

`Projects/<project>/<worker>/sync/MMDD_topic/` is the default branch-local
collaborator or meeting sync surface. Name folders with date and topic, and put
the actual report document inside the folder.

`Projects/<project>/sync/` is for shared project-level sync after the result is
safe to share as project consensus.

Update sync once per active working day with the smallest shareable outcome:

- what changed;
- why it matters;
- what cannot be claimed;
- what handoff or question remains;
- where the collaborator can find code, config, data/manifest, result folder,
  figure folder, key artifacts, checkpoints, logs, and repro command.

For experiment sync, include a compact `Artifact / Repro Map`. The sync should
let a collaborator understand the result and know where to continue without
asking where the code, data, figures, or outputs live.

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

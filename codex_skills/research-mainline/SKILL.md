---
name: research-mainline
description: Use when organizing or updating a research project's mainline, hypotheses, experiment cards, experiment results, and hypothesis status.
metadata:
  short-description: Maintain compact research mainline
---

# Research Mainline

Use this skill to keep a research project easy to inspect and easy to act on.
The goal is not to store every note. The goal is to make the current claim,
active hypotheses, planned experiments, experiment results, and current
hypothesis evaluation obvious.

## Required Main Structure

For each project, the main folder should be minimal:

```text
Projects/<project>/main/
  README.md
  current_mainline.md
  consensus.md
  status.md
  hypotheses/
    README.md
  experiments/
    README.md
    <experiment_id>/
      README.md
      purpose_card.md
      execution_plan.md
      summary.md
      detailed.md
      figures/
    <experiment_project_id>/
      README.md
      purpose_card.md
      execution_plan.md
      stages/
        <stage_id>/
          purpose_card.md
          execution_plan.md
          summary.md
          detailed.md
          figures/
      source_notes/
    hypotheses/
      <closure_id>/
        hypothesis_closure.md
        figures/
```

`README.md` is the default file to read first. It must point to every other
mainline file that matters.

Avoid adding default folders such as `handoff/` or `roadmap/`. If old material
must be preserved, put it under `legacy/` and do not make it part of the default
read path.

## File Roles

### `README.md`

The default entry point. It should tell the reader:

- what to read first;
- where the current mainline lives;
- where hypotheses live;
- where experiment cards live;
- where experiment results live;
- where current hypothesis evaluation lives.

### `current_mainline.md`

The current project state in one page:

- one-sentence mainline;
- current safest claim;
- what is not claimable;
- current active hypotheses;
- next decision.

### `consensus.md`

The current knowledge boundary:

- what is supported enough to use as a premise;
- what is only a working hypothesis;
- what remains unclear;
- what cannot be claimed;
- setup assumptions accepted for the next experiment.

Do not put raw logs or daily progress here. Update it only after hypothesis closure, result analysis, or meeting feedback changes what can be treated as known.

### `hypotheses/README.md`

The hypothesis index. Each hypothesis needs:

- hypothesis ID;
- short statement;
- status: `open`, `supported`, `weakened`, or `decided`;
- linked experiment card ID;
- next evidence needed.

Every experiment card must map to at least one hypothesis.

### `experiments/`

Experiment planning documents and result summaries live together in one folder
per experiment:

```text
experiments/<experiment_id>/
    README.md
    purpose_card.md
    execution_plan.md
    summary.md
    detailed.md
    figures/
```

For a gated experiment line, use recursive stage folders:

```text
experiments/<experiment_project_id>/
  README.md
  purpose_card.md
  execution_plan.md
  stages/
    <stage_id>/
      purpose_card.md
      execution_plan.md
      summary.md
      detailed.md
      figures/
  source_notes/
```

The top-level card explains the whole research logic chain. Stage cards explain
the local decision. `source_notes/` may store copied raw plans, meeting notes,
or daily notes as provenance; do not treat source notes as claim-safe results.

`purpose_card.md` is required before running. It should state:

- purpose / main reason;
- known narrative / premise;
- hypothesis to decide;
- data and task construction;
- setup boundary;
- metrics;
- what this can and cannot prove;
- next decision.

`execution_plan.md` is required once the experiment is ready to run. It should
state concrete configs, commands, artifacts, pass/fail criteria, and failure
modes.

`summary.md` is added after a run and should name:

- the corresponding experiment card;
- the hypothesis it changes;
- the direct result;
- the interpretation;
- the limitation;
- the key figure paths when figures exist;
- the claim update;
- the decision.

`detailed.md` is added after a run and should contain supporting tables, figures, seed notes, command
records, failed runs, and longer analysis. Do not make `summary.md` a raw log.

`summary.md` is also the local experiment closure. Do not create a separate
`closure.md` unless the user explicitly asks for a legacy split. For recursive
experiment projects, each stage closes locally through its own `summary.md`.

When figures exist, copy report-ready images into a `figures/` folder beside
the report and embed them with relative Markdown image links. A result is not
report-ready if the key plot path and what it supports are missing.

### `hypotheses/`

Use this folder for advisor-facing big closure documents. These synthesize a
tightly scoped hypothesis family or an experiment line across local experiment
summaries. They should not replace per-experiment `summary.md` files.

Each big closure should be a folder:

```text
hypotheses/<closure_id>/
  hypothesis_closure.md
  figures/
```

### `status.md`

Current hypothesis evaluation and what the latest results imply.

This is not a meeting report. It should answer:

- which hypotheses are supported, weakened, open, or decided;
- which results caused the current status;
- what the evidence suggests;
- what still cannot be claimed;
- what decision should be made next.

## Experiment Card Contract

Use this minimal purpose-card shape:

```markdown
# Experiment Card: E1 Short Name

Purpose / Main Reason:
Known Narrative / Premise:
Hypothesis To Decide:
Experiment Question:
Data And Task Construction:
Setup:
Baselines:
Metrics:
Expected Outcomes:
Can Prove:
Cannot Prove:
Status:
Next Decision:
```

Keep cards short. If a card needs long background, the background belongs in a
separate source note, the detailed execution plan, or `legacy/`, not in the
purpose card.

## Mainline Update Test

A result or discussion updates the mainline only if it changes one of:

- the current safest claim;
- the consensus boundary;
- a hypothesis status;
- an experiment card status;
- an experiment result interpretation;
- what cannot be claimed;
- the next decision.

If none change, write:

```text
No mainline update today.
```

## Output Shape

When answering, keep it short:

1. One-sentence conclusion
2. Mainline update: yes/no
3. What changed
4. What cannot be claimed
5. Next decision

Avoid praising novelty. Focus on whether the evidence moves the research forward.

## Formula Rule

When writing Markdown research documents, inline formulas must use `$...$` and display formulas must use `$$...$$`.

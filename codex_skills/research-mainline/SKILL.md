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
  status.md
  hypotheses/
    README.md
  plans/
    README.md
    E*.md
  experiments/
    README.md
    R*.md
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

### `hypotheses/README.md`

The hypothesis index. Each hypothesis needs:

- hypothesis ID;
- short statement;
- status: `open`, `supported`, `weakened`, or `decided`;
- linked experiment card ID;
- next evidence needed.

Every experiment card must map to at least one hypothesis.

### `plans/`

Only experiment cards belong here.

Every plan file should be a compact experiment card and should name the
hypothesis it tests. Do not put long narrative plans here.

### `experiments/`

Only experiment result summaries belong here.

Every result file should name:

- the corresponding experiment card;
- the hypothesis it changes;
- the direct result;
- the interpretation;
- the limitation;
- the decision.

### `status.md`

Current hypothesis evaluation and what the latest results imply.

This is not a meeting report. It should answer:

- which hypotheses are supported, weakened, open, or decided;
- which results caused the current status;
- what the evidence suggests;
- what still cannot be claimed;
- what decision should be made next.

## Experiment Card Contract

Use this minimal card shape:

```markdown
# Experiment Card: E1 Short Name

Hypothesis:
Question:
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
separate source note or `legacy/`, not in `plans/`.

## Mainline Update Test

A result or discussion updates the mainline only if it changes one of:

- the current safest claim;
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

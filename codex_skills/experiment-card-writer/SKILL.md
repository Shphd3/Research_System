---
name: experiment-card-writer
description: Use when designing, rewriting, or analyzing research experiments as purpose-first project-local experiment cards and detailed execution plans. Purpose cards connect the main purpose, mainline position, known narrative, hypotheses, experiment object, paradigm, expected outcomes, and hypothesis-update logic; execution plans contain concrete run details.
metadata:
  short-description: Write purpose-first experiment cards
---

# Experiment Card Writer

Convert experiment ideas, raw notes, logs, or result summaries into a
purpose-first experiment card and, when needed, a detailed execution plan.

The first job is to stabilize the researcher's thinking before execution:
state why the experiment exists, where it sits in the mainline, what known
narrative it relies on, and what hypothesis it can actually decide.

## Location Rule

Project-specific experiment cards should live inside the active project, normally under:

```text
Projects/<project>/main/
```

For branch-local work, use the branch folder instead of project-level `main/`, for example:

```text
Projects/from-attention-to-search/XingyuD/main/experiments/<experiment_id>/
```

Default new-experiment layout:

```text
experiments/<experiment_id>/
  README.md
  purpose_card.md
  execution_plan.md
  summary.md
  detailed.md
  figures/
```

For a linked experiment line, use a recursive project folder:

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

Use recursive folders when there is a gated logic chain such as data sanity ->
dense readback -> MoE separation -> real-data statistics. Copy raw daily plans
or meeting notes into `source_notes/` only when they are needed as provenance.

Do not create root-level `experiments/` cards unless the user explicitly asks
for a global/cross-project card.

## Pre-Experiment Thinking

Before writing a card, answer these internally and reflect them in the card:

1. What is the purpose / main reason for this experiment?
2. Where does this experiment sit in the current project mainline?
3. What known narrative, premise, or prior result motivates it?
4. What is the experiment purpose, as distinct from the general purpose?
5. What is the core hypothesis and what sub-hypotheses make it decidable?
6. What is the experiment object and high-level paradigm?
7. What result patterns would update the hypothesis?
8. What are the claim boundaries?

## Required Output For Purpose Card

Write `experiments/<experiment_id>/purpose_card.md` first by default. Keep it
focused on the purpose chain, not run mechanics. Commands, full configs,
hyperparameters, metric schemas, artifact contracts, and pass/fail mechanics
belong in `execution_plan.md`.

```markdown
# Experiment Card: E1 Router-Attention Recall

## 1. Purpose / Main Reason
Explain why this experiment exists and what thinking it is meant to clarify.

## 2. Mainline Position
Explain where this experiment sits in the active research chain.

## 3. Known Narrative / Premise
State the accepted premise, prior result, or working belief used by the
experiment. Keep it claim-safe.

## 4. Experiment Purpose
State the local decision this experiment is meant to make.

## 5. Hypothesis And Sub-Hypotheses
H1: Router bucket and attention top-token are aligned.

H1a:
H1b:
H1c:

## 6. Experiment Object
Name the data/model/signal object at a high level.

## 7. Experiment Paradigm
Describe the high-level comparison or diagnostic pattern.

## 8. Expected Outcomes And Hypothesis Update Logic
If H1 holds:

If H1 weakens:

If H1 fails:

## 9. What This Can Prove

## 10. What This Cannot Prove

## 11. Result
TBD.

## 12. Conclusion
TBD.

## 13. Next Step
TBD.
```

For recursive experiment projects:

- top-level `purpose_card.md` states the whole abstract purpose, known narrative,
  logic chain, hypotheses, stage map, and global claim boundary;
- each `stages/<stage_id>/purpose_card.md` states only the local purpose chain,
  local hypothesis, experiment object/paradigm, expected outcome logic, claim
  boundary, and next gate. It should not duplicate execution details.

## Required Output For Execution Plan

Write `experiments/<experiment_id>/execution_plan.md` when the user is preparing a run. It must be concrete
enough that another agent can execute without redesigning the experiment:

```markdown
# Execution Plan: E1 Router-Attention Recall

## 1. Run Goal

## 2. Data Construction

## 3. Model / Training / Evaluation Setup

## 4. Configs And Commands

## 5. Metrics And Artifacts

## 6. Pass / Fail Criteria

## 7. Failure Modes To Check

## 8. Result Location
```

For recursive experiment projects, the top-level `execution_plan.md` should
define stage order and gates. Each stage `execution_plan.md` should define the
actual runnable setup, metrics, artifacts, pass/fail criteria, and result
location.

## Required Output For Result Analysis

Each experiment result should be a folder. Put claim-safe synthesis in
`summary.md` and longer evidence in `detailed.md`. `summary.md` is also the
local experiment closure.

Use this compact shape for `summary.md`:

```markdown
# Result Summary: E1 Router-Attention Recall

### Purpose And Hypothesis
Briefly restate the experiment purpose and hypothesis from `purpose_card.md`.

### Observation
We observe: Gate candidate Recall@K = __, Random candidate Recall@K = __.

### Interpretation
This means whether Gate candidates contain more dense-attention top-M tokens than Random candidates.

### Limitation
This does not show:
- full inference will accelerate;
- all layers/heads behave the same;
- real long-context tasks will benefit.

### Key Figures
- Figure:
- Path:
- What it should show:
- Meeting use:

### Decision
Therefore:
- if Gate > Random: continue to candidate exact attention;
- if Gate ~= Random: check whether a memory router is needed;
- if only some layers/heads work: use layer/head-wise selective routing.
```

Use `detailed.md` for full tables, per-seed metrics, figures, logs, and
counterexamples. When figures exist, copy report-ready images into a local
`figures/` folder beside the report, embed them with Markdown image links, and
explain which claim boundary each figure supports.

`summary.md` must close the local loop:

```markdown
# Result Summary: E1 Router-Attention Recall

## Purpose And Hypothesis

## Observation

## Interpretation

## Limitation

## Key Figures
- Figure:
- Path:
- Supports:

## Claim Update
- Supported:
- Weakened:
- Still unclear:

## What Cannot Be Claimed

## Next Decision
```

## Rules

- Keep the card short.
- Start with purpose and known narrative, not model details.
- Separate `purpose_card.md` from `execution_plan.md` for new experiments.
- For multi-stage lines, create recursive `stages/<stage_id>/` folders instead
  of flattening all cards into one document.
- Store each experiment result as a folder with `summary.md` and `detailed.md`.
- Use `summary.md` as the local experiment closure after every experiment or stage result exists.
- Do not output multiple cards unless the user asks.
- Separate result, interpretation, limitation, and decision.
- Do not let a metric improvement become a stronger public claim than it supports.
- Prefer decision-oriented wording over long experiment narration.
- Every experiment card should specify the key figure(s) needed for advisor-facing reporting.
- Figures should be diagnostic, not decorative: they must support a claim boundary or next decision.
- Result summaries and detailed analyses should embed local `figures/` images when figures exist.
- Put local experiment closure in `experiments/.../summary.md`; put advisor-facing big closure synthesis in `main/hypotheses/`.
- When writing Markdown research documents, inline formulas must use `$...$` and display formulas must use `$$...$$`.

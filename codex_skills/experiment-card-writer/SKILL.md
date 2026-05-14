---
name: experiment-card-writer
description: Use when designing, rewriting, or analyzing research experiments as purpose-first project-local experiment cards and detailed execution plans, with known narrative, hypothesis, data/task construction, setup boundary, baselines, metrics, result, conclusion, and next decision.
metadata:
  short-description: Write purpose-first experiment cards
---

# Experiment Card Writer

Convert experiment ideas, raw notes, logs, or result summaries into a
purpose-first experiment card and, when needed, a detailed execution plan.

The first job is to stabilize the researcher's thinking before execution:
state why the experiment exists, what known narrative it relies on, and what
hypothesis it can actually decide.

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
2. What known narrative, premise, or prior result motivates it?
3. What is the core hypothesis?
4. How are data and task constructed to test that hypothesis?
5. Why is this setup meaningful: model, data, task, diagnostic target?
6. What are the boundary conditions of this setup?
7. Which experiments are needed, and do they jointly test the hypothesis rather than only show a suggestive signal?

## Required Output For Purpose Card

Write `experiments/<experiment_id>/purpose_card.md` first by default:

```markdown
# Experiment Card: E1 Router-Attention Recall

## 1. Purpose / Main Reason
Explain why this experiment exists and what thinking it is meant to clarify.

## 2. Known Narrative / Premise
State the accepted premise, prior result, or working belief used by the
experiment. Keep it claim-safe.

## 3. Hypothesis To Decide
H1: Router bucket and attention top-token are aligned.

## 4. Experiment Question
Given query token q_t, do router-retrieved candidate tokens cover dense attention top-M tokens?

## 5. Data And Task Construction
Data:
Task:
Target signal:
Why this construction tests H1:

## 6. Setup
Model:
Dataset:
Layer:
Head:
Signal source:
Candidate construction:

## 7. Baselines
- Random bucket
- Local window
- Oracle top-M
- Full attention

## 8. Metrics
- Recall@K
- Attention Mass Recall
- Candidate Ratio
- Sparse Output Error
- Accuracy Drop

## 9. Key Figures For Reporting
- Figure 1:
- Figure 2:
- Figure 3:

## 10. Expected Outcomes
If H1 holds:
Gate recall > Random recall.

If H1 fails:
Gate recall ~= Random recall.

## 11. What This Can Prove
It can test whether the router provides a coarse retrieval signal.

## 12. What This Cannot Prove
It cannot prove full inference speedup.
It cannot prove million-token scalability.
It cannot prove standard MoE routing is already sufficient.

## 13. Result
TBD.

## 14. Conclusion
TBD.

## 15. Next Step
TBD.
```

For recursive experiment projects:

- top-level `purpose_card.md` states the whole abstract purpose, known narrative,
  logic chain, hypotheses, stage map, and global claim boundary;
- each `stages/<stage_id>/purpose_card.md` states only the local purpose,
  local hypothesis, data/task construction, claim boundary, and next gate.

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
`summary.md` and longer evidence in `detailed.md`.

Use this compact shape for `summary.md`:

```markdown
# Result Summary: E1 Router-Attention Recall

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
- What it should show:
- Meeting use:

### Decision
Therefore:
- if Gate > Random: continue to candidate exact attention;
- if Gate ~= Random: check whether a memory router is needed;
- if only some layers/heads work: use layer/head-wise selective routing.
```

Use `detailed.md` for full tables, per-seed metrics, figures, logs, and
counterexamples.

## Rules

- Keep the card short.
- Start with purpose and known narrative, not model details.
- Separate `purpose_card.md` from `execution_plan.md` for new experiments.
- For multi-stage lines, create recursive `stages/<stage_id>/` folders instead
  of flattening all cards into one document.
- Store each experiment result as a folder with `summary.md` and `detailed.md`.
- Do not output multiple cards unless the user asks.
- Separate result, interpretation, limitation, and decision.
- Do not let a metric improvement become a stronger public claim than it supports.
- Prefer decision-oriented wording over long experiment narration.
- Every experiment card should specify the key figure(s) needed for advisor-facing reporting.
- Figures should be diagnostic, not decorative: they must support a claim boundary or next decision.
- When writing Markdown research documents, inline formulas must use `$...$` and display formulas must use `$$...$$`.

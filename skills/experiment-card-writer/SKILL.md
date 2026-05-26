---
name: experiment-card-writer
description: Use only for operational experiment execution plans after an anchor/purpose-card is clear. Do not create separate hypothesis purpose cards; anchors own purpose, hypothesis, physical priors, math, and result updates.
metadata:
  short-description: Write anchor-based execution plans
---

# Experiment Plan Writer

Use this skill to turn a clear anchor into an executable experiment plan.

Core rule: **anchor first, experiment second**. An experiment exists because an
anchor needs evidence, not because a new run is easy to launch.

Precondition: if the task lacks a stable problem definition, physical prior,
mathematical model, computational realization, or primary decision metric, stop
and use `skills/problem-anchor-writer/SKILL.md` first.

Language rule: execution plans should be written in Chinese by default. Keep
English only for metric names, code identifiers, experiment IDs, paths, quoted
terms, and established technical labels where translation would reduce clarity.

## Location Rule

Do not write a separate `hypotheses/<id>/purpose_card.md`.

Use the anchor as the purpose card:

```text
Projects/<project>/main_specialization/problem_anchors/<anchor_id>.md
Projects/<project>/main/problem_anchors/<anchor_id>.md
```

Write concrete run details in the experiment folder:

```text
Projects/<project>/main/experiments/<experiment_id>/execution_plan.md
Projects/<project>/main/experiments/<experiment_id>/summary.md
Projects/<project>/main/experiments/<experiment_id>/detailed.md
```

Default mapping:

```text
one anchor -> one primary experiment folder or one gated experiment line
```

Multi-stage experiments are allowed, but every stage must link back to the
anchor and state its local decision gate.

## Before Writing

First verify that the problem anchor already answers:

1. What parent problem and sharper subproblem are being addressed?
2. What physical prior makes this problem meaningful?
3. What mathematical object expresses that prior?
4. What computational realization follows from the math?

Then compress the experiment into:

1. Why does this hypothesis matter now?
2. What is the hypothesis, and what rivals must be distinguished?
3. What mathematical object, variables, and assumptions define it?
4. What is the smallest experiment that can change belief?
5. What result patterns would support, weaken, or redirect the hypothesis?
6. What cannot be claimed even if the result is positive?

## Execution Plan Template

Write this only when the user is ready to run:

```markdown
# Execution Plan: <experiment_id>

Anchor:

## 1. Run Goal

## 2. Data Construction

## 3. Model / Training / Evaluation Setup

## 4. Configs And Commands

## 5. Metrics And Artifacts

## 6. Pass / Fail Criteria

## 7. Failure Modes To Check

## 8. Result Location
```

## Result Summary Template

```markdown
# Result Summary: <experiment_id>

Anchor:

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

- Default to the minimum decisive experiment: one anchor, one sharp test,
  one primary decision metric, and one closure.
- Fewer, sharper experiments are preferred over many shallow runs.
- Do not propose broad variable sweeps, many metrics, or multiple loosely
  related runs before the first hypothesis update is closed.
- Add extra variables, ablations, seeds, or diagnostics only when they
  distinguish a named rival explanation or protect the validity of the primary
  conclusion.
- If the first result is ambiguous, write the ambiguity down and design the next
  minimal test from that uncertainty instead of expanding the current run into a
  large experiment grid.
- Do not start with architecture, scripts, or metrics before the anchor is clear.
- Do not create separate hypothesis purpose cards.
- Anchors are reasoning artifacts; execution plans are operational artifacts.
- After results, use `sync-closure-writer` and update the anchor.
- Separate result, interpretation, limitation, claim update, and decision.
- Do not let a metric improvement become a stronger public claim than it supports.
- Figures must support a claim boundary or next decision.
- Markdown formulas must use `$...$` or `$$...$$`.

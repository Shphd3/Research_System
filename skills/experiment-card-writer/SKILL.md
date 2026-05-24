---
name: experiment-card-writer
description: Use when designing, rewriting, or analyzing research experiments as hypothesis-first purpose cards and concrete execution plans. Purpose cards live in hypotheses/ and must cover problem level, purpose, hypothesis, mathematical modeling, experiment design, expected outcomes, and claim boundaries; execution plans live in experiments/ and contain run details.
metadata:
  short-description: Write hypothesis-first purpose cards
---

# Hypothesis Purpose Card Writer

Use this skill to turn a research idea into a sharp hypothesis purpose card and,
only after that, an executable experiment plan.

Core rule: **hypothesis first, experiment second**. An experiment exists because
a hypothesis needs evidence, not because a new run is easy to launch.

## Location Rule

Write the purpose card in the hypothesis folder:

```text
Projects/<project>/main/hypotheses/<hypothesis_id>/purpose_card.md
```

Do not create worker-local `main/` folders such as
`Projects/<project>/<worker>/main/`. Worker folders may contain code workspaces,
docs, or sync notes, but the project mainline stays in `Projects/<project>/main/`.

Write concrete run details in the experiment folder:

```text
Projects/<project>/main/experiments/<experiment_id>/execution_plan.md
Projects/<project>/main/experiments/<experiment_id>/summary.md
Projects/<project>/main/experiments/<experiment_id>/detailed.md
```

Default mapping:

```text
one hypothesis purpose card -> one primary experiment folder
```

Multi-stage experiments are allowed, but every stage must link back to the
primary hypothesis purpose card and state its local decision gate.

## Before Writing

Internally compress the task into:

1. What problem level is this hypothesis answering?
2. Why does this hypothesis matter now?
3. What is the hypothesis, and what rivals must be distinguished?
4. What mathematical object, variables, and assumptions define it?
5. What is the smallest experiment that can change belief?
6. What result patterns would support, weaken, or redirect the hypothesis?
7. What cannot be claimed even if the result is positive?

## Purpose Card Template

```markdown
# Hypothesis Purpose Card: <hypothesis_id>

## 1. Problem Level

Where this hypothesis sits in the research question stack.

## 2. Purpose

Why this hypothesis matters now and what decision it should unlock.

## 3. Hypothesis And Rivals

H:

Rival 1:

Rival 2:

## 4. Mathematical Modeling

Objects:

Variables:

Assumptions:

Expected relation:

## 5. Experiment Design

Data / task:

Model / signal:

Diagnostic target:

Baseline / control:

## 6. Expected Outcomes And Hypothesis Update Logic

If H holds:

If H weakens:

If a rival explains the result better:

## 7. What This Can Prove

## 8. What This Cannot Prove

## 9. Linked Experiment

Experiment folder:

## 10. Result

TBD.

## 11. Conclusion

TBD.

## 12. Next Step

TBD.

## 13. Result Documents

TBD.
```

Keep the purpose card concise. If background is long, put it in `source_notes/`
or a named material note under `Projects/<project>/<worker>/docs/`.

## Execution Plan Template

Write this only when the user is ready to run:

```markdown
# Execution Plan: <experiment_id>

Hypothesis purpose card:

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

Hypothesis purpose card:

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

## Post-Experiment Backfill

After an experiment finishes, update the original
`hypotheses/<hypothesis_id>/purpose_card.md`. Do not leave the purpose card as a
pre-experiment artifact.

Backfill these sections:

- `Result`: one paragraph with the direct result.
- `Conclusion`: one sentence stating whether the hypothesis is supported,
  weakened, redirected, or still open.
- `Next Step`: the next decision, not a task list.
- `Result Documents`: links to the experiment `summary.md`, `detailed.md`, key
  figures when needed, and `hypothesis_closure.md` once written.

The purpose card should remain concise. Detailed evidence belongs in
`experiments/<experiment_id>/summary.md` and `detailed.md`.

## Rules

- Default to the minimum decisive experiment: one hypothesis, one sharp test,
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
- Do not start with architecture, scripts, or metrics before the hypothesis is clear.
- Purpose cards are reasoning artifacts; execution plans are operational artifacts.
- Every purpose card must be completed after the experiment by linking result
  documents and filling `Result`, `Conclusion`, and `Next Step`.
- Separate result, interpretation, limitation, claim update, and decision.
- Do not let a metric improvement become a stronger public claim than it supports.
- Figures must support a claim boundary or next decision.
- Markdown formulas must use `$...$` or `$$...$$`.

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

For the current MoE specialization line, use this plan as the local style
reference for pre-run execution plans:

```text
Projects/from-attention-to-search/main/experiments/slot_context_dominance_router_specialization/execution_plan.md
```

Its important pattern is: decision question first, primary hypothesis and rival
explanation second, then data construction, controlled conditions, primary
metric, decision rules, and a minimal report table.

## Location Rule

Do not write a separate `hypotheses/<id>/purpose_card.md`.

Use the anchor as the purpose card:

```text
Projects/<project>/main_specialization/problem_anchors/<anchor_id>.md
Projects/<project>/main/problem_anchors/<anchor_id>.md
```

Write concrete run details and result closure in the experiment folder:

```text
Projects/<project>/main/experiments/<experiment_id>/execution_plan.md
Projects/<project>/main/experiments/<experiment_id>/summary.md
Projects/<project>/main/experiments/<experiment_id>/detailed.md
Projects/<project>/main/experiments/<experiment_id>/figures/
Projects/<project>/main/experiments/<experiment_id>/tables/
```

Every experiment document must link back to its anchor. Do not use opaque
English phrases as the story title. Give one rigorous, clear sentence that
states what the experiment is trying to decide.

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

`summary.md` now carries the role that old hypothesis closures used to carry.
It is the first post-result reading path and must close the experiment at the
claim level. It should be self-contained enough for a meeting or collaborator
recap, while linking to `detailed.md` for the full record.

```markdown
# Result Summary: <experiment_id>

Anchor:
Story:

## 0. Closure Summary

目的：

假设 / 问题：

结论：

关键证据：

结论边界：

下一步决策：

## Observation

## Interpretation

## Limitation

## Key Figures

![<figure title>](figures/<figure>.png)

Supports:

## Claim Update
- Supported:
- Weakened:
- Still unclear:

## What Cannot Be Claimed

## Next Decision
```

## Detailed Report Template

`detailed.md` is the complete experiment record and evidence version of the
same research story, not a metric dump or timeline. It must include the full
experiment details needed to audit or reproduce the result: data construction,
conditions, model/training/eval setup, seeds, commands, job ids, artifact
paths, curated tables, key figures, failed or partial runs when relevant, and
interpretation. It must start with the quick recap and then expand the same
logic through setup, evidence, interpretation, and links.

```markdown
# Detailed Result: <experiment_id>

Anchor:

Story:

## 0. Quick Recap

目的：

假设：

实验思路：

结论：

证据：

## 1. Anchor Link And Decision Point

Anchor:

Parent question:

This experiment updates:

## 2. Purpose

## 3. Hypothesis And Rival Explanations

## 4. Experiment Logic

## 5. Setup

## 6. Primary Metric And Decision Rule

## 7. Main Result

## 8. Key Figures

![<figure title>](figures/<figure>.png)

Supports:

## 9. Evidence Walkthrough

## 10. Full Experiment Record

## 11. Interpretation

## 12. Claim Boundary

## 13. Next Decision

## 14. Links And Artifact Map
anchor:
summary:
sync report:
code workspace:
runner:
config:
key code files:
data / manifest:
result dir:
figure dir:
key tables:
logs / checkpoints:
repro command:
```

The quick recap is short. The later sections expand the same five points:
purpose, hypothesis, experiment logic, conclusion, and evidence.

All code and artifact entries should be concrete paths when available. A reader
should be able to jump from the detailed report to the runner, config, result
directory, figures, and reproduction command without asking where the code
lives.

Figures are mandatory when figures exist. Put report-ready figures under
`figures/`, embed the important ones in both `summary.md` and `detailed.md`,
and write one sentence stating which claim each figure supports. Put curated
tables under `tables/` and link or summarize them near the relevant metric.

## Rules

- Default to the minimum decisive experiment: one anchor, one sharp test,
  one primary decision metric, and one closure.
- A plan should be organized around the decision it can change, not around
  scripts. Start with the decision question and rival explanation before run
  conditions.
- For specialization experiments, route-alignment metrics are supporting
  evidence. The primary metric should test whether route assignment agrees with
  expert causal utility whenever that utility can be measured.
- Every required condition must have a purpose column or sentence explaining
  which rival explanation it distinguishes.
- Include a minimal report table before the run when the result should be
  meeting-facing or collaborator-facing.
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
- After results, write `summary.md` and `detailed.md`, update the anchor and
  root anchor copy, then use `sync-closure-writer` when a meeting or
  collaborator-facing report is needed.
- Treat `summary.md` as the closure-level result document. Do not create a
  separate hypothesis closure for ordinary experiment results.
- Treat `detailed.md` as the full experiment record. It should be sufficient to
  reconstruct what was run, where artifacts live, and how the conclusion was
  derived.
- Separate result, interpretation, limitation, claim update, and decision.
- Always include the anchor path, result document links, and a one-sentence
  story written in clear research language.
- After writing `detailed.md`, link it from the active anchor's current
  evidence section.
- Do not let a metric improvement become a stronger public claim than it supports.
- Figures must support a claim boundary or next decision.
- Markdown formulas must use `$...$` or `$$...$$`.

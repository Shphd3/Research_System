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

Use this general pattern for pre-run execution plans: decision question first,
primary hypothesis and rival explanation second, then material or case
construction, controlled conditions, primary metric, decision rules, and a
minimal report table. Project-local plans can be used as style references only
after removing domain-specific assumptions.

## Location Rule

Do not write a separate `hypotheses/<id>/purpose_card.md`.

Use the anchor as the purpose card:

```text
Projects/<project>/<mainline>/problem_anchors/<anchor_id>.md
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
one anchor -> one primary experiment folder or one staged experiment line
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
7. Which implementation stages need local pass/fail evidence before the final
   metric can be trusted?

For multi-stage experiments, write a compact stage audit rather than a long
debug plan. Each important stage should fit one row:

```text
stage | local question | input evidence | pass/fail rule | debug artifact | handoff
```

If a stage needs many thresholds or examples, put them in `detailed.md` or the
remote runbook. The execution plan should only name the evidence needed to
trust the final result.

For any nontrivial algorithm stage, write the exact algorithm before the run.
The shortest acceptable specification is:

```text
input / parameters / intermediate variables / steps / pass conditions /
fail conditions / failure reasons / outputs / debug artifacts
```

Keep the anchor compact. Put this algorithm specification in the execution plan,
remote runbook, or `detailed.md`.

If several reasonable operationalizations fail in the same way, stop expanding
the experiment grid and audit the goal or metric. Ask whether the label,
primary metric, or success condition still matches the downstream decision.

## Execution Plan Template

Write this only when the user is ready to run:

```markdown
# Execution Plan: <experiment_id>

Anchor:

## 1. Run Goal

## 2. Data / Material / Case Construction

## 3. System / Procedure / Evaluation Setup

## 4. Configs And Commands

## 5. Metrics And Artifacts

## 6. Stage Audit

| Stage | Local Question | Input Evidence | Pass / Fail Rule | Debug Artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## 7. Pass / Fail Criteria

## 8. Failure Modes To Check

## 9. Result Location
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

## Operationalization Boundary

This result falsifies:

This result does not falsify:

Tested operationalization:

Alternative operationalizations still open:

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
experiment details needed to audit or reproduce the result: data, materials, or
case construction; conditions; system/procedure/evaluation setup; seeds or
replicates when relevant; commands, job ids, artifact paths, curated tables,
key figures, failed or partial runs when relevant, and interpretation. It must
start with the quick recap and then expand the same logic through setup,
evidence, interpretation, and links.

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

## 10. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / Failed / Unclear | Failure Reason | What This Rules Out |
| --- | --- | --- | --- | --- |
| | | | | |

Falsified physical prior:

Falsified operationalization / proxy:

Remaining rival explanations:

## 11. Goal / Metric Audit, If Triggered

Trigger:

Old goal / metric:

Repeated failure pattern:

Downstream decision:

Revised goal / metric:

Errors now acceptable:

Errors still harmful:

## 12. Full Experiment Record

## 13. Interpretation

## 14. Claim Boundary

## 15. Next Decision

## 16. Links And Artifact Map
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
- Proxy-alignment metrics are supporting evidence. The primary metric should
  test the claimed mechanism or decision-relevant effect whenever it can be
  measured or intervened on.
- Every required condition must have a purpose column or sentence explaining
  which rival explanation it distinguishes.
- Multi-stage experiments must include a compact stage audit. Do not trust a
  final metric unless the plan names the stage-local evidence that can explain
  success, failure, or uncertainty.
- Nontrivial algorithm stages must have an exact algorithm specification before
  running. Do not treat broad words like `group`, `match`, `stable`, `aligned`,
  `valid`, `filter`, or `score` as an algorithm until the exact computation is
  written.
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
- If repeated reasonable fixes fail with the same pattern, perform a goal /
  metric audit before adding another algorithmic fix.
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
- When a result is negative or ambiguous, state whether it falsifies the
  physical prior itself or only the tested operationalization / proxy.
- Separate result, interpretation, limitation, claim update, and decision.
- Always include the anchor path, result document links, and a one-sentence
  story written in clear research language.
- After writing `detailed.md`, link it from the active anchor's current
  evidence section.
- Do not let a metric improvement become a stronger public claim than it supports.
- Figures must support a claim boundary or next decision.
- Markdown formulas must use `$...$` or `$$...$$`.

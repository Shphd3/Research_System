---
name: experiment-card-writer
description: Use only for operational experiment execution plans after a compact anchor decision card is clear. Do not create separate hypothesis purpose cards; anchors own the decision question, physical priors, falsifiable hypothesis, minimal math, primary metrics, and result updates.
metadata:
  short-description: Write anchor-based execution plans
---

# Experiment Plan Writer

Use this skill to turn a clear anchor into an executable experiment plan.

First apply `research-progress-core`. An experiment plan is valid only when it
preserves the chain from hypothesis to operational definition, minimal test,
metric plus visual evidence, failure analysis, and refined hypothesis. For
nontrivial work, the execution plan owns the implementation contract. If the
plan cannot identify what result would falsify or weaken the hypothesis, do not
write it as a runnable experiment yet.

Core rule: **anchor first, protocol second, experiment third**. An experiment
exists because an anchor needs evidence, not because a new run is easy to
launch.

Precondition: if the task lacks one decision question, physical prior,
falsifiable hypothesis, one minimal mathematical model, minimal test, or primary
decision metric, stop and use `skills/problem-anchor-writer/SKILL.md` first.

Language rule: canonical protocols, execution plans, summaries, and detailed
records are written in English by default. If a Chinese companion is needed,
create a separate `_cn.md` file such as `execution_plan_cn.md`, `summary_cn.md`,
or `detailed_cn.md`. In conversation, explain new technical terms in Chinese
before using English names or abbreviations.

Use this general pattern for pre-run execution plans: decision question first,
primary hypothesis and rival explanation second, then material or case
construction, controlled conditions, primary metric, decision rules, and a
minimal report table. Project-local plans can be used as style references only
after removing domain-specific assumptions.

## Location Rule

Do not write a separate `hypotheses/<id>/purpose_card.md`.

Use the anchor as the decision card:

```text
Projects/<project>/<mainline>/problem_anchors/<anchor_id>.md
Projects/<project>/main/problem_anchors/<anchor_id>.md
```

Write concrete run details and result closure in the experiment folder:

```text
Projects/<project>/main/experiments/<experiment_id>/protocol_for_approval.md
Projects/<project>/main/experiments/<experiment_id>/execution_plan.md
Projects/<project>/main/experiments/<experiment_id>/summary.md
Projects/<project>/main/experiments/<experiment_id>/detailed.md
Projects/<project>/main/experiments/<experiment_id>/figures/
Projects/<project>/main/experiments/<experiment_id>/tables/
```

Experiment IDs may include date or iteration labels because they are records of
tests, for example `HMMDD_short_topic`, `HMMDDa_short_topic_smoke`, or
`HMMDDb_short_topic_full`. Do not use experiment-style names for anchors.

If the experiment ID uses an `A` prefix, the number after `A` must be the
primary anchor id, not the calendar date:

```text
A<anchor_id>_<short_topic>/
```

For example, experiments for
`problem_anchors/05_04_uniform_feature_specialization_after_position_removal_anchor.md`
should use `A05_04_<short_topic>/`. Calendar dates should be placed in run
names, daily report folders, logs, or result folders.

Every experiment document must link back to its anchor. Do not use opaque
English phrases as the story title. Give one rigorous, clear sentence that
states what the experiment is trying to decide.

Default mapping:

```text
one anchor -> one primary experiment folder or one staged experiment line
```

Multi-stage experiments are allowed, but every stage must link back to the
anchor and state its local decision gate.

### Anchor Mapping Rule

Every protocol, execution plan, `summary.md`, and `detailed.md` for an
experiment must include an explicit anchor mapping near the top:

```text
Primary anchor:
Anchor decision question:
Experiment role:
Stage mapping:
- P0 / E0 / stage name -> anchor test or rival explanation it audits
- P1 / E1 / stage name -> anchor test or rival explanation it audits
```

Stages such as dataset audits, smoke checks, probes, decompositions, positive
controls, and ablations are usually not separate anchors. They are local tests
inside the primary anchor unless they introduce a new parent problem, a new
decision question, or a new hypothesis line. If a stage cannot be mapped to the
anchor's decision question, stop and either park it or ask whether a new anchor
is needed.

## Before Writing

First verify that the problem anchor already answers:

1. What parent problem and sharper subproblem are being addressed?
2. What physical prior makes this problem meaningful?
3. What mathematical object expresses that prior?
4. What primary metric and observable object can test it?

Then compress the experiment into:

1. Why does this hypothesis matter now?
2. What is the hypothesis, and what rivals must be distinguished?
3. What mathematical object, variables, and assumptions define it?
4. What is the smallest experiment that can change belief?
5. What result patterns would support, weaken, or redirect the hypothesis?
6. What result pattern counts as insufficient evidence?
7. Which known good, known bad, and known confusing cases should be inspected?
8. What cannot be claimed even if the result is positive?
9. Which implementation stages need local pass/fail evidence before the final
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

## Protocol For Approval Template

Write this before code changes or runs. Keep it under 30 lines.

```markdown
# Protocol For Approval: <experiment_id>

Goal:
Decision question:
Tested hypothesis:
Rival explanation:
Data:
Model:
Routing / algorithm:
Loss / objective:
Conditions:
Checkpoints / seeds:
Primary metric:
Secondary metrics:
Known good case:
Known bad case:
Known confusing case:
Success:
Failure:
Insufficient evidence:
What this cannot claim:
User approval checklist:
```

Stop after writing this file. Do not run the experiment until the user approves
the protocol. After approval, write `execution_plan.md` without adding
unapproved conditions.

Write this only when the user is ready to run:

```markdown
# Execution Plan: <experiment_id>

Anchor:
Approved protocol:

## 1. Run Goal

## 2. Data / Material / Case Construction

Include known good, known bad, and known confusing cases when possible.

## 3. System / Procedure / Evaluation Setup

## 4. Configs And Commands

## 5. Metrics And Artifacts

For each decision metric, state the question it answers and the cost of false
positives and false negatives when those costs differ.

## 6. Stage Audit

| Stage | Local Question | Input Evidence | Pass / Fail Rule | Debug Artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## 7. Pass / Fail Criteria

Include success, failure, and insufficient-evidence criteria.

## 8. Failure Modes To Check

## 9. Result Location
```

## Result Summary Template

`summary.md` is required. It is the first post-result reading path and closes
the experiment at the claim-update level. It should be self-contained enough to
state purpose, hypothesis/question, conclusion, key evidence, claim boundary,
and next decision, while linking to `detailed.md` for the full record.

Every `summary.md` must also be a medium-detail audit surface, not just a short
conclusion. It must contain these sections, with canonical artifacts using
English headings:

```text
Purpose
How It Was Done
Metrics
What Result A Would Mean
What Result B Would Mean
Concrete Result Analysis
Claim Boundary
Next Decision
```

`Purpose` states the decision question. `How It Was Done` states the data,
model, intervention/control, seeds/checkpoints, and the exact routed/loss
position at enough detail to audit the setup. `Metrics` names the primary
metric first and explains why it decides the judgment. `What Result A Would
Mean` and `What Result B Would Mean` define the main support/weakening patterns
before interpreting the observed result. `Concrete Result Analysis` reports the
actual numbers, important seed or condition exceptions, and figure/table
interpretation. This should be less exhaustive than `detailed.md` but detailed
enough for a medium-level understanding of the experiment.

```markdown
# Result Summary: <experiment_id>

Anchor:
Story:

## Purpose

## How It Was Done

## Metrics

## What Result A Would Mean

## What Result B Would Mean

## Concrete Result Analysis

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

`detailed.md` is required. It is the complete experiment record and evidence
version of the same research story, not a metric dump or timeline. Unlike
`summary.md`, which should stay concise and decision-facing, `detailed.md`
should be complete enough for a later AI or collaborator to re-analyze the
problem without re-running or re-discovering the artifact structure. It must
include the full experiment details needed to audit, reproduce, and reason over
the result: data, materials, or case construction; all executed conditions;
system/procedure/evaluation setup; seeds or replicates when relevant; commands,
job ids, artifact paths, curated tables, key figures, failed or partial runs
when relevant, and interpretation. It must start with the quick recap and then
expand the same logic through setup, evidence, interpretation, and links.

```markdown
# Detailed Result: <experiment_id>

Anchor:

Story:

## 0. Quick Recap

Purpose:

Hypothesis:

Experiment logic:

Conclusion:

Evidence:

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

Separate single-observation evidence, change evidence, and summary evidence
when the result depends on training trajectories, seeds, checkpoints, ablations,
or before/after comparisons.

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
handoff report:
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
purpose, hypothesis, experiment logic, conclusion, and evidence. When the run
has multiple protocols, seeds, checkpoints, interventions, or negative results,
`detailed.md` should preserve the full curated result set: per-condition
tables, seed-level or checkpoint-level summaries, figure-by-figure
interpretations, failure or ambiguity analysis, and explicit notes on which
conditions were not run and why. Do not replace this with averages only; use
averages as summary evidence after recording the seed/checkpoint evidence that
supports or contradicts the claim.

All code and artifact entries should be concrete paths when available. A reader
should be able to jump from the detailed report to the runner, config, result
directory, figures, and reproduction command without asking where the code
lives.

Figures are mandatory when figures exist. Put report-ready figures under
`figures/`, embed the important ones in both `summary.md` and `detailed.md`,
and write one sentence stating which claim each figure supports. Put curated
tables under `tables/` and link or summarize them near the relevant metric.

When the result is meeting-facing, generate a report card from
`templates/reporting/report_card_template.md`. The report card is
an advisor-facing, self-contained evidence card derived from anchor,
`summary.md`, and `detailed.md`, not a second closure. In project records, save
it as:

```text
daily_research_reports/MMDD/<topic>/05_report_card.md
```

It must follow the shared structure:

```text
Source Files
Executive Summary
Research Process Update
Terms Used Here
Key Figures
Current Claim
Claim Boundary
Next Step
```

It should include the falsifiable hypothesis, operational definition, minimal
test, knowledge update, important figures, term definitions, claim boundary,
and next step. Do not include private advisor questions, rehearsal scripts, raw
logs, long tables, or implementation details in the report card.

## Rules

- Follow the `research-progress-core` communication rule: state what is tested,
  where evidence will be found, what can pass, what can fail, why failure would
  matter, and what next decision the experiment can change.
- Operational definitions must include success, failure, and insufficient
  evidence.
- Pre-run plans should name known good, known bad, and known confusing cases
  whenever the domain allows it.
- For trajectory, seed, checkpoint, ablation, or before/after claims, separate
  single-observation evidence, change evidence, and summary evidence.
- Default to the minimum decisive experiment: one anchor, one sharp test,
  one primary decision metric, and one closure.
- A plan should be organized around the decision it can change, not around
  scripts. Start with the decision question and rival explanation before run
  conditions.
- Proxy-alignment metrics are supporting evidence. The primary metric should
  test the claimed mechanism or decision-relevant effect whenever it can be
  measured or intervened on.
- If false positives and false negatives have different costs, metric design
  must state those costs before the run.
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
- Do not run or expand a nontrivial experiment before the protocol is approved.
- Short result first: after a run, write `summary.md` before expanding
  `detailed.md`.
- Do not create separate hypothesis purpose cards.
- Anchors are reasoning artifacts; execution plans are operational artifacts.
- After results, always write `summary.md` and `detailed.md`, then update the
  anchor when the result changes the current hypothesis, evidence, claim
  boundary, or next decision. Do not update root sync, package handoff reports,
  edit graph, commit, or push unless the user explicitly asks. Use
  `handoff-report-writer` only when that explicit handoff request exists.
- Treat `summary.md` as the first result reading path. Do not create a
  separate closure document for ordinary experiment results.
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

## Reference Delegation

Do not duplicate detailed research-method rules here. When needed, load the
relevant `research-progress-core/references/` file:

- `algorithm_specification.md` for exact algorithm or stage contracts;
- `profiling_and_evidence.md` for metric, figure, example, and stage evidence;
- `failure_decomposition.md` when a result fails without a local cause;
- `goal_audit.md` when repeated reasonable fixes fail in the same way;
- `research_loop_checklist.md` for a quick pre-run or post-run review.

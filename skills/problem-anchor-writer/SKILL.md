---
name: problem-anchor-writer
description: Use when auditing, polishing, writing, or updating a research anchor. The anchor is the project-local equivalent of research-exploration docs/design.md: a compact but complete current-state design document. For rough hand-written anchors, critique first before writing a formal anchor.
metadata:
  short-description: Write anchor design documents
---

# Problem Anchor Writer

Use this skill to write or revise a research anchor.

An anchor is the current-state research design document. It is equivalent to
the research-exploration `docs/design.md`, adapted to this repository's
anchor-first workflow. It should preserve the user's research judgment while
making the problem, priors, model, computational realization, falsification
tests, evidence, claim boundary, and next decision inspectable.

The anchor has two reading layers:

```text
Tiny Summary = short anchor replay for the human reader
Minimal Replay = the approval-facing 9-line judgment check
Full anchor = auditable design document for AI, replay, and boundary checks
```

Do not solve anchor length by deleting the design logic. Solve it by making the
Tiny Summary and Minimal Replay strong enough that the user can recover the
current question, judgment, evidence, boundary, and next decision before
reading the full anchor. The full anchor is an audit layer, not the first
reading path.

## Short Anchor Contract

The formal anchor keeps the 0-8 structure, but section 0 is the real
human-facing decision surface:

```text
0. Tiny Summary
   - Chinese short replay, 3-6 short lines
   - Minimal Replay with the required 9 fields
1-8. Full audit layer
   - compact evidence and reasoning for AI replay and boundary checks
```

Keep sections 1-8 short: at most three bullets per section by default, and no
bullet should carry run commands, seed dumps, broad grids, or full result
presentation. If a section cannot stay short, move the material to
`protocol.md`, `summary.md`, or `detailed.md`.

## Self-Contained Core Rule

An anchor must be minimally self-contained. Do not rely on chat history, meeting
memory, or another artifact for the meaning of local labels. The first time a
local shorthand is used, define the concrete object it names:

- method or metric labels such as `M1`, `M2`, or `oracle`;
- condition labels such as `C1`, `C2`, or named controls;
- model variants, data slices, and intervention settings;
- primary metrics and thresholds that decide support or weakening.

The definition can be one line, but it must let a new reader audit what was
compared and why it bears on the decision question. Tiny Summary may use labels
only if the full anchor defines them nearby.

## User Workflow

Default workflow:

```text
minimal hand-written anchor
-> AI critique and clarification
-> formal anchor draft
-> user review
-> protocol.md
-> implementation / run
```

Do not jump from a vague idea directly to protocol or code. If the anchor is
unclear, critique the rough anchor first and name the missing decisions.

## Minimal Anchor Gate

The anchor is a decision card, not a complete research report. Before writing
or approving a formal anchor, the user or assistant must produce this minimal
replay:

```text
Question:
Physical prior:
Core model:
Model term being tested:
Primary metric:
Falsifier:
Can claim:
Cannot claim:
Next decision:
```

If this replay is unclear, do not polish the full anchor. Simplify the anchor
and return to audit mode.

Hard constraints:

- one decision question;
- one core physical prior, or at most three tightly linked priors;
- one core mathematical decomposition or mechanism relation;
- one primary metric;
- one falsifier;
- one next decision.

## Anchor Split Gate

Apply this gate before writing, approving, or extending a formal anchor. The
anchor is allowed to be self-contained, but it must stay one auditable decision
card.

Split the work into separate anchors or child anchors when any of these are
true:

- the draft needs more than one decision question;
- the draft needs more than one primary metric to decide the claim;
- the draft needs more than one falsifier;
- the draft needs more than one next decision;
- the diagnostics test different rival explanations that do not share the same
  physical prior, model term, and falsifier;
- the anchor starts carrying multiple historical iterations instead of the
  current-state judgment.

Do not hide a split problem by adding more subsections. If the material is long
because it contains run details, commands, configs, broad ablations, or result
presentation, move it to `protocol.md`, `summary.md`, or `detailed.md`. If the
material is long because the research question has branched, create a separate
anchor with its own Minimal Replay and falsification test.

When several diagnostic points are needed, write them as separate falsifiable
cards unless they are all necessary parts of the same single decision. Each
card must state its own prior, tested model term, primary metric, falsifier,
claim boundary, and next decision.

`Computational Realization` is only a drift-prevention stub. It may name input
objects, computed variables, stages, evidence, and expected artifacts, but it
must not become an implementation plan.

If `Computational Realization` exceeds 8 bullets or contains commands, config
details, broad sweeps, seed dumps, or result interpretation, move that material
to `protocol.md` or `detailed.md`.

After results, update the anchor only by compressing the result into:

- supported / weakened / insufficient evidence;
- rival explanations ruled out or still alive;
- new claim boundary;
- one next decision;
- links to `summary.md` and `detailed.md`.

Do not paste result reports into the anchor.

## Minimal Anchor Audit Mode

When the user gives a minimal or rough anchor, treat it as exposed thinking, not
as a half-finished document for the AI to silently complete.

First return an audit:

- user judgments to preserve;
- Anchor Split Gate violations, if the draft contains multiple decision
  questions, primary metrics, falsifiers, next decisions, or unrelated rival
  explanations;
- unclear object, feature definition, metric, scope, or causal claim;
- physical priors that are missing, too vague, or not falsifiable;
- hypotheses without clear falsifiers;
- math objects that do not map to measurable variables;
- computational realization gaps where the implemented object may drift from
  the mathematical object;
- claims that are stronger than the proposed evidence;
- the smallest additions needed before a formal anchor can be written;
- candidate tests that require user approval before becoming Minimal Tests.

If a new physical prior seems necessary, propose it as a candidate. Do not write
it into the formal anchor until the user accepts it.

## Formal Anchor Mode

Write a formal anchor only when requested or when the user has approved the
rough anchor direction. The formal anchor should tighten the user's logic, not
replace it with a cleaner but different research question.

## Required Structure

```markdown
# <Anchor Title>

## 0. Tiny Summary
## 1. Problem Definition
## 2. Physical Priors
## 3. Falsifiable Hypotheses
## 4. Mathematical Model
## 5. Computational Realization
## 6. Minimal Falsification Tests
## 7. Current Evidence
## 8. Claim Boundary And Next Decision
```

Do not add extra top-level sections by default.

## Section Requirements

### 0. Tiny Summary

Write this section as the first reading path, not as a vague abstract. It must
contain both a Chinese Tiny Summary and the Minimal Replay. If section 0 is not
clear, the full anchor is not ready.

```text
父问题：
当前子问题：
当前判断：
关键证据：
最危险边界：
下一步决策：
```

Then include:

```text
Question:
Physical prior:
Core model:
Model term being tested:
Primary metric:
Falsifier:
Can claim:
Cannot claim:
Next decision:
```

Length target: 3 to 6 short lines for Tiny Summary, plus the 9-line Minimal
Replay. Do not hide missing definitions in section 0 by saying "see below".

### 1. Problem Definition

Must include:

```text
Parent problem:
Sharper subproblem:
Decision question:
Not in scope:
```

There should be exactly one decision question.

### 2. Physical Priors

Write one to three falsifiable priors. Each prior should say what mechanistic
belief makes the question meaningful.

Use:

```text
P1:
Meaning:
Could be wrong if:
```

### 3. Falsifiable Hypotheses

Each hypothesis must be derived from the physical priors and have clear support
and weakening conditions.

Use:

```text
H1:
Supported if:
Weakened if:
```

### 4. Mathematical Model

Only define mathematical objects that the experiment can measure or use.

Must include:

```text
Objects:
Core decomposition:
Mechanism relation:
Observable metrics:
Falsifier:
```

Every equation must map to a physical prior, a measurable object, and a code or
analysis path.

### 5. Computational Realization

This is the main addition relative to the older compact anchor. It is the
minimum implementation contract that connects the model to code.

The reason this section exists is to prevent a common research failure: the
physical prior and mathematical model sound clear, but the implemented
experiment measures a different object. Computational realization forces the
anchor to name the actual inputs, derived variables, algorithm stages,
stage-local evidence, and expected artifacts before the protocol or code is
written.

Include only:

```text
Input objects:
Computed variables:
Algorithm stages:
Stage-local evidence:
Expected artifacts:
```

Do not put long commands, raw configs, logs, or implementation timelines here.
Those belong in `protocol.md` and `detailed.md`.

### 6. Minimal Falsification Tests

Write at most three tests. Each test should answer one question and map to the
current decision.

Use:

```text
Test:
Question:
Intervention / comparison:
Primary metric:
Supports:
Weakens:
Insufficient evidence:
```

For a user's first minimal anchor draft, do not finalize this section without
checking that sections 1-5 are clear.

### 7. Current Evidence

Write observed evidence, not a long result report.

Use:

```text
Observation:
Interpretation:
Boundary:
Evidence links:
```

Link to `summary.md`, `detailed.md`, figures, or tables when they exist.

### 8. Claim Boundary And Next Decision

Must include:

```text
Can claim:
Cannot claim:
Next decision:
```

There should be exactly one next decision.

## What Does Not Belong In The Anchor

Move these outside the anchor:

- run commands;
- long config tables;
- raw logs;
- seed-by-seed dumps;
- broad ablation grids;
- full implementation plans;
- literature review;
- meeting scripts;
- multiple historical iterations that no longer decide the current question;
- result presentation that belongs in `summary.md` or `detailed.md`.

## Post-Result Update

After an experiment, update the same anchor if the result changes the physical
prior, hypothesis status, evidence, claim boundary, or next decision.

Do not paste the result report into the anchor. Convert the result into:

- supported / weakened / insufficient-evidence status;
- rival explanations weakened or still alive;
- new boundary;
- next decision;
- links to `summary.md` and `detailed.md`.

## Relationship To Other Skills

- Use `research-progress-core` to audit whether the research loop is complete.
- Use `experiment-card-writer` after the anchor identifies the minimal test and
  the user is ready to write `protocol.md`.
- Do not create separate `hypotheses/<id>/purpose_card.md` files for new work.

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

## Minimal Anchor Audit Mode

When the user gives a minimal or rough anchor, treat it as exposed thinking, not
as a half-finished document for the AI to silently complete.

First return an audit:

- user judgments to preserve;
- unclear object, feature definition, metric, scope, or causal claim;
- physical priors that are missing, too vague, or not falsifiable;
- hypotheses without clear falsifiers;
- math objects that do not map to measurable variables;
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

Write this section in Chinese as the quick judgment surface:

```text
父问题：
当前子问题：
核心假设：
最小证伪测试：
当前边界：
下一步决策：
```

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

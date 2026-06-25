---
name: problem-anchor-writer
description: Use when auditing, discussing, writing, or updating a research anchor. For rough Thinking Cards, critique and clarify the user's judgment first; write a formal anchor only after the Thinking Card is clear or explicitly approved.
metadata:
  short-description: Audit and write anchor decision cards
---

# Problem Anchor Writer

Use this skill to audit, discuss, write, or revise a research anchor.

An anchor is the current-state research design document. It is equivalent to
the research-exploration `docs/design.md`, adapted to this repository's
anchor-first workflow. It should preserve the user's research judgment while
making the problem, mechanism, variables, causal relation, metric, rival
explanation, evidence boundary, and next decision inspectable.

This skill minimally contains the advisor `research-exploration` design chain:

```text
conjecture -> physical priors -> mathematical model
-> implementation contract -> experiment -> failure analysis
-> updated conjecture
```

In this repository, the mapping is:

```text
Thinking Card = user's conjecture and mechanism intuition
Physical Prior Review = AI-user discussion that turns intuition into priors
Mathematical Model Review = AI-user discussion that tests whether the model
  really expresses the intuition
Formal anchor sections 1-8 = compact `docs/design.md` equivalent
protocol.md = experiment design / falsification plan
summary.md + detailed.md = evidence and failure analysis
anchor update = updated conjecture and claim boundary
```

## Anchor Reading Layers

The anchor has two layers:

```text
0. Thinking Card
   - human-facing mechanism judgment card
   - preserves the user's current phenomenon, mechanism guess, variables,
     causal relation, observable metric, rival explanation, and decision rule
1-8. Full audit layer
   - compact design layer for AI replay, protocol alignment, and boundary checks
```

Do not solve anchor length by deleting design logic. Solve it by making
section 0 short and useful, while keeping sections 1-8 compact. The user's
first writing surface is the Thinking Card, not the full anchor.

## Thinking Card Contract

`00_handwrite_anchor.md` should require only:

```markdown
## 0. Thinking Card

**Phenomenon:** why this phenomenon deserves explanation.

**Mechanism guess:** which mechanism the user suspects.

**Key variables:** the minimal variables needed.

**Causal relation:** the directional relation among those variables.

**Observable metric:** the number or figure that can observe the relation.

**Alternative explanation:** the rival explanation that could also explain it.

**Decision:** what result would lead to pursue / revise / park.
```

Do not ask the user to hand-write the 0-8 formal anchor before this card is
clear. Do not silently expand a rough card into a polished formal anchor.

## User Workflow

Default workflow:

```text
Thinking Card in 00_handwrite_anchor.md
-> Thinking Card Audit
-> Physical Prior Review
-> Mathematical Model Review
-> user clarification / approval
-> formal anchor draft
-> user review
-> protocol.md
-> implementation / run
```

If the Thinking Card is unclear, stay in audit mode. Do not write a protocol,
implementation plan, broad test matrix, or formal anchor.

## Physical Prior Review

After the Thinking Card is coherent, the AI must work with the user to turn the
mechanism guess into physical priors before writing the formal anchor.

Return a short review:

```text
Candidate physical prior:
Why this prior follows from the Thinking Card:
What would make the prior false:
Which variable should expose it:
Which rival explanation it separates:
Smallest correction to the user's intuition:
```

Do not silently replace the user's intuition with a cleaner prior. If multiple
priors are possible, name the alternatives and ask which one is the current
mainline. If the prior cannot be falsified, say so and return to the Thinking
Card.

## Mathematical Model Review

After the physical prior is clear, the AI must discuss the mathematical model
with the user before writing the formal anchor.

Return a short review:

```text
Candidate model:
Variables:
Causal or mechanistic relation:
Observable metric:
What the model explains:
What the model cannot explain:
Mismatch with the user's intuition:
Revision needed before formal anchor:
```

Every equation must map to a physical prior, a model variable, an
implementation or analysis path, and an experiment or profiling artifact. If
the model is only a metaphor, do not promote it into the formal anchor.

## Thinking Card Audit

When the user gives a rough Thinking Card, treat it as exposed thinking, not as
a half-finished document for the AI to complete.

First return an audit:

- user judgments to preserve;
- unclear phenomenon, mechanism, variable, causal direction, metric, rival
  explanation, scope, or decision rule;
- hidden assumptions or causal overclaims;
- whether the observable metric can actually see the proposed causal relation;
- the strongest alternative explanation still alive;
- the smallest edit needed to make the card decision-ready;
- candidate formal-anchor mapping, if useful, but not a formal anchor.

If a new physical prior, mathematical model, metric, or falsifier seems
necessary, propose it as a candidate. Do not write it into the formal anchor
until the user accepts it.

## Thinking Card Clarity Gate

Before writing or approving a formal anchor, the Thinking Card must answer:

```text
Phenomenon:
Mechanism guess:
Key variables:
Causal relation:
Observable metric:
Alternative explanation:
Decision:
```

Hard constraints:

- exactly one main phenomenon;
- one mechanism guess, or a small set of tightly linked mechanism guesses;
- a minimal variable set;
- a stated causal direction;
- one primary observable metric;
- at least one rival explanation;
- one decision rule: pursue / revise / park.

If these are unclear, do not polish the anchor. Return to the Thinking Card.

## Formal Anchor Mode

Write a formal anchor only when requested or when the user has approved the
Thinking Card direction after the Physical Prior Review and Mathematical Model
Review. The formal anchor should tighten the user's logic, not replace it with
a cleaner but different research question.

Required structure:

```markdown
# <Anchor Title>

## 0. Thinking Card
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

### 0. Thinking Card

Section 0 is the first reading path and should remain short. It may use the
user's wording when that wording preserves real judgment. It must include:

```text
Phenomenon:
Mechanism guess:
Key variables:
Causal relation:
Observable metric:
Alternative explanation:
Decision:
```

Do not replace this section with an abstract, literature motivation, result
summary, or AI-polished thesis statement. If the decision rule is missing, the
formal anchor is not ready.

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

This is a drift-prevention stub that connects the model to code. It may name
input objects, computed variables, algorithm stages, stage-local evidence, and
expected artifacts, but it must not become an implementation plan.

Include only:

```text
Input objects:
Computed variables:
Algorithm stages:
Stage-local evidence:
Expected artifacts:
```

If this section exceeds 8 bullets or contains commands, config details, broad
sweeps, seed dumps, or result interpretation, move that material to
`protocol.md` or `detailed.md`.

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

Do not finalize this section until the Thinking Card and sections 1-5 are
clear.

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

## Anchor Split Gate

Apply this gate before writing, approving, or extending a formal anchor. Split
the work into separate anchors or child anchors when any of these are true:

- the draft needs more than one decision question;
- the draft needs more than one primary metric to decide the claim;
- the draft needs more than one falsifier;
- the draft needs more than one next decision;
- diagnostics test different rival explanations that do not share the same
  phenomenon, mechanism guess, causal relation, and decision rule;
- the anchor starts carrying multiple historical iterations instead of the
  current-state judgment.

Do not hide a split problem by adding more subsections.

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

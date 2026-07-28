---
name: problem-anchor-writer
description: Use when auditing a human-written Thinking Card or writing and updating a formal research anchor after the card has been approved.
metadata:
  short-description: Audit Thinking Cards and write anchors
---

# Problem Anchor Writer

An independent Thinking Card preserves the human's initial mechanism judgment.
A formal anchor turns the approved judgment into an auditable research design.
They are linked artifacts, not two sections of one document.

## Artifact Boundary

```text
<anchor_stem>_thinking_card.md
  human-owned initial judgment and uncertainty

<anchor_id>_<topic>_anchor.md
  AI-auditable design: problem, prior, hypothesis, model, realization,
  minimal test, evidence, claim boundary, and next decision
```

The Thinking Card must not become a protocol. The anchor must link the approved
Thinking Card and must not copy it into section 0. Use
`<anchor_stem>_thinking_card.md`; Chinese companions use
`<anchor_stem>_thinking_card_cn.md`.

## Human-First Gate

For a new idea, ask the human to fill:

```text
Phenomenon:
Mechanism guess:
Strongest rival explanation:
Most uncertain point:
Evidence that would change my mind:
Current next decision:
```

The human may mark an item `unknown`. Do not manufacture a confident answer.
If no card exists, create or show only the blank template at
`templates/research_process/thinking_card_template.md`.

## AI Audit

Before a formal anchor, return a short audit:

```text
Judgments to preserve:
Unclear definitions:
Hidden assumptions or causal overclaims:
Strongest rival still alive:
Can the proposed metric separate the rivals?:
Smallest falsifier:
AI-proposed correction, if any:
```

Label every AI-added prior, variable, metric, or model as a proposal. Move to a
formal anchor only after the human corrects or approves the direction.

## Formalization Gate

The approved Thinking Card must support all of these:

- exactly one phenomenon and one decision question;
- one mechanism guess with a stated causal direction;
- a minimal variable set;
- one primary observable metric;
- at least one live rival explanation;
- pass, fail, and insufficient-evidence meanings;
- one next decision;
- a conservative cannot-claim boundary.

If the metric cannot distinguish the mechanism from its rival, return to the
Thinking Card. More experiments do not repair an undefined decision.

## Physical-Prior Review

Before writing the anchor, check:

```text
Candidate physical prior:
Why it follows from the human judgment:
What would make it false:
Variable that exposes it:
Rival explanation it separates:
```

## Mathematical-Model Review

Then check:

```text
Core model:
Variables:
Mechanistic relation:
Observable metric:
What the model explains:
What it cannot explain:
Mismatch with the human intuition:
```

Every equation must map to a prior, a concrete computation, and an experiment
or analysis artifact. Do not promote a metaphor into a mathematical claim.

## Formal Anchor Structure

Write a formal anchor only when the Thinking Card, prior, and model have been
approved. Use exactly these top-level sections:

```markdown
# <Anchor Title>

Thinking Card source: [<anchor_stem>_thinking_card.md](...)

## 1. Problem Definition
## 2. Physical Priors
## 3. Falsifiable Hypotheses
## 4. Mathematical Model
## 5. Computational Realization
## 6. Minimal Falsification Tests
## 7. Current Evidence
## 8. Claim Boundary And Next Decision
```

Do not add an abstract, timeline, literature review, or embedded Thinking Card.
Keep one decision question, one core model, one primary metric, one main
falsifier, and one next decision. Put run-level settings in `protocol.md`.

### Section Requirements

1. Define the parent problem, sharper subproblem, decision question, and every
   non-obvious term. For a metric, state computation, unit, decision role, and
   what it cannot prove.
2. Use at most three physical priors, preferably one. State falsifiers and the
   variable exposing each prior.
3. State the primary hypothesis, strongest rival, predictions under each, and
   pass/fail/insufficient meanings.
4. Define variables before equations. Separate assumptions, derived results,
   empirical propositions, and intuition.
5. Map every mathematical object to a tensor, component, dataset field,
   intervention, or analysis computation.
6. Use one decisive test plus necessary guards. State metric, threshold, rival
   separated, allowed claim, and cannot-claim boundary.
7. Link `protocol.md`, `summary.md`, and `detailed.md`; separate observation
   from interpretation and remaining uncertainty.
8. State supported, weakened, and unresolved claims; what cannot be claimed;
   and exactly one next decision.

## Parent and Subanchor Rule

A parent anchor owns one complete major research problem. A subanchor inherits
the parent question and adjudicates one local clause, rival explanation,
robustness check, or metric guard. It must not repeat the full story or create a
parallel mainline.

Use one folder per sibling parent anchor:

```text
main/problem_anchors/<line_id>/README.md
main/problem_anchors/<line_id>/<parent_id>_<topic>/
  <parent_id>_<topic>_anchor.md
  <parent_id>_<topic>_thinking_card.md
  subanchors/
    <parent_id>_<NN>_<topic>_anchor.md
    <parent_id>_<NN>_<topic>_thinking_card.md
```

Reading order or `depends_on` between two parent anchors does not make either a
subanchor. Store an item in `subanchors/` only when it inherits the containing
parent's decision question. Keep each Thinking Card beside the anchor it owns,
and make the line `README.md` distinguish sibling-parent dependency order from
parent--child ownership.

## Result Update

```text
human closed-book summary
-> AI evidence and boundary audit
-> summary.md / detailed.md update
-> anchor sections 7 and 8 update
-> daily_research_reports/MMDD/focus.md closure
```

The human summary states the question, direct result, confirmed and weakened
beliefs, current mechanism, cannot-claim boundary, and one next decision. AI
may improve expression only after that draft exists.

## Language

The Thinking Card may remain Chinese. The canonical anchor is English unless
the user says otherwise; a Chinese companion uses `_cn.md`. Translation must
not change the question, model, metric, thresholds, boundary, or next decision.

## Validation

1. The Thinking Card exists and is linked, not duplicated.
2. Human judgment and AI proposals remain distinguishable.
3. Sections 1-8 contain one decision question and one next decision.
4. The primary metric separates the hypothesis from its rival.
5. Observation, interpretation, claim, speculation, and boundary are separate.
6. Every linked artifact exists.
7. Inline formulas use `$...$`; display formulas use `$$...$$`.

For legacy migration, use
`scripts/migrate_embedded_thinking_cards.py`. It extracts section 0 verbatim,
creates a subject-bearing card, replaces old `source_draft` metadata, and links
the formal anchor to the new card.

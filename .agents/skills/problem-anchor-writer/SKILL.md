---
name: problem-anchor-writer
description: "Use when the user asks to clarify a research question or create, revise, or audit its formal research Anchor. Do not use for experiment protocols, result records, execution, or publication."
---

# Problem Anchor Writer

The researcher states the initial mechanism judgment directly in conversation
or the active Focus. A formal Anchor preserves the approved judgment and is the
sole canonical current research design for that project question. It must carry
every decision-bearing function needed to move from the question to a falsifier
and bounded next decision. Do not create a parallel `design.md` or an
intermediate judgment card.

## Artifact Boundary

```text
<anchor_id>_<topic>_anchor.md
  sole canonical research design: problem, prior, hypothesis, model,
  constructible realization, minimal falsifier, iterative evidence,
  claim boundary, and next decision
```

If an imported method asks for `design.md`, satisfy that role in this Anchor.
Do not add a second design owner or require the external method at runtime.

## Human-First Gate

For a new idea, ask the human to fill:

```text
Parent research direction or problem:
Phenomenon:
Mechanism guess:
Strongest rival explanation:
Most uncertain point:
Evidence that would change my mind:
Current blocking uncertainty:
Why this decision is needed now:
Current next decision:
Known source material, or Unknown:
```

The human may mark an item `unknown`. Do not manufacture a confident answer.
Keep this judgment in the active Focus or the conversation until it is approved
for formalization in the Anchor.

## AI Audit

Before a formal anchor, return a short audit:

```text
Judgments to preserve:
Direction placement and why this question is next:
Unclear definitions:
Hidden assumptions or causal overclaims:
Strongest rival still alive:
Can the proposed metric separate the rivals?:
Smallest falsifier:
Grounding gaps and source links needed:
AI-proposed correction, if any:
```

Label every AI-added prior, variable, metric, or model as a proposal. Move to a
formal anchor only after the human corrects or approves the direction.

## Grounding And No-Invention Gate

Every decision-bearing statement must be grounded in an explicitly confirmed
human judgment, an approved parent Anchor, or a verified linked artifact. An
AI-added prior, definition, variable, metric, threshold, mechanism, or claim
must remain labeled `AI_PROPOSAL` until the researcher approves it.

When required information is absent, write `Unknown` or `BLOCKED`, state why it
matters, and link the most direct artifact that could resolve it. Do not infer a
claim from a filename, run ID, expected pattern, neighboring Anchor, or missing
result. A link supports audit; the Anchor must still state the local meaning
needed to understand its question and boundary.

## Formalization Gate

The approved researcher account must support all of these:

- exactly one phenomenon and one decision question;
- the parent direction, current blocking uncertainty, and why this is the
  smallest decision that can change the direction;
- one mechanism guess with a stated causal direction;
- the mechanism-selection decision and source-grounded alternatives when prior
  work materially changes what computation is admissible;
- a minimal variable set;
- one primary observable metric;
- at least one live rival explanation;
- pass, fail, and insufficient-evidence meanings;
- one next decision;
- a conservative cannot-claim boundary.

If the metric cannot distinguish the mechanism from its rival, return to the
researcher account. More experiments do not repair an undefined decision.

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

## Learnable Research Design Gate

When the anchor fits a parameterized model from data, read
[`references/learnable_research_design.md`](references/learnable_research_design.md)
completely before approving sections 4-6. The design must separate data
construction, learning task, training objective, architecture, optimization,
and untouched confirmation evidence.

Keep their ownership explicit:

- section 2 owns claims about the external data-generating process;
- section 4 owns the learning task, exact objective, variables, and constraints;
- section 5 owns the constructible data pipeline, architecture,
  objective-to-computation map, optimization class, and inference path;
- section 6 owns only the smallest falsifier and necessary guards.

Do not let the Protocol invent a missing task, supervision source, objective,
or scientific architecture rationale. If any design block is unresolved, mark
the anchor insufficient and keep the next decision on that block.

## Formal Anchor Structure

Write a formal Anchor only when the research question, prior, and model have
been approved. Use exactly these top-level sections:

```markdown
# <Anchor Title>

## 1. Problem Definition
## 2. Physical Priors
## 3. Falsifiable Hypotheses
## 4. Mathematical Model
## 5. Computational Realization
## 6. Minimal Falsification Tests
## 7. Current Evidence
## 8. Claim Boundary And Next Decision
```

Do not add an abstract, timeline, literature review, or embedded intake form.
Keep one decision question, one core model, one primary metric, one main
falsifier, and one next decision. Put run-level settings in `protocol.md`.

## Correspondence With `research-exploration-skill`

This Anchor satisfies that method's `design.md` role. The mapping below is
fixed: do not rename Anchor sections to match an external document, and do not
create a parallel `design.md`.

| `design.md` section | Anchor section |
|---|---|
| 1. Problem Definition | `1. Problem Definition` |
| 2. Physical Priors | `2. Physical Priors` |
| 3. Mathematical Model | `4. Mathematical Model` |
| 4. Related Work and Computational Design Decisions | folded into `5. Computational Realization`, which states the sourced adopt/adapt/baseline/reject decision |
| 5. Computational Implementation | `5. Computational Realization` |
| 6. Experiments and Iterative Evidence | `6. Minimal Falsification Tests` together with `7. Current Evidence` |

Two Anchor sections have no `design.md` counterpart because that method carries
their function elsewhere. `3. Falsifiable Hypotheses` is retained here because
the primary hypothesis, the strongest live rival, and the separating outcome
must be adjudicated inside the design. `8. Claim Boundary And Next Decision`
carries the bounded claim and the exactly-one next decision that the method
requires of every active question.

**Question hierarchy is owned here, not by that method.** Where
`research-exploration-skill` describes a `docs/research_map.md` tree, a
`docs/problems/<ID>/` layout, and evidence propagation between parent and child,
this repository keeps its own rule instead: a parent Anchor owns one complete
major research problem, a subanchor inherits the parent question and adjudicates
one local clause, and sibling parents are distinguished from parent-child
ownership by the line `README.md`. Do not create a parallel question tree, a
`research_map.md`, or a `design.md` to satisfy that method.

Before drafting, revising, or approving an anchor, read
[`references/anchor_self_containment.md`](references/anchor_self_containment.md)
completely. Self-contained means that a cold reader can reconstruct the
research judgment without opening links; it does not mean that the anchor owns
execution or reproducibility detail. Apply the reference's zero-net-growth
rule and do not add top-level sections to satisfy readability.

### Section Requirements

1. Define the parent problem, sharper subproblem, decision question, and every
   non-obvious term. State the current blocking uncertainty and why this is the
   smallest decision that can change the parent direction. For a metric, state
   computation, unit, decision role, and what it cannot prove.
2. Use at most three physical priors, preferably one. State falsifiers and the
   variable exposing each prior.
3. State the primary hypothesis, strongest rival, predictions under each, and
   pass/fail/insufficient meanings.
4. Define variables before equations. Separate assumptions, derived results,
   empirical propositions, and intuition.
5. Map every mathematical object to a tensor, component, dataset field,
   intervention, or analysis computation. When prior work materially selects,
   adapts, supplies a baseline for, or rules out the mechanism, state that
   decision and its direct source here; do not add a literature-review section.
6. Use one decisive test plus necessary guards. State metric, threshold, rival
   separated, allowed claim, and cannot-claim boundary.
7. State the minimum local evidence unit before linking `protocol.md`,
   `summary.md`, or `detailed.md`: key comparison, direct observation, safest
   interpretation, and remaining uncertainty.
8. State supported, weakened, and unresolved claims; what cannot be claimed;
   how Pass, Fail, and Insufficient redirect or stop the parent direction; and
   exactly one next decision with its completion criterion and resume action.

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
  subanchors/
    <parent_id>_<NN>_<topic>_anchor.md
```

Reading order or `depends_on` between two parent anchors does not make either a
subanchor. Store an item in `subanchors/` only when it inherits the containing
parent's decision question. The line `README.md` distinguishes sibling-parent
dependency order from parent--child ownership.

## Result Update

```text
human closed-book summary
-> AI evidence and boundary audit
-> summary.md / summary_cn.md / detailed.md update
-> anchor sections 7 and 8 update
-> researcher completes the actual result in the already-active
   daily_research_reports/MMDD/focus_<problem>.md
-> `research-final-report` writes <anchor_stem>_final_report.md once the question
   reaches a stable bounded conclusion
```

The human summary states the question, direct result, confirmed and weakened
beliefs, current mechanism, cannot-claim boundary, and one next decision. AI
may improve expression only after that draft exists.

## Language

The researcher's original judgment may remain Chinese. The canonical Anchor is
English unless the user says otherwise; a Chinese companion uses `_cn.md`. Translation must
not change the question, model, metric, thresholds, boundary, or next decision.

## Validation

1. The researcher-approved judgment and AI proposals remain distinguishable.
2. Sections 1-8 contain one decision question and one next decision.
3. The primary metric separates the hypothesis from its rival.
4. Observation, interpretation, claim, speculation, and boundary are separate.
5. A cold reader can reconstruct the question-to-decision chain without
   opening a link; links support audit rather than carry the explanation.
6. Every term, label, symbol, metric, and identifier needed for the decision is
   defined at first use in plain language.
7. Every decision-bearing statement is human-confirmed, inherited from an
   approved linked source, verified from evidence, or explicitly labeled
   `AI_PROPOSAL`, `Unknown`, or `BLOCKED`.
8. Unresolved or disputed items state their local consequence and link the
   direct artifact needed to audit or resolve them.
9. Readability changes obey zero net growth: added local explanation displaces
   at least as much chronology, run detail, secondary evidence, or repetition.
10. Every linked artifact exists.
11. Inline formulas use `$...$`; display formulas use `$$...$$`.
12. When prior work changes mechanism choice, Section 5 records the sourced
    adopt, adapt, baseline, or reject decision.

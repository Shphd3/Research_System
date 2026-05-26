---
name: problem-anchor-writer
description: Use when writing or revising the unified anchor/purpose-card document for a research problem: problem boundary, physical priors, mathematical modeling, computational realization, minimal experiment, evidence updates, and claim boundary.
metadata:
  short-description: Write problem-anchor documents
---

# Problem Anchor Writer

Use this skill to write or update the anchor. The anchor is now the unified
purpose card: it replaces separate hypothesis purpose cards as the main
pre-run and post-run reasoning artifact.

It is not a run log and not a standalone execution plan. It is the bridge:

```text
research intuition -> physical prior -> mathematical model -> computational realization
```

Use `docs/examples/example.md` as the compact default structure. When a longer
style reference is needed, use
`docs/examples/problem_attention_gated_low_level_matching.md`.

After updating an active project anchor, copy it to the categorized root sync
anchor path when the project defines one, for example:

```text
sync/<sync_id>/anchors/<category>/<anchor_id>.md
```

The project-local anchor remains the source of truth. Verify that source and
root copy are identical before finishing.

## Core Rule

A problem-anchor document must make the problem falsifiable and bounded.

Do not start from architecture, metrics, or scripts. First define:

- the parent problem;
- the exact subproblem;
- what is inside and outside the boundary;
- the physical prior or mechanistic assumption;
- the mathematical objects that express the prior;
- the computational test implied by the math.

Physical priors are the most important section. A physical prior is not a vague
preference for an architecture; it is an assumption about the structure of the
task, representation, memory, routing signal, or causal utility that could be
wrong and that constrains both the math and implementation.

If the active mainline is unstable, do not create a separate hypothesis purpose
card. First write or update the anchor at the project-specific anchor path:

```text
Projects/<project>/main_specialization/problem_anchors/<anchor_id>.md
Projects/<project>/main/problem_anchors/<anchor_id>.md
```

Use `support / weaken / redirect` instead of claiming that an experiment will
fully prove a broad hypothesis.

## Required Structure

Use this structure by default:

```markdown
---
parent_node: <parent_problem_or_graph_node>
---

# <Problem Anchor Title>

## 1. Problem Definition

What is the parent problem?

What is the sharper subproblem?

What is the decision question?

What is inside the boundary?

What is outside the boundary?

## 2. Physical Priors

State the physical, semantic, mechanistic, or embodied priors that make the
problem meaningful.

Each prior should have real content. Avoid empty claims such as "the model
should learn useful features."

For example, a KV-index prior could be:

```text
Language hidden states are not a flat unstructured memory. They contain
semantic or functional neighborhoods that can be partitioned into smaller
candidate sets before exact attention.
```

## 3. Motivation And Mechanism

Why should the prior help the system?

What mechanism connects the prior to the target behavior?

What rival mechanism could explain the same observation?

## 4. Mathematical Modeling

Define the objects, variables, assumptions, and expected relations.

Use math to pin down the physical prior, not to decorate the document.

Include:

- objects;
- variables;
- assumptions;
- mapping or operator;
- predicted relation;
- decision metric or observable.

## 5. Computational Realization

Translate the mathematical model into implementation terms:

- data construction;
- model components;
- intervention or control;
- algorithm / runner;
- measured observables;
- artifact outputs.

Every implementation choice should trace back to a mathematical object or
assumption.

## 6. Minimal Decisive Test

Specify the smallest experiment that can update the problem anchor.

Include:

- controlled setup;
- baseline;
- negative or rival control if necessary;
- primary decision metric;
- expected outcomes.

Do not expand into a broad experiment grid before this first test is closed.

## 7. Falsifiable Outcomes

Supported if:

Weakened if:

Redirected if:

Still not proven:

## 8. Current Evidence

Link existing result summaries, closures, figures, or reports.

State what the evidence directly supports and what it does not support.

## 9. Claim Boundary And Next Decision

Safest current claim:

What cannot be claimed:

Next smallest decision:
```

## Post-Result Update

After an experiment or analysis finishes, update the same anchor rather than
creating a new hypothesis closure. Backfill:

- direct observation;
- interpretation;
- whether the physical prior is supported, weakened, redirected, or still open;
- what cannot be claimed;
- next decision;
- links to sync closure, figures, tables, code/config, and result directories.

Long evidence belongs in a sync closure or experiment detailed report. The
anchor keeps the research question and claim boundary alive.

## Writing Standards

- Write in the language requested by the user. If no language is requested, use
  English for the anchor document and Chinese for the discussion summary.
- Define terms before using abbreviations.
- Keep the document self-contained.
- Prefer one precise subproblem over a broad umbrella question.
- Physical priors must be meaningful enough to be wrong.
- Mathematical modeling must constrain implementation choices.
- Computational realization must not introduce extra variables that are not
  needed by the model or falsification test.
- Inline formulas must use `$...$`; display formulas must use `$$...$$`.

## Relationship To Other Skills

- Use `scholar-mode` before this skill when the research intuition is still
  vague or conceptually unstable.
- Use `experiment-card-writer` only for the operational execution plan after
  this anchor identifies the minimal decisive test.
- After evidence exists, update the anchor from `summary.md` / `detailed.md`;
  then use `sync-closure-writer` when a meeting or collaborator-facing closure
  is needed.

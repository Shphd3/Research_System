---
name: problem-anchor-writer
description: Use when writing or revising an English research problem-anchor document that defines the problem boundary, parent/subproblem relation, physical priors, mathematical modeling, and computational realization before designing experiments.
metadata:
  short-description: Write problem-anchor documents
---

# Problem Anchor Writer

Use this skill to write an English document that anchors what problem the
research is solving before proposing experiments or implementation details.

This is not a result report and not an execution plan. It is the bridge:

```text
research intuition -> physical prior -> mathematical model -> computational realization
```

When available, use the structure of
`docs/externel_resources/problem_attention_gated_low_level_matching.md` as the
style reference.

## Core Rule

A problem-anchor document must make the problem falsifiable and bounded.

Do not start from architecture, metrics, or scripts. First define:

- the parent problem;
- the exact subproblem;
- what is inside and outside the boundary;
- the physical prior or mechanistic assumption;
- the mathematical objects that express the prior;
- the computational test implied by the math.

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

## Writing Standards

- Write in clear English.
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
- Use this skill before `experiment-card-writer` when the problem boundary or
  physical prior is not yet fixed.
- Use `experiment-card-writer` after this document identifies the minimal
  decisive test.
- Use `hypothesis-closure` after evidence exists.

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

Use `docs/examples/example.md` as the compact default structure. Project-local
anchors can be used as style references only after checking that their domain
terms do not leak into a new problem.

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
- the key terms that must be operationalized before the experiment;
- the physical prior or mechanistic assumption;
- the mathematical objects that express the prior;
- the computational test implied by the math.

Physical priors are the most important section. A physical prior is not a vague
preference for a method or architecture. It is a refutable assumption about the
structure of the problem, data-generating process, representation, mechanism,
environment, objective, or intervention that constrains both the math and
implementation.

Each physical prior must satisfy four requirements:

1. Real-world meaning: it says something concrete about the task, data,
   system, environment, representation, mechanism, intervention, or objective.
2. Refutability: it can be wrong, and the anchor names what evidence would
   weaken or redirect it.
3. Mathematical constraint: it maps to objects, variables, relations, or
   observables in the model.
4. Implementation constraint: it determines what data, intervention, metric,
   artifact, or control the experiment must use.

For mechanism-centered anchors, use this general pattern:

- state one narrow decision question before any implementation detail;
- write what the anchor does not solve;
- express the physical prior as a refutable causal/mechanistic condition;
- connect the observable signal, intervention, and claimed mechanism;
- name the rival explanation explicitly;
- make the primary metric test the claimed mechanism, not just a convenient
  proxy, whenever that mechanism can be measured or intervened on.

If the active mainline is unstable, do not create a separate hypothesis purpose
card. First write or update the anchor at the project-specific anchor path:

```text
Projects/<project>/<mainline>/problem_anchors/<anchor_id>.md
Projects/<project>/main/problem_anchors/<anchor_id>.md
```

Use `support / weaken / redirect` instead of claiming that an experiment will
fully prove a broad hypothesis.

## Compact Operationalization Rule

Anchors should contain operational definitions, but they must stay compact. Do
not turn the anchor into a methodology appendix.

For a new anchor, define only the terms that control the decision, usually
three to five terms. For each term, write one line:

```text
term: success / failure / ambiguous or insufficient evidence
```

Use this to keep intuitive words such as `stable`, `specific`, `causal`,
`aligned`, `consistent`, `robust`, or `shortcut` from becoming unmeasured
claims. Put long threshold details, diagnostics, and examples in the execution
plan or `detailed.md`, not in the anchor.

## Required Structure

Use this structure by default:

```markdown
---
parent_node: <parent_problem_or_graph_node>
---

# <Problem Anchor Title>

## 汇报前 Summary

问题：

假设：

证据入口：

当前判断：

结论边界：

下一步：

## 1. Problem Definition

What is the parent problem?

What is the sharper subproblem?

What is the decision question?

What is inside the boundary?

What is outside the boundary?

Operational definitions, only for decision-critical terms:

```text
term: success / failure / ambiguous or insufficient evidence
```

## 2. Physical Priors

State the physical, semantic, mechanistic, or embodied priors that make the
problem meaningful.

Each prior should have real content. Avoid empty claims such as "the model
should learn useful features."

Check each prior against the four requirements:

1. real-world meaning;
2. refutability;
3. mathematical constraint;
4. implementation constraint.

For example, a general prior could be:

```text
The target system is not fully explained by a single global statistic. It has
condition-dependent structure that should appear in a measurable variable and
change predictably under a controlled intervention.
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
- whether the result falsifies the physical prior itself, or only one
  operationalization / proxy of that prior;
- whether the physical prior is supported, weakened, redirected, or still open;
- what cannot be claimed;
- next decision;
- links to sync closure, figures, tables, code/config, and result directories.

Long evidence belongs in a sync closure or experiment detailed report. The
anchor keeps the research question and claim boundary alive.

If repeated reasonable operationalizations fail and a goal / metric audit
changes the downstream decision, update only the anchor's decision question,
primary observable, claim boundary, and next decision. Keep the audit details in
`detailed.md` or a sync closure.

## Writing Standards

- Write in the language requested by the user. If no language is requested, use
  English for the anchor document and Chinese for the discussion summary.
- Define terms before using abbreviations.
- Keep the document self-contained.
- Prefer one precise subproblem over a broad umbrella question.
- Use section titles that match the active compact template when possible:
  `Reporting Summary`, `Problem Definition`, `Physical Priors`,
  `Mechanistic Motivation`, `Mathematical Modeling`,
  `Computational Realization`, `Minimal Falsifiable Test`,
  `Falsifiable Outcomes`, `Current Evidence`,
  `Claim Boundary And Next Decision`.
- `汇报前 Summary` / `Reporting Summary` is a short front summary for meeting or
  collaborator reading. It should be concise, written in Chinese by default for
  this research system, and should not replace the full anchor sections. Its
  job is to let the advisor understand the work in about 60 seconds: problem,
  hypothesis, evidence entry point, current judgment, boundary, and next step.
  The evidence entry point should be either one key figure or a 2-3 sentence
  description of the minimal experiment.
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

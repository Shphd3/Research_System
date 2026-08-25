---
name: research-document-explainer
description: "Use when the user asks to read, explain, simplify, unpack, or ELI5 an AI-written research document, experiment, proof, formula, evidence chain, or research idea, especially when they say they cannot quickly get it. Do not use to author or revise formal Anchors, Protocols, results, Focus files, meetings, executions, or publications."
---

# Research Document Explainer

Make the document understandable to an intelligent adult who is not already an
expert in its local subfield. Preserve accuracy: the goal is to restore missing
objects and reasoning links, not make the science childlike.

## Required Reference Routing

Always read [explanation_contract.md](references/explanation_contract.md).
Then read only the modes requested or required by the source:

- experiment design, method, metric, result, or experiment suggestion:
  [experiment_reasoning.md](references/experiment_reasoning.md);
- theorem, equation, derivation, proof, or theoretical gap:
  [theory_and_proof.md](references/theory_and_proof.md);
- mechanism, research direction, evidence chain, or next research idea:
  [research_thinking.md](references/research_thinking.md).

Several modes may apply. Do not load a mode merely because the document names
an experiment or formula in passing.

## Default Depth

Use a one-screen first pass unless the user explicitly requests deep,
line-by-line, or complete treatment. A first pass gives the core question,
plain-language answer or status, essential objects, one reasoning chain,
boundary, and available zoom-ins. It does not compress an entire document into
one dense mini-paper.

For deep treatment, keep the same dependency order and add layers. Define an
object before using its symbol; explain why a step exists before its technical
implementation; give the direct claim before qualifications.

## Source And Judgment Boundary

Use the named document first and follow only links needed to verify a
decision-bearing statement. Keep these states distinguishable:

```text
SOURCE             explicitly stated by the document
VERIFIED_EVIDENCE  checked in a canonical source
EXPLANATION        faithful plain-language restatement
AI_INFERENCE       derived interpretation, with premises
AI_PROPOSAL        suggested experiment, proof route, or research direction
UNKNOWN            missing or not established
```

Group labels by paragraph or section; do not prefix every sentence. Never fill
a missing definition, result, assumption, or human judgment with plausible
glue.

## Scope

This skill may explain documents and offer bounded `AI_PROPOSAL` suggestions.
It never authors, revises, approves, or changes the status of a formal Anchor,
Protocol, result record, Focus, meeting artifact, execution, or publication.
Explaining a named file does not mutate it. Route formal question or Anchor
changes to `problem-anchor-writer`, active research decisions and Focus work to
`research-progress-core`, formal Protocol/result work to
`experiment-card-writer`, remote execution to `remote-experiment-workflow`,
meeting synthesis to `meeting-outline-writer`, publication to
`research-mainline`, and literature positioning or theory critique beyond the
named document to `scholar-mode`.

End with one small comprehension checkpoint or a short menu of the exact nodes
available for deeper explanation. Do not use a generic “any questions?” ending.

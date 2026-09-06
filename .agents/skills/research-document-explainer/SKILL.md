---
name: research-document-explainer
description: "Use when the user asks to understand or simplify a research document, experiment, result, proof, formula, evidence chain, or idea. Do not use to author or revise canonical research artifacts."
---

# Research Document Explainer

Make the document understandable to an intelligent adult who is not already an
expert in its local subfield. Preserve accuracy: the goal is to restore missing
objects and reasoning links, not make the science childlike.

## Required Reference Routing

Always read [explanation_contract.md](references/explanation_contract.md).
For a Chinese explanation, also read
[terminology_contract.md](references/terminology_contract.md). Consult the
global [Research Terminology Registry](../../../docs/research_terminology.md)
only when the answer needs a recurring English alias; do not load it for a
plain-language answer that does not use one.
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

In every Chinese explanation, each English alias, abbreviation, run code,
metric label, or method name must receive a Chinese-first definition earlier in
that same explanation, even when the alias is globally `APPROVED`. It must also
be either globally registered or explicitly defined in the local **本次术语**
block. Speed and source wording do not waive this gate.

## Source And Judgment Boundary

Use the named document first and follow only links needed to verify a
decision-bearing statement. Keep these states distinguishable. In Chinese
output, use the Chinese labels on the left; the internal codes on the right are
not reader-facing shorthand:

```text
来源原文      SOURCE
已核验证据    VERIFIED_EVIDENCE
解释          EXPLANATION
AI 推断       AI_INFERENCE
AI 建议       AI_PROPOSAL
未知          UNKNOWN
```

Group labels by paragraph or section; do not prefix every sentence. Never fill
a missing definition, result, assumption, or human judgment with plausible
glue.

## Scope

This skill may explain documents and offer bounded AI suggestions (internal
state `AI_PROPOSAL`).
It never authors, revises, approves, or changes the status of a formal Anchor,
Protocol, result record, Focus, meeting artifact, execution, or publication.
Explaining a named file does not mutate it. Route formal question or Anchor
changes to `problem-anchor-writer`, active research decisions and Focus work to
`research-progress-core`, formal Protocol/result work to
`experiment-card-writer`, remote execution to `remote-experiment-workflow`,
meeting synthesis or handoff writing to the matching `research-communication`
mode, publication to `research-mainline`, and literature positioning or theory
critique beyond the named document to `scholar-mode`.

For completed-result delivery, end with the next-step analysis required by the
repository result rule. For other explanations, end with one small
comprehension checkpoint or a short menu of the exact nodes available for
deeper explanation. Do not use a generic “any questions?” ending.

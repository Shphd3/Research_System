---
name: research-document-explainer
description: "Explain a named research document, result, formula or idea at the requested depth. Use for understanding; not canonical artifact edits, research approval or execution."
---

# Research Document Explainer

Explain the exact named source first. Follow links only to define an essential
object, check a decision-bearing value or resolve the claim boundary. Missing
sources remain unknown; readable wording never upgrades an unconfirmed source.

## Narrow answer or deeper explanation

For a narrow question, use this entrypoint: give the direct answer, define only
indispensable terms in plain Chinese, explain the decisive relation and nearest
boundary. Preserve assumptions and distinguish source content from AI inference
or suggestion. Do not force a glossary, quiz, menu or artifact into a short answer.

For a broad or deep explanation, read
[explanation_contract.md](references/explanation_contract.md), then only the
needed mode:

- experiment design, measured result or metric reasoning:
  [experiment_reasoning.md](references/experiment_reasoning.md);
- a formula, derivation, proof or theoretical gap:
  [theory_and_proof.md](references/theory_and_proof.md);
- mechanism, research direction or evidence-chain interpretation:
  [research_thinking.md](references/research_thinking.md).

A passing mention of a formula or experiment does not require its mode. Read
[terminology_contract.md](references/terminology_contract.md) when recurring
English aliases, ambiguous terminology or a requested glossary need consistency;
look up only the needed entries in the
[terminology registry](../../../docs/research_terminology.md).

## Explain in dependency order

Lead with the question and answer, then the indispensable objects, their
relation, supporting evidence and boundary. Define the object before its symbol
and Chinese meaning before an English alias. An inline local definition is
sufficient; use a `本次术语` block only when several local terms need grouping.
Use an example, figure or analogy only when it clarifies the actual relation.

Default broad explanations to one screen; expand when requested without
repeating the same conclusion. For formulas state quantity, symbols/units,
operation and assumptions. Distinguish 来源原文, 已核验证据, 解释, AI 推断,
AI 建议 and 未知 only where the distinction matters; do not label every sentence.

## Output and completion

For completed-result delivery, link the Summary first and give the decisive
value/figure, boundary and AI-labeled next-step analysis required by root rules.
For other requests, finish when the user's question is answered. A comprehension
check or precise zoom-in menu is useful when teaching is requested, not a gate.

This skill does not edit, approve or change Focus, Anchor, Protocol, results or
execution state. Switch to the owning artifact skill only if the user requests
that work; a brief explanation does not automatically require it.

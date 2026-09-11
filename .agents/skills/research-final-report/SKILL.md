---
name: research-final-report
description: "Use when a research question has reached a stable bounded conclusion and needs its paper-style final report, or when the user asks for a final article, final synthesis, or to close one question. Writes one final report per question. Do not use for per-round notes, protocols, or result records."
---

# Research Final Report

Turn one **settled research question** into a self-contained, paper-style report.
One question, one final report.

This is not a per-round note. Write it only after the working documents have
converged enough that a careful reader can learn the whole question without the
chat history, raw code, raw logs, or every intermediate document.

Adapted from the MIT-licensed `Projects/research-exploration-skill` release at
commit `0963fe5`. The adaptation keeps that method's report structure and claim
discipline and binds them to this repository's artifacts.

## Trigger

Write the report when the question's Anchor reaches a stable bounded conclusion.
All of these must hold:

```text
the core question and its boundary are stated in the Anchor
the claim boundary is known and researcher-confirmed
the main experiments have run and their protocols were frozen before execution
the decision-bearing tables and figures have been interpreted
major contradictions are resolved, or written as limitations
the bounded answer can be returned to the parent Anchor, when a parent exists
any remaining question is a separate Anchor, or none (terminal)
```

If any item is missing, do not write the report yet: name the missing piece.
AI drafts; the researcher confirms the wording, the boundary, and the next
question before the report is treated as final.

## Output

```text
<anchor_dir>/<anchor_stem>_final_report.md       # canonical, English
<anchor_dir>/<anchor_stem>_final_report_cn.md    # Chinese companion, same body
```

The report is question-owned, not date-owned, so it lives beside the Anchor it
synthesizes. It is a **derived reading surface**: it explains and does not
replace the Anchor, `protocol.md`, `summary.md` / `summary_cn.md`, or
`detailed.md`, and it must not introduce a number, verdict, or eligibility
decision that those files do not already own.

## Required Inputs

Read only what the question needs, then rewrite the story from scratch. Do not
paste old sections together.

```text
the Anchor (all sections, especially 7 and 8)
each experiment's protocol.md, summary.md / summary_cn.md, detailed.md
the human-confirmed Focus result, boundary, and one next decision
the parent Anchor, when the answer is returned upward
figures and tables that the date directory already lists as reading copies
```

A link supports audit; it does not carry explanation the report needs.

## Writing Standard

Write for a careful reader who knows linear algebra, probability, and basic
machine learning but has not seen this project.

- Define every important term at first use.
- State every symbol in every equation.
- Explain why an equation matches the prior, and how it becomes code or a metric.
- Say what each experiment was expected to show, then what actually happened.
- Separate observation, interpretation, conjecture, and speculation.
- State what the result does not prove.
- Keep this repository's object distinctions: semantic routing, expert utility
  under intervention, end-task performance, and representation accessibility are
  different objects and may not substitute for one another.
- No buzzwords, unexplained abbreviations, or private nicknames.
- Mathematics uses `$...$` inline and `$$...$$` display.

## Required Structure

```text
# Title

## Abstract
One paragraph: question, method, main finding, limitation.

## 1. Motivation
## 2. Problem Formulation
    exact question, scope, parent/child relation, objects, variables, model
    setting, and the current bounded answer
## 3. Physical Priors
## 4. Mathematical Model
## 5. Computational Implementation
## 6. Experimental Design
## 7. Results
    one subsection per result
## 8. Analysis
    connect results back to the model; say why the evidence supports, weakens,
    or refines the hypothesis
## 9. Claim Boundary And Limitations
## 10. Conclusion
## 11. Next Research Question
    or `none (terminal)`; never invent one to fill the section

## Reproducibility Appendix
    scripts, result files, figures, key commands, seeds, steps, artifacts
```

## Result Section Contract

Every decision-bearing result subsection carries:

```text
Purpose:            what question this result answers
Setup:              data, model, condition, metric, what changed between runs
Expected if true:   concrete pattern or numeric direction
Expected if false:  concrete pattern or numeric direction
Observed result:    numbers, or references to a figure the date directory owns
Interpretation:     why those observations matter
Take-home:          one plain sentence the reader should remember
What this does not prove:  the most important limitation
```

Explain every cited figure in text. Do not assume the reader infers the
conclusion from the plot.

## Claim Discipline

- Use `The experiment supports this mechanism in this registered setting`, not
  `The experiment proves the mechanism`.
- When using causal language, name the intervention or falsification evidence;
  if the evidence is correlational, say so.
- If the report proposes a mechanism, include at least one live alternative
  unless the experiments rule it out.
- Never turn `Fail` or `Insufficient` into progress language.

## Completion

The report is complete when: it can be read without the chat history; every
condition and metric is defined before first use; each result has a setup and a
take-home sentence; the conclusion does not exceed the Anchor's claim boundary;
the next question is clearly separate or recorded `none (terminal)`; and the
appendix holds enough paths to reproduce the evidence.

Keep `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION` visible until the researcher
confirms the wording.

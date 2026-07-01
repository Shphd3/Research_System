---
name: meeting-brief-writer
description: Write or revise strict advisor-facing and group-meeting briefs from existing research artifacts. Use when the user asks for meeting_brief.md, group meeting preparation, advisor brief, 模式一/模式二, or a self-contained meeting narrative with mechanism, evidence, claim boundary, and next action.
---

# Meeting Brief Writer

## Overview

Use this skill for the formal meeting-facing document itself. Use
`handoff-report-writer` only after the brief exists and the user explicitly
asks to package or sync material for another reader or repository.

A meeting brief is not an experiment timeline. It is a problem-centered
decision document: current question, mechanism model, evidence, boundary, and
next execution action.

## Required Template

Before writing or revising any `meeting_brief.md`, read:

```text
templates/meeting/meeting_brief_template.md
```

Follow either `模式一` or `模式二` exactly.

- Use `模式一` when there is one dominant research question or one mechanism
  line, even if several experiments provide evidence.
- Use `模式二` only when multiple parent questions must be reported together
  and cannot honestly be expressed as one mechanism line.
- Do not replace the required sections with a generic executive summary,
  handoff report, speaking script, or experiment list.

For `模式一`, `## 0. 执行摘要` must include these bold fields exactly:

```text
研究问题
机制解释
主要结果
证据说明
结论边界
执行动作
```

It must also contain up to three numbered result sentences. Each result
sentence must be a complete conclusion, not a noun phrase.

## Source Order

Do not use chat history as evidence. Rebuild the brief from source artifacts in
this order:

```text
PROJECTS.md
relevant graph when needed
anchor
protocol.md
summary.md
detailed.md
figures/ and tables/
```

Use the anchor for the current claim boundary and next decision. Use
`summary.md` for the meeting conclusion and central figures. Use `detailed.md`
only for precise setup, numbers, artifact maps, and validation details.

## Writing Rules

- Write in Chinese by default for meeting-facing briefs.
- Define every non-obvious term before using it as evidence.
- Explain the Chinese meaning first, then put reusable English abbreviations in
  parentheses only when needed.
- Avoid project nicknames and English jargon in headings and claims. If a file
  name or metric abbreviation must remain, define it in `术语解释`.
- Make the question, mechanism, evidence, and result the grammatical subjects.
  Avoid organizing the brief around "we ran", "we tried", or "we did".
- Start with the strongest supported conclusion, then state boundary and next
  action.
- Separate observation, interpretation, decision, and speculation.
- Do not create stronger claims than the linked anchor, summary, and detailed
  records allow.

## Required Content Checks

The brief is incomplete unless it has:

- a self-contained `术语解释` table for metrics, conditions, data names,
  abbreviations, and shorthand labels;
- one minimal mechanism model or explicit statement that the model is missing;
- at most three main result points;
- for each result point: mechanism correspondence, metric/condition
  definition, evidence, explanation, boundary, and source;
- central figures embedded near the claims they support;
- an execution action with purpose and completion criterion;
- a source index linking every anchor, protocol, summary, detailed record, and
  embedded figure used.

## Validation Before Finishing

Before returning the brief:

1. Check that the template sections are present and in the required order.
2. Check that all embedded figure paths exist.
3. Search for leftover English shorthand in claims and replace it with Chinese
   explanation unless it is a defined abbreviation or a file path.
4. Check formulas use `$...$` for inline math and `$$...$$` for display math.
5. Check that the next action is a minimal decision-bearing action, not a broad
   wish list.

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

Every meeting brief must also be written to a dated meeting folder:

```text
daily_research_reports/MMDD/meetings/<distinguishable_topic>_meeting_brief.md
daily_research_reports/MMDD/meetings/<distinguishable_topic>_meeting_brief_cn.md
```

Use a distinguishable topic-bearing filename. Do not use generic names such as
`meeting_brief.md` inside the dated meeting folder. A project-local
`meeting_brief.md` may also be updated when it is the source surface for an
experiment, but the dated meeting copy is required for future meeting lookup.

When the user asks for a shortened or pre-meeting brief, still follow the
required template, but compress the content around one dominant problem, one
supported conclusion, the concrete outputs/evidence, the claim boundary, and
one next decision. Do not expand into a literature-style analysis, experiment
timeline, or broad option list.

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

Inside the executive summary:

- `机制解释` must be multi-line when formulas are needed. It must list the
  most important formulas as display math, each preceded by one plain-language
  sentence that states what the formula means.
- `主要结果` must contain the advisor-facing main conclusions as numbered
  points. These points are the conclusions to be reported aloud, not evidence
  labels or experiment names.
- `证据说明` must map directly to the numbered main results. If one conclusion
  has multiple evidence items, use nested bullets under that conclusion.
- Result sentences must be complete conclusions, not noun phrases.

The document title must be the problem title itself. Do not prefix the title
with `会议简报：`.

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
- Use fully objective wording. Do not write "the advisor asked", "we want to",
  "we tried", "I suggest", or similar process-centered phrasing unless the user
  explicitly asks for a personal speaking script. State the research object,
  conclusion, evidence, boundary, and next action directly.
- Make every meeting brief self-contained. Define the problem, conditions,
  metrics, and outputs inside the brief so the reader does not need chat
  history or prior daily notes.
- For short briefs, prioritize: problem -> conclusion -> produced artifacts
  and decisive evidence -> boundary -> next action. Keep mechanism explanation
  to the minimum needed to make the conclusion understandable.
- Define every non-obvious term before using it as evidence.
- Explain the Chinese meaning first, then put reusable English abbreviations in
  parentheses only when needed.
- Avoid project nicknames and English jargon in headings and claims. If a file
  name or metric abbreviation must remain, define it in `术语解释`.
- Make the question, mechanism, evidence, and result the grammatical subjects.
  Avoid organizing the brief around "we ran", "we tried", or "we did".
- Start with the strongest supported conclusion, then state boundary and next
  action.
- The mechanism explanation must list the most important formulas as separate
  numbered or bulleted items, with a one-sentence plain-language meaning for
  each formula. In the executive summary, these formulas must be display
  formulas using `$$...$$`, not inline-only formulas.
- The main results must be conclusion statements tied to the mathematical
  model. Each result point should be short enough to say aloud and must not use
  undefined technical terms.
- In the executive summary, `主要结果` is the place for the main conclusions
  themselves. Do not put the conclusion list under `证据说明`.
- The evidence explanation must correspond to the main result points. If one
  result has multiple evidence items, split them into smaller sub-bullets under
  that result rather than merging them into one dense paragraph.
- Separate observation, interpretation, decision, and speculation.
- Do not create stronger claims than the linked anchor, summary, and detailed
  records allow.

## Required Content Checks

The brief is incomplete unless it has:

- a self-contained `术语解释` table for metrics, conditions, data names,
  abbreviations, and shorthand labels;
- one minimal mechanism model or explicit statement that the model is missing;
- an executive summary where `机制解释` contains the key display formulas,
  `主要结果` contains the numbered conclusions, and `证据说明` maps evidence
  back to those conclusions;
- at most three main result points;
- for each result point: mechanism correspondence, metric/condition
  definition, evidence, explanation, boundary, and source;
- evidence bullets that map directly back to the result points;
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
6. Check that the dated meeting copy exists under
   `daily_research_reports/MMDD/meetings/` with a topic-bearing filename.

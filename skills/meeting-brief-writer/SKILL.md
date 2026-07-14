---
name: meeting-brief-writer
description: Write or revise strict advisor-facing and group-meeting briefs from existing research artifacts. Use when the user asks for meeting_brief.md, group meeting preparation, advisor brief, 模式一/模式二, or a self-contained meeting narrative with mechanism, evidence, claim boundary, and next action.
---

# Meeting Brief Writer

## Overview

Use this skill for the formal meeting-facing document itself. Use
`handoff-report-writer` only after the brief exists and the user explicitly
asks to package or sync material for another reader or repository.

A meeting brief is not an experiment timeline and not a compressed result
ledger. It is a short problem-centered decision document: the two or three
questions that matter now, the minimum model and concrete data needed to
understand them, the current answers, the boundary, and one next action.

Default length is at most two rendered pages. For a Chinese brief, target
roughly 1,200--1,800 Chinese characters excluding the source index. If the
brief needs more space, move setup, metrics, tables, and figures to the linked
`summary.md` or `detailed.md`; do not lengthen the brief into a second report.

Every meeting brief must also be written to a dated meeting folder:

```text
daily_research_reports/MMDD/meetings/<distinguishable_topic>_meeting_brief.md
daily_research_reports/MMDD/meetings/<distinguishable_topic>_meeting_brief_cn.md
```

Use a distinguishable topic-bearing filename. Do not use generic names such as
`meeting_brief.md` inside the dated meeting folder. A project-local
`meeting_brief.md` may also be updated when it is the source surface for an
experiment, but the dated meeting copy is required for future meeting lookup.

The executive summary must tell a reader what changed in this update, what is
now known, what is not known, and what happens next. Immediately after it, the
brief must state the questions being answered. Only then introduce the
mathematical model and the exact data construction.

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
本次更新
当前结论
结论边界
执行动作
```

Inside the executive summary, use no project codes, run labels, or unexplained
metrics. Do not put formulas there unless the conclusion is impossible to say
accurately without one. The summary is a speaking surface, not a proof.

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
- Use this fixed reading order: executive summary -> questions -> minimal model
  and exact data -> current answers -> boundary and one next decision -> source
  links.
- Define every non-obvious term before using it as evidence.
- Explain the Chinese meaning first, then put reusable English abbreviations in
  parentheses only when needed.
- Avoid project nicknames and English jargon in headings and claims. If a file
  name or metric abbreviation must remain, define it in `术语解释`.
- Make the question, mechanism, evidence, and conclusion the grammatical subjects.
  Avoid organizing the brief around "we ran", "we tried", or "we did".
- Start with the strongest supported conclusion, then state boundary and next
  action. Each answer may contain only: direct answer, decisive evidence,
  boundary, and source link. Do not repeat the same conclusion in a second
  long subsection.
- Use at most two display formulas in the whole brief. Every formula must be
  preceded by one plain-language sentence and followed by definitions of all
  symbols. Prefer one concrete example over a general derivation.
- Include one exact data example whenever the claim depends on a synthetic or
  constructed task. State input, required intermediate variable, output, and
  training target.
- Do not use quotation marks to package an undefined concept, an informal label,
  or a causal claim. Except for a necessary verbatim quotation, replace quoted
  phrases with a direct definition of the object, condition, mechanism, or claim
  boundary.
- Separate observation, interpretation, decision, and speculation.
- Do not create stronger claims than the linked anchor, summary, and detailed
  records allow.

## Required Content Checks

The brief is incomplete unless it has:

- a self-contained executive summary using the required five fields;
- two or three explicit questions, never a broad topic list;
- a compact `术语解释` table containing only terms actually used;
- one minimal mechanism model or an explicit statement that the model is
  missing;
- one exact data example when constructed data are central;
- one direct answer per question, with decisive evidence, boundary, and source;
- exactly one next decision with pass/stop criteria;
- a compact source index linking the anchor, protocol, and only the result
  documents needed for audit.

Figures are optional. Embed a figure only if it decides one of the stated
questions; otherwise link the relevant `summary.md`.

## Validation Before Finishing

Before returning the brief:

1. Check that the template sections are present and in the required order.
2. Check that the brief is within the default length and does not repeat an
   experiment report.
3. Check that all embedded figure paths exist.
4. Search for leftover English shorthand in claims and replace it with Chinese
   explanation unless it is a defined abbreviation or a file path.
5. Search for quotation marks and confirm that each remaining pair is a necessary
   verbatim quotation rather than a substitute for definition or explanation.
6. Check formulas use `$...$` for inline math and `$$...$$` for display math.
7. Check that the next action is a minimal decision-bearing action, not a broad
   wish list.
8. Check that the dated meeting copy exists under
   `daily_research_reports/MMDD/meetings/` with a topic-bearing filename.

# Meeting Materials

Use `daily_research_reports/MMDD/meeting/` for group meeting, advisor meeting,
and short preparation notes.

Recommended shape:

```text
daily_research_reports/MMDD/meeting/
  meeting_brief.md
  meeting_notes.md
  advisor_questions.md
  slide_outline.md
```

Use the shared brief template for pre-meeting decision framing:

```text
templates/meeting/meeting_brief_template.md
```

`meeting_brief.md` should start with the conclusion, then give only the minimum
reason, claim boundary, and next decision. It is for meeting preparation, not a
replacement for an experiment `summary.md`, `detailed.md`, or `05_report_card.md`.

For experiment results that need advisor-facing discussion, keep the fast
reporting entry in:

```text
daily_research_reports/MMDD/<topic>/05_report_card.md
```

Use the shared template:

```text
templates/reporting/report_card_template.md
```

The reporting card should use the fixed `05_report_card.md` structure from the
shared template. It should include or link the relevant anchor, `summary.md`,
and `detailed.md`, embed important figures, and define necessary terms. Do not
maintain a separate meeting-only report-card format.

Meeting documents should optimize for claim boundaries:

- what can be said strongly
- what can only be said weakly
- what cannot be said
- what the next decisive experiment is

For branch-local project meetings, package a handoff only when the user
explicitly asks for it. The default location is the day's topic folder:

```text
daily_research_reports/MMDD/<topic>/handoff_report.md
daily_research_reports/MMDD/<topic>/<anchor_id>.md
```

Use the project sync folder only when the user explicitly asks for project or
collaborator sync:

```text
Projects/<project>/<worker>/sync/MMDD_topic/
```

The daily meeting folder can keep local preparation notes, but the collaborator-
facing report should be copied to project sync only on explicit request.

## Private Meeting Notes

Use this lightweight structure for post-meeting or personal notes:

```text
# Meeting Notes

## Meeting Diagnosis

导师的 Toy claim 是什么：

我同意什么：

我的 stronger concern 是什么：

三个未放松的假设：

1.
2.
3.

## Group Mainline

主线内容更新：

next-to-do：

## Personal Research Notes

主线内容更新：

next-to-do：

other：
```

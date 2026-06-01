# Meeting Materials

Use `daily_research_reports/MMDD/meeting/` for group meeting, advisor meeting,
and short preparation notes.

Recommended shape:

```text
daily_research_reports/MMDD/meeting/
  meeting_brief.md
  advisor_questions.md
  slide_outline.md
```

For experiment results that need advisor-facing discussion, keep the fast
reporting entry in:

```text
daily_research_reports/MMDD/<topic>/05_report_card.md
```

Use the shared template:

```text
daily_research_reports/_templates/report_card_template.md
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

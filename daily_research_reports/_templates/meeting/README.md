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

For experiment results that need oral discussion, keep the fast reporting entry
in:

```text
daily_research_reports/MMDD/01_reporting/<hypothesis_id>_reporting_card.md
```

The reporting card should start with an empty oral report card for the user to
write before the meeting, then include or link the relevant anchor, `summary.md`,
and `detailed.md`.

Meeting documents should optimize for claim boundaries:

- what can be said strongly
- what can only be said weakly
- what cannot be said
- what the next decisive experiment is

For branch-local project meetings, the primary shareable artifact should be an
optional handoff report created after the anchor and result records are updated:

```text
Projects/<project>/<worker>/sync/MMDD_topic/
```

The daily meeting folder can keep local preparation notes, but the collaborator-
facing report belongs in the project sync folder.

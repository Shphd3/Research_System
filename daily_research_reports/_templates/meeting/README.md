# Meeting Materials

Use `daily_research_reports/MMDD/meeting/` for group meeting, advisor meeting, and PRISM-ready documents.

Recommended shape:

```text
daily_research_reports/MMDD/meeting/
  meeting_brief.md
  advisor_questions.md
  slide_outline.md
  prism/
    main.tex
    figures/
```

For experiment closures, keep the fast reporting entry in:

```text
daily_research_reports/MMDD/01_reporting/<hypothesis_id>_reporting_card.md
```

The reporting card should start with an empty oral report card for the user to
write before the meeting, then include or link the closure snapshot.

Meeting documents should optimize for claim boundaries:

- what can be said strongly
- what can only be said weakly
- what cannot be said
- what the next decisive experiment is

For branch-local project meetings, the primary shareable artifact should come
from the hypothesis closure and live under:

```text
Projects/<project>/<worker>/sync/MMDD_topic/
```

The daily meeting folder can keep local preparation notes, but the collaborator-
facing report belongs in the project sync folder.

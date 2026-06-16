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

`meeting_brief.md` should start with a three-point conclusion and one summary
sentence, then give only setup, key evidence, uncovered boundary, and next
decision. It is for meeting preparation, not a replacement for an experiment
`summary.md` or `detailed.md`.

For experiment results that need advisor-facing discussion, make `summary.md`
and `detailed.md` self-contained enough to read directly.

Meeting documents should optimize for claim boundaries:

- what can be said strongly
- what can only be said weakly
- what this conclusion does not cover
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

Advisor's toy claim:

What I agree with:

My stronger concern:

Three unrelaxed assumptions:

1.
2.
3.

## Group Mainline

Mainline update:

next-to-do：

## Personal Research Notes

Mainline update:

next-to-do：

other：
```

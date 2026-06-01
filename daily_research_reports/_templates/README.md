# Daily Card Templates

Daily cards belong inside `daily_research_reports/MMDD/`, not in a separate root-level daily log folder.

The daily card replaces the old daily report. It should reduce thinking load:
state the day's purpose, task-level conclusions, mainline update, claim boundary,
and next decision.

There is no separate daily-report skill. Use the template directly and keep each
task split into `Did / Result / Interpretation / Claim boundary / Conclusion`.

For a new day, create:

```text
daily_research_reports/MMDD/daily_card.md
```

Use `daily_card_template.md` as the compact first-pass structure.

When an experiment result is summarized, create a compact meeting/advisor/sync
report card only if the user asks for meeting preparation or the result needs
advisor-facing discussion:

```text
daily_research_reports/MMDD/<topic>/05_report_card_for_advisor.md
```

Use `report_card_template.md`. The report card is derived from the anchor,
`summary.md`, and `detailed.md`; it does not replace them. It is
advisor-facing content: embed important figures, define necessary terms, state
the research-process update, and keep private advisor questions in daily or
meeting notes.

Class notes and side thoughts should stay inside `daily_card.md` by default:

- `Recording / Class Notes`: only keep class points that affect research judgment, task planning, or future reading.
- `Small Thought Parking Lot`: park side ideas without expanding them unless they directly block the current 25 minute task.

Meeting materials for the same day should be created under:

```text
daily_research_reports/MMDD/meeting/
```

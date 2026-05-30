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

When an experiment result is summarized, create a compact meeting-prep
reporting card only if the result needs oral discussion:

```text
daily_research_reports/MMDD/01_reporting/<hypothesis_id>_reporting_card.md
```

Use `reporting_card_template.md`. The top oral report card is intentionally
blank so the user can write the group-meeting language themselves. The
project-local anchor, `summary.md`, and `detailed.md` remain the source of
truth.

Class notes and side thoughts should stay inside `daily_card.md` by default:

- `Recording / Class Notes`: only keep class points that affect research judgment, task planning, or future reading.
- `Small Thought Parking Lot`: park side ideas without expanding them unless they directly block the current 25 minute task.

Meeting materials for the same day should be created under:

```text
daily_research_reports/MMDD/meeting/
```

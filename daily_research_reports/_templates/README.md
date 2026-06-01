# Daily Research Templates

This folder keeps reusable templates for research reporting surfaces.

## Daily Notes

There is no longer a maintained daily-card template.

Daily notes should stay minimal and free-form. Recommended fields:

```text
purpose
closed loop
claim boundary
next decision
private advisor questions
report card pointer, if needed
```

Do not turn daily notes into a second report system.

## Report Card

When an experiment result is summarized, create an advisor-facing report card
only if the user asks for meeting preparation or the result needs advisor-facing
discussion:

```text
daily_research_reports/MMDD/<topic>/05_report_card.md
```

Use `report_card_template.md`. The report card is derived from the anchor,
`summary.md`, and `detailed.md`; it does not replace them. It is a short,
self-contained advisor-facing evidence card with fixed sections:

```text
Source Files
Executive Summary
Research Process Update
Terms Used Here
Key Figures
Current Claim
Claim Boundary
Next Step
```

Daily topic folders use the fixed filename `05_report_card.md`. If the same
card is synced to a project or collaborator package, copy the card together
with the anchor, `summary.md`, `detailed.md`, and referenced figures/tables.

## Meeting Notes

Private meeting notes may include questions, worries, and reminders that should
not appear in advisor-facing report cards unless the user explicitly wants them
there.

Meeting materials for the same day should be created under:

```text
daily_research_reports/MMDD/meeting/
```

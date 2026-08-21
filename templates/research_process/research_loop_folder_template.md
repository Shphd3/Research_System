# Minimal Research Loop Folder

Create only files required by the current decision:

```text
<topic>_anchor.md
protocol.md      # only when running a nontrivial experiment
summary.md       # after results exist
detailed.md      # reproducibility and complete evidence
figures/         # only decision-relevant figures
```

Optional:

```text
<topic>_thinking_card.md  # only for a new human mechanism judgment
tables/                   # curated tables referenced by results
archive/                  # superseded evidence kept for traceability
```

Roles:

- `anchor`: current question, hypothesis, evidence boundary, next decision.
- `protocol.md`: approved comparison, metric, gates, and execution contract.
- `summary.md`: conclusion, primary result, boundary, next decision.
- `detailed.md`: full setup, run evidence, failures, and artifact map.

Do not add separate implementation plans, daily logs, closure reports, or
competing final reports. At the start of a meeting cycle, create one living
`daily_research_reports/MMDD/focus_<problem>.md` with the four-part plain-
language design. After canonical results exist, the researcher completes that
Focus's result, boundary, and one next decision. Only then write the one full
reader-facing story at
`daily_research_reports/MMDD/docs/daily_report_<topic_slug>.md`.

Important questions outside the current task live briefly in
`Projects/<project>/main/parking_lot/README.md`. Create
`focus_meeting_<topic>.md` only for an explicitly requested meeting brief or
synthesis, not for every ordinary one-problem cycle.

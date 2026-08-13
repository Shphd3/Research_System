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
competing final reports. When a completed experiment or bounded synthesis is
delivered in the daily report, write the one full reader-facing artifact at
`daily_research_reports/MMDD/docs/daily_report_<topic_slug>.md`. After
the researcher confirms its knowledge update, condense it into
`daily_research_reports/MMDD/focus_<problem>.md` as a minimal summary and
navigation card. A meeting uses a separately
created `focus_meeting_<topic>.md` after the human chooses its merge scope and
core question. Link the owning project artifacts.

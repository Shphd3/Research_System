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

Do not add separate implementation plans, daily logs, meeting briefs, closure
reports, or routine final reports. Use the day's self-contained `focus.md` for
the human knowledge update, explanation path, and next decision; link the owning
project artifact.

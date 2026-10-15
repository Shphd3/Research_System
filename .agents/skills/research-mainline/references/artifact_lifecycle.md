# Artifact Lifecycle

Use this reference to identify the owning artifact and the smallest update
surface.

## Ownership

| Artifact | Owns | Must not own |
|---|---|---|
| Anchor | Current adjudicable research design, evidence boundary, next decision | Commands, full run ledger, broad sweep |
| `protocol.md` | Draft-to-approved experiment contract and authorization scope | Post-hoc question changes or results |
| `summary.md` | Complete first result reading, central evidence, boundary, next-step analysis | Full evidence ledger |
| `detailed.md` | Setup, conformance, deviations, evidence lineage, failures, artifact map | A stronger second conclusion |
| `focus_<problem>.md` | Stable human-owned question, design confirmation, result boundary, next decision | Technical Protocol or run history |
| final report | Paper-style self-contained explanation, one per settled question | New evidence or a competing verdict |
| story | Explicit line-level synthesis | New experimental claim |
| Graph, roadmap, sync | Derived navigation or reading view | Independent scientific state |

The canonical experiment chain is:

```text
Anchor -> protocol.md -> summary.md / summary_cn.md -> detailed.md -> Anchor update
```

Briefs derive from Focus/evidence without question closure. Final reports still
require a researcher-confirmed bounded answer.

## Smallest Update Test

Update the mainline only when the evidence changes an active route, Anchor
evidence, hypothesis, claim boundary, or next decision. Otherwise do not create
another report or status artifact.

Derived views copy only approved statements and exact source links. If they
disagree with an owning artifact, repair or regenerate the view; do not edit the
source to match the view.

## Figures

Keep a figure only when it supports the current verdict, boundary, or next
decision. Curated figures live beside the result records and state their
question, metric and unit, data and aggregation, axes, visible result, allowed
conclusion, and limitation. Debug figures stay outside `summary.md`.

A figure that a date's reader-facing artifact displays also has a reading copy
under `daily_research_reports/MMDD/figures/`, linked by a date-local relative
path and recorded in that directory's `SOURCES.md`. The experiment keeps the
evidence copy; the date copy is derived. Neither is automatically tracked. Select
small deliverable evidence through the payload manifest or include it in a local
reading bundle. See `layout_and_naming.md` for placement and source rules.

## Completion

After an update, check that every decision-bearing statement has one owner,
all dependent views point to it, English and Chinese companions preserve the
same verdict and boundary, and no completed Anchor retains stale result links
or a stale next decision.

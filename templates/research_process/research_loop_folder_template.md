# Research Loop Folder Template

Use this shape for a small mainline experiment or daily sandbox.

```text
00_handwrite_anchor.md
<topic>_anchor.md
protocol.md
summary.md
detailed.md
figures/
tables/
notes/
archive/
```

## File Roles

`00_handwrite_anchor.md`: rough user Thinking Card for AI audit. It should
contain only phenomenon, mechanism guess, key variables, causal relation,
observable metric, alternative explanation, and decision rule. It is not a
full 0-8 anchor.

`<topic>_anchor.md`: compact current-state design. First reading surface is
`Thinking Card`; sections 1-8 are the audit layer. In section 6, each minimal
test should state operational definition, stage-local evidence, and failure
meaning before it becomes protocol-ready.

`protocol.md`: experiment approval surface. Page 1 is `Approval Snapshot`;
later sections hold anchor alignment, conditions, profiling, and nontrivial
algorithm details. Include `Terminology / Definitions` before condition labels,
metrics, method names, or project shorthand are used.

`summary.md`: first post-run reading path. Include only the conclusion,
primary metric, claim boundary, next decision, and central figures needed for
that judgment. Start with what was established, what the experiment shows, and
what we do next. Define condition labels and metric names before using them as
evidence in a `Terminology / Definitions` section.

`detailed.md`: complete evidence ledger with protocol audit, setup, full
results, stage evidence, failure decomposition, debug-only evidence, and
artifact map. Its setup section should define the data, model, objective,
conditions, changed variables, held-fixed variables, seeds/checkpoints, paths,
and known limitations before result labels or plots are used. Keep the fuller
terminology table near the top.

`figures/`: report-ready evidence figures embedded in `summary.md` and
`detailed.md`. Debug-only plots stay in `detailed.md` or a viewer appendix.
Before a new central figure is added, preserve a plot contract: question,
metric definition and unit, data source, aggregation level, axis/legend meaning,
allowed conclusion, and limitation.

`tables/`: curated small tables used by result documents.

`notes/`: scratch material outside the main read path.

`archive/`: superseded probes kept for traceability.

Do not create separate implementation-plan files for new work.

Do not create a parallel `docs/design.md`, `docs/experiment_design.md`, or
`docs/visualization_results.md` tree for normal work. This folder maps those
advisor-spec roles to the local anchor / protocol / summary+detailed chain.
Create `final_report.md` only when a self-contained subproblem is being closed
as a stable synthesis.

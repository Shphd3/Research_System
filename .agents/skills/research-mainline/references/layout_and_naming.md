# Layout And Naming

Use this reference only for artifact placement or reorganization.

## Canonical Layout

```text
Projects/<project>/main/
  roadmap.md
  parking_lot/README.md
  problem_anchors/<line_id>/
    README.md
    <parent_id>_<topic>/
      <parent_id>_<topic>_anchor.md
      <parent_id>_<topic>_anchor_cn.md
      subanchors/<parent_id>_<NN>_<topic>_anchor.md
  experiments/A<line_number>/<anchor_stem>/<experiment_id>/
    protocol.md
    summary.md
    detailed.md
    figures/
    tables/
  stories/<line_id>/
    README.md
    <NN>_<topic>.md
    <NN>_<topic>_cn.md
```

Meeting-cycle files live at:

```text
daily_research_reports/MMDD/focus_<problem>.md
daily_research_reports/MMDD/focus_meeting_<topic>.md
daily_research_reports/MMDD/figures/<figure>.png
daily_research_reports/MMDD/figures/SOURCES.md
```

The Focus uses the date it was first created. Keep `cycle_start` and
`target_meeting` in metadata; do not move a living Focus at midnight.

## Date Figures

Every figure a date's reader-facing artifact references physically lives under
that date's `figures/` directory, and the artifact links it with a date-local
relative path such as `figures/x.png` or `../figures/x.png`. Do not link from a
date directory into `Projects/`, an execution workspace, or an absolute host
path: such a link breaks on archive, on another machine, and in a clone.

Two copies of the same figure are expected, and this is the one place where copy
rather than move is correct:

- the owning experiment's `experiments/A<line>/<experiment_id>/figures/` holds
  the evidence copy beside `summary.md` and `detailed.md`;
- `daily_research_reports/MMDD/figures/` holds the reading copy that this date's
  Focus and meeting material display.

Copy byte-identically and record each source in `figures/SOURCES.md`. When a
figure is regenerated, refresh both copies in the same step. A reading copy
never becomes an independent source: if the two disagree, the experiment copy is
authoritative and the date copy is stale.

`figures/SOURCES.md` has one row per file in the directory:

```text
| File | Origin | Source | SHA256 | Note |
|---|---|---|---|---|
| `x.png` | copy | `Projects/.../figures/x.png` | <sha256 of the reading copy> | <what it shows> |
| `y.png` | generated | `<builder>` from `<input>` | <sha256 of the reading copy> | <how it was built> |
```

`copy` means a byte-identical duplicate of an evidence figure, so its recorded
hash must still equal the source's. `generated` means the figure was produced
directly in this directory from a recorded builder and inputs, so there is no
second copy to compare against. If an evidence source later disappears, keep the
reading copy and keep its source path in the row: the lineage stays readable
even when the source does not.

In this repository the experiment copy usually lives under `Projects/`, which is
outside the root repository's tracked tree, so the date copy is often the only
version-controlled copy. That is a reason to keep the copy, not a reason to
treat it as new evidence.

Use a topic subdirectory only when one date has figures from genuinely different
topics whose filenames would otherwise collide. Debug galleries, unfiltered
render dumps, and per-run figure directories stay in the execution workspace and
are never copied here.

## Anchors

An Anchor name describes a stable question or mechanism, not a date, seed, or
single run. Sibling parent Anchors remain sibling folders even when one depends
on another. Use `subanchors/` only for a child that inherits its parent's
decision question and tests one local clause, rival, repair, robustness check,
or metric guard.

When an external method asks for `design.md`, the Anchor fulfills that role
without renaming or duplication.

## Experiments

In `A<anchor_id>_<topic>`, the number is the primary Anchor ID, not a date.
Use suffixes such as `smoke`, `full`, `followup`, or `ablation` only when they
identify a real experimental role. Put experiments beneath their Anchor family
rather than directly under the line folder.

## Stories And Focuses

Story filenames carry two-digit reading order and subject; English and `_cn`
companions share a stem. Do not create generic new `story.md` files or one
story per Anchor.

One active workstream has one current Focus, one question, and one next
decision. A meeting synthesis exists only when explicitly requested. Important
inactive questions go to the project Parking Lot only when they can change the
future direction and have a reopening condition.

## Migration Check

Move rather than copy. Update the line README and every in-scope project,
story, experiment, and graph reference. Verify that the old path
is absent, every new relative link resolves, and no duplicate canonical file
remains.

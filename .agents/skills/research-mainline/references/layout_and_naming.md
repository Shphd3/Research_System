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
daily_research_reports/MMDD/docs/daily_report_<topic_slug>.md
daily_research_reports/MMDD/focus_meeting_<topic>.md
```

The Focus uses the date it was first created. Keep `cycle_start` and
`target_meeting` in metadata; do not move a living Focus at midnight.

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
story, experiment, daily-report, and graph reference. Verify that the old path
is absent, every new relative link resolves, and no duplicate canonical file
remains.

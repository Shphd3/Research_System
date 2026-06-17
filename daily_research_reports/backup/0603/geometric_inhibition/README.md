# 0603 Geometric Inhibition Sync Package

## Read Order

1. `0501_center_separation_sync.md`
2. `05_report_card.md`
3. `meeting_brief.md`
4. `tables/h0603b_center_only_decision_metrics.csv`
5. `tables/h0603b_center_only_summary_by_seed.csv`

## Scope

This folder syncs the 05_01 result for the group-meeting discussion. The current decision is about whether `slot-init + center separation only` can produce stable slot-aligned routing in uniform multi-B synthetic data.

## Boundary

Here `geometric separation` means `router-center separation only`. It does not include the supervised token-margin / logit-margin conditions C2/C5.

## Included Files

- `0501_center_separation_sync.md`: self-contained sync conclusion for 05_01.
- `05_report_card.md`: advisor-facing report card using the 05_01 report-card structure.
- `meeting_brief.md`: shorter meeting-facing discussion note.
- `figures/`: copied decision figures.
- `tables/`: copied decision tables.

## Excluded

This local sync package does not include raw logs, checkpoints, datasets, full result directories, or 05_02 materials.

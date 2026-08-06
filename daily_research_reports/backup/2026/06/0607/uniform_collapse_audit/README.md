# 0607 Uniform Collapse Audit

## Read Order

1. `meeting_brief_cn.md`
2. `audit_report.md`
3. `theory_iteration.md`
4. `scripts/audit_uniform_data_init_geometry.py`

## Scope

This folder audits why the original uniform feature setting can still show
top-1 MoE routing collapse. It checks data uniformity, router initialization,
hidden common-direction sources, and the random-init plus top-1 lock-in
mechanism.

## Main Conclusion

No data-generation or random-router-initialization bug was found for the
random-init `R*` conditions. The important correction is that "common" here is
not a frequency common component. It is a hidden-state common component:
all feature centroids at the routed pre-target position share a large
position/template direction.

## Included Files

- `meeting_brief_cn.md`: meeting-facing short brief.
- `audit_report.md`: PASS / FAIL / UNCLEAR code-data-init audit.
- `theory_iteration.md`: hypothesis, math model, experiment, updated hypothesis.
- `figures/`: central figures used by the reports.
- `tables/`: generated audit tables.
- `scripts/audit_uniform_data_init_geometry.py`: local diagnostic script.

## Important Boundary

This audit explains a plausible mechanism for collapse and rules out two
simple bug explanations. It does not claim collapse is solved, and it does not
prove utility mismatch because forced-routing utility was not recomputed here.

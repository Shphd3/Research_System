# A06 Numbering / Parking / Reference Audit

Status: audit note before any renaming. Do not use this as a migration plan
until the user approves the direction.

## Conclusion

Do not park or renumber A06_10-A06_13. They have completed summaries,
detailed records, and run/job evidence.

Only A06_14 and A06_15 are parked dependency branches. They already have
parked anchor status and protocol-only experiment folders.

## Evidence Check

| Item | Files present | Result status | Migration judgment |
| --- | --- | --- | --- |
| A06_10 real-DCLM proxy operationalization | anchor, protocol, summary, detailed, figures/tables/log references | supported with boundary; ACP full01 and local full02 recorded | keep as mainline evidence |
| A06_11 real-DCLM proxy-center router init | anchor, protocol, summary, detailed, figures/tables/log references | supported with boundary; ACP full01 and local full02 recorded | keep as mainline evidence |
| A06_12 real-DCLM training preservation | anchor, protocol, summary, detailed, figures/tables/log references | not supported; preservation failure is central evidence | keep as mainline evidence |
| A06_13 failure decomposition | anchor, protocol, summary, detailed | supported bottleneck localization | keep as mainline evidence |
| A06_14 utility binding | parked anchor, conditional protocol only | dependency failed because A06_12 preservation failed | parked |
| A06_15 utility-aware init | parked anchor, conditional protocol only | depends on A06_14 utility signal | parked |

## Why Renumbering A06_10-A06_13 Is Risky

These anchors are referenced as current evidence in:

- `PROJECTS.md`;
- `sync/S000_current_specialization/README.md`;
- `sync/S000_current_specialization/research_lines/06_proxy_preservation_line_cn.md`;
- `Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/research_map.md`;
- `Projects/from-attention-to-search/main/experiments/README.md`;
- `daily_research_reports/0626/meeting/meeting_brief.md`;
- experiment protocols and detailed artifact maps.

Changing their numbers would rewrite executed evidence history and would make
old run names / job ids inconsistent with document names.

## Recommended Structure

Keep chronological IDs stable. Add subseries labels in `research_map.md`
instead of renumbering completed anchors.

Recommended A06 subseries:

| Subseries | Anchors | Meaning |
| --- | --- | --- |
| Common / collapse priors | A06_01-A06_05 | why common components and random geometry can dominate routing |
| Controlled feature reachability | A06_06-A06_09 | synthetic / controlled feature discovery and preservation |
| Real-DCLM proxy bridge | A06_10-A06_13 | real proxy discovery, router bridge, preservation failure, failure localization |
| Parked utility branch | A06_14-A06_15 | utility tests blocked until preservation works |
| Controlled route-relevance and center geometry | A06_16-A06_19 | no-position bridge, route-state selection, margin-centered follow-up |

## If The User Still Wants Physical Folder Parking

Only move A06_14 and A06_15, and keep their original IDs:

```text
problem_anchors/06_geometry_proxy_preservation/parked_utility/06_14_*.md
problem_anchors/06_geometry_proxy_preservation/parked_utility/06_15_*.md

experiments/A06/parked_utility/A06_14_*
experiments/A06/parked_utility/A06_15_*
```

Required reference updates if that move is approved:

- `PROJECTS.md`;
- root sync `S000_current_specialization`;
- A06 `research_map.md`;
- `problem_anchors/README.md`;
- `experiments/README.md`;
- every protocol / detailed artifact map that links to A06_14 or A06_15;
- daily meeting briefs only if they are intended to remain live references.

## Current Recommendation

Do not renumber now. Keep A06_10-A06_13 as executed evidence. Treat A06_14 and
A06_15 as parked in-place unless the user explicitly wants a physical parked
folder.

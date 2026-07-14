# S000 Anchor Index

The project-local anchor tree is the current source of truth:

```text
Projects/from-attention-to-search/main/problem_anchors/
```

## Current Lines

| Line | Current registry | Role |
|---|---|---|
| 05 | `main/problem_anchors/05_failure_mechanism/research_map.md` | Ordinary top-1 failure priors. |
| 06 | `main/problem_anchors/06_geometry_proxy_preservation/research_map.md` | Five-parent primary chain; active anchor is `06_04`. |
| 07 | `main/problem_anchors/07_features_overlap/` | Functional interference/value diagnostics. |
| 11 | `main/problem_anchors/11_informative_future_branch_mechanism/README.md` | Stable objective-level MTP mechanism baseline. |
| 12 | `main/problem_anchors/12_structured_compositional_mtp_workload/README.md` | Structured workload and active causal-use design. |

Paths above are relative to `Projects/from-attention-to-search/`.

## Copied Snapshot Boundary

The existing `sync/S000_current_specialization/anchors/` tree is a historical
copy made before the A06 consolidation and A11/A12 split. It is retained for
provenance, not for current decisions. Current readers must use the registries
above; no full anchor mirror was refreshed in this compact sync.

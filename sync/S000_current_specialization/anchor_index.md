# S000 Anchor Index

The project-local anchor tree is the current source of truth:

```text
Projects/from-attention-to-search/main/problem_anchors/
```

## Current Lines

| Line | Current registry | Role |
|---|---|---|
| 05 | `main/problem_anchors/05_failure_mechanism/research_map.md` | Ordinary top-1 failure priors. |
| 06 | [synchronized A06 registry](anchors/06_geometry_proxy_preservation/research_map.md) -> `main/problem_anchors/06_geometry_proxy_preservation/research_map.md` | Five-parent primary chain; active anchor is `06_04`. |
| 07 | `main/problem_anchors/07_features_overlap/` | Functional interference/value diagnostics. |
| 11 | `main/problem_anchors/11_informative_future_branch_mechanism/README.md` | Stable objective-level MTP mechanism baseline. |
| 12 | `main/problem_anchors/12_structured_compositional_mtp_workload/README.md` | Structured workload and active causal-use design. |

Paths above are relative to `Projects/from-attention-to-search/`.

## Copy Boundary

The full `anchors/` directory is synchronized from the current project-local
anchor tree. It contains all active research lines, parent anchors, subanchors,
Chinese companions, and existing closure reports. Project-local anchors remain
the source of truth; this mirror is the root-sync reading copy.

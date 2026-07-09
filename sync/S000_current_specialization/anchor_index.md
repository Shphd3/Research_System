# S000 Anchor Index

This file records the copied anchor snapshot for the active
feature-level expert-specialization line.

Source of truth:

```text
Projects/from-attention-to-search/main/problem_anchors/
```

Copied snapshot:

```text
sync/S000_current_specialization/anchors/
```

Sync rule:

```text
S000 anchor sync is copy-only and explicit. Update the project-local anchor
tree first, repair source links there, then copy the tree into this folder
when the user asks for S000 sync.
```

## Snapshot

Current copied anchor count: 103.

The removed historical anchor is not copied:

```text
07_high_dim_uniform_expert_geometry_gate_anchor.md
```

Its static expert-geometry experiments now point to:

```text
anchors/06_geometry_proxy_preservation/06_2x2_expert_geometry_gate_anchor.md
```

## Research Lines

| Line | Copied anchor count | Role |
|---|---:|---|
| `00_foundation_definition/` | 2 | Defines feature-level specialization and metric boundaries. |
| `01_common_operator_mechanism/` | 9 | Defines and audits common operators before method construction. |
| `05_failure_mechanism/` | 8 | Explains ordinary top-1 failure mechanisms and early lock-in. |
| `06_geometry_proxy_preservation/` | 42 | Main proxy discovery, initialization, and preservation line. |
| `07_features_overlap/` | 9 | Functional value, common/rare interference, and route-utility binding. |
| `08_real_data_preserved_specialization/` | 11 | Real-data preserved-specialization target line. |
| `09_common_rare_spectral_discrimination/` | 4 | Frequency and common/rare spectral-discrimination line. |
| `10_optimizer_learning_rate_mechanism/` | 4 | Optimizer and critical-learning-rate mechanism support line. |
| `11_long_horizon_mtp_objective/` | 12 | Supporting objective line for long-horizon MTP hidden-state supervision. |

## Reading Order

Start with:

```text
README.md
research_lines/00_overall_current_line_cn.md
anchors/README.md
```

Then read the line-specific folder:

```text
anchors/00_foundation_definition/
anchors/01_common_operator_mechanism/
anchors/05_failure_mechanism/
anchors/06_geometry_proxy_preservation/
anchors/07_features_overlap/
anchors/08_real_data_preserved_specialization/
anchors/09_common_rare_spectral_discrimination/
anchors/10_optimizer_learning_rate_mechanism/
anchors/11_long_horizon_mtp_objective/
stories/11_long_horizon_mtp_objective/story_cn.md
```

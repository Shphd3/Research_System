# Anchor Copies

This folder stores categorized root-sync copies of active project anchors.

The project-local anchor is the source of truth. These copies exist so a
web-side research partner can read the current anchor without entering project
repositories.

## Categories

| Category | Source project | Role |
|---|---|---|
| `expert_specialization/` | `Projects/from-attention-to-search/` | gating, route assignment, and expert causal utility anchors |

## Current Anchor Copies

| Anchor | Source |
|---|---|
| `expert_specialization/00_feature_level_expert_specialization_mainline_anchor.md` | synthesized root-sync mainline from A05/A06/A07 evidence |
| `expert_specialization/01_slot_context_dominance_router_specialization_anchor.md` | `Projects/from-attention-to-search/main/problem_anchors/01_slot_context_dominance_router_specialization_anchor.md` |
| `expert_specialization/02_ntp_style_top1_router_lockin_anchor.md` | `Projects/from-attention-to-search/main/problem_anchors/02_ntp_style_top1_router_lockin_anchor.md` |
| `expert_specialization/03_hierarchical_route_utility_binding_anchor.md` | `Projects/from-attention-to-search/main/problem_anchors/03_hierarchical_route_utility_binding_anchor.md` |

## Update Rule

Do not update these copies automatically when a project-local anchor changes.
Update them only when the user explicitly asks to sync root sync or names a
specific root anchor copy. Before finishing that requested sync, verify that the
source and sync copy are identical.

Current mainline package:

```text
sync/S000_current_specialization/anchors/expert_specialization/00_feature_level_expert_specialization_mainline_anchor.md
```

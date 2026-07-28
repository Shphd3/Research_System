# Research Stories

This folder stores line-level research stories for `from-attention-to-search`.

A story is a living synthesis for one research line. It connects the research
question, physical intuition, mathematical model, theorem state, anchor chain,
experiment evidence, claim boundary, and next decision. It does not replace
anchors, protocols, `summary.md`, or `detailed.md`.

## Active Stories

| Line | Story | Role |
|---|---|---|
| `06_geometry_proxy_preservation` | `06_geometry_proxy_preservation/01_functional_specialization_and_utility_routing.md`, `06_geometry_proxy_preservation/01_functional_specialization_and_utility_routing_cn.md` | Complete A06 story from route-relevant geometry and finite-margin preservation to expert utility, partial-feedback repair, and the real-workload utility-headroom gate. |
| `11_informative_future_branch_mechanism` | `11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary.md`, `11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary_cn.md` | Closed objective-level baseline: informative future signal, shared-parameter reachability, and the boundary between current-state formation and later standard-head use. |
| `12_structured_compositional_mtp_workload` | `12_structured_compositional_mtp_workload/01_structured_composition_workload_and_standard_head_use.md`, `12_structured_compositional_mtp_workload/01_structured_composition_workload_and_standard_head_use_cn.md` | Active workload line: computation-tree definition, depth-two base case, capability gate, controlled rank boundary, and intermediate-state causal-use design. |
| `13_mtp_task_property_decomposition` | `13_mtp_task_property_decomposition/01_task_relevant_relay_supervision.md`, `13_mtp_task_property_decomposition/01_task_relevant_relay_supervision_cn.md` | Relay-property decomposition from the hard-relay sufficient condition to the soft-relay measurement-window blocker. |
| `14_tree_low_rank_language_structure` | `14_tree_low_rank_language_structure/03_ntp_conditional_function_rank.md`, `14_tree_low_rank_language_structure/03_ntp_conditional_function_rank_cn.md` | Current A14 synthesis: probabilistic sparse activation, task-function reuse, the local Jacobian bridge, and the finite secant/path-integrated bridge required for complete training. |

## Sync Rule

When a research line is explicitly synced, sync both:

```text
main/problem_anchors/<line>/
main/stories/<line>/
```

The project-local story remains the source of truth. Root sync may copy it for
external readers only when explicitly requested.

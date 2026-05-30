# Proposed Graph Patch: Do Not Apply Without User Confirmation

Reason:

```text
The mainline next decision appears to move from slot-context strength toward route-function binding / factor attribution / write-in diagnostic.
```

Proposed node:

```yaml
- id: problem.route_function_binding_stable_feature_routing
  type: problem_anchor
  title: Route-Function Binding For Stable Feature Routing
  path: Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/route_function_binding_stable_feature_routing_anchor.md
  parent: problem.moe_expert_specialization
  status: active_proposed
  decision: diagnose routing_interference vs write_in_failure, then test minimal mechanism intervention
```

Proposed experiment node:

```yaml
- id: exp.H0531_route_function_binding_auto_research
  type: experiment
  title: H0531 Route-Function Binding Auto Research
  path: Projects/from-attention-to-search/main/experiments/H0531_route_function_binding_auto_research/summary.md
  anchor: problem.route_function_binding_stable_feature_routing
  status: planned
```

Proposed edge:

```yaml
- from: problem.slot_context_dominance_router_specialization
  to: problem.route_function_binding_stable_feature_routing
  relation: redirects_next_decision_to
  reason: slot visibility is not sufficient; next uncertainty is route-function binding vs write-in failure
```

Do not edit graph automatically unless user confirms.

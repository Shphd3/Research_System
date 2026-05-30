# Graph Update Proposal: 0531 Gating Auto Research

Do not edit graph automatically unless user confirms. This is a proposed navigation update only.

## Proposed Node

```yaml
- id: problem.route_function_binding_stable_gating
  type: problem_anchor
  title: Stable Route-Function Binding For Synthetic Feature Specialization
  path: Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/route_function_binding_stable_gating_anchor.md
  parent: problem.moe_expert_specialization
  status: active
  question: Can a routing/training mechanism bind route assignment to target-deciding feature and expert causal utility under synthetic NTP?
```

## Proposed Experiment Node

```yaml
- id: exp.0531_auto_route_function_binding
  type: experiment
  title: 0531 Auto Route-Function Binding
  path: Projects/from-attention-to-search/main/experiments/0531_auto_route_function_binding/summary.md
  anchor: problem.route_function_binding_stable_gating
  status: planned
  decision_gate: factor attribution -> candidate intervention -> stability
```

## Reason

Current sync says the mainline should redirect toward route-function binding, not context-strength sweeps or hierarchy depth. This node makes that decision explicit without replacing existing anchors.

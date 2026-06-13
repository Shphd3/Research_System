# Research Source Map

This course project derives its technical content from the ongoing MoE gating
specialization work.

## Primary Source Files

```text
Projects/graphs/expert_specialization.graph.yaml
Projects/from-attention-to-search/main/problem_anchors/01_slot_context_dominance_router_specialization_anchor.md
Projects/from-attention-to-search/main/problem_anchors/05_01_geometric_inhibition_anchor.md
Projects/from-attention-to-search/main/problem_anchors/05_02_assignment_binding_anchor.md
```

Useful result records:

```text
Projects/from-attention-to-search/main/experiments/A05_01_feature_key_routing_stability_center_only/summary.md
Projects/from-attention-to-search/main/experiments/A05_01_feature_key_routing_stability_center_only/detailed.md
Projects/from-attention-to-search/main/experiments/A05_01_feature_axis_audit_existing_logs/summary.md
Projects/from-attention-to-search/main/experiments/A05_01_feature_axis_audit_existing_logs/detailed.md
Projects/from-attention-to-search/main/experiments/A05_01_true_token_conditioned_inhibition_replay/summary.md
Projects/from-attention-to-search/main/experiments/A05_01_true_token_conditioned_inhibition_replay/detailed.md
```

## Defensible Current Claim

Observation:

```text
Some conditions produce high same-feature route consistency.
```

Interpretation:

```text
The router can be made stable under a weak feature-key definition, but this
metric alone does not distinguish specialization from collapse or lock-in.
```

Claim:

```text
The current work narrows the problem from "can routes be consistent?" to "can
routes bind to non-collapsed expert utility for an operational feature?"
```

Boundary:

```text
Do not claim that ordinary top-1 MoE naturally forms robust functional
specialization. Do not claim transfer to real-corpus or Zipfian settings yet.
```

Next research decision:

```text
Audit assignment binding and expert composition after fixing the operational
feature axis.
```

## Mainline Impact Gate For Course Writing

```text
affects hypothesis? no
affects claim boundary? yes, by packaging the boundary for course delivery
affects next decision? no
recommendation: pursue as course-delivery packaging, not as a new experiment
```

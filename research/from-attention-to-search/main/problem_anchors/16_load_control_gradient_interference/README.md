# A16 Load Control And Gradient Interference

## Direction Snapshot

- **Root research question:** Can an MoE keep expert load operationally usable while improving how its Router exposes functionally useful information, without slowing language-model learning or preventing expert differentiation?
- **Current answer:** A token-shared Router-input component sustains frozen Vanilla collapse. Centering removes a reproducible effective-LB cost at 50M, but it does not globally reduce LB cost or gradient conflict across 6B/10B states; the source trajectories did not actually apply the configured LB gradient.
- **Current claim boundary:** Existing evidence establishes a frozen routing dependency and an early counterfactual tradeoff, not a long-run harmful-LB mechanism or the superiority of dynamic expert bias.
- **One blocking uncertainty:** After the NLL-only increment branch failed to show a replicated 20B advantage, does direct expert-utility supervision reveal held-out functional information in the part of the same-layer increment not linearly predictable from the old state?
- **Active parent Anchor:** [A16_01 Incremental-Information Routing](16_01_incremental_information_lb_routing/16_01_incremental_information_lb_routing_anchor.md).
- **Why this Anchor is next:** The load-gradient path is now auditable, while fixed covariance bands lack functional admission. A no-op residual branch permits a direct long-run test without deleting the native Router path.
- **Decision dependency chain:** completed LB-gradient audit -> verified differentiable-LB runner -> incremental branch smoke -> four-arm paired 30B endpoint decision.
- **Parked direction:** The A16_00 dynamic-bias/effective-LB/no-controller comparison remains a separate load-controller intervention; it is not answered by A16_01.
- **Exactly one next decision:** execute the approved A16_01_01_E01 two-seed frozen expert-choice-regret gate.
- **Completion criterion:** Conditional-Utility receives a typed Pass/Fail/Insufficient verdict against Native, Raw-Utility, and Conditional-Haar on both registered 10B Native checkpoints.
- **Resume action:** finish implementation and smoke, then run the frozen gate; submit the six 10B-to-30B utility continuations only if that gate passes.

## Parent-Anchor Map

| Parent Anchor | Decision it owns | Depends on | Current state | Direction implication | Primary source |
| --- | --- | --- | --- | --- | --- |
| A16_00 Switch LB Gradient Conflict | Does the differentiable Switch load objective impose a held-out learning cost through conflicting Router/upstream updates? | A15 matched training and the migrated DC sustainer boundary | completed: global Centered-mediation H1 failed; early relief established | Compare dynamic bias with effective LB under Centered | [Anchor](16_00_switch_lb_gradient_conflict/16_00_switch_lb_gradient_conflict_anchor.md) |
| A16_01 Incremental-Information Routing | Under verified differentiable LB, does an explicit same-layer increment branch improve 30B NLL, and does a certified direction beat Haar? | A16_00's differentiability boundary and A15's direction-admission method | approved for implementation, smoke, and eight full jobs | Select practical versus direction-specific incremental routing evidence | [Anchor](16_01_incremental_information_lb_routing/16_01_incremental_information_lb_routing_anchor.md) |

## Reading Index

1. [A16_01 canonical Anchor](16_01_incremental_information_lb_routing/16_01_incremental_information_lb_routing_anchor.md)
2. [A16_01 Chinese Anchor](16_01_incremental_information_lb_routing/16_01_incremental_information_lb_routing_anchor_cn.md)
3. [A16_01_01 conditional-innovation subanchor](16_01_incremental_information_lb_routing/subanchors/16_01_01_regret_distilled_conditional_innovation_anchor.md)
4. [A16_01_01 frozen functional-gate Protocol](../../experiments/A16/A16_01_01_E01_frozen_regret_distillation_gate/protocol.md)
5. [A16_01_01 conditional 30B Protocol](../../experiments/A16/A16_01_01_E02_30b_conditional_innovation_confirmation/protocol.md)
6. [A16_01 original 30B Protocol](../../experiments/A16/A16_01_E01_30b_incremental_information_lb_routing/protocol.md)
7. [A16_00 canonical Anchor](16_00_switch_lb_gradient_conflict/16_00_switch_lb_gradient_conflict_anchor.md)
8. [Migrated DC sustainer subanchor](16_00_switch_lb_gradient_conflict/subanchors/16_00_01_dc_sustainer_boundary_anchor.md)
9. [Completed multistage result](../../experiments/A16/A16_00_02_E01_multistage_gradient_pathway_audit/summary.md)
10. [DC sustainer result](../../experiments/A16/A16_00_01_E01_dc_sustainer_audit/summary.md)
11. [Current line synthesis](../../stories/16_load_control_gradient_interference/01_load_control_gradient_interference_and_resolution.md)

## Ownership Boundary

- A15 retains representation-direction and semantic-certificate conclusions; A16_01 owns only the LB-controlled long-run Router intervention.
- A05 retains general top-1 collapse mechanisms.
- A07 retains common/rare gradient conflict inside expert parameters.
- A16 owns the interaction between the language-model objective and load-control mechanism, plus solution selection after that interaction is measured.

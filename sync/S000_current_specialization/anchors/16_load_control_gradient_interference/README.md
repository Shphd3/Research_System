# A16 Load Control And Gradient Interference

## Direction Snapshot

- **Root research question:** Can an MoE keep expert load operationally usable without letting load control slow language-model learning or prevent useful expert differentiation?
- **Current answer:** A token-shared Router-input component immediately sustains the frozen Vanilla collapse, but its removal is not a complete historical explanation. Whether the differentiable Switch load-balancing objective itself creates harmful optimization interference is not yet established.
- **Current claim boundary:** Existing evidence diagnoses a frozen routing dependency and a hard/soft load-control mismatch; it does not show that the load-balancing gradient reduces held-out learning efficiency.
- **One blocking uncertainty:** On the same global batch and optimizer state, does adding the Switch load-balancing gradient worsen the next-step held-out NLL while improving hard expert load?
- **Active parent Anchor:** [A16_00 Switch LB Gradient Conflict](16_00_switch_lb_gradient_conflict/16_00_switch_lb_gradient_conflict_anchor.md).
- **Why this Anchor is next:** Selecting dynamic expert bias before separating harmful gradient interference from beneficial regularization or ineffective hard-load control would make any later training comparison mechanistically ambiguous.
- **Decision dependency chain:** frozen DC dependency -> paired LM/LB gradient and shadow-update audit -> mechanism-conditioned load-control intervention -> matched training-efficiency test.
- **Parked direction:** Dynamic expert bias is the researcher-approved first intervention only if A16_00 supports harmful gradient interference or hard/soft control mismatch. Balanced assignment and Expert Choice remain structural references because they change the routing problem itself.
- **Exactly one next decision:** after the already approved Vanilla/Centered shadow-step audit, select whether the first load-control intervention should be dynamic expert bias, retained differentiable LB, or a hard/soft-control repair.
- **Completion criterion:** both seeds and both Vanilla/Centered conditions must have valid same-batch gradient decomposition, exact-state shadow updates, held-out NLL effects, and hard-load effects under the frozen verdict rule.
- **Resume action:** freeze the approved A16_00 Protocol in `main/experiments/A16/`, then implement and execute it; do not start dynamic-bias long training first.

## Parent-Anchor Map

| Parent Anchor | Decision it owns | Depends on | Current state | Direction implication | Primary source |
| --- | --- | --- | --- | --- | --- |
| A16_00 Switch LB Gradient Conflict | Does the differentiable Switch load objective impose a held-out learning cost through conflicting Router/upstream updates? | A15 matched training and the migrated DC sustainer boundary | Vanilla and Centered conditions approved for direct Protocol, implementation, smoke, and execution | Select the solution class before any new long training | [Anchor](16_00_switch_lb_gradient_conflict/16_00_switch_lb_gradient_conflict_anchor.md) |

## Reading Index

1. [A16_00 canonical Anchor](16_00_switch_lb_gradient_conflict/16_00_switch_lb_gradient_conflict_anchor.md)
2. [A16_00 Chinese Anchor](16_00_switch_lb_gradient_conflict/16_00_switch_lb_gradient_conflict_anchor_cn.md)
3. [Migrated DC sustainer subanchor](16_00_switch_lb_gradient_conflict/subanchors/16_00_01_dc_sustainer_boundary_anchor.md)
4. [DC sustainer result](/Projects/from-attention-to-search/main/experiments/A16/A16_00_01_E01_dc_sustainer_audit/summary.md)
5. [Current line synthesis](/Projects/from-attention-to-search/main/stories/16_load_control_gradient_interference/01_load_control_gradient_interference_and_resolution.md)

## Ownership Boundary

- A15 retains covariance-band and Relay training conclusions.
- A05 retains general top-1 collapse mechanisms.
- A07 retains common/rare gradient conflict inside expert parameters.
- A16 owns the interaction between the language-model objective and load-control mechanism, plus solution selection after that interaction is measured.

# Thinking Card — Cross-Position Standard-Head Use Boundary Anchor

> Migrated from [11_03_cross_position_standard_head_use_boundary_anchor.md](11_03_cross_position_standard_head_use_boundary_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** MTP can create a task-useful direction at the current state without improving the standard answer one token later.

**Mechanism guess:** Use requires transport through the intervening token. The cross-position Jacobian can rotate a useful direction into an adverse one even when changing the output head does not.

**Observable metric:** standard-head usefulness before and after the state transition, followed by a conservative held-out behavioral score.

**Decision:** current-state formation is not sufficient for standard-head benefit; stop enumerating bridge tokens or training lengths on this proxy.

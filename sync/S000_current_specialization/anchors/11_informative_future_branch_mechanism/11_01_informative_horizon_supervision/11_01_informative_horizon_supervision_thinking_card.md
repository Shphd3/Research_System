# Thinking Card — Informative-Horizon Supervision Anchor

> Migrated from [11_01_informative_horizon_supervision_anchor.md](11_01_informative_horizon_supervision_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** Predicting more future tokens sometimes creates an earlier semantic signal, but increasing the horizon alone does not reliably help.

**Mechanism guess:** A future target affects the current state only when it contains task information not already determined by the matched local context. The first-order effect is the vector sum of the centered output directions of all such covered targets.

**Observable metric:** hidden semantic velocity, the one-step movement of the current state toward the task-correct output direction.

**Decision:** close the question of when direct current-state supervision appears; do not use larger horizon length itself as the explanation.

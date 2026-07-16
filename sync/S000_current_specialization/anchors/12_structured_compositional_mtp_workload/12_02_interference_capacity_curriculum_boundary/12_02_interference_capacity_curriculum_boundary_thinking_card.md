# Thinking Card — Interference, Capacity, And Curriculum Boundary Anchor

> Migrated from [12_02_interference_capacity_curriculum_boundary_anchor.md](12_02_interference_capacity_curriculum_boundary_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** Extra future supervision can improve the future factor while worsening the standard objective in a limited shared representation.

**Mechanism guess:** The local effect is governed by gradient interaction, while a persistent tradeoff can be caused by insufficient task-relevant representation rank. A training schedule cannot create a missing independent direction.

**Observable metric:** standard-objective loss gap under a controlled rank intervention, with future-factor error as the benefit guard.

**Decision:** structural rank competition is a sufficient mechanism in the linear model; curriculum is not a structural-rank repair; do not infer a Transformer scale law yet.

# Thinking Card — Ground-Truth Common Projector Recovery Anchor

> Migrated from [01_02_ground_truth_projector_recovery_anchor.md](01_02_ground_truth_projector_recovery_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** Real-DCLM has no known $P_c^*$, so common estimator validity
cannot be judged directly from real hidden states.

**Mechanism guess:** If an estimator cannot recover a known common subspace in
a controlled setting with nuisance, imbalance, and residual entanglement, it
should not be used as a real-DCLM common operator.

**Key variables:** True projector $P_c^*$, candidate projector $\hat P$,
common strength, unique strength, group imbalance, common/residual angle,
feedback drift, and subspace recovery alignment.

**Causal relation:** Estimator validity should be tested against known common
subspace before the estimator is used to interpret real-DCLM preservation or
MoE specialization.

**Observable metric:** `subspace_alignment = ||U_c^T \hat U_c||_F^2 / k`.

**Rival Explanations:** Estimators may recover only high-variance directions,
only mean offsets, or only task-specific gradient directions rather than true
common structure.

**Decision:** If one estimator recovers $P_c^*$ across nuisance regimes and
passes gradient/loss guards, promote it to the next mechanism test. If
estimators succeed in different regimes, keep common as an operator family.

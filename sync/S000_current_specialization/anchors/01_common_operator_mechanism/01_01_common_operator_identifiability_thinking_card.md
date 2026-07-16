# Thinking Card — Common Operator Identifiability Anchor

> Migrated from [01_01_common_operator_identifiability_anchor.md](01_01_common_operator_identifiability_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** Common components affect routing, rare/common conflict, and
early training preservation, but PCA, mean, centering, route-logit contrast,
and gradient-based estimators can name different directions.

**Mechanism guess:** A common operator is not identifiable from hidden-state
geometry and next-token loss alone. It must be defined relative to a mechanism
criterion such as shared-prediction causality, cross-group gradient redundancy,
or proxy-preservation feedback.

**Key variables:** Hidden state $h$, group label $g$, candidate projector $P$,
shared loss $L_c$, rare/group loss $L_r$, group gradient $G_g$, and criterion
rankings across estimator families.

**Causal relation:** If common is criterion-dependent, then the estimator that
best explains activation variance need not be the estimator that best reduces
gradient redundancy or preserves route information.

**Observable metric:** `criterion_winner_diversity`, the number of distinct
estimator families that win across recovery, shared-loss sensitivity, and
gradient-overlap reduction criteria.

**Rival Explanations:** A single hidden-state top direction may dominate every
criterion; estimator disagreement may be caused only by noise or invalid group
labels; gradient criteria may measure update scale rather than common
structure.

**Decision:** If multiple estimator families win different mechanism criteria
in a controlled full run, pursue common as a mechanism-conditioned operator
family. If one estimator wins all criteria across regimes, revise toward a
single common operator route.

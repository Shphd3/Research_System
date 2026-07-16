# Thinking Card — Gradient Common Versus Activation Common Anchor

> Migrated from [01_03_gradient_common_vs_activation_common_anchor.md](01_03_gradient_common_vs_activation_common_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** Activation top directions can be strong, stable, and visually
"common", but they may not be the directions that create cross-group
optimization interference.

**Mechanism guess:** Optimization-relevant common is closer to the intersection
of group-conditioned gradient outer products than to the top eigenspace of
hidden-state covariance.

**Key variables:** Hidden state $h$, group label $g$, activation covariance
$C_h$, group gradient $G_g$, activation projector $P_{\mathrm{act}}$,
gradient-intersection projector $P_{\mathrm{grad}}$, shared target loss $L_c$,
and gradient-overlap reduction.

**Causal relation:** If gradient common is the optimization object, removing
$P_{\mathrm{grad}}h$ should reduce cross-group gradient overlap more than
removing $P_{\mathrm{act}}h$, especially when high-variance activation
directions are nuisance or unique directions.

**Observable metric:** `gradient_overlap_reduction_advantage`, defined as
gradient-overlap reduction from $P_{\mathrm{grad}}$ minus that from
$P_{\mathrm{act}}$.

**Rival Explanations:** Activation PCA may already capture the same common
object; gradient intersection may only track target scale; estimator
disagreement may disappear when shared-prediction loss is guarded.

**Decision:** If $P_{\mathrm{grad}}$ consistently beats $P_{\mathrm{act}}$ on
gradient-overlap reduction in activation-gradient mismatch regimes, carry
gradient common into the next functional/feedback bridge. If not, revise the
optimization-common hypothesis.

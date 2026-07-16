# Thinking Card — A07_06 Projected Common / Rare Conflict Splitting Anchor

> Migrated from [07_06_projected_common_rare_conflict_splitting_anchor.md](07_06_projected_common_rare_conflict_splitting_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** In A07_04, neural common/rare gradient conflict is measurable,
but centered unsupervised routing only weakly reduces conflict and does not beat
dense shared training on rare loss.

**Mechanism guess:** The router split may be too weak because frequent common
updates keep dominating shared experts. Their repeated update pressure can
dilute or overwrite the rare conflict gradient before the rare feature has
enough update mass to form a stable complementary direction.

**Key variables:** common feature $C$, rare feature $R$, frozen common
projector $P_C$, preconditioned update $u_t$, rare common-subspace fraction
$\alpha_R^C$, routing-weighted conflict $\mathcal{C}_{C,R}$, rare loss $L_R$,
and common loss $L_C$.

**Causal relation:** If rare conflict gradients are being diluted by frequent
common updates, then isolating the harmful common/rare conflict component, not
all common information, should reduce common/rare conflict and improve rare
loss without damaging common loss.

**Observable metric:** Primary metric is conflict reduction
$\Delta\mathcal{C}_{C,R}$, with rare-loss improvement versus dense shared as a
required strong guard. The diagnostic gate is rare update mass in the conflict
subspace above shuffled controls with stable raw-gradient and AdamW-update
projectors.

**Alternative explanations:** Rare failure may come from insufficient rare
data, capacity, unstable routing, bad proxy labels, load imbalance, dense model
advantage, or conflict not actually being concentrated in the common subspace.

**Decision:** Run the diagnostic protocol first. Pursue projected MoE only if a
stable conflict projector explains rare update absorption above controls.
Revise or park if projection lowers overlap but does not beat dense rare loss.

# Thinking Card — A07_02 Nested Tail Common-Subspace Control Anchor

> Migrated from [07_02_common_controlled_rare_interference_anchor.md](07_02_common_controlled_rare_interference_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** After the common backbone forms, rare nested child features may keep updating through the same high-gain common subspace.

**Mechanism guess:** Harmful interference occurs when tail updates are dominated by $P_C$ and this prevents child-specific directions from being learned.

**Key variables:** frozen common projector $P_C$, tail update direction $u_{\mathrm{tail}}$, update fraction $\alpha_{\mathrm{tail}}$, tail loss, common loss.

**Causal relation:** stable high-gain $P_C$ -> tail update concentration in $P_C$ -> child-specific learning is delayed; suppressing the $P_C$ component should reduce tail loss without damaging $A$.

**Observable metric:** tail loss improvement under common-subspace-suppressed updates, with reduced $\alpha_{\mathrm{tail}}$ as the mechanism guard.

**Alternative explanation:** any tail improvement may come from confidence capping, more regularization, easier optimization, or capacity rather than subspace control.

**Decision:** supported on the controlled rank-one nested surface; use as mechanism evidence, but do not promote to real MoE utility before A06 preservation.

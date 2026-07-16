# Thinking Card — A07_05: Common-Update Interference Diagnostic

> Migrated from [07_05_common_update_interference_diagnostic_anchor.md](07_05_common_update_interference_diagnostic_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** Rare or conflict examples may stay hard after common patterns
are learned. One possible reason is that rare updates reuse directions already
dominated by common examples.

**Mechanism guess:** Common examples create a stable update subspace. Rare
examples then project into that subspace, and common updates can push parameters
in a direction that hurts rare loss.

**Key variables:** common examples, rare/conflict examples, common-update
projector $P_C$, rare update $u_R$, rare common-update fraction
$\alpha_R^C$, common-to-rare loss effect $\Delta L_{R|C}$.

**Causal relation:** If common-update interference is real, rare updates should
have elevated projection into the common subspace, and applying a common update
should increase rare loss more than matched controls.

**Observable metric:** primary metric is
`common_to_rare_loss_effect`; `rare_common_update_fraction` and a gated
real-data observational bridge are diagnostic guards.

**Alternative explanation:** Rare failure may come from data scarcity, capacity,
label noise, unstable routing, or a bad rare validation surface rather than
common-update interference.

**Decision:** Pursue A07 utility only if common updates causally damage rare
loss on a controlled nested-conflict surface. After that pass, run a small
real-data observational bridge before promoting a partition-value anchor. Revise
if overlap is high but not harmful. Park if rare failure is explained by data,
capacity, or measurement noise.

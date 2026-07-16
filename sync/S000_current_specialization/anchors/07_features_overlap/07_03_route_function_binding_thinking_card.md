# Thinking Card — A07_03 Nested Route-Function Binding Anchor

> Migrated from [07_03_route_function_binding_anchor.md](07_03_route_function_binding_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** Even if routing separates nested levels, experts may still be functionally interchangeable.

**Mechanism guess:** A useful MoE partition should bind routed experts to child-specific computations, not merely balance load or preserve labels.

**Key variables:** nested level, route distribution $P(e\mid \ell)$, forced-route loss, fixed-route ablation damage, tail loss.

**Causal relation:** if routing carries real function, forcing a level through its routed expert should help that level, and ablating that expert under fixed routing should selectively hurt it.

**Observable metric:** fixed-route ablation selectivity for nested child levels.

**Alternative explanation:** route purity may reflect frequency, token identity, initialization, or load balance without expert-side function.

**Decision:** diagnostic positive control passed, but real MoE utility remains parked until A06 route preservation is solved.

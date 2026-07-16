# Thinking Card — A07 Nested Singular Interference Mainline Anchor

> Migrated from [07.md](07.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** Language features are nested: $A -> AB -> ABC -> ABCD$. Frequent parent features may become stable high-gain channels before rare child features are learned.

**Mechanism guess:** Cross-entropy first discovers useful singular directions, then keeps increasing their gains. Frequent parent features therefore create a common high-gain subspace. Rare child features may reuse it efficiently or be trapped by it.

**Key variables:** nested level, feature frequency, common projector $P_C$, singular gain $S_C$, subspace drift $\delta_C$, tail update fraction $\alpha_{\mathrm{tail}}$, tail loss.

**Causal relation:** high parent frequency -> early stable common direction -> late singular-gain growth -> tail updates concentrate in $P_C$ -> tail learning improves if reuse is useful, or stalls if reuse becomes interference.

**Observable metric:** the first reproduction metric is stable common subspace with continuing gain growth after warmup.

**Alternative explanation:** tail failure may come from too little data, insufficient capacity, bad target construction, or independent rare markers rather than common-subspace interference.

**Decision:** controlled nested reproduction and update-control passed; real MoE utility remains gated by A06 route preservation.

# Thinking Card — A07_01 Nested Common Backbone Reproduction Anchor

> Migrated from [07_01_common_rare_conflict_metric_audit_anchor.md](07_01_common_rare_conflict_metric_audit_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** In nested language-like data, common parent features may be learned before rare child features.

**Mechanism guess:** Standard CE/AdamW first aligns a singular direction to the common parent, then keeps increasing its gain after the direction stabilizes.

**Key variables:** nested level, frequency, common projector $P_C$, subspace drift $\delta_C$, common singular energy $S_C$, common and tail accuracy.

**Causal relation:** high $A$ frequency -> early parent accuracy -> stable $P_C$ -> late growth of $S_C$.

**Observable metric:** two-phase common-backbone signature: stable $P_C$ with continuing $S_C$ growth after common warmup.

**Alternative explanation:** the benchmark may be solved by token shortcuts, independent labels, or capacity memorization rather than nested parent reuse.

**Decision:** supported on the controlled rank-one nested surface; use it as the A07_02 gate, but do not generalize to wide transformers or real language.

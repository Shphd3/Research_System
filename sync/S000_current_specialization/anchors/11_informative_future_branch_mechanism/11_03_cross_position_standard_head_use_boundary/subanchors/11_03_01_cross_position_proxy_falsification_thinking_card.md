# Thinking Card — Cross-Position Proxy Falsification

> Migrated from [11_03_01_cross_position_proxy_falsification_anchor.md](11_03_01_cross_position_proxy_falsification_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** The branch variable is useful at the decision state but not at the later state used by the ordinary next-token head.
**Mechanism guess:** the intervening state transition rotates or suppresses the useful direction.
**Key variables:** state position, output-head identity, intervening token, held-out standard-head behavior.
**Causal relation:** hold the extra-loss direction fixed, vary head and position, then require any local gain to survive a behavioral test.
**Observable metric:** position-by-head usefulness followed by held-out standard-head gain.
**Rival explanations:** wrong auxiliary head; one special bridge token; insufficient training duration.
**Decision:** close these proxy variants because none establishes stable use.

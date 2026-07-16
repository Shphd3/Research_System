# Thinking Card — Shared-Parameter Reachability And Background-Sign Control

> Migrated from [11_02_01_reachability_and_background_sign_anchor.md](11_02_01_reachability_and_background_sign_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** A useful hidden-state gradient may fail to move trainable shared parameters in the same direction.
**Mechanism guess:** the encoder Jacobian controls reachability, while all other token losses add signed background pressure.
**Key variables:** direct path velocity, later NTP path velocity, background velocity, total velocity.
**Causal relation:** decompose one shared-parameter update and compare predicted with observed margin change.
**Observable metric:** parameter semantic velocity.
**Rival explanations:** fixed-head artifact; universally positive all-position transfer.
**Decision:** retain conditional reachability and signed background as the complete local conclusion.

# Thinking Card — A09_01 Common High-Gain Band / Rare Discrimination Anchor

> Migrated from [09_01_common_band_rare_discrimination_anchor.md](09_01_common_band_rare_discrimination_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** Common features can form high-gain directions. Rare information may still exist, but prediction can be dominated by the common direction.

**Mechanism guess:** The high-gain band contributes much of the score, but not necessarily the correct discrimination. The rare residual band is smaller, but may better separate the correct target from a common distractor.

**Key variables:** High-gain band, residual band, correct target, common distractor, rare loss, MoE split.

**Causal relation:** A large but weakly discriminative common band raises common distractor scores and suppresses rare-correct targets. A useful MoE split should reduce this mismatch.

**Observable metric:** Mismatch gap: high-gain score share minus high-gain discrimination share.

**Rival explanations:** Rare loss improvement may come from capacity, random splitting, load changes, or regularization rather than common/rare specialization.

**Decision:** Continue this mechanism only if the MoE split both lowers the mismatch gap and improves rare loss. Otherwise, park the method claim and keep the diagnostic.

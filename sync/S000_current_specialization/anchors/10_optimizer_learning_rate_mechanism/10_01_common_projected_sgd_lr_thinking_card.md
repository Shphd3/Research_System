# Thinking Card — 10_01 Common-Projected SGD Learning-Rate Anchor

> Migrated from [10_01_common_projected_sgd_lr_anchor.md](10_01_common_projected_sgd_lr_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** In LLM pretraining, SGD-style updates without adaptive normalization can use a much smaller effective learning rate than Adam. The seminar materials identify large-learning-rate SGD failures through loud layers and output-token classes with very uneven gradient norms.

**Mechanism guess:** The output-head gradient contains a batch-level common input direction. This common direction consumes update energy and amplifies frequent-token directions. Projecting out that common-gradient component should increase the stable SGD learning-rate ceiling without worsening rare-token learning.

**Key variables:** common gradient $G_c$, common-projected gradient $G_r$, critical learning rate $\eta_{\mathrm{crit}}$, rare-token loss, and rare-token update share.

**Causal relation:** A stronger common gradient creates a louder instability direction for vanilla SGD; removing that direction should increase the stable learning-rate ceiling.

**Observable metric:** The primary metric is $\eta_{\mathrm{crit}}(\mathrm{common\text{-}projected\ SGD}) / \eta_{\mathrm{crit}}(\mathrm{vanilla\ SGD})$.

**Rival Explanations:** Any improvement may come from gradient-norm shrinkage, random projection, or implicit token reweighting. The common direction may also carry necessary signal for rare-token learning.

**Decision:** If the synthetic output-head test shows at least a 3x critical-learning-rate increase, controls cannot explain it, and rare-token loss does not worsen, continue to small-real LM and Adam/Nesterov diagnostics. Otherwise revise or park this mechanism.

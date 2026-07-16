# Thinking Card — 10_02 Frequency-Singular SGD Instability Anchor

> Migrated from [10_02_frequency_singular_sgd_instability_anchor.md](10_02_frequency_singular_sgd_instability_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** High-learning-rate SGD in language-model-like training can fail after common tokens or common prefixes have already become easy. The 0701 design asks whether this is caused by frequency-shaped spectral amplification rather than by an optimizer artifact alone.

**Mechanism guess:** Zipfian prefix frequency creates coherent common-feature gradients. Those gradients grow a small number of high-gain singular directions in the output-facing matrix. Later or rarer prefix extensions partly reuse that same subspace. A large global SGD step is then unstable because the amplified modes dominate the logit movement.

**Key variables:** token frequency, common-prefix accuracy, rare-prefix accuracy, output-head top singular value, top spectral-band gradient mass $B_{\mathrm{top}}(G)$, extra-feature effective rank, extra-feature top-$k$ mass, and instability step.

**Causal relation:** Zipfian frequency -> common-feature gradient coherence -> singular-value growth -> later-feature projection into the top subspace -> high-learning-rate SGD instability localized to that subspace.

**Observable metric:** The primary metric is whether the first high-learning-rate SGD instability event is spectrally localized after measurable common-feature learning and singular concentration.

**Rival explanations:** Instability may be uniform curvature, finite-batch noise, attention dynamics, LayerNorm dynamics, or pure output-column norm imbalance without singular concentration. Stabilizing interventions may work only by shrinking update norms.

**Decision:** The first controlled run supports a narrower rare-suppression mechanism but not the full late-instability claim. Continue with an LR/noise boundary map before making a high-LR divergence claim.

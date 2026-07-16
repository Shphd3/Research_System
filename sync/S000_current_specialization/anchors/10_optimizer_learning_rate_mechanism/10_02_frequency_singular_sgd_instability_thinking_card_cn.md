# Thinking Card — 10_02 频率驱动的奇异值放大与 SGD 不稳定 Anchor

> Migrated from [10_02_frequency_singular_sgd_instability_anchor_cn.md](10_02_frequency_singular_sgd_instability_anchor_cn.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**现象：** 在类似语言模型的训练里，大学习率 SGD 可能在 common token / common prefix 已经学会之后发生不稳定。0701 design 关心的不是“哪个 optimizer 赢”，而是这种不稳定是否来自频率塑造出的谱方向放大。

**机制猜测：** Zipfian prefix 频率会产生反复一致的 common-feature 梯度；这些梯度会让输出头少数奇异方向变成高增益方向；后续 rare prefix extension 又部分复用这个子空间；全局 SGD 学习率太大时，更新首先在这些放大方向上失控。

**关键变量：** token frequency、common-prefix accuracy、rare-prefix accuracy、输出头 top singular value、top spectral-band gradient mass $B_{\mathrm{top}}(G)$、extra-feature effective rank、extra-feature top-$k$ mass、instability step。

**因果关系：** Zipfian frequency -> common-feature gradient coherence -> singular-value growth -> later-feature projection into top subspace -> high-learning-rate SGD instability localized to that subspace。

**可观测指标：** 主指标是高 LR SGD 的第一次不稳定事件是否发生在 common 学会和奇异谱集中之后，并且是否局部化在 top 谱带。

**竞争解释：** 不稳定可能来自均匀曲率、mini-batch noise、attention dynamics、LayerNorm dynamics，或者只是 output token column norm imbalance；稳定化干预也可能只是缩小了更新范数。

**决策：** 第一轮 controlled run 支持更窄的 rare suppression 机制，但不支持完整 late-instability claim。下一步应做 LR/noise boundary map，再判断是否能 claim 高 LR divergence 的根因。

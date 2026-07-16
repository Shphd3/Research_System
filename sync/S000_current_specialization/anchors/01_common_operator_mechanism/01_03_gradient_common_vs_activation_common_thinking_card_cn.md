# Thinking Card — 01_03 Anchor：Gradient Common vs Activation Common

> Migrated from [01_03_gradient_common_vs_activation_common_anchor_cn.md](01_03_gradient_common_vs_activation_common_anchor_cn.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon：** activation top direction 很强、很稳定、看起来像 common，但它不一定是造成跨 group 优化干扰的 common。

**Mechanism guess：** optimization-relevant common 更接近 group-conditioned gradient outer product 的交集，而不是 hidden covariance 的 top eigenspace。

**Key variables：** hidden state $h$，group label $g$，activation covariance $C_h$，group gradient $G_g$，activation projector $P_{\mathrm{act}}$，gradient-intersection projector $P_{\mathrm{grad}}$，shared target loss $L_c$，gradient-overlap reduction。

**Causal relation：** 如果 gradient common 才是优化对象，那么移除 $P_{\mathrm{grad}}h$ 应该比移除 $P_{\mathrm{act}}h$ 更能降低跨 group 梯度重叠，尤其是在高方差 activation 方向是 nuisance 或 unique direction 时。

**Observable metric：** `gradient_overlap_reduction_advantage`，定义为 $P_{\mathrm{grad}}$ 的 gradient-overlap reduction 减去 $P_{\mathrm{act}}$ 的 gradient-overlap reduction。

**Rival Explanations：** activation PCA 可能已经抓到了同一个 common；gradient intersection 可能只是 target scale；加入 shared-loss guard 后 estimator 差异可能消失。

**Decision：** 如果 $P_{\mathrm{grad}}$ 在 activation-gradient mismatch regimes 中稳定胜过 $P_{\mathrm{act}}$，下一步把 gradient common 带入 functional/feedback bridge；否则回头审计 optimization-common 假设。

# Thinking Card — 10_01 公共投影 SGD 学习率 Anchor

> Migrated from [10_01_common_projected_sgd_lr_anchor_cn.md](10_01_common_projected_sgd_lr_anchor_cn.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** 在 LLM 预训练中，不带自适应归一化的 SGD-style update 可用学习率远小于 Adam；seminar 材料显示大学习率 SGD 往往先被少数层或输出 token 类的巨大梯度触发不稳定。

**Mechanism guess:** 输出层梯度里存在跨样本共享的公共方向。这个公共方向吸收大量更新能量并放大 frequent-token 方向；如果把这部分公共梯度投掉，SGD 的临界学习率应变大，rare-token 相关更新不应变差。

**Key variables:** 公共梯度 $G_c$，公共投影后梯度 $G_r$，临界学习率 $\eta_{\mathrm{crit}}$，rare-token loss，rare-token 更新占比。

**Causal relation:** 公共梯度越强，vanilla SGD 越容易在 loud direction 上不稳定；公共投影后，稳定学习率上界应提高。

**Observable metric:** 主指标是 $\eta_{\mathrm{crit}}(\mathrm{common\text{-}projected\ SGD}) / \eta_{\mathrm{crit}}(\mathrm{vanilla\ SGD})$。

**Rival Explanations:** 提升可能只是总梯度范数变小、随机投影、或 token reweighting 的效果；也可能是公共方向本身包含必要学习信号，投掉后 loss 变差。

**Decision:** 若合成 output-head 测试中公共投影 SGD 的临界学习率提升至少 3x，且 norm-matched 与 random-projected controls 不能解释，同时 rare loss 不恶化，则进入 small-real LM / Adam / Nesterov 诊断；否则修改或暂停该机制。

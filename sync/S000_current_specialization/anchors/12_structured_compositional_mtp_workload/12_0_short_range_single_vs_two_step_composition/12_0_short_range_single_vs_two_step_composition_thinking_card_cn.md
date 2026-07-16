# Thinking Card — Anchor 12_0：短程单步与短程两步组合

> Migrated from [12_0_short_range_single_vs_two_step_composition_anchor_cn.md](12_0_short_range_single_vs_two_step_composition_anchor_cn.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**现象：** E02 的固定有限规则表可以被记忆，而且正向结果只出现在精确拟合尾部。现在真正要解释的是：当每个样本都现场生成新的局部关系图，答案分别需要一步或两步有序关系计算时，MTP 是否比 NTP 更早让标准主头达到同一掌握水平。

**机制猜测：** 标准 $K=2$ 第二预测头让最终答案在 `DECIDE` 位置直接获得监督，该位置比 `ANSWER_Y` 早两个词元。两步样本需要先得到中间状态再应用第二条关系，因此这条提前答案监督可能比在单步查找中更有帮助。

**关键变量：** 任务组合深度 $c\in\{1,2\}$、训练目标 $o\in\{\mathrm{NTP},\mathrm{MTP}\}$、分别取得资格的模型层数 $d\in\{2,4\}$，以及只由 NTP 校准冻结的任务载体和掌握阈值。

**待检验关系：** 在不查看 MTP 结果的前提下冻结任务载体、合格模型规模和准确率阈值后，MTP 相对 NTP 减少的达阈值步数是否在两步任务中更大。

**主要观测量：** 公共标准下一词元主头在完全独立、现场生成的测试图上首次达到同一冻结准确率阈值的优化步数。

**竞争解释：** 额外全位置损失的一般作用、更大梯度剂量、对语法或随机事实词元的预测收益而非组合收益、残余任务难度差异、容量地板或天花板，以及以优化步而非真实计算量衡量效率。

**决策：** 先只用 NTP 选择“能够稳定学会但不会立即饱和”的新图任务；在任何 MTP 结果产生前冻结生成器、合格模型规模、准确率阈值、种子和预算。正式阶段若任一目标未通过能力门槛，则停止，不解释组合机制。

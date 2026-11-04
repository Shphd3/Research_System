# 方法参考：《Towards Monosemanticity》与句内 feature 关系

状态：当前只完成设计与资产可行性核查；H1、H2 均为 `NOT RUN`。
来源：Bricken 等，Anthropic，2023，*Towards Monosemanticity: Decomposing Language Models With Dictionary Learning*。研究者已明确指定这篇论文。以下官方章节锚点已于 2026-10-28 对照原始 HTML 核实。

## 原论文提供了什么

论文的[“有限状态自动机”章节](https://transformer-circuits.pub/2023/monosemantic-features/index.html#phenomenology-fsa)讨论通过预测 token 联系起来的 feature 组合，包括自循环和交替出现，并将其与通常的模型内部回路区分。

[敏感性示例](https://transformer-circuits.pub/2023/monosemantic-features/index.html#feature-arabic-sensitivity)展示相关 feature 在不同 token 上响应。[Feature splitting](https://transformer-circuits.pub/2023/monosemantic-features/index.html#phenomenology-feature-splitting)指不同字典规模之间的分化与合并，关系不一定是树。[不同激活区间](https://transformer-circuits.pub/2023/monosemantic-features/index.html#global-analysis-interp-intervals)的可解释性也可能不同。论文还区分[数据相关性与模型性质](https://transformer-circuits.pub/2023/monosemantic-features/index.html#global-analysis-about-model)。

## 本轮如何借用

以下是针对当前问题的分析设计，不应写成原论文已经验证过的方法。

1. **借用“延续与轮替”的区分，形成 H1/H2。** H1 看同一个原生 feature 坐标是否在后续 token 再次出现。H2 看先前坐标不再出现时，是否仍可通过独立存在的旧图找到关联坐标。保留环与双向边；token 位置和节点度数都不能提供语义层级。
2. **把观测顺序与功能解释分开。** 缓存能显示“前位置 feature—后位置 token—后位置 feature”的测量序列。本轮不测前一个 feature 是否改变后一个 token 的概率，也不测它是否造成后续 feature 激活。不因此新增输出干预或功能实验。
3. **解释 feature 时读完整句子。** 数学、生物示例都显示全部 token，并列出所画 feature 的编号、激活值、token ID、位置和未展示数量。同时阅读支持例子与反例。“数学背景”这样的名称仍是解释，除非已有独立证据支持。
4. **将激活强度与是否延续分开。** 主统计沿用原生激活规则和预先固定的频率分组。热图使用缓存强度辅助阅读；不能因为弱激活看起来不好解释而临时调阈值。CrossCoder 的共享潜变量不等于每层分别激活。
5. **由背景对照承担统计判断。** 同领域不同文档匹配、保留边际计数的随机化用于处理本轮竞争解释；图覆盖还检查节点度数。这些是本轮设计，原论文没有替我们确定匹配规则、阈值或显著性依据。

## 不能由此得出的结论

即使结果为正，也只支持既定对照下的句内坐标延续或旧图关联，不能证明信息完整保留、因果回路、语义抽象或层级。不同字典规模之间的 feature splitting 不能改称句内 feature 替换。原论文提供值得检查的现象，并未验证我们缓存和旧图中的 feature 身份或含义。

## 简要对照：Cunningham 等（2023）

*Sparse Autoencoders Find Highly Interpretable Features in Language Models* 研究稀疏字典能否提供可解释、对行为有作用的分析单位。[第 3 节](https://arxiv.org/html/2309.08600v2#S3)根据激活文本生成解释，再用其他文本检查解释能否预测激活。[第 4 节](https://arxiv.org/html/2309.08600v2#S4)在间接宾语识别任务中替换反事实 feature 激活。[第 5.3 节](https://arxiv.org/html/2309.08600v2#S5.SS3)通过消融上游 feature、测量下游激活变化来构建关系示例。因此，那里的箭头具有干预含义。本轮可以借用“激活解释与功能检验分开”的思路；后者仍不在缓存分析范围内。

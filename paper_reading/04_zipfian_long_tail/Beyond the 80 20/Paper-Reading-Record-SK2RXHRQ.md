# Paper Reading Record

## Why I Read This

我读它是为了理解：

## My Mainline Anchor

它可能和我的研究主线关系是：sparse attention就是从full kv cache中retrieve 足够重要，信息足够干净的tokens用于attention的计算，这种情况下，如何选择这些tokens是一个很重要的问题。

## One Question Before Reading

我读这篇 paper 先只想回答一个问题：

如何选择sparse attention中的用于kv cache的部分。

## Do Not Overclaim

这篇 paper 的结论不能直接替代我自己的实验结论；它只能更新我的问题、假设、建模、实验设计或解释边界。

***

## First Pass

### Problem

论文想解决什么问题：

想解决的问题是更深入地<span class="highlight" data-annotation="%7B%22attachmentURI%22%3A%22http%3A%2F%2Fzotero.org%2Fusers%2F14440515%2Fitems%2FC4BXIZ6M%22%2C%22pageLabel%22%3A%221%22%2C%22position%22%3A%7B%22pageIndex%22%3A0%2C%22rects%22%3A%5B%5B106.732%2C594.7565468%2C327.6405006279999%2C604.3405680000001%5D%5D%7D%2C%22citationItem%22%3A%7B%22uris%22%3A%5B%22http%3A%2F%2Fzotero.org%2Fusers%2F14440515%2Fitems%2FNSWGJTIW%22%5D%2C%22locator%22%3A%221%22%7D%7D" ztype="zhighlight"><a href="zotero://open/library/items/C4BXIZ6M?page=1">“Reinforcement Learning with Verifiable Rewards”</a></span> <span class="citation" data-citation="%7B%22citationItems%22%3A%5B%7B%22uris%22%3A%5B%22http%3A%2F%2Fzotero.org%2Fusers%2F14440515%2Fitems%2FNSWGJTIW%22%5D%2C%22locator%22%3A%221%22%7D%5D%2C%22properties%22%3A%7B%7D%7D" ztype="zcitation">(<span class="citation-item"><a href="zotero://select/library/items/NSWGJTIW">Wang 等, 2025, p. 1</a></span>)</span>中的训练机制。

### Gap

已有方法或已有理解缺什么：

现有的方法直接训练所有的tokens，但是实际上对于哪些tokens真正促进推理的这种理解是有限的。

“These approaches neglect the heterogeneous functional roles tokens play in reasoning processes, potentially hindering further performance gains by failing to prioritize critical decision points in sequential reasoning trajectories.” <span class="citation" data-citation="%7B%22citationItems%22%3A%5B%7B%22uris%22%3A%5B%22http%3A%2F%2Fzotero.org%2Fusers%2F14440515%2Fitems%2FNSWGJTIW%22%5D%2C%22locator%22%3A%222%22%7D%5D%2C%22properties%22%3A%7B%7D%7D" ztype="zcitation">(<span class="citation-item"><a href="zotero://select/library/items/NSWGJTIW">Wang 等, 2025, p. 2</a></span>)</span> 🔤这些方法忽视了tokens在推理过程中所扮演的异构功能角色，可能通过未能优先考虑顺序推理轨迹中的关键决策点，从而阻碍进一步的性能提升。🔤

### Method

作者方法是什么：

（具体方法尚未明确，但是简单来说就是只在这20%的高熵上进行训练，从而提高RL的效率）

### Result

最关键结果是什么：

1.  【发现】首先指出，推理过程中，熵的分布是表现出明显的模式的。大多数的tokens以低熵（80%）进行生成的，少数tokens是具有高熵（20%）的。熵比较高的是作为语句的关键决策点的，决定了多条潜在的路径。
2.  定量结果发现，适度提高这些高熵分叉，有利于提高推理性能。

### Claim

作者真正声称了什么：

***

## Section Notes

### Section:

这一节在做什么：

新增概念 / 定义 / 方法：

它如何支撑主 claim：

我不确定的地方：

***

## Math / Mechanism Notes

关键对象：

关键公式：

这个公式在论证里起什么作用：

我需要回头确认的假设：

***

## Experiment Notes

<span class="highlight" data-annotation="%7B%22attachmentURI%22%3A%22http%3A%2F%2Fzotero.org%2Fusers%2F14440515%2Fitems%2FC4BXIZ6M%22%2C%22annotationKey%22%3A%22YUBUPJ87%22%2C%22color%22%3A%22%23ffd400%22%2C%22pageLabel%22%3A%222%22%2C%22position%22%3A%7B%22pageIndex%22%3A1%2C%22rects%22%3A%5B%5B183.114%2C498.192%2C524.41%2C507.776%5D%2C%5B70.866%2C487.233%2C218.599%2C496.817%5D%5D%7D%2C%22citationItem%22%3A%7B%22uris%22%3A%5B%22http%3A%2F%2Fzotero.org%2Fusers%2F14440515%2Fitems%2FNSWGJTIW%22%5D%2C%22locator%22%3A%222%22%7D%7D" ztype="zhighlight"><a href="zotero://open/library/items/C4BXIZ6M?page=2&#x26;annotation=YUBUPJ87">“we conduct controlled experiments by manually modulating the entropy of forking tokens during decoding.”</a></span> <span class="citation" data-citation="%7B%22citationItems%22%3A%5B%7B%22uris%22%3A%5B%22http%3A%2F%2Fzotero.org%2Fusers%2F14440515%2Fitems%2FNSWGJTIW%22%5D%2C%22locator%22%3A%222%22%7D%5D%2C%22properties%22%3A%7B%7D%7D" ztype="zcitation">(<span class="citation-item"><a href="zotero://select/library/items/NSWGJTIW">Wang 等, 2025, p. 2</a></span>)</span> 🔤我们通过手动调制分叉标记的熵来进行受控实验。🔤

实验想回答的问题：

控制组 / baseline：

指标：

结果：

作者解释：

我是否相信这个解释：

还缺什么实验：

***

## Paper Reading Card

论文标题：

我为什么读它：

核心问题：

作者方法：

关键结果：

作者解释：

我的判断：

和我研究的关系：

以后是否需要精读：是/否

***

## Mainline Update Check

这篇 paper 是否更新我的主线：是/否

如果是，更新了什么：

*   Hypothesis:
*   Modeling:
*   Experiment:
*   Interpretation:
*   Next decision:

如果否，它只是提供了什么背景启发：

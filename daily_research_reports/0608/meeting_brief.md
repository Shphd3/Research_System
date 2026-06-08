# Meeting Brief

## Meeting Summary

Conclusion:

在之前的uniform数据分布setting之下，路由坍缩并不是因为构造的数据是不均衡的和坏的router初始化造成的。数据尽管不存在common feature，但是一层transformer block输出的hidden state包含一个common shift. 当我们将这个common shift减掉进行路由以后，我们发现初始化时候的expert是能够回归均匀分发的。

但是common偏置的去除主要修复了早期的路由坍缩现象，要避免最终的坍缩，需要在训练过程中在几何上构造防止坍缩的正则化项。（早期使用load-balance能够极大程度缓解最终路由坍缩，但是治标不治本，并且不能构成feature especialization）

P1/P2: common-score $w_e^Tc$能预测 step-0 dominant expert，明显强于 random baseline。
这支持 common-offset mechanism。
P3/P5: logit-level common-offset cancellation 能降低 hard collapse，并保持 accuracy，但 final max-load 仍然偏高。
这说明 common-offset 是重要原因，但 common subtraction alone 不能完全解决 collapse。
Current interpretation:

P1/P2: common-score $w_e^Tc$能预测 step-0 dominant expert，明显强于 random baseline。
这支持 common-offset mechanism。
P3/P5: logit-level common-offset cancellation 能降低 hard collapse，并保持 accuracy，但 final max-load 仍然偏高。
这说明 common-offset 是重要原因，但 common subtraction alone 不能完全解决 collapse。
## Meeting Preparation

**Question:**

[One core question this meeting should answer.]

**Why this matters?**

[Explain why it affects the mainline judgment, claim boundary, or next experiment decision.]

**Hypothesis:**

[Falsifiable research hypothesis. State the parent problem / subproblem relation when needed.]

**Evidence:**

[Summarize the key evidence. Put the most important metric or figure first because it decides this judgment.]

1. [Evidence point: metric / figure / table / experiment condition.]
2. [Evidence point: what it cannot prove.]

**Boundaries:**

在我们的合成数据实验下，实验说明了：


| Protocol | 它问的问题                                                   | 结果说明                                                                                         |
| -------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **P1**   | common score (w_e^\top c) 能不能预测 step-0 dominant expert？ | 能。说明 step-0 偏向不是普通 random split，而是 common offset 在起作用。                                       |
| **P2**   | 这个预测跨 seed 是否稳定？                                        | 稳定。common-score agreement 接近 1.0，强于 random baseline。                                         |
| **P3**   | 训练时取消 common offset，collapse 会不会下降？                     | hard collapse 下降，但 final max-load 仍偏高。说明 common 是 early driver，但不是全部。                        |
| **P4**   | common-aware initialization 能不能修复 step-0 偏置？            | 能显著降低 step-0 load，但 final 结果 mixed。说明 init 通过 common score 影响 early routing，但 init alone 不够。 |
| **P5**   | 哪种 common subtraction 更稳定？                              | logit-level cancellation 最稳；SVD / low-rank residual 不稳定。                                     |
| **P6**   | anti-lockin warmup 能不能控制 final collapse？                | P6A 最强，final load 明显下降，accuracy 基本保持。说明 final collapse 需要 training-time control。             |
| **P7**   | final router 是不是选错 expert？                              | 不是简单“选错”。post-training route-utility match 很高，说明 route 和 expert utility 发生 co-adaptation。    |


**Cannot claim yet:**

[State the stronger conclusion that cannot be claimed yet.]

**Next Decision:**

[The smallest decision after this meeting: continue, redirect, add one diagnostic, or park.]

**Next Iteration:**

[If continuing, write the minimal decisive experiment. If not, write the park or redirect condition.]

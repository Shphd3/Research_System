# Meeting Brief

## Meeting Summary

Questions:

父问题：
在无 position embedding、feature 均匀的最小任务中，为什么 baseline线性router sparse top-1 MoE 仍然从随机初始化进入 collapse，而不是形成 slot-to-expert specialization？

Setup:



Conclusion:

1. 没有position embedding，同时feature在sequence中移动情况下，collapse仍然存在，此时的collapse主要来源于hidden state中的common元素主导了gating logits $w_e^T c \gg w_e^T h_{feature}$
2. 在合成数据实验的情形下，random initialization 在训练的初期总是会对齐hidden state中的common部分，如果这种对齐行为不被纠正，那么在NTP的训练范式下，线性gating矩阵就会发生lock-in，最后所有feature坍缩到唯一分发的专家上
3. 当我们将common部分删除，能够形成feature-level的specialization
4. 这个common的来源有一大部分来源于我们的数据构造：

```text


```

如上，由于我们的B是给定的，因此B经过attention + normalized之后的，所有的slot中都存在共同的部分：
我们根据这个消融，将B换成了B_i以后，发现路由NMI缓解了，但是还是存在common部分，这部分common部分的来源我们尚不知晓
5. 当我们给定一个特定的先验初始化，我们发现gating能够在早期lock-in到对应的specialization的情形，同时，这种初始化是在空间中连续变化的

Minimum reason:

这个合成无位置编码、且特征在序列中移动的实验设定，排除了三种一阶解释：

数据分布不均衡；
hidden state 中缺失 slot 信息；
slot-specialization 本身不可实现。

实验证据：
1 P1 表明：即使发生路由坍缩（collapse），模型仍然能够达到接近完美的任务性能。
2 P2 表明：slot 信息可以从 h_B中被准确解码。
3 P5 表明：在有利的 router 初始化条件下，slot-specialization 是可以实现的。

因此，现在对collapse最合理的解释是：
router 侧：common logit 主导（common-logit dominance）以及 sparse top-1 路由导致的早期锁定（early lock-in）。

Current interpretation:

显式控制位置因素之后，我们发现：
> 被路由的 B-position hidden state 中仍然存在一个 common component，而该 common component 对应的 router score 主导了 top-1 路由决策。

这个 common score 可能有两种来源：

1. 在初始化时就已经存在；
2. 在训练最开始的几个优化步骤中迅速增长。
随后，sparse top-1 routing 会在 slot-specific 信号尚未建立之前，将路由锁定到某一个早期占优的 expert 上，从而导致 collapse。

Next decision:

第二轮实验需要回答以下问题：

1. common-logit 优势是在 step 0 就已经很大，还是在训练初期逐渐增长出来的？
在移除 position embedding 之后，这个 common component 究竟来自哪里？
2. 如果主动消除（cancel）common-logit，是否能够让随机初始化的 sparse top-1 MoE 进入 slot-specialization 的可达优化盆地（reachable basin）？
3. 为什么 slot-initialized routing 能够保持稳定，而随机初始化 routing 会发生 collapse？

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

[State which conditions, data, model, training objective, initialization, or metric this conclusion covers.]

**Cannot claim yet:**

[State the stronger conclusion that cannot be claimed yet.]

**Next Decision:**

[The smallest decision after this meeting: continue, redirect, add one diagnostic, or park.]

**Next Iteration:**

[If continuing, write the minimal decisive experiment. If not, write the park or redirect condition.]

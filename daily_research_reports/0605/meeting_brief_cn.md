# Meeting Brief: 05_02 Feature Assumption Relaxation

## Meeting Summary

这轮我先暂停继续放松 feature assumptions，因为复查最简均匀数据发现：虽然 inhibition 可以提高 same-feature route consistency，但多数 seeds 出现 route collapse，而且 inhibition 有放大 collapse 的趋势。

因此当前最小问题变成：

> 在 feature 均匀分布、没有 compositional relaxation 的情况下，collapse 是早期几何/初始化已经决定的，还是训练中 top-1 选择逐步放大的？

这个问题必须先回答，否则后续 P1/P3/P2 的结果都会被 collapse 干扰，无法判断 router 是否真的在做 feature-level routing。

## Meeting Preparation

**Question:**

上一次汇报中，我们在“inhibition能够让相同的features稳定进入相同的expert”的前提下，准备进一步relax我们的假设：

1. token只由一个feature组成
2. feature是均匀分布的
3. 进入同一个expert的feature只有一个

但是复查均匀分布数据的实验发现，使用inhibition能够让同一个feature稳定进入到同一expert中，但是这个claim存在boundary, 在所有实验中，有多数seeds发生了路由坍缩。同时，inhibition存在加大这种collapse的趋势。

尽管在不坍缩的seeds中，inhibition能够让同一个feature稳定进入同一个expert，但是这种坍缩对于我们的进一步进行relax假设实验产生了极大的干扰，因此我们首先需要审计坍缩的发生阶段、发生的前提条件。

具体要先问出三个问题：
Q1: collapse expert 在 step 0 / 10 / 20 / 50 是否已经占优势？
Q2: feature hidden centroids 与 router vectors 的相似度，是早期就偏向 collapse expert，还是训练后才偏向？
Q3: collapse expert 是否更对齐所有 features 共享的 common direction？

**Why this matters?**

在feature均匀分布的情形下，已经排除了频率的影响，但是仍然在多个seeds发生路由坍缩。为了进一步地确认坍缩的原因，我们需要audit原来的实验结果，才能进一步relax假设，探索inhibition对于expert专一化的作用。

**Hypothesis:**

H1: 

[可被证伪的研究假设。必要时写清 parent problem / subproblem 关系。]

**Evidence:**

[自洽概括关键证据。先写最重要 metric 或 figure，因为它决定本次判断。]

1. [证据点：metric / figure / table / experiment condition。]
2. [证据点：它不能证明什么。]

**Boundaries:**

[当前结论只覆盖哪些条件、数据、模型、训练目标、初始化或 metric。]

**Cannot claim yet:**

[明确现在不能说的更强结论，避免会议中越界。]

**Next Decision:**

[本次会议后需要做出的最小决策：继续、转向、补一个诊断、还是 park。]

**Next Iteration:**

[如果决策是继续，写最小 decisive experiment；如果不是继续，写 park/redirect 条件。]


# Meeting Brief: 05_02 Feature Assumption Relaxation

## Meeting Summary



## Meeting Preparation

**Question:**

之前的实验中，我们发现使用inhibition能够让同一个feature稳定进入到同一expert中，但是这个claim存在boundary, 经过我们后续的审计发现，在所有实验中，有多数seeds发生了路由坍缩。

尽管在不坍缩的seeds中，inhibition能够让同一个feature稳定进入同一个expert，但是这种坍缩对于我们的进一步实验产生了极大的干扰，因此我们首先需要审计坍缩的发生阶段、发生的前提条件。

**Why this matters?**

在feature均匀分布的情形下，已经排除了频率的影响，但是仍然在多个seeds发生路由坍缩。为了进一步地确认坍缩的原因，我们需要audit原来的实验结果，才能进一步relax假设，探索inhibition对于expert专一化的作用。

**Hypothesis:**

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


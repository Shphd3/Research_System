# 00 Handwrite Anchor

## researcher judgment record

目的：通过2 * 2的实验来研究，Router无法按照feature分发的原因到底因为什么原因？

1. 初始化原因
2. 优化目标不对齐？Utility 与 空间中分布的划分这个目标不一致？

物理建模 / 假设：
不同的feature对应的是2维空间中的正交向量，
如果router能够稳定将这两个向量分开，那就说明在二维情况下，router是能够按照空间中向量信息分发的；如果router不能，说明NTP 中expert Utility 信息和优化目标和空间中的区域划分是矛盾的。
在这里，我想说的specialization是在router层面能够分开。
router没分开，除了优化目标不对齐，还有可能：1. router初始化prior有问题；2.实验做错了；3. 专家参数初始化有问题，一个专家足以捕捉所有关系
feature 是什么？ feature是我们定义的一个语义原子，这里我们想用正交向量代替。
expert 是什么？ 就是MoE中的FFN网络
router assignment 是什么？ 就是专家的分发（Top-1分发，不是soft routing，也不是argmax，要训练路由的）
route-pattern specialization 是什么？ 我们设定的正交的向量进入不同的专家。
utility-aligned specialization 暂时是否不研究？ 要研究，但是要有不同组的对照，因为utility很有可能是决定分发的一大因素。
第一轮 primary metric 是什么？ Router NMI （初 - 末）

最小实验：

构造一个最小的attn + MoE的目标
构造一个 2 维的NTP目标，控制以下变量：

1. 初始化方式（先验初始化、随机初始化）
2. 专家的初始化（分别优势初始化，单个优势初始化）

当前结论：

结论边界：

下一步：

## 1. Problem

Parent problem:

Sharper subproblem:

Decision question:

Why this matters now:

## 2. Physical Priors
What I believe about the system / data / mechanism:

Why this prior could be wrong:

What observable should change if it is right:

## 3. Hypothesis

Current hypothesis in one sentence:

Rival explanation 1:

Rival explanation 2:

What would make me change my mind:

## 4. Operational Definitions

Term 1:

```text
success:
failure:
insufficient evidence:
```

Term 2:

```text
success:
failure:
insufficient evidence:
```

## 5. Minimal Test

Smallest test I can run:

Known good case:

Known bad case:

Known confusing case:

Primary metric:

False-positive cost:

False-negative cost:

## 6. Mainline Impact Gate

```text
affects hypothesis? yes/no/unclear
affects claim boundary? yes/no/unclear
affects next decision? yes/no/unclear
recommendation: pursue / park / ignore
```

Reason:

## 7. Next Decision

Next smallest uncertainty:

Next action:

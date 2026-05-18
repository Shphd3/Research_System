# Paper Reading Record

## Why I Read This

我读它是为了理解：普通的Routing到底在学什么？Router是把怎么样性质不同的数据分到不同的Experts上进行学习了。

## My Mainline Anchor

它可能和我的研究主线关系是：理解Router的核心Failure Mode，是我日后设计出更好的Router的必要条件。

## One Question Before Reading

我读这篇 paper 先只想回答一个问题：

Router在训练过程中在按照什么原则对数据进行分发。

## Do Not Overclaim

这篇 paper 的结论不能直接替代我自己的实验结论；它只能更新我的问题、假设、建模、实验设计或解释边界。

***

## First Pass

### Problem

论文想解决什么问题：理论上解释MoE Router产生专一化的原因

### Gap

已有方法或已有理解缺什么：已有的方法揭示了MoE会自然而然显现出Specialization的现象，但在理论上没有解释MoE的Specialization主要原因是单独来自于线性Router、表征几何，还是说来自于Training Dynamics（NTP训练目标以及训练范式）

### Method

作者方法是什么：通过分析表征空间和Specialization的关系

### Result

最关键结果是什么：

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

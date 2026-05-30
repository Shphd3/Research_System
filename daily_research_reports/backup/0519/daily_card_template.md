# Daily Card - MMDD

## 1. Today's Purpose

今天最想推进的问题是：MoE Gating的失败模式是什么？ 使用MoE的Index进行Sparse Attention的reverse index retrieval是否make sense.

## 2. Mainline Anchor

它对应当前主线中的哪一个问题 / 假设 / 瓶颈：

## 3. Task Conclusions

### Task 1:

Did:

Conclusion:

### Task 2:

Did:

Conclusion:

### Task 3:

Did:

Conclusion:

## 4. Mainline Update

今天是否更新主线：是 / 否

如果是，更新了什么：

如果否，今天澄清了什么：

## 5. What I Cannot Claim Yet

今天的结果还不能说明什么：

## 6. Next Decision

下一步最小决策 / 最小实验 / 最小阅读任务：

## 7. 30s Explanation

如果明天要跟导师/学长说，30 秒版本是：

## 8. Thought Parking Lot

只记录会打断当前任务的旁支想法。关键规则：

> 只要它不阻塞当前 25 分钟产出，就先放进去，不追。

### Thought 1

突然想到的点：在不同的句子中，相同的token经过attention后，都会聚在一起，这个时候，是什么，是什么Property去区分语义信息呢？

它为什么看起来重要：理解Attention的行为，将便于我们更深地理解Gating应该关注什么量进行语义分发。

它是否真的阻塞当前 25 分钟任务：否

我什么时候回来看它：下一个对话进行询问

解释（一句话）：


### Thought 2

突然想到的点：现在的为什么token没有办法被分到不同空间的Expert上，实际上是因为Gating把整个空间拆得还不够干净。假如我们将空间拆干净之后，每个expert都是一个Micro Expert，那实际上有可能能够把不同的token分到不同的专家上去

它为什么看起来重要：我们想要把专家都拆到不同的子空间去处理，从而能够让每个子空间都各司其职。

它是否真的阻塞当前 25 分钟任务：否

我什么时候回来看它：组会完后进行询问。假如说我们把我们的gating网络能够做得大一些，并且做成多层级的，。1024维拆成1024个experts，并且向量要减去均值分发。

解释（一句话）：
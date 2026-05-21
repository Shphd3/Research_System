# Daily Card - MMDD

## 1. Today's Purpose

今天最想推进的问题是：整理研究逻辑线，然后探究Gating分发的路径行为。

## 2. Mainline Anchor

它对应当前主线中的哪一个问题 / 假设 / 瓶颈：我们认为，只要专家的分发够Specialized, 那么专家的buckets就足以让我们的Retrieval Index足够Clean，也足够support我们的Retrieval Index Sparse Attention.

## 3. Task Conclusions

### Task 1:

Did: 梳理研究逻辑线。

Conclusion:

研究逻辑线可以梳理如下：

**方法的根本基点/假设点**：attention 是高度 selective 的算子，当前Token真正需要的信息非常少，核心问题是：能不能把已有 token 按某种语义 / 表征结构分类，从而不用线性扫描全部 KV。

$$\downarrow$$

"长上下文 attention 的 KV memory 有没有一种可学习的 index structure？"

$$\downarrow_{可能的一种解法}$$

基于我们曾经研究的MoE模型，我们要问两个问题：

1. expert 能不能实现 specialization？
2. specialization 能不能帮助 reverse index / inverted index / KV retrieval？

这两个问题是可以独立进行验证的。我们的Claim是：即使Specialization不完美，只要比之前的好，就可以开始测其对Retrieval是否有帮助。

---

思路纠偏：先说问题是什么，不要上来就说 solution。例如：
> 现在的MoE能做到多少Specialization? 如果只能做到60%, 为什么剩下的百分之40%做不到？

---

针对于现在的Router为什么没能把表征分好，一个可能的观点：

1. 前普通 MoE 的 forward 是 token-level dispatch：一个 token 的整个 hidden vector 被送到一个或几个 expert；但这个 hidden vector 里面已经混合了很多 feature，所以 expert 可能学到的是混合后的 token/context bundle，而不是干净的 feature-level specialization。
   - 解释：我们的一个h，$h = h_{AB}$，其可能的分解是：$$h = \alpha A + \beta B + \gamma AB + \epsilon$$
     但是现在的MoE分发错了，它是根据h这个整体，将之分到专家上面去。
   - *确定了首要要研究的问题：**现在的Router是不是把feature混在一起了？***

---

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

## 8. Recording / Class Notes

用于记录上课 / 讲座 / 讨论中真正有用的内容，不写逐字稿。

Class / Session：

Key points：

Relation to my research / current task：

Action：

## 9. Small Thought Parking Lot

只收纳会打断当前任务的旁支想法，不展开分析。关键规则：

> 只要它不阻塞当前 25 分钟产出，就先放进去，不追。

- 突然想到的点：
  - 为什么看起来重要：
  - 是否阻塞当前 25 分钟任务：是 / 否
  - 回看时间：

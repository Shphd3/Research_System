# Meeting core

## Meeting Summary

我们主要探究的问题是为什么线性Router会在feature-to-expert specialization分发 fail掉. 之前我们在ABC长slot上进行了实验，得到的结论是：features在空间中可分，但是Router在训练时没有办法将features分开。

这次我们针对一个最简单的2维空间的Router行为进行探究。我的结论是：

> 对于两个正交的hidden states，线性Router有能力将两者分开。但是是否能够将features分开强依赖于早期的路由行为。

在当前 2×2 实验中，

1. 如果 step 0 已经把$e_1 = [1, 0] $， $e_2 = [0, 1]$, NTP training 没有把它稳定纠正成 feature-level split，而是产生了分发的确定性，也就是logits 上升，进而导致了没有被选中的专家under trained。
2. 如果 step 0 把$e_1 = [1, 0] $， $e_2 = [0, 1]$分到不同的expert上，那么训练过程中，Router对这种分发的确定性（表现为logits gap）会越来越强

## Meeting Preparation

**Question:**

我想回答的问题是：在最小的2 * 2系统中，NTP目标是否会自发地诱导MoE的Gating产生feature specialization.

**Why this matters?**

因为如果在最小系统中都没有办法形成稳定的Specialization，真实训练中MoE的gating产生的分发问题很有可能就不是线性矩阵的表达问题，而是训练目标和训练过程中优化路径的问题.

**Hypothesis:**

二维空间中，正交的两个向量非常容易分开，线性gating矩阵的问题并不是无法在表征空间中产生有效划分，而是由于NTP训练目标并未要求线性gating矩阵产生有效划分。

**Evidence:**
实验表明，在2维空间中，线性gating训练过程中能够将不同的feature分到不同的experts上，但是当线性Gating在初始时产生错误划分，将不同的feature分发到同一个expert上时，NTP 会放大初始 routing 偏置 / 错误分发，而不是主动纠正为 feature-level specialization。

1. 通过看优化过程中的分发演化，这个 toy setting 支持一个判断：2 * 2 实验的分发不一致性，是由于初始时刻的分划错误导致的。即使 feature 在表征空间中可分，NTP 也不保证 router 会把它们路由到不同 expert。

**Boundaries：**
目前的结论仅仅只针对于2维简单情形，高维情形中线性gating的能力没有办法确定。

**Next Iteration:**

下一步不是继续 2×2，也不是重复 structured initialization。
因为 previous ABC / multi-B detailed 已经显示 semantic / slot-centroid init 在 multi-B 下不充分。
下一步应该回到 multi-B synthetic，设计加入显式的 route-function binding signal，
检查它是否能同时改善 route-slot NMI、forced expert loss diagonal 和 Assign-Utility
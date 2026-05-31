# 00 Handwrite Anchor

## Report Summary（中文，汇报用）

目的：

物理建模 / 假设：

最小实验：

当前结论：

结论边界：

下一步：

## 1. Problem

Parent problem: 为什么 普通 线性Gating在 ABC synthetic 实验中没有办法按照feature特征进行分发？

Sharper subproblem: 在最简单的 2 * 2实验中，对于两个正交的Features，使用线性Router进行分发，是否能够稳定分开？如果分不开，是受到什么因素制约？

Decision question:

Why this matters now: 如果在最小2×2系统下Router都不能稳定分开两个正交Feature，
那么ABC实验中的failure就可能不是复杂数据导致的，
而是Router训练机制本身导致的。

## 2. Hypothesis

Current hypothesis in one sentence: 对于两个正交的Features，线性Router能够将之两个features稳定分发到不同的expert上进行处理。

H1:

线性Router具有表达
feature specialization的能力

H2:

NTP训练能够学出
feature specialization


Rival explanation 1: 线性分发能够表达features specialization，但是优化过程中会使得分发偏移。

Rival explanation 2: 线性分发本身就没有办法表达features specialization

What would make me change my mind: 如果不同seeds下最终都形成稳定对角分发，那么我的线性router 一定会发生collapse的假设就会被推翻

## 3. Operational Definitions

Term 1: Router-level specialization

```text
success: 

当不同的features在不同的seeds 稳定分发到不同的experts上，说明Router-level的转移话成立。

failure:

如果在一开始初始化的时候不同的features能够稳定分发到不同的experts上，但是训练的过程中不断探索，此时我们认为Router level specialization失败。

insufficient evidence:

success 和 failure现象没有办法稳定产生。也就是没有在所有seeds稳定出现，同时metrics没有办法判断训练中是否稳定。

```

Term 2: stable specialization

```text
success:
在多个 seeds 或多个 checkpoints 中，feature-to-expert 对应关系保持一致；
允许 expert 0/1 标签互换，但不允许 feature 混合或全塌缩到一个 expert。

failure:
初始化或早期 checkpoint 出现分离，但训练后分离消失、混合，或塌缩到单 expert。

insufficient evidence:
只看了一个 seed 或一个 final checkpoint，无法判断稳定性；
不同 seeds 结果互相矛盾，但还不清楚是训练噪声还是机制失败。

```

## 4. Physical Prior

What I believe about the system / data / mechanism:
正交情形的features使用内积是最可分的，线性Router具有这种分辨表达能力。
Why this prior could be wrong: 具有这种分辨表达能不达标在NTP训练目标下能够训出这种分辨表达能力。

What observable should change if it is right: 在二维情形下，都没有办法形成router-feature 对角线热力图，那么我相信的这个事实就是错的

## 5. Minimal Test

Smallest test I can run:
（还没有想清楚）2 features 2 experts，NTP训练

Known good case:

给系统最有利条件：两个 feature 正交、两个 expert 分别对 feature A/B 有优势初始化、router 有轻微对角先验。
如果机制可行，应当看到稳定 feature-to-expert 对角热力图和较高 NMI。
Known bad case: 

没有真实 feature 差异，或 router 输入不包含可区分 feature 信息。
此时 metric 不应显示强 feature-expert alignment。
如果仍显示强分离，说明 metric 或实验设置有假阳性。

Known confusing case:

feature 与 seed、position、slot、frequency、expert 初始化优势绑定在一起。
此时即使热力图好看，也不能判断 router 是按 feature 分，还是按 shortcut 分。

Primary metric: 
分发热力图 + NMI

False-positive cost:

False-negative cost:

## 6. Mainline Impact Gate

```text
affects hypothesis? yes
affects claim boundary? yes
affects next decision? yes
recommendation: pursue
```

Reason:如果 2x2 最小设置下都无法稳定形成 router-level feature separation，
那么 ABC synthetic 中的 failure 可能来自 router 训练机制本身；
如果 2x2 可以稳定分开，则下一步应逐步去掉有利初始化，定位失败来自初始化、优化目标还是 expert utility 不对齐。

## 7. Next Decision

Next smallest uncertainty:

Next action:


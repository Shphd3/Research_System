# Minimal Anchor Handwrite Draft

Use this by hand before asking AI to polish the anchor. Write rough bullets.
The goal is to expose your thinking, not to produce the final anchor.

## 0. Tiny Summary（中文）

目的：

物理先验：

假设：

最小实验：

我需要 AI 帮我检查：

## 1. Problem

Parent problem:

Sharper subproblem:

Decision question:

Uniform setting下为什么Gating仍然会collapse. 

## 2. Physical Prior

What I believe about the system / data / mechanism:

1. uniform frequency不等于zero mean; linear gate极易受到common offset的控制

Why this prior could be wrong:

1. 最终学到的routing不和common方向对齐

What observable should change if it is right:

1. 如果训练后审计，坍缩到的gating向量极易和common shift对齐，那么说明我们的认识是对的

## 3. Hypothesis

Current falsifiable hypothesis:

H1：在uniform setting 下，数据仍然存在common方向，该common方向仍强依赖于数据的构造的共现模式，改变共现模式以后，common方向会减弱

H2：random initialization情况下，线性 router 极易学到数据的common方向，该方向上不同数据的投影很大，从而主导了不同数据之间的分发，最终导致路由坍缩。

H3：减去common方向之后能够让数据分得更开，能够使得不同feature的数据得到不同的专家处理。

Rival explanation:

What would make me change my mind:

## 4. Mathematical Sketch

Objects / variables:

h = h_{common} + h_{features}

Relation I expect:

希望common方向和features的方向能够使用加性关系拆开，同时能够尽可能少地依赖于统计量

Observable implied by the relation:

common方向可以通过投影方法去除，同时在不同数据量下，方向估计稳定

## 5. Minimal Test

Smallest test I can run:

以下实验每次只改变一个变量：

1. 找出构造数据的共现模式（如出现位置、预测目标等），改变共现模式，查看是否能够减弱common方向（目前认知是mean方向，top_i奇异值方向）
2. 采用多seeds, 观察在多seeds的情况下，gating是否极易与common方向发生对齐. 先用原先的数据，实验完成后用1. 数据
3. 在我们的认知之内，common方向就是mean方向和top_i奇异值方向，因此我们采取的路由方式需要以合适的估计方式，估计这两个方向，然后减去方向，进行实验。

Primary metric / figure:

路由热力图

路由向量（特别是高频次被选中的专家对应的路由向量）与common方向的相似性热力图（内积 + cosine similarity）

Success:

Failure:

Insufficient evidence:

## 6. Next Decision

If supported:

1. 【真实数据上的更改】可以估计common方向，然后特地让gating向量都放在与common方向上正交的方向上？

If weakened:

1. 视情况而定

If unclear:

1. Make it clear, then divide & conquer!

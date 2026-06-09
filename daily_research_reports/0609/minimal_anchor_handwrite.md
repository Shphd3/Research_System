# Minimal Anchor Handwrite Draft

Use this by hand before asking AI to polish the anchor. Write rough bullets.
The canonical anchor is written in English. If Chinese helps thinking, write a
separate `_cn.md` companion; do not mix two full versions in one file.

## 0. Tiny Summary

Parent problem:

Current subproblem:

Core hypothesis:

Minimal test:

Current boundary:

Next decision:

## 1. Problem Definition

Parent problem: 

为什么MoE的gating不能稳定形成feature level的specialization?

Sharper subproblem:

在之前我们发现，collapse是由于position embedding造成的问题。现在我们排除这个因素（要么去position embedding，要么让slots出现在sequences中的不同位置），发现还是会造成expert collapse. 我们想要探明collapse的原因.

Decision question:

去掉position这个common因素的影响，为什么MoE还会发生collapse？构造的数据中是否还存在其他贡献因素

Not in scope:

1. 暂时不对真实表征空间提出解决方案

## 2. Physical Prior

首要是排除position的影响，其次在语言中，存在很多与slot无关的common信息。

P1: 同一slot下，表征含有关于slot的信息成分，从而对于同一个target, 不管对于所在B_i如何，都应该路由到同一个expert上. 同一slot下，如果预测目标不同，那么实际上可能存在不同的语义信息，因此通义slot不同target, 是否应该路由到同一个expert上应该分类讨论。

Meaning: 是不是路由应该按照的target feature来

Could be wrong if:

Meaning:

Could be wrong if:

## 3. Hypothesis

H1: 去掉common component以后，gating网络能够自动按照target学到分发的规律。

Supported if:

Weakened if:

H2: 当我们人为地将不同的target路由先验给到expert，那么expert能够一直保持这种feature学法。

H3：采用inhibition，能够让feature完美专一地学到对应的expert上

Supported if:

Weakened if:

## 4. Minimal Mathematical Model

Objects: H1 

Core decomposition:

Mechanism relation:

Observable metrics: 继续按照我们multi-Bi，但是使用我们的discriminative的实验setting. （位置不能固定）

Falsifier:

Objects: H2

Core decomposition:

Mechanism relation:

Observable metrics: 就只用一个B，然后slot一样discriminative（位置不能固定）

Falsifier:

## 5. Minimal Tests

Experiment:

Question:

Intervention:

Primary metric:

Supports:

Weakens:

## 6. Falsifiable Outcomes

Supported:

Weakened:

Insufficient evidence:

## 7. Current Evidence

Observation:

Interpretation:

Boundary:

## 8. Claim Boundary And Next Decision

Can claim:

Cannot claim:

Next decision:

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

在之前我们发现，collapse是由于position embedding造成的问题。现在我们排除这个因素（要么去position embedding，要么让slots出现在sequences中的不同位置），发现训练到最后还是会造成expert collapse. 我们想要探明collapse的原因.

Decision question:

去掉position这个common因素的影响，为什么MoE还会发生collapse？构造的数据中是否还存在其他common component？
如果去掉了所有common component，为什么Gating还是不能按照slot features进行分发？不同的slot出现的顺序导致了更新发生了重叠？还是其他什么原因？

Not in scope:

1. 暂时不对真实表征空间提出解决方案

## 2. Physical Prior

首要是排除position的影响，其次在语言中，存在很多与slot无关的common信息。

P1: 同一slot下，表征含有关于slot的信息成分，从而对于同一个target（target只和slot相关）, 不管对于所在B_i如何，都应该路由到同一个expert上. 

Meaning: 

Could be wrong if:

Meaning:

Could be wrong if:

P2: 在P1情况下，B_i所在的位置，我们认为应该是带有一个专有属于其自身的语义信息，这种语义信息很容易使得用于分发的hidden state看不到上文的slot信息

P3：数据的structure 应该能决定的事情是我们想要最终学成的表征空间的性质，但是router很有可能一开始没有学到这种语义结构，从而导致发生lock-in

P4：现有的线性gating，如果被训练太多，决策区域会变大，从而后续给定的token都会被包含进入其决策的空间区域中。

Meaning: 

Could be wrong if:
不同的token表征实际上是不含有common部分的，这样子线性gating即使被训练再多，也不会进行一致性的决策

Meaning:

Could be wrong if:



## 3. Hypothesis

H1（根据P1 和 P4提出）: 当我们按照slot进行初始化，避免early lockin的时候，同时我们分发数据给定slot的顺序一定，slot在sequences中不同位置出现时，应该能最终训出fully specialization的模型。（给定先验 + 防止某个专家向量被训得太好-P4）

Supported if:
跨seeds实现slot specialization

Weakened if:
理想训练情况下，发生slot专家分家情形

H2: 在H1成立的基础上，如果我们再加入几何上的Inhibition，我们能够让决策错误（同一slot-target对分到其他专家上）出现得更少

Supported if:

Weakened if:

## 4. Minimal Mathematical Model

Objects: 

被分发的hidden states 为 h

Core decomposition:

h = h_{common} + h_{semantic}

Mechanism relation:


r1 - slot - B_i - y_{slot} - r2

r1、r2长度不固定

Observable metrics: 

slot level 分发NMI

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

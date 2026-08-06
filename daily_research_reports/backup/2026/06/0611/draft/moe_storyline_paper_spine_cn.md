# MoE 论文故事线与导师对齐稿

Source: `daily_research_reports/0611/draft/moe_storyline_anchor_plan_0611.md`

Scope: This file extracts the paper-level storyline, claim boundary, mathematical center, and mentor-facing alignment message. It does not write the final anchors.

## 0. 结论

当前工作应收紧为一条论文主线和两个后续锚点。

论文主线是：稀疏 top-1 点积 MoE 的早期路由坍缩，可能来自隐藏状态里的共享成分被随机路由器投影成专家特异偏置。这个机制可以先在合成空间验证，再审计真实或半真实表征空间，并自然导向“感知共享成分的路由器初始化”。

两个后续锚点必须分开：

1. Anchor A：真实/半真实表征里是否存在同样的初始化几何问题。
2. Anchor B：如果问题存在，能否构造无标签的 common-aware 初始化方法。

## 1. 当前决策

论文中心不应继续扩散成“B residual 源头审计”或“负载均衡比较本身”。B residual 是支撑机制的证据，不是论文卖点；负载均衡是基线和边界测试，不是主科学问题。

当前主问题应表述为：

```text
common-logit bias as a router initialization failure mode.
```

中文含义：共享成分经过随机路由器后，变成不同专家的固定打分偏置，从而造成初始化时某些专家更容易被选中。

## 2. 导师真正关心的问题

导师不是主要要求再做一个 toy ablation，而是在问：

```text
如果 common-bias 机制是真的，能否把它变成一个简单的路由器初始化原则，
在真实表征空间验证，并说明专家数增加时这个问题更严重？
```

隐含机制链条是：

```text
存在共享表征
-> 随机点积路由器对共享方向给每个专家不同投影
-> 某些专家更容易被路由到，某些专家更难被访问
-> top-1 路由放大早期可访问性差异
-> 未使用专家无法学习
-> 专家数越多，极端共享投影赢家越容易出现
-> 因此路由器初始化应考虑表征/专家几何
```

导师可能喜欢当前结果的地方：

- 现象基础：共享方向能在路由器真正利用判别差异前主导分配。
- 数学对象清楚：$w_e^T c$。
- 干预简单：移除、抵消或均衡共享投影。
- 自然连接专家数 scaling 测试。
- 有实际方法指向：更好的路由器初始化。

导师可能认为缺少的部分：

- 真实表征证据：真实 hidden states 里是否也有这个机制。
- 初始化方法：能否定义简洁规则。
- 专家数 scaling：专家越多是否越容易坏。
- 数学解释：为什么共享投影会制造专家可访问性不平衡。

## 3. 谨慎写法与导师逻辑的差异

导师的前台框架更主动：

```text
这是一个基础初始化问题。
提出一个路由器初始化方法。
显示它能缓解专家数增加时的坍缩。
尽快形成 arXiv draft。
```

我们原来的谨慎框架更强调边界：

```text
当前只在合成设置里有受控机制。
还不能声称完整语言模型迁移。
还不能声称可部署方法。
负载均衡不等于特征专门化。
common-control 还没证明强于 load balance。
```

对齐策略是改变论文前台粒度：

```text
前台故事：
common-logit bias 揭示一个路由器初始化失败模式；
common-aware 初始化是自然的数学修正；
下一步在真实表征中审计几何，并做专家数压力测试。

内部边界：
不声称解决完整 LM MoE；
不声称负载均衡无用；
不声称已经证明专家具有完整功能专门化。
```

## 4. 最小 arXiv 草稿方向

题目方向：

```text
Common-Logit Bias Drives Early Routing Collapse in Sparse Top-1 MoE
```

副标题方向：

```text
A Mechanistic Study and Common-Aware Router Initialization
```

一句话 thesis：

```text
Even when discriminative features are represented and balanced, random dot-product top-1 routers can collapse because common hidden components induce expert-specific biases; this motivates common-aware router initialization and representation-space audits.
```

中文含义：即使判别特征已经存在且数据平衡，随机点积 top-1 路由器仍可能坍缩，因为隐藏状态的共享成分会制造专家特异偏置；这支持 common-aware 初始化和表征空间审计。

不能声称：

- 解决 MoE 坍缩。
- 取代负载均衡。
- 证明完整语言模型中的功能性专家专门化。
- 实际扩展到百万专家。

如果后续两个锚点成功，可以声称：

1. common-logit bias 是受控 top-1 点积 MoE 中早期、可预测、可干预的坍缩机制。
2. 同一 bias 可以在冻结真实/半真实表征空间中被审计。
3. common-aware 初始化能降低初始化时路由不平衡，并改善特征/残差对齐的路由。
4. 专家数增加会提高极端共享投影赢家出现的风险，因此这是专家数扩展相关的初始化问题。

## 5. 真实表征空间里的 feature 定义

不要先问“语言模型里的真实 feature 是什么”。应采用可操作定义：

```text
feature 是 hidden states 中可控制或可测量、且应被路由保留的变化。
```

三个实用定义：

1. 有标签的受控 feature：relation type、question type、answer type、domain、template family、syntactic role 等。指标包括 feature_NMI、per-feature route purity、feature margin vs common margin。第一版 arXiv 最推荐，因为指标清楚。
2. 残差聚类 feature：先估计共享子空间 $C$，去除共享成分得到 $h_{res}=P_{\perp C}h$，再聚类残差并检查路由是否保留聚类身份。它支持“残差结构对齐路由”，不是语义专门化。
3. 任务预测 feature：训练线性探针预测已知目标属性，把目标预测方向或类别当作 feature。它最接近合成 slot 设置。

本周推荐：

```text
primary: controlled labeled prompts
secondary: residual cluster audit
```

## 6. 与负载均衡的关系

不要写成：

```text
common-aware init beats load balance.
```

应写成：

```text
load balance 控制每个专家收到多少流量；
common-aware init 控制早期分配由什么信息决定。
```

三类指标：

- 使用率指标：max_load、active experts、routing entropy。
- 对齐指标：slot_NMI、feature_NMI、per-feature route purity、cluster-route mutual information。
- 机制指标：common margin、residual/feature margin、common argmax predicts route winner、route lock-in step。

核心比较：

```text
在相似使用率下，common-aware initialization 是否比 load balance alone 更改善 feature/residual alignment？
```

## 7. 论文数学核心

假设隐藏状态分解为：

$$
h_i = c + r_i
$$

路由器分数为：

$$
z_{i,e} = w_e^T h_i = w_e^T c + w_e^T r_i
$$

定义：

$$
a_e = w_e^T c
$$

关键点：$a_e$ 与 feature 无关，却对 expert 特异。因此它可以在 top-1 路由里制造初始化时的专家可访问性差异。

如果 $w_e \sim \mathcal{N}(0,\sigma^2 I)$，则：

$$
a_e = w_e^T c \sim \mathcal{N}(0,\sigma^2\|c\|^2)
$$

专家数 $E$ 增加时，专家集合中的最大 common projection 往往更大，所以更容易出现一个极端 common-aligned expert 主导早期路由。

这个推导支持：

```text
common projection can create initialization-time expert accessibility imbalance.
```

它不证明：

```text
initialization alone solves full training collapse.
```

## 8. 建议论文结构

1. Introduction：把 early collapse 引入为路由器初始化几何问题。
2. Controlled Setting：定义 synthetic ABC task 作为因果源。
3. Collapse Despite Feature Availability：说明 feature 可见不等于路由专门化。
4. Common-Logit Bias Mechanism：给出 $h=c+r$ 和 $z=w_e^Tc+w_e^Tr$。
5. Early Evidence and Intervention：展示 step-0 common margin、最终 dominant expert 预测、common-logit cancellation。
6. Real Representation Audit：放 Anchor A 结果。
7. Common-Aware Initialization：放 Anchor B 结果。
8. Load Balance and Boundary：说明负载均衡和 common-aware init 是互补关系。
9. Discussion：说明解决了什么、没解决什么，以及 persistent common-control / anti-lockin / functional expert specialization 的后续方向。

## 9. 立即执行顺序

17:30 的推荐动作：

1. 先写 Anchor A 粗稿。不要先写方法，因为真实表征审计回答导师的“是否真实存在”问题。
2. 把 Anchor A 发给别人 review / critique，不要立刻抛光。
3. 再写 Anchor B 粗稿，假设 Anchor A 支持 common-logit bias 存在。
4. 并行分派实验：真实表征审计、合成无标签初始化、负载均衡 2x2、专家数 scaling。

Anchor A review 应检查：

- 是否只有一个 decision question。
- 真实表征 feature 定义是否清楚。
- 指标是否足够。
- 是否没有过度声称 LM transfer。

## 10. 给导师的对齐话术

```text
我现在把故事线收紧成 router initialization geometry。
synthetic 部分已经说明 common component 会通过 w_e^T c 变成 expert-specific bias，解释 early collapse。
接下来我不继续做泛泛 toy audit，而是拆成两个 anchor：
第一，审计真实/半真实 hidden representation 里 random router 初始化是否也有 common-induced imbalance，并做 expert-count scaling；
第二，在这个几何上设计 label-free common-aware initialization，比如 common-equalized / common-orthogonal / residual-cluster init。
这样可以对齐您说的真实表征空间、初始化方法、以及专家数 scaling。
但文章里我会把 million-expert 作为 motivation，不直接 claim 已经解决 full-scale MoE。
```

## 11. 最终决策

使用两个 anchor：

```text
Anchor A: Real Representation Initialization Geometry Audit
Anchor B: Label-Free Common-Aware Router Initialization
```

不要把下一个 anchor 写成 B residual source，也不要写成单独的 load balance comparison，更不要直接跳到 full LM MoE training。

论文中心保持为：

```text
common-logit bias as a router initialization failure mode.
```

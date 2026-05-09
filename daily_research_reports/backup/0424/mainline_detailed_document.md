# 研究主线详细文档：从 shared head 到面向“一学就会，永不遗忘”的 Hierarchical MoE

> 说明：本文件的骨架严格参照 `main (6).tex`，并按照  
> **Hypothesis → Mathematical Modeling → Empirical Study → Next Iterations**  
> 的方式重写为当前版本。

---

# 1. Recent Updates

我们当前的研究主线，已经不再是“MoE 专家是否分得开”，而是：

> **为了达到“一学就会，永不遗忘”的终极目标，什么样的表征空间、单层结构和训练方式，能够让共享知识稳定保存，让新知识局部写入，并最终支持 Hierarchical MoE。**

当前最重要的四个更新如下。

## Update 1：shared head 与可塑空间必须分开

真实 hidden state 中存在 shared head。单纯用 raw hidden 做专家输入，会让共享的大方差结构压住真正适合专家学习的长尾变化。  
因此，MoE 的第一步不是“多上几个 expert”，而是先把共享/common 部分和可塑学习空间分开。

## Update 2：单层最稳的收益来自 expert 输入空间改变

在真实单层 block replacement 里，最稳定的收益不是“router 改看 tail”，而是：

> **expert 从 raw hidden 改成在去 common/head 化后的空间里计算。**

这一步把主线从表征猜想推进到了真实 block 机制。

## Update 3：进入 CL 后，full tail 太粗，需要重新定义 expert input

Phase7-Phase8 说明：不能再把 full PCA tail residual 直接当成 CL 第一版 expert input。  
静态 old-stage 更偏窄而稳的 `u25`，但进入 CL 后，更偏更完整的 functional span，也就是 `u50_ext`。

## Update 4：当前 CL 第一瓶颈不是 band 没切对，而是 horizon 太长

Phase8.1 最重要的发现不是学习率大小，而是：

> **adaptation horizon 太长会系统性 over-update。**

也就是说，当前模型前几步可以学到东西，但后几步把前面的收益冲坏了。  
所以现在最合理的下一步，不是继续切 band，也不是直接扩 hierarchy，而是回到正式的 matched forgetting 比较。

---

# 2. Background and Theoretical Critique

## 2.1 终极目标决定了我们不能只研究“专家分开”

如果目标只是做一个静态语言模型上稍微更好的 MoE，那么只看专家分工、负载均衡、聚类纯度，已经可以讲一部分故事。  
但我们的目标更高：

> **做一个能够支持“一学就会，永不遗忘”的 Hierarchical MoE。**

这意味着我们必须回答的，不只是“专家有没有分开”，而是：

1. 共享/common 知识如何稳定保留；
2. 新知识如何快速写入；
3. 写入如何局部、低干扰；
4. 这种局部写入能否自然扩展成真正的层级结构。

所以从一开始，我们就需要把“分得开”和“分得好”区分开。

- **分得开**：表征里有可读结构，例如 domain probe、purity、NMI 提高；
- **分得好**：这种划分真的让模型在下一词预测上变好，并且最终有助于低遗忘学习。

## 2.2 为什么从参数空间转向表征空间

最早很多关于 MoE 专一性的理解，容易落在参数空间差异上，例如参数正交、不同专家权重不同、负载均衡等。  
但这些都不够，因为：

1. 随机路由也可能造成参数不同；
2. 参数不同不等于学到了有任务价值的分工；
3. 真正重要的是：输入在进入专家前，被分配到了什么空间；专家实际上在学什么模式。

因此，我们把问题改写成：

> **语言的 Zipf 分布是否在 hidden representation 中制造了“共享/common 头部 + 长尾可塑残差”的结构？如果是，MoE 应该顺着这个结构设计。**

## 2.3 为什么不能直接把 full tail 当成最终答案

从早期结果看，去掉 shared head 后的 residual 比 raw hidden 更可分，也更适合专家计算。  
但进入 Phase7 以后，我们发现一个更细的问题：

> **top-16 之后整块 residual 太粗。**

因为其中混合了：

1. 仍有统计支持、对 next-token loss 有贡献的功能区域；
2. 更稀疏、更弱支持、可能不适合直接做第一版 expert input 的部分。

这就是为什么 Middle Tail 必须被重新定义，而不能继续用“full tail = 好空间”这种粗说法。

## 2.4 为什么 hierarchy 现在还不能直接上

我们做 hierarchical MoE，不是为了结构好看，而是因为最终目标真的需要分层：

- 第一层稳定保存共享/common；
- 第二层吸收更广的功能带；
- 第三层才可能进一步进入粗到细的层级路由。

但是现在 learned recursive 还没有成立。已有 toy 和 oracle gap 桥接结果说明：

> **recursive 的第一瓶颈是 coarse routing，而不是 fine-local routing。**

因此，在单层 CL 主线还未正式裁决之前，直接推进真实 hierarchy，只会让问题变得更难解释。

---

# 3. Hypotheses and Mathematical Modeling

## 3.1 Mainline hypotheses

当前阶段，最重要的四个假设如下。

### H1：共享/common 结构与可塑学习空间必须分开

如果不先把 raw hidden 中的大方差共享结构剥离出来，专家就会被共享/common 方向支配，看不见真正适合局部学习的长尾变化。

### H2：单层最稳的结构信号是 expert 在去 common/head 化后的空间中计算

当前更强的证据支持：

> **expert 输入空间比 router 是否只看 tail 更关键。**

因此，我们的结构重心先放在 expert 输入，而不是先把 router 完全改掉。

### H3：进入 CL 后，最合适的 expert input 不是 full tail，也不是最窄 core，而是更完整的 functional span

静态 block replacement 更偏 `u25`，因为它更窄、更稳、更容易学。  
但进入 CL 后，更偏 `u50_ext`，因为它覆盖了更多真正有功能价值的部分。

### H4：当前 CL 的第一瓶颈是 over-update，而不是 band 没切对

如果 adaptation horizon 过长，后几步会把前几步学到的有效更新冲坏。  
因此现在最重要的不是再切 band，而是固定 `u50_ext` 后，用短 horizon 做 formal matched forgetting。

---

## 3.2 Shared head 与 tail residual 的数学表达

记第 8 层目标位置的 hidden representation 为：

$$
x \in \mathbb{R}^d
$$

全局均值为：

$$
\mu = \mathbb{E}[x]
$$

中心化表示为：

$$
x_c = x - \mu
$$

对 centered covariance 做 PCA，前 $k$ 个主方向记为：

$$
V_k
$$

则早期的 tail residual 定义为：

$$
x_t = (I - V_k V_k^\top)(x-\mu)
$$

这一步的含义是：

1. 去掉均值；
2. 去掉 shared high-variance head；
3. 保留更可能承载 domain / semantic / long-tail 变化的 residual。

但是 Phase7 之后，我们已经知道：

> 对 CL 来说，full tail 不是最合理的第一版 expert input。

因此我们进一步引入 band 化的功能空间。

---

## 3.3 从 full tail 到 functional span

固定：

- 去掉前 16 个主方向；
- 用 $r95$ 表示累计解释方差达到 95% 的位置；
- 把 head 后的中段继续细分。

在 Phase7.6 中，我们引入：

$$
u25 = [17, 207]
$$

$$
u50 = [17, 398]
$$

$$
u75 = [17, 589]
$$

$$
l50 = [399, 781]
$$

并构造两个关键候选输入：

$$
x_{u25} = P_{u25}(x-\mu)
$$

$$
x_{u50\_ext} = x_{u50} + 0.25\,x_{ext}
$$

这里的思想不是再去寻找“唯一正确 band”，而是区分两件事：

1. **core band**：更窄、更稳、更容易学；
2. **functional span**：更宽、更完整、更能覆盖 next-token 所需功能。

当前最重要的结论是：

- 静态 block replacement 更偏 core band，也就是 `u25`；
- continual learning 更偏 functional span，也就是 `u50_ext`。

---

## 3.4 单层 factorized block 的数学形式

当前最稳的一层结构，不是完整 hierarchy，而是一个因子化 block：

$$
h_{\mathrm{out}}
=
h_{\mathrm{in}} + F_c(x) + F_t(x_{\mathrm{plastic}})
$$

其中：

- $F_c(x)$ 负责稳定共享/common 部分；
- $F_t(x_{\mathrm{plastic}})$ 负责可塑部分；
- 在当前 CL setting 下，$x_{\mathrm{plastic}}$ 的最佳候选是 `u50_ext`。

如果保留路由，则当前最有希望的 routed 版本是：

$$
h_{\mathrm{out}}
=
h_{\mathrm{in}} + F_c(x) + \sum_e g_e(x)F_e(x_{u50\_ext})
$$

这里我们故意先让 router 继续看 raw $x$，因为现有证据还不能说明 router 一定应该只看 tail-like 输入。

---

## 3.5 specialization 的数学定义

当前对 expert 专一性的最稳定义不是 purity 或 NMI，而是 token 级功能优势。

如果 router 选中的 expert 为 $e^\star$，替代 expert 为 $e'$，则反事实 expert gap 定义为：

$$
G_{\mathrm{cf}}(e')
=
\mathbb{E}
\left[
\ell(y,f_{e'}(c))
-
\ell(y,f_{e^\star}(c))
\right]
$$

如果：

$$
G_{\mathrm{cf}}(e') > 0
$$

说明当前被选 expert 对当前 token 的下一词预测损失更低，也就是说它有真正的任务功能优势。

这一定义对我们的总目标很重要，因为：

> 只有当 expert 真对当前 token 更有用时，后面才有资格讨论它是否也更适合局部写入新知识。

---

## 3.6 continual learning 的判断指标

进入 CL 后，我们不再只看静态 PPL，而是明确区分：

### 新知识学习收益
$$
LG(U) = L_{\text{query,before}} - L_{\text{query,after }U}
$$

表示在 support 上做了 $U$ 步适配以后，新 domain 的 query loss 降了多少。

### 旧知识遗忘代价
$$
FC(U) = L_{\text{old,after }U} - L_{\text{old,before}}
$$

表示适配后旧 domain loss 上升了多少。

### 只惩罚遗忘
$$
FC^+(U)=\max(FC(U),0)
$$

### 综合分数
$$
RAS(U)=LG(U)-FC^+(U)
$$

此外还要看：

- `ReachRate`：是否进入了可以按 matched learning gain 比较的区间；
- `matched forgetting`：在学到同样多新知识时，谁忘得更少。

这一步非常关键，因为它把“更适合 continual learning”从感觉，变成了可比较的裁决标准。

---

## 3.7 为什么 hierarchy 的下一步是 coarse objective，而不是直接扩模型

当前 recursive toy 和 oracle-gap bridge 的核心关系是：

$$
R5c \ll R5,\qquad R5d \not< R5
$$

这表示：

- 只修 coarse routing，就会大幅改善；
- 只修 fine-local routing，几乎没用。

因此下一阶段如果要继续推进 hierarchy，必须先让 coarse router 的目标与真实专家优势对齐，而不是先继续堆结构。

---

# 4. Empirical Study

## 4.1 What was executed by now

截至现在，整条主线大致完成了五类工作：

1. **表征空间诊断**：shared head、tail residual、head removal 条件；
2. **优化器 toy 与修正**：Weight Decay、学习率窗口；
3. **真实单层 block replacement**：从 proxy 转向真实语言建模收益；
4. **功能性专一性验证**：从 purity/NMI 转向 token 级 expert gap；
5. **CL 前置重定义与 smoke**：从 full tail 收缩到 `u50_ext + short horizon`。

下面按主线顺序整理。

---

## 4.2 从 shared head 到 tail residual

### 已完成的证据
1. 真实 Qwen hidden 中存在 shared head；
2. tail residual 在 domain probe / purity / NMI 上优于 raw hidden；
3. 去均值本身几乎只是负控制；
4. 去掉 shared head 有益是条件命题，不是永远成立。

### 这一步证明了什么
> raw hidden 里确实混有一块大方差共享结构，直接拿它做 expert learning 不合理。

### 还留下什么问题
> 表征更可分，不等于语言模型任务一定变好；所以必须转向 block-level 验证。

---

## 4.3 从 toy 机制到真实 block 机制

### 已完成的证据
1. toy 说明统一 Weight Decay 会更压制低方差 tail；
2. toy 说明学习率窗口也可能伤害 tail；
3. 但真实实验显示，WD-only 不是当前正结果主要来源，WD+LR 强解耦甚至最差。

### 这一步证明了什么
> 优化器确实可能伤害 tail，但当前真实模型里更稳的收益来自结构 factorization 和 expert 输入空间，而不是强 optimizer decoupling。

### 还留下什么问题
> 结构收益到底来自 split、容量、router，还是 expert 输入空间？这需要真实 block 消融。

---

## 4.4 真实单层 block replacement

### 已完成的证据
在 Qwen3-0.6B 的第 8 层替换 FFN 后，tail-conditioned hierarchical block 优于 baseline FFN 和 flat raw MoE。

### 这一步证明了什么
> 单层 factorized tail-conditioned block 在真实模型上有真正的语言建模收益。

### 还留下什么问题
> 这时候还不能说 router 一定更好，也不能说专家已经有强功能性专一性；所以要继续做机制拆解。

---

## 4.5 机制消融：先把真正起作用的因素拆出来

### 已完成的证据
1. C1 的收益不只是 split；
2. 也不只是多 expert 容量；
3. routed family 里最稳的收益来自 expert 输入从 $x$ 改到 tail-oriented residual；
4. router-only 改看 tail，不如 expert 改看 tail 稳定。

### 这一步证明了什么
> 当前最稳的结构机制是 expert-tail computation，而不是 router-only tail routing。

### 还留下什么问题
> 这种收益到底是不是“真正有任务价值的专一性”，而不只是结构上碰巧有效？

---

## 4.6 功能性专一性：从“分得开”推进到“分得好”

### 已完成的证据
1. 用反事实 expert gap 重新定义 specialization；
2. 单层 tail-conditioned block 在 middle / rare token 上有正 gap；
3. no-LB 下仍然成立。

### 这一步证明了什么
> 当前单层 block 已经出现真正对下一词预测有帮助的功能性专一性。

### 还留下什么问题
> band 的定义还太粗；尤其进入 CL 以后，full tail 是否还合适，并不清楚。

---

## 4.7 recursive 的位置：不是错了，而是该后置

### 已完成的证据
1. recursive oracle 上界很强；
2. learned recursive 没起来；
3. first bottleneck 在 coarse routing，不在 fine-local routing。

### 这一步证明了什么
> hierarchy 不是被否掉，而是需要在单层主线和 coarse objective 站住之后再回来。

### 还留下什么问题
> learned coarse router 应该怎么对齐 token-level expert advantage，仍是后续问题。

---

## 4.8 Phase7：为什么 full tail 不适合直接进 CL

### 已完成的证据
1. 把谱空间拆成 head / mid / ext / full tail；
2. 做 probe、functional intervention、dictionary 对比；
3. `remove_mid` 对 loss 的影响远大于 `remove_ext`；
4. sparse dictionary 的 top-K 重构明显优于 PCA top-K；
5. dictionary atom 的主要 overlap 落在 mid，而不是 ext。

### 这一步证明了什么
> 否掉的不是 tail 方向，而是“top-16 之后整块 residual 直接做 expert input”。

### 还留下什么问题
> 进入 CL 后，到底该选更窄 core，还是更完整 functional span？

---

## 4.9 Phase7.5 / Phase7.6：core band 与 functional span 的张力

### 已完成的证据
1. 静态 old-stage 最稳的单带是 `u25`；
2. frozen intervention 显示 `u50` 承载更多 next-token 功能；
3. lower-mid 不是独立有力补充；
4. hierarchy-ready 的 coarse/fine 证据仍然不足。

### 这一步证明了什么
> 现在真正得到的是“core band vs functional span”的张力，而不是 hierarchy-ready 证据。

### 还留下什么问题
> CL setting 下模型最终偏向哪一个？

---

## 4.10 Phase8-smoke / Phase8.1：进入 CL 后，问题终于被收束

### 已完成的证据
1. 把 `u25` 和 `u50_ext` 带入 CL；
2. 进入 CL 后，最佳 split input 和最佳 routed input 都变成 `u50_ext`；
3. 当前最优组是 `G4_u50_ext`；
4. 但这时还没有正式优于 `G0`，不能直接扩 full Phase8；
5. 继续做 stabilization smoke 后发现：真正问题不是学习率，而是 adaptation horizon 太长；
6. `U=4/8` 时已经开始进入 `LG \ge 0` 区间，`U=16/32` 后几乎系统性转负；
7. 这说明现在已经进入可做 matched forgetting 的 regime。

### 这一步证明了什么
> 对 CL 来说，更重要的不是最窄的 core，而是更完整的 functional span；当前首要瓶颈是 over-update。

### 还留下什么问题
> 在 matched learning gain 下，`G2_u50_ext` 或 `G4_u50_ext` 是否真的比 `G0` 忘得更少，是否接近或超过 `G0_ER`。

---

## 4.11 What this body of evidence establishes

到这里为止，我们已经真正建立了以下六点。

1. **shared head 存在**，所以共享/common 与可塑空间的分离不是拍脑袋；
2. **flat raw MoE 不是好方向**；
3. **单层最稳的结构机制是 expert 在 tail-oriented residual 上计算**；
4. **单层 block 已经出现功能性专一性**；
5. **进入 CL 后，full tail 不够精确，`u50_ext` 是当前更合理的可塑 functional span**；
6. **当前 CL 的第一瓶颈是 over-update，因此下一步应该是 formal matched forgetting，而不是继续切 band 或直接上 hierarchy。**

---

# 5. Next Iteration

## 5.1 Immediate experiments

### 实验 1：formal matched forgetting comparison

这是当前最重要的裁决实验。

#### 固定
- model: Qwen3-0.6B
- layer: 8
- expert input: `u50_ext`
- horizon: 以 `U=8` 为主
- learning rate multiplier: `0.5x` 和 `1.0x`
- groups:
  - `G0`
  - `G0_ER`
  - `G2_u50_ext`
  - `G4_u50_ext`

#### 目标
回答：

> 在 matched learning gain 下，factorized block 是否比 dense baseline 更少遗忘。

#### 判定
1. 如果 `G2_u50_ext > G0`，说明 split-dense CL block 已有价值；
2. 如果 `G4_u50_ext > G2_u50_ext`，说明 routing 在 CL 中开始带来真实收益；
3. 如果赢 `G0` 但输 `G0_ER`，只能说结构有帮助，还不能说超过简单 CL 方法；
4. 如果都不赢 `G0`，则当前 CL 主线还不稳，不能继续扩 hierarchy。

---

### 实验 2：router calibration 诊断（后置）

只有在 `G4_u50_ext` 的 matched forgetting 真正优于 `G2_u50_ext` 后，才值得继续做这一步。

#### 目标
检查 route score 是否能更好对齐 token-level expert advantage。

#### 作用
为后续真正的 routed CL block 和 coarse router 目标做准备。

---

### 实验 3：recursive coarse objective（再后置）

只有在单层 CL 主线站住后，才重新回来做。

#### 目标
缩小 learned recursive 与 oracle recursive 的 gap。

#### 作用
把当前“有 oracle 潜力但学不出来”的 hierarchy，推进成真正可学的 hierarchy。

---

## 5.2 A feasible architecture proposal

如果现在必须给出一个负责任的中间架构，我建议这样写。

### 第一层：稳定共享分支 + 可塑分支
$$
h_{\mathrm{out}}
=
h_{\mathrm{in}} + F_c(x) + F_t(x_{u50\_ext})
$$

含义：

- $F_c(x)$ 保存共享/common 知识；
- $F_t(x_{u50\_ext})$ 吸收更适合局部写入的新知识。

### 第二层：如果 routed 版本在 CL 中通过，再升级为
$$
h_{\mathrm{out}}
=
h_{\mathrm{in}} + F_c(x) + \sum_e g_e(x)F_e(x_{u50\_ext})
$$

含义：

- router 先继续看 raw $x$，因为当前不能证明它必须看 tail；
- experts 统一在 `u50_ext` 上计算。

### 第三层：只有当单层 CL 与 coarse objective 都站住，才考虑真正的 hierarchy

也就是说，真正的 Hierarchical MoE 不是现在就能直接写满的最终结构，而是下面这条路线的自然延伸：

1. shared/common 分支稳定；
2. functional span 可塑分支成立；
3. routed CL block 成立；
4. coarse objective 成立；
5. 然后才进入真正的 coarse-to-fine hierarchy。

---

## 5.3 What not to do next

当前阶段最不该做的三件事：

1. **不要再做一轮更细的 band slicing。**  
   因为当前最需要裁决的是 CL 主线，而不是继续扩搜索空间。

2. **不要直接进入 full Phase8 或真实 hierarchy。**  
   因为单层 CL 还没有正式排序。

3. **不要把 dictionary 立刻拉进主线架构。**  
   它很有启发，但还不是当前主线可部署输入。

---

## 5.4 A one-sentence closing

> **我们现在已经把问题收缩到了一个可以被正式裁决的边界：在 `u50_ext + short horizon` 这个 regime 下，稳定 common 分支加可塑 expert 分支，能不能在 matched learning gain 下比普通 dense 更少遗忘；只有这一步成立，Hierarchical MoE 才值得继续向前推进。**

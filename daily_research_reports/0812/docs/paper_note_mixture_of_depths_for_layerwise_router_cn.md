---
type: paper_reading_note
status: AI_DRAFT_FOR_RESEARCHER_READING
date: 2026-08-12
paper: "Mixture-of-Depths: Dynamically allocating compute in transformer-based language models"
authors: "David Raposo, Sam Ritter, Blake Richards, Timothy Lillicrap, Peter Conway Humphreys, Adam Santoro"
source: "https://arxiv.org/abs/2404.02258"
mainline: "A15 Layer-wise Router: turning a layer signal into a budgeted routing action"
---

# 怎样把“某层是否值得计算”变成可训练的 Router？——Mixture-of-Depths 精读

## 先读结论

Mixture-of-Depths（MoD，按深度混合计算）解决的不是“每层新增了什么语义”，而是一个更工程化的问题：

> 在每层固定只能处理一部分 token 的预算下，学习哪些 token 应执行昂贵的 Transformer block，哪些 token 应走 identity/no-op 路径。

这篇论文对我们的最大价值不是证明公共参数谱或细粒度后移，而是告诉我们，一个完整的 Layer-wise Router 必须同时定义五件事：

1. **动作**：选择专家、执行本层，还是跳过本层；
2. **决策时可见输入**：作决定时哪些表征已经算出来；
3. **预算**：每层允许多少 token 进入昂贵路径；
4. **训练目标**：什么端到端损失让 Router 学会有用的选择；
5. **部署规则**：训练时的全序列 top-$k$ 如何变成自回归生成时的因果决定。

MoD 最值得继承的原则是：

$$
\boxed{
\text{先固定动作与预算，再用任务损失判断路由是否有用。}
}
$$

因此，我们的公共谱、Attention 更新和 conditional gain 最多是 **Router 输入候选或机制诊断**。它们必须在相同负载、相同参数量和相同训练预算下，最终改善 expert-choice regret 或 held-out loss，才获得功能意义。

---

## 1. 先把论文问题讲成人话

标准 Transformer 对每个 token、每一层都执行相同计算：

$$
x_i^\ell
\longrightarrow
\operatorname{Attention+MLP}
\longrightarrow
x_i^{\ell+1}.
$$

这里：

- $\ell$ 是层号；
- $i$ 是 token 位置；
- $x_i^\ell\in\mathbb R^d$ 是第 $\ell$ 层入口的 token 状态。

MoD 允许每个 token 在每个路由层选择两条路径：

$$
\boxed{
\text{执行本层昂贵计算}
\quad\text{或}\quad
\text{直接原样通过}
}
$$

“原样通过”也叫 identity 或 no-op：输出等于输入，而不是把 token 删除或置零。

这与两个相近概念不同：

- **Early exit**：token 一旦退出，通常不再进入后续层；MoD 中 token 可以跳过第 $\ell$ 层，却在第 $\ell+1$ 层重新参加计算。
- **Mixture-of-Experts（MoE）**：在多个不同 MLP expert 中选一个；MoD 是在“执行本 block”和“不执行本 block”之间选择。

---

## 2. 用一个八 token 的玩具例子理解

假设一个序列有 $S=8$ 个 token，但第 $\ell$ 个路由层的 capacity（容量）是 $C=2$。这表示该层无论输入内容如何，都只允许两个 token 进入昂贵路径。

Router 给八个 token 打分：

$$
[0.1,\ 1.4,\ -0.2,\ 0.9,\ 0.3,\ 2.1,\ 0.0,\ 0.7].
$$

取 top-$2$ 后，第 6 个和第 2 个 token 被选中：

$$
m^\ell=[0,1,0,0,0,1,0,0].
$$

于是：

- token 2 和 6 执行 Attention+MLP；
- 其他 token 在该层直接保持 $x_i^{\ell+1}=x_i^\ell$；
- 下一层仍然会重新对所有 token 打分，所以跳过不是永久退出。

这个例子体现了 MoD 的核心分工：

> 人规定一层总共能花多少计算；模型只学习把这笔预算花给谁。

---

## 3. 数学由浅入深

### 3.1 第一级：Router 产生的只是相对优先级

第 $\ell$ 层输入序列为：

$$
X^\ell=(x_1^\ell,\ldots,x_S^\ell).
$$

论文使用每层线性 Router 给 token 一个标量分数：

$$
r_i^\ell=(w_\theta^\ell)^\top x_i^\ell.
$$

$r_i^\ell$ 的直接含义只是：

> 在当前序列和当前层中，Router 对 token $i$ 进入昂贵计算的相对偏好。

它不是经过论文证明的“信息量”“新增知识量”“语义粒度”或“预测熵”。不要因为一个分数与这些量相关，就把它重新命名成这些量。

### 3.2 第二级：capacity 固定总计算量

令每个路由层只允许 $C<S$ 个 token 参加昂贵计算。选择变量为：

$$
m_i^\ell
=
\mathbf 1\!\left[
i\in\operatorname{TopK}(r_1^\ell,\ldots,r_S^\ell;C)
\right].
$$

忽略相同分数的 tie-breaking，有：

$$
\sum_{i=1}^{S}m_i^\ell=C.
$$

这条等式非常重要。它保证不同序列在该层都使用相同的昂贵路径容量，因此性能差异不能轻易归因于某个方案偷偷多算了 token。

如果用比例表示：

$$
\rho=\frac{C}{S},
$$

那么 $\rho$ 就是每个路由层被处理的 token 比例。它是人工设定的预算，不是由 Router 自由决定的总计算量。

### 3.3 第三级：被选 token 更新，未选 token identity

令被选 token 的集合为：

$$
\widetilde X^\ell
=
\{x_i^\ell:m_i^\ell=1\},
\qquad |\widetilde X^\ell|=C.
$$

论文的更新写成：

$$
x_i^{\ell+1}
=
\begin{cases}
x_i^\ell+r_i^\ell f_i(\widetilde X^\ell),
&m_i^\ell=1,\\[4pt]
x_i^\ell,
&m_i^\ell=0.
\end{cases}
$$

紧凑写法是：

$$
x_i^{\ell+1}
=
x_i^\ell
+m_i^\ell r_i^\ell f_i(\widetilde X^\ell).
$$

$f_i$ 抽象表示该 block 对第 $i$ 个被选 token 的 Attention 与 MLP 更新。

这里有三个必须读懂的细节：

1. 未选 token 的输出仍是 $x_i^\ell$，不是零；
2. 路由分数 $r_i^\ell$ 不只决定 top-$k$ 排名，还乘在更新幅度上；
3. 未选 token 在该层不参与被压缩的 Attention，因此选择一个 token 也可能是为了让它成为其他 token 的信息源，而不只是改善它自己的当前预测。

### 3.4 第四级：不可微的 top-$k$ 为什么仍能训练

离散的 $m_i^\ell$ 对分数的排序变化不可微；模型并没有通过普通梯度直接对“谁进 top-$k$”求导。

但对已经被选中的 token，更新中含有：

$$
r_i^\ell f_i(\widetilde X^\ell).
$$

因此语言模型损失 $\mathcal L_{LM}$ 对分数存在梯度：

$$
\frac{\partial \mathcal L_{LM}}{\partial r_i^\ell}
=
\left\langle
\frac{\partial \mathcal L_{LM}}{\partial x_i^{\ell+1}},
f_i(\widetilde X^\ell)
\right\rangle,
\qquad m_i^\ell=1.
$$

白话解释：如果扩大某个被选 token 的更新有助于降低任务损失，它的 score 会收到相应训练信号。随着参数更新，不同 token 的相对排名也会变化。

边界同样重要：未选 token 不通过这条更新获得同样的直接梯度；top-$k$ 身份本身仍是离散的。论文展示这种训练机制在其设置中有效，但这不是“top-$k$ 已经变成完全可微”。

### 3.5 第五级：为什么 fixed capacity 能节省 Attention 计算

标准 self-attention 的 query-key 相互作用规模约为：

$$
S\times S.
$$

若只对 $C$ 个 token 做该层 Attention，则相互作用规模约为：

$$
C\times C.
$$

这部分的相对成本约为：

$$
\frac{C^2}{S^2}
=
\left(\frac{C}{S}\right)^2.
$$

例如 $C=S/2$，query-key 交互约为原来的 $1/4$。但不能据此说整个模型成本必然变成 $1/4$：MLP 更接近按 $C/S$ 缩放，embedding、normalization、通信和路由本身仍有成本。

---

## 4. 为什么论文强调 expert-choice 式 top-$k$

这里的 expert-choice 可以直译为“计算槽位选择 token”：每层只有 $C$ 个昂贵计算槽位，由这一个 block 从全序列中挑选最高分 token。

它与 token-choice 的差别是：

- token-choice：每个 token 自己决定去哪里，容易让某条路径过载；
- expert-choice：路径容量先固定，再挑选恰好 $C$ 个 token，负载天然可控。

对我们来说，最重要的不是照搬术语，而是 matched-load（匹配负载）原则：若比较两个 Router，它们必须具有相同的 expert 容量、no-op 比例或计算预算。否则损失改善可能只是更多 token 获得了更昂贵计算。

---

## 5. 训练时 top-$k$ 与自回归生成的冲突

### 5.1 冲突在哪里

训练时，完整长度为 $S$ 的序列已经存在。判断第 $i$ 个 token 是否属于全序列 top-$k$，需要比较：

$$
r_i^\ell
\quad\text{与}\quad
(r_1^\ell,\ldots,r_S^\ell).
$$

但自回归生成第 $i$ 个 token 时，未来 token 尚未出现。因此不能知道当前分数在最终完整序列中的排名。

这里“非因果”的是全序列路由决定，不是说 causal attention mask 被取消。

### 5.2 论文的第一种修复：辅助二分类目标

把训练期 top-$k$ 身份当作伪标签：

$$
y_i^\ell
=
\mathbf1[m_i^\ell=1].
$$

再让 Router score 同时预测该二分类标签：

$$
\mathcal L_{route}
=
-\sum_i
\left[
y_i^\ell\log\sigma(r_i^\ell)
+(1-y_i^\ell)\log(1-\sigma(r_i^\ell))
\right].
$$

总目标可以写成：

$$
\mathcal L
=
\mathcal L_{LM}
+\lambda\mathcal L_{route}.
$$

生成时便能用局部阈值决定是否执行，而不需要看到未来 token。

### 5.3 第二种修复：单独训练因果预测器

另加一个小预测器：

$$
\hat y_i^\ell
=
g_\phi(\operatorname{sg}(x_i^\ell)),
$$

其中 $\operatorname{sg}$ 是 stop-gradient：辅助预测器读取状态，但不把辅助损失反向传回主模型表征。

它学习预测“训练时完整序列 top-$k$ 是否会选中当前 token”。论文报告该预测任务达到约 97%--99% 准确率，并在大规模 held-out 序列上仅造成很小的 log-likelihood 退化。

必须保留一个边界：生成时的逐 token 阈值不再严格保证每个序列恰好选择 $C$ 个 token。因此训练时是严格 fixed capacity，部署时更接近学习同样平均选择率，存在 train--inference mismatch。

---

## 6. 论文实际做了什么、结果说明什么

### 6.1 经验设置

论文在 decoder-only language modeling 中比较 dense Transformer、MoD 和匹配 FLOPs 的基线。小预算搜索中，作者报告的最佳配置是：

- 隔一个 block 放一个 MoD routing block；
- 路由 block 使用 $C=256$、序列长度 $S=2048$，即 12.5% capacity；
- 中间保留 full-capacity block，而不是让所有层都极端稀疏。

这只是该模型规模、训练预算和数据设置下的经验选择，不能直接当作我们的固定超参数。

### 6.2 关键对照

论文用随机 Gaussian 分数做相同 top-$k$ 作为控制。随机路由显著差于 learned MoD，也差于相应 dense baseline。这支持：

> 功能收益来自学习到的 token 选择，而不只是任意删除计算。

### 6.3 性能与计算结果

在论文报告的 220M 对比中，MoD 每步速度约快 60%--66%，同时 held-out loss 略优于匹配基线。IsoFLOP 实验中，作者找到同时具有较低 loss 与较低每次 forward FLOPs 的 MoD 配置。

但这些数字必须这样读：

- “每步更快”不等于在相同总 FLOPs 下，完整训练 wall-clock 必然缩短同样比例；
- “loss 最多约改善 1.5%”指论文的 log-probability 训练目标比较，不是 accuracy 提升 1.5 个百分点；
- 结果来自从头训练的语言模型，不证明给一个冻结模型事后加谱 Router 会得到相同收益。

### 6.4 Router 模式观察

作者观察到某些 token 会连续多层被选择，路由频率与预测熵存在初步相关。它只能作为行为观察，不能升级为：

- 高熵就是新增信息；
- 高熵就是细粒度语义；
- 所有深层都应处理更细的信息。

---

## 7. MoD 如何与 MoE 结合：MoDE

论文进一步讨论 Mixture-of-Depths-and-Experts（MoDE）。

### 7.1 Staged MoDE：先决定是否执行，再选 expert

$$
\text{MoD Router}
\rightarrow
\begin{cases}
\text{identity/no-op},\\
\text{Attention}\rightarrow\text{MoE Router}\rightarrow E_m.
\end{cases}
$$

优点是未选 token 可以同时跳过 Attention 和 MLP；代价是需要两级决策。

### 7.2 Integrated MoDE：把 no-op 放进 expert 集合

先正常执行 Attention，然后在 expert 集合中加入：

$$
E_\varnothing(x)=0.
$$

Router 选择：

$$
\operatorname{Route}(x)
\in
\{E_1,\ldots,E_M,E_\varnothing\}.
$$

若选择 $E_\varnothing$，MLP residual branch 不写入更新。它结构更简单，但已经支付了 Attention 成本，所以只能节省 MLP expert 计算。

论文发现 integrated MoDE 优于仅仅缩小普通 expert capacity、让溢出 token 被动丢弃。物理区别是：

> 显式选择 no-op 是一个被优化的动作；因容量不足而被丢弃不是模型主动选择。

这一点与我们的 Layer-wise Router 很接近：如果要研究“不需要某层 expert 计算”，no-op 应成为明确路径，并用同负载随机 no-op 与被动 overflow 作控制。

---

## 8. 精确映射到我们的 Layer-wise Router

### 8.1 先区分两个完全不同的 Router

#### 方案 A：完整 block Router

动作是：

$$
\text{执行 Attention+MLP}
\quad\text{或}\quad
\text{跳过整个 block}.
$$

Router 必须在第 $\ell$ 层计算之前使用 $x_i^\ell$。它不能使用本层 Attention 输出 $A_i^\ell$ 或精确更新 $U_i^\ell$，因为得到这些量时，目标 Attention 成本已经支付。

#### 方案 B：Attention 后的 MLP expert Router

动作是：

$$
\text{在 }E_1,\ldots,E_M,E_\varnothing\text{ 中选择}.
$$

此时本层 Attention 已完成，因此 Router 可以读取：

$$
Z_i^\ell=X_i^\ell+A_i^\ell,
\qquad U_i^\ell,
\qquad P_B U_i^\ell.
$$

但它只能影响后续 MLP expert 选择，不能声称节省本层 Attention。

我们当前的 Attention 投影与谱带分析天然更接近方案 B。若研究目标其实是方案 A，就必须换成路由时刻可见的 pre-block 输入，不能数据泄漏式地读取未来更新。

### 8.2 公共谱不是 Router 的必要前提

MoD 每层直接从局部状态学习：

$$
r_i^\ell=(w^\ell)^\top x_i^\ell.
$$

它没有要求把所有层旋转到同一公共坐标。因此公共基的正确功能问题是：

> 在当前状态已经提供的信息之外，谱带特征能否增加对最佳动作或专家效用的预测，并最终改善匹配负载下的任务结果？

至少需要四个 matched controls：

| 条件 | Router 输入 | 作用 |
| --- | --- | --- |
| State-only | $x_i^\ell$ 或 $z_i^\ell$ | 强功能基线 |
| Spectrum-only | 固定公共谱带特征 $s_i^\ell$ | 检验谱信号自身是否足够 |
| State+spectrum | $[x_i^\ell;s_i^\ell]$ | 检验谱信号是否有条件增益 |
| State+random | $[x_i^\ell;q_i^\ell]$ | 排除低维投影/参数量本身的收益 |

其中 $q_i^\ell$ 必须与 $s_i^\ell$ 具有相同维数、归一化和参数预算。

由于我们的 Mean Response 基显示语义粒度的统计后移，但其他公共基不一定复现，公共基选择必须作为显式条件而不是被隐藏：Mean Response、另一种参数基和同维随机/Haar 控制要分开报告。若收益只存在于一个事后挑选的基，不能称为 basis-invariant 的 Router 原理。

### 8.3 Router 的目标必须是功能效用

若动作是选择 expert，可以定义每个 expert 的反事实损失：

$$
\mathcal L_e(x_i^\ell).
$$

oracle 最佳 expert 为：

$$
e_i^*=\arg\min_e\mathcal L_e(x_i^\ell).
$$

Router 的 expert-choice regret 为：

$$
\operatorname{Regret}
=
\mathbb E_i\left[
\mathcal L_{\hat e_i}(x_i^\ell)
-\min_e\mathcal L_e(x_i^\ell)
\right].
$$

若动作是执行或 no-op，则应比较执行后的任务损失下降与计算代价，例如候选目标：

$$
\mathcal J
=
\mathbb E[\mathcal L_{task}]
+\lambda\,\mathbb E[\text{compute}],
$$

或在固定 capacity 下只优化 $\mathcal L_{task}$。

语义标签预测、后谱能量、Attention 方差和 effective rank 都可以做诊断，但不能替代 regret 或 held-out loss。

### 8.4 Conditional Probing 与 MoD 如何接成一条链

[第一份 Conditional Probing 精读](/data/250010109/Research_System/daily_research_reports/0812/docs/paper_note_conditional_probing_for_layerwise_router_cn.md)先问：

$$
G_{\ell,Y}
=
CE(Y\mid X_\ell)
-CE(Y\mid X_\ell,U_\ell)
>0\ ?
$$

它筛查层更新是否带来目标条件下的额外可访问性。

MoD 再要求：

$$
\text{候选信号}
\rightarrow
\text{预算约束下的动作}
\rightarrow
\text{端到端功能收益}.
$$

两者合起来得到我们更严谨的主线：

$$
\boxed{
\begin{aligned}
&\text{旧状态之外是否有目标增量？}\\
&\Downarrow\\
&\text{谱带是否比同维控制保留更多增量？}\\
&\Downarrow\\
&\text{该信号是否在 matched load 下减少 regret 或 loss？}
\end{aligned}
}
$$

任何一层失败，都应停止把下一层正结果当作前一命题的证据。

---

## 9. 你当前最需要补牢的知识点

### 薄弱点一：Router 动作没有定义，就先讨论输入

“Layer-wise Router”可以指跳 block、选 MLP expert、选谱带模块或分配容量。动作不同，输入时刻、成本和评价指标都不同。先定义动作，再讨论公共基。

### 薄弱点二：没有处理信息可用时序

Attention 前的 Router 看不到本层 Attention 输出。使用尚未计算的特征会产生未来信息泄漏，并让节省计算的主张失效。

### 薄弱点三：几何相关性被当成功能标签

细粒度语义更偏后谱，只说明一种表征统计关系。中间仍缺：后谱特征是否预测哪个动作的边际收益，以及使用它是否改善任务结果。

### 薄弱点四：忽略 matched-load 控制

一个 Router 若激活更多 token 或更多 expert，任务损失更低并不说明选择更聪明。必须固定 capacity、expert 数、参数量、训练步数与计算预算。

### 薄弱点五：把可读性当作原模型使用

probe 能读出最佳 expert，不代表 Router 通过端到端训练会使用它，也不代表改善 loss。读取证据是准入条件，不是最终结论。

### 薄弱点六：把层当作独立重复样本

连续层属于同一条深度轨迹，高度相关。逐层正负不能被当作 36 个独立统计样本；应报告轨迹级趋势、阶段异质性或成对样本重采样。

---

## 10. 用这篇论文诱导自己思考

### 问题 1

我们说“逐层 Router”时，到底希望它作哪个动作？

- 跳过整个 block？
- 只跳过 MLP？
- 在多个 expert 之间选择？
- 给不同谱带模块分配计算？

如果一句话说不清动作，后面的 Router 输入与指标都还没有定义。

### 问题 2

如果细粒度后谱特征能很好预测 semantic label，却不能预测最佳 expert，你是否仍应使用它？

提示：可以保留为解释性变量，但不能作为功能 Router 的充分依据。

### 问题 3

为什么 state+spectrum 必须与 state-only 比，而不能只与 spectrum-only 比？

提示：实际 Router 已经能看当前状态。我们真正要证明的是谱特征在这个强基线之外提供增量，而不是单独有可预测性。

### 问题 4

如果 Mean Response 基有效，而 rank-consensus 或随机旋转基无效，结论是什么？

提示：最多说明某一具体参数几何产生了候选功能特征；不能说“公共谱原理”具有基不变性。需要预注册基选择，或把基变成可学习模块并用严格控制审计。

### 问题 5

如果 learned no-op 优于 capacity overflow，说明什么？

提示：主动选择“不计算”本身可以是有意义的动作；被动丢弃只是负载机制，二者不能混为一种路径。

### 问题 6

如果路由标签在训练时依赖完整未来序列，自回归部署怎样作决定？

提示：需要因果 predictor 或局部阈值，并单独报告 train--inference mismatch，而不能只给训练期 oracle top-$k$ 结果。

---

## 11. 这篇论文对主线的具体更新

### Problem 更新

我们不再笼统问“哪个谱带是新增信息”，而问：

> 在明确的层内决策时刻，哪个可用信号能够在固定预算下预测不同动作的边际效用？

### Architecture 更新

必须先选择两种架构之一：

1. pre-block Router：只能读取旧状态，动作是完整 block/no-op；
2. post-attention Router：可读取 Attention 更新，动作是 MLP expert/no-op。

### Evidence 更新

[Mean Response 公共基下的语义粒度结果](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E03_shared_basis_semantic_granularity/summary.md)只能支持谱位置具有候选解释意义；[全相邻层迁移结果](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/summary.md)不支持把它写成深度单调定律。这两类证据都不支持直接用后谱路由。

### Evaluation 更新

主指标应是 matched-load expert-choice regret、held-out task loss，或相同 FLOPs 下的性能。route accuracy 和谱图只能是诊断。

### 下一决策

在任何新 Router 实现前，先由研究者批准：Router 动作、决策时刻、capacity、目标效用与 matched controls。否则不同候选不是在回答同一个问题。

---

## 12. 一页复述卡

**论文问题：**在固定每层计算容量下，怎样动态决定哪些 token 执行昂贵 block？

**核心动作：**执行 Attention+MLP，或走 identity/no-op。

**核心 Router：**

$$
r_i^\ell=(w_\theta^\ell)^\top x_i^\ell,
\qquad
m_i^\ell=\mathbf1[i\in\operatorname{TopK}(r^\ell;C)].
$$

**核心更新：**

$$
x_i^{\ell+1}
=x_i^\ell+m_i^\ell r_i^\ell f_i(\widetilde X^\ell).
$$

**论文结果：**在其 decoder-only LM 设置中，learned fixed-capacity routing 优于随机选择，并找到更好的 loss--compute 权衡；MoDE 还表明显式 no-op 可与 expert 路由联合学习。

**对我们最重要的启示：**谱特征必须作为候选输入，与 state-only 和同维随机特征做 matched-load 对照，并由 regret 或 held-out loss 决定是否具有功能价值。

**不能声称：**MoD 没有证明公共基、低秩新增信息、语义后移或冻结模型上的谱 Router。

**原始来源：**[arXiv 摘要与 PDF](https://arxiv.org/abs/2404.02258)、[arXiv HTML 全文](https://arxiv.org/html/2404.02258)。

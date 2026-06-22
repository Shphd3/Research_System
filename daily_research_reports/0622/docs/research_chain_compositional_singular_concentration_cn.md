# 导师 Research Chain 拆解：组合特征为什么集中到高增益奇异子空间

## 结论

导师这篇稿子的核心链条不是“语言有组合性，所以模型会学语义层级”，而是更窄、更可检验的一条链：

**下一词预测损失会优先选择能高效降低损失的参数方向；早期高频/简单特征反复更新这些方向，使它们成为高增益奇异方向；后来的组合特征在这些方向上下降效率更高，于是被吸入共享子空间；共享带来复用，也带来常见特征和长尾特征的干扰。**

当前最强可说的是：受控嵌套前缀任务支持这个机制的一个 toy 版本。还不能直接声称自然语言语义普遍这样组织。

## 1. 要解决的问题

导师从一个基本张力出发：

语言看起来有语义层级和组合结构，但自回归语言模型训练时只优化下一词预测损失。也就是说，模型没有被显式要求学出“干净语义树”；如果语义特征出现，必须解释为它们如何降低交叉熵损失。

所以真正问题是：

1. 为什么组合特征会集中到少数高增益奇异方向？
2. 为什么这种集中会同时帮助复用、又制造常见特征和长尾特征的干扰？

这里的“高增益奇异方向”指矩阵奇异值分解中被大奇异值放大的方向。直观地说，同样大小的隐藏表示分量，放在大奇异值方向上，会对输出或注意力分数产生更大影响。

## 2. 第一层假设：语言组合性给出“继承 + 新增”的结构

导师先把自然语言抽象成一个可操作结构：

$$
\text{longer meaning}=\text{shorter meaning}+\text{new constraint}.
$$

比如：

city -> beautiful city -> NYC is a beautiful city -> NYC is a beautiful city in winter

对应到符号任务：

$$
A \to AB \to ABC \to ABCD \to \cdots
$$

这一步的作用不是证明自然语言等于前缀链，而是隔离一个最小结构：后来的表达继承前面的表达，并增加一个新成分。

因此可以定义：

$$
u_{AB}=u_A+\Delta_{A\to AB}.
$$

其中 $u_A$ 是旧特征，$\Delta_{A\to AB}$ 是新增特征。导师真正关心的对象不是整体前缀，而是每一步新增的 extra feature。

## 3. 第二层假设：高频简单特征先塑造参数几何

下一步是假设训练过程具有时间顺序和频率偏置：

1. 简单、高频特征出现更多。
2. 它们更早、更反复地被梯度更新。
3. 反复相似的更新会在参数矩阵中形成大奇异值方向。
4. 后来的复杂或长尾特征会面对已经成形的参数几何。

这一步是导师链条中的因果桥梁：从“语言组合性”走到“参数矩阵出现高增益方向”。它不是由 SVD 本身自动推出的，而是依赖训练动态：哪些样本先/多次更新哪些方向。

最危险边界：当前实验主要观察最终几何，还没有完全证明“早期频繁特征先造成奇异值增大”的训练时间因果链。

## 4. 第三层机制：为什么优化会偏好高增益方向

导师的数学核心在这里。

令输出矩阵为：

$$
z=Wh,\qquad W=U\Sigma V^\top.
$$

如果隐藏特征展开为：

$$
h=\sum_i c_i v_i,
$$

则输出为：

$$
Wh=\sum_i \sigma_i c_i u_i.
$$

这说明同样的隐藏系数 $c_i$，在大 $\sigma_i$ 方向上有更大输出影响。

但导师没有停在“输出更大”这个直觉，而是补了损失下降公式。对交叉熵：

$$
\nabla_z L=p-e_y.
$$

隐藏侧梯度为：

$$
\nabla_h L=W^\top(p-e_y)
=\sum_i \sigma_i \langle u_i,p-e_y\rangle v_i.
$$

因此沿 $v_i$ 的梯度步大小是：

$$
\Delta c_i=-\eta\sigma_i\langle u_i,p-e_y\rangle.
$$

更强的一阶损失下降公式是：

$$
\Delta L_i
\approx
-\eta\sigma_i^2\left\langle u_i,p-e_y\right\rangle^2.
$$

这一步给出精确判断：

**不是所有大奇异值方向都会吸引特征；只有“大奇异值 + 当前误差对齐”的方向才会被优化选择。**

这比“高增益方向吸引特征”更严谨，因为它加入了任务对齐条件。

## 5. 第四层机制：Q/K 为什么更容易集中，V 为什么不同

导师把输出矩阵逻辑迁移到注意力的 query/key 矩阵。

注意力分数是：

$$
s_{ti}=\frac{q_t^\top k_i}{\sqrt d}.
$$

softmax 会把分数差转化为指数级 odds ratio：

$$
\frac{\alpha_{ti}}{\alpha_{tj}}=\exp(s_{ti}-s_{tj}).
$$

但导师的关键不是“softmax 放大差异”这么简单，而是：

1. 损失梯度先指出哪些 attention score 改变有用。
2. $W_Q$ 和 $W_K$ 的大奇异值方向能用更小隐藏移动制造更大的 score margin。
3. softmax 再把这个 score margin 转成尖锐路由。

对 query 侧，损失下降形式为：

$$
\Delta L_a^Q
\approx
-\eta(\sigma_a^Q)^2
\left\langle u_a^Q,\gamma_t^Q\right\rangle^2.
$$

对 key 侧：

$$
\Delta L_b^K
\approx
-\eta(\sigma_b^K)^2
\left\langle u_b^K,\gamma_i^K\right\rangle^2.
$$

所以 Q/K 的选择也同样需要两个条件：高增益和分数梯度对齐。

$W_V$ 不同，因为它不决定“谁和谁交互”，而是在交互被选中后携带内容。如果 $W_V$ 也强烈塌缩到共享关系子空间，token 特定内容会丢失。因此导师预测：

$$
W_Q,\ W_K,\ W_{\mathrm{out}}
$$

会比 $W_V$ 更强地集中组合特征。

## 6. 第五层操作化：如何把抽象问题变成实验量

导师把“组合新增特征”定义成可测对象。

对每个前缀 $F$：

$$
u_F=
\operatorname{normalize}
\left(
\mathbb{E}[h_t\mid F]
-
\mathbb{E}[h_t\mid \text{random filler}]
\right).
$$

对 $X\to Y$：

$$
u_{\mathrm{extra}}(X\to Y)
=
\operatorname{normalize}
\left(
u_Y-(u_Y^\top u_X)u_X
\right).
$$

这个定义把“新增意义”变成了隐藏方向中不能由旧前缀解释的部分。

然后用 top-$k$ 奇异向量质量衡量集中度：

$$
M_k(u)=\sum_{i=1}^k \langle u,v_i\rangle^2.
$$

如果 $M_k$ 高，说明该特征主要落在矩阵的顶部奇异子空间里。

## 7. 第六层证据：实验支持哪些链条

实验支持三件事。

第一，模型确实学会了任务。$d=64$ 下所有结构化续写都是 $100\%$ accuracy，所以后续几何分析不是失败训练的残余。

第二，新增特征不是同一个方向。额外特征的平均距离约 $1.372$，接近正交距离 $1.414$。这排除了“所有新增特征都塌成同一向量”的解释。

第三，不同新增特征虽然方向不同，却共享 $W_{\mathrm{out}}$ 的高增益 top 子空间。多数 internal transition 在 $W_{\mathrm{out}}$ top-10 隐藏侧质量为 $86\%-94\%$。这支持关键区分：

$$
\text{different feature direction} \neq \text{different singular subspace}.
$$

第四，Q/K 和 V 的角色分化符合预测。$W_Q$ input side 平均 top-10 mass 为 $52.4\%$，$W_K$ 为 $49.8\%$，而 $W_V$ 只有 $6.2\%$。这支持“Q/K 负责关系路由，V 负责内容携带”的机制分工。

第五，增加维度没有消除集中。$d=32$ 到 $d=64$ 后，集中略有缓解但定性模式仍在，说明简单加宽模型不自动解决共享子空间复用。

## 8. 第七层解释：为什么这会造成 interference

“干扰”在这里不是泛泛说法，而是有一个线性代数机制。

若两个特征为：

$$
h_f=\sum_i c_{f,i}v_i,\qquad h_g=\sum_i c_{g,i}v_i,
$$

它们在共享 top-$k$ 方向上的重叠会被大奇异值放大到输出：

$$
Wh_f=\sum_i\sigma_i c_{f,i}u_i.
$$

因此，小的表示重叠也可能变成大的输出影响重叠。梯度同样经过 $W^\top$ 被放大，所以训练常见特征时更新的高增益方向，也会影响稀有特征。

这给出导师的最终权衡：

共享高增益子空间提高学习效率，因为相关特征复用已有计算；但它也把特征耦合在一起，长尾特征必须在已经被常见特征主导的子空间里争夺表达空间。

## 9. 这条链条的最强版本

最强但仍守边界的版本是：

1. 组合任务天然包含“继承 + 新增”结构。
2. 高频简单成分更早、更反复地降低损失。
3. 这些反复梯度会塑造高增益奇异方向。
4. 后来的组合新增特征，如果预测误差和这些方向对齐，就会因为下降效率更高而复用它们。
5. 对 Q/K，这种复用体现在关系路由和 attention margin 上；softmax 会进一步放大 score gap。
6. 对 V，任务要求保留 token 特定内容，所以集中较弱。
7. 因此，组合学习形成一个紧凑的高增益子空间。
8. 该子空间同时带来复用效率和特征干扰。

一句话：

**导师在把“组合语义”改写成“交叉熵下降如何塑造参数几何”，再从参数几何推出“复用和干扰为何同源”。**

## 10. 主要薄弱点和 rival explanations

### 10.1 训练时间因果还不够直接

观察到最终 top singular mass，并不自动证明早期高频特征先创造了这些 singular directions。可能的 rival explanation 是：任务本身低秩，最终解自然低秩；不一定需要“早期频繁特征先塑造”的时间顺序。

需要的证据：训练过程中跟踪 singular values、feature projection、频率条件和学习顺序，证明高频/simple 特征先进入 top subspace，后来的 extra features 再被吸入。

### 10.2 高 top-k mass 不等于因果使用

一个特征落在 top singular subspace 中，不代表模型必须使用这部分来完成预测。它可能是相关但非必要的几何现象。

需要的证据：投影删除或方向替换干预。比如移除 $h_{\mathrm{top}}$ 是否损害预测和注意力路由，移除 $h_{\mathrm{tail}}$ 是否只影响特异性。

### 10.3 嵌套前缀不是自然语言组合性的充分代理

前缀链只有一个非常干净的继承结构。自然语言有歧义、并列组合、层级句法、世界知识和多任务语义。当前实验只能支持“嵌套续写组合”这个边界。

需要的证据：半自然短语、频率控制、常见/稀有语义对，以及真实语料上的可解释定义。

### 10.4 terminal transition 是异常点

$ABCDEFG\to ABCDEFG.$ 的 $W_{\mathrm{out}}$ top-10 mass 只有 $16.9\%$，明显不同于内部转移。这可能说明终止标记和“继续链条”不是同一机制，不能被平均进同一个 conclusion。

需要的处理：把 internal continuation 和 terminal boundary 分开报告。

### 10.5 SVD basis 本身随训练变化

导师的梯度推导在局部固定 $W$ 的 SVD 下成立。但训练中 $W$ 和其奇异向量也在变化。最终版主张应避免说成静态几何决定一切，而应说“局部下降偏置和训练动态共同形成吸引”。

## 11. 和当前主线的关系

当前 expert specialization 主线关心的是：MoE 路由是否能形成稳定、可解释、可复用的 feature-level specialization，并且要先区分 slot、$B_i$、$(slot,B_i)$，再谈 utility binding。

这篇稿子不是直接替代当前 anchor 的结论。它更像一个上游机制解释：

- common-offset / common-logit 为什么可能在早期形成；
- 为什么常见成分会吸引后续特征；
- 为什么 route purity 或 same-feature consistency 可能只是共享高增益子空间的几何后果，而不是功能性 specialization；
- 为什么长尾/rare feature 可能被 common-feature subspace 干扰。

主线影响判断：

| 项 | 判断 |
|---|---|
| affects hypothesis? | yes，它提供“高频共同成分塑造高增益方向”的机制候选 |
| affects claim boundary? | yes，它提醒不能把共享子空间直接等同于干净 feature specialization |
| affects next decision? | unclear，除非下一步要设计 anti-common / anti-lockin 机制或频率实验 |
| recommendation | pursue as mechanism note; 不自动更新 graph/anchor，除非用户要把它并入主线 |

## 12. 下一步最小决策

如果要继续沿导师这条 research chain 推进，最小决策不是立刻扩大自然语言实验，而是先选一个因果检验：

1. 训练时间证据：记录 simple/common features 是否先占据 top singular subspace。
2. 因果干预证据：删除 top singular projection 是否同时损害 common 和 rare features。
3. 频率对照证据：common 和 rare compositions 是否竞争同一个 high-gain subspace。

我建议优先做第 2 个，因为它最直接检验“共享高增益子空间是否被模型因果使用”，能把几何相关性推进到机制证据。

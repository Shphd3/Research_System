# 0930｜自然 NTP 下的更新相容性：两轮 Reasoning 审计报告

> 状态：AI_DRAFT_AWAITING_HUMAN_CONFIRMATION  
> 目的：把“局部更新机制 → 自然文本联合分布 → 表征可预测性 → PCA / SAE 比较 → 后续 Router”串成一个可检验的研究链。  
> 注意：本文不批准新实验，不改变现有 Focus / Anchor / Protocol。所有新定义、指标与实验选择均为 AI_PROPOSAL，等待研究者判断。

---

## 一、第一轮 Reasoning：先把科学对象固定下来

### 1. Parent question

长期问题不是“SAE 有没有用”或“Router 应该是不是低秩”，而是：

> **在共享参数学习中，哪些自然文本数据适合一起学，哪些数据的更新需求不相容，从而可能值得分开？**

现有自然文本证据已经说明：领域表征可分与跨领域平均互助可以同时存在。因此，“领域不同”或“静态表征可分”都不能直接作为分开的依据。

### 2. 已建立的局部数学机制

固定模型状态 \(\theta_0\)，考虑一个共享线性参数块

\[
a = Wc+b.
\]

对一个 NTP 预测事件 \(z_i=(x_i,y_i)\)：

- \(x_i\)：真实自然文本前缀；
- \(y_i\)：该前缀的真实 next token；
- \(c_i\)：进入共享矩阵 \(W\) 的输入表征；
- \(a_i\)：\(W\) 的输出表征；
- \(e_i=\partial\ell_i/\partial a_i\)：该目标损失对输出表征的误差信号。

若该单目标损失对 \(W\) 的梯度只来自这一位置，则

\[
G_i = e_i c_i^\top.
\]

更一般地，若多个位置共同贡献，则保留真实聚合：

\[
G_i=\sum_t e_{it}c_{it}^\top.
\]

两条数据的局部更新相容性定义为

\[
K_{ij}=\langle G_i,G_j\rangle_F.
\]

在单位置情形下，

\[
K_{ij}
=(c_i^\top c_j)(e_i^\top e_j).
\]

若对 \(i\) 作普通小步 SGD 更新

\[
\Delta W_i=-\eta G_i,
\]

则对 \(j\) 的真实有限步后果定义为

\[
I_{i\to j}(\eta)
=
\ell_j(W+\Delta W_i)-\ell_j(W),
\]

并有局部展开

\[
I_{i\to j}(\eta)
=
-\eta K_{ij}+R_{i\to j}(\eta).
\]

因此：

- \(K_{ij}>0\)：局部一阶上互相帮助；
- \(K_{ij}<0\)：局部一阶上互相冲突；
- \(I_{i\to j}\) 才是实际有限步、有向的后果。

**这里已经完成的是局部机制，不是长期 shared-vs-separate 训练决策。**

### 3. Toy model 真正证明了什么

受控 label-flip toy 的价值是证明：

> **静态表征几何本身不能在“任意任务规则”下唯一决定更新符号。**

它并没有证明真实自然 NTP 中表征没有预测力。

真实 NTP 的数据来自同一个联合分布：

\[
(X,Y)\sim P_{\rm NTP},
\]

其中

\[
C=f_{\theta_0}(X),
\qquad
E=e_{\theta_0}(X,Y).
\]

因此 \(C,Y,E\) 不是任意拼接，而是同一自然语言分布与同一模型状态共同诱导出来的随机变量。

### 4. 从 toy 机制进入自然文本：新的数学问题

真正的新问题不是“表征决定不决定梯度”，而是：

\[
\boxed{
P(K_{ij}\mid c_i,c_j)
\text{ 是否具有稳定、可预测的结构？}
}
\]

定义条件均值

\[
\mu_K(c_i,c_j)
=
\mathbb E[K_{ij}\mid C_i=c_i,C_j=c_j],
\]

条件方差

\[
\sigma_K^2(c_i,c_j)
=
\operatorname{Var}(K_{ij}\mid C_i=c_i,C_j=c_j).
\]

在单位置线性块下，

\[
\mu_K(c_i,c_j)
=
(c_i^\top c_j)
\mathbb E[e_i^\top e_j\mid c_i,c_j],
\]

以及

\[
\sigma_K^2(c_i,c_j)
=
(c_i^\top c_j)^2
\operatorname{Var}(e_i^\top e_j\mid c_i,c_j).
\]

这两个式子把机制与表征研究真正接起来：

- 表征几何 \(c_i^\top c_j\) 是显式可见因子；
- 隐含难点是：在自然 NTP 下，误差信号相容性 \(e_i^\top e_j\) 是否能被当前表征统计性地预测；
- 若条件均值有稳定结构、条件方差不大，则 representation-only predictor 有可能；
- 若条件方差很大，则仅凭当前表征存在内在信息限制。

---

## 二、第一轮后得到的核心实验问题

> **在固定模型状态与固定 NTP 目标下，仅使用更新前可见的完整表征，能否在未见自然文本上预测真实局部更新相容性 \(K_{ij}\)，并进一步对应实际有限步后果 \(I_{i\to j}\)？**

这比“能不能分类领域”“SAE common 多不多”“PCA 方差高不高”更接近 Router 最终真正需要的依据。

---

# 三、第二轮 Reasoning：对第一轮方案做审计

第二轮主要检查：对象是否混用、信息是否泄漏、pair 是否伪独立、PCA/SAE 是否在错误空间上比较、局部预测是否被越级解释成 Router 收益。

## 1. 修正一：先预测连续相容性，不先做 help/harm 二分类

已有自然文本结果在领域平均层面普遍是帮助，直接训练 help/harm classifier 很容易退化成多数类预测。

因此第一阶段主对象建议保持连续：

\[
K_{ij}=\langle G_i,G_j\rangle_F.
\]

辅助诊断再报告归一化方向相容性

\[
\kappa_{ij}
=
\frac{\langle G_i,G_j\rangle_F}
{\|G_i\|_F\|G_j\|_F},
\]

以及有限步

\[
I_{i\to j}.
\]

含义：

- \(K\)：真实一阶相互作用强度与符号；
- \(\kappa\)：排除梯度范数后的方向相容性；
- \(I\)：有限步实际后果。

不能把三者当成同一个量。

## 2. 修正二：预测器允许的信息必须冻结

测试时 representation-only predictor 只能看到更新前的表示，例如

\[
q(c_i,c_j).
\]

**禁止作为测试输入：**

- 真 next token \(y_i,y_j\)；
- loss；
- \(e_i,e_j\)；
- \(G_i,G_j\)；
- \(K_{ij}\)；
- 人工领域标签。

训练阶段可以使用 \(K_{ij}\) 作监督，这应如实称为“用梯度监督学习一个事前表征预测器”，不能说整个方法“不需要梯度”。

## 3. 修正三：训练/测试必须先按文档分割，再组成 pair

数据对并不是独立样本。若一条文本同时出现在 train pair 和 test pair 中，即使另一端不同，也会造成严重泄漏。

因此：

1. 先按原始文档或近重复组拆 train/dev/test；
2. 再在各自内部构造 pair；
3. 不允许一端跨 split；
4. 统计不确定性按文档/来源层级处理，而不是把大量 pair 当独立重复。

## 4. 修正四：\(K\) 对称，\(I\) 有向

\[
K_{ij}=K_{ji}
\]

但

\[
I_{i\to j}\neq I_{j\to i}
\]

在有限步、归一化更新或真实优化器下通常成立。

因此：

- 学 \(K\) 的 predictor 应显式满足对称性；
- 有限步验证必须分别测 \(i\to j\) 和 \(j\to i\)。

## 5. 修正五：现有 SAE 与机制输入 \(c\) 不在同一空间

现有 SAE 主要编码的是共享矩阵输出表征 \(a\)，而局部梯度的输入因子是 \(c\)。

因此必须做同空间比较：

- 若研究 \(c\)：比较 full-\(c\)、PCA(\(c\))、随机子空间(\(c\))；若要 SAE(\(c\))，需另有编码器；
- 若使用现有 SAE：应先比较 full-\(a\) 与 SAE(\(a\))，不能把 SAE(\(a\)) 直接和 full-\(c\) 的性能差异全归因于“稀疏化”。

这也是为什么现阶段最好把 \(c\) 与 \(a\) 都保存。

## 6. 修正六：PCA/SAE 是“信息保留测试”，不是机制本身

### PCA

在训练集上拟合 \(P_k\)，得到

\[
u_i=P_k^\top(c_i-\bar c).
\]

用相同类型 predictor 预测 \(K_{ij}\)：

\[
q_k(u_i,u_j)\to K_{ij}.
\]

画

\[
\text{prediction quality}(k)
\]

随维数 \(k\) 的曲线，并与同秩随机子空间比较。

PCA 回答：

> **与更新相容性有关的预测信息是否集中在高方差低维子空间？**

它不回答：

> “PCA 主方向是不是模型真实更新路径。”

### SAE

对现有 SAE 的输出空间 \(a\)：

\[
z_i=E_{\rm SAE}(a_i).
\]

比较

\[
q_a(a_i,a_j)
\]

与

\[
q_{\rm SAE}(z_i,z_j).
\]

SAE 回答：

> **稀疏代码是否保留了 full-\(a\) 中关于更新相容性的预测信息？**

不是：

> “SAE common 原子就是干扰空间。”

如果 SAE 成功，可以进一步分析哪些原子/原子组合对预测最重要；如果失败，只能说明当前 SAE 表示没有保留足够预测信息，不能否定所有 SAE。

---

# 四、建议的具体分析顺序

## Stage A｜测量自然 NTP 的真值

固定一个 checkpoint \(\theta_0\) 和一个共享线性参数块 \(W\)。

候选数据单位：

\[
z_i=(x_{i,<t},y_i=x_{i,t})
\]

即自然文本前缀 + 一个真实下一词预测事件。

对每个事件保存：

\[
c_i,\quad a_i,\quad e_i,\quad G_i,\quad \ell_i.
\]

先做 autograd identity check：

- 单位置是否确实满足 \(G_i=e_ic_i^\top\)；
- 若不满足，则保留真实多位置求和，不强行使用单外积公式。

输出 pair 真值：

\[
K_{ij}=\langle G_i,G_j\rangle_F,
\qquad
\kappa_{ij},
\]

以及一部分 pair 的实际有限步

\[
I_{i\to j}(\eta).
\]

## Stage B｜先做最简单的 representation-only baseline

### B0：常数 / base-rate

预测训练集平均 \(K\)。

### B1：简单几何

只用

\[
\|c_i\|,\ \|c_j\|,\ c_i^\top c_j,\ \cos(c_i,c_j)
\]

预测 \(K\)。

这一步回答：

> 简单几何本身是否已足够？

### B2：完整表征 predictor

AI_PROPOSAL：使用一个对称的 Siamese predictor

\[
u_i=\phi(c_i),
\qquad
\widehat K_{ij}
=
\rho\bigl(
 u_i+u_j,\ |u_i-u_j|,\ u_i\odot u_j
\bigr).
\]

测试时只输入 \(c_i,c_j\)。

这一模型不预设低秩，也不预设 SAE。

第一阶段真正关键的结果不是“模型多强”，而是：

> full representation 是否在 unseen documents 上稳定优于常数和简单几何。

## Stage C｜估计“表征能解释多少”

用 held-out 预测残差近似检查：

\[
K_{ij}
=
\widehat\mu_K(c_i,c_j)+\epsilon_{ij}.
\]

观察：

- out-of-sample \(R^2\) / rank correlation；
- residual variance；
- residual 是否随领域、token frequency、model confidence 等系统偏移。

这一步对应我们数学模型中的：

\[
\mu_K(c_i,c_j)
\]

和剩余的不确定性。

## Stage D｜如果 full representation 有预测力，再问结构是什么

### D1：PCA rank curve

比较不同 \(k\)：

\[
q_k(P_k^\top c_i,P_k^\top c_j)\to K_{ij}.
\]

同时做同秩随机空间。

若很小 \(k\) 已接近 full-\(c\)，才支持“预测信息集中在低维结构”。

### D2：full-\(a\) vs SAE(\(a\))

先测

\[
q_a(a_i,a_j),
\]

再测

\[
q_{\rm SAE}(z_i,z_j).
\]

若 SAE 接近 full-\(a\)，说明当前 SAE 对这类预测信息保留较好。

### D3：以后才考虑 supervised compatibility subspace

如果 full-\(c\) 有效但 PCA/SAE 都不理想，可以再学习：

\[
r_i=P^\top c_i
\]

使 pairwise compatibility prediction 最好。

这时的 \(P\) 才是真正由“共享相容性”监督定义的候选路由子空间，而不是先验指定的 PCA/SAE 空间。

## Stage E｜有限步真实性检查

不能只停在 \(K\)。

在 test set 上只根据 predictor 的预测选择预先定义的高/中/低相容性区间，然后实际做：

\[
W'=W+\Delta W_i
\]

测

\[
I_{i\to j}.
\]

要求：

- 来源 \(i\) 自身确实改善；
- \(K\) 与实际 \(I\) 在小步下关系成立；
- 两个步长用于观察余项；
- 不用真实 \(K\) 或 \(I\) 事后挑 pair。

这样才能从“预测梯度内积”升级成“预测真实一步后果”。

---

# 五、不同结果分别说明什么

| 结果 | 允许的认识更新 |
|---|---|
| simple geometry ≈ full representation | 更新相容性主要可由简单几何关系预测；复杂表征模型可能没有必要 |
| full representation > simple geometry | 表征中存在超出简单相似度的 pair-specific compatibility 信息 |
| PCA 小 \(k\) ≈ full | 预测信息集中在一个较低维、高方差相关结构中 |
| SAE ≈ full-\(a\)，优于同容量基线 | 当前 SAE 稀疏表示保留了较多 compatibility 预测信息 |
| full-\(c\) 有效、full-\(a\)/SAE 弱 | 与更新相容性有关的信息在机制输入侧更明显，输出映射或当前 SAE 丢失了信息 |
| full representation 也预测很弱 | chosen representation-only operationalization 不足；不能说“所有表征都无信息” |
| 几乎所有 \(K>0\) | 先研究帮助强弱/排序，不硬造 help-harm 分类 |
| \(K\) 可预测但有限步 \(I\) 不跟随 | 一阶 compatibility 不足以代表实际一步后果，必须研究曲率/归一化/优化器作用 |

---

# 六、第二轮后的核心结论

现在最值得固定的不是：

> “SAE/PCA 能否找到干扰子空间？”

而是：

> **在固定 NTP 任务和模型状态下，更新前完整表征是否包含对真实更新相容性 \(K\) 的可泛化预测信息？如果有，这些信息以什么结构存在，PCA 或 SAE 分别保留了多少？**

这一步成立以后，Router 才真正有一个可学习的目标。

---

# 七、组会应怎样从头讲到这个问题

## 第一段｜为什么我们要研究这个问题

> 我们最终想判断哪些数据适合共享 Expert。以前容易把“语义不同”“表征可分”直接理解成应该分开，但已有自然文本实验发现：不同领域表征可以明显不同，同时一步更新仍然平均互相帮助。因此，语义或静态可分性本身不是共享/分开的判据。

## 第二段｜我们先补了什么机制

> 我们把一次共享参数更新写开。对于一个共享线性参数块，一条数据的梯度由输入表征 \(c\) 和下游误差信号 \(e\) 的外积形成；两条数据的局部更新相容性为
>
> \[
> K_{ij}=(c_i^\top c_j)(e_i^\top e_j).
> \]
>
> 所以表征关系只解释“更新怎样耦合”的一部分，最终是帮助还是冲突还与下游损失信号有关。

## 第三段｜toy model 给了什么、没给什么

> 受控任务证明了：如果人为保持表征不变而翻转任务规则，更新后果可以改变，因此静态表征不可能对任意任务都唯一决定梯度。但这只是一般信息边界，不等于自然语言里表征不能预测。

## 第四段｜为什么真实 NTP 是新的问题

> 真实预训练始终做同一个 Next Token Prediction。上下文、真实 next token、表征和误差信号都来自同一个自然文本分布和同一个模型状态，因此它们不是任意组合的。新的问题就变成：在这个真实联合分布里，更新相容性是否具有能被更新前表征预测的条件统计结构？

写成：

\[
P(K_{ij}\mid c_i,c_j).
\]

## 第五段｜现在要做什么

> 所以我们不先设计 Router，也不先假设低秩。先在真实自然文本上测每条数据的真实梯度和 pairwise compatibility，再只给 predictor 看更新前表征，测试它能否在新文档上预测 \(K\)。

然后依次比较：

\[
\text{constant}
\rightarrow
\text{simple geometry}
\rightarrow
\text{full representation}
\rightarrow
\text{PCA / SAE}.
\]

## 第六段｜结果如何决定下一步

> 如果完整表征都预测不了，就没有理由现在设计 representation-only Router；如果完整表征能预测，再看信息是否集中在 PCA 低维空间、SAE 稀疏特征或其他结构。只有到这里，Router 的具体形式才应该由实验结果决定。

---

# 八、这次组会最核心的一句话

> **我们已经从 toy model 得到了局部共享更新的机制，但现在真正要进入自然语言场景：检验在固定 NTP 任务下，真实文本表征中是否存在能够事前预测更新相容性的统计结构；如果存在，再研究这种信息是否可以被 PCA、SAE 或其他紧凑表示保留下来。**

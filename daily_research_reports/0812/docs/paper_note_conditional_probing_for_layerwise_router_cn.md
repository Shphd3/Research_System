---
type: paper_reading_note
status: AI_DRAFT_FOR_RESEARCHER_READING
date: 2026-08-12
paper: "Conditional probing: measuring usable information beyond a baseline"
authors: "John Hewitt, Kawin Ethayarajh, Percy Liang, Christopher D. Manning"
source: "https://arxiv.org/abs/2109.09234"
publication: "EMNLP 2021; https://aclanthology.org/2021.emnlp-main.122/"
mainline: "A15 Layer-wise Router: defining layer-added usable information"
---

# 一层相对旧状态到底新增了什么可用信息？——Conditional Probing 精读

## 先读结论

这篇论文最值得我们学的不是一种新的 probe，而是一个**比较逻辑**：如果想知道表征 $R$ 是否提供了基准表征 $B$ 中没有的目标信息，不能比较“$R$ 单独有多好”和“$B$ 单独有多好”，而应该比较：

$$
\boxed{
\text{只给 }B
\quad\text{vs.}\quad
\text{同时给 }(B,R)
}
$$

两者在留出数据上的交叉熵差，度量的是在指定预测器家族 $\mathcal V$ 中，$R$ 在 $B$ 之外增加了多少**可用信息**。

映射到我们的 Layer-wise Router：

- $B$ 可以是本层 Attention 写入之前的旧状态 $X_\ell$；
- $R$ 可以是本层精确更新 $U_\ell$，或其中不能被 $X_\ell$ 预测的部分 $R_{U,\ell}$；
- $Y$ 必须是我们真正希望 Router 使用的目标，例如目标语义、最佳专家身份或专家相对效用；
- 共同参数基只负责描述增量“位于哪里”，不负责定义它是不是新增可用信息。

最重要的边界是：conditional probing 建立的是**指定预测器家族下的留出可访问性**，不是 Shannon 意义的信息创造，也不是模型原生使用，更不是 Router 已经获得收益。

---

## 1. 为什么这篇论文正好击中我们当前的困难

我们此前反复把下列对象混在一起：

1. Attention 输出非零；
2. 两层方差谱不同；
3. 某个标签能从 Attention 输出单独读出来；
4. Attention 输出在旧状态之外增加了标签可预测性；
5. Router 或模型真的利用这部分信号降低了任务损失。

这五件事由弱到强，不能互相替代。Conditional Probing 精确处理的是第 4 件事：

> 已知基准表征以后，另一个表征是否还提供额外、可被指定计算家族提取的目标信息？

因此它帮助我们把研究问题从：

> “第 9 层 Attention 输出的方差落在哪个谱带？”

改成：

> “给定第 9 层写入前已经存在的状态以后，第 9 层更新是否还降低了目标预测风险？”

后一个问题才有资格接近“层新增可用信息”。

---

## 2. 先用一个数值例子理解

假设我们要预测三类目标 $Y$。

- 只给旧状态 $B$ 时，测试交叉熵是 $0.90$ nats；
- 只给新表征 $R$ 时，测试交叉熵是 $1.00$ nats；
- 同时给 $(B,R)$ 时，测试交叉熵是 $0.65$ nats。

如果做普通的 baseline 比较，会得到：

$$
0.90-1.00=-0.10,
$$

于是可能错误地说：$R$ 比 $B$ 差，没有信息。

但真正的问题是：$R$ 是否补充了 $B$。正确比较为：

$$
0.90-0.65=0.25\ \text{nats}.
$$

这表示：虽然 $R$ 单独不如 $B$，但它提供了 $B$ 没有的互补区分，使测试交叉熵降低了 $0.25$ nats/example。

这正是我们此前容易忽略的情形：

> 深层更新不必独自携带全部语义；它只需要补上旧状态缺少的那一部分。

---

## 3. 数学由浅入深

### 3.1 第一级：交叉熵是在测什么

预测器看到表征 $R$ 后输出标签分布 $f(R)$。对真实标签 $Y$，交叉熵风险为：

$$
\mathcal R(f;R,Y)
=
\mathbb E[-\log f(R)[Y]].
$$

如果模型给真实标签更高概率，$-\log p$ 更小，风险就更低。因此“加入一个表征以后测试交叉熵下降”可以理解为：该表征让目标在当前预测器能力范围内更容易被预测。

对数底决定单位：

- 自然对数：nats/example；
- 以 2 为底：bits/example。

论文的图表使用 bits；我们 A15_08 的记录使用 nats。二者只差一个常数：

$$
1\ \text{nat}=\frac{1}{\ln 2}\approx1.443\ \text{bits}.
$$

不能把交叉熵下降直接叫作“模型创造了多少 bit 的知识”；它只是在指定预测任务和预测器家族中的风险差。

### 3.2 第二级：为什么要指定预测器家族 $\mathcal V$

令 $\mathcal V$ 是允许使用的一组预测器，例如：

- 所有 affine-softmax 线性 probe；
- 固定宽度的一层 MLP；
- 与实际 Router 同结构的小网络。

论文定义 $\mathcal V$-entropy：

$$
H_{\mathcal V}(Y\mid R)
=
\inf_{f\in\mathcal V}
\mathbb E[-\log f(R)[Y]].
$$

白话解释：

> 在只允许使用 $\mathcal V$ 这套工具时，预测 $Y$ 最少还剩多少不确定性？

这里的 $\inf$ 表示在这个函数家族中寻找理论上最好的预测器。实际训练只能近似这个最优值，因此实验必须使用训练集拟合，在独立测试集估计风险。

为什么不直接使用互信息？如果两个表征由可逆变换关联，例如一个是容易读取的明文，另一个是难以解码的密文，它们与标签的 Shannon 互信息可以相同。但对线性预测器而言，明文显然更有用。$\mathcal V$-information 刻画的正是这种**计算约束下的可用性**。

### 3.3 第三级：单变量 $\mathcal V$-information

不知道 $R$ 时，对 $Y$ 的最佳风险记为 $H_{\mathcal V}(Y)$；知道 $R$ 后为 $H_{\mathcal V}(Y\mid R)$。二者之差为：

$$
I_{\mathcal V}(R\rightarrow Y)
=
H_{\mathcal V}(Y)
-H_{\mathcal V}(Y\mid R).
$$

箭头 $R\rightarrow Y$ 不是因果箭头。它表示 $R$ 被用作预测 $Y$ 的输入。

### 3.4 第四级：条件 $\mathcal V$-information

现在我们已经知道基准 $B$，再问 $R$ 增加多少可用信息：

$$
\boxed{
I_{\mathcal V}(R\rightarrow Y\mid B)
=
H_{\mathcal V}(Y\mid B)
-
H_{\mathcal V}(Y\mid B,R)
}
$$

这就是全文最关键的公式。

- 第一项：给定旧信息 $B$ 后，目标还剩多少预测困难；
- 第二项：再加入 $R$ 后，目标还剩多少预测困难；
- 差值：$R$ 填补了多少旧信息的缺口。

实验实现为两个匹配 probe：

$$
f_0([B;\mathbf 0])
\quad\text{和}\quad
f_1([B;R]).
$$

其中零向量只是“没有提供 $R$”的占位符，也可以直接只输入 $B$。保持相同输入接口和预测器家族，可以减少模型容量差异造成的混淆。

若性能定义成负交叉熵，则 conditional probing score 为：

$$
\operatorname{Perf}([B;R])
-
\operatorname{Perf}([B;\mathbf0])
=
CE(B)-CE(B,R).
$$

### 3.5 第五级：为什么理论值应当非负

论文要求预测器家族满足“可选择忽略输入”（optional ignorance）：加入 $R$ 后，预测器仍然可以把对应权重设为零，退化成只使用 $B$。

所以允许使用 $(B,R)$ 的最优风险不会高于只允许使用 $B$ 的最优风险：

$$
H_{\mathcal V}(Y\mid B,R)
\le
H_{\mathcal V}(Y\mid B).
$$

因此：

$$
I_{\mathcal V}(R\rightarrow Y\mid B)\ge0.
$$

实际实验中估计值可能轻微为负，因为有限数据、优化误差和正则化会使两个 probe 都没有达到各自最优。负值不能被解释为“加入信息真的有害”；首先应视为估计、训练或匹配问题。

### 3.6 第六级：确定性层为什么还能产生条件可用信息

这是理解“层新增信息”最关键、也最容易卡住的一步。

若本层更新由完整旧状态确定：

$$
U_\ell=g_\ell(X_\ell),
$$

那么在 Shannon 信息论中，知道完整 $X_\ell$ 后，$U_\ell$ 不再提供随机不确定性：

$$
I(U_\ell;Y\mid X_\ell)=0.
$$

这并不意味着本层计算毫无作用。受限预测器可能无法直接从 $X_\ell$ 读出某个复杂关系，而 $g_\ell$ 把它转换成更容易读取的特征。因此：

$$
I_{\mathcal V}(U_\ell\rightarrow Y\mid X_\ell)>0
$$

仍然可能成立。更准确的语言不是“层凭空创造了 Shannon 新信息”，而是：

> 本层计算增加了目标对指定读出器家族的可访问性。

还必须写清楚 $X_\ell$ 的观察范围。若 probe 只看到当前 token 的旧状态，而 Attention 更新读取整段上下文，那么 $U_{\ell,t}$ 还引入了 token-local baseline 看不到的上下文；若 baseline 是完整序列状态，则这种解释不再成立。两种实验回答的不是同一个“新增”。

---

## 4. 普通 baseline probing 为什么回答错了问题

普通做法比较：

$$
\operatorname{Perf}(R)-\operatorname{Perf}(B).
$$

它对应的是两个不同可用信息量之差：

$$
I_{\mathcal V}(R\rightarrow Y)
-
I_{\mathcal V}(B\rightarrow Y).
$$

它问的是：

> $R$ 单独是否比 $B$ 单独更好？

Conditional probing 问的是：

> 已经拥有 $B$ 后，$R$ 还能补充什么？

这两个问题只有在 $B$ 与 $R$ 携带完全重叠、且读取难度相似时才可能给出相似答案。层间研究恰恰不能预设这一点。

---

## 5. 论文具体做了什么

### 5.1 实验对象

作者以 ELMo 和 12 层 RoBERTa-base 为对象，预测五类语言属性：

- coarse POS（UPOS）；
- fine POS（XPOS）；
- dependency relation；
- named entity；
- SST-2 sentiment。

基准 $B$ 是非上下文词嵌入层 $\phi_0$，候选表征是各上下文层 $\phi_i$。预测器家族固定为 affine-softmax，即线性变换加 softmax。

### 5.2 关键结果

普通 baseline probing 显示 POS 信息在 RoBERTa 后层逐渐衰减；但在始终给 probe 提供输入词嵌入 $\phi_0$ 后，词嵌入不能解释的 POS 信息在更深层仍保持可访问。换言之，后层看似“丢失”的一部分主要是输入层已经提供的容易部分，而不是所有上下文化增量都消失。

对 dependency label，conditioning 缩小了层间差异；对 NER 和 sentiment，conditioning 没有改变总体趋势。这说明 conditional probing 不是必然制造一种更漂亮的新趋势，它只在 baseline 混淆确实存在时改变结论。

### 5.3 论文真正建立的结论

论文建立的是：

> 对一个明确 baseline，conditional probing 能估计指定预测器家族下，候选表征额外提供的目标可用信息，并可能揭示普通单层比较遮蔽的层间趋势。

它没有建立：

- probe 可读就等于模型原生使用；
- 表征中的信息具有因果作用；
- 新增可用信息是低秩的；
- 该信息适合作为 Router 输入；
- 任意更深层都必然增加更多信息。

---

## 6. 精确映射到我们的 A15 / Layer-wise Router

### 6.1 对象对应表

| Conditional Probing | 我们的层更新对象 | 含义 |
| --- | --- | --- |
| baseline $B$ | 写入前状态 $X_\ell$ | 本层之前已经可用的 token-local 信息 |
| representation $R$ | $U_\ell=Z_\ell-X_\ell$ 或 $R_{U,\ell}$ | 本层精确更新或旧状态不可线性预测的更新部分 |
| target $Y$ | 语义标签、终端 code、最佳专家或专家效用 | 必须由研究问题事先明确 |
| family $\mathcal V$ | 线性 probe、小 MLP 或实际 Router 家族 | 限定“可用”的计算能力 |
| conditional gain | $CE(X_\ell)-CE(X_\ell,R_{U,\ell})$ | 旧状态之外的留出目标增益 |

我们的严格对象为：

$$
X_\ell=N_\ell(h_\ell),
\qquad
Z_\ell=N_\ell(h_\ell+a_\ell),
\qquad
U_\ell=Z_\ell-X_\ell.
$$

进一步去掉可由旧状态线性预测的更新：

$$
R_{U,\ell}
=
U_\ell-\widehat{\mathbb E}_{lin}[U_\ell\mid X_\ell].
$$

然后测：

$$
G_{\ell,Y}
=
CE_{test}(f_X(X_\ell))
-
CE_{test}(f_{X+U}(X_\ell,R_{U,\ell})).
$$

这里必须避免把我们的额外控制写成论文原方法：Conditional Probing 本身直接比较 $X_\ell$ 与 $(X_\ell,U_\ell)$，**不要求先残差化**。$R_{U,\ell}$ 是我们为了隔离旧状态线性可预测部分而增加的 residual-relative 控制。

对没有额外正则约束的线性 joint probe，若 $\widehat{\mathbb E}_{lin}[U\mid X]=AX$，则：

$$
W_XX+W_U(U-AX)
=
(W_X-W_UA)X+W_UU.
$$

所以 $(X,U)$ 与 $(X,U-AX)$ 理论上表示同一个线性函数集合。若两者实验结果明显不同，首先应检查正则化、优化、数据切分或 residualizer 泄漏，而不能直接说残差化发现了另一种信息。

[A15_08 E04 的受控第 25 层结果](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/summary.md)已经建立了局部正增益；但两个候选方向只保留 33.24% 的完整增益。因此“存在新增可访问性”与“它能被二维谱方向充分压缩”必须分开判断。

### 6.2 公共基应当放在哪一步

正确顺序是：

1. 用 $X_\ell$ 与层更新定义同坐标的计算对象；
2. 用 conditional held-out gain 判断它是否包含旧状态之外的目标可用性；
3. 只有增益存在后，才把 $R_{U,\ell}$ 投到 Mean Response 基，问哪些谱带保留该增益；
4. 用同维随机/旋转子空间检查谱带是否特殊；
5. 最后才进入 Router 功能测试。

因此：

$$
\boxed{
\text{公共基是定位工具，不是新增信息定义。}
}
$$

### 6.3 对 Layer-wise Router 最重要的目标选择

如果最终目标是专家路由，仅以 coarse/fine semantic label 作为 $Y$ 还不够。语义粒度可预测，不代表不同专家处理它会产生不同效用。

更贴近 Router 的候选目标是：

$$
Y_\ell^*(x)
=
\arg\min_e \mathcal L_{\ell,e}(x),
$$

即在受控反事实评估中，哪个专家给该 token 带来最低损失；或者直接预测每个专家的边际效用向量。然后问谱带或条件更新是否在当前状态之外增加对 $Y_\ell^*$ 的预测能力。

这是本文没有提出、而是我们基于本文得到的研究推论。

---

## 7. 你当前最需要补牢的知识点

### 薄弱点一：把“表示不同”当成“新增信息”

方差、均值、谱位置或 CKA 不同只能说明表示发生变化。新增可用信息需要一个目标 $Y$ 和旧状态 baseline，并在留出数据上证明风险下降。

### 薄弱点二：把“单独可读”当成“在旧状态之外有用”

$U_\ell$ 单独能预测 $Y$，可能只是重复编码 $X_\ell$ 已有的信息。必须比较 $X_\ell$ 与 $(X_\ell,U_\ell)$。

### 薄弱点三：认为“信息”是与预测器无关的绝对对象

线性 Router 读不到、复杂 MLP 能读到的信息，对两种系统的工程价值不同。任何“可用信息”结论都必须带上 $\mathcal V$。

### 薄弱点四：从可读性跳到模型使用或 Router 收益

Probe 是观察工具。只有对候选信号做删除、替换、保留或实际路由干预，并观察任务损失/专家 regret，才能谈功能使用。

### 薄弱点五：没有先定义 $Y$

“新信息”不是无目标的。若 $Y$ 是 domain、semantic granularity、下一词、终端 code、最佳专家，它们定义的是完全不同的研究对象。Layer-wise Router 最终应以专家相对效用或任务损失为目标，而不仅是容易构造的语义标签。

---

## 8. 用这篇论文诱导自己思考

请先独立写下答案，再看后面的提示。

### 问题 1

如果 $U_\ell$ 单独预测 fine label 的 accuracy 很高，但加入 $X_\ell$ 后几乎不再降低交叉熵，你能声称什么？

提示：它说明 $U_\ell$ 可读，但大部分可能与旧状态冗余；不能称为本层新增的 fine 信息。

### 问题 2

如果 F9--F12 能区分 fine/coarse，却不能增加最佳专家身份的条件预测，你还会把它作为 Router 输入吗？

提示：它仍可作为语义解释坐标，但缺乏路由目标上的准入证据。

### 问题 3

为什么不应直接用一个很强的大 MLP probe？

提示：强 probe 可能从微弱、分散的表征中拟合出标签，却不代表实际轻量 Router 能利用；同时更容易产生容量和过拟合混淆。$\mathcal V$ 应由部署假设而不是为了得到正结果来确定。

### 问题 4

如果要比较所有层的 $G_{\ell,Y}$，是否还必须先构造公共基？

答案：不必须。每层都可比较同一单位的留出风险下降。公共基只在进一步解释和压缩“增量落在哪里”时需要。

### 问题 5

Router 在 Attention 前作决定时，能否把该层 Attention 更新 $U_\ell$ 作为输入？

答案：不能，因为 $U_\ell$ 尚未被计算。这是信息可用时序约束。若 Router 位于 Attention 后、MLP expert 前，则可以使用该更新，但只能影响后续 MLP/专家选择，不能节省已经发生的 Attention 计算。

---

## 9. 这篇论文对主线的具体更新

### Hypothesis 更新

原假设“深层 Attention 方差向后谱迁移，所以后谱是新增信息”应被拆成：

1. 某层更新在旧状态之外是否增加目标可访问性？
2. 若增加，哪一子空间保留这部分增益？
3. 若可压缩，该子空间是否改善 Router 的匹配功能指标？

### Modeling 更新

新增信息的操作性定义应带有四个限定：

$$
\boxed{
\text{目标 }Y
+
\text{baseline }X_\ell
+
\text{预测家族 }\mathcal V
+
\text{留出风险差}
}
$$

### Experiment 更新

先比较 state-only 与 state-plus-update；再检验固定谱带相对同维随机方向保留多少条件增益。不能从方差 atlas 中事后挑选有利层或谱带。

### Interpretation 更新

“语义越细越偏后谱”是描述性语义结构；它不能自动回答“哪层新增了更细信息”，也不能回答“Router 是否应使用后谱”。

### 下一决策

在 Layer-wise Router 设计之前，先明确 Router 最终预测的 $Y$：是语义类别、是否继续计算、最佳专家身份，还是每个专家的边际效用。没有这个定义，conditional information 和 Router objective 都无法成立。

---

## 10. 一页复述卡

**论文问题：**怎样测量表征在 baseline 之外提供的可用信息？

**核心方法：**比较只用 $B$ 的 probe 与同时用 $(B,R)$ 的 probe，而不是比较 $R$-only 与 $B$-only。

**核心公式：**

$$
I_{\mathcal V}(R\rightarrow Y\mid B)
=H_{\mathcal V}(Y\mid B)-H_{\mathcal V}(Y\mid B,R).
$$

**论文结果：**conditioning on input embeddings 后，RoBERTa 深层仍保持更多此前被普通 probing 遮蔽的 POS 可用信息；其他任务不一定改变趋势。

**对我们最重要的启示：**用旧状态 $X_\ell$ 作 baseline，用层更新作补充变量，先建立目标条件下的增量可访问性；公共参数谱只用于事后定位与压缩。

**不能声称：**conditional probe 正值不证明模型原生使用、低秩、因果作用或 Router 收益。

**原始来源：**[ACL Anthology 正式论文页](https://aclanthology.org/2021.emnlp-main.122/)、[arXiv 摘要与 PDF](https://arxiv.org/abs/2109.09234)、[arXiv HTML 全文](https://arxiv.org/html/2109.09234)。

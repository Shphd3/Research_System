# 多词元预测（MTP）如何学习长程语义信息

文档状态：
- 类型：回顾性综合文档
- 来源研究线：`11_long_horizon_mtp_objective`
- 本文语言：中文
- 最后更新：2026-07-08
- 当前结论边界：只讨论受控目标函数机制；不声称自然语言收益，也不声称专家路由收益

## 0. 术语约定

本文允许保留少量核心缩写，但必须先说明含义。

| 术语 / 缩写 | 中文含义 | 本文中的具体对象 | 为什么重要 | 不能证明什么 |
|---|---|---|---|---|
| 多词元预测（MTP） | 用同一个当前状态同时预测多个未来词元 | 损失函数 $L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j)$ | 研究它是否能把远处语义目标提前监督到当前状态 | 不等于自然语言里一定更好 |
| 下一词元预测（NTP） | 只预测紧邻的下一个词元 | 损失函数 $L_1(h_T)=\operatorname{CE}(q_1(\cdot\mid h_T),Y_1)$ | 作为 MTP 的对照目标 | 不代表模型绝不会学到长程信息 |
| 语言模型式训练（LM 训练） | 像普通语言模型一样在多个位置都施加预测损失 | 本文主要对应“全位置训练” | 更接近真实训练方式 | 会引入间接迁移，不能单独说明当前状态受到直接监督 |
| 稀疏专家模型（MoE） | 由路由器选择部分专家参与计算的模型 | 本文只把它作为未来主线连接对象 | 说明 A11 与项目主线的关系 | 本文不证明专家专业化或路由收益 |
| 当前前缀状态 $h_T$ | 模型读完当前前缀后的隐藏表示 | $h_T=f_\theta(X_{\le T})$ | 我们判断长程信息是否被写入的对象 | 不代表所有位置的状态都含有该信息 |
| 早期语义变量 $Z$ | 前缀早期出现、但未来才需要的信息 | 受控数据中的分支身份或分支变量 | 长程信息的目标变量 | 不等同于自然语言语义本身 |
| 预测范围 $K$ | 当前状态要预测多少个未来词元 | $K=1,2,3,\ldots$ | 决定目标函数是否覆盖第一个需要 $Z$ 的未来位置 | 不能推出 $K$ 越大越好 |
| 第一个语义显现位置 $\tau$ | 第一个真正需要 $Z$ 的未来位置 | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | 决定 MTP 是否有直接语义监督 | 真实语言中不一定固定 |
| 直接语义监督 | 当前状态 $h_T$ 自己被要求预测含 $Z$ 的未来目标 | $\operatorname{CE}(q_\tau(\cdot\mid h_T),S_Z)$ | 这是本文的核心机制 | 不等于所有恢复 $Z$ 的路径都来自它 |
| 间接迁移 | 其他位置的损失通过共享参数让 $h_T$ 也变得可读出 $Z$ | 全位置训练中的背景损失 | 解释 K=1/K=2 在全位置训练中也可能恢复 $Z$ | 不能否定直接语义监督的存在 |

## 1. 摘要

本文的主问题是：**多词元预测（MTP）是否比下一词元预测（NTP）更有利于学习长程语义信息，尤其是否更高效地把早期语义变量写入当前前缀状态。** 当前最稳妥的结论是：MTP 不是被证明“总是更强”，而是在受控长程语义构造中，当预测范围 $K$ 覆盖第一个真正需要早期语义变量 $Z$ 的未来位置 $\tau$ 时，远处语义目标会直接监督当前前缀状态 $h_T$。因此，足够低的对应未来位置损失会推出 $h_T$ 含有 $Z$。在无噪声 $\tau=3$ 实验里，覆盖 $\tau$ 的 K=3 比 K=1/K=2 更早、更稳恢复 $Z$；A11_05 进一步说明，这个效率优势中有一部分来自当前决策前缀上的第 3 个未来位置监督。但全位置训练中还存在间接迁移，所以不能说“只有 K=3 能学到 $Z$”，也不能说已经证明自然语言里 MTP 更好。下一步应收紧优化效率论证，而不是直接扩大到 K>3。

## 2. 研究问题

**主问题：** MTP 在长程语义学习上是否比 NTP 更好；更窄地说，是否更高效？

**当前研究问题：** 当早期变量 $Z$ 不影响紧邻的下一个词元，但影响更远未来词元时，MTP 是否会让当前前缀状态 $h_T$ 更早、更稳定地包含 $Z$？

**当前可判定问题：** 在受控构造中，如果第一个包含 $Z$ 信息的未来词元在位置 $\tau$，那么当 $K\ge\tau$ 时，MTP 是否给 $h_T$ 提供直接语义监督；这个直接语义监督是否解释无噪声构造中的学习效率优势？

这条线不是在研究 MoE 路由本身。它研究的是训练目标如何塑造隐藏表示。它以后可以作为 A06 / 路由主线的候选机制，但目前不能推出专家专业化或路由收益。

## 3. 为什么这个问题容易混淆

这条线最容易混在一起的概念有五个。

| 层次 | 问题 | 当前状态 |
|---|---|---|
| 表示存在 | $h_T$ 最后是否含有 $Z$？ | 在受控“第一个语义显现位置”构造中可证明 |
| 学习效率 | $h_T$ 是否更早、更稳学到 $Z$？ | 有无噪声受控证据，但还不是无条件定理 |
| 全位置迁移 | 语言模型式全位置训练里，K=1/K=2 是否也可能恢复 $Z$？ | 会，不能说未覆盖 $\tau$ 的 K 一定学不到 |
| 本地预测保持 | MTP 是否靠牺牲 $Y_1/Y_2$ 换来 $Z$？ | 当前无噪声实验中没有看到有效本地目标被牺牲 |
| 自然语言 / MoE | 受控机制是否推出自然语言或专家路由优势？ | 不能推出，仍是未来桥接问题 |

所以本文必须收束成一句话：

> MTP 的确定机制不是“预测更多就一定更好”，而是“当预测范围覆盖第一个语义显现位置时，远处语义目标会直接监督当前状态”；学习效率优势是在这个表示约束基础上的经验性、条件性结论。

## 4. 数据和训练布局

### 4.1 K=2 最小构造

早期变量是分支变量 $B$。序列是：

$$
X=(\operatorname{BR}_B,F_1,\ldots,F_L,U,A,S_B).
$$

当前前缀状态是：

$$
h_T^{(B)}=f_\theta(\operatorname{BR}_B,F_1,\ldots,F_L,U).
$$

未来两个词元是：

$$
Y_1=A,
$$

$$
Y_2=S_B.
$$

其中 $A$ 对所有分支相同，$S_B$ 由早期分支决定，且 $B\mapsto S_B$ 一一对应。因此：

$$
I(B;Y_1)=0,
$$

$$
I(B;Y_2\mid Y_1)=H(B).
$$

直观上，当前状态只预测 $Y_1$ 时不需要知道 $B$；但如果还要预测 $Y_2=S_B$，就必须知道 $B$。

### 4.2 K=3 第一个语义显现位置构造

为了说明 K=2 不是特殊情况，我们把第一个语义显现位置推到第 3 个未来位置：

$$
X=(\operatorname{BR}_Z,F_1,\ldots,F_L,U,A,C,S_Z).
$$

当前状态是：

$$
h_T=f_\theta(\operatorname{BR}_Z,F_1,\ldots,F_L,U).
$$

未来词元是：

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

信息结构是：

$$
I(Z;Y_1)=0,
$$

$$
I(Z;Y_2\mid Y_1)=0,
$$

$$
I(Z;Y_3\mid Y_1,Y_2)=H(Z).
$$

因此第一个语义显现位置是：

$$
\tau=3.
$$

K=1 和 K=2 在当前决策前缀上不覆盖 $\tau$；K=3 覆盖 $\tau$。

### 4.3 单决策前缀训练与全位置训练

**单决策前缀训练**指损失只施加在当前研究的那个前缀状态 $h_T$ 上。它最贴近理论问题：这个状态有没有被未来语义词元直接监督？

**全位置训练**指像普通语言模型一样，在所有合法位置都训练向后 $K$ 个词元的预测损失：

$$
L_K^{all}=\sum_t\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_t),X_{t+j}).
$$

全位置训练更接近语言模型训练，但也引入一个重要边界：即使当前决策前缀上的 K 没覆盖 $\tau$，其他位置的损失也可能通过共享参数把 $Z$ 间接写进 $h_T$。这就是间接迁移。

## 5. 物理直觉

把它想成一个长故事：

第一章给了一个设定 $Z$。中间很多句子局部上都能预测，不需要 $Z$。但结尾某句话第一次真正需要 $Z$。

NTP 在每个位置只问：“下一个词元是什么？”如果下一个词元是共享的、局部可预测的，那么当前状态可以不暴露 $Z$。

MTP 在当前状态上问：“后面几个词元是什么？”如果第 $K$ 个未来词元里第一次需要 $Z$，那么这个远处词元的错误会直接作用到当前状态 $h_T$ 上。

所以 MTP 的机制可以写成：

> 未来才显现的语义相关性，被 MTP 提前变成当前隐藏状态的监督。

这个直觉只在一个条件下成立：MTP 的预测范围必须覆盖第一个语义显现位置 $\tau$。如果 $K<\tau$，预测更多但仍然没预测到含 $Z$ 的词元，就没有确定的语义优势。

## 6. 术语和指标定义

| 术语 | 中文含义 | 具体对象 / 公式 | 为什么重要 | 不能证明什么 |
|---|---|---|---|---|
| 早期语义变量 $Z$ | 前缀里出现、未来才需要的信息 | 受控数据中是分支身份 | 长程信息的目标变量 | 自然语言语义本身 |
| 当前状态 $h_T$ | 读完前缀后的隐藏状态 | $h_T=f_\theta(X_{\le T})$ | MTP 是否监督这个状态 | 后面所有状态都含 $Z$ |
| 第一个语义显现位置 $\tau$ | 第一个未来词元中真正出现 $Z$ 信息的位置 | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | 决定 K 是否覆盖有效语义目标 | 真实语言固定预测步距 |
| 覆盖条件 | MTP 预测范围包含 $\tau$ | $K\ge\tau$ | 有直接语义监督 | 一定优化成功 |
| 不覆盖条件 | MTP 预测范围未到 $\tau$ | $K<\tau$ | 当前状态没有被含 $Z$ 的目标直接监督 | 全位置训练下完全不能学 |
| 直接语义监督 | 当前状态直接预测 $S_Z$ | $\operatorname{CE}(q_\tau(\cdot\mid h_T),S_Z)$ | 这是核心机制项 | MTP 所有收益 |
| 间接迁移 | 其他位置损失通过共享参数让 $h_T$ 可读出 $Z$ | 全位置训练中的背景损失 | 解释 K=1/K=2 也能恢复 | 直接语义监督无效 |
| 保守恢复分数 $Q(t)$ | 保守判断 $h_T$ 是否含 $Z$ | $Q(t)=\min\{A(t),P(t),S(t)\}$ | 主恢复指标 | 精确因果路径 |
| 高恢复时间 $T_{0.9}$ | 可靠达到高恢复的时间 | 连续 3 次评估满足 $Q(t)\ge0.9$ 的最早训练步 | 学习效率指标 | 最终能力 |
| 早期曲线面积 | 早期 $Q(t)$ 曲线面积 | $\frac{1}{W}\int_0^W Q(t)\,dt$ | 同时衡量速度和稳定性 | 梯度因果 |
| 本地预测保护指标 | 本地下一词元预测是否被破坏 | $Y_1/Y_2$ 损失和准确率 | 排除“牺牲本地预测换长程恢复”的解释 | 全语言质量 |
| 模型自身第 3 位置准确率 | 模型自己的第 3 未来位置预测头能否预测 $S_Z$ | $\Pr[\arg\max q_3(\cdot\mid h_T)=S_Z]$ | 区分模型自身预测与外部探针可读 | 下游路由收益 |

其中 $Q(t)$ 的三个分量是：

- $A(t)$：从冻结的 $h_T$ 解码含信息后缀或分支的准确率；
- $P(t)$：独立冻结探针的 $h_T\to Z$ 准确率；
- $S(t)$：分支替换一致性，即替换早期分支词元后，读出的分支是否随之改变。

取最小值是为了避免单一探针假阳性。

## 7. 数学模型

### 7.1 NTP

NTP 在当前状态只预测紧邻的下一个词元：

$$
L_1(h_T)=\operatorname{CE}(q_1(\cdot\mid h_T),Y_1).
$$

如果 $Y_1$ 不依赖 $Z$，这个损失没有直接理由要求 $h_T$ 保存 $Z$。

### 7.2 MTP / 向后 K 词元预测

MTP 在同一个状态上预测多个未来词元：

$$
L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j).
$$

如果 $K\ge\tau$ 且 $Y_\tau=S_Z$，其中 $Z\mapsto S_Z$ 一一对应，那么目标中包含：

$$
\lambda_\tau\operatorname{CE}(q_\tau(\cdot\mid h_T),S_Z).
$$

这就是直接语义监督。

### 7.3 梯度路径

若第 $j$ 个未来位置的预测头是线性读出：

$$
z_j=W_jh_T+b_j,
$$

$$
q_j=\operatorname{softmax}(z_j),
$$

则：

$$
\nabla_{h_T}L_K
=\sum_{j=1}^{K}\lambda_j W_j^\top(q_j-e_{Y_j}).
$$

当 $Y_\tau=S_Z$ 时，其中包含：

$$
\lambda_\tau W_\tau^\top(q_\tau-e_{S_Z}),
$$

这个项直接依赖 $Z$。这说明 MTP 提供了直接梯度路径，但还不能单独证明优化一定更快。

## 8. 定理和证明状态

### 8.1 K=2 分支不可区分状态的下界

在 K=2 构造中，如果当前状态不区分分支：

$$
h_T^{(1)}=\cdots=h_T^{(m)}=c,
$$

则任何只看 $h_T$ 的预测器都必须对所有分支使用同一个分布。由于 $S_B$ 在 $m$ 个不同词元上均匀分布：

$$
\inf_q\mathbb E[-\log q(S_B\mid h_T)]=\log m.
$$

所以不区分分支的 $h_T$ 不可能以低损失预测 $S_B$。

### 8.2 K=2 NTP 不强迫分支信息

NTP 只预测：

$$
Y_1=A.
$$

因为 $A$ 对所有分支共享，一个不区分分支的状态也可以令：

$$
q_1(A\mid c)=1.
$$

因此 NTP 在这个前缀上可以损失很低，但 $h_T$ 不含 $B$。

### 8.3 K=2 MTP 低损失推出 $h_T$ 含 $B$

向后两个词元预测损失是：

$$
L_2(h_T)=\operatorname{CE}(q_1,A)+\lambda\operatorname{CE}(q_2,S_B).
$$

如果：

$$
\mathbb E[-\log q_2(S_B\mid h_T)]\le\varepsilon,
$$

则：

$$
I(h_T;B)\ge H(B)-\varepsilon.
$$

证明核心是：交叉熵上界条件熵。

$$
H(S_B\mid h_T)\le \mathbb E[-\log q_2(S_B\mid h_T)]\le\varepsilon.
$$

又因为 $B\mapsto S_B$ 一一对应：

$$
H(B\mid h_T)=H(S_B\mid h_T).
$$

所以：

$$
I(h_T;B)=H(B)-H(B\mid h_T)\ge H(B)-\varepsilon.
$$

### 8.4 一般 K 的覆盖定理

令：

$$
\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}.
$$

**非覆盖定理：** 如果 $K<\tau$ 且 $Y_{1:K}$ 不含 $Z$ 信息，那么存在不含 $Z$ 的 $h_T$ 可以完成所有有效预测目标。因此，未覆盖 $\tau$ 的预测范围不强迫 $h_T$ 含 $Z$。

**覆盖定理：** 如果 $K\ge\tau$、$\lambda_\tau>0$、$Y_\tau=S_Z$，且 $Z\mapsto S_Z$ 一一对应，那么：

$$
\mathbb E[-\log q_\tau(S_Z\mid h_T)]\le\varepsilon
$$

推出：

$$
I(h_T;Z)\ge H(Z)-\varepsilon.
$$

如果只知道加权损失项：

$$
\lambda_\tau\mathbb E[-\log q_\tau(S_Z\mid h_T)]\le\epsilon,
$$

则：

$$
I(h_T;Z)\ge H(Z)-\frac{\epsilon}{\lambda_\tau}.
$$

这就是 11 线的核心理论结论。

### 8.5 学习效率还不是无条件定理

表示定理说的是：

> 如果对应未来词元损失足够低，那么 $h_T$ 必须含 $Z$。

它没有直接证明：

> 训练过程中一定更快达到低损失，或者一定更省样本。

要从表示约束推进到效率，需要额外优化假设。例如定义语义恢复损失：

$$
R_\phi(\theta)=\operatorname{CE}(s_\phi(h_T(\theta)),Z),
$$

未来位置梯度：

$$
g_\tau=\nabla_\theta L_\tau.
$$

如果存在：

$$
\langle \nabla_\theta R_\phi,g_\tau\rangle\ge\gamma>0,
$$

那么沿 $-g_\tau$ 更新会一阶降低 $R_\phi$。这可以给出有条件的效率论证，但这个内积为正不是当前无条件证明出来的，它需要实验或额外优化假设。

## 9. 机制分解

| 机制环节 | 机制主张 | 观测指标 | 当前证据 | 边界 |
|---|---|---|---|---|
| 数据层信息结构 | 早期变量 $Z$ 第一次在 $\tau$ 显现 | $I(Z;Y_j\mid Y_{<j})$ | K=2 和 K=3 受控构造清楚 | 受控数据，不是自然语言 |
| 直接表示监督 | $K\ge\tau$ 时损失直接要求 $h_T$ 预测 $S_Z$ | 模型自身含信息位置准确率，$Q(t)$ | K=2 定理、K=3 定理、A11_01/A11_04 | 依赖构造和目标一一对应 |
| 学习效率 | 直接语义监督是否更早恢复 $Z$ | $T_{0.9}$，早期曲线面积 | A11_03、A11_04_03、A11_05 支持无噪声受控效率优势 | 不是无条件定理 |
| 全位置间接迁移 | 未覆盖 $\tau$ 的 K 也可能通过其他位置恢复 $Z$ | 全位置 K=1/K=2 的 $Q(t)$ | A11_04_02/A11_04_03/A11_05 明确存在 | 不能说只有 K=3 能学 |
| 本地损失保护 | 长程恢复不是牺牲本地预测 | $Y_1/Y_2$ 损失和准确率 | 无噪声实验中有效本地目标保持 1.00 | 只保护受控本地目标 |
| 梯度有效性 | 未来位置梯度是否解释效率 | 梯度夹角、范数、$\Delta Q$ | 结果混合、证据不足 | 不能用夹角正负直接讲好坏 |
| 路由桥接 | MTP 表征能否帮助 MoE 路由相关状态 | 路由边界、保持指标 | 尚未建立 | 不能推出专家收益 |

## 10. 判定卡（Anchor）证据链

| 判定卡 | 决策问题 | 结果 | 支持的故事环节 | 边界 |
|---|---|---|---|---|
| 11_01：K=2 分支延迟构造 | 向后两个词元预测是否给同一个 $h_T$ 分支相关监督？ | 只预测下一词元可以学会 $A$ 但不区分分支；向后两个词元预测的第 2 位置准确率、探针、分支替换一致性全部为 1.00 | K=2 直接表示监督 | 相同分支初始化 + 受控数据 |
| 11_02：K=2 共享主干信号 / 干扰 | $L_2$ 是有用分支信号，还是噪声或探针假象？ | 无噪声第 2 头、分支替换、探针通过；噪声第 2 头接近随机；存在梯度冲突但未损害 $Y_1$ | 分支信号有效，单看探针不够 | 梯度冲突不等于有害 |
| 11_03：K=2 语义学习效率 | K=2 是否比只预测下一词元更早恢复 $Z$？ | 向后两个词元预测提高曲线面积、最终分数和达标率，但相同初始化下只有 2/5 个随机种子成功 | 初步学习效率证据 | 获取过程不稳定 |
| 11_04：K=3 第一个语义显现位置 | 优势是否由 $K$ 覆盖 $\tau$ 决定？ | 单决策前缀、无噪声 $\tau=3$ 中 K=3 强，K=1/K=2 低；全位置训练中 K=1/K=2 也可恢复 | 第一个语义显现位置覆盖机制 | 全位置训练不支持“只有 K=3 能学” |
| 11_04_03：K=3 学习效率优势 | K=3 是否更早、更稳恢复 $Z$？ | 单决策前缀中 K=3 达标率为 0.60/0.40，K=1/K=2 不达阈值；全位置训练中 K=3 最强但不是唯一 | 直接监督带来的效率优势 | 梯度诊断证据不足 |
| 11_05：语义效率桥接 | 全位置 K=3 优势是否来自当前决策前缀上的第 3 位置监督？ | K=2 加当前决策前缀第 3 位置监督后匹配 K=3；K=3 去掉该监督后变弱；本地预测保护通过 | 直接语义监督是机制组件 | 间接迁移仍存在，随机初始化存在泄漏 |

## 11. 实验结果的当前整合

### 11.1 A11_01：K=2 机制闭环

目的：验证 K=2 定理是否能在最小可训练模型中出现。

设置：$Y_1=A$ 共享，$Y_2=S_B$ 分支特异，比较“只预测下一词元”和“向后两个词元预测”。

主指标：第 2 未来位置的单前缀准确率、冻结探针、分支替换一致性。

观测结果：只预测下一词元时，第 2 未来位置准确率为 0，探针为 0.333，分支替换一致性为 0；向后两个词元预测时三者均为 1.00。

解释：$L_2$ 不是额外预测头装饰，而是对同一个 $h_T$ 的分支相关监督。

边界：这是受控确定性数据；不能推出自然语言收益，也不能推出 MTP 普遍优于 NTP。

来源：`Projects/from-attention-to-search/main/experiments/A11/A11_01_k2_branch_delayed_next_two/summary.md`

### 11.2 A11_03：K=2 效率初步证据

目的：从“最终含 $Z$”推进到“是否更早学到 $Z$”。

设置：无噪声、单决策前缀、K=2，随机种子 971-975，比较“只预测下一词元”和“向后两个词元预测”。

主指标：$Q(t)$、$T_{0.9}$、曲线面积。

观测结果：向后两个词元预测比只预测下一词元有更高曲线面积、最终分数和达标率；但相同初始化下只有 2/5 个随机种子成功。

解释：直接语义监督有效率优势迹象，但优化过程不稳定。

边界：这不是“优化必然成功”的证明。

来源：`Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/summary.md`

### 11.3 A11_04 / A11_04_03：K=3 第一个语义显现位置

目的：检验优势是否由“K 覆盖第一个语义显现位置 $\tau$”决定。

设置：

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

主指标：覆盖差异、$Q(t)$、$T_{0.9}$、曲线面积、本地预测保护指标。

观测结果：

- 单决策前缀、无噪声 $\tau=3$：K=1/K=2 不达阈值；K=3 达标率为 0.60/0.40，早期曲线面积明显更高；
- 全位置、无噪声 $\tau=3$：K=3 仍最强，但 K=1/K=2 也能恢复；
- 有噪声全位置训练出现假阳性恢复；
- 梯度有效性结果混合，不能单靠梯度夹角或范数解释。

解释：第一个语义显现位置覆盖支持“单个当前前缀受到直接监督”的机制；全位置训练中的间接迁移是真实边界。

边界：不能说 K=1/K=2 在全位置训练中学不到 $Z$。

来源：

- `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_03_k3_efficiency_advantage/summary.md`

### 11.4 A11_05：直接语义监督与间接迁移

目的：在全位置、无噪声 $\tau=3$ 中分离直接语义监督和间接迁移。

条件：

- K2：全位置训练 $Y_1,Y_2$；
- K3 完整条件：全位置训练 $Y_1,Y_2,Y_3$；
- K3 去掉当前决策前缀第 3 位置监督：K3 训练，但屏蔽 $\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)$；
- K2 加当前决策前缀第 3 位置监督：K2 训练，并额外加入当前决策前缀上的 $\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)$。

主指标：$Q(t)$、$T_{0.9}$、早期曲线面积、本地预测保护指标、模型自身第 3 位置准确率。

相同分支初始化下的观测结果：

| 条件 | 达标率 | $T_{0.9}$ | 早期曲线面积 | 最终 $Q$ | 模型自身第 3 位置准确率 |
|---|---:|---:|---:|---:|---:|
| K2 | 0.60 | 333 | 0.771 | 0.85 | 不适用 |
| K3 完整条件 | 1.00 | 300 | 0.965 | 1.00 | 1.00 |
| K3 去掉当前决策前缀第 3 位置监督 | 0.60 | 833 | 0.817 | 0.70 | 0.00 |
| K2 加当前决策前缀第 3 位置监督 | 1.00 | 250 | 0.969 | 1.00 | 1.00 |

解释：

1. 给 K2 加当前决策前缀第 3 位置监督后，它几乎等价于 K3 完整条件；
2. 从 K3 去掉当前决策前缀第 3 位置监督后，K3 明显变弱；
3. 有效的 $Y_1/Y_2$ 本地预测没有被破坏；
4. 随机初始化在第 0 步就 $Q=1.0$，所以它是初始化泄漏边界，不是速度证据。

边界：直接语义监督是机制组件，但不是唯一通路；全位置间接迁移仍然存在。

来源：`Projects/from-attention-to-search/main/experiments/A11/A11_05_semantic_efficiency_bridge/summary.md`

## 12. 反例和竞争解释

| 竞争解释 | 为什么合理 | 当前控制 / 证据 | 剩余风险 |
|---|---|---|---|
| NTP 也能最终学到长程变量 | 全位置训练下其他位置会训练共享参数 | A11_04_02/A11_05 显示 K=1/K=2 也可恢复 | 不能声称“只有 K=3 能学” |
| 探针假阳性 | 隐藏状态可被线性读出不等于模型自身预测头会使用 | $Q=\min\{A,P,S\}$，另看模型自身第 3 位置准确率 | $Q$ 仍可能被初始化饱和 |
| 随机嵌入身份泄漏 | 随机初始化可能让分支在第 0 步就可读 | 相同分支初始化作为主判断 | 需要更严格的无泄漏设置 |
| MTP 只是更多损失项或正则化 | K=3 多一个辅助目标可能泛化更好 | A11_05 用“K=2 加第 3 位置监督”和“K=3 去掉第 3 位置监督”分离 | 损失权重仍可进一步控制 |
| 本地任务被牺牲 | 长程恢复可能损害 $Y_1/Y_2$ | 本地预测保护指标显示有效本地目标保持 1.00 | 只保护受控本地目标 |
| 梯度冲突决定好坏 | $g_1,g_\tau$ 的梯度夹角有正有负 | A11_04_03 / A11_05 说明诊断结果混合 | 需要更清晰的一步更新或干预 |

## 13. 当前结论边界

### 可以说

1. 在受控 K=2 构造中，向后两个词元预测给当前 $h_T$ 提供 NTP 没有的分支相关直接监督。
2. 在一般“第一个语义显现位置”构造中，如果 $K\ge\tau$ 且 $Y_\tau=S_Z$ 一一对应 $Z$，低的第 $\tau$ 个未来位置损失推出 $h_T$ 含有 $Z$。
3. 在无噪声、单决策前缀 $\tau=3$ 实验中，K=3 比 K=1/K=2 更早、更稳恢复 $Z$。
4. 在无噪声、全位置 $\tau=3$ 实验中，K=3 仍然最强；A11_05 显示当前决策前缀第 3 位置监督是这个优势的一个可测机制组件。
5. 当前无噪声实验中，有效本地 $Y_1/Y_2$ 预测没有被牺牲。

### 不能说

1. MTP 在自然语言中已经证明优于 NTP。
2. K 越大越好。
3. 全位置训练中 K=1/K=2 不能恢复 $Z$。
4. 直接语义监督是全位置训练中恢复 $Z$ 的唯一通路。
5. 梯度夹角或范数比能直接说明梯度好坏。
6. 当前 A11 已经证明 MoE 路由保持、语义专家身份或专家收益。

### 仍然开放

1. 在什么优化假设下，直接语义监督能推出更短训练时间或更低样本需求？
2. 如何构造一个无泄漏的全位置训练设置，让 $Q(0)$ 不被随机初始化饱和？
3. MTP 写入的 $Z$ 是否更容易被模型自身读出或被路由器使用，而不只是被外部探针读出？
4. 这个目标函数层面的机制如何映射到 MoE 路由相关隐藏状态的形成？

## 14. 判定卡（Anchor）分解和下一步

| 判定卡 / 下一节点 | 决策问题 | 为什么需要 | 主指标 | 证伪条件 |
|---|---|---|---|---|
| 11_05 已完成 | 全位置 K=3 优势是否来自当前决策前缀第 3 位置监督？ | 分离直接语义监督与间接迁移 | $T_{0.9}$，早期曲线面积，模型自身第 3 位置准确率，本地预测保护指标 | K=2 加第 3 位置监督不改善，且 K=3 去掉该监督后不变弱 |
| 11_06：无泄漏效率桥接 | 在没有第 0 步泄漏的全位置训练中，第 3 位置直接监督是否仍改善效率？ | 解决随机初始化饱和和间接迁移过强 | $Q(0)$，$T_{0.9}$，早期曲线面积 | 所有条件第 0 步或早期都饱和，或第 3 位置直接监督没有增益 |
| 11_07：梯度干预 | 第 $\tau$ 个未来位置梯度是否一阶降低语义恢复损失？ | 把经验效率转成优化层面的条件论证 | 受控更新后的 $\Delta R_\phi$、$\Delta Q$、$\Delta L_{local}$ | $-g_\tau$ 不改善 $R_\phi/Q$ 或明显损害本地预测 |
| 未来连接 A06 | MTP 写入的 $Z$ 是否改善路由边界或保持性？ | 连接 MoE 保持主线 | 路由一致性、边界、符号翻转、语言模型损失 | 隐藏状态中的 $Z$ 不转化为路由相关边界 |

当前最小下一步是：

> 不扩 K，不上自然语言；先写 11_06 无泄漏全位置语义效率桥接，专门解决随机初始化饱和和间接迁移过强的问题。

## 15. 与主线的关系

`PROJECTS.md` 当前主线仍是“top-1 MoE 路由中的特征级专家专业化”，当前瓶颈是“保持性”。A11 不是替代主线，而是目标函数机制支线。

A11 能提供的桥是：

> 如果 MTP 能更早把长程变量 $Z$ 写进当前隐藏状态，那么未来可能帮助形成路由相关隐藏状态。

但这还没有证明。要连接回路由主线，需要一个明确协议，把：

$$
Z,\quad h_T,\quad \text{路由边界 / 保持性指标}
$$

放进同一个实验里。否则 A11 只能讨论隐藏表示，不应声称专家收益。

## 16. 下一步唯一决策

**建议下一步：写 11_06 无泄漏全位置语义效率判定卡。**

目的不是再证明 K=3 强，也不是扩到 K>3，而是解决 A11_05 暴露出的两个边界：

1. 随机初始化让 $Q(0)=1$，速度指标失效；
2. 全位置间接迁移太强，使未覆盖 $\tau$ 的 K 也能恢复。

11_06 应该固定无噪声 $\tau=3$，只改变泄漏控制和间接迁移强度，判断当前决策前缀第 3 位置直接监督是否仍带来更低 $T_{0.9}$ 或更高早期曲线面积。

## 来源索引

### 理论文档

- `daily_research_reports/0707/mtp_k2/mtp_k2_self_contained_theory_proof.md`
- `daily_research_reports/0707/mtp_k2/two_token_shared_trunk_theory_experiment_design.md`
- `daily_research_reports/0707/mtp_k2/long_horizon_next_k_theory_design.md`
- `daily_research_reports/0708/mtp_story_package/01_long_horizon_mtp_self_contained_story_v0.md`
- `daily_research_reports/0708/mtp_semantic_efficiency_package_v1/01_whole_story_line_mtp_long_horizon_semantic_efficiency_cn.md`

### 判定卡（Anchor）

- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/README.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_01_k2_branch_delayed_next_two_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_02_two_token_shared_trunk_signal_interference_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_03_k2_semantic_efficiency_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_04_k3_first_informative_horizon_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_05_semantic_efficiency_bridge_anchor.md`

### 实验证据

- `Projects/from-attention-to-search/main/experiments/A11/A11_01_k2_branch_delayed_next_two/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_01_k2_branch_delayed_next_two/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_02_k3_all_position_control/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_02_k3_all_position_control/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_03_k3_efficiency_advantage/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_03_k3_efficiency_advantage/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_05_semantic_efficiency_bridge/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_05_semantic_efficiency_bridge/detailed.md`

### 关键图表

- `Projects/from-attention-to-search/main/experiments/A11/A11_05_semantic_efficiency_bridge/figures/q_curves_identical.png`
- `Projects/from-attention-to-search/main/experiments/A11/A11_05_semantic_efficiency_bridge/figures/final_q_vs_native_h3.png`
- `Projects/from-attention-to-search/main/experiments/A11/A11_05_semantic_efficiency_bridge/tables/report_compact_summary.csv`

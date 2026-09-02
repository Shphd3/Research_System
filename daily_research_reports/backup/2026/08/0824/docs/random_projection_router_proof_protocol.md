# Qwen3-30B-A3B 更新残差的线性路由结构与随机投影保持

> **文档定位：** 自包含理论证明、门槛条件化实验协议与实测结果报告
> **唯一模型对象：** Qwen3-30B-A3B，48 个 Transformer block，隐藏维数 $d=2048$
> **实验证据：** A15_08_09_E02 全层定位与完整空间门槛实验
> **计算状态：** 全部计算协议已完成；外部 64 条独立人工语义复核尚未闭合，因此数据门槛 H1 的总体状态仍为 `Insufficient`
> **核心结论：** $R_U$ 中存在超越同层写入前状态 $X$ 的条件增量信息，但该信息没有形成可独立使用、跨模板稳健且具有正低尾 logit margin 的线性 Router 几何。

---

## 1. 研究问题与目标

### 1.1 研究对象

对 Qwen3-30B-A3B 的每个 Transformer block，本文考察 Attention 写入给随后混合专家模块带来的归一化状态变化。我们进一步去除这项变化中可由写入前状态线性预测的部分，得到更新残差 $R_U$。

本文只回答一个问题：

> 在 Qwen3-30B-A3B 中，$R_U$ 是否已经具有稳定的线性类别结构；如果完整空间首先满足正 margin 门槛，独立稠密高斯随机投影能否在 $m\ll d$ 时保持该结构？

这个问题必须分成两个按顺序执行的判断：

1. **信息存在性：** $R_U$ 相对同层写入前状态 $X$，是否提供受控制的新增预测效用；
2. **独立几何与保持性：** $R_U$ 单独使用时，是否已经形成稳定正 margin；只有答案为是，才讨论随机投影是否保持它。

二者不能互相替代。条件增量信息可以存在，但仍可能分散、纠缠或依赖 $X$，因而不能由 $R_U$ 单独形成稳健线性 Router。

### 1.2 研究目标

本文的目标是建立一条从数学前提到实验结论的闭合链：

$$
\text{全层无偏定位}
\rightarrow
\text{完整空间线性可访问性}
\rightarrow
\text{正低尾 margin 准入}
\rightarrow
\text{条件化随机投影保持}.
$$

理论部分回答“若结构已经存在，什么随机映射能够保持”；实验部分回答“Qwen3-30B-A3B 的冻结 $R_U$ 是否满足这些前提”。

### 1.3 当前直接答案

Qwen3-30B-A3B 的 48 层中，有 31 层的 $R_U$ 对 $X$ 具有显著正的受控增量效用；最大值位于 Block 39，为 $0.10994$ nat/样本。然而，按开发集规则冻结的主层 Block 48 和重复层 Block 38 都没有通过正低尾 margin 门槛。因此，随机投影保持实验没有满足前提，H4 的正确状态是 `SKIPPED_H3_NOT_PASS`。

### 1.4 结论边界

本文研究的是冻结表征上的离线线性类别结构，不直接证明：

- 8 个语义父类等于真实专家最优分工；
- 线性可读性等于语言模型损失收益；
- $R_U$ 中没有非线性信息；
- 联合表征 $(X,R_U)$ 不可用；
- 随机投影可以创造原空间不存在的结构；
- 当前结果已经验证层次化专家树或真实专家效用。

---

## 2. 术语与符号

### 2.1 Qwen3-30B-A3B 的层内表征

固定 block $\ell\in\{1,\ldots,48\}$ 和统一决策 token。对样本 $i$，定义：

- $h_{\ell,i}\in\mathbb R^d$：进入本层 Attention 前的 residual stream；
- $a_{\ell,i}\in\mathbb R^d$：Attention 输出投影后、加入 residual stream 前的写入；
- $N_\ell$：该 block 实际使用的 post-Attention RMSNorm；
- $d=2048$：隐藏维数。

写入前和写入后的归一化状态为

$$
X_{\ell,i}=N_\ell(h_{\ell,i}),
$$

$$
Z_{\ell,i}=N_\ell(h_{\ell,i}+a_{\ell,i}).
$$

精确归一化更新为

$$
U_{\ell,i}=Z_{\ell,i}-X_{\ell,i}.
$$

只在训练集上拟合多输出岭回归：

$$
(\widehat B_\ell,\widehat b_\ell)
=
\arg\min_{B,b}
\sum_{i\in\mathcal I_{\mathrm{train}}}
\left\|U_{\ell,i}-B^\top X_{\ell,i}-b\right\|_2^2
+\lambda\|B\|_F^2.
$$

更新残差定义为

$$
R_{U,\ell,i}
=
U_{\ell,i}
-\widehat B_\ell^\top X_{\ell,i}
-\widehat b_\ell.
$$

冻结目标层后简写

$$
r_i:=R_{U,\ell,i}.
$$

$R_U$ 的准确含义是“在注册岭回归族下，不能由 $X$ 线性预测的更新部分”。它不是信息论意义上的全新信息，也不是模型已经原生用于路由的证明。

### 2.2 标签与 Router

主任务标签为 $K=8$ 个语义父类：

$$
y_i\in[K]=\{1,\ldots,8\}.
$$

64 个细类只用于数据平衡和描述性功能维数审计，不用于主 H2--H4 判定。

本文中的 **Router** 指注册的多类线性读出器：

$$
s_k(r)=w_k^\top r+b_k,
\qquad k\in[K].
$$

它是一个离线几何探针，不代表真实 MoE 专家已经按这些标签分工。

### 2.3 公共成分、语义成分与有界扰动

为分析距离结构，考虑一般分解

$$
x_i=s_i+c+n_i,
$$

其中：

- $s_i$ 是样本相关的目标结构；
- $c$ 是所有样本共享的固定成分；
- $n_i$ 是样本相关扰动，且 $\|n_i\|_2\le\nu$。

固定成分 $c$ 会在样本差分中抵消；随样本变化的“公共趋势”不能被当作固定 $c$。

### 2.4 类内、类间距离与距离比

对语义成分定义

$$
a_s=\max_{y_i=y_j}\|s_i-s_j\|_2,
\qquad
b_s=\min_{y_i\ne y_j}\|s_i-s_j\|_2.
$$

对完整表征定义

$$
D_{\mathrm{in}}
=\max_{y_i=y_j}\|x_i-x_j\|_2,
$$

$$
D_{\mathrm{out}}
=\min_{y_i\ne y_j}\|x_i-x_j\|_2.
$$

当 $D_{\mathrm{in}}>0$ 时，极端距离比为

$$
\rho_{\mathrm{dist}}
=
\frac{D_{\mathrm{out}}}{D_{\mathrm{in}}}.
$$

$\rho_{\mathrm{dist}}>1$ 表示所有类间距离均大于所有类内距离，是非常强的有限样本几何条件。实验还报告稳健版本

$$
\widetilde\rho_{\mathrm{dist}}
=
\frac{Q_{0.05}(\text{类间距离})}
{Q_{0.95}(\text{类内距离})},
$$

但稳健比值不是定理 1 的极值对象。

### 2.5 最小 margin 与 5% 低尾 margin

样本 $i$ 相对错误类别 $k$ 的 logit margin 为

$$
\gamma_{ik}
=
(w_{y_i}-w_k)^\top r_i+b_{y_i}-b_k.
$$

理论中的全样本最小 margin 是

$$
\gamma_{\min}
=
\min_i\min_{k\ne y_i}\gamma_{ik}.
$$

实验中的逐样本 true-label margin 是

$$
\gamma_i
=
s_{y_i}(r_i)-\max_{k\ne y_i}s_k(r_i),
$$

其 5% 分位数为

$$
\Gamma_{0.05}
=
Q_{0.05}(\gamma_i).
$$

$\gamma_{\min}>0$ 是定理 2 对全部有限样本统一保持的强前提；$\Gamma_{0.05}>0$ 是实验采用的稳健低尾条件，意味着至少约 95% 的样本 margin 不低于该正值。二者不能写成同一对象。

### 2.6 单谱轴方差比与全空间 margin

给定训练集协方差谱基 $U=(u_1,\ldots,u_d)$，第 $j$ 个谱坐标为

$$
q_{ij}=u_j^\top r_i.
$$

设第 $k$ 类在该坐标上的均值为 $\mu_{k,j}$，全局均值为 $\mu_j$。定义单谱轴类间方差

$$
B_j
=
\sum_{k=1}^K\frac{n_k}{n}(\mu_{k,j}-\mu_j)^2,
$$

以及单谱轴类内方差

$$
W_j
=
\frac1n\sum_{i=1}^n(q_{ij}-\mu_{y_i,j})^2.
$$

当 $W_j>0$ 时，单谱轴方差比为

$$
F_j=\frac{B_j}{W_j}.
$$

$F_j$ 只回答“第 $j$ 个单独谱轴的类间变化相对类内变化有多大”。它是一维、无分类器的描述量。$\Gamma_{0.05}$ 则来自完整 $d$ 维空间中多个方向的线性组合，回答冻结分类器的低尾决策可靠性。即使所有单轴 $F_j$ 都不高，多轴组合仍可能产生正 margin；反过来，少数高 $F_j$ 也不保证完整分类器跨模板稳定。

### 2.7 几何维数与监督功能维数

若第 $k$ 类支持集位于仿射子空间

$$
\mathcal M_k\subseteq a_k+S_k,
\qquad
\dim(S_k)\le r_{\mathrm{geo}},
$$

则 $r_{\mathrm{geo}}$ 是几何仿射维数。

给定容许性能损失 $\eta>0$，定义监督功能维数

$$
r_{\mathrm{func}}(\eta)
=
\min\left\{
q:\exists P\in\mathbb R^{d\times q},\ P^\top P=I_q,
\operatorname{Risk}(P^\top r)
\le
\operatorname{Risk}(r)+\eta
\right\}.
$$

$r_{\mathrm{func}}$ 描述一个监督任务所需的输入维数；$r_{\mathrm{geo}}$ 描述数据支持集。一般情况下

$$
r_{\mathrm{func}}\ne r_{\mathrm{geo}}.
$$

### 2.8 JL 连续保持、谱坐标抽样与 LSH 离散检索

本文主随机映射为稠密高斯矩阵

$$
R\in\mathbb R^{m\times d},
\qquad
R_{ab}\overset{\mathrm{i.i.d.}}{\sim}\mathcal N(0,1/m),
$$

并令 $\phi_G(r)=Rr$。它属于 **Johnson--Lindenstrauss（JL）连续距离保持**：输出仍是实向量，并以高概率近似保持固定有限向量集合的欧氏长度、距离和相关内积。

随机谱坐标抽样先计算 $q=U^\top r$，再随机抽取少量 $q_j$。它可能漏掉集中在少数坐标上的信号，因此需要低相干条件；该条件不属于稠密高斯 JL 主定理。

**局部敏感哈希（Locality-Sensitive Hashing, LSH）** 把连续向量映射为离散哈希码，使相近向量更可能碰撞。LSH 可在未来用于超大规模专家池中的候选专家检索，但它不是本文定理 1--3 的依赖项，也没有在当前实验中被检验。JL 回答连续几何保持；LSH 回答近邻候选的离散检索效率，二者不能互换。

---

## 3. 主理论证明（引理 1、引理 2、定理 1--3）

主理论链为：

$$
\text{公共成分与扰动}
\rightarrow
\text{JL 距离保持}
\rightarrow
\text{固定 Router margin 保持}
\rightarrow
\text{线性投影不可能创造线性可分性}.
$$

### 3.1 引理 1：固定公共成分抵消，有界扰动收缩间隔

**引理 1。** 设

$$
x_i=s_i+c+n_i,
\qquad
\|n_i\|_2\le\nu,
$$

其中 $c$ 对所有样本固定。令

$$
D_{\mathrm{in}}=\max_{y_i=y_j}\|x_i-x_j\|_2,
\qquad
D_{\mathrm{out}}=\min_{y_i\ne y_j}\|x_i-x_j\|_2.
$$

则

$$
D_{\mathrm{in}}\le a_s+2\nu,
\qquad
D_{\mathrm{out}}\ge b_s-2\nu.
$$

若 $b_s-a_s>4\nu$，则 $D_{\mathrm{out}}>D_{\mathrm{in}}$。

**证明。** 对任意 $i,j$，

$$
x_i-x_j=(s_i-s_j)+(n_i-n_j),
$$

固定公共成分 $c$ 严格抵消。若 $y_i=y_j$，三角不等式给出

$$
\|x_i-x_j\|_2
\le
\|s_i-s_j\|_2+\|n_i\|_2+\|n_j\|_2
\le
\|s_i-s_j\|_2+2\nu.
$$

对所有同类样本对取最大值得 $D_{\mathrm{in}}\le a_s+2\nu$。若 $y_i\ne y_j$，反三角不等式给出

$$
\|x_i-x_j\|_2
\ge
\|s_i-s_j\|_2-\|n_i-n_j\|_2
\ge
\|s_i-s_j\|_2-2\nu.
$$

对所有异类样本对取最小值得 $D_{\mathrm{out}}\ge b_s-2\nu$。因此若 $b_s-a_s>4\nu$，

$$
D_{\mathrm{out}}
\ge b_s-2\nu
>a_s+2\nu
\ge D_{\mathrm{in}}.
$$

证毕。

**边界。** 该引理不创造间隔，只给出已有语义间隔在固定公共成分和有界扰动下仍为正的充分条件。

### 3.2 引理 2：固定向量的高斯长度集中

**引理 2。** 令 $R_{ab}\overset{\mathrm{i.i.d.}}{\sim}\mathcal N(0,1/m)$。对任意在抽取 $R$ 前固定的 $v\in\mathbb R^d$ 和 $0<\varepsilon<1$，

$$
\Pr\left[
\left|\|Rv\|_2^2-\|v\|_2^2\right|
\ge
\varepsilon\|v\|_2^2
\right]
\le
2\exp\left(-\frac{m\varepsilon^2}{12}\right).
$$

**证明。** $v=0$ 时结论显然。对 $v\ne0$，$R$ 的每一行与 $v$ 的内积独立服从 $\mathcal N(0,\|v\|_2^2/m)$，因而

$$
\frac{m\|Rv\|_2^2}{\|v\|_2^2}\sim\chi_m^2.
$$

卡方变量的 Chernoff 界给出

$$
\Pr\left[
\left|
\frac{\|Rv\|_2^2}{\|v\|_2^2}-1
\right|\ge\varepsilon
\right]
\le
2\exp\left[-m\left(
\frac{\varepsilon^2}{4}-\frac{\varepsilon^3}{6}
\right)\right].
$$

因为 $0<\varepsilon<1$ 时 $\varepsilon^2/4-\varepsilon^3/6\ge\varepsilon^2/12$，结论成立。证毕。

### 3.3 定理 1：有限样本 JL 距离与距离比保持

**定理 1。** 给定在抽取随机矩阵前固定的有限点集

$$
\mathcal X=\{x_1,\ldots,x_n\}\subset\mathbb R^d,
\qquad n\ge2.
$$

若

$$
m
\ge
\frac{12}{\varepsilon^2}
\log\frac{n(n-1)}{\delta},
\qquad 0<\varepsilon<1,
$$

则以至少 $1-\delta$ 的概率，对所有 $i\ne j$ 同时有

$$
(1-\varepsilon)\|x_i-x_j\|_2^2
\le
\|R(x_i-x_j)\|_2^2
\le
(1+\varepsilon)\|x_i-x_j\|_2^2.
$$

若进一步 $0<D_{\mathrm{in}}<D_{\mathrm{out}}$，则

$$
\boxed{
\rho'_{\mathrm{dist}}
\ge
\sqrt{\frac{1-\varepsilon}{1+\varepsilon}}
\rho_{\mathrm{dist}}
}.
$$

特别地，当

$$
\varepsilon
<
\frac{\rho_{\mathrm{dist}}^2-1}
{\rho_{\mathrm{dist}}^2+1},
$$

投影后仍有 $D'_{\mathrm{out}}>D'_{\mathrm{in}}$。

**证明。** 非零样本差向量至多有 $M=n(n-1)/2$ 个。由引理 2，每个固定差向量失真超过 $\varepsilon$ 的概率至多为 $2\exp(-m\varepsilon^2/12)$。对所有样本对使用并合界，总失败概率不超过

$$
2M\exp\left(-\frac{m\varepsilon^2}{12}\right)
=
n(n-1)\exp\left(-\frac{m\varepsilon^2}{12}\right)
\le\delta.
$$

所以全部样本对同时满足距离界。对同类样本对取最大值、对异类样本对取最小值，得到

$$
D'_{\mathrm{in}}
\le\sqrt{1+\varepsilon}\,D_{\mathrm{in}},
\qquad
D'_{\mathrm{out}}
\ge\sqrt{1-\varepsilon}\,D_{\mathrm{out}}.
$$

相除即得距离比下界；要求该下界大于 1，即得到最后的 $\varepsilon$ 条件。证毕。

**边界。** 定理 1 保持已经存在的有限样本欧氏距离结构。若原空间 $\rho_{\mathrm{dist}}\le1$，定理不提供投影后出现正极端距离间隔的保证。

### 3.4 定理 2：固定多类线性 Router 的 margin 与决策保持

**定理 2。** 在抽取 $R$ 前，固定有限数据 $\{(r_i,y_i)\}_{i=1}^n$ 和线性 Router $\{(w_k,b_k)\}_{k=1}^K$。假设：

1. $R$ 与数据、标签、权重和偏置独立；
2. $B_x:=\max_i\|r_i\|_2>0$；
3. $B_w:=\max_i\max_{k\ne y_i}\|w_{y_i}-w_k\|_2>0$；
4. 全样本最小 margin $\gamma_{\min}>0$。

令

$$
\eta
=
\min\left\{
\frac12,
\frac{\gamma_{\min}}{2B_xB_w}
\right\}.
$$

若

$$
m
\ge
\frac{12}{\eta^2}
\log\frac{4n(K-1)}{\delta},
$$

则以至少 $1-\delta$ 的概率，令 $z_i=Rr_i$、$\widetilde w_k=Rw_k$ 并保留 $b_k$，则对所有 $i$ 和 $k\ne y_i$ 同时有

$$
(\widetilde w_{y_i}-\widetilde w_k)^\top z_i
+b_{y_i}-b_k
\ge
\frac{\gamma_{\min}}2>0.
$$

因此全部有限样本的 argmax 决策保持，最小 margin 至少为 $\gamma_{\min}/2$。

**证明。** 令

$$
v_{ik}=w_{y_i}-w_k,
\qquad
a_i=\frac{r_i}{B_x},
\qquad
c_{ik}=\frac{v_{ik}}{B_w}.
$$

则 $\|a_i\|_2\le1$ 且 $\|c_{ik}\|_2\le1$。考虑至多含 $2n(K-1)$ 个向量的集合

$$
\mathcal Q
=
\{a_i+c_{ik},a_i-c_{ik}:i\in[n],\ k\ne y_i\}.
$$

由引理 2 和并合界，在给定维数条件下，以至少 $1-\delta$ 的概率，对所有 $q\in\mathcal Q$ 同时有

$$
\left|\|Rq\|_2^2-\|q\|_2^2\right|
\le\eta\|q\|_2^2.
$$

对 $a_i\pm c_{ik}$ 使用极化恒等式可得

$$
\left|
\langle Ra_i,Rc_{ik}\rangle
-\langle a_i,c_{ik}\rangle
\right|
\le\eta.
$$

恢复尺度后，

$$
\left|
\langle Rr_i,Rv_{ik}\rangle
-\langle r_i,v_{ik}\rangle
\right|
\le
\eta B_xB_w
\le
\frac{\gamma_{\min}}2.
$$

所以投影后的正确类别与任一错误类别的 logit 差至少为

$$
\gamma_{ik}-\frac{\gamma_{\min}}2
\ge\frac{\gamma_{\min}}2.
$$

该式对全部 $i,k$ 同时成立。证毕。

**5% 低尾推论。** 若只知道 $\Gamma_{0.05}>0$，取冻结子集

$$
\mathcal I_{0.05}
=
\{i:\gamma_i\ge\Gamma_{0.05}\}.
$$

该集合至少覆盖约 95% 的有限样本。在 $\mathcal I_{0.05}$ 上以 $\Gamma_{0.05}$ 代替 $\gamma_{\min}$ 应用定理 2，可得到该固定子集的统一保持保证；不能把它升级为全部样本保证。实验 H3 是低尾稳健准入规则，而不是全样本最小 margin 的验证。

**边界。** 定理不保证优化器能在低维空间重新学到 Router，不保证分布外泛化，也不把语义标签分类升级为真实专家效用。

### 3.5 定理 3：线性投影不能创造线性可分性

**定理 3。** 若一个标签映射不能由任何原空间多类线性 Router $r\mapsto Wr+b$ 正确实现，则对任意线性映射 $A\in\mathbb R^{m\times d}$，不存在投影空间线性 Router

$$
z\mapsto W'z+b',
\qquad z=Ar,
$$

能够正确实现同一标签映射。

**证明。** 若存在 $A,W',b'$ 可以正确实现，则复合映射为

$$
W'(Ar)+b'=(W'A)r+b'.
$$

它本身就是原空间线性 Router，与前提矛盾。证毕。

**实验边界。** 定理 3 的前提是“不存在任何原空间线性 Router”。一次注册探针实验失败不能证明这个全称命题；它只能说明在给定数据、探针族和统计功效下没有发现稳定线性结构。

---

## 4. 扩展定理（定理 4--5）

本节给出两个有额外结构假设的扩展。它们不参与当前 H0--H4 主结论。

### 4.1 定理 4：低维仿射子空间并集的统一嵌入

**定理 4。** 设

$$
\mathcal X
\subseteq
\bigcup_{k=1}^K(a_k+S_k),
\qquad
\dim(S_k)\le r_{\mathrm{geo}}.
$$

对每一对类别 $(k,\ell)$，定义

$$
L_{k\ell}
=
\operatorname{span}(a_k-a_\ell,S_k,S_\ell).
$$

则 $\dim(L_{k\ell})\le2r_{\mathrm{geo}}+1$。若

$$
m
\ge
\frac{48}{\varepsilon^2}
\left[
(2r_{\mathrm{geo}}+1)\log9
+\log\frac{2K^2}{\delta}
\right],
$$

则以至少 $1-\delta$ 的概率，对所有 $x,y\in\mathcal X$ 同时有

$$
(1-\varepsilon)\|x-y\|_2^2
\le
\|R(x-y)\|_2^2
\le
(1+\varepsilon)\|x-y\|_2^2.
$$

**证明。** 固定维数 $q\le2r_{\mathrm{geo}}+1$ 的子空间 $L$，记 $P_L$ 为正交投影，并定义限制在 $L$ 上的自伴压缩算子

$$
A_L=P_L(R^\top R-I)P_L\big|_L.
$$

在 $L$ 的单位球面上取半径 $1/4$ 的有限网 $\mathcal N$，满足 $|\mathcal N|\le9^q$。对每个 $u\in\mathcal N$，由引理 2 在误差 $\varepsilon/2$ 下有

$$
\Pr\left[
|u^\top A_Lu|>\frac\varepsilon2
\right]
\le
2\exp\left(-\frac{m\varepsilon^2}{48}\right).
$$

并合后，全部网点以相应高概率满足 $|u^\top A_Lu|\le\varepsilon/2$。任取 $x$ 为 $L$ 中单位向量，选择 $u\in\mathcal N$ 使 $\|x-u\|_2\le1/4$，则

$$
|x^\top A_Lx|
\le
\frac\varepsilon2
+\frac12\|A_L\|_{\mathrm{op}}.
$$

对 $x$ 取上确界得到 $\|A_L\|_{\mathrm{op}}\le\varepsilon$。因此 $L$ 中所有向量的平方长度都在 $1\pm\varepsilon$ 范围内保持。最后对至多 $K^2$ 个 $L_{k\ell}$ 使用并合界；任意 $x\in a_k+S_k$、$y\in a_\ell+S_\ell$ 都满足 $x-y\in L_{k\ell}$，结论成立。证毕。

**边界。** 定理 4 使用 $r_{\mathrm{geo}}$，不能用监督学习得到的 $r_{\mathrm{func}}$ 或 $r_{90}$ 代替其几何假设。

### 4.2 定理 5：低相干条件下的随机谱坐标抽样

在训练集协方差谱基 $U$ 中，对非零向量 $v$ 定义谱坐标 $q=U^\top v$ 和相干度

$$
\mu(v;U)
=
d\frac{\|q\|_\infty^2}{\|v\|_2^2}.
$$

独立均匀地、有放回地抽取 $J_1,\ldots,J_m\sim\operatorname{Unif}\{1,\ldots,d\}$，并定义

$$
\phi_C(v)
=
\sqrt{\frac dm}
(q_{J_1},\ldots,q_{J_m})^\top.
$$

**定理 5。** 给定抽样前固定的有限非零向量集合 $\mathcal V$，若

$$
\mu(v;U)\le\mu
\qquad
\forall v\in\mathcal V,
$$

且

$$
m
\ge
\frac{8\mu}{3\varepsilon^2}
\log\frac{2|\mathcal V|}{\delta},
\qquad 0<\varepsilon<1,
$$

则以至少 $1-\delta$ 的概率，对所有 $v\in\mathcal V$ 同时有

$$
(1-\varepsilon)\|v\|_2^2
\le
\|\phi_C(v)\|_2^2
\le
(1+\varepsilon)\|v\|_2^2.
$$

**证明。** 固定 $v$，令

$$
Y_t=d\frac{q_{J_t}^2}{\|v\|_2^2}.
$$

则 $\mathbb E[Y_t]=1$、$0\le Y_t\le\mu$、$\operatorname{Var}(Y_t)\le\mu$，且

$$
\frac{\|\phi_C(v)\|_2^2}{\|v\|_2^2}
=
\frac1m\sum_{t=1}^mY_t.
$$

由 Bernstein 不等式，

$$
\Pr\left[
\left|
\frac1m\sum_{t=1}^mY_t-1
\right|\ge\varepsilon
\right]
\le
2\exp\left(
-\frac{m\varepsilon^2}
{2\mu+2\mu\varepsilon/3}
\right).
$$

当 $0<\varepsilon<1$ 时，分母不超过 $8\mu/3$。再对 $\mathcal V$ 使用并合界，结论成立。证毕。

### 4.3 高谱熵不能替代低相干

谱熵描述能量的平均分散程度，相干度控制最大单坐标能量。归一化谱熵接近 1，仍可能存在远高于均匀水平的最大 leverage 坐标。因此

$$
\text{高谱熵}\not\Rightarrow\text{低相干}.
$$

当前 Block 48/38 的归一化谱熵为 $0.9888/0.9534$，但相干度为 $2.0435/3.5639$，TRAIN 充分维数界为 $83{,}892/114{,}975$，远高于注册最大维数 1,024。因此谱坐标抽样分支不具备运行资格。这不影响稠密高斯 JL 理论，因为稠密高斯投影不要求谱低相干。

---

## 5. 门槛条件化协议（H0--H4）

### 5.1 H0：Qwen3-30B-A3B 目标层的规范化无偏定位

对全部 48 个 block，只用 TRAIN 拟合、DEV 选择正则。对每层先拟合基于 $X_\ell$ 的基础分数，再分别加入同一样本的真实 $R_{U,\ell}$、重复的 $X_\ell$ 和 30 个独立错配的 $R_{U,\ell}$。令 $G_\ell^{\mathrm{true}}$、$G_\ell^{\mathrm{dupX}}$ 和 $G_{\ell,j}^{\mathrm{mis}}$ 表示相对同一基础分数的 DEV 交叉熵降低，单位为 nat/样本。定义

$$
T_\ell
=
G_\ell^{\mathrm{true}}
-
\max\left(
G_\ell^{\mathrm{dupX}},
Q_{0.95}\{G_{\ell,j}^{\mathrm{mis}}\}_{j=1}^{30}
\right).
$$

2,000 次按细类分层 bootstrap 在每次重采样中同时计算全部 48 层，并用最大中心化误差形成 familywise simultaneous 95% 区间。

- **H0 Pass：** 至少一层的同时区间下界严格大于 0；
- **H0 Fail：** 没有任何层满足该条件；
- **H0 Insufficient：** 数据、提取、拟合或同时区间守卫失效。

主层只在 H0-admitted 层中按独立 $R_U$ 的 DEV $\Gamma_{0.05}$、balanced accuracy、较小层号依次排序。重复层使用同一规则，并要求与主层至少相隔 4 个 block。TEST 标签在选层视图中被删除。

**实测：** H0 `Pass`；31/48 层的同时下界大于 0。最大值位于 Block 39：

$$
T_{39}=0.10994
\quad[0.09872,0.12080].
$$

冻结主层为 Block 48，重复层为 Block 38。Block 39 回答“哪里条件增量效用最大”；Block 48 回答“哪个 H0 合格层的独立 DEV 低尾 margin 最接近准入”。二者角色不同。

### 5.2 H1：数据有效性

H1 检查类别平衡、跨划分语义种子隔离、直接标签词、规范化重复、字符 5-gram 高相似、公式实例重用、模板绑定、词袋捷径和语义复核。

- **H1 Pass：** 所有机器守卫与独立人工语义复核都通过；
- **H1 Fail：** 确认存在泄漏、重复、错标或主类歧义；
- **H1 Insufficient：** 任一必要守卫尚未取得足够证据。

**实测：** 机器守卫全部通过；64 条 AI review 为 52 条 `PASS`、12 条 `PASS_WITH_NOTE`、零类别或算术错误。独立人工 review 尚未完成，因此总体 H1 为 `Insufficient`。这不改变已冻结的 H0/H2/H3 数值，但阻止把整个数据结论标为完全闭合。

### 5.3 H2：完整空间监督分类能力

在冻结层的 $R_U$ 上训练五种子 L2 多类逻辑回归。H2 要求同模板和新模板 TEST 的 balanced accuracy 95% 置信区间下界均严格高于机会水平 $1/K=0.125$，且收敛、区间宽度和种子稳定性守卫通过。

**实测：**

- Block 48：H2 `Fail`，因为新模板 TEST 下界 $0.12445$ 没有严格高于 $0.125$；
- Block 38：H2 `Pass`，两个 TEST 面板的下界都高于机会水平。

### 5.4 H3：完整空间正低尾 margin 准入

H3 是 H4 的硬门槛。对两个 TEST 面板同时要求：

1. balanced accuracy 的 95% 置信区间下界至少为 $0.90$；
2. $\Gamma_{0.05}$ 的 95% 置信区间下界大于 0；
3. 五个种子中至少四个通过，且主种子 24001 通过；
4. 收敛和区间精度守卫通过。

**实测：** Block 48 和 Block 38 均为 H3 `Fail`。两个层、两个 TEST 面板构成的四个 block--panel 单元中，所有 $\Gamma_{0.05}$ 及其置信区间均为负。

### 5.5 H4：条件化稠密高斯随机投影保持

仅当主层 H3 Pass 后，才独立抽取高斯矩阵并扫描

$$
m\in\{8,16,32,64,128,256,512,1024\},
$$

每个 $m$ 使用 30 个独立种子。冻结完整空间权重 $W$ 后使用 $z_i=Rr_i$、$\widetilde W=RW$，不在低维空间重训主 Router。

定义 normalized margin retention

$$
\operatorname{NMR}(m,R)
=
\frac{\Gamma_{0.05}^{(m,R)}}
{\Gamma_{0.05}^{\mathrm{full}}},
$$

以及机会校正准确率保留

$$
\operatorname{AR}(m,R)
=
\frac{A_{m,R}-1/K}
{A_{\mathrm{full}}-1/K}.
$$

H4 Pass 要求某个 $m\le d/8=256$ 在两个面板上同时满足注册的 NMR、AR 和决策一致率阈值。由于主层 H3 Fail，$\Gamma_{0.05}^{\mathrm{full}}<0$，NMR 不具备正 margin 保持意义。

**实测终态：** `SKIPPED_H3_NOT_PASS`。

这表示前提未满足，不表示“随机投影在满足正 margin 前提时失败”。

### 5.6 门槛结果总表

| 门槛 | 实测状态 | 直接依据 |
| --- | --- | --- |
| H0 全层无偏定位 | `Pass` | 31/48 层同时下界 $>0$；Block 39 达最大净增益 |
| H1 数据有效性 | `Insufficient` overall | 机器守卫通过；独立人工 review 未闭合 |
| H2 Block 48 | `Fail` | 新模板准确率下界 $0.12445\le0.125$ |
| H3 Block 48 | `Fail` | 两面板准确率远低于 0.90，且低尾 margin 为负 |
| H2 Block 38 | `Pass` | 两面板准确率下界均高于机会水平 |
| H3 Block 38 | `Fail` | 两面板准确率远低于 0.90，且低尾 margin 为负 |
| H4 高斯保持 | `SKIPPED_H3_NOT_PASS` | 主层 H3 未通过，NMR 前提不成立 |

---

## 6. 实验设计与数据规范

### 6.1 数据总体与类别结构

数据包含 8 个父类，每个父类包含 8 个细类，共 64 个细类：

| 父类 | 8 个细类 |
| --- | --- |
| 数学 | 代数、分析、组合数学、几何、数论、概率、统计、拓扑 |
| 物理学 | 凝聚态、电磁学、力学、光学、粒子物理、量子物理、相对论、热力学 |
| 化学 | 分析、电化学、无机、核化学、有机、物理、高分子、理论化学 |
| 生物学 | 细胞、发育、生态、进化、遗传、微生物、分子、生理学 |
| 计算机科学 | 算法、人工智能、网络安全、数据库、图形学、网络、操作系统、编程语言 |
| 经济学 | 发展、计量、金融、国际、劳动、宏观、微观、公共经济学 |
| 医学 | 心脏、内分泌、胃肠、免疫、肾脏、神经、肿瘤、呼吸病学 |
| 语言学 | 形态、语音、音系、语用、心理语言、语义、社会语言、句法 |

每个细类 300 条，共 $64\times300=19{,}200$ 条：

| 划分 | 每细类 | 总数 | 角色 |
| --- | ---: | ---: | --- |
| TRAIN | 180 | 11,520 | 拟合残差预测器和分类器 |
| DEV | 40 | 2,560 | 选择正则、定位层和冻结层 |
| TEST-same | 40 | 2,560 | 同模板留出评估 |
| TEST-new | 40 | 2,560 | 新模板留出评估 |

同一语义种子、实体组合、公式实例或数值实例只能进入一个划分。

### 6.2 Binding-controlled prompt

每条 prompt 同时包含来自 8 个父类的 8 张无标签语义卡，并使用 8 个中性 code 随机绑定。问题要求根据目标 code 找到对应语义卡并判断其父类。这样每条样本都包含 8 类词汇，标签由 code--card 绑定关系决定，而不是由某类词汇是否出现决定。

TRAIN、DEV 与 TEST-same 使用同一模板族但语义种子完全隔离；TEST-new 使用未出现在拟合阶段的模板族。所有 prompt 以统一的 `Answer:` 后缀结束，抽取该后缀最后一个 token。

### 6.3 数据守卫

正式数据满足：

- 19,200 个 row ID 唯一，类别、划分和推理类型平衡；
- 不直接出现父类或细类标签作为答案提示；
- 规范化文本无跨划分重复；
- 语义卡有序拼接的跨划分字符 5-gram Jaccard 不超过 0.35；
- 公式骨架、实体组合和数值实例不跨划分复用；
- prompt 长度在 119--302 个实测 token 范围内；
- unigram+bigram 词袋逻辑回归作为廉价泄漏基线；
- 每个细类抽一条定量或机制样本形成 64 条 review pack。

词袋基线在 TEST-same/TEST-new 的 balanced accuracy 为 $0.1270/0.1195$，接近 8 类机会水平 $0.125$，没有形成可替代深层表征的文本捷径。

### 6.4 模型、层和提取

- 模型：`/data/share/Qwen3-30B-A3B`；
- 架构：48 blocks，隐藏维数 2,048；
- 推理：BF16、eval mode、不生成、不更新参数；
- 保存数组：FP32；
- 抽取对象：所有 48 层的 $(X_\ell,U_\ell)$；
- 合并张量形状：`[48, 19200, 2, 2048]`；
- 四个 GPU shard 构成精确划分，有限值、重放、Attention 输出投影和 $U=Z-X$ 恒等式守卫全部通过。

每层残差预测器只在 TRAIN 拟合，DEV 从 $10^{-6}$ 至 $10^2$ 的正则网格中选择 $\lambda$。均值、方差和残差器在 TEST 前冻结。

### 6.5 H0 逐层定位

H0 使用确定性岭回归分数。每层均执行真实 $R_U$、重复 $X$ 和 30 个错配 $R_U$ 条件；所有选择只使用 TRAIN/DEV。2,000 次 bootstrap 以细类为分层单位，并用 48 层最大中心化误差形成同时区间。

选层回执记录完整 48 层表、输入哈希、主层、重复层、最小层间距、H0 状态和 TEST 标签缺失检查。

### 6.6 H2/H3 完整空间 probe

主 probe 是 L2 正则多类逻辑回归：

$$
(\widehat W,\widehat b)
=
\arg\min_{W,b}
\frac1{n_{\mathrm{train}}}
\sum_i
\operatorname{CE}(W^\top r_i+b,y_i)
+\lambda\|W\|_F^2.
$$

使用五个固定种子 24001--24005；DEV 在 $10^{-6}$ 至 $10^2$ 的网格中选正则；最大迭代 10,000，容差 $10^{-7}$。TEST 只在层和超参数冻结后评估一次。

每个 TEST 面板报告 balanced accuracy、macro-F1、正 margin 比例、margin 中位数、$\Gamma_{0.05}$ 及其 95% 区间。区间使用 2,000 次按类别分层 bootstrap，并在五个种子上进行层级聚合。

### 6.7 距离、功能维数与谱坐标诊断

每个冻结层、每个 TEST 面板精确枚举

$$
\binom{2560}{2}=3{,}275{,}520
$$

个无序样本对，其中 408,320 个同父类 pair、2,867,200 个异父类 pair。由此计算极端 $\rho_{\mathrm{dist}}$ 和稳健 $\widetilde\rho_{\mathrm{dist}}$，不使用 pair sampling。

监督正交功能维数 $r_{90}$ 表示机会校正准确率至少保留完整空间 90% 的最小监督投影维数。它是描述性任务维数，不是几何维数。

谱坐标抽样资格只用 TRAIN 差向量计算相干度和定理 5 充分维数；TEST 不参与运行资格选择。

### 6.8 实现与统计对照

以下对照保护结论有效性：

1. 标签置换分类器的区间必须包含机会水平；
2. 恒等投影必须逐样本复现完整空间分数；
3. 给所有样本加入相同向量后，pairwise difference 必须保持；
4. 所有注册 probe 必须收敛；
5. TEST 标签不得进入 H0 或选层；
6. 若 H3 未通过，H4 只能写入 `SKIPPED_H3_NOT_PASS`。

### 6.9 计算证据

正式运行使用一台 reserved 4×H100 80GB worker。正式任务状态为 `SUCCEEDED`；完整性审计确认必需 artifacts 和语义守卫全部存在。原始运行记录保存在实验 Detailed 中，本报告只引用决策相关数字。

---

## 7. 结果解释规则

### 7.1 三类可能分支

**分支 A：H3 Pass，且某个 $m\le d/8$ 通过 H4。**

允许结论：在注册数据、冻结线性 Router 和有限测试分布上，原空间已有的正低尾 margin、机会校正准确率和决策在该维数起被独立稠密高斯投影稳定保持。

**分支 B：H3 Pass，但所有注册低维 $m$ 均未通过 H4。**

允许结论：完整空间存在稳定线性结构，但在注册高斯分布、维数范围和统计精度下没有观察到强压缩保持。不能排除学习型投影或其他随机映射。

**分支 C：H3 Fail。**

允许结论：注册 $R_U$、线性 probe、数据和统计功效下，没有发现独立、稳健、正低尾 margin 的 Router 几何。H4 不具有可解释的正 margin 前提，必须停止。

当前实测属于分支 C。

### 7.2 当前结果允许声称什么

1. $R_U$ 不是“信息为空”：31/48 层在重复 $X$ 与错配 $R_U$ 控制后仍有正条件增量效用；
2. 条件增量信息与独立可路由几何是不同属性；
3. Block 48 和 Block 38 的独立 $R_U$ 都没有达到正低尾 margin；
4. 极端和稳健距离比都低于 1，与“没有独立类别簇 gap”的解释一致；
5. H4 是前提未满足后的条件跳过，而不是投影算法失败。

### 7.3 当前结果不能声称什么

1. 不能声称 $R_U$ 没有信息；
2. 不能声称任何线性子空间都不存在；
3. 不能声称联合 $(X,R_U)$、学习型线性表征或非线性表征不可用；
4. 不能声称随机投影无法保持一个真正具有正 margin 的 Router；
5. 不能把 $r_{90}=64$ 写成 64 维几何流形；
6. 不能把高谱熵写成谱坐标均匀；
7. 不能把父类准确率写成真实专家效用；
8. 不能把 LSH 写成 JL 定理的一部分；
9. 独立人工 H1 复核未完成前，不能把数据语义有效性标为完全闭合。

### 7.4 理论证据与实验观察的边界

数学定理是在明确假设下的演绎结论；有限实验不能“证明”定理。实验只检查 Qwen3-30B-A3B 的冻结对象是否满足定理的前提，并测量相应结果。当前 $\rho_{\mathrm{dist}}<1$、$\Gamma_{0.05}<0$，说明主保持前提没有被实测对象满足，而不是反驳 JL 定理。

---

## 8. 核心图表定义

### 8.1 主图

![Qwen3-30B-A3B 全层增量效用与完整空间准入](../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E02_qwen30b_all_layer_gain_and_preservation/figures/qwen30b_ru_layer_gain_curve.png)

### 8.2 图形契约

**问题。** 哪些 Qwen3-30B-A3B 层的 $R_U$ 对 $X$ 有受控条件增量效用；这些层的独立 $R_U$ 是否接近正低尾 margin 准入？

**数据来源。** 冻结 19,200 条数据；上图的定位指标只使用 TRAIN/DEV。图中主层和重复层在 TEST 打开前冻结。

**上半图。**

- 横轴：Transformer block 1--48；
- 纵轴：受控 DEV 交叉熵降低 $T_\ell$，单位 nat/样本；
- 蓝线：逐层点估计；
- 蓝色带：覆盖全部 48 层的同时 95% 区间；
- 黑色虚线：零净增益；
- 星号：最大净增益 Block 39；
- 金色/紫色竖线：冻结主层 Block 48 与重复层 Block 38。

**下半图。**

- 左纵轴红线：独立 $R_U$ 的 DEV true-label margin 5% 分位数；
- 右纵轴绿线：独立 $R_U$ 的 DEV balanced accuracy；
- 黑色虚线：零 margin；
- 金色/紫色竖线：主层与重复层。

**直接观察。** 31/48 层的受控增量效用同时下界为正，最大值在 Block 39；但所有层的独立 DEV 低尾 margin 都低于 0。主层与重复层是按 H3-readiness 规则选择，不是按最大净增益选择。

**允许结论。** 图支持“条件增量信息广泛存在”与“独立正 margin 几何没有形成”同时成立。

**限制。** 图不显示 H4 投影维数曲线，因为 H3 未通过；不允许从这张图推断真实专家效用或无标签学习一定成功。

### 8.3 决策数值表

| Block | 角色 | 受控增量效用 [同时 95% 区间] | 独立 DEV $\Gamma_{0.05}$ |
| ---: | --- | ---: | ---: |
| 39 | 最大条件增量效用 | 0.10994 [0.09872, 0.12080] | -0.54060 |
| 48 | 冻结主层 | 0.01369 [0.00248, 0.02456] | -0.52554 |
| 38 | 冻结重复层 | 0.06442 [0.05320, 0.07529] | -0.53000 |

---

## 9. 理论与实验结论

### 9.1 理论结论

1. 固定公共成分在样本差分中严格抵消；有界扰动只会以可计算幅度收缩已有距离间隔。
2. 稠密高斯 JL 投影在足够维数下，以高概率统一保持抽取前固定的有限样本距离。
3. 对抽取前固定、具有正最小 margin 的线性 Router，显式投影权重 $\widetilde w_k=Rw_k$ 能以高概率保持有限样本决策；正 $\Gamma_{0.05}$ 只支持对应 95% 低尾子集的稳健版本。
4. 线性投影后接线性 Router 的函数族包含于原空间线性 Router，因此线性投影不能创造原空间函数族中不存在的可分性。
5. 低维仿射子空间并集和低相干谱坐标抽样需要额外假设；监督功能维数和谱熵不能替代这些假设。
6. LSH 是未来大专家池的离散候选检索工具，不是 JL 连续保持定理的组成部分。

### 9.2 实验结论

| 对象 | TEST-same balanced accuracy [95% CI] | TEST-new balanced accuracy [95% CI] | TEST-same $\Gamma_{0.05}$ [95% CI] | TEST-new $\Gamma_{0.05}$ [95% CI] | H2/H3 |
| ---: | ---: | ---: | ---: | ---: | --- |
| Block 48 | 0.17125 [0.16484, 0.17813] | 0.12969 [0.12445, 0.13500] | -5.82955 [-5.95216, -5.74825] | -11.19046 [-11.40759, -11.06038] | `Fail/Fail` |
| Block 38 | 0.31016 [0.30203, 0.31805] | 0.23125 [0.22429, 0.23859] | -3.52356 [-3.59236, -3.46685] | -6.66276 [-6.79532, -6.54119] | `Pass/Fail` |

这里是两个 TEST 面板在两个冻结层上的四个 block--panel 结果。四个 $\Gamma_{0.05}$ 全部为负；主层 Block 48 的两个值为 $-5.83$ 和 $-11.19$。

精确全 pair 距离结果为：

| Block | TEST 面板 | $\rho_{\mathrm{dist}}$ | $\widetilde\rho_{\mathrm{dist}}$ |
| ---: | --- | ---: | ---: |
| 48 | same | 0.3321 | 0.7026 |
| 48 | new | 0.2027 | 0.5315 |
| 38 | same | 0.2314 | 0.5832 |
| 38 | new | 0.2205 | 0.5357 |

极端距离比位于 $0.20$--$0.33$，稳健距离比位于 $0.53$--$0.70$，全部低于 1。监督正交细类读出得到两个层的 $r_{90}=64$，但这是对弱 64 类读出器的功能压缩结果，不是几何 rank。

### 9.3 统一认识更新

理论和实验共同支持的最精确结论是：

> **Qwen3-30B-A3B 的 $R_U$ 中存在超越同层 $X$ 的条件增量信息，但这些信息没有自然组织成一个可独立使用、跨模板稳健且具有正低尾 logit margin 的线性 Router 空间。**

因此，当前瓶颈不是“如何压缩一个已经存在的良好 Router 空间”，而是“如何生成和组织一个与专家功能对齐的 Router 表征空间”。

### 9.4 下一阶段路线

最终决策指向：

> **开展基于无标签自演化与层次化专家树（Hierarchical Expert Tree）的表征空间生成学习。**

这一路线在当前证据下应被定义为新的可证伪研究问题，而不是既成结论：

1. **无标签自演化表征生成：** 不以当前 8 类语义标签作为训练目标，从模型自身轨迹、跨视图一致性和后续可定义的专家功能反馈中学习表示生成器 $g_\theta(X,R_U)$；
2. **层次化专家树：** 用学习到的表示先做粗粒度候选分支，再在子树内做细粒度专家选择，避免一次性在超大专家池中做平面全搜索；
3. **必要对照：** 同时比较 learned standalone $g_\theta(R_U)$、joint $g_\theta(X,R_U)$ 和模型原生 Router 输入，防止把 $X$ 中已有信息误记为 $R_U$ 的独立收益；
4. **最小准入条件：** 在真正留出的数据上，先取得正的低尾 margin 与专家效用一致的改进，再讨论 JL 压缩、LSH 候选检索或树搜索加速；
5. **LSH 的位置：** 只有当学习空间先表现出可靠邻域结构时，LSH 才可作为超大专家池的可选检索后端，它不承担表征生成或正 margin 建立。

当前实验没有证明无标签自演化或层次化专家树必然成功；它只把下一阶段问题从“保持已有空间”精确推进为“生成满足功能门槛的空间”。

---

## 10. 组会同步与认知更新总结

### 10.1 最小汇报

**核心问题：** Qwen3-30B-A3B 的更新残差 $R_U$ 是否已经形成独立、稳定、正 margin 的线性 Router 空间；若形成，能否由低维稠密高斯投影保持？

**目的：** 区分“$R_U$ 对 $X$ 有新增信息”和“$R_U$ 单独具备稳健路由几何”，并保证只有第二项通过后才解释随机投影。

**分析方法：**

1. 用 TRAIN/DEV 对 48 层做重复 $X$ 与错配 $R_U$ 控制下的无偏净增益定位；
2. 冻结 Block 48 主层和 Block 38 重复层，在两个 TEST 面板上评估完整空间准确率、5% 低尾 margin 和全 pair 距离；
3. 仅在主层 H3 通过后运行 JL 高斯投影扫描；本轮因 H3 Fail，H4 按协议跳过。

**理论证据：** 已证明固定公共成分抵消、有界扰动的间隔界、有限样本 JL 距离保持、固定正 margin Router 保持，以及线性投影不能创造线性可分性。扩展定理分别覆盖仿射子空间并集和低相干谱坐标抽样。

**实验结果：**

- H0：31/48 层正净增益；峰值 Block 39，$0.10994$ nat/样本；
- 选层：主层 Block 48，重复层 Block 38；
- H2/H3：Block 48 `Fail/Fail`，Block 38 `Pass/Fail`；
- 四个 block--panel 的 5% margin 全为负：$-5.83$、$-11.19$、$-3.52$、$-6.66$；
- 极端 $\rho_{\mathrm{dist}}=0.20$--$0.33<1$；
- H4：`SKIPPED_H3_NOT_PASS`。

**结论：** 存在条件增量信息，但缺乏独立正 margin 几何。随机投影没有被判为失败，而是没有获得运行与解释所需的正 margin 前提。

**认知更新：** 我们不再把当前问题理解为“压缩哪个层的 $R_U$”，而是理解为“如何让已有条件信息自组织成与专家功能对齐的可路由空间”。

**下一决策：** 开启“无标签自演化表征生成 + 层次化专家树”的新研究阶段；第一项准入证据必须是留出数据上的正低尾 margin 和真实专家效用，而不是仅有方差、谱熵、标签可读性或负载均衡。

### 10.2 一分钟复述

> 我们在 Qwen3-30B-A3B 全 48 层上先测 $R_U$ 是否给 $X$ 增加受控预测信息，再测 $R_U$ 单独是否形成正 margin。31 层确实有正新增效用，峰值在 Block 39；但按开发集冻结的 Block 48 和 Block 38 在测试集都没有正 5% margin，距离比也全部小于 1。因此准确结论是“信息存在，但没有形成独立稳健的 Router 几何”。高斯随机投影只负责保持已有结构，不能创造结构，所以 H4 必须跳过。下一阶段应转向无标签自演化的表征生成，并用层次化专家树组织大规模专家检索；在正 margin 和真实专家效用出现前，不讨论投影或 LSH 加速。

### 10.3 证据来源与阅读入口

- [E02 Summary](../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E02_qwen30b_all_layer_gain_and_preservation/summary.md)：结论优先的冻结数字与边界；
- [E02 Detailed](../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E02_qwen30b_all_layer_gain_and_preservation/detailed.md)：完整设置、区间、控制、运行回执和 artifact map；
- [E02 Protocol](../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E02_qwen30b_all_layer_gain_and_preservation/protocol.md)：门槛、冻结规则与条件执行契约；
- [A15_08_09 Anchor](../../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_09_random_projection_router_preservation_anchor.md)：研究问题和正式结论边界。

本报告是自包含的理论—实验综合阅读面；canonical 数值与执行证据仍以 Protocol、Summary 和 Detailed 为准。

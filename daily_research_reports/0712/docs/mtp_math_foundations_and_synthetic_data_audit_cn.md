# MTP 研究必备数学复习与合成数据审计

> 对应主故事：`Projects/from-attention-to-search/main/stories/12_structured_compositional_mtp_workload/01_structured_composition_workload_and_standard_head_use_cn.md`
> 目标：复习报告所需的信息论与低秩理论，并把合成数据构造及每项实验的数据输入写成可以逐项审计的形式。  
> 当前范围：只讨论下一词元预测（NTP）与后续两个词元预测（Next2），不讨论混合专家模型与路由器。

---

# 0. 先记住整条逻辑链

$$
\boxed{
\text{任务是否真的需要远程信息}
\rightarrow
\text{任务需要哪些独立变量}
\rightarrow
\text{模型是否有足够表征方向}
\rightarrow
\text{Next2 梯度是否与 NTP 冲突}
\rightarrow
\text{语义能否传到主头使用位置}
\rightarrow
\text{最终 NTP 性能}
}
$$

每一类公式只回答其中一个问题：

| 数学对象 | 回答的问题 |
|---|---|
| 熵、条件熵、互信息 | 哪些信息是必要的、远程的、联合的 |
| 梯度内积 | Next2 的一步更新是否损害 NTP |
| 秩、有效秩、子空间 | 模型能否同时承载局部变量和长程变量 |
| 状态转移雅可比 | 当前状态中的语义是否能到达下一位置 |
| 主头准确率或交叉熵 | 最终是否真正变好 |

不能用一个中间量替代另一个层次。例如，探针读出率高不能推出主 NTP 头一定更好。

---

# 1. 信息论基础：公式、物理意义和记忆方法

以下默认离散随机变量。若对数底数为 $2$，单位是 bit；若使用自然对数，单位是 nat。

## 1.1 单个事件的信息量

$$
\iota(x)=-\log p(x).
$$

**物理意义：** 一个事件越罕见，看到它带来的“惊讶”越大，因此信息量越大。

- $p(x)=1$：必然事件，信息量为 $0$；
- $p(x)$ 越小：信息量越大；
- 独立事件同时发生时，概率相乘、信息量相加。

**记忆：**

> 信息量 = 负对数概率 = “越不可能，越有信息”。

## 1.2 熵：平均还不知道多少

$$
H(X)
=
-\sum_x p(x)\log p(x)
=
\mathbb E[-\log p(X)].
$$

**物理意义：** 在观察 $X$ 之前，对 $X$ 的平均不确定性；也等于理想无损编码的平均长度。

若 $X$ 在 $M$ 个类别上均匀分布：

$$
H(X)=\log M.
$$

**记忆：**

> 熵 $H(X)$ = “没看 $X$ 之前，还不知道多少”。

## 1.3 联合熵

$$
H(X,Y)
=
-\sum_{x,y}p(x,y)\log p(x,y).
$$

链式法则：

$$
H(X,Y)=H(X)+H(Y\mid X).
$$

**物理意义：** 先编码 $X$，再在知道 $X$ 后编码 $Y$。

**记忆：**

> 联合 = 先知道第一个需要的长度 + 知道第一个后第二个剩余的长度。

## 1.4 条件熵：知道条件后还剩多少

$$
H(Y\mid X)
=
-\sum_{x,y}p(x,y)\log p(y\mid x).
$$

等价关系：

$$
H(Y\mid X)=H(X,Y)-H(X).
$$

**物理意义：** 已经知道 $X$ 后，$Y$ 还剩多少不确定性。

通常：

$$
H(Y\mid X)\le H(Y).
$$

**记忆：**

> 条件熵 = “知道 $X$ 后，$Y$ 还剩多少不知道”。

## 1.5 互信息：知道一个变量减少了多少不确定性

$$
I(X;Y)
=
H(Y)-H(Y\mid X).
$$

对称形式：

$$
I(X;Y)
=
H(X)+H(Y)-H(X,Y).
$$

KL 散度形式：

$$
I(X;Y)
=
D_{\mathrm{KL}}
\bigl(
p(x,y)\,\|\,p(x)p(y)
\bigr).
$$

**物理意义：**

- 若 $X,Y$ 独立，则联合分布等于边缘分布乘积，$I(X;Y)=0$；
- 若知道 $X$ 能完全确定 $Y$，则 $I(X;Y)=H(Y)$。

**最重要的记忆句：**

$$
\boxed{
I(X;Y)=\text{原来的不确定性}-\text{知道 }X\text{ 后剩余的不确定性}
}
$$

不要首先背三项熵公式；先背“减少量”，其他公式都能推出来。

## 1.6 条件互信息：给定已有信息后，新增变量还有多少价值

$$
I(X;Y\mid Z)
=
H(Y\mid Z)-H(Y\mid X,Z).
$$

**物理意义：** 已经知道 $Z$ 后，再观察 $X$ 能让我们对 $Y$ 少多少不确定性。

这正是长程任务最需要的量：局部上下文已经给定后，远程上下文是否仍有不可替代的信息。

**记忆：**

> 条件互信息 = “已有 $Z$ 以后，$X$ 还能帮多少”。

## 1.7 互信息链式法则

$$
I(Y;X_1,X_2)
=
I(Y;X_1)
+
I(Y;X_2\mid X_1).
$$

推广：

$$
I(Y;X_{1:m})
=
\sum_{i=1}^m
I(Y;X_i\mid X_{<i}).
$$

**物理意义：** 多个证据提供的信息可以按照“逐个加入证据”分解。

注意：每一项依赖加入顺序；总和不依赖顺序。

## 1.8 KL 散度：错误分布相对真实分布的额外编码代价

$$
D_{\mathrm{KL}}(P\|Q)
=
\sum_y P(y)
\log\frac{P(y)}{Q(y)}
\ge 0.
$$

**物理意义：** 数据来自 $P$，却使用 $Q$ 编码时，相比使用真实 $P$ 多花的平均编码长度。

KL 散度不对称：

$$
D_{\mathrm{KL}}(P\|Q)
\neq
D_{\mathrm{KL}}(Q\|P).
$$

**记忆：**

> KL = “真实世界用 $P$，模型却报 $Q$，因此多付出的代价”。

## 1.9 交叉熵：模型实际付出的编码长度

$$
H(P,Q)
=
-\sum_y P(y)\log Q(y).
$$

核心分解：

$$
\boxed{
H(P,Q)
=
H(P)
+
D_{\mathrm{KL}}(P\|Q)
}
$$

含义：

- $H(P)$：任务自身无法消除的不确定性；
- $D_{\mathrm{KL}}(P\|Q)$：模型错误带来的额外代价。

训练交叉熵，本质是在最小化 KL 散度，因为数据分布的熵 $H(P)$ 不由模型改变。

**记忆：**

> 交叉熵 = 世界本来有多难 + 模型额外有多错。

## 1.10 数据处理不等式

若形成马尔可夫链：

$$
X\rightarrow H\rightarrow \widehat Y,
$$

则：

$$
I(X;\widehat Y)\le I(X;H).
$$

**物理意义：** 对信息做后续处理不能凭空增加原始信息。

对本项目的含义：

- 如果 $H$ 中没有任务变量 $Z$，预测头不可能凭空恢复 $Z$；
- 但 $H$ 中有 $Z$，不代表预测头一定会使用它。

因此：

$$
I(H;Z)>0
$$

是可用性的必要条件之一，但不是充分条件。

## 1.11 Fano 不等式：低错误率要求表征中含有足够信息

若 $Z$ 有 $M$ 个类别，使用 $H$ 预测 $Z$ 的错误率为 $P_e$，则：

$$
H(Z\mid H)
\le
h(P_e)+P_e\log(M-1).
$$

于是：

$$
I(Z;H)
=
H(Z)-H(Z\mid H)
$$

满足下界：

$$
I(Z;H)
\ge
H(Z)-h(P_e)-P_e\log(M-1).
$$

**物理意义：** 若从隐藏状态几乎总能正确恢复一个高熵变量，那么隐藏状态中必然含有足够多关于该变量的信息。

**边界：** 它只说明信息存在，不说明模型自己的主头在使用该信息。

---

# 2. 报告中信息论定义的推导和物理意义

## 2.1 非局部信息比例 $L_w$

将决策位置前的上下文拆成：

- 远程部分：
  $$
  X_{\mathrm{far}}=X_{1:T-w};
  $$
- 局部窗口：
  $$
  X_{\mathrm{local}}=X_{T-w+1:T}.
  $$

定义：

$$
L_w
=
\frac{
I(Y;X_{\mathrm{far}}\mid X_{\mathrm{local}},Q)
}{
H(Y\mid X_{\mathrm{local}},Q)
}.
$$

由条件互信息定义：

$$
I(Y;X_{\mathrm{far}}\mid X_{\mathrm{local}},Q)
=
H(Y\mid X_{\mathrm{local}},Q)
-
H(Y\mid X_{\mathrm{full}},Q).
$$

因此：

$$
\boxed{
L_w
=
1-
\frac{
H(Y\mid X_{\mathrm{full}},Q)
}{
H(Y\mid X_{\mathrm{local}},Q)
}
}
$$

只在分母大于 $0$ 时定义。

### 物理意义

局部窗口尚未解决的答案不确定性中，有多少比例可以由远程上下文消除。

- $L_w=0$：远程上下文没有新增价值；
- $L_w=1$：局部窗口不够，而完整上下文能完全解决。

### 必须注意的边界

若任务是确定性的，并且完整上下文总能确定答案，则只要局部窗口不能确定答案，就会有 $L_w=1$。

所以 $L_w$ 测的是：

> 远程信息是否必要。

它不直接测：

- 证据有多远；
- 组合有多深；
- 模型有多难学。

因此还必须同时报告距离 $D$、组合深度 $d$ 和噪声或干扰强度。

## 2.2 联合必要性差值 $\Sigma_m$

定义：

$$
\Sigma_m
=
I(Y;E_{1:m}\mid Q)
-
\max_{A\subsetneq[m]}
I(Y;E_A\mid Q).
$$

### 物理意义

全部证据联合提供的信息，比最强的任何不完整证据集合多多少。

对于两个证据：

$$
\Sigma_2
=
I(Y;E_1,E_2\mid Q)
-
\max
\{I(Y;E_1\mid Q),I(Y;E_2\mid Q)\}.
$$

若：

$$
I(Y;E_1\mid Q)=I(Y;E_2\mid Q)=0,
$$

并且两者联合完全决定 $Y$，则：

$$
\Sigma_2=H(Y\mid Q).
$$

### 边界

$\Sigma_m$ 是我们定义的“联合必要性保护指标”，不是标准的部分信息分解中的严格协同信息。

它适合排除“某个单证据已经足够”的情况，但不能完整区分：

- 冗余信息；
- 独有信息；
- 高阶协同信息。

第一阶段实验使用它足够，但论文中不要把它直接称为标准 synergy。

## 2.3 信息性未来位置

设当前位置为 $t$，任务变量为 $Z$。定义第 $j$ 个未来词元的新增信息：

$$
\phi_j
=
I
\left(
Z;
Y_{t+j}
\mid
X_{\le t},Y_{t+1:t+j-1}
\right).
$$

若：

$$
\phi_j>0,
$$

表示在已经知道前缀和更近的未来词元后，第 $j$ 个未来词元仍包含关于 $Z$ 的新信息。

定义：

$$
\mathcal I_K
=
\{j\le K:\phi_j>0\}.
$$

### 物理意义

MTP 的因果对象不是 $K$ 本身，而是：

> 预测范围内是否覆盖了真正携带新任务信息的位置。

## 2.4 表征充分性

理想条件：

$$
I(Y;E\mid H,Q)\approx0.
$$

等价地：

$$
H(Y\mid H,Q)
\approx
H(Y\mid E,H,Q).
$$

**物理意义：** 一旦知道隐藏状态 $H$ 和问题 $Q$，重新查看原始证据 $E$ 几乎不能进一步改善答案预测。

这是“隐藏状态已经压缩了任务所需信息”的数学表达。

实践中无法直接精确估计，通常通过以下代理验证：

1. 从 $H$ 预测任务变量；
2. 给预测器额外加入原始证据，看损失是否显著下降；
3. 对 $H$ 做因果补丁，看答案是否按任务变量变化。

---

# 3. 公式记忆方法

## 3.1 一张关系图

只先背下面四句：

$$
\boxed{
\begin{aligned}
H(Y)&=\text{原来不知道多少},\\
H(Y\mid X)&=\text{知道 }X\text{ 后还不知道多少},\\
I(X;Y)&=\text{知道 }X\text{ 后减少了多少},\\
D_{\mathrm{KL}}(P\|Q)&=\text{模型报错分布带来的额外代价}.
\end{aligned}
}
$$

然后自动推出：

$$
I(X;Y)=H(Y)-H(Y\mid X),
$$

$$
H(P,Q)=H(P)+D_{\mathrm{KL}}(P\|Q).
$$

## 3.2 “原来—剩余—减少”记忆法

每次见到互信息，强迫自己念一遍：

> 原来有 $H(Y)$ 的不确定性；知道 $X$ 后剩 $H(Y\mid X)$；减少量就是 $I(X;Y)$。

条件互信息只是在前面增加“已经知道 $Z$”：

> 已经知道 $Z$ 后，原来剩 $H(Y\mid Z)$；再知道 $X$ 后剩 $H(Y\mid X,Z)$。

## 3.3 用两个极端情况检查公式

任何信息论公式都检查：

1. **独立情况：**
   $$
   X\perp Y
   \Rightarrow
   I(X;Y)=0.
   $$
2. **完全确定情况：**
   $$
   Y=f(X)
   \Rightarrow
   H(Y\mid X)=0,\quad I(X;Y)=H(Y).
   $$

若公式在这两个极端不符合直觉，通常是条件写错了。

## 3.4 每天两分钟背诵顺序

1. 写：
   $$
   H(Y),\quad H(Y\mid X),\quad I(X;Y).
   $$
2. 不看答案写：
   $$
   I(X;Y)=H(Y)-H(Y\mid X).
   $$
3. 加条件：
   $$
   I(X;Y\mid Z)=H(Y\mid Z)-H(Y\mid X,Z).
   $$
4. 写：
   $$
   H(P,Q)=H(P)+D_{\mathrm{KL}}(P\|Q).
   $$
5. 用一句话解释 $L_w$ 和 $\Sigma_2$。

---

# 4. 低秩表征竞争：NTP 方向究竟是什么

这是报告中最需要澄清的部分。

## 4.1 精确的最小线性模型

定义两个相互独立、已经白化的潜变量：

$$
u\in\mathbb R^{d_u},
\qquad
z\in\mathbb R^{d_z},
$$

$$
\mathbb E[uu^\top]=I,
\qquad
\mathbb E[zz^\top]=I,
\qquad
\mathbb E[uz^\top]=0.
$$

其中：

- $u$：决定下一词元的局部格式、词法或语法变量；
- $z$：决定第二个未来词元的长程组合变量。

输入潜变量：

$$
x=
\begin{bmatrix}
u\\z
\end{bmatrix}.
$$

共享表征为：

$$
h=Wx,
\qquad
W\in\mathbb R^{r\times(d_u+d_z)},
$$

其中 $r$ 是共享表征最多能承载的独立线性方向数。

两个目标分别为：

$$
t_1=A u,
\qquad
t_2=B z.
$$

预测头：

$$
\widehat t_1=C_1h,
\qquad
\widehat t_2=C_2h.
$$

联合平方损失：

$$
\mathcal L_\lambda
=
\mathbb E
\|\widehat t_1-t_1\|^2
+
\lambda
\mathbb E
\|\widehat t_2-t_2\|^2.
$$

平方损失不是语言模型交叉熵的完整等价物；它是对局部线性化后“哪些独立方向需要被共享表征保存”的最小分析模型。

## 4.2 NTP 方向如何构造

NTP 的真实目标映射写成：

$$
T_1=
\begin{bmatrix}
A&0
\end{bmatrix}.
$$

对 $A$ 做奇异值分解：

$$
A=U_A\Sigma_A V_A^\top.
$$

其中 $V_A$ 的列向量是输入潜变量空间中的 NTP 任务方向。

为什么？

沿 $v_i$ 改变输入：

$$
u\rightarrow u+\epsilon v_i
$$

会使 NTP 目标改变：

$$
t_1\rightarrow t_1+\epsilon A v_i.
$$

若对应奇异值 $\sigma_i(A)$ 大，说明该方向对 NTP 输出影响大，必须被共享表示保留。

因此：

$$
\boxed{
\text{NTP 方向}
=
\text{使 NTP 目标或损失显著变化的独立输入/隐藏方向}
}
$$

它不是人工指定的某个向量，而是由任务映射 $A$ 的主奇异方向定义。

未来目标方向同理由 $B$ 的右奇异向量定义。

## 4.3 为什么联合目标选择 $A^\top A+\lambda B^\top B$

将两个目标堆叠：

$$
T_\lambda
=
\begin{bmatrix}
A&0\\
0&\sqrt{\lambda}B
\end{bmatrix}.
$$

共享秩为 $r$ 的表征，相当于寻找 $T_\lambda$ 的最佳秩 $r$ 分解。

根据 Eckart–Young 定理，最佳秩 $r$ 子空间由 $T_\lambda$ 的前 $r$ 个右奇异向量张成。

而：

$$
T_\lambda^\top T_\lambda
=
\begin{bmatrix}
A^\top A&0\\
0&\lambda B^\top B
\end{bmatrix}.
$$

所以联合训练会从两组特征值中选择最大的 $r$ 个：

$$
\{\alpha_i=\sigma_i^2(A)\}
\cup
\{\lambda\beta_j=\lambda\sigma_j^2(B)\}.
$$

## 4.4 低秩竞争的精确含义

若：

$$
r\ge
\operatorname{rank}(A)+\operatorname{rank}(B),
$$

所有 NTP 和未来目标方向都可以保存，不存在由秩约束强制产生的竞争。

若：

$$
r<
\operatorname{rank}(A)+\operatorname{rank}(B),
$$

联合目标只能选一部分方向。

当某个未来方向满足：

$$
\lambda\beta_j>\alpha_i,
$$

它可能挤掉较弱的 NTP 方向 $\alpha_i$。

NTP 的最小残余风险等于未被选择的 NTP 特征值之和：

$$
R_{\mathrm{NTP}}
=
\sum_{i:\,v_i^{\mathrm{NTP}}\notin\mathcal S_r}
\alpha_i.
$$

这里 $\mathcal S_r$ 是联合目标选出的秩 $r$ 子空间。

## 4.5 一个数值例子

设 NTP 有两个必要方向：

$$
\alpha_1=9,\qquad \alpha_2=4.
$$

未来任务有两个方向：

$$
\beta_1=8,\qquad \beta_2=3.
$$

共享秩：

$$
r=2.
$$

### 纯 NTP，$\lambda=0$

选择：

$$
9,\ 4.
$$

两个 NTP 方向都保留，NTP 残余风险为 $0$。

### $\lambda=0.3$

未来方向权重为：

$$
2.4,\ 0.9.
$$

前两大仍是：

$$
9,\ 4.
$$

未来任务暂时没有挤掉 NTP 方向。

### $\lambda=0.6$

未来方向权重为：

$$
4.8,\ 1.8.
$$

前两大变成：

$$
9,\ 4.8.
$$

第二个 NTP 方向 $4$ 被未来方向挤出，NTP 残余风险增加 $4$。

### 若把秩提高到 $r=4$

四个方向都能保存，表示竞争消失。

这就是“容量不足导致 MTP 损害 NTP”的最小数学解释。

## 4.6 与梯度冲突的区别

低秩竞争和梯度冲突不是同一个现象。

| 机制 | 数学对象 | 含义 |
|---|---|---|
| 低秩竞争 | 联合任务需要的子空间维数超过可用秩 | 长期最优表示必须丢掉某些方向 |
| 梯度冲突 | $\langle g_1,g_2\rangle<0$ | 当前一步更新对两个损失方向相反 |
| 跨位置丢失 | $J_{T\to T+1}$ 对任务子空间衰减 | 信息形成后没有到达主头使用位置 |

可能出现：

- 没有长期秩竞争，但当前一步梯度冲突；
- 当前梯度不冲突，但最终低秩解必须取舍；
- 当前状态形成良好，但跨位置后被擦除。

实验必须分别测量。

## 4.7 在 Transformer 中如何定义 NTP 方向

真实模型中没有已知矩阵 $A$。在某个训练检查点，可以用隐藏状态梯度协方差近似 NTP 任务方向：

$$
g_h^{(1)}
=
\nabla_h\ell_{\mathrm{NTP}},
$$

$$
C_1
=
\mathbb E
\left[
g_h^{(1)}
g_h^{(1)\top}
\right].
$$

$C_1$ 的大特征值对应的特征向量，就是对 NTP 损失影响最大的隐藏状态方向。

未来目标同理：

$$
C_2
=
\mathbb E
\left[
g_h^{(2)}
g_h^{(2)\top}
\right].
$$

联合方向由：

$$
C_{\mathrm{joint}}
=
C_1+\lambda C_2
$$

的主特征子空间近似。

可以测：

1. 有效秩：
   $$
   r_{\mathrm{eff}}(C)
   =
   \frac{(\operatorname{tr}C)^2}{\operatorname{tr}(C^2)};
   $$
2. NTP 子空间与联合子空间的投影距离：
   $$
   D_{\mathrm{sub}}
   =
   \|P_1-P_{\mathrm{joint}}\|_F^2;
   $$
3. NTP 方向被联合训练挤出的能量：
   $$
   E_{\mathrm{drop}}
   =
   \operatorname{tr}
   \left[
   C_1(I-P_{\mathrm{joint}})
   \right].
   $$

这些量比“参数量”更直接地反映当前任务上的表征竞争。

---

# 5. 对原合成数据的关键审计

原报告使用了类似：

```text
Lina 的导师是 Omar。
Omar 被分配到 Kyoto。
问题：Lina 的导师被分配到哪里？
```

并希望满足：

$$
I(Y;E_1\mid Q)=0,
\qquad
I(Y;E_2\mid Q)=0.
$$

若 $E_2$ 指单独一句“Omar 被分配到 Kyoto”，这个条件不成立，因为该句直接包含答案 `Kyoto`。

即使模型不知道 `Omar` 是否是正确桥接实体，答案词本身已经出现在 $E_2$ 中，因此通常：

$$
I(Y;E_2\mid Q)>0.
$$

要严格满足单证据零信息，必须将 $E_1,E_2$ 定义为**完整的随机关系表**，而不是目标路径上的单行支持句。

---

# 6. 严格可审计的置换表数据

## 6.1 潜变量

实体集合：

$$
\mathcal E=\{0,\ldots,M-1\}.
$$

每个样本独立采样两个均匀随机置换：

$$
\pi_1,\pi_2\sim\operatorname{Unif}(S_M).
$$

采样查询实体：

$$
A\sim\operatorname{Unif}(\mathcal E).
$$

中间实体和答案：

$$
B=\pi_1(A),
\qquad
Y=\pi_2(B).
$$

## 6.2 两个证据块

第一证据块是完整表：

$$
E_1=\{(i,\pi_1(i)):i\in\mathcal E\}.
$$

第二证据块是完整表：

$$
E_2=\{(i,\pi_2(i)):i\in\mathcal E\}.
$$

两张表的行顺序分别随机打乱。

## 6.3 为什么单个证据块严格没有答案信息

### 只知道 $E_1$

给定查询 $A=a$ 和 $\pi_1$，可以知道：

$$
B=\pi_1(a).
$$

但 $\pi_2$ 是独立均匀随机置换，因此对固定 $B$：

$$
Y=\pi_2(B)
$$

在 $\mathcal E$ 上均匀分布。

所以：

$$
H(Y\mid Q,E_1)=\log M,
$$

$$
I(Y;E_1\mid Q)
=
H(Y\mid Q)-H(Y\mid Q,E_1)
=
0.
$$

### 只知道 $E_2$

给定查询 $A=a$ 和 $\pi_2$，由于 $\pi_1$ 是随机置换：

$$
B=\pi_1(a)
$$

在 $\mathcal E$ 上均匀分布。

置换保持均匀性，因此：

$$
Y=\pi_2(B)
$$

仍在 $\mathcal E$ 上均匀分布。

所以：

$$
I(Y;E_2\mid Q)=0.
$$

### 同时知道两张表

$$
Y=\pi_2(\pi_1(A))
$$

被完全确定：

$$
H(Y\mid Q,E_1,E_2)=0.
$$

因此：

$$
I(Y;E_1,E_2\mid Q)
=
H(Y\mid Q)
=
\log M.
$$

最终：

$$
\boxed{
\Sigma_2=\log M
}
$$

达到最大联合必要性。

## 6.4 序列格式

为了分离局部 NTP 变量和长程组合变量，再独立采样格式变量：

$$
U\sim\operatorname{Unif}\{0,1\}.
$$

输出序列：

```text
<DECIDE> <FMT_U> <ENTITY_Y>
```

于是，在 `<DECIDE>` 位置：

$$
Y_1=\langle \mathrm{FMT}_U\rangle
$$

只依赖局部格式指令 $U$；

$$
Y_2=\langle \mathrm{ENTITY}_Y\rangle
$$

依赖两张远程置换表的组合。

要求：

$$
U\perp(A,\pi_1,\pi_2,Y).
$$

这样才能保证 Next1 和 Next2 的统计目标真正分离。

## 6.5 一条具体文本样本

设 $M=4$：

$$
\pi_1=
\begin{pmatrix}
0&1&2&3\\
2&0&3&1
\end{pmatrix},
\qquad
\pi_2=
\begin{pmatrix}
0&1&2&3\\
1&3&0&2
\end{pmatrix}.
$$

查询 $A=1$。

因此：

$$
B=\pi_1(1)=0,
\qquad
Y=\pi_2(0)=1.
$$

文本可以渲染为：

```text
[RELATION R1]
E3 maps-to E1
E0 maps-to E2
E2 maps-to E3
E1 maps-to E0

...若干完整的干扰关系表...

[RELATION R2]
E2 maps-to E0
E0 maps-to E1
E3 maps-to E2
E1 maps-to E3

[QUERY]
Starting from E1, apply R1 and then R2.
Reply using format F0.

<DECIDE> <F0> E1
```

模型必须：

1. 在 R1 表中查得 $E1\rightarrow E0$；
2. 在 R2 表中查得 $E0\rightarrow E1$；
3. 输出 `E1`。

只看任何一张完整表，答案都是四个实体中的均匀随机变量。

---

# 7. 数据生成算法

```python
for sample_id in range(num_samples):
    pi1 = random_permutation(M)
    pi2 = random_permutation(M)
    query = random_entity(M)
    format_id = random_format()

    bridge = pi1[query]
    answer = pi2[bridge]

    table1 = shuffle([(i, pi1[i]) for i in range(M)])
    table2 = shuffle([(i, pi2[i]) for i in range(M)])

    distractor_tables = generate_independent_permutation_tables(
        count=num_distractors,
        size=M,
    )

    context = render(
        table1=table1,
        table2=table2,
        distractors=distractor_tables,
        query=query,
        format_id=format_id,
        tokenizer="atomic_reserved_tokens",
        randomized_templates=False,
        randomized_block_order=True,
    )

    target = [FORMAT_TOKEN[format_id], ENTITY_TOKEN[answer]]
```

---

# 8. 第一轮实验的确切数据契约

本节是可执行定义。前面章节解释为什么使用置换表；本节固定第一轮实验实际使用的变量取值、样本数量、数据视图和实验映射。除非新 protocol 明确批准，不改变这些值。

## 8.1 两套数据：精确审计集与模型训练集

### 数据集 `D_exact4`：只做信息论精确审计

固定：

$$
M=4.
$$

枚举：

$$
(\pi_1,\pi_2,A,U)
\in
S_4\times S_4\times\{0,1,2,3\}\times\{0,1\}.
$$

样本总数为：

$$
|D_{\mathrm{exact4}}|
=24^2\times4\times2
=4608.
$$

用途只有一个：直接从完整联合分布验证

$$
I(Y;E_1\mid Q)=0,
\qquad
I(Y;E_2\mid Q)=0,
$$

$$
I(Y;E_1,E_2\mid Q)=\log4.
$$

`D_exact4` 不用于训练模型，也不用于选择超参数。

### 数据集 `D_model8`：用于所有小模型实验

固定：

| 项目 | 确切值 |
|---|---:|
| 实体数量 $M$ | 8 |
| 目标关系表 | 2 张：$R_1,R_2$ |
| 干扰关系表 | 4 张 |
| 每张表行数 | 8 |
| 格式变量 | $U\in\{0,1\}$ |
| 查询顺序 | 主数据固定为先 $R_1$ 后 $R_2$ |
| 输入长度 | 155 个原子词元 |
| 目标长度 | 2 个原子词元 |
| 机会准确率 | $1/8=0.125$ |
| 数据生成 seeds | train `71201`; validation `71202`; audit `71203`; test `71204` |
| 模型训练 seeds | `971,972,973,974,975` |

每个实体 `E0` 至 `E7`、表标识、顺序标识、格式标识和答案都是 tokenizer 中的单一保留词元。第一轮不使用自然语言改写，避免把语言学习失败误判为组合或容量失败。

## 8.2 单条样本的完整潜变量

每条基础样本记录：

$$
s=(\pi_1,\pi_2,A,U,D_{1:4},o_{\mathrm{block}},o_{\mathrm{row}}).
$$

其中：

- $\pi_1,\pi_2$：两张目标置换表；
- $A$：查询起点；
- $U$：只决定第一个输出词元的格式变量；
- $D_{1:4}$：四张独立随机置换干扰表；
- $o_{\mathrm{block}}$：六张表的块顺序；
- $o_{\mathrm{row}}$：每张表内部的行顺序。

标签严格由：

$$
B=\pi_1(A),
\qquad
Y=\pi_2(B)
$$

产生。输出为：

$$
[Y_1,Y_2]
=
[\mathrm{FMT}_U,\mathrm{ENTITY}_Y].
$$

并要求：

$$
U\perp(\pi_1,\pi_2,A,B,Y,D_{1:4}).
$$

## 8.3 原子词元序列的确切长度

每张表由 1 个表头词元和 8 行组成；每行固定为 3 个词元：

```text
<TABLE_Rk> E_i <MAPS_TO> E_j ...
```

所以每张表长度为：

$$
1+8\times3=25.
$$

六张表共：

$$
6\times25=150
$$

个词元。查询尾部固定为 5 个词元：

```text
<QUERY> <START_Ea> <ORDER_R1_R2> <FORMAT_Fu> <DECIDE>
```

因此 `<DECIDE>` 及其以前的输入长度严格为：

$$
T=150+5=155.
$$

目标严格为：

```text
<FMT_u> <E_y>
```

所有单证据、局部和替换控制都使用“等长表替换”，不删除词元，因此输入长度始终为 155。

## 8.4 数据划分的确切大小

先采样互不重叠的置换对，再对每个置换对枚举全部：

$$
A\in\{0,\ldots,7\},
\qquad
U\in\{0,1\}.
$$

所以每个置换对产生：

$$
8\times2=16
$$

条样本。

| Split | 置换对数量 | 每对样本数 | 总样本数 | 用途 |
|---|---:|---:|---:|---|
| `train_full` | 512 | 16 | 8192 | 所有短训练实验 |
| `validation_full` | 64 | 16 | 1024 | checkpoint 与阈值选择 |
| `audit_full` | 64 | 16 | 1024 | 一步梯度、子空间和表征审计 |
| `test_full` | 128 | 16 | 2048 | 最终主头与因果控制评估 |

四个 split 不仅要求 $(\pi_1,\pi_2)$ 对不重叠，还要求其中出现的单独 $\pi_1$ 和 $\pi_2$ 也不跨 split 重复。每个 split 内 $A$、$U$ 和答案 $Y$ 都必须精确平衡。

## 8.5 确切的数据视图

下面所有视图均从同一个 `audit_full` 或 `test_full` 基础样本一对一派生，保持 sample id、长度、块数和表面统计一致。

| 视图名 | 改变什么 | 标签如何处理 | 是否训练使用 |
|---|---|---|---|
| `full` | 不改变 | $Y=\pi_2(\pi_1(A))$ | 是，唯一主训练视图 |
| `only_R1` | 用独立随机置换替换 $R_2$ | 保留原始 $Y$，理论只能猜测 | 否，只评估 |
| `only_R2` | 用独立随机置换替换 $R_1$ | 保留原始 $Y$，理论只能猜测 | 否，只评估 |
| `local` | 六张表全部替换为独立置换 | 保留原始 $Y$，理论只能猜测 | 否，只评估 |
| `distractor_swap` | 只重采样四张干扰表 | $Y$ 不变 | 否，只评估 |
| `R1_swap` | 替换 $\pi_1$ | 重算 $B,Y$ | 否，只评估 |
| `R2_swap` | 替换 $\pi_2$ | 重算 $Y$ | 否，只评估 |
| `order_reverse` | 查询改为先 $R_2$ 后 $R_1$ | $Y'=\pi_1(\pi_2(A))$ | 否，只评估 |
| `format_flip` | $U\leftarrow1-U$ | $Y_1$ 改变，$Y_2$ 不变 | 否，只评估 |

注意：`MTP-mask` 不是另一份数据。它读取与 `MTP-info` 完全相同的 `full` 序列，只在损失中遮蔽 `<DECIDE>` 位置的第二未来目标。

## 8.6 一条与正式实验完全同构的 $M=8$ 样本

```json
{
  "sample_id": "test_pair000_A5_U1",
  "M": 8,
  "pi1": [3, 0, 6, 2, 7, 1, 5, 4],
  "pi2": [4, 6, 1, 7, 0, 3, 5, 2],
  "query_A": 5,
  "format_U": 1,
  "distractors": [
    [1, 2, 3, 4, 5, 6, 7, 0],
    [7, 6, 5, 4, 3, 2, 1, 0],
    [2, 3, 4, 5, 6, 7, 0, 1],
    [5, 0, 7, 1, 3, 6, 2, 4]
  ],
  "block_order": ["D2", "R1", "D4", "D1", "R2", "D3"]
}
```

标签计算：

$$
B=\pi_1(5)=1,
\qquad
Y=\pi_2(1)=6.
$$

因此主目标为：

```text
<FMT_1> <E6>
```

同一样本的几个配对控制：

- `format_flip`：目标变为 `<FMT_0> <E6>`；
- `distractor_swap`：目标仍为 `<FMT_1> <E6>`；
- 若 $\pi'_1=[2,5,1,7,0,6,4,3]$，则 `R1_swap` 的答案为 $\pi_2(6)=5$，目标变为 `<FMT_1> <E5>`；
- 若 $\pi'_2=[7,2,6,0,4,1,3,5]$，则 `R2_swap` 的答案为 $\pi'_2(1)=2$，目标变为 `<FMT_1> <E2>`；
- `order_reverse` 的答案为 $\pi_1(\pi_2(5))=\pi_1(3)=2$，目标变为 `<FMT_1> <E2>`。

## 8.7 每一个实验具体使用什么数据

| 实验 | 研究问题 | 训练数据 | checkpoint/选择数据 | 决策数据 | 配对控制数据 |
|---|---|---|---|---|---|
| `E0_exact_information` | 单表是否严格零信息、双表是否联合充分？ | 不训练 | 不使用 | `D_exact4` 全部 4608 条 | 不需要 |
| `E1_one_step_gradient` | $-\eta\lambda\langle g_N,g_A\rangle$ 能否预测真实一步 NTP 差异？ | checkpoint 只由 `train_full` 产生 | `validation_full` | `audit_full` 1024 条，固定分成 32 个 batch，每 batch 32 条 | `format_flip`、`R1_swap`、`R2_swap` 用于区分局部与答案方向 |
| `E2_subspace_representation` | NTP 子空间是否被联合目标挤出，任务变量是否形成并跨位置保持？ | 不新增训练；复用 E1 checkpoints | 不使用 | `audit_full` | `format_flip` 定义局部方向；`R1_swap/R2_swap` 定义组合方向；`local` 检查捷径 |
| `E3_rank_competition` | 固定参数规模时，低秩是否使 Next2 损害 NTP？ | `train_full` 8192 条 | `validation_full` 1024 条 | `test_full` 2048 条 | `only_R1`、`only_R2`、`local`、`distractor_swap`、`R1_swap`、`R2_swap`、`order_reverse` |
| `E4_curriculum` | 课程是否只在已确认的低秩损害区缓解竞争？ | 与 E3 完全相同的 `train_full` | 与 E3 完全相同的 `validation_full` | 与 E3 完全相同的 `test_full` | 与 E3 完全相同；不生成新数据 |
| `E5_cross_position_use` | $h_T$ 中形成的答案方向是否到达 $h_{T+1}$ 的标准主头？ | 不新增训练；读取 E3/E4 checkpoints | 不使用 | `test_full` | `R1_swap`、`R2_swap`、`format_flip` 和隐藏状态配对补丁 |

所有 objective、秩和课程条件使用相同的 sample id 顺序、batch 顺序和 split manifest。数据差异不得成为条件差异。

## 8.8 本文当前明确不使用的数据

第一轮不使用：

- 自然语言模板外推；
- 新实体词表外推；
- 真实多跳问答；
- LongBench 或其他长上下文 benchmark；
- 不同上下文长度、证据数量或组合深度 sweep。

这些属于后续外部有效性实验，需要单独 anchor 和 protocol。本文的合成实验只能判断受控机制，不能支持真实语言或纯预训练收益。

---

# 9. 训练、验证和测试划分

不能简单按样本随机划分，否则模型可能记住实体—模板组合。

建议同时控制四类外推：

## 9.1 置换外推

训练、验证、测试使用互不重叠的 $(\pi_1,\pi_2)$ 对。

## 9.2 模板外推

不进入第一轮 E0--E5；后续若开启文本外推，测试使用未在训练中出现的语言模板。

## 9.3 位置外推

第一轮只随机化块顺序，不把位置外推作为决策条件。真正的位置外推需要单独 protocol。

## 9.4 实体符号外推

第一轮不启用。测试只外推新的置换与组合，不外推新的实体词元。

---

# 10. 必须构造的对照数据

## 10.1 完整证据

$$
(E_1,E_2,Q)
$$

正确率应显著高于机会水平。

## 10.2 只有第一表

$$
(E_1,Q)
$$

理论最优准确率：

$$
1/M.
$$

## 10.3 只有第二表

$$
(E_2,Q)
$$

理论最优准确率：

$$
1/M.
$$

## 10.4 局部窗口

只保留问题、格式指令和 `<DECIDE>` 附近词元。

理论最优准确率：

$$
1/M.
$$

## 10.5 干扰替换

保持 $(E_1,E_2,Q)$ 不变，只替换所有干扰表。

答案必须不变。

## 10.6 证据替换

替换 $\pi_1$ 或 $\pi_2$，重新计算答案。

模型输出必须随新答案改变。

## 10.7 关系顺序反转

问题从“先 $R_1$ 后 $R_2$”改为“先 $R_2$ 后 $R_1$”。

答案通常改变，用于检测模型是否真正执行有序组合。

---

# 11. NTP、Next2 和低秩实验如何在该数据上落地

## 11.1 训练目标

在 `<DECIDE>` 位置：

$$
L_1
=
\operatorname{CE}
\left(
q_1(\cdot\mid h_T),
\mathrm{FMT}_U
\right),
$$

$$
L_2
=
\operatorname{CE}
\left(
q_2(\cdot\mid h_T),
\mathrm{ENTITY}_Y
\right).
$$

标准 NTP 在这两个相邻决策位置上的训练损失必须包含格式词元和答案词元：

$$
L_{\mathrm N}
=L_1+L_{\mathrm{answer}}.
$$

Next2：

$$
L_{\mathrm{Next2}}
=L_{\mathrm N}+\lambda L_2.
$$

标准自回归主头在下一位置的真实答案损失：

$$
L_{\mathrm{answer}}
=
\operatorname{CE}
\left(
q_1(\cdot\mid h_{T+1}),
\mathrm{ENTITY}_Y
\right).
$$

最终比较必须包含 $L_{\mathrm{answer}}$ 或其准确率。

这一修正很重要：若把 NTP 定义成只有 $L_1$，NTP 从未在答案位置得到标准下一词元监督，就不能公平比较 Next2 是否帮助答案预测。E1--E4 的主实验采用上述“决策位置二元组损失”，不包含表格正文的全位置语言建模损失；因此只能支持受控机制结论，不能声称纯预训练收益。

## 11.2 如何人为控制表征秩

在共享主干和预测头之间加入秩为 $r$ 的线性瓶颈：

$$
\widetilde h
=
W_{\mathrm{up}}
W_{\mathrm{down}}h,
$$

其中：

$$
W_{\mathrm{down}}\in\mathbb R^{r\times d},
\qquad
W_{\mathrm{up}}\in\mathbb R^{d\times r}.
$$

所有预测头只读取 $\widetilde h$。

固定主干参数量，只改变：

$$
r\in\{r_{\mathrm{low}},r_{\mathrm{high}}\}.
$$

这样可以把“参数更多”和“任务可用表征秩更高”分开。

## 11.3 实验条件

秩竞争实验 E3 先只比较：

| 容量 | 目标 |
|---|---|
| 低秩 | NTP |
| 低秩 | 静态 Next2 |
| 高秩 | NTP |
| 高秩 | 静态 Next2 |

只有 E3 确认低秩静态 Next2 存在损害后，E4 才在完全相同数据上比较：

| 容量 | 目标 |
|---|---|
| 低秩 | NTP |
| 低秩 | 静态 Next2 |
| 低秩 | 正向课程 Next2 |
| 低秩 | 等累计 $\lambda$ 的延迟阶跃 Next2 |
| 高秩 | 静态 Next2 |
| 高秩 | 正向课程 Next2 |

不扫描 $K$、桥接词和大量损失权重。

## 11.4 关键测量

### 最终答案性能

$$
A_{\mathrm{main}}
=
\Pr[
\arg\max q_1(\cdot\mid h_{T+1})=Y
].
$$

### 梯度冲突

定义标准 NTP 目标和额外未来目标的梯度：

$$
g_{\mathrm N}
=\nabla_\theta L_{\mathrm N},
\qquad
g_{\mathrm A}
=\nabla_\theta L_2.
$$

$$
c_{\mathrm{NA}}
=
\frac{
\langle g_{\mathrm N},g_{\mathrm A}\rangle
}{
\|g_{\mathrm N}\|
\|g_{\mathrm A}\|
}.
$$

这里不能只用 $L_1$ 定义 NTP 方向，因为标准 NTP 还包含答案位置的 $L_{\mathrm{answer}}$。

### 一步有限差分验证

分别执行：

$$
\theta_{\mathrm N}'
=
\theta-\eta g_{\mathrm N},
$$

$$
\theta_{\mathrm M}'
=
\theta-\eta(g_{\mathrm N}+\lambda g_{\mathrm A}).
$$

测量：

$$
\Delta_{\mathrm{obs}}
=
L_{\mathrm N}(\theta_{\mathrm M}')
-
L_{\mathrm N}(\theta_{\mathrm N}').
$$

一阶预测：

$$
\Delta_{\mathrm{pred}}
=
-\eta\lambda
\langle g_{\mathrm N},g_{\mathrm A}\rangle.
$$

若两者在小学习率下不能对应，不能继续使用“一阶梯度冲突”解释训练结果。

### NTP 子空间保持

计算：

$$
C_{\mathrm N}
=
\mathbb E[
\nabla_h L_{\mathrm N}
\nabla_h L_{\mathrm N}^\top
],
$$

$$
C_{\mathrm A}
=
\mathbb E[
\nabla_h L_2
\nabla_h L_2^\top
].
$$

为对应第 4 节的线性任务能量模型，定义诊断矩阵：

$$
C_{\mathrm{task}}
=C_{\mathrm N}+\lambda C_{\mathrm A}.
$$

它不是联合梯度协方差的恒等式；真正的联合梯度协方差还包含交叉项。这里仅用它比较 NTP 与额外任务方向在固定秩预算下的竞争。取主子空间投影 $P_{\mathrm N},P_{\mathrm{task}}$，测：

$$
D_{\mathrm{sub}}
=
\|P_{\mathrm N}-P_{\mathrm{task}}\|_F^2.
$$

### 被丢失的 NTP 能量

$$
E_{\mathrm{drop}}
=
\operatorname{tr}
[
C_{\mathrm N}(I-P_{\mathrm{task}})
].
$$

预测：低秩静态 Next2 中 $E_{\mathrm{drop}}$ 更大，并与 NTP 性能退化相关。

---

# 12. 当前数据设计的审计清单

生成数据后必须逐项回答：

- [ ] 答案在实体集合中严格均匀吗？
- [ ] 格式变量 $U$ 与答案严格独立吗？
- [ ] 只给 $E_1$ 时理论准确率是否为 $1/M$？
- [ ] 只给 $E_2$ 时理论准确率是否为 $1/M$？
- [ ] 两张表联合是否完全决定答案？
- [ ] 行顺序和块顺序是否随机化，并确认第一轮没有混入自然语言模板？
- [ ] 答案词元是否为单一原子词元？
- [ ] 每个实体在每张表中出现频率是否相同？
- [ ] 干扰表是否和目标表具有相同表面统计？
- [ ] 训练和测试置换对是否严格不重叠？
- [ ] 局部窗口是否不包含任何目标表内容？
- [ ] 关系顺序反转是否重新计算答案？
- [ ] Next2 第二头是否经过公平初始化或校准？
- [ ] 最终指标是否使用标准主头从 $h_{T+1}$ 预测答案？

---

# 13. 最后需要背住的十个公式

$$
\iota(x)=-\log p(x)
$$

$$
H(X)=\mathbb E[-\log p(X)]
$$

$$
H(Y\mid X)=H(X,Y)-H(X)
$$

$$
I(X;Y)=H(Y)-H(Y\mid X)
$$

$$
I(X;Y\mid Z)=H(Y\mid Z)-H(Y\mid X,Z)
$$

$$
H(P,Q)=H(P)+D_{\mathrm{KL}}(P\|Q)
$$

$$
L_w
=
1-
\frac{H(Y\mid X_{\mathrm{full}},Q)}
{H(Y\mid X_{\mathrm{local}},Q)}
$$

$$
\Sigma_2
=
I(Y;E_1,E_2\mid Q)
-
\max\{I(Y;E_1\mid Q),I(Y;E_2\mid Q)\}
$$

$$
\Delta_{\mathrm{int}}
\approx
-\eta\lambda
\langle g_1,g_2\rangle
$$

$$
T_\lambda^\top T_\lambda
=
\operatorname{diag}
(A^\top A,\lambda B^\top B)
$$

对应的十句话：

1. 罕见事件信息大。
2. 熵是原始不确定性。
3. 条件熵是知道条件后剩余的不确定性。
4. 互信息是减少的不确定性。
5. 条件互信息是已有条件后新增的信息。
6. 交叉熵等于任务本身难度加模型错误。
7. 长程表示远处信息不可由局部替代。
8. 联合必要性表示完整证据比任何残缺证据多提供多少信息。
9. 负梯度内积表示未来目标正在抵消 NTP 更新。
10. 低秩模型只能保留联合任务能量最大的有限个方向。

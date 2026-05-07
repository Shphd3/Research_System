# 主线、Specialization 定义、Todo3 与 Todo2 的理论文档

## 背景主线
MoE 的核心不是把 token 分给更多 expert，而是先把表示中的共享部分和长尾语义部分分开，再让不同层次的信息拥有不同的正则化生存条件。

这句话可以拆成两半：

1. **表示侧问题**：如果 shared head 太强，router 在全空间里会优先响应共享高频结构，而看不见真正区分语义组的 tail。
2. **优化侧问题**：即使 tail 已经被送进某个 expert，若这个方向上的有效训练推动太弱，它仍会被统一正则压死。

Todo3 属于第一半，是表示侧的根定理。  
Todo2 是对 Todo3 的递归化推进：global head 去掉之后，residual 里是否还存在 local shared structure，需要继续拆。

---

# 一、我们要的 expert specialization 到底是什么，为什么好

## 目标
定义一种**对任务真的有用**的 specialization，而不是只看专家参数是否“不同”。

## 假设
- 输入表示记为 $X$。
- 任务目标记为 $Y$，在语言模型里它可以理解为 next-token 分布或 next-token loss。
- 存在一个潜在因素 $Z$，它表示“会改变正确下一步预测规律的模式”。  
  这里的 $Z$ 不一定是人工标好的语义标签；它可以是 domain、topic、entity family、instruction mode、代码语言、数学/自然语言模式、某种语义关系类型，或者更抽象的 latent mode。
- expert 路由结果记为 $E=r(X)$。

## 数学建模

### 1. 任务模式的最小模型
假设真实预测规律可以写成：

$$
Y = g_Z(X) + \varepsilon
$$

这里：

- $X$：当前 token 的上下文表示。
- $Z$：潜在模式，表示“当前这个位置到底落在哪种预测机制下”。
- $g_Z$：在模式 $Z$ 下的真实预测规律。
- $\varepsilon$：剩余噪声。

这条式子的物理意义很简单：

> 同样的表面形式 $X$，如果它处在不同的语义/任务模式 $Z$ 下，正确的下一步预测规律可能不一样。

### 2. 给定路由后，一个 expert 真正在做什么
路由把样本送到 expert $E=e$ 后，这个 expert 最理想的预测器是：

$$
f_e^*(x) = \mathbb E[Y \mid X=x, E=e]
$$

这句话的意思是：

> expert $e$ 能做到的最好情况，就是在“被送给它的样本子分布”上，输出条件期望。

把上式代入 $Y = g_Z(X)+\varepsilon$，得到：

$$
f_e^*(x)=\mathbb E[g_Z(x)\mid X=x,E=e]
$$

也就是说，expert $e$ 看到的其实是**多个模式 $Z$ 的混合平均**。

### 3. 为什么 specialization 好：它减少了 expert 内部的模式混杂
给定路由 $E$，全局最优风险可以写成：

$$
\mathcal R^*(E)=\mathbb E\big[(Y-f_E^*(X))^2\big]
$$

根据条件方差分解，

$$
\mathcal R^*(E)=\mathbb E\big[\operatorname{Var}(Y\mid X,E)\big]
$$

再代入 $Y=g_Z(X)+\varepsilon$，若 $\varepsilon$ 的条件方差记为 $\sigma^2$，则

$$
\mathcal R^*(E)=\sigma^2 + \mathbb E\big[\operatorname{Var}(g_Z(X)\mid X,E)\big]
$$

这里最关键的是第二项：

$$
\mathcal H(E;Z):=\mathbb E\big[\operatorname{Var}(g_Z(X)\mid X,E)\big]
$$

它的物理意义是：

> **同一个 expert 内部，还混着多少“互相不一样的预测规律”。**

如果一个 expert 同时接收很多不同模式 $Z$ 的样本，那么即使这些样本都经过同一个 $X$ 附近，它们需要的真实函数 $g_Z$ 也不一样，expert 就被迫去拟合一个混合平均，结果会更差。

因此，**好的 specialization** 不应该定义成“专家彼此不同”，而应该定义成：

> 路由 $E$ 是否让每个 expert 内部的任务模式更单一，从而让 $\mathcal H(E;Z)$ 更小。

### 4. 为什么这种好是实质性的
这不是一个“看上去更整齐”的指标，而有三层实质意义。

#### 第一层：每个 expert 的子问题更简单
若一个 expert 内部混了很多不同模式，它要学的是多个函数的平均；  
若一个 expert 内部模式更纯，它要学的是更单一的函数。

所以 specialization 的首要收益是：

> **固定参数量下，每个 expert 的拟合目标更简单。**

#### 第二层：梯度更一致，训练更稳
当一个 expert 里混着互相不一致的模式时，不同样本给出的梯度方向会互相打架。  
当一个 expert 里的样本在模式上更纯时，梯度更容易对齐。

所以 specialization 很可能带来：

> **更小的梯度冲突，更快的收敛，更稳定的训练。**

这里“训练更快”是**次级后果**，不是定义本身。

#### 第三层：真正受益的下游场景
specialization 最容易帮助下面这些场景：

1. **长尾知识 / 垂直领域**：例如医学、法律、代码、数学、冷门实体。
2. **模式切换明显的任务**：例如 code vs prose、工具调用 vs 叙述文本、公式推导 vs 常规生成。
3. **歧义消解强依赖上下文模式的场景**：例如同一 token 在不同 domain / word sense 下含义不同。
4. **组合式任务**：需要先识别当前语义模式，再调用对应子机制。

它不一定对所有频繁、共享、浅层句法型 token 都同等显著。  
因为这些 token 本来就更接近 shared head，未必需要很强的 specialization。

---

# 二、什么是“语义信号”，为什么我们老用标签 $z$

## 目标
澄清：理论里的 $z$ 不是说“每个 token 都有一个完美的人类标签”。

## 假设
我们需要一个变量来表示“会改变预测规律的潜在模式”。

## 数学建模

### 1. $z$ 的本质
在这里，$z$ 不是“词性标签”或“唯一的人类语义标签”。  
更准确地说，$z$ 是：

> **一个 latent factor：当它改变时，下一步预测规律也会改变，而且理想路由也应该跟着改变。**

因此，$z$ 可以是：

- 人工定义的 proxy label；
- document / span 级别的属性；
- teacher embedding 上的聚类；
- 某种隐变量分解的责任概率。

### 2. 为什么语言里一个 token 的标签可能并不唯一
这很正常。真实语言里的一个 token 常常同时带着多种属性：

- topic
- domain
- syntax role
- discourse role
- named entity type
- task mode

因此，一个 token 未必对应一个硬标签 $z$。  
更合理的做法是把 $z$ 看成**软变量**，即每个样本有一个 soft membership：

$$
q_n(z)=\Pr(Z=z\mid x_n)
$$

### 3. 硬标签和软标签怎么统一
如果是硬标签，分组均值是：

$$
\mu_z = \frac{1}{N_z}\sum_{n:y_n=z} x_n
$$

如果是软标签，则改成加权均值：

$$
\mu_z = \frac{\sum_n q_n(z)x_n}{\sum_n q_n(z)}
$$

后面的组间散度和组内散度也都可以做成 weighted version。  
所以理论里先写硬标签，是因为它最清楚；不是因为真实语言必须有完美硬标签。

### 4. 这里说的“语义信号”到底是什么
“语义信号”不要理解成玄学。  
这里它的意思很具体：

> **表示里那些能帮助区分潜在模式 $Z$，并且这种区分会改变真实预测规律的成分。**

所以它的判定标准不是“像不像人类语义”，而是：

- 它能不能稳定地区分不同模式；
- 这种模式差异会不会改变 next-token 的最优预测。

---

# 三、Todo3：Head Removal 之后的 separability 到底怎么定义，为什么不 trivial

## Todo3 和主线的关系
Todo3 是表示侧主线的根基。  
它负责回答：

> 为什么 router 不该直接在 full representation 上工作，而应该先去掉 centered covariance 的 shared head，再在 tail 上分流。

如果这个问题没定义清楚，后面所有关于 routing purity、expert specialization、递归拆分的说法都会悬空。

---

## 目标
定义一种**和 MoE specialization 真正相关**的 separability，而不是“图看起来更开”。

## 假设
- 给定某个与任务相关的 latent / proxy factor，记为 $z$。
- 表示记为 $x$。
- 我们先做 centered：

$$
x_c = x-\mu
$$

- 然后移除 centered covariance 的 top-$k$ 主方向 $V_k$：

$$
x_{\text{tail}} = P_t x_c,\qquad P_t=I-V_kV_k^\top
$$

这里：

- $\mu$：全局均值。
- $V_k$：共享高方差 head 子空间。
- $P_t$：把 shared head 去掉后的 tail 投影。
- $x_{\text{tail}}$：真正供 router 使用的 residual 表示。

## 数学建模

### 1. 几何 separability：组间散度 / 组内散度
对标签 $z$，定义组间散度和组内散度：

$$
B_z=\sum_c \pi_c (\mu_c-\mu)(\mu_c-\mu)^\top
$$

$$
W_z=\sum_c \pi_c \operatorname{Cov}(x\mid z=c)
$$

每个变量的物理意义：

- $\pi_c$：第 $c$ 个语义组的占比。
- $\mu$：全局均值。
- $\mu_c$：第 $c$ 个语义组的中心。
- $B_z$：**不同语义组中心彼此离得有多远**，是“组间信号”。
- $W_z$：**在固定语义组内部，样本还散得多不多**，是“组内噪音 / nuisance”。

于是定义 Fisher 型 separability：

$$
\mathrm{Sep}_F(P;z)=\frac{\operatorname{tr}(P B_z P^\top)}{\operatorname{tr}(P W_z P^\top)}
$$

它的物理意义很直接：

> 分子越大，说明不同组更远；分母越小，说明同组更紧。  
> 所以这个比例越大，语义组越容易分开。

### 2. 为什么“去掉均值更可分”不是核心
如果只做

$$
x' = x-\mu
$$

那么基于 centered scatter 的 separability 不变，因为：

- 组间中心差 $(\mu_c-\mu)$ 不变；
- 组内协方差也不变。

所以：

> **单纯去均值本身几乎是平凡操作，不是你们要 claim 的深刻点。**

真正非平凡的是：

> **去掉的是 shared high-variance subspace，而不是常数偏置项。**

### 3. Head removal 什么时候真的有利
设被移除的子空间基为 $U$。  
定义：

$$
b=\operatorname{tr}(B_z),\qquad w=\operatorname{tr}(W_z)
$$

再定义该子空间里被移除掉的“组间信号”和“组内噪音”：

$$
\delta_b=\operatorname{tr}(U^\top B_z U)
$$

$$
\delta_w=\operatorname{tr}(U^\top W_z U)
$$

物理意义：

- $\delta_b$：你删掉的子空间里，有多少原本对区分语义组有用的信号。
- $\delta_w$：你删掉的子空间里，有多少只是同组内部的共享噪音。

删掉之后的 separability 是：

$$
\mathrm{Sep}_F(P_t;z)=\frac{b-\delta_b}{w-\delta_w}
$$

要让它比原来更大，需要：

$$
\frac{b-\delta_b}{w-\delta_w} > \frac{b}{w}
$$

整理得到核心判据：

$$
\frac{\delta_b}{b} < \frac{\delta_w}{w}
$$

这句话非常关键，它的意思是：

> **只有当被删掉的子空间里，删掉的噪音比例大于删掉的语义信号比例时，head removal 才真正提升 separability。**

所以它并不 trivial。  
它不是“删共同部分一定更好”，而是一个**有条件成立**的命题。

### 4. 为什么这种 separability 和 MoE specialization 直接相关
仅仅有几何定义还不够，因为你们关心的是 routing。

所以再定义一个和简单 router 直接相关的版本：

$$
\mathrm{Sep}_{\mathcal R}(P;z)=1-\inf_{r\in\mathcal R}\Pr[r(Px)\neq z]
$$

其中 $\mathcal R$ 可以取线性 softmax router。

物理意义：

> 在固定简单 router 类下，投影后的表示能不能更好地预测模式 $z$。

这和 specialization 的关系是：

- 若 $z$ 更容易被 router 识别；
- 那么同一模式更容易进同一 expert；
- expert 内部的模式混杂更小；
- 前面定义的 $\mathcal H(E;Z)$ 也更小。

因此，这种 separability 不是视觉效果，而是**直接指向 MoE specialization 有用性**。

---

## 对 $x_{\text{tail}}=(I-V_kV_k^\top)(x-\mu)$ 路由的分析

### 结论先说
它**不是永远对**，但它和上面的 specialization 定义是对齐的，只要满足一个核心条件：

> 被去掉的 top-$k$ 主要承载 shared nuisance，而不是决定路由的语义信号。

### 为什么它会让 expert 接收更“专一”的信号
设 router 用 $x_{\text{tail}}$ 做决策。  
若上面的条件满足，则：

1. $W_z$ 中很多共享高方差噪音被去掉；
2. 组间有用差异保留得更多；
3. 线性 router 更容易按模式 $z$ 分流；
4. 每个 expert 的 $p(z\mid e)$ 会更尖锐；
5. expert 内部任务混杂更小。

这里“更专一”不是说 expert 只接收一个标签，  
而是说：

> **同一 expert 里，真正决定预测规律的模式混杂被减少了。**

### 它什么时候会失败
有三类典型失败条件：

1. **语义信号泄漏到 head 中**：删掉 head 时顺手把有用语义删掉了。
2. **$k$ 取太大**：过度截断，删掉了本该留给 router 的信息。
3. **估计的 $V_k$ 不稳定**：协方差估计过噪，去掉的不是稳定的 shared head。

因此，$x_{\text{tail}}$ 路由不是“理论上无条件最优”，而是：

> **当 shared head 真的是 nuisance 时，它是和 specialization 定义最一致的简单路由方式。**

---

# 四、Todo2：为什么 global tail 之后还要继续拆

## 目标
解释：为什么去掉 global head 之后，residual 里仍可能分不开；以及为什么继续做 local / conditional 的低秩拆分是合理的。

## 假设
语言表示可能有分层共享结构。  
一个合理的最小模型是：

$$
x = \mu + x_{\text{head}}^{(0)} + x_{\text{common}}^{(1)} + x_{\text{tail}}^{(1)}
$$

其中：

- $x_{\text{head}}^{(0)}$：全局共享 head，所有 token 都能看到。
- $x_{\text{common}}^{(1)}$：不是全局共享，而是在某个 coarse 组内部共享的 **local / conditional common**。
- $x_{\text{tail}}^{(1)}$：更细粒度的、真正用于 finer routing 的 residual。

注意：这里不建议再把第二项叫“common”而不加限定。  
更准确的名字是：

> **local common / conditional head**

因为它不是全局共享的，而是在某个粗粒度组内共享。

## 数学建模

### 1. 两层 latent factor
引入两层模式变量：

- $Z_1$：粗粒度模式，比如大 domain / 大任务类型。
- $Z_2$：细粒度模式，比如该 domain 内部的 finer semantic mode。

设第一次 global head removal 后得到：

$$
x^{(1)} = P_{\text{global}}(x-\mu)
$$

但在固定 $Z_1=c$ 的条件下，$x^{(1)}$ 里仍可能有一组强主方向 $U_c$，它们主要是 coarse group 内部共享的 local structure，而不是区分 $Z_2$ 的信号。

于是对每个 coarse group 再做一次 local projection：

$$
x_c^{(2)} = P_{\text{local},c}(x^{(1)}-\mu_c),\qquad P_{\text{local},c}=I-U_cU_c^\top
$$

### 2. 为什么这会有好处
物理上，这一步做的是：

> 在 coarse group 内，再把“组内共享但不帮助 finer routing 的低秩结构”去掉。

好处有三层：

1. **进一步减少 finer routing 的组内噪音**。  
2. **把 flat 一次性路由变成 coarse-to-fine 的分层路由**，降低单次路由难度。  
3. **让 expert 收到的样本更纯**，从而让 deeper expert 的 specialization 更稳定。

### 3. Todo2 的 separability 判据
在每个 coarse group $c$ 内，对 finer label $z_2$ 也定义自己的组间 / 组内散度：

$$
B_{z_2}^{(c)},\qquad W_{z_2}^{(c)}
$$

若 local head $U_c$ 移除掉的 nuisance 比移除掉的 fine-signal 更多，即：

$$
\frac{\delta_{b,c}}{b_c} < \frac{\delta_{w,c}}{w_c}
$$

则 local head removal 会提升该 coarse group 内的 finer separability。  
这就是 Todo3 判据在局部条件分布上的递归版本。

### 4. 对架构的启发
因此，Todo2 支持的不是“继续硬拆 tail”，而是：

> **在 coarse group 内，识别 local common，再把更深的 tail 留给下一层 router / expert。**

对应的 forward 可以写成一个更合理的层级形式：

$$
h_{\text{out}}
=E_{\text{common}}^{(0)}(x)
+
E_{\text{common}}^{(1)}(x^{(1)}, Z_1)
+
E_{\text{tail}}^{(2)}(x^{(2)}, Z_1, Z_2)
$$

这说明：
- global common 处理全局共享部分；
- local common 处理 coarse 组内共享部分；
- deeper tail 才交给更细粒度的 expert。

---

# 五、把三件事收束成一句清楚的话

1. **好的 specialization** 不是让专家参数看起来不同，而是让每个 expert 内部的任务模式更纯，从而减少模式混杂误差 $\mathcal H(E;Z)$。  
2. **Todo3** 说明：单纯去均值不够；真正重要的是去掉 centered covariance 的 shared high-variance head，这会在条件成立时提升和语义相关的 separability，并改善简单 router 的分流。  
3. **Todo2** 说明：global tail 之后 residual 里还可能有 local common；因此应该递归地做 conditional low-rank removal，形成 coarse-to-fine 的层级组合式 MoE。

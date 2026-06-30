# 软路由与 Top-K 路由的高增益坍塌机制解释

## TL;DR

本文要解释的核心问题是：路由器（router）的门控向量（gating vector）会不会被已有高增益方向吸引，从而导致路由坍塌、专家欠训练、门控学不到真正区分性方向。

当前判断：这个机制是数学上成立的，但不是无条件成立。严格条件是：路由误差信号在某个高增益输出方向上有非零投影，并且 Top-K 选择机制让未选专家长期缺少任务梯度。此时高增益方向会获得更大一阶下降收益，路由器会更倾向继续强化它。

负载均衡损失可以缓解“负载不均”，z-loss 可以缓解“logit 过大和数值不稳定”，但二者都不能单独保证门控向量学到专家条件化的区分性方向。因此它们可能修复表面负载，却不一定修复“语义路由坍塌”。

---

## 0. Thinking Card

**Phenomenon:** MoE 训练中，少数专家或少数路由方向吸收大量 token，其他专家得到较少训练，门控向量可能学习公共高频方向而不是区分性方向。

**Mechanism guess:** 路由矩阵中已有高增益方向会放大对应的路由误差梯度；Top-K 选择进一步造成“被选专家继续收到梯度，未选专家缺少梯度”的正反馈。

**Key variables:** 路由 logit $a$，路由概率 $q$，专家输出 $E_e(h)$，路由误差信号 $\gamma$，路由矩阵奇异值 $\sigma_i$，Top-K 选择集合 $S_K$，专家负载 $f_e$。

**Causal relation:**

$$
\text{high } \sigma_i + \langle u_i,\gamma\rangle\neq 0
\Rightarrow
\text{large router-gradient gain}
\Rightarrow
\text{larger logit margin}
\Rightarrow
\text{Top-K selection lock-in}.
$$

**Observable metric:** 高增益梯度占比、Top-K 边界间隔、未选专家任务梯度范数、专家负载不均、路由-专家效用对齐度。

**Rival Explanations:** 专家初始化差异、数据频率偏置、容量限制导致 token drop、通信/实现造成的局部负载偏差、辅助损失梯度干扰。

**Decision:** 若高增益投影指标能预测后续负载集中和区分性失败，则继续研究“高增益路由病态”；否则转向专家能力差异或容量机制。

---

## 1. 术语解释

**路由器（router）：** 给定 token 隐藏表示 $h\in\mathbb{R}^d$，输出每个专家的分数。

$$
a = Rh, \qquad a\in\mathbb{R}^N.
$$

其中 $R\in\mathbb{R}^{N\times d}$ 是路由矩阵，$N$ 是专家数。

**门控向量（gating vector）：** 路由矩阵 $R$ 的第 $e$ 行 $r_e^\top$。它决定专家 $e$ 对输入 $h$ 的打分：

$$
a_e = r_e^\top h.
$$

**软路由（soft routing）：** 所有专家都以 softmax 权重参与输出。

$$
q_e=\operatorname{softmax}(a)_e,
\qquad
y=\sum_{e=1}^N q_e E_e(h).
$$

**Top-K 路由：** 只选择分数最高的 $K$ 个专家。

$$
S_K(h)=\operatorname{TopK}(a),
\qquad
 y=\sum_{e\in S_K} q_e^K E_e(h).
$$

**路由坍塌（routing collapse）：** 少数专家长期获得过高负载，其他专家长期欠训练。更强的版本是：即使负载被均衡，门控仍未学到与专家能力匹配的区分性方向。

**高增益方向（high-gain direction）：** 若路由矩阵奇异值分解为

$$
R=\sum_i \sigma_i u_i v_i^\top,
$$

则 $v_i$ 是输入侧方向，$u_i$ 是专家-logit 侧方向，$\sigma_i$ 是该方向的放大倍数。若 $\sigma_i$ 大，则

$$
Rv_i=\sigma_i u_i.
$$

---

## 2. 软路由的一阶梯度

设主损失为 $\mathcal{L}(y)$，输出侧梯度为

$$
g_y=\nabla_y\mathcal{L}.
$$

定义第 $e$ 个专家的局部一阶代价：

$$
s_e=\langle g_y,E_e(h)\rangle.
$$

$s_e$ 的含义是：如果增加专家 $e$ 的权重，损失一阶上会增加多少。$s_e$ 越小，说明专家 $e$ 对当前 token 越有利。

软路由输出为

$$
y=\sum_e q_e E_e(h),\qquad q=\operatorname{softmax}(a).
$$

令

$$
\bar{s}=\sum_j q_j s_j.
$$

则路由 logit 的梯度是

$$
\gamma_e
:=
\frac{\partial \mathcal{L}}{\partial a_e}
=
q_e(s_e-\bar{s}).
$$

解释：

- 若 $s_e<\bar{s}$，则 $\gamma_e<0$。梯度下降会增大 $a_e$，即提高专家 $e$ 的路由概率。
- 若 $s_e>\bar{s}$，则 $\gamma_e>0$。梯度下降会减小 $a_e$，即降低专家 $e$ 的路由概率。

所以软路由真正学习的是：

$$
\text{提高比当前平均专家更有用的专家，压低更差的专家。}
$$

---

## 3. 门控向量如何更新

因为

$$
a_e=r_e^\top h,
$$

所以

$$
\frac{\partial \mathcal{L}}{\partial r_e}=\gamma_e h.
$$

梯度下降给出

$$
\Delta r_e=-\eta\gamma_e h.
$$

含义：

- 若专家 $e$ 对当前 token 更有用，即 $\gamma_e<0$，则

$$
\Delta r_e=\eta |\gamma_e|h.
$$

门控向量 $r_e$ 会向这个 token 的表示 $h$ 靠近。

- 若专家 $e$ 对当前 token 更差，即 $\gamma_e>0$，则

$$
\Delta r_e=-\eta\gamma_e h.
$$

门控向量 $r_e$ 会远离这个 token 的表示 $h$。

这给出最基本的路由学习机制：

$$
\boxed{
\text{专家相对有用} \Rightarrow \text{该专家 gating vector 吸收该 token 表示方向。}
}
$$

---

## 4. 高增益方向如何放大路由学习

考虑路由矩阵的奇异值分解：

$$
R=\sum_i \sigma_i u_i v_i^\top.
$$

路由误差信号是

$$
\gamma=\nabla_a\mathcal{L}.
$$

对隐藏表示的梯度是

$$
\nabla_h\mathcal{L}
=R^\top\gamma
=
\sum_i \sigma_i\langle u_i,\gamma\rangle v_i.
$$

因此，若路由误差信号在某个输出方向 $u_i$ 上有投影：

$$
\langle u_i,\gamma\rangle\neq 0,
$$

则隐藏表示上的梯度会沿 $v_i$ 方向被 $\sigma_i$ 放大。

若对隐藏表示做一小步梯度下降：

$$
\delta h=-\eta R^\top\gamma,
$$

诱导的 logit 变化为

$$
\delta a=R\delta h
=-\eta RR^\top\gamma
=-\eta\sum_i \sigma_i^2\langle u_i,\gamma\rangle u_i.
$$

一阶损失变化为

$$
\Delta\mathcal{L}
\approx
\langle \gamma,\delta a\rangle
=
-\eta\sum_i \sigma_i^2\langle u_i,\gamma\rangle^2.
$$

关键结论：

$$
\boxed{
\text{第 }i\text{ 个路由模式的一阶下降收益正比于 }
\sigma_i^2\langle u_i,\gamma\rangle^2.
}
$$

所以高增益本身不是充分条件。它必须和路由误差方向有投影。

更严谨地说：

$$
\sigma_i\text{ 大}
\not\Rightarrow
\text{一定被复用}.
$$

真正条件是：

$$
\sigma_i^2\langle u_i,\gamma\rangle^2
\text{ 相对其他方向更大。}
$$

---

## 5. 为什么这会导致 gating vector 学到公共高增益方向

门控向量的更新是

$$
\Delta r_e=-\eta\gamma_e h.
$$

若 token 表示 $h$ 本身主要落在公共高增益子空间 $\mathcal{V}_H$ 中，则

$$
\frac{\|P_{\mathcal{V}_H}\Delta r_e\|}{\|\Delta r_e\|}
=
\frac{\|P_{\mathcal{V}_H}h\|}{\|h\|}.
$$

这说明：门控向量更新方向由 token 表示 $h$ 决定。如果 $h$ 的主能量来自公共特征，例如频繁语法、常见 token 模式、位置模式或通用上下文模式，那么 gating vector 会优先学习这些方向。

这会产生病态：

$$
\text{公共高频方向可快速降低损失}
\Rightarrow
\text{门控向量对公共方向变敏感}
\Rightarrow
\text{Top-K 更常选择已有专家}
\Rightarrow
\text{其他专家缺少任务梯度}
\Rightarrow
\text{更难学到区分性方向。}
$$

---

## 6. Top-K 路由的推广

### 6.1 固定 Top-K 集合下的局部模型

令

$$
S=S_K(a)
$$

表示当前被选中的 $K$ 个专家。在一个小邻域内，如果 Top-K 集合不变，可以把它当作固定集合分析。

若采用 Top-K 内重新归一化：

$$
q_e^K=
\frac{\exp(a_e)}{\sum_{j\in S}\exp(a_j)}\mathbf{1}\{e\in S\},
$$

输出为

$$
y=\sum_{e\in S}q_e^K E_e(h).
$$

则路由梯度为

$$
\gamma_e^K=
\begin{cases}
q_e^K(s_e-\bar{s}_S), & e\in S,\\
0, & e\notin S,
\end{cases}
$$

其中

$$
\bar{s}_S=\sum_{j\in S}q_j^K s_j.
$$

这说明：

$$
\boxed{
\text{未选专家在任务损失下没有一阶路由梯度。}
}
$$

这是 Top-K 比软路由更容易锁死的核心原因。

### 6.2 使用全 softmax 权重但只 dispatch Top-K 的情况

有些实现先计算全 softmax：

$$
q=\operatorname{softmax}(a),
$$

然后只把 token 送到 Top-K 专家，输出近似为

$$
y=\sum_{e\in S}q_e E_e(h).
$$

此时未选专家可能通过 softmax 分母获得梯度，但这种梯度不是专家效用梯度。它主要来自概率竞争，而不是“这个专家是否适合该 token”的直接证据。

因此，即便不是严格零梯度，未选专家的学习信号仍然弱于被选专家。

### 6.3 Top-K 的正反馈

Top-K 有一个离散边界：

$$
\Delta_K=a_{(K)}-a_{(K+1)}.
$$

若 $\Delta_K$ 变大，则 Top-K 集合更稳定，未选专家更难进入集合。

于是得到正反馈：

$$
\text{早期被选}
\Rightarrow
\text{获得专家参数梯度和路由梯度}
\Rightarrow
\text{logit 更高}
\Rightarrow
\Delta_K\text{ 更大}
\Rightarrow
\text{继续被选。}
$$

高增益方向会加强这个正反馈，因为它让某些 logit 变化更快：

$$
\delta a_i
\propto
\sigma_i^2\langle u_i,\gamma\rangle.
$$

---

## 7. 负载均衡损失能缓解什么

Switch 风格负载均衡损失通常写作

$$
\mathcal{L}_{\text{bal}}
=\alpha N\sum_{e=1}^N f_eP_e.
$$

其中：

$$
f_e=\text{batch 中被分配到专家 }e\text{ 的 token 比例},
$$

$$
P_e=\frac{1}{T}\sum_{t=1}^T q_{e,t}.
$$

它的作用是让专家使用率更接近均匀分布。

对 router logit 的近似梯度形态是

$$
\frac{\partial \mathcal{L}_{\text{bal}}}{\partial a_{e,t}}
\approx
\frac{\alpha N}{T}
q_{e,t}\left(f_e-\sum_j f_jq_{j,t}\right).
$$

含义：

- 高负载专家会被压低；
- 低负载专家会被抬高；
- 该项不看专家是否真的适合当前 token。

所以负载均衡损失能缓解：

$$
\text{load collapse：少数专家负载过高。}
$$

但它不能保证缓解：

$$
\text{semantic collapse：路由没有学到专家条件化的区分性方向。}
$$

因此可能出现一种假象：负载看起来均衡，但 token 被均匀打散到专家，并不是因为专家真的分工清楚。

---

## 8. z-loss 能缓解什么

router z-loss 可写为

$$
\mathcal{L}_z
=eta\frac{1}{T}\sum_{t=1}^T
\left[\log\sum_{e=1}^N\exp(a_{e,t})\right]^2.
$$

令

$$
z_t=\log\sum_e\exp(a_{e,t}).
$$

则

$$
\frac{\partial \mathcal{L}_z}{\partial a_{e,t}}
=rac{2\beta}{T}z_tq_{e,t}.
$$

它主要惩罚 router logit 的整体尺度过大，降低数值不稳定和过强 softmax 饱和。

z-loss 能缓解：

$$
\text{logit scale runaway, numerical instability, overly sharp routing probability.}
$$

但它不能直接保证：

$$
\text{专家 }e\text{ 的 gating vector 学到专家 }e\text{ 的真实专长。}
$$

因此，z-loss 对高增益坍塌的作用是间接的：它可能减慢 logit margin 变大，但不消除高增益方向带来的相对一阶优势。

---

## 9. loss-free balancing 能缓解什么

无辅助损失负载均衡（loss-free balancing）的思想是：不把负载均衡写成反传损失，而是在 Top-K 选择前给每个专家加一个动态偏置。

选择时使用

$$
\tilde{a}_{e,t}=a_{e,t}+b_e.
$$

若专家 $e$ 近期负载过高，则降低 $b_e$；若负载过低，则提高 $b_e$。

典型更新是

$$
b_e\leftarrow b_e+u\operatorname{sign}(\bar{c}-c_e),
$$

其中 $c_e$ 是专家 $e$ 的近期负载，$\bar{c}$ 是平均负载。

它的优点：能控制负载，同时不向主损失注入负载均衡梯度。

它的边界：它仍然只控制“谁被选中”，不直接定义“为什么该专家适合这个 token”。所以它能缓解负载坍塌，但仍需额外指标判断是否缓解区分性路由失败。

---

## 10. 机制判断

### 10.1 可以严格说的结论

在局部一阶模型中，第 $i$ 个路由模式带来的下降收益是

$$
-\eta\sigma_i^2\langle u_i,\gamma\rangle^2.
$$

因此：

$$
\boxed{
\text{高增益方向有条件地获得优化优势。}
}
$$

条件是：

$$
\langle u_i,\gamma\rangle\neq 0.
$$

### 10.2 不能严格说的结论

不能直接说：

$$
\sigma_i\text{ 大} \Rightarrow \text{一定吸引后续特征。}
$$

因为若

$$
\langle u_i,\gamma\rangle=0,
$$

则该方向对当前路由误差没有一阶作用。

### 10.3 更准确的机制表述

若某个已有高增益模式满足

$$
\sigma_i^2\langle u_i,\gamma\rangle^2
\gg
\sigma_j^2\langle u_j,\gamma\rangle^2,
$$

则梯度下降会优先沿该模式降低损失。若该模式又提高了 Top-K 选择间隔，则会造成后续 token 更频繁进入同一专家集合，从而形成路由锁定。

---

## 11. 需要验证的最小实验

### Test 1: 高增益投影是否预测路由坍塌

**Question:** 高增益梯度占比是否能预测后续专家负载集中？

定义

$$
C_r=
\frac{\sum_{i\le r}\sigma_i^2\langle u_i,\gamma\rangle^2}
{\sum_i\sigma_i^2\langle u_i,\gamma\rangle^2}.
$$

若 $C_r$ 早期升高能预测后续负载不均或 Top-K margin 增大，则支持高增益机制。

### Test 2: 负载均衡是否只修复表面负载

比较：无辅助损失、负载均衡损失、z-loss、负载均衡 + z-loss、loss-free balancing。

同时记录：

$$
\text{Load MaxVio},
\quad
\text{Top-K margin},
\quad
C_r,
\quad
\text{router-utility alignment}.
$$

若负载均衡改善 MaxVio，但 $C_r$ 和 router-utility alignment 没有改善，则说明它修复的是负载，不是区分性路由。

### Test 3: 高增益方向干预

对 router 做谱约束、行归一化、或投影去除公共高增益子空间。

若干预后 Top-K 锁定下降、未选专家获得更多任务梯度，并且主损失不明显恶化，则支持“高增益方向导致病态学习”。

---

## 12. 当前 claim boundary

**Can claim:**

- 软路由下，路由 logit 梯度为 $q_e(s_e-\bar{s})$。
- 路由高增益方向的一阶下降收益含有 $\sigma_i^2$ 放大。
- Top-K 会削弱或切断未选专家的任务梯度，从而放大早期选择偏差。
- 负载均衡和 z-loss 不能单独证明门控学到了区分性方向。

**Cannot claim yet:**

- 不能声称所有 MoE 路由坍塌都由高增益方向导致。
- 不能声称负载均衡或 z-loss 无效；它们可能有效缓解负载和稳定性问题。
- 不能声称高增益方向必然导致坍塌；必须同时观察 $\langle u_i,\gamma\rangle$ 和 Top-K 锁定。

**Next decision:**

先做诊断，不先设计新方法。最小下一步是验证：

$$
C_r\text{ 是否早期预测 Top-K margin、负载不均和 router-utility alignment 下降。}
$$

若成立，再研究直接控制高增益路由子空间的方法；若不成立，转向专家能力差异、容量限制或辅助损失干扰机制。

---

## References

1. Shazeer et al., *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*, 2017. https://arxiv.org/abs/1701.06538
2. Lepikhin et al., *GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*, 2020. https://arxiv.org/abs/2006.16668
3. Fedus, Zoph, Shazeer, *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*, 2021. https://arxiv.org/abs/2101.03961
4. Zoph et al., *ST-MoE: Designing Stable and Transferable Sparse Expert Models*, 2022. https://arxiv.org/abs/2202.08906
5. Wang et al., *Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts*, 2024. https://arxiv.org/abs/2408.15664

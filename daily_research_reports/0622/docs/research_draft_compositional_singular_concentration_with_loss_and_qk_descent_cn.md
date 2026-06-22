# 组合式语言学习会把特征集中到高增益奇异子空间中

## 摘要

语言具有嵌套和组合结构。一个短语可以表达一个简单特征，更长的短语可以保留这个特征，同时加入新的约束。例如，"city" 可以变成 "beautiful city"，再变成 "NYC is a beautiful city"，再变成 "NYC is a beautiful city in winter"。每个更长的表达都不是与短表达独立的；它复用了之前的意义，并加入一个新的组成部分。

这篇草稿研究这种结构的一个机制性后果。如果许多简单特征和中间特征先被学到，那么模型参数可能会发展出少数高增益奇异方向。这里的“奇异方向”指矩阵分解后输入侧或输出侧最容易被放大的方向；“高增益”指这些方向对应的奇异值较大。一旦这些方向的奇异值变大，后来的特征就会在优化上偏向复用它们，因为沿着大奇异值方向加入一个很小的分量，就能对 logits 或注意力分数产生很大的改变。这能让学习更高效，但也会把许多不同特征混入同一个低维子空间，从而在常见特征和长尾特征之间制造干扰。

本文给出这个偏置的形式化梯度论证，并用嵌套前缀数据上的受控 transformer 实验作为支持。实验中，一个单层因果 transformer 学习 $A$、$AB$、$ABC$、$ABCD$，直到 $ABCDEFG.$ 这样的序列。模型能以 $100\%$ 准确率预测所有结构化续写；同时，每一步组合中新加入的“额外”特征主要集中在 $W_{\mathrm{out}}$、$W_Q$ 和 $W_K$ 的顶部奇异方向中，但没有集中在 $W_V$ 中。这说明组合性可能使用一个紧凑的高增益子空间来做路由和预测，而 value 向量更分散地保留 token 特定内容。

当前工作结论是：

$$
\boxed{
\text{组合式学习会产生可复用的高增益子空间，而这些子空间会吸引后来的特征。}
}
$$

这对学习有用，但对长尾特征危险，因为特征共享可能变成特征干扰。

## 1. 研究问题

自回归语言模型通过下一词预测训练：

$$
p_\theta(x_{t+1}\mid x_{\leq t}),
$$

并使用交叉熵损失：

$$
L_t=-\log p_\theta(x_{t+1}\mid x_{\leq t}).
$$

模型并没有被直接训练成构建一个干净的语义层级。它被训练来降低预测损失。因此，如果语义特征出现了，它们应当能通过“它们如何帮助降低损失”来解释。

这篇草稿的问题是：

**为什么组合特征倾向于集中在少数高增益奇异向量方向中？**

第二个问题是：

**为什么这种集中会导致常见特征和长尾特征之间的干扰？**

核心直觉是：语言学习是渐进的：

$$
\text{简单特征}
\rightarrow
\text{组合特征}
\rightarrow
\text{更复杂的组合特征}.
$$

简单且高频的特征会被多次遇到。它们更早被学到，也被反复更新。它们的梯度会在模型参数矩阵中形成主导奇异方向。之后的特征倾向于复用这些方向，因为这些方向已经是高增益的。

这产生一个权衡：

$$
\text{共享的低维子空间}
\quad
\Longrightarrow
\quad
\text{高效复用}
\quad
\text{以及}
\quad
\text{特征干扰}.
$$

## 2. 语言类比

合成实验使用嵌套符号前缀：

$$
A,\quad AB,\quad ABC,\quad ABCD,\quad ABCDE,\quad ABCDEF,\quad ABCDEFG,\quad ABCDEFG.
$$

这不是自然语言。它是对语言中一个性质的受控类比：

$$
\text{更长的意义}
=
\text{更短的意义}
+
\text{新约束}.
$$

在自然语言里，可以有：

$$
\text{city}
$$

然后是：

$$
\text{beautiful city}
$$

再然后是：

$$
\text{NYC is a beautiful city}
$$

再然后是：

$$
\text{NYC is a beautiful city in winter}.
$$

每个短语都保留了早先意义的一部分，同时加入新内容。这推动如下分解：

$$
u_{AB}
=
u_A
+
\Delta_{A\to AB},
$$

$$
u_{ABC}
=
u_{AB}
+
\Delta_{AB\to ABC},
$$

$$
u_{ABCD}
=
u_{ABC}
+
\Delta_{ABC\to ABCD}.
$$

这里 $u_X$ 是前缀 $X$ 的隐藏方向，$\Delta_{X\to Y}$ 是从 $X$ 走向 $Y$ 时新增的额外特征。

目标是理解这些额外特征的几何形态：

1. 它们是不是同一个方向？
2. 它们是不是彼此独立的方向？
3. 它们是否处在一个共享的低维高增益子空间里？
4. 它们是否因为这种共享而互相干扰？

## 3. 核心猜想

中心猜想是：

$$
\boxed{
\text{嵌套组合式学习会产生高增益奇异子空间，后来的特征会复用这些子空间。}
}
$$

更具体地说：

1. 简单且高频的特征先被学到。
2. 它们的梯度反复更新相似的模型方向。
3. 这些方向变成大奇异值方向。
4. 之后，更复杂或更长尾的特征会沿这些高增益方向获得更强梯度。
5. 因此，后来的特征倾向于复用这些方向，而不是均匀分布到所有可用维度中。
6. 这种复用让学习更高效，但也把不同特征耦合在一起。

这种耦合就是特征干扰的来源。

## 4. 形式模型

考虑一个隐藏表示：

$$
h\in\mathbb{R}^d.
$$

令一个模型矩阵把隐藏状态映射到 logits：

$$
z = Wh.
$$

令 $W$ 的奇异值分解为：

$$
W = U\Sigma V^\top
=
\sum_i \sigma_i u_i v_i^\top.
$$

这里：

- $v_i$ 是隐藏侧奇异向量；
- $u_i$ 是输出侧奇异向量；
- $\sigma_i$ 是方向 $i$ 的奇异值，也就是增益。

把隐藏特征展开到右奇异向量基中：

$$
h=\sum_i c_i v_i.
$$

则：

$$
Wh
=
\sum_i \sigma_i c_i u_i.
$$

这已经说明了前向传播中的增益：

$$
\boxed{
\text{同样的隐藏系数 } c_i \text{，它的输出影响正比于 } \sigma_i.
}
$$

如果 $\sigma_1\gg\sigma_{20}$，那么沿 $v_1$ 的分量会比同等大小的 $v_{20}$ 分量更大地改变输出。

## 5. 梯度证明：新特征偏向高增益方向

对交叉熵损失：

$$
L(z,y)=-\log p_y,
\qquad
p=\operatorname{softmax}(z).
$$

对 logits 的梯度是：

$$
\nabla_z L = p-e_y.
$$

对隐藏表示的梯度是：

$$
\nabla_h L
=
W^\top \nabla_z L.
$$

代入奇异值分解：

$$
\nabla_h L
=
V\Sigma U^\top (p-e_y).
$$

定义：

$$
\beta_i = u_i^\top(p-e_y).
$$

于是：

$$
\nabla_h L
=
\sum_i \sigma_i\beta_i v_i.
$$

一次梯度下降对隐藏特征的更新是：

$$
\Delta h
=
-\eta\nabla_h L
=
-\eta\sum_i\sigma_i\beta_i v_i.
$$

所以沿奇异方向 $v_i$ 的更新系数是：

$$
\Delta c_i
=
-\eta\sigma_i\beta_i.
$$

取绝对值：

$$
|\Delta c_i|
=
\eta\sigma_i|\beta_i|.
$$

这证明了关键的局部陈述：

$$
\boxed{
\text{在同样的误差投影 }|\beta_i|\text{ 下，更大的 }\sigma_i\text{ 会给出更大的特征更新。}
}
$$

如果误差向量没有特意与顶部输出奇异方向正交，则：

$$
\mathbb{E}\left[(\Delta c_i)^2\right]
=
\eta^2\sigma_i^2\mathbb{E}\left[\beta_i^2\right].
$$

如果：

$$
\mathbb{E}\left[\beta_i^2\right]\approx \text{constant},
$$

那么：

$$
\mathbb{E}\left[(\Delta c_i)^2\right]
\propto
\sigma_i^2.
$$

所以一个新特征的学习能量会偏向大奇异值方向。

精确条件是：

$$
\boxed{
\Delta c_i \propto \sigma_i\langle u_i,p-e_y\rangle.
}
$$

单独的大奇异值并不充分。输出误差还必须在对应的输出奇异向量上有非零投影。但如果某个大奇异值方向确实能帮助降低当前损失，梯度下降自然会偏向它。

### 5.1 沿单个奇异方向的端到端损失下降

上面的论证说明，隐藏更新沿高奇异值方向更大。但这还不是优化为什么应当偏好这些方向的完整端到端原因。缺失的一步是：增加这些方向上的有用分量，确实会降低交叉熵损失。

考虑隐藏状态沿某个右奇异向量的小扰动：

$$
\delta h = \epsilon v_i.
$$

这里 $\delta h$ 是隐藏表示变化，$\epsilon$ 是扰动大小，$v_i$ 是 $W$ 的隐藏侧奇异向量。由于 logits 为 $z=Wh$，诱导出的 logit 改变是：

$$
\delta z
=
W\delta h
=
\epsilon Wv_i
=
\epsilon \sigma_i u_i.
$$

因此，同样大小的隐藏扰动 $\epsilon$ 会产生幅度正比于 $\sigma_i$ 的 logit 改变。

对当前 logits 附近的损失做一阶泰勒展开：

$$
\delta L
\approx
\left\langle \nabla_z L,\delta z\right\rangle.
$$

对 softmax 交叉熵，$\nabla_z L=p-e_y$。代入 logit 扰动：

$$
\delta L
\approx
\epsilon \sigma_i\left\langle p-e_y,u_i\right\rangle.
$$

这个方程就是端到端下降准则。如果 $\left\langle p-e_y,u_i\right\rangle>0$，那么沿 $-v_i$ 移动会降低损失。如果 $\left\langle p-e_y,u_i\right\rangle<0$，那么沿 $+v_i$ 移动会降低损失。因此，在只沿奇异方向 $v_i$、扰动范数为 $\epsilon$ 时，可以得到的最佳一阶损失下降是：

$$
\max_{\delta h\in\operatorname{span}(v_i),\ \|\delta h\|=\epsilon}
(-\delta L)
\approx
\epsilon\sigma_i\left|\left\langle p-e_y,u_i\right\rangle\right|.
$$

这证明了更强的陈述：

$$
\boxed{
\text{在同样扰动大小和同样误差对齐下，更大的 }\sigma_i\text{ 给出更大的一阶损失下降。}
}
$$

因此，高增益方向不只是“表示更新更大”的方向。只要输出误差和对应输出侧奇异向量有非零对齐，它就是下降效率更高的方向。

这可以直接连接到上面的梯度更新。沿 $v_i$ 的梯度步系数是：

$$
\Delta c_i
=
-\eta\sigma_i\beta_i,
\qquad
\beta_i=\left\langle u_i,p-e_y\right\rangle.
$$

该方向诱导的隐藏扰动是：

$$
\delta h_i
=
\Delta c_i v_i.
$$

对应的 logit 扰动是：

$$
\delta z_i
=
W\delta h_i
=
-\eta\sigma_i^2\beta_i u_i.
$$

这个奇异方向分量造成的一阶损失变化是：

$$
\Delta L_i
\approx
\left\langle p-e_y,\delta z_i\right\rangle
=
-\eta\sigma_i^2\beta_i^2.
$$

等价地：

$$
\boxed{
\Delta L_i
\approx
-\eta\sigma_i^2\left\langle u_i,p-e_y\right\rangle^2.
}
$$

这里 $\Delta L_i$ 是梯度步沿 $v_i$ 的分量贡献的一阶损失变化。这个公式闭合了逻辑环：高奇异值方向受到偏好，是因为当它们和当前预测误差对齐时，每一步梯度更新能产生更大的交叉熵下降。

因此，精确表述应当是：

$$
\boxed{
\text{未来特征会被同时具备高奇异值和当前预测误差对齐的方向吸引。}
}
$$

这个条件很重要。大奇异值本身不保证损失下降。如果 $\left\langle p-e_y,u_i\right\rangle=0$，那么沿 $v_i$ 改变隐藏状态不会产生一阶损失下降。这个机制需要增益和有用性同时存在：$\sigma_i$ 提供增益，$\left\langle p-e_y,u_i\right\rangle$ 提供任务对齐。

这给出了端到端优化故事。早期高频特征通过某些输出方向反复降低损失。反复更新增大对应奇异值。之后相关特征产生的预测误差，往往在同一输出侧方向上有非零投影。由于这些方向现在有大的 $\sigma_i$，沿对应 $v_i$ 的一个小隐藏移动就能产生大的 logit 修正和大的一阶损失下降。因此，基于梯度的学习倾向于复用它们。

## 6. Softmax 会加强 Q/K 偏置

对注意力机制：

$$
q_t=W_Qh_t,
\qquad
k_i=W_Kh_i.
$$

注意力分数是：

$$
s_{ti}
=
\frac{q_t^\top k_i}{\sqrt d}.
$$

注意力权重是：

$$
\alpha_{ti}
=
\frac{\exp(s_{ti})}{\sum_{j\leq t}\exp(s_{tj})}.
$$

对两个位置 $i$ 和 $j$：

$$
\frac{\alpha_{ti}}{\alpha_{tj}}
=
\exp(s_{ti}-s_{tj}).
$$

所以 softmax 会放大分数差异。分数差为 $2$ 时：

$$
\exp(2)\approx 7.39.
$$

分数差为 $5$ 时：

$$
\exp(5)\approx 148.4.
$$

这解释了为什么一个有用的注意力分数差一旦出现，就能主导路由。但它本身还没有证明为什么基于梯度的学习会选择 $W_Q$ 或 $W_K$ 中的大奇异值方向来制造这个差距。我们还需要和输出 logit 情形一样的端到端损失下降论证。

### 6.1 通过 Query 奇异方向的损失下降

令位置 $t$ 的注意力输出为：

$$
o_t
=
\sum_{i\leq t}\alpha_{ti}r_i,
\qquad
r_i=W_Vh_i.
$$

这里 $o_t$ 是注意力输出，$\alpha_{ti}$ 是 query 位置 $t$ 到 key 位置 $i$ 的注意力权重，$r_i$ 是从位置 $i$ 携带来的 value 向量。

令下游损失为 $L$。定义分数梯度：

$$
g_{ti}
=
\frac{\partial L}{\partial s_{ti}}.
$$

对 softmax 注意力，这个梯度是：

$$
g_{ti}
=
\alpha_{ti}\left\langle \frac{\partial L}{\partial o_t}, r_i-o_t\right\rangle.
$$

这里 $\partial L/\partial o_t$ 是到达注意力输出的下游梯度。项 $r_i-o_t$ 衡量 value $r_i$ 和当前注意力平均值有多不同。这个公式给出了一个分数是否有用的精确条件。如果增大 $s_{ti}$ 会让输出更对齐下游梯度方向，那么 $g_{ti}$ 非零，梯度下降就会改变这个分数。

现在分解 query 矩阵：

$$
W_Q
=
U_Q\Sigma_QV_Q^\top
=
\sum_a \sigma_a^{Q}u_a^{Q}(v_a^{Q})^\top.
$$

这里 $v_a^{Q}$ 是 $W_Q$ 的隐藏侧奇异向量，$u_a^{Q}$ 是 query 侧奇异向量，$\sigma_a^{Q}$ 是方向 $a$ 的 query 增益。

考虑 query 侧隐藏状态沿 $v_a^{Q}$ 的小扰动：

$$
\delta h_t
=
\epsilon v_a^{Q}.
$$

query 改变量是：

$$
\delta q_t
=
W_Q\delta h_t
=
\epsilon\sigma_a^{Q}u_a^{Q}.
$$

对 key 位置 $i$ 诱导出的分数变化是：

$$
\delta s_{ti}
=
\frac{(\delta q_t)^\top k_i}{\sqrt d}
=
\frac{\epsilon\sigma_a^{Q}}{\sqrt d}\left\langle u_a^{Q},k_i\right\rangle.
$$

因此一阶损失变化是：

$$
\delta L
\approx
\sum_{i\leq t}g_{ti}\delta s_{ti}
=
\epsilon\sigma_a^{Q}\left\langle u_a^{Q},
\frac{1}{\sqrt d}\sum_{i\leq t}g_{ti}k_i
\right\rangle.
$$

定义 query 侧分数梯度向量：

$$
\gamma_t^{Q}
=
\frac{1}{\sqrt d}\sum_{i\leq t}g_{ti}k_i.
$$

这正是损失对 query 向量的梯度：

$$
\gamma_t^{Q}
=
\frac{\partial L}{\partial q_t}.
$$

于是：

$$
\delta L
\approx
\epsilon\sigma_a^{Q}\left\langle u_a^{Q},\gamma_t^{Q}\right\rangle.
$$

在只沿 query 隐藏侧奇异方向 $v_a^{Q}$、扰动范数为 $\epsilon$ 时，可以获得的最佳一阶损失下降是：

$$
\max_{\delta h_t\in\operatorname{span}(v_a^{Q}),\ \|\delta h_t\|=\epsilon}
(-\delta L)
\approx
\epsilon\sigma_a^{Q}\left|\left\langle u_a^{Q},\gamma_t^{Q}\right\rangle\right|.
$$

这证明了 query 侧选择规则：

$$
\boxed{
\text{大的 query 奇异值只有在其 query 侧奇异向量与分数梯度方向对齐时才会被偏好。}
}
$$

对应的梯度步给出更清楚的下降效率公式。通过 $W_Q$ 对 $h_t$ 的梯度是：

$$
\nabla_{h_t}^{Q}L
=
W_Q^\top\gamma_t^{Q}
=
\sum_a \sigma_a^{Q}\left\langle u_a^{Q},\gamma_t^{Q}\right\rangle v_a^{Q}.
$$

沿 $v_a^{Q}$ 的梯度步分量是：

$$
\Delta h_{t,a}^{Q}
=
-\eta\sigma_a^{Q}\left\langle u_a^{Q},\gamma_t^{Q}\right\rangle v_a^{Q}.
$$

把这个分量代回一阶损失变化：

$$
\Delta L_a^{Q}
\approx
-\eta (\sigma_a^{Q})^2
\left\langle u_a^{Q},\gamma_t^{Q}\right\rangle^2.
$$

这就是高增益 query 方向被选择的端到端原因。当两个 query 奇异方向和当前分数梯度向量有相近对齐时，$\sigma_a^{Q}$ 更大的方向会产生更大的一阶损失下降。

### 6.2 通过 Key 奇异方向的损失下降

同样的论证适用于 key 矩阵。分解：

$$
W_K
=
U_K\Sigma_KV_K^\top
=
\sum_b \sigma_b^{K}u_b^{K}(v_b^{K})^\top.
$$

扰动 key 位置 $i$ 的隐藏状态，方向为 $v_b^{K}$：

$$
\delta h_i
=
\epsilon v_b^{K}.
$$

则：

$$
\delta k_i
=
W_K\delta h_i
=
\epsilon\sigma_b^{K}u_b^{K}.
$$

对固定 query 位置 $t$，分数变化是：

$$
\delta s_{ti}
=
\frac{q_t^\top\delta k_i}{\sqrt d}
=
\frac{\epsilon\sigma_b^{K}}{\sqrt d}\left\langle q_t,u_b^{K}\right\rangle.
$$

如果同一个 key 向量影响多个 query 位置，一阶损失变化会对所有这些 query 求和：

$$
\delta L
\approx
\epsilon\sigma_b^{K}
\left\langle u_b^{K},
\frac{1}{\sqrt d}\sum_t g_{ti}q_t
\right\rangle.
$$

定义 key 侧分数梯度向量：

$$
\gamma_i^{K}
=
\frac{1}{\sqrt d}\sum_t g_{ti}q_t.
$$

这就是损失对 key 向量的梯度：

$$
\gamma_i^{K}
=
\frac{\partial L}{\partial k_i}.
$$

因此：

$$
\delta L
\approx
\epsilon\sigma_b^{K}\left\langle u_b^{K},\gamma_i^{K}\right\rangle.
$$

在只沿 key 隐藏侧奇异方向 $v_b^{K}$、扰动范数为 $\epsilon$ 时，可以获得的最佳一阶损失下降是：

$$
\max_{\delta h_i\in\operatorname{span}(v_b^{K}),\ \|\delta h_i\|=\epsilon}
(-\delta L)
\approx
\epsilon\sigma_b^{K}\left|\left\langle u_b^{K},\gamma_i^{K}\right\rangle\right|.
$$

梯度步贡献满足：

$$
\Delta L_b^{K}
\approx
-\eta (\sigma_b^{K})^2
\left\langle u_b^{K},\gamma_i^{K}\right\rangle^2.
$$

所以 key 侧选择规则是：

$$
\boxed{
\text{大的 key 奇异值只有在其 key 侧奇异向量与分数梯度方向对齐时才会被偏好。}
}
$$

再次强调，奇异值本身不充分。大的 $\sigma_b^{K}$ 只有在 $\langle u_b^{K},\gamma_i^{K}\rangle\neq 0$ 时才有用。优化偏好由增益和任务对齐共同决定。

### 6.3 为什么 Softmax 会加强这种选择

前两节说明了高奇异值 Q/K 方向为什么会被损失下降选择。softmax 会进一步加强这个效果，因为有用的分数改变会被转化成乘法式路由改变。

对两个位置 $i$ 和 $j$，定义分数间隔：

$$
m_{tij}
=
s_{ti}-s_{tj}.
$$

注意力 odds ratio 为：

$$
\frac{\alpha_{ti}}{\alpha_{tj}}
=
\exp(m_{tij}).
$$

假设沿 $v_a^{Q}$ 的 query 隐藏扰动改变这个间隔。由于：

$$
\delta s_{ti}
=
\frac{\epsilon\sigma_a^{Q}}{\sqrt d}\left\langle u_a^{Q},k_i\right\rangle,
$$

且：

$$
\delta s_{tj}
=
\frac{\epsilon\sigma_a^{Q}}{\sqrt d}\left\langle u_a^{Q},k_j\right\rangle,
$$

所以间隔变化是：

$$
\delta m_{tij}
=
\frac{\epsilon\sigma_a^{Q}}{\sqrt d}
\left\langle u_a^{Q},k_i-k_j\right\rangle.
$$

因此，为了得到目标间隔变化 $\Delta m$，所需隐藏扰动大小是：

$$
\epsilon
=
\frac{\sqrt d\,\Delta m}
{\sigma_a^{Q}\left\langle u_a^{Q},k_i-k_j\right\rangle},
$$

假设分母非零且符号符合目标方向。这让效率主张变得明确：在同样有用的间隔方向上，更大的 query 奇异值 $\sigma_a^{Q}$ 需要更小的隐藏移动，就能产生同样的乘法式注意力 odds 改变。

对应的 key 侧表达式是：

$$
\delta m_{tij}
=
\frac{\epsilon\sigma_b^{K}}{\sqrt d}
\left\langle u_b^{K},q_t\right\rangle
$$

当只相对 key $j$ 扰动 key $i$ 时成立。同样，在奇异向量与有用 query 方向对齐的前提下，更大的 $\sigma_b^{K}$ 可以用更小的隐藏移动创造同样的分数间隔变化。

因此，修正后的 Q/K 主张是：

$$
\boxed{
\text{Q/K 高增益方向被选择，是因为它们通过有用分数梯度给出更大的损失下降，并且每单位隐藏移动能产生更大的注意力间隔改变。}
}
$$

这比“softmax 只是放大分数差”更强。完整机制是：

$$
\text{损失梯度识别有用的分数改变}
\quad\rightarrow\quad
\text{大的 Q/K 奇异值高效实现这些改变}
\quad\rightarrow\quad
\text{softmax 把分数差转化成尖锐路由。}
$$

有用的分数矩阵是：

$$
S=QK^\top.
$$

如果有用注意力结构是低秩的：

$$
\operatorname{rank}(S_{\mathrm{useful}})=r,
$$

那么存在：

$$
\tilde Q,\tilde K\in\mathbb{R}^{n\times r}
$$

使得：

$$
S_{\mathrm{useful}}=\tilde Q\tilde K^\top.
$$

因此，如果任务只需要少数关系因子，Q/K 自然只需要少数有用方向。在嵌套前缀任务中，这些因子类似：

$$
\text{处在结构化前缀内部},
\qquad
\text{当前前缀阶段},
\qquad
\text{继续这条链},
\qquad
\text{边界或终止标记}.
$$

这给出 Q/K 低秩主张：

$$
\boxed{
W_Q \text{ 和 } W_K \text{ 在有用注意力分数结构低秩时会变得低维。}
}
$$

softmax 随后会加强这个效果，因为它把注意力集中到主导分数差上。但大奇异值方向被选择的原因，是上面的下降效率公式，而不只是 softmax 放大。

## 7. 为什么 $W_V$ 不同

value 投影是：

$$
v_i=W_Vh_i.
$$

与 $W_Q$ 和 $W_K$ 不同，$W_V$ 不用于计算成对相似性。它用于在注意力已经选中某个 token 或状态之后携带内容。

所以 $W_Q$ 和 $W_K$ 回答：

$$
\text{哪些 token 或状态应该交互？}
$$

而 $W_V$ 回答：

$$
\text{一旦交互被选中，应该携带什么内容？}
$$

如果 values 过强地塌缩进同一个高增益子空间，token 特定内容可能会丢失。因此我们预期：

$$
W_Q,\ W_K,\ W_{\mathrm{out}}
\quad
\text{比}
\quad
W_V
\quad
\text{对额外特征表现出更强集中。}
$$

这正是当前实验显示的现象。

## 8. 受控实验

### 8.1 数据集

主数据集包含嵌套前缀片段：

$$
A,\ AB,\ ABC,\ ABCD,\ ABCDE,\ ABCDEF,\ ABCDEFG,\ ABCDEFG.
$$

每个结构化前缀出现概率约为 $5\%$。来自 $J,\ldots,Z$ 的随机 filler token 填充其余部分：

$$
\Pr(\text{random filler})\approx 60\%.
$$

这个设置刻意简单。它让我们清楚知道哪个特征被继承，哪个特征是新加入的。

### 8.2 模型

模型是单层、单头因果 transformer：

$$
h_t
=
\operatorname{LN}
\left(
e(x_t)
+
W_O\sum_{i\leq t}\alpha_{ti}W_Ve(x_i)
\right).
$$

输出 logits 是：

$$
z_t=W_{\mathrm{out}}h_t.
$$

训练使用下一词交叉熵。主要设置为：

| setting | value |
|---|---:|
| layers | 1 |
| heads | 1 |
| context length | 8 |
| position embedding | none |
| batch size | 256 |
| training steps | 3000 |
| optimizer | AdamW |
| learning rate | $2\times 10^{-3}$ |
| dimensions tested | $d=32$, $d=64$ |

### 8.3 特征方向

对每个前缀 $F$，定义：

$$
u_F
=
\operatorname{normalize}
\left(
\mathbb{E}[h_t\mid F]
-
\mathbb{E}[h_t\mid \text{random filler}]
\right).
$$

对一个转移 $X\to Y$，定义继承成分：

$$
u_{\mathrm{common}}(X\to Y)
=
(u_Y^\top u_X)u_X.
$$

定义额外成分：

$$
u_{\mathrm{extra}}(X\to Y)
=
\operatorname{normalize}
\left(
u_Y-(u_Y^\top u_X)u_X
\right).
$$

额外成分是这篇草稿的主要对象。它衡量当更长前缀加入一个 token 时新产生的表示方向。

### 8.4 奇异向量对齐

对每个矩阵：

$$
W=U\Sigma V^\top,
$$

以及每个特征方向 $u$，定义它在奇异向量 $v_i$ 上的质量：

$$
m_i(u)=\langle u,v_i\rangle^2.
$$

top-$k$ 质量是：

$$
M_k(u)=\sum_{i=1}^k m_i(u).
$$

高 top-$k$ 质量表示该特征主要位于最高奇异值子空间中。

## 9. 结果

### 9.1 模型学会了结构化续写

对 $d=64$，所有结构化续写都以 $100\%$ 准确率被预测：

| continuation | accuracy | mean target probability | cross entropy |
|---|---:|---:|---:|
| $A\to AB$ | $100\%$ | $0.884$ | $0.124$ |
| $AB\to ABC$ | $100\%$ | $0.879$ | $0.129$ |
| $ABC\to ABCD$ | $100\%$ | $0.831$ | $0.185$ |
| $ABCD\to ABCDE$ | $100\%$ | $0.810$ | $0.211$ |
| $ABCDE\to ABCDEF$ | $100\%$ | $0.780$ | $0.249$ |
| $ABCDEF\to ABCDEFG$ | $100\%$ | $0.655$ | $0.423$ |
| $ABCDEFG\to ABCDEFG.$ | $100\%$ | $0.556$ | $0.587$ |

所以模型确实学会了嵌套链条。我们检查的几何结构不是训练失败的伪影。

### 9.2 额外特征是不同方向，但共享高增益子空间

归一化额外方向之间的成对距离是：

$$
d(u_i,u_j)=\sqrt{2-2u_i^\top u_j}.
$$

对 $d=64$，额外特征距离为：

| statistic | value |
|---|---:|
| minimum distance | $1.242$ |
| mean distance | $1.372$ |
| maximum distance | $1.477$ |

距离约 $1.41$ 表示接近正交。因此，额外特征并不全是同一个方向。

但它们仍共享高增益 $W_{\mathrm{out}}$ 子空间。对 $d=64$，$W_{\mathrm{out}}$ 隐藏侧 top-10 质量为：

| extra feature | top-10 mass |
|---|---:|
| $A\to AB$ | $93.7\%$ |
| $AB\to ABC$ | $92.1\%$ |
| $ABC\to ABCD$ | $91.4\%$ |
| $ABCD\to ABCDE$ | $89.9\%$ |
| $ABCDE\to ABCDEF$ | $90.6\%$ |
| $ABCDEF\to ABCDEFG$ | $86.0\%$ |
| $ABCDEFG\to ABCDEFG.$ | $16.9\%$ |

关键教训是：

$$
\boxed{
\text{不同特征方向} \neq \text{不同奇异子空间}.
}
$$

许多不同的额外特征可以存在于同一个顶部奇异向量子空间内。

### 9.3 更高维度会稍微分散特征，但不会消除集中

比较 $d=32$ 和 $d=64$：

| metric | $d=32$ | $d=64$ |
|---|---:|---:|
| final validation CE | $1.338$ | $1.338$ |
| $W_{\mathrm{out}}$ largest singular value | $2.379$ | $2.069$ |
| $W_{\mathrm{out}}$ effective rank | $15.57$ | $15.93$ |
| mean extra-feature distance | $1.370$ | $1.372$ |

$d=64$ 模型给表示更多空间，内部 top-10 质量比 $d=32$ 略低。但定性模式保留：内部额外特征仍集中在 $W_{\mathrm{out}}$ 顶部方向中。

这说明，单纯增加维度不会自动阻止共享子空间复用。

### 9.4 相邻额外特征比远距离额外特征更分离

对 $d=64$：

| pair type | mean distance | mean cosine |
|---|---:|---:|
| adjacent extra features | $1.437$ | $-0.033$ |
| remote extra features | $1.355$ | $0.080$ |

相邻转移包括：

$$
A\to AB
\quad \text{vs.} \quad
AB\to ABC.
$$

远距离转移包括：

$$
A\to AB
\quad \text{vs.} \quad
ABCD\to ABCDE.
$$

这支持一个想法：相邻前缀状态必须保持可区分。模型必须知道它处在 $AB$、$ABC$ 还是 $ABCD$，因为这些状态预测不同的下一个 token。远距离状态则可以更多复用同一个一般性的“继续链条”结构。

### 9.5 $W_Q$、$W_K$、$W_V$ 和 $W_O$ 扮演不同角色

对 $d=64$，额外特征在不同矩阵侧的平均 top-10 奇异向量质量为：

| matrix side | average top-10 mass |
|---|---:|
| $W_Q$ input side | $52.4\%$ |
| $W_K$ input side | $49.8\%$ |
| $W_V$ input side | $6.2\%$ |
| $W_{\mathrm{out}}$ hidden input side | internal transitions 通常为 $86\%-94\%$ |

这是一个重要的机制分裂。

query 和 key 矩阵用于计算注意力相似度：

$$
s_{ti}=q_t^\top k_i.
$$

因此，它们自然会集中关系结构。它们问的是：

$$
\text{哪个前缀状态应该和哪个上下文状态交互？}
$$

value 矩阵携带内容：

$$
v_i=W_Vh_i.
$$

因此，它没有那么强的理由把 token 特定信息塌缩到同一个高增益关系子空间中。

这给出解释：

$$
\boxed{
\text{Q/K 集中组合式路由，而 V 保留 token 特定内容。}
}
$$

## 10. 特征干扰

这种集中的有用部分是效率。许多相关特征可以共享同一个高增益子空间。

危险部分是干扰。

假设两个特征 $f$ 和 $g$ 为：

$$
h_f=\sum_i c_{f,i}v_i,
\qquad
h_g=\sum_i c_{g,i}v_i.
$$

它们的重叠是：

$$
\langle h_f,h_g\rangle
=
\sum_i c_{f,i}c_{g,i}.
$$

如果两个特征都集中在同一个 top-$k$ 方向中，则：

$$
\langle h_f,h_g\rangle
\approx
\sum_{i=1}^k c_{f,i}c_{g,i}.
$$

现在考虑输出影响：

$$
Wh_f
=
\sum_i \sigma_i c_{f,i}u_i.
$$

如果共享方向上的 $\sigma_i$ 很大，那么特征空间中很小的重叠也可能制造很大的输出影响重叠。

梯度也是如此：

$$
\nabla_h L
=
W^\top\nabla_z L
=
\sum_i \sigma_i
\langle u_i,\nabla_z L\rangle
v_i.
$$

所以如果两个特征共享高 $\sigma_i$ 方向，训练一个特征会更新也影响另一个特征的方向。

这就是特征干扰机制：

$$
\boxed{
\text{共享高增益子空间会耦合特征学习。}
}
$$

对常见特征来说，这可能有益，因为许多样本强化同一个计算。对稀有特征来说，这可能有害，因为它们较弱的梯度必须修改一个已经被常见特征梯度主导的子空间。

## 11. 主张边界

当前证据支持这个主张：

$$
\boxed{
\text{在受控嵌套前缀学习中，新的组合特征会变成共享高增益奇异子空间内的不同方向。}
}
$$

证据也支持：

$$
\boxed{
\text{Q/K 集中关系性路由，而 V 对这些额外特征保持较低集中。}
}
$$

当前证据还没有证明完整的自然语言主张。自然语言包含许多种组合性、歧义、层级和世界知识。受控数据集只隔离了一个成分：嵌套组合式续写。

因此，正确的主张边界是：

**这个实验展示了一种可能机制：组合式学习可以创造共享高增益子空间并引发特征干扰。它还没有证明所有语言语义都使用这个机制。**

## 12. 建议的后续实验

### 12.1 受控语义短语

把符号前缀替换成半自然短语：

```text
city
beautiful city
NYC is a beautiful city
NYC is a beautiful city in winter
```

然后定义同样的对象：

$$
u_{\mathrm{extra}}(\text{short phrase}\to\text{long phrase}).
$$

测试额外特征是否再次集中在 $W_Q$、$W_K$ 和 $W_{\mathrm{out}}$ 中，而较少集中在 $W_V$ 中。

### 12.2 常见组合与稀有组合

构造共享高层组合结构、但频率不同的特征对：

```text
common: the capital of France is Paris
rare: the capital of Tuvalu is Funafuti
```

测量稀有特征是否复用同一个高增益子空间，以及它们的学习是否被常见特征方向延迟或扭曲。

### 12.3 因果方向干预

对一个学到的稀有特征，把它的隐藏方向分解为：

$$
h_{\mathrm{rare}}
=
h_{\mathrm{top}}
+
h_{\mathrm{tail}},
$$

其中 $h_{\mathrm{top}}$ 是投影到顶部奇异向量上的部分，$h_{\mathrm{tail}}$ 是剩余部分。

然后干预：

$$
h' = h-\lambda h_{\mathrm{top}},
$$

或：

$$
h' = h-\lambda h_{\mathrm{tail}}.
$$

如果移除 $h_{\mathrm{top}}$ 同时损害常见和稀有特征，那么这些特征共享同一个高增益子空间。如果移除 $h_{\mathrm{tail}}$ 选择性损害稀有特征，那么稀有特征还需要较低增益方向来提供特异性。

### 12.4 训练目标比较

比较标准交叉熵与标签平滑或自适应平滑。预测是：

$$
\text{standard CE}
\quad
\text{会更强地推动常见高增益方向}.
$$

标签平滑应当降低继续增大已高置信常见特征 margin 的动机：

$$
\text{label smoothing}
\quad
\Rightarrow
\quad
\text{less extreme singular concentration}.
$$

这把当前组合性故事连接到更早的结果：smoothing 在保持预测准确率的同时，降低了矩阵范数和极端参数值。

## 13. 最终工作理论

当前工作理论是：

1. 语言学习是组合式的。
2. 许多复杂特征复用更简单的特征。
3. 高频简单特征更早被学到，并被反复更新。
4. 反复梯度创造高增益奇异方向。
5. 后来的特征偏向这些方向，因为这些方向能高效降低损失。
6. 这创造了一个紧凑的组合子空间。
7. 这个紧凑子空间改进复用和泛化。
8. 但它也把特征混在一起。
9. 这种混合导致干扰，尤其影响长尾特征。

一句话总结：

$$
\boxed{
\text{语言组合性鼓励低维复用，而低维复用同时创造高效学习和特征干扰。}
}
$$

这是当前研究中浮现出的主要研究提案。

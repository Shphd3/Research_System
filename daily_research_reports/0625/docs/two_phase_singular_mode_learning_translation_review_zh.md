# 《奇异模式学习的两阶段理论》完整中文翻译与理论审查

源文件：`two_phase_singular_mode_learning_proof_and_test.md`

---

# 第一部分：完整中文翻译

# 奇异模式学习的两阶段理论

## 一个自包含的形式化证明与最小测试

### 摘要

本文给出一个最小形式化解释，用来解释训练中观察到的一种两阶段现象：一个有用的奇异方向会先旋转到某个特征方向；当这个方向对齐之后，训练主要继续增大对应的奇异值。目标是区分讨论中常被混在一起的两个对象。奇异向量说明的是：**矩阵读取或写入哪个特征方向**。奇异值说明的是：**这个方向被放大得有多强**。

证明使用最简单的模型：一个用 margin-based loss（基于间隔的损失）训练的 rank-one linear map（秩一线性映射）。即使在这个玩具设定中，动力学也会自然分离。奇异向量的对齐误差带有一个饱和因子而下降；只要损失仍然奖励更大的 margin，奇异值就可以继续增长。这给出了一个清晰的数学解释：为什么 cross-entropy 训练倾向于产生稳定方向，但增益会持续增大。

中心结论是：

**$1-c(t)^2 = (1-c(0)^2)\exp\left(-\left(\sigma(t)^2-\sigma(0)^2\right)\right)$.**

这里，$c(t)$ 是已学习奇异向量和真实特征方向之间的对齐程度，$\sigma(t)$ 是奇异值。这个方程说明，对齐误差会随着奇异增益的增长而指数衰减。因此，方向学习会较早饱和，而增益放大可以在后期继续。

---

## 1. 动机

在训练好的神经网络矩阵中，一个大的奇异值通常表示模型创建了一个高增益通道。如果某个特征与相应的奇异向量对齐，那么该特征就能强烈影响 logits、attention scores 或下游 hidden states。

但是，这里有两个不同的学习过程。

第一个过程是 **direction discovery（方向发现）**。模型必须把某个奇异向量旋转到一个有用的特征方向。

第二个过程是 **gain amplification（增益放大）**。一旦有用方向被找到，模型就可以继续增大奇异值，以提高 margin 或 confidence。

问题是：这个两阶段图景能否被推导出来，而不只是被描述出来。

本文证明：在一个最小线性模型中，这个图景可以被推导出来。

---

## 2. 模型设定

考虑一个 rank-one linear model（秩一线性模型）：

**$W(t)=\sigma(t)u(t)v(t)^\top$.**

这里，$W(t)$ 是时刻 $t$ 的可训练矩阵，$\sigma(t)\geq 0$ 是它的奇异值，$u(t)$ 是输出侧奇异向量，$v(t)$ 是输入侧奇异向量。$u(t)$ 和 $v(t)$ 都具有单位范数。

为了隔离输入侧效应，假设输出方向已经固定为正确输出方向：

**$u(t)=u_\star$.**

这里，$u_\star$ 是目标输出方向。这个假设去掉了一个自由度，使我们可以专注于模型如何学习输入侧奇异向量和奇异值。

令输入特征是一个单位向量：

**$\|x\|=1$.**

模型输出为：

**$Wx=\sigma u_\star(v^\top x)$.**

定义已学习奇异向量和输入特征之间的对齐程度：

**$c=v^\top x$.**

这里，$c=\cos\theta$，$\theta$ 是 $v$ 和 $x$ 之间的夹角。如果 $c=1$，奇异向量就与特征方向完全一致。如果 $c=0$，奇异向量就与特征正交。

沿正确输出方向的标量 margin 为：

**$m=\sigma c$.**

这里，$m$ 是有用的输出强度。它是增益项 $\sigma$ 和对齐项 $c$ 的乘积。

这个方程是核心分解：

**$m=\sigma c$.**

它表示模型可以通过两种方式提高 margin：旋转 $v$ 使其靠近 $x$，从而增大 $c$；或者增大奇异值 $\sigma$。

---

## 3. 损失假设

假设损失是 margin 的递减函数：

**$\ell=\phi(m)$, with $\phi'(m)<0$.**

这里，$\phi(m)$ 是任意平滑损失，只要它奖励更大的 margin。

定义 residual learning pressure（剩余学习压力）：

**$r(m)=-\phi'(m)>0$.**

这里，$r(m)$ 衡量损失仍然有多强地想增大 margin。

对于 binary logistic loss，也就是最简单的 cross-entropy-like loss：

**$\phi(m)=\log(1+\exp(-m))$.**

于是：

**$r(m)=\frac{1}{1+\exp(m)}$.**

这个压力会随着 margin 增长而降低，但对任意有限的 $m$ 它始终为正。因此，cross-entropy 类型的损失即使在分类方向已经正确之后，也会继续奖励更大的 margin。

---

## 4. 奇异值的梯度流

因为 $m=\sigma c$，margin 对奇异值的导数为：

**$\frac{\partial m}{\partial \sigma}=c$.**

根据 gradient flow，奇异值演化为：

**$\frac{d\sigma}{dt}=-\frac{\partial \ell}{\partial \sigma}$.**

使用链式法则：

**$\frac{\partial \ell}{\partial \sigma}=\phi'(m)\frac{\partial m}{\partial \sigma}=\phi'(m)c$.**

由于 $r(m)=-\phi'(m)$，得到：

**$\frac{d\sigma}{dt}=r(m)c$.**

这个方程说明，只要当前奇异向量与特征方向有正对齐，奇异值就会增大。如果 $c>0$，则 $d\sigma/dt>0$。

---

## 5. 奇异向量的梯度流

奇异向量 $v$ 必须保持在单位球面上：

**$\|v\|=1$.**

因此，它的更新不能沿任意欧氏方向移动。它必须位于单位球面在 $v$ 处的切空间中。

对齐量为：

**$c=v^\top x$.**

$c$ 关于 $v$ 的欧氏梯度是 $x$。但是只有 $x$ 中与 $v$ 正交的分量，才能在保持 $\|v\|=1$ 的同时旋转 $v$。

切空间投影为：

**$(I-vv^\top)x$.**

这里，$I$ 是单位矩阵，$vv^\top x$ 是 $x$ 平行于 $v$ 的分量。因此，$(I-vv^\top)x$ 是 $x$ 中可以把 $v$ 旋转向特征方向的部分。

由于 $m=\sigma v^\top x$，单位球面上 $v$ 的梯度流为：

**$\frac{dv}{dt}=r(m)\sigma(I-vv^\top)x$.**

这个方程说明，$v$ 会朝 $x$ 旋转。旋转速度正比于剩余压力 $r(m)$、奇异值 $\sigma$，以及剩余切向错位 $(I-vv^\top)x$。

现在计算对齐动力学：

**$\frac{dc}{dt}=\frac{d}{dt}(v^\top x)=x^\top\frac{dv}{dt}$.**

代入 $dv/dt$：

**$\frac{dc}{dt}=r(m)\sigma x^\top(I-vv^\top)x$.**

因为 $\|x\|=1$ 且 $v^\top x=c$，所以：

**$x^\top(I-vv^\top)x=1-c^2$.**

因此：

**$\frac{dc}{dt}=r(m)\sigma(1-c^2)$.**

这是关键的方向学习方程。它包含饱和因子 $1-c^2$。当 $c$ 接近 $1$ 时，这个因子接近 $0$，因此 $v$ 的旋转必然变慢。

---

## 6. 耦合动力学与两阶段机制

我们已经推导出两个耦合微分方程：

**$\frac{d\sigma}{dt}=r(m)c$.**

**$\frac{dc}{dt}=r(m)\sigma(1-c^2)$.**

奇异值方程不包含饱和因子 $1-c^2$。对齐方程包含这个因子。

这个差异就是两阶段行为的数学来源。

为了更精确地看这一点，将对齐方程除以奇异值方程：

**$\frac{dc}{d\sigma}=\frac{\sigma(1-c^2)}{c}$.**

剩余压力 $r(m)$ 被抵消。这意味着，只要损失依赖于 $m=\sigma c$，对齐与奇异值增长之间的几何关系就与具体的递减 margin loss 无关。

重排：

**$\frac{c}{1-c^2}dc=\sigma d\sigma$.**

两边积分：

**$-\frac{1}{2}\log(1-c^2)=\frac{1}{2}\sigma^2+\mathrm{constant}$.**

使用初值 $c(0)=c_0$ 和 $\sigma(0)=\sigma_0$，得到：

**$1-c(t)^2=(1-c_0^2)\exp\left(-\left(\sigma(t)^2-\sigma_0^2\right)\right)$.**

这证明了中心结论。

对齐误差 $1-c(t)^2$ 随 $\sigma(t)^2$ 的增加而指数衰减。因此，中等程度的奇异值增长就可以快速让奇异向量几乎对齐特征方向。

一旦 $c(t)\approx 1$，对齐动力学变为：

**$\frac{dc}{dt}=r(m)\sigma(1-c^2)\approx 0$.**

方向几乎不再变化。

但奇异值动力学变为：

**$\frac{d\sigma}{dt}=r(m)c\approx r(m)$.**

所以，只要损失仍然存在正的剩余压力，奇异值就可以继续增长。

这证明了最小模型中的两阶段机制。

---

## 7. 定理陈述

**定理：rank-one linear model 中的两阶段奇异模式学习。**

考虑 rank-one model $W=\sigma u_\star v^\top$，其中 $\sigma\geq 0$，$\|v\|=1$，$\|x\|=1$，且 $u_\star$ 固定。令 margin 为 $m=\sigma v^\top x$，损失为 $\ell=\phi(m)$ 且 $\phi'(m)<0$。在 $v$ 约束在单位球面上的 gradient flow 下，定义 $c=v^\top x$ 和 $r(m)=-\phi'(m)>0$。则：

**$\frac{d\sigma}{dt}=r(m)c$.**

**$\frac{dc}{dt}=r(m)\sigma(1-c^2)$.**

因此：

**$1-c(t)^2=(1-c_0^2)\exp\left(-\left(\sigma(t)^2-\sigma_0^2\right)\right)$.**

所以，奇异向量的对齐误差会随着奇异增益增长而指数衰减。在对齐饱和之后，奇异向量变化很小；只要损失仍然奖励更大的 margin，奇异值就可以继续增加。

---

## 8. 对奇异向量和奇异值的解释

奇异向量 $v$ 回答的问题是：

**这个矩阵读取哪个输入特征方向？**

如果 $v$ 与 $x$ 对齐，那么矩阵就强烈读取特征 $x$。

奇异值 $\sigma$ 回答的问题是：

**这个矩阵把该特征方向放大得多强？**

如果 $v=x$，则：

**$Wx=\sigma u_\star$.**

这里，增大 $\sigma$ 会直接增大正确输出方向上的输出幅度。

因此，两阶段图景具有精确含义。

在第一阶段，训练通过把 $v$ 旋转到 $x$ 来发现特征方向。

在第二阶段，方向已经被发现后，训练继续增大增益 $\sigma$。

---

## 9. 为什么 cross-entropy 会产生后期奇异值增长

对于 logistic loss：

**$\phi(m)=\log(1+\exp(-m))$.**

剩余压力为：

**$r(m)=\frac{1}{1+\exp(m)}$.**

它对任意有限 $m$ 都为正。因此，即使 $c\approx 1$，奇异值动力学也满足：

**$\frac{d\sigma}{dt}\approx \frac{1}{1+\exp(\sigma)} > 0$.**

增长会变慢，但仍会继续。

这解释了为什么 cross-entropy 可以在奇异方向已经对齐之后继续增大奇异值。模型后期主要不是在学习方向，而是在增大 margin。

这也解释了为什么 confidence-capped loss 可以减少后期奇异值放大。如果当 $p_y\geq q$ 时损失被 capped，那么达到足够置信度后，剩余压力会变为零或变得很小。在这个模型中，这意味着 $r(m)$ 变为零或很小，所以 $d\sigma/dt$ 和 $dc/dt$ 都消失。由于对齐之后 $dc/dt$ 本来已经很小，主要实际效果是停止进一步的奇异值增长。

---

## 10. 与 C3S-AdamW 的关系

这个证明改变了我们对 C3S-AdamW 的理解。

C3S-AdamW 不应被理解为一种必然阻止特征与 top singular vectors 对齐的方法。有用的特征对齐属于第一阶段，应该被允许。

相反，该方法应被理解为控制第二阶段：

**C3S-AdamW 保留有用的方向发现，同时减少不必要的奇异值放大。**

这与观察到的模式一致：最终特征与 top singular vectors 的对齐可以保持较高，而对应奇异值显著下降。

正确的功能量不只是未加权对齐：

**$\langle f,v_i\rangle^2$.**

更重要的是 gain-weighted contribution（增益加权贡献）：

**$\sigma_i^2\langle f,v_i\rangle^2$.**

这里，$f$ 是已学习特征方向，$v_i$ 是一个奇异向量，$\sigma_i$ 是对应奇异值。只要奇异值降低，即使对齐项仍然很大，C3S 也可以减少高增益干扰。

---

## 11. 建议的最小测试

最简单的测试应直接测量两个预测阶段。

训练一个小线性模型或 transformer，并按固定步数保存 checkpoint。对于选定矩阵 $W(t)$，计算 top-$k$ 右奇异子空间：

**$P_k(t)=V_k(t)V_k(t)^\top$.**

这里，$V_k(t)$ 包含 $W(t)$ 的 top $k$ 个右奇异向量。

测量 subspace drift（子空间漂移）：

**$\delta_k(t)=\|P_k(t)-P_k(t-\Delta)\|_2$.**

这里，$\delta_k(t)$ 衡量 top-$k$ 奇异子空间在时间窗口 $\Delta$ 内变化多少。

测量 singular-gain growth（奇异增益增长）：

**$g_k(t)=\sum_{i=1}^k\sigma_i(t)^2-\sum_{i=1}^k\sigma_i(t-\Delta)^2$.**

这里，$g_k(t)$ 衡量同一窗口内 top singular values 增长了多少。

如果已知特征方向 $f(t)$，测量 feature alignment（特征对齐）：

**$a_k(t)=\|P_k(t)f(t)\|^2$.**

这里，$a_k(t)$ 衡量该特征有多少落入 top singular subspace。

测量 gain-weighted feature effect（增益加权特征效应）：

**$e_k(t)=\sum_{i=1}^k\sigma_i(t)^2\langle f(t),v_i(t)\rangle^2$.**

两阶段假说预测如下模式。

训练早期应有较高的子空间漂移和快速增长的特征对齐：

**$\delta_k(t)$ large, and $a_k(t)$ increasing.**

训练后期，在 cross-entropy 下应有较低的子空间漂移，但仍有持续奇异增益增长：

**$\delta_k(t)\approx 0$, while $g_k(t)>0$.**

在 confidence-capped loss 或 C3S-AdamW 下，后期奇异增益增长应更小：

**$g_k^{\mathrm{C3S}}(t)<g_k^{\mathrm{CE}}(t)$ during the late phase.**

但是，特征对齐可能保持相似：

**$a_k^{\mathrm{C3S}}(t)\approx a_k^{\mathrm{CE}}(t)$.**

因此，决定性信号是：

**C3S 下对齐相似，但奇异增益更低，增益加权效应更低。**

---

## 12. 最小实验协议

一个最小实验可以这样运行。

从相同初始化训练两个模型。

第一个模型使用标准 cross-entropy 和 AdamW。

第二个模型在 warmup 后使用 confidence-capped C3S-AdamW。

在 checkpoints $t=0,\Delta,2\Delta,\ldots,T$，记录选定矩阵 $W(t)$。

对每个 checkpoint，计算：

**$V_k(t)$, $\sigma_1(t),\ldots,\sigma_k(t)$, and $P_k(t)=V_k(t)V_k(t)^\top$.**

然后画四条曲线。

第一，画 subspace drift：

**$\delta_k(t)=\|P_k(t)-P_k(t-\Delta)\|_2$.**

第二，画 top-$k$ singular energy：

**$S_k(t)=\sum_{i=1}^k\sigma_i(t)^2$.**

第三，画 feature alignment：

**$a_k(t)=\|P_k(t)f(t)\|^2$.**

第四，画 gain-weighted feature effect：

**$e_k(t)=\sum_{i=1}^k\sigma_i(t)^2\langle f(t),v_i(t)\rangle^2$.**

预期结果是：标准 CE 和 C3S 可能都发现类似的 top singular directions，因此 $a_k(t)$ 可能相当。但 C3S 应在后期降低 $S_k(t)$ 和 $e_k(t)$。

这会支持更精确的 claim：

**所提出的方法不一定阻止 feature-subspace sharing；它减少 shared singular directions 上的过度增益放大。**

---

## 13. 结论边界

这个证明只对 rank-one linear model、固定输出方向、margin-based loss 精确成立。它并不证明每个神经网络矩阵都必须完全这样行为。

但是，这个证明识别出一个在更大模型中仍然相关的局部机制。对于任意矩阵块，奇异向量指定了一个特征读取或写入方向，奇异值指定了增益。一旦有用方向被找到，cross-entropy 类型的损失可以继续增大增益，因为它们继续奖励更大的 margin。

因此，这个证明为实验观察到的模式给出原则性解释：

**特征对齐可以保持较高，同时 proposed method 下奇异值下降。**

正确结论不是 top singular vectors 总是坏的。正确结论是，过度奇异增益可能产生干扰，而控制后期增益增长是一个有效的 optimizer objective。

---

## 14. 总结

rank-one proof 为两阶段假说提供了精确数学基础。

模型 margin 为：

**$m=\sigma c$.**

这里，$\sigma$ 是奇异增益，$c$ 是特征方向对齐。

gradient flow 给出：

**$\frac{d\sigma}{dt}=r(m)c$.**

**$\frac{dc}{dt}=r(m)\sigma(1-c^2)$.**

对齐方程包含饱和因子 $1-c^2$，而奇异值方程不包含。因此，方向学习自然饱和，而奇异值增长可以继续。

精确关系为：

**$1-c(t)^2=(1-c_0^2)\exp\left(-\left(\sigma(t)^2-\sigma_0^2\right)\right)$.**

这证明了奇异向量可以较早对齐，而奇异值后续仍继续增长。

建议测试是在训练中追踪 top singular subspace drift、top singular energy、feature alignment 和 gain-weighted feature effect。C3S-AdamW 的预期信号不一定是与 top singular vectors 的对齐更低，而是在对齐已经稳定之后，奇异值更低、增益加权特征效应更低。

---

# 第二部分：细致理论检查

## 总体裁定

**不能确认“理论检查无误”。**

该文档在“把 $\sigma$ 和 $v$ 当作直接可训练坐标，并对 $v$ 使用标准单位球面 gradient flow”的 toy model 内部，代数推导基本一致。但如果它声称解释“一个真实可训练矩阵 $W$ 在普通参数空间里的梯度流 / AdamW / SGD 下的奇异向量与奇异值动力学”，则存在一个 blocking issue：文档把奇异分解坐标当成了欧氏训练参数，忽略了从矩阵参数 $W$ 到 $(\sigma,v)$ 的诱导度量。

## Blocking issue：参数化度量不匹配

文档使用：

$$
\frac{dv}{dt}=r(m)\sigma(I-vv^\top)x
$$

这对应的是把 $\sigma$ 和 $v$ 作为独立参数，用标准度量直接训练：

$$
L(\sigma,v)=\phi(\sigma v^\top x), \quad \|v\|=1.
$$

但如果真实模型参数是矩阵本身，令

$$
W = u_\star a^\top, \quad a=\sigma v,
$$

则 margin 为

$$
m=a^\top x.
$$

普通欧氏 gradient flow 是：

$$
\frac{da}{dt}=r(m)x.
$$

分解 $a=\sigma v$ 后得到：

$$
\frac{d\sigma}{dt}=r(m)c,
$$

但

$$
\frac{dv}{dt}=\frac{r(m)}{\sigma}(I-vv^\top)x,
$$

因此：

$$
\frac{dc}{dt}=\frac{r(m)}{\sigma}(1-c^2).
$$

这时不变量变成：

$$
\sigma^2(1-c^2)=\sigma_0^2(1-c_0^2),
$$

也就是：

$$
1-c(t)^2=(1-c_0^2)\frac{\sigma_0^2}{\sigma(t)^2}.
$$

这不是文档中的

$$
1-c(t)^2=(1-c_0^2)\exp[-(\sigma(t)^2-\sigma_0^2)].
$$

所以：

- 若文档只作为“singular-coordinate toy model”，公式可成立；
- 若文档作为“真实矩阵训练的奇异动力学证明”，当前证明不成立；
- 要连接 AdamW/C3S-AdamW，必须先说明优化器实际作用在哪个参数空间，以及对应 metric 是什么。

## 其他理论边界

### 1. 需要 $c>0$ 或 signed alignment 假设

文档使用 $1-c^2$ 作为 alignment error。这个量把 $c=1$ 和 $c=-1$ 都视为“完美对齐”。但在固定输出方向 $u(t)=u_\star$ 的设定下，$v=-x$ 会给出负 margin：

$$
m=\sigma v^\top x=-\sigma.
$$

这不是正确分类方向。除非允许同时翻转 $u$ 和 $v$ 的符号，否则应限制在 $c\ge 0$ 的 basin，或把结论改成“unsigned subspace alignment”，而不是“正确 feature direction alignment”。

### 2. $\sigma=0$ 与 $c=0$ 是退化点

当 $\sigma=0$ 时，奇异向量不唯一；当 $c=0$ 时，文档中通过除以 $d\sigma/dt$ 得到 $dc/d\sigma$ 的推导需要小心。可以用守恒量微分来绕开 $c=0$，但文档目前没有说明这些退化点。

### 3. Cross-entropy 后期增长结论需要加入 weight decay 边界

文档对 logistic loss 的 $r(m)>0$ 判断正确。但 AdamW 含 decoupled weight decay 时，$\sigma$ 的动力学会多出类似 $-\lambda\sigma$ 的项。因此“奇异值持续增长”只在无 weight decay、或 loss pressure 大于衰减压力时成立。若连接 AdamW/C3S-AdamW，必须报告 weight decay 条件。

### 4. C3S-AdamW 部分是解释性 claim，不是由证明推出

文档证明最多支持：如果某方法降低 $\sigma_i$ 而保留 $\langle f,v_i\rangle^2$，则 gain-weighted effect 会下降。它没有从 C3S-AdamW 的更新式推导出这一点。因此 C3S 部分应写成“interpretation / predicted signature”，不能写成 theorem consequence。

### 5. Minimal test 需要避免 feature direction confound

如果 $f(t)$ 是训练中学习出的方向，那么 $a_k(t)=\|P_k(t)f(t)\|^2$ 同时受 $P_k(t)$ 和 $f(t)$ 漂移影响。最小测试最好使用 synthetic known feature $f_\star$，或至少同时报告 feature-probe stability。

### 6. Top-$k$ 指标受 singular value crossing 影响

$P_k(t)$ 和 $g_k(t)$ 在奇异值交叉时可能发生 jump 或模式替换。最小测试可以保留这些指标，但应加一个 matched-mode 或 subspace-restricted energy 检查，避免把 mode swapping 误解释为 direction discovery。

---

# 第三部分：文档主旨总结

本文档主要想说明：

1. 一个矩阵的奇异向量和奇异值代表不同对象：
   - 奇异向量：读/写哪个特征方向；
   - 奇异值：该方向的增益有多强。

2. 训练可被分解成两个阶段：
   - Phase 1：方向发现，奇异向量旋转到有用特征；
   - Phase 2：增益放大，方向稳定后，奇异值继续增大 margin。

3. 在文档的直接奇异坐标 toy model 中，方向对齐方程带有饱和因子 $1-c^2$，而奇异值方程没有这个饱和因子。因此方向学习会早停/饱和，增益可以继续增长。

4. 对 C3S-AdamW 的正确解释不应是“阻止特征对齐 top singular vectors”，而应是“允许有用方向对齐，但抑制后期过大的奇异值增益”。因此关键指标不是单纯 alignment，而是：

$$
\sigma_i^2\langle f,v_i\rangle^2.
$$

5. 最小测试应同时追踪：
   - top singular subspace drift；
   - top singular energy；
   - feature alignment；
   - gain-weighted feature effect。

---

# 第四部分：连接到 gating 研究与研究流程

## 1. 这个文档对 gating 主线的价值

它对当前 gating 研究不是直接证明 specialization，而是提供一个有用区分：

- **direction / identity**：router 或矩阵到底读到了哪个 feature direction；
- **gain / dominance**：某个方向在打分或输出中被放大到多强。

这与当前 gating collapse 主线对应：

- slot feature 可能已经在 routed hidden state 中存在；
- 但 router score 可能被 common component 的高增益方向主导；
- 所以 routing collapse 不一定是“没有 feature 信息”，而可能是“common direction 的 gain/bias 太强”。

在 dot-product router 中：

$$
z_{f,e}=w_e^\top h_f.
$$

若

$$
h_f=c+r_f,
$$

则

$$
z_{f,e}=w_e^\top c+w_e^\top r_f.
$$

其中 $w_e^\top c$ 是对所有 feature 共享的 expert-specific effective bias。它是 gating 版本的“高增益 common direction”。如果它早期大于 slot-specific term，top-1 router 会进入 common-collapse basin。

## 2. 导师真正要解决的问题

**导师要解决的问题不是：SVD 能不能解释一切。**

更准确地说，导师要你回答：

> 在最小可控 setting 中，普通 dot-product sparse top-1 MoE router 为什么不会稳定形成 feature-level specialization？它学到的是 feature identity，还是被 common/shared utility/gain 主导的 route-utility binding？

当前最小问题可以写成：

> 在 feature 均匀、position 控制、random-init、bias-free linear gate 下，为什么仍然出现 collapse？是 slot feature 不在 hidden state 中，还是 common component 通过 $w_e^\top c$ 形成 effective expert bias，并被 top-1 training 放大？

## 3. 物理先验

最小物理先验应写成可反驳形式：

> Transformer hidden state 不是纯 feature-specific representation。即使数据 feature frequency 均匀，routed hidden state 仍可能分解为 common component + feature residual：
>
> $$h_f=c+r_f.$$
>
> Dot-product router 对 common component 的投影 $w_e^\top c$ 会变成 expert-specific effective bias。若该 common bias 的差异大于 slot residual score 差异，则 early top-1 routing 会被 common direction 主导，而不是被 slot identity 主导。

这个 physical prior 的好处：

- 可反驳：如果 common term 不预测 step-0 dominant expert，或 common cancellation 不改善 slot_NMI，就被削弱；
- 有数学对象：$h_f,c,r_f,w_e,z_{f,e}$；
- 有 observable metric：common margin、slot margin、slot_NMI、max_load、route lock step；
- 能指导 implementation：router-side common-control / residual-control。

## 4. 假说

建议把假说分成主假说和边界假说。

### 主假说 H_gate

> 在 minimal dot-product sparse top-1 MoE 中，collapse 的主要早期机制不是 slot feature 缺失，而是 routed hidden state 的 common component 通过 $w_e^\top c$ 产生 expert-specific effective bias；这个 early common-logit dominance 被 top-1 training lock-in 放大，导致 final many-to-one routing collapse。

### 连接本文档的 gain 版本

> Gating collapse 可以被看成 direction 与 gain 的错位：slot direction 可能存在，但 common direction 的 router-score gain 更强，所以 top-1 decision 使用 common dominance，而不是 slot identity。

### 不能 claim 的版本

不能说：

- 已经证明 expert 功能是 causally specialized；
- load balance 就等于 feature specialization；
- top singular vectors 都是坏的；
- common component 是唯一原因；
- 这个机制已经能推广到真实 LM。

## 5. Minimal test

当前最小测试应优先服务 gating 主线，而不是照搬文档里的 C3S singular-value test。

### 固定设定

```text
dataset = D_min_block_shift
sequence = prefix + SLOT_s B_CONST Y_s + suffix
position embeddings disabled / zeroed / frozen
routing metric only at B_CONST position
router = dot-product sparse top-1
score_e(h)=w_e^T h
experts receive full h unless testing router-input-only intervention
```

### 干预组

只保留一个主干预：

```text
router score computed from common-controlled / residual-controlled representation
expert still receives full hidden state
no slot labels
no slot centroid initialization
sparse top-1 preserved
```

可实现为：

$$
z'_{f,e}=w_e^\top h_f - w_e^\top \hat c
$$

或

$$
z'_{f,e}=w_e^\top(h_f-\hat c).
$$

但最干净的版本是 logit-level cancellation，因为它直接控制 $w_e^\top c$。

### Primary metrics

```text
slot_NMI
per-slot route purity
accuracy
```

### Secondary diagnostics

```text
max_load
active experts
common margin
slot margin
route lock step
many-to-one merging count
```

### 成功标准

支持 H_gate，如果看到：

```text
common-controlled router:
  slot_NMI 大幅上升，接近 slot-init / common-cancel upper bound；
  accuracy 保持 1.0 或接近 baseline；
  common margin 下降；
  slot margin / common margin 比值上升；
  max_load 下降；
  many-to-one merging 减少；
  不使用 slot label 或 oracle centroid。
```

### 证伪 / 削弱标准

削弱或证伪 H_gate，如果看到：

```text
common term w_e^T c 不能预测 step-0 dominant expert；
common cancellation 不降低 early load concentration；
common-controlled router 只改善 max_load，但 slot_NMI 仍低；
accuracy 明显下降，说明方法破坏任务信息；
slot_NMI 改善完全依赖 slot labels / slot-centroid initialization；
final collapse 仍发生，且 common margin 已被控制，说明主因转向 expert utility co-adaptation 或 top-1 basin geometry。
```

## 6. 与文档 minimal test 的关系

文档的 singular-mode test 可以作为 secondary audit，而不是主线第一成功标准。

可加到 gating 实验中的附加测量：

```text
对 router weight matrix W_g 或 selected projection matrix：
  top-k singular subspace drift δ_k(t)
  top-k singular energy S_k(t)
  common direction alignment a_common(t)
  slot direction alignment a_slot(t)
  gain-weighted common effect e_common(t)
  gain-weighted slot effect e_slot(t)
```

关键不是证明“奇异值两阶段理论”本身，而是判断：

```text
collapse seeds from high-gain common direction?
common-control reduces gain-weighted common effect while preserving slot information?
```

## 7. 研究流程上的明确裁定

Verdict:
当前文档可作为“direction vs gain”的解释工具，但不能作为真实矩阵训练的完整理论证明。gating 主线应保留它的概念区分，修改其数学边界。

Blocking issue:
文档的 $dv/dt=r\sigma(I-vv^T)x$ 是直接训练奇异坐标的动力学，不是普通矩阵 $W$ 的欧氏梯度流。若不修正，不能把指数公式当作 neural matrix / AdamW 的严格证明。

Preserve:
保留两个核心概念：奇异向量表示读/写方向，奇异值表示 gain；以及指标 $\sigma_i^2\langle f,v_i\rangle^2$ 比单独 alignment 更接近功能效应。

Unclear:
C3S-AdamW 是否真的通过降低后期 singular gain 起作用，还需要 optimizer-level evidence；gating collapse 是否主要由 gain-weighted common direction 主导，需要 common-control 的 label-free minimal test。

Minimal next action:
写一个新的 active anchor：`label-free common-control / residual-control dot-product sparse top-1 router`，以 `slot_NMI + accuracy + common/slot margin` 为主指标，SVD 只作为 secondary diagnostic。

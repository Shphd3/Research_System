# C3S-AdamW 文档中文译文与理论审查

原文：`c3s_adamw_merged_rigorous_proof_with_negative_results.md`

说明：本文是逐节中文译文与理论审查版。公式保持原文形式；个别术语先给中文含义，再保留英文缩写。

---

# 第一部分：完整逐节中文译文

## 标题

# 从组合奇异集中到 C3S-AdamW

## 严格的问题陈述、逐步证明与优化器设计

---

## 摘要

语言学习具有嵌套结构。一个简单特征可以被更具体的特征复用，更具体的特征又可以被进一步具体的特征复用。在一个受控符号设定中，这种结构可以写成：

$$
A \rightarrow AB \rightarrow ABC \rightarrow ABCD.
$$

在自然语言中，类似结构是：`city` 可以扩展为 `beautiful city`，再扩展为 `NYC is a beautiful city`，最后扩展为 `NYC is a beautiful city in winter`。每个更长表达都保留前面的一部分含义，并加入新的约束。

本文提出一个统一的理论和方法。核心问题是：高频公共特征会较早且反复地被学习。它们的重复梯度会在 $W_{\mathrm{out}}$、$W_Q$、$W_K$ 等矩阵中形成高增益奇异子空间。之后出现的长尾特征会被吸引到这个子空间中，因为当该方向与当前预测误差对齐时，沿大奇异值方向移动可以带来更大的一级损失下降。这种复用有时有效，但也会造成干扰：许多不同特征通过同一组高增益方向耦合在一起。

本文还证明两个看似自然的替代方案无法解决该机制：球面隐藏状态加 AdamW、Poincaré 有界隐藏状态加 AdamW。它们约束的是表示几何，但不能保证实际 AdamW 更新方向中的公共子空间分量被抑制。

本文提出的解决方案是 **C3S-AdamW**，全称是 **置信度截断、冻结公共子空间抑制 AdamW**（Confidence-Capped Frozen Common-Subspace Suppressed AdamW）。方法先正常训练，使公共前置特征形成稳定骨架；然后估计并冻结公共特征子空间；之后使用置信度截断损失，阻止已经学会的公共样本继续产生不必要梯度，并抑制活跃更新方向在冻结公共子空间中的分量，迫使尚未学好的长尾特征使用互补维度。

中心陈述是：

$$
\boxed{
\text{公共特征学习会形成高增益骨架，而 C3S-AdamW 防止该骨架垄断后续长尾学习。}
}
$$

本文区分三类内容：已证明内容、所需假设、必须实验检验的经验命题。证明都在局部线性化设定中完成；这正是理解梯度训练机制的合适层级。推广到 Transformer 时，对每个选定参数块及其局部雅可比矩阵应用相同论证。

---

## 1. 哪些是已证明的，哪些是假设，哪些是经验命题

本文使用三类陈述。

**已证明陈述**：来自代数、一级泰勒展开或所提优化器定义。例如，如果更新向量 $u$ 被替换为 $(I-\rho P_C)u$，那么它在 $C$ 内部的分量会乘以 $1-\rho$，而 $C$ 外部的分量被精确保留。

**假设**：定理所需的条件。例如，冻结投影器定理假设公共子空间在 warmup 后稳定：

$$
\|P_C(t)-P_C(T_0)\|_2 \leq \epsilon_C.
$$

其中，$P_C(t)$ 是第 $t$ 步的公共特征投影器，$P_C(T_0)$ 是 warmup 后冻结的投影器，$\epsilon_C$ 是允许漂移量。

**经验命题**：必须测量。例如，$W_Q$、$W_K$、$W_{\mathrm{out}}$ 比 $W_V$ 表现出更强奇异集中，这可以由 nested-prefix 实验支持，但不是关于所有 Transformer 或所有自然语言的定理。

这个区分很重要，因为优化器的保证是几何保证：它保证活跃更新被重定向离开冻结公共子空间；但它本身不保证所有稀有特征都能被学会。后者还需要足够数据、模型容量和可识别性。

---

## 2. 嵌套特征产生时间学习顺序

合成结构是：

$$
A \rightarrow AB \rightarrow ABC \rightarrow ABCD.
$$

这里，$A$ 是公共前置特征，$AB$ 是复用 $A$ 的组合特征，$ABC$ 或 $ABCD$ 是更具体的嵌套特征。箭头表示后续特征依赖前面特征。

核心建模假设是学习时间尺度分离：

$$
T_C \ll T_T.
$$

其中，$T_C$ 是公共前置特征稳定所需时间尺度，$T_T$ 是长尾嵌套特征被学习的时间尺度。该假设由频率和前置结构支撑：公共特征出现更频繁，并且在后续组合特征能被表达前必须先被学到。

这个假设不是说公共特征之后不再出现。它们之后仍然出现。它说的是：公共特征的主导子空间会较早稳定。因此，可以在 warmup 后一次性估计公共特征子空间。

该假设的诊断量是：

$$
\delta(t)=\|P_C(t)-P_C(T_0)\|_2.
$$

$\delta(t)$ 衡量 warmup 后公共特征投影器的漂移。如果 $\delta(t)$ 小，冻结投影器方法合理；如果 $\delta(t)$ 大，说明 $T_0$ 太早，或者公共特征骨架仍在变化。

---

## 3. 奇异值产生更高效的下降方向

考虑一个从隐藏表示到 logits 的局部线性映射：

$$
z = Wh.
$$

其中 $h\in\mathbb{R}^d$ 是隐藏表示，$W$ 是可训练矩阵，$z$ 是 logit 向量。

对 $W$ 做奇异值分解：

$$
W=U\Sigma V^\top=\sum_i \sigma_i u_i v_i^\top.
$$

其中 $u_i$ 是输出侧奇异向量，$v_i$ 是隐藏侧奇异向量，$\sigma_i$ 是奇异值。奇异值表示方向 $v_i$ 的增益：沿单位方向 $v_i$ 移动，会在输出侧沿 $u_i$ 产生大小为 $\sigma_i$ 的变化。

把隐藏表示展开为：

$$
h=\sum_i c_i v_i.
$$

则

$$
Wh=\sum_i \sigma_i c_i u_i.
$$

这证明了前向增益事实：在相同隐藏系数 $c_i$ 下，输出效果正比于 $\sigma_i$。

使用 softmax 交叉熵：

$$
L(z,y)=-\log p_y,
\qquad
p=\operatorname{softmax}(z).
$$

其中 $p_y$ 是模型给正确标签 $y$ 的概率。

logit 梯度为：

$$
\nabla_z L=p-e_y.
$$

由链式法则：

$$
\nabla_h L=W^\top\nabla_z L.
$$

代入 SVD 得：

$$
\nabla_h L=V\Sigma U^\top(p-e_y).
$$

定义：

$$
\beta_i=u_i^\top(p-e_y).
$$

$\beta_i$ 是输出误差与输出侧奇异向量 $u_i$ 的对齐程度。因此：

$$
\nabla_h L=\sum_i \sigma_i\beta_i v_i.
$$

梯度下降对隐藏表示的更新为：

$$
\Delta h=-\eta\nabla_h L=-\eta\sum_i\sigma_i\beta_i v_i.
$$

因此沿 $v_i$ 的更新系数为：

$$
\Delta c_i=-\eta\sigma_i\beta_i.
$$

取绝对值得：

$$
|\Delta c_i|=\eta\sigma_i|\beta_i|.
$$

这证明局部更新结论：在相同误差对齐 $|\beta_i|$ 下，更大的奇异值 $\sigma_i$ 会沿 $v_i$ 产生更大的特征更新。

更强的陈述关于损失下降。考虑沿一个奇异方向的扰动：

$$
\delta h=\epsilon v_i.
$$

则 logit 变化为：

$$
\delta z=W\delta h=\epsilon\sigma_i u_i.
$$

一级泰勒展开给出：

$$
\delta L \approx \langle \nabla_z L,\delta z\rangle.
$$

代入后：

$$
\delta L\approx \epsilon\sigma_i\langle p-e_y,u_i\rangle.
$$

在固定扰动范数 $\epsilon$ 下，$\operatorname{span}(v_i)$ 中最优方向会选择降低损失的符号，因此：

$$
\max_{\delta h\in\operatorname{span}(v_i),\ \|\delta h\|=\epsilon}(-\delta L)
\approx
\epsilon\sigma_i|\langle p-e_y,u_i\rangle|.
$$

这证明下降效率陈述：

$$
\boxed{
\text{大奇异值只有在其输出侧奇异向量与预测误差对齐时才有用。}
}
$$

单独大的 $\sigma_i$ 不够。如果 $\langle p-e_y,u_i\rangle=0$，沿 $v_i$ 移动不会带来一级损失下降。

把真实梯度步在 $v_i$ 上的分量代入：

$$
\delta h_i=-\eta\sigma_i\beta_i v_i.
$$

诱导的 logit 变化是：

$$
\delta z_i=W\delta h_i=-\eta\sigma_i^2\beta_i u_i.
$$

来自该分量的一级损失变化：

$$
\Delta L_i\approx \langle p-e_y,\delta z_i\rangle
=-\eta\sigma_i^2\beta_i^2.
$$

等价地：

$$
\boxed{
\Delta L_i\approx -\eta\sigma_i^2\langle u_i,p-e_y\rangle^2.
}
$$

这解释了为什么高增益方向会吸引后来的特征：如果后来的特征产生的误差与已有大 $\sigma_i$ 的方向对齐，梯度下降就能通过复用该方向获得更大的一级损失下降。

---

## 4. Attention 的 Q/K 方向遵循同一下降原则

Attention 计算：

$$
q_t=W_Qh_t,
\qquad
k_i=W_Kh_i.
$$

attention 分数为：

$$
s_{ti}=\frac{q_t^\top k_i}{\sqrt d}.
$$

attention 权重为：

$$
\alpha_{ti}=\frac{\exp(s_{ti})}{\sum_{j\leq t}\exp(s_{tj})}.
$$

两个位置 $i,j$ 的权重比为：

$$
\frac{\alpha_{ti}}{\alpha_{tj}}=\exp(s_{ti}-s_{tj}).
$$

因此，一旦有有效分数间隔，softmax 会把它转成乘法级别的路由差异。但这本身不能证明为什么 $W_Q$ 或 $W_K$ 会产生大奇异值。证明仍来自一级损失下降。

attention 输出为：

$$
o_t=\sum_{i\leq t}\alpha_{ti}r_i,
\qquad
r_i=W_Vh_i.
$$

设

$$
g_{ti}=\frac{\partial L}{\partial s_{ti}}.
$$

对 softmax attention，有：

$$
\frac{\partial o_t}{\partial s_{ti}}=\alpha_{ti}(r_i-o_t).
$$

因此：

$$
g_{ti}=\alpha_{ti}\left\langle \frac{\partial L}{\partial o_t},r_i-o_t\right\rangle.
$$

这个式子表示增加分数 $s_{ti}$ 对下游损失是有利还是有害。

对 query 矩阵做分解：

$$
W_Q=U_Q\Sigma_QV_Q^\top=\sum_a \sigma_a^Q u_a^Q(v_a^Q)^\top.
$$

扰动 query 位置的隐藏状态：

$$
\delta h_t=\epsilon v_a^Q.
$$

则：

$$
\delta q_t=W_Q\delta h_t=\epsilon\sigma_a^Q u_a^Q.
$$

诱导的分数变化为：

$$
\delta s_{ti}=\frac{(\delta q_t)^\top k_i}{\sqrt d}
=\frac{\epsilon\sigma_a^Q}{\sqrt d}\langle u_a^Q,k_i\rangle.
$$

一级损失变化为：

$$
\delta L\approx \sum_{i\leq t} g_{ti}\delta s_{ti}
=\epsilon\sigma_a^Q\left\langle u_a^Q,\frac{1}{\sqrt d}\sum_{i\leq t}g_{ti}k_i\right\rangle.
$$

定义：

$$
\gamma_t^Q=\frac{1}{\sqrt d}\sum_{i\leq t}g_{ti}k_i.
$$

它正是 $\partial L/\partial q_t$。因此：

$$
\delta L\approx \epsilon\sigma_a^Q\langle u_a^Q,\gamma_t^Q\rangle.
$$

梯度步在 $v_a^Q$ 上的贡献带来：

$$
\Delta L_a^Q\approx -\eta(\sigma_a^Q)^2\langle u_a^Q,\gamma_t^Q\rangle^2.
$$

所以，大 query 奇异值只有当其输出侧 query 奇异向量与有用的分数梯度方向对齐时才被偏好。

key 矩阵结构相同。若

$$
W_K=U_K\Sigma_KV_K^\top=\sum_b \sigma_b^K u_b^K(v_b^K)^\top,
$$

定义：

$$
\gamma_i^K=\frac{1}{\sqrt d}\sum_t g_{ti}q_t.
$$

这就是 $\partial L/\partial k_i$。对应 key 侧损失下降为：

$$
\Delta L_b^K\approx -\eta(\sigma_b^K)^2\langle u_b^K,\gamma_i^K\rangle^2.
$$

因此：

$$
\boxed{
\text{Q/K 高增益方向被选择，是因为它们能高效地产生有用的分数变化，而 softmax 又把分数变化转成尖锐路由。}
}
$$

这也解释了为什么 $W_V$ 可能不同。$W_Q$ 和 $W_K$ 决定哪些状态交互；$W_V$ 在路由之后承载内容。因此，没有同等强的理由要求所有 value 内容都坍到同一个小的高增益路由子空间。

---

## 5. 共享高增益方向导致特征干扰

设两个特征表示为：

$$
h_f=\sum_i c_{f,i}v_i,
\qquad
h_g=\sum_i c_{g,i}v_i.
$$

原始表示重叠为：

$$
\langle h_f,h_g\rangle=\sum_i c_{f,i}c_{g,i}.
$$

输出效果为：

$$
Wh_f=\sum_i\sigma_i c_{f,i}u_i,
\qquad
Wh_g=\sum_i\sigma_i c_{g,i}u_i.
$$

由于 $u_i$ 正交，输出效果重叠为：

$$
\langle Wh_f,Wh_g\rangle=\sum_i\sigma_i^2c_{f,i}c_{g,i}.
$$

这就是精确的干扰放大公式。即使原始表示重叠中等，高 $\sigma_i$ 方向中的重叠也会在输出空间被 $\sigma_i^2$ 放大。

因此，如果两个特征共享同一个 top-$k$ 高增益子空间，那么改变一个特征会强烈影响另一个特征。当两个特征确实共享结构时，这是有用的；当稀有特征需要公共骨架不能表达的特异性时，这是有害的。

梯度中也有相同效果：

$$
\nabla_h L=W^\top\nabla_z L=\sum_i\sigma_i\langle u_i,\nabla_z L\rangle v_i.
$$

所以，高增益奇异方向也是高梯度流方向。这就是为什么公共特征子空间会成为后续学习的吸引子。

---

## 6. 为什么只做投影不够

一个自然方案是冻结公共特征子空间 $C$，并抑制后续梯度在 $C$ 内的分量。这个是必要的，但不充分。

原因是公共样本在后续训练中仍持续出现。普通交叉熵为：

$$
\ell_{\mathrm{CE}}=-\log p_y.
$$

只要 $p_y\neq 1$，它对正确标签 log 概率的导数就非零。在 softmax 模型中，精确 $p_y=1$ 需要无限 logit 间隔。因此，普通交叉熵会继续推动已经学会的公共样本经历：

$$
0.9\rightarrow0.99\rightarrow0.999\rightarrow0.9999.
$$

如果只抑制 $C$ 内部的分量，那么残余公共特征梯度可能移动到 $P_{\perp C}$ 中。这样公共特征会占领本来希望留给长尾特征的互补方向。

因此，方法需要两个机制：

$$
\boxed{
\text{置信度截断停止已学会公共样本的过度训练，子空间抑制重定向活跃长尾更新。}
}
$$

---

## 7. 为什么球面隐藏状态和 Poincaré 有界隐藏状态加 AdamW 不能解决该失败机制

本节给出负结果。结论不是说球面或 Poincaré 有界隐藏状态无用。它们可能降低激活范数增长，或改善某些表示几何。更窄、更强的结论是：

$$
\boxed{
\text{球面或 Poincaré 有界隐藏状态加普通 AdamW，本身不能保证抑制公共子空间复用。}
}
$$

原因是，已证明的失败机制存在于“通过已学习高增益子空间的更新方向”中。隐藏状态约束改变表示映射，但不必然移除 AdamW 更新方向中位于冻结公共特征子空间的分量。

### 7.1 需要的保证

令 $C$ 为冻结公共特征子空间，$P_C$ 为其投影器。令 $u_t$ 表示某个参数块在 weight decay 前的实际 AdamW 预条件更新方向。失败度量为公共子空间更新比例：

$$
\alpha_t^{\mathrm{upd}}
=
\frac{\|P_Cu_t\|^2}{\|u_t\|^2+\epsilon}.
$$

$\alpha_t^{\mathrm{upd}}$ 衡量实际更新方向有多少位于公共特征子空间。一个直接解决该失败机制的方法，应保证这个量对活跃长尾更新下降。

C3S-AdamW 定义：

$$
\tilde u_t=r_t(I-\rho_tP_C)u_t.
$$

当 $r_t>0$ 时，公共子空间分量变为：

$$
P_C\tilde u_t=r_t(1-\rho_t)P_Cu_t,
$$

互补分量变为：

$$
P_{\perp C}\tilde u_t=r_tP_{\perp C}u_t.
$$

因此，公共到互补的更新能量比会乘以 $(1-\rho_t)^2$。这是代数保证。

隐藏状态约束也必须用同一目标评价。仅仅限制 $\|h\|$ 不够；它必须降低实际优化器更新中 $\|P_Cu_t\|$ 相对于 $\|P_{\perp C}u_t\|$ 的比例。

### 7.2 球面隐藏状态约束激活范数，但不阻止参数空间复用

球面隐藏状态把隐藏表示 $h$ 替换为：

$$
\bar h=\frac{h}{\|h\|}.
$$

于是 $\bar h$ 位于单位球面，$\|\bar h\|=1$，隐藏状态范数不再是自由度。

但输出 logit 仍可以是：

$$
z_y=w_y^\top \bar h.
$$

由于 $\|\bar h\|=1$，模型仍能通过增大 $\|w_y\|$ 或更早参数矩阵的奇异值来增大 logit。因此，球面归一化阻断了一种大 logit 路径，但不阻止参数空间增益增长。

最小反例：二分类 logistic 回归，归一化特征 $\bar h$，标签 $y=1$：

$$
\ell(w)=\log(1+\exp(-w^\top \bar h)).
$$

梯度是：

$$
\nabla_w\ell(w)=-\sigma(-w^\top\bar h)\bar h.
$$

梯度方向正好是 $\bar h$。如果 $\bar h\in C$，则：

$$
P_C\nabla_w\ell(w)=\nabla_w\ell(w),
\qquad
P_{\perp C}\nabla_w\ell(w)=0.
$$

因此，在 AdamW 预条件器不把这个一维方向旋出时，

$$
\alpha^{\mathrm{upd}}=1.
$$

隐藏状态完全在球面上，但更新仍完全位于公共特征子空间。这给出形式化负结果：

$$
\boxed{
\text{球面归一化不推出 }\|P_Cu_t\|<\|u_t\|\text{，也不保证降低 }\alpha_t^{\mathrm{upd}}.
}
$$

### 7.3 球面隐藏状态仍允许奇异值放大

同一个反例还说明，交叉熵仍会放大参数范数：

$$
\|\nabla_w\ell(w)\|=\sigma(-w^\top\bar h)\|\bar h\|=\sigma(-w^\top\bar h).
$$

只要 $w^\top\bar h$ 有限，该量为正。因此普通交叉熵持续推动 $w^\top\bar h$ 增大。由于 $\|\bar h\|=1$，这种压力必须由 $w$ 或影响 $\bar h$ 方向的更早矩阵吸收。

所以，球面隐藏状态不能解决公共特征过度训练问题。它移除了隐藏状态径向增长，但保留了交叉熵推动参数空间 margin 增大的压力。

### 7.4 Poincaré 有界隐藏状态限制欧氏半径，但不控制 AdamW 更新几何

Poincaré 有界隐藏状态把表示映射到开单位球：

$$
h_B\in\mathbb{B}^d=\{x\in\mathbb{R}^d:\|x\|<1\}.
$$

这给隐藏表示施加欧氏范数上界，并可赋予半径双曲几何解释。原点到 $h_B$ 的双曲距离为：

$$
d_{\mathbb{B}}(0,h_B)=2\operatorname{arctanh}(\|h_B\|).
$$

但使用普通 AdamW 时，可训练参数仍在欧氏参数坐标中更新。隐藏表示虽在双曲球内，优化器不会自动把更新投影离开公共特征子空间 $C$。

同一反例适用。令输出 logit 为：

$$
z_y=w_y^\top h_B,
\qquad
\|h_B\|<1.
$$

二分类 logistic 损失为：

$$
\ell(w)=\log(1+\exp(-w^\top h_B)),
$$

梯度为：

$$
\nabla_w\ell(w)=-\sigma(-w^\top h_B)h_B.
$$

如果 $h_B\in C$，则整个参数更新位于公共特征子空间中：

$$
P_C\nabla_w\ell(w)=\nabla_w\ell(w),
\qquad
P_{\perp C}\nabla_w\ell(w)=0.
$$

因此 $\alpha^{\mathrm{upd}}=1$。隐藏状态在 Poincaré 球内有界，但 AdamW 更新仍完全与公共特征子空间对齐。

### 7.5 双曲度量不消除更新空间抑制的必要性

一种希望是 Poincaré 非线性几何会改变梯度，从而解决问题。但如果优化器仍是普通 AdamW，而不是显式控制相关子空间的黎曼优化器，则参数更新仍基于可训练矩阵的欧氏梯度。

设有界隐藏状态由可微映射产生：

$$
h_B=\phi(a),
$$

其中 $a$ 是未约束内部激活。则：

$$
\nabla_a\ell=J_\phi(a)^\top\nabla_{h_B}\ell.
$$

$J_\phi(a)$ 可以缩放或旋转梯度，但没有定义保证它移除公共子空间分量。一般不存在：

$$
P_CJ_\phi(a)^\top\nabla_{h_B}\ell=0.
$$

因此，Poincaré 约束可以改变梯度大小和局部几何，但不提供所需代数保证：

$$
\|P_Cu_t\|^2 \mapsto (1-\rho_t)^2\|P_Cu_t\|^2.
$$

只有显式的更新空间抑制算子能提供该保证。

### 7.6 负定理

**定理。** 球面隐藏状态加 AdamW、Poincaré 有界隐藏状态加 AdamW，本身都不能保证降低公共子空间更新主导性。更具体地说，对每种方法，都存在一个合法模型状态和一个合法样本，使隐藏表示满足该方法的几何约束，但 AdamW 更新方向满足 $P_Cu_t=u_t$，因此 $\alpha_t^{\mathrm{upd}}=1$。

**证明。** 球面情形：选取归一化隐藏状态 $\bar h$，满足 $\|\bar h\|=1$ 且 $\bar h\in C$。二分类 logistic 回归中，输出权重梯度为 $-\sigma(-w^\top\bar h)\bar h$，完全位于 $C$ 中。因此更新方向完全位于 $C$ 中，$P_Cu_t=u_t$ 且 $\alpha_t^{\mathrm{upd}}=1$。

Poincaré 情形：选取有界隐藏状态 $h_B$，满足 $\|h_B\|<1$ 且 $h_B\in C$。同样的 logistic 损失计算给出梯度 $-\sigma(-w^\top h_B)h_B$，也完全位于 $C$ 中。因此更新方向完全位于 $C$ 中。

两个构造都满足相应隐藏状态几何约束，但都没有降低公共子空间更新比例。因此，这两类方法不能证明解决奇异子空间复用机制所需的保证。

### 7.7 对论文的含义

正确结论不是球面或 Poincaré 隐藏状态整体不好，而是：

$$
\boxed{
\text{它们处理的是表示范数或表示几何，而本文失败机制是更新空间中的子空间复用问题。}
}
$$

因此，它们不是本文的主要解决方案。它们可以作为辅助控制，但严格解决方案必须作用在实际更新方向上。C3S-AdamW 正是这样做的。

---

## 8. C3S-AdamW：修正后的优化器设计

C3S-AdamW 有三个阶段。

第一阶段是 warmup：用 AdamW 和交叉熵正常训练，直到公共前置特征形成稳定骨架。

第二阶段是冻结：估计公共特征子空间 $C$，冻结其投影器 $P_C$。

第三阶段是修正训练：把普通交叉熵替换为置信度截断损失，并抑制活跃 AdamW 更新方向中的公共子空间分量。

更新空间细节很重要。AdamW 使用的是预条件更新方向，不是单纯原始梯度。如果在 Adam 的逐坐标预条件器之前投影原始梯度，除非该对角预条件器与 $P_C$ 可交换，否则它可能扭曲子空间。因此严格版本抑制的是 **Adam 预条件后的实际更新方向**。

令：

$$
u_t=A_tg_t.
$$

其中 $g_t$ 是选定参数块的原始梯度，$A_t$ 是 Adam 的正对角预条件器，$u_t$ 是 weight decay 前的预条件 Adam 方向。普通 AdamW 更新为：

$$
\Delta\theta_t^{\mathrm{AdamW}}=-\eta u_t-\eta\lambda\theta_t.
$$

C3S-AdamW 修改的是 $u_t$，而不只是 $g_t$。

---

## 9. 置信度截断损失和残余学习门

选择置信度阈值 $q<1$，例如 $q=0.9$。硬置信度截断损失为：

$$
\ell_{\mathrm{cap}}(x,y)=\max(-\log p_y+\log q,0).
$$

如果 $p_y<q$，样本仍活跃；如果 $p_y\geq q$，损失为零。

平滑版本为：

$$
\ell_{\mathrm{smooth}}(x,y)=\tau\log\left(1+\exp\left(\frac{-\log p_y+\log q}{\tau}\right)\right).
$$

其中 $\tau>0$ 是平滑温度。它对 $-\log p_y$ 的导数为：

$$
r_t=\sigma\left(\frac{\log q-\log p_{y,t}}{\tau}\right).
$$

$r_t$ 是残余学习门。如果 $p_{y,t}\ll q$，则 $r_t\approx1$；如果 $p_{y,t}\gg q$，则 $r_t\approx0$。它衡量样本是否仍应产生有意义学习压力。

---

## 10. 更新空间中的冻结公共子空间抑制

令 $U_C$ 为冻结公共特征子空间的正交基。投影器为：

$$
P_C=U_CU_C^\top.
$$

互补投影器为：

$$
P_{\perp C}=I-P_C.
$$

给定 Adam 预条件更新方向 $u_t$，定义与冻结公共子空间的对齐：

$$
\alpha_t=\frac{\|P_Cu_t\|^2}{\|u_t\|^2+\epsilon}.
$$

令：

$$
\rho_t=\rho_{\max}\alpha_t,
$$

其中 $\rho_{\max}\in[0,1]$。修正更新方向为：

$$
\tilde u_t=r_t(I-\rho_tP_C)u_t.
$$

最终更新：

$$
\Delta\theta_t=-\eta\tilde u_t-\eta\lambda\theta_t.
$$

这是严格优化器。与早期非正式版本的关键区别是：抑制应用在 Adam 预条件之后，因此证明作用于真实参数更新方向。

---

## 11. Transformer 参数块的矩阵形式

对矩阵块 $W\in\mathbb{R}^{m\times d}$，公共子空间可能在输入侧。设公共隐藏侧基为 $V_C\in\mathbb{R}^{d\times k}$，投影器为：

$$
P_C^h=V_CV_C^\top.
$$

若 $U_t$ 是 $W$ 的预条件 Adam 更新矩阵，则输入侧公共分量为：

$$
U_tP_C^h.
$$

修正更新为：

$$
\tilde U_t=r_t\left(U_t-\rho_tU_tP_C^h\right).
$$

如果相关公共子空间在输出侧，则使用左乘：

$$
\tilde U_t=r_t\left(U_t-\rho_tP_C^oU_t\right).
$$

这一输入侧 / 输出侧区别对实现很重要。矩阵向量化后，证明相同。

---

## 12. 算法

当 $t<T_0$ 时，正常训练：

$$
\Delta\theta_t=-\eta u_t-\eta\lambda\theta_t.
$$

在 $t=T_0$，估计公共特征子空间。一种方式是对选定矩阵做 SVD：

$$
W(T_0)=U\Sigma V^\top.
$$

如果隐藏侧方向相关，选取 $V$ 的前 $k$ 列作为 $V_C$；如果输出侧方向相关，选取 $U$ 的前 $k$ 列作为 $U_C$。

另一种方式是使用公共样本更新协方差：

$$
G_C=\mathbb{E}_{x\in\mathcal{D}_C}[u(x)u(x)^\top].
$$

其中 $u(x)$ 是公共或已学会样本产生的预条件更新方向。然后取：

$$
U_C=\operatorname{TopEig}_k(G_C).
$$

冻结 $P_C$ 后，每一步计算 $p_{y,t}$ 和：

$$
r_t=\sigma\left(\frac{\log q-\log p_{y,t}}{\tau}\right).
$$

计算 Adam 预条件更新方向 $u_t$，再计算：

$$
\alpha_t=\frac{\|P_Cu_t\|^2}{\|u_t\|^2+\epsilon},
\qquad
\rho_t=\rho_{\max}\alpha_t.
$$

修正更新方向：

$$
\tilde u_t=r_t(I-\rho_tP_C)u_t.
$$

最后更新：

$$
\Delta\theta_t=-\eta\tilde u_t-\eta\lambda\theta_t.
$$

---

## 13. 证明 I：冻结投影器近似

该证明说明为什么可以在 warmup 后只计算一次 $P_C$。

令 $P_C(t)$ 为第 $t$ 步理想公共特征投影器，$P_C(T_0)$ 为冻结投影器。假设：

$$
\|P_C(t)-P_C(T_0)\|_2\leq\epsilon_C
\qquad
\text{for all }t\geq T_0.
$$

在线抑制使用：

$$
\tilde u_t^{\mathrm{online}}=(I-\rho P_C(t))u_t.
$$

冻结抑制使用：

$$
\tilde u_t^{\mathrm{frozen}}=(I-\rho P_C(T_0))u_t.
$$

两者相减：

$$
\tilde u_t^{\mathrm{online}}-\tilde u_t^{\mathrm{frozen}}
= -\rho(P_C(t)-P_C(T_0))u_t.
$$

取范数并使用假设：

$$
\|\tilde u_t^{\mathrm{online}}-\tilde u_t^{\mathrm{frozen}}\|
\leq
\rho\epsilon_C\|u_t\|.
$$

因为 $0\leq\rho\leq1$，当 $\epsilon_C$ 小时，冻结方法可近似在线方法。

---

## 14. 证明 II：置信度截断阻止公共特征泄漏

对已学会样本，若：

$$
p_y\geq q,
$$

硬截断损失为：

$$
\ell_{\mathrm{cap}}(x,y)=\max(-\log p_y+\log q,0).
$$

因为 $p_y\geq q$，有：

$$
-\log p_y+\log q\leq0.
$$

所以：

$$
\ell_{\mathrm{cap}}(x,y)=0.
$$

在 $p_y>q$ 区域损失局部常数，梯度为零：

$$
\nabla_\theta \ell_{\mathrm{cap}}(x,y)=0.
$$

因此数据梯度更新方向为零。该样本不能在 $C$ 内或 $P_{\perp C}$ 内产生新运动。

在边界 $p_y=q$ 处，硬截断有次梯度；连续训练中该边界测度为零，也可选零次梯度或使用平滑版本。

平滑截断中，梯度乘以：

$$
r_t=\sigma\left(\frac{\log q-\log p_y}{\tau}\right).
$$

当 $p_y\gg q$ 时，$r_t\approx0$，更新不精确为零，但可忽略。这证明了平滑版本的泄漏控制。

---

## 15. 证明 III：子空间抑制保持互补分量

$P_C$ 是正交投影器，因此：

$$
P_C^2=P_C,
\qquad
P_{\perp C}=I-P_C,
\qquad
P_CP_{\perp C}=0.
$$

每个更新方向可分解为：

$$
u_t=P_Cu_t+P_{\perp C}u_t.
$$

抑制公共分量：

$$
\hat u_t=(I-\rho P_C)u_t.
$$

代入分解并化简：

$$
\hat u_t=(1-\rho)P_Cu_t+P_{\perp C}u_t.
$$

因此：

$$
P_C\hat u_t=(1-\rho)P_Cu_t,
$$

且：

$$
P_{\perp C}\hat u_t=P_{\perp C}u_t.
$$

所以抑制会缩小公共子空间分量，并精确保留互补分量。

加入残余学习门后，$\tilde u_t=r_t\hat u_t$，两个分量都被 $r_t$ 缩放。门控制样本是否继续学习；投影控制活跃更新去哪里。

---

## 16. 证明 IV：抑制降低公共子空间能量比

假设 $P_{\perp C}u_t\neq0$。抑制前公共到互补能量比为：

$$
R_{\mathrm{raw}}=\frac{\|P_Cu_t\|^2}{\|P_{\perp C}u_t\|^2}.
$$

抑制后：

$$
\hat u_t=(1-\rho)P_Cu_t+P_{\perp C}u_t.
$$

新比值为：

$$
R_{\mathrm{sup}}=\frac{\|(1-\rho)P_Cu_t\|^2}{\|P_{\perp C}u_t\|^2}
=(1-\rho)^2R_{\mathrm{raw}}.
$$

因为 $0\leq\rho\leq1$，有 $R_{\mathrm{sup}}\leq R_{\mathrm{raw}}$。如果 $\rho>0$ 且 $P_Cu_t\neq0$，不等式严格。

---

## 17. 证明 V：抑制降低高增益功能吸引

令 $J_t$ 为局部雅可比矩阵，把参数更新方向映射为相关模型输出的一级变化：

$$
\delta z_t\approx J_t\delta\theta_t.
$$

原始更新的公共子空间贡献为：

$$
\delta z_C=J_tP_Cu_t.
$$

互补贡献为：

$$
\delta z_\perp=J_tP_{\perp C}u_t.
$$

抑制后，公共贡献变为：

$$
\delta z_C^{\mathrm{sup}}=J_t((1-\rho)P_Cu_t)=(1-\rho)\delta z_C.
$$

互补贡献不变：

$$
\delta z_\perp^{\mathrm{sup}}=J_tP_{\perp C}u_t=\delta z_\perp.
$$

因此若 $\delta z_\perp\neq0$，公共功能效果与互补功能效果比值满足：

$$
Q_{\mathrm{sup}}
=\frac{\|\delta z_C^{\mathrm{sup}}\|}{\|\delta z_\perp^{\mathrm{sup}}\|}
=(1-\rho)Q_{\mathrm{raw}}.
$$

所以 C3S-AdamW 把公共子空间功能主导性降低 $1-\rho$ 倍。

---

## 18. 主定理

**定理。** 对 warmup 后的一个选定参数块，假设：

1. 公共特征投影器稳定：

$$
\|P_C(t)-P_C(T_0)\|_2\leq\epsilon_C.
$$

2. 已学会公共样本满足 $p_y\geq q$。

3. 活跃长尾样本有非零互补更新分量：

$$
P_{\perp C}u_t\neq0.
$$

4. 优化器使用：

$$
\tilde u_t=r_t(I-\rho_tP_C)u_t,
\qquad
\Delta\theta_t=-\eta\tilde u_t-\eta\lambda\theta_t.
$$

则：已学会公共样本在硬置信度截断下产生零数据梯度更新；活跃样本的公共子空间分量乘以 $1-\rho_t$，互补分量在残余门之前被保留；公共到互补更新能量比乘以 $(1-\rho_t)^2$；在局部线性化下，公共到互补功能效果比乘以 $1-\rho_t$。

因此，C3S-AdamW 同时停止已学会公共特征的过度训练，并降低活跃长尾更新受到的高增益公共子空间吸引。

---

## 19. 定理没有声称什么

该定理不声称 C3S-AdamW 总能提高验证损失。它声称 C3S-AdamW 以精确方式改变活跃更新的几何。

它不声称公共特征子空间自动稳定。稳定性必须用 $\delta(t)$ 测量。

它不声称互补空间有足够容量学习所有长尾特征。必须用长尾准确率、稀有模式恢复和有效秩诊断来测试。

它不声称所有自然语言语义都是低秩或像合成 prefix 任务一样嵌套。合成任务只隔离一个机制：嵌套组合延续。

---

## 20. 诊断与证伪标准

第一个诊断是子空间稳定性：

$$
\delta(t)=\|P_C(t)-P_C(T_0)\|_2.
$$

若 $\delta(t)$ 大，冻结投影器假设失败。

第二个诊断是更新对齐：

$$
\alpha_t=\frac{\|P_Cu_t\|^2}{\|u_t\|^2+\epsilon}.
$$

C3S 抑制后，活跃长尾样本的该量应有效下降。

第三个诊断是特征 top-$k$ 质量。对特征方向 $u$ 和奇异向量 $v_i$：

$$
M_k(u)=\sum_{i=1}^k\langle u,v_i\rangle^2.
$$

长尾额外特征应减少被迫集中到冻结公共子空间中的程度。

第四个诊断是有效秩：

$$
d_{\mathrm{eff}}=\frac{(\operatorname{tr}\Sigma)^2}{\operatorname{tr}(\Sigma^2)}.
$$

如果方法有效，长尾学习所用表示空间的有效秩应增加，或至少避免进一步坍缩。

第五个诊断是公共特征保持：置信度截断后，公共特征准确率应保持高。

第六个诊断是长尾改善：tail completion accuracy、rare feature recovery 或 long-tail loss 应改善。

若冻结公共子空间不稳定、置信度截断损害公共特征保持、或抑制 $P_Cu_t$ 未能降低 tail-update concentration 且未改善长尾恢复，则方法被证伪。

---

## 21. 实践效率

昂贵操作不是投影本身。冻结 $U_C$ 后，投影是低秩的：

$$
P_Cu=U_C(U_C^\top u).
$$

若参数块维度为 $p$，冻结秩为 $k$，开销是 $O(pk)$，不是 $O(p^2)$。

对隐藏侧投影器 $V_CV_C^\top$ 的矩阵块，更新修正为：

$$
\tilde U=r_t(U-\rho UV_CV_C^\top).
$$

当 $k\ll d$ 时，相对完整训练步便宜。

秩 $k$ 可按解释谱能量选择：

$$
\frac{\sum_{i=1}^k\sigma_i^2}{\sum_i\sigma_i^2}\geq\gamma.
$$

$\gamma$ 可从 $0.8$ 或 $0.9$ 开始。

合理的初始配置：

- warmup 到 common-prefix accuracy 饱和；
- $q=0.9$；
- $\rho_{\max}\in[0.3,0.7]$；
- 小但非零的平滑温度 $\tau$；
- 先作用于 $W_{\mathrm{out}}$，再作用于 $W_Q$ 和 $W_K$。

---

## 22. 实验计划

第一个实验应使用已有 nested-prefix benchmark。在同一架构、数据分布和训练预算下比较标准 AdamW 与 C3S-AdamW。

期望结果不只是更低 loss，而是学习几何改变：

$$
\text{公共特征保持准确，而尾部特征更少依赖冻结公共子空间。}
$$

核心测量包括：

- common-prefix accuracy；
- tail-prefix accuracy；
- subspace drift $\delta(t)$；
- update alignment $\alpha_t$；
- top-$k$ feature mass $M_k(u)$；
- effective rank $d_{\mathrm{eff}}$；
- $W_{\mathrm{out}}$、$W_Q$、$W_K$、$W_V$ 的奇异谱。

更强第二实验应在保持组合结构固定时改变频率。例如，用相同模板构造 common 和 rare factual patterns。预测是：C3S-AdamW 对稀有组合帮助大于对常见组合帮助，因为它专门针对长尾被公共骨架吸收的问题。

---

## 23. 最终工作理论

完整理论是：

1. 嵌套组合学习产生时间顺序：公共前置特征先于长尾组合特征被学习。
2. 公共特征的重复梯度产生高增益奇异方向。
3. 后续特征被这些方向吸引，因为当与预测误差对齐时，它们能带来更大的一级损失下降。
4. 这产生高效复用，也产生特征干扰。
5. 只投影不够，因为公共样本会继续产生交叉熵梯度，并可能泄漏到互补方向。
6. 置信度截断阻止已学会公共样本继续训练。
7. 冻结公共子空间抑制把活跃长尾更新从公共高增益骨架中重定向出来。
8. 在 Adam 预条件后应用抑制，可对实际更新方向给出严格保证。

一句话：

$$
\boxed{
\text{C3S-AdamW 保留有用的公共特征骨架，同时防止它垄断后续长尾学习。}
}
$$

---

# 第二部分：细致理论检查

## 总体结论

这篇文档的局部代数推导大体正确，尤其是以下部分：SVD 下的一级损失下降、Q/K attention score 的梯度方向、正交投影抑制的能量比证明、球面/Poincaré 约束的反例、以及“必须作用在 Adam 预条件后的实际更新方向”这一修正。

但不能说“整篇理论完全无误”。更准确的裁定是：

> 作为机制建模和优化器几何保证，文档基本站得住；作为自然语言训练中该机制必然存在、C3S 必然提升长尾学习的证明，还缺少经验前提验证与若干实现边界。

---

## 1. 可靠部分

### 1.1 奇异值下降效率推导正确

在固定 $W$、局部线性化、把 $h$ 当作可扰动变量时：

$$
\Delta L_i\approx -\eta\sigma_i^2\langle u_i,p-e_y\rangle^2
$$

推导成立。关键点也正确：大奇异值本身不够，必须和输出误差方向对齐。

### 1.2 Attention Q/K 推导基本正确

$$
\frac{\partial o_t}{\partial s_{ti}}=\alpha_{ti}(r_i-o_t)
$$

以及

$$
\gamma_t^Q=\frac{1}{\sqrt d}\sum_i g_{ti}k_i=\frac{\partial L}{\partial q_t}
$$

都成立。因此 Q/K 的高增益方向可被解释为“高效改变 attention score 的方向”。

### 1.3 干扰放大公式正确

若两个特征在隐藏侧奇异向量 $v_i$ 上有重叠，则输出重叠为：

$$
\langle Wh_f,Wh_g\rangle=\sum_i\sigma_i^2c_{f,i}c_{g,i}.
$$

所以高奇异值方向会放大输出侧耦合。这是文档最干净的数学核心之一。

### 1.4 负结果成立，但边界要写清

球面归一化和 Poincaré 有界隐藏状态确实不保证 AdamW 更新离开公共子空间。反例有效，因为它只需证明“存在一种合法状态使更新完全在 $C$ 中”。

### 1.5 C3S 的投影保证正确

对正交投影器 $P_C$：

$$
(I-\rho P_C)u=(1-\rho)P_Cu+P_{\perp C}u.
$$

因此公共/互补更新能量比乘以 $(1-\rho)^2$。这部分是严格代数结论。

---

## 2. 需要修正或加边界的部分

### 问题 1：从“局部隐藏扰动”到“真实参数训练”的桥还不完整

第 3 节证明的是：若可沿隐藏方向 $v_i$ 扰动，则大奇异值方向有更大一级下降。但真实训练更新的是参数，不是直接更新 $h$。文档后面用局部雅可比补桥，这是合理方向，但应明确：

> 该证明是局部线性化机制解释，不是全局训练动力学定理。

### 问题 2：“common 特征产生高增益子空间”是经验命题，不是已证明结论

文档自己承认需要测量，但后文叙述有时容易把它写成事实。应保持边界：

> 高频/common 是否真的在 $W_{out}, W_Q, W_K$ 中形成稳定 top subspace，必须由 spectrum、alignment、update covariance 和 drift 共同支持。

### 问题 3：AdamW moment state 没有被处理

C3S 抑制的是预条件后的 $u_t$，这能保证当步更新方向。但 AdamW 的一阶/二阶动量状态仍由原始梯度积累。如果 common 梯度长期进入 moment，它可能影响后续 $u_t$ 的方向和尺度。

建议补充实现边界：

- 方案 A：只 claim 每一步实际参数更新被抑制；
- 方案 B：进一步对 Adam moment 也做投影或重置；
- 方案 C：实验报告 moment alignment，确认 common moment 不再主导。

### 问题 4：weight decay 会产生额外更新

最终更新含有：

$$
-\eta\lambda\theta_t.
$$

即使数据梯度为零，weight decay 仍会移动参数。文档中“已学会 common example 产生 zero update”应改为：

> 已学会 common example 产生零数据梯度更新；总参数更新仍包括 decoupled weight decay。

这不破坏核心机制，但需要严谨表述。

### 问题 5：batch 训练中 $r_t$ 不是单一标量

文档按单样本推导。实际 mini-batch 中，$r_t$ 应是 per-example loss weight，而不是对整个 batch 的单一门控。若先聚合梯度再投影，common 与 tail 梯度可能相互抵消或混合。

建议最小实现中使用 per-example loss capping；若要做 per-example update projection，成本更高，需要说明近似。

### 问题 6：Feature top-k mass 的 feature direction 需要定义

$$
M_k(u)=\sum_{i=1}^k\langle u,v_i\rangle^2
$$

要求先定义特征方向 $u$。在合成任务中可定义；在真实语言中不清楚。真实数据版本必须用 probe direction、activation difference、causal feature vector 或 update direction 来替代。

### 问题 7：C3S 成功不只取决于几何，还取决于容量

文档已写“互补空间容量必须测试”。这点非常重要：如果 C3S 成功降低 $\alpha_t$ 但 tail 不提升，不能立刻说理论错，可能是：

- tail 数据不足；
- 互补空间容量不足；
- tail feature 不可识别；
- 公共子空间其实包含必要共享结构。

---

## 3. 审查后的 claim boundary

### 可以 claim

1. 在局部线性化下，高奇异值方向在与误差对齐时提供更大一级下降。
2. 共享高增益方向会放大输出侧特征耦合。
3. 只约束隐藏状态范数或几何，不能保证 AdamW 更新离开公共子空间。
4. 若 $P_C$ 稳定且更新方向 $u_t$ 已给定，C3S 抑制能严格降低 $u_t$ 中的公共子空间能量比例。

### 不能 claim

1. 自然语言训练一定形成稳定公共高增益子空间。
2. $W_Q/W_K/W_{out}$ 必然比 $W_V$ 更集中。
3. C3S-AdamW 必然提高验证集 loss。
4. C3S-AdamW 必然让所有 tail features 学好。
5. 球面/Poincaré 方法无用；只能说它们不提供本文所需的更新空间保证。

---

# 第三部分：全文主旨总结

这篇文档想解决的问题是：

> 语言中的公共/高频前置特征会先被学会，并在参数矩阵中形成高增益子空间；后来的长尾组合特征因为梯度下降效率，会倾向复用这些高增益方向；复用带来效率，也带来特征干扰。C3S-AdamW 试图保留公共骨架，同时防止它垄断长尾学习。

核心机制链条：

```text
嵌套组合结构
→ common 特征先学会
→ repeated gradients 形成高增益奇异子空间
→ tail 特征沿该子空间下降更快
→ tail 被吸收到 common backbone
→ feature interference / tail learning failure
→ confidence cap + update-space projection 修正
```

最关键的理论分解：

```text
不是“表示有界”问题；
而是“实际优化器更新方向是否仍在 common 子空间中”的问题。
```

---

# 第四部分：联系到我们的 Gating 研究

## 1. 相同点

我们的 MoE gating 研究中，已有核心模型是：

$$
h_f=c+r_f,
\qquad
z_{f,e}=w_e^\top h_f=w_e^\top c+w_e^\top r_f.
$$

这里 $c$ 是所有 feature 共享的 common component。它通过 $w_e^\top c$ 变成 expert-specific effective bias，导致 top-1 router 在随机初始化时偏向某个 expert。

C3S 文档中的 $C$ 是公共特征子空间。它的问题不是 router logit，而是训练更新方向 $u_t$ 被 $C$ 垄断。

共同结构是：

```text
公共成分/公共子空间不是无害背景；
它会通过模型的线性打分或梯度更新，被放大成主导机制。
```

## 2. 不同点

| 维度 | 我们当前 gating 主线 | C3S 文档 |
|---|---|---|
| 问题位置 | router score / top-1 decision | optimizer update direction |
| common 的作用 | 产生 expert-specific common logit bias | 形成高增益更新吸引子 |
| 失败形式 | routing collapse / slot_NMI 低 | tail feature 被 common backbone 吸收 |
| 当前目标 | label-free common-control router | C3S-AdamW optimizer |
| 第一指标 | slot_NMI、route purity、common margin | tail accuracy、update alignment、feature mass、effective rank |

因此，这篇文档不能直接替代我们的 active anchor。它更适合作为下一阶段：

> gate 不塌后，进一步测试 common/rare conflict 是否真的造成 feature interference 和 capacity loss。

## 3. 对我们研究流程的更新

正确流程不是立刻上 C3S-AdamW，而是先做 metric/data audit：

```text
1. 先验证 common/rare conflict 是否存在；
2. 再验证 tail update 是否真的集中在 common 子空间；
3. 再判断 C3S 类 update suppression 是否必要；
4. 最后才测试 optimizer 方法。
```

这符合我们现在的 research system：先裁定现象和物理先验，再上方法。

---

# 第五部分：导师真正要解决的问题、物理先验、假说、minimal test

## 1. 导师要解决的问题

更精确地说，导师要解决的不是“怎么设计一个新 optimizer”，而是：

> 在组合语言学习中，高频/common 特征是否会形成高增益公共骨架，并让长尾/更细粒度特征被迫复用该骨架，从而产生特征干扰和容量浪费？

对我们的 MoE 主线，对应问题是：

> MoE router 是否真正按 feature identity 分工，还是被 common component / common utility / high-gain common backbone 劫持，导致多个本该区分的 feature 被送到同一个 expert？

---

## 2. 物理先验

这里的“物理先验”是关于真实学习过程的可反驳事实，而不是方法偏好。

### P1：语言特征是嵌套组合的

简单特征会被更复杂特征复用：

$$
A\to AB\to ABC\to ABCD.
$$

可反驳：如果构造任务中没有复用结构，或者真实数据中 tail feature 不依赖 common feature，则该先验不适用。

### P2：common 特征先稳定

公共前置特征出现更多、被更多后续结构依赖，因此应更早稳定：

$$
T_C\ll T_T.
$$

可反驳：若 $\delta(t)=\|P_C(t)-P_C(T_0)\|_2$ 很大，说明 common subspace 未稳定。

### P3：梯度下降偏好一级损失下降更快的方向

若高奇异值方向与误差对齐，沿它更新更划算：

$$
\Delta L_i\approx -\eta\sigma_i^2\langle u_i,p-e_y\rangle^2.
$$

可反驳：若 tail error 与 common 高奇异方向不对齐，或者 tail update 不集中到 common subspace，则该机制不主导。

### P4：共享高增益方向会放大干扰

输出重叠为：

$$
\langle Wh_f,Wh_g\rangle=\sum_i\sigma_i^2c_{f,i}c_{g,i}.
$$

可反驳：若 common/tail 的功能输出不共享高 $\sigma_i$ 方向，或 tail 改动不影响 common/other features，则干扰不成立。

### P5：普通交叉熵会继续训练已学会 common 样本

只要 $p_y<1$，common 样本仍产生梯度。可反驳：若 common 样本后期梯度已经可忽略，confidence cap 的必要性下降。

---

## 3. 假说

### H1：common 特征形成稳定高增益子空间

支持条件：warmup 后 $\delta(t)$ 小；$W_{out}/W_Q/W_K$ 的 top singular subspace 与 common-feature/update covariance 对齐；top energy 或 common alignment 高。

削弱条件：$P_C$ 漂移大，或 top singular vectors 不对齐 common 特征。

### H2：tail 学习被吸入 common 子空间

支持条件：标准 AdamW 下 tail example 的更新对齐

$$
\alpha_t=\frac{\|P_Cu_t\|^2}{\|u_t\|^2+\epsilon}
$$

显著高；tail feature 的 top-$k$ mass $M_k(u)$ 高；tail error 高或恢复慢。

削弱条件：tail updates 主要在 $P_{\perp C}$，但 tail 仍学不好。

### H3：C3S 能改变更新几何并改善 tail

支持条件：C3S 后 tail 的 $\alpha_t$ 下降，$M_k$ 下降，有效秩不继续坍缩；common accuracy 保持；tail accuracy/loss 改善。

削弱条件：C3S 降低 $\alpha_t$ 但 tail 不改善，说明容量/可识别性/任务构造可能才是瓶颈。

### H4：隐藏状态几何约束不是主解

支持条件：sphere / Poincaré 控制组不能稳定降低 $\alpha_t$，也不能改善 tail conflict。

削弱条件：sphere / Poincaré 在相同预算下同样降低 $\alpha_t$ 并改善 tail，则文档的“不是 primary solution”需要改写。

---

## 4. Minimal test

### Test A：先做机制审计，不先测试方法

**任务**：nested-prefix 或 common+rare 合成任务。

```text
common: A
medium: AB
rare: ABC / ABCD
```

或：

```text
x = k_common + k_unique_i + noise
y = v_common + v_unique_i
```

**模型**：先用小 linear FFN 或小 Transformer；再扩展到 MoE。

**训练**：标准 AdamW。

**测量**：

```text
common accuracy / tail accuracy
T_C vs T_T
P_C drift: δ(t)
singular spectrum / effective rank
common alignment of top singular vectors
tail update alignment α_t
tail feature top-k mass M_k
head/tail reconstruction or prediction error
```

**支持机制**：common 先学会；$P_C$ 稳定；tail 更新高度进入 $C$；tail error 高。

**证伪机制**：common 不先稳定；$P_C$ 漂移大；tail 更新不在 $C$；tail error 与 common subspace 无关。

### Test B：再做最小干预

比较：

```text
1. AdamW baseline
2. confidence cap only
3. projection only
4. C3S-AdamW
5. spherical hidden state + AdamW
6. Poincaré-bounded hidden state + AdamW
```

保持架构、数据、训练预算、seed 相同。

主指标：

```text
tail accuracy / tail loss
common accuracy preservation
α_t reduction for tail updates
M_k reduction for tail feature directions
effective rank
singular spectrum and alignment
```

成功条件：

```text
C3S 降低 tail update 的 common-subspace dominance；
common accuracy 不掉；
tail recovery 改善；
cap-only/projection-only 不如完整 C3S；
sphere/Poincaré 不能提供同等 update-space guarantee。
```

失败条件：

```text
P_C 不稳定；
C3S 不降低 α_t；
common accuracy 被 cap 破坏；
tail 不改善且 α_t/M_k 也不变；
sphere/Poincaré 同样有效，说明“必须 update-space suppression”过强。
```

---

## 5. 和我们当前 Gating anchor 的最小连接

对我们现在的 MoE，先不要把 C3S 当主线方法。更合理的 next anchor 是：

```text
A07_01_common_rare_conflict_metric_audit
```

父问题：

```text
gate 不塌后，expert partition 是否真的降低 feature interference，而不是只让 load 更均匀？
```

当前子问题：

```text
common/rare conflict 是否能被合法、稳定、可证伪地测量？
```

最小测试：

```text
在已有 D_min_block_shift 或 nested-prefix synthetic 上，先审计 common subspace、tail update alignment、slot_NMI、route purity、tail accuracy、effective rank。
```

最小决策：

```text
如果 common/rare conflict 不能被稳定测量，park C3S；
如果能稳定测量，再测试 router-side common control 或 optimizer-side C3S。
```


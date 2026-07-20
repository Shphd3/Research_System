# 树状短序列表征的低秩传播：正式证明与 Claim Boundary

> 一句话结论：叶子共享低维空间并不足以保证整棵树保持同一低秩；在共享、按孩子角色区分的线性组合下，整个系统的秩由“可达子空间”的维数精确控制，公共不变子空间只是其中最强、最简单的充分条件。

---

## 0. Claim Boundary

本文只证明如下条件命题：

> 若短序列叶子表示位于一个低维线性子空间中，父节点由跨样本共享的组合算子产生，则树上表示的秩由这些算子作用于叶子空间后产生的可达子空间维数控制；在存在噪声时，可得到相应的有效秩上界。

本文不证明：

1. “短序列是语义基本单元”必然成立；
2. 短序列较短就必然低秩；
3. 使用同一个编码器或同一种组合方式就自动推出共享低维空间；
4. 任意线性或非线性组合都会保持固定秩；
5. 自然语言、世界知识或任意大模型隐藏状态天然低秩；
6. 低秩自动推出混合专家模型或扩散模型一定更优。

因此，本文给出的是一个**表示系统的条件理论**，不是关于自然语言本体的无条件定理。

---

## 1. 叶子低秩假设是否合理

### 1.1 可以作为假设，但不能作为结论

设每个叶子是短序列的表征向量：

\[
h(s)\in\mathbb R^d.
\]

对大量叶子样本进行堆叠：

\[
H_0=[h(s_1),\ldots,h(s_{n_0})]\in\mathbb R^{d\times n_0}.
\]

叶子共享严格低维空间的假设是：存在子空间

\[
S_0\subseteq\mathbb R^d,
\qquad \dim S_0=r\ll d,
\]

使得

\[
\operatorname{Col}(H_0)\subseteq S_0.
\]

这是假设，不由以下事实推出：

- 序列较短；
- 所有叶子使用同一个编码器；
- 所有叶子以后使用同一种组合规则。

“组合规则一致”约束的是父子映射；“叶子共享低维空间”约束的是叶子分布。两者必须分开提出和检验。

### 1.2 严格版本与现实版本

严格版本：

\[
\operatorname{rank}(H_0)\le r.
\]

现实中更合理的是近似版本：存在秩不超过 \(r\) 的矩阵 \(S_0^{\mathrm{mat}}\)，使得

\[
H_0=S_0^{\mathrm{mat}}+R_0,
\qquad
\|R_0\|_F\le\varepsilon_0.
\]

因此推荐顺序是：

1. 先证明严格低秩定理，明确结构边界；
2. 再证明噪声下的有效秩定理；
3. 实验中主要检验近似共享子空间，而不是数值上的严格矩阵秩。

---

## 2. 数学对象

考虑一批有序、平衡的 \(b\) 叉树，叶子层记为 \(\ell=0\)，根层记为 \(\ell=L\)。

- 节点表示维度：\(d\)；
- 第 \(\ell\) 层节点数：\(n_\ell\)；
- 第 \(\ell\) 层节点矩阵：

\[
H_\ell=[h_{\ell,1},\ldots,h_{\ell,n_\ell}]
\in\mathbb R^{d\times n_\ell}.
\]

定义所有层表示的横向拼接：

\[
H_{\le L}
=
[H_0,H_1,\ldots,H_L].
\]

“整个系统严格低秩”指：

\[
\operatorname{rank}(H_{\le L})\ll d.
\]

本文使用：

- \(r\)：叶子子空间维数；
- \(L\)：实际树深；
- \(K\)：树深上界；
- \(b\)：分支数。

不要同时用同一个符号表示秩和深度。

---

## 3. 组合模型

### 3.1 最小但保留顺序的共享线性组合

对每层 \(\ell\) 和孩子位置 \(j\in\{1,\ldots,b\}\)，定义：

- \(P_{\ell,j}\in\mathbb R^{n_\ell\times n_{\ell+1}}\)：选择每个父节点的第 \(j\) 个孩子；
- \(W_{\ell,j}\in\mathbb R^{d\times d}\)：该层共享的第 \(j\) 个孩子变换；
- \(E_{\ell+1}\in\mathbb R^{d\times n_{\ell+1}}\)：不能由共享线性组合解释的新方向、非线性误差或噪声。

组合关系为：

\[
\boxed{
H_{\ell+1}
=
\sum_{j=1}^{b}
W_{\ell,j}H_\ell P_{\ell,j}
+E_{\ell+1}.
}
\tag{3.1}
\]

二叉树中对应：

\[
h_p=W_{\ell,L}h_{c_L}+W_{\ell,R}h_{c_R}+e_p.
\]

这个模型比

\[
h_p=W(h_L+h_R)
\]

更合理，因为左右孩子可以承担不同角色；同时它仍足以给出明确的秩边界。

---

## 4. 证明层级 0：无约束组合时不存在非平凡秩保证

### 命题 0

只假设叶子秩为 \(r\) 且树深有限，若父节点组合函数可以任意选择，则父层可以在一层内达到满秩 \(d\)。

### 证明

取 \(r=1\)，令叶子为

\[
h(t)=t e_1.
\]

定义一个跨样本共享的非线性函数：

\[
F(h(t))=(1,t,t^2,\ldots,t^{d-1})^\top.
\]

对 \(d\) 个不同的 \(t_1,\ldots,t_d\)，父节点矩阵是范德蒙德矩阵，其秩为 \(d\)。

因此，即使叶子严格位于一维空间，任意共享非线性组合仍可在一层产生满线性秩。证毕。

### 结论

至少需要以下二者之一：

1. 对组合函数施加线性或低维像空间约束；
2. 直接假设组合函数在低维集合上近似闭合。

---

## 5. 证明层级 1：共享角色线性组合下的可达子空间定理

### 5.1 可达子空间

设叶子信号空间为

\[
\mathcal R_0=S_0.
\]

递归定义：

\[
\boxed{
\mathcal R_{\ell+1}
=
\sum_{j=1}^{b}W_{\ell,j}\mathcal R_\ell.
}
\tag{5.1}
\]

定义截至深度 \(L\) 的全局可达空间：

\[
\boxed{
\mathcal R_{\le L}
=
\mathcal R_0+\mathcal R_1+\cdots+\mathcal R_L.
}
\tag{5.2}
\]

这里的“和”是子空间和。

### 5.2 路径乘积表示

对路径 \(p=(j_0,\ldots,j_{\ell-1})\in[b]^\ell\)，定义路径算子：

\[
W_p^{(\ell)}
:=
W_{\ell-1,j_{\ell-1}}\cdots W_{1,j_1}W_{0,j_0}.
\]

则：

\[
\boxed{
\mathcal R_\ell
=
\sum_{p\in[b]^\ell}
W_p^{(\ell)}S_0.
}
\tag{5.3}
\]

证明由式 (5.1) 直接归纳得到。该表达说明：第 \(\ell\) 层所有可能方向，正是叶子空间沿所有长度为 \(\ell\) 的孩子角色路径传播后的像空间之和。

### 定理 1：可达子空间控制秩

假设：

1. \(E_\ell=0\)；
2. \(\operatorname{Col}(H_0)\subseteq S_0\)，且 \(\dim S_0=r\)；
3. 父子关系满足式 (3.1)。

则：

\[
\boxed{
\operatorname{Col}(H_\ell)\subseteq\mathcal R_\ell,
}
\tag{5.4}
\]

从而：

\[
\boxed{
\operatorname{rank}(H_\ell)
\le
q_\ell:=\dim\mathcal R_\ell,
}
\tag{5.5}
\]

以及：

\[
\boxed{
\operatorname{rank}(H_{\le L})
\le
q_{\le L}:=\dim\mathcal R_{\le L}.
}
\tag{5.6}
\]

#### 证明

初始层满足

\[
\operatorname{Col}(H_0)\subseteq\mathcal R_0.
\]

若

\[
\operatorname{Col}(H_\ell)\subseteq\mathcal R_\ell,
\]

则对每个 \(j\)：

\[
\operatorname{Col}(H_\ell P_{\ell,j})
\subseteq
\operatorname{Col}(H_\ell)
\subseteq
\mathcal R_\ell.
\]

因此：

\[
\operatorname{Col}
\left(
W_{\ell,j}H_\ell P_{\ell,j}
\right)
\subseteq
W_{\ell,j}\mathcal R_\ell.
\]

对所有孩子位置求和可得：

\[
\operatorname{Col}(H_{\ell+1})
\subseteq
\sum_{j=1}^{b}W_{\ell,j}\mathcal R_\ell
=
\mathcal R_{\ell+1}.
\]

由归纳法得到式 (5.4)。式 (5.5) 直接成立。

又因为

\[
\operatorname{Col}(H_{\le L})
\subseteq
\mathcal R_0+\cdots+\mathcal R_L,
\]

故式 (5.6) 成立。证毕。

### 解释

这是最核心、最宽松的线性结论：

> 整个系统是否低秩，不由“单个线性映射是否增秩”决定，而由所有路径上的线性映射把叶子空间扩展成多大的可达空间决定。

---

## 6. 证明层级 2：一般秩增长上界及其紧性

### 推论 1：最坏情形上界

由

\[
\dim(U_1+\cdots+U_b)
\le
\sum_{j=1}^{b}\dim U_j
\]

以及线性映射不增加单个子空间的维数，有：

\[
q_{\ell+1}
\le
bq_\ell.
\]

因此：

\[
\boxed{
q_\ell\le b^\ell r,
}
\tag{6.1}
\]

以及：

\[
\boxed{
q_{\le L}
\le
r\sum_{\ell=0}^{L}b^\ell
=
 r\frac{b^{L+1}-1}{b-1}
\quad(b>1).
}
\tag{6.2}
\]

若 \(L\le K\)，则：

\[
\operatorname{rank}(H_{\le L})
\le
\min\left
\{
 d,
 r\frac{b^{K+1}-1}{b-1}
\right\}.
\tag{6.3}
\]

所以“深度有界”只有在

\[
r\frac{b^{K+1}-1}{b-1}\ll d
\]

时才真正支持全局低秩。

### 命题 1：上界在一般情形下可达到

若 \(d\ge b^Lr\)，则存在叶子空间和共享角色矩阵，使对每个 \(0\le\ell\le L\)：

\[
q_\ell=b^\ell r.
\]

若进一步 \(d\ge r\sum_{\ell=0}^{L}b^\ell\)，还可以令各层可达空间彼此正交，从而：

\[
q_{\le L}=r\sum_{\ell=0}^{L}b^\ell.
\]

#### 证明

取任意 \(r\) 维初始空间 \(\mathcal R_0\)。假设已经构造出维数为 \(q_\ell\) 的 \(\mathcal R_\ell\)。当 \(d\ge bq_\ell\) 时，可在 \(\mathbb R^d\) 中选取 \(b\) 个两两正交的 \(q_\ell\) 维子空间：

\[
T_{\ell+1,1},\ldots,T_{\ell+1,b}.
\]

对每个 \(j\)，选取线性映射 \(W_{\ell,j}\)，使其在 \(\mathcal R_\ell\) 上为到 \(T_{\ell+1,j}\) 的单射。于是：

\[
W_{\ell,j}\mathcal R_\ell=T_{\ell+1,j}.
\]

因此：

\[
\mathcal R_{\ell+1}
=
\bigoplus_{j=1}^{b}T_{\ell+1,j},
\]

从而：

\[
q_{\ell+1}=bq_\ell.
\]

归纳得到 \(q_\ell=b^\ell r\)。在树森林中允许重复具有相同表示的节点，并令其余孩子取零向量，可以构造足够多的父节点，使观测矩阵实际张成全部 \(\mathcal R_{\ell+1}\)。

若每次进一步要求新选择的 \(T_{\ell+1,j}\) 与此前的 \(\mathcal R_{\le\ell}\) 正交，则各层可达空间彼此正交，故全局维数等于各层维数之和。证毕。

因此 \(b^\ell r\) 不是证明松弛造成的假象，而是共享角色线性组合允许的真实最坏情形。

### 含义

线性映射本身不会增加一个给定子空间的维数，但多个角色映射的像空间求和后可以增加维数：

\[
\dim(W_LS+W_RS)
\le 2\dim S,
\]

且可以取等号。

---

## 7. 证明层级 3：秩增长因子与逐层固定秩

定义第 \(\ell\) 层的几何增长因子：

\[
\gamma_\ell
:=
\frac{
\dim\left(
\sum_{j=1}^{b}W_{\ell,j}\mathcal R_\ell
\right)
}{
\dim\mathcal R_\ell
},
\qquad
0\le\gamma_\ell\le b.
\tag{7.1}
\]

当 \(q_\ell>0\) 时：

\[
q_{\ell+1}=\gamma_\ell q_\ell.
\]

于是：

\[
q_\ell
=
 r\prod_{t=0}^{\ell-1}\gamma_t.
\tag{7.2}
\]

这给出三种情形：

1. \(\gamma_\ell\approx b\)：角色像空间近似互相独立，秩快速增长；
2. \(1<\gamma_\ell<b\)：存在部分重叠，秩缓慢增长；
3. \(\gamma_\ell\le1\)：组合不会扩大可达维数。

### 定理 2：逐层固定秩的充分条件

若存在子空间 \(S_\ell\) 满足：

\[
\mathcal R_\ell\subseteq S_\ell,
\qquad
\dim S_\ell\le r_\ell,
\]

且

\[
\sum_{j=1}^{b}W_{\ell,j}S_\ell
\subseteq S_{\ell+1},
\qquad
\dim S_{\ell+1}\le r_{\ell+1},
\]

则：

\[
\operatorname{rank}(H_\ell)
\le r_\ell.
\]

若所有 \(r_\ell\le r\)，则每一层都至多秩 \(r\)。

### 边界

“每层秩不超过 \(r\)”仍不推出全局矩阵秩不超过 \(r\)，因为不同层的低维子空间可能互相旋转。

---

## 8. 证明层级 4：全局严格低秩

### 定理 3：全局可达维数判据

在定理 1 的条件下，如果

\[
\boxed{
\dim\mathcal R_{\le L}=q\ll d,
}
\tag{8.1}
\]

则：

\[
\boxed{
\operatorname{rank}(H_{\le L})\le q.
}
\tag{8.2}
\]

如果数据足够丰富，使

\[
\operatorname{Col}(H_{\le L})=
\mathcal R_{\le L},
\]

则：

\[
\operatorname{rank}(H_{\le L})=q.
\]

因此，在“可达方向都被样本激活”的条件下，\(q\) 不只是上界，而是整个系统的精确秩。

### 推论 2：公共不变子空间

若存在公共子空间 \(S_\star\subseteq\mathbb R^d\)，满足：

\[
S_0\subseteq S_\star,
\qquad
\dim S_\star=q,
\]

以及对所有 \(\ell,j\)：

\[
W_{\ell,j}S_\star\subseteq S_\star,
\]

则：

\[
\mathcal R_{\le L}\subseteq S_\star,
\]

从而：

\[
\boxed{
\operatorname{rank}(H_{\le L})\le q.
}
\]

### 重要说明

公共不变子空间只是一个强而易证的充分条件，不是必要条件。

真正最弱、最准确的判据是：

\[
\dim\mathcal R_{\le L}\ll d.
\]

因此，研究重点不应只放在“证明不变子空间存在”，而应放在“可达空间实际增长多快”。

---

## 9. 证明层级 5：噪声与有效秩

### 9.1 有效秩定义

定义最佳秩 \(q\) 逼近误差：

\[
\Delta_q(H)
:=
\min_{\operatorname{rank}(S)\le q}
\|H-S\|_F.
\]

根据奇异值分解：

\[
\Delta_q(H)^2
=
\sum_{i>q}\sigma_i(H)^2.
\]

定义尾部能量有效秩：

\[
\boxed{
r_\eta(H)
:=
\min\left\{
q:
\frac{\Delta_q(H)^2}{\|H\|_F^2}
\le\eta
\right\}.
}
\tag{9.1}
\]

### 9.2 近似模型

设：

\[
H_0=S_0^{\mathrm{mat}}+R_0,
\qquad
\operatorname{Col}(S_0^{\mathrm{mat}})\subseteq S_0,
\qquad
\|R_0\|_F\le\varepsilon_0.
\]

递归定义理想低维信号：

\[
S_{\ell+1}^{\mathrm{mat}}
=
\sum_{j=1}^{b}
W_{\ell,j}S_\ell^{\mathrm{mat}}P_{\ell,j}.
\]

观测系统满足：

\[
H_{\ell+1}
=
\sum_{j=1}^{b}
W_{\ell,j}H_\ell P_{\ell,j}
+E_{\ell+1}.
\]

定义残差：

\[
R_\ell=H_\ell-S_\ell^{\mathrm{mat}}.
\]

定义残差传播算子：

\[
\mathcal T_\ell(R)
:=
\sum_{j=1}^{b}W_{\ell,j}RP_{\ell,j}.
\]

令：

\[
g_\ell
:=
\|\mathcal T_\ell\|_{F\to F}
=
\sup_{R\ne0}
\frac{\|\mathcal T_\ell(R)\|_F}{\|R\|_F}.
\]

有粗略上界：

\[
g_\ell
\le
\sum_{j=1}^{b}
\|W_{\ell,j}\|_2\|P_{\ell,j}\|_2.
\]

定义：

\[
B_0=\varepsilon_0,
\qquad
B_{\ell+1}
=g_\ell B_\ell+
\|E_{\ell+1}\|_F.
\tag{9.2}
\]

### 定理 4：近似低秩传播

令：

\[
q_\ell:=\dim\mathcal R_\ell,
\qquad
q_{\le L}:=\dim\mathcal R_{\le L}.
\]

则：

\[
\boxed{
\Delta_{q_\ell}(H_\ell)
\le B_\ell.
}
\tag{9.3}
\]

并且：

\[
\boxed{
\Delta_{q_{\le L}}(H_{\le L})
\le
\left(
\sum_{\ell=0}^{L}B_\ell^2
\right)^{1/2}.
}
\tag{9.4}
\]

若：

\[
\frac{
\sum_{\ell=0}^{L}B_\ell^2
}{
\|H_{\le L}\|_F^2
}
\le\eta,
\]

则：

\[
\boxed{
r_\eta(H_{\le L})
\le q_{\le L}.
}
\tag{9.5}
\]

#### 证明

由定义：

\[
R_{\ell+1}
=
\mathcal T_\ell(R_\ell)+E_{\ell+1}.
\]

因此：

\[
\|R_{\ell+1}\|_F
\le
 g_\ell\|R_\ell\|_F
+
\|E_{\ell+1}\|_F.
\]

归纳得到：

\[
\|R_\ell\|_F\le B_\ell.
\]

理想信号 \(S_\ell^{\mathrm{mat}}\) 的列空间包含于 \(\mathcal R_\ell\)，所以：

\[
\operatorname{rank}(S_\ell^{\mathrm{mat}})
\le q_\ell.
\]

于是：

\[
\Delta_{q_\ell}(H_\ell)
\le
\|H_\ell-S_\ell^{\mathrm{mat}}\|_F
=
\|R_\ell\|_F
\le B_\ell.
\]

将所有理想信号拼接后，其列空间包含于 \(\mathcal R_{\le L}\)，秩至多为 \(q_{\le L}\)。拼接残差的 Frobenius 范数平方等于各层残差平方之和，因此得到式 (9.4)。式 (9.5) 由有效秩定义直接得到。证毕。

### 非平凡条件

定理成立不代表有解释力。至少需要：

\[
q_{\le L}\ll d
\]

以及：

\[
\frac{
\sqrt{\sum_\ell B_\ell^2}
}{
\|H_{\le L}\|_F
}
<1.
\]

若上界比整个矩阵范数还大，则数学上正确，但经验上空泛。

---

## 10. 为什么这套证明不应被视为“过于平凡”

### 10.1 确实平凡的部分

若直接假设存在一个公共不变的 \(r\) 维空间，则“所有层都在这个空间中”只需一步归纳。这个证明本身很简单，主要信息已经写在假设里。

### 10.2 非平凡的部分

真正有研究价值的是以下四点：

1. **无约束不可能性**：叶子一维也可经共享非线性映射变成满秩；
2. **最宽松线性边界**：角色共享线性组合最多按 \(b^\ell r\) 增长；
3. **可达空间刻画**：实际秩由所有路径像空间的重叠程度决定，而不是简单由“线性”决定；
4. **噪声下非平凡性**：需要同时控制可达维数和创新残差，才能推出有效秩。

因此，建议把论文主线写成：

\[
\text{无约束不可能}
\rightarrow
\text{一般线性秩增长}
\rightarrow
\text{可达空间刻画}
\rightarrow
\text{固定秩充分条件}
\rightarrow
\text{噪声有效秩}.
\]

---

## 11. 必须保留的反例

### 11.1 同一编码器不推出叶子低秩

令一个共享编码器满足：

\[
E(s_i)=e_i,
\qquad i=1,\ldots,d.
\]

所有样本使用同一编码器，但叶子矩阵为 \(I_d\)，秩为 \(d\)。

### 11.2 共享角色线性映射仍可增秩

令：

\[
S_0=\operatorname{span}(e_1).
\]

取：

\[
W_Le_1=e_1,
\qquad
W_Re_1=e_2.
\]

则：

\[
W_LS_0+W_RS_0
=
\operatorname{span}(e_1,e_2),
\]

维数从 1 增加到 2。

### 11.3 每层低秩不推出全局同秩

若每层分别位于互相正交的 \(r\) 维空间中，则每层秩均为 \(r\)，但：

\[
\operatorname{rank}(H_{\le L})
=(L+1)r
\]

在环境维数足够时可取等号。

---

## 12. 当前正式 Claim

### Claim A：最宽松精确结论

在共享角色线性组合下，整个系统的严格秩不超过全局可达空间维数：

\[
\operatorname{rank}(H_{\le L})
\le
\dim\mathcal R_{\le L}.
\]

### Claim B：仅依赖分支和深度的粗上界

\[
\operatorname{rank}(H_{\le L})
\le
\min\left\{
 d,
 r\sum_{\ell=0}^{L}b^\ell
\right\}.
\]

### Claim C：固定全局低秩

若：

\[
\dim\mathcal R_{\le L}=q\ll d,
\]

则整个系统严格低秩；公共不变子空间是一个足够但非必要的实现方式。

### Claim D：含噪有效秩

若可达维数较小，且残差递推量相对总能量较小，则：

\[
r_\eta(H_{\le L})
\le
q_{\le L}.
\]

---

## 13. 当前不能声称的内容

1. 所有短序列天然共享严格线性子空间；
2. 叶子低秩和树深有限就自动得到固定秩；
3. 共享线性组合必然保秩；
4. 每层低秩必然推出全局同一低秩；
5. 真实语言的低维结构一定是单一线性子空间，而不是多个子空间或非线性流形；
6. 理论上界正确就意味着它对真实系统非平凡；
7. 低秩必然要求大量低秩专家或扩散生成。

---

## 14. 接下来的证明任务

### 必须完成

1. 将“数据方向充分丰富”形式化为可检验的满激活条件；
2. 给出公共不变子空间之外、但可达维数缓慢增长的具体算子族；
3. 推导有限样本下可达子空间维数的统计估计误差；
4. 明确偏置项通过中心化或增广坐标处理；
5. 在需要时再扩展到近似非线性闭合。

### 暂时不需要

1. 任意非线性组合的普遍定理；
2. 世界知识图；
3. 复杂句法现象；
4. 混合专家训练算法；
5. 扩散模型性能证明；
6. 多种有效秩指标并行展开。

---

## 15. 最终研究问题

当前最准确、可执行的问题是：

> 对短序列叶子共享低维空间的树状表示系统，在跨样本共享、按孩子角色区分的线性组合下，可达子空间维数如何随深度增长；哪些子空间重叠或近似不变条件足以让全局严格秩或有效秩保持远小于环境维数？

这个问题既不把结论直接写进假设，也能与后续实验中的子空间维数、主角度、组合残差和有效秩一一对应。

# 树状短序列表征何时保持低维：正式证明收束版

> **文档角色：**这是 2026-07-21 组会的数学技术附件，用于集中放置定义、定理、
> 证明与反例。A14 项目的正式状态仍由项目 anchor、story 和实验结果文档维护。

## 0. 一句话结论与 Claim Boundary

**结论：**叶子表示共享低维空间，不能单独推出整棵树共享低维空间；在线性、按孩子
角色共享的组合模型中，整个系统的严格秩由“可达空间”的维数控制，而可达空间增长
又由角色压缩、同层方向复用和跨层方向复用精确决定。

本文证明的是条件命题：

1. 给定叶子共享空间和共享角色线性算子，可以精确核算每层与全局可达维数；
2. 全局严格秩不超过全局可达维数；
3. 若数据充分激活全部可达方向，该上界可以取等号；
4. 若累计新增方向受控，则全局维数固定或缓慢增长；
5. 加入受控残差后，可得到尾部能量意义下的有效秩上界。

本文不证明：

- 短序列天然共享低维空间；
- 自然语言必然是一棵树；
- Transformer 按该线性递推生成节点状态；
- 有限树深本身足以保证低维；
- 低维几何等于语义、行为使用或专家功能；
- 低维结构自动推出 MoE、低秩专家或稀疏 Router。

## 1. 数学对象与定义

考虑一批有序、平衡、有限深度的 $b$ 叉树。叶子层为 $\ell=0$，根层为
$\ell=L$。每个节点表示为 $h_v\in\mathbb R^d$。

将许多树中第 $\ell$ 层的节点向量按列堆叠：

$$
H_\ell=[h_{\ell,1},\ldots,h_{\ell,n_\ell}]
\in\mathbb R^{d\times n_\ell}.
$$

所有层的全局节点矩阵为：

$$
H_{\le L}=[H_0,H_1,\ldots,H_L].
$$

需要区分：

- **单层严格低秩：**$\operatorname{rank}(H_\ell)\ll d$；
- **所有层分别低秩：**每个 $H_\ell$ 的秩都小，但各层方向可以不同；
- **全局严格低秩：**$\operatorname{rank}(H_{\le L})\ll d$；
- **有效秩：**大部分矩阵能量由少量奇异方向解释，不要求其余奇异值严格为零。

叶子共享低维空间是一个数据假设：

$$
\operatorname{Col}(H_0)\subseteq S_0,
\qquad
\dim S_0=r\ll d.
$$

这里的“共享”指同一个 $S_0$ 跨样本复用，而不是每个叶子各自拥有一个小空间。

## 2. 共享角色线性组合模型

对第 $\ell$ 层、第 $j$ 个孩子角色，定义：

- $P_{\ell,j}$：从第 $\ell$ 层选择每个父节点的第 $j$ 个孩子；
- $W_{\ell,j}\in\mathbb R^{d\times d}$：同层、同角色跨样本共享的线性映射。

严格模型为：

$$
H_{\ell+1}
=
\sum_{j=1}^{b}
W_{\ell,j}H_\ell P_{\ell,j}.
$$

定义可达空间：

$$
\mathcal R_0=S_0,
\qquad
\mathcal R_{\ell+1}
=
\sum_{j=1}^{b}W_{\ell,j}\mathcal R_\ell,
$$

$$
\mathcal R_{\le L}
=
\mathcal R_0+\cdots+\mathcal R_L.
$$

记：

$$
q_\ell=\dim\mathcal R_\ell,
\qquad
Q_\ell=\dim\mathcal R_{\le\ell}.
$$

$q_\ell$ 是单层机制可达维数，$Q_\ell$ 是截至该层累计使用的全部方向数。

## 3. 定理层级

### T0：无约束非线性组合不存在非平凡线性秩保证

**命题。**即使叶子位于一维空间，跨样本共享的非线性组合函数也可以在一层产生
满线性秩。

**证明。**令 $S_0=\operatorname{span}(e_1)$，取 $d$ 个不同的非零实数
$t_1,\ldots,t_d$，令第 $i$ 个样本的第一个孩子为 $t_i e_1$，其余孩子固定为零。
使用同一个共享组合映射：

$$
F(t e_1,0,\ldots,0)=(t,t^2,\ldots,t^d)^\top.
$$

父层的 $d$ 个向量构成一个带非零列缩放的 Vandermonde 矩阵。由于 $t_i$ 两两不同且
非零，其行列式非零，所以父层秩为 $d$。证毕。

**最小反例。**在二维中，$F(t)=(t,t^2)$ 已可把两个一维输入样本映成两个线性无关
输出。

**边界。**共享函数不等于低维像空间。非线性推广必须额外要求低维集合近似闭合和
稳定性，不能从“函数共享”本身得到线性低秩。

### T1：可达空间包含定理

**定理。**在共享角色线性组合模型下，对任意层 $\ell$：

$$
\operatorname{Col}(H_\ell)\subseteq\mathcal R_\ell.
$$

因此：

$$
\operatorname{rank}(H_\ell)\le q_\ell,
\qquad
\operatorname{rank}(H_{\le L})\le Q_L.
$$

**证明。**基础层由叶子假设成立。若
$\operatorname{Col}(H_\ell)\subseteq\mathcal R_\ell$，则每个父节点都是若干
$W_{\ell,j}x_j$ 之和，其中 $x_j\in\mathcal R_\ell$。因此父节点属于
$\sum_jW_{\ell,j}\mathcal R_\ell=\mathcal R_{\ell+1}$。归纳得到单层包含关系。
将各层列空间相加，得到全局包含关系与秩上界。证毕。

**边界。**$Q_L$ 描述算子理论上允许的空间，不保证有限样本实际激活全部方向。

### T2：二叉树中角色压缩与方向复用的精确递推

在二叉树中定义左右角色像空间：

$$
V_{\ell,L}=W_{\ell,L}\mathcal R_\ell,
\qquad
V_{\ell,R}=W_{\ell,R}\mathcal R_\ell.
$$

记角色像空间维数：

$$
a_{\ell,L}=\dim V_{\ell,L},
\qquad
a_{\ell,R}=\dim V_{\ell,R},
$$

同层角色重叠：

$$
o_\ell=\dim(V_{\ell,L}\cap V_{\ell,R}),
$$

以及新层与历史空间的重叠：

$$
c_\ell
=
\dim(\mathcal R_{\ell+1}\cap\mathcal R_{\le\ell}).
$$

**定理。**允许角色算子在当前空间上降秩时，有：

$$
q_{\ell+1}
=
a_{\ell,L}+a_{\ell,R}-o_\ell,
$$

$$
Q_{\ell+1}
=
Q_\ell+q_{\ell+1}-c_\ell.
$$

合并得到：

$$
Q_{\ell+1}-Q_\ell
=
a_{\ell,L}+a_{\ell,R}-o_\ell-c_\ell.
$$

**证明。**第一式直接来自子空间维数公式
$\dim(A+B)=\dim A+\dim B-\dim(A\cap B)$。第二式对
$\mathcal R_{\le\ell}+\mathcal R_{\ell+1}$ 使用同一公式。证毕。

**机制解释。**

- $a_{\ell,j}$ 小表示角色映射主动丢失方向，即角色压缩；
- $o_\ell$ 大表示左右角色在同一层复用方向；
- $c_\ell$ 大表示新层继续使用历史方向。

**为什么只知道 $o_\ell,c_\ell$ 不够。**两个零映射与两个映到互异方向的单射都可
满足 $o_\ell=c_\ell=0$；前者下一层维数为 0，后者可为 2。因此还必须记录每个角色
像空间的维数 $a_{\ell,j}$。

### T3：角色算子单射时的重叠推论

若每个角色算子在 $\mathcal R_\ell$ 上单射，则：

$$
a_{\ell,L}=a_{\ell,R}=q_\ell,
$$

从而：

$$
q_{\ell+1}=2q_\ell-o_\ell.
$$

令当前空间维数为 $q$，以下三种情况都可达到：

1. **无重叠：**左右像空间正交，$o_\ell=0$，故 $q_{\ell+1}=2q$；
2. **部分重叠：**交空间维数为 $t$，故 $q_{\ell+1}=2q-t$；
3. **完全重叠：**左右像空间相同，$o_\ell=q$，故 $q_{\ell+1}=q$。

构造方法是在足够大的环境空间中分别选择两个 $q$ 维子空间，使其交维数为
$0,t,q$，再把 $\mathcal R_\ell$ 单射映到这两个子空间。

**边界。**完全层内重叠只保证下一层维数不增长。如果每一层都转向与历史正交的新
$q$ 维空间，仍有 $Q_L=(L+1)q$。因此 $o_\ell$ 不能替代跨层重叠 $c_\ell$。

### T4：一般 $b$ 叉树的精确递推与最坏上界

三个及以上子空间的和维数不能只由所有两两交集决定。定义：

$$
V_{\ell,m}=W_{\ell,m}\mathcal R_\ell,
\qquad
U_{\ell,0}=\{0\},
$$

$$
U_{\ell,m}=U_{\ell,m-1}+V_{\ell,m}.
$$

令：

$$
\rho_{\ell,m}
=
\dim(V_{\ell,m}\cap U_{\ell,m-1}),
$$

$$
\delta_{\ell,m}
=
a_{\ell,m}-\rho_{\ell,m}.
$$

$\delta_{\ell,m}$ 是第 $m$ 个角色相对已加入角色真正新增的维数。

**定理。**

$$
q_{\ell+1}
=
\sum_{m=1}^{b}\delta_{\ell,m}
=
\sum_{m=1}^{b}(a_{\ell,m}-\rho_{\ell,m}).
$$

**证明。**逐步使用：

$$
\dim(U_{\ell,m-1}+V_{\ell,m})
=
\dim U_{\ell,m-1}+a_{\ell,m}-\rho_{\ell,m}.
$$

从 $U_{\ell,0}=0$ 递推至 $U_{\ell,b}=\mathcal R_{\ell+1}$ 即得。角色加入顺序会改变
单个 $\rho_{\ell,m}$，但新增维数总和不改变。证毕。

因为 $a_{\ell,m}\le q_\ell$，所以：

$$
q_{\ell+1}\le bq_\ell,
$$

$$
q_\ell\le b^\ell r,
$$

$$
Q_L
\le
\min\left\{
d,
r\sum_{\ell=0}^{L}b^\ell
\right\}.
$$

当环境维度足够大，可以令同层各角色像空间彼此正交，并令新层与全部历史空间正交，
从而在达到环境维度前取到这些上界。因此这不是证明松弛，而是共享角色线性模型允许
的真实最坏情况。

**多叉反例。**在二维平面中取三条不同的一维直线。它们两两交集都为零，但三者之和
仍只有二维。普通两两容斥会错误预测三维，因此必须记录逐步新增维数。

### T5：不假设公共不变空间时的缓慢增长条件

定义每层相对历史真正新增的维数：

$$
\nu_\ell=q_{\ell+1}-c_\ell.
$$

由 T2/T4：

$$
Q_{\ell+1}=Q_\ell+\nu_\ell,
$$

所以：

$$
Q_L=r+\sum_{\ell=0}^{L-1}\nu_\ell.
$$

这是全局维数的精确核算式。

**固定单层维数的一个充分条件。**若每层有一个角色完整保留当前空间，且其他角色的
像空间都包含在此前角色已经产生的空间中，则 $q_{\ell+1}=q_\ell$，故
$q_\ell=r$。该条件不要求各层使用同一空间。

**单层至多线性增长。**若存在常数 $\beta\ge0$，使每层除第一个角色外真正新增的
方向总数至多为 $\beta$，则：

$$
q_{\ell+1}\le q_\ell+\beta,
\qquad
q_\ell\le r+\ell\beta.
$$

**全局至多线性增长。**若每层相对历史真正新增的方向满足
$\nu_\ell\le\gamma$，则：

$$
Q_L\le r+L\gamma.
$$

当 $r+L\gamma\ll d$ 时，T1 推出全局严格低秩。

**必要性说明。**上述锚定角色、$\beta$ 或统一 $\gamma$ 条件都不是必要条件；但是
$Q_L=r+\sum_\ell\nu_\ell$ 是恒等式。因此，对给定的维数预算而言，“累计跨层新增
方向较少”是全局低维的必要且充分描述，只是它本身还没有解释为何新增方向会少。

### T6：公共不变子空间是强充分条件

若存在 $S_\star\subseteq\mathbb R^d$，满足：

$$
S_0\subseteq S_\star,
\qquad
W_{\ell,j}S_\star\subseteq S_\star
$$

对所有层和角色成立，则：

$$
\mathcal R_\ell\subseteq S_\star
$$

对所有层成立，因而：

$$
\operatorname{rank}(H_{\le L})
\le Q_L
\le\dim S_\star.
$$

**证明。**从 $S_0\subseteq S_\star$ 出发归纳。若
$\mathcal R_\ell\subseteq S_\star$，则每个
$W_{\ell,j}\mathcal R_\ell\subseteq S_\star$，对子空间求和仍在 $S_\star$ 中。证毕。

**为什么不是必要条件。**有限深度内，算子可以把 $S_0$ 依次送入少量新方向，使
$Q_L\ll d$，但继续作用时最终离开该有限空间。因此有限深度全局低维不要求存在对
所有未来作用都不变的公共空间。

### T7：数据充分激活条件

定义第 $\ell$ 层的角色组合映射：

$$
\Phi_\ell:\mathcal R_\ell^b\to\mathcal R_{\ell+1},
$$

$$
\Phi_\ell(x_1,\ldots,x_b)
=
\sum_{j=1}^{b}W_{\ell,j}x_j.
$$

由可达空间定义，$\operatorname{Im}\Phi_\ell=\mathcal R_{\ell+1}$。
令 $D_\ell$ 为实际数据中所有孩子元组在积空间 $\mathcal R_\ell^b$ 里的线性张成。
则：

$$
\operatorname{Col}(H_{\ell+1})=\Phi_\ell(D_\ell).
$$

所以：

$$
\operatorname{Col}(H_{\ell+1})=\mathcal R_{\ell+1}
$$

当且仅当 $\Phi_\ell(D_\ell)=\mathcal R_{\ell+1}$。一个强充分条件是
$D_\ell=\mathcal R_\ell^b$。

若叶子满足 $\operatorname{Col}(H_0)=S_0$，且每一层都充分激活，则：

$$
\operatorname{Col}(H_{\le L})=\mathcal R_{\le L},
\qquad
\operatorname{rank}(H_{\le L})=Q_L.
$$

**最小反例。**设左右角色分别把一维输入映到 $e_1,e_2$，则可达空间是二维。如果
所有孩子对始终完全相关，使父节点只能取 $e_1+e_2$ 的倍数，观测父层仍只有一维。

**边界。**样本数量大不是充分条件；孩子角色之间的相关性仍可能阻止方向被激活。

### T8：偏置与仿射空间

考虑带共享层偏置的节点递推：

$$
h_p=b_\ell+\sum_{j=1}^{b}W_{\ell,j}h_{c_j}.
$$

主处理方式采用增广坐标。令：

$$
\widetilde h=
\begin{bmatrix}h\\1\end{bmatrix}.
$$

任选 $\alpha_j$ 满足 $\sum_j\alpha_j=1$，并定义：

$$
\widetilde W_{\ell,j}
=
\begin{bmatrix}
W_{\ell,j} & \alpha_jb_\ell\\
0 & \alpha_j
\end{bmatrix}.
$$

则：

$$
\sum_j\widetilde W_{\ell,j}\widetilde h_{c_j}
=
\begin{bmatrix}
b_\ell+\sum_jW_{\ell,j}h_{c_j}\\
1
\end{bmatrix}.
$$

因此共享偏置可以精确转化为 $d+1$ 维线性模型。直接研究仿射包与此在几何上等价；
按层中心化只有在层均值满足相同组合关系时才会精确消除偏置。

**边界。**节点特异偏置不能由同一个共享增广算子解释，应视为额外输入或创新残差。

### T9：含噪声时的有效秩推论

设观测系统满足：

$$
H_{\ell+1}
=
\mathcal T_\ell(H_\ell)+E_{\ell+1},
$$

其中：

$$
\mathcal T_\ell(X)
=
\sum_jW_{\ell,j}XP_{\ell,j}.
$$

定义最佳 rank-$q$ 逼近误差：

$$
\Delta_q(H)
=
\min_{\operatorname{rank}(S)\le q}\|H-S\|_F.
$$

令 $\overline H_0$ 是 $H_0$ 的最佳 rank-$r$ 逼近，并以
$S_0=\operatorname{Col}(\overline H_0)$ 作为理想叶子空间。递归定义
$\overline H_{\ell+1}=\mathcal T_\ell(\overline H_\ell)$。记残差
$R_\ell=H_\ell-\overline H_\ell$，并令：

$$
g_\ell
=
\|\mathcal T_\ell\|_{F\to F}.
$$

定义：

$$
B_0=\Delta_r(H_0),
\qquad
B_{\ell+1}=g_\ell B_\ell+\|E_{\ell+1}\|_F.
$$

因为：

$$
R_{\ell+1}=\mathcal T_\ell(R_\ell)+E_{\ell+1},
$$

所以归纳得到 $\|R_\ell\|_F\le B_\ell$。理想信号列空间位于
$\mathcal R_\ell$，故：

$$
\Delta_{q_\ell}(H_\ell)\le B_\ell,
$$

以及：

$$
\Delta_{Q_L}(H_{\le L})
\le
\left(\sum_{\ell=0}^{L}B_\ell^2\right)^{1/2}.
$$

定义尾部能量有效秩：

$$
r_\eta(H)
=
\min\left\{
q:
\frac{\Delta_q(H)^2}{\|H\|_F^2}\le\eta
\right\}.
$$

若：

$$
\sum_{\ell=0}^{L}B_\ell^2
\le
\eta\|H_{\le L}\|_F^2,
$$

则：

$$
r_\eta(H_{\le L})\le Q_L.
$$

**边界。**定理正确不代表上界有解释力。若归一化误差上界不小于 1，它不优于用零
矩阵近似的平凡保证，因而不能推出有效低秩。有效秩也不等于严格秩或非线性流形的
内在维数。

## 4. 必须保留的四个反例

1. **同一编码器不推出叶子共享空间。**共享编码器完全可以令
   $E(s_i)=e_i$，使叶子矩阵为满秩单位矩阵。
2. **共享线性角色仍会增秩。**一维叶子经左右角色分别映到 $e_1,e_2$，下一层即可
   变成二维。
3. **每层低秩不推出全局同秩。**各层分别位于互相正交的 $r$ 维空间时，每层秩均为
   $r$，全局秩却可达到 $(L+1)r$。
4. **低观测秩不推出低机制容量。**可达空间可以很大，但相关孩子样本只激活一个
   方向。

## 5. 最终定理状态

| 类型 | 当前内容 |
|---|---|
| Definition | 单层秩、全局秩、可达空间、角色像维数、层内与跨层重叠、有效秩 |
| Data assumption | 叶子跨样本共享低维空间 |
| Mechanism assumption | 父节点由同层、同角色跨样本共享的线性算子组合 |
| Proved result | T0–T9：不可能性、可达空间包含、精确维数递推、缓慢增长条件、激活与噪声边界 |
| Empirical proposition | 真实短语是否共享空间、真实节点是否服从局部组合、压缩与复用量是否小 |
| Speculation | 条件化局部空间可能比全局共享空间更接近真实表示；尚未验证 |

## 6. 三句直接回答

1. **叶子共享低维空间不能单独推出整棵树共享低维空间。**
2. **真正控制全局严格秩的最弱数学量，是全部树层可达空间之和的维数 $Q_L$。**
3. **要得到固定全局低维，必须控制角色像空间维数与累计跨层新增方向；公共不变空间
   只是一个强充分条件。**

## 7. 与实验和真实语言的关系

- E07 的合成结果核对了上述维数核算的实现与负对照，不是对代数定理的证明。
- E06 的真实模型结果不支持被检验的全局共享线性金标准切分算子，但没有否定条件
  定理或条件化局部模型。
- 当前所有关键真实或受控训练传播界均为空泛，因此 T9 尚未为真实表示提供有效低维
  解释。

## 8. 组会使用建议

主汇报只讲 T0、T1、T2/T5 和三句直接回答：先用 T0 说明原推理为何失败，再用 T1
引入可达空间，用 T2/T5 解释压缩与复用如何控制全局维数。T3、T4、T6–T9 作为导师
追问时的技术附录，不应在主讲中逐式展开。

## 9. 来源

- [7 月 21 日 focus](focus.md)
- [7 月 21 日 meeting brief](meetings/tree_low_rank_closure_meeting_brief_cn.md)
- [A14 中文 anchor](../../../../../Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure_anchor_cn.md)
- [A14 中文 story](../../../../../Projects/from-attention-to-search/main/stories/14_tree_low_rank_language_structure/01_tree_aligned_compression_without_linear_propagation_cn.md)
- [E07 可达空间核算](../../../../../Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/A14_E07_reachable_space_accounting/summary.md)

---
type: theory_supplement
status: HUMAN_CONFIRMED
created: 2026-08-30
source_meeting: 2026-08-28
scope: separability formation, native Gate accessibility, and progressive residual routing
---

# 理论补充：从语义因素到可分表征，再到有用专家

> **关键勘误与版本边界：**同目录旧稿 [theory_supplement_gradient_consistency_cn.md](theory_supplement_gradient_consistency_cn.md) 曾有两处不能作为 H100 证据：第 4 节把“任意两专家的边界是超平面”加强成余弦 Gate 不能实现异或，忽略了多个线性选择 cell 经专家输出重组后可形成非凸区域；第 5 节只假设三个单位秩一算子 Frobenius 正交，却据此断言 $A+B$ 必有两个非零奇异值。旧稿现已 reciprocal 标记为被本文取代，[A15_11 Anchor 第 4.3 节](../../../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_11_gradient_consistent_hierarchical_routing/15_11_gradient_consistent_hierarchical_routing_anchor.md) 也已收紧为成对边界命题。本文第 6 节采用“归一化不使单个分数或成对边界变成非线性，也不保证目标交互”的严格边界；第 7 节使用左右奇异向量分别正交的“双正交”条件，且 E03H 实际对角生成器满足它。本文是这两处命题的当前读取入口。

## 结论

本轮需要保留的理论主线不是“粗语义更常见，所以一定占据大方差方向”，而是：

$$
\text{预测任务持续需要某因素}
+\text{跨细类梯度不抵消}
\rightarrow
\text{模型可能形成相应特征}
\rightarrow
\text{该特征可能在未见数据上可读}
\rightarrow
\text{只有额外满足谱优势才进入 PCA 头部}.
$$

即使语义标签已经可读，还必须继续区分 Gate 是否看见、top-$k$ 是否保留、所选专家是否有用，以及任务损失是否真的下降。正确层级可以给出一种精确的条件函数分解，但“存在这个分解”不自动意味着它比参数和计算匹配的平坦非线性模型学得更快。

## 1. 五个不能互换的对象

| 对象 | 精确定义 | 本轮测量 | 不能替代 |
| --- | --- | --- | --- |
| 语义标签 | 研究者指定的父类或细类变量 $Y$ | `parent_id`、$p$、$b$ | 模型内部功能 |
| 表征可访问性 | 给定表示 $R$、读出族 $\mathcal F$ 和未见划分 $\mathcal S$，能否恢复 $Y$ | 跨模板线性探针 | 原生 Router 使用 |
| Gate 可访问性 | 原生 Gate 接口是否保留同一读出 | $H\rightarrow Z\rightarrow Q$ | 专家效用 |
| 反事实专家效用 | 同一样本改用等算力候选专家时，任务损失能降低多少 | $U_{ie}=L_i(a_0)-L_i(e)$ | 自然语义或因果形成机制 |
| 功能收益 | 同预算或更少样本下，测试任务误差是否降低 | 归一化均方误差和学习曲线面积 | 几何重合或标签相关性 |

因此，“可分”必须始终写成四元组：

$$
(Y,R,\mathcal F,\mathcal S).
$$

更换标签、表示、读出器或划分，研究对象就已经变了。

## 2. 粗类贡献方差，不等于粗类位于 PCA 头部

令 $C$ 为父类、$F$ 为父类内部细类、$H$ 为模型表示。全协方差可以分解为

$$
\Sigma_H
=\underbrace{\operatorname{Cov}_C\!\left(\mathbb E[H\mid C]\right)}_{\Sigma_B^C:\ \text{父类间}}
+\underbrace{\mathbb E_C\operatorname{Cov}_{F\mid C}\!\left(\mathbb E[H\mid C,F]\right)}_{\Sigma_B^{F\mid C}:\ \text{父类内细类间}}
+\underbrace{\mathbb E_{C,F}\operatorname{Cov}(H\mid C,F)}_{\Sigma_W:\ \text{细类内}}.
$$

混合多个父类通常会增加 $\Sigma_B^C$，但主成分分析（principal component analysis，PCA）只对三项之和排序，不知道哪一项是研究者关心的语义。对于 $K$ 个父类，中心化父类均值最多张成 $K-1$ 维；父类能量还可能分散在多个方向，而一个模板或词元因素可以独占更大的单一特征值。

在三部分占据互相正交子空间的简化模型中，父类子空间进入谱头部的一个充分条件是

$$
\lambda_{\min}^{+}(\Sigma_B^C)
>
\lambda_{\max}(\Sigma_B^{F\mid C}+\Sigma_W).
$$

这是一项额外的谱优势条件，不由“父类在语义树上更高”推出。若各协方差项不共享正交分块，还需要相应的特征间隙和扰动分析，不能机械套用这个简化不等式。

## 3. 频率只有通过不抵消的平均梯度才形成稳定方向

设与父类 $c$ 相关的一次训练事件梯度为 $g_{c,F}$，其跨细类条件均值为

$$
m_c=\mathbb E_{F\mid c}[g_{c,F}].
$$

在 $N$ 次训练事件中，父类 $c$ 约出现 $Np_c$ 次。忽略参数变化时，累计梯度的漂移项约为

$$
Np_cm_c,
$$

而零均值随机波动只按 $\sqrt{Np_c}$ 的量级增长。于是：

- 若 $m_c\neq0$，频率会放大一个稳定共享更新；
- 若 $m_c=0$，更多样本不会产生定向漂移，只会更准确地显露“平均更新为零”。

一个可测的跨细类梯度一致性为

$$
\rho_C
=
\frac{
\mathbb E_C\left\|\mathbb E_{F\mid C}g_{C,F}\right\|_2^2
}{
\mathbb E_{C,F}\|g_{C,F}\|_2^2
},
\qquad 0\le \rho_C\le1.
$$

但参数方向进一步变成激活方差，还要经过表示对参数的雅可比、归一化、残差连接、优化轨迹和最终任务尺度。因此

$$
\text{高频且同向}
\not\Rightarrow
\text{最终一定是最大主成分};
$$

它首先预测的是更稳定或更快的学习漂移。

## 4. 固定线性映射不能创造线性可分性

令 $z=Ah+c$。如果变换后存在分类器 $w^\top z+b$，那么

$$
w^\top(Ah+c)+b
=(A^\top w)^\top h+(w^\top c+b)
$$

已经是原表示上的线性分类器。因此，固定仿射映射后的线性函数族只是原线性函数族的子集。

- 满列秩线性升维保持“是否存在某个线性分隔面”；
- 降秩映射可能保留或删除已有判别方向；
- 有限样本准确率变好可以来自正则化、去噪或数值条件改善，不等于创造了新线性信息；
- 未归一化 margin 可以被缩放任意改变，不能独立裁定几何改善。

所以 common 删除、PCA、随机投影或任意固定线性后处理，都不能把严格不可线性分的数据从无到有变成线性可分。

## 5. 真正能暴露新决策的是任务对齐的非线性交互或条件化

令独立变量 $p,b\in\{-1,+1\}$，并令表面坐标 $q=pb$。从全局输入 $s=(p,q)$ 恢复 $b=pq$ 是异或关系，单个仿射超平面不能完成；固定 $p$ 后却有

$$
b=pq=\pm q,
$$

分支内只需读取 $q$ 的符号。于是两种方法都可以暴露决策：

1. 显式构造乘积特征 $pq$；
2. 先按 $p$ 条件化，再在分支内解释 $q$。

关键不是“维数更高”，而是函数族加入了原来没有的交互。任意非线性也不保证有用；它必须与目标边界对齐，并在未见模板上保持正低尾间隔。

## 6. X-MoE 式余弦 Gate 改变接口，不自动获得非线性选择边界

X-MoE 式分数可写成

$$
s_e(h)
=
\frac{(Wh)^\top e_e}{\|Wh\|_2\|e_e\|_2}.
$$

对同一个 token，$\|Wh\|_2$ 对所有专家相同。专家 $i,j$ 的排序只由

$$
h^\top W^\top
\left(
\frac{e_i}{\|e_i\|_2}
-
\frac{e_j}{\|e_j\|_2}
\right)
$$

的符号决定，所以任意两专家的边界仍是超平面。余弦 Gate 可以改变 Router 可见的行空间、消除专家向量范数竞争并改变优化条件，但归一化本身没有给单个 score 加入 $pq$ 这样的非线性交互，因而不自动保证解开异或或恢复目标层级。

这不等于“一般多专家 Router 无法实现异或”。多个线性比较可以把输入切成多个多面体 cell；如果若干专家输出被组合为同一任务标签，这些 cell 的并集可以是非凸区域，因而整体函数可以表示异或式分区。严格结论只到：**单个 score 和成对边界没有因余弦归一化变成非线性，目标交互与层级仍需额外结构或学习证据。**X-MoE 因而只启发本轮审计“原生 Gate 投影和 top-$k$ 各自保留什么”，不提供语义树或专家效用定理。原始来源为 [Chi et al., NeurIPS 2022](https://papers.nips.cc/paper_files/paper/2022/file/df4f371f1f89ec8ba5014b3310578048-Paper-Conference.pdf)。

## 7. 正确层级的精确残差分解与错误层级的 $1/3$ 下界

本节的解析 oracle 假设 $p,b\in\{-1,+1\}$ 独立等权，因此四个状态各占 $1/4$，并令 $q=pb$；输入 $z\sim\mathcal N(0,I)$、无观测噪声，归一化误差用四状态算子 Frobenius 误差的精确高斯期望计算。共同专家精确为 $C$，后继专家与冻结祖先方向精确正交。先取三个单位秩一算子

$$
C=u_0v_0^\top,\qquad
A=u_1v_1^\top,\qquad
B=u_2v_2^\top,
$$

并要求左右奇异向量分别正交：$u_i^\top u_j=0$ 且 $v_i^\top v_j=0$。这是**双正交**，比仅要求 Frobenius 内积 $\langle A,B\rangle_F=0$ 更强。

重要勘误：Frobenius 正交本身不能推出 $\operatorname{rank}(A+B)=2$。例如 $A=uv_1^\top$、$B=uv_2^\top$ 且 $v_1\perp v_2$ 时，$\langle A,B\rangle_F=0$，但 $A+B=u(v_1+v_2)^\top$ 仍为秩一。E03H 的冻结 Protocol 和生成器使用对角坐标投影，满足双正交，所以实际定理有效。

定义

$$
\Theta^{work}_{p,b}=C+pA+bB,
\qquad
\Theta^{fail}_{p,b}=C+qA+bB.
$$

因为 $(p,b)\leftrightarrow(q,b)$ 是双射，work 与 fail 包含完全相同的四个教师函数，只改变函数与具名父类 $p$ 的配对。

work 的父类优先树有精确分解

$$
C\longrightarrow pA\longrightarrow bB.
$$

fail 先按 $p$ 分支时，由 $b$ 在每个固定 $p$ 内等权，第一层残差条件均值为零；叶层必须用一个秩一专家拟合

$$
qA+bB=b(pA+B).
$$

双正交使 $A+B$ 有两个都等于 1 的非零奇异值。由 Eckart--Young 最佳低秩逼近定理，任何秩一近似至少遗漏一个单位能量。目标的 $C,A,B$ 总能量为 3，因此

$$
NMSE^{oracle}_{H,fail}=\frac13.
$$

这里的精确 $1/3$ 是上述四状态等权、各向同性高斯算子期望、精确共同祖先、双正交残差和秩至多一叶的解析 oracle。实际 float32 训练只要求 learned fail 端点不低于 $1/3-10^{-4}$；观测中位端点为 $0.336926$，通过该容差护栏，而不是数值上被宣称等于精确 oracle。允许状态不平衡、非各向同性输入、秩二叶、重选第一层、复用祖先方向或联合解冻后，下界不再自动成立。

## 8. 为什么“机制可实现”不等于“方法更优”

正确树证明的是一个函数类包含关系：它能以具名三阶段实现 work，并在 fail 受容量限制。要得到方法优势，还必须有一个匹配基线无法同样高效学习的缺口。

E03H 的平坦 Router 看见完整 $s=(p,q)$，是非线性多层感知机，并且每批都看到完整四叶组合。因此它可以直接学习 $pq$ 交互；正确树没有获得独占函数类或稀缺样本条件。实验中 `H_task` 和 `F_task` 的注册面积差区间跨零，没有建立正的层级收益；这支持下面的边界，而不证明两个方法普遍等价：

$$
\text{可解释条件分解}
\not\Rightarrow
\text{相对通用非线性的训练效率优势}.
$$

同理，效用臂的负面积差与 $0,1/6,2/3$ 逐种子模式表明当前监督合同失败并伴随缺失专家。与全部账本相容的最窄解释是：尚未成熟的候选专家产生停止梯度的最优候选标签，而 hard top-1 的任务梯度只进入已选专家；未选专家会饥饿，早期选择可自我强化，阶段冻结再把缺失分支固化。即使 Router 正确选择“当前候选集合中最好者”，候选集合也可能尚未学全所需函数。它不是唯一因果定理：效用交叉熵、任务直通梯度、负载平衡、初始化和冻结没有被分别干预。

## 9. 本轮确定的理论认识与边界

### 可以确定

- 父类贡献类间方差，但不保证父类判别方向位于 PCA 头部。
- 高频只有在跨细类平均梯度不抵消时，才产生稳定共享漂移。
- 固定线性映射不能创造原来不存在的线性分隔面；任务对齐非线性交互或条件化可以扩大读出函数族。
- X-MoE 式余弦 top-$k$ 的成对边界仍为超平面；它是接口与优化先验，不是非线性语义分解保证。
- 双正交秩一生成器中，正确父类树可精确分解，错误树具有 $1/3$ 秩一误差下界。
- 上述结构定理不推出相对匹配平坦非线性模型的经验效率优势。

### 仍不能确定

- 标准下一词元预测是否通过该梯度一致性链形成自然父类方向；
- Qwen 原生 Router 是否因果使用父类语义，或所选专家是否降低语言模型损失；
- 自然语义是否具有本合成四叶树，模型能否自行发现它；
- 其他固定目标、探索或专家预训练式效用监督是否能避免饥饿。

## 10. 已确认的唯一下一理论问题

三份来源原先登记了不同下一步：08:28 文档第 12.3 节选择先比较 `NTP-only / Oracle / Shuffled-oracle`，Oracle 上界门通过后再开放 `Search / Shuffled-search`；此前 Anchor 选择软的条件期望效用目标；完整对话则选择频率乘以跨细类梯度一致性。研究者现已裁定先闭合三者共同依赖的上游表示形成机制，第三条成为唯一下一决策；Oracle/Search 与软期望效用路线停放，不并行执行。

停止继续推广残差树，下一周期只检验：

> 在表面统计、细类相关预测事件数和总预测位置数固定的两级四叶下一词元预测任务中，每个样本内父类相关预测事件的重复次数是否足以形成父类判别方向；还是必须同时具有跨细类不抵消的平均梯度，并且只有父类类间协方差获得谱优势时，该方向才进入 PCA 头部？

这里的“频率”不是父类样本数：每个样本仍同时属于一个父类和一个细类。它具体指**每条训练序列中，正确下一词元分布确实依赖父类 $C$ 的目标位置数或重复次数**。高/低频条件保持总 token、总损失项、父细类样本数、词表、模板和标签熵不变；低频条件释放出的目标位置用与父类无关、难度和词频匹配的中性预测事件替换。梯度一致性条件只改变这些父类相关事件在不同细类下推动父类特征的同向或抵消关系。

最小设计是上述父类相关预测事件频率（高/低）乘以梯度一致性（高/低）的 $2\times2$，同时记录 $\rho_C(t)$、$\operatorname{tr}\Sigma_B^C(t)$、未见模板的 5% 低尾归一化间隔和父类判别子空间对累计 PCA 子空间的重合。只有四个条件都不能形成正间隔时，才进入正确层级、平坦语义和打乱层级的显式先验比较。

## 11. 证据入口

- [08:28 组会逐句校订](../../../0828/docs/0828组会_逐句校订与下一步研究方向.md)
- [`feature (9).pdf`](<../../../0828/docs/feature (9).pdf>)
- [Qwen E01H Summary](../../../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E01H_qwen_native_router_access_gap_h100/summary.md)
- [Synthetic E03H Summary](../../../../Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03H_counterfactual_utility_residual_tree_h100/summary.md)
- [组会主线](focus_meeting_gradient_consistent_hierarchical_routing_h100.md)
- [学习导读](learning_guide_gradient_consistent_hierarchical_routing_h100_cn.md)

对话 `学习可分性理论` 已完整读取五个回合且无更早分页，用于恢复问题演化和上游停止顺序；它不是实验数字来源。所有结果数值和机器判决以冻结 Protocol、最终 H100 Summary/Detailed 与完成审计为准。

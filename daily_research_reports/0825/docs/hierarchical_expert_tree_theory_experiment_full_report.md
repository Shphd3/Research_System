# 从“条件增量信息”到“可生成的层次路由几何”

## 随机投影结论审判、导师直觉重构、自演化层次化专家树的完整理论证明与合成实验协议

> **文档状态：**`AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`  
> **实验协议状态：**`DRAFT_NOT_EXECUTABLE`  
> **文档性质：**自包含理论—实验小论文 + 现有证据审判 + 下一次组会问题定义  
> **主要来源：**`0824 gating_原文.docx`、`0824_gating_会议记录_逐句校订与证明任务.md`、`random_projection_router_proof_protocol.md`、用户给出的《自演化层次化专家树小规模验证实验方案》  
> **适用边界：**本文给出可严格证明的理想化结论与可执行的实验契约；除已完成的随机投影实验外，层次化专家树实验均尚未执行。

---

# 0. 结论先行

## 0.1 对现有随机投影 proof 的审判

现有随机投影证明链在其明确假设下**基本正确**：

1. 固定公共平移不影响样本差分；
2. 稠密高斯随机投影在足够维数下保持抽取前固定有限点集的距离；
3. 对抽取前已经冻结且具有正最小间隔的线性 Router，同时投影样本与权重可以保持有限样本决策；
4. 线性映射后再接线性分类器，不可能创造原空间线性函数族中不存在的可分性；
5. 随机谱坐标抽样需要低相干条件，不能由高谱熵替代。

这套 proof 的主要问题**不是数学错误，而是研究位置发生了变化**：它回答的是“已有良好线性路由几何能否被保持”，而当前实验证据表明完整 $R_U$ 尚未形成稳定正低尾间隔。因此它应当被保留为**下游保持定理**，不能继续充当“如何生成可路由空间”的主理论。

## 0.2 对现有随机投影实验结果的审判

现有结果支持的最强结论是：

> 在注册的 Qwen3-30B-A3B、Binding-controlled 数据、残差定义和线性探针族下，$R_U$ 对 $X$ 存在受控条件增量预测效用，但没有观察到可独立使用、跨模板稳健且具有正 $5\%$ 低尾 logit margin 的线性 Router 几何。

这里被否定的是**独立 $R_U$ 的注册几何**，不是完整隐藏状态 $X$，更不是联合表示 $(X,R_U)$。因此当前证据不能作为“整个高维隐藏空间不可线性分”的直接实验证明。

不能把它改写为：

- “高维表示在数学意义上不可线性分”；
- “不存在任何线性子空间”；
- “随机投影失败”；
- “层次化专家树已经得到验证”。

此外，外部独立人工语义复核尚未闭合，所以整套数据结论仍是**条件成立、总体 `Insufficient`**，而不是完全封闭的最终证据。

## 0.3 对用户当前 Hierarchical Expert Tree 计划的审判

当前计划**不能直接执行**。它至少有九个会改变结论的结构性问题：

1. **分裂对象用错。**计划在根专家输出 $h_0=E_{\mathrm{root}}(x)$ 上做 PCA；导师明确修正的是从当前表示中去掉根专家可解释的公共子空间，再对 residual variation 分裂。
2. **把 Dense/Flat 失败写进了 $H_0$。**Dense 与 Flat MoE 完全可能得到正 margin；基线结果不能预先规定为负，只能作为竞争解释进行实测。
3. **“无标签”与训练目标矛盾，而且根任务定义错位。**Stage 1 使用 8 粗类标签、Stage 2 使用 64 细类标签；这最多是“无标签 gate + 有标签专家训练”，不是无标签自演化。更重要的是，8 粗类监督会主动迫使根 expert 编码分支信息，不能再把它解释为只学习所有样本共用功能的 common expert。
4. **PCA 不保证语义分裂。**第一主成分只最大化总方差；若无关 style/nuisance 方差更大，PCA 必然沿错误方向分裂。
5. **所谓低秩 expert 实际并不低秩。**$d_{\mathrm{mid}}=4d$ 是扩张型 FFN，不提供低秩 Jacobian 或低秩输出子空间保证。
6. **输入梯度投影不保证抗遗忘。**$W_{t+1}=W_t-\eta G_t(I-P_C)$ 只保证新 expert 不读取 $C$，不保证其输出不改变祖先分类 logits。
7. **固定 Qwen 残差不能回答训练因果。**在冻结 $r_i$ 上训练一个新 MLP，只能说明后处理能否重编码已有表示，不能解释 NTP 如何把低维语义映射到高维空间。
8. **Margin 计算存在定义风险。**探针必须只在 TRAIN 拟合、DEV 选正则、TEST 一次冻结评估；原始 logit margin 还受权重尺度影响，跨模型应使用归一化几何 margin。
9. **模型容量与计算不匹配。**单 Dense、4-expert Flat、根加两个子 expert 的参数量、活动计算量与训练阶段均不一致，无法把收益归因于树结构。

## 0.4 更新后的核心结论

真正需要回答的问题不是：

> “维度从低变高以后，为什么仍不可分？”

而是：

> **低维潜在语义经过什么映射时，线性可分性会被保留、丢失或生成；为什么标准训练可能只学到高频公共模式而没有形成稳定细分支 margin；一个带有 residual split、分支条件非线性更新和祖先输出保护的专家树，能否在明确条件下生成正 margin，并在条件失效时按理论失败？**

---

# 1. 现有证据与导师直觉的来源审计

## 1.1 组会前的旧方案

旧方案可以概括为：

1. 单个低秩 expert 先学习较粗层级或公共功能；
2. 冻结该 expert；
3. 增加两个 specialized experts；
4. 直接使用第一个 expert 的输出进行下一层 gating；
5. 递归扩展为 $1\rightarrow2\rightarrow4\rightarrow8$。

旧解释隐含了两个未经证明的假设：

- 上层 expert 在学习粗层级时会自动形成下一层分类；
- 直接使用上层 expert 输出就能把下一层数据分开。

已有合成与真实数据实验没有支持这套做法。

## 1.2 导师在组会中完成的关键修正

导师最终固定下来的关键修正不是“换一个更强的分类器”，而是**换掉 gating 所作用的数学对象**：

$$
\text{错误对象：}\quad E_{\mathrm{root}}(h)
$$

$$
\text{候选正确对象：}\quad r=(I-P_C)(h-\bar h),
$$

其中 $C$ 是根/祖先 expert 已经能够稳定解释的公共低秩子空间。

导师的物理解释是：

- common expert 表示所有分支共同需要的功能；
- specialized expert 的必要性不是“一个 expert 的 rank 不够”，而是剩余功能之间存在条件冲突，不能由同一个低秩映射兼容；
- 新 expert 不应重复学习祖先已经解释的方向；
- 下一层 gate 应查看“祖先没有解释好的变化”，而不是祖先已经解释好的输出。

## 1.3 关于高维可分性的组会更新

组会中还固定了另一条认识：

1. 从高维向低维做线性投影，不能凭空创造线性可分性；
2. 当前冻结大模型表示在注册线性探针下没有形成稳健正 margin；
3. 这更像是**表示生成训练没有把语义组织成良好路由几何**，而不是“随机降维算法选错”；
4. 需要研究低维语义本身的结构，以及训练映射为什么没有把它变成高维中的稳定可分结构。

## 1.4 导师关于 NTP 的 intuition

导师提出但尚未证明的训练动力学解释是：

- 下一词元预测在大量位置重复使用公共语言因素；
- 高频公共模式获得更频繁、更一致的梯度；
- 低频、条件化、互相冲突的 specialized 模式学习更慢；
- 因而模型虽处于高维隐藏空间，训练轨迹可能主要占据一个低有效维数、强各向异性的 common 子空间；
- 细分支信息可能存在，但没有被组织成独立、稳健、具有正 margin 的方向。

这条解释是**候选机制**，不是现有实验已经证明的事实。

## 1.5 导师明确要求的下一步形式

导师明确要求：

- 自己构造 synthetic benchmark；
- 使用一层 Transformer；
- 同时构造“应当 work”和“应当不 work”的条件；
- 理论条件与实验现象必须一一对应；
- 快速迭代，而不是直接在大模型上扩大搜索。

因此，下一阶段的主实验不能只复用冻结的 Qwen $R_U$；必须先有一个能够控制潜在维数、映射、方差、冲突、projector 误差和分裂可识别性的合成系统。

---

# 2. 当前随机投影理论与实验的逐项审判

## 2.1 理论部分

| 现有结论 | 审判 | 正确边界 |
|---|---|---|
| 固定公共向量在样本差分中抵消 | 正确 | 只适用于所有样本相同的固定平移；样本变化的 common nuisance 不会抵消 |
| 有界噪声使类间/类内距离出现可计算收缩 | 正确 | 距离 gap 是很强的充分条件，不是线性可分的必要条件 |
| 有限样本 JL 距离保持 | 正确 | 点集必须在抽取随机矩阵前固定；只保持已有几何 |
| 冻结正 margin Router 的随机投影保持 | 正确 | 需要原空间正最小 margin、随机矩阵独立、权重冻结；不保证低维重训能找到分类器 |
| 线性投影不能创造线性可分性 | 正确 | 逆方向不成立：原空间可分，投影后可能丢失判别方向 |
| 低维仿射子空间并集可统一嵌入 | 在给定假设下正确 | 几何维数不能用监督功能维数或 $r_{90}$ 替代 |
| 随机谱坐标抽样 | 在低相干假设下正确 | 高谱熵不推出低相干 |

### 2.1.1 最重要的逻辑位置修正

这些定理的逻辑位置应改为：

$$
\boxed{
\text{先生成正 margin 路由几何}
\rightarrow
\text{再用随机投影定理研究压缩保持}
}
$$

而不是：

$$
\text{随机投影}
\rightarrow
\text{期望自动出现可分性}.
$$

## 2.2 实验部分

### 2.2.1 支持的直接事实

现有实验在注册条件下得到：

- 31/48 层的 $R_U$ 对 $X$ 有正的受控条件增量效用；
- 最大值位于 Block 39；
- 冻结主层 Block 48 与重复层 Block 38 均未通过正低尾 margin 门槛；
- 四个 block--panel 单元的 $5\%$ margin 全为负；
- 极端与稳健 pairwise distance ratio 均小于 1；
- 因 H3 未通过，随机投影保持 H4 被条件跳过，而不是失败。

注册数值为：

| Block | 角色 | 受控增量效用 | TEST-ID balanced accuracy | TEST-OOD balanced accuracy | TEST-ID $\Gamma_{0.05}$ | TEST-OOD $\Gamma_{0.05}$ |
|---:|---|---:|---:|---:|---:|---:|
| 39 | 最大净增量层 | $0.10994\ [0.09872,0.12080]$ | 非冻结确认层 | 非冻结确认层 | DEV 为 $-0.54060$ | 非冻结确认层 |
| 48 | 冻结主层 | $0.01369\ [0.00248,0.02456]$ | $0.17125\ [0.16484,0.17813]$ | $0.12969\ [0.12445,0.13500]$ | $-5.82955\ [-5.95216,-5.74825]$ | $-11.19046\ [-11.40759,-11.06038]$ |
| 38 | 冻结重复层 | $0.06442\ [0.05320,0.07529]$ | $0.31016\ [0.30203,0.31805]$ | $0.23125\ [0.22429,0.23859]$ | $-3.52356\ [-3.59236,-3.46685]$ | $-6.66276\ [-6.79532,-6.54119]$ |

Block 48 的 H2 因新模板 balanced-accuracy 区间下界 $0.12445\le0.125$ 而失败；Block 38 的 H2 通过，但两层的 H3 均失败。四个极端距离比为 $0.3321,0.2027,0.2314,0.2205$，稳健距离比为 $0.7026,0.5315,0.5832,0.5357$，全部低于 1。距离结果与“没有形成独立类别簇 gap”一致，但距离 gap 不是线性可分的必要条件。

数据机器守卫已通过，AI 复核为 52 条 `PASS`、12 条 `PASS_WITH_NOTE`、零明确类别/算术错误；外部独立人工 64 条复核未完成，因此 H1 总体仍为 `Insufficient`。

### 2.2.2 不能推出的结论

一次 L2 逻辑回归探针失败只能说明：

> 在给定数据、训练划分、正则网格、优化器、探针族和统计功效下，没有发现注册的稳健线性结构。

并且本次对象是独立 $R_U$。若要建立“完整高维隐藏状态没有稳健 margin”，必须对 $X$、$R_U$ 与联合 $(X,R_U)$ 使用同一冻结规则做直接比较；现有 H0 的“加入 $R_U$ 后有条件增量效用”反而说明联合对象与独立 residual 不能混为一谈。

它不能证明全称命题：

$$
\nexists\,W,b\quad\text{使真实分布线性可分}.
$$

### 2.2.3 Margin 的后续改进

现有实验使用 true-label logit margin：

$$
\gamma_i=s_{y_i}(h_i)-\max_{k\ne y_i}s_k(h_i).
$$

其符号与分类正确性一致，但数值会随分类器权重尺度变化。跨模型比较应改为归一化几何 margin：

$$
\bar\gamma_i
=
\min_{k\ne y_i}
\frac{(w_{y_i}-w_k)^\top h_i+b_{y_i}-b_k}
{\|w_{y_i}-w_k\|_2}.
$$

它表示样本到最近错误决策超平面的有符号欧氏距离，更适合比较 Dense、Flat MoE 和 Tree 表征。

---

# 3. 导师脑海中已经固定与尚未固定的内容

## 3.1 组会前导师主要相信的内容

1. 大模型/专家在训练中倾向于学习低秩功能；
2. common 模式先稳定，specialized 模式更晚、更难；
3. specialized experts 的意义是隔离互相冲突的条件映射，而非单纯扩大单 expert 的 rank；
4. 可递归地冻结已有 expert，再增加新 expert；
5. 新 expert 不应沿祖先已占用方向继续更新；
6. 初始化差异或低维中心可能提供早期对称性破缺。

## 3.2 组会结束后已经固定的认识

### 固定认识 A：旧实验操作错了对象

不能直接用 common expert 输出做下一层路由；应使用 common expert **不能解释的 residual variation**。

### 固定认识 B：高维不自动意味着可分

维数升高只提供函数空间容量。若映射没有保留或展开细分支信息，或者训练只强化公共模式，高维表示仍可能没有稳定测试 margin。

### 固定认识 C：树结构必须服务于冲突分解

增加专家的核心理由必须是不同分支需要不同条件函数；若所有数据可由同一函数处理，则树结构没有必要。

### 固定认识 D：旧方向应被保护

祖先已学公共功能必须被保留；新专家应处理其补空间中的剩余功能，不能通过重复学习祖先方向来获得表面增益。

### 固定认识 E：必须同时设计成功与失败数据

合成数据必须包含理论必然成功、理论必然失败和容易混淆的条件，不能只构造一个正向 benchmark。

## 3.3 组会后仍未固定、必须由新理论和实验决定的内容

1. $C$ 应由祖先参数列空间、祖先输出空间、Jacobian 空间还是数据 PCA 定义；
2. 无标签 split 应使用 PCA、聚类、专家效用差、梯度冲突还是其他信号；
3. NTP 本身是否足以使 residual branch 自发分开；
4. 是否必须加入显式局部 margin/对比目标；
5. Tree 是否优于参数与计算严格匹配的 Dense/Flat MoE；
6. 自然语义是否满足“当前分支信号是 residual covariance 最大 spike”的 PCA 条件；
7. Qwen 的 $R_U$ 是否存在可递归恢复的层次结构。

因此，小 paper 必须把上述未定事项写成假设、竞争解释和失败分支，不能写成导师已经确认的事实。

---

# 4. 确定的 Next Meeting Problem

## 4.1 唯一核心问题

> **在一个潜在语义维数远小于隐藏维数、且具有二叉层次功能冲突的可控模型中，标准线性抬升为什么不能自动改善线性可分性；样本变化的高维公共 nuisance 和 common-first 训练为什么会阻碍有限样本 learner 获得稳定 margin；当 residual split 可识别时，分支条件的非线性 residual expert 更新与祖先输出保护能否生成正的局部及全局线性 margin？**

## 4.2 当前判断

当前最可信的判断是：

- 现有 $R_U$ 中“信息存在”与“独立正 margin 几何存在”是不同命题；
- 单纯线性投影只能保持或破坏已有结构，不能生成结构；
- residualization 的非平凡价值只能是降低 nuisance 维数、改善有限样本学习、提供更好的 split 坐标和阻止重复学习；
- 真正把负低尾 margin 变为正 margin 的步骤必须包含**分支条件非线性**或**显式几何生成目标**，而不能只是一个固定线性投影。

## 4.3 最强竞争解释

> 完整表示本来包含足够线性信息；现有失败只来自探针样本量、正则、尺度、数据构造或优化。只要使用相同训练课程和足够容量的 Dense/Flat MoE，也会得到同样的正 margin；residual tree 并非必要机制。

## 4.4 恰好一个下一决策

> **是否把“可识别 residual split + 分支条件低秩更新 + 祖先 logits 零干扰”冻结为正式的几何生成机制，并授权一层 Transformer 的无标签合成实验？**

完成标准不是“跑出一张正向图”，而是：

1. 下文定理 1--9 在同一套定义下自洽；
2. PCA split 的成功条件与反例均有严格证明；
3. 专家必要性由功能冲突风险而非参数量解释；
4. 抗遗忘由输出零空间给出精确保证；
5. 每个假设均映射到可控制的 synthetic 参数和一个可观测量。

---

# 5. 统一数学模型

## 5.1 潜在层次语义

令一条样本对应深度为 $L$ 的二叉路径

$$
b=(b_1,\ldots,b_L)\in\{-1,+1\}^L.
$$

当 $L=6$ 时共有 $2^6=64$ 个叶类：前 3 位表示 8 个粗类，后 3 位表示每个粗类中的 8 个细类。

潜在语义维数仅为 $r_{\mathrm{sem}}=L$，远小于隐藏维数 $d$。

## 5.2 高维表示分解

在树节点 $v$ 上，设样本已经被祖先正确送达。当前表示写为

$$
h_v
=
U_Cc_v
+
\alpha_v b_v u_v
+
\sum_{w\succ v}\alpha_w b_wu_w
+
U_Nn_v,
$$

其中：

- $C_v=\operatorname{span}(U_C)$ 是祖先已解释的公共/保护子空间；
- $c_v$ 是样本变化的 common-style nuisance，而不是所有样本相同的固定平移；
- $u_v\in C_v^\perp$ 是当前二分支方向；
- $w\succ v$ 表示后代方向；
- $U_Nn_v$ 是与当前分支无关的 nuisance；
- $d\gg L$ 只表示环境维数大，不自动表示 $b_v$ 可被稳定线性恢复。

真实 residual 为

$$
r_v=(I-P_{C_v})(h_v-\mathbb E[h_v\mid v]).
$$

## 5.3 低秩 expert

每个 expert 使用真正的瓶颈形式

$$
E_v(h)=B_v\phi(A_vh),
$$

其中

$$
A_v\in\mathbb R^{r_e\times d},
\qquad
B_v\in\mathbb R^{d\times r_e},
\qquad
r_e\ll d.
$$

其局部 Jacobian 为

$$
J_v(h)=B_vD_\phi(A_vh)A_v,
$$

因此

$$
\operatorname{rank}J_v(h)\le r_e.
$$

这才是本文所说的低秩 expert。使用 $d_{\mathrm{mid}}=4d$ 的标准扩张 FFN 不满足该低秩定义。

## 5.4 功能冲突对象

为了区分“可分类”与“专家有功能收益”，引入 payload $q$ 和分支条件目标函数

$$
t=M_{b_v}q,
$$

其中 $M_{+}$ 与 $M_{-}$ 分别是两个分支需要的低秩映射。若 $M_+\ne M_-$，单个共享 expert 必须在两个条件函数之间折中；正确路由的两个 experts 可以分别实现二者。

---

# 6. 完整理论证明

## 定理 1：满列秩线性抬升严格保持线性可分性

### 陈述

令潜在变量 $z\in\mathbb R^r$，高维表示为

$$
h=Az+c,
$$

其中 $A\in\mathbb R^{d\times r}$ 满列秩，$c\in\mathbb R^d$ 固定。对任意多类标签映射，$z$ 上存在仿射线性分类器当且仅当 $h$ 上存在仿射线性分类器。

### 证明

若潜在空间存在分数

$$
s_k(z)=v_k^\top z+a_k,
$$

令

$$
w_k=A(A^\top A)^{-1}v_k,
\qquad
b_k=a_k-w_k^\top c.
$$

则

$$
w_k^\top h+b_k
=
 v_k^\top(A^\top A)^{-1}A^\top A z+a_k
=
 v_k^\top z+a_k.
$$

所以潜在空间的每个线性决策都能在高维像空间中完全复现。

反过来，若高维空间存在

$$
s_k(h)=w_k^\top h+b_k,
$$

代入 $h=Az+c$ 得

$$
s_k(h)
=(A^\top w_k)^\top z+(w_k^\top c+b_k),
$$

它本身就是潜在空间中的仿射线性分类器。证毕。

### 推论

单纯把低维语义通过一个无噪声、单射的线性映射放入更高维空间，**既不会改善，也不会恶化其线性可分性**。如果高维实验变差，至少有一项不成立：

- 映射不是单射；
- 映射是非线性的并发生折叠；
- 观测含样本变化 nuisance/噪声；
- 语义标签本来不是潜在空间中的线性函数；
- 有限样本 learner 没有找到存在的判别方向；
- 训练目标没有要求该方向形成稳定 margin。

---

## 定理 2：任意线性降维不能创造原空间不存在的线性可分性

### 陈述

令投影表示为 $z=Ah$。若 $z$ 上存在多类线性 Router

$$
s'(z)=W'z+b'
$$

正确实现给定标签映射，则原表示 $h$ 上也存在多类线性 Router 正确实现同一映射。

### 证明

复合分数为

$$
s'(Ah)=W'Ah+b'.
$$

令

$$
W=W'A,
\qquad b=b',
$$

则 $Wh+b$ 与投影空间分数逐样本完全相同，因此 argmax 决策也完全相同。证毕。

### 研究含义

该定理证明现有随机投影 proof 的核心否定结论是正确的。它只否定“线性投影创造结构”，不否定下文的**分支条件非线性映射**可以生成新几何。

一个最小反例是异或关系。令 $z_1,z_2\in\{-1,+1\}$，标签 $y=z_1z_2$。正类两点与负类两点的凸包都包含原点，因此在原二维空间中不存在严格仿射分隔超平面；加入交互特征

$$
\phi(z)=(z_1,z_2,z_1z_2)
$$

后，只需读取第三坐标即可线性分类。真正起作用的是**与任务相关的非线性交互项**，不是 ambient dimension 本身。Tree 的分支条件 expert 正是要学习这类条件化特征展开。

---

## 定理 3：高维无关 nuisance 增加有限样本判别方向估计误差

### 假设

考虑平衡二分类：

$$
y\in\{-1,+1\},
\qquad
h=y\mu+c+\varepsilon,
$$

其中

$$
\mu\in C^\perp,
\quad
c\sim\mathcal N(0,\tau_C^2P_C),
\quad
\varepsilon\sim\mathcal N(0,\sigma^2I_d),
$$

且三者独立。令 $r_C=\dim C$。

用 $n$ 个带标签样本估计均值差方向：

$$
\widehat\mu_h=\frac1n\sum_{i=1}^ny_ih_i.
$$

### 结论 1：完整状态估计误差

有

$$
\widehat\mu_h
\sim
\mathcal N\!\left(
\mu,
\frac{\tau_C^2P_C+\sigma^2I_d}{n}
\right),
$$

从而

$$
\boxed{
\mathbb E\|\widehat\mu_h-\mu\|_2^2
=
\frac{\tau_C^2r_C+\sigma^2d}{n}
}.
$$

### 证明

因为 $y_i^2=1$ 且 $y_i$ 与 $c_i,\varepsilon_i$ 独立，

$$
\widehat\mu_h-
\mu
=
\frac1n\sum_{i=1}^ny_i(c_i+\varepsilon_i).
$$

每项均值为零，协方差为 $\tau_C^2P_C+\sigma^2I_d$；独立平均后协方差除以 $n$。高斯向量平方范数期望等于协方差迹，因此得到结论。

### 结论 2：真实 residual 的估计误差

令

$$
r=(I-P_C)h=y\mu+(I-P_C)\varepsilon
$$

以及

$$
\widehat\mu_r
=
\frac1n\sum_{i=1}^ny_ir_i.
$$

则

$$
\boxed{
\mathbb E\|\widehat\mu_r-\mu\|_2^2
=
\frac{\sigma^2(d-r_C)}{n}
}.
$$

若进一步知道 specialized 信号位于 $r_S$ 维子空间 $S\subset C^\perp$，并使用 $P_Sr$，则

$$
\boxed{
\mathbb E\|\widehat\mu_S-\mu\|_2^2
=
\frac{\sigma^2r_S}{n}
}.
$$

### 结论 3：一个完全显式的样本量充分条件

设估计误差 $e=\widehat\mu-\mu$，协方差迹为 $V/n$，并取 $0<a<1$。由 Markov 不等式，

$$
\Pr\left(\|e\|_2>a\|\mu\|_2\right)
\le
\frac{V}{na^2\|\mu\|_2^2}.
$$

因此若

$$
n\ge
\frac{V}{\delta a^2\|\mu\|_2^2},
$$

则以至少 $1-\delta$ 的概率，$\|e\|\le a\|\mu\|$。

此时

$$
\frac{\widehat\mu^\top\mu}
{\|\widehat\mu\|_2}
\ge
\frac{1-a}{1+a}\|\mu\|_2.
$$

证明为

$$
\widehat\mu^\top\mu
\ge
\|\mu\|^2-\|e\|\|\mu\|
\ge
(1-a)\|\mu\|^2,
$$

以及

$$
\|\widehat\mu\|
\le
(1+a)\|\mu\|.
$$

### 结论 4：测试低尾 margin

在 residual 测试分布

$$
r=y\mu+\varepsilon_\perp,
\qquad
\varepsilon_\perp\sim\mathcal N(0,\sigma^2P_{C^\perp})
$$

上，固定非零 $w\in C^\perp$ 的归一化 margin

$$
M=\frac{yw^\top r}{\|w\|}
$$

服从

$$
M\mid w
\sim
\mathcal N\!\left(
\frac{w^\top\mu}{\|w\|},
\sigma^2
\right).
$$

因此

$$
Q_{0.05}(M\mid w)
=
\frac{w^\top\mu}{\|w\|}
-z_{0.95}\sigma,
$$

其中 $z_{0.95}\approx1.645$。结合上面的角度界，一个充分条件是

$$
\frac{1-a}{1+a}\|\mu\|
>
1.645\sigma.
$$

### 解释

完整状态并不缺少 $\mu$。它的问题是有限样本估计量会在 $r_C$ 个高方差、与标签无关的方向上产生随机分量。residualization 删除了

$$
\frac{\tau_C^2r_C}{n}
$$

这一项；若还知道 specialized 候选空间，则把维数项从 $d$ 压到 $r_S$。

这证明的是**样本复杂度与估计方差优势**，不是信息创造。在该固定维数、高斯模型和一致估计器下，随着 $n\to\infty$，完整状态 learner 应当追平。

---

## 定理 4：residual PCA 分裂何时严格恢复真实分支

### 成功模型

在某个节点上，设 residual 为

$$
r=y\mu+\epsilon,
\qquad
y\in\{-1,+1\}\text{ 平衡},
\qquad
\epsilon\sim\mathcal N(0,\sigma^2I_q).
$$

记 $m=\|\mu\|$、$u=\mu/m$。

### 结论 1：总体 PCA

总体协方差为

$$
\Sigma=\mu\mu^\top+\sigma^2I_q.
$$

其第一特征向量为 $u$，第一特征值为 $m^2+\sigma^2$，其余特征值均为 $\sigma^2$，eigengap 为 $m^2$。

PCA 方向符号本身不可识别；为陈述错误率，选择与 $\mu$ 同向的符号。使用 gate

$$
\widehat y=\operatorname{sign}(u^\top r)
$$

时，错误率为

$$
\Pr(\widehat y\ne y)
=
\Phi\!\left(-\frac m\sigma\right),
$$

归一化 margin 的 $5\%$ 分位数为

$$
\boxed{
\Gamma_{0.05}=m-1.645\sigma
}.
$$

所以总体 PCA 获得正低尾 margin 的充要条件是

$$
m>1.645\sigma.
$$

### 证明

协方差分解直接给出特征结构。并且

$$
yu^\top r=m+yu^\top\epsilon
\sim\mathcal N(m,\sigma^2).
$$

因此错误率和分位数结论成立。

### 结论 2：有限样本协方差扰动

设训练协方差为

$$
\widehat\Sigma=\Sigma+E,
\qquad
\|E\|_{\mathrm{op}}\le\delta<\frac{m^2}{2},
$$

$\widehat u$ 是其第一单位特征向量，并选择符号使 $\widehat u^\top u\ge0$。则

$$
(\widehat u^\top u)^2
\ge
1-\frac{2\delta}{m^2}.
$$

### 证明

由 $\widehat u$ 的最大 Rayleigh 商性质，

$$
\widehat u^\top\widehat\Sigma\widehat u
\ge
u^\top\widehat\Sigma u.
$$

左侧满足

$$
\widehat u^\top\widehat\Sigma\widehat u
\le
\sigma^2+m^2(\widehat u^\top u)^2+\delta,
$$

右侧满足

$$
u^\top\widehat\Sigma u
\ge
\sigma^2+m^2-\delta.
$$

因此

$$
m^2(\widehat u^\top u)^2+\delta
\ge
m^2-\delta,
$$

即得结论。

于是有限样本 gate 的低尾 margin 下界为

$$
\Gamma_{0.05}
\ge
m\sqrt{1-\frac{2\delta}{m^2}}
-1.645\sigma.
$$

### 推论：公共子空间估计误差如何扰动 residual margin

令真实 residual 与估计 residual 分别为

$$
r=(I-P_C)(h-\mathbb E h),
\qquad
\widehat r=(I-\widehat P_C)(h-\mathbb E h).
$$

若

$$
\|\widehat P_C-P_C\|_{\mathrm{op}}\le\delta_C,
\qquad
\|h-\mathbb E h\|_2\le R,
$$

则

$$
\|\widehat r-r\|_2
\le
\delta_CR.
$$

因此，对任意单位法向量 $w$，归一化 margin 的逐样本扰动至多为 $\delta_CR$。若真实 residual 的 $5\%$ 低尾 margin 为 $\gamma_{0.05}>0$，且

$$
\delta_CR<\gamma_{0.05},
$$

则估计 residual 的对应低尾 margin 仍为正。该结论解释了实验中为什么必须扫描 projector 误差；它不保证 PCA 方向本身可识别。

### 必须注册的失败反例：最大方差是 nuisance

令

$$
r=y\mu+\eta q+\epsilon,
$$

其中 $q$ 是与 $\mu$ 正交的单位向量，$\eta\sim\mathcal N(0,\tau^2)$，且 $\eta,y,\epsilon$ 相互独立。协方差在 $u$ 和 $q$ 方向的特征值分别为

$$
\sigma^2+m^2,
\qquad
\sigma^2+\tau^2.
$$

若

$$
\tau^2>m^2,
$$

第一主成分为 $q$，且 $q^\top r$ 与 $y$ 独立。任何按第一主成分符号得到的 split 对真实分支的错误率为 $1/2$。

### 结论

“PCA split 能发现语义”不是一般事实。它只有在**当前分支信号是 residual covariance 中可识别的最大 spike**时成立。该条件必须作为实验入场门，而不能事后解释。

---

## 定理 5：common 模式在二次近似训练中被更快学习

### 模型

令训练目标在局部线性化后为

$$
\mathcal L(\theta)
=
\frac12(\theta-\theta^*)^\top
H(\theta-\theta^*),
$$

其中

$$
H=\lambda_CP_C+\lambda_SP_S,
\qquad
\lambda_C>\lambda_S>0,
\qquad
P_CP_S=0.
$$

$C$ 表示高频 common 模式，$S$ 表示低频 specialized 模式。梯度下降为

$$
\theta_{t+1}=\theta_t-\eta H(\theta_t-\theta^*),
$$

并假设 $0<\eta\le 1/\lambda_C$。该更强条件保证两个收缩因子均非负，且 common 模式的收缩因子严格更小。

### 结论

误差在两个子空间中分别为

$$
P_C(\theta_t-\theta^*)
=(1-\eta\lambda_C)^tP_C(\theta_0-\theta^*),
$$

$$
P_S(\theta_t-\theta^*)
=(1-\eta\lambda_S)^tP_S(\theta_0-\theta^*).
$$

由于 $0\le1-\eta\lambda_C<1-\eta\lambda_S<1$，common 模式误差收缩更快，因而在该二次模型中先被学习。

### 证明

由 $P_C,P_S$ 正交且与 $H$ 对易，分别对更新式左乘两个投影即可得到一阶线性递推，归纳即得。

### 边界

该定理只证明二次/线性化模型中的谱偏置。它不证明真实 NTP 的 Hessian 必然满足上述分解，也不证明表示一定低秩。合成实验必须直接测量 common 与 specialized 梯度协方差或学习曲线，而不能把该 intuition 当作已知事实。

---

## 定理 6：为什么存在功能冲突时需要 specialized experts

### 模型

令 payload $q$ 满足 $\mathbb E[q]=0$，且

$$
\operatorname{Cov}(q)=\Sigma_q,
\qquad
\Sigma_q\succeq0.
$$

分支 $y\in\{-1,+1\}$ 平衡且与 $q$ 独立。目标为

$$
t=M_yq,
$$

其中

$$
M_y=\overline M+\frac y2\Delta,
\quad
\overline M=\frac{M_++M_-}{2},
\quad
\Delta=M_+-M_-.
$$

共享线性 expert 使用同一个 $Wq$，风险为

$$
R_{\mathrm{shared}}(W)
=
\mathbb E\|Wq-M_yq\|_2^2.
$$

### 结论 1：单共享 expert 的不可消除风险

有

$$
R_{\mathrm{shared}}(W)
=
\operatorname{tr}
\bigl[(W-\overline M)\Sigma_q(W-\overline M)^\top\bigr]
+
\frac14\operatorname{tr}(\Delta\Sigma_q\Delta^\top).
$$

因此 $W^*=\overline M$ 是一个最优共享 expert（当 $\Sigma_q$ 奇异时最优解可不唯一），最小风险为

$$
\boxed{
R_{\mathrm{shared}}^*
=
\frac14D,
\qquad
D:=\operatorname{tr}(\Delta\Sigma_q\Delta^\top)
}.
$$

### 证明

代入 $M_y$：

$$
Wq-M_yq
=(W-\overline M)q-\frac y2\Delta q.
$$

平方展开后，交叉项因 $\mathbb E[y]=0$ 且 $y\perp q$ 消失，得到分解。第一项在 $W=\overline M$ 处取零。

### 结论 2：正确路由的两个 experts

令两个 experts 分别取 $W_+=M_+$、$W_-=M_-$。若 gate 完全正确，则风险为 0。

对一般 gate，令错误指示为 $I_{\mathrm{err}}$。此时精确风险为

$$
R_{\mathrm{MoE}}
=
\mathbb E\left[
I_{\mathrm{err}}\,\|\Delta q\|_2^2
\right].
$$

定义按功能冲突幅度加权的路由错误率

$$
\eta_D
=
\frac{
\mathbb E[I_{\mathrm{err}}\|\Delta q\|_2^2]
}{D}.
$$

则

$$
R_{\mathrm{MoE}}=\eta_DD.
$$

若错误事件与 $q$ 独立且普通错误率为 $\eta$，则 $\eta_D=\eta$。所以相对于最优共享线性 expert，两个 experts 的功能收益条件为

$$
\boxed{\eta_D<\frac14}.
$$

### 研究含义

- $D>0$ 才表示存在真实功能冲突；
- $D=0$ 时增加专家没有理论必要性；
- 仅有高 gate purity 但 $D\approx0$，不能声称 expert specialization 有功能价值；
- oracle gate 也不能降低损失时，问题在数据没有冲突，而不是 gate 没学好。

---

## 定理 7：同时保证“不读取 common”与“不改变祖先 logits”的正确约束

### 定义

令 $C$ 是祖先已占用输入子空间。令所有需要保护的祖先线性读出堆叠为

$$
W_A\in\mathbb R^{m_A\times d}.
$$

定义其零空间正交投影

$$
P_K
=
I-W_A^\top(W_AW_A^\top)^\dagger W_A,
$$

则

$$
\operatorname{range}(P_K)=\ker W_A,
\qquad
W_AP_K=0.
$$

定义新 expert：

$$
\boxed{
\delta(h)
=
P_KB\phi\bigl(A(I-P_C)h\bigr)
}.
$$

### 结论 1：不重新读取 common

对任意 $c\in C$，

$$
\delta(h+c)=\delta(h).
$$

### 证明

因为 $(I-P_C)c=0$。

### 结论 2：祖先 logits 精确不变

令最终状态 $h'=h+\delta(h)$，则

$$
W_Ah'=W_Ah.
$$

### 证明

$$
W_Ah'
=W_Ah+W_AP_KB\phi(\cdot)
=W_Ah.
$$

上述精确不变性只覆盖直接作用于 $h$ 的冻结线性读出。若祖先决策还经过 RMSNorm、LayerNorm、注意力或其他非线性模块，则必须保护复合函数的 Jacobian/输出，而不能把本定理升级为完整语言模型功能零遗忘。

### 结论 3：原计划梯度投影为什么不够

原约束

$$
A_{t+1}=A_t-\eta G_t(I-P_C)
$$

在初始化满足 $A_0P_C=0$ 时，只能保证后续 $A_tP_C=0$，因为

$$
A_{t+1}P_C
=A_tP_C-\eta G_t(I-P_C)P_C
=A_tP_C.
$$

这只说明输入侧不读取 $C$，不能推出

$$
W_A\delta(h)=0.
$$

因此不能推出 $\Delta\mathrm{Acc}_{\mathrm{coarse}}=0$。要获得严格抗遗忘，必须同时施加输出零空间投影 $P_K$，或者将粗任务永远只在冻结的祖先状态上评估；后者只是旁路保留，不是最终表示上的不遗忘。

### 近似投影的鲁棒性

若使用近似 $\widehat P_K$，满足

$$
\|W_A\widehat P_K\|_{\mathrm{op}}\le\epsilon_K,
\qquad
\|B\phi(\cdot)\|\le M,
$$

则单个祖先 logit 向量漂移至多为

$$
\|W_A\delta\|\le\epsilon_KM.
$$

任意两类祖先 margin 至多下降 $2\epsilon_KM$。若原祖先最小 margin 大于该值，预测保持。

---

## 定理 8：分支条件 residual 更新可以把低尾 margin 从负变正

### 模型

在一个节点，设 residual 为

$$
r=y\mu u+\epsilon,
$$

其中 $u$ 为单位方向、$y\in\{-1,+1\}$、$\mu>0$。为同时满足定理 7 的祖先保护，先假设

$$
u\in C^\perp\cap\ker W_A.
$$

令 gate 输出 $\widehat y\in\{-1,+1\}$，两个 child experts 实现分支条件增量

$$
\delta_{\widehat y}=a\widehat y\,u,
\qquad a>0,
$$

最终表示为

$$
z=r+\delta_{\widehat y}.
$$

### Oracle/正确路由结论

在 $\widehat y=y$ 的样本上，若 $u^\top\epsilon\sim\mathcal N(0,\sigma^2)$，则沿 $u$ 的归一化正确类 margin 为

$$
M=yu^\top z
=\mu+a+yu^\top\epsilon,
$$

所以

$$
\boxed{
Q_{0.05}(M)=\mu+a-1.645\sigma
}.
$$

即使基础 residual 满足

$$
\mu-1.645\sigma\le0,
$$

只要

$$
a>1.645\sigma-\mu,
$$

正确分支上的条件更新也能使低尾 margin 转正。

### 与祖先保护的兼容条件

若原始分支方向 $u$ 不完全位于 $\ker W_A$，只能沿

$$
\widetilde u
=
\frac{P_Ku}{\|P_Ku\|_2}
$$

进行受保护更新。有效可用信号按 $\|P_Ku\|_2$ 缩放；当 $P_Ku=0$ 时，不存在既沿该方向分离又严格保持祖先线性 logits 的更新。这是 Tree 机制的必要兼容性门，而不是实现细节。

### 为什么不与定理 2 矛盾

整体映射为

$$
r\mapsto r+a\,\widehat y(r)u,
$$

其中 $\widehat y(r)$ 由 gate 决定，因此是分支条件的分段仿射映射，不是固定线性投影。定理 2 只禁止线性映射创造线性可分性，不禁止条件非线性映射重新组织几何。

### Gate 错误边界

对误路由样本，增量方向反向，margin 变为

$$
M_{\mathrm{wrong}}
=\mu-a+yu^\top\epsilon.
$$

因此总体 $5\%$ 分位数取决于错误比例及错误样本的幅度分布。特别地，若误路由比例达到或超过 $5\%$，低尾分位数可能主要由误路由样本决定；即使错误率低于 $5\%$，仍需在正确路由子集上保留足够条件 margin。实验必须同时测 gate 错误率、条件 margin 和总体 margin，不能只报告平均准确率。

---

## 定理 9：正交层次 code 可以形成全局线性可分的叶类

### 模型

令 $u_1,\ldots,u_L$ 两两正交，叶路径 $b\in\{-1,+1\}^L$ 的无噪声中心为

$$
\nu_b=\sum_{t=1}^La_tb_tu_t,
\qquad a_t>0.
$$

观测为

$$
z=\nu_b+\epsilon.
$$

定义多类线性分数

$$
s_b(z)=\nu_b^\top z-\frac12\|\nu_b\|^2.
$$

### 结论

所有中心具有相同范数。对任意错误叶 $b'\ne b$，

$$
s_b(z)-s_{b'}(z)
=
\frac12\|\nu_b-\nu_{b'}\|^2
+(\nu_b-\nu_{b'})^\top\epsilon.
$$

若对所有 $b'\ne b$ 有

$$
|(\nu_b-\nu_{b'})^\top\epsilon|
<
\frac12\|\nu_b-\nu_{b'}\|^2,
$$

则叶类被上述线性分类器正确分类。

### 证明

由于所有 $\|\nu_b\|^2=\sum_ta_t^2$，

$$
\begin{aligned}
s_b-s_{b'}
&=(\nu_b-\nu_{b'})^\top(\nu_b+\epsilon)\\
&=\nu_b^\top\nu_b-\nu_{b'}^\top\nu_b
 +(\nu_b-\nu_{b'})^\top\epsilon\\
&=\frac12\|\nu_b-\nu_{b'}\|^2
 +(\nu_b-\nu_{b'})^\top\epsilon.
\end{aligned}
$$

条件保证其为正。

### 递归路由误差

若深度 $t$ 的 gate 在祖先正确条件下错误率为 $\eta_t$，则整条路径错误率满足

$$
\Pr(\text{path error})
\le
\sum_{t=1}^L\eta_t.
$$

这是并合界。若每个后代更新都使用包含全部祖先节点线性读出的 $W_A$ 构造 $P_K$，定理 7 才保证后代更新不会改变已形成的祖先线性决策。

---

# 7. 理论结论的精确边界

## 7.1 已严格证明

1. 无噪声满列秩线性抬升不改变线性可分性；
2. 线性降维不能创造原空间不存在的线性可分性；
3. 样本变化的高维 common nuisance 增加有限样本判别方向的估计方差；
4. residualization 在注册高斯模型中删除可计算的 nuisance 维数项；
5. PCA split 在 spiked residual mixture 下恢复分支，在 nuisance spike 更大时必然失败；
6. 条件函数冲突为 specialized experts 提供非容量型必要性；
7. 输入补空间加输出零空间约束精确保护祖先读出；
8. 正确 gate 后的分支条件非线性 residual 更新可以把低尾 margin 推正；
9. 正交层次 codebook 可以使 $2^L$ 个叶类由全局线性分类器分开。

## 7.2 尚未证明

1. 真实 NTP 必然产生定理 5 的 common/specialized Hessian 分解；
2. Qwen 表征中的真实语义满足 PCA spike 条件；
3. 无标签 PCA split 与真实专家效用分支一致；
4. AdamW 能在低秩 GELU expert 中找到定理 8 的理想更新；
5. 自然语言具有正交层次 code；
6. Tree 一定优于参数与计算匹配的 Dense/Flat MoE；
7. 现有 8×8 语义标签就是真实最优专家分工。

这些只能由下述实验逐项检验。

---

# 8. 更新后的方法：Protected Residual Hierarchical Expert Tree

## 8.1 祖先占用子空间

**AI_PROPOSAL（待实验比较）：**对于每个低秩 expert

$$
E_a(h)=B_a\phi(A_ah),
$$

其输出始终位于 $\operatorname{col}(B_a)$。节点 $v$ 的祖先占用子空间定义为

$$
C_v
=
\operatorname{span}\{\operatorname{col}(B_a):a\in\operatorname{Anc}(v)\}.
$$

实验中仅用 TRAIN 上冻结参数构造其正交基 $Q_{C_v}$，并令

$$
P_{C_v}=Q_{C_v}Q_{C_v}^\top.
$$

这一定义比“根输出 PCA 前若干维”更直接地对应“祖先参数已经能够写入的低秩方向”，但它仍只是一个可检验的 operationalization；实验必须与祖先 Jacobian 空间、输出样本子空间和 oracle $C_v$ 对照。

## 8.2 正确的 split 输入

对送达节点 $v$ 的 TRAIN 表示 $h_i$，先减去节点 TRAIN 均值，再删除祖先占用子空间：

$$
r_{v,i}
=(I-P_{C_v})(h_i-\bar h_v).
$$

不能在 $P_{C_v}h_i$ 或祖先 expert 输出上寻找下一层分支。

## 8.3 无标签候选 split

计算

$$
\widehat\Sigma_v
=
\frac1{N_v-1}\sum_i r_{v,i}r_{v,i}^\top.
$$

取第一特征向量 $u_v$，将标量

$$
z_i=u_v^\top r_{v,i}
$$

用一维 two-means 得到阈值 $t_v$，并定义

$$
\widehat b_{v,i}
=\operatorname{sign}(z_i-t_v).
$$

必须通过以下无标签 split guards 才允许生长：

1. eigengap ratio
   $$
   g_v=\frac{\lambda_1-\lambda_2}{\max(\lambda_1,10^{-12})}
   $$
   达到冻结阈值；
2. 两个子节点样本比例均在 $[0.3,0.7]$；
3. 对 TRAIN bootstrap 重算时，第一方向投影重合和 split 一致率稳定；
4. 不是已注册的高方差 style 控制方向。

语义标签只在最终评估 gate purity 时打开，不能参与 $u_v,t_v$ 的选择。

## 8.4 子 expert

令 $W_{A,v}$ 堆叠所有祖先任务/节点读出的 pairwise logit-difference 行向量，构造

$$
P_{K_v}
=
I-W_{A,v}^\top(W_{A,v}W_{A,v}^\top)^\dagger W_{A,v}.
$$

子 expert 为

$$
\delta_{v,b}(h)
=
P_{K_v}B_{v,b}\phi\left(A_{v,b}r_v(h)\right).
$$

最终状态递归为

$$
h_{t+1}
=
h_t+
\delta_{v_t,\widehat b_{v_t}}(h_t).
$$

祖先 expert、祖先 gate、共享 trunk 在新阶段冻结。

## 8.5 两个训练版本

### 版本 T1：Tree-NTP

只用分支内的下一词元损失训练新 child experts：

$$
\mathcal L_{\mathrm{T1}}
=
\mathcal L_{\mathrm{NTP}}.
$$

它最接近导师的自发学习 intuition，但没有理论保证 margin 会增大。

### 版本 T2：Tree-NTP + pseudo-margin

在不使用真实语义标签的前提下，固定 PCA split 的单位法向量 $u_v$ 与阈值 $t_v$，使用其 pseudo-label $\widehat b$ 加入局部几何 margin：

$$
\mathcal L_{\mathrm{sep}}
=
\frac1{N_v}
\sum_i
\left[
 m_0-
\widehat b_{v,i}
\bigl(u_v^\top r_{v,i}^{\mathrm{after}}-t_v\bigr)
\right]_+.
$$

这里 $u_v,t_v,\widehat b$ 在 child 训练前冻结，避免额外可学习分类头单独吸收目标；梯度只能通过 child update 改变表示。若 $P_{K_v}u_v=0$，该节点记为 `PROTECTION_CONFLICT`，不得强制优化该 margin。

总目标为

$$
\mathcal L_{\mathrm{T2}}
=
\mathcal L_{\mathrm{NTP}}
+\lambda_{\mathrm{sep}}\mathcal L_{\mathrm{sep}}.
$$

T2 明确承担“几何生成”角色。若 T1 失败而 T2 成功，正确结论是：树结构与 NTP 本身不足，需要直接的局部分离目标。

---

# 9. 精确合成数据设计

实验分为两个必要层次：

1. **E1：向量生成模型。**直接检验所有定理、阈值和反例；
2. **E2：一层 Transformer 语言建模。**检验 common-first 训练与无标签树生长是否在实际优化中出现。

冻结 Qwen $R_U$ 的 19,200 条数据被降级为后续桥接实验 E3，不能替代 E1/E2。

## 9.1 E1：Theorem-aligned Vector Tree Benchmark

### 9.1.1 叶类与划分

- 树深：$L=6$；
- 叶类：64；
- 每叶 300 条；
- 总计：19,200 条；
- TRAIN：每叶 180，共 11,520；
- DEV：每叶 40，共 2,560；
- TEST-ID：每叶 40，共 2,560；
- TEST-OOD：每叶 40，共 2,560。

独立单位是一个 latent seed；同一 seed 的语义路径、payload、噪声实例不能跨划分。

### 9.1.2 表示生成

主设置：

- ambient dimension $d=256$；
- common dimension $r_C=16$；
- hierarchy directions 6；
- payload dimension $p=16$；
- expert bottleneck $r_e=8$。

首先抽取互相正交的固定基

$$
U_C\in\mathbb R^{d\times r_C},
\qquad
U_Q\in\mathbb R^{d\times p},
\qquad
u_1,\ldots,u_6,
\qquad
U_N,
$$

其中 $U_N$ 补齐剩余维数。生成 payload

$$
q\sim\mathcal N(0,I_p)
$$

并令

$$
h
=
U_Cc
+
\kappa_qU_Qq
+
\sum_{t=1}^6\alpha_tb_tu_t
+
U_Nn.
$$

$U_Qq$ 使 expert 实际能够读取功能 payload；若不把 $q$ 放入输入，定理 6 的功能目标不可学习。主值取 $\kappa_q=0.5$。

主成功设置使用递减信号

$$
(\alpha_1,\ldots,\alpha_6)
=(2.4,2.0,1.7,1.4,1.2,1.0),
$$

使在正确祖先节点内，当前 bit 的协方差 spike 大于后代 bit、payload 单方向方差和各向同性噪声。

$$
c\sim\mathcal N(0,\tau_C^2I_{r_C}),
\qquad
n\sim\mathcal N(0,\sigma^2I),
$$

主值为 $\tau_C=3$、$\sigma=0.5$。oracle common projector 使用 $\operatorname{span}(U_C)$；learned projector 使用祖先 expert 的注册 operationalization，两者必须分别报告。

### 9.1.3 功能目标

令输出维数为 $p$。每个内部节点 $v$ 抽取两个 rank-$r_e$ 线性映射

$$
M_{v,+},M_{v,-}\in\mathbb R^{p\times p},
$$

并固定一个 common 映射 $M_0$。叶路径的目标为

$$
t
=
M_0q+
\sum_{v\in\operatorname{path}(b)}
\beta_vM_{v,b_v}q+
\zeta,
$$

其中 $\zeta\sim\mathcal N(0,\sigma_t^2I_p)$。冲突强度定义为

$$
D_v
=
\operatorname{tr}
\left[(M_{v,+}-M_{v,-})
\Sigma_q
(M_{v,+}-M_{v,-})^\top\right].
$$

E1 的学习任务是由高维输入 $h$ 预测 $t$；gate 只读取注册路由表示，expert 同时读取 residual 路由坐标与 payload 坐标。这样“是否分对”和“分开后是否降低功能风险”是两个可独立测量的对象。

### 9.1.4 必须运行的生成机制条件

| Regime | 变化 | 理论预期 |
|---|---|---|
| S1 Identifiable | $u_v\perp C_v$、$P_{K_v}u_v=u_v$、当前 spike 最大、$D_v>0$、分支映射秩 $\le r_e$ | residual-PCA + protected child 应成功 |
| F1 Variance distractor | 增加单位 nuisance 方向 $v_v\perp u_v$ 与系数 $\xi_v\sim\mathcal N(0,\tau_v^2)$，且 $\tau_v^2>\alpha_v^2$ | PCA split 应跟随 nuisance；oracle split 仍成功 |
| F2 Common overlap | 令 $u_v=\cos\theta\,u_C+\sin\theta\,u_\perp$，扫 $\theta$ | residual 信号按 $\sin\theta$ 衰减；$\theta=0$ 必败 |
| F3 Projector error | 用旋转后的 $\widehat P_C$，扫 $\delta_C=\|\widehat P_C-P_C\|_{\mathrm{op}}$ | 当 $\delta_CR$ 接近真实 residual margin 时出现转折 |
| F4 No conflict | 令 $M_{v,+}=M_{v,-}$ | gate 可纯，但专家功能收益应为零 |
| F5 Large sample | 扫每叶训练数 $n\in\{8,16,32,64,128,180\}$ | full-state 与 residual 差距随 $n$ 增大而缩小 |
| F6 Nonlinear XOR | 当前分支由两个 residual 坐标 XOR 决定 | 线性/PCA gate 失败，非线性 gate 可成功 |

### 9.1.5 E1 的精确拟合与步骤

E1 不用非凸 GELU 训练来“验证”代数定理，而使用可审计的闭式或凸优化对象：

1. **common predictor：**在 TRAIN 上用 reduced-rank ridge regression 拟合 $M_0q$，DEV 选择 ridge，随后冻结；
2. **route representation：**分别构造 full、oracle residual、learned residual、common-output 与 random/oracle split；
3. **split：**PCA 与 1D two-means 只用 TRAIN；DEV 只选择预注册 eigengap/balance operating point；
4. **branch experts：**在每个冻结分支中，对剩余功能目标拟合 rank-$r_e$ reduced-rank regression；
5. **geometry update：**使用定理 8 的受保护分支增量，幅度 $a$ 从预注册网格 $\{0,0.25,0.5,1,2\}$ 仅用 DEV 选择；
6. **确认：**在 TEST-ID/OOD 同时报告 split、归一化 margin、功能风险、祖先 logit 漂移与 oracle regret。

这样 E1 分离三个问题：split 是否可识别、分支函数是否冲突、受保护更新是否能生成 margin。只有 E1 按定理通过，才允许把失败或成功归因到 E2 的 NTP 优化。

### 9.1.6 ambient dimension sweep

固定 $r_{\mathrm{sem}}=6$，扫

$$
d\in\{32,64,128,256,512,1024,2048\}.
$$

必须区分两种维数增长：

1. **可删除 common 维数增长：**新增维数加入 $C$。full-state learner 按定理 3 恶化，而真实 residual 与 oracle specialized-subspace learner 应基本稳定；
2. **不可删除外部噪声维数增长：**新增维数加入 $C^\perp$ 的 $U_N$。full-state 与只做 de-common 的 residual learner 都会恶化，只有 oracle/learned specialized-subspace learner 应基本稳定。

这两个 sweep 防止把“去 common”错误解释为能够删除所有高维噪声。

## 9.2 E2：One-layer Hierarchical NTP Benchmark

### 9.2.1 数据语义

每个样本仍由路径

$$
b\in\{-1,+1\}^6
$$

生成。真实 bit 和叶类只用于数据生成与最终评估，不作为 router 或 expert 的显式输入。

### 9.2.2 词表与可泛化 cue 编码

1. 64 个 shared grammar tokens；
2. 每个深度 $t$、符号 $b_t$ 各有 512 个中性 cue ID；
3. 128 个 neutral payload tokens；
4. 128 个 neutral output tokens；
5. 结构 token：`<BOS>`、`<ROUTE>`、`<Q0>`--`<Q6>`、`<ANSWER>`、`<EOS>`。

为了避免 TEST 使用“从未训练过的随机 embedding 行”而导致伪 OOD 失败，cue ID 的输入 embedding 在数据生成前由冻结因子模型产生：

$$
e_{t,b,j}=g_t+b\,s_t+\xi_{t,b,j},
$$

其中 $g_t,s_t$ 是固定低维因子，$\xi$ 是可控 nuisance。所有 cue embedding 在模型训练中冻结；TRAIN/DEV/TEST 使用不重叠的 ID，但共享同一生成规律。这样 OOD 检验的是新 atom 与新模板，而不是未初始化词向量。

所有 code 使用中性名称，prompt 中不出现“数学、物理、粗类、细类”等标签词。真实 path bit 只保存在评估 manifest 中。

### 9.2.3 一个 episode 与层次功能目标

一个独立 episode 先生成共同上下文：

1. 24 个由共享 8-state Markov grammar 产生的 common tokens；
2. 六个 depth cue，各自从对应的冻结 cue family 抽取一个 atom；
3. cue 顺序由模板随机置换；
4. 一个 payload token $q_j$；
5. 一个 `<ROUTE>` token，其隐藏状态作为所有 gate 的输入。

同一 episode 派生 $L+1$ 个独立 query view；每个 view 只包含一个 query，避免因果模型从前一个答案看到后续答案：

$$
\text{context},\ <Q_t>,\ <ANSWER>,\ o_{\pi_{b_{1:t}}(j)}.
$$

$t=0$ 时 $\pi_{b_{1:0}}=\pi_0$ 是所有路径共用的 common payload permutation；$t\ge1$ 时，$\pi_{b_{1:t}}$ 是前 $t$ 个节点条件 permutation 的复合。节点 permutation 在任务生成时固定并跨 TRAIN/DEV/TEST 共享，因为它们定义同一个待泛化函数；禁止复用的是 episode seed、cue ID、payload—模板组合，而不是目标函数本身。

该任务要求模型逐层选择不同 payload transformation，直接实现定理 6 的功能冲突，而不是只做语义标签分类。

### 9.2.4 划分

完整确认规模沿用 19,200 个 episode：

| Split | 每叶 | 总 episode | 模板/cue 规则 |
|---|---:|---:|---|
| TRAIN | 180 | 11,520 | 训练模板族 A，TRAIN cue-ID pool |
| DEV | 40 | 2,560 | 模板族 A，DEV cue-ID pool |
| TEST-ID | 40 | 2,560 | 模板族 A，TEST-ID cue-ID pool |
| TEST-OOD | 40 | 2,560 | 未见模板族 B，TEST-OOD cue-ID pool |

以下对象不得跨划分复用：episode/grammar seed、cue ID、完整 payload—cue—模板组合。同一组节点 permutation 必须冻结并跨划分复用，才能检验同一功能在新表达上的泛化。

为了满足导师要求的快速迭代，先运行 $L=3$、8 叶、每叶同样 300 个 episode 的 smoke benchmark；只有机制门通过后才运行 $L=6$、64 叶确认规模。

### 9.2.5 Stage corpus

- Stage 0：只优化 `<Q0>` 的 common payload transformation；该目标与路径 $b$ 独立，不使用 8 粗类标签；
- Stage $t=1,\ldots,L$：新增 `<Q_t>` 的 prefix-conditioned transformation，其他已注册 query 仅用于冻结评估与祖先保护；
- 每阶段目标仍是下一词元交叉熵；
- 真实 bit/leaf 标签不进入 gate、loss、checkpoint 选择、split 阈值或 projector 估计；
- 所有 stage 在开始前已生成同一套 sealed TEST views，训练过程中不可读取。

### 9.2.6 数据守卫

1. 所有 row ID 唯一；
2. TRAIN/DEV/TEST atom 与 seed 隔离；
3. episode 文本/Token n-gram 无跨划分近重复；
4. cue 位置随机，防止位置直接编码 bit；
5. bag-of-words 和仅 common-token 分类器必须接近机会水平；
6. 随机打乱 cue 后性能应回落；
7. 仅 payload 不能预测 path；
8. TEST-OOD 模板在任何选择前密封。

E2 的主结论仅针对该可控一层模型。它检验“训练机制能否实现已证明的几何条件”，不证明真实预训练大模型具有相同 Hessian、split spike 或功能分区。

---

# 10. 模型与严格对照

## 10.1 一层 Transformer

主配置：

- decoder-only causal Transformer；
- layer 数：1；
- $d_{\mathrm{model}}=256$；
- attention heads：4；
- expert bottleneck $r_e=16$；
- GELU；
- 输出 code 使用冻结线性原型；普通输入 embedding 可训练，cue embedding 按 9.2.2 冻结；
- context length 不超过 64；
- dropout 0；
- theorem-aligned 主条件在 Tree 更新之后不再施加 RMSNorm/LayerNorm，直接接冻结线性输出头，使定理 7 的 logit 不变性精确适用；
- 另设 post-RMSNorm 鲁棒性条件，只能使用复合读出的 Jacobian 近似保护，不能声称精确零漂移；
- BF16 训练、FP32 指标累积。

$d=1024$ 作为确认规模；$d=2048$ 只在机制通过后运行。

## 10.2 条件表

| ID | 条件 | Split 输入 | Split | 新容量组织 | 保护 |
|---|---|---|---|---|---|
| C0 | Dense-Joint | 完整状态 | 无 | 单 Dense，全阶段联合 | 无 |
| C1 | Dense-Curriculum | 完整状态 | 无 | 与 Tree 相同阶段和 token budget | 冻结/新增容量匹配 |
| C2 | Flat-MoE | 完整状态 | learned flat gate | 平铺 experts | 标准负载均衡 |
| C3 | Tree-CommonOutput | $P_Ch$ / ancestor output | PCA | 层次 children | 输入投影可选 |
| C4 | Tree-FullState | $h$ | PCA | 层次 children | 输出保护 |
| C5 | Tree-Residual-PCA | $(I-\widehat P_C)(h-\bar h)$ | PCA + 1D two-means | proposed | 输入 + 输出保护 |
| C5O | Tree-Residual-PCA-OracleC | $(I-P_C^{\mathrm{true}})(h-\bar h)$ | 同 C5 | projector 上界 | 同 C5 |
| C6 | Tree-Residual-Random | residual | 平衡随机 split | 同 C5 | 同 C5 |
| C7 | Tree-Residual-Oracle | residual | 真实 path bit，仅作上界 | 同 C5 | 同 C5 |
| C8 | Tree-Residual-NoProtect | residual | 同 C5 | 同 C5 | 无输出零空间 |
| C9 | Tree-Residual-PCA+Margin | residual | 同 C5 | 同 C5 + pseudo-margin | 输入 + 输出保护 |

## 10.3 参数与计算匹配

不能只比较一个 Dense、4 个 Flat experts 和 3 个 Tree experts。必须同时报告：

1. **active-compute matched Dense：**每个 token 激活的瓶颈总宽度与 Tree 路径相同；
2. **total-parameter matched Dense：**总参数与整棵 Tree 相同；
3. **Flat MoE：**总 expert 参数与 Tree 相同，活动 expert 数与 Tree 路径活动计算量匹配；
4. 所有条件共享相同 attention、embedding、LM head、训练 token 数、optimizer 和阶段数据。

如果无法同时匹配总参数与活动计算，应保留两种 Dense/Flat 对照，而不能只选对方法有利的一种。

---

# 11. 精确训练与执行步骤

## 11.1 预检

1. 生成全部 manifest；
2. 验证 64 叶平衡与 split 隔离；
3. 运行词袋、位置、payload-only 泄漏基线；
4. 验证 Oracle split 在 E1 的 S1 条件可以达到理论 margin；
5. 验证 Random split 接近随机；
6. 验证 identity/no-op 模型逐样本复现输入；
7. 验证输出 projector 满足
   $$
   \|W_AP_K\|_{\mathrm{op}}<10^{-6}.
   $$

任一预检失败，正式训练停止。

## 11.2 Stage 0：common/root 学习

- 所有条件使用相同初始化 seed；
- 只优化与路径无关的 `<Q0>` common transformation，不使用 8 粗类或 64 细类监督；
- AdamW；
- 建议初始 LR $3\times10^{-4}$；
- weight decay $0.01$；
- batch size 256 query views，并按 episode 聚合；
- 每 250 step 在 DEV 评估；
- 最大 10,000 step；
- DEV NLL 连续 8 次评估无改善则停止；
- checkpoint 只由 DEV common-query NLL 选择；
- TEST 保持密封。

Stage 0 后冻结 shared attention/trunk、root expert、输出 code 原型和 common-query 读出。根 split 只从冻结 `<ROUTE>` 状态的 residual statistics 构造；不能由粗类标签训练。

## 11.3 每个深度的生长阶段

对深度 $t=1,\ldots,L$：

1. 按已冻结祖先 gate 将 TRAIN episode 送到节点；
2. 从 `<ROUTE>` 状态构造 $C_v$ 与 $P_{C_v}$；
3. 计算 residual；
4. 在 TRAIN 上拟合 PCA 与 1D two-means；
5. 运行 eigengap、balance、bootstrap stability 与 protection-compatibility guards；
6. 若 guard 不通过，该节点标记 `NO_SPLIT_IDENTIFIABLE` 或 `PROTECTION_CONFLICT`，不强制生长；
7. 初始化两个 rank-$r_e$ children；
8. 将所有已激活祖先 query 的输出 code pairwise-difference 行堆叠为 $W_{A,v}$，应用输入 residual projector 与输出 ancestor-nullspace projector；
9. 仅用当前 `<Q_t>` 下一词元损失训练本深度新 children；旧 query 不回传梯度，只用于逐步验证祖先 logits 不变；
10. 每节点样本等权聚合，避免大节点压倒小节点；
11. 最大 5,000 step，DEV 当前 query NLL patience 8；
12. 冻结本阶段 children、gates、node statistics 与当前 query 读出；
13. 进入下一深度。

## 11.4 随机种子

主实验使用 5 个模型 seed：

$$
\{24001,24002,24003,24004,24005\}.
$$

E1 每个生成 regime 使用额外 20 个数据 seed；PCA split bootstrap 使用 500 次；最终指标区间使用 2,000 次层级 bootstrap。

## 11.5 不能使用的信息

TEST-ID 与 TEST-OOD 的真实 path、leaf、expert utility、margin 或 loss 均不得用于：

- 选择 $C_v$；
- 选择 PCA 方向、阈值、rank 或是否 split；
- 选择 checkpoint；
- 选择 $\lambda_{\mathrm{sep}}$；
- 选择 report 中展示的节点。

---

# 12. 指标、统计单位与裁定规则

## 12.1 主指标：OOD 最差节点归一化低尾 margin

对每个内部节点 $v$，只用 TRAIN 拟合二元 L2 逻辑回归 probe，DEV 选择正则，随后冻结。若冻结 probe 的 $\|w_v\|_2<10^{-12}$，该节点直接记为 `DEGENERATE_PROBE`，不得人为归一化。否则对节点 TEST-OOD 样本定义

$$
\bar\gamma_{v,i}
=
\frac{y_{v,i}(w_v^\top h_i+b_v)}{\|w_v\|_2}.
$$

节点低尾 margin：

$$
\Gamma_{v,0.05}^{\mathrm{OOD}}
=Q_{0.05}(\bar\gamma_{v,i}).
$$

全树主指标：

$$
\boxed{
\Gamma_{\mathrm{tree}}^{\mathrm{OOD}}
=
\min_{v\in\mathcal V_{\mathrm{internal}}}
\Gamma_{v,0.05}^{\mathrm{OOD}}
}.
$$

取最差节点自动避免用平均值掩盖局部失败。

## 12.2 主要处理效应

令 $\mathcal B$ 为匹配的 Dense、Flat、CommonOutput、FullState 和 RandomSplit 对照。定义

$$
\Delta\Gamma
=
\Gamma_{\mathrm{C5}}^{\mathrm{OOD}}
-
\max_{b\in\mathcal B}
\Gamma_b^{\mathrm{OOD}}.
$$

### Geometry Pass

同时满足：

1. C5 的 $\Gamma_{\mathrm{tree}}^{\mathrm{OOD}}$ 同时 95% 区间下界 $>0$；
2. $\Delta\Gamma$ 的配对同时 95% 区间下界 $>0$；
3. 5 个 seed 至少 4 个同向，主 seed 通过；
4. TEST-ID 与 OOD 均不触发收敛/区间精度守卫。

Dense/Flat 是否为负不是 Pass 的前提。若它们也为正，只能根据处理效应判断 Tree 是否有额外价值。

## 12.3 功能必要 guard

定义 fine functional answer 的 held-out NLL：

$$
L_{\mathrm{func}}.
$$

定义相对最佳匹配基线的改善

$$
\Delta L
=
L_{\mathrm{best\ baseline}}-L_{\mathrm{C5}}.
$$

定义 shared 与 oracle 的可用功能 gap

$$
G_{\mathrm{func}}
=
L_{\mathrm{shared}}-L_{\mathrm{oracle}},
$$

以及路由后剩余 regret 比例

$$
R_{\mathrm{regret}}
=
\frac{L_{\mathrm{routed}}-L_{\mathrm{oracle}}}
{\max(G_{\mathrm{func}},10^{-8})}.
$$

### Full Mechanism Pass

除 Geometry Pass 外，还要求：

1. $\Delta L$ 的 OOD 95% 区间下界 $>0$；
2. 当 $G_{\mathrm{func}}>0$ 时，$R_{\mathrm{regret}}$ 的 95% 区间上界 $\le0.10$，即 routed Tree 收回至少 90% 的 oracle-vs-shared 可用 gap；
3. F4 No-conflict 中 $|\Delta L|$ 的 95% 区间完全落入预注册等价带 $[-0.01,0.01]$ nat/query，避免把容量噪声写成功能专门化。

若 margin 转正但 $\Delta L\le0$，状态为 `GEOMETRY_ONLY`，不能声称 MoE specialization 有功能收益。若 oracle gap 本身不为正，则状态为 `NO_FUNCTIONAL_CONFLICT_ADMISSION`。

## 12.4 抗遗忘 hard guard

在最终表示上计算所有祖先 pairwise logits。定义

$$
D_{\mathrm{ancestor}}
=
\max_i
\|W_Ah_i^{\mathrm{after}}-W_Ah_i^{\mathrm{before}}\|_\infty.
$$

精确投影实现要求

$$
D_{\mathrm{ancestor}}\le10^{-5}
$$

并且祖先预测逐样本一致。该 hard guard 只适用于 theorem-aligned 直接线性读出条件；post-RMSNorm 条件必须另报复合 logits 漂移，不能套用精确零漂移门槛。若只在冻结旧状态上评估而最终状态改变，不算通过该 guard。

## 12.5 无标签 split 指标

真实 path 只在评估时打开。每个节点报告：

- 二元 balanced accuracy，在交换左右标签后取最大；
- normalized mutual information；
- split balance；
- eigengap；
- bootstrap assignment stability；
- 与高方差 nuisance 变量的对齐。

不使用“二叉 split 与 8 类标签的 ARI”作为主指标，因为两个 partition 的粒度不同且无法直接解释满分含义。

## 12.6 其他诊断

1. common leakage：
   $$
   \|A_vP_{C_v}\|_F,
   \qquad
   \|W_AP_{K_v}B_v\|_F;
   $$
2. branch function conflict $D_v$；
3. routed expert regret：
   $$
   L_{\mathrm{routed}}-L_{\mathrm{oracle\ expert}};
   $$
4. common/specialized gradient covariance 特征值；
5. 每个 depth 的方向幅度与有效秩；
6. $n,d,r_C,\tau_C,\sigma,\delta,\theta$ 的缩放曲线。

## 12.7 统计单位

- 基本独立单位：latent semantic seed / atom bundle；
- 模型 seed 是第二层随机性；
- 2,000 次 bootstrap 以 semantic seed/episode bundle 为主要独立单位并按 leaf 分层；5 个模型 seed 作为固定复制条件报告 4/5 一致性，不用 5 个 seed 伪装成充分的随机效应总体；
- 节点多重性通过“最差节点”统计量和 max-centered bootstrap 处理；
- TEST-OOD 是主确认面板，TEST-ID 是必要复制面板。

---

# 13. Pass / Fail / Insufficient 的完整定义

## 13.1 Pass

`FULL_PASS` 需要：

1. residual split guards 通过；
2. C5 在 OOD 的最差节点 margin 下界 $>0$；
3. 相对全部匹配对照的 $\Delta\Gamma$ 下界 $>0$；
4. functional NLL 改善下界 $>0$；
5. ancestor logits 精确保护；
6. S1 成功；F1 中 PCA 失败而 oracle 成功；F2 随 $\sin\theta$ 单调衰减且 $\theta=0$ 失败；F4 不产生功能收益；
7. Oracle/Random controls 表现符合 known-good/known-bad 预期。

## 13.2 Typed Failures

- `SPLIT_FAIL`：Oracle Tree 成功，PCA Tree 失败；
- `SPECIALIZATION_FAIL`：PCA purity 高，但 Oracle/PCA children 都无功能收益；
- `PROTECTION_CONFLICT`：真实/候选分支方向几乎完全落在祖先读出的行空间中，严格保护与继续分离不可兼得；
- `PROTECTION_FAIL`：理论兼容条件满足，但 margin 或 loss 改善仍伴随祖先 logits 漂移；
- `NO_TREE_ADVANTAGE`：Dense/Flat 同样达到或超过 C5；
- `RESIDUAL_PRIOR_FAIL`：FullState 成功而 Residual 失败，且 fine 信号与 common 子空间重合；
- `TASK_TOO_EASY`：全部方法均接近完美，无法区分机制；
- `TASK_TOO_HARD`：Oracle split 也不能得到正 margin 或功能收益。

## 13.3 Insufficient

出现任一情况即为 `INSUFFICIENT`：

- 数据泄漏守卫失败；
- split balance/eigengap 不足但仍被强制分裂；
- 参数/计算无法匹配；
- TEST 参与选择；
- probe 不收敛；
- 置信区间过宽；
- 祖先保护实现误差超标；
- 仅一个 seed 正向；
- Qwen 19,200 数据的独立人工语义 review 尚未闭合却被当作最终确认。

---

# 14. 不同结果分支及研究建议

| 直接结果 | 最安全解释 | 研究建议 |
|---|---|---|
| C5、C7 均成功，C3/C4/C6 失败，且功能 NLL 改善 | residual 对象、可识别 split 和保护更新共同有效 | 正式建立 mechanism anchor，再做 Qwen bridge |
| C7 成功但 C5O/C5 失败 | expert 架构可用，但 residual-PCA 无法发现真实分支 | 停止“PCA=语义”叙述，转向专家效用差、梯度冲突或多视图 split |
| C5O 成功但 C5 失败 | split 机制可用，common 子空间估计错误 | 比较参数列空间、Jacobian 空间与数据输出空间，不扩大 Tree |
| C5 margin 转正但 NLL 不改善 | 产生了标签几何，但不对应专家功能 | 不进入真实 MoE；重新定义 route target 为 expert utility |
| C5 与 C4 相同 | residual 不是必要条件 | 只保留为正则化/样本效率候选，不声称机制必需 |
| Dense/Flat 也同样正且功能相同 | 任务可由普通训练解决，树无额外价值 | 增强条件冲突或降低容量；若仍相同，停止树主张 |
| FullState 优于 Residual | fine 信号部分位于 $C$，投影删除了有效信息 | 改为 soft subtraction、条件 projector 或保留交叉项 |
| PCA 对 nuisance 纯、Oracle 成功 | 最大方差不是语义 | 把 eigengap 仅当可识别性 guard，不当语义证据 |
| NoProtect 遗忘、Protected 不遗忘 | 输出零空间约束必要 | 保留定理 7 机制 |
| Protected 仍遗忘 | $W_A$ 定义或非线性读出不完整 | 扩展保护对象，不能声称严格抗遗忘 |
| 小样本 residual 优、大样本追平 | 支持有限样本方差降低 | 将贡献写成 sample efficiency，不写成信息创造 |
| E1 成功、E2 失败 | 理论几何存在，但 NTP/优化未实现 | 引入显式 local margin 或更直接的功能反馈 |
| E2 成功、Qwen bridge 失败 | 合成条件未在真实表征中成立 | 审计 $C$、spike、冲突与分布漂移，不扩大模型 |
| Qwen supervised bridge 成功、无标签版本失败 | 标签可重编码，但自演化 split 未成立 | 不能声称无标签层次树；研究监督来源 |

---

# 15. 对原 19,200 条 Qwen residual 计划的正确定位

## 15.1 保留价值

现有 19,200 条 Binding-controlled 数据适合做：

- 冻结表示上的 supervised re-encoding 上界；
- residual/full-state/common-output 的对比；
- 低秩 child 架构与输出保护的工程 sanity check；
- TEST-ID / 新模板泛化检查。

## 15.2 不能承担的结论

它不能单独证明：

- NTP 为什么形成 common-first 表示；
- 低维语义如何被映射到高维；
- 无标签 PCA 为什么对应真实分支；
- 树结构自发产生专家功能；
- 训练中的几何是因 Tree 生成，而不是后处理重新编码。

## 15.3 对原计划的最低修改

若保留该桥接实验，必须：

1. 先完成数据 H1 独立人工 review；
2. 将 Stage 1/Stage 2 明确命名为 `SUPERVISED_ORACLE_REENCODING`；
3. gate 在
   $$
   (I-P_C)(h-\bar h)
   $$
   上拟合，而非根 expert 输出；
4. 使用 $r_e\ll d$ 的瓶颈 expert；
5. 加入 output-nullspace protection；
6. 以 matched Dense/Flat/Curriculum 为对照；
7. probe 只在 TRAIN/DEV 拟合选择；
8. 使用归一化 margin；
9. 将 64-way 全局 margin 降为辅助，节点/path margin 作为主几何指标；
10. 不预注册 Dense/Flat 必然为负。

---

# 16. 对用户原始三模型方案的逐项修订

## 16.1 Dense Baseline

原 Dense 可以保留，但应增加两种匹配版本：

- active-compute matched；
- total-parameter matched。

并使用与 Tree 相同的 staged corpus 和训练 token 数。不能只用一次性 64 类混合训练，否则差异同时包含 curriculum、冻结和容量增长。

## 16.2 Flat MoE

Flat MoE 必须：

- 与 Tree 总 expert 参数匹配；
- 与 Tree 活动计算匹配；
- 使用相同 root/common 预训练阶段；
- 报告 top-1 与 matched-active top-$k$ 之一；
- 负载均衡只能控制使用率，不能替代功能效用指标。

## 16.3 Tree

原公式

$$
h_{\mathrm{final}}
=h_0+pE_{00}(h_0)+(1-p)E_{01}(h_0)
$$

应改为

$$
r=(I-P_C)(h_0-\bar h_0),
$$

$$
\widehat b=\operatorname{Split}(r),
$$

$$
h_{\mathrm{final}}
=h_0+
P_KB_{\widehat b}
\phi(A_{\widehat b}r).
$$

若要保持真正的树状稀疏计算，使用 hard top-1 分支；soft sigmoid 混合会同时激活两个 child experts，不能直接解释为二叉树。

---

# 17. 理论自检

## 17.1 已检查且成立的部分

| 项目 | 状态 | 检查 |
|---|---|---|
| 线性抬升等价 | PASS | 构造了双向分类器 |
| 线性投影非创造 | PASS | 复合权重 $A^\top w$ |
| nuisance MSE | PASS | 协方差迹精确计算 |
| residual MSE | PASS | 正交投影后维数项正确 |
| margin 分位数 | PASS | 条件高斯的一维投影 |
| PCA population recovery | PASS | rank-one spike 协方差 |
| PCA finite perturbation | PASS | Rayleigh 商给出对齐下界 |
| PCA nuisance counterexample | PASS | 最大特征值转向无关方向 |
| common-first 二次模型 | PASS | 正交谱模态递推 |
| shared-expert conflict risk | PASS | 平方损失精确分解；错误率使用功能加权定义 |
| output-nullspace invariance | PASS | $W_AP_K=0$ |
| branch update margin | PASS | 一维高斯平移 |
| hierarchical code separability | PASS | 等范数最近中心线性分数 |

## 17.2 明确没有证明的部分

- 低秩 GELU expert 的非凸优化会达到构造解；
- PCA gate 在自然语义数据上满足 spike 条件；
- pseudo-margin 不会强化错误 nuisance cluster；
- NTP 的真实 Hessian 具有固定 $C/S$ 分解；
- 祖先读出 $W_A$ 已覆盖所有需要保护的语言功能；
- 64 个人工语义叶类就是真实专家效用分区。

## 17.3 最容易再次犯的理论错误

1. 把“探针失败”写成“不存在任何线性分类器”；
2. 把“residual probe 更好”写成“residual 创造新信息”；
3. 把“PCA 方差最大”写成“语义最强”；
4. 把输入梯度正交写成最终输出不遗忘；
5. 把标签监督重编码写成无标签自演化；
6. 把正 margin 写成真实专家效用；
7. 把合成数据成立写成真实 LLM 已满足相同假设。

---

# 18. 下一次组会应提交的最小闭环

## 18.1 必须提交

1. 定理 1--9 的两页压缩版证明；
2. 一张“假设—可控参数—可观测量—成功/失败方向”表；
3. E1 向量 synthetic 的 S1、F1、F2、F4 四个 regime；
4. Oracle、Random、CommonOutput、FullState、Residual 五个最小条件；
5. 一张样本量 $n$ 与 nuisance dimension $d-r_{\mathrm{sem}}$ 的缩放图；
6. 一张 PCA spike ratio 与 gate purity/margin 的相变图；
7. 祖先 logits 精确不变的单元验证。

## 18.2 本次不应先做

- 不先训练 Qwen3-30B-A3B 新模型；
- 不先实现 127-expert 完整深树；
- 不先讨论 JL/LSH 压缩；
- 不把已打开的 19,200 数据当作唯一确认；
- 不用一次正结果跳过 matched baselines 与失败 regime。

## 18.3 下一决策规则

### Pass

E1 中：

- work regime 按定理成功；
- PCA nuisance regime 按定理失败、oracle 成功；
- no-conflict regime 无功能收益；
- output protection 精确成立；
- residual 的有限样本优势随 $n$ 增大消失。

则授权 E2 一层 Transformer full protocol。

### Fail

若连 oracle split + protected children 都无法在冲突任务中产生 margin 或降低损失，则 tree 架构的核心机制没有成立，应停止扩大。

### Insufficient

若只得到 residual 分类变好，但没有功能冲突、输出保护、样本缩放或 failure regime，则仍不能进入一层 Transformer 主实验。

---

# 19. Protocol A--G 状态台账

| Block | 内容 | 当前状态 |
|---|---|---|
| A | 问题、竞争解释、claim boundary | `PROPOSED`，本文已给出 |
| B | E1/E2 数据构造与 provenance | `PROPOSED`，需确认具体词表与 regime 数值 |
| C | NTP 任务、pseudo-label 与禁止真实标签 | `PROPOSED` |
| D | 低秩 expert、residual split、output protection | `PROPOSED` |
| E | NTP / pseudo-margin、优化和停止 | `PROPOSED` |
| F | 匹配基线、主 margin、功能 guard、结果分支 | `PROPOSED` |
| G | seeds、资源、artifact 路径与执行审批 | `BLOCKED`，尚未指定代码仓库与资源上限 |

**Cross-block consistency：**理论上已形成一致候选，但因 A--G 尚未被研究者显式确认，协议必须保持 `DRAFT_NOT_EXECUTABLE`。

---

# 20. 最终研究认识更新

现有随机投影工作没有失败；它完成了一个必要的否定边界：

> 线性压缩不会替模型创造原本不存在的路由几何。

现有大模型实验进一步把问题定位为：

> 条件增量信息存在，但没有被组织成独立、跨模板稳健、具有正低尾 margin 的 Router 空间。

导师在 0824 组会提出的真正新方向，是把研究对象从“压缩已有表示”改为“生成可路由表示”：

$$
\text{common-first learning}
\rightarrow
\text{remove explained subspace}
\rightarrow
\text{identify residual branch}
\rightarrow
\text{branch-conditional low-rank update}
\rightarrow
\text{protect ancestor function}
\rightarrow
\text{positive hierarchical margin}.
$$

这条链中，只有中间若干理想化代数结论已经能被严格证明；PCA split、NTP 自发分化和真实专家效用仍必须通过 success/failure 成对的合成实验裁定。

因此下一次组会最准确的问题不是“我们的 Tree 能不能 work”，而是：

> **在什么最小条件下，residual split 是可识别的、specialized expert 是功能上必要的、分支条件更新能够生成正 margin、祖先功能能够被精确保护；这些条件一旦被破坏，实验是否按理论失败？**

只有这个问题闭合后，才应把机制迁移到 Qwen 冻结表示；只有真实专家效用和正 OOD margin 都出现后，旧随机投影 proof 才重新成为下一阶段的压缩工具。

---

# Source Map

1. `0824 gating_原文.docx`：
   - 00:06--01:23：旧层级分发方案及失败假设；
   - 02:44--13:07：common/specialized 低秩专家、功能冲突与渐进生长；
   - 13:24--18:30：从“使用祖先输出”修正为“减去祖先可解释空间后使用 residual”；
   - 19:51--31:31：线性投影非创造、高维表示 margin 不足及 NTP common-first intuition；
   - 31:50--32:26：一层 Transformer、synthetic work/fail 成对实验要求。
2. `0824_gating_会议记录_逐句校订与证明任务.md`：逐句校订、P0--P6 初步形式化和原 next-meeting 任务。
3. `random_projection_router_proof_protocol.md`：随机投影定理 1--5、H0--H4 协议、Qwen3-30B-A3B 实测数值与结论边界；其中数据 H1 尚未完成人工独立复核。
4. 用户提供的《自演化层次化专家树小规模验证实验方案》：Dense、Flat MoE、Tree 三模型候选设计；本文对其数据、任务、目标、架构、优化和确认边界逐块修订。
5. Research_System skills：`research-progress-core`、`problem-anchor-writer`、`experiment-card-writer`、`research-story-writer`、`scholar-mode`。

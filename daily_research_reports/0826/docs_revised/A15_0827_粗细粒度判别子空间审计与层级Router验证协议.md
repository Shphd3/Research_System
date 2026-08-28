---
document_type: corrected_experiment_protocol_and_architecture_decision_note
status: SUPERSEDED_NOT_EXECUTABLE
date: 2026-08-27
research_line: A15_MoE_Router_representation_hierarchy
title: 粗细粒度判别子空间审计与层级 Router 验证协议
sources:
  - feature (7)(1).pdf
  - 0826会议记录.md
  - 0824_gating_会议记录_逐句校订与证明任务.md
  - A15_低维语言因素到可分高维表征_理论与最小实验协议(1).md
---

> 本稿把几何审计、功能验证和架构选择写成一个协议，已被研究者纠正。当前只保留
> 为历史设计材料，不得据此实现或运行。新的活动问题见
> [focus_coarse_fine_direction_alignment.md](../focus_coarse_fine_direction_alignment.md)；
> 待其四段白话设计获得确认后，再另写只回答方向对齐的 Protocol。

# 粗细粒度判别子空间审计与层级 Router 验证协议

## 0. 结论先行

本轮应当把研究问题冻结为：

> **在真实粗细粒度自然语言数据上，粗粒度判别子空间与父类条件下的细粒度判别子空间，是近似正交、显著重叠，还是父类特异的不同局部坐标系？**

这确实比直接训练层级 MoE 更接近当前未知。先做冻结表征审计，再由结果选择架构。

但旧实验中“单领域需要 7 维、八个领域合并需要 56/64 维，因此不同领域依赖不同子空间”的强结论需要撤回。主要原因不是实验数值一定错误，而是 **7 与 56 本身受分类头输出维数的代数上界控制**：

- 对一个 8 分类线性探针，去掉所有类别共享的 logit 后，判别权重矩阵的秩天然不超过 \(8-1=7\)；
- 对八个独立的 8 分类任务，把八个判别头拼接后，联合秩天然不超过 \(8\times 7=56\)；
- 因而“7 维可保留单任务线性功能”不能证明表示本身具有 7 维内在语义结构；“56 或 64 维覆盖八个任务”也不能单独证明八个任务子空间互相独立。

当前实验最多支持较弱陈述：

> **在注册的监督线性探针与训练方式下，一个小共享投影比每个任务单独拟合更难同时保留所有任务性能；但其原因可能是任务方向不同，也可能是分类头秩上界、估计不稳定、有限样本噪声或优化非唯一性。**

要把它升级为“父类特异局部子空间”，必须补上三类证据：

1. **同一任务子空间可复现；**
2. **不同任务之间的几何重合显著低于同一任务复现度；**
3. **一个领域学到的输入子空间不能有效迁移到另一个领域，即存在功能性而不仅是几何性的差异。**

---

# 第一部分：旧实验勘误

## 1. “单领域 7 维”的逻辑漏洞

设冻结表征为 \(X\in\mathbb R^{n\times d}\)，八分类线性探针权重为

\[
W\in\mathbb R^{d\times 8}.
\]

令

\[
H_8=I_8-\frac18\mathbf 1\mathbf 1^\top
\]

去掉所有类别共享的 logit 方向，则有效判别权重为

\[
W_{\mathrm{disc}}=WH_8.
\]

由于 \(\operatorname{rank}(H_8)=7\)，必有

\[
\operatorname{rank}(W_{\mathrm{disc}})\le 7.
\]

因此总存在分解

\[
W_{\mathrm{disc}}=P_7A_7,
\qquad
P_7\in\mathbb R^{d\times 7},
\quad
A_7\in\mathbb R^{7\times 8}.
\]

这与原实验中的低秩形式

\[
X P_r A_r
\]

完全对应。换言之：

> **只要最终任务仍是线性八分类，7 维足以表示任意中心化线性分类头；它是分类问题的代数上界，不是从数据中发现的“语义内在维数”。**

所以原结论应由：

> 单个领域内部的细分类功能只需要约 7 维低维语义子空间。

改为：

> 单个八分类任务的监督线性判别头可被不超过 7 个输入方向表示；当前结果尚不能据此判断真实表示的内在任务维数。

### 1.1 怎样重新定义“有效功能维数”

不再把 \(7\) 本身当作发现，而定义

\[
r_{0.95}
=
\min\left\{r:
\operatorname{Perf}(r)
\ge
\operatorname{Perf}_{\mathrm{chance}}
+0.95\bigl(
\operatorname{Perf}_{\mathrm{full}}-
\operatorname{Perf}_{\mathrm{chance}}
\bigr)
\right\}.
\]

其中：

- \(\operatorname{Perf}_{\mathrm{full}}\) 是完整冻结表征上的正则化线性探针性能；
- \(\operatorname{Perf}(r)\) 是只使用前 \(r\) 个注册判别方向的留出性能；
- 必须在未见模板测试集上计算；
- \(r\in\{1,2,\ldots,7\}\)。

只有当 \(r_{0.95}\ll7\)，且不同 split/seed 下稳定，才可以说该八分类任务的**线性功能有效维数**低于代数上限。

---

## 2. “八个领域需要 56/64 维”的逻辑漏洞

设第 \(c\) 个领域的八分类有效权重为 \(W_cH_8\)。拼接八个任务：

\[
W_{\mathrm{union}}
=
[W_1H_8,\ldots,W_8H_8].
\]

则

\[
\operatorname{rank}(W_{\mathrm{union}})
\le
\sum_{c=1}^{8}\operatorname{rank}(W_cH_8)
\le 8\times7=56.
\]

因此：

- 56 是八个八分类线性头联合表示的代数上界；
- 64 已经超过该上界，若 56→64 仍带来明显线性分类改善，应优先检查优化未收敛、目标未中心化、任务并非独立头，或评估中包含了额外非线性；
- “到 56 才达到 90%”最多说明当前学习到的八个判别头没有被更小共享空间很好压缩，不能直接说明八个真实语义子空间互相正交。

### 2.1 正确要估计的量

真正有意义的是联合稳定判别矩阵的有效秩：

\[
r_{\mathrm{union},0.95}
=
\min\left\{r:
\text{一个共享 }r\text{ 维输入空间，使八个任务在留出集上均保留至少 95% 的自身功能}
\right\}.
\]

并将它与以下两者比较：

\[
\max_c r_{c,0.95},
\qquad
\sum_c r_{c,0.95}.
\]

解释边界为：

- 接近最大值：不同任务高度共享；
- 介于最大值与和之间：部分共享；
- 接近和：与局部空间并集相容，但仍需稳定性和迁移证据。

---

## 3. “两两重合只有 1%–2%”仍不足以下结论

原结果在第 24、28 层报告约 1.27% 和 1.79% 的两两重合。对于 \(d=4096,r=7\) 的两个随机子空间，期望归一化重合约为

\[
\frac rd=\frac7{4096}\approx0.171\%.
\]

因此 1.27% 与 1.79% 虽然绝对值小，却分别约为随机水平的 7.4 倍和 10.5 倍，不能简单写成“几乎完全不重合”。更关键的问题是：

1. 没有报告同一领域在不同训练子集、seed 下的子空间重合；
2. 监督低秩分解存在多个性能近似相同的解，几何方向可能不唯一；
3. 原始欧氏角度会受表征各向异性影响；
4. 几何重合小不等价于功能迁移差。

因此必须增加：

- **同任务复现度**；
- **跨任务重合与同任务复现度的差值**；
- **跨任务子空间迁移矩阵**。

只有满足

\[
\text{same-task stability}
\gg
\text{cross-task overlap}
\]

且跨任务投影显著损失留出性能，才支持“父类特异的判别坐标”。

---

## 4. 当前仍可保留的事实

以下认识不依赖 7/56 解释，仍应保留：

1. PCA 最大方差方向不是稳定的语义判别方向；判别方向更多位于谱的中后部；
2. 学会粗粒度分类不会自动获得细粒度分类能力；
3. 全局删除粗粒度/父类信息可能造成不同父类叶节点碰撞；
4. 人工给出正确父类条件后，细粒度表征和语言模型损失可能改善；
5. 当前需要先查明粗、细判别子空间关系，再确定是全局 residual Router 还是父类条件 Router。

---

# 第二部分：本轮唯一研究问题

## 5. 数学对象

设：

- 粗粒度标签 \(C\in\{1,\ldots,K_C\}\)；
- 每个粗类内部的细粒度标签 \(F\in\{1,\ldots,K_F\}\)；
- 冻结表示 \(H\in\mathbb R^d\)。

定义：

- \(S_C\)：用于区分粗类的监督线性判别子空间；
- \(S_{F\mid c}\)：固定粗类 \(c\) 后，用于区分其内部细类的监督线性判别子空间；
- \(S_F^{\mathrm{shared}}\)：一个由所有粗类共用、但允许每个粗类拥有独立分类头的共享输入子空间。

本轮不把这些对象称为“真实语义子空间”，而称为：

> **在指定表示、标签、线性函数族与数据 split 下，由监督探针识别的判别子空间。**

这避免把探针权重空间直接等同于模型内部唯一存在的语义坐标。

## 6. 三个竞争假设

### H1：全局正交 residual

\[
S_{F\mid c}\approx S_F,
\qquad
S_F\perp S_C,
\qquad \forall c.
\]

预测：

- 不同父类的细粒度子空间高度共享；
- 去掉 \(S_C\) 后细分类性能不降，甚至提高；
- 一个全局 residual Router 足够。

### H2：粗细方向重叠

\[
S_{F\mid c}\cap S_C\neq\{0\}.
\]

预测：

- 粗、细判别空间有显著主角重合；
- 删除 \(S_C\) 会损失细分类信息；
- 架构需保留父类上下文，并使用条件化或斜投影，而非硬正交删除。

### H3：父类特异局部坐标

\[
S_{F\mid c}\not\approx S_{F\mid c'},
\qquad c\neq c'.
\]

预测：

- 每个局部子空间自身稳定；
- 跨父类几何重合和功能迁移显著较低；
- 一个小共享输入空间无法保留所有任务；
- 架构应先确定父节点，再调用父类特异的局部 Router/experts。

若三个假设均不成立，说明线性子空间模型本身不足，暂时不能用静态低秩几何指导 Router。

---

# 第三部分：数据集的确定构造

## 7. 合成向量数据：验证分析方法能否恢复已知真值

合成数据不用于证明真实语言表示满足某一结构，只用于验证：

- 子空间估计算法是否正确；
- overlap、cross-transfer 和谱位置图能否区分不同几何情形；
- 旧 7/56 结论为何可能由分类头秩上界产生。

### 7.1 固定参数

\[
d=128,
\quad K_C=4,
\quad K_F=4,
\quad r_C=3,
\quad r_F=3,
\quad r_N=16.
\]

每个叶类生成：

- TRAIN：2000；
- DEV：500；
- TEST：1000。

总样本量：\(4\times4\times3500=56{,}000\)。

生成互相正交的基础子空间：

- \(U_C\in\mathbb R^{128\times3}\)：粗粒度空间；
- \(U_N\in\mathbb R^{128\times16}\)：高方差但与标签无关的 nuisance；
- \(U_{F\mid c}\in\mathbb R^{128\times3}\)：细粒度空间。

令 \(a_c\in\mathbb R^3\) 为四个粗类的正四面体编码，\(b_f\in\mathbb R^3\) 为四个细类的正四面体编码。样本为

\[
h_{c,f}
=
2U_Ca_c
+
U_{F\mid c}b_f
+
4U_N\xi
+
0.5\varepsilon,
\]

其中

\[
\xi\sim\mathcal N(0,I_{16}),
\qquad
\varepsilon\sim\mathcal N(0,I_{128}).
\]

选择 nuisance 方差大于语义信号，是为了构造“PCA 头部不等于判别方向”的已知情形。

### 7.2 三个主情形

#### S1：全局正交细粒度空间

\[
U_{F\mid1}=\cdots=U_{F\mid4}=U_F,
\qquad U_F^\top U_C=0.
\]

真值：支持 H1。

#### S2：粗细重叠

先生成 \(V_F\perp U_C\)，再令

\[
U_F^{(\rho)}
=
\operatorname{qf}
\left(
\sqrt{1-\rho^2}V_F+
ho U_CR
\right),
\qquad \rho=0.5,
\]

其中 \(R\) 为随机正交矩阵，所有父类共用该细粒度空间。

真值：支持 H2，硬删除 \(S_C\) 应损失细粒度性能。

#### S3：父类特异局部空间

四个 \(U_{F\mid c}\) 在 \(U_C^\perp\) 中分别生成，并令它们两两正交。

真值：支持 H3。每个局部空间低维且稳定，但共享空间的维数随父类数量增长。

### 7.3 额外碰撞反例

构造

\[
h_{c,f}=U_Ca_c+U_Fb_{\pi_c(f)}+\varepsilon,
\]

其中不同父类使用不同置换 \(\pi_c\)。去掉 \(U_Ca_c\) 后，不同父类叶节点可能获得相同 residual。该反例验证：

> **父类条件可能是解释局部坐标语义所必需的信息，不能把“去父类”与“父类条件化”混为一谈。**

### 7.4 合成数据通过条件

分析代码必须满足：

1. S1 中恢复低 coarse–fine overlap，且 coarse residual 不损失 fine 性能；
2. S2 中恢复显著 overlap，且 coarse residual 出现性能下降；
3. S3 中 same-task stability 高、cross-task transfer 低；
4. PCA 头部主要落在 nuisance 空间，而监督判别空间位于后续谱段；
5. 在任意四分类任务中，算法不得把 \(r=3\) 直接解释为内在秩发现，因为它等于 \(K_F-1\)。

若这些 sanity check 失败，不进入真实自然语言数据。

---

## 8. 真实自然语言数据：回答真正的研究问题

### 8.1 数据来源

使用之前已构造的粗细粒度自然语言数据：

- 8 个粗粒度领域；
- 每个领域 8 个细粒度子领域；
- 共 64 个叶类；
- 总计 19,200 条样本，即每个叶类 300 条。

沿用已有领域集合：数学、物理、化学、生物、计算机、经济、医学、语言学。细类沿用现有数据定义，不在本轮重新改名或重标。

### 8.2 必需元数据

每条样本必须带有：

```text
sample_id
coarse_id
fine_id
template_id
concept_id
generation_seed
split
```

若现有数据缺少 `template_id` 或 `concept_id`，应先补齐或重新生成；否则无法区分语义泛化与模板/关键词记忆。

### 8.3 固定 split

对每个叶类的 300 条样本，按以下规则划分：

| split | 每叶数量 | 模板 | 概念 | 用途 |
|---|---:|---|---|---|
| TRAIN | 160 | 训练模板 | 训练概念 | 子空间和 probe 拟合 |
| DEV | 40 | 训练模板 | 与 TRAIN 不重合 | 正则与 rank 选择 |
| TEST-ID | 50 | 训练模板 | 与 TRAIN/DEV 不重合 | 同模板确认 |
| TEST-OOD | 50 | 完全未见模板 | 与其他 split 不重合 | 主结论 |

总数为 \(160+40+50+50=300\)。

划分使用固定哈希：

\[
\operatorname{hash}(\text{sample\_id},240827)
\]

排序后确定，不允许根据结果重新划分。

### 8.4 数据控制

必须满足：

1. 四个 split 中每个叶类严格等量；
2. 读出位置和 answer token 在所有类别中一致；
3. prompt 长度分布在类别间匹配；
4. 文本中不出现粗类或细类标签名称作为直接答案；
5. 同一 semantic concept 不跨 split；
6. TEST-OOD 模板不出现在 TRAIN/DEV；
7. 每个模板在各类别中的频率匹配；
8. 报告词表重叠、长度和模板分类准确率，排除明显表面泄漏。

### 8.5 表征对象

主对象固定为第 24 层的候选新增更新 \(R_{U,24}\)，第 28 层只作一次确认。

设：

\[
X_\ell=N_\ell(h_\ell),
\qquad
Z_\ell=N_\ell(h_\ell+a_\ell),
\qquad
U_\ell=Z_\ell-X_\ell.
\]

仅在 TRAIN 上拟合

\[
\widehat B_\ell
=
\arg\min_B
\|U_{\ell,\mathrm{train}}-X_{\ell,\mathrm{train}}B\|_F^2
+\lambda\|B\|_F^2,
\]

然后对所有 split 定义

\[
R_{U,\ell}=U_\ell-X_\ell\widehat B_\ell.
\]

\(\lambda\) 只由 DEV 选择。禁止使用 TEST 重新拟合“可预测旧信息”。

### 8.6 MVP 范围

次日 11 点前只做：

- 数学、物理两个粗类；
- 每个粗类选择样本数和模板数均匹配的 4 个细类；
- 第 24 层；
- 一个固定 split；
- 完成方法 sanity、主图和结论。

只有当结果不稳定，才加入第 28 层；不同时扩大到 8×8 和新模型训练。

---

# 第四部分：确定的子空间求解算法

## 9. 为什么不直接把 ridge 的 rank 当作语义秩

普通多类岭回归为

\[
\widehat W_\lambda
=
(X^\top X+\lambda I)^{-1}X^\top Y.
\]

可以把 \(\operatorname{col}(\widehat W_\lambda H_K)\) 作为一个**probe-selected 判别空间**，但其秩至多为 \(K-1\)。因此它适合定位方向，不适合单独证明表示内在低秩。

本协议采用：

- **正则化层次 Fisher 判别**估计几何子空间；
- **岭回归/多项逻辑回归**验证投影后的留出功能。

两者职责分开。

---

## 10. 统一噪声度量：先在同一坐标系中比较

直接比较不同任务的欧氏子空间角度会受到表征各向异性影响。首先在 TRAIN 上计算叶类内协方差：

\[
W_{\mathrm{leaf}}
=
\sum_{c,f}\pi_{cf}
\operatorname{Cov}(H\mid C=c,F=f).
\]

使用 Ledoit–Wolf 收缩得到正定矩阵

\[
\widetilde W_{\mathrm{leaf}}.
\]

定义统一白化表示

\[
Z
=
\widetilde W_{\mathrm{leaf}}^{-1/2}(H-\mu).
\]

之后所有 coarse、fine 和 shared 子空间都在同一个 \(Z\) 坐标系中求解和比较。

这一白化的含义是：方向差异按叶类内部噪声尺度归一化，而不是被原始高方差轴支配。

---

## 11. 粗粒度判别子空间

记白化表示的全局均值为 \(\bar z\)，粗类条件均值为 \(\bar z_c\)。在统一白化空间计算

\[
B_C
=
\sum_c\pi_c
(\bar z_c-\bar z)(\bar z_c-\bar z)^\top.
\]

对 \(B_C\) 做特征分解：

\[
B_CQ_C=Q_C\Lambda_C.
\]

按特征值从大到小取前 \(r_C\) 个方向：

\[
S_C(r_C)=\operatorname{span}(Q_C[:,1:r_C]),
\qquad r_C\in\{1,\ldots,K_C-1\}.
\]

它等价于在统一 within-leaf metric 下求 coarse 类间/类内比最大的方向。主比较使用 DEV 选择的 \(r_{0.95}\)，同时完整报告全部 rank 曲线；全量八粗类时上限为 7，MVP 仅有数学/物理两粗类时上限为 1。

---

## 12. 父类条件细粒度判别子空间

固定父类 \(c\)，记白化表示中的细类均值为 \(\bar z_{c,f}\)，父类均值为 \(\bar z_c\)。定义

\[
B_{F\mid c}
=
\sum_f\pi_{f\mid c}
(\bar z_{c,f}-\bar z_c)
(\bar z_{c,f}-\bar z_c)^\top.
\]

分解：

\[
B_{F\mid c}Q_{F\mid c}
=
Q_{F\mid c}\Lambda_{F\mid c}.
\]

定义

\[
S_{F\mid c}(r)
=
\operatorname{span}(Q_{F\mid c}[:,1:r]),
\qquad r\in\{1,\ldots,K_F-1\}.
\]

这里的上限是 \(K_F-1\)，由分类标签结构决定，不作为实验发现；全量八分类时为 7，MVP 四分类时为 3。

---

## 13. 共享细粒度输入空间

正确的共享问题是：所有父类共用同一个输入投影，但每个父类拥有自己的分类头。

定义 pooled conditional-fine scatter：

\[
B_F^{\mathrm{pooled}}
=
\sum_c\pi_c B_{F\mid c}.
\]

其前 \(r\) 个特征向量构成候选共享空间：

\[
S_F^{\mathrm{shared}}(r).
\]

同时做一个多任务功能验证：

\[
\min_{P^\top P=I,\{A_c\}}
\sum_c
\mathcal L_c(Y_c,Z_cPA_c)
+\lambda\sum_c\|A_c\|_F^2.
\]

其中 \(P\in\mathbb R^{d\times r}\) 共享，\(A_c\) 为父类特异 head，

\[
r\in\{1,2,4,8,12,16,24,32,40,48,56\}.
\]

不再使用 64 作为有解释力的 rank，因为八个中心化八分类头的联合代数上限是 56。MVP 的两个父类、每父类四分类时，联合上限仅为 \(2\times(4-1)=6\)，对应 rank 网格改为 \({1,2,3,4,5,6}\)。

---

## 14. 子空间几何量

对正交基 \(Q_S,Q_T\)，定义归一化重合：

\[
\Omega(S,T)
=
\frac{\|Q_S^\top Q_T\|_F^2}
{\min(\dim S,\dim T)}
=
\frac{1}{\min(r_S,r_T)}
\sum_i\cos^2\theta_i.
\]

同时报告全部主角 \(\theta_i\)，不只报告一个平均百分比。

### 14.1 同任务复现度

对每个父类，将 TRAIN 按样本哈希分成 A/B 两半，独立估计：

\[
S_{F\mid c}^{A},
\qquad
S_{F\mid c}^{B}.
\]

定义

\[
\operatorname{Stab}_c
=
\Omega(S_{F\mid c}^{A},S_{F\mid c}^{B}).
\]

如果 \(\operatorname{Stab}_c\) 不显著高于随机基线，则该领域子空间本身不可识别，不能解释跨领域 overlap。

### 14.2 跨父类几何差异

比较

\[
\Omega(S_{F\mid c},S_{F\mid c'})
\]

与

\[
\sqrt{\operatorname{Stab}_c\operatorname{Stab}_{c'}}.
\]

只在 within-task stability 足够高时，才允许将较低 cross-task overlap 解释为任务特异性。

---

## 15. 功能迁移比几何重合更关键

对子空间 \(S_{F\mid c}\) 和目标父类 \(c'\)：

1. 用 \(S_{F\mid c}\) 投影父类 \(c'\) 的 TRAIN 表征；
2. 在投影后重新拟合一个属于 \(c'\) 的分类 head；
3. 在 \(c'\) 的 TEST-OOD 上评估。

定义

\[
T_{c\to c'}
=
\frac{
\operatorname{Perf}_{c'}(S_{F\mid c})-
\operatorname{Perf}_{c'}(S_{\mathrm{rand}})
}{
\operatorname{Perf}_{c'}(S_{F\mid c'})-
\operatorname{Perf}_{c'}(S_{\mathrm{rand}})
}.
\]

解释：

- \(T_{c\to c'}\approx1\)：源父类空间对目标父类同样有效，支持共享坐标；
- \(T_{c\to c'}\ll1\)：即使重新训练目标 head，源空间仍不能承载目标任务，支持父类特异输入空间。

该指标比直接拿两个不同标签体系的分类头互相测试更合理，因为它只检验输入空间是否可迁移。

---

## 16. 粗粒度与细粒度关系的四个直接对照

对每个父类 \(c\) 的细分类任务，比较：

1. **Full：**完整白化表示 \(Z\)；
2. **Coarse-only：**\(P_{S_C}Z\)；
3. **Coarse-residual：**\((I-P_{S_C})Z\)；
4. **Local-fine：**\(P_{S_{F\mid c}}Z\)；
5. **Shared-fine：**\(P_{S_F^{\mathrm{shared}}}Z\)；
6. **Random：**同维 Haar 随机空间。

所有条件都重新拟合相同的正则化分类 head；正则强度由 DEV 选择，TEST 只打开一次。

主要回答：

- coarse-only 是否包含 fine 信息；
- coarse-residual 是否删除了 fine 信息；
- local-fine 是否显著优于 shared-fine；
- local 优势能否跨模板泛化。

---

## 17. PCA 谱位置的正确画法

PCA 只用于回答“判别子空间落在总方差谱的哪一段”，不用于生成判别子空间。

在 TRAIN 全体表示上得到 PCA 基 \(V=[v_1,\ldots,v_d]\)。把 4096 个方向按排名划成 16 个等宽 bin，每 bin 256 维。对子空间 \(S\) 定义第 \(j\) 个 bin 的能量：

\[
e_j(S)
=
\frac{\|V_j^\top Q_S\|_F^2}{\dim S},
\qquad
\sum_{j=1}^{16}e_j(S)=1.
\]

该量对同一 bin 内的基旋转不敏感，比逐个 PCA 轴画单一权重更稳定。

必须同时画：

- \(S_C\)；
- 每个 \(S_{F\mid c}\) 的均值与区间；
- \(S_F^{\mathrm{shared}}\)；
- 随机同维空间。

“粗细位于同一谱段”只说明它们在方差排名上相近，不等于子空间方向重合；必须与 \(\Omega\) 联合解释。

---

# 第五部分：输出图与结果裁定

## 18. 必须输出的三张图

### 图 1：方法 sanity 图（合成数据）

四列对应 S1、S2、S3、碰撞反例；每列显示：

- 真值 coarse–fine overlap 与估计值；
- full/coarse/residual/local 的 fine TEST 性能；
- same-task stability 与 cross-task transfer。

目的：确认分析流程能区分已知几何，而不是先在真实数据上解释噪声。

### 图 2：真实数据主图

一个 2×2 面板：

- A：每个父类的 rank–TEST-OOD 性能曲线；
- B：same-task stability、cross-task overlap、随机基线；
- C：\(T_{c\to c'}\) 跨父类 transfer heatmap；
- D：Full / Coarse-only / Coarse-residual / Local / Shared 的细分类性能。

这张图直接回答“共享还是条件化”。

### 图 3：PCA 谱段图

按 16 个谱段画 \(S_C\)、\(S_{F\mid c}\)、shared fine 的能量分布。该图只解释位置，不承担主裁定。

---

## 19. 结果—认识—架构对应表

| 实验结果 | 允许的认识 | 架构选择 |
|---|---|---|
| local 子空间稳定；跨父类 transfer≈1；与 coarse 近正交；coarse-residual 不降 | 存在近似全局共享的 fine residual 空间 | 全局 common/coarse projector + 共享 residual Router |
| local 稳定；与 coarse 显著重叠；删除 coarse 明显伤害 fine | coarse/fine 共享方向，硬正交删除错误 | 保留父表示；条件化 gate；学习斜投影或交互特征 |
| local 稳定；cross transfer 低；shared rank 随父类数增长 | fine 坐标由父类决定，整体是局部空间并集 | 先父类路由，再使用父节点特异 projector 和 child experts |
| local 不稳定；跨模板性能接近随机 | 当前线性子空间对象不可识别 | 停止用静态线性几何设计 Router；先学习新表征或非线性 gate |
| 只在 TRAIN 成立，TEST-OOD 消失 | 模板/词汇记忆 | 数据或 split 失败，不讨论架构 |

---

## 20. 本轮 Pass / Fail / Insufficient

### Pass

至少获得以下一种稳定结构，并在 TEST-OOD 与第 28 层确认：

1. H1、H2、H3 中至少一个得到一致支持；
2. same-task stability 显著高于随机；
3. 几何结果与 coarse-removal / cross-transfer 的功能结果一致；
4. 结果不是由模板或词汇泄漏解释。

### Fail

- 预注册的 H1/H2/H3 均与功能结果不一致；或
- 条件化、residual、local/shared 无稳定区别。

此时应放弃“线性条件子空间决定 Router”的当前版本。

### Insufficient

- 合成 sanity 失败；
- 同任务子空间不可复现；
- TEST-OOD 线性可读性太低，无法估计关系；
- 数据缺少 concept/template 元数据；
- 不同方法给出矛盾结果且无法由误差条解释。

---

# 第六部分：导师架构的可执行还原

## 21. 会议中真正固定的部分

0824 与 0826 材料能够共同支持的内容只有：

1. 每个 expert 保持低秩；
2. 先学习一个所有数据共同使用的祖先/公共函数；
3. 祖先函数在后续阶段继续参与前向计算；
4. 新 expert 不应重复学习祖先已经解释的方向或函数；
5. 新 expert 用于隔离相互冲突的剩余模式；
6. 结构按 \(1\to2\to4\) 逐层扩展；
7. 需要先用小型一层 Transformer 同时构造 work 与 fail 条件。

会议材料对以下问题没有给出唯一答案：

- 父 expert 参数是永久冻结，还是仍允许慢速更新；
- common 子空间究竟由参数列空间、激活空间还是梯度空间定义；
- split 触发阈值是什么；
- learned gate 使用聚类中心、梯度效用还是分类器。

因此不能把任意一种细节写成“导师已经确定”。最一致的可执行解释是：

> **祖先 expert 保留在前向路径中，但在训练新 child 时 stop-gradient；child 的输入或梯度被限制为不重复祖先方向。**

这同时解释“界不能从模型输出中删除”与“门训练时要剔除界的梯度”。

---

## 22. 原始候选实现：全局 residual tree

根节点：

\[
E_0(h)=B_0\phi(A_0h),
\qquad
h_0=h+E_0(h).
\]

训练根节点收敛后，冻结 \(A_0,B_0\)，但保留 \(E_0(h)\) 的前向贡献。

定义祖先占用子空间的一个候选实现：

\[
C_0=\operatorname{col}(B_0),
\qquad
P_{C_0}=B_0(B_0^\top B_0)^\dagger B_0^\top.
\]

child 输入：

\[
r_0=(I-P_{C_0})(h-\mu).
\]

两个低秩 child：

\[
E_{1,j}(r_0)=B_{1,j}\phi(A_{1,j}r_0),
\qquad j\in\{1,2\}.
\]

输出：

\[
h^+
=h+E_0(h)+E_{1,g(r_0)}(r_0).
\]

进一步分裂时，对每个已有节点独立增加两个 child，并在累计祖先子空间的 residual 中训练。

这是对导师 0824 intuition 的最直接形式化，但它只有在 H1 近似成立时才合理。

---

## 23. 根据当前认识修正后的候选：父类条件 residual tree

若真实实验支持 H2/H3，则不能使用一个全局 residual gate。节点 \(\nu\) 应拥有自己的：

- 父节点身份或路径编码 \(e_\nu\)；
- 局部祖先空间 \(C_\nu\)；
- 局部 gate \(g_\nu\)；
- 两个局部 child experts。

定义

\[
r_\nu=(I-P_{C_\nu})(h_\nu-\mu_\nu).
\]

局部 gate 输入为

\[
\widetilde r_\nu=[r_\nu;e_\nu]
\]

或等价的父节点条件化函数，而不是把所有父类 residual 混在同一个全局池中。

节点更新：

\[
h_{\nu j}
=h_\nu+E_{\nu j}(\widetilde r_\nu),
\qquad
j=g_\nu(\widetilde r_\nu).
\]

如果 H2 显示 coarse/fine 重叠显著，还应将硬正交投影替换为学习的条件投影：

\[
r_\nu=M_\nu h_\nu,
\]

其中 \(M_\nu\) 通过“保留父类功能 + 最大化子类效用 + 抑制重复祖先功能”的目标联合学习，而不是强制 \(M_\nu=I-P_{C_\nu}\)。

---

# 第七部分：架构验证数据

## 24. 为什么真实表示审计与架构训练必须分开

当前真实数据实验回答：

> 粗、细判别几何是什么。

小模型训练实验回答：

> 在该几何成立时，某种树状训练机制能否利用它产生功能收益。

前者不需要训练新架构；后者只有在前者给出架构选择后才进入。不能用人为写入正交结构的合成数据替代真实几何结论。

---

## 25. 一层 Transformer 的最小验证数据

### 25.1 潜在变量

\[
c\in\{0,1\},
\qquad
f\in\{0,1\},
\qquad
q\in\{0,\ldots,7\},
\qquad
u_1,\nu_2\in\{0,\ldots,15\}.
\]

序列：

```text
<BOS> <TASK_t> <COARSE_c> <FINE_f> <PAYLOAD_q>
<N1_u1> <N2_u2> <QUERY> <ANSWER> <OUT_y> <EOS>
```

使用四种等概率 token 顺序模板，OOD 只使用未见模板和反转 nuisance 相关性，不引入未见 token。

### 25.2 三级目标

根任务：

\[
y_{\mathrm{root}}=q.
\]

粗任务：

\[
y_{\mathrm{coarse}}=(q+4c)\bmod 8.
\]

细任务：

\[
y_{\mathrm{fine}}
=(q+4c+2(f\oplus c))\bmod8.
\]

最后一式使细粒度映射依赖父类：同一个 \(f\) 在不同 \(c\) 下并不具有完全相同的功能含义。这是 H3 的最小 function-conflict benchmark。

### 25.3 对照数据

1. **Global-fine control：**
   \[
   y=(q+2f)\bmod8,
   \]
   fine 功能跨父类共享；
2. **No-fine-conflict control：**
   \[
   y=(q+4c)\bmod8,
   \]
   增加 fine experts 不应有收益；
3. **Overlap control：**将 coarse 与 fine cue 映射到部分共享的 embedding/feature 方向，硬 residual 删除应失败；
4. **Oracle gate：**先直接使用真实 \(c,f\) 选择 expert，隔离专家结构；oracle 成功后再研究 learned gate。

### 25.4 小模型

- 一层 pre-norm causal Transformer；
- \(d=64\)，4 个注意力头；
- root rank 8；
- 两个 coarse child，各 rank 4；
- 每个 coarse child 下两个 fine child，各 rank 2；
- Stage 1 训练 root；
- Stage 2 保留 root 前向并 stop-gradient，训练 coarse children；
- Stage 3 保留祖先路径并 stop-gradient，训练 fine children；
- 比较 global residual tree 与 parent-conditioned residual tree；
- 所有模型使用相同总参数、训练步数、oracle gate 和数据顺序。

### 25.5 主裁定

仅当 parent-conditioned data 中满足：

1. parent-conditioned tree 的 TEST-OOD NLL 显著低于 global residual tree；
2. Global-fine control 中两者差异消失；
3. No-fine-conflict 中 tree 不优于参数匹配 shared adapter；
4. 祖先任务输出不发生显著退化；

才允许声称：

> 父类条件依赖性，而非单纯增加参数，决定了层级 Router 的必要性。

---

# 第八部分：真正决定架构的数据特性

## 26. 唯一关键：父类条件依赖性

最终架构不应由“世界看起来有树状标签”决定，而应由以下数据特性决定：

> **细粒度判别坐标或条件函数，是否在不同父类之间保持不变。**

将其操作化为三个联合证据：

1. **局部稳定性：**同一父类的 \(S_{F\mid c}\) 在不同 split/seed 下可复现；
2. **跨父类迁移性：**\(T_{c\to c'}\) 是否接近 1；
3. **粗细重叠性：**删除 \(S_C\) 是否损失细粒度性能。

架构决策：

- 高迁移、低重叠 → 全局 residual Router；
- 高迁移、高重叠 → 共享但非正交的条件投影；
- 低迁移、局部稳定 → 父类特异层级 Router；
- 局部不稳定 → 不使用线性子空间架构。

这比“方差越大语义越粗”更直接，因为它对模型结构给出可证伪的选择。

---

# 第九部分：MVP 执行顺序

## 27. 次日 11 点前的最小闭环

### Step 1：30–45 分钟

实现合成向量 S1/S2/S3，验证：

- LDA/Fisher 求解；
- overlap；
- same-task stability；
- cross-transfer；
- coarse-residual 对照。

### Step 2：2–3 小时

在真实数据上只取：

- 数学、物理；
- 每类 4 个细类；
- Block 24；
- TEST-OOD 为主。

输出：

1. same-task vs cross-task overlap；
2. 2×2 cross-transfer matrix；
3. Full / Coarse / Residual / Local / Shared 性能；
4. 一个 16-bin 谱位置图。

### Step 3：停止并写结论

只回答：

> 当前结果更接近 H1、H2 还是 H3？

不在同一晚训练新 MoE、不扩到所有层、不调 learned gate。

### Step 4：仅在不稳定时追加

- Block 28；或
- 第二个数据 split。

不同时追加二者。

---

# 第十部分：修订后的 focus.md

## synthetic exp fine

### dxy

#### 0827

##### 当前唯一问题

在冻结的真实粗细粒度语义表征中，粗粒度判别子空间 \(S_C\) 与父类条件细粒度判别子空间 \(S_{F\mid c}\) 的关系是什么：

1. 全局共享且近似正交；
2. 与 coarse 显著重叠；
3. 随父类变化的局部坐标系。

该问题决定后续使用全局 residual Router，还是父类条件的局部 Router。

##### 先完成的勘误

“单领域八分类只需 7 维”不能证明局部语义空间是 7 维，因为任意中心化八分类线性头的秩都不超过 7；八个任务联合不超过 56 维也同样是代数上界。此前“不同领域需要不同子空间”的结论必须重新通过子空间稳定性和跨领域功能迁移验证。

##### 数据

1. 合成向量数据：构造正交共享、粗细重叠、父类特异三种已知子空间关系，用于验证分析算法；
2. 真实数据：已有 8 粗类×8 细类自然语言数据；主实验先取数学、物理各 4 个细类，使用 Block 24 的 \(R_U\)，Block 28 仅作确认；
3. 所有结论以未见模板 TEST-OOD 为主。

##### 判别子空间求解

1. 在 TRAIN 上计算叶类内 pooled covariance，并用 Ledoit–Wolf 收缩；
2. 在统一白化坐标中计算 coarse scatter \(B_C\) 与 conditional-fine scatter \(B_{F\mid c}\)；
3. 取对应特征向量构成 \(S_C\) 和 \(S_{F\mid c}\)；
4. 用 ridge/logistic probe 在 DEV 选择正则，在 TEST-OOD 验证投影后的功能；
5. 不把 \(K-1\) 的分类头秩上限解释成表示内在秩。

##### 必须计算的量

1. 同一任务 split-half 子空间复现度；
2. coarse–fine 和 fine–fine 主角/归一化 overlap；
3. 跨父类输入子空间 transfer：用源父类子空间投影目标父类，再重新训练目标 head；
4. Full、Coarse-only、Coarse-residual、Local-fine、Shared-fine、Random 的留出性能；
5. 判别子空间在 16 个 PCA 谱段中的能量分布。

##### 必须输出的主图

一个 2×2 面板：

- rank–TEST-OOD 性能；
- same-task stability vs cross-task overlap；
- cross-transfer heatmap；
- Full/Coarse/Residual/Local/Shared 对照。

PCA 谱段图只作解释，不承担结论。

##### 可能结论

- local 稳定、跨父类 transfer 高、与 coarse 近正交：支持全局 residual Router；
- local 稳定、与 coarse 重叠且去 coarse 性能下降：支持保留父上下文的条件投影；
- local 稳定、跨父类 transfer 低：支持父类特异层级 Router；
- local 不稳定或 OOD 不可读：否定当前线性条件子空间路线。

##### 停止规则

完成 Block 24、两个父类、一个 split 后若结论清晰，立即停止扩展并写认识更新；不在本轮训练完整 MoE。

---

# 最终 next-meeting problem

> **在真实自然语言表征中，细粒度判别信息是否是父类条件化的局部低维功能，而不是一个可由全局 coarse-removal 暴露的统一 residual 子空间？**

# 最小实验雏形

> 先用已知真值的合成向量验证子空间分析方法；再在 Qwen 第 24 层、数学/物理各四个细类上，比较 coarse、coarse-residual、local fine 与 shared fine 子空间的 OOD 功能、复现度、主角重合和跨父类迁移。结果直接选择全局 residual、重叠条件投影或父类特异 Router 三种架构之一。

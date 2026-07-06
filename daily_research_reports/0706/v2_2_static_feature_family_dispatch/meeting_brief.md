# paper V2.2 静态特征家族分发

## 0. 执行摘要

**研究问题：** 在整体表示谱近似各向同性、特征家族频率均匀的受控分布中，是否能构造一个无标签静态路由器，使专家负载均衡并保持同一特征家族不被切碎。

**机制解释：** 谱各向同性只提供干净的距离度量；特征家族的局部可恢复性提供可识别的家族身份；频率均匀提供按家族均分后得到负载均衡的质量条件。

**核心公式：**

1. 受控特征分布：

$$
F\sim\mathrm{Unif}(\{1,\ldots,K\}),\qquad
X\mid F=k=\mu_k+\epsilon,\qquad
\operatorname{Cov}(\widetilde X)\approx I_d.
$$

2. 无标签恢复与静态路由：

$$
\mathbb{P}(\widehat h(X)\neq F)\leq\eta,\qquad
g(X)=a(\widehat h(X)).
$$

3. 负载均衡与家族完整性：

$$
\mathbb{P}(g(X)=e)\approx 1/E,\qquad
C_{\mathrm{fam}}=\frac1K\sum_{k=1}^K\max_e\mathbb{P}(g(X)=e\mid F=k).
$$

**主要结果：** V2.2 支持一个受控静态结论：在谱平、频率均匀、局部可恢复三条件同时成立时，BFSR 可以构造保持特征家族且负载均衡的静态分发；仅有谱各向同性不能自然构造特征专门化路由。

**证据说明：** 关键指标同时检查负载和家族完整性：LoadCV 衡量专家负载是否均匀，family consistency 衡量同一家族是否主要进入同一专家，cluster accuracy 衡量无标签恢复是否正确。当前 V2.2 产出中：

1. E1 显示三条件成立时，BFSR-Cluster 达到 LoadCV 0.003、family consistency 0.990、cluster accuracy 0.986。
2. E2 和 E3 显示谱各向同性单独不能产生特征分发，local recoverability 才决定 specialization 质量。
3. E4 和 E5 显示 whitening 只是 metric repair；频率不均匀时，需要按 estimated family mass 分配才能恢复负载均衡。

**结论边界：** 当前证据不支持真实语言模型 hidden states 已满足这些条件，也不支持训练保持、专家效用、learned router 动态或自动选择特征家族数。

**执行动作：** 下一步最小动作不是再问是否存在 gradient signal，而是解释 A06_27 embedding-gradient 正结果为什么成立：梯度能量是否选中 route position，梯度方向是否提供 feature identity，正 margin 是否解释训练保持。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算方式 | 单位或公式 | 为什么影响当前判断 | 不能证明什么 |
|---|---|---|---|---|---|
| 特征家族 | 应该稳定进入同一专家的潜在特征类别 | 受控数据中的 latent family $F$ | $F\in\{1,\ldots,K\}$ | 判断路由是否保持同类样本 | 真实语义专家 |
| 谱各向同性 | 整体表示没有主导方差方向 | 白化或中心化后检查 $\operatorname{Cov}(\widetilde X)\approx I_d$ | 协方差条件 | 给聚类提供干净距离度量 | feature family identity |
| 局部可恢复性 | family 在表示空间中能被无标签方法恢复 | 聚类恢复 $\widehat h(X)$ 后与 $F$ 比较 | cluster accuracy | 决定 specialization 是否可识别 | 训练收益 |
| Feature NMI | 特征编号和路由专家的一致度 | NMI(feature id, selected expert) | $0$ 到 $1$ | 判断 feature 是否被分开 | expert utility |
| Margin p05 | 路由间隔的低分位安全垫 | matched expert score 减去最强 competing expert score 的第 5 百分位 | logit difference | 判断分区是否有训练保持安全垫 | 最优性或真实收益 |
| 梯度能量 | 某个 hidden state 对 loss 的影响强度 | $E_{i,p}=\|\nabla_{h_{i,p}}\mathcal L_i\|_2^2$ | 非负数 | 判断任务相关位置能否无标签被选中 | 语义 feature identity |
| LoadCV | 专家负载变异系数 | expert mass 的标准差除以均值 | 越低越均衡 | 判断负载是否均匀 | family 是否完整 |
| Family consistency | 同一 family 是否主要进入同一专家 | $C_{\mathrm{fam}}=\frac1K\sum_{k=1}^K\max_e\mathbb{P}(g(X)=e\mid F=k)$ | $0$ 到 $1$ | 判断 family 是否被切碎 | expert utility |
| BFSR | 平衡特征专门化路由 | normalize -> cluster -> assign -> route | 静态构造流程 | 当前方法产出 | learned router |

## 2. 机制解释与建模

**核心模型：**

1. 受控特征分布：

$$
F\sim\mathrm{Unif}(\{1,\ldots,K\}),\qquad
X\mid F=k=\mu_k+\epsilon,\qquad
\operatorname{Cov}(\widetilde X)\approx I_d.
$$

2. 无标签恢复与静态路由：

$$
\mathbb{P}(\widehat h(X)\neq F)\leq\eta,\qquad
g(X)=a(\widehat h(X)).
$$

3. 负载均衡与家族完整性：

$$
\mathbb{P}(g(X)=e)\approx 1/E,\qquad
C_{\mathrm{fam}}=\frac1K\sum_{k=1}^K\max_e\mathbb{P}(g(X)=e\mid F=k).
$$

**符号含义：**

- $F$：潜在特征家族。
- $K$：特征家族数量；$E$：专家数量。
- $X$：路由器读取的表示向量。
- $\mu_k$：第 $k$ 个特征家族的中心；$\epsilon$：家族内扰动。
- $\widetilde X$：谱归一化后的表示向量。
- $\eta$：无标签恢复 family identity 的错误率上界。
- $G=g(X)$：静态路由器输出的专家编号。
- $\widehat h(X)$：无标签恢复出的特征家族编号。
- $a(\cdot)$：把 recovered family 分配到 expert 的映射。
- $C_{\mathrm{fam}}$：同一 family 被集中分到同一 expert 的平均程度。

**机制链条：**

1. 谱各向同性控制距离度量，使聚类不被全局强方差方向扭曲。
2. 局部可恢复性使无标签聚类能够恢复 feature family identity。
3. 频率均匀使 recovered families 均衡分配给 experts 后得到近似负载均衡。

**当前问题分解：**

- 需要判定的是三条件是否足以构造 balanced and coherent 的静态分发。
- 最危险的替代解释是：负载均衡或谱各向同性本身已经足够。
- 当前实验能区分静态几何机制，不能区分真实训练目标下的 feature center 是否存在。

## 3. 主要结果

**一句话总结：** V2.2 关闭了受控静态 clean case：BFSR 在三条件同时成立时有效，移除关键条件时出现可预测失败。

### 结果 1：三条件同时成立时，静态特征家族分发可以被构造。

**机制对应：** 对应“谱控制 + 局部可恢复 + 频率均匀”的完整机制链条。

**指标或条件定义：** E1 是 positive clean case；LoadCV 越低表示负载越均匀，family consistency 越高表示 family 越完整。

**证据：** E1 中 BFSR-Cluster 达到 LoadCV 0.003、family consistency 0.990、cluster accuracy 0.986。

**解释：** 低 LoadCV 和高 family consistency 同时成立，说明该方法不是只平衡 token 数，而是在保持 family 的同时平衡 experts。

**边界：** 该结果只覆盖受控静态分布，不证明训练中保持或真实语言模型收益。

**来源：** `papers/spectral_partition_router_v2_2/exp/results/summary.md`；`papers/spectral_partition_router_v2_2/AUDIT_2026_07_06.md`。

### 结果 2：谱各向同性单独不能定义 feature family identity。

**机制对应：** 对应第 2 节中“谱各向同性只控制 metric，不提供 family identity”的环节。

**指标或条件定义：** E2 是 isotropy-only null；expert information fraction 衡量 expert id 携带多少 family 信息。

**证据：** 在 $X\sim\mathcal N(0,I_d)$ 且 $F\perp X$ 的条件下，label-free 方法的信息量约为 0.002。

**解释：** 当表示中没有可恢复 family 结构时，谱再均匀也无法让路由器恢复 family identity。

**边界：** 该结果不排除其他带任务信号的 center 发现方法。

**来源：** `papers/spectral_partition_router_v2_2/PROBLEM_STATEMENT.md`；`papers/spectral_partition_router_v2_2/exp/results/summary.md`。

### 结果 3：可恢复性和频率均匀分别控制 specialization 与 mass balance。

**机制对应：** 对应第 2 节中“local recoverability”和“frequency uniformity”的两个条件。

**指标或条件定义：** E3 扫描 family separation；E5 破坏 family frequency uniformity。

**证据：** E3 中 separation 从 0.45 到 2.50 时，cluster accuracy 从 0.063 到 0.942，family consistency 从 0.294 到 0.956。E5 中频率不均匀时，equal-number BFSR 的 LoadCV 为 0.149，mass-aware BFSR 降到 0.029。

**解释：** family 越可恢复，specialization 越好；family 频率不均匀时，按 family 数量均分不再等价于按 mass 均分。

**边界：** 该结果不说明 $K$ 能自动选择，也不说明真实 hidden states 已满足 local recoverability。

**来源：** `papers/spectral_partition_router_v2_2/RESEARCH_PLAN.md`；`papers/spectral_partition_router_v2_2/exp/results/summary.md`。

## 4. 执行动作

**下一步动作：** 围绕 A06_27 的 embedding-gradient 正结果写一个机制审计：解释梯度为什么能选中 route-relevant states，并判断它能否从“位置选择”推进到“稳定 feature identity”。

**目的：** 区分三种解释：梯度能量只是在找监督 route position；梯度方向携带 feature identity；正 margin 才是训练后保持的直接原因。

**完成判据：** 在同一 uniform no-position bridge 中，报告 embedding-gradient top1/direction、all-position、route-position、Fisher-only 的 Feature NMI、Margin p05、matched preserve 和 signal role share；若 A06_27 的 warmup-40 结论能由明确机制链解释，再进入 margin-thickened gradient-selector 方法；否则只保留 synthetic route-state selector claim。

## 5. 证据索引

| 结果 | 证据 | 主要指标或图 | 支持什么 | 不能证明什么 | 来源 |
|---|---|---|---|---|---|
| 结果 1 | E1 clean case | LoadCV 0.003；family consistency 0.990；cluster accuracy 0.986 | 三条件成立时 BFSR 有效 | 训练收益 | `exp/results/summary.md` |
| 结果 2 | E2 isotropy-only null | expert information fraction 约 0.002 | 谱各向同性单独不够 | 所有任务相关方法失败 | `exp/results/summary.md` |
| 结果 3 | E3/E5 ablation | recoverability sweep；frequency ablation | 可恢复性和频率均匀分别控制不同环节 | 真实 hidden states 和自动选 $K$ | `AUDIT_2026_07_06.md` |
| 下一步桥接 | A06_27 gradient selector | warmup-40 embedding-gradient top1: Feature NMI 1.000；Margin p05 10.083；final Feature NMI 1.000 | 梯度能选中 route-relevant population | real-DCLM、语义专家或 expert utility | `A06_27_gradient_fisher_route_state_selector/summary.md` |

## 6. 来源索引

**Anchor：** `papers/spectral_partition_router_v2_2/PROBLEM_STATEMENT.md`

**Protocol：** `papers/spectral_partition_router_v2_2/exp/EXPERIMENT_PLAN.md`

**Summary：** `papers/spectral_partition_router_v2_2/exp/results/summary.md`

**Detailed：** `papers/spectral_partition_router_v2_2/AUDIT_2026_07_06.md`

**Figures：** `papers/spectral_partition_router_v2_2/latex/figures/`

**Related mechanism note：** `Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/soft_router_topk_mechanism_note_cn.md`

**Gradient next-step source：** `Projects/from-attention-to-search/main/experiments/A06/A06_27_gradient_fisher_route_state_selector/summary.md`；`Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_27_gradient_fisher_route_state_selector_anchor.md`

## 7. 补充材料

### 组会汇报稿

1. 问题先说清楚：当前 V2.2 处理的是一个受控静态问题。给定均匀出现的特征家族和近似谱各向同性的表示，目标不是只让专家负载均衡，而是让同一个特征家族尽量进入同一个专家。

2. 机制用三条公式讲。第一条是数据设定：$F$ 均匀采样，$X\mid F=k=\mu_k+\epsilon$，并且归一化后 $\operatorname{Cov}(\widetilde X)\approx I_d$。这说明谱条件只是在清理距离度量。第二条是恢复和路由：如果 $\mathbb{P}(\widehat h(X)\neq F)\leq\eta$，就可以用 $g(X)=a(\widehat h(X))$ 把恢复出的家族分到专家。第三条是判断标准：$\mathbb{P}(g(X)=e)\approx 1/E$ 看负载，$C_{\mathrm{fam}}$ 看同一家族有没有被切碎。

3. 结果可以概括成一句话：三条件同时成立时，BFSR 能构造保持特征家族且负载均衡的静态分发；但只有谱各向同性不够。E1 同时得到低 LoadCV 和高 family consistency；E2/E3 说明真正决定 specialization 的是 family 可恢复性；E5 说明频率不均匀时必须按 family mass 分配。

4. 边界要说清楚：这关闭的是受控静态 clean case，不等于真实语言模型 hidden states 已满足条件，也不等于专家已经有训练收益。它解决的是“几何上能不能构造 balanced and coherent dispatch”，不是最终的 functional specialization。

5. 下一步十秒：gradient 线已经有明确正结果。A06_27 中 embedding-gradient selector 在 warmup 40 达到 Feature NMI 1.000、Margin p05 10.083、final Feature NMI 1.000。所以下一步不是再问有没有 gradient 信号，而是解释它为什么成立：是梯度能量选中了 route-relevant position，还是梯度方向提供了 feature identity，或者是正 margin 让这个分区能被训练保持。

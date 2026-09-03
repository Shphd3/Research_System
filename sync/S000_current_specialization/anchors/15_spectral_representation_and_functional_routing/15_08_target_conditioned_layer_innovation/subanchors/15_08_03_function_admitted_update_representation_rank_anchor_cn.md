---
anchor_id: 15_08_03_function_admitted_update_representation_rank
status: COMPLETED_INSUFFICIENT_BASIS_SENSITIVE_HREP_FAIL
canonical_companion: 15_08_03_function_admitted_update_representation_rank_anchor.md
parent_anchor: ../15_08_target_conditioned_layer_innovation_anchor_cn.md
depends_on: 15_08_02_layerwise_conditional_fine_added_accessibility_anchor_cn.md
parent_line: 15_spectral_representation_and_functional_routing
execution_authority: APPROVED_AND_COMPLETED_FULL_ANALYSIS
created: 2026-08-16
updated: 2026-08-16
---

# A15_08_03：跨层功能准入更新的参数谱位置与表征低秩性

父问题见 [A15_08](../15_08_target_conditioned_layer_innovation_anchor_cn.md)。功能前置门见 [A15_08_02](15_08_02_layerwise_conditional_fine_added_accessibility_anchor_cn.md)。英文正式版本见 [Canonical Anchor](15_08_03_function_admitted_update_representation_rank_anchor.md)。

## 1. Problem Definition

本子 Anchor 只问一个条件问题：

> 不同预注册层的 conditional-fine 新增可访问性、参数谱能量位置、父类内 residual-update 表征秩和 token 几何有何差别；深层是否同时表现为功能增强与公共参数谱后移，哪些具名层又由稳定低维表征承载该增益？

“参数谱位置”指父类内中心化 $R_U$ 的归一化方差能量在 MLP 强响应到弱响应参数方向中的位置；它不定义新增信息。“表征秩”指更新激活点云自身的维数集中程度，不是八分类判别器受标签自由度限制的任务秩。“稳定”指 TRAIN 冻结的子空间不重新拟合，就能在表达互斥的 DEVELOPMENT 和 CONFIRMATION 上保留几何。主要交付是完整跨层剖面：A15_08_02 的逐层净收益、本层 MLP 谱最大能量带、冻结公共参数谱位置、逐层表征秩以及层—层 token 几何 CKA。所有合格 block 的谱和投影增益曲线都必须在打开 CONFIRMATION 前预注册；只有通过功能门的层可以获得任务相关解释。

这是最小的下一决策：更新对象精确后才能谈 covariance/PCA；要把低秩解释为任务相关，还必须先有新增可访问性。Router 效益不在本 Anchor 内。

## 2. Physical Priors

1. **本层谱与公共谱承担不同角色。**本层 MLP 谱说明更新相对该层自身参数响应落在哪里；冻结公共参数谱才提供跨层同一坐标。任一谱位置都只是参数几何，不能替代同一 $X$ 功能增益。
2. **表征秩来自 token 维度的联合变化。**若更新点云低维，完整协方差的特征值能量应集中，TRAIN 冻结主子空间应在未见表达上保留方差；逐方向参数谱能量不能回答这一问题。
3. **高方差不自动等于任务相关。**只有 PCA 子空间保留已准入的同一 $X$ 留出增益并超过同秩随机空间，才允许加上任务相关解释。

## 3. Falsifiable Hypotheses

**H-DEPTH-SPEC — 功能增强伴随公共参数谱后移。**在预注册浅层和深层总体对比中，深层 $T_\ell$ 更大，且同一冻结 Mean Response 参数基中的 $R_U$ 归一化谱质心更靠后。两部分必须分别通过；本层最大能量带后移只作机制侧描述。

**H-REP — 稳定低秩更新表征及功能保留。**至少一个功能准入层的父类内 residual-update 谱相对样本可识别秩高度集中；TRAIN 冻结 PCA 在两个留出 split 复现；少量方向还保留 full update 至少 80% 的 conditional-fine 增益并超过同秩 Haar。

**最强竞争解释 R-GEO/NUIS — 几何重分配或 nuisance 集中。**公共谱后移可能只在 Mean Response 基中出现而没有功能增强；本层最大带可能因坐标随层变化而移动；表面低秩也可能来自 $n<d$、模板/尺度结构或单一 split covariance 噪声。这一竞争解释预测：功能与谱位置不共同变化、另一公共基不同号、留出低秩不复现，或 PCA 无法保留功能增益。

`REGISTERED`：用预注册浅层—深层中位数差裁定 H-DEPTH-SPEC；Mean Response 为主公共坐标，Rank Consensus 只检查基敏感性；最大能量带作描述，完整谱质心为主位置量。另用 $r_{80}^{rep}/(n-P)\le0.10$ 定义实际紧凑性，要求两个留出 split 至少保留 75% 方差，并要求至少 80% 功能保留且超过同秩 Haar q95。这些定义和阈值已于 2026-08-16 获得批准并在打开 CONFIRMATION 前冻结。

若 A15_08_02 得到 $\mathcal L^+=\varnothing$，全层谱与聚类只能作描述，本 Anchor 的功能低秩 verdict 不被激活。尽管如此，投影增益仍需对所有合格层提前冻结并计算，不能用 $\mathcal L^+$ 在确认后选择分析方法。

## 4. Mathematical Model

对父类为 $p(i)$ 的样本 $i$，$R_{U,\ell,i}\in\mathbb R^d$ 是 A15_08_02 已冻结的同 token residual update。只去除 TRAIN 父类公共均值：

$$
\widetilde R_{\ell,i}=R_{U,\ell,i}-\mu^{tr}_{\ell,p(i)}.
$$

每层本地 MLP 输入侧参数算子及其强到弱响应谱为

$$
K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}
+W_{up,\ell}^{\top}W_{up,\ell}
=B_\ell\Gamma_\ell B_\ell^\top.
$$

将 $B_\ell$ 按 rank 分成16个等宽带。投影方差在带 $b$ 的总和 $E^{local}_{\ell,b}$ 定义本层激活，$\arg\max_bE^{local}_{\ell,b}$ 是最大能量带；不同层本地带只共享相对 rank，方向身份不同。

跨层公共坐标使用已冻结 Mean Response 基 $B^{MR}$，即对所有 $K_\ell/\operatorname{tr}(K_\ell)$ 等层平均后特征分解。Rank Consensus 基 $B^{RC}$ 则对每层本地等秩带 projector 作排序加权平均，保留跨层秩共识但丢弃参数响应幅度，只作敏感性对照。对视角 $v\in\{local,MR,RC\}$，令方向归一化能量为 $p^v_{\ell,j}$、归一化 rank 为 $\rho_j$，谱质心为

$$
C^v_\ell=\sum_jp^v_{\ell,j}\rho_j.
$$

`REGISTERED`：预注册浅层集合 $\mathcal E$ 与深层集合 $\mathcal D$，分别计算

$$
\Delta_T=\operatorname{median}_{\ell\in\mathcal D}T_\ell-
\operatorname{median}_{\ell\in\mathcal E}T_\ell,
\qquad
\Delta_C^{MR}=\operatorname{median}_{\ell\in\mathcal D}C^{MR}_\ell-
\operatorname{median}_{\ell\in\mathcal E}C^{MR}_\ell.
$$

$\Delta_T$ 测功能增强，$\Delta_C^{MR}$ 测该公共参数坐标中的谱后移；任一量都不能替代另一量。原始总投影能量另行报告，但只表示更新幅度，不是新增信息量。

将 TRAIN 行堆成 $M_\ell^{tr}\in\mathbb R^{n\times d}$ 并做 SVD；等价的完整中心化 covariance 为

$$
C_\ell^{tr}=\frac{1}{n-P}(M_\ell^{tr})^\top M_\ell^{tr}
=V_\ell\Lambda_\ell V_\ell^\top.
$$

令 $p_{\ell,j}=\lambda_{\ell,j}/\sum_k\lambda_{\ell,k}$，表征 effective rank 与 80% 方差秩为

$$
r_{eff,\ell}^{rep}=\exp\left(-\sum_jp_{\ell,j}\log p_{\ell,j}\right),
$$

$$
r_{80,\ell}^{rep}=\min\left\{r:\sum_{j\le r}p_{\ell,j}\ge0.8\right\}.
$$

冻结 TRAIN projector $P_{\ell,r}=V_{\ell,r}V_{\ell,r}^\top$。它在留出 split $s$ 的表征保留率为

$$
V_{\ell,r}^{s}
=\frac{\operatorname{tr}(P_{\ell,r}C_\ell^{s})}
{\operatorname{tr}(C_\ell^{s})}.
$$

对每个合格层，把 $R_U$ 投到 $P_{\ell,r}$，只按 TRAIN/DEVELOPMENT 纪律重拟合 correction，并计算 $G_{\ell,r}^{PCA}$。功能充分性为

$$
D_{\ell,r}^{func}=G_{\ell,r}^{PCA}-0.8G_{\ell,full},
$$

同时使用配对留出不确定性与同秩 Haar correction 对照。该任务量不能替代 $r_{80}^{rep}$ 作为表征秩定义。

跨层 token 几何比较不依赖公共基：对同序样本构造父类内中心化 token Gram 矩阵 $G_\ell=M_\ell M_\ell^\top$，计算 linear CKA：

$$
CKA(\ell,m)=
\frac{\langle HG_\ell H,HG_mH\rangle_F}
{\|HG_\ell H\|_F\,\|HG_mH\|_F}.
$$

$H$ 对 token 行中心化。CKA 比较两层是否产生相似的 token—token 更新几何，不要求公共参数基或逐主成分配准；它不测低秩，也不测功能增益。

## 5. Computational Realization

1. 复用 A15_08_02 的样本顺序、split manifest、token site 和 $R_{U,\ell}$。两个 Protocol 都必须在打开 CONFIRMATION 前冻结，并共享一次 model forward；不能看完 A15_08_02 的正层后才加入 A15_08_03。
2. 每层每个 split 都减去 TRAIN 父类均值；不减 child 均值，因为 child 差别正是 conditional-fine 对象的一部分。
3. 在样本空间中做 SVD，避免显式形成 $4096\times4096$ 稠密矩阵。可识别秩上限是 $n-P$ 而非 4096；每个秩同时除以该上限汇报。
4. PCA 方向与候选秩只从 TRAIN 冻结。DEVELOPMENT/CONFIRMATION 只投影和汇报，不能重新旋转或排序方向。
5. `REGISTERED`：使用 512 个逐坐标独立打乱 token 行的 null；它保留每个坐标的边际分布，但破坏跨坐标的 token 联合变化。
6. 对同一个父类内中心化 $R_U$，先计算每层本地 $K_\ell$ 的16带能量、最大能量带和谱质心；再计算冻结 Mean Response 与 Rank Consensus 公共基中的完整能量谱和谱质心。参数基不从语义标签或 CONFIRMATION 中选择。
7. 将全层 $T_\ell$、本地谱位置、两种公共谱位置、normalized $r_{eff}^{rep}$、$r_{80}^{rep}$、留出方差保留率和 linear-CKA heatmap 并列展示。只有 $T_\ell$ 属于新增信息判据，其余面板属于参数或 token 几何。
8. 对每个合格层，在可识别秩范围内评估 $r\in\{1,2,4,8,16,32,64,128,256,512\}$，报告通过 80% 功能保留的最小秩，并逐秩比较同秩 Haar；只有与 $\mathcal L^+$ 的联合交集获得任务相关解释。
9. token 级辅助分析：在 $r_{80}^{rep}$ 的 TRAIN PCA 坐标中，按父类分别拟合 $k=8$ k-means；中心冻结后应用到留出 split；报告重采样稳定性和 child 标签 ARI/NMI，并与同秩 Haar、父类内标签置乱比较。聚类不能改变 H-REP。

## 6. Minimal Falsification Tests

H-DEPTH-SPEC 的决定性比较是：$\Delta_T$ 与 $\Delta_C^{MR}$ 的同时 95% 区间下界均大于零；若 Rank Consensus 未通过同一正向判据，类型标记为 `BASIS_SENSITIVE`，不得声称基不变后移。最大本地能量带不进入 Pass。

H-REP 的决定性比较是：至少一个层同时通过 A15_08_02 正新增可访问性、表征紧凑、冻结留出几何和功能保留。所有层、谱带与候选秩必须在打开 CONFIRMATION 前进入规则。

`REGISTERED` **Pass — `STABLE_FUNCTION_RETAINING_LOW_RANK_UPDATE`：**$r_{80}^{rep}/(n-P)\le0.10$；真实 $r_{80}^{rep}$ 小于坐标置乱 q05；TRAIN projector 在 DEVELOPMENT 和 CONFIRMATION 各保留至少 75% 方差；且某个注册 $r$ 的 $D_{\ell,r}^{func}$ 配对 95% 下界为正，并超过同秩 Haar q95。

H-DEPTH-SPEC 分别报告 `FUNCTION_ONLY`、`SPECTRAL_SHIFT_ONLY`、`BOTH` 或 `NEITHER`；只有 `BOTH` 支持原联合假设。H-REP 的 **Fail — `REPRESENTATION_OR_FUNCTION_NOT_LOW_RANK`：**存在有效功能正收益层，但每一层都明确排除了至少一个联合条件：紧凑性、留出几何或 80% 功能保留。Fail 必须指出失败条件，不能只写“PCA 失败”。

**Insufficient：**没有功能正收益层；covariance trace 可忽略；有限样本/split guard 失败；关键区间跨零；PCA 方向或秩泄漏留出真值；或必要数组/provenance 缺失。

聚类不稳定不能制造 H-REP Fail，稳定聚类也不能挽救表征或功能充分性失败。

## 7. Current Evidence

1. 0813 组会因为旧分析丢失同 token 配对和方向间联合变化，形成“同 token 变化 → 中心化 covariance → PCA → token 聚类”的方法链；同时明确 PCA 只能证明几何压缩，不能单独证明新增任务信息。该边界见[合并会议记录](/daily_research_reports/backup/2026/08/0813/meeting_notes/0813_meeting_merged_clean_record_cn.md)。
2. [A15_02_05](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_05_E01_balanced_taxonomy_attention_write_atlas/summary.md) 没有得到稳定 fine-specific 本地秩后移，但没有计算当前父类内 $R_U$ covariance 或冻结 PCA 的留出保留率。
3. [A15_08_E04](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/summary.md) 的两个注册目标方向只保留一次局部 full gain 的 33.24%。它排除了直接假定 rank two，但属于另一目标的任务检索结果，不是表征秩测量。
4. 既有 Attention-write 结果在 Mean Response 基中显示 basis-conditioned 后移，而 Rank Consensus 未复现，且相邻层变化非单调；它说明必须保留公共基敏感性对照，不能继承为当前 $R_U$ 结论。该边界见 [0813 会议知识更新](/daily_research_reports/backup/2026/08/0813/focus_meeting_common_basis_attention_write.md)。
5. [A15_08_03_E01](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_03_E01_function_admitted_update_spectral_rank_analysis/summary.md) 已于 2026-08-16 按冻结 Protocol 完成。A15_08_02 给出的功能准入层为 $\mathcal L^+=\{24,28\}$。浅层 2--12 与深层 25--35 的功能中位差 $\Delta_T=-0.0046$，同时区间跨零；Mean Response 的 $\Delta_C=0.0285$ 为正，而 Rank Consensus 的 $\Delta_C=-0.0397$ 为负，因此联合结果为 `INSUFFICIENT_BASIS_SENSITIVE`。
6. 没有一层通过 H-REP 的稳定表征低秩四项合取。block 24/28 的 $r_{80}$ 分别为 149/106，但 TRAIN 子空间在 CONFIRMATION 仅保留 42.1%/54.6% 方差。两层的功能保留均在最小注册秩 256 通过；这说明功能可压缩到 256 维，不等于更新云整体稳定低秩。
7. 三切分完整 35×35 CKA 和聚类均已完成，但只作辅助几何。CKA 有放回 percentile 区间受到重复 token 抬高 Gram 相似度的校准警告，不用于认定层间断点；block 24/28 聚类 ARI 也未超过同秩 Haar q95。

## 8. Claim Boundary And Next Decision

H-DEPTH-SPEC 的 `BOTH` 最多说明：在当前模型、对象、任务、深度窗口和冻结公共参数坐标中，conditional-fine 净收益整体增强且归一化参数谱位置整体后移。H-REP Pass 最多说明：某个具名功能准入层的父类内 residual-update 点云谱集中，少量 PCA 方向在未见表达上保留大部分注册增益。CKA 可以描述哪些层共享 token 几何；聚类可以描述稳定 child 富集。

它不能把谱后移单独称为新增信息增加，不能把本层同 rank 称为跨层同一方向，也不能证明 PCA 方向是模型原生 feature、表征在样本总体外内禀秩恰为 $r$、cluster 就是 expert，或 Router 会改善。它也不能把 $\mathcal L^+$ 之外的纯几何低秩层改称为任务相关新增信息。

**唯一下一决策：**是否对 blocks 24、28 的 TRAIN-frozen rank-256 功能保留空间进行独立的冻结因果干预或 Router 效用检验。现有实验不能回答模型原生使用或分发收益，且不会自动授权该后续。

**完成条件：已满足。**中英文 Anchor 与 canonical Protocol 已同步；参数基、谱带、深度窗口、数据、null、秩、统计不确定性和 A15_08_02 张量复用合同均有收据与归档产物。

**恢复动作：**无需重跑本实验。后续引用时必须分开写：功能新增层为 24、28；公共谱后移为 basis-sensitive；稳定表征低秩未通过；功能仅能准确写为“最小注册通过秩 256”。

# Summary: A15_08_07_E01 CLINC150 逐层新增可访问性与 PCA 功能秩

Primary Anchor: [A15_08_02](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_02_layerwise_conditional_fine_added_accessibility_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status: `ELIGIBLE_AI_DRAFT_AWAITING_DXY_JUDGMENT`

## Result Snapshot

**注册裁定：**`FAIL_ALL_LAYERS_NONPOSITIVE`。

在 CLINC150 的“已知 domain、预测其内部 15 个 intent”任务上，block 2--36 的完整、正确配对 \(R_{U,\ell}\) 都没有超过同预算的 null envelope。35 个 block 的 simultaneous 95% 上界全部小于 0，因此正集合为

\[
\mathcal L^+_{\mathrm{CLINC}}=\varnothing.
\]

这次新数据上没有恢复出功能定义下的“涌现层”。由于任何层的 full-\(R_U\) 都没有先通过功能准入，所有层的 \(r_{G80}\)、\(r_{G90}\) 均为 `NA_NO_FULL_ADMISSION`，而不是“超过 512 维”。

## 目的

检验两件有依赖顺序的事：

1. 换成具有 domain--intent 结构的真实意图数据后，哪一层的 Attention 精确更新能在旧状态之外增加细粒度 intent 的线性可访问性？
2. 只有某层先通过上述功能门，才问一个低维 PCA 子空间能否在未见数据上保留完整 \(R_U\) 增益的 80% 或 90%。

这个顺序对应两次会议共同收紧后的路线：同 token 更新 \(\rightarrow\) 功能准入 \(\rightarrow\) 功能充分子空间 \(\rightarrow\) Router；不是先从方差谱直接命名“新增信息”。

## 分析方法

对 Qwen3-8B 的每个合格 block，固定 decision token，并定义

\[
X_\ell=N_\ell(h_\ell),\quad
Z_\ell=N_\ell(h_\ell+a_\ell),\quad
U_\ell=Z_\ell-X_\ell,
\]

\[
R_{U,\ell}=U_\ell-\widehat{\mathbb E}_{lin}[U_\ell\mid X_\ell].
\]

TRAIN 拟合残差化器和读出，DEVELOPMENT 只选正则，官方 TEST 一次性评估。功能主统计量为

\[
T_\ell=G_{\ell,full}-
\max\left(G_{\ell,duplicate\text{-}X},q_{.95}(G_{\ell,mismatch})\right).
\]

只有 simultaneous 95% LCB\((T_\ell)>0\) 才把该层称为“新增可访问性层”。PCA 阶段比较头部 PCA 与同秩 Haar 随机方向；几何阶段另报 covariance 的 \(r_{80}^{var}\)、\(r_{90}^{var}\)，但不让几何结果覆盖功能门。

## 结论

### 1. 新数据上没有通过注册判据的涌现层

最接近 0 的也是 block 2：full gain 为 0.2042，但 null envelope 为 0.5075，故 \(T_2=-0.3032\)，simultaneous 95% 区间为 \([-0.3179,-0.2886]\)。此前合成 taxonomy 上确认的 blocks 24/28 在本任务上也没有复现：

| Block | full-\(R_U\) gain | null envelope | \(T_\ell\) | simultaneous 95% CI | 功能准入 |
| ---: | ---: | ---: | ---: | ---: | --- |
| 2 | 0.2042 | 0.5075 | -0.3032 | [-0.3179, -0.2886] | Fail |
| 24 | 0.1480 | 0.6261 | -0.4781 | [-0.4891, -0.4671] | Fail |
| 28 | 0.0756 | 0.6713 | -0.5957 | [-0.6062, -0.5851] | Fail |
| 36 | 0.0402 | 0.6839 | -0.6437 | [-0.6527, -0.6346] | Fail |

主导 null envelope 的是 duplicate-\(X\) 分支，而不是错配更新。这说明当前单一线性 \(X\) 基线没有耗尽旧状态中可由第二个同预算分支取得的任务结构；不能把 full-\(R_U\) 的原始正 gain 全部归因给“本层特有的新信息”。

![逐层累计可读性与匹配新增可访问性](figures/figure_1_clinc150_layerwise_accessibility.png)

上图上半部分横轴是 Transformer block，纵轴是从 \(X_\ell/Z_\ell\) 线性读出已知 domain 内 intent 的 TEST accuracy；下半部分纵轴才是逐 block 的匹配超额收益 \(T_\ell\)。\(X/Z\) 可读性从浅层开始就很高并继续累积，但所有 \(T_\ell\) 都显著为负。累计可读性高不等于某一 block 新增了旧状态之外的可访问性。

### 2. \(G_{80}/G_{90}\) 为 NA，不是“PCA 没扫到足够大”

定义 \(G_{80}=0.8G_{full}\)、\(G_{90}=0.9G_{full}\) 的前提，是 \(G_{full}\) 已经超过同一 \(X\) 的容量对照。这里前提对所有层都不成立，因此没有一个已确认功能效应可供“保留 80%/90%”，正式功能秩只能写 `NA_NO_FULL_ADMISSION`。

![PCA 功能保留分析](figures/figure_2_clinc150_pca_g80_g90.png)

图中的 PCA 曲线仍是描述性诊断。例如 blocks 24/28 的 PCA-256 对“未准入 full gain 的 80%”有正的描述性 LCB，但 90% 没通过；因为分母本身未准入，这不能改写成“256 维保持功能完整性”。

### 3. 几何能量有一定集中，但不等于功能低秩

在 4096 维 \(R_U\) 中，各层解释 80% 方差需要 180--434 维，解释 90% 方差需要 298--732 维。block 24 为 264/472，block 28 为 207/342。可以说 covariance 能量比全宽更集中；不能说这些维度保存了已确认新增功能。

此前对完全相同 blocks 24/28 \(R_U\) 数组做过 domain 条件化分析：不同 domain 的判别方向稳定且有区别，但 domain 内完整更新云本身仍然宽，cross-minus-within normalized \(r_{90}\) 的 simultaneous LCB 分别为 -0.0100 与 -0.0053。因此现有证据不支持“整体高秩主要只是很多窄小 domain 子空间叠加”。

## 会议语境中的认识更新

- **0813 的方法没有被否定。**同一 token 先作差、中心化 covariance、PCA，仍是描述候选更新点云的正确几何流程。
- **0817 的警告被本实验验证为必要。**PCA 最大化方差，不保证分类或 Router 功能；表示几何秩与 gating 功能秩必须分开。
- **本次更新：**在 CLINC150 上，现有线性 \(R_U\) 操作化未能从旧状态的额外读出容量中分离出任何 block-local intent 增益。因此当前不能从 PCA/聚类直接进入 Router。

## Claim Boundary

**可以声称：**在冻结 Qwen3-8B、指定 prompt/decision token、CLINC150 已知-domain 15-way intent 和注册线性读出下，blocks 2--36 均未超过匹配同-\(X\) 对照；所以没有功能准入层，\(r_{G80}/r_{G90}\) 均为 NA。

**不能声称：**模型没有 intent 信息；Attention 没有任何新计算；不存在非线性新信息；\(R_U\) 在信息论上无新意；低维 Router 不可能；几何分析无意义。

## Next Decision — AI Proposal, Awaiting dxy

下一次只解决一个归因问题：**全层负 \(T_\ell\) 是因为当前单头 \(X\) 基线欠拟合，还是正确配对 \(R_U\) 在能力匹配后仍没有 update-specific intent utility？**

建议用同一交叉拟合与同一总参数预算，对比 joint matched-capacity \(X\)-only 与 \(X+R_U\) 读出。只有正确配对 \(R_U\) 在这个更严格的同容量比较中获胜，才恢复 PCA 功能秩和 Router 分析；否则应修改“新增信息”的操作化，而不是继续挑 PCA 维数。

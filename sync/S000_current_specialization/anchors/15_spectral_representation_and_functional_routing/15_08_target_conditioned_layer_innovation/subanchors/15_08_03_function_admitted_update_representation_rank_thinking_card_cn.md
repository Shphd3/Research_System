---
card_id: 15_08_03_function_admitted_update_representation_rank
owner: researcher
status: COMPLETED_INSUFFICIENT_BASIS_SENSITIVE_HREP_FAIL
parent_anchor: ../15_08_target_conditioned_layer_innovation_anchor_cn.md
depends_on: 15_08_02_layerwise_conditional_fine_added_accessibility_anchor_cn.md
created: 2026-08-16
updated: 2026-08-16
---

# Thinking Card：功能准入更新的参数谱位置与表征低秩性

## 研究者已确认的判断

1. 核心目标是比较不同层相对旧状态新增的信息：不同层新增多少细粒度可访问性、更新在参数谱的什么位置激活、token 几何怎样变化、以及由多少维表征承载。最终才从具名层中寻找可用于后续分发的低维空间。
2. “表征低秩”指 token 更新点云本身能被低维线性空间稳定表征，不等同于八分类读出天然只需少量判别方向。
3. 分析对象必须保留同一个 token 的层内精确更新，并沿用

$$
R_{U,\ell}=U_\ell-\widehat{\mathbb E}_{lin}[U_\ell\mid X_\ell].
$$

4. 参数谱比较保留两个不同角色：先看 $R_{U,\ell}$ 在本层 MLP 参数谱的最大能量带与相对位置；再看它在冻结公共参数基上的激活位置，使所有层能够用同一把尺子比较。
5. 之前的待检验假设是：随层加深，conditional-fine 新增可访问性整体增强，同时新增更新的归一化能量在公共参数谱中后移。两部分必须分别测量并同时成立；谱后移不能替代功能新增。
6. token-level 方法应落实 0813 组会提出的“同 token 更新 → 中心化协方差 → PCA → token 级聚类”，补充参数谱逐方向能量没有保留的联合变化。
7. 所有 block 都应形成可比较的功能增益、本层谱、公共谱、低秩和跨层几何轨迹；功能实验和几何分析应在打开 CONFIRMATION 前一起冻结，并复用同一次提取。不能先看功能正层再事后设计谱带或 PCA；几何也不能替代功能 verdict。

## 当前剩余不确定性

实验已经裁定当前模型与 taxonomy 下的层级画像：功能准入层为 24、28；公共谱后移在 Mean Response 与 Rank Consensus 中异号；没有一层通过稳定表征低秩合取；两层功能都在最小注册秩 256 得到保留。仍未知的是这个 256 维空间是否被模型原生因果使用、是否跨任务/模型复现，以及能否改善 Router 分发。

## 最强竞争解释

1. 看似低秩只是样本数小于隐藏维度造成的有限样本秩上限。
2. 前几个主成分只承载模板、尺度或父类共同变化，并不承载 child 区分。
3. TRAIN 上的紧凑谱不会复现在表达互斥的 DEVELOPMENT/CONFIRMATION。
4. 聚类稳定只是几何分组，未必对应细类，也未必有 Router 效益。
5. 公共谱后移可能只是在特定基下发生的方差重分配；本层最大能量带也可能因相邻带能量接近而跳动，二者都不等于功能新增随深度增加。

## 已批准并执行的联合分析方法

对每层构造本地 MLP 输入侧参数算子

$$
K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}+W_{up,\ell}^{\top}W_{up,\ell}.
$$

把父类内中心化的 $R_{U,\ell}$ 投到本层 $K_\ell$ 的特征方向，使用16个等秩带报告每带能量、最大能量带和谱质心。这回答“更新相对本层自己的强—弱参数响应主要落在哪里”；不同层本地 rank 不解释为同一方向。

再把所有层投到冻结 Mean Response 公共参数基，使用完整归一化能量谱、谱质心和后段能量份额检验跨层后移；Rank Consensus 公共基只作基敏感性对照。最大能量带用于直观展示，谱质心作为主要位置量，因为 argmax 容易在相邻带间跳动。

将公共谱位置曲线与 A15_08_02 的 $T_\ell$ 曲线并列，预先冻结浅层—深层总体对比。只有功能净收益随深度增强和公共谱位置后移同时成立，才支持原联合假设；任一单独成立都给独立类型化结论。

对每层的 $R_{U,\ell}$ 先减去该父类在 TRAIN 中的均值，保留父类内部的 token 变化；在 TRAIN 上做完整 SVD/PCA，报告表征 effective rank、80% 方差秩和 stable rank。用 TRAIN 冻结的前 $r$ 维子空间在 DEVELOPMENT/CONFIRMATION 上直接测方差保留率，避免重新选方向。

token 几何分支不依赖公共参数基，而对同一批 token 的父类内中心化更新计算线性 CKA：它比较两层 token—token 几何是否相近，不要求两层主成分逐向量配准。

对所有合格层都预先计算 TRAIN-frozen PCA 子空间的同一 $X$ 细类增益曲线；若某层同时通过完整 $R_U$ 功能门、少量 PCA 方向保留 full-$R_U$ 增益的 80%、并超过同秩 Haar，才允许说“该低维表征同时保留了已验证功能”。这样可以与功能实验一次执行，又不发生先看正层再选择分析的泄漏。

聚类只作辅助：在 PCA token 坐标上按父类分别做 $k=8$ 的 k-means，检查未见表达上的聚类稳定性和 child 富集，并与同秩 Haar 和标签置乱比较。聚类不进入低秩 Pass，也不直接定义专家。

## 已批准并执行的可证伪门槛

原深度—谱假设先给独立 verdict：预注册浅层—深层 $T_\ell$ 对比和 Mean Response 谱质心对比均为正，且各自同时区间下界大于零，才记为 `FUNCTION_GROWTH_WITH_COMMON_SPECTRAL_RIGHT_SHIFT`。若 Rank Consensus 未通过同一个正向判据，则结论必须标记为 `BASIS_SENSITIVE`。本层最大能量带不进入这一 Pass。

令 TRAIN 每层父类内中心化后的样本可识别秩上限为 $n-P$。候选“稳定表征低秩层”需同时满足：

1. $r_{80}^{rep}/(n-P)\le 0.10$；
2. TRAIN 冻结子空间在 DEVELOPMENT 和 CONFIRMATION 上各保留至少 75% 总方差；
3. 真实 $r_{80}^{rep}$ 小于独立坐标置乱 null 的 5% 分位；
4. 若该层属于功能正收益集合 $\mathcal L^+$，还需找到 $r$ 使 PCA 子空间的留出增益不低于 full-$R_U$ 增益的 80%，并超过同秩 Haar q95。

这些 10%、75%、80% 和 null 分位最初由 AI 提议，已由研究者批准并在 CONFIRMATION 开启前冻结。

## 结果更新与唯一下一决策

完整分析已完成：

- 深层功能总体增强不成立；
- Mean Response 后移而 Rank Consensus 反向，结论为 basis-sensitive；
- 更新云有跨坐标联合结构，但稳定表征低秩无层通过；
- blocks 24、28 的新增功能最小在注册 rank 256 通过 PCA/Haar 判据；
- CKA 与聚类只保留为辅助几何，不能改变功能或低秩 verdict。

唯一下一决策是：是否为 blocks 24、28 的 rank-256 空间另行冻结因果干预或 Router 效用协议。当前实验不自动授权该后续。

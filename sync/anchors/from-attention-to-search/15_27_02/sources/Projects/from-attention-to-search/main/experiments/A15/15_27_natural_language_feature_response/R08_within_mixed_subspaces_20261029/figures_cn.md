# 六类图：对象、两种读法、实际结果与边界

所有图均为R07固定数据上的探索性续接。主图来自block27，早/中层与结尾控制各自单独保存。PCA/UMAP只在发现集拟合；开发/旧留出仅投影。

## 图1：数学、生物的主要变化空间是否相似？

横轴是各自保留4/8/16/32个主方向；纵轴是两个方向集合的重合度，0正交、1完全相同。黑线是同样本量的跨域分半，蓝/橙线是数学/生物同域分半，灰线是随机空间。紫线是完整发现集，样本更多，不能直接与同域分半当作同量比较。

两种可能读法：若黑线接近蓝橙，且蓝橙本身稳定，支持主要变化相近；若黑线更低但蓝橙稳定，支持存在差别。若蓝橙自身很低，先保留估计不足。

实际结果：最后层16维黑0.295、蓝0.395、橙0.436；随机期望0.0156。它们既不是相同空间，也远不是随机正交。跨减同域平均−0.120；200次划分范围[−0.134,−0.102]。同域稳定性有限，不能直接定性为两套确定的领域空间。

不能推出：不能给共同方向命名为语法，也不能由不同方向推分专家。

![图1](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure1_overlap_block27_all.png)

同格式控制：[早层](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure1_overlap_block1_all.png) · [中层](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure1_overlap_block13_all.png) · [只example](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure1_overlap_block27_E0.png) · [只explanation](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure1_overlap_block27_E1.png)

## 图2：混合空间更贴近谁？

横轴k；纵轴为混合PCA空间与某个单域PCA空间的重合度。蓝色混合—数学，橙色混合—生物。都是发现集独立中心化得到的空间。

两种可能读法：两条都高，表示混合保留双方方向；一高一低，只能说混合几何更贴近一方，也可能因为该方变化幅度更大。

实际结果：最后层16维为0.713与0.637；数学略高。数学/生物池化总方差分别28934.07/23887.25，幅度不相同。单结尾example时数学方差8600.33反而小于生物10191.88，因此幅度不能被当成完整解释。

不能推出：不是模型偏爱数学，不是共享语义比例；两类PCA自身都是有限样本估计。

![图2](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure2_mixture_overlap_block27_all.png)

同格式控制：[早层](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure2_mixture_overlap_block1_all.png) · [中层](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure2_mixture_overlap_block13_all.png) · [只example](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure2_mixture_overlap_block27_E0.png) · [只explanation](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure2_mixture_overlap_block27_E1.png)

## 图3：中心差异被哪些主要空间覆盖？

横轴k；纵轴是单位数学减生物均值差向量的平方投影比例。三色是数学、生物、混合空间；实线是发现均值差，虚线是旧留出均值差投到这些固定空间。

两种可能读法：混合高而单域低，说明混合空间更充分容纳中心差；三者都高，则中心差与域内主要变化重用相近空间。

实际结果：最后层16维：发现数学74.99%、生物67.96%、混合99.89%；旧留出54.01%、33.40%、93.33%。混合覆盖保持较高；域内覆盖有明显减弱，不能说中心差完全处于域内，也不能说完全在外。

不能推出：比例不是分类信息占比。这里的PCA不是旧R07自然文本PCA，不能用99.89%替换旧58.12%。

![图3](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure3_center_projection_block27_all.png)

同格式控制：[早层](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure3_center_projection_block1_all.png) · [中层](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure3_center_projection_block13_all.png) · [只example](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure3_center_projection_block27_E0.png) · [只explanation](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure3_center_projection_block27_E1.png)

## 图4：混合前k维的变化来自哪里？

横轴k；纵轴为该混合空间内的方差份额。蓝色域内，橙色两域中心差，分母一致，二者相加为100%。

两种可能读法：橙色大，说明中心分离贡献了很多变化；蓝色大，说明大部分变化仍发生在领域内部，但域内可含结尾、词汇和措辞。

实际结果：最后层16维总方差26783.71＝域内24350.63＋类间2433.08，即90.92%与9.08%。example/explanation分开后类间分别36.28%/19.93%。所以图3几乎全覆盖中心差与图4类间不到一成可以同时成立。

不能推出：不是feature贡献、不是语义含量，也不能把蓝色直接命名为共有知识。

![图4](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure4_variance_sources_block27_all.png)

同格式控制：[早层](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure4_variance_sources_block1_all.png) · [中层](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure4_variance_sources_block13_all.png) · [只example](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure4_variance_sources_block27_E0.png) · [只explanation](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure4_variance_sources_block27_E1.png)

## 图5：真实目标表征的局部邻近怎样呈现？

每点是一条文本的最后目标token。输入是该层真实1024向量；二维横纵轴没有固定语义。蓝/橙为领域，圆/三角为example/explanation；无边、灰边、黑边分别是发现/开发/原留出。

两种可能读法：颜色接近分组，可描述领域关联；形状分开，则结尾也在组织二维邻近。二者可能同时出现，不预设哪一个是语义原因。

实际结果：三层主种子图都可见结尾结构；最后层圆形区域领域分开较明显，三角区域仍有混合。早层也能看见领域相关结构，故不能凭深层图讲“领域直到深层才产生”。另外两个固定种子中，15近邻重合平均：早层约0.57–0.58，中层0.68，晚层0.65–0.66；具体布局并不恒定。

不能推出：不是自然簇证明，不能按图中簇数命名知识、比较层间坐标或声称深层更可分。

![图5](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure5_umap_block27_seed42_domain.png)

三层独立图：[block1](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure5_umap_block1_seed42_domain.png) · [block13](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure5_umap_block13_seed42_domain.png) · [同坐标按结尾着色](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure5_umap_block27_seed42_ending.png)

固定种子对照：[seed17](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure5_umap_block27_seed17_domain.png) · [seed73](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure5_umap_block27_seed73_domain.png)

## 图6：同一批文本的联合feature使用模式怎样呈现？

每点仍是文本目标token，输入为A22原生14层联合编码得到的16384维共享z。只一份z、只一套主图，颜色/形状/划分标记同图5。

两种可能读法：若颜色结构随种子保留，可描述联合使用中的领域关联；若主要按结尾分开，说明结尾是必须保留的解释。

实际结果：原生门控产生每目标206–264个非零坐标，无零向量。主图同时呈现结尾与领域结构，也有混合位置；跨种子15近邻重合约0.65–0.66。三种种子都保存，未挑分离最好的一张。

不能推出：不能与最后层真实表征直接判“更好”，因为输入为14层；不把z复制成逐层激活，不说明Attention传递或功能因果。

![图6](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure6_umap_joint_z_seed42_domain.png)

固定种子对照：[seed17](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure6_umap_joint_z_seed17_domain.png) · [seed73](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/figures/figure6_umap_joint_z_seed73_domain.png)

## 用同一对文本理解“域内变化”

F06数学W0：
> In this case, a rectangular floor is covered with identical square tiles. Multiplying the number along its length by the number across its width gives the total.

F06生物W0：
> A leaf surface is covered with many small pores. Their density and opening size influence how rapidly water vapor can escape into the air. The account is brief.

两者分别接完全相同的结尾`This passage presents a concrete example`，或`This passage provides a brief explanation`；目标都是该结尾最后一个词，零起算位置36。取最后层真实向量，不取feature或decoder。

这对固定例子在混合第一主方向上的得分：数学example −180.55、生物example −141.80；数学explanation +71.03、生物explanation +173.80。这里主方向符号任意，正负本身没有数学/生物含义。两域都随结尾发生大移动，说明“同一领域内部”也有很大的文本形式变化。这是实例，不代替完整方差分解。

反例必须保留：把同一家族数学换成W1措辞后，example得分−33.14，高于生物W1的−110.34；W0时数学反而更低。所以不能把混合第一主方向直接叫“数学更高”的领域方向，更不能把主成分都命名为语法或知识。

这8条实例是旧R07输入规则已固定展示的F06，不为新图选取；完整原文、坐标、投影平方量见[实例表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R08_within_mixed_subspaces_20261029/tables/fixed_F06_examples.csv)。

## 不确定性怎么读

图1阴影是200次家族分半划分范围；它们来自同一24个家族，不是200批独立数据。图2–4阴影/线为200次家族重采样百分位范围。非线性重合和单位方向投影会有重采样偏移：部分原点估计在范围之外；所有这些单元在附录保留，不能把图当成已校准的正式置信推断。

单结尾的32维分半秩不够，图1不画可估曲线；完整发现集仍支持32维。单域bootstrap32维仅35/200次秩够，图2/3对应阴影不画，条件百分位只留表中。不同估计的分母、样本数和有效重复数不能互相替换。

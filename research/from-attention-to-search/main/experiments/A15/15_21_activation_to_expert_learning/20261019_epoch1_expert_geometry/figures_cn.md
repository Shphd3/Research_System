# 图索引与证据边界

这些图回答本轮Protocol中的训练资格、方向差异与谱集中程度问题，服务于Anchor的路由学习问题，不更新Anchor或作机制批准。数值及解读见[Summary](summary_cn.md)；完整机器表保留在tables。曲线均为描述性汇总；无未计算的不确定带。

## 训练证据

![训练证据](figures/figure1_expert_training_evidence.png)

横轴为10条件，纵轴为每模型8个expert中的合格数量；并列柱区分seed，浅色暴露数量与深色收益数量分开；130充分暴露、49有收益；不能证明收敛。

来源：[数据](tables/expert_training_evidence.csv)。生成文件同名PDF/SVG可导出。预期分支：若方向重合则不支持方向区分，若不同只支持几何区分；若q集中程度下降才支持该谱描述的各向同性增加。实际观察与允许结论以Summary为准。

## 主要条件输出PCA

![主要条件输出PCA](figures/figure2a_output_PCA_similarity.png)

同行列expert的rank16输出重叠；5主要条件×两seed；灰色NA；低重叠不等于语义分工。

来源：[数据](tables/within_model_similarity.csv)。生成文件同名PDF/SVG可导出。预期分支：若方向重合则不支持方向区分，若不同只支持几何区分；若q集中程度下降才支持该谱描述的各向同性增加。实际观察与允许结论以Summary为准。

## 其余条件输出PCA

![其余条件输出PCA](figures/figure2b_output_PCA_similarity.png)

相同定义，另外5条件；保留阴性和退化条件；不能把NA当0。

来源：[数据](tables/within_model_similarity.csv)。生成文件同名PDF/SVG可导出。预期分支：若方向重合则不支持方向区分，若不同只支持几何区分；若q集中程度下降才支持该谱描述的各向同性增加。实际观察与允许结论以Summary为准。

## 共同坐标参数方向

![共同坐标参数方向](figures/figure3_parameter_direction_similarity.png)

gate/up共同输入右方向、down共同输出左方向；上排W1、下排增量；点/三角区分seed，误差线为同模型expert对的四分位范围；不同对象不等同响应PCA。

来源：[数据](tables/similarity_summary.csv)。生成文件同名PDF/SVG可导出。预期分支：若方向重合则不支持方向区分，若不同只支持几何区分；若q集中程度下降才支持该谱描述的各向同性增加。实际观察与允许结论以Summary为准。

## 前16绝对奇异值

![前16绝对奇异值](figures/figure4_absolute_top16_spectra.png)

横轴rank1–16、纵轴绝对σ；先seed内再跨seed平均；强度与归一化形状分开。

来源：[数据](tables/top16_singular_values.csv)。生成文件同名PDF/SVG可导出。预期分支：若方向重合则不支持方向区分，若不同只支持几何区分；若q集中程度下降才支持该谱描述的各向同性增加。实际观察与允许结论以Summary为准。

## 所有合格expert完整谱

![所有合格expert完整谱](figures/figure5_full_normalized_energy_spectra.png)

横轴rank1–1024，纵轴q；W1/增量分开；均值无独立重复置信区间。

来源：[数据](tables/spectral_curve_source.csv.gz)。生成文件同名PDF/SVG可导出。预期分支：若方向重合则不支持方向区分，若不同只支持几何区分；若q集中程度下降才支持该谱描述的各向同性增加。实际观察与允许结论以Summary为准。

## 初始化配对变化

![初始化配对变化](figures/figure6_initialization_changes.png)

同expert的W0→W1；gate/up变得略集中；down初始零的归一化比较NA。

来源：[数据](tables/paired_initial_changes.csv)。生成文件同名PDF/SVG可导出。预期分支：若方向重合则不支持方向区分，若不同只支持几何区分；若q集中程度下降才支持该谱描述的各向同性增加。实际观察与允许结论以Summary为准。

## T_S1 seed11逐expert谱

![T_S1 seed11逐expert谱](figures/figure7_seed11_individual_expert_spectra.png)

按expert保留完整谱和绝对前16谱；星号通过收益规则；平谱与收益不等价。

来源：[数据](tables/spectral_curve_source.csv.gz)。生成文件同名PDF/SVG可导出。预期分支：若方向重合则不支持方向区分，若不同只支持几何区分；若q集中程度下降才支持该谱描述的各向同性增加。实际观察与允许结论以Summary为准。

## T_S1 seed22逐expert谱

![T_S1 seed22逐expert谱](figures/figure7_seed22_individual_expert_spectra.png)

同上，独立列出第二seed；同编号不自动代表跨条件同功能。

来源：[数据](tables/spectral_curve_source.csv.gz)。生成文件同名PDF/SVG可导出。预期分支：若方向重合则不支持方向区分，若不同只支持几何区分；若q集中程度下降才支持该谱描述的各向同性增加。实际观察与允许结论以Summary为准。

## 来源到自然路由

![来源到自然路由](figures/figure8_source_routing.png)

T_S1 seed11，6个≥20问答来源；P(expert|source)与相对全局负载的lift；来源非纯领域。

来源：[数据](tables/epoch1_source_dispatch.csv)。生成文件同名PDF/SVG可导出。预期分支：若方向重合则不支持方向区分，若不同只支持几何区分；若q集中程度下降才支持该谱描述的各向同性增加。实际观察与允许结论以Summary为准。

## 49收益子集完整谱

![49收益子集完整谱](figures/figure9_benefit_subset_spectra.png)

只取通过收益判据子集，完整1024项曲线；需与figure5全130对读，不能筛赢家冒充整体。

来源：[数据](tables/benefit_subset_matrix_summary.csv)。生成文件同名PDF/SVG可导出。预期分支：若方向重合则不支持方向区分，若不同只支持几何区分；若q集中程度下降才支持该谱描述的各向同性增加。实际观察与允许结论以Summary为准。

## 收益子集输出PCA

![收益子集输出PCA](figures/figure10_benefit_subset_PCA.png)

主要5条件，只有两端都通过的expert对；灰色NA；少量相关配对不作显著性结论。

来源：[数据](tables/within_model_similarity.csv)。生成文件同名PDF/SVG可导出。预期分支：若方向重合则不支持方向区分，若不同只支持几何区分；若q集中程度下降才支持该谱描述的各向同性增加。实际观察与允许结论以Summary为准。

## 收益子集前16能量谱

![收益子集前16能量谱](figures/figure11_benefit_subset_top16_energy.png)

每项σ²/全部1024项总能量；W1/增量分列，seed内平均后等权两seed；不能把局部纵轴差异读成普遍能力优势。

来源：[数据](tables/top16_singular_values.csv)。生成文件同名PDF/SVG可导出。预期分支：若方向重合则不支持方向区分，若不同只支持几何区分；若q集中程度下降才支持该谱描述的各向同性增加。实际观察与允许结论以Summary为准。

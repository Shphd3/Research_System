# 两张主图怎么读

## 图1：实际贡献是否向谱尾移动？

![图1](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/figures/figure1_contribution_weighted_spectrum.png)

每个点是该文档域/字典中，某一个谱段的平均贡献占比。横轴是按PCA方差由大到小排序的16段，每段64方向；纵轴是“活跃 feature 的贡献加权谱分布”的百分比。蓝色近高，橙色远高；阴影为5000次文档重采样的95%点对点区间。每域20篇，原4842个近远共同query/head；每位置先把自己的16段归一，再位置→head→query→文档逐级等权，不能按所有token贡献总量混合加权。

该图保留真实贡献幅度，不乘特征值，不做feature RMS标准化；每位置以及均值的16段总和均为1。看橙线是否将更多比例移到后段。实际四个面板远高前64占比均略增：SAE数学81.46%→84.08%，生物81.71%→83.97%；CC数学48.72%→50.10%，生物44.64%→45.74%。这与平均排名降低的点估计一致。多数近远区间仍跨零，不能凭曲线局部分开宣布稳定前移。不能称它为原表征解释方差，也不跨字典比较谁更“语义”。

## 图2：右移是否可靠，是否超出中等关注的近远变化？

![图2](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/figures/figure2_primary_mean_rank_differences.png)

一个圆点＝远高平均排名减近高；一个菱形＝这一变化再减远中减近中。横轴为主成分排名差，正值更偏尾，负值更偏前；竖虚线为0。四行固定为SAE数学/生物、CC数学/生物，每行20文档。误差棒为配对文档95%点对点区间，右侧q是8个主比较的统一BH校正。不能用“某个组显著、另一个不显著”代替菱形的直接差中差。

圆点均在0左侧；SAE生物区间不跨0，校正后q=0.1216，其余圆点区间跨0；所有菱形区间跨0。可支持本批未发现稳定右移，不能证明完全没有关联，也没有确认统一、强Attention特有的前移。

完整数值、原中等对照、窗口检查、等权/合成/真实表征附图见[辅助结果](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/auxiliary_cn.md)。图1/2均是同一固定PCA基下的探索性既有文档分析。

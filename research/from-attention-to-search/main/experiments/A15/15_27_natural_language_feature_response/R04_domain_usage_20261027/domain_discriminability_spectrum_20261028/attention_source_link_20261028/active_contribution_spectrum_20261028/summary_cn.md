# 问题

**远处强 Attention 来源位置，全部活跃 feature 的实际贡献方向，是否比近处更偏表征谱尾？** 本轮用每个来源位置全部活跃坐标，保留原贡献幅度；不再限于领域Top-16。比较的是“活跃 feature 的贡献加权谱分布”，不叫原表征解释方差。

# 答案

**本批数据没有支持“远处更偏谱尾”。四组点估计反而向谱前部移动，但经8项统一校正后，尚未确立稳定的反向关系。** 平均主成分排名按1–1024逐方向计算，数值越大越偏尾，不表示语义更复杂。

|字典／文本|近高→远高平均排名|远高−近高及95%区间|
|---|---|---|
|SAE／数学|78.05 → 66.95|-11.10 [-26.09, +1.15]|
|SAE／生物|77.79 → 67.12|-10.66 [-21.91, -2.39]|
|CC／数学|230.32 → 224.10|-6.22 [-17.61, +7.28]|
|CC／生物|249.76 → 243.33|-6.43 [-15.77, +4.52]|

每域20篇文档；区间按文档配对重采样。SAE生物的单项区间未跨零，但校正q=0.1216；其余近远区间跨零，8项主比较均未达到0.05。高组变化再减中等关注变化，四个差中差区间均跨零，因此也未支持强 Attention 特有的右移。[图1：完整16段分布](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/figures/figure1_contribution_weighted_spectrum.png) · [图2：两项主对比](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/figures/figure2_primary_mean_rank_differences.png)

# 推进程度

**已把静态decoder方向，推进到真实位置上的全活跃集合、按当时贡献幅度加权的测量。** 等权成员、合成向量和原表征均已核对，不能替代主量：例如CC数学的远高减近高，贡献加权为−6.22，合成向量−1.25，中心化原表征+3.08，三者区间都跨零。交叉项会改变分布，不能挑其中一种作为有利答案。[辅助结果](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/auxiliary_cn.md)

窗口检查仅保留原pair两端均在32:192的记录，仍有40篇文档，query从320减至289、共同query/head从4842减至3288。四组加权近远点估计仍为负，注意力相关差中差仍跨零。但近远绝对位置与Attention概率仍不同，词面、结构词和空白也未完全匹配。这只是窗口敏感性检查，不能推出长程语义或传递机制。

全部为已反复查看文档的探索性补充。缓存内适用计算、两主图、辅助图与完整表均完成；新增模型前向、训练、PCA拟合、候选重选均0。[逐图读法](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/figures_cn.md) · [统计与混杂完整解释](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/detailed_cn.md) · [原始表索引](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/data_index_cn.md)

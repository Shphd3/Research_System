# 辅助结果：保留所有口径

## 中等Attention与窗口检查

[中等关注完整16段图](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/figures/aux_weighted_middle_attention.png)使用与高组相同的计算。SAE数学中组排名95.13→80.94（−14.19），生物99.10→84.71（−14.39）；CC数学224.93→221.66（−3.28），生物245.01→239.64（−5.37）。高、中两种近远变化均不能直接归因于强Attention。

[窗口内16段图](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/figures/aux_window_weighted_spectrum.png) · [窗口排名差图](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/figures/aux_window_mean_rank_differences.png)。只过滤原pair，不另找control。全部40文档保留；数学query160→145、cells2399→1635，生物query160→144、cells2443→1653。近pair10733→7295，远pair14055→7118，四组重新在3288共同单元上统计。

窗口内加权远高−近高：SAE数学−15.32[-31.69,-0.50]、生物−11.92[-22.82,-2.88]；CC数学−6.47[-19.04,7.36]、生物−1.94[-13.87,11.30]。对应差中差+0.17[-9.16,10.45]、+3.12[-6.27,12.12]、−2.85[-8.95,3.26]、−0.11[-6.36,6.29]均跨零。这是描述性敏感性区间，没有追加或替代8项主检验。来源绝对位置仍不相等；窗口操作还将远高实际Attention均值从数学0.005265/生物0.007701降至0.000344/0.000317，不能称完全匹配。

## 等权、合成、原表征分别回答什么

- [等权方向分布](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/figures/aux_equal_spectrum.png)／[等权排名差](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/figures/aux_equal_rank_differences.png)：每个活跃成员的单位decoder方向等权，不看其当时幅度。用于区分成员组成与贡献幅度重加权，不能代替主量。
- [合成向量分布](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/figures/aux_synthesized_spectrum.png)／[合成排名差](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/figures/aux_synthesized_rank_differences.png)：先相加z×原尺度decoder，再投影平方；有交叉项，没有decoder偏置或重构残差，不是完整原表征。
- [中心化真实表征分布](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/figures/aux_real_spectrum.png)／[真实表征排名差](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/figures/aux_real_rank_differences.png)：真实hook缓存减原发现合并均值，各位置投影平方归一后沿原层级平均。它也不同于把所有位置合起来计算的原PCA方差曲线。

|字典|文本|口径|远高−近高及区间|再减中组变化及区间|
|---|---|---|---|---|
|SAE|数学|贡献加权|-11.10 [-26.09, +1.15]|+3.08 [-4.46, +11.76]|
|SAE|数学|等权成员|-3.96 [-8.97, +1.77]|-0.96 [-6.36, +4.83]|
|SAE|数学|合成向量|-7.15 [-16.58, +1.68]|-0.17 [-6.39, +6.23]|
|SAE|数学|中心化原表征|-3.73 [-13.39, +5.94]|-8.42 [-17.10, +0.63]|
|SAE|生物|贡献加权|-10.66 [-21.91, -2.39]|+3.72 [-5.32, +11.83]|
|SAE|生物|等权成员|-3.70 [-10.27, +2.62]|-0.07 [-4.38, +3.94]|
|SAE|生物|合成向量|-9.17 [-20.34, -1.30]|+1.65 [-5.44, +8.26]|
|SAE|生物|中心化原表征|-8.08 [-20.29, +2.20]|-5.13 [-10.88, +0.61]|
|CC|数学|贡献加权|-6.22 [-17.61, +7.28]|-2.95 [-10.00, +4.24]|
|CC|数学|等权成员|-1.08 [-3.59, +1.52]|-1.30 [-3.79, +1.13]|
|CC|数学|合成向量|-1.25 [-13.50, +11.83]|-5.17 [-15.74, +5.71]|
|CC|数学|中心化原表征|+3.08 [-10.39, +16.05]|-4.90 [-15.96, +6.70]|
|CC|生物|贡献加权|-6.43 [-15.77, +4.52]|-1.06 [-6.41, +3.95]|
|CC|生物|等权成员|-1.41 [-4.26, +1.34]|-0.42 [-2.46, +1.45]|
|CC|生物|合成向量|-5.84 [-17.35, +5.02]|-4.38 [-11.25, +2.82]|
|CC|生物|中心化原表征|-4.70 [-18.13, +7.41]|-2.33 [-9.54, +5.19]|

贡献加权与等权的**水平**差明显，例如SAE数学近高排名78.05，而等权235.59；远高66.95，而等权231.63。实际大贡献更集中于前部方向；这不等于所有活跃成员的方向都在前部，也不等于已分离纯z强度与decoder范数的作用。近远**变化差异**则不够精确：等权变化减加权变化，四组为+7.14[-3.44,20.06]、+6.97[-3.35,18.36]、+5.14[-8.91,16.77]、+5.02[-6.30,14.90]，均跨零。因此不能确定近远差主要由幅度还是成员组成驱动。[两口径直接配对比较](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/tables/paired_readout_differences.csv)

## 交叉项确实改变数值

合成平方范数−各成员平方范数和，再除以后者，得到每位置交叉项的相对量；随后仍沿原层级平均。数学近高/远高：SAE+48.19%/+43.50%，CC+14.38%/+13.32%；生物SAE+46.78%/+44.91%，CC+15.48%/+13.80%。这是平方范数的相对变化，不是信息增益或原表征解释率。不同谱段还存在增强与抵消，完整带符号交叉项见[逐文档表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/tables/cross_band_relative_power_by_document.csv)。

例如CC数学远高−近高：单支贡献平方求和−6.22，合成后−1.25，真实表征+3.08，三者区间均跨零；窗口内合成点估计+0.41而主量−6.47，也都未支持稳定反向判别。不能因选了不同口径就宣称尾部或前部结论成立。合成与真实表征还存在偏置、残差、中心化原点差别，不能把它们的全部差异都算成交叉项。

[全部读数/16段/近远差/差中差](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/active_contribution_spectrum_20261028/tables/spectral_contrasts.csv)保留所有结果；辅助表的p为空，不伪装成已统一校正的额外确认。

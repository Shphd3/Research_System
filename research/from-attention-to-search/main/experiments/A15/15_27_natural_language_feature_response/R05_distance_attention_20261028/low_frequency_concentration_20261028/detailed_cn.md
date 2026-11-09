# 计算、三图读法和完整证据

本轮属于表征组织读数；未新增行为实验或功能干预。输入是原40数学/生物留出文本（各20），来源位置的原生A22共享z。层接口为0起点blocks1,3,...27的residual-post。独立DCLM低频4469成员固定，不含参考低支持组。贡献为线性z×decoderL2范数，不平方；每位置低频内部归一，保留全部4469维。原模型尺度在份额中抵消，不另挑尺度。

## 图1：多少成员承担低频贡献？

![K80](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/figures/figure1_K80_by_layer.png)

横轴实际block，纵轴达到80%贡献所需成员数。近高/远高两线，两领域分开。线越低越集中，均值可为非整数。每层使用同一合格来源位置：原高/中配对两端都必须14接口低频总贡献>0，整对筛选，再求近远共同query/head；不重配对、不以小总量删样。位置→head→query→文档等权，40文档均保留。图中的后半K80略高，固定深浅差值完整保留，未挑某层。

## 图2：实例由谁主导？

![实例](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/figures/figure2_dominant_members.png)

横轴固定24feature编号，只由原发现集sum_z排名选择；纵轴输入顺序前2篇/域，每篇近高/远高首个合格事件，共8行。前7/后7接口平均份额并排，同色标。颜色占该位置全部低频贡献的比例，没乘Attention，不重新归一到24展示列；其余质量标在右侧。如果展示列覆盖不足，只说明这些冻结列没覆盖这个实例，不能把“其余”当一个共同feature。完整4469维实例数组和每行前5真实成员分别在analysis/display_heatmap.npz、tables/display_case_top_members.csv。实例不代替领域匹配统计。冻结24列覆盖不足的事实保留，另有明确标注为事后展示的[完整原生活跃并集补图](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/display_addendum_cn.md)，不改变样本或统计。

## 图3：主导组合与领域是否对应？

![领域对应](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/figures/figure3_domain_correspondence.png)

横轴block，纵轴完整4469份额向量cosine的“同领域不同文档−跨领域”。两条线是近高/远高，严格tokenID和仅词形匹配分别画，不能混合。正值表示当前匹配位置中同域更像，不等于语义专一。严格支持覆盖13%–16%，后半−前半区间跨0。仅词形匹配覆盖更广，仍比较不同词，不能升级为严格语义验证。匹配位置差<=8、活跃低频数差<=2；原配对相对Attention及上下文、词面、文档来源等混杂仍在。

每个anchor按冻结输入协变量，分别选一个不同文档同域和一个跨域位置，未查看份额或相似度。anchor原位置权重在匹配子集内归一，再文档等权、两域各半。bootstrap不把位置对当独立：独立抽样数学/生物文档，将anchor/within/cross三个文档的抽样次数相乘，条件于已冻结匹配；误差仍不代表新语料独立确认。残余位置/数量差、参与文档和匹配覆盖全量保存。

## z=1参照与稳定性

![参照](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/figures/aux_K80_decoder_reference.png)

同一位置只保留原生z>0名单，把这些成员的幅度临时设1，乘原decoder范数。参照中的总量是任意单位激活下的计算量，不作为原模型实际幅度比较。无模型修改或前向。参照保留名单本身的语境选择，因此只能解释“给定这些名单后，decoder幅度能产生什么分布”。实际z下K80通常更低，但它的固定深浅变化仍为正；不能由静态更集中推出深度集中增强。

![有效成员数](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/figures/aux_Neff_by_layer.png)
![总量和活跃数](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/figures/aux_total_and_native_active_count.png)

所有位置原活跃数及低频总贡献完整保留；没有低频贡献记NA、不记0。position_checks.json保存不可估数量；low_total_support_quantiles.csv保存最小/1%/中位/99%总量，不按结果设阈值排除。原活跃名单不随14层改变，贡献集中度可随decoder的成员间比例改变；这不是层间首次形成或迁层。

## 全量数据与复现

|产物|用途|
|---|---|
|[layer_group_statistics.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/layer_group_statistics.csv)|每层K80/Neff/总量/正贡献成员数，实际与参照、近远/高中/窗口|
|[predefined_depth_contrasts.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/predefined_depth_contrasts.csv)|所有预定前7/后7文档配对差与区间|
|[all_positions_concentration.csv.gz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/all_positions_concentration.csv.gz)|全部7680位置×14层×实际/参照的完整原数值|
|[low_total_support_quantiles.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/low_total_support_quantiles.csv)|零总量/极小正总量诊断|
|[support_by_document.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/support_by_document.csv)|整对资格筛选和窗口支持损失|
|[retained_events.csv.gz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/retained_events.csv.gz)|实际来源、原Attention、距离、文档内层级权重|
|[unique_high_source_positions.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/unique_high_source_positions.csv)|近高/远高去重位置与token、权重|
|[matched_triples.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/matched_triples.csv)|每个anchor的同域/跨域不同文档匹配|
|[matching_coverage.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/matching_coverage.csv)|严格及词形匹配覆盖与文档数|
|[matching_residual_covariates.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/matching_residual_covariates.csv)|位置/活跃数残差，不声称完全匹配|
|[domain_correspondence_by_layer.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/domain_correspondence_by_layer.csv)|同域/跨域cosine、差值和文档区间|
|[domain_correspondence_depth_changes.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/domain_correspondence_depth_changes.csv)|预定深浅领域对应变化，含参照差异|
|[display_cases.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/display_cases.csv)|冻结展示样本|
|[display_feature_columns.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/display_feature_columns.csv)|发现集固定列与选择分数|
|[display_case_top_members.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/display_case_top_members.csv)|每例实际主导ID、份额与浅深对照|

positions目录保存实际z与参照的每层完整7680×4469份额CSR。native_low_z.npz与固定范数可精确重构；position_values.npz同时保存活跃数、总量、K80、Neff、全层有效mask。matched_similarities.npz保留每个匹配三元组的两种cosine，不删除不利样本。所有图都有表，不以二维图选成员。

复现顺序：analyze.py positions、aggregate、statistics、matching、context_statistics；然后audit.py、render_report.py。输入SHA与冻结设置见config.json，协议保持冻结。全量缓存内适用项完成；新增前向/训练/字典/聚类/候选/任务/资源/TEST均0。旧产物不覆盖，无Focus/Anchor或机制接受状态变更。全部区间为探索性点式95%，未新增p值；小样本宽区间不等于相同。

## 同一实例的名单、主导者与集中程度

冻结首例数学DOC_math_00879的admits位置159，共9个原生活跃低频成员，所有14接口都用这份名单。K80前/后半平均6.000/5.857，是整体K80略升趋势中的局部反例；主导份额从前半f2624的21.74%变为后半f7474的21.80%。这里主导者可以改变，名单并未逐层重选。另一个固定of来源有16个活跃低频成员，K80前/后半8.714/9.000。全部8例的数值在[固定实例读数](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/display_case_numeric_readings.csv)，不据此命名语义模块。

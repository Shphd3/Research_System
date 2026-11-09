# 低频贡献是否由更少成员承担，主导成员是否对应领域？

## 问题与读数

固定原来源位置、4469低频成员与14接口。K80是累计承担低频组80%贡献的最小成员数；Neff=1/Σp²。分母是低频组自己，两者越小越集中；原活跃名单不变。零低频贡献记NA，不记0。全部是旧留出上的探索性描述。

## 答案

固定前7/后7接口比较，四组实际z下的K80均值都略升，没有呈现“后半由更少成员承担”的方向。文档配对差值如下：

|领域/来源|前7平均K80|后7平均K80|后−前及95%文档区间|
|---|---:|---:|---:|
|数学／近高|3.206|3.317|+0.110 [+0.044, +0.177]|
|数学／远高|3.437|3.588|+0.151 [+0.075, +0.224]|
|生物／近高|4.170|4.597|+0.427 [+0.341, +0.521]|
|生物／远高|4.144|4.448|+0.305 [+0.220, +0.394]|

Neff同向增加，数学近高的Neff变化区间跨0；其余三组为正向描述。实际z相对z=1参照在两半都更集中，但参照也不是后半更集中，因此不能把“实际比参照集中”改写为“随层更集中”。[固定比较](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/predefined_depth_contrasts.csv) · [图1](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/figures/figure1_K80_by_layer.png)

严格tokenID匹配下，“同域减跨域相似度”的后半−前半变化：近高+0.0239，区间[-0.0074,+0.0929]；远高+0.0234，[-0.0108,+0.0628]。严格支持仅近高178／远高264锚点，分别约13.0%／16.0%合格来源位置。仅词形匹配的变化更偏正，但仍可由不同词面混杂，并且z=1参照也出现相似或更大的变化。[领域对应全表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/domain_correspondence_depth_changes.csv) · [图3](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/figures/figure3_domain_correspondence.png)

## 推进程度

这批缓存未显示“更少成员承担后半层贡献”，不能沿它继续推出“更专一”。已补齐完整4469维主导份额、不同文档比较、严格/词形匹配、离线z=1参照和活跃数/贡献总量诊断。没有新模型前向、训练、字典、候选或干预。z=1参照仍保留语境选择出的活跃名单，不是无语境基线。领域对应也不是细粒度语义或功能专一化。

原近远共同query/head4842个，经14层有效性整对筛选保留4795个，40文档均保留；窗口32:192保留3212个。极小正贡献不删除。所有区间为探索性点式区间，无新增p值，不把它们当多项同时确认。

[三图读法与完整证据](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/detailed_cn.md) · [是否激活的位置统计](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/../activation_occurrence_by_position_20261028/summary_cn.md)。研究者机制接受与下一步Unknown。

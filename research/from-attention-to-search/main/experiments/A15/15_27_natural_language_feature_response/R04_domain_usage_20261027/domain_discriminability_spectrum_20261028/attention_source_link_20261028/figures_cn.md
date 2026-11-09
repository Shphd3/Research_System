# 四张图，每张只回答一个问题

## 图1：方向整体偏在哪里？

![方向谱位置](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/figures/figure1_spectrum_position.png)

一个点＝一个固定子集在某谱段内，单位decoder平方投影的成员平均；横轴为主成分方差由大到小的16段，每段64方向；纵轴为平方投影百分比，16段加起来100%。绿色为固定集合；灰带是1000套同数量、DCLM频率及发现文档支持匹配集合的点对点95%范围，**不是文档置信区间**。每字典的数学/生物子集分别画9/7成员。先看绿线相对自己的灰带，不跨字典比绝对比例。例：SAE数学头段50.75%，背景中位39.31%。反例：SAE f11667虽头段81.95%，远高相对中等对照的变化并未确认。可支持相对背景的方向偏移；不能推出激活更强或语义更高级。

## 图2：同一集合在远处是否用得更强？

![含零贡献](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/figures/figure2_zero_inclusive_usage.png)

每点＝20篇同域文档中的同域方向子集平均；横轴近1–32/远129–160tokens，纵轴为每成员原hook贡献先除以其固定发现RMS后再等权平均，**包含未激活零值**。橙为档内高Attention，蓝为中等对照；误差棒为5000次文档重采样95%点对点区间。位置→head→query→文档逐级等权，同query/head近远共同支持。看两线各自近远变化，再直接相减，不以两组显著性是否不同代替差中差。例：SAE数学高组−0.0997，中组−0.0908，二者差−0.0089，[-0.0449,0.0272]。反例：单个f11667的高组含零原贡献上升，整体数学集合下降，个体不能代替整体。可支持当前使用模式的描述；主差中差不足以确认统一远高增强。

[出现率辅助图](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/figures/aux_activation_rate.png)与[激活后强度辅助图](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/figures/aux_active_conditional_contribution.png)分别回答更常用/用时更强；[含零原尺度图](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/figures/aux_zero_inclusive_native_contribution.png)、[激活后原尺度图](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/figures/aux_active_conditional_native_contribution.png)保留绝对量。无命中时条件强度NA，不能补0；不同feature的RMS尺度不同，原尺度和标准化结论均保留。CrossCoder贡献是共享z对最后层的解码幅值，不叫功能重要性。

## 图3：远高是否更偏低频？

![全部活跃成员低频占比](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/figures/figure3_all_active_low_frequency_share.png)

每点＝所有活跃feature的低频成员占比，先在每个前文端按活跃总数作分母，再沿同一层级等权；**不是只数Top16候选**。横轴近/远，纵轴百分比，高/中两条线沿用旧配对。每域20篇；误差棒复用旧5000次文档区间。SAE生物9.98%→8.50%是反对普遍增加的真实观察；CC数学1.92%→2.06%则是方向相反的例子，不能删。数量另表：CC数学近高5.96个低频、远高6.20个；总活跃数307.16→294.66。可支持没有一致低频增加的描述；不能按占比推断信息量或低频功能。

## 图4：统计落到了哪些真实词？

![真实来源词与反例](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/figures/figure4_real_text_sources.png)

每块＝一个按固定规则取出的真实来源事件；SOURCE为前文端，QUERY为查询token。精确位置、距离、原Attention写在图内。右侧列该处全部活跃总数、Top16命中数及原候选示例；完整活跃ID/原激活/贡献在附录，图内按Top16优先再编号排序显示少量行，不按幅度挑赢家。C块显式显示换行，D块显式显示SAE候选不响应。例子只解释具体输入，不估计总体类别比例或证明传递。

A例：数学文档DOC_math_00879的query #161 “ matching”关注#30 “ nodes”，距离131，Attention=0.000196876。该位置SAE f11667贡献8.704、f19841贡献4.489；老共有f16240贡献17.282。CC生物方向f652也在此贡献8.543，说明“偏向生物”不等于“数学中绝不出现”。B例中“ species”并未激活任何SAE Top16，却有旧生物f11399=4.832和f12478=8.441。C例换行处CC f652=10.820。D例“ exacerbated”没有SAE Top16命中，仍有旧生物f12478=3.678。语义作用仅为文本上的候选解释，不把这条边称为实际传递。

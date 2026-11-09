# 远近强 Attention 来源：低频贡献是否相对偏深层？

## 问题

同一query/head关注的远处来源，比近处来源是否在后半覆盖层多分配低频feature贡献，而且超过中等Attention的变化？这里统计的是来源token原生共享z乘各层decoder范数；不是各层独立激活。

## 答案

数学：主判据未得到清楚支持；区间和校正结果保留证据不足，不能据此说两者完全相同。 生物：主判据未得到清楚支持；区间和校正结果保留证据不足，不能据此说两者完全相同。

下表为百分点，方括号是95%文档配对区间。“深浅变化”是blocks15–27的7接口平均低频份额减blocks1–13的7接口平均份额（编号从0计）。正值才符合假设。正式判断对两域4项检验统一校正，不能只看热图颜色。

| 领域 | 高组远−近的深浅变化 | 再扣中等关注变化 |
|---|---:|---:|
| 数学 | +0.22 [-0.45, +0.93] | -0.00 [-0.44, +0.41] |
| 生物 | +0.21 [-0.49, +0.99] | +0.61 [+0.06, +1.19] |

[四项主检验与校正](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/tables/primary4_tests.csv) · [各条件深浅变化](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/tables/deep_minus_shallow_by_condition.csv)

四项统一校正后均未达到预定支持标准。生物扣中项的重采样区间略高于零，但正式signflip检验p=0.05565、校正q=0.2226；不能单凭该区间改判支持。窗口32:192检查中，高组主量数学约−0.03、生物−0.38个百分点，区间仍跨零。[窗口完整结果](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/tables/all_primary_type_contrasts.csv)

## 推进程度

最直接的认识是：低频成员的“后半层贡献变大”与“后半层占比变大”分得开。按固定前7/后7接口平均，数学近高的低频份额为8.32%→3.53%，远高为7.75%→3.18%；生物对应8.29%→4.51%、7.99%→4.42%。低频平均成员的贡献大小后半高于前半，但高频增长更多，低频份额反而下降。这是当前来源位置的一般分配特点，不能写成远高特有的低频深层化。[固定深浅均值](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/tables/depth_phase_contributions.csv)

已把“低频的绝对贡献大小”和“低频占全部成员贡献的份额”分开。平均成员的大小见[图1](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/figures/figure1_member_contribution.png)；五距离的逐层份额见[图2](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/figures/figure2_low_frequency_share.png)；预先固定的判据见[图3](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/figures/figure3_primary_contrasts.png)。训练层尺度在同一层的份额分子分母中抵消，所以原尺度不能单独修复份额结果。

原留出数学、生物各20篇；近远主比较共同支持合计4842个query/head；五档共同支持合计4635个。四频率组固定成员数为低4469、中4437、高4451、参考低支持3027，份额分母含全部16384成员。来源窗口32:192的敏感性保留40篇、3288个共同query/head，不能视为已经匹配绝对位置。[支持与损失](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/tables/support_summary.csv)

本轮完成全部适用缓存内统计和三类主图，新增前向/训练/字典/候选筛选均为0。旧留出已反复查看，因此是探索性补充。结果涉及当前来源位置的共享z成员使用权重；不说明feature首次形成层、动态迁层、长程语义、Attention因果传递或功能重要性。研究者对机制及下一步的判断仍为Unknown。

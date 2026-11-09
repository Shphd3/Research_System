# 三张主图怎么读

## 图1：平均一个成员，在哪些层实际贡献更大？

![图1](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/crosslayer_frequency_actual_contribution_20261028/figures/figure1_member_mean.png)

横轴为从0计的模型block编号1,3,…27，共14个，不是连续14层；纵轴为训练归一化空间的含零贡献范数，**刻度1代表0.001**。每点先对每feature在每文档160位置求均值，再固定组全成员等权，最后20文档等权。高/中/低组分别4451/4437/4469个成员，没激活的成员仍在分母中。阴影为5000次文档重采样95%点对点区间。

看同一层的三条线：两域高频均高于低频，28个高−低比较均过42项校正。看完整层形状，block1到3先下降、随后总体增大，不能简化为全程单调。它说明当前文本中平均成员的实际重构范数，不说明功能重要性或在哪层形成。

## 图2：高低频差异是否随领域、层变化？

![图2](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/crosslayer_frequency_actual_contribution_20261028/figures/figure2_high_minus_low.png)

每点是同文档内“高频组每成员均值−低频组每成员均值”，再对各域20文档等权；单位与图1相同。数学/生物是两组独立文档，阴影分别按文档重采样；同一文档的14层和高低组一起抽样保留配对。零线表示高低频相同，不能用两条阴影是否重叠替代领域差异检验。

实际两线全为正。直接比较两域差值，block1–21生物更大，23/25/27证据不足；不是最后层默认代表完整语义。全部14层的直接差及42项校正在[完整主表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/crosslayer_frequency_actual_contribution_20261028/tables/primary42_comparisons.csv)，[领域直接差辅助图](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/crosslayer_frequency_actual_contribution_20261028/figures/aux_domain_interaction.png)按“数学差−生物差”画零线。

## 图3：各层范数和由哪些频率成员组成？

![图3](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/crosslayer_frequency_actual_contribution_20261028/figures/figure3_frequency_composition.png)

横轴同上，纵轴每个位置的“某组成员贡献范数之和／全部16384成员贡献范数之和”，先在位置计算比例，再每文档160位置、每域20文档等权。包含高/中/低/参考低支持四组，图例给固定组大小；四组份额每位置加总100%，分母0时应NA，本数据没有零分母。阴影为文档95%点对点区间。

高频份额从block1到27，数学56.40%→83.62%、生物61.13%→82.85%；不是每一步都增加。低频数学14.26%→2.97%，生物11.93%→4.48%，但生物block19→23从3.81%回到5.12%，反对简单单调概括。这是受组成员数量影响的范数和份额，不能替代图1的平均成员，也不是解释方差或合成重构向量的长度占比。

原模型尺度三图和出现率/条件强度见[辅助结果](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/crosslayer_frequency_actual_contribution_20261028/auxiliary_cn.md)。各组实际激活支持为：

|领域|频率组|固定成员|20文档曾激活成员|每文档平均激活成员|
|---|---|---|---|---|
|数学|低频|4469|2956|472.05|
|数学|中频|4437|4160|1766.75|
|数学|高频|4451|4430|3508.55|
|数学|参考低支持|3027|532|44.55|
|生物|低频|4469|2951|446.40|
|生物|中频|4437|4060|1669.40|
|生物|高频|4451|4410|3327.90|
|生物|参考低支持|3027|674|57.10|

出现率、激活成员数来自同一个共享z，不会因为换decoder层而重新变成独立激活。
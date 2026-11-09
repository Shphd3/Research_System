# 是否激活：不同位置的完整统计

同一token位置的A22联合共享z只有一个是否激活名单。14个decoder接口共用它，因此不能测成14套独立的激活趋势。这里补齐不同文本位置/来源距离的二值出现统计，不使用decoder范数或Attention加权激活值。

定义：原生z>0为活跃。低/中/高/参考低支持固定4469/4437/4451/3027成员。活跃数量、除固定组人数的出现率、除全部活跃数的组成、至少一员活跃概率四项分开。下表为原近远共同支持、20文档/域的描述均值：

|领域/来源|全部活跃数|低频活跃数|低频组内出现率|低频占活跃成员比例|高频活跃数|
|---|---:|---:|---:|---:|---:|
|数学／近高|307.16|5.96|0.133%|1.92%|260.98|
|数学／远高|294.66|6.20|0.139%|2.06%|248.62|
|生物／近高|290.81|8.59|0.192%|2.95%|243.76|
|生物／远高|284.45|8.41|0.188%|2.90%|237.68|

出现率的分母是4469个固定低频成员；组成的分母是每位置全部活跃成员。组成先逐位置相除再逐级平均，不能从表中两个平均数直接相除。没有新p值或机制结论。

完成范围：40篇×192位置；全部16384坐标逐绝对位置出现次数；全部原来源条件的逐feature加权出现率；五距离、近远共同支持、高中Attention、四分层与窗口敏感性。低支持/缺支持保留，<10文档不计算区间。文档bootstrap5000次，旧留出反复查看，均为探索性。新增前向、训练、字典、候选和任务均0。

[图1：固定组出现率](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/activation_occurrence_by_position_20261028/figures/figure1_source_activation_rate.png) · [图2：活跃成员构成](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/activation_occurrence_by_position_20261028/figures/figure2_source_active_composition.png) · [图3：全部绝对位置](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/activation_occurrence_by_position_20261028/figures/figure3_absolute_positions.png)。每图横轴是来源位置或距离，不是模型层。点/线为文档平均；source图阴影为文档95%点式区间。绝对位置图混有词面和上下文变化，不推断语义逐步变细。

[完整数据索引](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/activation_occurrence_by_position_20261028/detailed_cn.md)。本轮统计回答出现与否，新增的组内贡献集中问题另有独立记录，不混成一种读数。研究者机制解释与下一步Unknown。

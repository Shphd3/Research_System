# 三类主图怎样读

所有主图：A22原生14层联合共享z；0起点blocks1,3,...27 residual-post。原留出20篇/域；主分层是来源与query不同tokenID且非标点。全部新统计均为已查看数据上的探索性分析。

## 图1：平均一个高频/低频成员实际贡献多大？

![图1](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/figures/figure1_member_contribution.png)

横轴是14个实际覆盖block，纵轴是固定组平均每成员的含零L2范数贡献，主图单位0.001（刻度1等于0.001）；两色是近高与远高，行分高/低频，列分领域。一个点先在来源位置用z×decoder范数，除固定成员数，再依次平均位置/head/query/文档。阴影为5000次文档重采样的95%点式区间。低频4469、高频4451成员，未激活仍进入分母。

同一层比较两色。沿曲线看贡献分配；不要把大小当份额。允许结论是该固定组平均成员在这些来源位置贡献更多/更少；不能据此推断更重要、更细语义或首次在深层形成。[完整均值及区间](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/tables/group_layer_means.csv.gz)

直接观察：近高、远高曲线都先降后升；固定后7接口的低频贡献均值高于前7接口，但高频的增长更多。没有按层另作显著性检验，曲线距离本身不是额外确认。

## 图2：低频份额如何随距离与覆盖层变化？

![图2](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/figures/figure2_low_frequency_share.png)

横轴block，纵轴五档来源距离，颜色是先在每个位置算出的“低频成员贡献范数和/全部16384成员贡献范数和”，再逐级平均。高/中Attention并排，两域分行，四面板同色标。虚线只是前7/后7接口的统计划分。五档只使用共同query/head，因此支持量与图1主比较可能不同，不能把它当同一总体的逐点替代。

看每行跨层图案是否相近；远处后半更亮只是描述，图3才检验相应预测。范数和有意不包括方向抵消，不是解释方差。不能靠热图推断长程语义。[五档支持量](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/tables/support_summary.csv)

直接观察：五档距离的行大体同向，由前部较高向后部较低；生物后段的局部回升也同时出现在多档距离及高中Attention中。没有出现清楚的“只有远高在后半特别亮”的组织图案。

## 图3：远高的额外深浅变化是否清楚？

![图3](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/figures/figure3_primary_contrasts.png)

横轴数学/生物，纵轴百分点；圆点是高Attention中远−近的“后7层平均份额−前7层平均份额”，方点再减中等Attention对应变化。一个点是文档内先做完整差值，再对文档平均。误差棒是95%配对文档区间，四项p统一BH校正。正值符合预测，负值相反，跨零保留不清楚。不能因为一项显著而另一项不显著就声称二者不同；方点直接检验它们的差异。

允许解释是当前来源位置的相对贡献组织。即使方向清楚，也不证明Attention实际传递了这些成分。[四项预定主检验](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/tables/primary4_tests.csv)

直接观察：四项统一校正后均未达到支持标准。数学扣中项接近零；生物扣中项为正，保留其正向区间与未通过校正的检验值，不把这一个点改写成假设确认。

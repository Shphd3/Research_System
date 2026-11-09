# 问题

**真实数学、生物文本中，高频与低频feature实际激活以后，对14个覆盖层的重构贡献有多大，是否随领域变化？** 本轮用A22原生联合共享z和全部16384坐标；主量是训练归一化空间中的贡献**范数**，未激活算0，固定组成员与文档等权。

# 回答

**高频组平均每成员的含零贡献，在两域全部14个覆盖block都更大；但低频成员被用到时，贡献反而更强。** 以最后block27为参照，训练空间结果为：

|文本|高频每成员含零贡献|低频每成员含零贡献|高频／低频出现率|
|---|---|---|---|
|数学|0.001879|0.000067|5.741%／0.145%|
|生物|0.001885|0.000104|5.467%／0.191%|

数学中，先逐feature/文档计算的激活时平均贡献，高频约0.0240、低频0.0363；生物为0.0255／0.0394。高频优势并不是“每次更强”，出现率差异更突出。不能把这些组均值直接相乘，算成出现次数或强度的因果份额。

**跨层使用分布随领域变化，但不是所有层都能区分。** 覆盖的block1–21（11个读数），生物的高频−低频差更大；42项统一校正后保留，最后block23/25/27的领域差异证据不足。decoder在两域完全相同，变化来自共享z和成员使用权重。

**不能把原尺度上升当作单一层深规律。** 数学低频组从block1到27，训练空间均值0.000124→0.000067，而原模型空间0.001144→0.024955；训练尺度9.199→374.350解释了两个版本的区别。低频的范数和占比，数学总体14.26%→2.97%，生物11.93%→4.48%；生物末段有局部回升，没有“越深低频越多”的统一趋势。

# 推进程度

已把旧25个受控候选的跨层图，补充为40篇真实文档（每域20、各160位置）上全部固定频率成员的实际贡献、出现率、条件强度和逐位置份额；旧层范数/训练尺度与原z直接复用。新前向、训练、字典、候选筛选和Attention分组均0。

同一个feature的跨层相对轮廓由decoder固定；这些数值不是逐层独立激活、功能重要性或首次形成位置。结论用于继续讨论当前文本的使用权重，原留出已反复查看，全部属于探索性补充。[三张图与读法](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/crosslayer_frequency_actual_contribution_20261028/figures_cn.md) · [真实数值例子和完整解释](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/crosslayer_frequency_actual_contribution_20261028/detailed_cn.md) · [辅助/原尺度结果](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/crosslayer_frequency_actual_contribution_20261028/auxiliary_cn.md) · [数据与复现](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/crosslayer_frequency_actual_contribution_20261028/data_index_cn.md)

# 一页简版：分发校准有效，留出学习尚未受益

**目的。** 在固定预算下改善专家分工。本轮先检验：让含低频feature的输入到达指定专家，是否能改善下一token预测。低频指字典原子在TRAIN中少出现，不等于困难或未知知识。

**模型与对照。** 冻结Qwen3-0.6B Base、CrossCoder和原输出头；第28层末端增加8个完整SwiGLU专家，每位置选1个。T频率名单、R11固定随机名单，各比较S0原评分、S1组级校准、S2条件幅度校准、S3频率与幅度校准；另两个学习router参考。S1是事前主方案，10条件×2训练seed均完成同样3轮。

**三条认识更新。**

1. **评分确实影响接收。** T的S1使低频接收0.0023%→33.4%，零接收960→5；S2仍为0%，S3达41.7%。接收改善不等于输入已同频。[分发图](../normalized_route_learning/figures/figure5_dispatch_outcomes.png)。
2. **接收改善没有带来本轮留出学习收益。** S1相对原评分的低频NLL差为+0.1807/+0.1853，变差；相对随机S1虽低0.0326/0.0256，仍未通过联合门槛。20个终点均差于冻结基座。TRAIN拟合下降而EVAL上升，需要先解决泛化/更新强度问题。[配对图](../normalized_route_learning/figures/figure8_primary_paired_differences.png)。
3. **本例没有安全的新输入归属。** 排除feature2命中位置训练背景后，分别适配8个专家：94个留出位置的NLL全上升，旧损害0.0206–0.0517，全超0.01。不能把事后最低损失专家当安全推荐。[适配图](../normalized_route_learning/figures/figure10_target_assignment.png)。

**边界。** NLL越低越好；低频主指标先算每feature命中位置均值再等权平均，位置有重叠。两个模型seed、一个随机名单；文档独立性未知，EVAL此前已查看。这里只检验冻结表征旁支，不证明容量提升、语义分工或φ学习效用。原h仍保留common信息。机制判断待研究者讨论。

**唯一下一问题（AI建议，未运行）。** 用独立开发集预先固定各条件共用的较小更新强度后，在新留出文本上A/B/C差异是否仍存在？先区分当前学习设置的泛化失败与评分组织差异。

[完整概要](../../../Projects/from-attention-to-search/main/experiments/A15/15_21_activation_to_expert_learning/20261019_normalized_learning/summary_cn.md) · [完整报告与全部结果](../../../Projects/from-attention-to-search/main/experiments/A15/15_21_activation_to_expert_learning/20261019_normalized_learning/detailed_cn.md) · [逐图解释/术语](../../../Projects/from-attention-to-search/main/experiments/A15/15_21_activation_to_expert_learning/20261019_normalized_learning/figures_cn.md) · [冻结Protocol](../../../Projects/from-attention-to-search/main/experiments/A15/15_21_activation_to_expert_learning/20261019_normalized_learning/protocol_cn.md)。

## 讨论时看哪几张图

图5先回答“有没有改变实际接收”；图7/8再回答“是否学得更好”；图10最后回答“目标留出条件下是否有安全归属”。不要把这三个问题合成一条已经证实的机制链。

## 两个追问

**为什么B−A与B−C都要看？** 前者在同T名单内改变评分尺度，后者在同S1下改变名单组织。B只比C好、却比A坏，不能满足事前主张；负载/曝光仍随策略改变。

**为什么不能说同频专家无效？** 本轮只测冻结表征、一个随机名单、固定优化预算；所有条件对基座留出都恶化，尚未在可保持泛化的旁支更新范围内区分组织作用。

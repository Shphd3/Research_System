# 今日讨论：均值成分与频率路由

本轮检验“高频feature是否主要组成真实表征均值”，并固定名单比较除均值与减均值。冻结分析、必要同位置前向已完成，没有训练专家或提交新外部任务。

- 最高频段平均向量沿真实TRAIN均值方向投影−0.0931；预处理均值与解码偏置不能漏掉，不能把高频幅度直接叫作表征均值。
- 最低频feature平均接收：原始0%，比值72.22%，减法17.58%。减法低频段接收的位置虽更多，其中87.33%根本没有原始最低频段激活。
- 原表征中心化：最低频接收仍0%，每维MSE33.59→61.99，平均激活数304.69→415.49。编码失配限制机制解释。

范围：85548TRAIN／22446既有复核答案预测位置，固定四段×两子组；已有复核不是独立确认。每feature接收不等于位置占比，更不等于学习收益。负载均匀也不代表有效分工。

AI建议的唯一下一决策：是否只保留R1比值评分作为下一次另行批准的学习对照候选，与R0比较。此处不启动训练。

[一页](../../../Projects/from-attention-to-search/main/experiments/A15/15_23_mean_component_frequency_routing/20261019_mean_component_routing_20261019T082513Z/one_page_cn.md) · [完整结论](../../../Projects/from-attention-to-search/main/experiments/A15/15_23_mean_component_frequency_routing/20261019_mean_component_routing_20261019T082513Z/summary_cn.md) · [详细方法和限制](../../../Projects/from-attention-to-search/main/experiments/A15/15_23_mean_component_frequency_routing/20261019_mean_component_routing_20261019T082513Z/detailed_cn.md) · [五张图和读法](../../../Projects/from-attention-to-search/main/experiments/A15/15_23_mean_component_frequency_routing/20261019_mean_component_routing_20261019T082513Z/figures_cn.md) · [全部源表](../../../Projects/from-attention-to-search/main/experiments/A15/15_23_mean_component_frequency_routing/20261019_mean_component_routing_20261019T082513Z/tables_index_cn.md) · [固定文本](../../../Projects/from-attention-to-search/main/experiments/A15/15_23_mean_component_frequency_routing/20261019_mean_component_routing_20261019T082513Z/texts/cases_cn.md)。

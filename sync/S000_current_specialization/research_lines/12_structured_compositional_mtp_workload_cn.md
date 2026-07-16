# 12 结构化组合任务与标准头使用

## 当前问题

A11 的更早直接信号，能否在每个样本都重新生成规则、并要求一步或两步有序查表的任务中，更明显地加速两步任务的标准主头学习？

## 已确认的边界

固定规则表 E02 可以被 NTP 和 MTP 精确拟合，但正交互只出现在准确率恰好为 `1.0` 的最后阶段，不能支持一般收敛优势。E03 又因一步与两步任务的查询相关结构不对称而被拒绝。

E04 随后定义逐样本双映射平衡载体，并完成全部 12 条批准的 NTP Stage A 轨迹。没有模型规模合格：2 层两步任务结束在约 `0.250`，4 层两步任务约 `0.329`；4 层一步任务虽然两个种子接近 `0.999`，仍有一个种子停在 `0.838`。因此没有冻结掌握阈值。

后验审计还发现删行必要性守卫无效：完整双射删去一行后，缺失输出仍可由其余四行没有使用的值补全。E04 只能作为能力地板描述，不能形成正式 MTP 比较。

## 唯一下一决策

决定是在冻结的 2/4 层、20,000 步合同下关闭 E04，还是用新 Protocol 重开载体/能力设计。Stage B、封存确认比较和所有 MTP 运行继续阻塞。

来源：[A12 索引](../../../Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/README.md) · [12_0 锚点](../../../Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_0_short_range_single_vs_two_step_composition/12_0_short_range_single_vs_two_step_composition_anchor.md) · [E04 总结](../../../Projects/from-attention-to-search/main/experiments/A12/12_0_short_range_single_vs_two_step_composition/A12_0_E04_balanced_per_sample_dual_map/summary.md) · [详细记录](../../../Projects/from-attention-to-search/main/experiments/A12/12_0_short_range_single_vs_two_step_composition/A12_0_E04_balanced_per_sample_dual_map/detailed.md)

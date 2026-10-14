# 结果摘要：特征图层级与跨层解码幅度分布

## 目的

回答：统计图层级较高的Feature，其跨层解码幅度分布是否更偏深层？本轮只比较已有CrossCoder结果，不评估共享／分离学习或专家分发。

## 模型

固定最终14层、16,384特征CrossCoder。主集合为D/V支持均≥200且V图非孤立的15,537个Feature。h是完整V统计图到叶节点的最长出边路径；p是同一Feature在14层的decoder范数占比。L是按p加权的一基实际模型层号，**只表示幅度平均位置，不能代表整个分布移动**。每Feature等权，未训练或推理。

## 假设

原预期是较高h整体对应更深的解码分布。竞争解释是建边规则耦合频率与h，以及层尺度／重构保真差异。以全体L、完整p／热图和预定频率比较共同检查，不能由局部图或单个相关系数定结论。

## 结论

**整体数据不支持“层级越高，幅度平均位置整体越深”。** 主描述性Spearman为−0.277976；D图为−0.279321，raw坐标为−0.157788。h=1到3的L中位数依次为19.902、15.007、14.305；h=4有回升，不能改写成严格单调规律。[整体与参照统计](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/depth_vs_layer_summary.csv)。

| 图层级h | Feature数 | L中位数 | L四分位范围 |
|---|---|---|---|
| 0 | 20 | 22.717 | 22.321—23.414 |
| 1 | 8,896 | 19.902 | 14.319—22.759 |
| 2 | 5,347 | 15.007 | 12.660—20.696 |
| 3 | 1,209 | 14.305 | 12.420—18.297 |
| 4 | 63 | 16.226 | 13.527—19.187 |
| 5 | 2 | 18.509 | 16.704—20.313 |


**分布形状不是单纯平移。** 14层平均p表显示，h=1、2、3的第2层平均占比分别15.39%、25.06%、30.20%，第28层分别17.00%、13.95%、13.25%，浅层与深层幅度并存。最高h=5只有937、3461两个节点，L分别22.118、14.899；同层级可有不同轮廓，不能据两点推断最高级总体。完整14层均值见[各层级14层平均p](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/hierarchy_mean_p.csv)，个体轮廓见图2。

**频率解释仍未排除。** 11个可比较格中7正4负，格差值中位数+0.194模型层；它是格间摘要，不是全体Feature的调整后效应。局部混合结果不能挽救整体假设，也不能证明频率造成了整体反向。没有通过门槛的单一固定频率格；新澄清规则已实现。[全部频率比较格](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/frequency_overlap_comparison.csv)。

## 分析与限制

图1固定两锚点展开30节点101边；图2同30节点；图3含全部15,537节点。640缓存块约15.0GiB全部读取并核对hash，30节点计数匹配，交付150随机＋90高激活记录。远程任务pt-icv8hyi3在4卡H100 Reserved上计算64.13秒，峰值aggregate RSS约3.55GiB；另有图1排版修正及交付核对成本，见完成回执。

D/V为同bin复核，原文档独立性未知，V参与过筛选；节点不独立，不报告p值／置信区间。固定频率区间及5分位仍不是严格频率匹配。第28层已有FVE86.4722%、替换CE+0.305962nats限制保留。这些结果不能证明层功能、语义复杂度、层间因果组合或专家收益。科学状态和下一步由研究者裁定。

入口：[三类图及读图说明](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures_cn.md)；[全部源表索引](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables_cn.md)；[全部随机／高激活文本](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/text_examples_cn.md)；[完整中文报告](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/detailed_cn.md)。本轮交付后停止。

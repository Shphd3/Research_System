# 频率区间残差MoE旁支

受控执行完成；主学习比较NOT RUN，原因是原评分导致A前三专家零路由、八专家覆盖资格不通过。工程smoke PASS不代表学习收益。

[一页中文概要](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/frequency_interval_residual_moe/summary_cn.md) · [完整Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/frequency_interval_residual_moe/protocol_cn.md) · [Detailed与三类图](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/frequency_interval_residual_moe/detailed_cn.md) · [执行目录](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z)

任务pt-vv7zkyxf，pipeline72.46秒，CPU分析22.55秒。旧结果保留，未commit/push，未启动下一轮。

后续已完成[逐feature分发诊断](../meeting_report/meeting_brief_feature_dispatch_cn.md)：只解释既有路由，未启动新评分或正式学习。原执行与本轮诊断保留独立目录。

# 10月22日：频率分发与语义组合的研究推进

[本日讨论入口](meeting_report/meeting_brief_moe_meeting_questions_cn.md) · [English](README.md)

本次先核对普通MoE与负载均衡对照，再结合导师的rank-one直觉，研究自然文本中高低频语义原子的组合关系。对照保存产物审计通过；新缓存统计在同词、同来源子集中保留特定搭档关联，但同旧路由匹配的支持不足。没有新增模型训练。

准备组会先读讨论稿第10节及可直接讲的版本。下一候选问题是：同一个低频语义原子与哪些高频原子的组合能够跨文本复现，旧频率分发是否把这些组合混在一起？[候选Anchor](../../Projects/from-attention-to-search/main/research_notes/frequency_routing_rank_one_20261022_candidate_anchor_cn.md)给出目的、假设、模型、数据与决定分支，保留为AI建议。会议原文及更新来源在讨论稿同目录的`sources/`与`source_manifest.json`。

第1–9节保留独立构造关系任务的证据：位置/顺序敏感性和共同变化方向。其正式记录仍由[项目Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_18_context_relation_organization_use/first_flow_v3/summary_cn.md)与[Focus](../../Projects/from-attention-to-search/main/focus/focus_context_relation_organization_use_cn.md)持有，不用该任务替代自然文本频率分析。

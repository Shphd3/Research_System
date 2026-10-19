# 10月18日：CrossCoder结构、分发与下一决策

[English](README.md) · [项目路线](../../Projects/from-attention-to-search/main/roadmap.md)

**当天讨论主入口：[低频feature为何没有到达负责专家](meeting_report/meeting_brief_feature_dispatch_cn.md)。** 汇总问题、模型、三条证据、四张图、近期六段结果与唯一待讨论决策。今日诊断计算完成；新评分、重分组及学习实验没有启动，科学解释待研究者审阅。

- [本轮正式Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/feature_group_to_actual_dispatch/20261018_routing_audit/summary_cn.md)／[Anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/crosscoder_feature_relations/feature_group_to_actual_dispatch/anchor_cn.md)／[Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/feature_group_to_actual_dispatch/20261018_routing_audit/protocol_cn.md)／[Detailed](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/feature_group_to_actual_dispatch/20261018_routing_audit/detailed_cn.md)：正式研究材料归项目。
- [近期结果项目索引](/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/qwen3_crosscoder_tooling/20261018_routing_progress_cn.md)：串联关系图、跨层decoder、旧学习、φ探索、八专家smoke与本次逐feature诊断，保留各自边界。
- [八专家旁支前序执行](frequency_interval_residual_moe/README_cn.md)：原评分覆盖未过，正式学习NOT RUN。
- [既有φ关系组阅读入口](phi_relations/README.md)：独立探索材料，未因本轮而重写。
- [本日四图来源与可放大文件](figures/SOURCES.md)。

此页是阅读导航，非新设计、Focus状态或科研批准。

## 给主任agent的便携讨论包

[下载ZIP结果包](../backup/2026/10/cleanup_20261019/1018/feature_dispatch_routing_audit_20261018_portable.zip) · [先读交接稿](feature_dispatch_routing_audit/director_agent_handoff_cn.md) · [包内目录](feature_dispatch_routing_audit/README_cn.md) · [打包校验回执](feature_dispatch_routing_audit_package_receipt.json)

包内含双语Anchor／Protocol／结果、四图的PNG／SVG／PDF、选定完整逐feature表与12张文本卡；不含模型或激活缓存。离线阅读链接及源hash已核对。

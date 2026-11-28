# 小模型 MoE：长尾特征应该怎样分给专家？

本地独立研究项目。目标是在总体预测质量受控时，降低小模型学会长尾细节所需的训练 token 与计算。当前有一个待裁定的候选问题：两个特征共用参数时，一方学到的东西能否改善另一方在新文本上的预测？

| 需要做什么 | 从这里进入 |
|---|---|
| 判断本轮问题与首个 ablation | [项目总入口](../../research/small-model-moe/README.md) · [组会讨论稿](../../daily_research_reports/1128/meeting_report/feature_grouping_cn.md) |
| 继续研究记录 | [探索日志](../../research/small-model-moe/main/explore/1128_feature_grouping/log.md) |
| 查理论原稿或旧实验 | [理论推导库](../../research/small-model-moe/sources/theory/README.md) · [完整历史副本](../../research/small-model-moe/history/README.md) |
| 查代码 | [本项目代码](code) · [协作仓中的作者工作区](../small_model/users) |

从系统根目录用 Python 3 和 Matplotlib 运行 `python Projects/small-model-moe/code/1128_meeting_figure.py`，即可从共享执行盘的留出评估 CSV 重画[组会图与数值表](../../research/small-model-moe/main/explore/1128_feature_grouping/figures/SOURCES.md)。

本目录承载问题摘要和可运行代码，[main](main) 通向本轮研究，[research](research) 通向含原件与历史的完整目录。上游协作仓继续位于 Projects/small_model，训练输出归执行工作区。当前成果与研究者的下一步选择见探索日志。

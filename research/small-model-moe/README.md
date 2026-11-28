# 小模型研究：用更少的数据和计算学会长尾

**本轮候选。** 在浅层共享、中后层专门化的学生里，两个低频特征何时值得共用叶专家？提议用一方的参数更新能否改善另一方在独立文本上的预测作判据。已有深四层教师路由在 30 亿训练 tokens 时比 A0 的稀有词 PPL 低 6.35，总体 NLL 低 0.00780。跨父复用能否增加这项收益仍待检验。[30 亿配对结果](/data/250010109/MoE_Router/experiments/1127_qwen_hd4_oracle/runs/formal/Qwen-HD4-Oracle/paired_3000000000.csv)

| 阅读顺序 | 内容 |
|---|---|
| [11 月 28 日组会稿](../../daily_research_reports/1128/meeting_report/feature_grouping_cn.md) | 一分钟口播、导师明确待办、HRJ 自述安排、目的与候选实验。 |
| [前两轮做到哪里](main/research_notes/1128_prior_work.md) | Qwen 表征、真实与合成长尾学习、历代学生与教师拓扑、同预算留出表、CHJ 与 HRJ 的结论边界。 |
| [本轮探索日志](main/explore/1128_feature_grouping/log.md) | V5 逐项修订、单样本宽度推导、合学判据、最小对照、何时值得改架构。研究者决定为 Unknown。 |
| [理论原件](sources/theory/README.md) · [会议原件](sources/meetings) | 早期分组与可分性、V5、两份 V6.2、验证报告、11 月 23–28 日的一手记录。 |
| [历史副本与校验](history/README.md) | 旧项目完整 main、分支资料及历史执行记录，保留原有层次、原解释和归属。 |
| [本项目代码](../../Projects/small-model-moe/README.md) · [组内协作仓](../../Projects/small_model/users) | 本地科研与上游合作者更新的两个入口。 |

系统 Git 保存本轮研究文字、原始 Markdown 推导、项目代码与历史校验摘要。会议原件、PDF 和整份历史快照可在共享工作区查看。

新的问题讨论追加在 main/explore 的相应日志；源文放 sources，历史快照放 history，组会材料按日期放 daily_research_reports。候选承接原项目在办问题 2「特征层级与 expert 分发」。是否将其确认为新项目首要在办问题，由研究者决定。[系统项目表](../../PROJECTS.md)

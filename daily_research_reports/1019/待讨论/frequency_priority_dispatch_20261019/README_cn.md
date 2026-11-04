# 10月19日待讨论：频率优先与实际分发

本包是已完成结果的派生阅读副本，供研究者与Agent讨论。**不新增科学结论，不授权新实验。**

建议阅读：[交接说明](handoff_report_cn.md) → [Summary](summary_cn.md) → [图册及术语](figures_cn.md) → [Detailed](detailed_cn.md)。也可读[当日原讨论稿副本](discussion_cn.md)。[English](README.md)。

## 包内内容

- [用户Anchor](design/anchor_cn.md)、[Protocol](protocol_cn.md)、[冻结实现](design_freeze.json)，及双语Summary／Detailed／下一问题。
- 全部19幅图，每幅PNG／SVG／PDF；图B共14页，图C三页，A为流程示意，D为关系增量。
- 184张[可读文本卡](text_cases_cn.md)及[完整机器文本卡](texts/dispatch_text_cases.json)，保留token ID、真实位置和完整可见前文。
- `tables/`：组成员、逐低频目标、全部可靠feature负责接收、完整实际feature列表、配对变化、固定关系边、随机／区间／代价等最终证据表。
- [科研推理审计](reasoning_audit_cn.md)、`provenance/`中的选定核验回执、[文件来源与hash](payload_manifest.json)。

## 保留的结论和边界

七个可运行策略均完成；F完全集中，T在65,402个EVAL位置中65,401个仍进同一专家，低频960/964仍零接收。Tφ改变175个成员的负责名单，但实际route与T逐位置相同；优化组内关系目标没有自动改善分发。随机参考增加接收但头部频率差距仍大，不能宣布整体成功。

P因缺同位置原预处理14层联合H而NOT RUN；未用末层h或zD替代。EVAL已被查看、文档独立性未知。本轮未训练专家，未测试学习／容量收益。下一方向仍是[AI建议](next_decision_cn.md)，具体评分校准和任何后续运行均待研究者决定。

## 打包范围

这是便于离线阅读和核对最终图表的精选结果包，**不含模型权重、hidden/z激活缓存、原始bin语料、NPZ矩阵、原始日志或执行代码**。完整结果表按直接引用和讨论需求选择，不是整run复制；本包不能独立重做原始缓存统计。包外来源改为[明确清单](provenance/external_sources.md)，包内阅读链接均为相对路径。

原正式结果仍在项目 `main/experiments/A15/15_20_frequency_priority_actual_dispatch/20261019_dispatch/`。复制只改阅读链接，中文Anchor、Protocol和冻结原件保持原字节，统计与科研状态不变。

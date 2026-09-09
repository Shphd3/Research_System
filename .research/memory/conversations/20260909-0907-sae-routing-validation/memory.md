# Conversation Memory: offline hierarchy parameter scaffold

Conversation name: 0907-SAE 路由有效性验证
Source conversation ID: 01a07c43-d099-7d63-8e11-83867d8f7c6b
Created at: 2026-09-09T08:39:00Z
Updated at: 2026-09-09T08:39:00Z
Continues from: .research/memory/conversations/20260908-sae-balanced-routing/memory.md

## Objective

完成两阶段离线分析的初步本地框架、层级参数规划与接续记录，完整实验留待后续。本文为非规范工作上下文；不替代正式设计、批准或结果。旧接续记录仍保留其训练后分析工作，不用本次离线范围覆盖它。

## Current State

执行目录：`/data/250010109/MoE_Router/experiments/20260909_sae_hierarchy_offline_analysis/`。
截图中的七个文件已存在。本轮补充README、参数耦合审计、逐边激活指标与逐层词元覆盖、只读缓存审计及安全软件检查入口。21项合成测试通过，源码编译检查通过；未拟合完整真实数据、未创建新正式运行、未训练、未提交远程任务。
实际完成范围和未实现项以该目录README为准：原记录/缓存真实接入、全量调度、打乱副本资格、文本/条件熵和最终绘图尚未完成。`render_results.py`未创建，不是漏掉已有结果。

## Working Understanding

已核验：旧图深度0–3是四层，学长旧图0–5是六层。旧深度函数无最大3截断。阶段二2×4组预算不是原子图深度。
代数关系：反向包含率=正向包含率/频率比。0.90正向下限与0.70反向严格上限隐含频率比>1.286；1.2降到1.1单独无效，现作负对照。
待验证解释：高频候选池或旧选边顺序跳过中间节点。合成嵌套集合在旧/近频率排序下发现深度1/4，但两者联合预测增益均不合格；不能当真实机制证据。
找到旧E17逐词元数组，发现261632行、复现261634行，均32个正槽位；只读哈希/结构检查通过。尚缺原记录映射、采样与完整模型身份及跨数据重复审计，正式`token_relation_cache`仍为空。片段缓存不能替代词元激活。

## Decisions And Constraints

当前请求仅初步实现、规划和memory；不运行完整扫描。其操作范围已记入实现计划首段，仍非正式Protocol。保持同一SAE的30000原子/top32，不人为补节点、不删边消环、不追求六层达标。不修改Focus/Anchor/Graph，不覆盖旧实验，不提交Git或外部同步。
优先对比候选池与选边顺序；支持量、冗余频率比、反向门槛单列诊断。发现/复现双改及组合档默认延后。0.5是我们明确定义的弱包含诊断，不冒称学长图复现。分别报告发现、旧规则复现、支持量合格三张图。
记录成对重抽样当前函数采用来源×标签分层，是较初稿来源分层的明确待确认细化。

## Open Loops

1. 认证候选词元缓存，恢复过滤后词元到原记录/文本映射；失败则先明确仅匿名词元探索的范围，不能输出记录级区间或例子。
2. 小规模真实子集的时间/峰值内存检查，补逐候选拒绝与链条稳定性输出。
3. 研究者确认最小真实参数诊断、输入标签、2×4及重复预算后，完善两阶段真实接入和产物；不自动执行所有预设。

## Resume Point

先读实现计划第9节和工作区README，再检查`local_checks/historical_token_cache_audit.json`列出的身份/映射缺口。不要从远程训练或旧S0–S6流程续跑。若后续仅让解释参数，保持只读；若批准完善实现，按缺口推进并重复合成测试，完整扫描另确认具体范围。

## Canonical References

- `daily_research_reports/0909/sae_offline_two_stage_implementation_plan_cn.md`：唯一维护的方法/参数与实现计划，仍为建议而非Protocol。
- `daily_research_reports/0909/sae_hierarchy_clustering_todo_cn.md`：历史参数与原文来源，不维护第二套方案。
- 执行目录`README.md`、`hierarchy_presets.json`、`local_checks/framework_verified_20260909.json`：软件职责、预设、21项测试及源码身份。
- 执行目录`local_checks/historical_token_cache_audit.json`：只读检查与未合格事项。
- `/data/250010109/MoE_Router/experiments/20260904_a15_13_e17_sae_hierarchy/runs/threshold-sweep-20260904/threshold_sweep_summary.json`与`hierarchy_core.py`：旧图层数、门槛及排序的实际证据。

本项尚无正式Protocol、Summary或Detailed，不从这些接续文字推导科学批准。

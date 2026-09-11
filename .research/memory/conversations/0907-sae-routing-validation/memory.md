# Conversation Memory: 0907-SAE 路由有效性验证

Conversation name: 0907-SAE 路由有效性验证
Processed by: Codex (harness: Codex app-server; model: unknown)
Source conversation ID: 01a07c43-d099-7d63-8e11-83867d8f7c6b
Created at: 2026-09-09T08:39:00Z
Latest update at: 2026-09-09T08:39:00Z
Continues from: .research/memory/conversations/sae-balanced-routing/memory.md
Environment: container /data/250010109 (`repo`=Research_System, `exec`=MoE_Router);
  also read from the Windows checkout C:\Users\250010109\data\Research_System.
  /data is a network mount (quarkfs_client); /root/** is container-local and lost
  on recycle. From the Windows checkout, `exec` and /root/** are not-visible.

## 2026-09-09T08:39:00Z -- 离线框架脚手架与接续记录

- Summary: 完成两阶段离线分析的初步本地框架、层级参数规划与接续记录，完整实验留待后续；旧接续记录仍保留其训练后分析工作，不用本次离线范围覆盖它。执行目录：`/data/250010109/MoE_Router/experiments/20260909_sae_hierarchy_offline_analysis/`。截图中的七个文件已存在；本轮补充 README、参数耦合审计、逐边激活与逐层词元覆盖指标、只读缓存审计及安全软件检查入口。21 项合成测试通过、源码编译检查通过；未拟合完整真实数据、未创建新正式运行、未训练、未提交远程任务。实际完成范围以该目录 README 为准：原记录/缓存真实接入、全量调度、打乱副本资格、文本/条件熵和最终绘图尚未完成；`render_results.py` 未创建，不是漏掉已有结果。已核验：旧图深度 0–3 是四层、学长旧图 0–5 是六层；旧深度函数无最大 3 截断；阶段二 2×4 组预算不是原子图深度。代数关系：反向包含率=正向包含率/频率比；0.90 正向下限与 0.70 反向严格上限隐含频率比>1.286；1.2 降到 1.1 单独无效，现作负对照。待验证解释：高频候选池或旧选边顺序跳过中间节点；合成嵌套集合在旧/近频率排序下发现深度 1/4，但两者联合预测增益均不合格，不能当真实机制证据。旧 E17 逐词元数组 261632 行、复现 261634 行，均 32 个正槽位，只读哈希/结构检查通过；尚缺原记录映射、采样与完整模型身份及跨数据重复审计，正式 `token_relation_cache` 仍为空，片段缓存不能替代词元激活。约束：保持同一 SAE 的 30000 原子/top32，不人为补节点、不删边消环、不追求六层达标；不修改 Focus/Anchor/Graph，不覆盖旧实验，不提交 Git 或外部同步；优先对比候选池与选边顺序，支持量、冗余频率比、反向门槛单列诊断；发现/复现双改及组合档默认延后；0.5 是明确定义的弱包含诊断，不冒称学长图复现；分别报告发现、旧规则复现、支持量合格三张图；成对重抽样当前函数采用来源×标签分层，是较初稿来源分层的明确待确认细化。
- Current work: 无新执行。当前请求仅初步实现、规划和 memory；范围已记入实现计划首段，仍非正式 Protocol；不运行完整扫描。
- Next action: 先读实现计划第 9 节和工作区 README，再检查 `local_checks/historical_token_cache_audit.json` 列出的身份/映射缺口。不要从远程训练或旧 S0–S6 流程续跑。若后续仅让解释参数，保持只读；若批准完善实现，按缺口推进并重复合成测试，完整扫描另确认具体范围。
- References: `daily_research_reports/0909/sae_offline_two_stage_implementation_plan_cn.md`（唯一维护的方法/参数与实现计划，仍为建议而非 Protocol）；`daily_research_reports/0909/sae_hierarchy_clustering_todo_cn.md`（历史参数与原文来源，不维护第二套方案）；执行目录 `README.md`、`hierarchy_presets.json`、`local_checks/framework_verified_20260909.json`（软件职责、预设、21 项测试及源码身份）；执行目录 `local_checks/historical_token_cache_audit.json`（只读检查与未合格事项）；`/data/250010109/MoE_Router/experiments/20260904_a15_13_e17_sae_hierarchy/runs/threshold-sweep-20260904/threshold_sweep_summary.json` 与 `hierarchy_core.py`（旧图层数、门槛及排序的实际证据）。

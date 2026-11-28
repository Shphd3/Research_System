# Conversation Memory: 梳理小模型研究并创建项目

Conversation name: 1128 小模型长尾研究推进与科研系统整理
Conversation ID: 01a220d7-eddc-7423-92d8-5dfa9e03619f
Processed by: Codex (harness: Codex desktop; model: unknown)
Created at: 2026-11-28T06:55:44Z
Latest update at: 2026-11-28T09:35:47Z
Continues from: ../1125-V6长尾学习动力学/memory.md and ../1126-sae-特征聚类与表征分析/memory.md
Environment: repo=/data/250010109/Research_System, exec=/data/250010109/MoE_Router, upstream=/data/250010109/Research_System/Projects/small_model

## 2026-11-28T06:55:44Z -- 启动小模型独立研究项目

- Summary: 已读两条源对话、原始理论、11 月 27 日逐字稿和 28 日 HRJ 沟通，并拉取组内协作仓。旧项目研究记录与理论原件已导入独立项目。现有训练证据复核至 Qwen-HD4-Oracle 正式 30 亿 token 留出结果。
- Current work: 当前讨论承接原项目问题 2。研究者尚未裁定以跨文档双向更新收益作为合学指标。已完成会议材料、条件推导与候选对照，未执行新增配对干预或训练。
- Next action: 等研究者修改或选择本轮问题。若选择该指标，按探索日志锁定同一字典、同一存档和发现/验证文档，先测一次可撤销更新在独立文本上的作用；分组证据不足时先校准代理。远程执行和训练预算由研究者决定。
- References: [项目表](../../../../PROJECTS.md)只增加项目导航，首要问题待裁定。[组会稿](../../../../daily_research_reports/1128/meeting_report/feature_grouping_cn.md)区分导师要求、HRJ 安排与 AI 建议。[探索日志](../../../../research/small-model-moe/main/explore/1128_feature_grouping/log.md)保存条件推导与跑前预测。[历史与新结果](../../../../research/small-model-moe/main/research_notes/1128_prior_work.md)定位同预算原始证据。[旧记录复制口径](../../../../research/small-model-moe/history/README.md)给出研究资料的恢复入口。

## 2026-11-28T09:26:15Z -- 系统整理完成与续研

- Summary: 对话已改名为「1128 小模型长尾研究推进与科研系统整理」。本记录沿用原路径。Projects 顶层保留 10 个项目，另有 archive/ 集中存放 Ruijun、Decommon 训练与评估以及 diffusion 四个项目。
- Current work: KV 合并至 Projects/kv_cache，main 快进至 a252bae。依研究者要求删除本地 DXY 与 xyDeng。SCO 训练资料合入 sco-control，已安装控制技能仍指向 sco-skill，公开指南保留为分支。scholar-mode 工程已从 Projects 删除，含未推提交的副本保存在 /data/250010109/.local/share/Trash/files/scholar-mode-20261128-092229。系统内同名研究技能可用，旧 Sidecar 默认程序路径随工程移除。Ruijun 归档内有 160 个原有缺目标的内部相对链接。
- Next action: 回到本轮小模型长尾问题，请研究者裁定或修改跨文档更新收益这一合学判据，再依探索日志决定最小诊断。当前无新增实验与预算决定。
- References: [系统组织图](../../../../docs/system_map.html)、[项目表](../../../../PROJECTS.md)、[归档索引](../../../../Projects/archive/README.md)、[组会稿](../../../../daily_research_reports/1128/meeting_report/feature_grouping_cn.md)、[小模型探索日志](../../../../research/small-model-moe/main/explore/1128_feature_grouping/log.md)。工作树入口检查 155 项通过。科学判断由探索日志及其源证据承载。

## 2026-11-28T09:35:47Z -- 四项目归档与多节点训练技能

- Summary: 依研究者的新指示，KV、旧 SCO、NTP 和 router-representation-coupling 均移至 Projects/archive。Projects 顶层保留六个工作目录，归档八个项目。当前本机安装的技能为 sco-control-training，源在 Projects/sco-control。
- Current work: HTML 流程图把实验名称及其 Anchor、Protocol、项目代码与配置、可外置的执行目录、结果回链及 Git 归档串联。已验证归档路由项目的 22 份 Git 记录和 NTP 仓自检。本轮为目录整理与本机安装。
- Next action: 按先前讨论继续裁定小模型长尾特征合学判据。实验资源和启动时点仍待研究者决定。
- References: [流程图](../../../../docs/system_map.html#workflow)、[归档索引](../../../../Projects/archive/README.md)、[训练技能](../../../../Projects/sco-control/skills/sco-control-training/SKILL.md)、[本轮研究问题](../../../../research/small-model-moe/main/explore/1128_feature_grouping/log.md)。

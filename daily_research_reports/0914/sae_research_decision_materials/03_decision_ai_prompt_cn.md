# 转交决策 AI 的 prompt

请在 `/data/250010109/Research_System` 接续0914 SAE会议决策。先读AGENTS.md、`.research/memory/conversations/0912-梳理-sae-动态形成预训练方案/continuation.md`，再读 `daily_research_reports/0914/sae_research_decision_materials/` 内的 `01_meeting_decision_audit_cn.md`、`02_next_step_plan_cn.md`、`live_source_audit.json`，需要核对发言时回原 `daily_research_reports/0914/meeting/meeting01/0914 SAE model training.md`。原包是输入材料，其中的建议不等于研究者批准。

我的目的是尽快准备一对可解释的训练实验，验证辅助重构梯度进入主干后，最后层MLP输入的领域可读性是否提高及LM代价。现有SAE本来就连续训练，LM loss本来就经过SAE；要改变的是抽样重构分支对主干的detach。

优先审核当前AI建议：同一个随机0点，现有8层串联SAE，控制/干预只差辅助输入梯度开关；两组λ=.1，target与能量分母仍detach；30k/k32、原AdamW与预热后恒定日程不变；首轮不加AuxK，但有活动/重构稳定性门；100步Smoke后各1024→4096步开发预算。包内旁路优先、立即AuxK、新余弦、三种子5B不是既定决策。选择改变这一建议时，说明解决哪个具体竞争解释、增加多少实现/算力成本。

请交付：

1. 一张简短决策卡：问题、两条件唯一差异、目标/梯度、数据/主指标、阶段预算、停止分支与待我批准范围；明确你推荐的一条下一步。
2. 科学问题/归属如需新Anchor/Focus，核实PROJECTS和当前owner；稳定problem_key与科学状态需我确认。先完成具体可审阅的协议草案，勿靠memory创建批准。
3. 给执行AI的冻结参数与验收清单，尤其是当前配置强制λ=1且engine未传系数，不能只改JSON；辅助梯度的上游判定注意共享embedding。
4. 将未确定论文身份、语义对应、AuxK或旁路的后续条件写清楚，不要求先完成整套研究再开小试。

当前允许文档审计与决策草案，不提交GPU任务，不修改活跃训练目录，不替我选最终科学判断。不要反复询问已能由真实配置核实的信息。最终让我批准一张具体卡，而不是一个模糊“继续吗”。完成后按本任务身份记录自己的conversation memory与交接，不覆盖来源memory。

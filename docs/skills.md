# 按任务使用技能

已知文件、常规代码修改、本地测试和简单查询可直接处理。需要专门方法时，选与当前交付物匹配的一行。各技能入口列出其适用参考，读到足够完成当前任务即可。

| 当前任务 | 入口 |
|---|---|
| 为现有问题提出机制、设计最小比较、解释新结果 | [research-progress-core](../.agents/skills/research-progress-core/SKILL.md) |
| 对指定推理、因果链或替代解释作审查 | [research-reasoning-auditor](../.agents/skills/research-reasoning-auditor/SKILL.md) |
| 讨论尚未定型的理论、文献定位或反例 | [scholar-mode](../.agents/skills/scholar-mode/SKILL.md) |
| 解释指定文档、公式或已有结论 | [research-document-explainer](../.agents/skills/research-document-explainer/SKILL.md) |
| 起草或修订正式问题设计 Anchor | [problem-anchor-writer](../.agents/skills/problem-anchor-writer/SKILL.md) |
| 起草 Protocol、写实验 Summary / Detailed | [experiment-card-writer](../.agents/skills/experiment-card-writer/SKILL.md) |
| 查任务、执行已授权的远端运行 | [remote-experiment-workflow](../.agents/skills/remote-experiment-workflow/SKILL.md)。需要 SCO 多节点、设备或存储命令时查 [sco-control-training](../Projects/sco-control/skills/sco-control-training/SKILL.md)。 |
| 写组会稿、研究线叙事或交接材料 | [research-communication](../.agents/skills/research-communication/SKILL.md) |
| 判断某个问题是否已适合导师讨论 | [research-sync-gate](../.agents/skills/research-sync-gate/SKILL.md) |
| 编辑现有研究文字 | [anti-defensive-writing](../.agents/skills/anti-defensive-writing/SKILL.md) |
| 综合已经定案的问题，写最终报告 | [research-final-report](../.agents/skills/research-final-report/SKILL.md) |
| 整理项目、归档或推送系统记录 | [research-mainline](../.agents/skills/research-mainline/SKILL.md) |
| 维护研究图 | [research-graph-sop](../.agents/skills/research-graph-sop/SKILL.md) |
| 保存或恢复会话进度 | [research-memory](../.agents/skills/research-memory/SKILL.md) |

系统技能的源文件在 `.agents/skills/`，Claude 入口链接到同一目录。多节点训练技能源于 `Projects/sco-control/`。修改技能后运行 `python tools/check_skills.py`；安装系统技能到另一工作区时用 `tools/install_skill_routes.py` 生成指向原件的入口。

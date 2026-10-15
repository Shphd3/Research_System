# SAE坐标与语义分派：结构变化来自哪里？

```text
type: meeting_knowledge_update
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
scope: one_problem
problem_key: A15.sae_hierarchical_teacher_construction
```

本文件是研究者明确要求的组会准备视图，不覆盖既有研究Focus/Anchor。核心背景与问题来自2026-09-11研究者本轮说明；具体测量由E21补充证据记录拥有。

**核心问题：** 固定字典与变化字典下看到的结构演化，究竟来自模型表征、SAE编码还是特征分组；这种变化是否成为实际分派依据？

**阅读入口：** [四段式组会报告](../../0911_minimal_followup/meeting_report_cn.md)。先看直觉图，再按真实图A→B→C→D讲解；[90秒练习](../../0911_minimal_followup/meeting_practice_cn.md)。

**知识更新草稿：** 固定几何分组没有平均收紧。刷新SAE改善了重构，但固定h后的替换分析显示，重新分组引起的教师关系变化更大。没有建立跨种子稳定的路由跟随；不能由此宣布SAE无用，也不能宣布语义分派或任务收益已得到证明。

**证据：** [Summary](../../../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E21_dynamic_structural_teacher/supplementary_0911/summary.md)、[Detailed](../../../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E21_dynamic_structural_teacher/supplementary_0911/detailed.md)。

**补查后的认识更新（AI草拟）：** 第256步同图重复基本稳定，记录取样和共现单位更敏感。旧分组的段级统计与当前刷新的词元级统计不同；相似位置不一定是相似内容。不能把大幅教师变化直接当新语义，也不能以“停止动态分组”替代导师的结构演化问题。完整解释见 [白话解析](../../../../Projects/from-attention-to-search/main/research_notes/sae_representation/20260911/0911_minimal_followup/results_explained_cn.md)。

**唯一下一决策（AI建议）：** 在统一观察规则下，能否识别并持续追踪一种具有明确内容或操作含义的结构？先用同操作不同格式、不同操作同格式的独立判断文本对核验；若只支持格式，就收窄到格式/位置结构，不称为语义专家或动态分组必要性。语义粒度和科学判断仍由研究者确认，未改变原Focus或Anchor。

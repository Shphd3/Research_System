# SAE坐标与语义分派：结构变化来自哪里？

```text
type: meeting_knowledge_update
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
scope: one_problem
problem_key: A15.sae_hierarchical_teacher_construction
```

本文件是研究者明确要求的组会准备视图，不覆盖既有研究Focus/Anchor。核心背景与问题来自2026-09-11研究者本轮说明；具体测量由E21补充证据记录拥有。

**核心问题：** 固定字典与变化字典下看到的结构演化，究竟来自模型表征、SAE编码还是特征分组；这种变化是否成为实际分派依据？

**阅读入口：** [四段式组会报告](0911_minimal_followup/meeting_report_cn.md)。先看直觉图，再按真实图A→B→C→D讲解；[90秒练习](0911_minimal_followup/meeting_practice_cn.md)。

**知识更新草稿：** 固定几何分组没有平均收紧。刷新SAE改善了重构，但固定h后的替换分析显示，重新分组引起的教师关系变化更大。没有建立跨种子稳定的路由跟随；不能由此宣布SAE无用，也不能宣布语义分派或任务收益已得到证明。

**证据：** [Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E21_dynamic_structural_teacher/supplementary_0911/summary.md)、[Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E21_dynamic_structural_teacher/supplementary_0911/detailed.md)。

**唯一下一决策（AI建议）：** 刷新特征组是否稳定且有足够语义一致性，值得继续用于监督？完成标准是固定h/编码器的分组重复性及独立文本语义核验；任何一项不支持就停止相应动态分组主张。恢复动作是打开固定探针和例子，先由研究者独立解释一组文本。没有新主模型训练授权或科学状态迁移写入本视图。

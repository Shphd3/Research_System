派生阅读副本；原件位置：`Projects/from-attention-to-search/main/focus/focus_spectral_hierarchical_router_curriculum_cn.md`。
[精确原始文件](../../../../../sources/Projects/from-attention-to-search/main/focus/focus_spectral_hierarchical_router_curriculum_cn.md)；研究修改仍回到原件。

---

# 渐进与全层级谱路由监督

problem_key: `spectral_hierarchical_router_curriculum`
anchor_id: `15_29`
question_state: `USER_ACTIVATED`
design_state: `USER_FIXED_P_F_CONTRACT`
task_state: `PARTIAL_P_FORMAL_SUBMITTED_F_SCHEDULING_BLOCKED`
result_state: `NO_TRAINING_RESULT`
human_result_judgment: `Unknown`
question_closure: `Unknown`

研究者已固定：同一teacher谱树，P逐步启用中后监督、F从开始全部启用，各训50B有效token，其余控制一致。三步为冻结并独立复核上下文树；2卡5090spot核查损失、梯度、数据和真实恢复；通过后按共享8卡上限顺序提交P/F两个8卡5090spot作业。本次完成标准是smoke通过后的真实job ID及配置、资源和终点核实，不需等50B结束。

匹配验证loss的P优势仅是本seed方向性支持；相同或更差是不支持；目标或执行门失败则不足，不改随机标签，不省略smoke。跨seed、天然语义层级、自适应切换不在范围。科研接受Unknown，普通baseline保留。

[Anchor](../problem_anchors/15_spectral_representation_and_functional_routing/15_29_spectral_hierarchical_router_curriculum/15_29_spectral_hierarchical_router_curriculum_anchor_cn.md) · [Protocol](../experiments/A15/15_29_spectral_hierarchical_router_curriculum/R01_progressive_vs_full/protocol_cn.md) · [执行入口](../../../../../UNAVAILABLE.md)。

# 普通 top-2 MoE 对照执行状态

**训练与保存评估已完成。** 实际产出任务为 `pt-0hi8ldns`，运行记录确认使用 `h100-4-reserved`、4 张 H100 80GB。MoE 与 MoE_LB 各两个种子均达到 168 次更新、85,548 个有效答案目标，保存了终点、逐位置结果及恢复状态。

2026-10-22 的保存产物审计通过：冻结代码与配置身份、目标对齐、配对初始化、训练计数、负载均衡计算、终点参数摘要，以及保存的逐位置和逐 feature 指标均一致。此次审计没有重新前向或训练；此前另一项冻结诊断的回放失败继续单独保留。当前没有从这些检查中发现重跑四个模型的理由。[详细结果](detailed_cn.md) · [审计记录](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_rankone_progress/20261022_review/controls_audit.json)

提交历史：`pt-50sa30mo` 尚未启动即按用户要求取消；随后以原配置重提为 `pt-0hi8ldns`。旧任务不列为产物生产者。[产物清单](artifact_manifest.json)保留提交历史与更正证据。执行范围仍为[修订02](execution_amendment_02_cn.md)，没有新增任务或续训。此页报告保存产物的完成状态，不是平台实时状态查询；科学机制判断保留 `Unknown`。

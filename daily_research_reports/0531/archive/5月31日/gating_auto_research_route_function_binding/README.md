# 0531 Gating Auto Research Plan Package

## 结论

当前 Gating 研究下一步不应继续做 broad hierarchy sweep。应转向：

```text
route-function binding + feature decomposition / write-in diagnostic
```

目标是找到一种 routing，使 synthetic NTP 中不同 feature 能被稳定分到不同 expert，并且这个分发在训练中、推理时、跨 seed、跨 checkpoint 都稳定；同时要求该机制未来能迁移到真实训练场景。

## Canonical repo placement

建议把本包内容落到仓库内：

```text
daily_research_reports/0531/gating_auto_research_route_function_binding/
```

主线 anchor 建议路径：

```text
Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/route_function_binding_stable_feature_routing_anchor.md
```

主实验建议路径：

```text
Projects/from-attention-to-search/main/experiments/H0531_route_function_binding_auto_research/
```

root sync anchor 建议路径：

```text
sync/S000_current_specialization/anchors/expert_specialization/route_function_binding_stable_feature_routing_anchor.md
```

## Files

| File | Role |
|---|---|
| `route_function_binding_stable_feature_routing_anchor.md` | 新 anchor 草案：定义父问题、物理先验、数学建模、最小可证伪测试。 |
| `execution_plan.md` | 可执行实验计划：多阶段 auto research，但每阶段有明确决策门。 |
| `agent_runbook.md` | 给 agent 的逐步执行说明、分支规则、停止规则、artifact 要求。 |
| `experiment_matrix.yaml` | 实验矩阵、条件、指标、阈值、输出路径。 |
| `implementation_contract.md` | 数据构造、模型变体、routing/intervention、指标算法的实现契约。 |
| `result_reasoning_ledger_template.md` | agent 每轮实验后填写的 observation / interpretation / boundary / next decision。 |
| `summary_template.md` | `summary.md` 模板。 |
| `detailed_template.md` | `detailed.md` 模板。 |
| `handoff_report_template.md` | 可选汇报报告模板。 |
| `graph_patch_suggestion.md` | 建议图更新，不自动改 graph，需要用户确认。 |
| `codex_task_prompt.md` | 可直接交给 agent / Codex 的长程任务 prompt。 |

## Auto research rule

Agent 不允许直接展开大 sweep。必须按：

```text
anchor -> smoke -> diagnostic -> mechanism intervention -> stability -> summary/detailed -> anchor update
```

每个阶段都要写：

```text
observation / interpretation / claim / speculation / boundary / next decision
```

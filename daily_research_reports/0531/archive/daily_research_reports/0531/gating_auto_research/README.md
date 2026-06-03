# 0531 Gating Auto Research Plan

结论：下一阶段不要继续加 hierarchy 深度，也不要直接进真实语料。当前最小主线是：

```text
先诊断 router logits 被哪个 factor 控制，
再测试能否用 route-function binding / residualized gating / prior gating / nonlinear gating
在 synthetic NTP 中形成稳定、可解释、可复用的 feature-level expert specialization。
```

本文件夹是交给 agent 连续执行半晚上的 auto-research 包。它不是结果记录；它是 pre-run anchor + execution plan + agent runbook + result templates。

## Intended Repo Paths

如果 agent 在 `Research_System` repo 中执行，建议复制到这些位置：

```text
anchor source:
Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/route_function_binding_stable_gating_anchor.md

root sync copy:
sync/S000_current_specialization/anchors/expert_specialization/route_function_binding_stable_gating_anchor.md

experiment folder:
Projects/from-attention-to-search/main/experiments/0531_auto_route_function_binding/

handoff / daily package:
daily_research_reports/0531/gating_auto_research/
```

## Files

```text
anchor/route_function_binding_stable_gating_anchor.md
experiments/0531_auto_route_function_binding/execution_plan.md
experiments/0531_auto_route_function_binding/agent_runbook.md
experiments/0531_auto_route_function_binding/metrics_contract.md
experiments/0531_auto_route_function_binding/experiment_matrix.yaml
experiments/0531_auto_route_function_binding/result_templates/summary_template.md
experiments/0531_auto_route_function_binding/result_templates/detailed_template.md
experiments/0531_auto_route_function_binding/result_templates/anchor_update_template.md
agent/auto_research_prompt.md
graph_update_proposal.md
install_to_repo.sh
manifest.json
```

## One-Sentence Direction

```text
Find a routing/training mechanism whose route decision is controlled by the target-deciding feature and whose selected expert has causal next-token utility for that feature, under controlled synthetic NTP and stress-tested for training/inference stability.
```

## Stop Rule

Agent 不应该把“跑了很多实验”当成进展。每一轮必须回答：

```text
observation -> interpretation -> claim boundary -> next decision
```

如果一个方法提升 CE 但不提升 route-function binding，判为不解决当前问题。

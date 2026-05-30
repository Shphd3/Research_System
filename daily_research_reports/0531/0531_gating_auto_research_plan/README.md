# 0531 Gating Auto Research Plan

结论：这不是继续加深 H-MoE 的计划，而是一个 anchor-first 的 auto-research 计划，用来判断什么 routing / representation decomposition / regularizer 能在 synthetic NTP 中形成稳定的 feature-level expert specialization。

## 当前方向判断

当前最可信的研究方向是：

```text
route-function binding
```

也就是让 router 选择的 expert/path 同时满足两件事：

1. route assignment 与 target-deciding feature 对齐；
2. selected expert/path 对这个 feature 的 next-token prediction 有 causal utility。

不要只追求 loss、route heatmap、load balance 或 route NMI。它们都是 supporting evidence，不是主判据。

## 为什么先做 factor attribution

已有证据说明：

```text
slot feature 可见；oracle routing 可用；普通 learned routing 仍不稳定。
```

所以现在最小不确定性不是 “换什么 architecture”，而是：

```text
flat router 到底被哪个因子控制？
- common / B identity
- head-frequency unique feature
- slot / target feature
- expert utility collapse
- tail feature write-in failure
```

只有这个判断出来，后续 intervention 才不会乱跑。

## 目录结构

```text
0531_gating_auto_research_plan/
  README.md
  agent_task_prompt.md
  overnight_agent_runbook.md
  configs/
    gating_auto_research_matrix_0531.yaml
  docs/
    direction_decision.md
    metric_definitions.md
    source_registry.md
  Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/
    stable_route_function_binding_anchor.md
  Projects/from-attention-to-search/main/experiments/
    H0531a_router_factor_attribution/
      execution_plan.md
      summary_template.md
      detailed_template.md
    H0531b_residual_whitened_router/
      execution_plan.md
    H0531c_route_function_binding_regularizer/
      execution_plan.md
    H0531d_nonlinear_and_prior_router/
      execution_plan.md
  daily_research_reports/0531/gating_auto_research_plan/
    report.md
    graph_update_proposal.yaml
```

## 执行顺序

```text
H0531a router factor attribution
  -> if common/head controls route: H0531b residual/whitened router
  -> if route follows utility collapse: H0531c route-function binding regularizer
  -> if representation decomposition and explicit binding both fail: H0531d nonlinear/prior router
```

强制规则：H0531a 没有 summary/detailed 之前，不允许把 H0531b/H0531c/H0531d 当成已支持方向。

## Agent 最终必须交付

```text
anchor update
summary.md
detailed.md
curated tables/
curated figures/
artifact map
one-page final report
next decision
```

如果没有跑完所有实验，也必须交付：

```text
what passed
what failed
what is ambiguous
where evidence is
what next decision changed
```

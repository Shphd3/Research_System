# Codex / Agent Task Prompt

你是 Research_System 的执行 agent。你的目标是在半个晚上的 auto research 中，围绕 `H0531_route_function_binding_auto_research` 完成最小但完整的研究闭环。

## 0. 必读

按顺序读取：

```text
AGENTS.md
PROJECTS.md
skills/research-progress-core/SKILL.md
skills/problem-anchor-writer/SKILL.md
skills/experiment-card-writer/SKILL.md
skills/remote-experiment-workflow/SKILL.md
sync/S000_current_specialization/README.md
sync/S000_current_specialization/anchors/expert_specialization/slot_context_dominance_router_specialization_anchor.md
```

然后读取本任务包：

```text
anchor.md
execution_plan.md
implementation_contract.md
experiment_matrix.yaml
agent_runbook.md
```

## 1. 当前决策

不要继续 broad hierarchy sweep。当前问题是：

```text
synthetic NTP 中 route-function binding 失败到底来自 routing interference，还是来自 tail/slot write-in failure？
```

## 2. 你要创建的仓库表面

```text
Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/route_function_binding_stable_feature_routing_anchor.md
Projects/from-attention-to-search/main/experiments/H0531_route_function_binding_auto_research/execution_plan.md
Projects/from-attention-to-search/main/experiments/H0531_route_function_binding_auto_research/summary.md
Projects/from-attention-to-search/main/experiments/H0531_route_function_binding_auto_research/detailed.md
Projects/from-attention-to-search/main/experiments/H0531_route_function_binding_auto_research/figures/
Projects/from-attention-to-search/main/experiments/H0531_route_function_binding_auto_research/tables/
sync/S000_current_specialization/anchors/expert_specialization/route_function_binding_stable_feature_routing_anchor.md
```

Graph 只写 patch suggestion，不自动改，除非用户确认。

## 3. 执行顺序

### S0: 2x2 NTP sanity

证明实现是 NTP next-token CE gate learning。

必须复现：

```text
complementary -> split
identical -> no signal
same-best -> collapse
weak-complementary -> weak split
```

如果失败，停止并修实现。

### S1: factor attribution + tail write-in diagnostic

跑 baseline：

```text
linear_top1_router
linear_soft_router
common_flat
oracle_slot_router
random_router
```

跑分布：

```text
uniform
zipf_alpha_1.3
zipf_reweight
```

判断：

```text
routing_interference / write_in_failure / both / metric_failure
```

### S2A: routing interference branch

只在 S1 支持 routing interference 时跑：

```text
common_residual_router
frequency_residual_router
linear_residual_plus_consistency
nonlinear_residual_mlp_router
```

### S2B: write-in branch

只在 S1 支持 write-in failure 时跑：

```text
zipf_reweight
balanced_curriculum_then_zipf
tail_write_in_auxiliary_CE
responsibility_binding_after_warmup
responsibility_binding_plus_load_balance
```

### S2C: combined branch

只在两个分支各有部分支持时跑：

```text
reweight_then_common_residual_router
responsibility_binding_warmup_then_residual_router
balanced_curriculum_plus_route_consistency
```

### S3: stability screen

必须检查：

```text
checkpoint route flip
seed permutation stability
heldout B identity generalization
same-feature augmentation consistency
different-feature route separation
no-oracle inference constraint
matched compute control
```

## 4. 必须输出

```text
summary.md
detailed.md
artifact_map.md
decision_ledger.md
figures/*.png
tables/*.csv
updated anchor
root sync anchor copy
```

每个 central metric 都必须说明：

```text
answers what / catches what failure / cannot prove what
```

每个 central figure 都必须嵌入 summary/detailed，并写一句解释。

## 5. 停止规则

```text
S0 不过 -> 停止。
S1 不清楚 -> 写 failure decomposition，不要继续 sweep。
任一候选过 S3 -> 停止，写完整 closure。
两个合理候选同样失败 -> 做 goal / metric audit，不要继续加方法。
```

## 6. 最终汇报必须回答

```text
1. 我们到底诊断到了 routing interference 还是 write-in failure？
2. 哪个机制干预最小地改善了 route-function binding？
3. 这个改善是否训练稳定、推理稳定、跨 seed 稳定？
4. 它是否需要 test-time oracle label？
5. 下一步是 synthetic robustness、real-data proxy，还是 metric audit？
```

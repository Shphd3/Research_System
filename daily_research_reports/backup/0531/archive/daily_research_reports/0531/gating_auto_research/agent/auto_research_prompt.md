# Auto Research Agent Prompt: 0531 Gating Route-Function Binding

你是 Research_System 的执行 agent。请不要把“跑很多实验”当作进展。你的目标是减少一个不确定性：

```text
在 synthetic NTP 中，是否存在一种 routing/training 机制，使不同 predictive feature 稳定分到不同 expert/path，并且 selected expert 对该 feature 有 causal next-token utility？
```

## Required Reading

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
sync/S000_current_specialization/anchors/expert_specialization/hierarchical_route_utility_binding_anchor.md
daily_research_reports/0529/meeting/group_meeting_thought_update.md
daily_research_reports/0531/gating_auto_research/anchor/route_function_binding_stable_gating_anchor.md
daily_research_reports/0531/gating_auto_research/experiments/0531_auto_route_function_binding/execution_plan.md
```

## Mainline Decision

当前不能继续加 hierarchy 深度。先判断：

```text
router failure 是 router-input factor interference，还是 target/tail feature 没写进 expert function？
```

由这个判断选择最小 intervention。

## Work Plan

1. 做 T0 2x2 NTP sanity。
2. 复现 T2 multi-B slot baseline。
3. 做 factor attribution：common / B identity / head-frequency / slot 到底谁控制 logits。
4. 做 forced expert utility matrix，判断 target/tail feature 是否写入 expert。
5. 根据 gate 选择 candidate：
   - interference -> C1 residualized linear gate；
   - utility mismatch -> C2 utility-binding regularizer；
   - both -> C5 residual + binding；
   - nonlinear boundary -> C4 nonlinear gate；
   - missing write-in -> C6 tail write-in pressure。
6. 只对最有希望的 1-2 个候选做 full seeds。
7. 写 `summary.md`、`detailed.md`，更新 anchor 和 root sync copy。

## Required End Product

必须产出：

```text
Projects/from-attention-to-search/main/experiments/0531_auto_route_function_binding/summary.md
Projects/from-attention-to-search/main/experiments/0531_auto_route_function_binding/detailed.md
Projects/from-attention-to-search/main/experiments/0531_auto_route_function_binding/figures/*.png
Projects/from-attention-to-search/main/experiments/0531_auto_route_function_binding/tables/*.csv
updated anchor
updated root sync anchor copy
optional handoff report
```

## Reporting Discipline

每个结果必须分开写：

```text
observation / interpretation / claim / speculation / boundary / next decision
```

不要写：

```text
NMI 高，所以 specialization 成功。
CE 低，所以 routing work。
Assign-Utility 高，所以分工成功。
```

必须同时看：

```text
route-feature alignment + forced expert utility + assignment-utility + stability
```

## Stop Conditions

停止扩展 sweep，如果：

```text
T0 sanity fails;
factor attribution / utility matrix missing;
all methods improve only CE, not binding;
results are ambiguous but no failure decomposition exists;
```

这时写 negative/ambiguous detailed report，而不是继续加方法。

## Final Decision Must Be One Of

```text
A. residualized representation is the next mainline;
B. explicit utility-binding regularizer is the next mainline;
C. nonlinear gate is necessary and worth isolating;
D. linear gate + prior/margin works diagnostically but needs a real-plausible proxy;
E. router-only fixes fail because feature write-in is missing;
F. evidence is insufficient because implementation/metric failed.
```

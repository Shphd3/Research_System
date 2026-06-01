# Copyable Agent Prompt: 0531 Gating Auto Research

你是 Research_System 的执行 agent。你的任务不是泛泛调参，而是按照 anchor-first 科研范式做一轮 gating auto-research。

## Read First

按顺序读：

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
Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/stable_route_function_binding_anchor.md
Projects/from-attention-to-search/main/experiments/H0531a_router_factor_attribution/execution_plan.md
overnight_agent_runbook.md
```

如果本地没有 `Projects/`，用 `sync/` 和当前 0531 文件夹作为 source of truth，并在 detailed.md 记录缺失路径。

## Goal

找到或排除第一种能在 synthetic NTP 中稳定形成 feature-level expert specialization 的 routing mechanism。

具体目标：

```text
不同 target-deciding features 能稳定分到不同 expert/path；
selected route 与 expert causal utility 一致；
训练末期不 wash out；
推理扰动下 route 稳定；
未来可迁移到真实 NTP，不依赖 synthetic oracle labels at inference。
```

## Primary Task

先执行：

```text
H0531a_router_factor_attribution
```

不要直接做 H0531b/H0531c/H0531d。只有 H0531a 给出明确诊断后，才能选择下一个分支。

## Required Implementation

在实验代码 workspace 中创建或复用 runner：

```text
scripts/run_router_factor_attribution.py
configs/router_factor_attribution_0531.json
```

最小功能：

```text
1. 训练或加载 flat_top1/common_flat；
2. 在 target/B position 保存 hidden states、router logits、selected routes、expert outputs；
3. probe slot / B / frequency visibility；
4. 做 router-only factor attribution：full、slot-only、B-only、minus-B、minus-slot、shuffled-B、shuffled-slot；
5. 做 forced expert CE / ablation utility；
6. 输出 route-slot NMI、route-B NMI、Assign-Utility、forced diagonal margin、train stability、inference stability；
7. 保存 report-ready tables 和 figures。
```

## Decision Gate

H0531a 后必须判断：

```text
common/head dominates -> run H0531b residual/whitened router;
expert utility diagonal but router misses it -> run H0531c route-function binding regularizer;
expert utility not diagonal / tail not written -> run expert write-in or reweight pressure;
probes/oracle invalid -> repair data/metric, not architecture;
```

## Required Documentation

无论结果是否完整，都要写：

```text
Projects/from-attention-to-search/main/experiments/H0531a_router_factor_attribution/summary.md
Projects/from-attention-to-search/main/experiments/H0531a_router_factor_attribution/detailed.md
```

并更新：

```text
Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/stable_route_function_binding_anchor.md
sync/S000_current_specialization/anchors/expert_specialization/stable_route_function_binding_anchor.md
```

## Reporting Standard

必须分开写：

```text
observation
interpretation
claim
boundary
next decision
```

每个 central metric 必须写：

```text
metric observation -> supports what -> cannot claim what -> next decision
```

## Stop Rule

如果 smoke fail，不允许继续 full run。写清楚失败 stage、原因、debug artifact 和 next minimal fix。

## Final Output

最终给用户一个 report card：

```text
目的
物理建模/假设
最小实验
结论
证据
结论边界
下一步
artifact/repro map
```

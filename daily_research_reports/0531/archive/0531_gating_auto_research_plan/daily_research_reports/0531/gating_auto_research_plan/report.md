# Handoff Report: 0531 Gating Auto Research Plan

Anchor:

```text
Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/stable_route_function_binding_anchor.md
```

Summary:

```text
Pre-run plan. Result summary will be created after H0531a.
```

Detailed:

```text
Pre-run plan. Detailed result will be created after H0531a.
```

## 0. Oral Report Card

目的：

```text
找到一种 synthetic NTP 中稳定的 feature-level routing 机制：不同 target-deciding features 分到不同 expert/path，且 selected path 对 next-token prediction 有 causal utility。
```

物理建模 / 假设：

```text
hidden state = common/B identity + slot/target feature + frequency/head component + noise。普通 flat router 可能绑定到 common/head 或 utility collapse，而不是 target-deciding feature。
```

最小实验：

```text
先做 H0531a router-factor attribution，判断 route logits 和 utility-best expert 到底由 common、head-frequency、B identity、slot/target feature、还是 expert write-in failure 控制。
```

当前结论：

```text
这是 pre-run plan。已有证据只支持 route-function mismatch 是当前主问题，不支持继续直接加 hierarchy depth。
```

证据：

```text
slot visible + oracle works 但 learned routing 不稳定；common_flat 有帮助但 hierarchy alone 不稳定；Zipf linear FFN 支持 head write-in / tail write-in failure。
```

结论边界：

```text
本计划只覆盖 synthetic NTP gating mechanism，不证明真实语料或 deployment。
```

下一步：

```text
执行 H0531a。如果 common/head dominance 成立，进 H0531b；如果 utility mismatch 成立，进 H0531c；如果 write-in failure 成立，先进 expert write-in/reweight。
```

## 1. What Will Be Tested

```text
H0531a: Which factor controls learned routing, and does the target-deciding feature have expert causal utility?
```

The experiment separates:

```text
route input control
expert utility formation
metric false positives
training/inference stability
```

## 2. Evidence Location

Pre-run artifacts:

```text
overnight_agent_runbook.md
agent_task_prompt.md
configs/gating_auto_research_matrix_0531.yaml
Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/stable_route_function_binding_anchor.md
Projects/from-attention-to-search/main/experiments/H0531a_router_factor_attribution/execution_plan.md
```

Post-run artifacts should be:

```text
Projects/from-attention-to-search/main/experiments/H0531a_router_factor_attribution/summary.md
Projects/from-attention-to-search/main/experiments/H0531a_router_factor_attribution/detailed.md
Projects/from-attention-to-search/main/experiments/H0531a_router_factor_attribution/tables/
Projects/from-attention-to-search/main/experiments/H0531a_router_factor_attribution/figures/
```

## 3. What Counts As Passing

```text
A candidate direction is selected by evidence, not preference.
```

Passing H0531a means:

```text
factor probes valid;
router attribution interpretable;
forced expert utility valid;
decision table identifies dominant failure mode;
next intervention is justified.
```

## 4. What Would Fail Or Stay Ambiguous

Failure:

```text
oracle slot router fails;
forced expert loss invalid;
model does not learn target;
factor edits not interpretable;
only aggregate metrics are reported.
```

Ambiguous:

```text
different seeds point to different dominant factors;
route-slot NMI and utility heatmap disagree;
common/head attribution depends entirely on estimator choice.
```

## 5. Interpretation

The plan treats gating as a causal binding problem, not a heatmap problem:

```text
routing is successful only if the selected path is both feature-aligned and utility-useful.
```

## 6. Claim Boundary

Can claim after H0531a only if evidence supports:

```text
which factor controls current routing;
which intervention should be run next.
```

Cannot claim after H0531a alone:

```text
new routing method works;
real training transfer;
H-MoE solved the problem;
load balance is enough.
```

## 7. Next Decision

```text
H0531a result decides H0531b vs H0531c vs write-in pressure vs metric/data repair.
```

## 8. Artifact / Repro Map

code workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
```

runner:

```text
scripts/run_router_factor_attribution.py
```

config:

```text
configs/router_factor_attribution_0531.json
```

key code files:

```text
existing synthetic data/model code from hierarchical_route_utility_binding runner
new attribution runner
new utility forcing evaluator
```

data / manifest:

```text
sample_id, slot_id, B_id, frequency_rank, target_token, target_position, condition, seed
```

result dir:

```text
results/H0531a_router_factor_attribution/<run_name>
```

figure dir:

```text
Projects/from-attention-to-search/main/experiments/H0531a_router_factor_attribution/figures/
```

key files:

```text
probe_scores.csv
router_attribution.csv
forced_expert_loss.csv
decision_metrics_by_seed.csv
```

checkpoints / logs:

```text
logs/H0531a_router_factor_attribution/<run_name>.log
```

repro command:

```bash
python scripts/run_router_factor_attribution.py --config configs/router_factor_attribution_0531.json --run_name H0531a_router_factor_attribution_full
```

job id:

```text
fill after submission
```

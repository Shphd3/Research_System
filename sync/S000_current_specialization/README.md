# S000 Current Specialization

This root sync entry summarizes the active feature-level expert-specialization
research line. It is a reading map, not an anchor mirror.

## Main Question

```text
Can top-1 MoE gating form a stable, interpretable, and useful feature-level
expert partition?
```

Current narrower decision:

```text
Can a step-0 real-DCLM proxy partition be preserved through the step-5/10
training window without unacceptable language-model loss regression?
```

## Adjudication Ladder

This line moves from a fuzzy vision to testable states:

```text
fuzzy vision -> phenomenon -> physical prior -> mathematical model
-> falsifiable hypothesis -> minimal experiment -> updated understanding
```

Current ladder:

| Level | Question | Main metric | Cannot claim |
|---|---|---|---|
| 0. Failure | Why ordinary top-1 collapses or merges. | step-0 NMI, max load, common margin | A method. |
| 1. Proxy discovery | Whether a route-relevant proxy exists. | cluster stability, proxy NMI, nuisance guards | Semantic experts. |
| 2. Initialization | Whether proxy centers can become gate rows. | step-0 `proxy_route_NMI`, load | Training success. |
| 3. Preservation | Whether the partition survives early training. | `proxy_route_NMI@step5/10` plus LM loss | Utility. |
| 4. Utility | Whether the preserved partition reduces interference. | rare loss, route-function binding, causal ablation | Specialization from load/NMI alone. |
| 5. Scaling | Whether many experts increase activated capacity. | per-expert effective rank, routing stability, utility per activated FLOP | Scaling from active-expert count alone. |

Current position:

```text
active bottleneck: 3. Preservation
```

Levels 0-2 have enough evidence to motivate the preservation test. Level 4 is
supported only in controlled D07 evidence, not real-DCLM utility. Level 5 is
parked.

## Research-Line Map

| File | Role |
|---|---|
| `research_lines/00_overall_current_line_cn.md` | overall 05/06/07 logic chain and strict boundary |
| `research_lines/05_failure_mechanism_line_cn.md` | why ordinary top-1 routing fails |
| `research_lines/06_proxy_preservation_line_cn.md` | route-relevant proxy discovery, initialization, and preservation |
| `research_lines/07_interference_value_line_cn.md` | when a partition has functional value |

## One-Line State

A05 shows that ordinary top-1 routing can fail through common components,
wrong geometric objects, and early-training feedback. A06 shows that
route-position feature geometry can be found and routed, but all-position
clustering is the wrong population and ordinary real-DCLM training can erase a
step-0 proxy partition. A07 shows why value must be judged through
common/rare interference or expert utility, but current neural evidence is not
enough to claim real functional MoE specialization.

## Source Links

Project-local synthesis:

```text
Projects/from-attention-to-search/main/problem_anchors/05_06_07_initialization_collapse_to_interference_chain_cn.md
```

Key source summaries:

```text
Projects/from-attention-to-search/main/experiments/A05/A05_04_03_real_text_common_logit_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_10_real_dclm_proxy_feature_operationalization/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_11_real_dclm_proxy_center_router_initialization/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_all_position_route_relevant_feature_discovery/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_01_common_rare_conflict_metric_audit/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_02_common_controlled_rare_interference/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_03_route_function_binding/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_04_common_rare_gradient_conflict_splitting/summary.md
```

## Boundary

Controlled synthetic results can validate mechanism, metric surfaces, and
known-feature routing under controlled labels. They do not prove natural
language semantics or real checkpoint behavior.

Real-DCLM proxy results can show stable hidden-state proxy clusters, step-0
linear routability, and early-training overwrite. They do not by themselves
prove semantic expert identity or causal expert utility.

## Next Decision

Write one real-DCLM preservation / anti-feedback protocol. The primary metric
is `proxy_route_NMI` at step 5/10 under fixed step-0 proxy labels, with LM loss
as the guard.

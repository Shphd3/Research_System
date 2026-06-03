# Agent Runbook: Half-Night Auto Research For Stable Feature Routing

## 0. Operating rule

Do not optimize for many runs. Optimize for closing one uncertainty at a time.

Required loop:

```text
hypothesis -> operational definition -> minimal test -> metric + visual evidence -> failure analysis -> refined hypothesis
```

Every result must separate:

```text
observation / interpretation / claim / speculation / boundary / next decision
```

## 1. Preflight

Read in this order:

```text
AGENTS.md
PROJECTS.md
skills/research-progress-core/SKILL.md
skills/problem-anchor-writer/SKILL.md
skills/experiment-card-writer/SKILL.md
skills/remote-experiment-workflow/SKILL.md
sync/S000_current_specialization/README.md
sync/S000_current_specialization/anchors/expert_specialization/slot_context_dominance_router_specialization_anchor.md
this package: route_function_binding_stable_feature_routing_anchor.md, execution_plan.md, implementation_contract.md
```

Then write a short preflight note:

```text
active project:
active anchor:
new proposed anchor:
experiment folder:
code workspace:
available runner:
missing implementation pieces:
```

If `Projects/from-attention-to-search/graph.yaml` is unavailable, use root sync and this package; do not block.

## 2. Create / update repo surfaces

Suggested paths:

```text
Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/route_function_binding_stable_feature_routing_anchor.md
Projects/from-attention-to-search/main/experiments/H0531_route_function_binding_auto_research/execution_plan.md
Projects/from-attention-to-search/main/experiments/H0531_route_function_binding_auto_research/summary.md
Projects/from-attention-to-search/main/experiments/H0531_route_function_binding_auto_research/detailed.md
Projects/from-attention-to-search/main/experiments/H0531_route_function_binding_auto_research/figures/
Projects/from-attention-to-search/main/experiments/H0531_route_function_binding_auto_research/tables/
sync/S000_current_specialization/anchors/expert_specialization/route_function_binding_stable_feature_routing_anchor.md
```

Do not edit `graph.yaml` unless user confirms the proposed graph patch.

## 3. Stage S0: 2x2 NTP sanity

Goal:

```text
Prove the runner is doing NTP-style next-token CE gate learning, not fixed-gate proxy or random clustering.
```

Run:

```text
complementary / identical / same_best / weak_complementary
```

Required table:

| Case | Final CE | P(correct route) | Margin | Decision |
|---|---:|---:|---:|---|

Decision:

```text
If analytic pattern fails: stop and fix implementation.
If analytic pattern passes: proceed to S1.
```

## 4. Stage S1: diagnose failure type

Run baseline models:

```text
linear_top1_router
linear_soft_router
common_flat
oracle_slot_router
random_router
```

Regimes:

```text
uniform
zipf_alpha_1.3
zipf_reweight
```

Seeds:

```text
smoke: 1 seed
first full: 5 seeds
expand to 10 seeds only if result is near threshold
```

Produce:

```text
factor_attribution_r2.csv
selected_route_factor_nmi.csv
factor_removal_flip_rate.csv
forced_expert_ce_matrix.csv
ablation_utility_matrix.csv
head_mid_tail_utility_gap.csv
```

Branch decision:

```text
routing_interference if:
  slot/tail utility-best expert exists, but router logits / selected route are dominated by common/head/B identity.

write_in_failure if:
  slot/tail utility-best expert is weak or absent, especially under Zipf, and reweight improves it.

both if:
  utility weak under Zipf and route still reads nuisance after utility appears.

metric_failure if:
  target acc high but utility metrics conflict repeatedly.
```

## 5. Stage S2A: routing-interference branch

Run only if S1 supports routing interference.

Variants:

```text
common_residual_router
frequency_residual_router
linear_residual_plus_consistency
nonlinear_residual_mlp_router
```

Controls:

```text
raw_h_mlp_router
random_subspace_removed_router
slot_subspace_removed_negative_control
matched_compute_linear_router
```

Pass:

```text
route-feature NMI improves;
assignment-utility improves;
forced utility already exists and selected route now matches it;
checkpoint and heldout B stability improve.
```

Fail:

```text
only target CE improves;
MLP improves only by B identity shortcut;
residual method destroys utility or target accuracy;
route alignment improves but utility agreement does not.
```

## 6. Stage S2B: write-in branch

Run only if S1 supports write-in failure.

Variants:

```text
zipf_reweight
balanced_curriculum_then_zipf
tail_write_in_auxiliary_CE
responsibility_binding_after_warmup
responsibility_binding_plus_load_balance
```

Pass:

```text
tail/slot forced utility diagonal appears;
tail/head utility gap shrinks;
route-function binding improves after utility appears;
stability does not degrade.
```

Fail:

```text
reweight improves CE but not utility diagonal;
aux objective creates artificial expert labels but fails heldout B;
responsibility binding reinforces collapse.
```

## 7. Stage S2C: combined branch

Run only if both S2A and S2B partially pass.

Minimal combined candidates:

```text
reweight_then_common_residual_router
responsibility_binding_warmup_then_residual_router
balanced_curriculum_plus_route_consistency
```

Stop after first candidate passes S3 stability. Do not expand into more combinations before closure.

## 8. Stage S3: stability and transfer screen

Required checks:

```text
checkpoint route flip after burn-in;
seed permutation stability;
heldout B identity route NMI;
same-feature augmentation consistency;
different-feature route separation;
no-oracle inference constraint;
matched compute and matched target accuracy.
```

Pass thresholds:

```text
checkpoint flip <= 0.05;
seed stability >= 0.80;
heldout B route NMI >= 0.70;
same-feature consistency >= 0.90;
different-feature separation >= 0.80.
```

## 9. Closure procedure

After each decisive stage:

1. Write / update `summary.md`.
2. Write / update `detailed.md`.
3. Update anchor `Current Evidence`, `Claim Boundary`, `Next Decision`.
4. Copy anchor to root sync path and verify identical.
5. Write optional `report.md` only if needed for meeting or web-side handoff.
6. Write `agent_logs/decision_ledger.md` with decisions and why branches were pursued or parked.

## 10. Mainline impact gate for new ideas

Before trying any unplanned idea, write:

```text
Mainline impact:
- affects hypothesis? yes/no/unclear
- affects claim boundary? yes/no/unclear
- affects next decision? yes/no/unclear
- recommendation: pursue / park / ignore
```

Default:

```text
park architecture ideas until S1 diagnoses mechanism.
park real-corpus transfer until S3 passes synthetic stability.
ignore metrics that do not distinguish route-function binding.
```

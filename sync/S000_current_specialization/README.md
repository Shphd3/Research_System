# S000 Current Specialization

This root sync entry summarizes the active feature-level expert-specialization
research line. It is both a reading map and an explicit anchor-copy sync
surface.

The project-local source of truth remains:

```text
Projects/from-attention-to-search/main/problem_anchors/
```

The copied anchor snapshot lives here:

```text
anchors/
```

Use `anchor_index.md` to inspect the copied anchor groups. The mirror is
updated only when the user explicitly asks to sync S000.

## Main Question

```text
Can top-1 MoE gating form a stable, interpretable, and useful feature-level
expert partition?
```

Current narrower decision:

```text
Can a nested-learning-inspired common/rare routing audit define a stable common
operator and show that common-subtracted routing improves rare-feature margins
without unacceptable language-model loss regression?
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
| `anchor_index.md` | copied-anchor inventory and line grouping |
| `anchors/` | copied project-local anchor tree from `from-attention-to-search` |
| `stories/` | copied project-local line stories when explicitly synced |
| `research_lines/00_overall_current_line_cn.md` | overall 05/06/07 logic chain and strict boundary |
| `research_lines/05_failure_mechanism_line_cn.md` | why ordinary top-1 routing fails |
| `research_lines/06_proxy_preservation_line_cn.md` | route-relevant proxy discovery, initialization, and preservation |
| `research_lines/07_interference_value_line_cn.md` | when a partition has functional value |

Supporting objective line:

```text
anchors/11_long_horizon_mtp_objective/
stories/11_long_horizon_mtp_objective/story_cn.md
```

This line is not the active MoE gating mainline. It asks whether multi-token
prediction can directly supervise the current hidden state to retain a
long-horizon variable. Current A11 evidence supports a controlled
representation guarantee and a controlled efficiency-mechanism direction.
A11_06 supports the first-order hidden readout-margin mechanism. A11_07 shows
that direct decision-prefix horizon-3 supervision gives stronger native H3
prediction and `M_Z_ref` under no-leakage all-position training, while
all-position indirect transfer can still make `Z` probe-readable. A11_08
supports the general-K vector-sum mechanism. A11_08b shows the primary
hidden-velocity mechanism is not only a step-0 artifact under frozen output
heads. A11_09 supports the next-K inclusion law: K matters when it newly
covers an informative future horizon, and the increment depends on centered
output-direction alignment. A11_10 supports the all-position native/probe
split: direct H3 conditions reach native H3=1.0 and large `M_Z_ref`, while
K2 and masked K3 can keep nontrivial `Q` but native H3 remains 0 and
`M_Z_ref` stays near zero. Boundary: `Q` alone is not direct-supervision
evidence; larger K is not automatically better; MoE routing transfer remains
open.

## One-Line State

A05 shows that ordinary top-1 routing can fail through common components,
wrong geometric objects, and early-training feedback. A06 shows that
route-position feature geometry can be found and routed, all-position
clustering is the wrong population, and controlled center initialization is
preserved by positive margin buffer rather than active center tracking. A06_21
decomposes this buffer; A06_23 sharpens it into a finite-threshold claim:
$q\ge0.05$ preserves, while $q=0.02$ starts correct and still crosses routing
boundaries during training. Ordinary real-DCLM training can erase a step-0
proxy partition. A06_22 reproduces that collapse, but common/residual
dominance flips across common projectors, so common is a candidate mechanism,
not an established root cause. A07 shows why value must be judged through
common/rare interference or expert utility, but current neural evidence is
not enough to claim real functional MoE specialization.

A11 is a supporting objective line: in controlled long-horizon MTP tasks, when
K covers the first informative future token, low loss at that horizon forces
the current hidden state to contain the delayed variable. A11_06 / A11_07 add
controlled efficiency evidence: the covering target creates positive
hidden-state readout-margin velocity and stronger native direct prediction.
A11_08 / A11_08b / A11_09 further show that general-K gains are governed by
which informative horizons are covered and whether their centered readout
directions align, not by K size alone. A11_10 adds that all-position recovery
must separate probe-readable `Q` from native direct readout. This may inform a
future route-relevant hidden-state objective, but it does not prove gating
preservation or expert utility.

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
Projects/from-attention-to-search/main/experiments/A06/A06_08_label_free_feature_discovery_initialization/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_all_position_route_relevant_feature_discovery/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_02_router_center_tracking_preservation/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_03_feature_drift_margin_boundary/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_04_margin_crossing_causal_stress/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_05_margin_basin_robust_initialization/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_21_margin_budget_preservation_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_22_router_common_residual_trajectory_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_23_top1_lockin_margin_threshold/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_01_common_rare_conflict_metric_audit/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_02_common_controlled_rare_interference/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_03_route_function_binding/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_04_common_rare_gradient_conflict_splitting/summary.md
Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/README.md
Projects/from-attention-to-search/main/stories/11_long_horizon_mtp_objective/story_cn.md
Projects/from-attention-to-search/main/experiments/A11/A11_04_03_k3_efficiency_advantage/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_04_03_k3_efficiency_advantage/meeting_brief.md
Projects/from-attention-to-search/main/experiments/A11/A11_05_semantic_efficiency_bridge/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_06_readout_effective_margin_efficiency/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_07_no_leakage_all_position_efficiency/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_08_general_k_readout_margin_dynamics/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_08b_output_geometry_dynamics_audit/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_09_next_k_inclusion_law/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_10_all_position_indirect_transfer_dynamics/summary.md
daily_research_reports/0629/docs/nested_prediction_spectral_anisotropy_causal_rewrite_v4.md
daily_research_reports/0701/meeting_brief.md
```

## Boundary

Controlled synthetic results can validate mechanism, metric surfaces, and
known-feature routing under controlled labels. They do not prove natural
language semantics or real checkpoint behavior.

Real-DCLM proxy results can show stable hidden-state proxy clusters, step-0
linear routability, and early-training overwrite. They do not by themselves
prove semantic expert identity or causal expert utility.

## Next Decision

Define a physically grounded common operator $P_C$ and run a bounded
common-subtracted routing audit. Compare routing on raw $h$ with routing on
$(I-P_C)h$. The primary metric is rare-feature margin; guards are matched
preserve fraction, `proxy_route_NMI`, sign-flip rate, LM loss, max load, active
experts, and projector robustness. If common dominance still flips by
projector as in A06_22, park method claims. If common subtraction improves
rare-feature margins without hurting LM loss, then write the next gating
mechanism anchor.

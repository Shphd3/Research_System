# Projects

This file is the current project-state registry for `Research_System`.
Read it after `AGENTS.md`.

`AGENTS.md` defines general operating rules. This file defines the active
research line, active branch, current evidence boundary, and next decision.

## Reading Rule

For project-specific work:

1. Identify the active project here.
2. Read the relevant graph under `Projects/graphs/`.
3. Read only the linked project-local anchor, experiment `summary.md`,
   `detailed.md`, sync note, meeting note, or paper note needed for the
   current question.

Do not scan whole project repositories by default.

## Active Research Line

Primary research theme:

```text
feature-level expert specialization in top-1 MoE gating
```

Current working project:

```text
Projects/from-attention-to-search/
Projects/from-attention-to-search/XingyuD/
```

Reference project:

```text
Projects/kv_cache/
Projects/kv_cache/main_specialization/specialization_overview.md
```

`Projects/kv_cache` is read-only unless the user explicitly asks to edit it.
Only the `xyDeng` branch is under our management; do not push `main`.

Current graph hub:

```text
Projects/graphs/expert_specialization.graph.yaml
Projects/graphs/kv_cache_retrieval.graph.yaml
Projects/graphs/specialization_papers.graph.yaml
```

Graph refresh status:

```text
The project anchors and this registry contain the 2026-07-14 A06
consolidation, A11/A12 split, and A11/A12 parent/subanchor cleanup. The Sidecar
specialization graph has not yet received that separately approved refresh.
For those current decisions, use the linked project-local anchor registries
rather than an older graph-node summary.
```

For graph display, use Sidecar with workspace root:

```text
/data/250010109/Research_System
```

## Research Vision And Adjudication Ladder

The whole specialization project should be read as a staged adjudication
ladder, not as a single method claim. Each level answers one narrower
question and earns only the claim that its metric can support.

| Level | Decision question | Primary metric | Cannot claim |
|---|---|---|---|
| 0. Failure | Why ordinary top-1 routing collapses or merges under apparently uniform features. | step-0 NMI, max load, common margin | A working method. |
| 1. Proxy discovery | Whether a route-relevant proxy exists. | cluster stability, proxy NMI, nuisance guards | Semantic experts. |
| 2. Initialization | Whether the proxy can be converted into gate rows. | step-0 `proxy_route_NMI`, load | Training success. |
| 3. Preservation | Whether the partition survives early training. | `proxy_route_NMI@step5/10` plus LM loss | Expert utility. |
| 4. Utility | Whether a preserved partition reduces interference or has causal expert value. | rare loss, route-function binding, causal ablation | Specialization from load/NMI alone. |
| 5. Scaling | Whether many experts increase activated capacity. | per-expert effective rank, routing stability, utility per activated FLOP | Scaling from active-expert count alone. |

`NMI` is normalized mutual information, used here as a route-label agreement
metric. It can show alignment or collapse, but it does not prove functional
expert value by itself.

Current position in this ladder:

```text
active bottleneck: real-workload gate between 4. Utility and 5. Scaling
```

Practical reading:

```text
Level 0 has failure-mechanism evidence.
Level 1 has controlled and real-DCLM proxy evidence, with semantic boundaries.
Level 2 has real-DCLM step-0 proxy-center router evidence.
Level 3 has controlled mechanism evidence: finite low-tail margin is the local
preservation state, and its motion depends on utility, signed background
pressure, representation motion, router motion, and transmitted update scale.
Level 4 has controlled neural evidence: correct conditional exposure creates
held-out specialist utility, selected-only weighted top-1 can fail to discover
an unselected specialist, and one challenger plus a lower-tail utility
certificate repairs that failure under frozen four-expert assumptions.
Level 4 has not passed on a real pretrained-LLM workload. Level 5 remains
parked until stable real expert-utility headroom and learned Router capture are
both established.
```

Do not promote a higher-level claim when only a lower-level metric passed.
For example, balanced load or high route NMI can support non-collapse or
alignment, but cannot by itself support utility or scaling.

## Current Question

Current decision question:

```text
Does unfiltered repository-level code completion contain positive,
cross-split-stable held-out oracle routing headroom after token-identity,
local-only, load-matched, and split-overfitting controls?
```

This question is parent anchor `A06_04`. It is downstream of completed
`A06_03_01`--`A06_03_04`: expert-function formation, selected-path blindness,
bounded challenger discovery, and the lower-tail phase switch. No additional
Router method is justified until this workload premise passes.

## Current Route

The current route is:

```text
05 failure mechanism
-> 06 route-relevant geometry and finite-margin preservation
-> 06 controlled expert utility and partial-feedback correction
-> 06 real-workload expert-utility headroom gate
-> 07 functional interference value only after the gate passes
```

Supporting objective lines:

```text
11 informative-future branch mechanism
-> 12 structured compositional MTP workload
```

Primary A06 story:

```text
Projects/from-attention-to-search/main/stories/06_geometry_proxy_preservation/01_functional_specialization_and_utility_routing.md
Projects/from-attention-to-search/main/stories/06_geometry_proxy_preservation/01_functional_specialization_and_utility_routing_cn.md
```

Current A06 anchor registry and active anchor:

```text
Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/research_map.md
Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor.md
Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor_cn.md
```

A06 organization rule:

```text
one complete parent anchor per major decision
-> local controls and method falsifiers under parent/subanchors/
-> experiments inherit parent + subanchor + run identifiers
```

Current A06 experiment registry:

```text
Projects/from-attention-to-search/main/experiments/A06/README.md
```

Supporting A11 story:

```text
Projects/from-attention-to-search/main/stories/11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary.md
Projects/from-attention-to-search/main/stories/11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary_cn.md
```

Current A11 parent-anchor registry:

```text
Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/README.md
```

Supporting A12 story:

```text
Projects/from-attention-to-search/main/stories/12_structured_compositional_mtp_workload/01_structured_composition_workload_and_standard_head_use.md
Projects/from-attention-to-search/main/stories/12_structured_compositional_mtp_workload/01_structured_composition_workload_and_standard_head_use_cn.md
```

Current A12 parent-anchor registry and active parent:

```text
Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/README.md
Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_03_standard_head_causal_use/12_03_standard_head_causal_use_anchor.md
```

Role:

```text
A11 identifies the objective-level NTP/MTP difference on a short matched
branch. A12 tests whether that earlier signal becomes functionally useful on a
structured composition workload. Neither line replaces the MoE preservation
mainline.
```

Current A11 parent-anchor chain:

```text
1. Informative-horizon supervision: supported in controlled hidden-state
   dynamics; information inclusion and output-direction alignment, not K alone,
   determine the direct signal.
2. Hidden-to-parameter transmission: conditionally supported in controlled
   Transformer settings; all-position background is signed.
3. Cross-position standard-head boundary: current-state formation is not
   sufficient for later standard-head behavior; the proxy bridge branch is
   closed.
```

Current A11 boundary:

```text
A11 establishes an earlier direct first-order signal from informative future
targets, conditional shared-parameter reachability, a cross-position
sufficiency failure. It does not establish long-range composition, tree
reasoning, neural scale effects, curriculum benefit, real-workload transfer,
or Router/MoE value. A11 is a stable baseline with no active run.
```

Current A12 parent-anchor chain:

```text
1. Structured workload and capability gate: a computation-tree model defines
   intermediate-state composition. The current two-table task is only its
   depth-two serial base case. Its joint-evidence construction is valid, but
   the tested from-scratch small Transformers remain near chance.
2. Interference, capacity, and curriculum boundary: insufficient
   representation rank is a sufficient tradeoff mechanism in the oracle
   linear model; dose-matched curriculum cannot create missing rank. This is
   not a neural scale law.
3. Intermediate-state causal use: active design. First establish one shared
   task-capable checkpoint, then compare NTP and informative Next-2 through
   the same standard head and intervene on the intermediate state B rather
   than only the final-answer code Y.
```

Current A12 boundary:

```text
A12 establishes a valid depth-two joint-evidence workload, a failed current
from-scratch learner branch, and a controlled linear missing-rank mechanism.
It does not establish neural causal use, MTP superiority, a general branching
tree result, a model-scale law, curriculum benefit in a capacity-sufficient
regime, real-workload transfer, or Router/MoE value.
```

Exactly one next decision inside the supporting A11/A12 route:

```text
Review the revised A12 causal-use protocol and run only its shared capability gate.
If the gate fails, do not compare NTP and Next-2 and do not interpret
representation patches.
```

Sharper logic:

```text
ordinary top-1 routing can collapse under uniform features
-> route-relevant hidden geometry is reachable, but all-position mixing can
   select the wrong state population
-> real-DCLM proxy centers are linearly routable at step 0 but are overwritten
   by ordinary training
-> finite low-tail margin is the local preservation state; common energy alone
   is not a stable causal explanation
-> expert utility sets task-directed boundary pressure, while signed background
   projection and representation-router-optimizer co-dynamics consume or
   restore margin
-> correct conditional exposure creates held-out specialist function
-> selected-only weighted top-1 can preserve a correct specialist but cannot
   discover it from a wrong rank on the learned bridge
-> one rotating challenger supplies the missing counterfactual utility
-> q10 or lower-CVaR10 safely switches from discovery to top-1 exploitation in
   the frozen four-expert system
-> the next decision is whether a real workload has stable expert-utility
   headroom worth routing
```

## Current Evidence Boundary

Can claim:

```text
Route-relevant hidden geometry can initialize a controlled partition, and real
DCLM proxy centers are linearly routable at step 0. Ordinary real-DCLM training
can overwrite that proxy routing. Positive low-tail margin is the local
preservation buffer, but its dynamics require expert utility, signed background
projection, representation motion, router motion, and transmitted update scale.
Correct conditional exposure creates held-out specialist utility. On the
learned bridge, selected-only weighted top-1 preserves a correct specialist but
does not discover it from rank 2 or rank 4. One rotating challenger restores
discovery, and q10/lower-CVaR10 utility rules terminate audition without
premature stopping in the frozen four-expert system.
```

Cannot claim:

```text
Real semantic experts exist.
Balanced load proves specialization.
High route NMI proves expert utility.
The current common projector is the true causal common operator.
Common subtraction is already a validated routing method.
Any first sign flip proves irreversible routing collapse.
A07 neural proxy already proves useful MoE specialization.
The controlled challenger Router transfers to joint pretrained-LLM training.
Repository code has positive held-out expert-utility headroom.
The controlled phase switch scales to many experts or saves wall-clock cost.
Reverse KV retrieval follows from the current evidence.
```

## 05 / 06 / 07 Reading Entry

Root sync now stores research-line synthesis, not full anchor mirrors:

```text
sync/S000_current_specialization/README.md
sync/S000_current_specialization/research_lines/00_overall_current_line_cn.md
sync/S000_current_specialization/research_lines/05_failure_mechanism_line_cn.md
sync/S000_current_specialization/research_lines/06_proxy_preservation_line_cn.md
sync/S000_current_specialization/research_lines/07_interference_value_line_cn.md
```

Project-local source anchors remain the source of truth:

```text
Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/
Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/
Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/
```

Most important current evidence:

```text
Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/research_map.md
Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_00_functional_specialization_contract/06_00_functional_specialization_contract_anchor.md
Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor.md
Projects/from-attention-to-search/main/experiments/A05/A05_04_03_real_text_common_logit_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_04_E01_real_proxy_operationalization/summary.md
Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_04_E03_real_proxy_training_overwrite/summary.md
Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_03_E04_all_position_pool_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_01_E06_margin_budget_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E01_representation_router_optimizer/summary.md
Projects/from-attention-to-search/main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_01_E01_trainable_expert_utility/summary.md
Projects/from-attention-to-search/main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_02_E01_wrong_rank_correction/summary.md
Projects/from-attention-to-search/main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_03_E01_rotating_challenger/summary.md
Projects/from-attention-to-search/main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_04_E03_tail_safe_certificate/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_01_common_rare_conflict_metric_audit/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_02_common_controlled_rare_interference/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_03_route_function_binding/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_04_common_rare_gradient_conflict_splitting/summary.md
Projects/from-attention-to-search/main/stories/11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary.md
Projects/from-attention-to-search/main/stories/11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary_cn.md
Projects/from-attention-to-search/main/stories/12_structured_compositional_mtp_workload/01_structured_composition_workload_and_standard_head_use.md
Projects/from-attention-to-search/main/stories/12_structured_compositional_mtp_workload/01_structured_composition_workload_and_standard_head_use_cn.md
Projects/from-attention-to-search/main/experiments/A11/11_01_informative_horizon_supervision/A11_01_01_E01_next_k_inclusion_law/summary.md
Projects/from-attention-to-search/main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E02_all_position_path_decomposition/summary.md
Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E02_end_to_end_use_boundary/summary.md
Projects/from-attention-to-search/main/experiments/A12/12_01_compositional_workload_capability_gate/A12_01_01_E02_explicit_binding_calibration/summary.md
Projects/from-attention-to-search/main/experiments/A12/12_02_interference_capacity_curriculum_boundary/A12_02_01_E01_task_rank_competition/summary.md
Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_03_standard_head_causal_use/12_03_standard_head_causal_use_anchor.md
Projects/from-attention-to-search/main/experiments/A12/12_03_standard_head_causal_use/A12_03_E01_standard_head_causal_use/protocol.md
daily_research_reports/0629/docs/nested_prediction_spectral_anisotropy_causal_rewrite_v4.md
daily_research_reports/0701/meeting_brief.md
```

## Active Mainline Sync Rule

For this active specialization line, `PROJECTS.md` and the active root sync
entry must move together when the mainline state changes.

A mainline state change means an accepted update to any of these objects:

```text
current decision question
active ladder level
current route
current evidence boundary
claim boundary
next decision
web-side source links
```

When that happens, update the active root sync entry in the same task:

```text
sync/S000_current_specialization/README.md
sync/S000_current_specialization/research_lines/00_overall_current_line_cn.md
and the affected 05 / 06 / 07 research-line note when needed
```

This rule is for keeping web-side and cross-project readers current. It is not
a raw-output mirror and does not authorize graph edits, external collaborator
sync, handoff packaging, commits, pushes, or copying full anchors unless the
user explicitly asks for those actions.

## Synthetic Versus Real Boundary

Controlled synthetic experiments can establish:

```text
whether a mechanism is possible;
whether a metric surface is valid;
whether a known feature partition can be discovered, routed, preserved, or
used under controlled labels and controlled nuisance variables.
```

They cannot establish:

```text
natural-language semantics;
real-checkpoint behavior;
deployable routing;
real expert utility;
robust transfer from controlled labels to open text.
```

Real-DCLM proxy experiments can establish:

```text
whether stable hidden-state proxy clusters exist;
whether those proxy clusters are linearly routable at step 0;
whether ordinary next-token training preserves or erases that proxy routing.
```

They cannot establish by themselves:

```text
semantic feature identity;
causal expert utility;
dense-beating MoE value;
final pretrained-MoE behavior.
```

## Next Decision

Do not run another broad feature-existence, common-subtraction, or spectral
router sweep. The next anchor should decide one causal bottleneck:

```text
representation-router-optimizer co-dynamics under full-sequence LM training
```

Primary metric:

```text
whether router-only, representation-only, joint-SGD, or joint-AdamW freeze
interventions reproduce or remove matched-margin first crossing and re-entry
```

Required guards:

```text
margin p05, matched identity, route NMI, LM loss, first-cross time, re-entry
time, X/A/Q/h source-center trajectories, raw source gradients, AdamW moments,
actual preconditioned boundary updates, max load, and active experts
```

The exact three-term finite margin decomposition is an algebraic validity guard,
not causal evidence. Method construction is allowed only after freeze
interventions localize the necessary path to representation formation, router
correction, optimizer transmission, or their interaction.

## Root Surfaces

- `AGENTS.md`: general agent behavior and repository rules.
- `PROJECTS.md`: this current project-state registry.
- `sync/`: compact research-line synthesis for web-side or cross-project readers.
- `Projects/graphs/`: Sidecar-readable graph manifests.
- `daily_research_reports/`: daily cards and meeting materials.
- `paper_reading/`: paper and blog reading cards.
- `templates/`: maintained reusable templates.
- `prompts/`: reusable prompts.
- `skills/`: repo-tracked skill sources.

## Web-Side Rule

Web-side agents should not rely on chat history. If they cannot inspect
`Projects/`, use this file and `sync/` first, then ask a local Codex agent to
expose the relevant graph, anchor, or experiment record.

## Course Delivery Projects

Academic Writing Project 2 is a course-delivery wrapper:

```text
Projects/academic_writing/
```

It uses the current MoE gating specialization work as source material for
slides, a poster, and a CVPR-format manuscript. It does not replace the
research mainline and should not update graphs, root sync, or experiment
records unless explicitly requested.

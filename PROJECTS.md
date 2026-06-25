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
active bottleneck: 3. Preservation
```

Practical reading:

```text
Level 0 has failure-mechanism evidence.
Level 1 has controlled and real-DCLM proxy evidence, with semantic boundaries.
Level 2 has real-DCLM step-0 proxy-center router evidence.
Level 3 is the current unsolved bottleneck: ordinary training erases the proxy
partition by step 5/10.
Level 4 has controlled D07 support only; neural/real-DCLM utility is not yet
supported.
Level 5 is parked until preservation and utility are both better defined.
```

Do not promote a higher-level claim when only a lower-level metric passed.
For example, balanced load or high route NMI can support non-collapse or
alignment, but cannot by itself support utility or scaling.

## Current Question

Current decision question:

```text
Can a step-0 real-DCLM proxy partition be preserved through the step-5/10
training window without unacceptable language-model loss regression?
```

This question is downstream of A05/A06 and upstream of stronger A07 utility
claims.

## Current Route

The current route is:

```text
05 failure mechanism
-> 06 route-relevant proxy discovery, initialization, and preservation
-> 07 functional interference value after preservation
```

Sharper logic:

```text
ordinary top-1 routing can collapse under uniform features
-> collapse can come from common components, wrong hidden-state populations,
   and early-training feedback
-> route-position feature geometry can be discovered and linearly routed
-> all-position clustering is not a valid proxy population
-> real-DCLM proxy routing exists at step 0 but ordinary training erases it
-> functional value must be tested through common/rare interference or expert
   utility, not load balance alone
```

## Current Evidence Boundary

Can claim:

```text
Controlled route-position feature partitions are reachable. Ordinary top-1
routing does not naturally discover or preserve the right partition. In real
DCLM early training, proxy routing can be overwritten by step 5/10.
```

Cannot claim:

```text
Real semantic experts exist.
Balanced load proves specialization.
High route NMI proves expert utility.
A07 neural proxy already proves useful MoE specialization.
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
Projects/from-attention-to-search/main/problem_anchors/05_06_07_initialization_collapse_to_interference_chain_cn.md
```

Most important current evidence:

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

Do not run another broad feature-existence sweep. The next useful protocol
should decide one bottleneck:

```text
real-DCLM early-preservation / anti-feedback
```

Primary metric:

```text
proxy_route_NMI at step 5/10 under fixed step-0 proxy labels
```

Required guards:

```text
LM loss, max load, active experts, common margin, and exact gate-input audit
```

If preservation succeeds, return to A07 utility on a preserved partition. If it
fails, decompose gate update, hidden-state drift, expert feedback, and optimizer
geometry before proposing another method.

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

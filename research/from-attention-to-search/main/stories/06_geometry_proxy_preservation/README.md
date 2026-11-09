# A06 Story Registry

This folder owns the line-level synthesis for A06.

## Ordered Story Registry

| Order | Story pair | Scope | Status |
|---:|---|---|---|
| 01 | `01_functional_specialization_and_utility_routing.md`, `01_functional_specialization_and_utility_routing_cn.md` | Complete A06 story: route-relevant geometry, preservation dynamics, expert utility, partial-feedback repair, and the first registered real-code headroom failure | **Current primary synthesis** |
| 02 | `paper_reading_router_dynamics_cn.md` | Router-dynamics paper notes and local connections | Supporting reading; not a formal story |

Exactly one formal story pair is active. Anchor-specific results remain in
anchors and experiment reports rather than becoming separate stories.

## Current Line Judgment

```text
route-relevant geometry is reachable
-> real proxy routing can still be overwritten by training
-> finite margin is the local preservation state
-> correct exposure creates held-out specialist utility
-> selected-only top-1 can preserve but fail to discover a useful expert
-> one challenger supplies the missing counterfactual utility
-> lower-tail utility safely switches back to top-1 in the frozen bridge
-> relevant context changes expert effects on CrossCodeEval
-> the selected expert is not split stable and positive absolute headroom fails
```

This closes the controlled synthetic mechanism chain. It does not establish a
deployable LLM Router, natural semantic experts, joint-training stability,
many-expert scaling, or systems savings. The CrossCodeEval result closes only
the registered final-layer frozen-pool clause; it does not adjudicate every
unfiltered repository-code workload or layer.

## Active Decision

The only active A06 decision is:

> After the registered CrossCodeEval final-layer pool failed split stability
> and positive absolute headroom, should A06 approve one training-time
> selective-sharing test on an explicit real rare/common workload?

Current parent:
`../../problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor.md`
with Chinese companion
`../../problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor_cn.md`.

Completed local clause and result:
`../../problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/subanchors/06_04_01_context_conditioned_expert_utility_anchor.md`
and
`../../experiments/A06/06_04_real_workload_utility_headroom/A06_04_01_E01_context_conditioned_expert_utility/summary.md`.

## Reading Order

1. `01_functional_specialization_and_utility_routing_cn.md` for the current Chinese synthesis.
2. `01_functional_specialization_and_utility_routing.md` for the canonical English synthesis.
3. `../../problem_anchors/06_geometry_proxy_preservation/research_map.md` for the five-parent-anchor chain and local subanchors.
4. `anchor_threads/06_04/story_fragment.md` for the bounded `kv_cache` continuity, feature-context, systems-cost, and push-time evidence.
5. `paper_reading_router_dynamics_cn.md` for supporting literature notes.

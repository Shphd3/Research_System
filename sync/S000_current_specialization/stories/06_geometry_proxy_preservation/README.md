# A06 Story Registry

This folder owns the line-level synthesis for A06.

## Ordered Story Registry

| Order | Story pair | Scope | Status |
|---:|---|---|---|
| 01 | `01_functional_specialization_and_utility_routing.md`, `01_functional_specialization_and_utility_routing_cn.md` | Complete A06 story: route-relevant geometry, preservation dynamics, expert utility, partial-feedback routing, controlled repair, and the real-workload gate | **Current primary synthesis** |
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
```

This closes the controlled synthetic mechanism chain. It does not establish a
deployable LLM Router, natural semantic experts, joint-training stability,
many-expert scaling, or systems savings.

## Active Decision

The only active A06 decision is:

> Does unfiltered repository-level code completion contain positive,
> cross-split-stable held-out oracle routing headroom after nuisance controls?

Active draft:
`../../problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor.md`
with Chinese Thinking Card
`../../problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor_cn.md`.

## Reading Order

1. `01_functional_specialization_and_utility_routing_cn.md` for the current Chinese synthesis.
2. `01_functional_specialization_and_utility_routing.md` for the canonical English synthesis.
3. `../../problem_anchors/06_geometry_proxy_preservation/research_map.md` for the five-parent-anchor chain and local subanchors.
4. `paper_reading_router_dynamics_cn.md` for supporting literature notes.

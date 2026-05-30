# Source Registry Used By This Plan

This file records which repo rules and current evidence this plan used.

## Repository rules

```text
AGENTS.md
PROJECTS.md
skills/research-progress-core/SKILL.md
skills/problem-anchor-writer/SKILL.md
skills/experiment-card-writer/SKILL.md
skills/remote-experiment-workflow/SKILL.md
skills/research-mainline/SKILL.md
skills/handoff-report-writer/SKILL.md
skills/research-progress-core/references/algorithm_specification.md
```

## Current project state

```text
sync/S000_current_specialization/README.md
sync/S000_current_specialization/anchors/expert_specialization/slot_context_dominance_router_specialization_anchor.md
sync/S000_current_specialization/anchors/expert_specialization/hierarchical_route_utility_binding_anchor.md
daily_research_reports/0529/hierarchical_route_utility_binding/detailed.md
```

## Existing evidence imported into this plan

```text
1. ordinary top-1 NTP can learn target but does not reliably form route-function binding.
2. slot information can be visible and oracle routing can work while learned routing remains unstable.
3. common_flat is currently more promising than pure flat_top1 or deeper hierarchical_common, but common path alone is not proven.
4. structural hierarchy alone is weakened as a main explanation.
5. linear FFN frequency toy supports head write-in / tail write-in failure under Zipf.
```

## Current route

```text
diagnose router factor control
-> decide residual/whitening vs explicit binding regularizer vs expert write-in pressure
-> stress under Zipf/common compositional data
-> only then consider real training transfer
```

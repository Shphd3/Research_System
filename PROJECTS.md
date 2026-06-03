# Projects

This is the root project registry for the research system. Use it after
`AGENTS.md`.

## Global Rule

For project-specific work, identify the project here, then read only the
project's graph, anchor, roadmap, worker README, sync report, or result summary
needed for the current question.

Do not scan whole project repositories by default. The graph is the navigation
layer; problem anchors and sync reports are the reasoning layer.

## Project Priority

Primary mainline:

```text
Projects/kv_cache/
```

Main specialization reference:

```text
Projects/kv_cache/main_specialization/specialization_overview.md
```

Mainline question:

```text
How can gating make MoE experts form stable, interpretable, reusable feature-level specialization?
```

Read-only rule:

```text
Do not edit Projects/kv_cache unless the user explicitly asks.
```

Active work branch:

```text
Projects/from-attention-to-search/
Projects/from-attention-to-search/XingyuD/
```

This branch stores current experiments, branch-local sync notes, anchors, and
Sidecar-readable graph updates that support the primary mainline.

Current branch anchor:

```text
Projects/from-attention-to-search/main/problem_anchors/01_slot_context_dominance_router_specialization_anchor.md
```

Current branch graph:

```text
Projects/from-attention-to-search/graph.yaml
```

## Current Route

The current research route is:

```text
define feature-level expert specialization
-> diagnose why baseline gating does not produce stable functional specialization
-> bind route assignment to expert causal utility
-> test downstream effects only after specialization is supported
```

Reverse KV retrieval is now archived as a downstream-effect line. It should not
be used as the first success criterion for the current anchor.

## Root Surfaces

- `AGENTS.md`: global agent behavior and repository rules.
- `PROJECTS.md`: project priority and routing map.
- `sync/`: compact root-level current-state summaries for web-side partners.
- `daily_research_reports/`: daily cards and meeting materials.
- `paper_reading/`: paper and blog reading cards.
- `templates/`: single maintained reusable-template folder.
- `prompts/`: reusable prompts.
- `skills/`: repo-tracked skill sources.

Current root sync:

```text
sync/S000_current_specialization/
```

Current root anchor copy:

```text
sync/S000_current_specialization/anchors/expert_specialization/01_slot_context_dominance_router_specialization_anchor.md
```

This copy is updated only when the user explicitly asks to sync root sync. The
project-local anchor remains the source of truth.

## Web-Side Rule

Web-side agents should not rely on chat history or old compatibility snapshots.
If they cannot see `Projects/`, use `PROJECTS.md` and `sync/` summaries, then
ask the user or a local Codex agent to expose the relevant graph, anchor, or
sync report.

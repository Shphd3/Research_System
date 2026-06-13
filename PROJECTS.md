# Projects

This is the root project registry for the research system. Use it after
`AGENTS.md`.

## Global Rule

For project-specific work, identify the project here, then read the relevant
cross-project graph under `Projects/graphs/`, and only then read the linked
project anchor, roadmap, worker README, sync report, or result summary needed
for the current question.

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
result records that support the primary mainline.

Current branch anchor:

```text
Projects/from-attention-to-search/main/problem_anchors/01_slot_context_dominance_router_specialization_anchor.md
```

Cross-project graph hub:

```text
Projects/graphs/
Projects/graphs/expert_specialization.graph.yaml
Projects/graphs/kv_cache_retrieval.graph.yaml
Projects/graphs/specialization_papers.graph.yaml
```

Legacy branch-local graph:

```text
Projects/from-attention-to-search/graph.yaml
```

The graph hub lives under `Projects/graphs/`, not inside a single project. Its
nodes link to concrete project documents such as anchors, experiment summaries,
detailed records, report cards, and paper notes.

Graph display rule:

```text
Use Sidecar to display/open graphs. For cross-project graphs, start Sidecar
with workspace root `/data/250010109/Research_System` and graph manifest such
as `Projects/graphs/expert_specialization.graph.yaml`. Do not create ad hoc
HTML graph views unless the user explicitly asks for an exported static
artifact.
```

## Current Route

The current research route is:

```text
define feature-level expert specialization
-> answer the advisor's weak toy question: same-feature route consistency
-> audit operational feature identity: slot vs B_i vs (slot, B_i)
-> audit non-collapse and expert composition under the chosen feature definition
-> only then test route-utility binding
-> only then test Zipfian / real-corpus robustness
```

Current local focus:

```text
Before route-utility binding, first define the operational feature and test
what the router actually binds to: slot, B_i, or the atomic pair (slot, B_i).
Also distinguish weak same-feature consistency from non-collapsed feature
specialization.
```

Reverse KV retrieval is now archived as a downstream-effect line. It should not
be used as the first success criterion for the current anchor.

## Root Surfaces

- `AGENTS.md`: global agent behavior and repository rules.
- `PROJECTS.md`: project priority and routing map.
- `sync/`: compact root-level current-state summaries for web-side partners.
- `Projects/graphs/`: Sidecar-readable cross-project graph manifests.
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

## Course Delivery Projects

Academic Writing Project 2 is tracked as a course-delivery wrapper:

```text
Projects/academic_writing/
```

It uses the current MoE gating specialization work as source material for
slides, a poster, and a 10-page CVPR-format manuscript. It does not replace the
`from-attention-to-search` research mainline and should not update graphs,
root sync, or experiment records unless explicitly requested.

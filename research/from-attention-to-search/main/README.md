# from-attention-to-search project entry

[中文](README_cn.md) · [Research roadmap](roadmap.md) · [Project rules](../AGENTS.md) · [Research question map](research_map.md)

Use the [roadmap](roadmap.md) to locate an A-numbered line and question. This conversation's small-model relation analysis is the [A15_18 factual report](experiments/A15/15_18_context_relation_organization_use/first_flow_v3/summary.md). A named result can be read directly without traversing every index.

## Current map entry — 4 November

[Spectra, composition, output interventions and training utility](research_map_update_20261104.md): 166 owners, 85 parents and 81 children. Start with seven reading groups, then inspect the complete tree.

## Map refresh — 31 October

[New work and classification audit](research_map_update_20261031.md): 159 formal owners, 84 parents and 75 children. The seven reading groups do not change question priorities or scientific acceptance.

## Research map and offline interactive view

The [Chinese research map](research_map_cn.md) and [English entry](research_map.md) explain the roles of each line, parent question and local child. [research_map.json](research_map.json) is derived navigation data. Scientific design, researcher judgment and results remain with the original Anchors, Focus records and experiment records.

From the project root, run `python scripts/render_research_map.py --data main/research_map.json --output <execution-side-html>`, replacing the output argument with an execution-side HTML path. The generated view opens offline. The [existing file on this machine](/data/250010109/MoE_Router/research_reading/20261105_checkpoint_evidence_use/research_map.html) is a local reading artifact, not a cross-machine web address; regenerate it from the same data on another machine.

## Working together with the map

Describe an idea, question or confusing passage in ordinary language. AI locates
the most relevant existing question, explains the connection and uses a real
example to establish a shared understanding.

First distinguish an explanation that needs clarification from evidence that is
actually missing. When further research is needed, connect existing observations,
rival explanations and the remaining gap. Present one concrete next choice and
what each route could answer. The researcher owns research priorities and
mechanism judgments.

When discussion establishes a new connection, evidence boundary or
researcher-confirmed next decision, AI maintains the owning records, map text
and interactive view, then briefly explains what changed, why and what remains
open. New ideas begin as proposals rather than automatic Anchors or experiments.
The researcher need not learn IDs or organize files first.

## Record ownership

| Location | Owns | Does not replace |
|---|---|---|
| [focus/](focus/README.md) | Stable questions, researcher judgment and next decisions | Execution authorization |
| [problem_anchors/](problem_anchors/README.md) | A-numbered scientific designs | Focus judgment or Protocol approval |
| [experiments/](experiments/README.md) | Exact contracts, result summaries and full evidence | Scientific acceptance with execution completion |
| [datasets/](datasets/README.md) | Dataset identity, provenance and views | Execution-side raw data and activations |
| [research_notes/](research_notes/) | Derivations, discussions, source packages and supporting notes | The current design |
| [stories/](stories/) | Cross-round reading syntheses | Frozen results or scientific state |
| [organization_migrations/](organization_migrations/20261022/README.md) | Relocations, old paths and identifier mappings | New hypotheses, approval or results |

The [ownership registry](anchor_ownership.json) covers 159 formal owners, parent/child relations, language companions, experiment ownership and legacy identities. A00 is a historical definition redirect. Archives, sources, supporting_records and historical_support preserve material rather than additional current Anchors.

## Two registered layouts

- `parent_subanchor`: each independent parent has a folder; local controls, repairs and rivals live in its `subanchors/`. Dependency alone does not create parenthood.
- `registered_flat`: established A01 / A05 / A07 / A09 / A10 lines retain their flat layout without mixing layouts inside a line. The A01 experiment directory `A01_common_operator` is explicitly registered.

Formal experiment records belong to their A line and owner. Protocol, Summary and Detailed retain separate roles. Models, raw outputs, large caches and unfiltered logs remain in execution repositories. New work follows the [project rules](../AGENTS.md) and [system rules](../../../AGENTS.md).

This entry only navigates. Focus identities, language authority, judgment and approval remain in their owning records. [PROJECTS.md](../../../PROJECTS.md) selects the project; the [roadmap](roadmap.md) and owners navigate within it.

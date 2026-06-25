# Research Files

This repository is a research-process workspace. It is not the remote experiment codebase.

The goal is to preserve research judgment: project graph, problem anchors,
hypotheses, evidence, claim boundaries, protocols, result records, and
meeting materials.

## Current Research Snapshot

The active specialization question is no longer whether a controlled feature
partition can be constructed. A05, A06, and A07 currently say:

- ordinary top-1 routing can fail because the gate follows a common component,
  the wrong hidden-state population, or an early-training feedback path;
- route-position feature geometry is reachable, but all-position clustering is
  not a reliable proxy for route-relevant states;
- real-text proxy routing can exist at step 0, but ordinary training can erase
  it by step 5/10;
- functional specialization remains unclaimed until a preserved partition also
  improves feature utility or reduces common/rare interference.

Current mainline anchor:

```text
sync/S000_current_specialization/anchors/expert_specialization/00_feature_level_expert_specialization_mainline_anchor.md
```

Current next decision:

```text
Write and approve one real-text early-preservation protocol: can a step-0 DCLM
proxy partition survive the step-5/10 training window without unacceptable
language-model loss regression?
```

Canonical research artifacts are written in English by default. Chinese
companion files are allowed when useful; add `_cn` before the extension, for
example `summary_cn.md` or `<anchor_id>_cn.md`.

## Start Here

- `AGENTS.md`: project-level Codex instructions.
- `PROJECTS.md`: project registry, active route, graph hub, and root-level state map.

## Working Areas

- `daily_research_reports/`: dated folders for daily cards, meeting materials, experiment summaries, and report bundles.
- `paper_reading/`: literature cards and reading notes.
- `skills/`: repo-tracked source copies of personal Codex skills.
- `sync/`: cross-project anchor summaries and reusable research state.
- `templates/`: the single maintained folder for reusable templates.
- `prompts/`: reusable project prompts and older workflow prompts.
- `docs/`: setup notes for tooling and workflow maintenance.

## Daily Loop

1. Read `PROJECTS.md`, then the relevant graph under `Projects/graphs/` and
   the linked problem anchor, experiment result, paper note, or sync note.
2. Decide whether today's work updates the graph, anchor, claim boundary, or
   next decision.
3. Write a compact daily card, anchor update, protocol, or result record.
4. State the conclusion for each task, not a task log.
5. Park side thoughts instead of chasing them during the current 25 minute task.
6. Update anchors only when evidence changes the route, claim boundary,
   bottleneck, hypothesis status, or next decision.
7. Do not update root sync, package handoff reports, edit graph manifests,
   commit, or push unless explicitly requested.

Daily notes should be placed at `daily_research_reports/MMDD/` when useful.
There is no maintained daily-card template; keep daily notes minimal and
free-form.

Reusable templates live in `templates/`. Do not create new reusable templates
inside daily, paper-reading, docs, or project folders by default.

Class notes and side thoughts should stay inside `daily_card.md` by default.
Use `Class Notes` for class points, and `Small Thought Parking Lot` for side
ideas that should not interrupt the current task.

Meeting materials should be placed at `daily_research_reports/MMDD/meeting/`.

## Physical-Prior-First Loop

For project research, write a problem anchor before experiment work when the
question is not yet stable. The anchor should state the physical prior before
the falsifiable hypothesis:

```text
Projects/graphs/<topic>.graph.yaml
Projects/<project>/main/problem_anchors/<anchor_id>.md
```

After the anchor is stable, write `protocol.md` for user approval before
implementation or running:

```text
Projects/<project>/main_specialization/problem_anchors/<anchor_id>.md
Projects/<project>/main/problem_anchors/<anchor_id>.md
Projects/<project>/main/experiments/A<anchor_id>/<experiment_id>/protocol.md
Projects/<project>/main/experiments/A<anchor_id>/<experiment_id>/summary.md
Projects/<project>/main/experiments/A<anchor_id>/<experiment_id>/detailed.md
```

Default principle: fewer, sharper experiments. Each experiment should deepen
understanding, test a hypothesis, or change a next decision.
Nontrivial experiments should stop at `protocol.md` until the user approves the
implementation or run.

When a handoff is explicitly requested, place the handoff report and the most
important anchor copy in today's folder by default:

```text
daily_research_reports/MMDD/<topic>/handoff_report.md
daily_research_reports/MMDD/<topic>/<anchor_id>.md
```

When syncing a daily result to another project or collaborator repo, copy the
same curated set: subject-bearing anchor, `protocol.md`, `summary.md`,
`detailed.md`, and only the figures/tables referenced by those documents.

## Web-Side AI

Web-side theory AI should treat this repository as research memory, not as the
experiment codebase. Start from `AGENTS.md`, `PROJECTS.md`, and root `sync/`.
Use `Projects/graphs/` for the cross-project map. Use project-local graph,
anchor, `summary.md`, and `detailed.md` only when the user or Codex exposes
them.

Web-side AI should propose research judgments and questions. Codex/local agents
perform repository edits after the user confirms the research-state change.

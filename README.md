# Research Files

This repository is a research-process workspace. It is not the remote experiment codebase.

The goal is to preserve research judgment: project graph, problem anchors,
evidence, claim boundaries, protocols, result records, stories, and meeting
materials.

## Current Research Snapshot

The project map lives in `PROJECTS.md`; today's resume point and daily research
ledger live in `CURRENT.md`. The compact web-side research line lives in:

```text
sync/S000_current_specialization/
```

The active specialization line currently runs:

```text
05 failure mechanism
-> 06 geometry, preservation, expert utility, and sparse discovery
-> 06 real-workload utility headroom gate
-> 07 interference value only after the gate passes
```

The project-level next decision is narrow: decide whether unfiltered
repository-level code completion has positive, cross-split-stable held-out
oracle routing headroom after registered nuisance controls.

For the 2026-07-17 group meeting, a separate draft cross-line theme asks what a
long-context Router should optimize so that selected evidence preserves the
ordinary prediction head's decision under a fixed budget. This working theme is
published in `sync/S000_current_specialization/research_lines/13_long_context_functional_retrieval_working_theme_cn.md`;
it does not replace the A06 decision or authorize an experiment.

Canonical research artifacts are written in English by default. Chinese
companion files are allowed when useful; add `_cn` before the extension, for
example `summary_cn.md` or `<anchor_id>_cn.md`.

## Start Here

- `AGENTS.md`: general Codex rules for this repository.
- `PROJECTS.md`: current project registry, active route, graph hub, claim
  boundary, and next decision.
- `CURRENT.md`: today's focus, completed progress, claim boundary, and resume
  action; it links to the authoritative source artifacts.
- `sync/S000_current_specialization/`: published research-line summaries and
  the generated link-safe full anchor mirror. Republish it only through
  `skills/research-mainline/scripts/publish_anchor_mirror.py`.

## Working Areas

- `daily_research_reports/`: dated folders for daily cards, meeting materials, experiment summaries, and report bundles.
- `paper_reading/`: literature cards and reading notes.
- `skills/`: repo-tracked source copies of personal Codex skills.
- `sync/`: compact research-line summaries and reusable current-state maps.
- `templates/`: the single maintained folder for reusable templates.
- `prompts/`: reusable project prompts and older workflow prompts.
- `docs/`: setup notes for tooling and workflow maintenance.

## Daily Loop

1. Before AI use, write today's question, current mechanism guess, strongest
   rival, uncertainty, mind-changing evidence, and one decision.
2. Read `PROJECTS.md`, then `CURRENT.md`, then the relevant graph under
   `Projects/graphs/` and the linked problem anchor, experiment result, paper
   note, or sync note.
3. Decide whether today's work updates the graph, anchor, claim boundary, or
   next decision.
4. Update the compact resume point in `CURRENT.md`; write a detailed daily
   card, anchor update, protocol, or result record only when needed.
5. At the end of the day, close source material and write the direct result,
   changed belief, claim boundary, and next decision from memory. AI audits and
   revises only after this human draft.
6. Park side thoughts instead of chasing them during the current task.
7. Update anchors only when evidence changes the route, claim boundary,
   bottleneck, hypothesis status, or next decision.
8. Do not update root sync, package handoff reports, edit graph manifests,
   commit, or push unless explicitly requested.

Daily notes should be placed at `daily_research_reports/MMDD/` when useful.
There is no maintained daily-card template; keep daily notes minimal and
free-form.

Reusable templates live in `templates/`. Do not create new reusable templates
inside daily, paper-reading, docs, or project folders by default.

Class notes and side thoughts should stay inside `daily_card.md` by default.
Use `Class Notes` for class points, and `Small Thought Parking Lot` for side
ideas that should not interrupt the current task.

Meeting materials should be placed at `daily_research_reports/MMDD/meetings/`.
The final meeting brief contains only the executive summary and starts from a
human-written draft.

## Physical-Prior-First Loop

For project research, first write an independent Thinking Card, then let AI
audit it. Write the formal anchor only after the human approves the question,
physical prior, rival, metric, boundary, and decision:

```text
Projects/graphs/<topic>.graph.yaml
templates/research_process/thinking_card_template.md
Projects/<project>/main/problem_anchors/<anchor_id>.md
```

Name project-local cards with the anchor stem:

```text
<anchor_stem>_thinking_card.md
<anchor_stem>_thinking_card_cn.md
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

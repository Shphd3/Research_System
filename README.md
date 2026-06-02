# Research Files

This repository is a research-process workspace. It is not the remote experiment codebase.

The goal is to preserve research judgment: project graph, problem anchors,
hypotheses, evidence, claim boundaries, result records, handoff reports, and
meeting-ready reports.

## Start Here

- `AGENTS.md`: project-level Codex instructions.
- `PROJECTS.md`: project registry, active project route, and root-level state map.

## Working Areas

- `daily_research_reports/`: dated folders for daily cards, meeting materials, experiment summaries, and report bundles.
- `paper_reading/`: literature cards and reading notes.
- `skills/`: repo-tracked source copies of personal Codex skills.
- `sync/`: cross-project anchor summaries and reusable research state.
- `templates/`: the single maintained folder for reusable templates.
- `prompts/`: reusable project prompts and older workflow prompts.
- `docs/`: setup notes for tooling and workflow maintenance.

## Daily Loop

1. Read `PROJECTS.md`, then the active project's `graph.yaml` and relevant
   problem anchor or sync note.
2. Decide whether today's work updates the graph, anchor, claim boundary, or
   next decision.
3. Write a compact daily card, anchor update, protocol, or result record.
4. State the conclusion for each task, not a task log.
5. Park side thoughts instead of chasing them during the current 25 minute task.
6. Update anchors only when evidence changes the route, claim boundary,
   bottleneck, hypothesis status, or next decision.
7. Do not update root sync, package handoff reports, edit `graph.yaml`, commit,
   or push unless explicitly requested.

Daily notes should be placed at `daily_research_reports/MMDD/` when useful.
There is no maintained daily-card template; keep daily notes minimal and
free-form.

Reusable templates live in `templates/`. Do not create new reusable templates
inside daily, paper-reading, docs, or project folders by default.

Class notes and side thoughts should stay inside `daily_card.md` by default. Use `Recording / Class Notes` for class points, and `Small Thought Parking Lot` for side ideas that should not interrupt the current task.

Meeting materials should be placed at `daily_research_reports/MMDD/meeting/`.

## Hypothesis-First Loop

For project research, write a problem anchor before hypothesis and experiment
work when the question is not yet stable:

```text
Projects/<project>/main/problem_anchors/<anchor_id>.md
Projects/<project>/graph.yaml
```

After the anchor is stable, write a short protocol for user approval before the
operational execution plan:

```text
Projects/<project>/main_specialization/problem_anchors/<anchor_id>.md
Projects/<project>/main/problem_anchors/<anchor_id>.md
Projects/<project>/main/experiments/<experiment_id>/protocol_for_approval.md
Projects/<project>/main/experiments/<experiment_id>/execution_plan.md
Projects/<project>/main/experiments/<experiment_id>/summary.md
Projects/<project>/main/experiments/<experiment_id>/detailed.md
daily_research_reports/MMDD/<topic>/05_report_card.md
```

Default principle: fewer, sharper experiments. Each experiment should deepen
understanding, test a hypothesis, or change a next decision.
Nontrivial experiments should stop at `protocol_for_approval.md` until the user
approves the run.

When a handoff is explicitly requested, place the handoff report and the most
important anchor copy in today's folder by default:

```text
daily_research_reports/MMDD/<topic>/handoff_report.md
daily_research_reports/MMDD/<topic>/<anchor_id>.md
```

When syncing a daily result to another project or collaborator repo, copy the
same curated set: subject-bearing anchor, `summary.md`, `detailed.md`,
`05_report_card.md`, and only the figures/tables referenced by those documents.

## Web-Side AI

Web-side theory AI should treat this repository as research memory, not as the
experiment codebase. Start from `AGENTS.md`, `PROJECTS.md`, and root `sync/`.
Use project-local graph, anchor, `summary.md`, and `detailed.md` only when the
user or Codex exposes them.

Web-side AI should propose research judgments and questions. Codex/local agents
perform repository edits after the user confirms the research-state change.

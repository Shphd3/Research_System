# Research Files

This repository is a research-process workspace. It is not the remote experiment codebase.

The goal is to preserve research judgment: project graph, problem anchors,
evidence, claim boundaries, protocols, result records, stories, and meeting
materials.

## State Location

Project routes, claim boundaries, and project-level next decisions live only in
`PROJECTS.md`. Each day's human idea, progress, and resume point live in
`daily_research_reports/MMDD/focus.md`. Compact web-side research lines live
under:

```text
sync/
```

Do not copy changing research conclusions into this README; use it only for
repository orientation.

Canonical research artifacts are written in English by default. Chinese
companion files are allowed when useful; add `_cn` before the extension, for
example `summary_cn.md` or `<anchor_id>_cn.md`.

## Start Here

- `AGENTS.md`: general Codex rules for this repository.
- `PROJECTS.md`: current project registry, active route, graph hub, claim
  boundary, and next decision.
- `daily_research_reports/MMDD/focus.md`: one day's human-written idea,
  group-meeting questions, question-by-question closure, and resume action;
  create it from the maintained focus template.
- `sync/`: explicitly published research-line summaries and generated
  link-safe anchor mirrors. Use the current entry named in `PROJECTS.md` and
  republish mirrors only through
  `skills/research-mainline/scripts/publish_anchor_mirror.py`.

## Working Areas

- `daily_research_reports/`: one daily `focus.md` plus dated meeting materials,
  experiment summaries, and report bundles.
- `paper_reading/`: literature cards and reading notes.
- `skills/`: repo-tracked source copies of personal Codex skills.
- `sync/`: compact research-line summaries and reusable current-state maps.
- `templates/`: the single maintained folder for reusable templates.
- `prompts/`: reusable project prompts and older workflow prompts.
- `docs/`: setup notes for tooling and workflow maintenance.

## Daily Loop

1. Create or reopen `daily_research_reports/MMDD/focus.md` from
   `templates/research_process/focus_writing_template.md`, replace its title
   with the day's exact central research question, then list the core questions
   that the group meeting must answer. All questions must serve one overall
   decision.
2. Read `PROJECTS.md`, today's `focus.md`, then the relevant graph under
   `Projects/graphs/` and only the linked problem anchor, experiment result,
   paper note, or sync note needed for that advancement point.
3. If exploration is needed, generate at most three distinct candidates,
   select one, and park the rest before further work.
4. Write the four-sentence central judgment in the researcher's own words. AI
   asks one blocking question at a time; the researcher revises the same
   section in place.
5. Perform only the derivation, reading, diagnostic, or approved experiment
   needed to close the advancement point.
6. At the end of the day, close source material and answer every listed
   question from memory. Each answer has one decisive experiment or missing-
   experiment marker and one cannot-claim boundary. Finish with one overall
   advisor decision and one next action. AI audits only after this human draft.
7. Park side thoughts instead of chasing them during the current task.
8. Update anchors only when evidence changes the route, claim boundary,
   bottleneck, hypothesis status, or next decision.
9. Do not update root sync, package handoff reports, edit graph manifests,
   commit, or push unless explicitly requested.

Each research day has exactly one daily state file:
`daily_research_reports/MMDD/focus.md`. It is retained as the human's daily
idea/progress ledger, but it does not replace `PROJECTS.md`, anchors, protocols,
or result records. Do not create a second daily card, current log, or parallel
research-state file.

Reusable templates live in `templates/`. Do not create new reusable templates
inside daily, paper-reading, docs, or project folders by default.

Class notes, meeting materials, and side documents may still live under the
dated folder, but they do not duplicate the role of `focus.md`. Park side ideas
outside the active focus unless they change its one next decision.

For a routine single-center group meeting, the completed daily `focus.md` is
the speaking outline. Use `daily_research_reports/MMDD/meetings/` only when a
meeting combines several daily foci or research lines, or when a separate
outline is explicitly requested. A finished brief is not created by default.

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

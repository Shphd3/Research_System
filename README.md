# Research Files

This repository is a research-process workspace. It is not the remote experiment codebase.

The goal is to preserve research judgment: project graph, problem anchors,
evidence, claim boundaries, protocols, result records, stories, and meeting
materials.

## State Location

Project routes, claim boundaries, and project-level next decisions live only in
`PROJECTS.md`. Complete reader-friendly daily experiment and evidence reports
live in `daily_research_reports/MMDD/docs/daily_report_<topic_slug>.md`.
Bounded problem-level knowledge updates condensed from confirmed reports live in
`daily_research_reports/MMDD/focus_<problem>.md`; concise progressive meeting
updates live in new `daily_research_reports/MMDD/focus_meeting_<topic>.md`
files. Compact web-side research lines live under:

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
- `daily_research_reports/MMDD/docs/daily_report_<topic_slug>.md`: the
  complete reader-friendly report derived from canonical experiment evidence.
- `daily_research_reports/MMDD/focus_<problem>.md`: one problem's human-owned,
  minimal knowledge summary and navigation card derived from a confirmed daily
  report.
- `daily_research_reports/MMDD/focus_meeting_<topic>.md`: one meeting's
  progressive answer to a named problem, or to an explicitly human-scoped
  multi-problem set.
- `sync/`: explicitly published research-line summaries and generated
  link-safe anchor mirrors. Use the current entry named in `PROJECTS.md` and
  republish mirrors only through
  `.agents/skills/research-mainline/scripts/publish_anchor_mirror.py`.

## Working Areas

- `daily_research_reports/`: dated problem knowledge updates, human-scoped
  meeting syntheses, experiment summaries, and report bundles.
- `paper_reading/`: literature cards and reading notes.
- `.agents/skills/`: repo-tracked, natively discovered Codex skills; see
  `docs/skills.md` for the responsibility and trigger index.
- `sync/`: compact research-line summaries and reusable current-state maps.
- `templates/`: the single maintained folder for reusable templates.
- `prompts/`: reusable project prompts and older workflow prompts.
- `docs/`: setup notes for tooling and workflow maintenance.

## Daily Loop

1. Read `PROJECTS.md`, the relevant prior `focus_<problem>.md`, then the
   relevant graph under `Projects/graphs/` and only the linked problem anchor,
   experiment result, paper note, or sync note needed for the current problem.
2. State the current judgment, strongest rival, evidence that would change the
   judgment, and one next decision. `Unknown` is valid.
3. If exploration is needed, generate at most three distinct candidates,
   select one, and park the rest before further work.
4. Perform only the derivation, reading, diagnostic, or approved experiment
   needed to close the advancement point.
5. After eligible evidence and the researcher's result judgment exist, create
   `daily_research_reports/MMDD/docs/daily_report_<topic_slug>.md` from
   the maintained daily-report template. It explains the full experiment and
   knowledge update while linking canonical evidence.
6. After the researcher confirms that report's knowledge wording, condense it
   into `daily_research_reports/MMDD/focus_<problem>.md`. AI verifies evidence,
   drafts the explanation flowchart, and checks that the focus adds nothing not
   present in the confirmed daily report.
7. Update anchors only when evidence changes the route, claim boundary,
   bottleneck, hypothesis status, or next decision.
8. Do not update root sync, package handoff reports, edit graph manifests,
   commit, or push unless explicitly requested.

A day may contain several `focus_<problem>.md` files when several problems reach
bounded answers. If none does, do not invent a conclusion merely to create a
daily file. Legacy bare `focus.md` files remain valid historical artifacts but
are not the naming pattern for new files. Problem focuses do not replace
`PROJECTS.md`, anchors, protocols, or result records.

Reusable templates live in `templates/`. Do not create new reusable templates
inside daily, paper-reading, docs, or project folders by default.

For a meeting, always create a new `focus_meeting_<topic>.md` from
`templates/meeting/meeting_focus_template.md`. For one named problem, proceed
after the human states the core question. For multiple independent problems,
require exact source paths, exclusions, and one core question before merging.
The meeting file answers that question progressively and does not overwrite
source focuses. Create a separate speaking outline only when explicitly
requested after the meeting focus is complete.

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

After the anchor is stable, use `experiment-card-writer` to write the complete
candidate directly into `protocol.md` as `DRAFT_NOT_EXECUTABLE`. AI then
surfaces only decision-critical parts for review and updates the same file.
Promote it only after every block is confirmed and consistency passes:

```text
Projects/<project>/main_specialization/problem_anchors/<anchor_id>.md
Projects/<project>/main/problem_anchors/<anchor_id>.md
Projects/<project>/main/experiments/A<anchor_id>/<experiment_id>/protocol.md
Projects/<project>/main/experiments/A<anchor_id>/<experiment_id>/summary.md
Projects/<project>/main/experiments/A<anchor_id>/<experiment_id>/detailed.md
daily_research_reports/MMDD/docs/daily_report_<topic_slug>.md
daily_research_reports/MMDD/focus_<problem>.md
```

The experiment-local `summary.md` and `detailed.md` remain the canonical result
and evidence records. The `daily_report` is the complete reader-friendly
explanation derived from them. Only after the researcher confirms its knowledge
update is it condensed into the one-problem focus. The focus keeps only the
question, concise update, one decisive result, boundary, next decision, and
report link; it must not introduce new evidence or strengthen the daily report.

Default principle: fewer, sharper experiments. Each experiment should deepen
understanding, test a hypothesis, or change a next decision.
Nontrivial experiments should stop at the promoted `protocol.md` until the
user explicitly approves the requested scope: implementation, smoke, or full
run. Approval of one scope does not authorize the next.

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

# Codex Research System

This repository manages research judgment and process, not the remote
experiment codebase.

## Language And Response

- Default conversation language: Chinese.
- Start with the conclusion, then give only the reason, claim boundary, and
  next decision needed for the current question.
- Canonical research artifacts are English unless the user explicitly chooses
  another language. Chinese companions use `_cn.md`.
- An independent Thinking Card and the human-owned daily focus may preserve the
  user's Chinese mechanism judgment.
- Define technical terms in plain Chinese before reusing English names or
  abbreviations in conversation.
- Treat user ideas as hypotheses to audit. Point out undefined objects, hidden
  assumptions, rival explanations, metric mismatch, causal overclaim, and
  missing boundary conditions.
- Separate direct result, observation, interpretation, claim, speculation,
  boundary, and next decision.
- When the user asks for a number or run status, return the measured result
  first. Do not delay it for document cleanup.

## Start Here

For research work:

1. Read `PROJECTS.md`.
2. Read `daily_research_reports/MMDD/focus.md` for today's human idea, focus,
   and resume point when it exists.
3. Identify the active project and worker surface.
4. Read the graph named in `PROJECTS.md`.
5. Read only the linked anchor, story, protocol, result, meeting note, paper
   note, or raw material needed for the question.
6. Decide whether the work changes an anchor, claim boundary, graph, sync
   surface, or next decision before writing a long response.

Do not use chat history as the main research memory.

## Human-AI Research Cycle

The human owns the initial judgment and final approval. AI retrieves, audits,
formalizes, checks, and edits.

```text
daily focus: human advancement point + current idea
-> AI focus audit
-> existing anchor work, or human Thinking Card for a new formal question
-> human correction / approval when a Thinking Card is needed
-> formal anchor when a new question is promoted
-> approved protocol
-> execution and evidence record
-> human closed-book summary
-> AI evidence and boundary audit
-> canonical research artifact update when needed
-> daily focus closure
```

Before AI writes a formal anchor or prepares a meeting outline, the human
should state:

```text
phenomenon
mechanism guess
strongest rival explanation
most uncertain point
evidence that would change the judgment
current next decision
```

`Unknown` is valid. AI may propose candidate definitions, priors, metrics, and
counterexamples, but must label them and must not silently invent the user's
judgment.

After a research cycle, the human first writes from memory:

```text
question
direct result
confirmed belief
weakened or rejected belief
current mechanism and reason
cannot-claim boundary
exactly one next decision
```

AI then verifies sources and wording without strengthening the claim.

## Focus And Writing

Do not keep a research question in permanent divergence. One divergent round
may propose at most three genuinely different candidates unless the user asks
for a wider survey. Then choose one to pursue and park the rest before
generating more possibilities.

Every substantial work session must have exactly one advancement point:

```text
By the end of this session, I will make [one object or relation] clear enough
to decide [one decision], by writing [one human-owned output], with completion
defined as [one inspectable criterion].
```

Reading, coding, running, plotting, and discussion are activities, not
advancement points. They count only when they clarify or reject a judgment,
freeze a definition, change a claim boundary, or enable the stated decision.

Each research day keeps exactly one retained focus file:

```text
daily_research_reports/MMDD/focus.md
```

Create it from `templates/research_process/focus_writing_template.md`. The
title is the exact research question at the center of that day, never a generic
date or `Daily Focus` label. Under it, the researcher lists the few core
questions that must be answered in the group meeting. They are subquestions of
one advancement point, not parallel research directions. The researcher writes
the four-sentence central judgment and one direct answer for each question. AI
identifies only the most blocking ambiguity, asks one question, waits for the
answer, maps answers to existing or missing experiments, and asks the
researcher to revise in place. AI must not write the answers for the
researcher.

The title, core-question list, and shared completion standard together define
the single advancement point; do not add a separate activity checklist.

The daily focus file owns the human's daily idea, progress, and resume point.
It does not own project truth. If evidence changes a hypothesis, boundary, or
next decision, update the relevant anchor, result record, protocol, story, or
`PROJECTS.md` as well.

## State Ownership

| Surface | Owns |
|---|---|
| `AGENTS.md` | stable repository behavior and hard boundaries |
| `PROJECTS.md` | project map, active routes, project-level boundaries and decisions |
| `daily_research_reports/MMDD/focus.md` | one day's human idea, core meeting questions, question-by-question closure, routine speaking outline, and resume action |
| `Projects/graphs/` | thin navigation between questions, claims, evidence, and tasks |
| Thinking Card | human's initial mechanism judgment and uncertainty |
| anchor | one adjudicable research design and its current boundary |
| story | line-level mathematical and evidence synthesis |
| `protocol.md` | approved test contract |
| `summary.md` | first result reading path |
| `detailed.md` | complete evidence ledger and artifact map |
| root `sync/` | explicitly published external-reading surface |

If a project-state statement here conflicts with `PROJECTS.md`, move the state
out of this file and treat `PROJECTS.md` as current.

## Thinking Card And Anchor

New Thinking Card names are subject-bearing and collision-safe:

```text
<anchor_stem>_thinking_card.md
<anchor_stem>_thinking_card_cn.md
```

The card is independent and human-owned. The formal anchor links it and does
not duplicate it as section 0.

Default anchor paths:

```text
Projects/<project>/main/problem_anchors/<line>/<anchor_id>_<topic>_anchor.md
Projects/<project>/main/problem_anchors/<line>/<anchor_id>_<topic>/
  <anchor_id>_<topic>_anchor.md
  subanchors/<anchor_id>_<NN>_<topic>_anchor.md
```

A parent anchor owns one complete major problem. A subanchor inherits the
parent question and adjudicates one local clause, rival, robustness check, or
metric guard. Do not mix flat and nested layouts inside one active line without
an explicit migration that updates indexes and references.

Formal anchors use sections 1-8:

```text
1. Problem Definition
2. Physical Priors
3. Falsifiable Hypotheses
4. Mathematical Model
5. Computational Realization
6. Minimal Falsification Tests
7. Current Evidence
8. Claim Boundary And Next Decision
```

Each anchor has one decision question, one core model, one primary metric, one
main falsifier, pass/fail/insufficient meanings, a conservative boundary, and
exactly one next decision. Commands, full configs, raw logs, and broad sweeps
belong outside anchors.

After evidence exists, update the same anchor. Do not create a separate
`hypotheses/`, closure-report, or routine `final_report.md` layer.

## Story

Stories live under:

```text
Projects/<project>/main/stories/<line>/README.md
Projects/<project>/main/stories/<line>/<NN>_<topic>.md
Projects/<project>/main/stories/<line>/<NN>_<topic>_cn.md
```

The line README orders story pairs and marks exactly one current primary
synthesis. English and Chinese companions must agree on theorem state,
evidence verdict, boundary, and next decision. Stories link to anchors and
results; they do not replace or strengthen them. Historical snapshots use
subject-bearing names under `archive/<snapshot_id>/`.

## Experiment Chain

Default chain:

```text
anchor -> protocol.md -> summary.md -> detailed.md -> anchor update
```

- Do not implement or run a nontrivial experiment before `protocol.md` is
  approved.
- `protocol.md` owns question alignment, conditions, primary metric,
  pass/fail/insufficient rules, guards, approval state, and execution contract.
- `summary.md` is conclusion-first: what is established, what the primary
  metric shows, boundary, central figures, and next decision.
- `detailed.md` owns the complete setup, seeds, commands, job IDs, full tables,
  stage evidence, failures, artifact map, and visualization audit.
- Add conditions, seeds, and diagnostics only when they separate a named rival
  or protect the primary conclusion.
- Every central plot needs a contract: question, metric and unit, data source,
  aggregation, axes/legend, allowed conclusion, and limitation. Audit the
  rendered artifact before delivery.
- Important figures live locally beside the result documents and are embedded,
  not merely listed by path.

Before pursuing a tangent, apply:

```text
affects hypothesis? yes/no/unclear
affects claim boundary? yes/no/unclear
affects next decision? yes/no/unclear
recommendation: pursue / park / ignore
```

## Meeting Preparation

For a routine meeting around one daily research center, the completed
`daily_research_reports/MMDD/focus.md` is the default speaking outline. Do not
create another meeting document that repeats its questions, answers, or
evidence mapping.

Use `templates/meeting/meeting_outline_template.md` only when the meeting
combines several daily foci or research lines, or when the user explicitly asks
for a separate meeting outline. It is still human-completed, not a finished
brief. AI may propose speaking logic, identify unclear points, and map each
conclusion to an existing or missing experiment. The researcher writes the
actual explanation; AI audits evidence, boundaries, and order afterward.

Present every completed experiment as one loop:

```text
question -> decisive experiment -> direct result -> conclusion
-> cannot-claim boundary -> next decision
```

Do not stack derivations, formulas, complete tables, or run timelines in the
speaking path. Keep them in anchors and result records. Do not create a
separate final brief unless the researcher explicitly requests it after
completing the outline.

## Explicit Publication And Sync

Default behavior updates only project-local sources and today's
`daily_research_reports/MMDD/focus.md`.

These actions require an explicit user request:

```text
edit an existing graph
publish root sync or a full mirror
sync to a collaborator repo
package a handoff
commit
push
```

Project-local anchors remain the source of truth. When a root anchor mirror is
explicitly requested, generate it with:

```text
python skills/research-mainline/scripts/publish_anchor_mirror.py
```

The publisher copies the complete anchor tree and rewrites links that leave the
tree to repository-root absolute paths so the published mirror remains
clickable. Do not hand-edit generated mirror files; update the source and
republish. Update the root-sync README, line summary, and index in the same
explicit publication task.

External collaborator sync is a separate curated package. Check the target
repo status first; do not overwrite dirty collaborator files. Copy only the
approved anchor, protocol, summary, detailed record, and referenced figures or
tables. Exclude private notes, raw logs, checkpoints, datasets, full result
directories, and unrelated anchors. Commit or push only when explicitly asked.

## Graph

Graphs are thin navigation; Markdown artifacts remain the reasoning source.
Use only these node roles when possible: question, claim, concept, method,
evidence, source, task, output. Link nodes to concrete source files and keep
summaries to current previews.

Before changing an existing graph, obtain confirmation unless the current user
request explicitly authorizes that edit. When asked to display a graph, use the
local Sidecar app through `sidecar-thinking`; do not substitute a custom graph.

## Terminology And Formula Rules

Define every non-obvious term, abbreviation, metric, condition, method label,
run label, and plot label before using it as evidence. A metric definition must
state its concrete computation, unit/formula, decision role, and what it cannot
prove.

Use `$...$` for inline formulas and `$$...$$` for display formulas.

## Repository And Execution Boundary

Keep the root focused on:

```text
AGENTS.md  PROJECTS.md  README.md
Projects/  sync/  templates/  prompts/  skills/
paper_reading/  papers/  daily_research_reports/  docs/
```

Root `templates/` is the only maintained reusable-template location.

Local `Research_System` owns research-process artifacts and curated evidence.
Remote/container workspaces own experiment code, debugging, runs, raw outputs,
checkpoints, logs, result generation, and cluster submissions. Use Git as the
normal synchronization path. SSH/SCP is only for explicit small inspection,
recovery, or port forwarding.

Do not promote raw outputs, checkpoints, datasets, or unfiltered logs into the
research mainline.

## Local Skills

Use repository skills when the task matches:

- `research-progress-core`: research logic and uncertainty reduction.
- `problem-anchor-writer`: Thinking Card audit and anchor construction.
- `experiment-card-writer`: protocol, summary, and detailed records.
- `meeting-outline-writer`: AI-supported, human-completed advisor outline.
- `research-mainline`: project organization and explicit publication.
- `research-graph-sop`: thin graph maintenance.
- `handoff-report-writer`: explicit curated handoff packaging.
- `remote-experiment-workflow`: remote execution and artifact maps.
- `sidecar-thinking`: local graph display.
- `scholar-mode`: unstable research intuition and literature framing.

Detailed templates and validation checklists live in those skills, not here.

## Git

Never revert user changes. Commit or push only when explicitly requested.
When committing, prefer one lightweight daily commit:

```text
MMDD: mainline update - <one sentence conclusion>
MMDD: daily note - no mainline update
```

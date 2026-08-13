# Codex Research System

This repository manages research judgment and process, not the remote
experiment codebase.

## Language And Response

- Default conversation language: Chinese.
- Start with the conclusion, then give only the reason, claim boundary, and
  next decision needed for the current question.
- Canonical research artifacts are English unless the user explicitly chooses
  another language. Chinese companions use `_cn.md`.
- An independent Thinking Card and human-owned problem or meeting focus may
  preserve the user's Chinese mechanism judgment.
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
2. Read only the relevant `daily_research_reports/MMDD/focus_<problem>.md`, or
   the human-selected source focuses named by a meeting focus, when they exist.
3. Identify the active project and worker surface.
4. Read the graph named in `PROJECTS.md`.
5. Read only the linked anchor, story, protocol, result, meeting note, paper
   note, or raw material needed for the question.
6. Decide whether the work changes an anchor, claim boundary, graph, sync
   surface, or next decision before writing a long response.

Do not use chat history as the main research memory.

## Human-AI Research Cycle

The human owns the research judgment and approval. AI retrieves evidence,
audits logic, formalizes approved work, executes, and maintains technical
records.

```text
one-page problem knowledge update
-> AI identifies one blocking issue
-> approved protocol only when an experiment is needed
-> execution
-> AI writes the evidence record
-> human states the result and boundary from memory
-> AI verifies
-> human states the resulting knowledge update
-> AI writes the reader-friendly daily report from the verified record and
   human judgment
-> human confirms or corrects that daily report
-> update only the smallest owning artifact and, when the problem is bounded,
   condense the confirmed daily report into its problem focus
```

Before formalizing a new question, the human states:

```text
current judgment
reason or mechanism
strongest rival or uncertainty
evidence that would change the judgment
next decision
```

`Unknown` is valid. AI may propose candidate definitions, priors, metrics, and
counterexamples, but must label them and must not silently invent the user's
judgment.

After execution, the human first states:

```text
question
direct result
updated judgment
cannot claim
next decision
```

AI verifies numbers, evidence, and wording without strengthening the claim.

## Focus And Writing

Daily writing has one full explanatory report followed by two focus forms.

### Daily Research Report

For every completed experiment or bounded evidence synthesis that changes a
research judgment, claim boundary, or next decision and is delivered in the
daily report, create:

```text
daily_research_reports/MMDD/docs/daily_report_<topic_slug>.md
```

Use `templates/research_process/daily_report_template.md`. This file is the
complete, reader-friendly, self-contained explanation of the day's result and
knowledge update. A reader should understand the question, objects,
hypotheses, decisive comparison, metrics, direct result, inference, boundary,
and next decision without chat history. Self-contained means sufficient for
understanding and judgment; it does not mean copying the complete run ledger.

The project-local `summary.md` and `detailed.md` remain the canonical result
and evidence sources. Every decision-bearing number and figure in the daily
report must trace to those records. The daily report must preserve material
negative results, uncertainty, deviations, and failed assumptions; it must not
reframe `Fail` or `Insufficient` as progress language. Before the researcher
confirms the knowledge wording, mark it
`AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`. Only a confirmed daily report may be
the source of a completed problem focus.

### Problem Knowledge Update

When one problem reaches a bounded answer, create:

```text
daily_research_reports/MMDD/focus_<problem_slug>.md
```

The file is a short, human-owned **summary and navigation card** condensed from
one confirmed daily report, not a second experiment report. A day may contain
several problem focus files when several problems reach bounded answers. If no
problem reaches a bounded answer, or the source daily report is not
human-confirmed, do not manufacture a focus conclusion. Legacy bare `focus.md`
files may remain; do not create new ones or bulk-rename them without an explicit
migration.

Keep the focus normally within 20--30 lines. It contains only:

1. exactly one concrete answered problem;
2. a two-to-four-sentence human-confirmed knowledge update;
3. one sentence giving the decisive comparison and direct result;
4. the cannot-claim boundary and exactly one next decision;
5. one prominent link to the complete daily report.

Do not repeat setup, terminology tables, formulas, full metrics, multiple
results, figures, flowcharts, provenance tables, completion criteria, or resume
instructions in the focus. Those belong to the daily report. A focus may repeat
one number only when the knowledge update would otherwise be ambiguous.

The researcher writes or explicitly approves the core question, knowledge
update, mechanism, claim boundary, and next decision. AI may prefill the source
link and verify the one decisive result. AI must not infer a stronger conclusion
from experimental results. A focus must name its source daily report first and
must not introduce a result, interpretation, boundary, or next decision absent
from that confirmed source. Corrections flow only from canonical evidence to
the daily report and then to the focus.

### Meeting Knowledge Synthesis

For every meeting synthesis, create a new file:

```text
daily_research_reports/MMDD/focus_meeting_<topic_slug>.md
```

A one-problem meeting uses the lightweight path when the researcher names the
problem, note, or problem focus and states the meeting's core question. A
multi-problem meeting starts as `AWAITING_HUMAN_SCOPE` until the researcher
provides the exact source focus paths, exclusions, and core question. AI must
not infer a multi-problem merge range or introduce a joint judgment that no
selected source owns.

The meeting focus follows the same knowledge-update principle as a problem
focus, but answers one core question through two to four progressive
subquestions. Each direct answer gives only the minimum evidence, its reach,
and why the next question is necessary. Do not require a merge table, evidence
ledger, flowchart, or speaking script. Add a visual only when it materially
clarifies a decisive relation. If AI drafts unconfirmed knowledge wording, keep
`AI_DRAFT_AWAITING_HUMAN_CONFIRMATION` visible. A separate speaking outline is
created only when explicitly requested after the meeting focus is complete.

Use at most three genuinely different candidates in one divergent round, then
choose one and park the rest. Reading, coding, running, and plotting count as
progress only when they change a judgment, boundary, or decision.

## State Ownership

| Surface | Owns |
|---|---|
| `AGENTS.md` | stable repository behavior and hard boundaries |
| `PROJECTS.md` | project map, active routes, project-level boundaries and decisions |
| `daily_research_reports/MMDD/docs/daily_report_<topic_slug>.md` | full reader-friendly experiment or evidence report, verified knowledge update, boundary, and one next decision; derived from canonical evidence |
| `daily_research_reports/MMDD/focus_<problem>.md` | minimal summary and navigation card: one answered problem, concise knowledge update, one decisive result, boundary, and one next decision |
| `daily_research_reports/MMDD/focus_meeting_<topic>.md` | one meeting's concise progressive knowledge update from a named problem or a human-scoped multi-problem set |
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

Canonical anchor paths:

```text
Projects/<project>/main/problem_anchors/<line>/README.md
Projects/<project>/main/problem_anchors/<line>/<parent_id>_<topic>/
  <parent_id>_<topic>_anchor.md
  <parent_id>_<topic>_anchor_cn.md
  <parent_id>_<topic>_thinking_card.md
  <parent_id>_<topic>_thinking_card_cn.md
  subanchors/
    <parent_id>_<NN>_<topic>_anchor.md
    <parent_id>_<NN>_<topic>_anchor_cn.md
    <parent_id>_<NN>_<topic>_thinking_card.md
    <parent_id>_<NN>_<topic>_thinking_card_cn.md
```

A research line may contain several sibling parent anchors, and every parent
anchor receives its own `<parent_id>_<topic>/` folder. Dependency or reading
order between parent anchors does not make one a subanchor of another.
`subanchors/` contains only children that inherit that folder's parent decision
question and adjudicate one local clause, rival, repair, robustness check, or
metric guard. Parent anchor files and their Thinking Cards stay together in the
parent folder; child Thinking Cards stay beside their child anchors in
`subanchors/`. The line `README.md` indexes sibling parents, dependency order,
current boundary, and one next decision.

Legacy flat layouts may remain until an explicit migration. New or reorganized
multi-parent lines must use the canonical folder-per-parent layout. A migration
must move rather than copy the source files, update all indexes and references,
remove the old path, and verify that no duplicate canonical version or broken
local link remains.

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

Canonical experiment chain:

```text
anchor -> protocol.md -> summary.md -> detailed.md -> anchor update
```

Daily reading chain after eligible evidence and human judgment:

```text
summary.md + detailed.md + anchor update
-> daily_report_<topic_slug>.md
-> focus_<problem>.md
```

- Use `experiment-card-writer` to write the complete candidate directly into
  `protocol.md` as `DRAFT_NOT_EXECUTABLE`, then surface only decision-critical
  parts for review. Update that same file after corrections; do not create a
  chat-only or second planning draft.
- Promote the Protocol only after every block is explicitly confirmed and
  cross-block consistency passes. Do not implement or run before the promoted
  `protocol.md` records explicit approval for the requested execution scope.
- `protocol.md` owns question alignment, conditions, primary metric,
  pass/fail/insufficient rules, guards, approval state, and execution contract.
- `summary.md` is conclusion-first: what is established, what the primary
  metric shows, boundary, central evidence, any decision-relevant figures, and
  next decision.
- `detailed.md` owns the complete setup, seeds, commands, job IDs, full tables,
  stage evidence, failures, artifact map, and visualization audit when figures
  are decision-relevant.
- The daily report owns the complete reader explanation, not canonical
  evidence. It must link the exact Anchor, Protocol, Summary, and Detailed
  records, explain every central metric and figure in plain language, preserve
  the registered verdict and boundary exactly, and contain exactly one next
  decision.
- Create the problem focus only by compressing a human-confirmed daily report.
  The focus keeps only the question, concise update, one decisive result,
  boundary, one next decision, and report link; it may not add or strengthen
  content.
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

Always create a new `focus_meeting_<topic>.md` from
`templates/meeting/meeting_focus_template.md`. For one named problem, proceed
once the researcher has stated the core question. For multiple independent
problems, require the exact human-selected merge scope and exclusions before
synthesis. In both cases, organize the meeting as a concise progressive answer
to one question, not an experiment correction or source-by-source audit.

Use `templates/meeting/meeting_outline_template.md` only when the user
explicitly asks for a separate speaking outline after the meeting focus is
complete.

Present every completed experiment as one loop:

```text
question -> key comparison -> direct result -> conclusion
-> cannot claim -> decision
```

Keep formulas, complete tables, and run timelines in anchors and result
records.

## Explicit Publication And Sync

Default behavior updates only project-local sources, the applicable
reader-friendly daily report, and the problem or meeting focus files under
`daily_research_reports/MMDD/`.

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
python .agents/skills/research-mainline/scripts/publish_anchor_mirror.py
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
Projects/  sync/  templates/  prompts/  .agents/
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

Repository skills live in `.agents/skills/` and are discovered directly by
Codex. Do not maintain personal-directory copies of these repository skills.

Use repository skills when the task matches:

- `research-progress-core`: research logic and uncertainty reduction.
- `problem-anchor-writer`: Thinking Card audit and anchor construction.
- `experiment-card-writer`: blockwise experiment audit, confirmed protocol,
  summary, and detailed records.
- `research-story-writer`: line-level mathematical and evidence synthesis.
- `meeting-outline-writer`: human-scoped meeting focus and optional speaking outline.
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

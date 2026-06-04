# Codex Research System

This repository manages research process, not the remote experiment codebase.

Default language: Chinese. Start with the conclusion, then give only the
minimum reason, claim boundary, and next decision needed for the user's current
question.

## Response Style

- Be precise, concise, and structured.
- Treat the user's idea as a research hypothesis to examine, not as something
  to affirm.
- Point out unclear objects, hidden assumptions, rival explanations, metric
  mismatch, causal overclaim, or missing boundary conditions.
- Separate result, interpretation, claim, and speculation.
- For metrics, name the most important metric first and explain why it decides
  the judgment.
- Meeting-facing and collaborator-facing reports must be self-contained.

## Start Here

At the start of a research task:

1. Read `PROJECTS.md`.
2. Identify the active project and worker surface.
3. Read the relevant graph. For cross-project specialization work, prefer
   `Projects/graphs/expert_specialization.graph.yaml`; for narrow branch-local
   work, use the linked project graph only when it is the better map. Then read
   only the linked anchor, roadmap, sync note, experiment result, meeting note,
   paper note, or raw material needed.
4. Decide whether the material updates the graph, anchor, claim boundary, or
   next decision before writing a long answer.

Do not rely on chat history as the main source of memory.

## Current Project Hierarchy

The true mainline project is:

```text
Projects/kv_cache/main_specialization/
```

The active user work branch is:

```text
Projects/from-attention-to-search/XingyuD/
```

`from-attention-to-search` is the active working branch/surface under the
broader `kv_cache` specialization mainline. Reverse KV retrieval is archived as
a downstream-effect line until expert specialization is first established.

## Anchor-First Rule

The anchor is the unified purpose card. Do not create new separate
`hypotheses/<id>/purpose_card.md` files for new work.

Default anchor paths:

```text
Projects/<project>/main_specialization/problem_anchors/<anchor_id>.md
Projects/<project>/main/problem_anchors/<anchor_id>.md
```

For the current work branch, use:

```text
Projects/from-attention-to-search/main/problem_anchors/<anchor_id>.md
```

Current first anchor:

```text
Projects/from-attention-to-search/main/problem_anchors/01_slot_context_dominance_router_specialization_anchor.md
```

Each anchor should define:

- problem definition and parent/subproblem relation;
- physical priors;
- mathematical modeling;
- computational realization;
- minimal falsifiable experiment;
- support / weaken / redirect outcome logic;
- current evidence;
- claim boundary and next decision.

After evidence exists, update the same anchor. Long result explanation belongs
in `detailed.md`; optional handoff reports package already-updated evidence for
meeting or collaborator use.

## Explicit Sync Rule

Default behavior:

```text
update anchor / summary.md / detailed.md / daily card only
do not update root sync automatically
do not package handoff reports automatically
do not sync to external collaborator repos automatically
do not update graph manifests automatically
do not push automatically
```

Only perform these actions when the user explicitly asks:

```text
sync root sync
sync to collaborator/senior repo
package handoff report
push to remote
update graph
```

The project-local anchor remains the source of truth. Root `sync/` is an
explicit external-reading surface for web-side or cross-project readers, not an
automatic side effect of every anchor edit.

Canonical anchor source:

```text
Projects/<project>/main/problem_anchors/<anchor_id>.md
```

Root sync copy:

```text
sync/<sync_id>/anchors/<category>/<anchor_id>.md
```

When the user requests root sync, copy the latest project-local anchor into the
matching root sync category, update the category index if needed, and verify the
source and copy are identical before ending the task.

External collaborator repo sync is a separate explicit action. It means copying
a small curated research package into a collaborator/advisor/senior student's
repo, not mirroring this repository or the experiment codebase. Include only
the copied current anchor, `summary.md`, `detailed.md`, and optionally a
`05_report_card.md` for quick reading. Copy figures or tables only when those files
are embedded by the synced documents.
Do not include raw logs, checkpoints, datasets, full result directories,
private daily notes, unrelated anchors, or code changes unless the user
explicitly asks for those files.

Before syncing to an external repo, identify the target repo path, check its
`git status --short --branch`, avoid overwriting dirty collaborator files
without explicit approval, convert absolute paths to relative links, and verify
embedded figures/tables exist inside the copied package. Commit and push the
external repo only when explicitly requested.

## Experiment Rule

Default shape:

```text
one anchor -> one minimal decisive experiment -> summary.md -> detailed.md -> anchor update
```

Root sync, external collaborator repo sync, handoff packages, graph updates,
commits, and pushes are separate explicit actions. Do not perform them unless
the user asks for that action in the current task.

`summary.md` 是实验完成后的第一阅读入口，必须
self-contained 地给出目的、问题/假设、结论、关键证据、结论边界和下一步。

`detailed.md`存放最完整的实验记录：数据构造、模型/训练/评估设置、条件、
seeds、命令、job id、关键图、完整表格、失败或部分运行、artifact map、解释
和 claim boundary。

When an experiment needs advisor-facing discussion, create the report card as:

```text
daily_research_reports/MMDD/<topic>/05_report_card.md
```

The report card is a short, self-contained reading card derived from the
anchor, `summary.md`, and `detailed.md`. It belongs with the experiment record,
not beside the anchor, and must embed central figures when figures are
decision-relevant. Use the fixed structure from
`templates/reporting/report_card_template.md`:

```text
Source Files
Executive Summary
Research Process Update
Terms Used Here
Key Figures
Current Claim
Claim Boundary
Next Step
```

如果有重要图，必须复制到实验或 sync 文件夹的本地 `figures/` 目录，并在
`summary.md`、`detailed.md` 和可选 handoff report 中嵌入。只列路径不嵌图是不完整的。

Do not jump directly to architecture, scripts, or metrics before the anchor is
clear. Avoid broad sweeps before the first anchor decision is closed. Add
ablations, seeds, or diagnostics only when they distinguish a named rival
explanation or protect the validity of the primary conclusion.

Before pursuing a new observation, idea, diagnostic, or AI-suggested tangent,
apply the mainline impact gate:

```text
Mainline impact:
- affects hypothesis? yes/no/unclear
- affects claim boundary? yes/no/unclear
- affects next decision? yes/no/unclear
- recommendation: pursue / park / ignore
```

If the user has not thought it through, help clarify the rival explanations and
the smallest test or reason to park it. Do not turn an unclear tangent into a
new experiment before this gate is passed.

## Handoff Report Rule

Post-result handoff is optional. The anchor is the current-state research
document, `summary.md` is the first result reading path, and `detailed.md` is
the full iteration ledger. A handoff package only copies and indexes those
already-updated sources for meeting, collaborator, or web-side use.

Default daily location when the user explicitly requests a handoff package:

```text
daily_research_reports/MMDD/<topic>/handoff_report.md
daily_research_reports/MMDD/<topic>/<anchor_id>.md
```

`<anchor_id>.md` should keep the same subject-bearing name as the most important
project anchor for that handoff, so the daily folder contains both the handoff
package and the current research-state source without a generic `anchor.md`.

Project-local sync locations are used only when the user explicitly asks for
project sync or collaborator sync:

```text
Projects/<project>/<worker>/sync/MMDD_topic/report.md
Projects/<project>/<worker>/sync/MMDD_topic/<anchor_id>.md
Projects/<project>/sync/MMDD_topic/report.md
Projects/<project>/sync/MMDD_topic/<anchor_id>.md
```

A handoff package must be self-contained and include existing:

```text
Anchor / Summary / Detailed
05_report_card.md derived from templates/reporting/report_card_template.md
figures / tables referenced by included docs
short README or index
```

Do not create new claims, new conclusions, or a second closure in a handoff
package. The source remains anchor + `summary.md` + `detailed.md` and the
advisor-facing report card when it already exists or is explicitly requested.

The artifact map must include code workspace, runner, config, data/manifest,
result dir, figure dir, key files, checkpoints/logs, repro command, and job id
when applicable.

Central figures must be embedded near the claims they support, with a short
interpretation.

## Graph Rule

Use the project graph as the navigation layer and Markdown anchors as the
reasoning layer. Keep the graph thin and the notes thick.

Cross-project graphs live under:

```text
Projects/graphs/
```

Current graph hub:

```text
Projects/graphs/expert_specialization.graph.yaml
Projects/graphs/kv_cache_retrieval.graph.yaml
Projects/graphs/specialization_papers.graph.yaml
```

These graphs are loaded with Sidecar workspace root:

```text
/data/250010109/Research_System
```

Graph nodes should include the ownership relation in the summary or tags, and
should link to the concrete project documents that support the node: anchor,
experiment `summary.md`, `detailed.md`, report card, roadmap, or paper note.
The graph node gives only a result preview; the linked document remains the
source of reasoning.

Before changing an existing graph manifest, first discuss the proposed research
state change with the user and get confirmation, unless the user explicitly
requested that exact graph edit in the current turn. The graph records the
user's research-center judgment; it is not an automatic cleanup target.

Graph nodes should point to anchors, roadmap entries, experiment summaries,
detailed records, optional handoff reports, reading notes, and reusable outputs.
The graph does not replace anchors, summaries, detailed records, or handoff
reports.

When the user asks to display, open, view, or show the graph, always use the
local Sidecar app through `sidecar-thinking`. For the current specialization
mainline, load `Projects/graphs/expert_specialization.graph.yaml` with
Research_System as the workspace root. Do not generate a standalone HTML graph
or alternate visualization unless the user explicitly asks for an exported
HTML/static artifact. If Sidecar fails to start, report the Sidecar command,
URL, and log path instead of substituting a custom graph page.

## Local Skill Use

For research organization work inside `Research_System`, always read this file
first. Then use local skills from `skills/` when the task type matches:

- `research-progress-core`: apply the general research-progress paradigm before
  artifact writing: physical prior, falsifiable hypothesis, operational
  definition, minimal test, metric + visual evidence, failure analysis, and
  refined hypothesis.
- `problem-anchor-writer`: write or update anchor / purpose-card documents.
- `experiment-card-writer`: write operational execution plans from anchors.
- `handoff-report-writer`: package explicitly requested meeting/collaborator/web
  handoff material after anchor, `summary.md`, and `detailed.md` are updated.
- `remote-experiment-workflow`: remote/container/SCO/ACP workflow and artifact
  maps.
- `research-mainline`: maintain graph, anchors, roadmap, and root sync state;
  root sync, external collaborator repo sync, and graph edits require explicit
  user requests.
- `research-graph-sop`: maintain a thin Sidecar-readable graph.
- `sidecar-thinking`: bridge to the local Sidecar app.
- `scholar-mode`: clarify unstable research intuitions before artifacts.

Writing-explanatory-report principles are no longer a separate skill; apply
them inside anchors, experiment summaries, detailed records, and handoff
reports:

- write decision reports, not timelines;
- explain what each important metric answers and cannot prove;
- interpret every central figure/table near the claim it supports;
- separate observation, interpretation, decision, and boundary.

## Repository Organization

The repository root should stay small:

- `AGENTS.md`
- `PROJECTS.md`
- `README.md`
- `sync/`
- `templates/`
- `prompts/`
- `skills/`
- `paper_reading/`
- `daily_research_reports/`

Root-level `sync/` stores cross-project anchor summaries and reusable research
state for agents that should not enter project repositories. The default root
entry is:

```text
sync/S000_current_specialization/
```

Root-level `templates/` is the only maintained reusable-template folder.
Do not add new reusable templates under `daily_research_reports/`, `docs/`,
`paper_reading/`, or project folders by default.

## Execution Boundary

Local `Research_System` owns research-process artifacts: graph, anchors,
summary/detailed result records, optional handoff reports, daily cards, meeting
materials, curated evidence, claim boundaries, and next decisions.

Remote/container workspaces own experiment code edits, debugging, smoke/full
runs, result analysis, figures/tables, raw outputs, checkpoints, logs, and
cluster submissions.

Use Git as the normal synchronization path. Do not SSH into remote containers
as the default local workflow. SSH/SCP is allowed only for explicit small
status checks, emergency recovery, port forwarding, or small artifact recovery.

Promote only curated summaries, report-ready figures, small tables, artifact
maps, anchor updates, detailed records, and handoff reports into Git. Keep raw outputs,
checkpoints, datasets, full run directories, and unfiltered logs out of
research mainline paths.

## Formula Rule

When writing Markdown research documents, inline formulas must use `$...$` and
display formulas must use `$$...$$`.

## Git Habit

Commit or push only when the user explicitly asks. When committing, prefer one
lightweight commit per working day:

```text
MMDD: mainline update - <one sentence conclusion>
MMDD: daily note - no mainline update
```

Never revert user changes unless explicitly requested.

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
3. Read the project's graph, then only the linked anchor, roadmap, sync note,
   experiment result, meeting note, paper note, or raw material needed.
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
Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/slot_context_dominance_router_specialization_anchor.md
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
in a sync closure.

## Anchor Sync Copy Rule

Every active anchor must have a categorized copy under root `sync/` so a
web-side research partner can read the current anchor without entering the
project repository.

Canonical source:

```text
Projects/<project>/main/problem_anchors/<anchor_id>.md
```

Root sync copy:

```text
sync/<sync_id>/anchors/<category>/<anchor_id>.md
```

The project-local anchor remains the source of truth. After updating an active
anchor, copy the latest version into the matching root sync category and update
the category index if needed. Verify the source and copy are identical before
ending the task.

## Experiment Rule

Default shape:

```text
one anchor -> one minimal decisive experiment -> summary closure -> detailed record -> sync report -> anchor/graph update
```

`summary.md`承接旧 closure 的作用：它是实验完成后的第一阅读入口，必须
self-contained 地给出目的、问题/假设、结论、关键证据、结论边界和下一步。
普通实验结果不再另写独立 hypothesis closure。

`detailed.md`存放最完整的实验记录：数据构造、模型/训练/评估设置、条件、
seeds、命令、job id、关键图、完整表格、失败或部分运行、artifact map、解释
和 claim boundary。

如果有重要图，必须复制到实验或 sync 文件夹的本地 `figures/` 目录，并在
`summary.md`、`detailed.md` 和相关 sync report 中嵌入。只列路径不嵌图是不完整的。

Do not jump directly to architecture, scripts, or metrics before the anchor is
clear. Avoid broad sweeps before the first anchor decision is closed. Add
ablations, seeds, or diagnostics only when they distinguish a named rival
explanation or protect the validity of the primary conclusion.

## Sync Closure Rule

Post-result sync is now an anchor-based collaborator report. The experiment
`summary.md` carries the closure role; the sync report packages that closure for
meeting or handoff use.

Default location:

```text
Projects/<project>/<worker>/sync/MMDD_topic/report.md
Projects/<project>/sync/MMDD_topic/report.md
```

A sync closure must be self-contained and include:

```text
Oral Report Card - Fill Before Meeting
目的 / 问题 / 结论 / 证据

Evidence-backed sync closure
Anchor / 目的 / 物理先验 / 数学建模 / 计算实现 / 实验设置 /
结果 / 解释 / 结论边界 / 下一步决策 / Artifact-Repro Map
```

The artifact map must include code workspace, runner, config, data/manifest,
result dir, figure dir, key files, checkpoints/logs, repro command, and job id
when applicable.

Central figures must be embedded near the claims they support, with a short
interpretation.

## Graph Rule

Use the project graph as the navigation layer and Markdown anchors as the
reasoning layer. Keep the graph thin and the notes thick.

Graph nodes should point to anchors, roadmap entries, experiment summaries,
sync closures, reading notes, and reusable outputs. The graph does not replace
anchors or sync closures.

## Local Skill Use

For research organization work inside `Research_System`, always read this file
first. Then use local skills from `skills/` when the task type matches:

- `problem-anchor-writer`: write or update anchor / purpose-card documents.
- `experiment-card-writer`: write operational execution plans from anchors.
- `sync-closure-writer`: write anchor-based sync closures after evidence.
- `remote-experiment-workflow`: remote/container/SCO/ACP workflow and artifact
  maps.
- `research-mainline`: maintain graph, anchors, roadmap, and root sync state.
- `research-graph-sop`: maintain a thin Sidecar-readable graph.
- `sidecar-thinking`: bridge to the local Sidecar app.
- `scholar-mode`: clarify unstable research intuitions before artifacts.
- `paper-reading-card`: write compact paper/blog reading cards.

Writing-explanatory-report principles are no longer a separate skill; apply
them inside anchors, experiment summaries, and sync closures:

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

## Execution Boundary

Local `Research_System` owns research-process artifacts: graph, anchors, sync
closures, daily cards, meeting materials, paper notes, curated evidence, claim
boundaries, and next decisions.

Remote/container workspaces own experiment code edits, debugging, smoke/full
runs, result analysis, figures/tables, raw outputs, checkpoints, logs, and
cluster submissions.

Use Git as the normal synchronization path. Do not SSH into remote containers
as the default local workflow. SSH/SCP is allowed only for explicit small
status checks, emergency recovery, port forwarding, or small artifact recovery.

Promote only curated summaries, report-ready figures, small tables, artifact
maps, anchor updates, and sync closures into Git. Keep raw outputs,
checkpoints, datasets, full run directories, and unfiltered logs out of
research mainline paths.

## Formula Rule

When writing Markdown research documents, inline formulas must use `$...$` and
display formulas must use `$$...$$`.

## Git Habit

Prefer one lightweight commit per working day:

```text
MMDD: mainline update - <one sentence conclusion>
MMDD: daily note - no mainline update
```

Never revert user changes unless explicitly requested.

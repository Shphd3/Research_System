---
name: research-system-remote-workflow
description: Use when organizing Research_System daily workflow, project mainline cleanup, active/archive experiment structure, collaborator sync, group-meeting reports, closure-document templates, or deciding whether experiment work belongs in local review, a remote container, or SCO/ACP.
---

# Research System Remote Workflow

## Core Boundary

Treat this local repository as the research-process system, not the default
experiment code workspace.

Local `Research_System` owns research mainlines, hypotheses, closures, graph
maps, daily cards, sync notes, meeting reports, curated results, claim
boundaries, and next decisions.

Remote Codex/container workspaces own experiment code edits, debug runs, smoke
runs, full runs, result analysis, report-ready figures/tables, datasets, raw
outputs, checkpoints, logs, and cluster submissions.

Cluster/SCO/ACP owns formal or long training jobs.

Do not make the local Windows agent SSH into a remote container as the default
experiment workflow. If the agent is already running inside the target remote
container, edit, run, analyze, commit, and push there. If the agent is running
locally, use local work for research-process edits, review, Git pulls, and only
small explicit smoke tests.

Use Git as the normal synchronization path between local and remote. Keep SSH or
SCP as an explicit ad hoc utility for small status checks, quick table copies,
or emergency recovery, not as the standard development loop.

Smoke tests may run either locally or in a remote container when they are small,
explicit, and useful. Full experiments and cluster submissions should run from
the remote container or cluster workflow.

## Daily Research Chain

Maintain one chain per active experiment:

```text
purpose -> hypothesis -> execution -> result -> interpretation -> hypothesis update -> sync/report
```

Before execution, update:

```text
Projects/<project>/main/hypotheses/<hypothesis_id>/purpose_card.md
Projects/<project>/main/experiments/<experiment_id>/execution_plan.md
```

After results, update:

```text
Projects/<project>/main/experiments/<experiment_id>/summary.md
Projects/<project>/main/experiments/<experiment_id>/detailed.md
Projects/<project>/main/hypotheses/<hypothesis_id>/purpose_card.md
Projects/<project>/main/hypotheses/<hypothesis_id>/hypothesis_closure.md
```

Update these only when the project-level judgment changes:

```text
Projects/<project>/main/current_mainline.md
Projects/<project>/main/status.md
Projects/<project>/main/roadmap.md
Projects/<project>/main/consensus.md
Projects/<project>/graph.yaml
```

Use `daily_research_reports/MMDD/` for process notes, group-meeting transcript
digests, daily cards, workflow reflections, and meeting preparation. Do not put
global workflow notes into project `docs/`.

## Active Versus Archive

Keep `Projects/<project>/main/` narrow. Active folders should answer the current
proposition or the next gate.

Archive older, superseded, weakly related, or supporting experiments under:

```text
Projects/<project>/main/experiments/archive/
Projects/<project>/main/hypotheses/archive/
```

Keep an archive index with the archived item, why it is archived, when to
consult it again, and which current node supersedes it.

Do not delete evidence unless the user explicitly asks.

## Execution Location Rule

When the user asks to modify experiment code, run experiments, inspect logs, or
submit SCO jobs:

1. Read or confirm the local purpose card / execution plan first.
2. Determine the current execution context when it matters:
   - `hostname`
   - `pwd`
   - `nvidia-smi`
   - `git status --short --branch`
   - `which sco` or `/root/.sco/bin/sco`
3. If already in the remote container, work directly in that checkout: edit,
   smoke, run, analyze, commit, and push curated code/docs.
4. If local on Windows, do not SSH by default. Pull/review via Git, update
   research-process artifacts, or run only small explicit smoke tests.
5. Use `remote-sco-collaboration` only when the user explicitly asks to connect
   by SSH, inspect a remote session, start/check CCI, copy a small artifact, or
   manage remote access.
6. Use `experiment-acp-runner` when submitting jobs from the remote/container
   workflow.
7. Submit SCO only after the command, config, output dir, and pass/fail metric
   are explicit.
8. Record job id, command, log path, result path, and first diagnosis in a
   project-local sync or experiment summary.

Promote only curated conclusions and report-ready figures back into
`Research_System`.

## Experiment Sync Loop

For experiments that require code edits, GPU execution, or SCO/ACP execution,
use this order:

```text
1. local: write or confirm purpose_card.md and execution_plan.md
2. remote/container: pull latest before editing code or configs
3. remote/container: edit, smoke, run, analyze, and create report-ready figures/tables
4. remote/container or cluster: submit SCO/ACP when needed and record job id, command, log path, result path
5. remote/container: write the result summary, sync note, or closure draft with artifact map
6. remote/container: commit and push curated code/docs/results needed for reproducibility
7. local: pull the pushed changes, then update mainline, graph, and meeting docs
```

Remote commit allowed:

- code changes, configs, launch scripts, runbooks;
- small curated tables or report-ready figures;
- `summary.md`, `detailed.md`, closure drafts, sync reports;
- artifact maps with code workspace, runner, config, data manifest, result dir,
  figure dir, logs/checkpoints path, repro command, and job id.

Remote commit forbidden unless explicitly curated:

- raw logs;
- checkpoints;
- datasets;
- full run directories;
- unfiltered generated figures or tables;
- temporary cache files.

The local workspace should not become a manual copy target for remote artifacts.
After remote push, local work starts from `git pull` and focuses on research
judgment: mainline update, claim boundary, graph links, daily/meeting reports,
and collaborator-facing sync.

## Skill Responsibility Map

Use this skill as the workflow gatekeeper only. It decides where work belongs
and which artifact should be updated.

- `research-system-remote-workflow`: local/remote/cluster boundary, daily
  workflow, active/archive cleanup, closure/sync/report shape.
- `remote-sco-collaboration`: explicit SSH session, host selection, CCI checks,
  preflight, port forwarding, small ad hoc remote artifact access.
- `experiment-acp-runner`: concrete ACP/SCO command construction, dry-run,
  submission, monitoring, and run summary.
- `experiment-card-writer`: pre-run hypothesis purpose card and execution plan.
- `hypothesis-closure`: post-run closure from evidence.
- `writing-explanatory-reports`: long `detailed.md` / result-analysis writing.

Do not duplicate these roles inside one artifact. When two skills appear to
apply, use this skill first to choose the artifact boundary, then call the
specialized skill.

## Closure Document Shape

A closure document should have a short user-fill section first, followed by the
evidence-backed closure. The top section is for the researcher to prepare oral
language before a meeting; the lower section is the auditable record.

Use this shape:

```markdown
# <Hypothesis ID> Closure

## Oral Report Card - Fill Before Meeting

目的：

假设：

结论：

证据：

## 1. 目的

## 2. 假设

## 3. 数学建模

## 4. 实验设置

## 5. 结果

## 6. 解释

## 7. 结论边界

## 8. 下一步决策

## 9. Artifact / Repro Map
code workspace:
runner:
config:
data / manifest:
result dir:
figure dir:
key files:
checkpoints / logs:
repro command:
```

Only the oral card should be blank or first-person. The evidence-backed
sections must cite experiment summaries, figures, configs, code paths, and
remote run artifacts when available.

## Collaborator Sync As Trajectory

Create collaborator-facing sync under:

```text
Projects/<project>/<worker>/sync/MMDD_topic/
```

Use one primary sync folder per date for each worker. If a day has multiple
experiments, versions, audits, or diagnostics, put those reports in subfolders
under the date's primary sync. Do not create several competing same-date sync
entry points.

Sync is not just one closure copied somewhere else. It should connect several
closures or experiment stages into a readable research trajectory for
collaborators.

Each sync must be self-contained and project-local:

```markdown
## 0. Closure-Style Daily Summary
Today's judgment:
Strongest hypothesis update:
Key evidence:
Claim boundary:
Next decision:

## 1. 目的
## 2. 假设
## 3. 数学建模
## 4. 实验设置
## 5. 结论
## 6. 证据
## 7. 结论边界
## 8. 下一步决策
## 9. Artifact / Repro Map
```

The first section should read like a concise closure summary that the user can
adapt as their own meeting summary. Put detailed setup, tables, figure-by-figure
discussion, and repro links after that front judgment.

The artifact map must include code workspace, runner, config, data or manifest,
result dir, figure dir, key files, checkpoints or logs, and repro command.

Do not cite root-level `daily_research_reports/` from project sync. Integrate
the needed content into the sync itself.

## Group Meeting Report

Group-meeting reports belong under:

```text
daily_research_reports/MMDD/meeting/
daily_research_reports/MMDD/meeting/prism/
```

Build them from the project-local sync and mainline, not from chat history.
Keep the report self-contained: question, motivation, hypothesis, setup, key
result, interpretation, claim boundary, next decision, and artifact map.

---
name: research-system-remote-workflow
description: Use when organizing Research_System daily workflow, project mainline cleanup, active/archive experiment structure, collaborator sync, group-meeting reports, closure-document templates, or when coding/training/SCO work should happen on a remote container, usually 10109, instead of the local research-process repository.
---

# Research System Remote Workflow

## Core Boundary

Treat this local repository as the research-process system, not the experiment
code workspace.

Local `Research_System` owns research mainlines, hypotheses, closures, graph
maps, daily cards, sync notes, meeting reports, curated results, claim
boundaries, and next decisions.

Remote containers / SCO own code edits, training scripts, debug runs, datasets,
raw outputs, checkpoints, logs, and SCO submissions.

There are multiple usable containers. Default to `10109` because it is the
user's usual active container, but accept another container if the user names
one or the remote host registry indicates a better target.

Do not edit local experiment code or launch local training when the user asks
for actual code implementation, remote execution, or SCO submission. Use
`remote-sco-collaboration` first, then `experiment-acp-runner` when submitting
jobs.

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

## Remote Coding And SCO Rule

When the user asks to modify experiment code, run experiments, inspect logs, or
submit SCO jobs:

1. Read the local purpose card / execution plan first.
2. Use `remote-sco-collaboration`.
3. Select host `10109` by default unless the user names another active machine.
4. SSH to the remote container and run preflight:
   - `hostname`
   - `pwd`
   - `nvidia-smi`
   - `git status --short --branch`
   - `which sco` or `/root/.sco/bin/sco`
5. Modify code only in the remote project workspace.
6. Run a smoke/debug path before a full run.
7. Submit SCO only after the command, config, output dir, and pass/fail metric
   are explicit.
8. Record job id, command, log path, result path, and first diagnosis in a
   project-local sync or experiment summary.

Promote only curated conclusions and report-ready figures back into
`Research_System`.

## Skill Responsibility Map

Use this skill as the workflow gatekeeper only. It decides where work belongs
and which artifact should be updated.

- `research-system-remote-workflow`: local/remote boundary, daily workflow,
  active/archive cleanup, closure/sync/report shape.
- `remote-sco-collaboration`: SSH session, host selection, preflight, port
  forwarding, remote handoff note.
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

Sync is not just one closure copied somewhere else. It should connect several
closures or experiment stages into a readable research trajectory for
collaborators.

Each sync must be self-contained and project-local:

```markdown
## 0. Reading Path
This sync connects:
- closure / experiment A:
- closure / experiment B:
- current next decision:

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

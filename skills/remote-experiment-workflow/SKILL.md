---
name: remote-experiment-workflow
description: Use when deciding or executing the remote/container/SCO/ACP workflow for experiments: local-vs-remote boundary, SSH/CCI preflight, cluster submission, monitoring, artifact maps, and curated sync updates.
metadata:
  short-description: Remote experiment workflow
---

# Remote Experiment Workflow

Use this skill for the whole remote experiment loop. It replaces the old split
between local workflow, remote session, and ACP runner skills.

Core rule:

```text
anchor -> protocol_for_approval.md -> execution plan
-> remote/container smoke or run -> curated result
-> summary/detailed -> anchor update
```

Root sync, handoff reports, graph edits, commits, and pushes are explicit
follow-up actions only. External collaborator repo sync is also explicit. Do
not perform any of these unless the user asks.

Local `Research_System` owns graph, anchors, summary/detailed result records,
optional handoff reports, daily cards, meeting material, claim boundaries, and next decisions. Remote/container
workspaces own code edits, debug runs, full runs, result analysis, figures,
tables, raw outputs, checkpoints, and logs.

## Before Any Run

Read:

1. `PROJECTS.md`;
2. active project `graph.yaml`;
3. relevant anchor under the project mainline's `problem_anchors/` directory,
   or the project anchor folder named by the user;
4. the execution plan or runbook named by the user;
5. the experiment workspace `AGENTS.md`, if present.

Do not start from scripts or metrics before the anchor states the decision
question and the primary metric.

## Local / Remote Boundary

- If Codex is already inside the target remote/container, work there directly:
  edit, smoke, run, analyze, and write curated docs. Commit and push only when
  the user explicitly asks.
- If Codex is local, do not SSH by default. Use local work for research-process
  edits, Git pull/review, and small explicit smoke checks.
- Use SSH/SCP only for explicit small status checks, port forwarding, quick
  artifact recovery, or CCI control.
- Full experiments and formal cluster submissions should run from the
  remote/container or SCO/ACP path.

## Remote / CCI Preflight

If SSH/CCI is explicitly needed, read
`references/remote_hosts.yaml` before choosing a host unless the user gives a
newer target.

Check before editing or submitting:

```bash
hostname
pwd
nvidia-smi
git status --short --branch
which sco || ls /root/.sco/bin/sco
ps -eo pid,lstart,etime,cmd | grep -E '[s]leep 4h|setup_env'
```

Do not overwrite remote work. Pull only after checking the working tree.

For reusable local helpers, use:

```powershell
powershell -ExecutionPolicy Bypass -File skills/remote-experiment-workflow/scripts/remote_sco_session.ps1 -HostKey h100-2gpu-10109 -Action print
```

## SCO / ACP Submission

Submission is a substep, not a separate research workflow.

Before submission, make explicit:

- code workspace;
- runner or launch script;
- config;
- data or manifest;
- output directory;
- GPU count / quota / image;
- smoke command;
- full command;
- primary pass/fail metric;
- expected artifacts.

For ACP/SCO jobs, record:

```text
job id:
command:
config:
log path:
result dir:
first diagnosis:
```

Always run a smoke/debug path before a formal long run when possible.

## Curated Artifacts

When the user explicitly asks for a commit, it may include:

- code changes, configs, launch scripts, runbooks;
- small curated tables or report-ready figures;
- experiment `summary.md` / `detailed.md`;
- anchor updates;
- root sync anchor copies, only when root sync was explicitly requested;
- handoff report drafts, only when handoff was explicitly requested;
- external collaborator repo sync packages, only when that external sync was
  explicitly requested;
- artifact maps.

Do not commit raw logs, checkpoints, datasets, full run directories,
unfiltered generated figures/tables, or temporary cache files unless the user
explicitly curates them.

When syncing to a senior student's or collaborator's external repo, do not copy
the experiment workspace or codebase by default. Copy only the curated package:
copied current anchor, `summary.md`, `detailed.md`, optional `05_report_card.md`,
and figures/tables only when referenced by those synced documents.

## Handoff

After results exist, first write or update the curated experiment documents:

```text
Projects/<project>/main/experiments/<experiment_id>/summary.md
Projects/<project>/main/experiments/<experiment_id>/detailed.md
```

`detailed.md` must start with:

```markdown
## 0. Quick Recap

目的：

假设：

实验思路：

结论：

证据：
```

Then update the relevant anchor if the result changes the physical prior,
mathematical model, computational realization, claim boundary, or next decision.
Do not copy the updated anchor to root sync unless the user explicitly requests
root sync.

Finally, package a handoff only if the user explicitly requests one. The default
daily handoff location is:

```text
daily_research_reports/MMDD/<topic>/handoff_report.md
daily_research_reports/MMDD/<topic>/<anchor_id>.md
```

Project-local sync is used only if the user explicitly requests project or
collaborator sync:

```text
Projects/<project>/<worker>/sync/MMDD_topic/report.md
Projects/<project>/<worker>/sync/MMDD_topic/<anchor_id>.md
```

If the need is advisor discussion, first fill the shared report card and save
it in the experiment folder:

```text
daily_research_reports/MMDD/<topic>/05_report_card.md
```

Use `daily_research_reports/_templates/report_card_template.md` as the source
template. The handoff package may include the existing filled report card, but
should not define a separate report-card structure or create new research
content.
The filename is always `05_report_card.md` in daily or sync packages.

It must include a compact artifact / repro map:

```text
code workspace:
runner:
config:
key code files:
data / manifest:
result dir:
figure dir:
key files:
checkpoints / logs:
repro command:
job id:
```

## Report Writing Standard

All curated reports and optional handoff reports must be decision reports, not timelines.
They should separate:

- observation;
- interpretation;
- decision;
- claim boundary.

Every central metric must say what question it answers, what failure mode it
catches, and what it cannot prove. Every central figure must have a nearby
one-sentence interpretation.

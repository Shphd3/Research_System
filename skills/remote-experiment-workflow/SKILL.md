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
anchor -> execution plan -> remote/container smoke or run -> curated result
-> summary/detailed -> anchor update -> root anchor copy -> optional handoff report
```

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
  edit, smoke, run, analyze, write curated docs, commit, and push.
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

Remote commit may include:

- code changes, configs, launch scripts, runbooks;
- small curated tables or report-ready figures;
- experiment `summary.md` / `detailed.md`;
- anchor updates;
- root sync anchor copies;
- optional handoff report drafts;
- artifact maps.

Do not commit raw logs, checkpoints, datasets, full run directories,
unfiltered generated figures/tables, or temporary cache files unless the user
explicitly curates them.

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
Copy the updated anchor to the root sync category when the project uses root
anchor copies.

Finally, write or update a project-local handoff report only if a meeting,
collaborator, or web-side reader needs a self-contained package:

```text
Projects/<project>/<worker>/sync/MMDD_topic/report.md
```

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

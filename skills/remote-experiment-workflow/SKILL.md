---
name: remote-experiment-workflow
description: Use when deciding or executing the remote/container/SCO/ACP workflow for experiments: local-vs-remote boundary, SSH/CCI preflight, cluster submission, monitoring, artifact maps, and curated sync updates.
metadata:
  short-description: Remote experiment workflow
---

# Remote Experiment Workflow

Use this skill for execution-environment logistics. It does not define the
research question; the anchor and protocol do that.

Core rule:

```text
anchor -> protocol.md -> remote/container smoke or run
-> curated result artifacts -> summary.md / detailed.md -> anchor update
```

Root sync, handoff packages, graph edits, commits, and pushes are explicit
follow-up actions only. External collaborator repo sync is also explicit. Do
not perform any of these unless the user asks.

Local `Research_System` owns graph, anchors, protocols, summary/detailed result
records, daily notes, meeting material, claim boundaries, and next decisions.
Remote/container workspaces own code edits, debug runs, full runs, result
analysis, figures, tables, raw outputs, checkpoints, and logs.

## Before Any Run

Read:

1. `PROJECTS.md`;
2. the relevant graph or roadmap;
3. the active anchor under `problem_anchors/`;
4. `protocol.md` for the experiment;
5. the experiment workspace `AGENTS.md`, if present.

Do not start from scripts or metrics before the anchor states the decision
question and the protocol states the primary metric, conditions, and
success/failure/insufficient-evidence rules.

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
- experiment `protocol.md`, `summary.md`, and `detailed.md`;
- anchor updates;
- root sync anchor copies, only when root sync was explicitly requested;
- handoff packages, only when handoff was explicitly requested;
- external collaborator repo sync packages, only when that external sync was
  explicitly requested;
- artifact maps.

Do not commit raw logs, checkpoints, datasets, full run directories,
unfiltered generated figures/tables, or temporary cache files unless the user
explicitly curates them.

When syncing to a senior student's or collaborator's external repo, do not copy
the experiment workspace or codebase by default. Copy only the curated package:
current anchor, `protocol.md`, `summary.md`, `detailed.md`, and figures/tables
only when referenced by those synced documents.

## Result Writing Boundary

After results exist, first write or update:

```text
Projects/<project>/main/experiments/A<anchor_id>/<experiment_id>/summary.md
Projects/<project>/main/experiments/A<anchor_id>/<experiment_id>/detailed.md
```

`summary.md` must include central visualization explanations for the main
figures. `detailed.md` must include protocol compliance audit, stage evidence,
full visualization results, and artifact map.

Then update the relevant anchor if the result changes the physical prior,
mathematical model, computational realization, claim boundary, or next decision.
Do not copy the updated anchor to root sync unless the user explicitly requests
root sync.

## Handoff

Package a handoff only if the user explicitly requests one. The package should
copy or index existing anchor, `protocol.md`, `summary.md`, `detailed.md`, and
referenced figures/tables.

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

All curated reports and optional handoff packages must be decision reports, not
timelines. They should separate:

- observation;
- interpretation;
- decision;
- claim boundary.

Every central metric must say what question it answers, what failure mode it
catches, and what it cannot prove. Every central figure must explain purpose,
setup, how to read, observed result, take-home, and remaining uncertainty.

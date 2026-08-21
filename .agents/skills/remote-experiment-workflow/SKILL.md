---
name: remote-experiment-workflow
description: "Plan and execute research experiment logistics across local containers, SSH, CCI, SCO, and ACP, including preflight, submission, monitoring, logs, and artifact maps. Use when the user asks to run, inspect, or manage remote or cluster experiments. Do not design the research hypothesis; pair with sco-control for SCO platform resource commands."
---

# Remote Experiment Workflow

Use this skill for execution-environment logistics. It does not define the
research question; the anchor and protocol do that.

Use `sco-control` for SCO platform-specific resource, image, storage, cluster,
and job commands; use this skill to connect those operations to the approved
research protocol and evidence chain.

If the active project provides a narrower transport skill, such as
`kv-cache-remote-collaboration` for a server that Codex cannot access directly,
use that project skill for the transport loop. Keep this skill responsible for
the Research_System protocol, run, evidence, and artifact-map chain.

Core rule:

```text
anchor -> protocol.md -> remote/container smoke or run
-> curated result artifacts -> summary.md / detailed.md -> anchor update
```

Root sync, graph edits, commits, and pushes are explicit follow-up actions
only. Handoff packages and external collaborator repo sync are explicit-only
work owned by `handoff-report-writer`; do not perform them through this skill.

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

Before implementation, smoke, or full run, verify that the Protocol records
all audit blocks as confirmed, cross-block consistency as passed, and explicit
approval for the requested execution scope. Approval for one scope does not
authorize a later scope.

## Local / Remote Boundary

- If Codex is already inside the target remote/container, work there directly
  within the approved execution scope: edit, smoke, run, analyze, and write
  curated docs. Commit and push only when the user explicitly asks.
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

When smoke scope is approved, run a smoke/debug path before a formal long run
when possible. Do not treat smoke approval as full-run approval.

## Curated Artifacts

When the user explicitly asks for a commit, it may include:

- code changes, configs, launch scripts, runbooks;
- small curated tables or report-ready figures;
- experiment `protocol.md`, `summary.md`, and `detailed.md`;
- anchor updates;
- root sync anchor copies, only when root sync was explicitly requested;
- artifact-map inputs for a separately requested handoff or external sync;
  `handoff-report-writer` owns package assembly and copying;
- artifact maps.

Do not commit raw logs, checkpoints, datasets, full run directories,
unfiltered generated figures/tables, or temporary cache files unless the user
explicitly curates them.

When `handoff-report-writer` handles a separately requested external sync, its
inputs from this skill are limited to the current anchor, `protocol.md`,
`summary.md`, `detailed.md`, referenced figures or tables, and the verified
artifact map. The experiment workspace and codebase are not package inputs by
default.

## Result Writing Boundary

After results exist, first write or update:

```text
Projects/<project>/main/experiments/A<line_number>/<anchor_stem>/<experiment_id>/summary.md
Projects/<project>/main/experiments/A<line_number>/<anchor_stem>/<experiment_id>/detailed.md
```

`summary.md` must explain any central decision-relevant figures.
`detailed.md` must include protocol compliance audit, stage evidence, and the
artifact map; include full visualization results only when visual evidence is
decision-relevant.

Then update the relevant anchor if the result changes the physical prior,
mathematical model, computational realization, claim boundary, or next decision.
Do not copy the updated anchor to root sync unless the user explicitly requests
root sync.

## Handoff Routing

If the user explicitly requests a handoff or external collaborator sync,
switch to `handoff-report-writer`. This skill contributes the verified run and
artifact map; it does not assemble, copy, or synchronize the package.

Provide this compact artifact / repro map to the handoff workflow:

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

All curated reports, and all report inputs passed to a handoff workflow, must
be decision records rather than timelines. They should separate:

- observation;
- interpretation;
- decision;
- claim boundary.

Every central metric must say what question it answers, what failure mode it
catches, and what it cannot prove. Every central figure must explain purpose,
setup, how to read, observed result, take-home, and remaining uncertainty.

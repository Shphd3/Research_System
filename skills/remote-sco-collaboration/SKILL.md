---
name: remote-sco-collaboration
description: Use when Codex explicitly needs an SSH/CCI/SCO remote-access layer: connecting to a named remote machine, checking or starting a GPU container, inspecting remote status/logs, forwarding ports, copying small artifacts, or preparing a cluster handoff.
---

# Remote SCO Collaboration

Use this skill only for the remote session layer. It is not the default
experiment workflow.

If Codex is already running inside the target remote/container, do not SSH
again. Work directly in that checkout, then commit and push curated code/docs.
If Codex is running locally and the task can be handled by Git pull/review or
research-process edits, do not SSH. Keep SSH/SCP for explicit small status
checks, quick table copies, port forwarding, CCI control, or emergency recovery.

Use `experiment-acp-runner` after the remote workspace and target experiment
plan are clear.

## Local / Remote Boundary

Treat local `Research_System` as the research-process repository. It owns
mainlines, hypotheses, closures, graph maps, daily cards, sync notes, meeting
reports, curated results, claim boundaries, and next decisions.

Remote Codex/container workspaces own experiment code edits, debug runs, smoke
runs, full runs, result analysis, report-ready figures/tables, datasets, raw
outputs, checkpoints, logs, and cluster submissions.

Local Windows may run small explicit smoke tests when useful. Full experiments
and formal cluster jobs should run from the remote/container or SCO/ACP
workflow.

When the user asks to modify experiment code or run experiments from a local
Windows conversation, first decide whether the right action is to switch to a
remote Codex/container conversation or to sync via Git. Use this skill only when
the user explicitly asks for SSH/CCI/SCO remote access or a small ad hoc remote
copy/status action.

Promote only curated conclusions and report-ready figures back into
`Research_System`.

## Required References

Read `references/remote_hosts.yaml` before choosing or connecting to a remote
machine. Treat it as the canonical host list unless the user gives a newer SSH
config.

Use `scripts/remote_sco_session.ps1` when a reusable local command helps. It can
print SSH commands, run remote preflight checks, or start a port forward from
the host registry.

## Entry Mode And CCI Selection

Before SSH or starting CCI, establish the entry mode:

- If the user is working locally and explicitly needs to control a remote CCI,
  use `ssh` to reach an available control container, usually 10109, then run
  SCO commands there.
- If the user is already inside a remote CCI, do not SSH again. Inspect the
  current container with `hostname`, `nvidia-smi`, `which sco`, and the process
  timer commands below.
- If the user is local and only needs the latest curated code/docs, use Git pull
  instead of SSH.

When the task is to check or start a CCI, list the user's CCI apps first:

```bash
/root/.sco/bin/sco cci apps list --workspace-name share-space --keyword 250010109 --page-size 500
```

Default CCI target is `shphd-mig` (`app-p05e0rfj`) unless the user explicitly
asks for the 2GPU Codex container. Treat `shphd-mig` style containers as
mutually exclusive: if any intended MIG CCI is already `RUNNING` or
`PROGRESSING`, do not start another one without asking.

For the usual 4-hour CCI session, SCO does not expose a direct expected-stop
field. If inside the container, infer the stop time from the setup sleep:

```bash
ps -eo pid,lstart,etime,cmd | grep -E '[s]leep 4h|setup_env'
```

The four-hour timer starts when `sleep 4h` begins, not necessarily at CCI
create time.

## Workflow

1. Identify whether Codex is local, already inside a remote/container, or
   explicitly controlling a remote CCI. Ask one concise question if unclear.
2. Identify the target host or CCI from the user's message. If multiple choices
   are plausible, ask for one concise choice; default to `shphd-mig` for normal
   MIG work.
3. State the selected host alias, SSH endpoint, CCI app name, and intended
   session duration when known.
   Default session duration is about four hours.
4. If already inside the target remote/container, skip SSH and run local
   preflight in that environment.
5. If local and SSH is explicitly needed, list CCI state before starting
   anything. Start a suspended CCI only after confirming no mutually exclusive
   MIG CCI is already running or progressing.
6. Connect with SSH only after the user has indicated the active machine or
   explicitly requested the remote action. Use the host alias from the user's
   SSH config when available.
7. On the remote machine, check:
   - `hostname`
   - `pwd`
   - `nvidia-smi`
   - `which sco` or `ls /root/.sco/bin/sco`
   - `ps -eo pid,lstart,etime,cmd | grep -E '[s]leep 4h|setup_env'`
   - project workspace path, usually under `/data/250010109/Research_System`
8. Pull or inspect the relevant project repository only after checking for
   local uncommitted work on the remote.
9. For cluster submission, switch to `experiment-acp-runner`: read the active
   project mainline, hypothesis purpose card, execution plan, experiment
   workspace `AGENTS.md`, and runbook before writing SCO/ACP commands.
10. Start with a smoke/debug job before a formal training run. Smoke may be
   local or remote when small and explicit; full runs should use the
   remote/container or cluster path. Record job id, command, log path, result
   path, and first diagnosis.

## SSH Patterns

Use the configured alias when possible:

```bash
ssh "[2GPU]118.145.32.132[10109]"
ssh "[Mig]118.145.32.132[11109]"
ssh "[MIG-2c]118.145.32.132[12109]"
```

Helper examples:

```powershell
powershell -ExecutionPolicy Bypass -File skills/remote-sco-collaboration/scripts/remote_sco_session.ps1 -HostKey h100-2gpu-10109 -Action print
powershell -ExecutionPolicy Bypass -File skills/remote-sco-collaboration/scripts/remote_sco_session.ps1 -HostKey h100-2gpu-10109 -Action preflight
powershell -ExecutionPolicy Bypass -File skills/remote-sco-collaboration/scripts/remote_sco_session.ps1 -HostKey h100-2gpu-10109 -Action forward -LocalPort 4317
```

For Sidecar or other local web tools running on the remote container, forward a
local port:

```bash
ssh -N -L 4317:127.0.0.1:4317 "<host-alias>"
```

If multiple containers are active, use different local ports:

```bash
ssh -N -L 4318:127.0.0.1:4317 "<host-alias>"
ssh -N -L 4319:127.0.0.1:4317 "<host-alias>"
```

## Session Guardrails

- Do not assume the GPU count from the host name. Confirm with `nvidia-smi`.
- Do not start long training from a local Windows process repo. Use remote
  Codex/container or SCO/ACP.
- Do not start long training immediately after connecting. First verify code,
  data paths, image/env, and a small smoke path.
- Do not overwrite remote work. Run `git status --short --branch` before pull,
  checkout, or cleanup.
- Keep raw logs, checkpoints, and run outputs on the remote/project experiment
  workspace. Only promote curated summaries, figures, and claim updates into
  `main/`, `sync/`, or root `results/`.
- If the session is expected to last about four hours, prefer a short session
  note with start time, host, purpose, active branch, and expected handoff.

## Remote Session Note

When useful, create or update a small project-local note under:

```text
Projects/<project>/<worker>/sync/MMDD_remote_session/
```

Include:

```text
host:
start_time:
expected_duration:
purpose:
project_path:
branch:
gpu_check:
sco_check:
commands_run:
job_ids:
log_paths:
next_handoff:
```

Do not put raw logs into the note. Link paths only.

## Relation To Experiment ACP Runner

This skill stops at remote access, environment checks, and handoff structure.
For actual SCO/ACP job construction, quota/GPU/image rules, dry-run commands,
monitoring commands, and result summaries, use `experiment-acp-runner`.

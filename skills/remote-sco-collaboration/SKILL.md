---
name: remote-sco-collaboration
description: Use when Codex needs to work through a remote SSH container or H100 collaboration machine before running local debugging, remote development, SCO commands, ACP submissions, log inspection, or cluster training for research experiments. Trigger when the user names a remote machine, asks to connect to a GPU container, wants a time-boxed remote session, or wants to bridge local research planning to remote SCO/ACP execution.
---

# Remote SCO Collaboration

Use this skill to bridge local research planning to remote H100 container work.
It handles the remote session layer. Use `experiment-acp-runner` after the
remote workspace and target experiment plan are clear.

## Required References

Read `references/remote_hosts.yaml` before choosing or connecting to a remote
machine. Treat it as the canonical host list unless the user gives a newer SSH
config.

Use `scripts/remote_sco_session.ps1` when a reusable local command helps. It can
print SSH commands, run remote preflight checks, or start a port forward from
the host registry.

## Workflow

1. Identify the target host from the user's message or ask for one concise
   choice if multiple hosts are plausible.
2. State the selected host alias, SSH endpoint, and intended session duration.
   Default session duration is about four hours.
3. Connect with SSH only after the user has indicated the active machine. Use
   the host alias from the user's SSH config when available.
4. On the remote machine, check:
   - `hostname`
   - `pwd`
   - `nvidia-smi`
   - `which sco` or `ls /root/.sco/bin/sco`
   - project workspace path, usually under `/data/250010109/Research_System`
5. Pull or inspect the relevant project repository only after checking for
   local uncommitted work on the remote.
6. For cluster submission, switch to `experiment-acp-runner`: read the active
   project mainline, hypothesis purpose card, execution plan, experiment
   workspace `AGENTS.md`, and runbook before writing SCO/ACP commands.
7. Start with a smoke/debug job before a formal training run. Record job id,
   command, log path, result path, and first diagnosis.

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

# ACP Submit Template Pattern

Use this pattern when generating or modifying a shell template that submits ACP jobs. Keep personal identifiers, access tokens, concrete workspace names, cluster names, storage ids, and project paths outside the template by passing them through environment variables.

## Required Environment

```bash
SCO_WORKSPACE       # workspace name
SCO_AEC2            # AEC2 cluster name, or public when using public cluster flags
CONTAINER_IMAGE_URL # fully qualified image URL
STORAGE_MOUNT       # volume_id[:subdir]:container_path
REMOTE_PROJECT_DIR  # project path inside the mounted storage
SPEC                # worker spec from the cluster's list-workerspec output
```

Common optional environment:

```bash
SCO_PROFILE="${SCO_PROFILE:-}"            # set this explicitly for each account
WORKER_NODES="${WORKER_NODES:-1}"
QUOTA_TYPE="${QUOTA_TYPE:-reserved}"   # reserved or spot
PRIORITY="${PRIORITY:-normal}"         # normal, high, highest
DRY_RUN="${DRY_RUN:-1}"
```

## Task Families

Use task families instead of hard-coding project-specific job names:

- `*-smoke`: one or a few steps, tiny sample counts, external logging disabled.
- `*-pilot`: medium run, periodic save/eval, normal experiment tags.
- `*-full`: long run, same script as pilot with larger step counts.
- `*-diagnostics` or `*-analysis`: no training loop; set checkpoint names and sample/SVD/quant limits.
- `scripts/*` or `*.sh`: custom script path; derive a safe job name from the basename.

## Dispatch Shape

Task dispatch should set only:

- `JOB_NAME`
- `TARGET_SCRIPT`
- optional `ENTRY_ARG`
- extra exported environment variables

Keep command rendering centralized so all tasks share quoting and submission behavior.

```bash
set_target() {
  local job="$1"
  local script="$2"
  local entry_arg="${3:-}"
  JOB_NAME="${JOB_NAME:-${job}}"
  TARGET_SCRIPT="${TARGET_SCRIPT:-${script}}"
  ENTRY_ARG="${ENTRY_ARG:-${entry_arg}}"
}

add_export() {
  EXTRA_EXPORTS+=("$1=$2")
}
```

## ACP Submission

Use [acp_submit_template.sh](acp_submit_template.sh) to build the remote command with shell-quoted arguments and pass it as `--command`. The template passes `SCO_PROFILE` as the CLI's `--profile` when set. For multiple accounts, use a separate `sco.<account>.local.env` file for each profile. This filename pattern is ignored by Git.

## Dry Run

From a repository checkout, copy the example to an ignored local file and fill in the resource values for this account. Initialize credentials separately with `sco init`.

```bash
cp skills/sco-control-training/references/sco.local.env.example ./sco.local.env
```

Preview from a subshell to keep the account's settings local to this command.

```bash
(
  source ./sco.local.env
  DRY_RUN=1 bash skills/sco-control-training/references/acp_submit_template.sh smoke
)
```

The preview prints the full argument list without invoking `sco`. Check the profile, target resources and remote command. Set `DRY_RUN=0` on the template invocation only when submitting an authorized job.

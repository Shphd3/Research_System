---
name: sco-control-training
description: Prepare and inspect SenseCore ACP training, including multi-node RTX 5090 Socket tuning, H100 RDMA validation, multi-account jobs and AFS or AOSS storage.
---

# SCO Control Training

Use this skill to operate `sco` pragmatically from shell templates and known command patterns. Prefer the embedded patterns below before reading references. Load reference files only when the user asks for a less common flag, a YAML example, or a precise command variant.

Use the RTX 5090 recipe for that topology, the distributed ACP guide for cross-job rendezvous and RDMA checks, and the AOSS guide for storage operations.

- [RTX 5090 training recipe](references/rtx5090-training-cn.md)
- [Distributed ACP jobs](references/acp-distributed-cn.md)
- [AOSS mounts and AFS comparisons](references/aoss-storage-cn.md)

## Operating Rules

- Treat query/inspect as the default first step: list resources, describe the target, then run mutating commands only when intent is explicit.
- For destructive operations (`delete`, quota/ACL updates, stop running jobs/apps), show the exact command and ask unless the user already explicitly requested execution.
- Prefer `-o json` or `-o yaml` when a command supports it and the next step needs parsing.
- Do not assume a single-user workspace. ACP `jobs list` can return other users' jobs; filter client-side by the runtime user id or by job display-name patterns.
- Initialize credentials with `sco init` and keep them in the local SCO profile. Store non-secret deployment settings separately using the [local environment example](references/sco.local.env.example).
- In controlled/sandboxed environments, build commands and files first; skip live `sco` tests unless the user asks.

## Multiple Accounts

- Use an authorized named profile for each identity. Pass `sco --profile "$SCO_PROFILE" ...` to every command in a multi-account workflow. The bundled ACP template takes the same `SCO_PROFILE` variable. Before submitting, verify the target workspace, cluster, quota and storage with that profile. For an existing job, verify its owner by job ID before modifying it. A shared workspace list can include jobs owned by other members.
- For shared training inputs, use a versioned AFS directory and grant read-only access to the participating users or group. Verify that a recipient's actual ACP worker can read a known file and that writes to a disposable test location under the same permissions are denied. See [AEC2 and AFS](references/aec2-afs.md#afs-acl).
- Automatic RDMA provisioning in the tested H100 ACP configuration requires **at least two worker nodes per ACP job** on an RDMA-capable pool. GPU count within one worker does not trigger this provisioning. See [ACP multi-node RDMA](references/acp.md#multi-node-rdma) for the submission and verification steps.
- For one DDP run spanning separately submitted ACP jobs, verify worker reachability to the rendezvous endpoint. Run a small all-reduce with ranks from both jobs and inspect the NCCL logs for the actual cross-job transport. Each rank reads its own batches. For replicated DDP, use the designated writer (usually global rank 0) to save reduced metrics and checkpoints to the owning account's output directory.

## Priority Workflow

1. Establish context:
   ```bash
   sco config profiles list
   sco aec2 clusters list
   sco afs volume list
   sco ccr images list
   ```
2. Query compute capacity:
   ```bash
   sco aec2 clusters list-workerspec --workspace-name "$WORKSPACE" --aec2-name "$AEC2"
   sco aec2 clusters describe --name "$AEC2"
   ```
3. Submit or manage jobs:
   - ACP batch/training jobs: use `sco acp jobs create`, or the shell-template pattern in [run_sco_pattern.md](references/run_sco_pattern.md).
   - For a reusable sanitized ACP submitter, adapt [acp_submit_template.sh](references/acp_submit_template.sh).
   - CCI long-running/debug containers: generate a YAML config and use `sco cci apps create`.
4. Inspect:
   ```bash
   sco acp jobs list --workspace-name "$WORKSPACE" --page-size 10
   sco acp jobs describe --workspace-name "$WORKSPACE" -o json "$JOB_ID"
   sco acp jobs get-workers --workspace-name "$WORKSPACE" "$JOB_ID"
   sco acp jobs stream-logs --workspace-name "$WORKSPACE" "$JOB_ID"
   sco cci apps list --workspace-name "$WORKSPACE"
   sco cci apps describe "$APP" --workspace-name "$WORKSPACE" -o yaml
   ```

## Command Map

ACP jobs, highest priority:
```bash
sco acp jobs create --workspace-name "$WORKSPACE" --aec2-name "$AEC2" --job-name "$JOB" \
  --container-image-url "$IMAGE" --training-framework pytorch --worker-nodes "$NODES" \
  --worker-spec "$SPEC" --priority normal --quota-type reserved --storage-mount "$VOL:/data" \
  --command "$COMMAND"
sco acp jobs list --workspace-name "$WORKSPACE" --page-size 20 -o table
sco acp jobs list --workspace-name "$WORKSPACE" --page-size 100 -o json
sco acp jobs describe --workspace-name "$WORKSPACE" -o json "$JOB_ID"
sco acp jobs get-workers --workspace-name "$WORKSPACE" "$JOB_ID"
sco acp jobs stream-logs --workspace-name "$WORKSPACE" "$JOB_ID" --follow
sco acp jobs exec --workspace-name "$WORKSPACE" --worker-name "$WORKER" "$JOB_ID"
sco acp jobs stop --workspace-name "$WORKSPACE" "$JOB_ID"
sco acp jobs start --workspace-name "$WORKSPACE" "$JOB_ID"
```

If the user gives a user id, use it only as a runtime filter, for example:

```bash
sco acp jobs list --workspace-name "$WORKSPACE" --page-size 100 -o table | awk 'NR<=4 || /'"$USER_ID"'/'
```

CCI apps, highest priority:
```bash
sco cci apps create "$APP" --workspace-name "$WORKSPACE" --config ./cci-app.local.yaml
sco cci apps list --workspace-name "$WORKSPACE" --keyword "$USER_ID" --page-size 20
sco cci apps list --workspace-name "$WORKSPACE" --aec2-name "$AEC2" --state RUNNING
sco cci apps describe "$APP" --workspace-name "$WORKSPACE" -o yaml
sco cci apps update "$APP" --workspace-name "$WORKSPACE" --replicas 1
sco cci apps stop "$APP" --workspace-name "$WORKSPACE"
sco cci apps start "$APP" --workspace-name "$WORKSPACE"
sco cci apps delete "$APP" --workspace-name "$WORKSPACE"
```

CCI `--keyword` fuzzy-matches `user_name`, `display_name`, or `name`, so use the runtime user id only as a query value, not as a skill default.

AEC2 queries:
```bash
sco aec2 clusters list
sco aec2 clusters describe --name "$AEC2"
sco aec2 clusters list-workerspec --workspace-name "$WORKSPACE" --aec2-name "$AEC2"
```

If AEC2 reports `SUBSCRIPTION_NAME_REQUIRED`, rerun with a configured profile or explicit global `--subscription`/`--resource-group` values from the user's environment.

AFS storage:
```bash
sco afs volume list
sco afs volume list -i "$VOLUME_ID"
sco afs volume ls -i "$VOLUME_ID" -d /
sco afs dir-quota list -i "$VOLUME_ID"
sco afs dir-quota create -i "$VOLUME_ID" -d /path --files 100000 --capacity 1024
sco afs dir-quota update -i "$VOLUME_ID" -d /path --files 100000 --capacity 2048
sco afs dir-acl list -i "$VOLUME_ID" -d /path
sco --profile "$OWNER_PROFILE" afs dir-acl create -i "$VOLUME_ID" -d "$INPUT_DIR" -p r -u "$READER_USER_ID"
```

AOSS/CCR images:
```bash
sco ccr images list
sco ccr images list -p
sco ccr namespaces list
sco ccr namespaces get "$NAMESPACE"
sco ccr builds create -n "$NAMESPACE" -f ./Dockerfile -t "$TAG" -c ./context
sco ccr builds list -n "$NAMESPACE"
sco ccr builds log -n "$NAMESPACE" "$BUILD_ID"
sco ccr labels list
sco ccr labels update "$IMAGE_NAME" -n "$NAMESPACE" -c gpu,cpu -p acp,ams
```

## Built-In Defaults From Submit Templates

When the user asks to create or adapt a submission template, preserve this shape unless they override it:

- worker spec from the target pool: `SPEC`
- default worker nodes: `1`
- default image variable: `CONTAINER_IMAGE_URL`
- default storage mount format: `volume_id:/data`
- workspace and AEC2 cluster are environment variables, not hard-coded constants
- command construction: `cd "$REMOTE_PROJECT_DIR"`, export env vars, echo task metadata, then `bash "$TARGET_SCRIPT" "$ENTRY_ARG"`
- preview the full command first. Set `DRY_RUN=0` for authorized submission.

For task-switching guidance, read [run_sco_pattern.md](references/run_sco_pattern.md). For a shell skeleton, use [acp_submit_template.sh](references/acp_submit_template.sh).

## Reference Loading

- Read [acp.md](references/acp.md) for ACP commands, RDMA verification and cross-job DDP rank assignment.
- Read [cci.md](references/cci.md) for CCI YAML structure and container-app management.
- Read [aec2-afs.md](references/aec2-afs.md) for workerspec, cluster lookup, storage mount, quota, and ACL patterns.
- Read [images.md](references/images.md) for CCR/AOSS image listing, builds, namespaces, and labels.
- If vendor SCO docs are available locally, read them only as a last resort for rare flags.

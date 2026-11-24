# ACP Jobs

ACP is the main path for training/batch jobs.

## Create

```bash
sco acp jobs create --workspace-name "$WORKSPACE" --aec2-name "$AEC2" --job-name "$JOB" \
  --priority normal \
  --storage-mount "$VOLUME_ID:/data" \
  --container-image-url "$IMAGE" \
  --training-framework pytorch \
  --worker-nodes "$WORKER_NODES" \
  --worker-spec "$SPEC" \
  --quota-type reserved \
  --command "$COMMAND"
```

Required: `--workspace-name`, `--aec2-name`, `--job-name`, `--container-image-url`, `--training-framework`, `--worker-nodes`, `--worker-spec`, `--command`.

Useful optional flags: `--priority normal|high|highest`, `--storage-mount volume_id[:subdir]:path`, `--env key:value,...`, `--follow`, `--quota-type spot|reserved`, `--enable-fault-tolerance`, `--retry-times`.

Quota type maps to resource class: `reserved` is standard/reserved quota and is the default; `spot` is idle/preemptible quota. Use `--quota-type spot` only when the user explicitly wants idle resources and accepts possible interruption.

For public clusters, `--aec2-name public` also needs `--az` and `--vpc-id`.

## Multi-node RDMA

For the tested H100 ACP configuration, automatic RDMA provisioning is decided per ACP job and requires a multi-node request. On an RDMA-capable pool, set `--worker-nodes 2` or more **on each participating job**. The worker spec controls GPUs per worker. In the tested pool, one worker with two GPUs received no RDMA device, even when two such jobs ran on distinct hosts. Jobs with two workers and one or two GPUs per worker received RDMA devices. Check the provisioning policy if using a different pool or spec.

After submission, use `sco acp jobs get-workers` to confirm placement on distinct physical hosts. Check the job's `rdma/hca` resource request when exposed and verify device visibility in each worker with `ibv_devinfo -l`. For a run spanning multiple jobs, execute a small NCCL all-reduce that crosses job boundaries and inspect the matching channel logs. `NET/IB` and plugins such as `NET/IBext_v8` indicate an RDMA backend. Use the port's link layer to distinguish InfiniBand from RoCE. A `GDRDMA` suffix indicates GPUDirect RDMA on that channel. `NET/Socket` identifies socket transport.

### Launching one DDP run across two ACP jobs

For two jobs with two workers each and the same GPU count per worker, use `TOTAL_NODES=4`. Both jobs' worker indices start at zero. Set `NODE_RANK_OFFSET=0` in the owner job and `NODE_RANK_OFFSET=2` in the other job. The global node ranks are then 0–3. With two GPUs per worker, `GPUS_PER_NODE=2` gives eight GPU ranks.

After placement, get the owner job's first worker address from the platform's worker list and choose a rendezvous port reachable from all four workers. Share the address and port over a channel both jobs are authorized to use, such as job-scoped coordination objects in AOSS. Have each worker wait for those settings before running the project launcher. Use the same run settings on all workers, with the offset chosen per job. ACP's `SENSECORE_PYTORCH_NODE_RANK` supplies the worker index within that job. The ACP template can pass a role or config path to the project launcher via `ENTRY_ARG`. [ACP environment variables](https://www.sensecore.cn/help/docs/cloud-foundation/compute/acp/acpUserGuide/acpEnvironmentVariable)

```bash
node_rank=$((NODE_RANK_OFFSET + SENSECORE_PYTORCH_NODE_RANK))
torchrun --nnodes="$TOTAL_NODES" --nproc-per-node="$GPUS_PER_NODE" \
  --node-rank="$node_rank" --master-addr="$MASTER_ADDR" \
  --master-port="$MASTER_PORT" "$TRAIN_SCRIPT"
```

The launcher and training script belong to the project. Use the same read-only inputs and assign a different shard to each GPU rank. In replicated DDP, the owner's global rank 0 records the reduced metrics and writes checkpoints. The rendezvous port is for process discovery. Verify the data path with the NCCL check above.

## Query And Control

```bash
sco acp jobs list --workspace-name "$WORKSPACE" --page-size 10
sco acp jobs list --workspace-name "$WORKSPACE" --page-size 100 -o json
sco acp jobs describe --workspace-name "$WORKSPACE" -o json "$JOB_ID"
sco acp jobs get-workers --workspace-name "$WORKSPACE" "$JOB_ID"
sco acp jobs stream-logs --workspace-name "$WORKSPACE" "$JOB_ID"
sco acp jobs stream-logs --workspace-name "$WORKSPACE" "$JOB_ID" --worker-name "$WORKER" --follow
sco acp jobs exec --workspace-name "$WORKSPACE" --worker-name "$WORKER" "$JOB_ID"
sco acp jobs stop --workspace-name "$WORKSPACE" "$JOB_ID"
sco acp jobs start --workspace-name "$WORKSPACE" "$JOB_ID"
sco acp jobs delete --workspace-name "$WORKSPACE" "$JOB_ID"
```

Use `describe` to find worker names before `exec` or worker-specific logs.

Some SCO component builds do not accept server-side `--user-name` or `--state` filters for `jobs list`. When a filter is unavailable, list first and filter client-side:

```bash
sco acp jobs list --workspace-name "$WORKSPACE" --page-size 100 -o table | awk 'NR<=4 || /'"$USER_ID"'/'
```

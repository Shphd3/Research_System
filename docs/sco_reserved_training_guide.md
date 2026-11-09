# Reserved training in share and P12

[中文完整操作指南](sco_reserved_training_guide_cn.md)

The account can submit single-node, four-H100 Reserved jobs through either
`share-space` or the P12 workspace. P12 job `pt-mqi6ojfn` finished successfully
on 2026-11-09 Beijing time. Four distinct H100 80GB devices, per-device matrix
multiplication, four-rank NCCL all-reduce, and bidirectional access to the existing
AFS storage passed. This qualifies the infrastructure path; a concrete model
still uses its own training smoke, launcher and resume contract.

Different authorized experiments may use the two workspaces. Submit each main
training task in exactly one selected workspace. A queued job is inspected by
its existing ID rather than duplicated in the other workspace.

## 1. Workspace selection

| Item | share | P12 |
|---|---|---|
| Selector | `share` | `p12` |
| Workspace | `share-space` | `p12-large-model-training-platform-on-domestic-computing` |
| Registered profile | `h100-4-reserved` | `p12-h100-4-reserved` |
| Verified pool | `share-cluster` | `share-cluster` |
| Worker specification | `n6ls.iu.i40.4` | `n6ls.iu.i40.4` |
| Quota type | `reserved` | `reserved` |

Both profiles request one node, four H100 80GB SXM5 devices, 88 vCPUs and
960 GiB host memory. GPU memory and host memory are separate resources.
The [execution envelope](execution_envelope.md) remains the current owner of
resource, image and mount values. The global default remains the share profile;
P12 is explicitly selected.

The workspaces have separate accounting but use the same underlying H100 pools.
The November 8–9 inspection found a four-device/88-vCPU default formal member
quota in share, and a 192-device default Reserved member setting plus a
192-device workspace-wide Reserved cap in P12. P12's two H100 pools share that
cap. It is neither a private personal allocation nor 192 devices per pool.
The P12 smoke request was charged as four devices in P12 while the share formal
group remained at zero devices. Simultaneous four-plus-four execution was not
tested. Reserved requests can still wait for a suitable node.

## 2. Image and existing storage

The current default image key is `shphd-lite-0911`; resolve its URL from the
envelope. The P12 smoke used Python 3.10, PyTorch
`2.3.0a0+6ddf5cf85e.nv24.04` and CUDA 12.4.

Both profiles mount AFS volume `01995892-d478-76d8-aec7-13fd8284477e`
(`afs-share-01g`) at `/data`. The user's files remain at `/data/250010109`.
An explicit mount is required; switching workspace does not require copying
the user's tree to another volume. The remote command explicitly changes to
the task directory.

The smoke verified a locally generated 256 KiB challenge and source hashes
remotely, wrote and fsynced a uniquely tagged response, and verified that response
again from the submitting container. Its four-GPU test ran for about 14.25 seconds.
The final platform state was `SUCCEEDED`.

Evidence root:

```text
/data/250010109/MoE_Router/experiments/20261108_p12_four_gpu_storage_smoke/20261108T155519Z/
```

Read `execution_certificate_completed.json`, `local_verification.json`,
`result.json` and `pod.log`. The earlier `execution_certificate.json` preserves
the initial five-minute startup observation and is not the completed result.

## 3. Submit through the existing template

The selector reuses the canonical resolver, submission gates, durable pod logs
and JSON receipts. It defaults to a dry run and selects exactly one workspace.

```bash
SUBMIT=/data/250010109/Research_System/templates/execution/acp_submit_reserved_workspace.sh
export REMOTE_DIR=/data/250010109/MoE_Router/experiments/YOUR_EXPERIMENT
export REMOTE_CMD='bash scripts/run_authorized_training.sh'
```

Replace the example task path and launcher with the actual authorized task.
The launcher activates its qualified runtime, loads its frozen configuration
and launches training. If it already invokes `torchrun`, do not wrap it in a
second `torchrun`. Two independent workspace jobs are not one eight-GPU job.

Preview share:

```bash
export RESERVED_WORKSPACE=share
export JOB_NAME=YOUR_UNIQUE_SHARE_JOB_NAME
export RUN_ROOT="$REMOTE_DIR/acp_receipts/$JOB_NAME"
bash "$SUBMIT"
```

Preview P12:

```bash
export RESERVED_WORKSPACE=p12
export JOB_NAME=YOUR_UNIQUE_P12_JOB_NAME
export RUN_ROOT="$REMOTE_DIR/acp_receipts/$JOB_NAME"
bash "$SUBMIT"
```

Inspect the printed workspace, profile, node count, specification, Reserved
quota, image and mount. Keep the selected workspace and task variables in the
current shell. For a concrete authorized task whose applicable smoke has passed:

```bash
DRY_RUN=0 \
ALLOW_SUBMIT=1 \
PROTOCOL_APPROVED=1 \
SMOKE_GATE_PASSED=1 \
bash "$SUBMIT"
```

These values assert actual authorization and passed task-specific gates; copying
the example does not create them. Save the returned `pt-...` ID. Receipts and raw
platform output are written under `RUN_ROOT`; durable remote output is written
under `REMOTE_DIR/acp_receipts/pod/`. The selector rejects an existing receipt for
the same job name in that receipt directory. If creation times out or returns an
ambiguous response, inspect the workspace for the unique job name before retrying.

## 4. Inspect either workspace

```bash
TOOL=/data/250010109/MoE_Router/experiments/20261108_p12_four_gpu_storage_smoke/agent_submission_guide/sco_workspace.py
```

Use `--workspace share` or `--workspace p12` with the same ACP commands:

```bash
python "$TOOL" --workspace share jobs list --user-name 250010109 --page-size 20 -o json
python "$TOOL" --workspace share jobs describe -o json YOUR_SHARE_JOB_ID
python "$TOOL" --workspace share jobs get-workers YOUR_SHARE_JOB_ID
python "$TOOL" --workspace share jobs stream-logs YOUR_SHARE_JOB_ID

python "$TOOL" --workspace p12 jobs list --user-name 250010109 --page-size 20 -o json
python "$TOOL" --workspace p12 jobs describe -o json YOUR_P12_JOB_ID
python "$TOOL" --workspace p12 jobs get-workers YOUR_P12_JOB_ID
python "$TOOL" --workspace p12 jobs stream-logs YOUR_P12_JOB_ID
```

The wrapper starts the corrected local workspace compatibility bridge and then
invokes the existing SCO ACP entry point. Credentials stay in the existing local
SCO profile. Both explicit-workspace read paths were checked. Finished pod stdout
may disappear; use the durable AFS log and result. Lists can include other users,
so filter by the account and do not operate on other users' jobs.

## 5. Scheduling and alternative specifications

The successful smoke first produced `FailedScheduling` events. Its requested
four GPUs, 88 vCPUs and 960 GiB host memory had to fit together on one node.
`insufficient nodeSpec quota` for CPU or memory describes node/specification
allocation constraints, not evidence that the account lacks P12 access.
`34000m` represents 34 CPU cores. A count of matching nodes is not a count of
idle nodes; cordoned nodes do not accept new workloads. An unbound PVC event
describes an unbound storage claim at that scheduling attempt. This smoke later
passed actual storage access.

The catalog also advertises four-GPU variants
`n6ls.iu.i40.4.16c256g` (16 vCPU, 256 GiB) and
`n6ls.iu.i40.4.32c512g` (32 vCPU, 512 GiB). They were not run in this test and are
not automatic fallbacks. Select and register a changed task resource explicitly;
less host capacity can affect data loading and CPU work and does not guarantee
immediate scheduling.

P12 also binds `computing-cluster-01g-02`, whose standard four-GPU catalog name is
case-sensitive `N6lS.Iu.I10.4` (88 vCPU, 920 GiB). This is a separate pool path
that was not executed here. Register and qualify it explicitly if later selected.

## 6. Training, recovery and handoff

Reuse the concrete task's Protocol and launcher and the
[training observability contract](training_observability_contract.md). Preserve
effective global token batch, data order, loss normalization and valid-token/update
coordinates. Check required input IDs through the [asset registry](../assets/README.md)
before using model states or data, and register actually saved training checkpoints.

The shared AFS mount makes existing checkpoint files accessible from either
workspace. The training program must still restore model, optimizer, scheduler,
RNG, data position and token/update counters. Platform `jobs start` alone does
not establish an exact checkpoint resume. Inspect the original job before moving
workspaces; never run two copies of one trajectory writing to the same directory.
Use distinct receipts and output segments for authorized continuation.

For the next Agent: read this guide and the current envelope; choose one workspace
per main task; preview the resolved tuple; execute only the authorized task;
preserve its ID and durable evidence; do not duplicate it because of a queue or
query error. Different authorized experiments may run on different workspaces.
The P12 engineering smoke is already complete and need not be resubmitted.

Relevant sources: [workspace selector](../templates/execution/acp_submit_reserved_workspace.sh),
[base submission template](../templates/execution/acp_submit_template.sh),
[training reuse index](training_reuse_index.md), and the completed execution
certificate in the evidence root above.

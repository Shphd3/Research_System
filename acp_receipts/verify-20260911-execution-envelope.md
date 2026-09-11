# Run Receipt: execution-envelope submission verification / verify-env-0911

Owner: `docs/execution_envelope.md` (this is a repository-maintenance
verification, not a scientific experiment; no protocol or Focus is involved)
Status: SUCCEEDED

## Resolved tuple

| Field | Value |
| --- | --- |
| resource_profile | `h100-4-reserved` (default) |
| execution_surface | acp |
| workspace / aec2 | `share-space` / `share-cluster` (zone `cn-sh-01g`) |
| worker_spec / worker_nodes / worker_processes | `n6ls.iu.i40.4` / 1 / 4 |
| quota_type / priority | `reserved` / `normal` |
| image_id | `shphd-lite-0911` (default) |
| image_url (expanded) | `registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423` |
| activation script | none: the verification command used the image's own interpreter |
| dependency layer | none |
| storage_mount | `01995892-d478-76d8-aec7-13fd8284477e:/data` |
| gpu_used | true |
| job id | `pt-qk9pkesv` (preceded by `pt-6afcy76u`, same tuple, no persisted log) |
| retry count | 0 |
| submitted_at / terminal_at (UTC) | 2026-09-10T17:01:16Z / 2026-09-10T17:01:56Z |

## Entry point

Submitted through `templates/execution/acp_submit_template.sh`, which resolved
the tuple from `docs/execution_envelope.md` via `./researchctl envelope` and
called `sco_acp_compat.sh` from the envelope's `submission.entry_point`.

Gates satisfied: `DRY_RUN=0` / `ALLOW_SUBMIT=1` / `PROTOCOL_APPROVED=1`.
`SMOKE_GATE_PASSED` was not required: the job name is not a `-full` run.

## Scope and roots

Approved scope: researcher's 2026-09-11 instruction to verify, from the new
container, that the repository's SCO submission path submits correctly and with
the correct values.

Submission receipts: `acp_receipts/submit-verify-env-0911-20260910T170116Z.json`,
`acp_receipts/submit-verify-envelope-0911-20260910T165709Z.json`.
Pod log: `acp_receipts/pod/verify-env-0911-20260910T170132Z.log`.

## Monitoring

`monitor_owner`: this conversation (DeepSeek harness, deepseek-flash),
`sco acp jobs describe` polled in a managed background job.

Reported checkpoints: `STARTING` 17:01:31Z, `SUCCEEDED` 17:01:56Z.

## First diagnosis

The first verification job `pt-6afcy76u` also succeeded, but the platform kept
no pod stdout: `sco acp jobs stream-logs` returned only the scheduling line.
Cause: ACP does not retain a finished pod's stdout. Change: the submit template
now tees the remote command's output into `<REMOTE_DIR>/acp_receipts/pod/` on the
mounted storage, and the second job is the one that produced durable evidence.

## Measured environment (pod stdout, verbatim)

```text
[env] profile=h100-4-reserved image=shphd-lite-0911 host=pt-b2032ac835e647c39414790e9e8eb4f5-worker-0
GPU 0: NVIDIA H100 80GB HBM3 (UUID: GPU-28e46a11-9d21-ceaf-5b96-e8a1f9666b1e)
GPU 1: NVIDIA H100 80GB HBM3 (UUID: GPU-6dd83c56-c817-367f-e624-421eff2d1b94)
GPU 2: NVIDIA H100 80GB HBM3 (UUID: GPU-e5b81db6-f28c-1c92-c6f0-dc7c08ecde18)
GPU 3: NVIDIA H100 80GB HBM3 (UUID: GPU-fd232091-fe18-920e-1b8f-c0d7b2eece49)
Python 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0]
torch 2.3.0a0+6ddf5cf85e.nv24.04 cuda 12.4 cuda_available True numpy 1.24.4
/data/250010109/Research_System
VERIFY_OK
```

The worker `pt-3955ce1f5e5c4019ba9a127d6c0c82d6-worker-0` reported resource
`N6lS(4 GPUs, 88 vCPU, 960 GiB)` and phase `Succeeded`.

## Eligibility

This receipt certifies only that the envelope's profile, image URL, entry point,
mount, and activation-free command path work, and that the image's declared
interpreter, torch, CUDA, and numpy versions match the pod's measurement. It is
not scientific evidence and supports no result claim. The two verification jobs
consumed about two minutes of the reserved node each; they trained nothing.

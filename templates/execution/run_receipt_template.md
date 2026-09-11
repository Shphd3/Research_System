# Run Receipt: <experiment id> / <job name>

Owner: <protocol.md path>
Status: <SUBMITTED | RUNNING | SUCCEEDED | FAILED | PARTIAL>

## Resolved tuple

| Field | Value |
| --- | --- |
| resource_profile | <key from docs/execution_envelope.md> |
| execution_surface | acp |
| workspace / aec2 | |
| worker_spec / worker_nodes / worker_processes | |
| quota_type / priority | |
| image_id | <key from docs/execution_envelope.md> |
| image_url (expanded) | |
| activation script | |
| dependency layer | |
| storage_mount | |
| gpu_used | true / false |
| job id | |
| retry count | |
| submitted_at / terminal_at (UTC) | |

## Entry point

Submitted through: <sco_acp_compat.sh, or the workspace submit script that calls it>

Gates satisfied: `DRY_RUN=0` / `ALLOW_SUBMIT=1` / `PROTOCOL_APPROVED=1` /
`SMOKE_GATE_PASSED=1` for a full run

Exact command: <verbatim>

## Scope and roots

Approved scope: <what this job is authorized to do>

Code root / run root / result root / log path:

## Monitoring

`monitor_owner`: <conversation name, agent, model>

Monitoring method: <managed background job id or equivalent>

Reported checkpoints: <state changes only, not a progress log>

## First diagnosis

<the first failure or anomaly, its cause, and whether any scientific input was
touched>

## Eligibility

<which artifacts this job may certify, and which are failure-ledger evidence
only>

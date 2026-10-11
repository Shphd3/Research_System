# Implementation And Execution

Repository paths are Research_System-root-relative. Input: requested stage,
owning Anchor/Protocol, workspace and existing scoped authorization.

## Resolve Scope

Read the owning question/contract and workspace `AGENTS.md`; use `PROJECTS.md`
only if ownership is unclear. Check conditions, primary readout, supporting/
non-supporting/insufficient branches and stage gates. Drafting authorizes no
implementation/run; existing in-scope authorization needs no repeat approval.
Small local checks follow root AGENTS. Smoke approval alone is not full approval.

Before training implementation/code reuse, inspect actual sources following
`docs/training_reuse_index.md`. Training also requires
`docs/training_observability_contract.md`: loss/token telemetry, matched global
batch, token schedules and finite/counting/resume Smoke checks. Do not duplicate
that contract or impose an objective component absent from the model.

For training/resume and analysis that reads checkpoints, datasets or saved
representations, follow the [asset lifecycle](../../../../assets/README.md#training-and-analysis-lifecycle).
Record and check the stage's required input IDs and their exact parent/interface.
The training contract names final/required checkpoint saves; artifact completion
registers the actual outputs through [artifacts.md](artifacts.md).

Before submission, resolve profile, image, activation/dependency layer and
entry point from `docs/execution_envelope.md`, never memory. An authorized scope
using the envelope default creates no new gate. A different resource/image/scope
requires a researcher-authorized exception recorded in the Protocol; no silent
fallback. Debug hosts are not compute reservations.

Before resume/retry inspect existing job/output state; preserve checkpoint,
optimizer, RNG, token and data lineage. Do not duplicate live runs or overwrite
completed artifacts. Reuse qualification when applicable; record an explicit
Smoke waiver as waived, not PASS.

## Launch And Record

Resolve runner/config, data manifest, command, output path, stage,
profile/image/runtime, expected artifacts and stop gates. Training includes
the observability contract's log location, reductions, batch and token schedule.

For ACP use `templates/execution/acp_submit_template.sh`: its resolver reads
the envelope, defaults to dry run, enforces gates and writes a receipt. Check
the dry run before authorized submission. Set `REMOTE_DIR` and `RUN_ROOT` to
the experiment workspace/run root, not the template verification defaults. Use
`sco-control` without bypassing the supported entry point.

```bash
JOB_NAME=<name> REMOTE_CMD='<command>' bash templates/execution/acp_submit_template.sh
DRY_RUN=0 ALLOW_SUBMIT=1 PROTOCOL_APPROVED=1 JOB_NAME=<name> REMOTE_CMD='<command>' \
  bash templates/execution/acp_submit_template.sh
```

Approval flags reflect actual scope. Preserve command/config identity; the
template tees output to mounted `<REMOTE_DIR>/acp_receipts/pod/`, since finished
pod stream output is not evidence. Use
`templates/execution/execution_certificate_template.md` for environment, job, command,
config, log/result paths, GPU use, monitor owner and first diagnosis. An accepted
submission receipt is not the certificate of what actually ran.

Finish with the authorized stage's receipt/logs/outputs or explicit failure;
do not promote scientific judgment or the next gate. After submission use
[startup.md](startup.md). Requested result work uses [artifacts.md](artifacts.md).

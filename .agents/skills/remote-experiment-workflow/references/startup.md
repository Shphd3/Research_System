# Startup And Monitoring

Input: existing job ID, submission receipt, durable output path and authorized
supervision scope. Inspect that job; do not launch a replacement. Each run root
has one monitoring owner; verify that ownership before continued polling and
use an explicit handoff before replacing another conversation's owner.

Without explicit continuous/completion-time monitoring, observe a short startup
window: scheduling, expected workers/runtime, Smoke or first bounded progress
gate when available, durable logging and immediate failures. Honor user/Protocol
time limits. If still queued at the limit, report unverified runtime checks
and end polling while leaving the job scheduled; never wait indefinitely.

Report job ID, verified progress, log, uncertainty and throughput-based ETA (or
unknown). Ending monitoring neither terminates nor authorizes resubmission.
Later inspect the same ID. Cancellation, retry, fallback or stage advancement
must already be authorized.

For requested ongoing monitoring, follow its duration/completion and failure
conditions; report meaningful transitions. Create no unrequested automation.
Operational completion cannot unseal CONFIRM: its scope and gates still govern.
ACP completion requires durable mounted pod output and expected artifacts;
scheduling/stream-log output is insufficient.

# Explicit SSH / CCI

Read [remote_hosts.yaml](remote_hosts.yaml) when choosing a debug host unless
the user names a newer target. Four-hour hosts are not reserved profiles;
`docs/execution_envelope.md` governs submissions. Use a project transport skill
if required. If already in the target container, work there within scope.

Check host/workspace identity and relevant processes before mutation; GPU work
also verifies hardware/runtime. Before edits/pulls inspect the working tree
and preserve others' work. Status needs only the job's identity/evidence.

SSH/SCP is for explicit small status checks, forwarding, recovery or CCI control;
full runs use the authorized container/SCO/ACP path. The existing
[PowerShell helper](../scripts/remote_sco_session.ps1) supports
print/connect/preflight/forward using the same registry.

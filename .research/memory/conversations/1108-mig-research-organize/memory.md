# Conversation Memory: 1108-mig-research-organize

Conversation name: 1108-mig-research-organize
Conversation ID: dade3be2-884f-4a18-a3a9-98063cf78572 (Claude Code session; transcript /root/.claude/projects/-data-250010109-Research-System/dade3be2-884f-4a18-a3a9-98063cf78572.jsonl, backed up under chat_history_backups/claude/live)
Processed by: Claude Code (harness: Claude Code CLI 2.1.280, interactive --remote-control session "MIG" in tmux claude-mobile; model: claude-opus-5-5). The contract's agent list has no Claude entry; recorded as-is rather than mislabelled.
Created at: 2026-11-08T10:29:01Z
Latest update at: 2026-11-08T10:29:01Z
Continues from: none
Environment: data=/data/250010109 (visible); repo=/data/250010109/Research_System (visible); claude-runtime=/root/.claude (visible now, ephemeral: lost on container restart, restored from data)

## 2026-11-08T10:29:01Z -- Container persistence audit, MiMo removal, Remote Control service; checkpoint before restart

- Summary: Infra-only conversation; no scientific artifact, Anchor, Protocol or experiment touched. (1) Audited Claude chat persistence: /root/.claude is restored at boot from chat_history_backups/claude/live by setup_env.sh, and a 120 s loop backs it up; a scratch-dir restore round trip matched runtime (all session jsonl present, settings identical). (2) Found and fixed a gap: `setup_env.sh finalize` (scheduled 4 h stop) only checked the Codex marker; it now runs backup_claude_fast.sh first, falling back to a periodic generation <30 min old. (3) At the user's request MiMo was removed: claude_provider.py default profile is now `official` (claude.ai login, no ANTHROPIC_BASE_URL/apiKeyHelper), MiMo profiles and runtime_env/secrets/mimo_api_key deleted; deepseek profile kept but would disable Remote Control. (4) Added an always-online Remote Control server: ops/claude_remote_control.sh in tmux `claude-rc` (`claude remote-control --name Mig --spawn same-dir --permission-mode bypassPermissions` in Research_System), started by setup_env.sh after a successful Claude restore, waits for the restore marker, restarts with backoff. Verified Connected and unattended reconnect after `claude-rc restart`. (5) Full backup-all-fast at 10:27Z succeeded; Claude generation 20261108T102712Z verified, runtime=50 / backup=50 session files.
- Current work: User is about to restart the container to test end-to-end. Not yet verified: a real container restart (only service restart + restore round trip were tested). PATH fix for sco inside claude-rc (adds /root/.sco/bin) is written but only takes effect on next claude-rc start; two app-spawned sessions were active so the service was not restarted. Old manual session (this one, tmux claude-mobile) will not auto-return after restart; its transcript is backed up.
- Next action: After restart, verify: `claude-rc status` running and `claude-rc logs` shows Connected; Claude app shows environment Mig/Research_System and can create a new session; previous sessions (including this one) are listed/resumable; `/root/.claude/settings.json` has no ANTHROPIC_BASE_URL; `which sco` works inside an app-spawned session. Then take on user's pending request: manage SCO/ACP job submission from these sessions (use the compat shim, see Claude memory acp-sco-cli-topology). If claude-rc is not Connected, check /tmp/claude-rc-start.log and chat_history_backups/claude/ops/logs/remote-control.log (likely login/consent or proxy not up).
- References:
  - /data/250010109/PERSISTENCE_RUNBOOK.md (two 2026-11-08 sections document both changes)
  - /data/250010109/setup_env.sh (finalize branch; start_claude_remote_control); pre-change copy setup_env.sh.before-claude-finalize-20261108
  - /data/250010109/chat_history_backups/claude/ops/claude_remote_control.sh (the service)
  - /data/250010109/runtime_env/claude_provider.py; pre-change copy claude_provider.py.before-remove-mimo-20261108
  - /data/250010109/chat_history_backups/claude/ops/claude_sync.py (backup scope: excludes only ide, telemetry, worktrees, _sync_snapshots)

@AGENTS.md

# Claude Code Compatibility

`AGENTS.md` is the core policy. Skills live in `.agents/skills/` (exposed under
`.claude/skills/`). In the exploration lane use only `research-progress-core`,
`research-reasoning-auditor` and `remote-experiment-workflow`; load other skills
and `docs/formal_lane.md` only for the formal lane or an explicit request.
User instructions take precedence.

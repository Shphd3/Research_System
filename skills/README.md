# Skills

This folder is only an index. Actual repo-tracked skill sources live in:

```text
codex_skills/
```

Installed local copies live in:

```text
C:\Users\250010109\.codex\skills\
```

Edit `codex_skills/<skill>/SKILL.md` first, then sync the installed copy when needed.

## How Codex Uses Skills

Codex uses a skill when:

- the user explicitly names it, or
- the task clearly matches the skill description.

Codex then reads that skill's `SKILL.md` and follows its required output and rules.

Skills are task-specific. Global reply style belongs in `AGENTS.md`, not in a skill.

## Active Skills

| Skill | Use |
|---|---|
| `research-mainline` | Decide whether material updates the active project mainline. |
| `claim-auditor` | Check whether claims exceed evidence. |
| `experiment-card-writer` | Write compact experiment cards and result-decision blocks. |
| `daily-report-coach` | Compress daily work into a concise daily report. |
| `meeting-brief-coach` | Produce 30s / 1min advisor-facing explanations and brief written meeting notes. |
| `prism-report` | Build group-meeting-ready PRISM reports. |
| `paper-reading-card` | Turn papers or blogs into compact reading cards. |

## Retired / Merged Skills

These source skills were merged and should not be used as separate defaults:

| Old skill | Merged into |
|---|---|
| `daily-research-report` | `daily-report-coach` |
| `meeting-brief-builder` | `meeting-brief-coach` |

## Project-Specific Skill

| Skill | Status |
|---|---|
| `moe-specialization-diagnosis` | Keep available for MoE-specific analysis, but do not move it into a project folder yet. |

## Cleanup Rule

Do not add new skills unless the task is repeated often and cannot be handled by one of the active skills.

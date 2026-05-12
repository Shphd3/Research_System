# Skills

This folder is only an index. Repo-tracked skill sources live in:

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

## Active Global Skills

| Skill | Use |
|---|---|
| `research-mainline` | Decide whether material updates the active project mainline. |
| `claim-auditor` | Check whether claims exceed evidence. |
| `experiment-card-writer` | Write compact experiment cards and result-decision blocks. |
| `daily-report-coach` | Compress daily work into a concise daily report. |
| `meeting-brief-coach` | Produce 30s / 1min advisor-facing explanations and brief written meeting notes. |
| `prism-report` | Build group-meeting-ready PRISM reports. |
| `paper-reading-card` | Turn papers or blogs into compact reading cards. |

## Formula Rule

When a skill writes Markdown research documents:

- inline formulas must use `$...$`;
- display formulas must use `$$...$$`;
- raw LaTeX formulas should not appear in prose without math delimiters.

## Removed / Merged Skills

| Old skill | Status |
|---|---|
| `daily-research-report` | Merged into `daily-report-coach`. |
| `meeting-brief-builder` | Merged into `meeting-brief-coach`. |
| `moe-specialization-diagnosis` | Removed from global skills because it is project-specific. |

## Cleanup Rule

Do not add new global skills unless the task is repeated often and cannot be handled by one of the active global skills.

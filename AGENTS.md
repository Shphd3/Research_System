# Codex Research System

This folder is a research-process workspace, not the remote code repository.
Remote servers run experiments. This workspace preserves research judgment, evidence, reports, and presentation practice.

## Start Here

At the start of any research task:

1. Read `CURRENT.md`.
2. Read the daily report or raw material named by the user.
3. Decide whether the material updates the mainline before writing a long response.

Do not rely on chat history as the main source of memory.

## Mainline Discipline

Every research output must answer:

- What was done?
- What is the one-sentence conclusion?
- Does this update the current mainline?
- What can we not claim yet?
- How should this be explained in 30 seconds?

If there is no mainline update, say `No mainline update today` and explain why.

Do not turn experiment logs into reports by summarizing every detail. Keep only evidence that changes the hypothesis, modeling, empirical support, limitation, or next decision.

## Daily Report Shape

Use this compact structure for `daily_report.md`:

```markdown
# Daily Report - MMDD

## What I Did

## Core Conclusion

## Mainline Update

## What I Cannot Claim Yet

## 30s Meeting Script
```

## Codex Skills

Use these personal skills when they exist:

- `research-mainline`: judge whether material updates the research mainline.
- `daily-report-coach`: compress daily work into a clear daily report.
- `meeting-brief-coach`: produce advisor-facing 30 second and 1 minute explanations.

The repo-tracked skill sources live in `codex_skills/`. The installed copies live in `C:\Users\250010109\.codex\skills\`.

## Git Habit

Prefer one lightweight commit per working day:

- `MMDD: mainline update - <one sentence conclusion>`
- `MMDD: daily note - no mainline update`

Keep generated binaries, archives, LaTeX build outputs, and temporary iCloud files out of git.

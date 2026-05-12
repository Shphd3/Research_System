---
name: daily-report-coach
description: Use when turning daily research work, experiment notes, reading notes, blockers, meeting preparation, or next-day plans into a concise daily report anchored to the active project mainline.
metadata:
  short-description: Write concise daily reports
---

# Daily Report Coach

Use this skill to write or revise a daily research report. Do not turn the day into a task log.

Daily reports should live under:

```text
daily_research_reports/MMDD/daily_report.md
```

## Required Output

Use this compact structure by default:

```markdown
# Daily Report - MMDD

## What I Did

## Core Conclusion

## Mainline Update

## Viewpoint Update / Self-Audit

## What I Cannot Claim Yet

## 30s Meeting Script
```

Optional fields only when useful:

```markdown
## Problems / Blockers

## Tomorrow's Plan

## Questions For Advisor
```

## Rules

- Read the active project mainline first when available.
- Keep only evidence that affects the mainline, claim boundary, or next decision.
- Do not list every experiment detail.
- The viewpoint update must be one research judgment, not a diary reflection.
- The self-audit must name the vulnerable part: unsupported assumption, ambiguous definition, missing control, possible counterexample, or over-strong wording.
- If no viewpoint changed, write `No viewpoint update today` and explain why.
- The 30 second script must be understandable to someone who has not followed every detail.
- Avoid vague phrases like "interesting result"; state what the result supports, weakens, or leaves unresolved.
- When writing Markdown research documents, inline formulas must use `$...$` and display formulas must use `$$...$$`.

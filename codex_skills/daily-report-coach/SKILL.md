---
name: daily-report-coach
description: Use when turning daily research work, experiment notes, reading notes, blockers, meeting preparation, or next-day plans into a concise daily card anchored to the active project mainline.
metadata:
  short-description: Write concise daily cards
---

# Daily Card Coach

Use this skill to write or revise a daily card. Do not turn the day into a task log or long report.

Daily cards should live under:

```text
daily_research_reports/MMDD/daily_card.md
```

## Required Output

Use this compact structure by default:

```markdown
# Daily Card - MMDD

## 1. Today's Purpose

## 2. Mainline Anchor

## 3. Task Conclusions

### Task 1

Did:

Conclusion:

## 4. Mainline Update

## 5. What I Cannot Claim Yet

## 6. Next Decision

## 7. 30s Explanation
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
- Each task must end with a conclusion. If a task has no conclusion, state what remains undecided.
- The mainline update must say whether the day changed a hypothesis, modeling definition, claim boundary, bottleneck, or next decision.
- The self-audit belongs in `What I Cannot Claim Yet`: unsupported assumption, ambiguous definition, missing control, possible counterexample, or over-strong wording.
- The 30 second script must be understandable to someone who has not followed every detail.
- Avoid vague phrases like "interesting result"; state what the result supports, weakens, or leaves unresolved.
- When writing Markdown research documents, inline formulas must use `$...$` and display formulas must use `$$...$$`.

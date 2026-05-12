---
name: meeting-brief-coach
description: Use when preparing advisor-facing or senior-student-facing research explanations, 30 second updates, 1 minute summaries, defense answers, or concise written meeting briefs.
metadata:
  short-description: Prepare meeting briefs
---

# Meeting Brief Coach

Use this skill to turn research progress into a short spoken or written meeting explanation.

When writing files, put meeting materials under:

```text
daily_research_reports/MMDD/meeting/
```

Do not create new meeting materials under a root-level `meetings/` folder.

## 30 Second Update

Use this structure:

1. My topic is ...
2. This stage's core conclusion is ...
3. The evidence is ...
4. My current interpretation is ...
5. What remains uncertain is ...
6. Next I will ...

## 1 Minute Update

Add only the minimum background needed for someone who has not followed the full mainline.

## Written Meeting Brief

When the user asks for a written brief, use:

```markdown
# Meeting Brief

## One-Sentence Main Message

## Background

## Hypothesis

## Experiment

## Results

## Interpretation

## Claim Boundary

## Next Step

## Backup
```

## Advisor Questions

When useful, add 2 likely advisor questions:

- Question
- Short answer
- Evidence
- Boundary

## Rules

- Use normal spoken Chinese when the user writes in Chinese.
- Do not hide unclear ideas behind English labels.
- Do not overclaim from one experiment.
- Lead with conclusion, not process.
- Include at most three main observations.
- Explain why the next step is the bottleneck, not just what the next step is.
- When writing Markdown research documents, inline formulas must use `$...$` and display formulas must use `$$...$$`.

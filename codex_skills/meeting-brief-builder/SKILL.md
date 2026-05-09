---
name: meeting-brief-builder
description: Use when preparing advisor or group-meeting updates from mainline files, experiment cards, claim board, daily reports, or PRISM report drafts.
metadata:
  short-description: Build meeting briefs
---

# Meeting Brief Builder

Prepare a concise research meeting brief.

Default output location for new meeting materials:

```text
daily_research_reports/MMDD/meeting/
```

Do not create new meeting materials under a root-level `meetings/` folder.

## Required Output

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

## Rules

- Optimize for what the audience should remember.
- Use claim boundaries from `claim_board.md`.
- Include at most three main observations.
- The next step must be the next decisive experiment, not a long wish list.
- Add 2-3 likely advisor questions when useful.

---
name: experiment-card-writer
description: Use when converting raw experiment notes, model comparison tables, synthetic reports, logs, or meeting notes into a structured experiment card with question, hypothesis, setup, controls, results, claim strength, limitations, and next experiment.
metadata:
  short-description: Write experiment cards
---

# Experiment Card Writer

Convert raw experiment material into a structured research experiment card.

## Required Output

```markdown
# Experiment Card

## Question

## Hypothesis

## Setup

## Controls

## Metrics

## Results

### Raw Observations

### Interpretation

## Claim Strength

## Limitations

## Next Experiment
```

## Claim Strength Labels

Use:

- supported
- weakly supported
- unsupported
- contradicted
- unclear

## Rules

- Separate raw observations from interpretation.
- Always name controls and oracle / upper bound if available.
- If the evidence is weak, say it is weak.
- Do not let a good-looking metric become a stronger public claim than it supports.

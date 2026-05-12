---
name: experiment-card-writer
description: Use when designing, rewriting, or analyzing experiments as compact project-local experiment cards with hypothesis, setup boundary, baselines, metrics, result, conclusion, and next decision.
metadata:
  short-description: Write compact experiment cards
---

# Experiment Card Writer

Convert experiment ideas, raw notes, logs, or result summaries into one compact experiment card.

## Location Rule

Project-specific experiment cards should live inside the active project, normally under:

```text
Projects/<project>/main/
```

For branch-local work, use the branch folder instead of project-level `main/`, for example:

```text
Projects/from-attention-to-search/XingyuD/main/plans/
Projects/from-attention-to-search/XingyuD/main/experiments/
```

Do not create root-level `experiments/` cards unless the user explicitly asks for a global/cross-project card.

## Pre-Experiment Thinking

Before writing a card, answer these internally and reflect them in the card:

1. What is the core hypothesis?
2. Why is this setup meaningful: model, data, task, diagnostic target?
3. What are the boundary conditions of this setup?
4. Which experiments are needed, and do they jointly test the hypothesis rather than only show a suggestive signal?

## Required Output For Experiment Design

Output one card by default:

```markdown
# Experiment Card: E1 Router-Attention Recall

## 1. Hypothesis To Decide
H1: Router bucket and attention top-token are aligned.

## 2. Experiment Question
Given query token q_t, do router-retrieved candidate tokens cover dense attention top-M tokens?

## 3. Setup
Model:
Dataset:
Layer:
Head:
Signal source:
Candidate construction:

## 4. Baselines
- Random bucket
- Local window
- Oracle top-M
- Full attention

## 5. Metrics
- Recall@K
- Attention Mass Recall
- Candidate Ratio
- Sparse Output Error
- Accuracy Drop

## 6. Key Figures For Reporting
- Figure 1:
- Figure 2:
- Figure 3:

## 7. Expected Outcomes
If H1 holds:
Gate recall > Random recall.

If H1 fails:
Gate recall ~= Random recall.

## 8. What This Can Prove
It can test whether the router provides a coarse retrieval signal.

## 9. What This Cannot Prove
It cannot prove full inference speedup.
It cannot prove million-token scalability.
It cannot prove standard MoE routing is already sufficient.

## 10. Result
TBD.

## 11. Conclusion
TBD.

## 12. Next Step
TBD.
```

## Required Output For Result Analysis

Use this compact block:

```markdown
## Result R1

### Observation
We observe: Gate candidate Recall@K = __, Random candidate Recall@K = __.

### Interpretation
This means whether Gate candidates contain more dense-attention top-M tokens than Random candidates.

### Limitation
This does not show:
- full inference will accelerate;
- all layers/heads behave the same;
- real long-context tasks will benefit.

### Key Figures
- Figure:
- What it should show:
- Meeting use:

### Decision
Therefore:
- if Gate > Random: continue to candidate exact attention;
- if Gate ~= Random: check whether a memory router is needed;
- if only some layers/heads work: use layer/head-wise selective routing.
```

## Rules

- Keep the card short.
- Do not output multiple cards unless the user asks.
- Separate result, interpretation, limitation, and decision.
- Do not let a metric improvement become a stronger public claim than it supports.
- Prefer decision-oriented wording over long experiment narration.
- Every experiment card should specify the key figure(s) needed for advisor-facing reporting.
- Figures should be diagnostic, not decorative: they must support a claim boundary or next decision.
- When writing Markdown research documents, inline formulas must use `$...$` and display formulas must use `$$...$$`.

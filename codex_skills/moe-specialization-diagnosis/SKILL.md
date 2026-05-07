---
name: moe-specialization-diagnosis
description: Use when diagnosing MoE specialization results, routing metrics, sparse feature division, function alignment, frequency-tail behavior, interference, forgetting, or metric limitations in the user's Hierarchical MoE research.
metadata:
  short-description: Diagnose MoE specialization
---

# MoE Specialization Diagnosis

Use this skill for the user's Feature-Zipf / Hierarchical MoE research.

## Diagnostic Axes

Check specialization along six axes:

- feature-level specialization: experts separate sparse input features
- function-level specialization: expert functions align with true mechanisms
- routing-level specialization: routing assignments are stable and meaningful
- frequency / tail behavior: high, middle, rare, or unique mechanisms behave differently
- interference / forgetting behavior: specialization reduces update interference or forgetting
- metric limitations: current metrics may not measure the intended mechanism

## Required Output

```markdown
# MoE Specialization Diagnosis

## Feature-Level Specialization

## Function-Level Specialization

## Routing-Level Specialization

## Frequency / Tail Behavior

## Interference / Forgetting Relevance

## Metric Limitations

## Current Best Explanation

## Next Diagnostic Experiment
```

## Rules

- Do not equate high NMI with functional specialization.
- Do not equate low loss with correct mechanism recovery.
- Treat oracle results as recoverability checks.
- Identify whether hierarchy helps features, functions, routing stability, or none of them.

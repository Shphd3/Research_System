# Profiling And Evidence

Use this reference when planning, running, or reviewing research evidence.

## Rule

Do not stop at a top-line metric or yes/no answer. The explanation comes from
stage-level profiling:

```text
final result -> stage evidence -> bottleneck or support -> conjecture update
```

For each important stage, record:

```text
question
input evidence
output evidence
failure evidence
artifact
interpretation
```

## Minimum Evidence

Every experiment report should include:

```text
purpose
setup
parameters
metrics
good examples
bad examples
confusing examples
visual or inspectable evidence when possible
interpretation
next experiment or decision
```

Aggregate metrics are not enough when false positives, false negatives, or
stage-local failures can hide inside an average.

## Evidence Types

When evidence unfolds over training, seeds, checkpoints, ablations, or changing
conditions, separate three kinds of evidence:

```text
single-observation evidence: what is true in one observation, seed, checkpoint, or run
change evidence: what changes or persists across observations, seeds, checkpoints, or conditions
summary evidence: what is true after aggregating observations
```

Do not replace change evidence with a single-observation proxy unless the proxy
itself is the thing being tested. For training trajectories, seed stability, and
before/after comparisons, report the change evidence explicitly.

## Fast Micro-Test

For slow loops, run a small diagnostic before a full run:

```text
known good cases
known bad cases
known confusing cases
small number of samples or observations
one or two parameter settings
stage-local artifacts
clear stop condition
```

Full sweeps are useful only after the micro-test shows that the
operationalization is worth scaling.

Known cases should be chosen before interpreting the result:

```text
known good: should pass if the operationalization is valid
known bad: should fail if the operationalization is not too permissive
known confusing: likely to reveal ambiguity, shortcut use, or metric mismatch
```

## Strong Reference Comparison

When an oracle, trusted reference, manual label, or controlled benchmark exists,
use it to understand error structure, not only to compute one final score.

Ask:

```text
How do true positives look at each stage?
How do false positives look at each stage?
How do false negatives look at each stage?
Which variables separate them?
Which variables fail to separate them?
What is the cost of a false positive?
What is the cost of a false negative?
```

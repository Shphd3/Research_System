# Failure Decomposition

Use this reference when the result is wrong but the cause is not local yet.

## Rule

Do not ask only why the whole system failed. Break the failure into smaller
questions until the bottleneck is observable and fixable:

```text
big failure -> candidate sub-problems -> stage-local tests
-> verified bottleneck -> targeted fix
```

## Record

For each decomposition level, record:

```text
parent failure
candidate sub-problems
test for each sub-problem
answer for each sub-problem
evidence supporting each answer
remaining bottleneck
```

Each level must produce an answer, even when the answer is `not the cause`.
Negative answers are progress when they remove false explanations.

## Common Checks

Choose checks that match the domain. Common questions include:

```text
Is the benchmark unable to answer the question?
Is the visualization or analysis wrong?
Is the ground truth wrong or mismatched?
Is the evidence ambiguous?
Is the correct case missing from the candidate set?
Is the decision rule too strict?
Is the decision rule too permissive?
Is the metric rewarding the wrong behavior?
Is a later stage hiding an earlier-stage failure?
```

Only change the algorithm after the decomposition identifies a specific failed
sub-problem. If several causes remain plausible, instrument them first.

## Final Causal Path

When resolved, record:

```text
big failure -> falsified explanations -> verified bottleneck
-> fix -> remaining unsolved problem
```

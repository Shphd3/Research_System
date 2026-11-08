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

Record the answer each tested level supports, including `not the cause` or
`Unknown`. Negative answers are progress when they remove false explanations;
an unresolved cause need not block a test that separates the remaining ones.

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

Claiming a root-cause fix requires localization evidence. When several causes
remain plausible, a bounded algorithm intervention can be a distinguishing test
within the authorized scope. State which rival outcomes it separates and what
else changes; a candidate repair is not an established cause. Instrument first
when the intervention would otherwise be uninterpretable. Avoid requiring proof
of the cause before allowing the experiment needed to identify it.

## Graded Interface Diagnosis

When interface difficulty could hide the bottleneck, consider a short ladder:
ideal interface -> controlled mixing/sharing -> real or learned interface.
For addressing/routing, useful candidates are oracle addressing, fixed random
sharing, structure-based sharing and learned routing. Choose only levels that
separate live explanations; the ladder is not a required new experiment program.

At each selected level, state the difficulty removed, the difficulties retained,
permitted information and fairness of the comparison. Account for capacity,
supervision, data exposure, initialization, update budget and interface changes.
An oracle using unavailable truth is a diagnostic reference, not an ordinary
performance baseline. Existing evidence may make an additional level unnecessary.

Success after removing one difficulty localizes a candidate bottleneck only as
far as the matched comparison permits. Failure under ideal addressing does not
uniquely implicate reading: check viable alternatives such as capacity, writing
or training, supervision, initialization, interface compatibility and task code.
Pick the smallest separator among the remaining alternatives and retain Unknown
where the levels change more than one relevant factor.

## Final Causal Path

When resolved, record:

```text
big failure -> falsified explanations -> verified bottleneck
-> fix -> remaining unsolved problem
```

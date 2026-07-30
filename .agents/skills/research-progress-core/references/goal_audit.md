# Goal Audit

Use this reference when repeated reasonable fixes fail, or when the old metric
may not match the downstream decision.

## Trigger

Audit the goal when:

```text
several reasonable operationalizations fail
the same error pattern keeps returning
the label may not match the downstream purpose
false positives and false negatives have different costs
a high metric still produces an unhelpful result
```

## Questions

Ask:

```text
What downstream decision will use this result?
Are we solving that decision, or only matching a convenient label?
Are the labels too strict, too loose, or mismatched?
Do false positives and false negatives have equal cost?
Which old errors are acceptable or useful?
Which old errors remain harmful?
Would another metric better capture useful progress?
What is costly to miss?
What is safe to include even if imperfect?
```

## Record

Write:

```text
original goal
downstream decision
old success metric
observed failure pattern
cost of false positives
cost of false negatives
revised goal
revised metric
old errors now acceptable or useful
errors still harmful
```

If the goal changes, update the current-state document before designing the
next experiment.

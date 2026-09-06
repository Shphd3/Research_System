# Result Interpretation

Use this reference to interpret completed evidence or diagnose a failed result.

## Eligibility First

Before interpreting, verify the frozen Protocol, completed conditions, primary
metric, hard guards, seeds or independence units, deviations, and evidence
paths. Incomplete or ineligible evidence may be described but cannot support a
registered conclusion.

Separate:

```text
observation      directly measured
interpretation   explanation suggested by the observation
claim            safest supported statement
speculation      untested possibility
boundary         what the evidence cannot support
decision         what happens next
```

Return requested numbers and run status before explanation.

## Decision-Bearing Evidence

Lead with the comparison and metric closest to the research question. Define a
metric by its concrete computation, unit, decision role, and non-claim. Name
the true independence unit; layers, tokens, checkpoints, and arms are not
automatically independent replicates.

Use the smallest sufficient figure set. Each retained figure states the
question, metric and unit, data and aggregation, axes, visible result, allowed
conclusion, and limitation. Prefer the decisive negative or mixed result over
an easier positive diagnostic. Do not promote debug plots.

When `summary.md` exists, link it instead of repeating its four-part account.
The chat response gives only the direct verdict, smallest decisive value,
important figure and reading instruction, nearest boundary, and why the next
step follows. Label an unconfirmed next step `AI 建议`.

## Failure Localization

Classify a failure before changing the method:

```text
prior failure
model failure
proxy or operationalization failure
implementation failure
metric failure
```

Test the smallest candidate bottleneck. A negative result is progress when it
removes a rival explanation. Use `failure_decomposition.md` when several causes
remain live and `goal_audit.md` only when repeated attempts or the metric itself
show that the target may be wrong.

## Next Step

The next-step analysis must name the unresolved uncertainty, why the completed
result makes that uncertainty next, the smallest separating action, its
completion condition, and the observation that would stop or redirect it. It
does not authorize a new experiment or scientific transition.

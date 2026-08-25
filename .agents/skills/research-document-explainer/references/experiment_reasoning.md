# Experiment Explanation And Suggestion Mode

Use this mode to explain an experiment, method, Protocol, result record, plot,
metric, or an explicitly requested experiment suggestion. It explains and
proposes; it does not approve a run or write a formal Protocol.

## Explain The Existing Experiment

Reconstruct one experiment in this order:

1. **Decision question** — which uncertainty has different downstream actions?
2. **Objects** — model state, data unit, treatment, control, target, and
   statistical unit in plain language.
3. **Decisive contrast** — exactly what differs and what is held fixed.
4. **Metric** — concrete computation, unit, decision role, threshold, and what
   it cannot prove.
5. **Guards** — only the controls or checks needed to rule out a named rival or
   protect eligibility.
6. **Outcome branches** — Pass, Fail, and Insufficient as changes to the
   research judgment, not merely threshold labels.
7. **Current evidence** — direct result separately from interpretation and
   claim boundary.

Explain a multi-stage design as gates. At each gate state why downstream work
is not interpretable before it passes.

## Suggest Experiments

Offer a suggestion only when the user asks or when one missing comparison is
the direct reason the document cannot answer its own question. Give at most
three genuinely different candidates and recommend one.

Every candidate is an `AI_PROPOSAL` with this shape:

```text
uncertainty or named rival
smallest treatment-control comparison
held-fixed variables
primary metric and unit
positive, negative, and insufficient readings
stopping rule
which judgment or boundary would change
```

Prefer the smallest probe plus matched control that can falsify the proposed
explanation. A diagnostic is not a separate core experiment when it only
protects the same verdict.

## Boundaries

- A suggested experiment is not an approved Protocol or authorization to run.
- Do not change a frozen Protocol while explaining it. Describe a possible
  amendment as `AI_PROPOSAL` and route formal work to
  `experiment-card-writer`.
- Do not treat a readable representation, proxy metric, or successful
  classifier as functional or causal evidence without the required contrast.
- Respect the active core-task Focus. Park or omit a tangent rather than
  presenting it as the next active experiment.

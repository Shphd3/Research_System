# Algorithm Specification

Use this reference when a research method contains nontrivial stages,
thresholds, fitting, matching, ranking, clustering, filtering, or hidden
heuristics.

## Rule

Do not run an experiment until the method is written as an exact algorithm.
Words such as `stable`, `aligned`, `valid`, `cluster`, `match`, `filter`, or
`score` are not algorithms until their computation and failure cases are
defined.

## Required Block

For each nontrivial stage, write:

```text
input
parameters
intermediate variables
step-by-step procedure
pass conditions
fail conditions
failure reasons
outputs
debug artifacts
```

For every important parameter, record:

```text
name
value
meaning
why this value is used
expected effect if too small
expected effect if too large
```

## Alignment Check

Before coding or running, verify:

```text
physical prior: what should happen in the system?
math model: what variables measure it?
algorithm: what exact steps compute those variables?
experiment: what result would support or falsify the model?
```

If a heuristic is not implied by the prior or math, name it as an implementation
heuristic and state how it could bias the result.

## Stage Contract

For each pipeline stage, record:

```text
input assumptions
local objective
exact steps
expected intermediate output
pass/fail criterion
named failure reasons
debug artifact
representative pass examples
representative fail examples
next-stage handoff contract
```

After the stage runs, record input counts, accepted outputs, rejected outputs by
reason, and the artifacts a human can inspect.

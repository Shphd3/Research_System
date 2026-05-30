# Research Documentation

Use this reference when writing or revising research artifacts.

## Two Documents

Separate the clean current theory from the research history:

```text
current-state document:
  latest problem definition, priors, model, implementation contract,
  falsification plan, evidence, claim boundary, and current uncertainty

iteration ledger:
  append-only record of conjecture -> operationalization -> profiling
  -> result -> interpretation -> goal audit when needed -> conjecture update
```

The current-state document should be rewritten as understanding improves. The
iteration ledger should preserve what was tried and what it falsified.

Do not bury failed operationalizations inside the current model. Keep them in
the ledger as evidence about what was tested and why it failed.

## Testable Argument

For a nontrivial research problem, write:

```text
conjecture
task input and output
core difficulty
physical priors
mathematical model for each prior
implementation stage for each model
experiment that can falsify the priors
conjecture update from the result
```

Useful subsection shape:

```text
Objective
Physical prior
Model
Implementation contract
Evidence
Boundary
Next decision
```

## Iteration Record

For each iteration, record:

```text
Conjecture
Physical parameterization
Operationalization
Profiling plan
Result
Interpretation
Conjecture update
Next uncertainty
```

If an experiment tests only one operationalization of a broader prior, say so.
A failed proxy should not be written as a failed prior unless profiling rules
out the broader prior.

## Equation And Parameter Rules

Every equation must map to:

```text
physical prior
model variable
implementation stage
experiment or profiling artifact
```

Every important hyperparameter must have:

```text
name
value
definition
reason for this value
effect if too low or too high, when useful
```

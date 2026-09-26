# Learnable Research Design Contract

Use this contract only when the active anchor fits a parameterized model from
data. It adapts selected learnable-model safeguards from the advisor's
`research-exploration` method to the Research_System anchor-first workflow.

## Contents

1. Design order
2. Data construction and provenance
3. Learning task
4. Training objective
5. Architecture and inductive bias
6. Optimization and selection
7. Confirmation boundary
8. Anchor gate

## Design Order

Resolve and audit the blocks in this order:

```text
data construction
-> learning task
-> training objective and constraints
-> model / architecture
-> optimization and checkpoint selection
-> inference and untouched confirmation
```

Later blocks may expose a problem in an earlier block. Reopen the earliest
affected block instead of patching the later block around it.

## Data Construction And Provenance

State at anchor level:

```text
source population or generating process
unit of one example
sampling and filtering logic
transformations and candidate construction
target, label, or pseudo-label provenance
permitted and forbidden fields
known selection bias or distribution shift
principle separating training, development, and confirmation evidence
model-independent construction checks
```

The anchor owns why this construction tests the research question. Exact file
versions, manifests, seeds, and commands belong to `protocol.md`.

## Learning Task

Define the task independently of the architecture:

```text
permitted input
required output or decision
prediction unit and scope
target semantics
allowed supervision
refusal, invalid, or no-answer behavior
why task success would address the anchor question
what task success would not establish
```

If the task cannot be stated without naming one architecture, the task is
underspecified or the architecture has been mistaken for the question.

## Training Objective

State the exact optimized quantity, likelihood, posterior, or constrained
objective. Define each term, coefficient, aggregation, normalization, and hard
constraint. Trace every term to the learning task and a named prior.

Audit shortcuts such as constant or collapsed output, target copying,
identity memorization, privileged-field access, future-data leakage, scale or
coordinate ambiguity, and one term dominating because of units or counts.
Desired properties and evaluation metrics are not automatically trainable
objectives.

## Architecture And Inductive Bias

State the minimal function family needed to realize the task and objective:

```text
input encoding
components and information flow
capacity, dimensions, and sharing
hard constraints and their enforcement
prior-to-inductive-bias rationale
frozen engineering choices versus scientific choices
remaining architecture-specific failure mode
```

A convenient or familiar architecture is a baseline, not evidence for a
mechanism. Keep the rationale concise when the architecture is not the active
uncertainty.

## Optimization And Selection

At anchor level, freeze the optimization class, admissible stopping and
checkpoint-selection information, and the reason these choices do not use
confirmation truth. Put exact schedules, resource settings, and launch details
in the Protocol.

## Confirmation Boundary

Separate four information roles:

- `OPERATIONAL`: fields available when the frozen system is used;
- `TRAIN`: contributes gradients, fitting, or pseudo-label construction;
- `DEVELOPMENT`: selects a checkpoint or operating point;
- `CONFIRMATION`: remains untouched until the model and decision rule freeze.

The same example or label cannot both fit and independently confirm the same
claim. Evaluation-only truth must not enter candidates, gradients, fitting,
checkpoint selection, thresholds, or per-example decisions.

## Anchor Gate

- `PASS`: all applicable blocks are explicit, mutually consistent, and mapped
  to sections 2, 4, 5, and 6 without run-level clutter.
- `FAIL`: a block is missing, two blocks are conflated, confirmation truth can
  leak upstream, or the architecture precedes an undefined task or objective.
- `NOT APPLICABLE`: the active anchor uses only a fixed diagnostic or
  deterministic computation and fits no parameters.

Do not request a run-ready Protocol while this gate is `FAIL`.

## Section Ownership

Keep their ownership explicit:

- section 2 owns claims about the external data-generating process;
- section 4 owns the learning task, exact objective, variables, and constraints;
- section 5 owns the constructible data pipeline, architecture,
  objective-to-computation map, optimization class, and inference path;
- section 6 owns only the smallest falsifier and necessary guards.

Do not let the Protocol invent a missing task, supervision source, objective,
or scientific architecture rationale. If any design block is unresolved, mark
the anchor insufficient and keep the next decision on that block.

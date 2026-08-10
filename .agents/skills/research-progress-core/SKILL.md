---
name: research-progress-core
description: "Use when the user asks to audit a research judgment, separate rival explanations, design a minimal falsifier, interpret a result boundary, analyze a failure, or close one bounded problem as a knowledge update. Do not use for project paths, meeting synthesis, document schemas, remote operations, or publication."
---

# Research Progress Core

Research progress means reducing one important uncertainty. Prefer the shortest
loop that can change a judgment:

```text
judgment -> rival -> minimal test -> direct result -> updated boundary -> decision
```

Use a mathematical model or multi-stage implementation only when the question
requires it.

## Fast Human-AI Loop

The human owns the judgment and approval. AI owns retrieval, logic audit,
formalization, implementation detail, execution, and evidence bookkeeping.

At the start, obtain:

```text
current judgment
reason or mechanism
strongest rival or uncertainty
evidence that would change the judgment
next decision
```

`Unknown` is valid. Propose missing definitions or tests as AI proposals; do
not silently replace the human judgment.

Use this workflow:

```text
one problem and its current judgment
-> identify one blocking issue
-> approved Protocol only if an experiment is needed
-> execute
-> AI records evidence
-> human states result and boundary from memory
-> AI verifies
-> human states the knowledge update
-> update the smallest owning artifact and, when bounded, its problem focus
```

After execution, ask the human to state:

```text
question
direct result
updated judgment
cannot claim
next decision
```

Verify the statement without strengthening it.

## One Advancement Point

Keep one decision per substantial session:

```text
By the end of this session, make [one relation] clear enough to decide
[one decision], with completion defined by [one inspectable criterion].
```

Reading, coding, running, and plotting are activities. They count as progress
only when they change a judgment, boundary, or decision.

Use at most three genuinely different candidates in one divergent round. Then
choose one and park the rest.

## Problem Knowledge Update Focus

When one problem reaches a bounded answer, create
`daily_research_reports/MMDD/focus_<problem>.md` from
`templates/research_process/focus_writing_template.md`. Several problems may
close on one day; no closure means no invented focus conclusion. Leave legacy
bare `focus.md` files unchanged.

This artifact is a **knowledge update, not an experiment-result analysis**.
The researcher first writes or explicitly approves several connected, natural,
complete sentences saying what is now understood. Those sentences must be
readable without run IDs, metric tables, pass/fail labels, or the Protocol.
Until that judgment exists, use `AWAITING_HUMAN_JUDGMENT`; AI must not derive a
stronger conclusion from the results.

Put the results below the knowledge update and use them to explain it:

```text
decisive comparison
-> verified direct result
-> why that result changes the prior understanding
-> strongest remaining rival and cannot-claim boundary
```

Define a metric in plain language before naming it or citing its value. Keep
only the minimum result and one decisive local figure or table needed to
separate the main explanation from its rival; link full evidence to
`summary.md` or `detailed.md`. The flowchart must reconstruct the inference in
plain language, and the final section must contain exactly one next decision,
its completion criterion, and resume action.

The human owns the question, knowledge update, mechanism, boundary, and next
decision. AI may verify facts and links, explain the decisive visual, draft the
flowchart, and expose one blocking ambiguity. Route meeting synthesis to
`meeting-outline-writer`; do not merge several problem focuses through this
skill.

## Decide Whether Work Is Worth Doing

Before opening a new branch of work, ask:

```text
affects hypothesis?
affects claim boundary?
affects next decision?
```

Pursue only if at least one answer is yes. Park plausible but non-decisive work;
ignore unrelated work.

Before proposing a method, classify the move:

```text
root-cause audit
metric audit
proxy or operationalization test
method construction
robustness or scale check
```

Do not start with method construction unless evidence identifies what the
method must control. A useful method proposal names:

```text
phenomenon
mechanism belief
controlled term
rival separated
primary metric
falsifier
allowed claim
remaining uncertainty
```

If these are unclear, reduce the method to a diagnostic or park it.

## Learnable-Experiment Uncertainty Gate

Before proposing or repairing a learnable experiment, locate the one primary
uncertainty:

```text
data construction  source population, sampling, transformation, target provenance
learning task      what permitted input must produce which output
training objective exact optimized quantity and constraints
architecture       function family and inductive bias
optimization       update rule, schedule, stopping, and checkpoint selection
evaluation         untouched evidence and the decision metric
```

Use the causal order `data construction -> learning task -> training objective
-> architecture -> optimization -> evaluation`. Architecture may be a simple
frozen baseline, but it is not scientifically settled while the task or
objective remains undefined. Do not repair an uncertainty in one block by
silently changing another.

Route research-design uncertainty to the current anchor through
`problem-anchor-writer`. Route exact run conditions to `experiment-card-writer`
only after the anchor-level blocks are coherent. Keep exactly one next decision
focused on the first unresolved block.

## Experiment Contract

Do not run a nontrivial experiment without an approved `protocol.md`.

Use `experiment-card-writer` to write the complete candidate directly into
`protocol.md` as `DRAFT_NOT_EXECUTABLE`, then surface only decision-critical
items for review. The draft may contain exact candidate settings but cannot
authorize action. Promote it only after every block is confirmed and
cross-block consistency passes.

The first page is the user's approval surface and must state:

```text
decision question
hypothesis and strongest rival
treatment and control
what changes and what stays fixed
primary metric
pass / fail / insufficient
cannot claim
approval scope: Protocol / implementation / smoke / full run
```

Put algorithms, parameters, commands, seeds, profiling, artifact paths, and
debug checks after the approval page. Add a condition or diagnostic only when
it separates a named rival or protects the primary conclusion.

Before full run, verify:

```text
approved conditions match implementation
smoke validates data, hooks, replay, and outputs
thresholds and checkpoint rules are frozen
test data does not guide tuning
result paths preserve reproducibility
```

## Evidence And Interpretation

Audit Protocol compliance before interpreting:

```text
all registered conditions completed?
primary metric exists?
hard gates applied?
seeds and checkpoints recorded?
known-good, known-bad, and confusing cases reviewed?
```

If compliance fails, record incomplete evidence; do not update the claim as if
the experiment were decisive.

Separate:

```text
observation: directly measured
interpretation: suggested explanation
claim: safest current statement
speculation: untested possibility
boundary: what evidence cannot support
decision: what happens next
```

For each result, present:

```text
question
key comparison
direct result
conclusion
cannot claim
next decision
```

Return requested numbers and run status first.

## Metrics, Terms, And Figures

Define any non-obvious term before using it as evidence:

```text
plain meaning
concrete object or computation
unit or formula
decision role
what it cannot prove
```

A primary metric must distinguish the hypothesis from its strongest rival.
Name important false-positive and false-negative costs when asymmetric.

Keep only decision-relevant figures. Every central figure must make clear:

```text
question
metric and unit
data and aggregation
axes and legend
allowed conclusion
limitation
```

Read `references/profiling_and_evidence.md` for complex evidence or figure
design.

## Failure And Goal Audit

When a result fails, first localize whether it is:

```text
prior failure
model failure
proxy or operationalization failure
implementation failure
metric failure
```

Test the smallest candidate bottleneck before changing the method. A negative
result is progress when it removes an explanation.

Audit the goal when several reasonable attempts fail similarly or the metric
does not match the downstream decision. Read:

- `references/failure_decomposition.md` for multi-stage failures;
- `references/goal_audit.md` for metric or objective mismatch;
- `references/algorithm_specification.md` for fragile multi-stage algorithms.

## Artifact Ownership

Use the smallest necessary artifact:

```text
focus_<problem>.md self-contained problem knowledge update and result explanation
focus_meeting_<topic>.md concise progressive meeting knowledge update; owned by meeting-outline-writer
Thinking Card new, unformed mechanism judgment only
anchor        current formal question and claim boundary
protocol.md   approved experiment contract
summary.md    concise result and decision
detailed.md   complete evidence and reproducibility ledger
story         explicit line-level synthesis only
```

Do not duplicate the same conclusion across new daily cards, briefs, closure
reports, or implementation plans. Update the owning artifact and link it.

Use `research-mainline` for paths and publication rules,
`problem-anchor-writer` for anchors, and `experiment-card-writer` for Protocol
and result records. Use `remote-experiment-workflow` only for execution
logistics.

## Writing Rule

Write decision reports, not timelines. Start with:

```text
what is established
what the experiment shows
what happens next
```

Then state the boundary. Do not use polished prose to conceal an undefined
object or upgrade a claim.

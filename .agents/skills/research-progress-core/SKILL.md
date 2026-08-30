---
name: research-progress-core
description: "Use when the user asks to maintain one meeting-cycle core-task Focus, audit a research judgment, separate rival explanations, design a minimal falsifier, interpret a result boundary, analyze a failure, or write the delayed reader-friendly daily report after the human result exists. Do not use for project paths, meeting synthesis, remote operations, or publication."
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
group meeting or explicit research reset
-> one active two-day core-task Focus per explicitly active workstream
-> researcher confirms the core question and four-element experiment accounts
-> approved Protocol only if an experiment is needed
-> execute
-> AI records evidence
-> human states result and boundary from memory
-> AI verifies
-> human completes the actual result in the Focus
-> AI writes the reader-friendly daily report only after that result is complete
-> human confirms or corrects that report
-> update the smallest owning artifact and close the cycle
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

## One Meeting-Cycle Advancement Point

Keep one active decision from one group meeting to the next, normally a two-day
cycle:

```text
By the end of this session, make [one relation] clear enough to decide
[one decision], with completion defined by [one inspectable criterion].
```

Reading, coding, running, and plotting are activities. They count as progress
only when they change a judgment, boundary, or decision.

Use at most three genuinely different candidates in one divergent round. Then
choose one. The active Focus should contain one self-contained core experiment
and may contain at most three only when each is necessary for the same core
answer. Supporting controls remain inside the core experiment. Park only key
future direction questions; ignore minor tangents.

Focus creation is human-gated. Never create or reset a Focus because a task
adds an experiment, control, diagnostic, replication, failure analysis, result
interpretation, or report. Keep those under the owning Focus when they answer
its core question. Create or reset a Focus only after the researcher explicitly
declares an independent core question active for a new meeting cycle and
confirms its stable `problem_key` and one next decision.

## Reader-Friendly Daily Report

After eligible evidence exists and the researcher has completed or explicitly
confirmed the direct result, boundary, knowledge update, and one next decision
in the active Focus, create or update:

```text
daily_research_reports/MMDD/docs/daily_report_<topic_slug>.md
```

Use `templates/research_process/daily_report_template.md`. The daily report
is a compact, problem-driven paper: it reconstructs one argument from the
human-owned question to one bounded knowledge update. It is not a run ledger,
a multi-depth repetition of the verdict, or a replacement for canonical result
records. Do not create even an AI-draft placeholder before the Focus reaches
`HUMAN_RESULT_CONFIRMED`.

Use this positive recipe in order:

```text
question-form title + provenance metadata
-> one short abstract: question, method distinction, decisive result, boundary
-> human question and why the previous measure cannot answer it
-> task, data splits, statistical unit, and terms
-> method logic and, when gated, one semantic flowchart
-> hypotheses, treatment/control mapping, metrics, and decision rules
-> direct results: what was done, observed, allowed, and limited
-> knowledge update, cannot-claim boundary, exactly one next decision
-> compact canonical source map
```

Use a question-form title without the answer. The abstract is the only early
verdict. After it, the body follows the logical dependency from question to
conclusion once; the conclusion then compresses
the inference without copying the abstract, results table, or boundary list.
Normally use seven main sections and about 2,500--5,000 Chinese characters, or
an equivalent compact length in another language, excluding metadata,
formulas, tables, and sources. Complete definitions take priority over a
mechanical length cap.

Use the project-local Anchor, frozen Protocol, `summary.md`, and `detailed.md`
as canonical sources. Self-contained means the report supplies enough context
to understand and judge the result without chat history; it does not duplicate
the full evidence ledger. Every decision-bearing number, figure, eligibility
label, verdict, boundary, and next decision must match its canonical source.

Define every non-obvious term before its first use in a hypothesis, formula,
table, or figure. A definition states its plain meaning, exact object or
computation, decision role, and main non-claim. Always define TRAIN,
DEVELOPMENT, CONFIRMATION/TEST, episode or other independence unit, condition,
readout/probe, metric unit, control quantile, and uncertainty procedure when
they appear. If the current run reused frozen earlier-split assets, say
explicitly what the current run trained, selected, and did not train or select.

Each method component gets one role: for example location diagnostic, exact
difference, candidate construction, or verdict-bearing held-out test. When
three or more dependent steps or a gate determine whether downstream work is
admitted, embed one Mermaid flowchart with semantic nodes, Pass/Fail paths, and
the current stopping point. A text arrow chain does not substitute for the
requested visual. If the user explicitly requests a flowchart, include one even
when the reasoning is shorter.

Each result block follows one loop:

```text
what was tested -> direct result -> plain-language scale or baseline
-> allowed interpretation -> adjacent limitation
```

Normally use one central result table and no more than two figures that answer
genuinely different evidence clauses. Explain axes, units, intervals, correct
baseline, allowed reading, and limitation beside each figure. Put eligibility
in one short paragraph. Predecessor histories, environment retries, commands,
receipts, hashes, and artifact inventories stay in `detailed.md` unless one
fact changes whether the result is eligible or how it must be interpreted.
Preserve material negative results and uncertainty; never turn `Fail` or
`Insufficient` into optimistic wording.

The report includes the design-level uncertainty contract: independence unit,
aggregation, draw count, primary seed, interval construction, and where a
control quantile is recomputed. Per-seed ledgers, sampled-index arrays, and
retry details remain in `detailed.md`.

Using one meeting note as the named source of one experiment question is not
meeting synthesis. Route to `meeting-outline-writer` only when the task merges
multiple meeting problems or prepares the meeting itself.

After the entry gate is satisfied, keep
`AI_DRAFT_AWAITING_HUMAN_CONFIRMATION` visible until the researcher confirms
the complete story. A draft must not invent or strengthen the researcher's
mechanism judgment.

## Living Core-Task Focus

At the start of a group-meeting cycle, create or audit exactly one
`daily_research_reports/MMDD/focus_<problem>.md` for each explicitly active
workstream from `templates/research_process/focus_writing_template.md`. Leave
legacy bare `focus.md` and historical result-summary Focus files unchanged.

This artifact is the **living human-owned task card**, not a Protocol or result
ledger. It contains one core question and one to three experiments. Each
experiment has exactly four elements:

```text
1. purpose: the part of the core question resolved and why this test is needed
2. hypothesis: predicted contrast, strongest rival, and separating observation
3. analysis method: one to three plain-language items; each says what is done,
   what is compared, and why the comparison answers the question
4. conclusion: before execution, possible result branches and how each changes
   later experiments; after execution, direct result, bounded conclusion, and
   effect on the Focus
```

After all current experiment blocks are interpreted, the researcher adds the
Focus-level knowledge update, cannot-claim boundary, and exactly one next
decision. AI verifies those fields
against canonical evidence without strengthening them. Put formulas, exact
hyperparameters, statistical details, tables, figures, evidence lineage, and
run history in the owning Anchor, Protocol, Summary, Detailed, and delayed
daily report.

**REQUIRED WRITING STANDARD:** Use `research-document-explainer` to calibrate
the Focus's plain-language experiment account. Apply its reader order and
terminology contract: define the object before its alias or symbol, state why a
step exists before how it is implemented, use natural complete sentences with
one main relation each, and keep direct evidence separate from interpretation.
`research-progress-core` retains ownership of the Focus; the explainer supplies
the writing standard only.

The human owns the question, expected branches, conclusion, mechanism,
boundary, and next decision. Ordinary one-problem meetings use this Focus
directly. Route only an explicitly requested meeting brief, speaking outline,
or multi-problem synthesis to `meeting-outline-writer`.

## Decide Whether Work Is Worth Doing

Before opening a new branch of work, ask:

```text
affects hypothesis?
affects claim boundary?
affects next decision?
```

Pursue only if it is required to close the active core task. If at least one
answer is yes but the work is not currently required, add one concise entry to
the project's `main/parking_lot/README.md` only when it is a key future
direction and has an explicit reopening condition. Ignore minor or unrelated
work without creating an artifact.

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

Before drafting it, require the active Focus's core question and every
experiment's four-element plain-language account to be researcher-confirmed.
The Protocol must implement the same question and
may not expand one core experiment into an unbounded suite. A maximum of three
core experiments is allowed; controls and diagnostics do not count separately
when they only protect one registered verdict.

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

Within a daily report, the whole adjudicated experiment is one result for this
rule. Result subsections give only their direct reading and adjacent limitation;
the global claim boundary and next decision appear once in the conclusion.

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
focus_<problem>.md living meeting-cycle core task and human-owned result account
daily_report_<topic_slug>.md delayed complete reader-friendly story after the human result; derived from canonical evidence
focus_meeting_<topic>.md optional requested meeting brief or synthesis; owned by meeting-outline-writer
main/parking_lot/README.md key non-active future questions and reopening conditions
Thinking Card new, unformed mechanism judgment only
anchor        current formal question and claim boundary
protocol.md   approved experiment contract
summary.md    concise result and decision
detailed.md   complete evidence and reproducibility ledger
story         explicit line-level synthesis only
```

The Focus is the single short cycle surface; the subject-bearing
`daily_report_<topic_slug>.md` is the one full reader-facing story after the
human result exists. Do not create additional daily cards, briefs, closure
reports, or implementation plans that duplicate either role. Neither replaces
`summary.md` or `detailed.md` as a truth source.

Use `research-mainline` for paths and publication rules,
`problem-anchor-writer` for anchors, and `experiment-card-writer` for Protocol
and result records. Use `remote-experiment-workflow` only for execution
logistics.

## Writing Rule

Write decision reports, not timelines. The abstract starts with:

```text
question -> decisive result -> bounded answer -> next decision
```

The body then reconstructs `question -> definitions -> test -> result ->
inference` in that order. Do not use polished prose to conceal an undefined
object or upgrade a claim.

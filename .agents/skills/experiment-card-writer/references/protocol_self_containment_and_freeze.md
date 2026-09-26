# Protocol Self-Containment And Freeze Contract

Use this contract for every new, reopened, promoted, or amended
`protocol.md`.

## Contents

1. [Ownership boundary](#ownership-boundary)
2. [Cold-reader approval gate](#cold-reader-approval-gate)
3. [Grounding and no-invention rule](#grounding-and-no-invention-rule)
4. [Approval snapshot](#approval-snapshot)
5. [Protocol structure](#protocol-structure)
6. [Scientific stage contract](#scientific-stage-contract)
7. [Frozen analysis plan](#frozen-analysis-plan)
8. [Preflight, smoke, and scale-up](#preflight-smoke-and-scale-up)
9. [Frozen choices and provenance](#frozen-choices-and-provenance)
10. [Freeze and amendment lifecycle](#freeze-and-amendment-lifecycle)
11. [Final audit](#final-audit)

## Ownership Boundary

The Protocol is a self-contained **approval and execution contract**. It must
let a cold reader decide whether the proposed experiment is aligned,
interpretable, constructible, and safe to execute.

It does not own the full research design. Link the Anchor for complete physical
priors, mathematical derivations, and line history. Restate only the local
meaning needed to approve this experiment.

The Protocol owns:

- the tested Anchor clause and strongest rival;
- treatment, controls, held-fixed variables, and confirmation boundary;
- exact data, task, architecture, objective, and execution choices;
- primary analysis and verdict rules;
- stage operations, stop rules, expected artifacts, and approval state.

Classify the experiment as one of:

```text
root-cause audit
metric audit
operationalization or proxy test
method construction
robustness check
```

Method construction is not an admissible first move unless the Anchor already
contains a supported mechanism or metric target. The role must explain what
kind of uncertainty is reduced; it is not a decorative label.

It does not own observed results, result interpretation, an updated claim, or
a result-derived next research decision. Those belong to `summary.md`,
`detailed.md`, and the updated Anchor.

## Cold-Reader Approval Gate

Without chat history, code inspection, or opening a link, a reader must be able
to answer:

1. What one uncertainty does this experiment resolve?
2. Which exact Anchor claim, prior, model term, or falsifier can it change?
3. What are treatment, control, changed variable, and held-fixed variables?
4. What is the strongest rival, and which condition or guard separates it?
5. What enters each stage, what operation occurs, and what output is expected?
6. What primary metric and analysis rule determine Pass, Fail, or Insufficient?
7. What preflight and smoke evidence is required before scale-up?
8. What execution scope is approved, and what remains unauthorized?
9. Where will intermediate, final, and failure artifacts be written?
10. What can the experiment not claim even if it passes?

If an answer depends on an unexplained ID, inherited private context, or a bare
link, the Protocol is not approval-ready.

## Grounding And No-Invention Rule

Every decision-bearing item must come from one of:

```text
APPROVED_ANCHOR       approved research question, metric, falsifier, boundary
HUMAN_CONFIRMED       explicit researcher decision recorded in the ledger
VERIFIED_SOURCE       existing code, data, configuration, or evidence inspected
AI_PROPOSAL           candidate choice awaiting confirmation
UNKNOWN_OR_BLOCKED    missing information that prevents promotion
```

Do not silently invent a dataset, threshold, split, seed, architecture value,
resource limit, stop rule, expected effect, or evidence source. Label a useful
candidate `AI_PROPOSAL`; label a required missing choice `BLOCKED`.

State the local meaning first, then link its source. A filename, run ID, config
name, or Anchor label cannot substitute for an explanation.

## Approval Snapshot

Link the confirmed active Focus. Preserve its question, purpose, at-most-three
plain-language analysis steps, completion rule and supporting/non-supporting/
insufficient branches. Explain technical labels locally; links support audit.

For a training Protocol, read and apply the repository's
`docs/training_observability_contract.md`: freeze effective global batch,
valid-token counting, loss reduction, token budget/checkpoints/schedules,
TensorBoard directory and required tags. Optimizer-update comparisons require
equal effective tokens/update; otherwise compare cumulative valid prediction
tokens. A different batch is unmatched unless it is the registered variable.

Put this compact snapshot first:

```text
Document status:
Approval status:
Block audit status:
Cross-block consistency:
Execution scope approved:
Design frozen at / registered revision:
Purpose:
Primary Anchor:
Confirmed active Focus:
Anchor decision question:
Anchor physical prior tested:
Anchor core model term tested:
Anchor falsifier:
Experiment role:
Primary metric from Anchor:
Claim boundary from Anchor:
Minimal setup:
Treatment and controls:
Changed variable:
Held fixed:
Conditions to run:
Pass:
Fail:
Insufficient:
Cannot claim:
Approval decision:
```

Keep it short. If the mechanism cannot be understood without a broad condition
table, return to the Anchor and split the question.

## Protocol Structure

New or reopened Protocols should keep this audit order. Existing frozen
Protocols need not be reformatted.

```markdown
# Protocol: <experiment_id>

## 0. Approval Snapshot
## 1. Terminology / Definitions
## 2. Anchor Alignment
## 3. Tested Hypothesis
## 4. Rival Explanations
## 5. Data Construction And Provenance
## 6. Learning Task And Permitted Supervision
## 7. Model / Architecture And Frozen Variants
## 8. Training Objective And Optimization
## 9. Conditions, Seeds, And Checkpoints
## 10. Primary Metric And Frozen Analysis Plan
## 11. Secondary Metrics And Guards
## 12. Known Good / Known Bad / Known Confusing Cases
## 13. Scientific Procedure And Stage Contracts
## 14. Algorithm, Output, And Provenance Contract
## 15. Success / Failure / Insufficient Evidence
## 16. What This Cannot Claim
## 17. Block Confirmation, Freeze, And Amendment Ledger
```

Define non-obvious terms, abbreviations, condition labels, symbols, and metrics
before using them for approval. A metric definition must include computation,
unit, decision role, and what it cannot prove.

Register every condition or diagnostic:

| Item | Anchor clause | Model term or rival | Why needed | Evidence role | Pass | Fail | Insufficient | Artifact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | |

Do not include an item merely because it is easy to run.

## Scientific Stage Contract

Describe the experiment in causal execution order. Merge stage profiling and
algorithm meaning so the reader does not need to cross-reference two plans.

| Stage | Goal | Input and assumptions | How | Why | Expected output | Pass / fail / insufficient | Named failure | Artifact | Handoff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | | |

- **Goal** names the uncertainty resolved at that stage.
- **How** states the exact operation and decision-bearing parameters.
- **Why** traces the operation to the Anchor prior, model term, rival, or
  validity guard.
- **Expected output** states the schema or observable, not the hoped-for result.
- **Named failure** distinguishes measurement, data, implementation, metric,
  and scientific failure.
- **Handoff** names what the next stage receives and what cannot proceed.

For a nontrivial algorithm, also freeze inputs, parameters, intermediate
variables, ordered steps, outputs, debug artifacts, refusal/break behavior,
and failure reasons. Do not use “fit,” “stable,” “valid,” or “match” without
the exact computation or test.

## Frozen Analysis Plan

The primary metric section must freeze:

```text
estimand or decision quantity
concrete computation and unit
unit of observation
unit of independence
aggregation levels and weights
uncertainty interval or test
one-sided or two-sided rule
multiplicity handling, when applicable
missing, failed, excluded, and outlier handling
checkpoint or operating-point selection
development versus untouched confirmation use
Pass, Fail, and Insufficient mapping
false-positive and false-negative costs when asymmetric
analysis script / revision / output table
unsealing point after which the rule cannot change
```

Secondary metrics cannot rescue a failed primary result unless the Protocol
registered a typed outcome that explicitly permits that interpretation.

## Preflight, Smoke, And Scale-Up

Use the smallest evidence needed before expensive execution:

```text
model-independent data and schema preflight
known-good case
known-bad case
known-confusing case
implementation identity or no-op check
small smoke with exact acceptance and stop rules
artifact completeness check
resource and runtime ceiling
criterion that permits scale-up
```

Passing a smoke proves only the registered smoke properties. It does not
authorize a full run or scientific claim. Record distinct authorization scopes for implementation, smoke and full
execution. Reuse explicit scope approval already given; do not add a fresh
approval turn for each phase or for local checks exempt under root rules.

## Frozen Choices And Provenance

Every outcome-changing choice must be fixed, part of a frozen sweep with a
selection rule, or `BLOCKED`.

Use a compact registry when choices are numerous:

| Choice | Value or range | Scientific or engineering | Grounding source | State | Reopens |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Record enough provenance to distinguish the intended design from the actual
execution:

```text
Anchor revision
Protocol registered revision or scientific-body hash
code revision and dirty-state policy
configuration revision
data / manifest identity
environment or image identity
randomness and seeds
resource profile and ceiling
expected artifact roots
```

Absolute commands and paths may live here when required for execution, but do
not let them replace the scientific procedure.

## Freeze And Amendment Lifecycle

Before execution:

```text
DRAFT_NOT_EXECUTABLE
-> all A-G confirmed and consistency PASS
-> DESIGN_CONFIRMED_NOT_EXECUTABLE
-> explicit APPROVED_FOR_<SCOPE>
```

At the first execution approval, record `design_frozen_at` and a registered
revision or hash for the scientific body and decision-bearing configuration.

After execution starts, preserve the registered body. Permitted updates are:

- execution status and receipts;
- links to `summary.md` and `detailed.md`;
- an append-only amendment.

An amendment must record:

```text
amendment id and time
before value
after value
reason
whether any data or result was already visible
affected blocks and conditions
approval
result eligibility impact
```

Never overwrite the old value. A post-start change to data, supervision,
objective, architecture, condition logic, metric, threshold, exclusion,
stopping, or confirmation boundary is scientifically material unless proven
otherwise. Mark affected evidence `INELIGIBLE` or bound its claim explicitly.

Do not write observed results, interpretation, final claim, or a new research
direction into the registered body. The Protocol may point to result records.

## Final Audit

Mark each item `PASS` or `FAIL` before promotion or execution:

```text
Anchor question and claim boundary are unchanged:
Every decision-bearing choice is grounded, proposed, or blocked:
Approval snapshot is understandable without links:
Treatment, controls, changed variable, and held-fixed variables are explicit:
Every stage has Goal / Input / How / Why / Output / status / artifact / handoff:
Primary analysis is frozen and yields one verdict mapping:
Preflight and smoke gates protect scale-up:
Confirmation truth cannot leak into fitting or selection:
Artifacts and provenance can be audited:
A-G are confirmed and cross-block consistency passes:
Only the named execution scope is approved:
The post-start freeze and amendment rule is recorded:
```

Any `FAIL` prevents promotion or execution.

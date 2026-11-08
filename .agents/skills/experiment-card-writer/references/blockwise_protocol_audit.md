# In-File Draft-First Protocol Audit

Use this audit while writing and approving the single canonical `protocol.md`.
Write the complete candidate into the file first, then surface its important
decisions for review and verify that the confirmed blocks form one experiment.

## Contents

1. Document and block status
2. Audit blocks
3. Write first, then surface review
4. Cross-block consistency audit
5. Protocol promotion and execution approval
6. Change control
7. Post-start freeze boundary

## Document And Block Status

Use these document states:

- `DRAFT_NOT_EXECUTABLE`: the full candidate exists, but one or more blocks
  remain proposed, blocked, reopened, or inconsistent;
- `DESIGN_CONFIRMED_NOT_EXECUTABLE`: all blocks and consistency checks passed,
  but no execution scope is approved;
- `APPROVED_FOR_<SCOPE>`: only the named scope is authorized, such as
  implementation, smoke, or full run.

Use these block states:

- `PROPOSED`: the file contains a candidate not yet confirmed;
- `BLOCKED`: required information or judgment is missing;
- `CONFIRMED`: the researcher explicitly accepted the block after AI audit;
- `REOPENED`: a later correction invalidated the earlier confirmation.

One reply may explicitly confirm one, several, or all blocks. Silence or an
ambiguous acknowledgment does not confirm a block. AI may diagnose an
inconsistency but cannot replace the researcher's confirmation.

## Audit Blocks

### A. Question And Claim Boundary

Confirm the anchor clause, tested hypothesis, strongest rival, primary
falsifier, allowed claim, cannot-claim boundary, and experiment role.

### B. Data Construction And Provenance

Confirm source population, example unit, sampling and filtering, transforms,
target provenance, permitted and forbidden fields, split principle, leakage
guards, model-independent checks, and known distribution shift.

### C. Learning Task And Supervision

Confirm permitted input, required output, prediction unit, target semantics,
supervision source, invalid/refusal behavior, and why task success bears on the
anchor question.

### D. Model And Architecture

Confirm input encoding, components, information flow, sharing, dimensions,
hard constraints, frozen variants, scientific rationale, and engineering-only
choices. Do not confirm this block while the task or objective is undefined.

### E. Training Objective And Optimization

Confirm the exact objective terms, weights, normalization, constraints,
shortcut controls, optimizer class, schedule, stopping, development data, and
checkpoint-selection rule. Trace every objective term to Block C and the
anchor model.

### F. Comparison And Decision Evidence

Confirm treatment, controls, held-fixed variables, primary metric, guards,
pass/fail/insufficient meanings, known good/bad/confusing cases, required
figures or tables, and the rival separated by each condition.

For fitted or sampled comparisons, separate independent source units from
bootstrap or gradient-resampling counts. A finite-library mean is an empirical
reference, not an exact population gradient. Record post-freeze selections as
exploratory. Non-significance does not establish equivalence; an equivalence
claim needs a justified, predeclared margin and an appropriate interval/test.

#### Mechanism Substitution Controls

When method A is hypothesized to improve outcome Y through mediator M, consider
a different operation B that changes M, and an A variant that changes the method
without improving M. Choose feasible controls that resolve the priority unknown;
do not turn this into a mandatory extra experiment suite. Define M independently
of Y and predeclare its measurement, comparison and matching rule. Do not select
variants for favorable evaluation outcomes or assume M failed to improve without
measuring it. State which possible observations support, weaken or still fail to
distinguish the mechanism, and how each changes the next decision.

If A and B produce comparable M and predicted Y changes, this supports a common
explanation but does not uniquely identify mediation. If an A variant retains
the outcome improvement despite no measured M improvement, the simple M-only
account is weakened, subject to measurement sensitivity and other changed
factors. Losing the outcome benefit when M improvement is prevented supports
the explanation only as far as those other factors are controlled. If B
cannot match the relevant M or other loss-relevant changes, report the remaining
ambiguity rather than claiming the mechanism was refuted.

For routing versus batch construction, specify the same checkpoint, parameter
block, target evaluation path, gradient mean/variation and subsequent validation
loss. Account for data exposure, expert load, gate weights, loss normalization,
compute, update count and initial optimizer state. Record what is matched and
what cannot be matched simultaneously. Gradient accumulation is a distinct
operation; token correlations, rescaling, optimizer steps and routing changes
can break equivalence. A local comparison does not identify a long-run cause.

### G. Execution And Reproducibility Boundary

Confirm seeds, checkpoints, smoke boundary, resource ceiling, expected
artifacts, failure-stop conditions, code/config ownership, result paths, and
which approval scopes may later be granted. AI may write candidate commands and
configuration into the draft, but they remain non-executable proposals.

## Write First, Then Surface Review

Before asking for confirmation, create or update the complete `protocol.md`
covering A-G. Fill every grounded field, label inferred choices as assumptions,
mark missing human judgment `BLOCKED`, and set the document state to
`DRAFT_NOT_EXECUTABLE`. Do not create `protocol_draft.md`, an implementation
plan, or a chat-only competing draft.

After the file is written, return a compact review extract:

```text
File written:
Document state:
Decision-critical items:
- [block] proposed decision — why it needs review
AI-detected inconsistency:
Blocked or assumed item:
What confirmation would promote:
A-G status ledger:
```

Surface an item when changing it would alter the hypothesis, claim boundary,
data or supervision boundary, task, objective, scientific architecture choice,
primary comparison or metric, pass/fail/insufficient rule, resource ceiling, or
execution scope. Leave routine details in the file unless they are inconsistent
or blocked.

Invite the researcher to `CONFIRM`, `CORRECT`, or `BLOCK` any subset in one
reply. An equally unambiguous natural-language confirmation is valid; no magic
keyword is required. Confirmation of a named block freezes every clearly
listed point unless the researcher excludes one.

After a reply, update the file first, apply all corrections together, reopen
affected dependencies, and show only changed decision-critical items plus the
updated ledger. Do not paste the full file into chat unless requested.

## Cross-Block Consistency Audit

After A-G are individually `CONFIRMED`, verify all of these:

```text
data construction exposes the phenomenon named in A
data fields and target provenance obey C's supervision boundary
task input/output is compatible with D's architecture
objective optimum represents success on C rather than a shortcut
architecture and optimizer can realize every objective term and constraint
treatment and controls change only the registered variables
primary metric distinguishes the hypothesis from the strongest rival
development choices cannot access untouched confirmation truth
resources, stop rules, and artifacts can execute every registered condition
pass/fail/insufficient rules yield one unambiguous claim-boundary update
```

If any check fails, update the file, mark the earliest affected block
`REOPENED`, and re-audit it and every dependent block. Do not silently change a
confirmed block during promotion.

## Protocol Promotion And Execution Approval

Promote the same `protocol.md` from `DRAFT_NOT_EXECUTABLE` to
`DESIGN_CONFIRMED_NOT_EXECUTABLE` only when:

```text
all blocks A-G = CONFIRMED
cross-block consistency = PASS
no unresolved choice changes the result interpretation
```

At promotion, the candidate conditions, configuration, commands, metrics,
artifacts, and stop rules become the confirmed design. Preserve a compact
confirmation ledger in the file, not the full conversation.

Design confirmation alone does not authorize execution. Record the exact
scope already explicitly authorized in the user request, current session or
owning contract; obtain only genuinely missing approval under the repository
rules. Implementation, smoke, full execution and publication/Git are distinct
scopes, not mandatory separate confirmation turns. Small local checks retain
the root exemption. Never treat silence as new authorization.

## Change Control

Any post-confirmation change to data construction, task, supervision, objective,
architecture, condition logic, primary metric, pass/fail rule, or confirmation
boundary reopens the affected block, downgrades the file to
`DRAFT_NOT_EXECUTABLE`, and invalidates execution approval until the dependent
blocks and consistency audit pass again. Update the Protocol review notes; do
not create a competing execution-plan file.

## Post-Start Freeze Boundary

This reopening rule applies before execution starts. After the first approved
execution begins, preserve the registered scientific body and apply
`protocol_self_containment_and_freeze.md`. Record any material change as an
append-only amendment with its evidence-eligibility impact; never silently
overwrite the pre-run contract.

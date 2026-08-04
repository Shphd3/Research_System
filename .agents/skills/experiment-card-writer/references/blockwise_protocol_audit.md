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

Design confirmation does not authorize execution. Obtain an explicit scope
decision for each requested step: implementation, smoke, full run, and optional
publication or Git action; then record only that scope in the document state.

## Change Control

Any post-confirmation change to data construction, task, supervision, objective,
architecture, condition logic, primary metric, pass/fail rule, or confirmation
boundary reopens the affected block, downgrades the file to
`DRAFT_NOT_EXECUTABLE`, and invalidates execution approval until the dependent
blocks and consistency audit pass again. Update the Protocol review notes; do
not create a competing execution-plan file.

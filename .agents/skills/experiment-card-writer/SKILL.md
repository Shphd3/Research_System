---
name: experiment-card-writer
description: "Write, audit, confirm, and freeze an anchor-aligned protocol.md, then create evidence-grounded summary.md and detailed.md records with explicit provenance and claim boundaries. Use for experiment design, Protocol approval or amendment, result interpretation, or result-record maintenance after the Anchor is clear. Do not redefine the research question, invent missing judgment or evidence, operate remote jobs, or publish artifacts."
---

# Experiment Protocol And Result Writer

Use this skill only after the formal Anchor has one approved decision question,
primary metric, main falsifier, claim boundary, and next decision. The Anchor
owns the research design; this skill owns the experiment contract and evidence
record.

```text
anchor -> protocol.md -> summary.md -> detailed.md -> anchor sections 7-8
```

Store the canonical files together:

```text
Projects/<project>/main/experiments/A<anchor_id>/<experiment_id>/
  protocol.md
  summary.md
  detailed.md
  figures/
  tables/
```

## Mandatory Reference Routing

Read the required references completely before acting:

- For any Protocol draft, revision, confirmation, promotion, or amendment,
  read [blockwise_protocol_audit.md](references/blockwise_protocol_audit.md)
  and
  [protocol_self_containment_and_freeze.md](references/protocol_self_containment_and_freeze.md).
- For any result interpretation, `summary.md`, or `detailed.md` work, read
  [result_evidence_lineage.md](references/result_evidence_lineage.md).
- Before creating or revising `detailed.md`, also read
  [detailed_record_standard.md](references/detailed_record_standard.md).

Do not copy the references into the output. Apply their contracts in the
canonical files.

## Hard Gates

### 1. Anchor Alignment

Do not let the Protocol invent or redefine the research question, physical
prior, mathematical target, primary metric, falsifier, or claim boundary. If
the Anchor does not determine one of them, stop and return the missing decision
to `problem-anchor-writer`.

Every added condition, seed, checkpoint, diagnostic, or figure must either
separate a named rival explanation or protect the validity of the primary
conclusion. Park everything else.

### 2. Draft First, Then Review

Write the complete candidate directly into the single canonical `protocol.md`
as `DRAFT_NOT_EXECUTABLE`. Do not create a chat-only draft, a second Protocol,
or a separate implementation plan.

Cover audit blocks A-G, label unsupported choices `PROPOSED`, mark missing
judgment `BLOCKED`, and surface only decision-critical items for researcher
review. Silence is not confirmation.

Promote the same file to `DESIGN_CONFIRMED_NOT_EXECUTABLE` only when every
block is `CONFIRMED`, cross-block consistency is `PASS`, and no unresolved
choice can change interpretation.

### 3. Self-Contained Approval Contract

Require a short approval snapshot before the audit layer. A cold reader must be
able to state, without opening a link:

- the one uncertainty and Anchor clause tested;
- treatment, control, changed variable, and held-fixed variables;
- the primary metric and registered analysis rule;
- Pass, Fail, and Insufficient meanings;
- the smallest approved execution scope;
- what the experiment cannot claim.

Require a constructible stage contract, frozen analysis plan, preflight/smoke
boundary, failure-stop rules, and artifact destinations. Links support audit;
they must not carry information needed to approve the run.

### 4. Protocol Freeze And Amendment

Design confirmation does not authorize execution. Obtain explicit approval for
each requested scope such as implementation, smoke, or full run.

At the first execution approval, freeze the scientific body, registered
criteria, and decision-bearing configuration. After execution starts:

- never rewrite the registered hypothesis, conditions, metric, threshold, or
  verdict rule;
- never insert observed results, interpretation, or a result-derived next
  decision into the Protocol body;
- add only execution status, receipts, result links, or an append-only
  amendment with before/after values, reason, timing, and eligibility impact.

Any silent post-start change makes the affected result ineligible.

### 5. Result Grounding And Human Judgment

Never infer a result from a plan, expected pattern, partial log, filename, or
missing artifact. Use `NOT RUN`, `UNKNOWN`, `MISSING`, or `INELIGIBLE` when
that is the verified state.

Before AI writes or revises the conclusion, require the researcher to record:

```text
Question:
Direct result:
Confirmed:
Weakened or rejected:
Current mechanism and reason:
Cannot claim:
Exactly one next decision:
```

AI may verify measurements, evidence lineage, wording, and boundary. It must
not invent the initial judgment or strengthen it beyond the registered rule
and eligible evidence.

### 6. Evidence Lineage

Every decision-bearing number, table, figure, and verdict must trace:

```text
raw artifact
-> computation or transformation
-> aggregation and uncertainty
-> registered criterion
-> observed value
-> verdict
-> bounded claim
```

Record Protocol conformance and every deviation before interpreting results.
An artifact path alone is not evidence lineage.

### 7. Summary And Detailed Ownership

`summary.md` is the shortest complete result reading path. Keep only the
decision-bearing setup, registered rule, direct result, smallest central
evidence, claim boundary, and one next decision with completion criterion and
resume action.

`detailed.md` is the only complete evidence ledger. It owns full setup,
conformance and deviations, evidence lineage, all eligible results, stage and
failure decomposition, run receipts, and the artifact manifest.

The two files may repeat only the primary metric definition, primary observed
value, verdict, claim boundary, and next decision. Those repeated fields must
match exactly. Neither file may claim more than the Anchor permits.

### 8. Visual Evidence

Include a figure only when it supports the current verdict, claim boundary, or
next decision. Define its data source, metric and unit, aggregation, axes and
legend, observed result, allowed conclusion, and limitation before promotion.
Move debug-only figures out of `summary.md`.

### 9. Close The Chain

After eligible evidence and researcher judgment are consistent:

```text
summary.md / detailed.md
-> update Anchor section 7 with the minimum local evidence unit
-> update Anchor section 8 with the bounded claim and one next decision
-> after the human states a bounded knowledge update, create or update
   daily_research_reports/MMDD/focus_<problem>.md
```

`summary.md` and `detailed.md` analyze and preserve experimental results; they
do not themselves constitute the focus conclusion. In the problem focus, the
human-approved knowledge update comes first as natural complete sentences, and
the selected result appears below only to explain it.

Do not create a closure report or line synthesis through this skill. Route an
explicit line-level synthesis to `research-story-writer` and path/state changes
to `research-mainline`.

## Language And Safety

- Write English canonical files first unless the user chooses another
  language; companions must preserve all rules, numbers, and boundaries.
- Use `$...$` and `$$...$$` for Markdown mathematics.
- Do not implement, run, submit, publish, sync, commit, or push through this
  skill without the separate authorization required for that action.

# Result Evidence Lineage Contract

Use this contract when interpreting an experiment or writing `summary.md` and
`detailed.md`.

## Contents

1. [Ownership and no-invention boundary](#ownership-and-no-invention-boundary)
2. [Evidence eligibility](#evidence-eligibility)
3. [Protocol conformance and deviations](#protocol-conformance-and-deviations)
4. [Evidence lineage](#evidence-lineage)
5. [Summary contract](#summary-contract)
6. [Detailed contract](#detailed-contract)
7. [Artifact manifest](#artifact-manifest)
8. [Figure contract](#figure-contract)
9. [Cross-file consistency](#cross-file-consistency)
10. [Final audit](#final-audit)

## Ownership And No-Invention Boundary

The result record must distinguish:

```text
registered expectation
direct observation
derived statistic
interpretation
claim
speculation
boundary
next decision
```

Never turn an expected pattern, partial log, plan, filename, missing run, or
correlated diagnostic into an observed result. Use `NOT RUN`, `UNKNOWN`,
`MISSING`, `INVALID`, or `INELIGIBLE` when appropriate.

The researcher owns the initial result judgment. AI verifies measurements,
sources, consistency, and wording. If the researcher has not provided the
closed-book judgment, present the required scaffold rather than inventing a
conclusion.

`summary.md` owns the first canonical result reading path. `detailed.md` owns
the complete evidence ledger. The Protocol owns the registered plan and must
not be rewritten with result-derived content. A subject-bearing daily report
under `daily_research_reports/MMDD/docs/` may provide a fuller reader
explanation, but it is derived from these canonical records and cannot become
the sole evidence source.

## Evidence Eligibility

Before interpreting a result, classify every decision-bearing condition:

```text
ELIGIBLE       executed under the registered contract and required guards pass
BOUNDED        usable only for a narrower claim because a named deviation exists
INELIGIBLE     cannot adjudicate the registered claim
MISSING        required evidence or artifact does not exist
NOT_RUN        execution never occurred
```

Do not average eligible and ineligible conditions. Do not use secondary or
debug evidence to repair a missing primary result.

## Protocol Conformance And Deviations

Compare the frozen Protocol with actual execution before reading the result:

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Cover at least:

- Protocol revision and approved execution scope;
- data and split identity;
- task and supervision boundary;
- code, configuration, model, objective, and optimizer identity;
- treatment, controls, and held-fixed variables;
- seeds, checkpoints, stop conditions, resources, and completion;
- primary analysis script, aggregation, uncertainty, and verdict rule;
- required guards, tables, figures, and artifacts;
- amendments, retries, exclusions, missing runs, and post-hoc analyses.

Record a deviation even when it appears harmless. State why it does or does not
change eligibility; do not silently call every item `passed`.

## Evidence Lineage

Evidence lineage means that a future reader can reproduce the route from an
artifact to a bounded claim without guessing an intermediate step.

Use one row per decision-bearing result:

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | |

The required chain is:

```text
raw observation
-> validated schema
-> transformation or estimator
-> aggregation and uncertainty
-> registered comparison and threshold
-> observed value
-> typed verdict
-> bounded claim
```

For trajectories, seeds, checkpoints, ablations, or before/after claims,
separate:

- single-observation evidence;
- within-unit change evidence;
- across-unit summary evidence.

Name the independence unit. Layers, tokens, documents, checkpoints, and arms
are not automatically independent experimental replicates.

## Summary Contract

Keep `summary.md` short and conclusion-first. It must be understandable without
chat history but need not reproduce the complete setup.

Use this structure:

```markdown
# Summary: <experiment_id>

Primary Anchor:
Frozen Protocol:
Detailed record:
Result status / eligibility:

## Result Snapshot

Verdict:
What we established:
What the experiment shows:
What we do next:

## Decision-Bearing Setup

Question:
Treatment and control:
Changed variable:
Held fixed:
Primary metric and unit:
Known limitation:

## Verdict Basis

| Registered rule | Observed value | Guard / eligibility | Verdict | Evidence source |
| --- | --- | --- | --- | --- |
| | | | | |

## Key Evidence

## Central Figure, Only When Needed

## Claim Boundary

Can claim:
Cannot claim:

## Next Decision

Decision:
Completion criterion:
Resume action:
```

Define only decision-critical terms. Give the primary result and its source
before supporting diagnostics. Link each decision-bearing table or figure to
its curated source table or lineage row; a final generic link to `detailed.md`
is insufficient.

## Detailed Contract

Apply [detailed_record_standard.md](detailed_record_standard.md) for the full
structure. The detailed record must contain:

- a quick result recap;
- complete terminology and actual setup;
- frozen Protocol identity and conformance/deviation table;
- primary decision rules;
- the full evidence-lineage table;
- eligible results separated from debug, failed, ambiguous, and ineligible
  evidence;
- stage evidence and failure decomposition;
- interpretation, claim boundary, and one next decision;
- complete run record and artifact manifest.

`detailed.md` may be long, but it must be layered. A reader should reach the
verdict and evidence eligibility before the run history.

## Artifact Manifest

An artifact path alone is not an auditable record. Use:

| Artifact | Purpose | Producer / revision | Source inputs | Hash or identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |

Include the frozen Protocol revision, code/config/data identity, primary source
tables, analysis outputs, central figures, job receipts, and required failure
artifacts. Raw logs and checkpoints may remain on the worker surface; link
their manifest rather than copying them into the research mainline.

## Figure Contract

Before promoting a central figure, record:

```text
Anchor question
Protocol question
metric definition and unit
raw data source
aggregation and uncertainty
axis and legend meaning
expected pattern under registered outcomes
observed result
allowed conclusion
what the figure cannot prove
lineage row or source table
Anchor update implication
```

Place only the smallest decision-bearing figure set in `summary.md`. Put full
visual evidence in `detailed.md`; put debug-only figures in a clearly labeled
appendix or omit them.

## Cross-File Consistency

Summary and Detailed may repeat only:

- primary metric definition;
- primary observed value;
- typed verdict and evidence eligibility;
- claim boundary;
- exactly one next decision, completion criterion, and resume action.

These fields must match exactly. Detailed may narrow a Summary claim but must
not strengthen it. The Anchor update may be more compact but must preserve the
same verdict and boundary.

Full setup, all conditions, stage evidence, deviations, run history, and the
artifact manifest belong only in Detailed. Summary may state only the minimum
decision-bearing setup.

When a reader-friendly daily report is required, enforce this one-way chain:

```text
Protocol + Summary + Detailed + Anchor update
-> daily_report_<topic_slug>.md
-> focus_<problem>.md
```

The daily report may repeat verified material needed for a cold reader, but
every decision-bearing number and figure must link to its canonical lineage.
Its eligibility, verdict, boundary, and one next decision must match Summary,
Detailed, and the Anchor exactly. Before human confirmation, mark its knowledge
wording `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`. A completed focus must cite a
human-confirmed daily report and keep only the question, concise update, one
decisive result, boundary, next decision, and report link. It cannot introduce
a new number, interpretation, boundary, or decision.

## Final Audit

Mark each item `PASS` or `FAIL`:

```text
Researcher supplied the initial judgment, or the document remains scaffolded:
Protocol revision and execution scope are identified:
Conformance and every deviation are recorded before interpretation:
Every primary result is eligible or explicitly bounded/ineligible:
Every decision-bearing number has complete evidence lineage:
Observation, derived statistic, interpretation, and claim are separate:
Summary is conclusion-first and links primary sources directly:
Detailed is the only complete evidence ledger:
Figures have source, aggregation, observed result, and limitation:
Summary, Detailed, and Anchor verdicts and boundaries agree:
Any daily report preserves canonical eligibility, verdict, lineage, boundary, and next decision:
Any completed focus cites a human-confirmed daily report and contains only the minimal summary fields:
Exactly one next decision has a completion criterion and resume action:
No missing value, expected pattern, or filename was turned into evidence:
```

Any `FAIL` blocks result finalization or Anchor promotion.

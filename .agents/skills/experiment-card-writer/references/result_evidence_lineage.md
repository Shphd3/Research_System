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
sources, consistency and wording. Reuse judgment already provided in this session
or active Focus; do not demand a duplicate closed-book account. If interpretation
is missing, complete the authorized factual records and evidence lineage. Mark
the missing human judgment `Unknown`, keep any AI interpretation `AI_PROPOSAL`,
and scaffold only the unfilled interpretation/decision fields below. This does
not finalize or promote human scientific judgment:

```text
Question:
Direct result:
Confirmed:
Weakened or rejected:
Current mechanism and reason:
Cannot claim:
Exactly one next decision:
```

`summary.md` owns the first canonical result reading path. `detailed.md` owns
the complete evidence ledger. The Protocol owns the registered plan and must
not be rewritten with result-derived content. A subject-bearing final report
written beside the Anchor may provide a fuller reader explanation, but it is
derived from these canonical records and cannot become the sole evidence
source.

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

Keep `summary.md` short, with the conclusion before detailed analysis. It must
be understandable without chat history but need not reproduce the complete setup.
Its reader body covers purpose, necessary model, hypothesis, bounded conclusion
and supporting analysis in an order that makes their logical links clear.
Ordinary chat links to it and explains the minimal
objects, comparison and boundary needed to answer the user's question, without
repeating the full result ledger. For first-use operations, rationale and formula
meaning, use the shared [writing contract](../../../../docs/report_writing.md#objects-operations-and-first-use-terms).

Use the maintained root [Summary template](../../../../templates/research_process/experiment_summary_template.md)
and its [Chinese companion](../../../../templates/research_process/experiment_summary_template_cn.md).
The content roles are:

1. **Purpose:** state the scientific uncertainty and what an answer changes.
2. **Model:** define the actual system, task, trainable/frozen objects, update or
   intervention and observable. Explain needed relations, assumptions and units.
3. **Hypothesis:** state one or two falsifiable expectations and the strongest
   credible rival at the original population, conditions and time horizon.
   Name the distinguishing comparison; do not invent registration.
4. **Conclusion:** answer the Purpose with the smallest decisive values and
   eligibility boundary. State what is supported, weakened or unresolved.
   A metric change or typed verdict alone is not a scientific answer.
5. **Analysis:** explain comparisons, baselines, held-fixed quantities, actual
   steps, metrics, aggregation, uncertainty and rival adjudication. Link decisive
   claims to source evidence. Material residuals and approximation errors remain
   visible; complete diagnostics and history stay in Detailed.

An optional evidence table names the registered rule, observed value, guard or
eligibility, verdict and source. Optional figures include a reading sentence.
Claim boundaries belong in the Conclusion and are justified in Analysis;
next-step reasoning follows the evidence without adding a second conclusion.

Apply this coverage to new or requested revised summaries; headings and order
may change for clarity, and necessary explanations may grow. Do not batch rewrite
historical records, frozen Protocols or evidence to satisfy a new presentation
format. A layout change preserves scientific meaning and researcher authority.

When the next decision is unconfirmed, state `Unknown` once with the unresolved
uncertainty. Add completion, stop and resume details only when an actual next
action has been chosen and those details matter.

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

For actual trained checkpoints and reusable analysis caches, link their asset
IDs and current access evidence following the
[asset lifecycle](../../../../assets/README.md#training-and-analysis-lifecycle).
Plans and `NOT_RUN` conditions have no produced checkpoint; failed saves remain
missing/partial. A pure audit reports gaps rather than implying it performed
registration or a new payload check.

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

For a settled-question final report and question closure, use this ownership chain:

```text
confirmed plain-language design in the active Focus
-> Protocol -> authorized execution
-> Summary / summary_cn.md + Detailed + Anchor update
-> researcher-completed result and boundary in the same Focus
-> <anchor_stem>_final_report.md
-> cycle close
```

The final report may repeat verified material needed for a cold reader, but
every decision-bearing number and figure must link to its canonical lineage.
Its eligibility, verdict, boundary, and next question must match Summary,
Detailed, the Anchor, and the researcher's result account in the active Focus.
Before human confirmation, mark its knowledge wording
`AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`. A settled-question final report requires
the researcher's result and boundary in the active Focus and a stable bounded
conclusion. An explicitly requested provisional synthesis may be written earlier:
complete source-backed facts, label it provisional, and leave unresolved judgment
unknown. It neither closes the question nor promotes evidence. The Focus cannot become
the sole source of a number, eligibility decision, deviation, or verdict; those
remain in canonical result records.

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
Any final report preserves canonical eligibility, verdict, lineage, boundary, and next question:
A settled final report has a human-confirmed Focus result; a requested provisional synthesis remains labeled and preserves unknowns:
A confirmed next decision has the necessary completion conditions; an unconfirmed decision is stated as Unknown without empty fields:
No missing value, expected pattern, or filename was turned into evidence:
```

Any `FAIL` blocks result finalization or Anchor promotion, not the requested
read-only audit or independent evidence verification. Report the failing item
and its evidence without changing human-owned scientific state. Result records
do not constitute the human-owned Focus conclusion; update Anchor sections 7–8
only after eligible evidence and human judgment agree. After a stable bounded
question and the human-completed Focus, route its one final report to
`research-final-report`; the researcher closes or corrects the cycle. Explicit
line synthesis belongs to `research-communication`, placement/state changes to
`research-mainline`; do not create a separate closure report here.

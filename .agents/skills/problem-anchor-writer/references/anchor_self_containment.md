# Anchor Self-Containment Contract

## Contents

1. [Purpose and boundary](#purpose-and-boundary)
   - [Formal Anchor structure](#formal-anchor-structure)
2. [Research-question contract](#research-question-contract)
3. [Zero-net-growth rule](#zero-net-growth-rule)
4. [Cold-reader gate](#cold-reader-gate)
5. [Grounding and no-invention contract](#grounding-and-no-invention-contract)
6. [Eight-section writing contract](#eight-section-writing-contract)
7. [Link, label, and context rules](#link-label-and-context-rules)
8. [Formula and metric rules](#formula-and-metric-rules)
9. [Compression replacements](#compression-replacements)
10. [Parent and subanchor rule](#parent-and-subanchor-rule)
11. [Final audit](#final-audit)

## Purpose And Boundary

Use this contract when drafting, revising, or auditing a formal anchor.

An anchor is self-contained when a cold reader with no chat history, code, or
linked document can reconstruct the research judgment:

```text
decision question
-> world claims or mathematical assumptions
-> formal claim or empirical hypothesis versus rival
-> mathematical relation
-> computational realization
-> decisive falsifier
-> current evidence
-> claim boundary
-> one next decision
```

This is **research-judgment self-containment**, not execution self-containment.
Commands, full configurations, run histories, complete tables, logs, and raw
artifacts remain in `protocol.md`, `summary.md`, and `detailed.md`. Links make
the anchor auditable; they must never carry meaning required to understand the
decision.

## Formal Anchor Structure

Write a formal Anchor only when the research question, prior, and model have
been approved. Use exactly these top-level sections:

```markdown
# <Anchor Title>

## 1. Problem Definition
## 2. Physical Priors
## 3. Falsifiable Hypotheses
## 4. Mathematical Model
## 5. Computational Realization
## 6. Minimal Falsification Tests
## 7. Current Evidence
## 8. Claim Boundary And Next Decision
```

Do not add an abstract, timeline, literature review, or embedded intake form.
Keep one decision question, one core model, one decisive criterion, one main
falsifier, and one next decision. Put run-level settings in `protocol.md`.

Keep exactly one phenomenon and decision question with a minimal variable set.
Retain at most three priors/assumptions, preferably one. Section 4 separates
assumptions, derivations, empirical claims and intuition; each equation maps to
its assumptions, proof/computation and evidence.
Section 6 states the decisive check, separated rival, allowed claim and boundary;
experimental claims also state the metric and justified threshold.
Every linked artifact must exist. Inline formulas use `\(...\)`, displays `\[...\]`.
Canonical English and `_cn.md` companions preserve the same question, model,
criterion, boundary and next decision unless the user chooses otherwise.

## Research-Question Contract

The Anchor must make the research question self-contained at its own decision
level. A reader must not need the parent Anchor, line README, chat, or code to
understand what is being adjudicated.

Section 1 must establish:

```text
parent direction or root problem
current established boundary
one blocking uncertainty
why this answer changes the parent judgment; chosen route or necessary dependency
exact decision question
in-scope and out-of-scope objects
what each Pass / Fail / Insufficient outcome would change or stop
```

For a root parent, the parent direction is the research line. For a subanchor,
restate only the inherited parent clause needed to understand the local
decision. Do not copy the parent story.

The question must name concrete subjects, actions or relations, conditions,
and the observable decision. Avoid questions such as “does it work?” or “is
the signal useful?” until `it`, `work`, `signal`, and `useful` have one local
meaning.

Self-contained does not mean self-justifying. If the question depends on an
unsettled premise, state the premise as unsettled, explain its consequence,
and link the artifact that records or could resolve it.

For theory-only questions, label mathematical assumptions instead of inventing
physical priors. Use proof/counterexample obligations instead of an experimental
metric, dataset or threshold. Keep the eight-section ownership and apply only
the active claim's requirements; a preferred route is not a necessary dependency.

## Zero-Net-Growth Rule

Improving self-containment must not make the anchor longer by default.

For every sentence added to explain a decision-bearing relation, remove or
compress at least as much material that belongs elsewhere or repeats existing
meaning. Remove these first:

- run IDs, seed lists, exact commands, and configuration detail;
- chronology that does not change the current judgment;
- secondary metrics that do not separate the named rivals;
- repeated caveats already captured by one claim boundary;
- generic background and literature context not used by the core model;
- multiple equations where one relation carries the decision;
- labels or headings that restate the following sentence.

Do not add an abstract, glossary, timeline, literature review, extra evidence
section, or supplementary top-level section. Rewrite the eight owning sections
instead.

## Cold-Reader Gate

The anchor passes only if a reader can answer all of these from the anchor
alone:

1. What exact decision question is being adjudicated, and what is out of scope?
2. Which world claims or mathematical assumptions motivate the design?
3. What claim or empirical hypothesis is checked, and what would refute it?
4. What is the one mathematical relation or objective that encodes the idea?
5. How does each decision-bearing mathematical object become an actual data,
   model, intervention, or analysis object?
6. What proof/counterexample or empirical comparison adjudicates it, and what
   do supporting, non-supporting and insufficient evidence change?
7. What was directly observed, what is the safest interpretation, and what
   remains unresolved?
8. What is the conservative claim boundary and the one next decision, including
   its completion criterion and resume action?

Apply only the active claim's questions. If an applicable answer requires hidden
context or an unexplained label, repair its explanation in the Anchor.

## Grounding And No-Invention Contract

Classify every decision-bearing statement by its actual basis:

```text
HUMAN_CONFIRMED     explicit researcher judgment in conversation, Focus, or review
APPROVED_PARENT     inherited clause from an approved parent Anchor
VERIFIED_EVIDENCE   direct result or source inspected and linked
AI_PROPOSAL         candidate definition, prior, variable, metric, or mechanism
UNKNOWN             information is absent but does not yet block formalization
BLOCKED             missing information prevents an adjudicable Anchor
```

The prose need not repeat these labels on every sentence. It must use an
explicit label wherever a cold reader could mistake a proposal, assumption, or
missing fact for an established judgment.

Never invent or silently complete:

- the researcher's mechanism judgment or preferred direction;
- a physical prior, causal direction, or strongest rival;
- a variable, dataset, task, supervision source, architecture rationale, or
  objective;
- a metric definition, threshold, pass/fail rule, or confirmation boundary;
- an experiment result, numerical value, literature conclusion, or source;
- a parent dependency, current status, or next decision.

When a required item is missing, use this local record:

```text
Status: Unknown | BLOCKED | AI_PROPOSAL
Missing or disputed item:
Why it matters for this decision:
Current safe boundary:
Direct source or artifact to inspect:
What would resolve it:
```

If no source exists, say so. Do not create a citation-like link to a merely
related document. If sources conflict, preserve the conflict and keep the
claim unresolved.

A linked artifact supports provenance; it does not carry the Anchor's local
explanation. Before each decision-bearing link, state the inherited clause,
observed result, uncertainty, or boundary that the link audits.

## Eight-Section Writing Contract

### 1. Problem Definition

Lead with the exact decision question. Name the parent problem and sharper
subproblem only to establish scope. State the current blocking uncertainty,
why it is the smallest direction-changing question, and what Pass, Fail, and
Insufficient would redirect or stop. Define each indispensable term at first
use, including what is measured and what is excluded.

### 2. Physical Priors

State empirical priors as testable world claims; formal assumptions as such.
Explain their consequences and limits. Retain only those affecting the claim.

### 3. Falsifiable Hypotheses

For an empirical claim, place the hypothesis beside its strongest live rival.
State the tested relation and each prediction. For a formal claim state its
assumptions and proof/refutation obligation. A hypothesis name or
condition label is not an explanation.

### 4. Mathematical Model

State the scientific relation before the equation. Define every symbol at
first use, retain one core relation when possible, and say what decision the
relation supports and what it cannot establish.

### 5. Computational Realization

Follow logical order, including causal order where relevant. Map every
decision-bearing mathematical object to a constructible data field, tensor,
component, proof step, intervention, or analysis computation. For a scientifically
meaningful stage, state its goal, how it works, and why it is needed. Exclude
run settings that belong to the Protocol.

When prior work materially changes which mechanism is admissible, record the
representative alternative, its relevant mechanism and supervision boundary,
the direct source, and the local adopt, adapt, baseline, or reject decision in
this section. Omit prior-art catalogues that do not change the computation.

### 6. Minimal Falsification Tests

Specify the decisive proof/refutation or empirical comparison and necessary
guards. Empirical metrics need a computation, unit, decision role, justified
threshold and limitation. State supporting, non-supporting and insufficient
branches and their decision consequences before interpreting evidence.

### 7. Current Evidence

Use the minimum local evidence unit:

```text
key comparison -> direct observation -> safest interpretation -> unresolved rival
```

Give the value or qualitative result needed for the decision in the anchor.
Put complete tables, run histories, and artifact maps behind links only after
the local meaning is clear. Use `NOT RUN` or `Unknown` when appropriate.

### 8. Claim Boundary And Next Decision

State what is supported, weakened, unresolved, and not claimable. End with
exactly one next decision, its completion criterion, and the concrete resume
action. State how the current outcome changes, stops, or leaves unchanged the
parent direction. Do not replace the decision with a broad backlog.

## Link, Label, And Context Rules

- Introduce each link with the local question, result, or boundary that the
  linked artifact audits.
- Link the most direct source for inherited questions, disputed premises,
  external evidence, and unresolved items. Do not cite a neighboring document
  merely because it is topically related.
- Do not write “see the result,” “as discussed above,” “the current signal,” or
  similar phrases whose meaning depends on hidden context.
- Define run labels, condition names, abbreviations, and identifiers before
  using them as evidence. Prefer their scientific meaning over their ID.
- A table caption, plot label, section title, or filename cannot carry an
  explanation that the prose omits.
- Keep each fact in its owning section. Do not repeat it merely to improve
  transitions; use a short causal connector instead.

## Formula And Metric Rules

Before a formula, state the logical, causal or decision idea in words. After
the formula, state:

```text
symbols and units
concrete computation
decision role
what the value cannot prove
```

Keep formulas or metrics needed for the claim and decisive check. Link fuller
proofs or diagnostics after the Anchor explains the essential relation.

## Compression Replacements

| Replace | With |
|---|---|
| a list of run IDs | the key comparison and direct result |
| a chronology of attempts | the current evidence state |
| several correlated metrics | the primary metric and its limitation |
| repeated caveats | one conservative claim boundary |
| multiple equivalent equations | one decision-bearing relation |
| a bare link | a local conclusion followed by its audit link |
| an unexplained condition label | the scientific difference it denotes |

## Parent And Subanchor Rule

A parent anchor must close its complete major decision. A subanchor must be
self-contained for its local decision while restating only the inherited
parent clause needed to understand that decision, usually in one sentence. It
must not copy the parent's full background, model, or evidence chain.

### Placement

A parent anchor owns one complete major research problem. A subanchor inherits
the parent question and adjudicates one local clause, rival explanation,
robustness check, or metric guard. It must not repeat the full story or create a
parallel mainline.

Existing project layout remains valid; do not silently migrate a flat line.
For a new or explicitly migrated parent/subanchor layout, use one folder per
sibling parent:

```text
main/problem_anchors/<line_id>/README.md
main/problem_anchors/<line_id>/<parent_id>_<topic>/
  <parent_id>_<topic>_anchor.md
  subanchors/
    <parent_id>_<NN>_<topic>_anchor.md
```

Reading order or `depends_on` between two parent anchors does not make either a
subanchor. Store an item in `subanchors/` only when it inherits the containing
parent's decision question. The line `README.md` distinguishes sibling-parent
dependency order from parent--child ownership.

## Final Audit

Apply the cold-reader gate and grounding rules to the active claim. Check source
identity, language consistency, placement, branch consequences and one next
decision. Mark applicable gaps `FAIL`; do not manufacture requirements for an
inactive stage or a sound argument. Passing checks grants no scientific approval.
Replace lower-value content to repair gaps under the zero-net-growth rule;
add no document layer or top-level section.

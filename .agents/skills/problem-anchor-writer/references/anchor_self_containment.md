# Anchor Self-Containment Contract

## Contents

1. [Purpose and boundary](#purpose-and-boundary)
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
-> physical prior
-> primary hypothesis versus strongest rival
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

## Research-Question Contract

The Anchor must make the research question self-contained at its own decision
level. A reader must not need the parent Anchor, line README, chat, or code to
understand what is being adjudicated.

Section 1 must establish:

```text
parent direction or root problem
current established boundary
one blocking uncertainty
why this uncertainty is the smallest decision that can change the direction
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
2. What claim about the physical or data-generating world motivates the design?
3. What are the primary hypothesis and strongest live rival, and how do their
   predictions differ?
4. What is the one mathematical relation or objective that encodes the idea?
5. How does each decision-bearing mathematical object become an actual data,
   model, intervention, or analysis object?
6. What single comparison and primary metric can falsify the hypothesis, and
   what do pass, fail, and insufficient mean?
7. What was directly observed, what is the safest interpretation, and what
   remains unresolved?
8. What is the conservative claim boundary and the one next decision, including
   its completion criterion and resume action?

If any answer requires opening a link, recalling a conversation, inspecting
code, or interpreting an unexplained label, the anchor fails the gate.

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

State the prior first as a plain claim about the world. Then name the observable
that exposes it and what would make it false. Prefer one prior; retain another
only when it changes the core prediction.

### 3. Falsifiable Hypotheses

Place the primary hypothesis beside the strongest live rival. State the causal
direction and distinct observable prediction of each. A hypothesis name or
condition label is not an explanation.

### 4. Mathematical Model

State the physical or causal idea before the equation. Define every symbol at
first use, retain one core relation when possible, and say what decision the
relation supports and what it cannot establish.

### 5. Computational Realization

Follow causal order rather than implementation chronology. Map every
decision-bearing mathematical object to a constructible data field, tensor,
component, intervention, or analysis computation. For a scientifically
meaningful stage, state its goal, how it works, and why it is needed. Exclude
run settings that belong to the Protocol.

When prior work materially changes which mechanism is admissible, record the
representative alternative, its relevant mechanism and supervision boundary,
the direct source, and the local adopt, adapt, baseline, or reject decision in
this section. Omit prior-art catalogues that do not change the computation.

### 6. Minimal Falsification Tests

Specify one decisive comparison, one primary metric, and only the guards needed
to rule out the named rival. Define the metric's concrete computation, unit or
formula, decision role, threshold logic, and what it cannot prove. State pass,
fail, and insufficient outcomes before any evidence is interpreted.

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

Before a formula, state the causal or decision idea in plain language. After
the formula, state:

```text
symbols and units
concrete computation
decision role
what the value cannot prove
```

Keep only the formula and primary metric needed to distinguish the hypothesis
from its strongest rival. Move derivations and secondary diagnostics to their
owning artifacts.

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

## Final Audit

Read the anchor once without opening links and mark each item `PASS` or `FAIL`:

```text
Question and scope are explicit:
Prior and causal direction are explicit:
Hypothesis and strongest rival predict different observations:
Core model is understandable before its equation:
Model-to-computation mapping is complete:
Primary metric and verdict rules are defined:
Evidence separates observation from interpretation:
Boundary and one next decision are reconstructible:
Question placement explains why this decision is next:
Pass / Fail / Insufficient implications for the parent direction are explicit:
Every proposal, unknown, and blocked item is unmistakable:
No human judgment, source, value, threshold, or result was invented:
No link carries required explanatory content:
No sentence can be removed without weakening the decision chain:
```

Approval requires every item to pass. If a missing explanation is needed,
rewrite or replace lower-value content under the zero-net-growth rule rather
than adding a new document layer or top-level section.

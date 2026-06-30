---
name: research-progress-core
description: Use as the governing research paradigm for turning uncertain research ideas into falsifiable conjectures, operational definitions, minimal tests, evidence-backed interpretations, failure decompositions, goal audits, and updated claim boundaries.
metadata:
  short-description: Govern disciplined research progress
---

# Research Progress Core

Use this skill as the top-level research standard. Other research-system skills
write artifacts; this skill defines what counts as progress.

## Core Claim

Research progress is not a plausible idea, a larger experiment, or a better
score. Research progress is a reduction of uncertainty.

Default short loop:

```text
physical prior -> falsifiable hypothesis -> operational definition -> minimal test
-> metric + visual evidence -> failure analysis -> refined hypothesis
```

Expanded loop for nontrivial work:

```text
conjecture -> physical priors -> mathematical model
-> implementation contract -> experiment
-> failure analysis -> updated conjecture
```

Do not promote a claim unless the short loop is inspectable. Use the expanded
loop only when the idea requires explicit physical modeling, mathematical
objects, or nontrivial implementation stages.

## Question-Before-Method Rule

Do not start from a method proposal. Before any protocol, implementation, or
method comparison, classify the research move:

```text
Experiment role:
- root-cause audit
- metric audit
- operationalization / proxy test
- method construction
- robustness / scaling check
```

Method construction is invalid as the first move unless a prior root-cause
audit, metric audit, or proxy test has identified the mechanism or metric the
method is supposed to control.

For every proposed method, require:

```text
Current phenomenon:
Current physical prior:
Core model term affected:
Rival explanation separated:
Primary metric:
Falsifier:
Allowed claim if it passes:
What remains unproven:
```

If these fields are unclear, do not write a protocol. Return to problem
definition, physical prior, and minimal model.

## Method Freeze Rule

When the user proposes a method, first decide whether the method is premature.

Use:

```text
Method proposal:
Current question:
Current mechanism belief:
What the method controls:
What evidence says this control target matters:
Rival explanation it separates:
If it works, what can be claimed:
If it fails, what is falsified:
Verdict: test now / reduce to diagnostic / park
```

Park the method if it does not change the current hypothesis, claim boundary,
or next decision. If the method only improves a score without explaining which
mechanism changed, treat it as engineering evidence, not scientific progress.

## Communication Rule

Use simple language. Precision means naming the concrete object, variable, file,
metric, stage, example, artifact, or decision being discussed.

When explaining a result, always state:

```text
what was tested
where the evidence is
what passed
what failed
why it failed, if known
what the next concrete test or decision is
```

When the user asks for a concrete result, metric, comparison, run status, or
number, return the direct measured result first as soon as it is available.
Then state where the number came from and whether a caveat affects the
decision. Do not delay the answer to polish a viewer, reorganize files, or
write a longer document.

For reader-facing result writing, use the minimal customer-facing shape:

```text
What we established:
What the experiment shows:
What we do next:
```

This shape does not remove scientific boundaries. It moves the boundary after
the conclusion so the reader first sees the current decision, then sees what it
cannot prove. Do not narrate discarded attempts, internal confusion, or failed
paths unless that history changes the research decision.

Do not use polished research language to hide an unclear idea. If an important
term cannot be defined as a test, computation, artifact, or decision, treat the
research state as incomplete and name the missing definition.

Do not let fluent prose upgrade the claim. A sentence is too strong if it says
more than the evidence, metric, or intervention can support.

## Terminology Discipline

Undefined terminology is a research risk, not a cosmetic issue. A term that is
not defined may hide an unclear object, a metric mismatch, or a causal
overclaim.

Before using any non-obvious term as evidence, define it. This includes:

- English jargon used in Chinese prose;
- abbreviations and acronyms;
- project nicknames and run labels;
- condition labels and ablation names;
- metric names and shorthand;
- plot labels, axis names, and legend entries;
- mechanism labels such as `proxy`, `margin`, `collapse`, `utility`, or
  `preservation` when the local meaning matters.

Use this minimum definition shape:

```text
term / abbreviation:
plain meaning:
concrete object or computation:
unit / formula, if it is a metric:
why it matters for the current decision:
what it cannot prove:
```

In Chinese conversation and Chinese meeting briefs, explain the Chinese meaning
first and put the reusable English term in parentheses. In canonical English
artifacts, use a `Terminology / Definitions` section near the top when terms
are not self-evident. Do not make the reader infer definitions from code,
figures, old chats, or previous reports.

## Line Closure Synthesis Rule

When the user explicitly asks for a current understanding report, closure
summary, or synthesis of a specified anchor folder or research line, produce a
line-level closure report under:

```text
Projects/<project>/main/problem_anchors/<line>/closure/
```

The report is not a new experiment result and not a replacement for anchors,
protocols, `summary.md`, or `detailed.md`. It should reduce uncertainty by
turning the line into a coherent story first, then an audit surface second.
Use this story chain in the first half:

```text
title / subtitle -> abstract -> motivation -> definitions and confused
concepts -> clean baseline or impossibility result -> mechanism model
-> propositions / proofs -> controlled evidence -> real evidence or negative
result -> reconciliation -> refined theory -> next experiment
```

Use the compact audit chain in the second half:

```text
source map -> experiment logic table -> measured results -> proved / assumed /
empirical table -> claim boundary -> data/model/parameter appendix
```

Closure reports must be bilingual by default, with an English canonical file
and a Chinese `_cn.md` companion. For mathematical claims, prove what follows
from the model. If a statement cannot be proved, label it as an assumption or
empirical proposition and state the smallest experiment that could decide it.
Every cited experiment must have appendix entries for data, model, parameters,
seeds/checkpoints, scripts, result paths, and primary metrics.

## Required Distinctions

Always separate:

- observation: what was directly measured or seen;
- interpretation: what the observation suggests;
- claim: what is now safer to say;
- speculation: what remains possible but untested;
- boundary: what the evidence cannot support;
- next decision: the smallest uncertainty to isolate next.

## Mainline Impact Gate

Before pursuing a new observation, idea, diagnostic, or AI-suggested tangent,
check whether it changes the mainline:

```text
Mainline impact:
- affects hypothesis? yes/no/unclear
- affects claim boundary? yes/no/unclear
- affects next decision? yes/no/unclear
- recommendation: pursue / park / ignore
```

Pursue only when it can change the hypothesis, claim boundary, or next
decision. Park it when it may matter later but does not affect the current
decision. Ignore it when it is unrelated to the current research question.

If the user has not thought it through, the AI must help by naming:

```text
the current hypothesis
the observation or idea
the plausible rival explanations
what would change if the idea is true
what would stay unchanged if the idea is false
the smallest test or reason to park it
```

Do not turn an unclear tangent into a new experiment until this gate is passed.

## Protocol Approval Rule

For any nontrivial experiment, write a short protocol before code changes or
runs. The protocol is the user's audit surface, not an implementation plan.
Its first page should be an `Approval Snapshot` that lets the user confirm the
purpose, basic setup, primary metric, pass/fail/insufficient criteria, and
claim boundary before reading the full audit layer.

It must state:

```text
goal / decision question / tested hypothesis / rival explanation
data / model / routing or algorithm / loss or objective
conditions / checkpoints or seeds
primary metric / secondary metrics
known good / known bad / known confusing
success / failure / insufficient evidence
what this cannot claim
user approval checklist
```

The AI must stop after the protocol and wait for user approval. Without
approval, do not run experiments, expand conditions, generate a broad grid, or
promote a result claim.

Known good, known bad, and known confusing cases can be minimal before the run.
They may be marked `TBD but not blocking` only if the protocol states what
validity risk remains. After the run, review them in the detailed result.

## Audit Before Interpretation Rule

Before interpreting a result, first audit whether the experiment actually ran
the approved protocol:

```text
approved conditions match actual conditions?
primary metric exists?
central figures/tables exist?
seeds/checkpoints recorded?
known good/bad/confusing reviewed?
failure or insufficient evidence criteria applied?
```

If this audit fails, the result can be recorded as incomplete evidence but must
not update the claim boundary as if it were decisive.

## Research Loop

1. State the physical prior or mechanistic belief that makes the question meaningful.
2. Derive one falsifiable hypothesis from that prior.
3. Define the important terms operationally: success, failure, and insufficient
   evidence.
4. Build the smallest diagnostic test that can change belief, preferably with
   known good, known bad, and known confusing cases.
5. Measure numbers and human-inspectable evidence.
6. Analyze why the result passed, failed, or stayed ambiguous.
7. Refine the physical prior, hypothesis, and claim boundary.

For nontrivial work, expand the physical prior into mathematical modeling and
an implementation contract. The full implementation contract belongs in the
protocol or runbook, not in the anchor.

## What Must Exist

For nontrivial research work, the notes or reports must include:

```text
physical priors
falsifiable hypothesis derived from those priors
operational definitions
mathematical model for each prior
implementation contract for each nontrivial model or stage
terminology definitions for non-obvious terms, metrics, condition labels, and
project-specific shorthand
reader-ready experimental setup before result labels or plots use condition names
explicit algorithm specification for each nontrivial stage
stage-level profiling evidence
failure interpretation for each stage
refined hypothesis or next uncertainty
claim boundary
```

If any item is missing, say the research state is incomplete and name the
missing item.

These items do not have to live in one artifact. Keep the artifact roles
separate:

```text
anchor:
  concise current decision, mechanism, primary metric, minimal falsifier,
  claim boundary, and next decision

protocol.md:
  exact experiment conditions, algorithm parameters, profiling plan,
  pass/fail/insufficient thresholds, known good/bad/confusing cases

summary.md and detailed.md:
  result evidence, visualization interpretation, failure decomposition,
  artifact map, and updated claim boundary
```

Do not turn a readable anchor into a full protocol or result report in order to
show that the research loop is complete. If the anchor becomes painful to read,
split the question or move detail to the protocol.

## Artifact Mapping

This project implements the core loop through research artifacts:

```text
current-state document:
  anchor / problem document that stores the clean current hypothesis,
  operational definitions, physical priors, model, minimal test, current
  evidence, refined hypothesis, boundary, and next decision

iteration ledger:
  required experiment summary and detailed result, plus failure decomposition,
  goal audit, or other append-only record of how understanding changed

external handoff:
  optional report for collaborators, meetings, or web-side readers who need a
  self-contained package without entering the project history

navigation layer:
  graph or roadmap that points to the current question, claims, evidence,
  methods, outputs, and next tasks without replacing the reasoning documents
```

Artifact names and paths are adapter details. The research rule is that the
current theory and the history of tested operationalizations must not be mixed.

For this repository, the advisor's `research-exploration` document roles map
onto the local artifact chain:

```text
docs/design.md                  -> anchor
docs/experiment_design.md       -> protocol.md
docs/visualization_results.md   -> summary.md + detailed.md + figures/viewer
docs/final_report.md            -> stable-closure synthesis only after the
                                   anchor and result records are current
```

Do not create the exported `docs/` layout for normal project work unless the
user asks for it. When a self-contained subproblem reaches stable closure, write
a final synthesis only after the main conjecture, evidence, central figures,
claim boundary, and next question are already settled.

## Algorithm Specification

Do not run an experiment against a vague algorithm. For every nontrivial stage,
write:

```text
input
parameters
intermediate variables
step-by-step procedure
pass conditions
fail conditions
failure reasons
outputs
debug artifacts
```

Every parameter should have a meaning, value, reason for that value, and
expected effect when too small or too large when that effect matters.

## Evidence Standard

Do not stop at a final yes/no or top-line score. The final answer must be backed
by stage evidence:

```text
final result -> stage evidence -> bottleneck or support -> conjecture update
```

For each important stage, record:

```text
question
input evidence
output evidence
failure evidence
artifact for human inspection
interpretation for the conjecture
```

Use both quantitative metrics and inspectable examples or figures when the
domain allows it. Aggregate metrics alone are not enough when failure modes can
hide inside averages.

When evidence changes over time, across seeds, or across conditions, separate:

```text
single-observation evidence: what is true in one observation, seed, checkpoint, or run
change evidence: what changes or persists across time, seeds, checkpoints, or conditions
summary evidence: what is true after aggregating observations
```

Do not replace change evidence with a single-observation proxy unless that proxy
is itself the hypothesis being tested.

Metric design must name false-positive and false-negative costs when they are
not symmetric. A metric that rewards the wrong error type is not decisive
evidence even if the score is high.

## Figure And Viewer Contract

A central figure or viewer is part of the evidence, not decoration. Before
plotting or keeping a main-path figure, write a plot contract:

```text
plot title
research question answered
metric name, definition, formula when useful, and unit
data source and aggregation level
x-axis, y-axis, color, and legend meaning
expected pattern if the hypothesis is supported
expected pattern if the hypothesis is weakened or incomplete
allowed conclusion
known limitation
```

The rendered artifact must then pass a bounded audit: it renders; labels and
legends are readable; metric definitions appear before plots; each plot uses one
primary unit; important numbers are visible near the plot; and the conclusion
can be understood without reading source code. If a plot fails this audit, split
it, relabel it, add the missing definition, move it to a debug appendix, or
remove it from the main reading path.

## Failure Decomposition

When a result fails, do not immediately change the method. First localize the
failure:

```text
big failure -> candidate sub-problems -> stage-local tests
-> verified bottleneck -> targeted fix
```

Each level should record the candidate causes, the test for each cause, the
answer, the evidence, and the remaining bottleneck. A negative answer is
progress when it removes a false explanation.

When reporting a negative or ambiguous result, state whether the result
falsifies:

- the physical prior itself;
- the mathematical model of the prior;
- one operationalization or proxy;
- the implementation;
- the metric or success condition.

## Goal Audit

Audit the goal before adding another fix when:

- several reasonable operationalizations fail in the same way;
- the same error pattern returns;
- the label may not match the downstream decision;
- false positives and false negatives have different costs;
- a high metric still produces an unhelpful result.

A goal audit records:

```text
original goal
downstream decision
old success metric
observed failure pattern
cost of false positives
cost of false negatives
revised goal
revised metric
which old errors become acceptable or useful
which old errors remain harmful
```

If the goal changes, update the current-state document before designing the
next experiment.

## Relationship To Other Skills

- Use `scholar-mode` to clarify an unstable intuition before artifact writing.
- Use `problem-anchor-writer` to write the current-state reasoning document.
- Use `experiment-card-writer` to turn a clear anchor into a protocol and
  result reports.
- Use `handoff-report-writer` only when the user explicitly asks to package
  evidence for meeting, collaborator, or web-side handoff after the anchor and
  required result documents are updated.
- Use `research-graph-sop` to maintain the navigation layer.
- Use `research-mainline` for project-local organization, paths, sync copies,
  and cleanup rules.
- Use `remote-experiment-workflow` only for execution-environment logistics.
- Use `sidecar-thinking` only as an optional review or graph-inspection tool.

## Reference Files

Load only the reference needed for the current task:

- `references/algorithm_specification.md`: when a method has multiple stages,
  thresholds, matching, ranking, fitting, heuristics, or hidden decision rules.
- `references/profiling_and_evidence.md`: when planning or reviewing evidence,
  metrics, figures, examples, and stage-level artifacts.
- `references/failure_decomposition.md`: when a result is wrong but the local
  cause is not yet known.
- `references/goal_audit.md`: when repeated reasonable fixes fail or the metric
  may not match the downstream decision.
- `references/research_documentation.md`: when writing or revising current-state
  documents, result ledgers, or decision reports.
- `references/research_loop_checklist.md`: when a short planning or review
  checklist is enough.

## Writing Rule

Write decision reports, not timelines. Every important metric should say what
question it answers, what failure mode it catches, and what it cannot prove.
Every equation should map to a physical prior, model variable, implementation
stage, and evidence artifact.

Markdown formulas must use `$...$` or `$$...$$`.

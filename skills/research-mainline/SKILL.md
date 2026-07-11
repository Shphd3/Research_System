---
name: research-mainline
description: Use when organizing or updating a research project's mainline state: graph, roadmap, anchors, protocols, experiment result records, explicitly requested root anchor copies, external collaborator repo sync packages, handoff packages, archive state, and project status.
metadata:
  short-description: Maintain compact research mainline
---

# Research Mainline

Use this skill to keep the active research state easy to inspect and act on.
It does not define the research method; it maps the method onto project paths.

First apply `research-progress-core`. Then use this skill only to decide where
the current state lives, whether the mainline changed, and which surfaces need
to be updated.

## Mainline Goal

The mainline should make these items obvious:

- current research question;
- active anchor;
- strongest current evidence;
- refined hypothesis or current uncertainty;
- claim boundary;
- next decision;
- links to the protocol and result records that justify the state.

## Required Surfaces

```text
Projects/<project>/
  graph.yaml
  main/
    roadmap.md
    problem_anchors/
      <anchor_id>.md
    experiments/
      A<anchor_id>/
        <experiment_id>/
          protocol.md
          summary.md
          detailed.md
          figures/
          tables/
```

Legacy two-file planning records may remain in old experiments, but new work
should use `protocol.md`.

Explicit optional surfaces:

```text
Projects/<project>/<worker>/sync/MMDD_topic/
Projects/<project>/sync/MMDD_topic/
sync/<sync_id>/anchors/<category>/<anchor_id>.md
daily_research_reports/MMDD/
<external_collaborator_repo>/<agreed_path>/MMDD_topic/
```

Do not update optional sync, external collaborator sync, handoff, graph, commit,
or push surfaces unless the user explicitly asks for that action.

## Naming Rules

### Anchor Names

Anchor names describe a stable research question or hypothesis line, not a day
or one run.

Use:

```text
<mechanism_or_question>_anchor.md
<factor>_<effect>_anchor.md
<problem_axis>_<decision>_anchor.md
```

Do not create a new anchor for each daily iteration, seed, smoke run, or failed
operationalization. Update the same anchor unless the parent question or
hypothesis line changes.

### Experiment Names

When an experiment folder uses an `A` prefix, the number after `A` is the
primary anchor id, not the calendar date:

```text
A<anchor_id>_<short_topic>/
A<anchor_id>a_<short_topic>_smoke/
A<anchor_id>b_<short_topic>_full/
```

Calendar dates belong in run names, daily report paths, logs, or result
folders, not in the anchor-code position.

Use suffixes only when they distinguish real iteration roles:

```text
smoke
full
followup
ablation
trajectory
seed_sweep
```

Store active experiments under the anchor-family folder:

```text
main/experiments/A<anchor_id>/<experiment_id>/
```

For example, experiments whose id starts with `A05_` belong under
`main/experiments/A05/`.

### Story Names

Story folders may contain more than one document, so the filename must carry
both reading order and subject:

```text
main/stories/<line_id>/<NN>_<topic>.md
main/stories/<line_id>/<NN>_<topic>_cn.md
```

Use a two-digit `NN`. Keep the English canonical story and Chinese companion
on the same stem. The line `README.md` must order all story pairs and mark one
pair as the current primary synthesis. Do not use generic `story.md` or
`story_cn.md` names for new or renamed stories, and do not create one story per
anchor.

Archived snapshots repeat their snapshot identifier in the filename:

```text
archive/<snapshot_id>/<snapshot_id>.md
archive/<snapshot_id>/<snapshot_id>_cn.md
```

### Daily Reports

Daily report folders are date-first because they record work for a day:

```text
daily_research_reports/MMDD/<topic>/
```

Daily reports do not replace anchors or experiment records. If the day changes
the hypothesis, evidence, boundary, or next decision, update the anchor too.

## Core Artifact Chain

Default chain:

```text
anchor -> protocol.md -> summary.md -> detailed.md -> anchor update
```

Root sync copies, handoff packages, graph edits, commits, and pushes are
explicit follow-up actions only.

Every mainline artifact must be terminology-safe. If a document uses
non-obvious terms, English jargon, abbreviations, metric names, condition
labels, model variants, project shorthand, or plot labels, it must define them
before using them as evidence. Use `Terminology / Definitions` for English
canonical artifacts and `术语解释` for Chinese meeting or companion files.

This chain is the local adapter for the advisor's `research-exploration` spec:

```text
anchor                              = docs/design.md role
protocol.md                         = docs/experiment_design.md role
summary.md + detailed.md + figures  = docs/visualization_results.md role
final_report.md                     = stable-closure synthesis after the
                                      working evidence and anchor are current
problem_anchors/<line>/closure/     = specified research-line synthesis for
                                      the current expected process, evidence
                                      chain, mathematical model, and boundary
```

Do not create the exported `docs/` layout for ordinary mainline work unless the
user asks for that layout. The anchor-first layout remains canonical.

Artifact roles must stay aligned:

| Artifact | Owns | Must not do |
|---|---|---|
| `00_handwrite_anchor.md` | rough Thinking Card and exposed user judgment | require or become a full 0-8 anchor before audit |
| anchor | current minimal adjudicable design | become a runbook, full result report, or broad ablation list |
| `protocol.md` | how one anchor clause will be tested | change the question post hoc or add unrelated sweeps |
| `summary.md` | first reading path: conclusion, primary metric, central figures | contain the full evidence ledger |
| `detailed.md` | complete evidence ledger, failure decomposition, artifact map | create a second conclusion stronger than the anchor allows |
| `closure/<topic>_closure_report.md` | line-level stable synthesis requested for an anchor folder | replace source artifacts or make claims stronger than linked evidence |
| `figures/` or viewer | visual evidence for the current judgment | include decorative plots or disguise debug plots as decision evidence |
| anchor update | supported / weakened / insufficient evidence, boundary, next decision | paste a result report into the anchor |

## File Roles

### Graph

Navigation layer only. It points to questions, anchors, protocols, evidence,
methods, outputs, and tasks. It does not replace Markdown reasoning.

Before editing an existing graph, use `research-graph-sop` and get the user's
confirmation of the research-state change unless the user explicitly requested
that exact graph edit.

### Roadmap

Compact route and gate logic. Use it for the order of anchors, stop rules, and
high-level project route. Do not put detailed evidence here.

### Anchor

The anchor is the project-local equivalent of research-exploration
`docs/design.md`: a compact but complete current-state research design
document. It should include one decision question, physical priors,
falsifiable hypotheses, one core mathematical model, computational realization,
minimal falsification tests, current evidence, claim boundary, and one next
decision. Each minimal falsification test should include its operational
definition, stage-local evidence, and failure meaning before it becomes
protocol-ready.

The anchor has two reading layers. `Thinking Card` is the short human-facing
mechanism judgment card: phenomenon, mechanism guess, key variables, causal
relation, observable metric, alternative explanation, and decision rule. The
remaining sections are the auditable design layer for AI review, replay,
protocol alignment, and boundary checks.

The required anchor structure is:

```text
0. Thinking Card
1. Problem Definition
2. Physical Priors
3. Falsifiable Hypotheses
4. Mathematical Model
5. Computational Realization
6. Minimal Falsification Tests
7. Current Evidence
8. Claim Boundary And Next Decision
```

Do not put commands, long configs, raw logs, broad ablations, or full result
presentation in the anchor. Put those in `protocol.md`, `summary.md`, and
`detailed.md`.

`Computational Realization` exists to prevent theory/code drift: the anchor
must say what input objects, computed variables, algorithm stages,
stage-local evidence, and expected artifacts instantiate the mathematical
model before the protocol or implementation expands it.

### Protocol

`protocol.md` is the approved experiment design. It replaces the old two-file
planning split. It should align with the advisor's research-exploration
`docs/experiment_design.md` role.

Its first page should be an `Approval Snapshot`: purpose, anchor alignment,
minimal setup, conditions to run, primary metric, pass/fail/insufficient
criteria, claim boundary, and approval decision. Put stage profiling,
algorithm details, commands, and artifact maps after this snapshot.

It must include the decision question, tested hypothesis, rival explanations,
data/model/algorithm/objective, conditions, primary metric, secondary metrics,
known good/bad/confusing cases, stage-level profiling plan, success/failure/
insufficient-evidence conditions, what cannot be claimed, and approval status.

For nontrivial algorithms, it must include input, parameters, intermediate
variables, steps, outputs, debug artifacts, pass conditions, fail conditions,
and failure reasons.

### Summary

`summary.md` is the first post-result reading path. It must include purpose,
exact setup, primary metric, result, key evidence, claim boundary, and next
decision.

It should start with a concise result snapshot: what is established, what the
experiment shows through the primary metric, and what action follows. It should
not narrate internal trial history unless that history changes the claim
boundary or next decision. Define every condition label, metric abbreviation,
and visible shorthand in `Terminology / Definitions` before using it as
evidence.

It must also absorb the key parts of research-exploration
`docs/visualization_results.md`: each central figure should explain what it
tests, how to read it, observed result, take-home, and what it does not prove.
Keep only figures that support the current claim boundary or next decision.

### Detailed

`detailed.md` is the full evidence ledger. It must include protocol compliance
audit, setup, metrics, stage evidence, failure decomposition, full experiment
record, interpretation, claim boundary, next decision, artifact map, and a full
`Visualization Results` section.

Every central figure or viewer should state purpose, setup, how to read,
observed result, take-home, and remaining uncertainty.
Separate decision evidence, stage-level profiling evidence, debug-only
evidence, and failed or ambiguous evidence. Debug-only figures must not be
promoted into `summary.md` as decision evidence.

For new central plots or browser viewers, require a plot contract before
plotting and a bounded rendered-artifact audit before delivery. The contract
must state the question answered, metric definition and unit, data source,
aggregation level, axis/legend meaning, allowed conclusion, and limitation.
The audit must check that the rendered artifact is readable and understandable
without source-code knowledge.

### Closure

`problem_anchors/<line>/closure/` is the specified research-line synthesis
surface. It is used when the user asks to close, summarize, audit, or
understand a named anchor folder or line as a unit. It is not a default side
effect of every experiment.

Do not create placeholder closure folders or `closure/README.md` files. When a
closure report is actually requested and written, use:

```text
closure/<line>_closure_report.md
closure/<line>_closure_report_cn.md
```

The English file is canonical unless the user explicitly chooses Chinese as
canonical. The Chinese companion must match the same claims, metrics,
boundaries, and next decision.

A closure report must use two layers.

Story layer, first:

- title and subtitle that state the research object;
- abstract with the current verdict and next decision;
- motivation that explains why the question matters;
- explicit separation of confused concepts;
- clean baseline, impossibility result, or no-effect case;
- mechanism model and proof-level statements where possible;
- controlled evidence;
- real evidence or negative result;
- reconciliation between controlled and real outcomes;
- refined working theory;
- next experiment.

Audit layer, second:

- source map;
- experiment-to-experiment logic table;
- result table with primary metrics and source links;
- table separating proved statements, assumptions, and empirical propositions;
- claim boundary;
- compact appendix listing data, model, training/evaluation settings, seeds,
  checkpoints, scripts, result paths, and primary metrics.

Keep the report compact. Link to anchors and experiment records instead of
copying their setup or result sections wholesale. Do not use a closure report
to introduce new experimental claims. If the mathematical model cannot prove a
stated mechanism, mark the statement as an assumption or empirical proposition
and name the smallest experiment needed to test it.

## External Sync And Handoff

Use these only when explicitly requested. A sync or handoff package should copy
or index existing:

```text
anchor
protocol.md
summary.md
detailed.md
figures/ and tables/ referenced by included docs
short README or index
```

Do not create new claims, second closures, or stronger conclusions in a handoff
package. Do not include raw logs, checkpoints,
datasets, full result directories, unfiltered generated figures/tables, caches,
private notes, unrelated anchors, or code changes unless explicitly requested.

## Mainline Update Test

A result or discussion updates the mainline only if it changes at least one of:

- active route or next project decision;
- anchor evidence;
- refined hypothesis;
- claim boundary;
- next decision;
- graph navigation after user-confirmed research judgment.

If none changed, write:

```text
No mainline update today.
```

## Archive Rule

Keep active `experiments/` focused on the proposition currently being verified.
Move older, superseded, weakly related, or support-only experiments into
`experiments/archive/` with a short index:

```text
archived folder
why archived
when to consult again
```

Archive evidence instead of deleting it unless the user explicitly asks to
delete it.

## Rules

- Keep mainline thin; put reasoning in anchors and result records.
- By default, update only anchor / `protocol.md` / `summary.md` /
  `detailed.md` / daily note.
- Do not create separate implementation-plan files for new work.
- Do not update root sync, sync to an external collaborator repo, package
  handoff reports, edit graph, commit, or push unless the user explicitly asks.
- Do not promote raw logs, checkpoints, datasets, full run directories, or
  unfiltered generated outputs into mainline paths.
- Do not leave completed anchors with stale evidence, claim boundary, next
  decision, or result links.
- When central figures exist, curated copies should appear in the experiment
  `figures/` folder and be embedded and explained in `summary.md` and
  `detailed.md`.
- Markdown formulas must use `$...$` or `$$...$$`.

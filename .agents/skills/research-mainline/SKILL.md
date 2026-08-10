---
name: research-mainline
description: "Organize Research_System project paths, artifact ownership, archive state, and mainline status, and publish the root anchor mirror only when explicitly requested. Use when placing or reorganizing anchors, stories, experiment records, roadmaps, or project state. Do not define research judgment, run experiments, package handoffs, or sync to external collaborator repositories."
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
    stories/
      <line_id>/
        README.md
        <NN>_<topic>.md
        <NN>_<topic>_cn.md
    problem_anchors/
      <line_id>/
        README.md
        <parent_id>_<topic>/
          <parent_id>_<topic>_anchor.md
          <parent_id>_<topic>_anchor_cn.md
          <parent_id>_<topic>_thinking_card.md
          <parent_id>_<topic>_thinking_card_cn.md
          subanchors/
            <parent_id>_<NN>_<topic>_anchor.md
            <parent_id>_<NN>_<topic>_anchor_cn.md
            <parent_id>_<NN>_<topic>_thinking_card.md
            <parent_id>_<NN>_<topic>_thinking_card_cn.md
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

Do not update root sync, graph, commit, or push surfaces unless the user
explicitly asks for that action. External collaborator sync and handoff
packaging belong to `handoff-report-writer`, which is also explicit-only.

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

### Parent Anchor Folders

For every new or reorganized multi-parent research line, use one folder per
parent anchor:

```text
main/problem_anchors/<line_id>/README.md
main/problem_anchors/<line_id>/<parent_id>_<topic>/
  <parent_id>_<topic>_anchor.md
  <parent_id>_<topic>_thinking_card.md
  subanchors/<parent_id>_<NN>_<topic>_anchor.md
```

Sibling parent anchors remain sibling folders even when one depends on another.
Place an anchor in `subanchors/` only when it inherits the parent's decision
question and tests one local clause, rival, repair, robustness check, or metric
guard. Keep each Thinking Card beside the anchor it owns. The line `README.md`
must distinguish sibling-parent dependency order from parent--child ownership.

Before creating or reorganizing a line `README.md`, read
[`references/line_direction_contract.md`](references/line_direction_contract.md)
completely. Put a short direction snapshot before the artifact index. Derive
its state and route from approved Anchors and verified results; never invent a
transition to make the direction look complete.

When migrating a line, move the canonical files instead of copying them, update
the line README plus every project, story, experiment, daily-note, and graph
reference in scope, remove the old path, and check for duplicate canonical
files and broken relative links. Do not leave sibling parents inside another
parent's `subanchors/` directory.

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

### Focus Files

Place a bounded problem update at
`daily_research_reports/MMDD/focus_<problem>.md`; several may exist on one day.
Place every meeting synthesis in a newly created
`daily_research_reports/MMDD/focus_meeting_<topic>.md`. A one-problem meeting
uses the researcher-named problem or note and core question. A multi-problem
meeting requires exact human-selected source paths, exclusions, and one core
question before synthesis. Legacy bare `focus.md` files may remain; do not
migrate them implicitly.

Focus files are human-owned knowledge updates, not experiment-result reports or
canonical project truth. Results appear below the natural-language conclusion
as its explanation. Meeting focuses use a concise progressive question chain,
not a mandatory merge table or evidence ledger. If a focus changes a
hypothesis, evidence boundary, or next decision, also update the smallest
canonical owning artifact.

## Core Artifact Chain

Default chain:

```text
anchor -> protocol.md -> summary.md -> detailed.md -> anchor update
```

Root sync copies, graph edits, commits, and pushes are explicit follow-up
actions only. Handoff packages are explicit follow-up work owned by
`handoff-report-writer`.

Every mainline artifact must be terminology-safe. If a document uses
non-obvious terms, English jargon, abbreviations, metric names, condition
labels, model variants, project shorthand, or plot labels, it must define them
before using them as evidence. Use `Terminology / Definitions` for English
canonical artifacts and `术语解释` for Chinese meeting or companion files.

This chain is the local adapter for the advisor's `research-exploration` spec:

```text
anchor                      = one authoritative current research design
protocol.md                 = one draft-to-approved experiment contract;
                              non-executable until confirmation and consistency
summary.md + detailed.md    = direct result, evidence, and reproducibility
figures / viewer            = optional decision evidence when visual inspection matters
story pair                  = explicit stable line synthesis; no automatic
                              competing final_report layer
```

Do not create the exported `docs/` layout for ordinary mainline work unless the
user asks for that layout. The anchor-first layout remains canonical.

Artifact roles must stay aligned:

| Artifact | Owns | Must not do |
|---|---|---|
| `<anchor_stem>_thinking_card.md` | independent human judgment before AI formalization | become a formal anchor, protocol, or AI-authored conclusion |
| anchor | current minimal adjudicable design | become a runbook, full result report, or broad ablation list |
| `protocol.md` | the single in-file lifecycle from complete candidate to confirmed test | be treated as executable before all audit blocks pass, change the question post hoc, or add unrelated sweeps |
| `summary.md` | first reading path: conclusion, primary metric, central figures | contain the full evidence ledger |
| `detailed.md` | complete evidence ledger, failure decomposition, artifact map | create a second conclusion stronger than the anchor allows |
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

The independent `<anchor_stem>_thinking_card.md` is the human-facing judgment surface. The
formal anchor links that card and contains the auditable design layer for AI
review, replay, protocol alignment, and boundary checks. Do not duplicate the
card in new anchors.

The required anchor structure is:

```text
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

State the Anchor's parent direction, blocking uncertainty, why this is the
smallest direction-changing decision, and how each verdict affects the route.
The line README owns the multi-Anchor map; do not copy its full history.

`Computational Realization` exists to prevent theory/code drift: the anchor
must say what input objects, computed variables, algorithm stages,
stage-local evidence, and expected artifacts instantiate the mathematical
model before the protocol or implementation expands it.

### Protocol

`protocol.md` is the single draft-to-approved experiment design. AI writes the
complete candidate there first as `DRAFT_NOT_EXECUTABLE`, covering
question/boundary, data, task/supervision, model/architecture,
objective/optimization, comparison/evidence, and execution/reproducibility.
It then surfaces only decision-critical items for review, updates the same file
after corrections, and promotes it after confirmation and a cross-block
consistency pass. Do not create a separate draft execution-plan artifact.

Its first page should be an `Approval Snapshot`: document state, purpose, anchor alignment,
minimal setup, conditions to run, primary metric, pass/fail/insufficient
criteria, claim boundary, and approval decision. Put stage profiling,
algorithm details, commands, and artifact maps after this snapshot.

It must include the decision question, tested hypothesis, rival explanations,
data construction/provenance, learning task/supervision, model/architecture,
training objective/optimization, conditions, primary and secondary metrics,
known cases, stage-level profiling, success/failure/insufficient meanings,
cannot-claim boundary, block confirmation ledger, and approval status.

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

When central visual evidence exists, it must absorb the relevant
research-exploration viewer role: each central figure should explain what it
tests, how to read it, observed result, take-home, and what it does not prove.
Keep only figures that support the current claim boundary or next decision.

### Detailed

`detailed.md` is the full evidence ledger. It must include protocol compliance
audit, setup, metrics, stage evidence, failure decomposition, full experiment
record, interpretation, claim boundary, next decision, and artifact map. Add a
`Visualization Results` section only when visual evidence is decision-relevant.

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

### Story

`main/stories/<line>/` is the line-level synthesis surface. Use it when the
user asks to summarize, audit, or understand a research line as a unit. Do not
create a separate closure or final-report tree that duplicates the story.

The English canonical story and Chinese `_cn.md` companion must share the same
numbered subject-bearing stem and match on claims, metrics, boundaries, and the
next decision.

A formal story uses two layers.

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

Keep the story compact. Link to anchors and experiment records instead of
copying their setup or result sections wholesale. Do not use a story to
introduce new experimental claims. If the mathematical model cannot prove a
stated mechanism, mark the statement as an assumption or empirical proposition
and name the smallest experiment needed to test it.

## Publication And Handoff Routing

This skill owns only project organization and an explicitly requested root
anchor-mirror publication. For an external collaborator sync or handoff
package, switch to `handoff-report-writer`; this skill may identify the
canonical source artifacts and destination path, but it must not copy or
package them.

The handoff skill may copy or index existing:

```text
anchor
protocol.md
summary.md
detailed.md
figures/ and tables/ referenced by included docs
short README or index
```

Do not create new claims, independent syntheses, or stronger conclusions in a
handoff package. Do not include raw logs, checkpoints,
datasets, full result directories, unfiltered generated figures/tables, caches,
private notes, unrelated anchors, or code changes unless explicitly requested.

When the user explicitly requests the root anchor mirror, publish and validate
it through:

```text
python .agents/skills/research-mainline/scripts/publish_anchor_mirror.py
python .agents/skills/research-mainline/scripts/publish_anchor_mirror.py --check
```

The generated mirror keeps internal links relative and rewrites links that
leave `problem_anchors/` to repository-root absolute paths. Do not hand-edit
generated mirror files.

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
- Do not update root sync, edit graph, commit, or push unless the user
  explicitly asks. Never perform external collaborator sync or handoff
  packaging through this skill; route that explicit request to
  `handoff-report-writer`.
- Do not promote raw logs, checkpoints, datasets, full run directories, or
  unfiltered generated outputs into mainline paths.
- Do not leave completed anchors with stale evidence, claim boundary, next
  decision, or result links.
- When central figures exist, curated copies should appear in the experiment
  `figures/` folder and be embedded and explained in `summary.md` and
  `detailed.md`.
- Markdown formulas must use `$...$` or `$$...$$`.

# Research System

This repository preserves research judgment, designs, evidence, and process.
Experiment code, remote runs, raw outputs, checkpoints, and logs stay in the
corresponding execution workspace.

## Entry Points

- `AGENTS.md`: stable behavior, scientific invariants, authority, and approval
  boundaries.
- `PROJECTS.md`: active projects and workstreams, their priorities, current
  Focus paths, scientific boundaries, and resume points.
- `daily_research_reports/MMDD/focus_<problem>.md`: one workstream's living
  meeting-cycle question, confirmed plain-language design, result boundary,
  and next decision.
- `Projects/<project>/main/problem_anchors/`: canonical current research
  designs. An Anchor fulfills the role of `design.md`; do not create both.
- `Projects/<project>/main/experiments/`: Protocol, Summary, Detailed record,
  and decision-bearing figures or tables.
- `.agents/skills/`: repository Skills discovered directly by Codex. See
  `docs/skills.md` for the trigger index.
- `templates/`: the only maintained reusable-template area.
- `sync/`: an explicitly published derived reading surface, never a source of
  scientific truth.

For a narrow explanation, number, status, or named-file audit, start from that
source. Do not load this whole map merely because it exists.

## Research Flow

```text
select or activate one workstream
-> focus_<problem>.md
-> canonical Anchor
-> protocol.md
-> approved execution scope
-> summary.md + detailed.md
-> researcher-confirmed result, boundary, and next decision
-> Focus and Anchor update
-> optional daily report, meeting material, story, Graph, or sync publication
```

### 1. Focus

Creating or resetting a Focus is a researcher-owned decision. Each active
workstream has one current Focus, one core question, one next decision, and at
most three necessary experiments. Each experiment uses:

```text
Purpose -> Hypothesis -> Analysis method -> Conclusion or outcome branches
```

Focus metadata keeps four independent fields:

```text
task_state
question_state
design_state
result_state
```

Protocol approval and execution status are not copied into the Focus.

### 2. Anchor

The Anchor is the sole canonical current design. It connects the problem,
physical prior, falsifiable hypotheses, mathematical model, constructible
computation, minimum falsifier, current evidence, claim boundary, and exactly
one next decision. Run settings and commands do not belong there.

### 3. Formal Experiment

```text
Anchor -> protocol.md -> summary.md -> detailed.md -> Anchor update
```

- `protocol.md` owns the frozen test contract and approval scope. Drafting does
  not authorize execution.
- `summary.md` owns the complete first result reading: Purpose, Hypothesis,
  Analysis method, Conclusion, central evidence, boundary, and next-step
  analysis.
- `detailed.md` owns execution state, complete setup, conformance and
  deviations, evidence lineage, failures, full results, and artifact map.
- Code, logs, checkpoints, datasets, and unfiltered outputs remain in the
  execution workspace.

After evidence exists, the researcher states or confirms the direct result,
claim boundary, and one next decision. AI verifies those statements without
strengthening them. Update the Focus and Anchor only with that confirmed
meaning.

### 4. Derived Reading Surfaces

- `daily_research_reports/MMDD/docs/daily_report_<topic>.md`: delayed,
  self-contained explanation written only after the source Focus has
  `result_state: HUMAN_CONFIRMED`.
- `focus_meeting_<topic>.md`: created only for an explicitly requested meeting
  brief or synthesis; an ordinary one-problem meeting uses its Focus.
- Story: explicitly requested line-level mathematical or evidence synthesis.
- Graph: thin navigation between questions, claims, methods, evidence, and
  tasks.
- Root `sync/`: explicitly requested external-reading publication.

Derived views may summarize canonical sources but cannot create or strengthen
a scientific claim.

## Operational Coordination

`researchctl` is a tracked repository-local executable. It needs no package
installation or background process:

```text
./researchctl context <problem_key> --task "<concrete part>" [--path <path> ...]
./researchctl release [task_id]
./researchctl status [problem_key] [--all]
./researchctl check [problem_key]
./researchctl check --repository
```

Use `context` before changing a registered scientific problem. Repository
maintenance and read-only explanations need no invented problem key. Multiple
conversations may handle different parts of the same problem; same-problem and
path overlap are advisory only and never block work or transfer authority.

If this repository directory survives a container restart, both `researchctl`
and repository Skills remain available without reinstallation. The runtime
registry survives only when `.research/runtime/` is on persistent storage; it
is operational state and is not restored by a fresh Git clone.

## Context And Artifact Rule

- Read `PROJECTS.md` only for workstream selection or project-level state.
- Read a Graph only for navigation, graph work, or graph-dependent synthesis.
- Load one matching Skill and only the reference needed for the requested
  outcome.
- A narrow answer, local diagnosis, or temporary exploration creates no
  canonical artifact by default.
- Create a document only when it has a distinct owner and durable research or
  communication value.
- Chat history is context, not canonical research memory.

## Communication

Canonical artifacts are English unless the researcher chooses otherwise;
Chinese companions use `_cn.md`. Lead with the answer, define indispensable
terms, separate evidence from interpretation, and preserve negative or
insufficient results.

When a completed experiment has `summary.md`, link it first in chat and do not
rewrite its four-part account. Give only the direct verdict, smallest decisive
value, important figure and reading, nearest boundary, and next-step analysis.
Label an unconfirmed next step `AI 建议`.

## Approval And Completion

Proceed with local reads, in-scope edits, relevant tests, and non-destructive
verification. Pause for a missing human scientific judgment, an expensive full
remote run, destructive or external action, material scope expansion,
publication, collaborator sync, commit, or push.

Finish when the requested deliverable exists, decision-bearing claims trace to
evidence, proportionate checks pass, and no in-scope work remains without new
evidence or human authority. A first draft or first successful implementation
is not completion by itself.

## Supporting Areas

- `paper_reading/`: source-grounded literature records.
- `papers/`: paper-writing workspaces derived from canonical evidence.
- `prompts/`: supporting prompts for environments that cannot use repository
  Skills directly.
- `docs/`: terminology, Skill index, examples, and setup notes.

No root document should duplicate current project conclusions from
`PROJECTS.md`, Anchors, or result records.

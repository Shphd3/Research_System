# Research System

This repository preserves research judgment, designs, evidence, and process.
Experiment code, remote runs, raw outputs, checkpoints, and logs stay in the
corresponding execution workspace.

## Entry Points

- `AGENTS.md`: stable behavior, scientific invariants, authority, and approval
  boundaries.
- `PROJECTS.md`: active projects and workstreams, their priorities, current
  Focus paths, scientific boundaries, and resume points.
- `docs/training_reuse_index.md`: verified map of previous training code,
  datasets, tokenizer, historical runs, and reuse warnings. Read it before a
  new model-training implementation or an explicit prior-code reuse request.
- `docs/training_observability_contract.md`: required TensorBoard loss records,
  valid-token comparison coordinate, global-batch matching, and schedule/resume
  rules for every new model-training run.
- `daily_research_reports/MMDD/focus_<problem>.md`: one workstream's living
  meeting-cycle question, confirmed plain-language design, result boundary,
  and next decision.
- `Projects/<project>/main/problem_anchors/`: canonical current research
  designs. An Anchor fulfills the role of `design.md`; do not create both.
- `Projects/<project>/main/experiments/`: Protocol, Summary, Detailed record,
  and decision-bearing figures or tables.
- `.agents/skills/`: repository Skills discovered directly by Codex. See
  `docs/skills.md` for the trigger index.
- `.research/memory/conversations/`: versionable cumulative working logs for
  continuing one logical conversation across Codex threads or accounts. Each
  checkpoint appends a timestamped entry; records are non-canonical and do not
  represent scientific consensus.
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

Read the owning Focus, Anchor, Protocol, or result record before changing a
scientific problem. Multiple conversations may work independently; the
researcher decides when coordination is needed. There is no repository-local
task registry or mandatory global checker.

Training submission remains deterministic without a general control plane:
`templates/execution/acp_submit_template.sh` calls the small, dedicated
`templates/execution/resolve_execution_envelope.py` resolver. Skills explain
the workflow; this resolver only turns selected profile and image keys into the
exact runtime values required by the shell command.

Conversation memory is ordinary repository content rather than runtime state.
It may be versioned when continuity across checkouts is wanted; a fresh clone
receives only committed checkpoints. Git presence never grants scientific
approval or makes a memory statement canonical. Each Codex conversation gets
its own conversation-named record on first write; later checkpoints from that
same conversation append a new timestamped entry instead of replacing the
snapshot.

## Context And Artifact Rule

- Read `PROJECTS.md` only for workstream selection or project-level state.
- Read a Graph only for navigation, graph work, or graph-dependent synthesis.
- Load one matching Skill and only the reference needed for the requested
  outcome.
- When resuming conversation memory, read the named record's `memory.md` in
  full (the accumulating log; the newest entry is the current state). There is
  no `history.md`.
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

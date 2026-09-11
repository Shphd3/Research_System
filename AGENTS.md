# Codex Research System

This repository preserves research judgment, designs, evidence, and process.
Experiment code, remote runs, raw outputs, checkpoints, and logs remain in the
corresponding execution workspace.

## Language And Communication

- Default conversation language is Chinese. Canonical research artifacts are
  English unless the researcher chooses otherwise; Chinese companions use
  `_cn.md`.
- Lead with the answer. Include only the reasoning, evidence boundary, and next
  decision needed for the question.
- Define an indispensable technical term in plain Chinese before reusing its
  English name or abbreviation. Use `$...$` and `$$...$$` for formulas.
- Treat proposed ideas as hypotheses. Distinguish direct result, observation,
  interpretation, claim, speculation, limitation, and decision.
- Prefer precise prose to process narration, generic background, or repeated
  caveats. Use a table or figure only when it makes a decisive relation easier
  to understand.

## Human And AI Authority

The researcher owns:

- the active research question and its priority;
- mechanism judgment, uncertainty, and the strongest rival;
- scientific approval, claim boundaries, and scientific state transitions;
- the final interpretation of completed evidence.

AI may retrieve evidence, audit logic, propose labeled alternatives, formalize
approved work, implement in-scope changes, run proportionate checks, and
maintain operational records. AI must not infer missing human judgment,
silently strengthen a claim, or treat a filename, run label, diagnostic, or
expected pattern as evidence.

`Unknown` is a valid scientific state.

## Context And Concurrent Work

Load context according to the task:

- For a narrow explanation, number, run status, or named-file audit, begin with
  that source and follow only links needed to answer.
- Read `PROJECTS.md` when selecting a workstream or checking project-level
  scientific state. Read a Graph only for navigation, graph maintenance, or an
  explicitly graph-dependent synthesis.
- Before changing a registered scientific problem, use
  `./researchctl context <problem_key> --task "<concrete part>"` and add
  `--path <expected-path>` when known. Read only the returned Focus or Anchor
  and sources needed for that part.
- Repository maintenance does not invent a scientific `problem_key` and does
  not require registration.

One conversation records at most one open task, but many conversations may
work on different parts of the same problem. `researchctl` reports same-problem
and path overlap as advisory information only. An overlap never blocks work,
expires work, transfers scientific authority, or chooses a winner; the
researcher decides whether coordination is needed. Close the task with
`./researchctl release` when its stated part is completed or abandoned. A
named stale task may be closed as registry cleanup; that does not transfer or
change scientific authority.

Do not use chat history as the canonical research memory.

For cross-session continuation, use
`.research/memory/conversations/<conversation>/memory.md` as non-canonical
working context: one log per conversation, named by conversation, where each
checkpoint appends a timestamped summary and never replaces older ones. Load it
only when resuming or recalling that conversation; otherwise load none. First
write creates a distinct record rather than overwriting another conversation's
memory. Resume reads the whole log; the newest entry is the current state.
Verify claims and approvals against the owning Focus, Anchor, Protocol, Summary,
or Detailed record; versioning never makes memory canonical. Each record notes
its processing agent (Codex, DeepSeek, or DeepSeek via Claude). Use
`research-memory` for creation, checkpointing, and retrieval.

## Scientific Invariants

### Focus

Each researcher-activated workstream has one current meeting-cycle
`focus_<problem>.md`, one core question, and one next decision. A Focus may
contain up to three genuinely necessary experiments serving that question.
Creating or resetting a Focus is a human-owned scientific transition; do it
only after the researcher explicitly activates an independent question and
confirms its stable `problem_key` and next decision.

Before execution, the experiment's four parts — Purpose, Hypothesis, Analysis
method, and the pre-registered decision branches — are owned by `protocol.md`.
The Focus names each experiment, its one-line purpose, the outcome that would
separate the strongest rival, and the protocol path; it does not restate the
protocol body.

After execution, the researcher owns the Focus-level updated judgment,
cannot-claim boundary, and next decision. The experiment-level four-part result
is owned by `summary.md` with its Chinese companion `summary_cn.md`; the full
round record is owned by `detailed.md`. AI verifies these against evidence
without strengthening them, and never copies a protocol or summary body into the
Focus. The Focus keeps one rolling round summary compressed from `detailed.md`,
one row per round; the same round history kept in two places is `FAIL`.

Focus lifecycle fields are orthogonal: `task_state`, `question_state`,
`design_state`, and `result_state`. Protocol approval is owned only by
`protocol.md`; execution status is owned only by `detailed.md` or its execution
record. Do not combine or mirror these states in a single Focus `status`.

### Anchor

The project Anchor is the sole canonical current research design; do not create
a parallel `design.md`. It must be self-contained enough to adjudicate the
question and must connect problem, priors, falsifiable hypotheses,
mathematical model, constructible computation, minimum falsifier, current
evidence, claim boundary, and exactly one next decision. Update the same Anchor
as evidence changes the design. Detailed structure and checks belong to
`problem-anchor-writer`.

### Formal Experiments And Evidence

The canonical chain is:

```text
Anchor -> protocol.md -> summary.md -> detailed.md -> Anchor update
```

- `protocol.md` is the approved test contract. Drafting it does not authorize
  implementation or execution.
- A full or expensive remote run requires explicit execution approval for its
  scope. Small local implementation checks do not.
- `summary.md` owns the first result reading path and `summary_cn.md` is its
  Chinese companion; `detailed.md` owns complete setup, provenance, deviations,
  tables, failures, and artifact map.
- A reader-friendly daily report is written only after canonical evidence
  exists and the researcher has stated or approved the result, boundary, and
  next decision. It explains but does not replace the evidence records.
- Add conditions, seeds, diagnostics, and artifacts only when they separate a
  named rival, protect the main conclusion, or are required for reproducibility.
- A reader-facing artifact references only figures that physically live under
  its own date `figures/` directory, by a date-local relative path. The
  experiment keeps the evidence copy; the date copy is the reading copy. Copies
  are expected, and the date directory records where each came from.

## Learning And Group Meeting Updates

- Anchor each group meeting in one explicit, bounded, falsifiable mechanism
  question. A definite question does not require a predetermined or positive
  answer; `Unknown` remains valid when evidence is insufficient.
- The primary deliverable is a knowledge update: the prior explanation, its
  strongest rival, the evidence that separates them, what is now understood
  about why a method works or fails, and the remaining boundary and next
  decision. Distinguish a literature-derived insight from a newly established
  empirical mechanism.
- Run completion, debugging, parameter sweeps, and metric changes are supporting
  evidence, not the meeting's central contribution. An experiment matters
  because it changes a mechanism judgment; do not present implementation
  progress or a tuning summary as that judgment.
- Do not manufacture a causal explanation from a performance change or a
  representation diagnostic. State which link is supported, which rival
  remains, and what would falsify the proposed explanation.
- Daily research plans must reserve protected time for learning and independent
  explanation. Specify the minimum reading order, the question each reading
  resolves, and a small comprehension output before allocating implementation
  work. Do not let monitoring or unfinished runs consume the learning plan.

## Result Reading And Reply

`summary.md` is the complete first reading surface for a finished experiment;
`summary_cn.md` is its Chinese companion and carries the same four-part body.
Its reader body uses Purpose, Hypothesis, Analysis method, and Conclusion. Put
the full, evidence-grounded four-part account there once; do not reproduce it
in chat with merely different wording.

When `summary.md` exists, the chat response begins with its link so the
researcher can read that account first. Then give only:

- the direct verdict and smallest decisive value;
- the smallest sufficient set of important figures, each beside the conclusion
  it supports with one sentence explaining how to read it;
- the nearest claim boundary;
- analysis of the next step: which unresolved uncertainty it targets, why it
  follows from this result, and what outcome would stop or redirect it.

If the next step has not been confirmed by the researcher, label it `AI 建议`;
do not write it as an owned scientific decision. Use the four-part format in
chat only when no canonical Summary exists or the researcher explicitly asks
for a standalone speaking or meeting brief.

Background, implementation history, run order, and secondary diagnostics stay
out unless they determine evidence eligibility or are necessary to understand
a decisive comparison. Omit decorative, redundant, or ineligible figures and
never manufacture missing evidence. Keep semantic routing, expert utility under
intervention, end-task performance, and representation accessibility distinct
when applicable.

## State Ownership

| Surface | Owns |
|---|---|
| `AGENTS.md` | Stable behavior, scientific invariants, and boundaries |
| `PROJECTS.md` | Scientific project map, active workstreams, priorities, and project decisions |
| `.research/runtime/state.json` | Machine-written task routing and advisory overlap events only |
| `.research/memory/conversations/` | Versionable, non-canonical cumulative conversation working context only |
| `focus_<problem>.md` | Human-owned current task, result boundary, and next decision |
| Anchor | Canonical current research design and its boundary |
| `protocol.md` | Experiment contract and its approval state |
| `docs/execution_envelope.md` | Target profile, image and runtime-layer registry, submission entry point, and execution-certificate contract |
| `summary.md` / `summary_cn.md` / `detailed.md` | Canonical result reading path and its Chinese companion / evidence ledger and execution state |
| Graph, story, daily report, root `sync/` | Derived navigation or reading views |

Machine state must never own scientific claims, approval, priority, verdicts,
or next decisions. If a derived view conflicts with its canonical source,
repair or regenerate the view; do not create another source of truth.

## Autonomy And Approval

Proceed by default with local reads, in-scope edits, relevant tests, and
non-destructive verification. Pause only when the next action requires:

- a human-owned scientific state transition or missing judgment that changes
  the outcome;
- an expensive or full remote run whose profile, image, or scope is not already
  fixed by an authorized protocol. A submission that resolves to the execution
  envelope's default profile under an authorized protocol scope is execution,
  not a new approval gate;
- a destructive or external action, including publication, collaborator sync,
  commit, or push;
- material expansion beyond the requested scope.

Warnings from `researchctl` are not approval gates. Protocol drafting is not
execution approval.

## Completion Rule

Continue until the requested deliverable exists, decision-bearing claims trace
to evidence, proportionate checks pass, material failures and unknowns are
recorded, and no remaining in-scope work can proceed without new evidence or
human authority. A first draft or first successful implementation is not a
completion condition by itself.

For a narrow answer, completion means the question is answered and its evidence
boundary is explicit; it does not require a canonical artifact. For a formal
design, experiment, result record, or publication task, use the completion
contract in the matching Skill.

## Skill Router

Repository Skills live in `.agents/skills/`. Load a Skill only when its
description matches the task; then follow only the relevant reference or
script it routes to.

- `research-progress-core`: Focus, research judgment, falsifiers, failures, and
  delayed daily reports.
- `problem-anchor-writer`: Anchor creation, revision, and design audit.
- `experiment-card-writer`: Protocol and canonical result records.
- `research-document-explainer`: concise explanation of research documents,
  formulas, evidence, and results.
- `research-communication`: explicit meeting brief, story, or curated handoff.
- `research-memory`: non-canonical cross-session working context.
- `research-sync-gate`: readiness for advisor sync or one next question.
- `research-mainline`: project placement, archive state, and explicit root
  publication.
- `research-graph-sop`: graph inspection or maintenance.
- `remote-experiment-workflow`: remote execution logistics and artifact maps.
  It resolves the target profile, image key, and submission entry point from
  `docs/execution_envelope.md` before any submission.
- `scholar-mode`: unsettled scientific ideas, papers, theory, and literature.
- `sidecar-thinking`: explicit local graph display.

User instructions take precedence over Skill workflow preferences. A Skill may
not invent approval requirements beyond the boundaries above.

## Repository And Git Boundaries

Keep canonical process artifacts in this repository and raw execution material
in its execution workspace. Do not promote raw outputs, checkpoints, datasets,
or unfiltered logs into the research mainline. Root `templates/` is the only
maintained reusable-template location.

Never revert user changes. Commit, push, publish, edit an existing Graph, or
sync to another repository only when explicitly requested.

Use `./researchctl check --repository` for deterministic checks of current
Focus state, registered references, Protocol authorization records,
PROJECTS--Focus drift, Skill references, and declared execution keys against
`docs/execution_envelope.md`. Treat overlap and derived-view drift as visible
reminders, not automatic scientific or publication actions.

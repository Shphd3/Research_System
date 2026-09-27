# Codex Research System

Research judgment/designs/evidence belong here; experiment code, raw outputs,
logs, datasets and checkpoints belong in the execution workspace.

## Communication And Authority

- Converse in Chinese; canonical artifacts are English unless the researcher
  chooses otherwise, with `_cn.md` companions. Define essential terms in plain
  Chinese; use `\(...\)` / `\[...\]`. Lead with the answer, boundary and needed
  decision; favor precise prose over narration and decorative figures/tables.
  Math formatting follows [docs/markdown_math.md](docs/markdown_math.md): Codex-first
  delimiters, standalone display blocks, and unchanged literal code/currency.
- Distinguish direct result, observation, interpretation, hypothesis, claim,
  speculation, limitation and decision; proposed/expected patterns are not evidence.
- The researcher owns questions, priorities, mechanism judgments, uncertainty,
  strongest rivals, scientific approval, claim boundaries, state transitions
  and final interpretations. `Unknown` is valid.
- AI may retrieve/audit, propose labeled alternatives, formalize approved work,
  implement/verify in-scope changes and maintain operational records. Never
  invent judgment, strengthen claims or treat names/diagnostics as proof.
  Concurrent chats transfer no authority; the researcher decides coordination.

## Read Only The Context Needed

- Named question/result/status: start at its source; follow needed links only.
- Select/check a workstream through `PROJECTS.md` and its Focus/Anchor; read
  current Focus or Anchor before changing the problem. Graphs/indexes/Stories
  are optional navigation/synthesis. Load only matching Skills/references.
- Before proposing training implementation or reusing prior project code, read
  `docs/training_reuse_index.md`, inspect sources, and state what to reuse,
  adapt or reject before writing code.
- Before relying on active workstream links, run
  `python tools/check_current_entrypoints.py`: existence/versioning only, never
  a scientific verdict or approval.

Use the same authority and output contracts across models. Select the Skill
that owns the requested deliverable; add another only for a necessary subtask.
Reuse unchanged instructions already in context, but refresh decision-bearing
sources before acting or editing. A model switch is not new authorization.
For a supplied operational continuation brief, use `research-memory` brief mode
and its required sources; an explicitly resumed log still follows the full-log
rule below. Keep write scopes disjoint during concurrent work.

Chat/memory is never scientific authority. Use `research-memory` and
`.research/memory/conversations/<conversation>/memory.md`: one distinct log per
conversation, timestamped append-only checkpoints with processing-agent identity.
Never overwrite earlier entries/other conversations. Load only to resume/recall
that conversation; read the whole log, newest entry last as working state. Verify claims/approvals
against Focus/Anchor/Protocol/Summary/Detailed; versioning grants no authority.

## Scientific Records

### Focus

Each researcher-activated workstream has one current `focus_<problem>.md`, one
core question and one next decision, with at most three necessary experiments.
Create/reset only after the researcher activates an independent question and
confirms its stable `problem_key` and next decision.

Focus states Purpose, Hypothesis, Analysis method and preregistered supporting/
non-supporting/insufficient branches in plain language before execution;
Protocol states them precisely. No contradictions: Protocol governs execution,
Focus intended meaning, without copying Protocol numbers. Afterward, the
researcher owns judgment, cannot-claim boundary and next decision. Never paste
Protocol/Summary bodies into Focus or strengthen evidence.

Keep one rolling summary from Detailed, one row per round; duplicate round
histories are `FAIL`. Lifecycle fields are independent:
`task_state`, `question_state`, `design_state`, `result_state`. Do not combine
them into `status`, mirror Protocol approval, or mirror execution state.
Use `research-progress-core` for the detailed Focus contract.

### Anchor And Experiments

Anchor is the sole current design, with no parallel `design.md`: self-contained
problem, priors, falsifiable hypotheses, mathematical model, constructible
computation, minimum falsifier, evidence, boundary, exactly one next decision.
Update the same Anchor; use `problem-anchor-writer` for structure/checks.

```text
Anchor -> protocol.md -> summary.md / summary_cn.md -> detailed.md -> Anchor update
```

- Protocol owns contract/approval; drafting authorizes neither implementation
  nor execution. Full/expensive remote runs require scoped approval; small local
  implementation checks do not.
- Summary is the complete first result reading surface; its Chinese companion
  carries the same **Purpose, Hypothesis, Analysis method, Conclusion** body.
  Detailed owns setup, provenance, deviations, tables, failures and artifact map.
- One round is one day's work. Detailed records in order: question/hypothesis;
  setup/controls; data; test/confirmation split; result or `NOT RUN`; insight,
  boundary update and next decision. First four plus `NOT RUN` is a complete
  round; completed results require all six.
- Add conditions, seeds, diagnostics or artifacts only to separate a named
  rival, protect the conclusion or reproduce it.
- A proposed research test must separate named explanations and state how
  supporting, non-supporting and insufficient outcomes change the judgment.
- One question gets one paper-style final report after its Anchor settles and
  the researcher confirms result, boundary and next question. Use
  `research-final-report`; it explains, never replaces evidence.
- In external exploration workflows, Anchor replaces `design.md`; Protocol,
  Summary and Detailed remain contract/result/iteration, Focus an extra card.

Before any new training implementation/run, read and follow
`docs/training_observability_contract.md`. It owns required TensorBoard scalars
and normalization, token-based comparison/batch matching, Protocol freezes and
finite/token-count/resume smoke checks. Missing/ambiguous records make affected
comparisons ineligible. Do not duplicate or weaken that contract.

## Learning, Meetings And Result Replies

Meetings center one bounded falsifiable mechanism question, not a required
positive answer. Deliver prior explanation, strongest rival, separating
evidence, knowledge update, boundary and next decision. Separate literature
insight from newly measured mechanism. Completion/debugging/sweeps/metric changes
are supporting work, not mechanism judgment. Performance/geometry alone cannot
establish causality: state the supported link, rival and falsifier. Keep
accessibility, semantic routing, intervened expert utility and performance distinct.

Daily plans protect learning/independent explanation before implementation:
minimum reading order, each source's question and a small comprehension output.
Monitoring/unfinished runs cannot consume this time. Daily reports wait for
canonical results and human Focus judgment; `Unknown` leaves them pending.
Link Focus/Anchor/Summary/Detailed; state one update, rival, boundary and human
next decision without copying result bodies, ledgers or large tables.

With Summary, start replies with its link, then give verdict/smallest decisive
value, minimal decisive figures beside their conclusions with one reading
sentence, nearest boundary and next-step uncertainty/rationale/stop outcome.
Unconfirmed next steps are `AI 建议`. Repeat the four-part body in chat only
without Summary or for a requested standalone speaking/meeting brief. Include
history/secondary diagnostics only for eligibility or the decisive comparison;
never manufacture evidence or show ineligible/redundant/decorative figures.

## Remaining State Ownership

Focus, Anchor, Protocol, Summary and Detailed own the roles specified above;
execution state belongs only to Detailed or its execution record.

| Surface | Owns |
|---|---|
| `AGENTS.md` | Stable behavior and scientific boundaries |
| `PROJECTS.md` | Project map, workstreams, priorities and project decisions |
| Conversation memory | Non-canonical working context only |
| `docs/execution_envelope.md` | Profiles, image/runtime registry, submission and execution certificates |
| `docs/training_observability_contract.md` | Telemetry, normalization and comparison coordinates |
| Final report, Graph, Story, roadmap, sync | Derived reading/navigation |

Machine state owns no scientific claims, approvals, priorities, verdicts or next
decisions. Repair conflicting derived views from their source, not another authority.

## Autonomy, Execution And Completion

Proceed with local reads, in-scope edits/tests and non-destructive checks. Pause
only for missing human scientific judgment/state transitions, material scope
expansion, destructive/external actions, or full/expensive remote runs without
authorized profile/image/scope. An authorized Protocol using the envelope's
default profile creates no new gate. User instructions outrank Skill preferences;
Skills cannot invent approval gates. Do not re-request approval already given
for the same action and scope.

Absent requested continuous/completion-time monitoring, verify bounded startup
(scheduling, runtime/workers, Smoke/first progress gate, immediate failures),
report job ID, verified progress, boundary and evidence-based ETA, then stop
polling while it runs. Later inspect that job; do not resubmit because monitoring ended.

Complete the deliverable, evidence trace, proportionate checks and failure/
unknown record; continue while authorized work remains possible. First drafts
or first successful implementations are insufficient. Narrow answers need no
formal artifact; formal work follows its Skill completion contract.

## Skills And Storage

Use `.agents/skills/<name>/SKILL.md` only for its matching task, then only the
references it routes to:

| Task | Skill |
|---|---|
| Purpose, causal logic, rivals, proxy/construct audit | `research-reasoning-auditor` |
| Focus, judgment, falsifier, failure | `research-progress-core` |
| Anchor creation/revision/design audit | `problem-anchor-writer` |
| Protocol and canonical result records | `experiment-card-writer` |
| Settled-question final report | `research-final-report` |
| Explain documents, formulas, evidence | `research-document-explainer` |
| Requested meeting, Story, handoff/sync | `research-communication` |
| Conversation working context | `research-memory` |
| Advisor readiness or one next question | `research-sync-gate` |
| Placement, archival, explicit root publication | `research-mainline` |
| Explicit Graph work | `research-graph-sop` |
| Remote operations/artifact maps | `remote-experiment-workflow` |
| Unsettled theory/method/literature | `scholar-mode` |
| Explicit local graph display | `sidecar-thinking` |

Resolve remote profile/image/entry point from `docs/execution_envelope.md`.
Root `templates/` alone owns reusable templates. Git tracks research text,
scripts, configs and small provenance manifests. Raw execution and generated
tables/figures/logs/caches/fonts stay local/execution-side with paths/digests in
Detailed; explicitly requested curated packages may carry reading copies.

Dated reader artifacts display only figures physically in their date's
`figures/`, linked date-relatively. Keep experiment evidence/date reading copies
with recorded origins; `research-mainline` owns placement details. No raw outputs
in the mainline.

Never revert user changes. Commit, push, publish, edit an existing Graph or sync
to another repository only on explicit request. Before commit run
`python tools/check_git_payload.py`. Use focused tests/source inspection; do not
require a repository-wide registry or task-tracking command.

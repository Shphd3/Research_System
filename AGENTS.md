# Research System

Research judgment, designs and evidence belong here. Experiment code, raw data,
outputs, logs and checkpoints belong in the execution workspace.

## Authority And Communication

Converse in Chinese. Canonical artifacts are English with `_cn.md` companions
unless the researcher chooses otherwise. Lead with the answer and its boundary;
define essential terms before notation. Use precise prose, not compulsory
headings or decorative tables. Math follows [docs/markdown_math.md](docs/markdown_math.md).

Separate observations, derivations, interpretations, hypotheses and decisions.
The researcher owns questions, priorities, strongest rivals, mechanism judgment,
scientific approval, claim boundaries and state transitions. AI may inspect,
audit, offer labeled alternatives, formalize confirmed choices, and implement
and verify authorized work. Missing judgment stays `Unknown`; a successful run,
audit, model switch or another conversation supplies no scientific authority.

## Context And Reasoning

Start at the named source. Use `PROJECTS.md` only to select a workstream; inspect
its current Focus/Anchor before changing its question. Check existing derivations
and evidence before declaring something missing. Distinguish an absent model,
an unshown derivation, an untested mechanism and an unsupported decision leap.
If access is incomplete, bound the search claim rather than asserting absence.

Select the task owner in [docs/skills.md](docs/skills.md) and only needed references.
Reuse unchanged guidance; refresh decision-bearing sources. Apply the
[method kernel](docs/methodology/research_exploration_kernel.md) by research stage,
not as a serial skill chain. Preserve useful conjectures and counterexamples.

Before relying on active workstream paths run `python tools/check_current_entrypoints.py`;
it checks navigation, not scientific validity. Before new training implementation
or code reuse inspect `docs/training_reuse_index.md` and the actual source;
state reuse, adaptation or rejection. Training and comparisons must follow
`docs/training_observability_contract.md`; do not duplicate or weaken its
telemetry, token/batch normalization, freeze or resume checks.

Memory is non-canonical. `research-memory` keeps one conversation log with
timestamped, agent-identified append-only entries; never overwrite earlier or
other conversations' entries. Explicit resumption reads the full log. Verify
scientific claims and approval against their owners, not memory.

## Record Ownership

| Record | Owns |
|---|---|
| `PROJECTS.md` | Stable workstream navigation and source links, not copied results or next steps |
| Focus | One activated question and researcher-owned next decision |
| Anchor | Sole current scientific design; never a parallel `design.md` |
| Protocol | Exact experiment contract, review, approval and amendments |
| Summary / `_cn.md` | Complete Purpose, Hypothesis, Analysis method, Conclusion |
| Detailed / execution record | Setup, provenance, deviations, results and execution state |
| Meeting brief / Story / final report / Graph / sync | Derived explanation or navigation, not new authority |
| `docs/execution_envelope.md` | Profiles, images, submission and execution certificates |

Keep one current Focus per workstream at its existing path across dates,
meetings and conversations; language companions are one record. Create/reset
only after researcher activation of an independent question, stable `problem_key`
and next decision. New results or reports do not create another Focus.
Keep at most three necessary experiments. Preserve independent `task_state`,
`question_state`, `design_state`, `result_state`; do not mirror execution/approval.
Focus holds human scientific judgment and source links, not duplicated result
tables, round ledgers or speaking scripts.

Anchor keeps its eight-section contract through `problem-anchor-writer`.
A round records question/hypothesis, setup/controls, data, confirmation split,
result or `NOT RUN`, and insight/boundary/next decision. Planned rounds may stop
at `NOT RUN`; completed rounds need all six. Preserve full evidence once, not
duplicate histories. Finish authorized factual records even when human
interpretation is unknown. Never reinterpret frozen results during refactoring.

Experiments need a named uncertainty, credible alternative, distinguishing
comparison and supporting/non-supporting/insufficient outcomes. A formula's
implementation check is not a new empirical discovery. Local effects, long-term
training and design decisions require separate evidence or an explicit bridge.
Question closure and its one final report require a researcher-confirmed bounded
answer; negative or insufficient results cannot be polished into support.

## Meetings And Delivery

Protect independent understanding before more implementation. A missing
explanation needs repair, not automatically a new experiment. Explain the objects,
what changes, why, the tested relation and its boundary; schematic loss curves
cannot replace derivations or local effects establish long-term design benefit.

Requested speaking preparation uses `research-communication`: one dated
`docs/meeting_brief_<topic>[_cn].md` derived from Focus and evidence, not a new
`focus_meeting_*`. Follow the user's timing, keep detail in backup, and do not
wait for a positive result. Unknown human judgment does not block a factual
brief; the brief does not activate, confirm or close a scientific question.

Ordinary result delivery links Summary first, with the decisive comparison,
useful figure/reading, boundary and next uncertainty, not a repeated full body.
A requested brief is the speaking entry instead. Unconfirmed steps are `AI 建议`.
Daily synthesis still waits for canonical results and human Focus judgment.

## Execution, Storage And Completion

Proceed with reads, in-scope edits, local tests and non-destructive checks.
Pause only for missing consequential human judgment, scope expansion,
destructive/external actions, or unapproved full/expensive remote runs. User
instructions prevail over skill preferences; never re-request approval already
given for the same scope. A drafted or confirmed design alone is not run approval.
Keep concurrent write scopes disjoint and never revert user changes.

Absent requested ongoing monitoring, verify bounded startup, first progress
and immediate failures; report verified status, job ID and evidence-based ETA,
then stop polling. Later inspect the existing job, not resubmit it.

Root `templates/` owns reusable templates. Track research text, scripts, configs
and small provenance manifests, not raw outputs, caches, checkpoints or fonts.
Curated packages may contain reading copies. Dated documents use their
own date's `figures/` with relative links and recorded origins. Independent
repositories under `Projects/` keep their own ownership; do not silently merge them.

Commit, push, publish, external sync and existing Graph edits require explicit
request. Before commit run `python tools/check_git_payload.py` and proportionate
changed-scope tests; report unavailable checks honestly. Skill edits require
structural/link checks; changed math requires source checks, not claims of rendered
verification. Complete the authorized deliverable and evidence trace. Narrow answers need no artifact.

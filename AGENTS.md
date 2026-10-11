# Research System

System owns rules and navigation; projects own research; daily folders hold
meetings and short updates. Code, raw outputs and checkpoints belong in execution.

## Authority And Communication

Use Chinese. Canonical artifacts are English with `_cn.md` companions
unless the researcher chooses otherwise. Lead with the answer and its boundary.
Use short, direct sentences, explicit actors and consistent terms; define objects
before notation. Preserve conditions and uncertainty when simplifying. Use [writing](docs/report_writing.md) and [math](docs/markdown_math.md) guidance.

Separate observations, derivations, interpretations, hypotheses and decisions.
The researcher owns questions, priorities, strongest rivals, mechanism judgment,
scientific approval, claim boundaries and state transitions. AI may inspect,
audit, suggest alternatives, formalize choices, and complete authorized work.
Missing judgment stays `Unknown`; execution, audits and other chats grant no
scientific authority.

## Context And Reasoning

Start at the named source. `PROJECTS.md` selects a project; its roadmap selects
the Focus/Anchor. Read those owners before changing a question. Check existing derivations
and evidence before declaring something missing. Distinguish an absent model,
an unshown derivation, an untested mechanism and an unsupported decision leap.
If access is incomplete, bound the search claim rather than asserting absence.

Use the smallest task owner in [docs/skills.md](docs/skills.md), then only its
applicable references. Reuse instructions; refresh decision-bearing sources.
The [method kernel](docs/methodology/research_exploration_kernel.md) guides open
research, not routine tasks or a serial skill chain. Allow reasoned conjectures
and counterexamples; apply the current stage without inventing future documents.

Check navigation with `python tools/check_current_entrypoints.py` before using
active workstream paths; this does not validate science. Before new training implementation
or code reuse inspect `docs/training_reuse_index.md` and the actual source;
state reuse, adaptation or rejection. Training and comparisons must follow
`docs/training_observability_contract.md`; do not duplicate or weaken its
telemetry, token/batch normalization, freeze or resume checks.

Before using model/SAE checkpoints, saved representations or datasets, consult
the [asset registry](assets/README.md) and check required IDs with
`tools/check_assets.py --strict`. Follow its lookup-before-pause rule; an older
access snapshot does not establish access in the current conversation.
Authorized training completion must register actually saved checkpoints through
the registry's [training and analysis lifecycle](assets/README.md#training-and-analysis-lifecycle);
keep payloads execution-side and record missing saves explicitly.

Memory is non-canonical. Use `research-memory`: one conversation log,
timestamped append-only entries with processing-agent identity. Never overwrite
other conversations or earlier entries. Explicit log resumption reads the full
log; operational briefs read their required sources instead. Verify approval
and scientific claims against their owning records, not memory.

## Record Ownership

| Record | Owns |
|---|---|
| `PROJECTS.md` / project roadmap | Project access / workstream navigation and priority |
| Focus | One stable activated question and researcher-owned next decision |
| Anchor | Sole current scientific design; never a parallel `design.md` |
| Protocol | Exact experiment contract, review, approval and amendments |
| Summary / `_cn.md` | Complete Purpose, Model, Hypothesis, Conclusion, Analysis, in that order |
| Detailed / execution record | Setup, provenance, deviations, results and execution state |
| Final report / Story / Graph / sync | Derived reading or navigation, not new authority |
| `docs/execution_envelope.md` | Profiles, images, submission and execution certificates |

Create/reset Focus only for a researcher-activated independent question with
confirmed `problem_key` and next decision. Keep it in the project's `main/focus/`;
reuse its path across dates/meetings. An authorized relocation preserves identity;
translations are companions. Keep at most three necessary experiments per question.
Preserve independent `task_state`, `question_state`, `design_state`,
`result_state`; do not mirror execution/approval into a combined status. Focus
states scientific meaning, Protocol exact execution; resolve contradictions
without silently rewriting either. Focus links to Summary; round history stays in Detailed.

Anchor keeps its eight-section contract through `problem-anchor-writer`.
A round records question/hypothesis, setup/controls, data, confirmation split,
result or `NOT RUN`, and insight/boundary/next decision. Planned rounds may stop
at `NOT RUN`; completed rounds need all six. Preserve full evidence once, not
duplicate histories. Finish factual records even when human interpretation is
unknown. Never reinterpret frozen results during refactoring.

Experiments need an uncertainty, credible rival, distinguishing comparison and
supporting/non-supporting/insufficient decision branches. A formula's
implementation check is not a new empirical discovery. Local effects, long-term
training and design decisions require separate evidence or an explicit bridge.
Question closure and its one final report require a researcher-confirmed bounded
answer; negative or insufficient results cannot be polished into support.

## Meetings And Delivery

Focus owns the question; a requested brief goes in the day's `meeting_report/`.
Link one speaking entry from the day index: question, model, result, boundary,
decision, then evidence and Q&A. Deliver self-contained Markdown; explain decisive
values, formulas and figure findings in prose. No webpage is needed for reading.

Explain objects and computation before implementation. Separate derivation,
measurement and open bridges; description, prediction, causation and utility.
A schematic is no mechanism; bounded results do not establish broader benefit.

Link Summary with decisive evidence and boundary; briefs may restate these.
Use Purpose → Model → Hypothesis → Conclusion → Analysis for new or revised
experiment summaries and multi-paragraph research analyses. Define the actual
system and measured quantities before hypotheses; state the bounded answer
before its detailed evidence. Follow the shared writing contract and template.
This changes exposition, not frozen evidence, approval or scientific state.
Unconfirmed wording stays pending; next steps are
`AI 建议`. Daily synthesis keeps its human-judgment gate; drafts grant no run authority.

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

Root `templates/` owns reusable templates. Track text, scripts, configs and small
provenance manifests, not raw outputs, caches, checkpoints or fonts. Selected
evidence exceptions require the payload manifest. Date-local figures record origins.
Independent repositories keep their ownership. For incomplete checkouts or legacy
paths use [project access](docs/project_access.md), not a duplicate editable source.

Commit, push, publish, external sync and existing Graph edits require explicit
request. Before commit run `python tools/check_git_payload.py` and relevant
changed-scope tests; report unavailable checks honestly. Skill edits require
structural/link checks; changed math requires source checks, not claims of rendered
verification. Complete deliverables and evidence traces. Narrow answers need no formal artifact.

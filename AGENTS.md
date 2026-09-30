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

Use the smallest task owner in [docs/skills.md](docs/skills.md), then only its
applicable references. Reuse unchanged instructions; refresh decision-bearing
sources before acting. The [method kernel](docs/methodology/research_exploration_kernel.md)
guides open research and mechanism work, not routine deterministic tasks or a
mandatory serial skill chain. Allow reasoned conjectures and counterexamples;
apply only the current stage, without inventing future models or documents.

Before relying on active workstream paths run `python tools/check_current_entrypoints.py`;
it checks navigation, not scientific validity. Before new training implementation
or code reuse inspect `docs/training_reuse_index.md` and the actual source;
state reuse, adaptation or rejection. Training and comparisons must follow
`docs/training_observability_contract.md`; do not duplicate or weaken its
telemetry, token/batch normalization, freeze or resume checks.

Memory is non-canonical. Use `research-memory`: one conversation log,
timestamped append-only entries with processing-agent identity. Never overwrite
other conversations or earlier entries. Explicit log resumption reads the full
log; operational briefs read their required sources instead. Verify approval
and scientific claims against their owning records, not memory.

## Record Ownership

| Record | Owns |
|---|---|
| `PROJECTS.md` | Navigation, workstreams, priorities and project decisions |
| Focus | One stable activated question and researcher-owned next decision |
| Anchor | Sole current scientific design; never a parallel `design.md` |
| Protocol | Exact experiment contract, review, approval and amendments |
| Summary / `_cn.md` | Complete Purpose, Hypothesis, Analysis method, Conclusion |
| Detailed / execution record | Setup, provenance, deviations, results and execution state |
| Final report / Story / Graph / sync | Derived reading or navigation, not new authority |
| `docs/execution_envelope.md` | Profiles, images, submission and execution certificates |

Create/reset Focus only for a researcher-activated independent question with
confirmed `problem_key` and next decision. Reuse its path across dates/meetings;
translations are companions. Keep at most three necessary experiments per question.
Preserve independent `task_state`, `question_state`, `design_state`,
`result_state`; do not mirror execution/approval into a combined status. Focus
states scientific meaning, Protocol exact execution; resolve contradictions
without silently rewriting either. Focus links to Summary; round history stays in Detailed.

Anchor keeps its eight-section contract through `problem-anchor-writer`.
A round records question/hypothesis, setup/controls, data, confirmation split,
result or `NOT RUN`, and insight/boundary/next decision. Planned rounds may stop
at `NOT RUN`; completed rounds need all six. Preserve full evidence once, not
duplicate histories. Finish authorized factual records even when human
interpretation is unknown. Never reinterpret frozen results during refactoring.

Experiments need an uncertainty, credible rival, distinguishing comparison and
supporting/non-supporting/insufficient decision branches. A formula's
implementation check is not a new empirical discovery. Local effects, long-term
training and design decisions require separate evidence or an explicit bridge.
Question closure and its one final report require a researcher-confirmed bounded
answer; negative or insufficient results cannot be polished into support.

## Meetings And Delivery

Focus owns the question; a requested brief goes in the day's `meeting_report/`,
never a meeting Focus. The day index links one speaking entry. Follow requested
order: question/update, model, result/boundary/decision; then evidence and Q&A.

Explain before implementation. Define objects/computation; separate derivation,
measurement and open bridges. A schematic is no mechanism; bounded results do not
establish broader design benefit. Distinguish description, prediction, causation
and utility. Check prior work before absence claims.

Link Summary with decisive evidence and boundary; briefs may restate these.
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

Root `templates/` owns reusable templates. Track research text, scripts, configs
and small provenance manifests, not raw outputs, caches, checkpoints or fonts.
Requested curated packages may contain reading copies. Dated documents use their
own date's `figures/` with relative links and recorded origins. Independent
repositories under `Projects/` keep their own ownership; do not silently merge them.

Commit, push, publish, external sync and existing Graph edits require explicit
request. Before commit run `python tools/check_git_payload.py` and proportionate
changed-scope tests; report unavailable checks honestly. Skill edits require
structural/link checks; changed math requires source checks, not claims of rendered
verification. Complete the authorized deliverable and evidence trace; a first
draft is not completion. Narrow answers need no formal artifact.

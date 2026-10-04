# Repository Skills

Canonical skills live only in `.agents/skills/<name>/`. Keep one installed root
catalog, not personal copies. Select by task, then read that entry and applicable
references; never treat the following ownership table as a serial workflow.

## Task Ownership

| Requested outcome | Skill |
|---|---|
| Purpose, hypothesis, causal/mathematical chain or proxy audit | `research-reasoning-auditor` |
| Question discovery/refinement, Focus judgment, falsifier, result/failure | `research-progress-core` |
| Formal Anchor and scientific design | `problem-anchor-writer` |
| Protocol, Summary, Detailed and evidence lineage | `experiment-card-writer` |
| Settled-question final synthesis | `research-final-report` |
| Plain-language explanation of a named document | `research-document-explainer` |
| Explicit meeting, Story or curated handoff/sync | `research-communication` |
| Repository-local conversation context | `research-memory` |
| Advisor readiness or one next question | `research-sync-gate` |
| Placement, archival or explicit publication | `research-mainline` |
| Remote jobs, logs and artifact transport | `remote-experiment-workflow` |
| Unsettled theory, method or literature critique | `scholar-mode` |
| Explicit graph maintenance | `research-graph-sop` |
| Explicit local Sidecar display/API operations | `sidecar-thinking` |

Implicit selection does not authorize writes, runs, publication or state changes.
Add an owner only for a necessary subtask. A brief audit may finish in chat;
a requested document follows its owning contract. Existing decisions and scope
carry across models; do not demand repeated approvals or duplicate checks.

## Method Integration, Not Another Skill

The [kernel](methodology/research_exploration_kernel.md) integrates the pinned
research-exploration method. The [coverage mapping](methodology/research_exploration_mapping.md)
records each obligation, local owner, regression case and intentional exclusion.
This preserves methodology without importing a competing root skill, `design.md`,
automatic viewer or second question tree. Attribution is in
[THIRD_PARTY_NOTICES](../THIRD_PARTY_NOTICES.md).

Use only the relevant stage:
- New question: importance and structure before choosing a mechanism.
- Mechanism diagnosis: inspect existing work, then distinguish derivation,
  empirical, presentation and decision-bridge gaps.
- Active design: exact variables/objective/constraints, permitted information,
  prior-art decision when material, and stage-local Goal/How/Why.
- Experiment/results: identifiable comparison, micro-test, frozen confirmation,
  stage evidence, failure localization and bounded upward update.
- Communication: explain the mechanism to a first reader without turning a
  missing slide into missing science or a local effect into a design verdict.

This is a reading guide, not required extra calls or reply headings. Deep rules
are read when the selected task needs them; quick questions do not load the
mapping, fixture suite or all downstream owners.

## Artifact And Authority Boundaries

Focus owns current human judgment; Anchor the sole scientific design; Protocol
the precise contract/approval; Summary the first complete result; Detailed the
preserved evidence/round ledger. Stories, final reports, graphs and memory cannot
replace those sources. Keep complete history once and derive summaries from it.

Protocol drafting remains one `DRAFT_NOT_EXECUTABLE` file with A-G critical review;
promotion does not silently authorize execution. Results may finish factual work
while human interpretation stays unknown. Learned designs require distinct data,
task, objective, architecture, selection and confirmation boundaries.

Reports share [writing and medium rules](report_writing.md). Local HTML is a derived
view when it improves reading, not another evidence owner. Project Focuses and
formal records stay outside daily folders; [access](project_access.md) covers
incomplete checkouts and legacy paths.

Communication selects the requested meeting, Story or handoff mode. Handoff,
external copying, commit/push, graph changes and publication remain explicitly
scoped. Memory resumption is not scientific authorization; operational briefs and
explicit full-log resumption retain their different reading contracts.

Repositories under `Projects/` remain independently owned. Project-specific skills
are not root duplicates to merge. SCO platform semantics stay with the project's
`sco-control`; remote research execution uses the root envelope and remote owner.

## Validation And Load Budget

After skill edits run `python tools/check_skills.py`. Use the installed
skill-creator `quick_validate.py` when available; report its absence rather than
claiming execution. Run `python -m unittest discover -s tools/tests` for local
regression tests and `python tools/check_markdown_math.py <changed-math-files>`
for source containers. These checks establish structure/code behavior, not
scientific correctness, target rendering or live model trigger quality. Behavioral
checks use cross-domain [scenarios](methodology/research_exploration_regression_cases.md)
and actual answers; distinguish self-review from independent evaluation.

Preserve lean entrypoints. Compare like-for-like read paths, including required
references, rather than claiming all tasks save the entrypoint percentage.
Web project instructions must not exceed the recorded pre-refactor character or
UTF-8 byte budget. Optional references are not free when actually loaded.
Verify live skill discovery in a fresh client task separately; this refactor does
not silently change a running client's context or model settings.

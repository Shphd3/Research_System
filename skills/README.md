# Skills

This folder is the canonical repo-tracked source for research-system skills.

Installed local copies live in:

```text
C:\Users\250010109\.codex\skills\
```

Edit `skills/<skill>/SKILL.md` first, then sync the installed copy when needed.

## Active Skills

| Skill | Use |
|---|---|
| `research-progress-core` | Governing research paradigm: physical prior, falsifiable hypothesis, operational definition, minimal test, metric plus visual evidence, failure analysis, and refined hypothesis. |
| `research-mainline` | Maintain compact project anchors, result records, and project organization; graph, root sync, external collaborator sync, handoff, commit, and push actions require explicit user request. |
| `scholar-mode` | Clarify research intuitions, theory framing, methodology critique, and literature fit. |
| `problem-anchor-writer` | Write anchor design documents with one decision question, physical priors, math, computational realization, falsifiable tests, evidence, boundary, and next decision. |
| `experiment-card-writer` | Write `protocol.md`, `summary.md`, and `detailed.md` from anchors. |
| `meeting-brief-writer` | Write or revise strict advisor-facing `meeting_brief.md` files. First read and strictly apply `templates/meeting/meeting_brief_template.md`. |
| `handoff-report-writer` | Package existing anchor, protocol, summary, detailed, figures, tables, and finalized meeting material for collaborator/web/external handoff. |
| `remote-experiment-workflow` | Manage local/remote/container/SCO/ACP experiment workflow, preflight, submission, monitoring, and artifact maps. |
| `research-graph-sop` | Maintain a thin graph of questions, claims, evidence, methods, outputs, and next tasks. |
| `sidecar-thinking` | Optional bridge to the local Sidecar app for review sessions and graph inspection. |

## Skill Responsibility Boundary

Do not treat every skill as a separate workflow. Use this responsibility map:

| Layer | Skill | Owns | Does not own |
|---|---|---|---|
| Research paradigm | `research-progress-core` | What counts as research progress: physical prior, falsifiable hypothesis, operational definition, minimal test, metric plus visual evidence, failure analysis, and refined hypothesis. | Project-specific paths, platform commands, or tool adapters. |
| Remote workflow | `remote-experiment-workflow` | Local/remote/cluster boundary, SSH/CCI preflight, ACP/SCO submission, monitoring, artifact map, curated handoff. | Defining the research problem. |
| Anchor reasoning | `problem-anchor-writer` | Current-state design document: phenomenon, one decision question, physical priors, falsifiable hypotheses, one core mathematical model, computational realization, minimal tests with operational definitions, stage-local evidence, failure meaning, evidence, claim boundary, one next decision. | Raw logs, command construction, protocol details, literature review, long reports. |
| Experiment protocol and results | `experiment-card-writer` | Approved `protocol.md`, result `summary.md`, and full `detailed.md` from an anchor. | Separate purpose cards or separate implementation-plan files. |
| Meeting brief | `meeting-brief-writer` | Strict advisor-facing `meeting_brief.md`: current question, mechanism model, evidence, boundary, and next action. Must follow `templates/meeting/meeting_brief_template.md` mode one or mode two exactly. | Packaging, external sync, creating new claims, replacing anchors or result records. |
| External handoff | `handoff-report-writer` | Explicitly requested packaging of existing artifacts or curated collaborator repo sync package after anchor and result records are updated. | Writing the meeting brief itself; creating new research claims; replacing anchor, `summary.md`, or `detailed.md`; automatic handoff creation; syncing code or raw outputs by default. |
| Mainline | `research-mainline` | Project anchors, roadmap, result records, and explicit root/project/external sync or graph actions. | Raw logs, remote job operation, automatic graph/root-sync/external-sync/push. |
| Graph | `research-graph-sop` | Thin `graph.yaml` navigation map. | Replacing Markdown reasoning files. |

## Artifact Alignment Contract

Keep the artifact chain narrow. Each file owns one layer of judgment or
evidence; it must not silently absorb another file's job.

| Artifact | Owns | Must not do |
|---|---|---|
| `00_handwrite_anchor.md` | rough Thinking Card and exposed user judgment | require or become a full 0-8 anchor before audit |
| anchor | current minimal adjudicable design | become a runbook, full result report, or broad ablation list |
| `protocol.md` | how one anchor clause will be tested | change the question post hoc or add unrelated sweeps |
| `summary.md` | first reading path: conclusion, primary metric, central figures | contain the full evidence ledger |
| `detailed.md` | complete evidence ledger, failure decomposition, artifact map | create a second conclusion stronger than the anchor allows |
| `figures/` or viewer | visual evidence for the current judgment | include decorative plots or disguise debug plots as decision evidence |
| anchor update | supported / weakened / insufficient evidence, boundary, next decision | paste a result report into the anchor |

Current consolidation decision:

```text
Remote workflow skills are merged. Purpose cards and hypotheses are unified
into anchors. Post-result closure happens in the updated anchor and required
`summary.md` / `detailed.md`; handoff reports are optional external packages.
Research progress is governed by research-progress-core; the other skills are
artifact writers or local adapters.
```

## Research Paradigm

Canonical research artifacts are written in English by default. Chinese
companion versions are allowed when useful; name them with `_cn` before the
extension, for example `<anchor_id>_cn.md`, `summary_cn.md`,
`protocol_cn.md`, `summary_cn.md`, or `detailed_cn.md`. The English file is the source of
truth unless the user explicitly says otherwise. Conversation with the user may
remain Chinese-first for explanation.

Default short research loop:

```text
physical prior -> falsifiable hypothesis -> operational definition -> minimal test
-> metric + visual evidence -> failure analysis -> refined hypothesis
```

Default project artifact loop:

```text
anchor -> protocol.md -> summary.md -> detailed.md -> anchor update
```

Root sync, external collaborator repo sync, handoff reports, graph edits,
commits, and pushes are explicit follow-up actions only.

Terminology is part of the artifact contract. Any anchor, protocol, summary,
detailed record, closure report, meeting brief, or viewer that uses non-obvious
terms, English jargon, abbreviations, metric names, condition labels, model
variants, or project shorthand must define them before using them as evidence.
Use `Terminology / Definitions` in English canonical artifacts and `术语解释`
in Chinese companions or meeting briefs.

Minimum definition:

```text
term / abbreviation
plain meaning
concrete object or computation
unit / formula, if metric
why it matters for the current decision
what it cannot prove
```

Minimal advisor-spec adapter:

```text
docs/design.md                  -> anchor
docs/experiment_design.md       -> protocol.md
docs/visualization_results.md   -> summary.md + detailed.md + figures/viewer
docs/final_report.md            -> stable-closure synthesis after the anchor
                                   and result records are current
```

Do not create a parallel `docs/` tree for normal project work unless the user
asks for that exported layout.

`protocol.md` is required before implementation or running. It is the approved
experiment design and replaces the old protocol/execution-plan split.

`summary.md` is required. It is the first post-result reading path and must
state the purpose, exact setup, primary metric, conclusion, key evidence, claim
boundary, and next decision. It must explain central figures using the
visualization-results standard.

It should start with the reader-facing result shape: what we established, what
the experiment shows through the primary metric, and what we do next. Condition
labels, metric names, and visible shorthand must be defined in
`Terminology / Definitions` before they are used as evidence.

`detailed.md` is required. It is the complete experiment record. It must
preserve the full setup, conditions, seeds, commands, job ids, curated tables,
important figures, visualization results, artifact map, failed or partial runs
when relevant, and the evidence walkthrough.

After results exist, the original anchor must be backfilled with:

```text
Result
Conclusion
Next Step
Result Documents
```

The anchor should link the experiment `protocol.md`, `summary.md`,
`detailed.md`, and key figures. If the project uses
root anchor copies, update the root copy only when the user explicitly requests
root sync, then verify that it matches the source anchor.

Anchors belong in the project mainline's `problem_anchors/` directory;
protocols and result evidence belong in `experiments/`.

Default one-to-one mapping:

```text
Projects/<project>/<mainline>/problem_anchors/<anchor_id>.md
Projects/<project>/main/experiments/A<anchor_id>/<experiment_id>/protocol.md
```

An experiment should correspond to one primary anchor. Multi-stage experiment
lines may have stage-level sub-decisions, but they should still link back to
the primary anchor.

`detailed.md` must begin with:

```markdown
## 0. Quick Recap

目的：

假设：

实验思路：

结论：

证据：
```

The rest of `detailed.md` expands the same structure. It must include the
anchor link, result document links, the decision point, setup, primary metric,
key figures, evidence walkthrough, full experiment record, interpretation,
claim boundary, next decision, and artifact map.
Do not use opaque English phrases as story labels; write one rigorous and clear
sentence describing the experiment's research story.

Keep active `experiments/` focused on the proposition currently being verified.
Older, weakly related, superseded, or supporting-only experiments should be
collected under `experiments/archive/` with a short index. Archive evidence
rather than deleting it unless deletion is explicitly requested.

Anchors are decision cards, not reports. They must include:

- one decision question;
- physical priors;
- falsifiable hypotheses;
- one minimal mathematical model;
- computational realization / implementation contract;
- minimal tests with primary metrics;
- operational definitions, stage-local evidence, and failure meaning for each
  minimal falsification test;
- supported / weakened / insufficient-evidence outcomes;
- current evidence;
- claim boundary and one next decision.

Each anchor has two reading layers. `Thinking Card` is the short human-facing
mechanism judgment card: phenomenon, mechanism guess, key variables, causal
relation, observable metric, alternative explanation, and decision rule. The
remaining sections are the auditable design layer for AI review, replay,
protocol alignment, and boundary checks.
`Computational Realization` prevents theory/code drift by naming the
implemented inputs, computed variables, algorithm stages, stage-local evidence,
and expected artifacts.

For nontrivial research work, the artifact loop is incomplete unless it also
records stage-level evidence, the failure interpretation for each important
stage, whether a result falsifies the physical prior or only one
operationalization, and the next uncertainty to isolate.

## Project Support Surfaces

- `daily_research_reports/MMDD/<topic>/`: default location for an explicitly
  requested handoff report and the copied most important anchor.
- `Projects/<project>/sync/`: explicitly requested project-local
  collaborator-facing sync of shareable results, boundaries, and handoffs.
- `Projects/<project>/<worker>/sync/MMDD_topic/`: branch-local meeting or
  collaborator sync folder; use only when project sync is explicitly requested.
  Handoff packages should copy existing anchor/protocol/result records, plus
  referenced figures/tables, and add only a short README or index for
  navigation.
- `Projects/<project>/<worker>/docs/`: named material documents that help write
  anchors, result records, and handoff reports.
- `graph.yaml`: default thin research graph. Use `research-graph-sop`; keep
  graph structure lightweight and store reasoning in Markdown anchors and notes.
- `sync/<sync_id>/anchors/<category>/<anchor_id>.md`: categorized root copy of
  an active anchor for web-side and cross-project reading.
- `<external_collaborator_repo>/<agreed_research_sync_path>/MMDD_topic/`:
  explicitly requested sync package for a senior student's or collaborator's
  GitHub repo. Include only a minimal curated package: copied anchor,
  `protocol.md`, `summary.md`, `detailed.md`, and figures/tables only when
  referenced by those synced documents. Do not include raw logs, checkpoints,
  datasets, full result dirs, private notes, unrelated anchors, code changes,
  or uncurated configs unless explicitly requested.

## Reporting Figure Rule

Experiment result reports and collaborator sync must include the most important
report-ready figure(s) when figures exist and are central evidence. Copy them
into the local `figures/` folder and embed them in `summary.md` and
`detailed.md`. Each central figure needs purpose, setup, how-to-read, observed
result, take-home, and remaining uncertainty. Do not make the reader infer the
result from a dry metric list.

Before a new central plot or viewer is delivered, preserve a plot contract:
question answered, metric definition and unit, data source, aggregation level,
axis and legend meaning, allowed conclusion, and limitation. Rendered viewers
must pass a bounded audit for readable labels, visible metric definitions,
visible key numbers, and no source-code-only interpretation.

## Formula Rule

When a skill writes Markdown research documents:

- inline formulas must use `$...$`;
- display formulas must use `$$...$$`;
- raw LaTeX formulas should not appear in prose without math delimiters.

## Cleanup Rule

Do not add new global skills unless the task is repeated often and cannot be
handled by one of the active global skills.

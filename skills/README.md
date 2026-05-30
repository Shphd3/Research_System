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
| `research-progress-core` | Governing research paradigm: hypothesis, operational definition, minimal test, metric plus visual evidence, failure analysis, and refined hypothesis. |
| `research-mainline` | Maintain compact project graph, anchors, result records, root sync anchors, and project organization. |
| `scholar-mode` | Clarify research intuitions, theory framing, methodology critique, and literature fit. |
| `problem-anchor-writer` | Write unified anchor/purpose-card documents from boundary and physical priors to math, implementation, evidence, and next decision. |
| `experiment-card-writer` | Write operational experiment execution plans from anchors. |
| `handoff-report-writer` | Write optional meeting/collaborator/web handoff reports after anchor, summary, and detailed records are updated. |
| `remote-experiment-workflow` | Manage local/remote/container/SCO/ACP experiment workflow, preflight, submission, monitoring, and artifact maps. |
| `research-graph-sop` | Maintain a thin graph of questions, claims, evidence, methods, outputs, and next tasks. |
| `sidecar-thinking` | Optional bridge to the local Sidecar app for review sessions and graph inspection. |

## Skill Responsibility Boundary

Do not treat every skill as a separate workflow. Use this responsibility map:

| Layer | Skill | Owns | Does not own |
|---|---|---|---|
| Research paradigm | `research-progress-core` | What counts as research progress: hypothesis, operational definition, minimal test, metric plus visual evidence, failure analysis, and refined hypothesis. | Project-specific paths, platform commands, or tool adapters. |
| Remote workflow | `remote-experiment-workflow` | Local/remote/cluster boundary, SSH/CCI preflight, ACP/SCO submission, monitoring, artifact map, curated handoff. | Defining the research problem. |
| Anchor reasoning | `problem-anchor-writer` | Purpose, hypothesis, physical priors, math, computational realization, minimal test, evidence update, claim boundary. | Raw logs or command construction. |
| Execution plan | `experiment-card-writer` | Concrete run plan from an anchor. | Separate purpose cards. |
| External handoff | `handoff-report-writer` | Optional self-contained report for meeting, collaborator, or web-side handoff after anchor and result records are updated. | Replacing anchor, `summary.md`, or `detailed.md`. |
| Mainline | `research-mainline` | Project graph, anchors, roadmap, sync anchors. | Raw logs or remote job operation. |
| Graph | `research-graph-sop` | Thin `graph.yaml` navigation map. | Replacing Markdown reasoning files. |

Current consolidation decision:

```text
Remote workflow skills are merged. Purpose cards and hypotheses are unified
into anchors. Post-result closure happens in the updated anchor and required
`summary.md` / `detailed.md`; handoff reports are optional external packages.
Research progress is governed by research-progress-core; the other skills are
artifact writers or local adapters.
```

## Research Paradigm

Default short research loop:

```text
hypothesis -> operational definition -> minimal test
-> metric + visual evidence -> failure analysis -> refined hypothesis
```

Default project artifact loop:

```text
anchor -> execution plan -> summary.md -> detailed.md -> anchor update -> root anchor copy -> optional handoff report
```

`summary.md` is required. It is the first post-result reading path and must
state the purpose, hypothesis or question, conclusion, key evidence, claim
boundary, and next decision.

`detailed.md` is required. It is the complete experiment record. It must preserve the full
setup, conditions, seeds, commands, job ids, curated tables, important figures,
artifact map, failed or partial runs when relevant, and the evidence walkthrough.

After results exist, the original anchor must be backfilled with:

```text
Result
Conclusion
Next Step
Result Documents
```

The anchor should link the experiment `summary.md`, `detailed.md`, key figures,
and optional handoff report when needed. If the project uses root anchor copies,
update the root copy in the same turn and verify that it matches the source
anchor.

Anchors belong in the project mainline's `problem_anchors/` directory;
execution plans and result evidence belong in `experiments/`.

Default one-to-one mapping:

```text
Projects/<project>/<mainline>/problem_anchors/<anchor_id>.md
Projects/<project>/main/experiments/<experiment_id>/execution_plan.md
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

Anchors must include:

- problem definition / level;
- purpose;
- hypothesis and rival explanations;
- physical priors;
- mathematical modeling;
- computational realization;
- minimal experiment design;
- expected outcomes and hypothesis-update logic;
- claim boundary.

For nontrivial research work, the artifact loop is incomplete unless it also
records stage-level evidence, the failure interpretation for each important
stage, whether a result falsifies the physical prior or only one
operationalization, and the next uncertainty to isolate.

## Project Support Surfaces

- `Projects/<project>/sync/`: daily collaborator-facing sync of shareable
  results, boundaries, and handoffs.
- `Projects/<project>/<worker>/sync/MMDD_topic/`: branch-local meeting or
  collaborator sync folder; the reporting document lives inside this folder.
  Handoff reports should use a compact self-contained structure and must include
  a compact artifact / repro map: code, runner, config, data or manifest, result
  folder, figure folder, key files, checkpoints/logs, and repro command.
- `Projects/<project>/<worker>/docs/`: named material documents that help write
  anchors, result records, and handoff reports.
- `graph.yaml`: default thin research graph. Use `research-graph-sop`; keep
  graph structure lightweight and store reasoning in Markdown anchors and notes.
- `sync/<sync_id>/anchors/<category>/<anchor_id>.md`: categorized root copy of
  an active anchor for web-side and cross-project reading.

## Reporting Figure Rule

Experiment result reports and collaborator sync must include the most important
report-ready figure(s) when figures exist and are central evidence. Copy them
into the local `figures/` folder and embed them in `summary.md`, `detailed.md`,
and the optional handoff `report.md` when applicable. Each figure needs a nearby sentence
explaining what it supports. Do not make the reader infer the result from a dry
metric list.

## Formula Rule

When a skill writes Markdown research documents:

- inline formulas must use `$...$`;
- display formulas must use `$$...$$`;
- raw LaTeX formulas should not appear in prose without math delimiters.

## Cleanup Rule

Do not add new global skills unless the task is repeated often and cannot be
handled by one of the active global skills.

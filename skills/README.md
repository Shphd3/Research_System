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
| `research-mainline` | Maintain compact project mainline, hypothesis status, and result routing. |
| `scholar-mode` | Clarify research intuitions, theory framing, methodology critique, and literature fit. |
| `experiment-card-writer` | Write hypothesis-first purpose cards and experiment execution plans. |
| `hypothesis-closure` | Close a hypothesis from its purpose card and evidence. |
| `experiment-acp-runner` | Turn execution plans into ACP/SCO dry runs, submissions, monitoring records, and summaries. |
| `prism-report` | Build group-meeting-ready PRISM reports. |
| `paper-reading-card` | Turn papers or blogs into compact reading cards. |
| `research-graph-sop` | Maintain a thin graph of questions, claims, evidence, methods, outputs, and next tasks. |
| `writing-explanatory-reports` | Write detailed experiment reports and result analyses under `experiments/`. |
| `sidecar-thinking` | Optional bridge to the local Sidecar app for review sessions and graph inspection. |
| `remote-sco-collaboration` | Connect to remote H100 containers, verify session state, and bridge local research work to SCO/ACP execution. |

## Research Paradigm

Default project loop:

```text
hypothesis purpose card -> execution plan -> experiment result summary -> hypothesis closure -> mainline/status update
```

After results exist, the original purpose card must be backfilled with:

```text
Result
Conclusion
Next Step
Result Documents
```

The purpose card should link the experiment `summary.md`, `detailed.md`, key
figures when needed, and `hypothesis_closure.md`.

After a hypothesis closure is finished, create a daily reporting card under:

```text
daily_research_reports/MMDD/01_reporting/<hypothesis_id>_reporting_card.md
```

The card should leave the oral-report section blank for the user to write before
meeting, then include or link the closure snapshot for fast daily access.

The purpose card belongs in `hypotheses/`; the execution plan and result
evidence belong in `experiments/`.

Default one-to-one mapping:

```text
Projects/<project>/main/hypotheses/<hypothesis_id>/purpose_card.md
Projects/<project>/main/experiments/<experiment_id>/execution_plan.md
```

An experiment should correspond to one primary hypothesis. Multi-stage
experiment lines may have stage-level sub-decisions, but they should still link
back to the primary hypothesis purpose card.

Keep active `experiments/` focused on the proposition currently being verified.
Older, weakly related, superseded, or supporting-only experiments should be
collected under `experiments/archive/` with a short index. Archive evidence
rather than deleting it unless deletion is explicitly requested.

Purpose cards must include:

- problem level;
- purpose;
- hypothesis and rival explanations;
- mathematical modeling;
- experiment design;
- expected outcomes and hypothesis-update logic;
- claim boundary.

## Project Support Surfaces

- `Projects/<project>/sync/`: daily collaborator-facing sync of shareable
  results, boundaries, and handoffs.
- `Projects/<project>/<worker>/sync/MMDD_topic/`: branch-local meeting or
  collaborator sync folder; the reporting document lives inside this folder.
  Experiment sync should use the closure-like structure `目的 / 假设 / 数学建模 /
  实验设置 / 结论 / 证据 / 结论边界 / 下一步决策 / 结果文档`, and must include a compact
  artifact / repro map: code, runner, config, data or manifest, result folder,
  figure folder, key files, checkpoints/logs, and repro command.
- `Projects/<project>/<worker>/docs/`: named material documents that help write
  hypothesis purpose cards and closures.
- `graph.yaml`: optional thin research graph. Use `research-graph-sop`; keep
  graph structure lightweight and store reasoning in Markdown notes.
- `results/R001_short_name/`: curated stage-level research outcomes that are
  stable enough to reuse across mainlines, closures, meetings, or reports.

## Reporting Figure Rule

Experiment result reports and collaborator sync should include the most
important report-ready figure(s) when figures are central evidence. Each figure
needs a nearby sentence explaining what it supports. Do not make the reader infer
the result from a dry metric list.

## Formula Rule

When a skill writes Markdown research documents:

- inline formulas must use `$...$`;
- display formulas must use `$$...$$`;
- raw LaTeX formulas should not appear in prose without math delimiters.

## Cleanup Rule

Do not add new global skills unless the task is repeated often and cannot be
handled by one of the active global skills.

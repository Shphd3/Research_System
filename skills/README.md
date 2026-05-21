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

## Research Paradigm

Default project loop:

```text
hypothesis purpose card -> execution plan -> experiment result summary -> hypothesis closure -> mainline/status update
```

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
- `Projects/<project>/<worker>/docs/`: named material documents that help write
  hypothesis purpose cards and closures.
- `graph.yaml`: optional thin research graph. Use `research-graph-sop`; keep
  graph structure lightweight and store reasoning in Markdown notes.
- `results/R001_short_name/`: curated stage-level research outcomes that are
  stable enough to reuse across mainlines, closures, meetings, or reports.

## Formula Rule

When a skill writes Markdown research documents:

- inline formulas must use `$...$`;
- display formulas must use `$$...$$`;
- raw LaTeX formulas should not appear in prose without math delimiters.

## Cleanup Rule

Do not add new global skills unless the task is repeated often and cannot be
handled by one of the active global skills.

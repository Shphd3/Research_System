---
name: research-mainline
description: Use when organizing or updating a research project's graph, anchors/purpose cards, experiment folders, result summaries, sync closures, root sync anchors, and project status.
metadata:
  short-description: Maintain compact research mainline
---

# Research Mainline

Use this skill to keep a research project easy to inspect and easy to act on.
The goal is not to store every note. The goal is to make the current question,
anchors, evidence, claim boundary, and next decision obvious.

## Required Project Structure

```text
Projects/<project>/
  graph.yaml
  main/
    README.md
    roadmap.md
    problem_anchors/
      README.md
      <anchor_id>.md
    experiments/
      README.md
      <experiment_id>/
        README.md
        execution_plan.md
        summary.md
        detailed.md
        figures/
```

For `kv_cache`, the specialization mainline uses:

```text
Projects/kv_cache/research/graph.yaml
Projects/kv_cache/main_specialization/
Projects/kv_cache/main_specialization/problem_anchors/
```

Optional project support surfaces:

```text
Projects/<project>/sync/
Projects/<project>/<worker>/sync/MMDD_topic/
Projects/<project>/<worker>/docs/
sync/R001_short_name/
```

## File Roles

### `graph.yaml`

The default navigation layer for the project and the Sidecar entry point. It
should answer in under a minute:

- what is being investigated;
- which anchors, claims, methods, evidence, and tasks matter now;
- what is active, blocked, draft, or done;
- which Markdown files hold the reasoning.

Use `research-graph-sop` for changes to `graph.yaml`. The graph should stay
thin; Markdown files hold the thick reasoning.

### `main/problem_anchors/`

This is the living reasoning layer and the unified purpose-card layer. Each
anchor should define:

- problem definition;
- physical priors;
- mathematical modeling;
- computational realization;
- minimal falsifiable test;
- current evidence;
- claim boundary and next decision.

Update an anchor when experiments change the physical prior, mathematical
object, computational test, interpretation, claim boundary, or next decision.

Do not create a separate `hypotheses/<id>/purpose_card.md` for new work. The
anchor owns the purpose, hypothesis, rival explanations, math, minimal test,
evidence update, and next decision.

### `main/roadmap.md`

Compact route and gate logic. Use it for the current research route, stop
rules, and the order in which anchors or experiments should be resolved.

### `experiments/`

This is the execution and evidence layer. Each experiment should map to one
primary anchor.

```text
experiments/<experiment_id>/
  README.md
  execution_plan.md
  summary.md
  detailed.md
  figures/
```

`execution_plan.md` contains concrete configs, commands, metrics, artifacts,
pass/fail criteria, and failure modes.

`summary.md` is the closure-level local result synthesis. It inherits the role
of the old hypothesis closure inside the experiment folder. It must link the
anchor and state observation, interpretation, limitation, claim update, key
figures, and next decision. It is the first reading path after a result exists.

`detailed.md` is the complete experiment record. It stores the full setup, data
construction, model/training/eval details, conditions, seeds, command records,
job ids, longer tables, key figures, failed or partial runs, artifact maps, and
supporting analysis. It must start with:

```markdown
## 0. Quick Recap

目的：

假设：

实验思路：

结论：

证据：
```

The rest of `detailed.md` should expand the same structure with anchor links,
the decision point, setup, primary metric, key figures, evidence walkthrough,
full experiment record, interpretation, claim boundary, next decision, and
artifact map. The artifact map must include code workspace, runner or launch
script, config, key code files, data or manifest, result directory, figure
directory, key tables, logs/checkpoints, job id, and reproduction command when
available. Do not let `detailed.md` become a raw appendix without a story.

Important figures are mandatory when they exist. Copy report-ready figures into
the experiment folder's local `figures/` directory, embed them in both
`summary.md` and `detailed.md`, and write what each figure proves or fails to
prove. Put curated tables in `tables/`.

After `detailed.md` is written, the active anchor must link back to it from the
current evidence section.

Keep the first reading path in `experiments/` narrow. Active experiments should
be the ones most relevant to the proposition currently being verified. Move
older, weakly related, superseded, or purely supporting experiments into
`experiments/archive/` and maintain an `archive/README.md` with:

- archived folder;
- why it was archived;
- when it should be consulted again.

Do not delete evidence just because it is no longer active. Archive it unless
the user explicitly asks to delete it.

### `sync/` And Sync Closures

`Projects/<project>/<worker>/sync/MMDD_topic/` is the default branch-local
collaborator or meeting sync surface. Use exactly one primary sync folder per
date for each worker. If the day contains several hypotheses, stages,
diagnostics, or experiment versions, put them as subfolders under that date's
primary sync instead of creating several same-date top-level sync entries.

`Projects/<project>/sync/` is for shared project-level sync after the result is
safe to share as project consensus.

Update sync once per active working day with the smallest shareable outcome:

- what changed;
- why it matters;
- what cannot be claimed;
- what handoff or question remains;
- where the collaborator can find code, config, data/manifest, result folder,
  figure folder, key artifacts, checkpoints, logs, and repro command.

For a given date, maintain one consolidated daily sync as the first reading
path. Put supporting diagnostics, extra figures, version reports, or detailed
artifact maps in subfolders, but keep the daily conclusion, evidence, boundary,
and next decision in one main document.

The top of the main `report.md` should be closure-like rather than purely
procedural: start with a compact researcher-facing summary that the user can
read aloud or edit as their own conclusion. This first section should anchor:
what changed today, the strongest hypothesis update, the key evidence, the
claim boundary, and the next decision. Put detailed experiment sections,
tables, figure walkthroughs, and artifact maps after this front summary.

This front summary is required and must be section `## 0. Closure-Style Daily
Summary`. Treat it like the user-fill judgment card in a hypothesis closure:
leave clearly marked blank slots by default so the user can write the final
meeting-facing judgment. Do not fill it with Codex's own final wording unless
the user explicitly provides or confirms that wording. The default slots are:
purpose, hypothesis, conclusion, evidence, what cannot be claimed, and next
decision. Do not bury the user's own summary below implementation details.

Project-local sync must only reference paths visible inside the project
repository. Do not cite root-level `Research_System` materials such as
`daily_research_reports/`; if such material informed the sync, integrate the
necessary content into the sync itself.

For experiment sync, write an anchor-based sync closure and include a compact
`Artifact / Repro Map`. The sync should let a collaborator understand the
result and know where to continue without asking where the code, data, figures,
or outputs live.

Experiment sync should use the same self-contained research-judgment structure
as closures after the front summary:

```markdown
## 0. Closure-Style Daily Summary（用户填写）
## 1. 目的
## 2. 假设
## 3. 数学建模
## 4. 实验设置
## 5. 结论
## 6. 证据
## 7. 结论边界
## 8. 下一步决策
## 9. 结果文档
```

When figures are central evidence, copy the most important report-ready figures
into the sync folder's local `figures/` directory and embed them with one
sentence explaining what each figure supports. Do not leave the sync as dry text
when visual evidence is what makes the claim understandable.

Do not put raw logs, full tables, or unfiltered experiment outputs here.

### `<worker>/docs/`

Use `Projects/<project>/<worker>/docs/` for named material documents that help
write future purpose cards and closures: concept notes, mathematical modeling,
metric guides, figure guides, meeting-derived definitions, and reusable
explanations.

### `graph.yaml`

Use `research-graph-sop` when a project needs a lightweight map of questions,
claims, evidence, methods, sources, outputs, and next tasks. The graph is a
navigation layer; Markdown files remain the reasoning layer.

### root `sync/`

Use root-level `sync/` for cross-project anchor summaries, categorized anchor
copies, and curated stage-level outcomes that are stable enough to cite without
entering project repositories.

Active anchors must be mirrored into root sync:

```text
sync/<sync_id>/anchors/<category>/<anchor_id>.md
```

The project-local anchor is the source of truth. When it changes, copy it to
the root sync category in the same turn and verify that the source and copy are
identical.

Do not place disconnected raw outputs here. Raw outputs stay under the project
experiment workspace.

## Mainline Update Test

A result or discussion updates the mainline only if it changes one of:

- graph route;
- anchor claim boundary;
- anchor status;
- experiment interpretation;
- what cannot be claimed;
- next decision.

If none change, write:

```text
No mainline update today.
```

## Daily / Meeting Workflow

Maintain one chain per active anchor:

```text
anchor -> execution -> summary/detailed -> anchor update -> root anchor copy -> sync closure/report
```

Daily cards are not task logs. They should keep only evidence that affects the
mainline, claim boundary, or next decision. If no viewpoint changed, write
`No viewpoint update today` or `No mainline update today` and explain why in one
sentence.

For group-meeting preparation, build reports from project-local sync and
mainline files, not from chat history. Meeting reports belong under:

```text
daily_research_reports/MMDD/meeting/
daily_research_reports/MMDD/meeting/prism/
```

Use a self-contained structure:

```markdown
## 1. Research Question
## 2. Why This Matters
## 3. Current Hypothesis
## 4. Experiment Setup
## 5. Key Result
## 6. Interpretation
## 7. What We Cannot Claim
## 8. Next Decision
## 9. Backup Figures / Artifact Map
```

Assume the reader has not followed prior notes. In three minutes they should
understand the question, evidence, boundary, and next action.

## Rules

- Prefer fewer, sharper experiments over many weak ones.
- Do not promote raw logs, temporary notes, or exploratory branches into
  `main/`.
- Keep sync closures self-contained but concise.
- Do not leave completed anchors with stale evidence, claim boundary, next
  decision, or result document links.
- When figures exist, copy report-ready images into local `figures/` and
  explain what each figure supports.
- Markdown formulas must use `$...$` or `$$...$$`.

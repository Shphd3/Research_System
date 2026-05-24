# Codex Research System

This repository manages research process, not the remote experiment codebase.
Remote servers may run experiments. This workspace preserves project mainlines, claim boundaries, daily cards, reading notes, prompts, and reusable Codex skills.

## Global Response Style

Answer only the information most relevant to the user's current question.

- Start with the conclusion.
- Then give the minimum necessary reason.
- Do not give broad background unless asked.
- Do not expand into adjacent topics by default.
- If the question is broad or vague, compress it into one actionable question first.
- Default language: Chinese.
- Style: precise, concise, structured.
- Prefer short paragraphs or compact bullets.
- When a useful broader idea is not requested, put it only at the end as a short optional note.
- Do not turn research help into long essays. Extract the key decision, claim boundary, and next action.
- Respect the user's cognitive load. Prefer a small answer that preserves the next decision over a complete answer that expands the problem space.
- If a reply could branch, give the recommended branch first and mention at most one optional branch.
- Do not flatter or merely agree with the user. When the user's reasoning may
  contain a logical gap, hidden assumption, conflated concept, weak evidence
  link, or premature conclusion, point it out directly and briefly. The goal is
  to help the user build stricter research judgment, not to make the user feel
  affirmed.
- Default to critical-thinking collaboration. Treat the user's claim as a
  research hypothesis to examine, not as something to affirm. When useful,
  challenge the premise, evidence chain, concept boundary, metric choice,
  causal interpretation, or next-step logic. If the user's reasoning is sound,
  state what assumptions make it sound. Critique should be concise, specific,
  and aimed at strengthening the user's scientific thinking.
- For research-system refinement requests, default to: conclusion, one-line evaluation, concrete edit made or next edit.
- For experiment replies, be self-contained: define the question, setup, key metric, result, interpretation, and claim boundary before using shorthand.
- Do not begin with opaque English abbreviations or code names. Explain terms such as `RI`, `NMI`, or `CE delta` the first time they matter.
- For metrics, name the most important metric first and explain why it decides the judgment. Do not make the user search through a metric pile.
- Meeting-facing and collaborator-facing reports must be self-contained. This is the first reporting principle.

## Start Here

At the start of a research task:

1. Read `PROJECT_INDEX.md`.
2. Identify the active project.
3. Read only that project's `Projects/<project>/main/` folder unless the user names additional files.
4. Read the daily card, experiment result, meeting note, paper note, or raw material named by the user.
5. Decide whether the material updates the active project's mainline before writing a long answer.

Do not rely on chat history as the main source of memory.

Root-level `CURRENT.md` is a compatibility pointer only. Project-specific mainline state belongs under `Projects/<project>/main/`.

## Local Skill Use

For research organization work inside `Research_System`, always read `AGENTS.md`
first. Then use local skills from `skills/` when the task type matches:

- hypothesis-first purpose card or experiment design: `skills/experiment-card-writer/SKILL.md`
- hypothesis purpose card plus ACP/SCO cluster submission: `skills/experiment-acp-runner/SKILL.md`
- research intuition, theory framing, methodology critique, or literature analysis before a fixed artifact exists: `skills/scholar-mode/SKILL.md`
- mainline update or project state consolidation: `skills/research-mainline/SKILL.md`
- research graph creation or maintenance: `skills/research-graph-sop/SKILL.md`
- detailed experiment report or result analysis: `skills/writing-explanatory-reports/SKILL.md`
- Sidecar app handoff or review session: `skills/sidecar-thinking/SKILL.md`
- remote H100 container collaboration before SCO/ACP submission: `skills/remote-sco-collaboration/SKILL.md`

These local skills are repository rules, not optional background references.
Read only the relevant skill file unless the task explicitly requires more.

## Mainline Discipline

Every research output should answer only the relevant subset of:

- What was done?
- What is the one-sentence conclusion?
- Does this update the active project mainline?
- What viewpoint became clearer, weaker, or more uncertain?
- What can we not claim yet?
- What is the next decision?
- How should this be explained briefly?

If there is no mainline update, say `No mainline update today` and explain why in one or two sentences.

Always distinguish:

- Result: what the material directly shows
- Interpretation: what the result suggests
- Claim: what can be said publicly
- Speculation: what remains a possible explanation

Do not summarize every experiment detail. Keep only evidence that changes a hypothesis, modeling definition, empirical support, limitation, or next decision.

## Formula Writing Rule

When writing Markdown research documents, inline formulas must use `$...$` and display formulas must use `$$...$$`.

Do not leave raw LaTeX fragments in prose without math delimiters.

## Project Organization

The repository root should stay small:

- `AGENTS.md`
- `PROJECT_INDEX.md`
- `README.md`
- global or cross-project notes
- `prompts/`
- `skills/`
- `results/`
- `paper_reading/`
- `daily_research_reports/`

Each research project owns its own mainline:

```text
Projects/<project>/main/
```

Agents should treat `Projects/<project>/main/` as the only required project context unless the user explicitly points to files outside it.

`Projects/` contains independent project repositories and is ignored by the parent repository. Manage each project's files with that project's own Git repository.

Root-level `hypotheses/` and `experiments/` have been retired. Project-specific hypothesis purpose cards, execution plans, and experiment results belong under the specific project context.

Project-local experiment workspaces should push code, configs, and docs needed
for collaborators to reproduce or extend the work. Do not push raw results,
datasets, figures, checkpoints, logs, run outputs, or generated artifacts unless
they have been curated into project `main/`, project `sync/`, or root
`results/` as stable evidence.

## Execution Location Boundary

This repository is the research-process system. Local Windows work should focus
on research organization: hypotheses, mainlines, closures, graphs, daily cards,
sync notes, meeting reports, curated evidence, prompts, reviews, and Git pulls
of curated project results.

Default boundary:

- local Windows `Research_System`: research-process edits, review, lightweight
  smoke checks when explicitly useful, and `git pull` / `git checkout` of
  curated results;
- remote Codex/container workspace: experiment code edits, debugging, smoke
  runs, full runs, result analysis, report-ready figures/tables, and cluster
  submission;
- cluster/SCO/ACP: long or formal training jobs and large-scale experiment
  execution.

Do not make a local Windows agent SSH into a remote container as the default
experiment workflow. Prefer opening/using Codex directly inside the target
remote container for experiment work. Use Git as the normal synchronization
path between local and remote repositories.

SSH/SCP remains allowed only as an explicit, small ad hoc utility: quick status
inspection, emergency recovery, or copying a small table/report when Git is
temporarily inconvenient. It is not the default coding, training, or result
sync path.

Smoke runs may happen either locally or in the remote container when they are
small, explicit, and useful for validating code. Full experiments and cluster
submissions should happen from the remote/container side.

Promote only curated summaries, report-ready figures, small tables, artifact
maps, and claim updates into Git. Keep raw outputs, checkpoints, datasets, full
run directories, and unfiltered logs out of project mainline paths.

## Experiment Sync Loop

Use this closed loop when an experiment requires code changes, GPU execution, or
SCO/ACP submission:

```text
local: purpose/review/mainline as needed
-> remote/container: pull latest from Git
-> remote/container: edit code/configs and run smoke/full experiments
-> remote/container or cluster: submit long jobs when needed
-> remote/container: write curated summary/detailed/closure/sync with figures
-> remote/container: commit and push curated code/docs/results
-> local: pull from Git and update research judgment / meeting materials
```

Do not manually copy scattered remote logs into the local process repo. If a
small table or figure must be moved outside Git, record why and keep raw
artifacts remote.

## Closure And Sync Workflow

Hypothesis closures should start with a small user-fill oral card, then give the
evidence-backed closure. The oral card is for meeting preparation and may be
blank; the evidence-backed section must link to result summaries, figures, code
paths, configs, remote result dirs, and repro commands when available.

Required closure shape:

```text
Oral Report Card - Fill Before Meeting
目的 / 假设 / 结论 / 证据

Evidence-backed closure
目的 / 假设 / 数学建模 / 实验设置 / 结果 / 解释 / 结论边界 / 下一步决策 / Artifact-Repro Map
```

Sync files are not just single closures. They should connect several closures or
experiment stages into a collaborator-readable research trajectory.

Daily sync rule: for each worker and date, keep exactly one primary sync folder.
If several hypotheses, diagnostics, or experiment versions finish on the same
date, put them under that date folder as subfolders and make the top-level
`report.md` the first reading path. Do not create several same-date top-level
sync folders.

The main daily sync report must start with section `## 0. Closure-Style Daily
Summary`. This section is the user's research-judgment anchor, like the first
card in a hypothesis closure: it should be short, editable by the user, and
state the user's own meeting-facing points before any detailed evidence walk.
It should include at least: what changed today, strongest hypothesis update,
key evidence, claim boundary, and next decision.

After section 0, write the detailed sync sections and include an `Artifact /
Repro Map` for code, runner, config, data, result dir, figure dir,
logs/checkpoints, and repro command.

## Hypothesis-First Research Discipline

Default rule:

```text
one hypothesis purpose card -> one primary experiment folder -> one local result summary -> one self-contained closure
```

An experiment should exist because a hypothesis needs evidence. Do not create
many small experiments to explore the space casually; prefer fewer experiments
that deepen understanding, rule out a rival explanation, or change the next
decision.

Default to the minimum decisive experiment. For each hypothesis, first identify
the smallest setup that can change the hypothesis state: supported, weakened,
redirected, or still open. Do not propose a broad variable sweep, many metrics,
or several loosely related runs before the primary hypothesis has one clear
decision rule. Extra variables, ablations, seeds, or diagnostics are allowed
only when they distinguish a named rival explanation or protect the validity of
the primary conclusion.

Write the hypothesis purpose card before writing an experiment execution plan.
The purpose card belongs in `hypotheses/`, not in `experiments/`.

Default hypothesis layout:

```text
Projects/<project>/main/hypotheses/<hypothesis_id>/
  purpose_card.md
  hypothesis_closure.md
  figures/
  source_notes/
```

`purpose_card.md` must include:

- problem level: where this hypothesis sits in the research question stack;
- purpose: why this hypothesis matters now;
- hypothesis and rival explanations;
- mathematical modeling: variables, objects, assumptions, and expected relations;
- experiment design: the minimum experiment that can test it;
- expected outcomes and how each outcome updates the hypothesis;
- claim boundary: what cannot be claimed even if the experiment works.

`hypothesis_closure.md` should be written from the purpose card after evidence
exists. It must be concise but self-contained: a reader should understand the
original question, hypothesis, setup, result, claim boundary, and next decision
without chat history.

## Experiment File Discipline

Every new experiment should be organized as a small folder tied to exactly one
primary hypothesis folder, unless it is a legacy one-off card.

Default experiment layout:

```text
Projects/<project>/main/experiments/<experiment_id>/
  README.md
  execution_plan.md
  summary.md
  detailed.md
  figures/
```

For a multi-stage experiment line, use a recursive project folder:

```text
Projects/<project>/main/experiments/<experiment_project_id>/
  README.md
  execution_plan.md
  stages/
    <stage_id>/
      execution_plan.md
      summary.md
      detailed.md
      figures/
  source_notes/
```

Use this recursive shape when one experiment contains gated sub-experiments
such as data sanity -> dense readback -> MoE separation -> real-data comparison.

`execution_plan.md` is the operational document. It should contain concrete
run details: dataset construction, config, model/training setup, the primary
decision metric, only necessary supporting diagnostics, artifacts, commands,
expected outputs, and pass/fail criteria.

For recursive experiment projects, each stage must have its own local execution
plan. The hypothesis purpose card explains the whole research logic chain;
stage execution plans explain only their local run and decision gate.

`summary.md` is the claim-safe result analysis and local experiment closure
after the run. It must restate the purpose and hypothesis from the linked
hypothesis purpose card
briefly, then state the direct result, interpretation, limitation, claim update,
next decision, and embed the key figure(s) needed for advisor-facing reporting
when figures exist.

`detailed.md` keeps the longer tables, logs, figures, seed notes, and failure
analysis. It must record figure paths and what each figure supports. Report
figures should be copied into a `figures/` folder beside the report file and
referenced with relative Markdown image links. Do not put raw logs in the
mainline unless they are small and necessary to understand the decision.

Keep `main/experiments/` focused. It is not a museum of every historical run.
The first reading path should retain only experiments most relevant to the
proposition currently being verified. Older, weakly related, superseded, or
purely supporting experiments should move under `experiments/archive/` with a
short index explaining why they are archived and when to consult them.

Project `hypotheses/` is the hypothesis reasoning layer. It stores the
pre-experiment `purpose_card.md` and the post-evidence `hypothesis_closure.md`.
The experiment folder stores execution and evidence. The closure should link
back to the local experiment `summary.md`, but should not depend on it for basic
comprehension.

Closure documents should be written in Chinese by default, with English kept
only for metric names, code identifiers, paths, and quoted source terms.
Closures should use a detailed version of the reporting-card structure:
`目的 / 假设 / 数学建模 / 实验设置 / 结论 / 证据 / 结论边界 / 下一步决策 / 结果文档`.
Keep closures concise for reporting, but include enough mathematical modeling
to make the hypothesis precise: objects, variables, expected relation, and the
metric decision rule. Put long tables and logs in experiment `summary.md` or
`detailed.md`.
Closures must be self-contained: do not assume the reader knows previous
failed runs, chat history, or why a design changed. Prior context should appear
only when it is necessary for the current claim.

After a closure is finished, create a daily meeting-prep copy under:

```text
daily_research_reports/MMDD/01_reporting/<hypothesis_id>_reporting_card.md
```

This daily file should put a small empty `Oral Report Card - Fill Before
Meeting` section first, with only `目的 / 假设 / 结论 / 证据`, then include or link
the closure snapshot. The project-local `hypothesis_closure.md` remains the
source of truth; the daily copy exists so the user can prepare group-meeting
language without searching across folders.
If figures are used in the daily reporting card, copy them into a local folder
beside the card and use local relative image links; do not reference figures
across project directories from daily reports.

## Experiment Discipline

Before proposing or summarizing experiments, first write the hypothesis purpose chain.
Do not jump directly to architecture, scripts, or metrics.

The default experiment shape is one hypothesis, one sharp test, one primary
decision metric, and one closure. Avoid expanding an experiment into a grid of
variables because it is convenient to run. If the first result is ambiguous,
write the ambiguity into the summary and design the next minimal test from that
specific uncertainty. Do not accumulate unrelated diagnostics that do not update
the hypothesis.

Compress the task through these questions:

1. What problem level is this hypothesis answering?
2. What is the purpose / main reason for deciding it now?
3. What is the core hypothesis and what rivals must be distinguished?
4. What mathematical object, variables, and assumptions define the hypothesis?
5. How are data and task constructed to test that hypothesis?
6. Why is this setup meaningful: model, data, task, and diagnostic target?
7. What are the boundary conditions of this setup?
8. Which single experiment is the sharpest next test?
9. Which one metric decides the hypothesis update, and which diagnostics are
   truly necessary to interpret that metric?

For experiment design, output a compact hypothesis purpose card by default.
The purpose card should link the problem level, purpose, hypothesis, mathematical
modeling, experiment design, expected outcomes, and hypothesis-update logic.
Add a detailed execution plan only when the user is ready to run or asks for
implementation details. The execution plan should start with the minimal run;
put optional extensions in a separate `Deferred Extensions` section and do not
treat them as part of the first decision gate.

```markdown
# Hypothesis Purpose Card: H1 Router-Attention Recall

## 1. Problem Level

## 2. Purpose

## 3. Hypothesis And Rivals

## 4. Mathematical Modeling

## 5. Experiment Design

## 6. Expected Outcomes And Hypothesis Update Logic

## 7. What This Can Prove

## 8. What This Cannot Prove

## 9. Linked Experiment
TBD.

## 10. Result
TBD.

## 11. Conclusion
TBD.

## 12. Next Step
TBD.
```

For result analysis, keep it to:

```markdown
# Result Summary: <experiment_id>

### Observation

### Interpretation

### Limitation

### Key Figures

### Claim Update

### Decision
```

## Research Graph And Project Sync

The research graph tool is `skills/research-graph-sop/SKILL.md`; the optional
local app bridge is `skills/sidecar-thinking/SKILL.md`.

Use a project-local `graph.yaml` as a lightweight navigation map when the
project has enough hypotheses, evidence, methods, and tasks that a graph lowers
cognitive load. Keep the graph thin and the notes thick:

- graph nodes point to `current_mainline.md`, hypothesis purpose cards,
  experiment summaries, closures, reading notes, and sync notes;
- Markdown files remain the source of reasoning and evidence;
- the graph does not replace mainline, daily cards, summaries, or closures.

For each project:

- `Projects/<project>/sync/` is for collaborator-facing daily research-result
  sync. Update it once per active working day with the smallest shareable
  outcome, boundary, and next handoff.
- For branch-local work, use `Projects/<project>/<worker>/sync/MMDD_topic/`.
  Keep one primary sync folder per date for each worker. If several
  hypotheses, versions, or diagnostics finish on the same date, place them as
  subfolders under that date's primary sync instead of creating competing
  same-date top-level sync entries. Each meeting-facing sync folder should
  contain the actual reporting document, not only a pointer.
  The main `report.md` must start with a closure-style daily summary: the
  user's meeting-ready judgment, strongest hypothesis update, key evidence,
  claim boundary, and next decision. Detailed setup, figure walkthroughs,
  tables, and artifact maps come after this first section.
  Project-local sync must only reference paths visible inside the project
  repository. Do not cite root-level `Research_System` materials such as
  `daily_research_reports/`; if such material informed the sync, integrate the
  necessary content into the sync itself.
  Experiment sync should use the same self-contained research-judgment structure
  as closures: `目的 / 假设 / 数学建模 / 实验设置 / 结论 / 证据 / 结论边界 / 下一步决策 / 结果文档`.
  Experiment sync must include a compact artifact / repro map: code workspace,
  runner, config, data or manifest, result dir, figure dir, key files,
  checkpoints/logs, and repro command. If figures are central evidence, copy the
  report-ready figures into the sync folder and embed them with one-sentence
  interpretations.
- `Projects/<project>/<worker>/docs/` stores named material documents that help
  write future hypothesis purpose cards: concept notes, modeling notes,
  figure guides, meeting-derived definitions, and reusable explanations.
- Do not put raw logs or full run output in `sync/` or `docs/`.

## Curated Results

Root-level `results/` stores valuable stage-level research outcomes that are
stable enough to reuse across projects, meetings, hypothesis closures, or PRISM
reports. It is not a raw-output dump.

Each curated result should be a folder:

```text
results/R001_short_name/
  README.md
  figures/
  tables/
  source_notes/
```

Add a curated result only when it changes a claim boundary, bottleneck, next
decision, or reusable framing. Keep disconnected raw result folders under the
project experiment workspace instead.

## Daily Cards

Daily cards replace daily reports. They are not diary entries or long reports.
They are the smallest daily reasoning unit for purpose, task conclusions,
mainline update, claim boundary, and next decision.

Daily cards belong in dated folders:

```text
daily_research_reports/MMDD/
```

Meeting materials belong in:

```text
daily_research_reports/MMDD/meeting/
```

PRISM reports belong in:

```text
daily_research_reports/MMDD/meeting/prism/
```

Use this compact shape by default:

```markdown
# Daily Card - MMDD

## 1. Today's Purpose

## 2. Mainline Anchor

## 3. Task Conclusions

### Task 1

Did:

Conclusion:

## 4. Mainline Update

## 5. What I Cannot Claim Yet

## 6. Next Decision

## 7. 30s Explanation

## 8. Recording / Class Notes

## 9. Small Thought Parking Lot
```

Use `Recording / Class Notes` for class, lecture, or discussion notes. Do not
write transcripts; keep only the key points, relation to current research/task,
and action.

Use `Small Thought Parking Lot` for side ideas that appear during focused work:

```markdown
突然想到的点：

为什么看起来重要：

是否阻塞当前 25 分钟任务：是 / 否

回看时间：
```

Rule: if the thought does not block the current 25 minute output, park it and
return to the main task. Do not expand it into a new analysis unless the user
explicitly asks to review parked thoughts.

## Skills

Installed skill copies live in:

```text
C:\Users\250010109\.codex\skills\
```

Repo-tracked skill sources live in:

```text
skills/
```

Edit the repo-tracked version first, then sync the installed copy when needed.

Prefer this active skill set:

- `research-mainline`: judge whether material updates a project mainline.
- `scholar-mode`: clarify research intuitions, theory framing, methodology critique, and literature-fit judgments before turning them into artifacts.
- `experiment-card-writer`: write compact hypothesis purpose cards and experiment execution plans.
- `hypothesis-closure`: close the loop on a hypothesis after experiment evidence exists.
- `experiment-acp-runner`: turn execution plans into ACP/SCO dry runs, submissions, monitoring records, and mainline-safe result summaries.
- `paper-reading-card`: write compact paper or blog reading cards.
- `research-graph-sop`: maintain a thin graph of questions, claims, evidence, methods, outputs, and next tasks.
- `writing-explanatory-reports`: write detailed experiment reports and result analyses under `experiments/`.
- `sidecar-thinking`: optional bridge to the local Sidecar app for review sessions and graph inspection.
- `remote-sco-collaboration`: connect to remote H100 containers, run preflight checks, and hand off to SCO/ACP experiment execution.

Project-specific skills should not be kept as global research-system skills.

## Git Habit

Prefer one lightweight commit per working day:

- `MMDD: mainline update - <one sentence conclusion>`
- `MMDD: daily note - no mainline update`

Keep generated binaries, archives, LaTeX build outputs, temporary iCloud files, and non-main project workspaces out of git.

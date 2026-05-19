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
first. Then use local skills from `codex_skills/` when the task type matches:

- experiment plan or experiment card: `codex_skills/experiment-card-writer/SKILL.md`
- experiment card plus ACP/SCO cluster submission: `codex_skills/experiment-acp-runner/SKILL.md`
- experiment result or daily synthesis: `codex_skills/daily-report-coach/SKILL.md`
- claim boundary or public wording audit: `codex_skills/claim-auditor/SKILL.md`
- mainline update or project state consolidation: `codex_skills/research-mainline/SKILL.md`
- meeting / group-report preparation: `codex_skills/meeting-brief-coach/SKILL.md`

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
- `codex_skills/`
- `paper_reading/`
- `daily_research_reports/`

Each research project owns its own mainline:

```text
Projects/<project>/main/
```

Agents should treat `Projects/<project>/main/` as the only required project context unless the user explicitly points to files outside it.

`Projects/` contains independent project repositories and is ignored by the parent repository. Manage each project's files with that project's own Git repository.

Root-level `hypotheses/` and `experiments/` have been retired. Project-specific hypotheses, experiment cards, and experiment results belong under the specific project context.

## Experiment File Discipline

Every new experiment should be organized as a small folder, not as an isolated
flat note, unless it is a legacy one-off card.

Default experiment layout:

```text
Projects/<project>/main/experiments/<experiment_id>/
  README.md
  purpose_card.md
  execution_plan.md
  summary.md
  detailed.md
  figures/
```

For a multi-stage experiment line, use a recursive project folder:

```text
Projects/<project>/main/experiments/<experiment_project_id>/
  README.md
  purpose_card.md
  execution_plan.md
  stages/
    <stage_id>/
      purpose_card.md
      execution_plan.md
      summary.md
      detailed.md
      figures/
  source_notes/
```

Use this recursive shape when one experiment contains gated sub-experiments
such as data sanity -> dense readback -> MoE separation -> real-data comparison.

`purpose_card.md` is the first document to write. It stabilizes the research
thinking before execution. It is not the place for operational details. It must
connect the experiment's purpose chain:

- the overall purpose and why this experiment exists;
- where it sits in the active project mainline;
- the known narrative, premises, or prior results being used;
- the experiment purpose;
- the hypothesis and refined sub-hypotheses;
- the experiment object and high-level paradigm;
- the expected result patterns and how each would update the hypothesis;
- what cannot be claimed even if the experiment works.

Keep concrete run details, commands, config paths, model hyperparameters,
metric schemas, artifact contracts, and pass/fail mechanics in
`execution_plan.md`, not in `purpose_card.md`.

`execution_plan.md` is the operational document. It should contain concrete
run details: dataset construction, config, model/training setup, metrics,
artifacts, commands, expected outputs, and pass/fail criteria.

For recursive experiment projects, each stage must have its own local purpose
card and execution plan. The top-level purpose card explains the whole research
logic chain; stage cards explain only their local decision.

`summary.md` is the claim-safe result analysis and local experiment closure
after the run. It must restate the purpose and hypothesis from the purpose card
briefly, then state the direct result, interpretation, limitation, claim update,
next decision, and embed the key figure(s) needed for advisor-facing reporting
when figures exist.

`detailed.md` keeps the longer tables, logs, figures, seed notes, and failure
analysis. It must record figure paths and what each figure supports. Report
figures should be copied into a `figures/` folder beside the report file and
referenced with relative Markdown image links. Do not put raw logs in the
mainline unless they are small and necessary to understand the decision.

Project `hypotheses/` is reserved for larger advisor-facing hypothesis closure
documents. These synthesize one experiment line or a tightly scoped hypothesis
family for reporting; each big closure should live in its own subfolder with a
local `figures/` directory, and should link back to the local experiment
`summary.md` files rather than replacing them.

Big closure documents should be written in Chinese by default, with English kept
only for metric names, code identifiers, paths, and quoted source terms.
Keep big closures concise for reporting: merge mainline anchor with hypothesis,
merge claim update with cannot-claim boundaries, and merge weakest point with
next decision. Put setup details and long tables in experiment `summary.md` or
`detailed.md`.
Big closures must be self-contained: do not assume the reader knows previous
failed runs, chat history, or why a design changed. Prior context should appear
only when it is necessary for the current claim.

## Experiment Discipline

Before proposing or summarizing experiments, first write the purpose chain.
Do not jump directly to architecture, scripts, or metrics.

Compress the task through these questions:

1. What is the purpose / main reason for this experiment?
2. What known narrative or premise makes this experiment meaningful?
3. What is the core hypothesis?
4. How are data and task constructed to test that hypothesis?
5. Why is this setup meaningful: model, data, task, and diagnostic target?
6. What are the boundary conditions of this setup?
7. Which experiments are needed, and do they jointly test the hypothesis rather than only show a suggestive signal?

For experiment design, output a compact purpose card by default. The purpose
card should link the mainline position, known premises, experiment purpose,
hypothesis, object, paradigm, expected outcomes, and hypothesis-update logic.
Add a detailed execution plan only when the user is ready to run or asks for
implementation details.

```markdown
# Experiment Card: E1 Router-Attention Recall

## 1. Purpose / Main Reason

## 2. Mainline Position

## 3. Known Narrative / Premise

## 4. Experiment Purpose

## 5. Hypothesis And Sub-Hypotheses

## 6. Experiment Object

## 7. Experiment Paradigm

## 8. Expected Outcomes And Hypothesis Update Logic

## 9. What This Can Prove

## 10. What This Cannot Prove

## 11. Result
TBD.

## 12. Conclusion
TBD.

## 13. Next Step
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
codex_skills/
```

Edit the repo-tracked version first, then sync the installed copy when needed.

Prefer this active skill set:

- `research-mainline`: judge whether material updates a project mainline.
- `claim-auditor`: audit claim strength against evidence.
- `experiment-card-writer`: write compact experiment cards and result-decision blocks.
- `hypothesis-closure`: close the loop on a hypothesis after experiment evidence exists.
- `experiment-acp-runner`: turn experiment cards into ACP/SCO dry runs, submissions, monitoring records, and mainline-safe result summaries.
- `daily-report-coach`: write compact daily cards.
- `meeting-brief-coach`: prepare 30 second / 1 minute advisor-facing explanations.
- `prism-report`: build meeting-ready PRISM reports.
- `paper-reading-card`: write compact paper or blog reading cards.

Project-specific skills should not be kept as global research-system skills.

## Git Habit

Prefer one lightweight commit per working day:

- `MMDD: mainline update - <one sentence conclusion>`
- `MMDD: daily note - no mainline update`

Keep generated binaries, archives, LaTeX build outputs, temporary iCloud files, and non-main project workspaces out of git.

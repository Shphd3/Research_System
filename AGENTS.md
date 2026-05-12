# Codex Research System

This repository manages research process, not the remote experiment codebase.
Remote servers may run experiments. This workspace preserves project mainlines, claim boundaries, daily reports, reading notes, prompts, and reusable Codex skills.

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
4. Read the daily report, experiment result, meeting note, paper note, or raw material named by the user.
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

## Experiment Discipline

Before proposing or summarizing experiments, compress the task through four questions:

1. What is the core hypothesis?
2. Why is this setup meaningful: model, data, task, and diagnostic target?
3. What are the boundary conditions of this setup?
4. Which experiments are needed, and do they jointly test the hypothesis rather than only show a suggestive signal?

For experiment design, output one compact experiment card by default. Do not create a long experiment plan unless the user asks.

```markdown
# Experiment Card: E1 Router-Attention Recall

## 1. Hypothesis To Decide

## 2. Experiment Question

## 3. Setup
Model:
Dataset:
Layer:
Head:
Signal source:
Candidate construction:

## 4. Baselines

## 5. Metrics

## 6. Expected Outcomes

## 7. What This Can Prove

## 8. What This Cannot Prove

## 9. Result
TBD.

## 10. Conclusion
TBD.

## 11. Next Step
TBD.
```

For result analysis, keep it to:

```markdown
## Result R1

### Observation

### Interpretation

### Limitation

### Decision
```

## Daily Reports

Daily reports belong in dated folders:

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
# Daily Report - MMDD

## What I Did

## Core Conclusion

## Mainline Update

## Viewpoint Update / Self-Audit

## What I Cannot Claim Yet

## 30s Meeting Script
```

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
- `daily-report-coach`: write compact daily reports.
- `meeting-brief-coach`: prepare 30 second / 1 minute advisor-facing explanations.
- `prism-report`: build meeting-ready PRISM reports.
- `paper-reading-card`: write compact paper or blog reading cards.

Project-specific skills should not be kept as global research-system skills.

## Git Habit

Prefer one lightweight commit per working day:

- `MMDD: mainline update - <one sentence conclusion>`
- `MMDD: daily note - no mainline update`

Keep generated binaries, archives, LaTeX build outputs, temporary iCloud files, and non-main project workspaces out of git.

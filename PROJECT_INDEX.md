# Project Index

This is the first lookup target for ChatGPT Project, GitHub connector, Codex cloud, and local Codex tasks.

## Global Rule

For any project-specific task, read only:

```text
Projects/<project>/main/
```

Do not scan the full project folder unless the user explicitly names extra files. The `main/` folder is the compressed project context: current question, mainline, claim boundary, and next decision.

`Projects/` contains independent project repositories and is ignored by this parent repository. If a cloud or web agent needs project-local files, index or clone the specific project repository as well.

## Active Project

Current primary project:

```text
Projects/from-attention-to-search/
```

Repository:

```text
https://github.com/BinaryCheater/from-attention-to-search.git
```

Required context:

- `Projects/from-attention-to-search/main/current_mainline.md`

Optional supporting files only when requested:

- `Projects/from-attention-to-search/docs/architecture.md`
- `daily_research_reports/0511/architecture.md`
- `daily_research_reports/0511/flat_real_inference.md`

Current project question:

> Can long-context attention be reframed as model-native search over dynamic KV memory, with hierarchical indexing and exact sparse attention over retrieved candidates?

## Secondary Project

MoE / continual-learning project:

```text
Projects/MoE-Continual-Learning/
```

Required context:

- `Projects/MoE-Continual-Learning/main/README.md`
- `Projects/MoE-Continual-Learning/main/01_current_state.md`
- `Projects/MoE-Continual-Learning/main/FILE_INDEX.md`

Use this only when the user explicitly asks about MoE, specialization, forgetting, or old Feature-Zipf results.

## Root-Level Files

- `AGENTS.md`: global agent behavior and repository rules.
- `PROJECT_INDEX.md`: project routing and lookup map.
- `README.md`: repository overview.
- `CURRENT.md`: compatibility pointer, not canonical project state.
- `claim_board.md`: legacy or cross-project claim board. Prefer project-local claim files when present.

Removed root-level project folders:

- `experiments/`: project-specific experiment cards should live under the specific project.
- `hypotheses/`: project-specific hypotheses should live under the specific project.
- `mainline.md`: merged into the project-local mainline convention and root `CURRENT.md` pointer.

## Daily Work

- `daily_research_reports/_templates/daily_log_template.md`: daily report template.
- `daily_research_reports/MMDD/`: daily work folder.
- `daily_research_reports/MMDD/meeting/`: meeting materials.
- `daily_research_reports/MMDD/meeting/prism/`: PRISM report and figures.

## Reading Memory

- `paper_reading/_templates/summary_card.md`: shortest first-pass card.
- `paper_reading/_templates/paper_reading_record.md`: full paper reading process.
- `paper_reading/_templates/blog_reading_record.md`: blog / essay reading process.
- `paper_reading/`: categorized paper and blog notes.

## Project Prompts

- `prompts/project_instructions/research_progress_project_prompt.md`: ChatGPT Project prompt for web-side reasoning.

## Skill Sources

Use `skills/README.md` for the skill map.

Primary active skills:

- `codex_skills/research-mainline/SKILL.md`
- `codex_skills/claim-auditor/SKILL.md`
- `codex_skills/experiment-card-writer/SKILL.md`
- `codex_skills/daily-report-coach/SKILL.md`
- `codex_skills/meeting-brief-coach/SKILL.md`
- `codex_skills/prism-report/SKILL.md`
- `codex_skills/paper-reading-card/SKILL.md`

## Web-Side Mode Map

Use `prompts/project_instructions/research_progress_project_prompt.md` and choose one mode:

1. Meeting transcript debrief
2. Mainline planning / experiment design
3. Experiment result sync / claim audit
4. Pre-meeting convergence
5. Daily viewpoint update

## Write Policy

ChatGPT Project should not assume it can write to this repository. It should give concise suggested file edits for the user to copy, or ask the user to delegate edits to Codex cloud.

Codex cloud may edit files in this repository, but should follow `AGENTS.md`, use `PROJECT_INDEX.md`, and keep project context under `Projects/<project>/main/`.

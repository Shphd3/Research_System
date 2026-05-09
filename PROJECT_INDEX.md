# Project Index

This file is the first lookup target for ChatGPT Project, GitHub connector, and Codex cloud tasks.

## Core Research State

- `AGENTS.md`: repository rules for Codex and research workflow.
- `CURRENT.md`: current research state, safest claim, bottleneck, and current task.
- `mainline.md`: long-term research mainline and open questions.
- `claim_board.md`: current claim status and evidence boundaries.

## Daily Work

- `daily_research_reports/_templates/daily_log_template.md`: daily report template.
- `daily_research_reports/MMDD/daily_report.md`: daily report for one date.
- `daily_research_reports/MMDD/meeting/`: meeting materials for one date.
- `daily_research_reports/MMDD/meeting/prism/`: PRISM report and figures for one date.

## Experiment Memory

- `experiments/`: cross-day experiment cards.
- `daily_research_reports/MMDD/experiment_analysis.md`: date-local experiment analysis when available.
- `results/`: reusable result summaries or artifacts.

## Reading Memory

- `paper_reading/_templates/paper_reading_record.md`: paper reading record template.
- `paper_reading/_templates/blog_reading_record.md`: blog / essay reading record template.
- `paper_reading/`: categorized paper and blog notes.

## Project Prompts

- `prompts/project_instructions/research_progress_project_prompt.md`: ChatGPT Project system prompt for web-side reasoning.
- `prompts/project_instructions/group_meeting_project_prompt.md`: older group-meeting prompt kept for reference.

## Personal Codex Skills

- `codex_skills/research-mainline/SKILL.md`
- `codex_skills/claim-auditor/SKILL.md`
- `codex_skills/daily-report-coach/SKILL.md`
- `codex_skills/prism-report/SKILL.md`
- `codex_skills/meeting-brief-builder/SKILL.md`
- `codex_skills/meeting-brief-coach/SKILL.md`

## Web-Side Mode Map

Use `prompts/project_instructions/research_progress_project_prompt.md` and choose one mode:

1. Meeting Transcript Debrief
2. Mainline Planning / Experiment Design
3. Experiment Result Sync / Claim Audit
4. Pre-Meeting Convergence
5. Daily Viewpoint Update

## Write Policy

ChatGPT Project should not assume it can write to this repository. It should output suggested file updates for the user to copy, or ask the user to delegate file edits to Codex cloud.

Codex cloud tasks may edit files in this repository, but should follow `AGENTS.md` and keep outputs under the correct dated folder.

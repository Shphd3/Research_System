# Research Files

This repository is a research-process workspace. It is not the remote experiment codebase.

The goal is to preserve research judgment: mainline, hypotheses, evidence, claim boundaries, daily cards, paper reading cards, and meeting-ready PRISM reports.

## Start Here

- `CURRENT.md`: current research mainline, safest claim, bottleneck, and next decision.
- `PROJECT_INDEX.md`: project routing and lookup map.
- `AGENTS.md`: project-level Codex instructions.
- `PROJECT_SNAPSHOT_from_attention_to_search.md`: root-visible active-project
  snapshot for web-side and paper-reading AI that cannot access `Projects/`.

## Working Areas

- `daily_research_reports/`: dated folders for daily cards, meeting materials, PRISM reports, experiment summaries, and report bundles.
- `paper_reading/`: literature cards and reading notes.
- `skills/`: repo-tracked source copies of personal Codex skills.
- `results/`: curated folders for valuable stage-level research outcomes.
- `prompts/`: reusable project prompts and older workflow prompts.
- `docs/`: setup notes for tooling and workflow maintenance.

## Daily Loop

1. Read `CURRENT.md` and relevant evidence.
2. Decide whether today's work updates the mainline.
3. Write a compact daily card or hypothesis purpose card.
4. State the conclusion for each task, not a task log.
5. Park side thoughts instead of chasing them during the current 25 minute task.
6. Update project-local `main/` files only when evidence changes the mainline, claim boundary, bottleneck, hypothesis status, or next decision.
7. Commit the research-system update.

Daily cards should be placed at `daily_research_reports/MMDD/daily_card.md`. Use `daily_research_reports/_templates/daily_card_template.md`.

Class notes and side thoughts should stay inside `daily_card.md` by default. Use `Recording / Class Notes` for class points, and `Small Thought Parking Lot` for side ideas that should not interrupt the current task.

Meeting materials should be placed at `daily_research_reports/MMDD/meeting/`. PRISM reports should be placed at `daily_research_reports/MMDD/meeting/prism/`.

## Hypothesis-First Loop

For project research, write the hypothesis purpose card before the experiment
execution plan:

```text
Projects/<project>/main/hypotheses/<hypothesis_id>/purpose_card.md
Projects/<project>/main/experiments/<experiment_id>/execution_plan.md
Projects/<project>/main/experiments/<experiment_id>/summary.md
Projects/<project>/main/hypotheses/<hypothesis_id>/hypothesis_closure.md
```

Default principle: fewer, sharper experiments. Each experiment should deepen
understanding, test a hypothesis, or change a next decision.

## Codex Web

This local repository is ready to be connected to a remote GitHub repository for Codex Web usage. See `docs/codex_web_setup.md`.

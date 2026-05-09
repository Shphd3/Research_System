# Codex Research System

This folder is a research-process workspace, not the remote code repository.
Remote servers run experiments. This workspace preserves research judgment, evidence, reports, and presentation practice.

## Start Here

At the start of any research task:

1. Read `CURRENT.md`.
2. Read `mainline.md`.
3. Read `claim_board.md` when the task involves interpretation, reports, or meetings.
4. Read the daily report, experiment card, or raw material named by the user.
5. Decide whether the material updates the mainline before writing a long response.

Do not rely on chat history as the main source of memory.

## Mainline Discipline

Every research output must answer:

- What was done?
- What is the one-sentence conclusion?
- Does this update the current mainline?
- What viewpoint did today's work refine, correct, or make more uncertain?
- What can we not claim yet?
- How should this be explained in 30 seconds?

If there is no mainline update, say `No mainline update today` and explain why.

Do not turn experiment logs into reports by summarizing every detail. Keep only evidence that changes the hypothesis, modeling, empirical support, limitation, or next decision.

Always distinguish:

- Result: what the experiment or paper directly shows
- Interpretation: what the result suggests
- Claim: what can be said publicly
- Speculation: what remains a possible explanation

Daily work must include a short viewpoint update. This is not a diary reflection. It should state one research judgment that became clearer through experiments, paper reading, blog reading, or discussion. It must also name the weakest or most attackable part of that judgment:

- unsupported assumption
- ambiguous definition
- missing control
- possible counterexample
- wording that sounds stronger than the evidence
- next check needed to make the view more defensible

If there is no viewpoint update, write `No viewpoint update today` and state whether the day only added background, implementation progress, or raw material.

Maintain `claim_board.md` after major experiments. Every claim should be marked as `supported`, `weakly supported`, `unsupported`, `contradicted`, or `unclear`.

Experiment cards belong in `experiments/`. Every experiment card should include question, hypothesis, setup, controls, metrics, raw results, interpretation, claim strength, limitations, and next experiment.

## Daily Report Shape

Daily reports belong in dated folders under `daily_research_reports/MMDD/`. Do not create a separate root-level daily log folder.

Use `daily_research_reports/_templates/daily_log_template.md` as the starting template.

Meeting materials also belong inside the same dated daily folder:

```text
daily_research_reports/MMDD/meeting/
```

Put PRISM reports under:

```text
daily_research_reports/MMDD/meeting/prism/
```

Use this compact structure for `daily_report.md`:

```markdown
# Daily Report - MMDD

## What I Did

## Core Conclusion

## Mainline Update

## Viewpoint Update / Self-Audit

## What I Cannot Claim Yet

## 30s Meeting Script
```

## Codex Skills

Use these personal skills when they exist:

- `research-mainline`: judge whether material updates the research mainline.
- `daily-report-coach`: compress daily work into a clear daily report.
- `meeting-brief-coach`: produce advisor-facing 30 second and 1 minute explanations.
- `prism-report`: write or update group-meeting-ready PRISM project reports.
- `experiment-card-writer`: convert raw experiment material into a structured experiment card.
- `claim-auditor`: classify claims against current evidence.
- `meeting-brief-builder`: build advisor/group-meeting briefs from experiment cards and claim board.
- `paper-reading-card`: convert a paper into a compact reading card.
- `moe-specialization-diagnosis`: diagnose feature/function/routing/frequency/forgetting specialization.

The repo-tracked skill sources live in `codex_skills/`. The installed copies live in `C:\Users\250010109\.codex\skills\`.

## Repository Layout

Keep the repository root small. The root should contain only the core navigation files:

- `AGENTS.md`
- `CURRENT.md`
- `mainline.md`
- `claim_board.md`
- `README.md`

Put reusable prompts in `prompts/`, tooling notes in `docs/`, paper notes in `paper_reading/`, and all daily work including meeting materials in `daily_research_reports/MMDD/`.

## Paper Reading Library

Use `paper_reading/` for literature accumulation.

Each paper should live under one category folder and contain at least `summary_card.md`.
Use `paper_reading/_templates/summary_card.md` as the required first-pass card.

Do not turn every paper into a long note. Deep notes are only needed when the paper changes the mainline, creates a risk, or becomes necessary for a PRISM report.

## Git Habit

Prefer one lightweight commit per working day:

- `MMDD: mainline update - <one sentence conclusion>`
- `MMDD: daily note - no mainline update`

Keep generated binaries, archives, LaTeX build outputs, and temporary iCloud files out of git.

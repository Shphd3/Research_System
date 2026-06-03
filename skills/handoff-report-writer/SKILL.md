---
name: handoff-report-writer
description: Use only when existing research artifacts must be packaged for a meeting, collaborator, web-side reader, or external repo sync after the anchor, summary, detailed result, and optional report card already exist.
metadata:
  short-description: Package existing research artifacts
---

# Handoff Report Writer

This skill packages existing research artifacts. It does not create new
research content, new claims, new conclusions, or a second closure.

The source of truth remains:

```text
<anchor_id>.md = current-state hypothesis, evidence, boundary, next decision
summary.md = first post-result reading path
detailed.md = full evidence ledger and artifact map
05_report_card.md = advisor-facing evidence card, if it already exists or is explicitly requested
```

## Core Rule

Use this skill only when the user explicitly asks to package, hand off, sync, or
copy existing material.

The job is:

```text
select existing files
copy them into the target package
preserve subject-bearing filenames
copy only referenced figures/tables
write a short README or index
verify links and file existence
report what was included and excluded
```

Do not write from chat history alone. Do not invent missing results. Do not
replace anchor backfill, `summary.md`, `detailed.md`, or the advisor report
card.

If a handoff package includes `05_report_card.md`, keep it in the exact shared
structure from `templates/reporting/report_card_template.md`.
Do not convert it into a separate oral report, private question list, or second
closure.

## When To Use

Use this only when at least one is true:

- the user asks for a handoff package;
- the user asks to sync to root sync, project sync, or an external collaborator
  repo;
- a collaborator or advisor needs a small self-contained file package;
- a web-side or GitHub-side reader needs curated current artifacts without raw
  experiment outputs.

Do not create a handoff package for every ordinary experiment by default.

## Required Inputs

Read only the existing artifacts needed for the package:

```text
required:
- relevant anchor
- summary.md
- detailed.md

optional:
- protocol_for_approval.md
- execution_plan.md
- 05_report_card.md
- figures/ referenced by included markdown
- tables/ referenced by included markdown
```

If the requested package needs a report card and none exists, use
`templates/reporting/report_card_template.md` only when the user
explicitly asks to create it. Otherwise, package the existing sources and note
that no report card was included.

## Default Package Shape

Use date/topic folders:

```text
<target_root>/MMDD_or_YYYY-MM-DD/<topic>/
  README.md
  <anchor_id>.md
  summary.md
  detailed.md
  protocol_for_approval.md      # optional
  execution_plan.md             # optional
  05_report_card.md             # optional
  figures/                      # only referenced figures
  tables/                       # only referenced tables
```

For daily local packages:

```text
daily_research_reports/MMDD/<topic>/
```

For project-local sync:

```text
Projects/<project>/<worker>/sync/MMDD_topic/
Projects/<project>/sync/MMDD_topic/
```

For external collaborator repo sync:

```text
<external_collaborator_repo>/<agreed_research_sync_path>/MMDD_topic/
```

Use the target repo's existing convention when one is known. If no destination
is known, ask for the destination path before copying.

## README / Index Only

The only new text this skill should normally write is a short `README.md` or
index for navigation:

```markdown
# <date> <topic> Handoff Package

## Read Order

1. `05_report_card.md` if present
2. `<anchor_id>.md`
3. `summary.md`
4. `detailed.md`

## Scope

One or two sentences copied or tightly paraphrased from `summary.md`.

## Boundary

One or two sentences copied or tightly paraphrased from `summary.md`.

## Included Files

...
```

Do not add a new argument, new interpretation, new next step, new advisor
questions, or new experiment design in the package README.

## Include / Exclude Rules

Include only curated, reader-facing artifacts:

```text
anchor
summary.md
detailed.md
05_report_card.md
protocol or execution plan when useful for audit
figures and tables referenced by included markdown
```

Exclude by default:

```text
raw logs
checkpoints
datasets
full run directories
temporary caches
unfiltered generated figures/tables
private daily notes
unconfirmed speculation
unrelated anchors
old archived evidence
experiment code changes
```

Copy code only when the user explicitly asks for code sync.

## Safety Checks

Before copying into any external repo:

1. Check the target repo `git status --short --branch`.
2. Do not overwrite dirty collaborator files without explicit approval.
3. Keep all copied paths inside the requested target folder.
4. Convert absolute local links into relative package links when needed.
5. Verify every embedded figure/table exists inside the copied package.
6. Report included and excluded file classes before commit or push.

A request to sync files means copy/update the package. Commit and push only when
the user explicitly asks.

## Output Report

After packaging, report:

```text
target package path
included files
excluded file classes
missing optional files, if any
whether commit/push was performed
```

Keep the response short.

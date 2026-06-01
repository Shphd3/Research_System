---
name: handoff-report-writer
description: Use only when evidence must be packaged for a meeting, collaborator, or web-side handoff after the anchor, experiment summary, and detailed result are already updated.
metadata:
  short-description: Write optional research handoff reports
---

# Handoff Report Writer

Use this skill after evidence exists and after the core research documents are
updated. A handoff report is an optional external package. It is not the main
research document and it is not a second closure.

The source of truth remains:

```text
<anchor_id>.md = current-state hypothesis, evidence, refined hypothesis, boundary, next decision
summary.md = first post-result reading path
detailed.md = full iteration ledger and artifact map
```

## Core Rule

First apply `research-progress-core`. The report must state:

```text
what was tested
where the evidence is
what passed
what failed
why it failed, if known
what the next concrete test or decision is
```

Do not write a handoff report from chat history alone. Do not use it to replace
anchor backfill, `summary.md`, or `detailed.md`.

## When To Use

Use this only when the user explicitly asks for a handoff report and at least
one is true:

- a collaborator or advisor needs a self-contained report;
- a senior student's or collaborator's GitHub repo needs a small curated sync
  package;
- a web-side or GitHub-side reader should understand the result without entering
  the project repository;
- a meeting requires an advisor-facing report card and artifact map;
- multiple result documents need to be packaged into one handoff.

Do not create a handoff report for every ordinary experiment by default.

For ordinary advisor discussion, prefer a compact
`05_report_card_for_advisor.md` in the daily or experiment folder. It should be
derived from the anchor, summary, and detailed result. Use a formal handoff
report only when a collaborator, meeting package, or web-side reader needs a
self-contained transfer document.

## Required Inputs

Read in order:

1. `PROJECTS.md`;
2. project `graph.yaml`, only for navigation;
3. relevant anchor;
4. experiment `summary.md`;
5. experiment `detailed.md`;
6. key figures, tables, and artifact paths needed for reproduction.

## Location

Default daily handoff:

```text
daily_research_reports/MMDD/<topic>/handoff_report.md
daily_research_reports/MMDD/<topic>/<anchor_id>.md
```

`<anchor_id>.md` is a copy of the most important project anchor for the handoff.
Keep the subject-bearing basename from the source anchor; do not rename it to
generic `anchor.md`.

Branch-local meeting or collaborator handoff, only when project sync is
explicitly requested:

```text
Projects/<project>/<worker>/sync/MMDD_topic/report.md
Projects/<project>/<worker>/sync/MMDD_topic/<anchor_id>.md
```

Project-level handoff, only when project-level sync is explicitly requested and
the result is stable enough to share as project context:

```text
Projects/<project>/sync/MMDD_topic/report.md
Projects/<project>/sync/MMDD_topic/<anchor_id>.md
```

Root sync handoff for web-side readers is used only when root sync is explicitly
requested. It should point to the root anchor copy:

```text
sync/<sync_id>/anchors/<category>/<anchor_id>.md
```

External collaborator repo sync is used only when the user explicitly asks to
sync material to a collaborator, advisor, senior student's repo, or another
external GitHub repository. It should be a small curated package, not a mirror
of the research or experiment repo:

```text
<external_collaborator_repo>/<agreed_research_sync_path>/MMDD_topic/
  <anchor_id>.md
  summary.md
  detailed.md
  report_card.md       # optional, for quick reading
  figures/             # only if referenced by synced docs
  tables/              # only if referenced by synced docs
```

Use the external repo's existing convention when one is known. If no convention
is known, ask for the destination path before copying.

## Required Shape

The advisor-facing report card must reuse the shared report card structure from
`daily_research_reports/_templates/report_card_template.md`.
A handoff report may include the filled report card inline, but should not
define a separate incompatible report-card template. The fields below are the
handoff-facing copy of that shared report card.

```markdown
# Handoff Report: <topic>

Anchor:
Summary:
Detailed:
Most important anchor copy:

## 0. Advisor-Facing Report Card

目的：

物理建模 / 假设：

最小实验：

结论：

证据：

关键术语：

结论边界：

下一步：

## 1. What Was Tested

## 2. Evidence Location

## 3. What Passed

## 4. What Failed Or Stayed Ambiguous

## 5. Interpretation

## 6. Claim Boundary

## 7. Next Decision

## 8. Key Figures

![<figure title>](figures/<figure>.png)

Supports:

## 9. Artifact / Repro Map

code workspace:
runner:
config:
key code files:
data / manifest:
result dir:
figure dir:
key files:
checkpoints / logs:
repro command:
job id:
```

## External Collaborator Sync Package

When the handoff target is a senior student's or collaborator's repo, include
only curated material:

```text
required:
- copied current anchor using the anchor's subject-bearing filename
- summary.md
- detailed.md

optional:
- report_card.md, when the collaborator needs a fast advisor-facing summary
- figures/ or tables/, only when referenced by anchor, summary, detailed, or
  report_card
- README.md or index, only when the external repo requires one
- execution_plan.md, when syncing a proposed experiment before execution
```

Never include raw logs, checkpoints, datasets, full result directories,
unfiltered generated figures/tables, temporary caches, unrelated anchors, or
private daily notes. Do not include code changes unless the user explicitly asks
for code sync.

Before copying or updating files in the external repo:

1. Check the target repo `git status --short --branch`.
2. Do not overwrite dirty collaborator files without explicit approval.
3. Convert absolute local paths to relative package links.
4. Verify every embedded figure/table exists inside the copied package.
5. Report the included and excluded file classes before commit or push.

A request to sync the package means copy/update the package. Commit and push the
external repo only when the user explicitly asks for commit or push.

## Writing Standard

This is a decision report, not a timeline. Keep it shorter than `detailed.md`.
It should package the conclusion and evidence for transfer, not re-run the full
reasoning.

Report cards are for the advisor or collaborator to read. Do not include
private advisor questions, "if interrupted" scripts, hidden uncertainty notes,
or brainstorming prompts. Put those in the user's daily card or private meeting
notes. Define every non-obvious term used in the card.

Every important metric must state what question it answers, what failure mode
it catches, and what it cannot prove. Every central figure must have a nearby
one-sentence interpretation.

## Reference Delegation

If the handoff needs more than packaging, do not expand this skill. Load the
relevant `research-progress-core/references/` file instead:

- `profiling_and_evidence.md` when deciding which evidence is sufficient;
- `failure_decomposition.md` when the handoff must explain a bottleneck;
- `goal_audit.md` when the handoff explains a changed metric or goal.

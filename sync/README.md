# Root Sync

Root `sync/` is for compact current-state summaries that help a web-side
research partner understand the active research route without entering every
project folder.

It is not a raw-output dump and not a replacement for project-local sync
reports.

It is also not the same as syncing to a collaborator, advisor, or senior
student's external GitHub repo. External collaborator repo sync is an explicit
curated package copy into that repo's agreed destination folder.

## Current Root Sync

```text
S000_current_specialization/
```

This is the only default root sync entry. It summarizes the current
specialization mainline using curated evidence from:

```text
Projects/from-attention-to-search/XingyuD/sync/
Projects/from-attention-to-search/main/experiments/
```

Older root sync structures have been removed from the default reading path.
Historical project evidence should live in project-local `archive/` folders or
project-local sync reports.

## Anchor Copy Rule

Root sync is an explicit external-reading surface, not an automatic side effect
of every project-local anchor update. When the user explicitly asks to sync
root sync, mirror the active project anchor into root sync with an explicit
category:

```text
sync/<sync_id>/anchors/<category>/<anchor_id>.md
```

The project-local anchor is the source of truth; the root sync copy is the
web-side and cross-project reading copy. When root sync is requested, update
the sync copy in the same turn and verify that the source and copy are
identical.

## Sync Action Meanings

Use these as separate commands:

| User says | Action |
|---|---|
| sync root sync | update root `sync/` reading copies and indexes |
| sync to collaborator repo | copy a curated package into the external repo |
| package handoff | copy existing anchor / summary / detailed / 05_report_card / referenced figures and tables into a handoff folder |
| update graph | edit project `graph.yaml` after the research-state change is confirmed |
| push | commit or push only the explicitly requested repo/branch |

If the user only asks to update an experiment, update the project-local anchor,
`summary.md`, and `detailed.md`; do not touch root sync, handoff, graph, or
Git remotes.

## What The User Must Specify

Before a sync action, clarify these points when they are not already explicit:

```text
sync type: root sync / project sync / external collaborator repo
target path or repo branch, if external
date/topic package name
source anchor or experiment folder
include 05_report_card? yes/no
include protocol or execution_plan? yes/no
include figures/tables? only referenced / all curated
update graph? yes/no
commit or push? yes/no, and which repo/branch
```

If these are unclear, report the ambiguity first instead of guessing a broader
sync scope.

## Daily / Project Sync Package

The sync package should be the same shape whether it is copied into today's
daily folder, project-local sync, or an external collaborator repo:

```text
<anchor_id>.md
summary.md
detailed.md
05_report_card.md
figures/   # only referenced key figures
tables/    # only curated evidence tables
README.md  # short index
```

Do not create new conclusions during sync. Sync packages copy the current
research state; the anchor, `summary.md`, and `detailed.md` remain the source
documents.

Current categories:

| Category | Meaning |
|---|---|
| `expert_specialization/` | anchors about gating, route assignment, and expert causal utility |

## Add A Root Sync Only When

- it changes the current mainline question, claim boundary, or next decision;
- it is needed by a web-side partner that may not have project-local access;
- it compresses several project-local sync reports into one stable current
  state.

Do not add root sync folders for every experiment.

## Current Formal Project Evidence

The 2026-05-31 mechanism audit has been synced into root sync as the current
key experiment package:

```text
sync/S000_current_specialization/reports/0531_2x2_top1_router_lockin/
```

It contains the latest mechanism anchor, `summary.md`, `detailed.md`,
`05_report_card.md`, and only the key referenced figures/tables.

The current root anchor copies are numbered and live under:

```text
sync/S000_current_specialization/anchors/expert_specialization/
```

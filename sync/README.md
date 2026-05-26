# Root Sync

Root `sync/` is for compact current-state summaries that help a web-side
research partner understand the active research route without entering every
project folder.

It is not a raw-output dump and not a replacement for project-local sync
reports.

## Current Root Sync

```text
S000_current_specialization/
```

This is the only default root sync entry. It summarizes the current
specialization mainline using curated evidence from:

```text
Projects/from-attention-to-search/XingyuD/sync/
```

Older root sync structures have been removed from the default reading path.
Historical project evidence should live in project-local `archive/` folders or
project-local sync reports.

## Anchor Copy Rule

Every active project anchor must be mirrored into root sync with an explicit
category:

```text
sync/<sync_id>/anchors/<category>/<anchor_id>.md
```

The project-local anchor is the source of truth; the root sync copy is the
web-side and cross-project reading copy. When the source anchor changes, update
the sync copy in the same turn and verify that the source and copy are
identical.

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

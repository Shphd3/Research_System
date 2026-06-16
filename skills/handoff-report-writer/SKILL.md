---
name: handoff-report-writer
description: Use only when existing research artifacts must be packaged for a meeting, collaborator, web-side reader, or external repo sync after the anchor, protocol, summary, detailed result, and referenced figures/tables already exist.
metadata:
  short-description: Package existing research artifacts
---

# Handoff Package Writer

Use this skill only when the user explicitly asks for a meeting,
collaborator, web-side, or external repository handoff package.

Do not create new research claims, new conclusions, or a second closure. The
source of truth remains:

```text
anchor = current-state research design and claim boundary
protocol.md = approved experiment design
summary.md = first result reading path
detailed.md = full evidence ledger and visualization results
figures/ and tables/ = referenced evidence artifacts
```

## Package Contents

Include only the smallest curated set needed for the reader:

```text
<anchor_id>.md
protocol.md
summary.md
detailed.md
figures/      # only files embedded or directly referenced
tables/       # only files embedded or directly referenced
README.md     # short index and scope, when useful
```

Do not include:

```text
raw logs
checkpoints
datasets
full result directories
unfiltered generated figures/tables
caches
private meeting notes
unrelated anchors
code changes unless explicitly requested
```

## Handoff README

When adding an index, keep it short:

```markdown
# <Topic> Handoff

## Scope

## Source Files

- Anchor:
- Protocol:
- Summary:
- Detailed:
- Figures:
- Tables:

## Current Claim

## Claim Boundary

## Next Decision
```

The README should point to the existing artifacts. It should not reinterpret the
result beyond what the anchor, summary, and detailed documents already say.

## External Repo Sync

Before copying into an external repo:

1. Identify the target repo path and destination folder.
2. Check `git status --short --branch` in the target repo.
3. Do not overwrite dirty collaborator files without explicit approval.
4. Convert absolute local links into relative links.
5. Copy only the curated package.
6. Verify referenced figures/tables exist inside the copied package.
7. Show the inclusion/exclusion list before commit or push.

Commit and push only when the user explicitly asks.

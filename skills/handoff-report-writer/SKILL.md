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

## Minimal Self-Contained Rule

Every meeting brief, collaborator package, or web-side reading surface must be
minimally self-contained. Define local shorthand labels before using them as
evidence, including:

- metric or method labels such as `M1`, `M2`, or named ablations;
- condition or setting labels such as `C1`, `C2`, or dataset slices;
- model/router variants and negative controls;
- primary metrics whose names are not self-explanatory.

Keep the definitions short, but make the object concrete. A reader should be
able to understand the compared settings and the decision without chat history,
the protocol, or the full detailed report. Do not solve this by copying full
configs or timelines into the brief.

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

---
name: handoff-report-writer
description: Use only when existing research artifacts must be packaged for a meeting, collaborator, web-side reader, or external repo sync after the anchor, protocol, summary, detailed result, and referenced figures/tables already exist.
metadata:
  short-description: Package existing research artifacts
---

# Handoff Package Writer

Use this skill only when the user explicitly asks for a meeting,
collaborator, web-side, or external repository handoff package.

For group-meeting or advisor-facing briefs, the first goal is that the advisor
can quickly understand what problem is being solved. A meeting brief is not an
experiment retelling. It reports how the researcher's judgment changed, why
that update is supported, what boundary remains, and what decision is needed
next.

Do not create new research claims, new conclusions, or a second closure. The
source of truth remains:

```text
anchor = current-state research design and claim boundary
protocol.md = approved experiment design
summary.md = first result reading path
detailed.md = full evidence ledger and visualization results
figures/ and tables/ = referenced evidence artifacts
```

The brief may synthesize a higher-level cognitive update across several
existing summaries only when the synthesis is directly supported by those
sources. If the synthesis is not fully supported, write it as an unresolved
question or next decision, not as a claim.

## Meeting Brief Modes

Use one of two modes.

Mode A: cognitive-update brief.
Use when one anchor or one experiment line produced the main update.

Required order:

```text
problem being solved
old or uncertain judgment
updated judgment
2-4 key evidence items from summary.md
central figures, if they decide the claim boundary or next decision
can claim / cannot claim
meeting decision needed
source map
```

Mode B: merged brief.
Use when several days, anchors, or experiment summaries must be reported
together.

Do not concatenate old briefs. Merge by the main research question:

```text
shared problem
subquestions merged
single higher-level judgment update
evidence modules, one per source summary or anchor
cross-result interpretation
conflicts or remaining rival explanations
can claim / cannot claim
meeting decision needed
source map and excluded material
```

If the source briefs answer different parent questions, do not force one
merged claim. Split them into separate mainline updates and mark unrelated
results as parked or side evidence.

## Source Priority

Use sources in this order:

1. updated anchor for the current claim boundary and next decision;
2. `summary.md` for the meeting conclusion, key evidence, and central figures;
3. `detailed.md` for setup checks, numeric precision, and artifact maps;
4. protocol only to verify the approved question, conditions, and primary
   metric.

Do not use chat history as the source of a meeting claim. Do not pull debug
plots from `detailed.md` into the brief unless they directly decide the current
claim boundary or next decision.

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

For a private daily meeting folder, `meeting_brief.md` may point to existing
project artifacts instead of copying the full package. If the user asks for a
handoff package or external sync, copy only the curated files listed above.

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

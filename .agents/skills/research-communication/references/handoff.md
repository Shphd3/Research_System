# Handoff Mode

Use this mode only after an explicit user request to package, copy, hand off, or
synchronize an already approved set of research artifacts. It packages existing
meaning; it does not author meeting content, create a claim, or reinterpret a
result.

## Entry Gate

Confirm the destination, selected source scope, and requested action. When
meeting material is included, it must already contain the researcher-approved
question, answer, boundary, and next decision. If the user is still asking to
write or revise that material, use meeting mode first and do not package it yet.

Use source priority:

```text
completed meeting surface, when included
selected problem Focus
Anchor
Summary
Detailed
Protocol for contract verification only
```

Do not use chat or debug plots as evidence.

## Curated Contents

Include only requested and directly referenced items:

```text
meeting Focus or outline
selected problem Focus
Anchor
protocol.md
summary.md
detailed.md
referenced figures and tables
short README index when useful
```

Exclude raw logs, checkpoints, datasets, full result directories, caches,
private notes, unrelated Anchors, unfiltered figures, and code changes unless
the user explicitly requests them.

The optional README lists scope, source files, current claim, claim boundary,
and next action. It must not create a new synthesis.

## External Action

An external copy or sync requires an explicit user request. Resolve the exact
target repository and destination first. Check its Git status before copying.
Do not overwrite dirty collaborator files without explicit approval. Convert
local absolute links to package-relative links and verify that every referenced
figure and table is included.

Show the inclusion and exclusion set before a commit or push.
Commit and push only when the user explicitly asks.

## Validation

Verify that every packaged claim already exists in a canonical source, all
local links resolve inside the package, no excluded artifact entered the
destination, and the destination's pre-existing dirty changes remain untouched.

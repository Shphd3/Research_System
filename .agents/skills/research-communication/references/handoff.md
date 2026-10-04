# Handoff Mode

Use this mode after an explicit request to package, copy, hand off, or
synchronize selected research artifacts. It packages existing
meaning; it does not author meeting content, create a claim, or reinterpret a
result.

## Entry Gate

Resolve destination, source scope and action from the request; reuse confirmed
instructions. Preserve the sources' approval, draft and Unknown labels. A local
reading copy may include pending material without confirming it. If writing is
also requested, complete it through the owning mode before packaging. Ask only
when a consequential destination, scope or required scientific judgment is missing.

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
meeting brief or outline
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

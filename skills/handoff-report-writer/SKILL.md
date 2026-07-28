---
name: handoff-report-writer
description: Use only when existing research artifacts must be packaged for a meeting, collaborator, web-side reader, or external repo sync after the anchor, protocol, summary, detailed result, and referenced figures/tables already exist.
metadata:
  short-description: Package existing research artifacts
---

# Handoff Package Writer

Use this skill only when the user explicitly asks for a collaborator,
web-side, external repository, or already-written meeting-material handoff
package.

If the user asks to prepare, rewrite, or revise meeting material, use
`meeting-outline-writer` first. Return to this skill only if the user also asks
to package, copy, index, sync, commit, or push the human-completed material.

For group-meeting or advisor-facing handoff packages, the completed meeting
material must already follow `meeting-outline-writer`: a routine meeting uses
the day's `focus.md`, while a multi-focus meeting may use a separate outline.
It must contain the researcher's own answers or explanation. This skill only
packages existing material and source artifacts without changing the claim.

Do not create new research claims, new conclusions, or an independent
synthesis. The
source of truth remains:

```text
anchor = current-state research design and claim boundary
protocol.md = approved experiment design
summary.md = first result reading path
detailed.md = full evidence ledger and visualization results
figures/ and tables/ = referenced evidence artifacts
```

Separate meeting material may connect a higher-level update across several existing
summaries only when the synthesis is directly supported by those sources. If
the synthesis is not fully supported, write it as an unresolved boundary or an
execution action, not as a claim.

## Meeting Material Package Gate

Apply this gate before packaging meeting material. If the user is asking to
write or revise the material itself, stop using this skill and use
`meeting-outline-writer` instead.

- Read the completed daily `focus.md`; for a separately justified outline, also
  read `templates/meeting/meeting_outline_template.md`.
- Verify that every core question or topic contains the researcher's own answer
  or explanation rather than AI-completed prose.
- Verify that each empirical conclusion maps to an existing experiment or is
  explicitly marked as needing a new experiment.
- Verify that each completed result follows `question -> experiment -> result
  -> conclusion -> boundary -> next decision`.
- Keep the speaking path conclusion-first and free of stacked derivations,
  complete tables, run timelines, and unnecessary formulas.
- Preserve the advisor discussion point, live rival, cannot-claim boundary,
  and one candidate next action.
- Do not convert the outline into a polished full report during packaging.

For multi-topic material, retain the chosen question or topic order. Do not
concatenate historical briefs or reorganize topics around run
chronology.

## Source Priority

Use sources in this order:

1. completed daily `focus.md` or separate outline for the researcher's core
   question, knowledge update, mechanism, and next decision;
2. updated anchor for the current claim boundary and execution action;
3. `summary.md` for the meeting conclusion, key evidence, and central figures;
4. `detailed.md` for setup checks, numeric precision, and artifact maps;
5. protocol only to verify the approved question, conditions, and primary
   metric.

Do not use chat history as the source of a meeting claim. Do not pull debug
plots from `detailed.md` into the brief unless they directly support the
current result boundary or execution action.

## Minimal Self-Contained Rule

Every meeting focus/outline, collaborator package, or web-side reading surface must be
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

Use this minimum definition shape:

```text
术语：
中文含义：
具体对象或计算方式：
单位 / 公式，如果是指标：
为什么影响当前判断：
不能证明什么：
```

## Package Contents

Include only the smallest curated set needed for the reader:

```text
focus.md or <topic>_meeting_outline_cn.md  # existing human-completed meeting surface
<anchor_id>.md
protocol.md
summary.md
detailed.md
figures/      # only files embedded or directly referenced
tables/       # only files embedded or directly referenced
README.md     # short index and scope, when useful
```

For a private daily meeting folder, `meeting_outline_cn.md` may point to existing
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

## Next Action
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

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

If the user asks to write, rewrite, or revise `meeting_brief.md`, use
`meeting-brief-writer` first. Return to this skill only if the user also asks
to package, copy, index, sync, commit, or push the finalized material.

For group-meeting or advisor-facing handoff packages, the meeting brief itself
must already follow `meeting-brief-writer`. This skill only packages the
existing brief and its source artifacts without changing the claim.

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

The brief may synthesize a higher-level update across several existing
summaries only when the synthesis is directly supported by those sources. If
the synthesis is not fully supported, write it as an unresolved boundary or an
execution action, not as a claim.

## Meeting Brief Package Gate

Apply this gate before packaging any `meeting_brief.md`. If the user is asking
to write or revise the brief itself, stop using this skill and use
`meeting-brief-writer` instead.

- For any meeting package that includes a meeting brief, first read
  `templates/meeting/meeting_brief_template.md` and verify that the final brief
  contains only the required executive summary.
- Verify that the researcher's initial draft existed before AI revision. A
  handoff package must not turn an AI-generated first judgment into a human
  meeting claim.
- The executive summary must contain `研究问题`, `我的初始判断`, `本次结果`,
  `机制解释`, `决定性证据`, `结论边界`, `执行动作`, and `来源`.
- Write the brief in Chinese by default. Use English only for file names,
  paths, formulas, and abbreviations that have already been defined in Chinese.
- Use precise and concise language. Do not use English jargon as a substitute
  for explanation.
- Define non-obvious metrics, abbreviations, conditions, or project shorthand
  inline before using them as evidence; do not add a second report section.
- Write the brief as a reader-facing decision document. Lead with what is now
  established, what the evidence shows, and what action follows.
- Do not narrate discarded attempts, internal debugging history, or embarrassing
  caveats unless that history changes the advisor's decision. Put scientific
  boundaries in `结论边界`, not inside the headline claim.
- Do not use oral labels such as "30-second summary" in the document. The
  brief must be formally written but easy to present aloud.
- Make the question, mechanism, evidence, and result the grammatical subjects
  of the main sentences. Do not organize the brief around "we ran", "we did",
  "we tested", or similar activity-centered phrasing.
- The executive summary must contain the research question, mechanistic
  interpretation, main result, result boundary, and execution action.
- The mechanistic interpretation must include the minimal model, relation, or
  mechanism chain used to decompose the problem. If no model exists, state that
  the model is missing and do not invent one.
- The main result must start with one summary sentence, followed by at most
  three numbered result points.
- Each result point title must be a complete sentence understandable to a
  non-specialist undergraduate. It cannot be a noun phrase.
- Each result point must include mechanism alignment, evidence, explanation,
  boundary, and source.
- Each result point must define the metric, condition, or shorthand needed to
  understand the evidence before using it as proof.
- Do not write discussion-point sections or advisor-question lists. Put the
  next minimal step under `执行动作` with purpose and completion criterion.

## Meeting Brief Modes

Use one of two modes.

Mode A: single research-line brief.
Use when one anchor or one experiment line produced the main update.

Required order:

```text
executive summary
mechanistic interpretation and minimal model
main result: one sentence plus up to three result points
execution action: next step, purpose, completion criterion
evidence index
source index
backup material
```

Mode B: multi-source brief.
Use when several days, anchors, or experiment summaries must be reported
together.

Do not concatenate old briefs. Merge by the main research question:

```text
executive summary for the shared problem
shared mechanism or model
merged main result: one sentence plus up to three result points
source result modules
remaining conflicts or rival explanations
execution action
evidence index and source index
excluded material and reason
```

If the source briefs answer different parent questions, do not force one
merged result. Split them into separate mainline updates and mark unrelated
results as parked or side evidence.

## Source Priority

Use sources in this order:

1. updated anchor for the current claim boundary and execution action;
2. `summary.md` for the meeting conclusion, key evidence, and central figures;
3. `detailed.md` for setup checks, numeric precision, and artifact maps;
4. protocol only to verify the approved question, conditions, and primary
   metric.

Do not use chat history as the source of a meeting claim. Do not pull debug
plots from `detailed.md` into the brief unless they directly support the
current result boundary or execution action.

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

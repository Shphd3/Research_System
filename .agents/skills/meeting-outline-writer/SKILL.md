---
name: meeting-outline-writer
description: "Use when the user asks to prepare or audit an advisor meeting, group-meeting focus, meeting brief, speaking flow, or multi-problem discussion plan. Do not use for handoff packaging, publication, or sync."
---

# Meeting Focus Writer

A meeting focus is an optional concise knowledge update, not the default
meeting-cycle task card, an experiment correction, result audit, or Protocol
recap. Ordinary one-problem cycles use their active `focus_<problem>.md`
directly. Use this skill only when the researcher explicitly requests a meeting
brief, speaking preparation, or synthesis; then organize it as a progressive
question chain so each answer creates the need for the next question.

For that explicit request, create a new artifact:

```text
daily_research_reports/MMDD/focus_meeting_<topic>.md
```

Use `templates/meeting/meeting_focus_template.md`. Do not overwrite a source
`focus_<problem>.md`.

## Choose The Scope Path

### One-problem meeting

Use the lightweight path when the user explicitly asks for a brief and names
one active problem Focus, note, or problem plus the meeting's core question.
Do not add an
`AWAITING_HUMAN_SCOPE` scaffold or demand a merge ledger.

If the user asks AI to draft the knowledge wording, use status
`AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`. Use `HUMAN_CONFIRMED` only after the
researcher explicitly approves or corrects that wording.

### Multi-problem meeting

When two or more independent problem updates are being combined, first require:

```text
one core question
exact source focus paths
explicit exclusions
one advisor decision, when needed
```

Until those fields are supplied, create only the scaffold with status
`AWAITING_HUMAN_SCOPE`. Do not infer the merge range from recency, chat,
`PROJECTS.md`, or semantic similarity. After the gate, use the same concise
output shape as the one-problem path; list sources compactly instead of adding
a mandatory merge table.

## Output Contract

### Completed Single-Experiment Brief

When the researcher asks for a meeting-ready report of one completed
experiment, use the project's completed-experiment reply format instead of the
generic progressive-question layout below:

1. audit the completed comparison set and the actual single-stage or staged
   training schedule, including optimizer-update counts and the stage handoff;
2. write Purpose in one sentence;
3. write one or two short Hypotheses;
4. write at most three Analysis-method bullets;
5. write numbered Conclusions, each immediately followed by one eligible
   decision-bearing figure and one plain `How to read` sentence.

For Router or MoE work, explicitly separate semantic dispatch, intervention-
measured expert utility, end-task performance, and representation evidence.
Keep the status `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION` until the researcher
confirms the result wording. Preserve exactly one next decision and its
completion criterion after the four-section report.

Use the generic contract below for other one-problem knowledge syntheses and
human-scoped multi-problem meetings.

Use these sections in order:

```text
1. meeting theme and one core question
2. current knowledge update in connected natural sentences
3. a progressive question chain with two to four necessary steps
4. claim boundary and exactly one next decision
```

For each step in the question chain, write:

```text
question
direct answer
minimum decisive evidence
how far that answer reaches
why the next question is now necessary
```

Later questions must depend on earlier answers. Do not organize by run order or
document order. Delete any step that does not change the final boundary or next
decision.

The final section includes the exactly one next decision, its completion
criterion, and the first resume action. Add one advisor ruling only when the
user requests it or the decision genuinely requires it.

## Knowledge-Update Rule

The opening wording states what is now understood without relying on run IDs,
metric names, pass/fail labels, or protocol details. Results come afterwards
and explain the update; they do not replace it.

If the evidence is negative or insufficient, explain which interpretation it
removes or why the question remains open. Do not frame the meeting around
debugging an experiment unless debugging itself is the user-selected research
question.

Never create a joint judgment that no selected source owns. Preserve a source
conflict instead of smoothing it over. If AI drafts wording beyond an already
approved problem update, keep the draft status visible.

## Evidence Rule

Use the fewest results needed to make each answer intelligible. Define a
non-obvious metric in plain language before its value. Keep formulas, full
tables, run histories, guard ledgers, and configurations in their owning
artifacts.

A figure, compact table, or flowchart is optional. Include it only when it
materially improves the reader's understanding of a decisive relation. Do not
require a merge table, evidence ledger, or flowchart merely to fill a template.

Each empirical statement still preserves:

```text
direct result
allowed inference
cannot-claim boundary
source link
```

## Source Order

Do not use chat as evidence. Read only:

```text
explicit meeting scope
-> named note or focus_<problem>.md
-> linked anchor and summary.md
-> detailed.md only for numeric or provenance verification
```

For a one-problem brief, the active Focus and its linked sources are enough when
they answer the core question. For a multi-problem meeting, include only the
human-selected sources.

## Optional Speaking Outline

Create a separate speaking outline from
`templates/meeting/meeting_outline_template.md` only when explicitly requested
after the meeting focus is complete. It may change presentation order but must
not rewrite the knowledge update or become a second evidence record.

## Common Mistakes

| Wrong shape | Correction |
| --- | --- |
| experiment verdicts lead the document | lead with the knowledge update |
| every ordinary cycle creates another meeting focus | use the active core-task Focus unless a separate brief was explicitly requested |
| sources are copied into a large audit table | link them and keep only decision evidence |
| questions are parallel topics | make each answer motivate the next question |
| a figure and flowchart are always present | include visuals only when they clarify a decisive relation |
| representation evidence becomes Router function | state the functional gap explicitly |

## Validation

1. The user explicitly requested a meeting brief or synthesis; a new
   `focus_meeting_<topic>.md` exists and source Focus files are unchanged.
2. The artifact uses the one-problem or multi-problem scope path correctly.
3. The opening is a knowledge update, not an experiment-result analysis.
4. Two to four questions form one progressive reasoning chain.
5. Each answer gives only its minimum evidence and explicit reach.
6. Direct result, interpretation, and cannot-claim boundary remain distinct.
7. No mandatory merge table, audit ledger, flowchart, or speaking script bloats the focus.
8. The document ends with exactly one decision, completion criterion, and resume action.
9. `HUMAN_CONFIRMED` appears only after explicit researcher approval.

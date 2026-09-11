# Meeting Mode

Use this mode only when the researcher explicitly requests a meeting brief,
speaking preparation, or multi-problem synthesis. An ordinary one-problem cycle
uses its active `focus_<problem>.md` directly.

## Output

Create:

```text
daily_research_reports/MMDD/focus_meeting_<topic>.md
```

Compose the meeting brief directly from the named Focus and the four-part
Summary; there is no meeting template. Never overwrite a source Focus. When a
speaking order is explicitly requested, add it in the same document after the
brief is complete rather than opening a second template.

## Scope

For one problem, use the named Focus or source and the meeting's core question.
Do not create an `AWAITING_HUMAN_SCOPE` scaffold.

For two or more independent problems, require one core question, exact source
Focus paths, explicit exclusions, and the advisor decision when one is needed.
Until supplied, the only permitted scaffold status is `AWAITING_HUMAN_SCOPE`.
Do not infer the merge range from recency, `PROJECTS.md`, chat, or similarity.

AI-drafted knowledge wording remains
`AI_DRAFT_AWAITING_HUMAN_CONFIRMATION` until the researcher approves or corrects
it.

## Completed Single Experiment

First audit the completed comparisons and whether training was staged. For each
stage state the trainable and frozen objects, data passes, actual optimizer
updates, batch and accumulation, objective, learning rates, checkpoint rule,
and handoff.

Then use exactly four sections:

1. **Purpose:** one plain sentence.
2. **Hypothesis:** one or two short falsifiable statements.
3. **Analysis method:** at most three bullets; each states the comparison and
   uncertainty resolved.
4. **Conclusion:** one numbered item per decision-bearing answer, with the
   smallest decisive value, boundary, one eligible supporting figure when one
   exists, and one sentence explaining how to read it.

Keep exactly one next decision and its completion condition. For Router or MoE
work, separate semantic dispatch, intervention-measured expert utility,
end-task performance, and representation evidence.

## Other Meeting Syntheses

Use this order:

```text
meeting theme and one core question
current knowledge update
two to four progressive questions
claim boundary and exactly one next decision
```

For each progressive question give its direct answer, minimum decisive evidence,
reach, and why the next question is necessary. Delete a question that does not
change the final boundary or decision.

## Sources And Validation

Read the explicit scope, then the named Focus, linked Anchor and Summary, and
Detailed only when a number or provenance needs verification. Use the fewest
results needed. Preserve source conflicts rather than smoothing them over.

Before delivery verify that the request was explicit, source Focus files remain
unchanged, direct result and interpretation are separate, the question chain is
progressive, and the document ends with one decision, completion criterion, and
resume action.

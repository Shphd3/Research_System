---
name: meeting-outline-writer
description: Build a human-completed advisor-meeting outline from existing research artifacts. Use when preparing a meeting brief, meeting structure, speaking outline, or advisor discussion; AI supplies prompts and experiment-to-conclusion mappings but does not write the researcher's full explanation.
metadata:
  short-description: Prepare human-owned meeting outlines
---

# Meeting Outline Writer

The default routine speaking artifact is the day's completed `focus.md`: a
self-contained research briefing with a bounded knowledge update, mechanism,
flowchart, experiment structure, and next decision. It is not an AI-written
conclusion.

## Default Boundary

When the meeting covers one daily research center, revise
`daily_research_reports/MMDD/focus.md` in place. Do not create a second file
that duplicates its questions, answers, or evidence mapping.

Create a separate meeting outline only when the meeting combines several daily
foci or research lines, or the user explicitly requests one. Do not directly
generate a finished brief.

When a separate outline is justified, use this template exactly:

```text
templates/meeting/meeting_outline_template.md
```

Separate-outline output:

```text
daily_research_reports/MMDD/meetings/<topic>_meeting_outline_cn.md
```

The completed outline is normally the speaking surface. Create a separate
final brief only when the researcher has filled every topic in their own words
and explicitly requests a separate final document.

## Human Ownership Gate

AI may fill:

- an explanation flowchart drafted from the human conclusion and mechanism;
- plain-language experiment structure and verified direct measurements;
- meeting decision and topic order proposed from current sources;
- short speaking prompts for each topic;
- unclear definitions, hidden assumptions, and live rivals to address;
- existing experiment or figure that can explain each conclusion;
- the allowed claim and limitation of that experiment;
- a missing-experiment prompt when no existing result can support the point;
- transition prompts and an evidence-boundary audit.

AI must leave the conclusion, mechanism judgment, and `我的讲解（研究者填写）`
for the researcher. It must
not fill that field from chat history, infer the researcher's voice, or turn
bullet prompts into polished speech before the researcher drafts it.

After the researcher fills the outline, AI may:

- check whether the explanation is coherent and understandable;
- verify numbers, metrics, and source links;
- identify a conclusion that lacks an experiment;
- identify an experiment that does not support the nearby conclusion;
- remove unnecessary formulas and implementation detail;
- lightly edit wording without replacing the researcher's mechanism judgment.

## Source Order

Do not use chat as evidence. Read only the sources required for the requested
meeting topics:

```text
PROJECTS.md -> today's focus.md -> relevant anchor -> summary.md -> detailed.md
```

Use `focus.md` for the researcher's core question, bounded knowledge update,
mechanism, and next decision; use the anchor for the canonical claim boundary,
`summary.md` for the result conclusion and central evidence, and `detailed.md`
only to verify numbers, setup, or artifact links. Meeting material links these
sources rather than copying derivations or tables.

## Topic Construction

Every topic must do one distinct job in the advisor discussion:

```text
topic decision
one-sentence conclusion
AI speaking prompts
researcher-owned explanation
conclusion-to-experiment mapping
result closure, if evidence exists
source
```

Do not organize topics by experiment chronology. Organize them by the
reasoning chain needed for the advisor to challenge the current judgment.
Delete a topic if it does not change the meeting decision or prepare a
necessary transition.

## Conclusion-To-Experiment Mapping

For every conclusion, state one of:

```text
supported by an existing experiment
needs a new experiment
is a framing statement and needs no experiment
```

When an existing experiment is used, name:

```text
experiment or figure
decisive contrast
direct result
allowed conclusion
cannot-claim boundary
```

When a new experiment is needed, propose only:

```text
rival explanations to separate
smallest experiment
primary metric
result that would change the conclusion
```

This is an experiment prompt, not an approved Protocol. Do not expand it into
conditions, seeds, implementation, or a sweep unless the user separately asks
for a Protocol.

## Result Closure Rule

Present each completed experiment as one conclusion-bearing loop:

```text
question -> decisive experiment -> direct result -> conclusion
-> cannot-claim boundary -> next decision
```

Use the fewest numbers needed to establish the direction and decision. Do not
stack mathematical derivations, complete tables, run timelines, or multiple
metrics in the speaking path. Include a formula only when the advisor cannot
understand the decision without it; otherwise link the source artifact.

Negative and insufficient results are complete loops when they eliminate an
explanation or reveal that the experiment cannot adjudicate the claim.

## AI Audit Output

After the human draft, keep the audit short:

```text
unclear object
conclusion without adequate evidence
experiment with an overclaimed interpretation
topic without a closed loop
detail or formula to remove
```

Do not rewrite a full finished brief unless explicitly requested after this
audit.

## Validation

1. The artifact is an outline, not AI-completed prose.
2. Every topic has one decision role and one human-owned explanation field.
3. Every empirical conclusion maps to an existing or explicitly missing
   experiment.
4. Every completed result follows the conclusion loop.
5. Evidence and interpretation are distinguishable.
6. The strongest live rival and cannot-claim boundary are visible.
7. Formulas and implementation details are absent unless indispensable.
8. The outline ends with one advisor discussion point and one candidate next
   action.

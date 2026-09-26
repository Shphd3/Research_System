---
name: research-sync-gate
description: "Audit advisor/group discussion readiness or one next research question: evidence, rival and decision. Does not automatically create a Focus or authorize experiments."
---

# Research Sync Gate

Audit the researcher's judgment before polishing it. A meeting does not require
a new two-day task or Focus.

## Input And Scope

Start with the named account/result and relevant existing Focus; follow
Anchor/Summary links needed for disputed claims. Use `PROJECTS.md` only to
select a workstream. Chat is context, not evidence.

Default to an audit. Create/reset a Focus only when the researcher requests
that transition, activates the independent question and confirms its stable
`problem_key` and next decision. Then use `research-progress-core` and
`templates/research_process/focus_writing_template.md`, not another schema.
Existing confirmed choices need no repeat approval. Missing judgment stays
unknown; label candidate wording `AI 建议` and request only decisive missing input.

## Reasoning Check

Before execution, check the plain-language Purpose, Hypothesis, Analysis method
and Conclusion branches:

```text
question -> uncertainty -> hypothesis versus strongest rival
-> separating measurement/intervention
-> supporting / non-supporting / insufficient outcomes
-> decision changed by each outcome
```

After execution: eligible comparison -> direct result -> bounded update ->
remaining rival / cannot-claim boundary -> researcher-owned next decision.
Check object, data unit, observation position, metric and completion rule only
where they affect this chain. Define essential terms in plain Chinese. For a
causal/proxy confusion use `research-reasoning-auditor` before rewriting.

One Focus permits at most three necessary experiments for one question; controls
are not separate questions. Other authorized workstreams may coexist. Flag
mixed questions here, but never automatically park, reset or replace another
workstream. Narrowing a meeting or proposing reopening conditions is an AI
proposal. If the design changes materially, preserve the confirmed question
and flag the changed design as awaiting judgment; do not silently transfer old
confirmation or mutate scientific state during an audit.

## Output And Completion

Return `READY_FOR_SYNC`, `READY_FOR_PROTOCOL`, `NEEDS_HUMAN_JUDGMENT` or
`NOT_READY_OBJECT_OR_LOGIC`, the smallest material gap if any, and a concrete
revision/evidence link. This is readiness assessment, not scientific approval.
Finish with a traceable boundary and next decision, or identify the exact
missing judgment/evidence. A narrow audit requires no persistent artifact.

Use the existing Focus for ordinary meetings; `research-communication` owns
requested briefs/outlines or multi-question synthesis. After design confirmation,
`experiment-card-writer` owns a requested Protocol. This skill neither writes
Protocols nor runs experiments.

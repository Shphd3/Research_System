# Research Thinking Explanation Mode

Use this mode when the user wants to understand the research idea, mechanism,
evidence chain, unresolved uncertainty, or possible next directions behind a
document.

## Reconstruct The Research Logic

Use this dependency order:

```text
umbrella problem
-> local decision question
-> source or human judgment
-> proposed mechanism or physical prior
-> strongest rival explanation
-> evidence that distinguishes them
-> current claim boundary
-> one next decision
```

State where the document enters this chain and which links it does not own. A
Protocol owns a test contract, not the researcher's root judgment. A result
record owns evidence, not an automatically strengthened conclusion. An
AI-written draft does not become human judgment because it is coherent.

## Explain The Mechanism

Name the entities, direction of influence, intermediate link, and observable
prediction. Separate:

- a semantic association from a causal mechanism;
- readability from spectral or geometric localization;
- localization from functional or causal use;
- a proxy improvement from the final decision objective.

Use the strongest clear version of the source idea, then show exactly where a
rival can still produce the same observation.

## Suggest Research Directions

When requested, offer at most three directions labeled `AI 建议` (internal
state `AI_PROPOSAL`) and recommend one.
For each direction state:

```text
what uncertainty it reduces
why existing evidence cannot answer it
minimal falsifier or proof obligation
effect on hypothesis: yes / no / unclear
effect on claim boundary: yes / no / unclear
effect on next decision: yes / no / unclear
completion condition
```

A direction is worth pursuing only when it changes a hypothesis, boundary, or
decision. Keep minor diagnostics and implementation chores out of the research
idea list. Respect the one active core task; a useful non-active direction is
not automatically the next experiment.

## Close The Explanation

End by separating:

```text
what the source establishes
what the explanation clarifies
what remains unknown
one recommended AI proposal, when requested
what still requires human judgment
```

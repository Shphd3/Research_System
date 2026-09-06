# Story Mode

Use this mode for an explicitly requested research-line story or paper-like
stage synthesis. A story presents the line-level argument; it never replaces an
Anchor, Protocol, Summary, Detailed record, or ordinary meeting Focus.

## Sources

Read the named line README and current story first. Follow only the links needed
to the relevant Anchors and result records. Read Detailed only to verify a
decision-bearing number or provenance. Do not load every project artifact or
use chat as the source of truth.

## Placement

Use:

```text
Projects/<project>/main/stories/<line_id>/README.md
Projects/<project>/main/stories/<line_id>/<NN>_<topic>.md
Projects/<project>/main/stories/<line_id>/<NN>_<topic>_cn.md
```

The two-digit number gives reading order and the topic names the subject. The
line README orders story pairs and marks one current primary synthesis. Do not
create generic `story.md`, one full story per Anchor, or a routine competing
`final_report.md`.

Formal stories are bilingual unless the user chooses otherwise. English is
canonical and the Chinese companion uses the same stem plus `_cn.md`. They must
agree on theorem state, evidence, boundary, and next decision.

## Modes And Structure

Use prospective mode for a new line, retrospective mode when results exist, and
synthesis mode for a stable stage. Scale the sections to the evidence, but keep
this dependency order:

```text
title and status
terminology and abstract
research question and source of confusion
data or training layout
physical intuition and definitions
mathematical and theorem state
mechanism decomposition
Anchor and experiment evidence
counterexamples and rivals
claim boundary
next Anchor decomposition and one next decision
source map
```

Put the data and training layout before theorem claims. State theorem
assumptions and limitations. Distinguish proved statements, assumptions, and
empirical propositions. If evidence is insufficient, keep it insufficient.

## Validation

Verify that the story is self-contained, all terms and metrics precede their
use, evidence links to canonical sources, claims do not exceed those sources,
English and Chinese companions agree when both are required, and the final
decision is singular and actionable. Mention downstream artifacts that may
need synchronization, but do not edit Graph, root Sync, commit, or push without
an explicit request.

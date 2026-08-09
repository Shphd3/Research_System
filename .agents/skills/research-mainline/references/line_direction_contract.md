# Research-Line Direction Contract

Use this contract when creating, reorganizing, or auditing
`main/problem_anchors/<line_id>/README.md`.

## Contents

1. [Purpose and boundary](#purpose-and-boundary)
2. [Direction snapshot](#direction-snapshot)
3. [Parent-anchor map](#parent-anchor-map)
4. [Grounding and no-invention](#grounding-and-no-invention)
5. [Reading index](#reading-index)
6. [Final audit](#final-audit)

## Purpose And Boundary

The line README answers:

```text
What broad question organizes this line?
What is currently established?
What remains the one blocking uncertainty?
How do sibling parent Anchors divide the problem?
Why is the active Anchor next?
What result would stop, redirect, or continue the route?
```

It is a direction map, not a full synthesis or evidence ledger. The Story owns
paper-like line synthesis; Anchors own local research designs; Summary and
Detailed own results. The README links these artifacts without copying them.

## Direction Snapshot

Put this short block before the artifact index:

```text
Root research question:
Current answer:
Current claim boundary:
One blocking uncertainty:
Active parent Anchor:
Why this Anchor is next:
Decision dependency chain:
Parked directions and reopening conditions:
Exactly one next decision:
Completion criterion:
Resume action:
```

Write the `Current answer` as a bounded knowledge state, not a chronology of
runs. The dependency chain must explain decision logic rather than merely list
Anchor IDs.

## Parent-Anchor Map

Use one row per sibling parent:

| Parent Anchor | Decision it owns | Depends on | Current state | Direction implication | Primary source |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Two parents remain siblings when one must be read or decided before another.
Use a subanchor only when it inherits one parent's decision question and tests
a local clause, rival, repair, robustness condition, or metric guard.

Do not encode a broad roadmap as a deep subanchor tree.

## Grounding And No-Invention

Derive every current-state sentence from approved Anchors and verified result
records. Before a link, state the local question, result, boundary, or route
implication that the link audits.

Do not invent:

- a dependency because two Anchors share a topic;
- a completed result from a Protocol, plan, folder name, or missing Summary;
- a current verdict by merging incompatible Anchor boundaries;
- an active route or next decision absent researcher approval;
- a reopened direction without its registered reopening condition.

When the line state is unsettled, write:

```text
Status: Unknown | Disputed | BLOCKED
What is missing or conflicting:
Why it changes the route:
Direct sources:
Decision needed:
```

Preserve disagreement between sources instead of smoothing it into one story.

## Reading Index

Group the index by sibling parent Anchor. Within each group, prefer:

```text
parent Anchor
-> active subanchor, when any
-> Protocol only when needed for the current decision
-> Summary as the first result path
-> Detailed only for audit
```

Do not maintain one flat chronological list when the research line contains
multiple parents. Remove duplicate descriptions, superseded run narration, and
links that do not help reconstruct the direction. Link the current primary
Story once for full synthesis.

## Final Audit

Mark each item `PASS` or `FAIL`:

```text
The root question and current bounded answer are explicit:
One blocking uncertainty and one next decision are explicit:
The active parent and why it is next are understandable without IDs:
Sibling dependency and parent-child ownership are not conflated:
Each status and route implication has a direct approved source:
Unknown, disputed, and blocked states remain visible:
The index is grouped by decision ownership rather than chronology:
The README does not duplicate the Story, Anchor, or result ledger:
```

Any `FAIL` means the line is navigable only by private context and must be
reorganized before publication or handoff.

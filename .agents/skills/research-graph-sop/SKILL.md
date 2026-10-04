---
name: research-graph-sop
description: "Inspect or maintain a research graph when the user asks for graph work. Not automatic context refresh, hypothesis development or result interpretation."
---

# Research Graph

Keep the graph a small navigation map. Scientific judgments and evidence remain
in their owning Focus, Anchor, Protocol and result records; a tidy graph cannot
confirm a claim or choose a research direction.

## Choose the requested operation

- **Inspect:** read the named graph and only the sources needed to check its
  claims, links or relationships. Report discrepancies; inspection does not
  authorize edits. If no graph exists, report that fact instead of creating one.
- **Create or edit:** proceed within the user's current or earlier explicit scope.
  Reuse that authorization. If a proposed change needs a new scientific judgment,
  leave it unresolved and ask only for that missing decision. Finish independent
  authorized link or structure repairs without repeating approval.
- **Schema validation or editing:** read the [format contract](references/graph_format.md)
  for node/edge vocabulary and YAML fields. A source-consistency explanation
  does not need the whole schema or a viewer.

Opening a repository, receiving a hypothesis or completing an experiment does
not itself request graph work. If only a report changed and the research route
did not, no graph update is needed.

## Keep sources and graph consistent

Represent the confirmed source question, claim, evidence relation and boundary.
Flag an unsupported edge instead of changing the scientific interpretation to
fit it. Distinguish question hierarchy, logical dependence and shared evidence.
A graph edge is not evidence by itself.

Use the smallest set of nodes that need navigation, reuse or tracking. Keep long
reasoning, quotations, round histories and drafts in Markdown. Link existing
notes; do not create a document for every node or invent future questions.

New proposed nodes remain `draft` unless an owning source establishes another
state. `active`, `blocked` and `done` follow their source meanings; a completed
task does not close a scientific question. Preserve source uncertainty.

## Complete the requested work

For inspection, give the supported finding and any unavailable source. For edits,
verify the requested relationships, valid ids/types, links and unchanged scientific
meaning. Report changed nodes/edges, relevant source links and remaining gaps.
Missing links in a draft must be intentional and named. Do not launch a service,
publish, or modify other research artifacts merely to complete graph maintenance.

# Root Sync

Root `sync/` is a compact navigation surface. The 2026-09-03 generated copies
were retired on 2026-09-24 because they duplicated project records and carried
stale state. Current scientific state is in `PROJECTS.md`, the owning Focus,
Anchor, and result records. A reader needs the project checkout for those links.

Root sync is not:

- a raw-output dump;
- a mirror of every project anchor;
- a replacement for project-local anchors, protocols, summaries, or detailed
  records;
- a collaborator-repo sync package.

## Current Entry

```text
sync/S000_current_specialization/
```

This entry summarizes the active feature-level expert-specialization line.
Read it in this order:

```text
sync/S000_current_specialization/README.md
sync/S000_current_specialization/anchor_index.md
sync/S000_current_specialization/protocol_index.md
sync/S000_current_specialization/result_index.md
```

## Source Of Truth

Project-local files remain the source of truth:

```text
Projects/from-attention-to-search/main/problem_anchors/
Projects/from-attention-to-search/main/experiments/
Projects/from-attention-to-search/main/roadmap.md
Projects/graphs/
```

Root sync links to those files without copying their bodies. A separately
requested external package may still be curated for a specific reader.

## Update Rule

Update root sync only when the user explicitly requests publication or a
web-side research-line summary. A mainline state change may make the current
view stale, but does not itself authorize publication.

A mainline state change means a change to the current decision question,
active ladder level, route, evidence boundary, claim boundary, next decision,
or web-side source links. When updating root sync:

1. State the research line and claim boundary.
2. Link the source anchors and experiment summaries.
3. Keep the synthetic-versus-real-data boundary explicit.
4. Do not create stronger claims than the source anchors allow.
5. Verify linked source files exist before committing.

Root sync remains a compact reading surface. It must not mirror raw outputs,
checkpoints, receipts, unfiltered logs, or unrelated project material.

## External Sync Is Different

Syncing to a collaborator, advisor, or senior student's repository is a
separate explicit action. It copies a curated package into that external repo.
Root `sync/` does not perform that action by itself.

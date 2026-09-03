# Root Sync

Root `sync/` is the compact external-reading surface for the research system.
It is written for a web-side research partner or cross-project reader who
should understand the current research line without scanning project folders.

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
sync/S000_current_specialization/stories/README.md
sync/S000_current_specialization/protocol_index.md
sync/S000_current_specialization/result_index.md
sync/S000_current_specialization/research_lines/00_overall_current_line_cn.md
sync/S000_current_specialization/research_lines/05_failure_mechanism_line_cn.md
sync/S000_current_specialization/research_lines/06_proxy_preservation_line_cn.md
sync/S000_current_specialization/research_lines/07_interference_value_line_cn.md
```

## Source Of Truth

Project-local files remain the source of truth:

```text
Projects/from-attention-to-search/main/problem_anchors/
Projects/from-attention-to-search/main/experiments/
Projects/from-attention-to-search/main/roadmap.md
Projects/graphs/
```

Root sync compresses the current logic and links to those files. A user-requested
curated result package may include canonical Summary/Detailed records and their
decision-bearing figures, but never raw runs, checkpoints, receipts, or
unfiltered logs.

The explicitly published `anchors/`, `stories/`, and `protocols/` trees are
small Markdown mirrors for external reading. The optional `results/` tree is a
curated copy of explicitly requested result records and figures. All generated
mirrors remain secondary to the project-local source.

## Update Rule

For the active specialization line named in `PROJECTS.md`, update root sync
whenever a mainline state change is accepted in `PROJECTS.md`, or when the user
explicitly asks for root sync or a web-side research-line summary.

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

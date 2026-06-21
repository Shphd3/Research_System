# Research Loop Folder Template

Use this shape for a small mainline experiment or daily sandbox.

```text
00_handwrite_anchor.md
<topic>_anchor.md
protocol.md
summary.md
detailed.md
figures/
tables/
notes/
archive/
```

## File Roles

`00_handwrite_anchor.md`: rough user judgment for AI audit, not a polished
anchor.

`<topic>_anchor.md`: compact current-state design. First reading surface is
`Tiny Summary` plus `Minimal Replay`; sections 1-8 are the audit layer.

`protocol.md`: experiment approval surface. Page 1 is `Approval Snapshot`;
later sections hold anchor alignment, conditions, profiling, and nontrivial
algorithm details.

`summary.md`: first post-run reading path. Include only the conclusion,
primary metric, claim boundary, next decision, and central figures needed for
that judgment.

`detailed.md`: complete evidence ledger with protocol audit, setup, full
results, stage evidence, failure decomposition, debug-only evidence, and
artifact map.

`figures/`: report-ready evidence figures embedded in `summary.md` and
`detailed.md`. Debug-only plots stay in `detailed.md` or a viewer appendix.

`tables/`: curated small tables used by result documents.

`notes/`: scratch material outside the main read path.

`archive/`: superseded probes kept for traceability.

Do not create separate implementation-plan files for new work.

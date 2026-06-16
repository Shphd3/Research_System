# Research Loop Folder Template

Use this folder shape for a daily sandbox or a small mainline experiment.

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

`00_handwrite_anchor.md`: rough user judgment. This is the thinking surface
before AI critique. It may be incomplete.

`<topic>_anchor.md`: formal anchor and current-state research design. It is the
project-local equivalent of research-exploration `docs/design.md`.

`protocol.md`: experiment design and approval surface. It replaces the old
two-file split between approval notes and implementation details. The AI stops
here until the user approves implementation or running.

`summary.md`: first post-run reading path. It must include central
visualization-result explanations for the main figures.

`detailed.md`: complete evidence ledger, protocol compliance audit,
stage-level evidence, full visualization results, and artifact map.

`figures/`: report-ready central figures embedded and explained in
`summary.md` and `detailed.md`.

`tables/`: curated small tables used by the result documents.

`notes/`: private scratch notes that are not part of the main read path.

`archive/`: old probes or superseded proxies kept for traceability, not for the
main read path.

Do not create separate implementation-plan files for new work. Legacy files may
remain in old folders as historical evidence.
